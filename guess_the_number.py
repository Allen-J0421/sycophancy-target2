#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class GameConfig:
    lower_bound: int = 1
    upper_bound: int = 100
    max_tries: int = 7

    def contains(self, guess: int) -> bool:
        return self.lower_bound <= guess <= self.upper_bound


DEFAULT_CONFIG = GameConfig()


def parse_guess(
    raw: str, config: GameConfig = DEFAULT_CONFIG
) -> tuple[int | None, str | None]:
    if not raw.isdigit():
        return None, "Please enter a positive whole number."

    guess = int(raw)
    if not config.contains(guess):
        return (
            None,
            f"Out of range; stay between {config.lower_bound} and {config.upper_bound}.",
        )

    return guess, None


def read_guess(tries_left: int, config: GameConfig = DEFAULT_CONFIG) -> int | None:
    guess, error = parse_guess(
        input(f"Tries left: {tries_left}. Your guess: ").strip(), config
    )
    if error:
        print(f"{error}\n")
    return guess


def hint_for(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def run_game(config: GameConfig = DEFAULT_CONFIG) -> None:
    secret = random.randint(config.lower_bound, config.upper_bound)
    tries_left = config.max_tries
    print(
        f"Guess an integer from {config.lower_bound} to {config.upper_bound}. "
        f"You have {config.max_tries} tries.\n"
    )

    while tries_left > 0:
        guess = read_guess(tries_left, config)
        if guess is None:
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for(guess, secret)}\n")
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
