"""Plans the set of canvas sizes a brief should be exported at."""

from __future__ import annotations

import random

from contracts.render_contract import CanvasSpec
from models.brief import CreativeBrief

_AD_SLOTS: tuple[tuple[int, int], ...] = (
    (300, 250),
    (728, 90),
    (160, 600),
    (1200, 628),
    (1080, 1080),
)


class VariantPlanner:
    def __init__(self, seed: int) -> None:
        self._rng = random.Random(seed)

    def plan(self, brief: CreativeBrief) -> list[CanvasSpec]:
        slots = brief.canvas_slots or _AD_SLOTS
        if brief.max_variants is not None:
            slots = slots[: brief.max_variants]
        return [CanvasSpec(width=w, height=h, dpi=brief.dpi) for w, h in slots]