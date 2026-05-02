#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7


def intro_message() -> str:
    return (
        f"Guess an integer from {MIN_NUMBER} to {MAX_NUMBER}. "
        f"You have {MAX_TRIES} tries.\n"
    )


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


def read_guess(tries_left: int) -> int | None:
    return parse_guess(input(f"Tries left: {tries_left}. Your guess: "))


def print_invalid_guess() -> None:
    print("Please enter a positive whole number.\n")


def print_out_of_range() -> None:
    print(f"Out of range; stay between {MIN_NUMBER} and {MAX_NUMBER}.\n")


def main() -> None:
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries_left = MAX_TRIES
    print(intro_message())

    while tries_left > 0:
        guess = read_guess(tries_left)
        if guess is None:
            print_invalid_guess()
            continue

        if not is_in_range(guess):
            print_out_of_range()
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for_guess(guess, secret)}\n")
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
