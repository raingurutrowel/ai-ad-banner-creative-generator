"""Render pipeline data shapes. These cross the host/plugin boundary."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class CanvasSpec(BaseModel):
    """Pixel canvas the creative is composed onto."""

    width: int = Field(gt=0, le=8192)
    height: int = Field(gt=0, le=8192)
    dpi: int = Field(default=72, ge=36, le=600)
    background: str = "#FFFFFF"


class CopyBlock(BaseModel):
    headline: str
    subhead: str = ""
    cta: str = ""
    legal: str = ""


class StylePreset(BaseModel):
    name: str
    palette: list[str]
    headline_font: str
    body_font: str
    corner_radius: int = 0
    extras: dict[str, Any] = Field(default_factory=dict)


class RenderRequest(BaseModel):
    canvas: CanvasSpec
    copy: CopyBlock
    preset: StylePreset
    brand_kit_id: str | None = None
    seed: int = 6767
    export_format: ExportFormat = ExportFormat.PNG


class RenderResult(BaseModel):
    request_id: str
    output_path: str
    width: int
    height: int
    bytes_written: int
    duration_ms: int