from enum import Enum
from typing import ClassVar


class GridExportFormats(Enum):
    """Grid Export Formats enumeration."""

    geotiff = "image/tiff;subtype=geotiff"


class VectorExportFormats(Enum):
    """Vector Export Formats enumeration."""

    geopackage = "application/x-ogc-gpkg"


class ExportFormats(dict, Enum):
    """Represents the export formats for raster and vector data."""

    grid: ClassVar = {"grid": GridExportFormats.geotiff.value}
    vector: ClassVar = {"vector": VectorExportFormats.geopackage.value}
