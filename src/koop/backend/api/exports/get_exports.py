from datetime import datetime

from pydantic import BaseModel, TypeAdapter
from requests import Session


class _ResponseSchema(BaseModel):
    """The export schema."""

    id: int
    name: str
    created_at: datetime
    state: str
    url: str
    download_url: str | None


def get_exports(session: Session, domain: str, api_version: str) -> list:
    """Returns a list of exports you've created.

    https://apidocs.koordinates.com/#tag/Exports/operation/getExports

    Args:
        session (requests.Session): The session to use to make the request.
        domain (str): The domain to use to make the request.
        api_version (str): The version of the API to use.

    Returns:
        list: The JSON response.
    """
    url = f"https://{domain}/services/api/v{api_version}/exports/"

    with session.get(url) as response:
        response.raise_for_status()
        return TypeAdapter(list[_ResponseSchema]).validate_python(response.json())


def get_export_from_id(
    session: Session, domain: str, api_version: str, export_id: int
) -> _ResponseSchema:
    """Returns a list of exports you've created.

    Args:
        session (requests.Session): The session to use to make the request.
        domain (str): The domain to use to make the request.
        api_version (str): The version of the API to use.
        export_id (int): The ID of the export to get.

    Returns:
        list: The JSON response.
    """
    url = f"https://{domain}/services/api/v{api_version}/exports/{export_id}/"

    with session.get(url) as response:
        response.raise_for_status()
        return _ResponseSchema(**response.json())
