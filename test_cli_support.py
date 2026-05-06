import unittest

from cli_support import parse_positive_int


class ParsePositiveIntTests(unittest.TestCase):
    def test_parse_positive_int(self) -> None:
        self.assertEqual(parse_positive_int("42"), 42)
        self.assertIsNone(parse_positive_int("abc"))
        self.assertIsNone(parse_positive_int(""))
        self.assertIsNone(parse_positive_int("0"))
        self.assertIsNone(parse_positive_int("-1"))


if __name__ == "__main__":
    unittest.main()
