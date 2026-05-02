#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol


class RandomSource(Protocol):
    def randint(self, a: int, b: int) -> int: ...


@dataclass(frozen=True)
class GameConfig:
    minimum: int = 1
    maximum: int = 100
    max_tries: int = 7

    def includes(self, guess: int) -> bool:
        return self.minimum <= guess <= self.maximum


CONFIG = GameConfig()
MIN_NUMBER = CONFIG.minimum
MAX_NUMBER = CONFIG.maximum
MAX_TRIES = CONFIG.max_tries


def intro_message(config: GameConfig = CONFIG) -> str:
    return (
        f"Guess an integer from {config.minimum} to {config.maximum}. "
        f"You have {config.max_tries} tries.\n"
    )


def parse_guess(raw: str) -> int | None:
    stripped = raw.strip()
    if not stripped.isdigit():
        return None
    return int(stripped)


def is_in_range(guess: int, config: GameConfig = CONFIG) -> bool:
    return config.includes(guess)


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low - try something larger."
    return "Too high - try something smaller."


def read_guess(tries_left: int) -> int | None:
    return parse_guess(input(f"Tries left: {tries_left}. Your guess: "))


def print_invalid_guess() -> None:
    print("Please enter a positive whole number.\n")


def print_out_of_range(config: GameConfig = CONFIG) -> None:
    print(f"Out of range; stay between {config.minimum} and {config.maximum}.\n")


def choose_secret(config: GameConfig, rng: RandomSource = random) -> int:
    return rng.randint(config.minimum, config.maximum)


def main(config: GameConfig = CONFIG, rng: RandomSource = random) -> None:
    secret = choose_secret(config, rng)
    tries_left = config.max_tries
    print(intro_message(config))

    while tries_left > 0:
        guess = read_guess(tries_left)
        if guess is None:
            print_invalid_guess()
            continue

        if not is_in_range(guess, config):
            print_out_of_range(config)
            continue

        if guess == secret:
            print("Correct! You win.\n")
            return

        print(f"{hint_for_guess(guess, secret)}\n")
        tries_left -= 1

    print(f"No tries left. The number was {secret}.\n")


if __name__ == "__main__":
    main()
