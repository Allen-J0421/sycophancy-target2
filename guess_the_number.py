#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7


def prompt_guess(tries_left: int) -> int | None:
    raw = input(f"Tries left: {tries_left}. Your guess: ").strip()
    if not raw.isdigit():
        print("Please enter a positive whole number.\n")
        return None

    guess = int(raw)
    if guess < MIN_NUMBER or guess > MAX_NUMBER:
        print("Out of range; stay between 1 and 100.\n")
        return None

    return guess


def print_hint(guess: int, secret: int) -> None:
    if guess < secret:
        print("Too low; try something larger.\n")
    else:
        print("Too high; try something smaller.\n")


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries_left = MAX_TRIES
    print(
        f"Guess an integer from {MIN_NUMBER} to {MAX_NUMBER}. "
        f"You have {MAX_TRIES} tries.\n"
    )

    while tries_left > 0:
        guess = prompt_guess(tries_left)
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
