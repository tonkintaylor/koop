from pydantic import BaseModel
from requests import Session

from koop.backend.api.exports.post_export import post_export


class _ResponseItemsSchema(BaseModel):
    item: str
    color: str | None = None
    license: dict | None = None
    price: float
    currency: str | None
    is_valid: bool
    invalid_reasons: list[str]
    size_estimate_zipped: int


class _ResponseSchema(BaseModel):
    items: list[_ResponseItemsSchema]
    size_estimate_zipped: int
    is_valid: bool
    invalid_reasons: list[str]
    suggested_crs: list[dict]
    suggested_crs_vertical: list[dict]
    name: str
    zip_filename: str
    delivery: dict
    courier_cost: dict


def validate_export(  # noqa: PLR0913
    session: Session,
    domain: str,
    api_version: str,
    layer_id: int,
    export_format: str,
    file_type: str | None = None,
    tiles: list[str] | None = None,
) -> _ResponseSchema:
    """Validate an export request.

    https://apidocs.koordinates.com/#tag/Exports/operation/validateExportRequest
    The Export Validation endpoint accepts the same content as the Export Creation
    API but will not create/start the export and will return additional information.

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
    url = f"https://{domain}/services/api/v{api_version}/exports/validate/"

    response = post_export(
        session, url, domain, api_version, layer_id, export_format, file_type, tiles
    )

    return _ResponseSchema(**response.json())
