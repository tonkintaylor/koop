from pydantic import BaseModel
from requests import Session

from koop.backend.api.exports.post_export import post_export


def create_export(  # noqa: PLR0913
    session: Session,
    domain: str,
    api_version: str,
    layer_id: int,
    export_format: str,
    file_type: str | None = None,
    tiles: list[str] | None = None,
) -> dict:
    """Create and start a new export.

    https://apidocs.koordinates.com/#tag/Exports/operation/postExport

    Args:
        session: The session to use to make the request.
        domain: The domain to use to make the request.
        api_version: The version of the API to use.
        layer_id: The ID of the layer to export.
        export_format: The format to export the layer to.
        file_type: The file type to export the layer to. Defaults to None.
        tiles: The tiles to export. Defaults to None.

    Returns:
        dict: The JSON response.
    """
    url = f"https://{domain}/services/api/v{api_version}/exports/"

    response = post_export(
        session, url, domain, api_version, layer_id, export_format, file_type, tiles
    )

    return _ResponseSchema(**response.json())


class _ResponseSchema(BaseModel):
    """The response schema."""

    id: int
    name: str
    created_at: str | None
    created_via: str
    state: str
    url: str
    download_url: str | None
    user: dict
    delivery: dict
    items: list[dict]
    crs: dict
    extent: str | None
    formats: dict
    options: dict | None
    size_estimate_unzipped: int
    size_complete_zipped: int | None
    size_complete_unzipped: int | None
    is_cropped: bool
    invoice: str | None
    _from: dict
    progress: float
