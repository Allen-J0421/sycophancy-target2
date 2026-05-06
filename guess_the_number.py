#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random

LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_TRIES = 7


def parse_guess(raw: str) -> tuple[int | None, str | None]:
    if not raw.isdigit():
        return None, "Please enter a positive whole number."

    guess = int(raw)
    if guess < LOWER_BOUND or guess > UPPER_BOUND:
        return None, f"Out of range; stay between {LOWER_BOUND} and {UPPER_BOUND}."

    return guess, None


def read_guess(tries_left: int) -> int | None:
    guess, error = parse_guess(input(f"Tries left: {tries_left}. Your guess: ").strip())
    if error:
        print(f"{error}\n")
    return guess


def hint_for(guess: int, secret: int) -> str:
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
        guess = read_guess(tries_left)
        if guess is None:
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for(guess, secret)}\n")
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
