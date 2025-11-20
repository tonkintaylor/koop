import os

import pytest

from koop.backend.api.download_layer import download_layer

IS_NOT_PR_BUILD = os.getenv("BITBUCKET_PR_ID") is None
IS_ON_CI = os.getenv("CI") is not None


@pytest.mark.skipif(
    IS_ON_CI and IS_NOT_PR_BUILD,
    reason="Only running tests which query the API on PR builds",
)
def test_download_layer(tmp_path, koordinates_connection, layer_id):
    expected_output_dir = tmp_path / "kx-koop-test-GPKG"
    expected_output_gpkg = expected_output_dir / "koop-test.gpkg"
    expected_output_txt = expected_output_dir / "koop-test.txt"

    download_layer(
        session=koordinates_connection.session,
        domain=koordinates_connection.domain,
        api_version=koordinates_connection.api_version,
        layer_id=layer_id,
        output_dir=tmp_path,
    )

    assert expected_output_dir.exists()
    assert expected_output_gpkg.exists()
    assert expected_output_txt.exists()
