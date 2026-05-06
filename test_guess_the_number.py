import unittest

import guess_the_number as gtn


class TestGuessTheNumber(unittest.TestCase):
    def test_parse_guess_valid(self) -> None:
        self.assertEqual(gtn.parse_guess("1"), 1)
        self.assertEqual(gtn.parse_guess(" 42 "), 42)
        self.assertEqual(gtn.parse_guess("100"), 100)

    def test_parse_guess_rejects_non_digit(self) -> None:
        with self.assertRaises(ValueError):
            gtn.parse_guess("")
        with self.assertRaises(ValueError):
            gtn.parse_guess("  ")
        with self.assertRaises(ValueError):
            gtn.parse_guess("nope")
        with self.assertRaises(ValueError):
            gtn.parse_guess("-1")

    def test_parse_guess_rejects_out_of_range(self) -> None:
        with self.assertRaises(ValueError):
            gtn.parse_guess("0")
        with self.assertRaises(ValueError):
            gtn.parse_guess("101")

    def test_hint_for_guess(self) -> None:
        self.assertIn("Too low", gtn.hint_for_guess(guess=10, secret=20))
        self.assertIn("Too high", gtn.hint_for_guess(guess=30, secret=20))


if __name__ == "__main__":
    unittest.main()

