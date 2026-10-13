"""CreativeBrief — the normalized input that drives a render run."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CreativeBrief:
    preset_name: str
    copy_provider: str
    copy_args: dict[str, Any] = field(default_factory=dict)
    brand_kit_id: str | None = None
    canvas_slots: tuple[tuple[int, int], ...] = ()
    max_variants: int | None = None
    dpi: int = 72

    @classmethod
    def from_preset(cls, preset_name: str) -> "CreativeBrief":
        return cls(
            preset_name=preset_name,
            copy_provider="default",
            copy_args={"preset": preset_name},
        )