import unittest

from catalog_checker import validate_rows


class CatalogCheckerTests(unittest.TestCase):
    def test_valid_catalog_has_no_issues(self):
        headers = ["sku", "name", "price", "image_url"]
        rows = [
            {
                "sku": "SKU-001",
                "name": "USB-C Cable",
                "price": "9.99",
                "image_url": "https://example.com/cable.jpg",
            }
        ]
        self.assertEqual(validate_rows(headers, rows), [])

    def test_duplicate_sku_is_reported(self):
        headers = ["sku", "name", "price", "image_url"]
        rows = [
            {"sku": "A", "name": "First", "price": "1", "image_url": "https://example.com/1.jpg"},
            {"sku": "A", "name": "Second", "price": "2", "image_url": "https://example.com/2.jpg"},
        ]
        issues = validate_rows(headers, rows)
        self.assertIn("duplicate_sku", [issue.code for issue in issues])

    def test_invalid_price_and_image_url_are_reported(self):
        headers = ["sku", "name", "price", "image_url"]
        rows = [
            {"sku": "A", "name": "Item", "price": "free", "image_url": "not-a-url"}
        ]
        issues = validate_rows(headers, rows)
        codes = [issue.code for issue in issues]
        self.assertIn("invalid_price", codes)
        self.assertIn("invalid_image_url", codes)

    def test_missing_required_column_is_reported(self):
        issues = validate_rows(["sku", "name"], [])
        self.assertIn("missing_column", [issue.code for issue in issues])


if __name__ == "__main__":
    unittest.main()
