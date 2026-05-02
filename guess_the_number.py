#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

import random


def main() -> None:
    secret = random.randint(1, 100)
    tries_left = 7
    print("Guess an integer from 1 to 100. You have 7 tries.\n")

    while tries_left > 0:
        raw = input(f"Tries left: {tries_left}. Your guess: ").strip()
        if not raw.isdigit():
            print("Please enter a positive whole number.\n")
            continue

        guess = int(raw)
        if guess < 1 or guess > 100:
            print("Out of range; stay between 1 and 100.\n")
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        if guess < secret:
            print("Too high — try something smaller.\n")
        else:
            print("Too low — try something larger.\n")

        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
