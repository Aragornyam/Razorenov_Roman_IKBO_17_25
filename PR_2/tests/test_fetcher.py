import unittest
from core.fetcher import clean_version


class TestFetcher(unittest.TestCase):
    def test_clean_version(self):
        self.assertEqual(clean_version("^1.2.3"), "1.2.3")
        self.assertEqual(clean_version("~4.5.0"), "4.5.0")
        self.assertEqual(clean_version("latest"), "latest")
        self.assertEqual(clean_version("invalid_ver"), "latest")


if __name__ == "__main__":
    unittest.main()
