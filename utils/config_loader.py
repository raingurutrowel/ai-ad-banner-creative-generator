"""Loads `config/plugins.toml` into a typed HostConfig."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class HostConfig:
    assets_root: str
    render_root: str
    export_root: str
    max_workers: int
    enabled_plugins: list[str]
    disabled_plugins: list[str]
    default_caps: dict[str, list[str]] = field(default_factory=dict)


def load_config(path: Path) -> HostConfig:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    host = raw.get("host", {})
    enabled = raw.get("enabled", {}).get("plugins", [])
    disabled = raw.get("disabled", {}).get("plugins", [])
    caps = raw