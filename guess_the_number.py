#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random


LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_TRIES = 7


def in_range(value: int) -> bool:
    return LOWER_BOUND <= value <= UPPER_BOUND


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def main() -> None:
    secret = random.randint(LOWER_BOUND, UPPER_BOUND)
    tries_left = MAX_TRIES
    print(
        f"Guess an integer from {LOWER_BOUND} to {UPPER_BOUND}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        raw = input(f"Tries left: {tries_left}. Your guess: ").strip()
        if not raw.isdigit():
            print("Please enter a positive whole number.\n")
            continue

        guess = int(raw)
        if not in_range(guess):
            print(
                f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}.\n"
            )
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for_guess(guess, secret)}\n")

        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
