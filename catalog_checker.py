#!/usr/bin/env python3
"""Validate product catalog CSV files for common data-quality issues."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = {"sku", "name", "price", "image_url"}
URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)


@dataclass
class Issue:
    row: int
    field: str
    code: str
    message: str


def validate_rows(headers: list[str], rows: Iterable[dict[str, str]]) -> list[Issue]:
    """Return validation issues for CSV rows. Row numbers include the header row."""
    normalized_headers = {header.strip().lower() for header in headers if header}
    issues: list[Issue] = []

    for missing in sorted(REQUIRED_COLUMNS - normalized_headers):
        issues.append(Issue(1, missing, "missing_column", f"Required column '{missing}' is missing."))

    seen_skus: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        normalized = {(key or "").strip().lower(): (value or "").strip() for key, value in row.items()}
        sku = normalized.get("sku", "")
        name = normalized.get("name", "")
        price = normalized.get("price", "")
        image_url = normalized.get("image_url", "")

        if not sku:
            issues.append(Issue(row_number, "sku", "empty_sku", "SKU must not be empty."))
        elif sku in seen_skus:
            issues.append(Issue(row_number, "sku", "duplicate_sku", f"SKU '{sku}' is duplicated."))
        else:
            seen_skus.add(sku)

        if not name:
            issues.append(Issue(row_number, "name", "empty_name", "Product name must not be empty."))

        if not price:
            issues.append(Issue(row_number, "price", "empty_price", "Price must not be empty."))
        else:
            try:
                numeric_price = float(price)
                if numeric_price < 0:
                    issues.append(Issue(row_number, "price", "negative_price", "Price must not be negative."))
            except ValueError:
                issues.append(Issue(row_number, "price", "invalid_price", f"Price '{price}' is not a valid number."))

        if not image_url:
            issues.append(Issue(row_number, "image_url", "empty_image_url", "Image URL must not be empty."))
        elif not URL_PATTERN.match(image_url):
            issues.append(Issue(row_number, "image_url", "invalid_image_url", "Image URL must start with http:// or https://."))

    return issues


def check_csv(path: str | Path) -> list[Issue]:
    """Read and validate a CSV file."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        return validate_rows(headers, reader)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a product catalog CSV for common data issues.")
    parser.add_argument("csv_file", help="Path to the product catalog CSV file")
    parser.add_argument("--json", action="store_true", help="Print issues as JSON")
    args = parser.parse_args(argv)

    try:
        issues = check_csv(args.csv_file)
    except (OSError, csv.Error) as exc:
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(issue) for issue in issues], indent=2))
    elif not issues:
        print("Catalog looks good: no issues found.")
    else:
        for issue in issues:
            print(f"Row {issue.row} [{issue.field}] {issue.code}: {issue.message}")
        print(f"\nFound {len(issues)} issue(s).")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
