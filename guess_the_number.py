#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random
from collections.abc import Callable


LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_TRIES = 7

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def in_range(value: int) -> bool:
    return LOWER_BOUND <= value <= UPPER_BOUND


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def prompt_guess(
    tries_left: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int | None:
    raw = input_fn(f"Tries left: {tries_left}. Your guess: ").strip()
    if not raw.isdigit():
        output_fn("Please enter a positive whole number.\n")
        return None

    guess = int(raw)
    if not in_range(guess):
        output_fn(
            f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}.\n"
        )
        return None

    return guess


def play_game(
    secret: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    tries_left = MAX_TRIES
    output_fn(
        f"Guess an integer from {LOWER_BOUND} to {UPPER_BOUND}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        guess = prompt_guess(tries_left, input_fn, output_fn)
        if guess is None:
            continue

        if guess == secret:
            output_fn("Correct! You win.\n")
            return

        output_fn(f"{hint_for_guess(guess, secret)}\n")

        tries_left -= 1

    output_fn(f"No tries left. The number was {secret}.\n")


def main() -> None:
    play_game(random.randint(LOWER_BOUND, UPPER_BOUND))


if __name__ == "__main__":
    main()
