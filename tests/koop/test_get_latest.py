import importlib
import os
import re

import pytest

import koop.get_latest
from koop.get_latest import get_latest_layer

IS_NOT_PR_BUILD = os.getenv("BITBUCKET_PR_ID") is None
IS_ON_CI = os.getenv("CI") is not None


@pytest.mark.skipif(
    IS_ON_CI and IS_NOT_PR_BUILD,
    reason="Only running tests which query the API on PR builds",
)
class TestGetLatest:
    def test_unit(self, cache_dir, koordinates_connection, layer_id):
        fn = get_latest_layer(
            conn=koordinates_connection,
            layer_id=layer_id,
        )

        assert fn.exists()
        assert fn.parent == cache_dir
        assert re.match(rf"{layer_id}_\d+_[a-fA-F\d]{{32}}.gpkg", fn.name)

    def test_caching(self, cache_dir, koordinates_connection, layer_id, monkeypatch):
        fn1 = get_latest_layer(
            conn=koordinates_connection,
            layer_id=layer_id,
        )
        # Sabotage download_layer so it fails if called, ensuring that the function is
        # using the cache
        with monkeypatch.context() as m:
            m.setattr(
                "koop.backend.api.download_layer.download_layer",
                lambda **kwargs: kwargs["keyerror"],
            )
            # Reimport to ensure the monkeypatch is applied
            importlib.reload(koop.get_latest)

            fn2 = get_latest_layer(
                conn=koordinates_connection,
                layer_id=layer_id,
            )

            assert fn1 == fn2
            assert fn1.parent == cache_dir

            # Ensure the monkeypatch was applied
            fn1.unlink()
            with pytest.raises(KeyError):
                get_latest_layer(
                    conn=koordinates_connection,
                    layer_id=layer_id,
                )

        importlib.reload(koop.get_latest)

    def test_cache_dir_not_set(self, monkeypatch, koordinates_connection, layer_id):
        with monkeypatch.context() as m:
            # There is no KOOPCACHE_DIR environment variable set in CI
            if not os.getenv("CI"):
                m.delenv("KOOPCACHE_DIR")

            expected_msg = (
                "Please set the KOOPCACHE_DIR environment variable to your desired"
                " cache directory."
            )
            with pytest.raises(ValueError, match=expected_msg):
                get_latest_layer(
                    conn=koordinates_connection,
                    layer_id=layer_id,
                )

    def test_cache_doesnt_have_rubbish(
        self, cache_dir, koordinates_connection, layer_id
    ):
        _ = get_latest_layer(
            conn=koordinates_connection,
            layer_id=layer_id,
        )

        num_cached_files_and_folders = len(list(cache_dir.glob("*")))

        assert num_cached_files_and_folders == 1

    def test_cache_dir_doesnt_exist(
        self, monkeypatch, koordinates_connection, layer_id, tmp_path
    ):
        with monkeypatch.context() as m:
            cache_dir = tmp_path / "nonexistent"
            m.setenv("KOOPCACHE_DIR", str(cache_dir))
            get_latest_layer(
                conn=koordinates_connection,
                layer_id=layer_id,
            )

            assert cache_dir.exists()
