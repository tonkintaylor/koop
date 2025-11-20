from requests import Response, Session

from koop.backend.api.exports.enums import (
    ExportFormats,
)
from koop.backend.api.exports.schemas import ExportRequestSchema


def post_export(  # noqa: PLR0913
    session: Session,
    url: str,
    domain: str,
    api_version: str,
    layer_id: int,
    export_format: str,
    file_type: str | None = None,
    tiles: list[str] | None = None,
) -> Response:
    """Post an export request.

    Args:
        session: The session to use to make the request.
        url: The URL to use to make the request.
        domain: The domain to use to make the request.
        api_version: The version of the API to use.
        layer_id: The ID of the layer to export.
        export_format: The format to export the layer to.
        file_type: The file type to export the layer to. Defaults to None.
        tiles: The tiles to export. Defaults to None.

    Returns:
        requests.Response: The response.
    """
    data = {
        "formats": _layer_format(export_format, file_type),
        "items": [
            {
                "item": f"https://{domain}/services/api/v{api_version}/layers/{layer_id}/",
            }
        ],
    }

    if tiles:
        data["items"][0]["tiles"] = tiles

    data = ExportRequestSchema(**data)

    with session.post(url, json=data.model_dump(exclude_none=True)) as response:
        response.raise_for_status()
        return response


def _layer_format(export_format: str, file_type: str | None = None) -> dict:
    if file_type is None:
        return ExportFormats[export_format].value
    msg = f"Invalid export format: {file_type}"
    raise ValueError(msg)
