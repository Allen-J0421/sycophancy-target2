#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7


def read_guess(*, tries_left: int) -> int:
    while True:
        raw = input(f"Tries left: {tries_left}. Your guess: ").strip()
        if not raw.isdigit():
            print("Please enter a positive whole number.\n")
            continue

        guess = int(raw)
        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            print(f"Out of range; stay between {MIN_NUMBER} and {MAX_NUMBER}.\n")
            continue

        return guess


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries_left = MAX_TRIES
    print(
        f"Guess an integer from {MIN_NUMBER} to {MAX_NUMBER}. You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        guess = read_guess(tries_left=tries_left)
        if guess == secret:
            print("Correct! You win.\n")
            return

        if guess < secret:
            print("Too low — try something larger.\n")
        else:
            print("Too high — try something smaller.\n")

        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
