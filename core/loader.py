"""Discovers and loads extension modules under `extensions/`."""

from __future__ import annotations

import importlib
import logging
from dataclasses import dataclass
from pathlib import Path

from contracts.errors import PluginLoadError
from core.registry import HookRegistry
from core.context import HostContext
from utils.config_loader import HostConfig
from utils.manifest_io import read_manifest

log = logging.getLogger("ad_banner.loader")


@dataclass(frozen=True)
class LoadedPlugin:
    name: str
    version: str
    module: str
    hooks: list[str]


class PluginLoader:
    """Loads plugins in the order declared in `[enabled].plugins`."""

    def __init__(self, ctx: HostContext, registry: HookRegistry, config: HostConfig) -> None:
        self._ctx = ctx
        self._registry = registry
        self._config = config

    def load_all(self) -> list[LoadedPlugin]:
        loaded: list[LoadedPlugin] = []
        for short_name in self._config.enabled_plugins:
            try:
                loaded.append(self._load_one(short_name))
            except PluginLoadError:
                log.exception("plugin %s failed to load; continuing", short_name)
        return loaded

    def _load_one(self, short_name: str) -> LoadedPlugin:
        pkg_path = Path(self._ctx.repo_root) / "extensions" / short_name
        manifest = read_manifest(pkg_path / "manifest.toml")
        module_name = f"extensions.{short_name}.plugin"

        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 — surfaced as PluginLoadError
            raise PluginLoadError(f"import failed for {module_name}: {exc}") from exc

        register = getattr(module, "register", None)
        if not callable(register):
            raise PluginLoadError(f"{module_name} has no callable register()")

        bound_registry = _OwningRegistry(self._registry, owner=manifest.name)
        try:
            register(bound_registry)
        except Exception as exc:  # noqa: BLE001
            raise PluginLoadError(f"register() raised for {manifest.name}: {exc}") from exc

        return LoadedPlugin(
            name=manifest.name,
            version=manifest.version,
            module=module_name,
            hooks=list(manifest.hooks),
        )


class _OwningRegistry:
    """Wraps HookRegistry so plugin registrations are attributed to their owner."""

    def __init__(self, inner: HookRegistry, owner: str) -> None:
        self._inner = inner
        self._owner = owner

    def add_copy_provider(self, name: str, fn: object) -> None:
        self._inner.add_copy_provider(name, fn, owner=self._owner)  # type: ignore[arg-type]

    def add_style_preset(self, name: str, preset: object) -> None:
        self._inner.add_style_preset(name, preset, owner=self._owner)

    def add_brand_kit_loader(self, name: str, fn: object) -> None:
        self._inner.add_brand_kit_loader(name, fn, owner=self._owner)  # type: ignore[arg-type]

    def add_exporter(self, name: str, fn: object) -> None:
        self._inner.add_exporter(name, fn, owner=self._owner)  # type: ignore[arg-type]