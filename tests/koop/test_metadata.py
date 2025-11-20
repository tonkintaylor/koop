import os

import pytest
from defusedxml import ElementTree

from koop.backend.api.layers_and_tables.get_details import LayerDetails
from koop.metadata import DublinCoreMetadata

IS_NOT_PR_BUILD = os.getenv("BITBUCKET_PR_ID") is None
IS_ON_CI = os.getenv("CI") is not None


def _mock_get_layer_details(*args, **kwargs):
    _ = args, kwargs
    return LayerDetails(
        id=1,
        url="https://open.spotify.com/track/2ylpbsHqGUAv3za4JkyMgz?si=68ccb8ba423d4022",
        type="mongolian",
        title="throat singing",
        kind="vector",
        published_at="yesterday arvo",
        metadata=None,
        version_id=23,
    )


def _mock_get_layer_details_with_metadata(*args, **kwargs):
    _ = args, kwargs
    return LayerDetails(
        id=1,
        url="https://open.spotify.com/track/2ylpbsHqGUAv3za4JkyMgz?si=68ccb8ba423d4022",
        type="mongolian",
        title="throat singing",
        kind="vector",
        published_at="yesterday arvo",
        metadata={
            "title": "Koop Test",
        },
        version_id=23,
    )


def canonicalize(xml_string):
    """Convert XML string to canonical form."""
    root = ElementTree.fromstring(xml_string)
    return ElementTree.tostring(root, encoding="unicode", method="xml")


def assert_xml_strings_equal(xml_string1, xml_string2):
    """Compare two XML strings for equality regardless of element order."""
    canonical_xml1 = canonicalize(xml_string1)
    canonical_xml2 = canonicalize(xml_string2)
    return canonical_xml1 == canonical_xml2


class TestDublinCoreMetadata:
    def test_edit_metadata_fields(self):
        metadata = DublinCoreMetadata(title="Old Title")
        metadata.edit_metadata_fields(title="New title", source="BBQ")
        assert metadata.title == "New title"
        assert metadata.source == "BBQ"

    def test_update_source_field(self, koordinates_connection, layer_id, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr("koop.metadata.get_layer_details", _mock_get_layer_details)
            metadata = DublinCoreMetadata(source="BBQ")
            metadata.update_source_field(
                conn=koordinates_connection,
                layer_ids=[layer_id],
                version_ids=[23],
            )
        assert metadata.source is not None
        assert "throat singing" in metadata.source, "Title not in source"
        assert "yesterday arvo" in metadata.source, "Published date not in source"
        assert "23" in metadata.source, "Version ID not in source"

    def test_update_source_with_latest_layer_versions(
        self, koordinates_connection, layer_id, monkeypatch
    ):
        with monkeypatch.context() as m:
            m.setattr("koop.metadata.get_layer_details", _mock_get_layer_details)
            metadata = DublinCoreMetadata(source="BBQ")

            metadata.update_source_with_latest_layer_versions(
                conn=koordinates_connection, layer_ids=[layer_id]
            )
        assert metadata.source is not None
        assert "throat singing" in metadata.source, "Title not in source"
        assert "yesterday arvo" in metadata.source, "Published date not in source"
        assert "23" in metadata.source, "Version ID not in source"

    def test_populate_template(self, koordinates_connection, layer_id, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr("koop.metadata.get_layer_details", _mock_get_layer_details)
            metadata = DublinCoreMetadata.populate_template(
                conn=koordinates_connection, layer_id=layer_id
            )
        assert metadata.title == "throat singing"
        assert metadata.type == "vector"
        assert metadata.date == "yesterday arvo"

    def test_xml_reading_and_writing(self, metadata_xml):
        metadata = DublinCoreMetadata.from_raw_xml(metadata_xml)
        assert metadata.title == "Koop Test"
        assert metadata.creator == "Tonkin + Taylor"

        new_xml = metadata.as_xml()
        assert_xml_strings_equal(metadata_xml, new_xml)

    def test_from_koordinates_no_metadata(
        self, koordinates_connection, layer_id, monkeypatch
    ):
        with monkeypatch.context() as m:
            m.setattr(
                "koop.backend.api.layers_and_tables.get_details.get_layer_details",
                _mock_get_layer_details,
            )

            with pytest.raises(ValueError, match="Layer has no metadata."):
                DublinCoreMetadata.from_koordinates(
                    conn=koordinates_connection, layer_id=layer_id
                )

    @pytest.mark.skip(reason="Haven't figured out quite how I want to test this yet")
    def test_from_koordinates_with_metadata(
        self, koordinates_connection, layer_id, monkeypatch
    ):
        with monkeypatch.context() as m:
            m.setattr(
                "koop.backend.api.layers_and_tables.get_details.get_layer_details",
                _mock_get_layer_details_with_metadata,
            )

            metadata = DublinCoreMetadata.from_koordinates(
                conn=koordinates_connection, layer_id=layer_id
            )
        assert metadata.title == "Koop Test"
