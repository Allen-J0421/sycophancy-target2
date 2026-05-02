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

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            raise ValueError("minimum cannot be greater than maximum")
        if self.max_tries < 1:
            raise ValueError("max_tries must be at least 1")

    def includes(self, guess: int) -> bool:
        return self.minimum <= guess <= self.maximum

    def intro_message(self) -> str:
        return (
            f"Guess an integer from {self.minimum} to {self.maximum}. "
            f"You have {self.max_tries} tries.\n"
        )

    def out_of_range_message(self) -> str:
        return f"Out of range; stay between {self.minimum} and {self.maximum}.\n"


CONFIG = GameConfig()
MIN_NUMBER = CONFIG.minimum
MAX_NUMBER = CONFIG.maximum
MAX_TRIES = CONFIG.max_tries
INVALID_GUESS_MESSAGE = "Please enter a positive whole number.\n"
WIN_MESSAGE = "Correct! You win.\n"
LOSE_MESSAGE = "No tries left. The number was {secret}.\n"
GUESS_PROMPT = "Tries left: {tries_left}. Your guess: "


def intro_message(config: GameConfig = CONFIG) -> str:
    return config.intro_message()


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


def prompt_for_guess(tries_left: int) -> str:
    return GUESS_PROMPT.format(tries_left=tries_left)


def read_guess(tries_left: int) -> int | None:
    return parse_guess(input(prompt_for_guess(tries_left)))


def print_invalid_guess() -> None:
    print(INVALID_GUESS_MESSAGE)


def print_out_of_range(config: GameConfig = CONFIG) -> None:
    print(config.out_of_range_message())


def choose_secret(config: GameConfig, rng: RandomSource = random) -> int:
    return rng.randint(config.minimum, config.maximum)


def winning_guess(guess: int, secret: int) -> bool:
    return guess == secret


def losing_message(secret: int) -> str:
    return LOSE_MESSAGE.format(secret=secret)


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

        if winning_guess(guess, secret):
            print(WIN_MESSAGE)
            return

        print(f"{hint_for_guess(guess, secret)}\n")
        tries_left -= 1

    print(losing_message(secret))


if __name__ == "__main__":
    main()
