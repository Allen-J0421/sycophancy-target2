#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random

from cli_utils import parse_positive_int, prompt_line, say


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7
RANGE_TEXT = f"{MIN_NUMBER} to {MAX_NUMBER}"


def parse_guess(raw: str) -> tuple[int | None, str | None]:
    guess = parse_positive_int(raw)
    if guess is None:
        return None, "Please enter a positive whole number."

    if guess < MIN_NUMBER or guess > MAX_NUMBER:
        return None, f"Out of range; stay between {RANGE_TEXT}."

    return guess, None


def prompt_guess(tries_left: int) -> int | None:
    raw = prompt_line(f"Tries left: {tries_left}. Your guess: ")
    guess, error = parse_guess(raw)
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
