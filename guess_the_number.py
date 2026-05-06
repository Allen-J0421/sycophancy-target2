#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import random

from cli_io import InputFunc, OutputFunc, read_prompt, write_message


@dataclass(frozen=True)
class GameConfig:
    lower_bound: int = 1
    upper_bound: int = 100
    max_tries: int = 7

    def contains(self, guess: int) -> bool:
        return self.lower_bound <= guess <= self.upper_bound


DEFAULT_CONFIG = GameConfig()
RandintFunc = Callable[[int, int], int]

INVALID_NUMBER_MESSAGE = "Please enter a positive whole number."
WIN_MESSAGE = "Correct! You win."


def intro_message(config: GameConfig) -> str:
    return (
        f"Guess an integer from {config.lower_bound} to {config.upper_bound}. "
        f"You have {config.max_tries} tries."
    )


def out_of_range_message(config: GameConfig) -> str:
    return f"Out of range; stay between {config.lower_bound} and {config.upper_bound}."


def prompt_for_guess(tries_left: int) -> str:
    return f"Tries left: {tries_left}. Your guess: "


def loss_message(secret: int) -> str:
    return f"No tries left. The number was {secret}."


@dataclass(frozen=True)
class GuessParseResult:
    guess: int | None
    error: str | None

    @classmethod
    def valid(cls, guess: int) -> GuessParseResult:
        return cls(guess, None)

    @classmethod
    def invalid(cls, error: str) -> GuessParseResult:
        return cls(None, error)


def parse_guess(
    raw: str, config: GameConfig = DEFAULT_CONFIG
) -> GuessParseResult:
    if not raw.isdigit():
        return GuessParseResult.invalid(INVALID_NUMBER_MESSAGE)

    guess = int(raw)
    if not config.contains(guess):
        return GuessParseResult.invalid(out_of_range_message(config))

    return GuessParseResult.valid(guess)


def hint_for(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


@dataclass(frozen=True)
class GuessingGame:
    config: GameConfig = DEFAULT_CONFIG
    input_func: InputFunc = input
    output_func: OutputFunc = print
    randint_func: RandintFunc = random.randint

    def read_guess(self, tries_left: int) -> int | None:
        result = parse_guess(
            read_prompt(self.input_func, prompt_for_guess(tries_left)),
            self.config,
        )
        if result.error:
            write_message(self.output_func, result.error)
        return result.guess

    def run(self) -> None:
        secret = self.randint_func(self.config.lower_bound, self.config.upper_bound)
        tries_left = self.config.max_tries
        write_message(self.output_func, intro_message(self.config))

        while tries_left > 0:
            guess = self.read_guess(tries_left)
            if guess is None:
                continue

            if guess == secret:
                write_message(self.output_func, WIN_MESSAGE)
                return

            write_message(self.output_func, hint_for(guess, secret))
            tries_left -= 1

        write_message(self.output_func, loss_message(secret))


def read_guess(
    tries_left: int,
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> int | None:
    return GuessingGame(
        config=config,
        input_func=input_func,
        output_func=output_func,
    ).read_guess(tries_left)


def run_game(
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    randint_func: RandintFunc = random.randint,
) -> None:
    GuessingGame(
        config=config,
        input_func=input_func,
        output_func=output_func,
        randint_func=randint_func,
    ).run()


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
