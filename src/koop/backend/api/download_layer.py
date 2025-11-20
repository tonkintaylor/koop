from pathlib import Path
from time import sleep
from zipfile import ZipFile

from requests import Session

from koop.backend.api.exports.create_export import create_export
from koop.backend.api.exports.get_exports import get_export_from_id
from koop.backend.api.exports.validate_export import validate_export
from koop.backend.api.layers_and_tables.get_details import get_layer_details


def download_layer(
    *,
    session: Session,
    domain: str,
    api_version: str,
    layer_id: int,
    output_dir: Path,
) -> Path:
    """Download a layer from the Koordinates server.

    Args:
        session: The session to use to make the request.
        domain: The domain to use for the request.
        api_version: The version of the API to use for the request.
        layer_id: The ID of the layer to download.
        output_dir: The directory to save the downloaded layer to.

    Returns:
        The path to the directory whether the layer is saved.

    """
    layer_details = get_layer_details(session, domain, api_version, layer_id)

    # validate
    validation_response = validate_export(
        session,
        domain,
        api_version,
        layer_id,
        export_format=layer_details.kind.value,
    )

    if not validation_response.is_valid:
        raise ValueError(validation_response.invalid_reasons)

    export = create_export(
        session,
        domain,
        api_version,
        layer_id,
        export_format=layer_details.kind.value,
    )

    # wait for export to complete
    export_url = wait_for_export(session, domain, api_version, export.id)

    # download
    filename = download_export(session, export_url, output_dir)

    # unzip
    unzipped_dir = unzip_export(output_dir / filename)

    return unzipped_dir


def wait_for_export(
    session: Session, domain: str, api_version: str, export_id: int
) -> str:
    """Wait for the export to complete.

    Args:
        session: The session to use to make the request.
        domain: The domain to use for the request.
        api_version: The version of the API to use for the request.
        export_id: The ID of the export to wait for.

    """
    state = "processing"
    while state != "complete":
        sleep(1)

        export = get_export_from_id(session, domain, api_version, export_id)
        state = export.state

        if state not in ["processing", "complete"]:
            msg = f"Export failed with state: {state}"
            raise ValueError(msg)

    return export.download_url


def download_export(session: Session, export_url: str, output_dir: Path) -> Path:
    """Download the export from the Koordinates server.

    Args:
        session: The session to use to make the request.
        domain: The domain to use for the request.
        api_version: The version of the API to use for the request.
        export_url: The URL of the export to download.
        output_dir: The directory to save the downloaded export to.

    """
    with session.get(export_url, stream=True) as response:
        response.raise_for_status()

        if "Content-Disposition" in response.headers:
            filename = response.headers["Content-Disposition"].split(
                "filename*=UTF-8''"
            )[1]
        else:
            filename = "export.zip"

        with (output_dir / filename).open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

    return filename


def unzip_export(zip_path: Path) -> Path:
    """Unzip the export.

    Args:
        zip_path: The path to the export to unzip.

    """
    output_dir = zip_path.parent / zip_path.stem

    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    zip_path.unlink()

    return output_dir
