import unittest
from catalog_checker import validate_rows


class CatalogValidationTests(unittest.TestCase):
    def test_valid_row(self):
        self.assertEqual(validate_rows([{"sku":"A1", "name":"Stand", "price":"12.5", "image_url":"https://example.com/a.png"}]), [])

    def test_missing_and_duplicate_sku(self):
        rows = [
            {"sku":"X", "name":"One", "price":"1", "image_url":"https://x.test/1"},
            {"sku":"x", "name":"Two", "price":"2", "image_url":"https://x.test/2"},
            {"sku":"", "name":"Three", "price":"3", "image_url":"https://x.test/3"},
        ]
        issues = validate_rows(rows)
        self.assertTrue(any("duplicate SKU" in issue for issue in issues))
        self.assertTrue(any("missing SKU" in issue for issue in issues))

    def test_bad_price_and_image(self):
        issues = validate_rows([{"sku":"A", "name":"Item", "price":"free", "image_url":"ftp://image"}])
        self.assertTrue(any("price must be a number" in issue for issue in issues))
        self.assertTrue(any("image_url must start" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
