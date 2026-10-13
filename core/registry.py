"""Hook registry. Plugins publish capabilities here; the pipeline consumes them."""

from __future__ import annotations

from typing import Any, Callable

from contracts.errors import PluginLoadError

CopyProvider = Callable[[str, dict[str, Any]], str]
StylePresetFactory = Callable[[str], Any]
BrandKitLoader = Callable[[str], dict[str, Any]]
Exporter = Callable[[Any, str], bytes]


class HookRegistry:
    """Collects plugin hooks. First registration wins; duplicates are rejected."""

    def __init__(self) -> None:
        self._copy_providers: dict[str, CopyProvider] = {}
        self._style_presets: dict[str, StylePresetFactory] = {}
        self._brand_kits: dict[str, BrandKitLoader] = {}
        self._exporters: dict[str, Exporter] = {}
        self._owners: dict[tuple[str, str], str] = {}

    def _claim(self, kind: str, name: str, owner: str) -> None:
        key = (kind, name)
        if key in self._owners:
            raise PluginLoadError(
                f"hook {kind}:{name} already registered by {self._owners[key]}"
            )
        self._owners[key] = owner

    def add_copy_provider(self, name: str, fn: CopyProvider, *, owner: str = "?") -> None:
        self._claim("copy", name, owner)
        self._copy_providers[name] = fn

    def add_style_preset(self, name: str, preset: Any, *, owner: str = "?") -> None:
        self._claim("preset", name, owner)
        self._style_presets[name] = lambda _n, _p=preset: _p

    def add_brand_kit_loader(self, name: str, fn: BrandKitLoader, *, owner: str = "?") -> None:
        self._claim("brandkit", name, owner)
        self._brand_kits[name] = fn

    def add_exporter(self, name: str, fn: Exporter, *, owner: str = "?") -> None:
        self._claim("export", name, owner)
        self._exporters[name] = fn

    def copy_provider(self, name: str) -> CopyProvider:
        return self._copy_providers[name]

    def style_preset(self, name: str) -> Any:
        return self._style_presets[name](name)

    def brand_kit(self, name: str) -> dict[str, Any]:
        return self._brand_kits[name](name)

    def exporter(self, fmt: str) -> Exporter:
        return self._exporters[fmt]

    def names(self) -> dict[str, list[str]]:
        return {
            "copy": sorted(self._copy_providers),
            "preset": sorted(self._style_presets),
            "brandkit": sorted(self._brand_kits),
            "export": sorted(self._exporters),
        }