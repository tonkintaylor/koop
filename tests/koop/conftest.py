import os

import pytest

from koop.backend.conn import KoordinatesConnection


@pytest.fixture()
def cache_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("koopcache")
    # Store the original value of the environment variable
    original_value = os.environ.get("KOOPCACHE_DIR")

    # Set the environment variable to the temporary directory
    os.environ["KOOPCACHE_DIR"] = str(tmp_dir)

    yield tmp_dir

    # Restore the original value of the environment variable
    if original_value is None:
        del os.environ["KOOPCACHE_DIR"]
    else:
        os.environ["KOOPCACHE_DIR"] = original_value


@pytest.fixture(scope="package")
def koordinates_connection():
    conn = KoordinatesConnection()
    yield conn
    conn.close()


@pytest.fixture(scope="package")
def layer_id():
    return 119171


@pytest.fixture()
def metadata_xml(assets_dir) -> str:
    fn = assets_dir / "metadata.xml"
    with fn.open("r") as f:
        return f.read()
