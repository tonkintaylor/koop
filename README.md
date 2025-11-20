# Koop

A package for interfacing with Koordinates.

## Installation

Install the package from PyPI:

```bash
pip install koop
```

## Configuration

The following environment variables are required:

- `KOORDINATES_API_KEY`: Your Koordinates API key.
- `KOOPCACHE_DIR`: Directory to store cached layers.

## Usage

### Get a Layer

You can download and cache a layer using its ID:

```python
from koop import get_layer_from_id

# Returns a Path object to the downloaded Geopackage
layer_path = get_layer_from_id(
    layer_id=123,
    api_key="your-api-key"
)
```

## License

MIT License
