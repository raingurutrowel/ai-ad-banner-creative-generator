"""Stable plugin-facing protocols. Frozen at host version 0.6.x."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    """Declared metadata for a plugin. Read from `manifest.toml` at load."""

    name: str = Field(min_length=1, max_length=64)
    version: str
    api_version: str = "0.6"
    capabilities: list[str] = Field(default_factory=list)
    hooks: list[str] = Field(default_factory=list)
    description: str = ""


@runtime_checkable
class PluginContext(Protocol):
    """The only handle a plugin gets to host state."""

    @property
    def assets_root(self) -> str: ...

    @property
    def render_root(self) -> str: ...

    def read_asset(self, rel_path: str) -> bytes: ...

    def write_render(self, rel_path: str, payload: bytes) -> None: ...

    def fetch(self, url: str, *, timeout_s: float = 10.0) -> bytes: ...


@runtime_checkable
class RegistryProtocol(Protocol):
    """Hook surface handed to `register(registry)`."""

    def add_copy_provider(self, name: str, fn: Any) -> None: ...

    def add_style_preset(self, name: str, preset: Any) -> None: ...

    def add_brand_kit_loader(self, name: str, fn: Any) -> None: ...

    def add_exporter(self, name: str, fn: Any) -> None: ...


@runtime_checkable
class PluginProtocol(Protocol):
    """A loaded plugin module must expose `register(registry)`."""

    def register(self, registry: RegistryProtocol) -> None: ...