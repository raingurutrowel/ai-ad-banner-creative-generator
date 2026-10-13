"""Composes a creative onto a Pillow canvas using the active style preset."""

from __future__ import annotations

import logging
import random

from PIL import Image, ImageDraw

from contracts.render_contract import RenderRequest, StylePreset
from core.registry import HookRegistry
from core.context import HostContext

log = logging.getLogger("ad_banner.composer")


class CanvasComposer:
    def __init__(self, registry: HookRegistry, ctx: HostContext, seed: int) -> None:
        self.registry = registry
        self.ctx = ctx
        self._rng = random.Random(seed)

    def compose(self, request: RenderRequest) -> Image.Image:
        spec = request.canvas
        preset = request.preset
        img = Image.new("RGB", (spec.width, spec.height), spec.background)
        draw = ImageDraw.Draw(img)

        self._paint_backdrop(draw, spec.width, spec.height, preset)
        self._paint_headline(draw, request)
        self._paint_cta(draw, request, preset)
        return img

    def _paint_backdrop(
        self, draw: ImageDraw.ImageDraw, w: int, h: int, preset: StylePreset
    ) -> None:
        primary = preset.palette[0] if preset.palette else "#000000"
        accent = preset.palette[1] if len(preset.palette) > 1 else "#FFFFFF"
        draw.rectangle([0, 0, w, int(h * 0.62)], fill=primary)
        draw.rectangle([0, int(h * 0.62), w, h], fill=accent)

    def _paint_headline(self, draw: ImageDraw.ImageDraw, request: RenderRequest) -> None:
        pad = int(min(request.canvas.width, request.canvas.height) * 0.06)
        draw.text((pad, pad), request.copy.headline, fill="#FFFFFF")

    def _paint_cta(
        self, draw: ImageDraw.ImageDraw, request: RenderRequest, preset: StylePreset
    ) -> None:
        pad = int(min(request.canvas.width, request.canvas.height) * 0.06)
        r = preset.corner_radius
        y0 = int(request.canvas.height * 0.78)
        draw.rounded_rectangle(
            [pad, y0, pad * 5, y0 + pad * 1.6],
            radius=r,
            fill=preset.palette[2] if len(preset.palette) > 2 else "#111827",
        )
        draw.text((pad * 1.4, y0 + pad * 0.4), request.copy.cta, fill="#FFFFFF")