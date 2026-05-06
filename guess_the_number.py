#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random

LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_TRIES = 7


def read_guess(tries_left: int) -> int | None:
    raw = input(f"Tries left: {tries_left}. Your guess: ").strip()
    if not raw.isdigit():
        print("Please enter a positive whole number.\n")
        return None

    guess = int(raw)
    if guess < LOWER_BOUND or guess > UPPER_BOUND:
        print(f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}.\n")
        return None

    return guess


def print_hint(guess: int, secret: int) -> None:
    if guess < secret:
        print("Too low — try something larger.\n")
    else:
        print("Too high — try something smaller.\n")


def main() -> None:
    secret = random.randint(LOWER_BOUND, UPPER_BOUND)
    tries_left = MAX_TRIES
    print(
        f"Guess an integer from {LOWER_BOUND} to {UPPER_BOUND}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        guess = read_guess(tries_left)
        if guess is None:
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print_hint(guess, secret)
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
