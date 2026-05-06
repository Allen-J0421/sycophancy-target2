import unittest

import guess_the_number
from test_support import ScriptIO


class GuessTheNumberTests(unittest.TestCase):
    def test_hint_for_guess(self) -> None:
        self.assertEqual(
            guess_the_number.hint_for_guess(10, 20),
            "Too low — try something larger.",
        )
        self.assertEqual(
            guess_the_number.hint_for_guess(30, 20),
            "Too high — try something smaller.",
        )

    def test_validate_guess(self) -> None:
        self.assertEqual(guess_the_number.validate_guess("10"), (10, None))
        self.assertEqual(
            guess_the_number.validate_guess("abc"),
            (None, "Please enter a positive whole number.\n"),
        )
        self.assertEqual(
            guess_the_number.validate_guess("150"),
            (None, "Out of range; stay between 1 and 100.\n"),
        )

    def test_play_game_uses_injected_io(self) -> None:
        io = ScriptIO(["abc", "150", "10"])
        guess_the_number.play_game(
            10,
            input_fn=io,
            output_fn=io.write,
        )

        self.assertEqual(
            io.outputs,
            [
                "Guess an integer from 1 to 100. You have 7 tries.\n",
                "Please enter a positive whole number.\n",
                "Out of range; stay between 1 and 100.\n",
                "Correct! You win.\n",
            ],
        )
        self.assertEqual(
            io.prompts,
            [
                "Tries left: 7. Your guess: ",
                "Tries left: 7. Your guess: ",
                "Tries left: 7. Your guess: ",
            ],
        )


if __name__ == "__main__":
    unittest.main()
