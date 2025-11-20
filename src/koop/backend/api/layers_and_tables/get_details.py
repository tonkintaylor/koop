from enum import Enum
from hashlib import md5

from pydantic import BaseModel, ConfigDict
from requests import Session


class _LayerTypes(str, Enum):
    """The layer types."""

    vector = "vector"
    grid = "grid"


class LayerDetails(BaseModel):
    """The Layer Details schema."""

    model_config = ConfigDict(frozen=True)

    id: int
    url: str
    type: str
    title: str
    kind: _LayerTypes
    published_at: str
    metadata: dict | None
    version_id: int

    def get_hex_hash(self) -> str:
        """Generate a hexadecimal hash for the layer details."""
        hash_key = (
            self.id,
            self.url,
            self.type,
            self.title,
            self.kind,
            self.published_at,
        )
        hash_key = str(hash_key).encode("utf-8")
        hash_digest = md5(hash_key).hexdigest()
        return hash_digest


def get_layer_details(
    session: Session,
    domain: str,
    api_version: str,
    layer_id: int,
    version_id: int | None = None,
) -> LayerDetails:
    """Get details of a layer or a table.

    https://apidocs.koordinates.com/#tag/Layers/operation/getLayersById

    Args:
        session: The session to use to make the request.
        domain: The domain to use to make the request.
        api_version: The version of the API to use.
        layer_id: The ID of the export to get.
        version_id: The version of the layer to get, if not provided the latest version
        will be returned.

    Returns:
        list: The JSON response.
    """
    url = f"https://{domain}/services/api/v{api_version}/layers/{layer_id}/"

    if version_id is not None:
        url += f"versions/{version_id}/"

    with session.get(url) as response:
        response.raise_for_status()
        response_dict = response.json()
        return LayerDetails(**response_dict, version_id=response_dict["version"]["id"])


def get_layer_metadata(
    session: Session, domain: str, api_version: str, layer_id: int
) -> str:
    """Get the metadata for a layer."""

    layer_details = get_layer_details(
        session=session, domain=domain, api_version=api_version, layer_id=layer_id
    )
    if layer_details.metadata is None:
        msg = "Layer has no metadata."
        raise ValueError(msg)

    dc_url = layer_details.metadata["dc"]

    with session.get(dc_url) as response:
        raw_xml = response.content

    return raw_xml
