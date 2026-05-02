#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7


def parse_guess(raw: str) -> int | None:
    stripped = raw.strip()
    if not stripped.isdigit():
        return None
    return int(stripped)


def is_in_range(guess: int) -> bool:
    return MIN_NUMBER <= guess <= MAX_NUMBER


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low - try something larger."
    return "Too high - try something smaller."


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries_left = MAX_TRIES
    print(
        f"Guess an integer from {MIN_NUMBER} to {MAX_NUMBER}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        guess = parse_guess(input(f"Tries left: {tries_left}. Your guess: "))
        if guess is None:
            print("Please enter a positive whole number.\n")
            continue

        if not is_in_range(guess):
            print(f"Out of range; stay between {MIN_NUMBER} and {MAX_NUMBER}.\n")
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for_guess(guess, secret)}\n")
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
