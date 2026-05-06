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

    def test_play_round_injected_io(self) -> None:
        inputs = iter(["nope", "0", "49", "50"])
        outputs: list[str] = []

        def input_fn(_prompt: str) -> str:
            return next(inputs)

        def output_fn(line: str) -> None:
            outputs.append(line)

        gtn.play_round(secret=50, tries=2, input_fn=input_fn, output_fn=output_fn)

        # Should include at least one error message, a hint, and the win message.
        self.assertTrue(any("Please enter a positive whole number" in o for o in outputs))
        self.assertTrue(any("Out of range" in o for o in outputs))
        self.assertTrue(any("Too low" in o for o in outputs))
        self.assertTrue(any(o == "Correct! You win." for o in outputs))

    def test_play_round_eof_exits_gracefully(self) -> None:
        outputs: list[str] = []

        def input_fn(_prompt: str) -> str:
            raise EOFError

        def output_fn(line: str) -> None:
            outputs.append(line)

        gtn.play_round(secret=50, tries=1, input_fn=input_fn, output_fn=output_fn)
        self.assertIn("Goodbye.", outputs)


if __name__ == "__main__":
    unittest.main()
