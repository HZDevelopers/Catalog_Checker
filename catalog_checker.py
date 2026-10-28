"""Validate a product catalog CSV and report common data-quality issues."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Iterable

REQUIRED = ("sku", "name", "price", "image_url")


def validate_rows(rows: Iterable[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    seen_skus: set[str] = set()
    for line, row in enumerate(rows, start=2):
        sku = (row.get("sku") or "").strip()
        name = (row.get("name") or "").strip()
        price = (row.get("price") or "").strip()
        image = (row.get("image_url") or "").strip()
        if not sku:
            issues.append(f"Line {line}: missing SKU")
        elif sku.casefold() in seen_skus:
            issues.append(f"Line {line}: duplicate SKU '{sku}'")
        else:
            seen_skus.add(sku.casefold())
        if not name:
            issues.append(f"Line {line}: missing product name")
        try:
            value = float(price)
            if value < 0:
                issues.append(f"Line {line}: price cannot be negative")
        except (TypeError, ValueError):
            issues.append(f"Line {line}: price must be a number")
        if image and not image.startswith(("https://", "http://")):
            issues.append(f"Line {line}: image_url must start with http:// or https://")
        if not image:
            issues.append(f"Line {line}: missing image_url")
    return issues


def check_file(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = {h.strip().lower() for h in (reader.fieldnames or [])}
        missing = [field for field in REQUIRED if field not in headers]
        if missing:
            return ["Missing required CSV columns: " + ", ".join(missing)]
        normalized = ({(k or "").strip().lower(): (v or "") for k, v in row.items()} for row in reader)
        return validate_rows(normalized)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a product catalog CSV for common data issues.")
    parser.add_argument("csv_file", type=Path, help="Path to catalog CSV")
    args = parser.parse_args()
    if not args.csv_file.is_file():
        parser.error(f"File not found: {args.csv_file}")
    issues = check_file(args.csv_file)
    if issues:
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Catalog looks good: no issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
