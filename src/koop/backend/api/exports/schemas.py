from typing import Literal

from pydantic import BaseModel

from koop.backend.api.exports.enums import (
    ExportFormats,
)
from koop.backend.crs import NZTM2000_EPSG


class PolygonExtent(BaseModel):
    """https://geojson.org/geojson-spec.html#polygon."""

    type: Literal["Polygon"]
    coordinates: list[list[list[float]]]


class MultiPolygonExtent(BaseModel):
    """https://geojson.org/geojson-spec.html#multipolygon."""

    type: Literal["MultiPolygon"]
    coordinates: list[list[list[list[float]]]]


class ExportRequestItems(BaseModel):
    """The request items schema."""

    item: str
    color: str | None = None
    tiles: list[str] | None = None
    raster_resolution_multiplier: int | None = None
    include_raster_tab: bool | None = None
    include_geometry_field: bool | None = None
    include_hatching: bool | None = None
    include_xdata: bool | None = None


class ExportRequestSchema(BaseModel):
    """The request schema."""

    crs: str = NZTM2000_EPSG
    formats: ExportFormats
    items: list[ExportRequestItems]
    name: str | None = None
    extent: None = None
    options: dict | None = None
    delivery: dict[str, str] = {"method": "download"}
