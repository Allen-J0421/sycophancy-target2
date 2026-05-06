#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from __future__ import annotations

from collections.abc import Callable
import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def parse_guess(raw: str, *, min_value: int = MIN_NUMBER, max_value: int = MAX_NUMBER) -> int:
    raw = raw.strip()
    if not raw.isdigit():
        raise ValueError("Please enter a positive whole number.")

    guess = int(raw)
    if guess < min_value or guess > max_value:
        raise ValueError(f"Out of range; stay between {min_value} and {max_value}.")

    return guess


def hint_for_guess(*, guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def play_round(
    *,
    secret: int,
    tries: int = MAX_TRIES,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    output_fn(f"Guess an integer from {MIN_NUMBER} to {MAX_NUMBER}. You have {tries} tries.")
    output_fn("")
    tries_left = tries

    while tries_left > 0:
        try:
            guess = parse_guess(input_fn(f"Tries left: {tries_left}. Your guess: "))
        except ValueError as exc:
            output_fn(str(exc))
            output_fn("")
            continue

        if guess == secret:
            output_fn("Correct! You win.")
            output_fn("")
            return

        output_fn(hint_for_guess(guess=guess, secret=secret))
        output_fn("")
        tries_left -= 1

    output_fn(f"No tries left. The number was {secret}.")
    output_fn("")


def main() -> None:
    play_round(secret=random.randint(MIN_NUMBER, MAX_NUMBER), tries=MAX_TRIES)


if __name__ == "__main__":
    main()
