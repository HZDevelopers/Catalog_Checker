# Catalog Checker

A small, dependency-free Python command-line tool that checks product catalog CSV files for common data-quality problems.

## What it checks

- Required columns: `sku`, `name`, `price`, and `image_url`
- Empty SKU and product names
- Duplicate SKUs
- Missing, non-numeric, or negative prices
- Missing image URLs and URLs that do not start with `http://` or `https://`

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Quick start

Clone the repository, then run:

```bash
python catalog_checker.py examples/products.csv
```

To receive machine-readable output:

```bash
python catalog_checker.py examples/products.csv --json
```

Exit codes:
- `0`: no issues found
- `1`: validation issues found
- `2`: the file could not be read

## CSV format

The header row must contain these columns (column names are case-insensitive):

```csv
sku,name,price,image_url
SKU-001,USB-C Cable,9.99,https://example.com/cable.jpg
SKU-002,Desk Stand,24.50,https://example.com/stand.jpg
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Limitations

This tool validates CSV structure and basic values only. It does not download image URLs, verify that a product exists, or connect to any store platform.

## Contributing

Issues and pull requests are welcome. Please include a focused test for bug fixes and new validation rules.

## License

Released under the MIT License. See [LICENSE](LICENSE).
