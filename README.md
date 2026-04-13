<h1 align="center">
  <img src="https://github.com/user-attachments/assets/bbf2e050-449f-43c3-90df-14e2cc3060d2"><br>
</h1>

# koop

[![PyPI Version](https://img.shields.io/pypi/v/koop.svg)](https://pypi.python.org/pypi/koop)
[![PyPI Supported Versions](https://img.shields.io/pypi/pyversions/koop.svg)](https://pypi.python.org/pypi/koop)
![PyPI License](https://img.shields.io/pypi/l/koop.svg)

A Python client for the [Koordinates](https://koordinates.com/) platform API. Download geospatial layers (vector and raster), cache them locally, and manage Dublin Core metadata — all from a single function call.

## Overview

[Koordinates](https://koordinates.com/) is a geospatial data management platform used by organisations such as [LINZ](https://data.linz.govt.nz/) (Land Information New Zealand) to publish and share geospatial datasets. `koop` wraps the Koordinates REST API to let you:

1. **Download layers by ID** — vector layers arrive as GeoPackage files, raster layers as GeoTIFF files.
2. **Cache downloads** — each file is stored under a content-addressed name (`{layer_id}_{version_id}_{hash}.gpkg`), so repeated requests for the same version are served from disk.
3. **Manage metadata** — fetch, edit, and export Dublin Core (ISO 19115) metadata as XML.

### Features

- **Layer downloading** — download vector or raster layers from any Koordinates domain using a layer ID. The export is created server-side and streamed to your machine.
- **Version-aware caching** — downloaded layers are cached in a local directory (`KOOPCACHE_DIR`). The cache key includes the layer version and a hash of the layer details, so updated layers are re-downloaded automatically.
- **Dublin Core metadata** — fetch metadata from Koordinates, edit fields programmatically, track source layers with version history, and export to OAI_DC XML.
- **Multi-domain support** — connect to any Koordinates instance (e.g., `data.linz.govt.nz`, `ttgroup.koordinates.com`, or your own).
- **API key authentication** — connections authenticate via an `Authorization: key <api_key>` header. The key can be passed explicitly or read from the `KOORDINATES_API_KEY` environment variable.

## Installation

```bash
# With uv
uv add koop

# With pip
pip install koop
```

## Configuration

Set up the following environment variables before using `koop`:

```bash
# Required: Your Koordinates API key
export KOORDINATES_API_KEY="your-api-key-here"

# Required: Directory for caching downloaded layers
export KOOPCACHE_DIR="/path/to/cache/directory"
```

## Quick Start

```python
from pathlib import Path
from koop import get_layer_from_id
from koop.backend.conn import KoordinatesConnection
from koop.metadata import DublinCoreMetadata

# Simple layer download with caching
layer_path = get_layer_from_id(
    layer_id=123,
    api_key="your-api-key"
)
# Returns: Path to cached GeoPackage file

# Using custom domain (e.g., LINZ data)
linz_layer = get_layer_from_id(
    layer_id=456,
    api_key="your-api-key",
    domain="data.linz.govt.nz"
)

# Advanced: Using the connection object directly
conn = KoordinatesConnection(
    api_key="your-api-key",
    domain="ttgroup.koordinates.com"
)

try:
    # Get layer metadata
    metadata = DublinCoreMetadata.from_koordinates(
        conn=conn,
        layer_id=123
    )
    print(f"Layer title: {metadata.title}")
    print(f"Published: {metadata.date}")

    # Edit metadata fields
    metadata.edit_metadata_fields(
        description="Updated description",
        creator="Your Organization"
    )

    # Update source field with specific layer versions
    metadata.update_source_field(
        conn=conn,
        layer_ids=[123, 456],
        version_ids=[1, 2]
    )

    # Export metadata to XML
    metadata.to_xml(Path("metadata.xml"))

finally:
    conn.close()
```

## Main Features

### Layer Download and Caching

Download layers from Koordinates with automatic caching based on layer version:

```python
from koop import get_layer_from_id

# Download and cache a layer
layer_path = get_layer_from_id(
    layer_id=123,
    api_key="your-api-key"
)

# Subsequent calls with the same layer ID return the cached file
# if the version hasn't changed
cached_path = get_layer_from_id(layer_id=123, api_key="your-api-key")
```

### Metadata Management

Work with Dublin Core compliant metadata:

```python
from koop.backend.conn import KoordinatesConnection
from koop.metadata import DublinCoreMetadata

conn = KoordinatesConnection(api_key="your-api-key")

# Fetch metadata from Koordinates
metadata = DublinCoreMetadata.from_koordinates(conn=conn, layer_id=123)

# Access metadata fields
print(metadata.title)
print(metadata.description)
print(metadata.publisher)

# Create metadata template from layer details
template = DublinCoreMetadata.populate_template(conn=conn, layer_id=123)

# Update source field with latest layer versions
metadata.update_source_with_latest_layer_versions(
    conn=conn,
    layer_ids=[123, 456, 789]
)

conn.close()
```

### Connection Management

Manage connections to Koordinates API:

```python
from koop.backend.conn import KoordinatesConnection

# Connect to default domain (ttgroup.koordinates.com)
conn = KoordinatesConnection(api_key="your-api-key")

# Connect to LINZ Koordinates instance
linz_conn = KoordinatesConnection(
    api_key="your-api-key",
    domain="data.linz.govt.nz"
)

# API version specification (default is "1.x")
custom_conn = KoordinatesConnection(
    api_key="your-api-key",
    domain="ttgroup.koordinates.com",
    api_version="1.x"
)

# Always close connections when done
conn.close()
```

## How It Works

When you call `get_layer_from_id`, the following happens:

1. A `KoordinatesConnection` is opened to the target domain.
2. Layer details (title, type, version, etc.) are fetched from the `/layers/{id}/` API endpoint.
3. The cache directory is checked for an existing file matching the layer version and content hash.
4. If no cache hit, an export job is created on the Koordinates server, polled until complete, and the resulting ZIP is downloaded and extracted.
5. The extracted GeoPackage (or GeoTIFF) is renamed to the cache key and stored for future use.
6. The path to the local file is returned.

## API Reference

### `get_layer_from_id(layer_id, api_key, domain)`

Top-level convenience function. Downloads and caches a layer, returning a `Path` to the local file.

| Parameter    | Default                       | Description                                  |
| ------------ | ----------------------------- | -------------------------------------------- |
| `layer_id`   | *required*                    | Integer layer ID on the Koordinates platform |
| `api_key`    | *required*                    | Koordinates API key                          |
| `domain`     | `"ttgroup.koordinates.com"`   | Koordinates instance hostname                |

### `KoordinatesConnection`

Manages an authenticated `requests.Session` against a Koordinates instance.

| Parameter     | Default                       | Description                    |
| ------------- | ----------------------------- | ------------------------------ |
| `api_key`     | `KOORDINATES_API_KEY` env var | API key for authentication     |
| `domain`      | `"ttgroup.koordinates.com"`   | Target Koordinates hostname    |
| `api_version` | `"1.x"`                       | API version string             |

Call `conn.close()` when finished to release the underlying session.

### `DublinCoreMetadata`

Pydantic model representing the 15 Dublin Core metadata elements (title, creator, subject, description, publisher, contributor, date, type, format, identifier, source, language, relation, coverage, rights).

| Method                                                       | Description                                                     |
| ------------------------------------------------------------ | --------------------------------------------------------------- |
| `from_koordinates(conn, layer_id)`                           | Fetch metadata from the Koordinates API                         |
| `populate_template(conn, layer_id)`                          | Create a metadata template pre-filled from layer details        |
| `edit_metadata_fields(**kwargs)`                             | Update one or more metadata fields                              |
| `update_source_field(conn, layer_ids, version_ids)`          | Set the source field to specific layer/version pairs            |
| `update_source_with_latest_layer_versions(conn, layer_ids)`  | Set the source field using the latest version of each layer     |
| `as_xml()`                                                   | Return metadata as an OAI_DC XML string                         |
| `to_xml(path)`                                               | Write metadata to an XML file                                   |
| `from_raw_xml(xml)`                                          | Parse an OAI_DC XML string into a `DublinCoreMetadata` instance |

## License

MIT License
