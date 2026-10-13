"""Read-through asset store for brand kits, fonts, and reference images."""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

log = logging.getLogger("ad_banner.assets")


class AssetStore:
    def __init__(self, assets_root: Path) -> None:
        self._root = assets_root

    @lru_cache(maxsize=128)
    def read(self, rel_path: str) -> bytes:
        target = (self._root / rel_path).resolve()
        if self._root.resolve() not in target.parents:
            raise ValueError(f"asset path escapes root: {rel_path}")
        log.debug("asset read: %s", rel_path)
        return target.read_bytes()

    def list_brand_kits(self) -> list[str]:
        kit_dir = self._root / "brand_kits"
        if not kit_dir.exists():
            return []
        return sorted(p.stem for p in kit_dir.glob("*.toml"))