#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random

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


def validate_guess(raw: str) -> tuple[int | None, str | None]:
    guess = parse_positive_int(raw)
    if guess is None:
        return None, "Please enter a positive whole number.\n"

    if not in_range(guess):
        return None, (
            f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}.\n"
        )

    return guess, None


def prompt_guess(
    tries_left: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int | None:
    raw = input_fn(f"Tries left: {tries_left}. Your guess: ").strip()
    guess, message = validate_guess(raw)
    if message is not None:
        output_fn(message)
        return None

    return guess


def respond_to_guess(
    guess: int,
    secret: int,
    output_fn: OutputFn = print,
) -> bool:
    if guess == secret:
        output_fn("Correct! You win.\n")
        return True

    output_fn(f"{hint_for_guess(guess, secret)}\n")
    return False


def play_game(
    secret: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    output_fn(
        f"Guess an integer from {LOWER_BOUND} to {UPPER_BOUND}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    tries_left = MAX_TRIES
    while tries_left > 0:
        guess = prompt_guess(tries_left, input_fn, output_fn)
        if guess is None:
            continue

        if respond_to_guess(guess, secret, output_fn):
            return

        tries_left -= 1

    output_fn(f"No tries left. The number was {secret}.\n")


def main() -> None:
    play_game(random.randint(LOWER_BOUND, UPPER_BOUND))


if __name__ == "__main__":
    main()
