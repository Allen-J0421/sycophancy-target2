#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random

from cli_utils import parse_int_in_range, prompt_line, say


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7
RANGE_TEXT = f"{MIN_NUMBER} to {MAX_NUMBER}"


def prompt_guess(tries_left: int) -> int | None:
    guess, error = parse_int_in_range(
        prompt_line(f"Tries left: {tries_left}. Your guess: "),
        MIN_NUMBER,
        MAX_NUMBER,
        range_text=RANGE_TEXT,
    )
    if error is not None:
        say(error)
        return None

    return guess


def guess_feedback(guess: int, secret: int) -> str:
    return (
        "Too low; try something larger."
        if guess < secret
        else "Too high; try something smaller."
    )


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    say(f"Guess an integer from {RANGE_TEXT}. You have {MAX_TRIES} tries.")

    for tries_left in range(MAX_TRIES, 0, -1):
        guess = prompt_guess(tries_left)
        if guess is None:
            continue

        if guess == secret:
            say("Correct! You win.")
            return

        say(guess_feedback(guess, secret))

    say(f"No tries left. The number was {secret}.")


if __name__ == "__main__":
    main()
