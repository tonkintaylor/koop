<h1 align="center">
  <img src="https://github.com/user-attachments/assets/bbf2e050-449f-43c3-90df-14e2cc3060d2"><br>
</h1>

# koop

[![PyPI Version](https://img.shields.io/pypi/v/koop.svg)](https://pypi.python.org/pypi/koop)
[![PyPI Supported Versions](https://img.shields.io/pypi/pyversions/koop.svg)](https://pypi.python.org/pypi/koop)
![PyPI License](https://img.shields.io/pypi/l/koop.svg)

A Python package for interfacing with the Koordinates API, enabling seamless download and caching of geospatial layers with metadata management.

## Overview

`koop` provides a simple and efficient interface for working with Koordinates, a leading geospatial data management platform. Download layers, manage metadata, and integrate with your geospatial workflows.

### Features

- 📥 **Automatic layer downloading**: Download and cache layers from Koordinates using layer IDs.
- 🗄️ **Smart caching**: Automatically cache downloaded layers to avoid redundant downloads.
- 📋 **Metadata management**: Extract, edit, and manage Dublin Core compliant metadata.
- 🔐 **API authentication**: Secure connection management with API key authentication.
- 🌐 **Multi-domain support**: Connect to different Koordinates domains (e.g., LINZ, custom instances).
- 🗂️ **GeoPackage export**: All layers are exported as GeoPackage files for easy integration.

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

## API Reference

### Main Functions

- `get_layer_from_id(layer_id, api_key, domain="ttgroup.koordinates.com")`: Download and cache a layer by ID

### Connection

- `KoordinatesConnection(api_key, domain, api_version)`: Create an authenticated connection to Koordinates API

### Metadata

- `DublinCoreMetadata.from_koordinates(conn, layer_id)`: Fetch metadata from Koordinates
- `DublinCoreMetadata.populate_template(conn, layer_id)`: Create metadata template from layer details
- `DublinCoreMetadata.edit_metadata_fields(**kwargs)`: Update metadata fields
- `DublinCoreMetadata.update_source_field(conn, layer_ids, version_ids)`: Update source field with specific versions
- `DublinCoreMetadata.update_source_with_latest_layer_versions(conn, layer_ids)`: Update source with latest versions
- `DublinCoreMetadata.to_xml(path)`: Export metadata to XML file
- `DublinCoreMetadata.as_xml()`: Get metadata as XML string

## License

MIT License
