from pathlib import Path

from defusedxml.ElementTree import fromstring
from pydantic import BaseModel

from koop.backend.api.layers_and_tables.get_details import (
    get_layer_details,
    get_layer_metadata,
)
from koop.backend.conn import KoordinatesConnection


class DublinCoreMetadata(BaseModel):
    """Dublin Core compliant metadata.

    Attributes:
        title: The name given to the resource.
        creator: An entity primarily responsible for making the content of the resource.
        subject: The topic of the content of the resource.
        description: An account of the content of the resource.
        type: The nature or genre of the content of the resource.
        source: A Reference to a resource from which the present resource is derived.
        relation: A reference to a related resource.
        coverage: The extent or scope of the content of the resource.
        publisher: An entity responsible for making the resource available.
        contributor: An entity responsible for making contributions to the content of
        the resource.
        rights: Information about rights held in and over the resource.
        date: A date associated with an event in the life cycle of the resource.
        format: The physical or digital manifestation of the resource.
        identifier: An unambiguous reference to the resource within a given context.
        language: A language of the intellectual content of the resource.
    """

    title: str | None = None
    creator: str | None = None
    subject: str | None = None
    description: str | None = None
    type: str | None = None
    source: str | None = None
    relation: str | None = None
    coverage: str | None = None
    publisher: str | None = None
    contributor: str | None = None
    rights: str | None = None
    date: str | None = None
    format: str | None = None
    identifier: str | None = None
    language: str | None = None

    def as_xml(self) -> str:
        """Convert the metadata to an XML string."""
        xml = (
            '<oai_dc:dc xmlns:dc="https://purl.org/dc/elements/1.1/" '
            'xmlns:gco="https://www.isotc211.org/2005/gco" '
            'xmlns:gmd="https://www.isotc211.org/2005/gmd" '
            'xmlns:gts="https://www.isotc211.org/2005/gts" '
            'xmlns:oai_dc="https://www.openarchives.org/OAI/2.0/oai_dc/" '
            'xmlns:gml="https://www.opengis.net/gml" '
            'xmlns:xlink="https://www.w3.org/1999/xlink" '
            'xmlns="https://purl.org/dc/elements/1.1/">'
        )
        for key, value in self.model_dump().items():
            if value:
                xml += f"<dc:{key}>{value}</dc:{key}>"
        xml += "</oai_dc:dc>"
        return xml

    def to_xml(self, fn: Path) -> None:
        """Write the metadata to an XML file."""
        xml = self.as_xml()
        with fn.open("w") as f:
            f.write(xml)

    @classmethod
    def from_raw_xml(cls, xml: str) -> "DublinCoreMetadata":
        """Create a DublinCoreMetadata object from raw XML."""
        ns = {"dc": "https://purl.org/dc/elements/1.1/"}
        root = fromstring(xml)
        metadata = {}

        for field in cls.model_fields.keys():
            element = root.find(f"dc:{field}", ns)
            if element is not None:
                metadata[field] = element.text

        return cls(**metadata)

    @classmethod
    def from_koordinates(
        cls, *, conn: KoordinatesConnection, layer_id: int
    ) -> "DublinCoreMetadata":
        """Create a DublinCoreMetadata object by querying Koordinates directly."""

        raw_xml = get_layer_metadata(
            session=conn.session,
            domain=conn.domain,
            api_version=conn.api_version,
            layer_id=layer_id,
        )

        return DublinCoreMetadata.from_raw_xml(raw_xml)

    def edit_metadata_fields(self, **kwargs: dict) -> None:
        """Edit the metadata fields."""
        for key, value in kwargs.items():
            if key not in type(self).model_fields:
                msg = f"Field {key} not in model."
                raise ValueError(msg)
            setattr(self, key, value)

    def update_source_field(
        self,
        *,
        conn: KoordinatesConnection,
        layer_ids: list[int],
        version_ids: list[int],
    ) -> None:
        """Update the source field with the given layer and version IDs."""

        if len(layer_ids) != len(version_ids):
            msg = "The number of layer IDs and version IDs must be the same."
            raise ValueError(msg)
        layers_details = [
            get_layer_details(
                session=conn.session,
                domain=conn.domain,
                api_version=conn.api_version,
                layer_id=layer_id,
                version_id=version_id,
            )
            for layer_id, version_id in zip(layer_ids, version_ids, strict=True)
        ]
        layer_titles = [layer.title for layer in layers_details]
        publish_dates = [layer.published_at for layer in layers_details]

        self.source = _create_source_field(
            layer_ids, layer_titles, version_ids, publish_dates
        )

    def update_source_with_latest_layer_versions(
        self, *, conn: KoordinatesConnection, layer_ids: list[int]
    ) -> None:
        """Update the source field with the latest versions of the given layer IDs."""
        layers_details = [
            get_layer_details(
                session=conn.session,
                domain=conn.domain,
                api_version=conn.api_version,
                layer_id=layer_id,
            )
            for layer_id in layer_ids
        ]
        layer_titles = [layer.title for layer in layers_details]
        version_ids = [layer.version_id for layer in layers_details]
        publish_dates = [layer.published_at for layer in layers_details]

        self.source = _create_source_field(
            layer_ids, layer_titles, version_ids, publish_dates
        )

    @classmethod
    def populate_template(cls, *, conn: KoordinatesConnection, layer_id: int):  # noqa: ANN206
        """Create a DublinCoreMetadata instance using layer details."""

        layer_details = get_layer_details(
            session=conn.session,
            domain=conn.domain,
            api_version=conn.api_version,
            layer_id=layer_id,
        )

        return cls(
            title=layer_details.title,
            type=layer_details.kind.name,
            date=layer_details.published_at,
        )


def _create_source_field(
    layer_ids: list[int],
    layer_titles: list[str],
    version_ids: list[int],
    dates: list[str],
) -> str:
    """Create a source field from the given layer IDs and titles."""
    csv = "layer_id,title,version_id,last_updated\n"
    for layer_id, title, version_id, date in zip(
        layer_ids, layer_titles, version_ids, dates, strict=True
    ):
        csv += f"{layer_id},{title},{version_id},{date}\n"

    return csv
