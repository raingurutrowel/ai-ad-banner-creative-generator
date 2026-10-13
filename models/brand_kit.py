"""BrandKit — palette, fonts, and logo refs loaded from a TOML file."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BrandKit(BaseModel):
    id: str
    label: str
    palette: list[str] = Field(default_factory=list)
    headline_font: str = "Inter-Bold"
    body_font: str = "Inter-Regular"
    logo_asset: str | None = None