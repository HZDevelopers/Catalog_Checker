
# Catalog Checker

A simple Python tool for validating product catalog CSV files.

## Features

- Checks for required columns: `sku`, `name`, `price`, and `image_url`.
- Detects duplicate SKUs.
- Identifies missing or invalid product information.
- Checks for invalid and negative prices.
- Validates image URL formats.
- Supports JSON output for validation results.
- Includes automated unit tests.

## Requirements

- Python 3.10 or newer recommended.
- No third-party packages required.

## Installation

1. Download or clone this repository.
2. Open a terminal in the project directory.
3. Verify Python is installed:

   ```bash
   python --version
   ```

## Usage

Validate the example product catalog:

```bash
python catalog_checker.py examples/products.csv
```

Display validation results in JSON format:

```bash
python catalog_checker.py examples/products.csv --json
```

The tool reports validation issues with the row number, field name, and issue type. If the catalog is valid, it reports that no issues were found.

## CSV Format

Your CSV file should include these columns:

```csv
sku,name,price,image_url
A001,USB Cable,500,https://example.com/usb.jpg
A002,Phone Stand,800,https://example.com/stand.jpg
```

Replace the sample values with your own product data.

## Running Tests

Run the automated test suite from the project directory:

```bash
python -m unittest discover -s tests -v
```

The tests cover valid catalogs, duplicate SKUs, invalid prices, invalid image URLs, and missing required columns.

## Contributing

Contributions, bug reports, and suggestions are welcome. Please test your changes before submitting a pull request.

## License

See the `LICENSE` file for license information.
