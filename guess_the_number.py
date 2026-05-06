#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from collections.abc import Callable
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class GameConfig:
    lower_bound: int = 1
    upper_bound: int = 100
    max_tries: int = 7

    def contains(self, guess: int) -> bool:
        return self.lower_bound <= guess <= self.upper_bound


DEFAULT_CONFIG = GameConfig()
InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]
RandintFunc = Callable[[int, int], int]


def parse_guess(
    raw: str, config: GameConfig = DEFAULT_CONFIG
) -> tuple[int | None, str | None]:
    if not raw.isdigit():
        return None, "Please enter a positive whole number."

    guess = int(raw)
    if not config.contains(guess):
        return (
            None,
            f"Out of range; stay between {config.lower_bound} and {config.upper_bound}.",
        )

    return guess, None


def write_message(output_func: OutputFunc, message: str) -> None:
    output_func(f"{message}\n")


def read_guess(
    tries_left: int,
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> int | None:
    guess, error = parse_guess(
        input_func(f"Tries left: {tries_left}. Your guess: ").strip(), config
    )
    if error:
        write_message(output_func, error)
    return guess


def hint_for(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def run_game(
    config: GameConfig = DEFAULT_CONFIG,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    randint_func: RandintFunc = random.randint,
) -> None:
    secret = randint_func(config.lower_bound, config.upper_bound)
    tries_left = config.max_tries
    write_message(
        output_func,
        f"Guess an integer from {config.lower_bound} to {config.upper_bound}. "
        f"You have {config.max_tries} tries.",
    )

    while tries_left > 0:
        guess = read_guess(tries_left, config, input_func, output_func)
        if guess is None:
            continue

        if guess == secret:
            write_message(output_func, "Correct! You win.")
            return

        write_message(output_func, hint_for(guess, secret))
        tries_left -= 1

    write_message(output_func, f"No tries left. The number was {secret}.")


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
