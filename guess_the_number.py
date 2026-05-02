#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random

from cli_utils import parse_int_in_range, prompt_line, say


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7
RANGE_TEXT = f"{MIN_NUMBER} to {MAX_NUMBER}"


def prompt_guess(tries_left: int) -> int | None:
    raw = prompt_line(f"Tries left: {tries_left}. Your guess: ")
    guess, error = parse_int_in_range(raw, MIN_NUMBER, MAX_NUMBER, range_text=RANGE_TEXT)
    if error is not None:
        say(error)
        return None

    return guess


def print_hint(guess: int, secret: int) -> None:
    if guess < secret:
        say("Too low; try something larger.")
    else:
        say("Too high; try something smaller.")


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries_left = MAX_TRIES
    say(f"Guess an integer from {RANGE_TEXT}. You have {MAX_TRIES} tries.")

    while tries_left > 0:
        guess = prompt_guess(tries_left)
        if guess is None:
            continue

        if guess == secret:
            say("Correct! You win.")
            return

        print_hint(guess, secret)
        tries_left -= 1

    say(f"No tries left. The number was {secret}.")


if __name__ == "__main__":
    main()
