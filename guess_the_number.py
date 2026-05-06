#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from collections.abc import Callable
from dataclasses import dataclass
import random

from cli_io import InputFunc, OutputFunc, write_message


@dataclass(frozen=True)
class GameConfig:
    lower_bound: int = 1
    upper_bound: int = 100
    max_tries: int = 7

    def contains(self, guess: int) -> bool:
        return self.lower_bound <= guess <= self.upper_bound


DEFAULT_CONFIG = GameConfig()
RandintFunc = Callable[[int, int], int]


@dataclass(frozen=True)
class GuessParseResult:
    guess: int | None
    error: str | None


def parse_guess(
    raw: str, config: GameConfig = DEFAULT_CONFIG
) -> GuessParseResult:
    if not raw.isdigit():
        return GuessParseResult(None, "Please enter a positive whole number.")

    guess = int(raw)
    if not config.contains(guess):
        return GuessParseResult(
            None,
            f"Out of range; stay between {config.lower_bound} and {config.upper_bound}.",
        )

    return GuessParseResult(guess, None)


def hint_for(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


@dataclass
class GuessingGame:
    config: GameConfig = DEFAULT_CONFIG
    input_func: InputFunc = input
    output_func: OutputFunc = print
    randint_func: RandintFunc = random.randint

    def read_guess(self, tries_left: int) -> int | None:
        result = parse_guess(
            self.input_func(f"Tries left: {tries_left}. Your guess: ").strip(),
            self.config,
        )
        if result.error:
            write_message(self.output_func, result.error)
        return result.guess

    def run(self) -> None:
        secret = self.randint_func(self.config.lower_bound, self.config.upper_bound)
        tries_left = self.config.max_tries
        write_message(
            self.output_func,
            f"Guess an integer from {self.config.lower_bound} "
            f"to {self.config.upper_bound}. You have {self.config.max_tries} tries.",
        )

        while tries_left > 0:
            guess = self.read_guess(tries_left)
            if guess is None:
                continue

            if guess == secret:
                write_message(self.output_func, "Correct! You win.")
                return

            write_message(self.output_func, hint_for(guess, secret))
            tries_left -= 1

        write_message(self.output_func, f"No tries left. The number was {secret}.")


def read_guess(
    tries_left: int,
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> int | None:
    return GuessingGame(config, input_func, output_func).read_guess(tries_left)


def run_game(
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    randint_func: RandintFunc = random.randint,
) -> None:
    GuessingGame(config, input_func, output_func, randint_func).run()


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
