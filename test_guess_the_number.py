import unittest

import guess_the_number
from test_support import make_script_io


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

    def test_play_game_uses_injected_io(self) -> None:
        input_fn, outputs = make_script_io(["abc", "150", "10"])
        guess_the_number.play_game(
            10,
            input_fn=input_fn,
            output_fn=outputs.append,
        )

        self.assertEqual(
            outputs,
            [
                "Guess an integer from 1 to 100. You have 7 tries.\n",
                "Please enter a positive whole number.\n",
                "Out of range; stay between 1 and 100.\n",
                "Correct! You win.\n",
            ],
        )


if __name__ == "__main__":
    unittest.main()
