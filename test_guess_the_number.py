import unittest

from guess_the_number import GameConfig, hint_for, parse_guess, run_game


class GuessTheNumberTests(unittest.TestCase):
    def test_parse_guess_uses_config_bounds(self) -> None:
        config = GameConfig(lower_bound=10, upper_bound=20, max_tries=3)

        self.assertEqual(parse_guess("15", config), (15, None))
        self.assertEqual(parse_guess("abc", config)[0], None)
        self.assertEqual(parse_guess("9", config)[0], None)

    def test_hint_for_compares_guess_to_secret(self) -> None:
        self.assertTrue(hint_for(3, 5).startswith("Too low"))
        self.assertTrue(hint_for(7, 5).startswith("Too high"))

    def test_run_game_accepts_injected_io_and_randomness(self) -> None:
        answers = iter(["x", "3", "5"])
        prompts: list[str] = []
        output: list[str] = []

        def input_func(prompt: str) -> str:
            prompts.append(prompt)
            return next(answers)

        run_game(
            GameConfig(lower_bound=1, upper_bound=10, max_tries=3),
            input_func=input_func,
            output_func=output.append,
            randint_func=lambda lower, upper: 5,
        )

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
