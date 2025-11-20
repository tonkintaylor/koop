from pathlib import Path

from koop.backend.conn import KoordinatesConnection
from koop.get_latest import get_latest_layer

__all__ = ["get_layer_from_id"]


def get_layer_from_id(
    layer_id: int, api_key: str, domain: str = "ttgroup.koordinates.com"
) -> Path:
    """Helper function to get the latest layer from Koordinates.

    Args:
        layer_id (int): The layer ID.
        api_key (str): Your API key.
        domain (str, optional): The domain of the API.

    Returns:
        Path: The path to the latest layer.

    """
    conn = KoordinatesConnection(
        api_key,
        domain,
    )

    try:
        return get_latest_layer(conn=conn, layer_id=layer_id)
    finally:
        if conn:
            conn.close()
