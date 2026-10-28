# Catalog Checker

A small, dependency-free Python command-line tool that checks product catalog CSV files for common data-quality problems before import or publication.

## Features

- Checks required columns: `sku`, `name`, `price`, `image_url`
- Finds missing SKU, product name, price, and image URL
- Detects duplicate SKUs (case-insensitive)
- Validates numeric, non-negative prices
- Checks image URL schemes (`http://` or `https://`)
- Returns a non-zero exit code when issues are found, so it can be used in scripts/CI

## Requirements

- Python 3.10+
- No third-party dependencies

## Quick start

```bash
python catalog_checker.py examples/products.csv
```

## CSV format

```csv
sku,name,price,image_url
STAND-01,Aluminum Laptop Stand,29.99,https://example.com/stand.jpg
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Roadmap

- Optional JSON report output
- Configurable required columns
- More URL and currency validation
- GitHub Actions CI

## Contributing

Issues and pull requests are welcome. Please include a clear reproduction case and tests for behavior changes. Keep the tool dependency-free unless a dependency is justified.

## License

MIT. See [LICENSE](LICENSE).
