import unittest

from guess_the_number import (
    GameConfig,
    GuessingGame,
    GuessParseResult,
    hint_for,
    intro_message,
    loss_message,
    out_of_range_message,
    parse_guess,
    prompt_for_guess,
)


class GuessTheNumberTests(unittest.TestCase):
    def test_parse_guess_uses_config_bounds(self) -> None:
        config = GameConfig(lower_bound=10, upper_bound=20, max_tries=3)

        self.assertEqual(parse_guess("15", config), GuessParseResult.valid(15))
        self.assertIsNone(parse_guess("abc", config).guess)
        self.assertIsNone(parse_guess("9", config).guess)

    def test_hint_for_compares_guess_to_secret(self) -> None:
        self.assertTrue(hint_for(3, 5).startswith("Too low"))
        self.assertTrue(hint_for(7, 5).startswith("Too high"))

    def test_message_helpers_use_configured_values(self) -> None:
        config = GameConfig(lower_bound=10, upper_bound=20, max_tries=3)

        self.assertEqual(
            intro_message(config),
            "Guess an integer from 10 to 20. You have 3 tries.",
        )
        self.assertEqual(
            out_of_range_message(config),
            "Out of range; stay between 10 and 20.",
        )
        self.assertEqual(prompt_for_guess(2), "Tries left: 2. Your guess: ")
        self.assertEqual(loss_message(17), "No tries left. The number was 17.")

    def test_run_game_accepts_injected_io_and_randomness(self) -> None:
        answers = iter(["x", "3", "5"])
        prompts: list[str] = []
        output: list[str] = []

        def input_func(prompt: str) -> str:
            prompts.append(prompt)
            return next(answers)

        game = GuessingGame(
            config=GameConfig(lower_bound=1, upper_bound=10, max_tries=3),
            input_func=input_func,
            output_func=output.append,
            randint_func=lambda lower, upper: 5,
        )
        game.run()

        self.assertEqual(
            prompts,
            [
                "Tries left: 3. Your guess: ",
                "Tries left: 3. Your guess: ",
                "Tries left: 2. Your guess: ",
            ],
        )
        self.assertEqual(output[-1], "Correct! You win.\n")


if __name__ == "__main__":
    unittest.main()
