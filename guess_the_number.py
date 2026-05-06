#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random
from dataclasses import dataclass

from cli_support import InputFn, OutputFn, parse_positive_int


LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_TRIES = 7


def in_range(value: int) -> bool:
    return LOWER_BOUND <= value <= UPPER_BOUND


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def _prompt_guess(
    tries_left: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int | None:
    raw = input_fn(f"Tries left: {tries_left}. Your guess: ").strip()
    guess = parse_positive_int(raw)
    if guess is None:
        output_fn("Please enter a positive whole number.\n")
        return None

    if not in_range(guess):
        output_fn(
            f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}.\n"
        )
        return None

    return guess


def prompt_guess(
    tries_left: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int | None:
    return _prompt_guess(tries_left, input_fn, output_fn)


@dataclass
class GuessingGame:
    secret: int
    tries_left: int = MAX_TRIES
    input_fn: InputFn = input
    output_fn: OutputFn = print

    def prompt_guess(self) -> int | None:
        return _prompt_guess(self.tries_left, self.input_fn, self.output_fn)

    def play(self) -> None:
        self.output_fn(
            f"Guess an integer from {LOWER_BOUND} to {UPPER_BOUND}. "
            f"You have {MAX_TRIES} tries.\n"
        )

        while self.tries_left > 0:
            guess = self.prompt_guess()
            if guess is None:
                continue

            if guess == self.secret:
                self.output_fn("Correct! You win.\n")
                return

            self.output_fn(f"{hint_for_guess(guess, self.secret)}\n")

            self.tries_left -= 1

        self.output_fn(f"No tries left. The number was {self.secret}.\n")


def play_game(
    secret: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    GuessingGame(secret=secret, input_fn=input_fn, output_fn=output_fn).play()


def main() -> None:
    play_game(random.randint(LOWER_BOUND, UPPER_BOUND))


if __name__ == "__main__":
    main()
