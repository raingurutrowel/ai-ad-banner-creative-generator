"""Maps a RenderRequest onto the registered exporters and style hooks."""

from __future__ import annotations

import logging

from contracts.render_contract import RenderRequest, RenderResult
from contracts.errors import RenderError
from core.registry import HookRegistry
from services.canvas_composer import CanvasComposer

log = logging.getLogger("ad_banner.handler.render")


class RenderHandler:
    def __init__(self, registry: HookRegistry, composer: CanvasComposer) -> None:
        self._registry = registry
        self._composer = composer

    def handle(self, request: RenderRequest, request_id: str) -> RenderResult:
        fmt = request.export_format.value
        try:
            exporter = self._registry.exporter(fmt)
        except KeyError as exc:
            raise RenderError(f"no exporter registered for {fmt}") from exc

        image = self._composer.compose(request)
        payload = exporter(image, fmt)
        out_rel = f"renders/{request_id}.{fmt}"

        from utils.timer import Stopwatch  # local import keeps cold-start light

        with Stopwatch() as sw:
            self._composer.ctx.write_render(out_rel, payload)

        return RenderResult(
            request_id=request_id,
            output_path=out_rel,
            width=image.width,
            height=image.height,
            bytes_written=len(payload),
            duration_ms=sw.elapsed_ms,
        )