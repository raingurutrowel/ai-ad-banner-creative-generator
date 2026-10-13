"""Top-level pipeline: brief -> copy -> styled canvas -> exported asset."""

from __future__ import annotations

import logging
import uuid

from contracts.render_contract import RenderRequest, RenderResult
from core.registry import HookRegistry
from core.context import HostContext
from handlers.render_handler import RenderHandler
from handlers.copy_handler import CopyHandler
from services.canvas_composer import CanvasComposer
from services.variant_planner import VariantPlanner
from models.brief import CreativeBrief

log = logging.getLogger("ad_banner.pipeline")


class RenderPipeline:
    def __init__(self, registry: HookRegistry, ctx: HostContext, seed: int) -> None:
        self._registry = registry
        self._ctx = ctx
        self._seed = seed
        self._composer = CanvasComposer(registry=registry, ctx=ctx, seed=seed)
        self._render = RenderHandler(registry=registry, composer=self._composer)
        self._copy = CopyHandler(registry=registry)
        self._planner = VariantPlanner(seed=seed)

    def render_preset(self, preset_name: str) -> list[RenderResult]:
        preset = self._registry.style_preset(preset_name)
        brief = CreativeBrief.from_preset(preset_name)
        copy_block = self._copy.generate(brief.copy_provider, brief.copy_args)

        results: list[RenderResult] = []
        for canvas in self._planner.plan(brief):
            request = RenderRequest(
                canvas=canvas,
                copy=copy_block,
                preset=preset,
                brand_kit_id=brief.brand_kit_id,
                seed=self._seed,
            )
            req_id = uuid.uuid4().hex[:12]
            results.append(self._render.handle(request, req_id))
        return results