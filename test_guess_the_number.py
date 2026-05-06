import unittest

from cli_support import ConsoleIO
import guess_the_number


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
        inputs = iter(["abc", "150", "10"])
        outputs: list[str] = []
        io = ConsoleIO(
            input_fn=lambda prompt: next(inputs),
            output_fn=outputs.append,
        )

        guess_the_number.play_game(10, input_fn=io.input_fn, output_fn=io.output_fn)

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
