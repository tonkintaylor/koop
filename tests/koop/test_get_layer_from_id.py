import os
import re

from koop import get_layer_from_id


class TestGetFromId:
    def test_unit(self, cache_dir, layer_id):
        fn = get_layer_from_id(
            layer_id=layer_id,
            api_key=os.getenv("KOORDINATES_API_KEY"),
        )

        assert fn.exists()
        assert fn.parent == cache_dir
        assert re.match(rf"{layer_id}_\d+_[a-fA-F\d]{{32}}.gpkg", fn.name)
