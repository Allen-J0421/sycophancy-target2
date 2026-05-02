#!/usr/bin/env python3
"""Interactive number guessing game (1-100, limited tries)."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Protocol

from cli_io import (
    CliIO,
    InputReader,
    MessageWriter,
    print_message,
    resolve_reader,
)
from input_parsing import parse_positive_int


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


def choose_secret(config: GameConfig, rng: RandomSource = random) -> int:
    return rng.randint(config.minimum, config.maximum)


@dataclass(frozen=True)
class GuessOutcome:
    message: str
    uses_try: bool = False
    won: bool = False


@dataclass
class GameSession:
    config: GameConfig
    secret: int
    tries_left: int = field(init=False)

    @classmethod
    def start(cls, config: GameConfig, rng: RandomSource = random) -> GameSession:
        return cls(config=config, secret=choose_secret(config, rng))

    def __post_init__(self) -> None:
        self.tries_left = self.config.max_tries

    @property
    def has_tries_left(self) -> bool:
        return self.tries_left > 0

    def prompt(self) -> str:
        return prompt_for_guess(self.tries_left)

    def intro_message(self) -> str:
        return self.config.intro_message()

    def losing_message(self) -> str:
        return losing_message(self.secret)

    def read_guess(self, reader: InputReader) -> int | None:
        return parse_guess(reader(self.prompt()))

    def evaluate(self, guess: int | None) -> GuessOutcome:
        outcome = evaluate_guess(guess, self.secret, self.config)
        if outcome.uses_try:
            self.tries_left -= 1
        return outcome

    def play_turn(self, reader: InputReader) -> GuessOutcome:
        return self.evaluate(self.read_guess(reader))


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
    return parse_positive_int(raw)


def is_in_range(guess: int, config: GameConfig = CONFIG) -> bool:
    return config.includes(guess)


def hint_for_guess(guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low - try something larger."
    return "Too high - try something smaller."


def prompt_for_guess(tries_left: int) -> str:
    return GUESS_PROMPT.format(tries_left=tries_left)


def read_guess(tries_left: int, reader: InputReader | None = None) -> int | None:
    reader = resolve_reader(reader)
    return parse_guess(reader(prompt_for_guess(tries_left)))


def print_invalid_guess() -> None:
    print_message(INVALID_GUESS_MESSAGE)


def print_out_of_range(config: GameConfig = CONFIG) -> None:
    print_message(config.out_of_range_message())


def start_session(config: GameConfig = CONFIG, rng: RandomSource = random) -> GameSession:
    return GameSession.start(config, rng)


def winning_guess(guess: int, secret: int) -> bool:
    return guess == secret


def losing_message(secret: int) -> str:
    return LOSE_MESSAGE.format(secret=secret)


def evaluate_guess(guess: int | None, secret: int, config: GameConfig = CONFIG) -> GuessOutcome:
    if guess is None:
        return GuessOutcome(INVALID_GUESS_MESSAGE)

    if not is_in_range(guess, config):
        return GuessOutcome(config.out_of_range_message())

    if winning_guess(guess, secret):
        return GuessOutcome(WIN_MESSAGE, won=True)

    return GuessOutcome(f"{hint_for_guess(guess, secret)}\n", uses_try=True)


def run_game(
    config: GameConfig = CONFIG,
    rng: RandomSource = random,
    reader: InputReader | None = None,
    writer: MessageWriter | None = None,
) -> None:
    io = CliIO.resolve(reader, writer)

    session = GameSession.start(config, rng)
    io.write(session.intro_message())

    while session.has_tries_left:
        outcome = session.play_turn(io.read)
        io.write(outcome.message)

        if outcome.won:
            return

    io.write(session.losing_message())


def main(config: GameConfig = CONFIG, rng: RandomSource = random) -> None:
    run_game(config, rng)


if __name__ == "__main__":
    main()
