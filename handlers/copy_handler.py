"""Resolves copy blocks via the registered copy providers."""

from __future__ import annotations

from typing import Any

from contracts.render_contract import CopyBlock
from core.registry import HookRegistry


class CopyHandler:
    def __init__(self, registry: HookRegistry) -> None:
        self._registry = registry

    def generate(self, provider: str, brief: dict[str, Any]) -> CopyBlock:
        fn = self._registry.copy_provider(provider)
        raw = fn(provider, brief)
        return CopyBlock(
            headline=raw.get("headline", ""),
            subhead=raw.get("subhead", ""),
            cta=raw.get("cta", ""),
            legal=raw.get("legal", ""),
        )