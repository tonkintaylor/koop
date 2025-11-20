import os
import shutil
from pathlib import Path

from koop.backend.api.download_layer import download_layer
from koop.backend.api.layers_and_tables.get_details import get_layer_details
from koop.backend.conn import KoordinatesConnection


def get_latest_layer(
    *,
    conn: KoordinatesConnection,
    layer_id: int,
) -> Path:
    """Get the latest version of a specified layer. Returns cached data if available."""

    # Get layer details
    layer_details = get_layer_details(
        conn.session, conn.domain, conn.api_version, layer_id
    )
    details_hash = layer_details.get_hex_hash()

    # Check if layer is already cached
    cache_dir = _get_cache_dir()
    fn = cache_dir / f"{layer_id}_{layer_details.version_id}_{details_hash}.gpkg"

    if fn.exists():
        return fn

    # Download the layer
    output_dir = download_layer(
        session=conn.session,
        domain=conn.domain,
        api_version=conn.api_version,
        layer_id=layer_id,
        output_dir=cache_dir,
    )

    # Find the geopackage in the output directory
    geopackages = list(output_dir.glob("*.gpkg"))
    if len(geopackages) != 1:
        msg = "Should only be one geopackage per export"
        raise ValueError(msg)
    (geopackage,) = geopackages

    # Rename the geopackage to the hash
    geopackage.rename(fn)

    # Remove the content that came with the geopackage
    if _is_file_in_dir(geopackage, output_dir):
        msg = "Geopackage should be moved"
        raise ValueError(msg)
    shutil.rmtree(output_dir)

    return fn


def get_latest_layer_details(conn: KoordinatesConnection, layer_id: int) -> dict:
    """Get the latest version of a specified layer. Returns cached data if available."""
    # Get layer details
    layer_details = get_layer_details(
        conn.session, conn.domain, conn.api_version, layer_id
    )

    return layer_details


def _get_cache_dir() -> Path:
    """Get the cache directory."""
    cache_dir = os.environ.get("KOOPCACHE_DIR")
    if cache_dir is None:
        msg = (
            "Please set the KOOPCACHE_DIR environment variable to your "
            "desired cache directory."
        )
        raise ValueError(msg)

    cache_dir = Path(cache_dir)

    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    return cache_dir


def _is_file_in_dir(file: Path, directory: Path) -> bool:
    """Check if a file is in a directory."""
    try:
        file.relative_to(directory)
        return file.exists()

    except ValueError:
        return False
