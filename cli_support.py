"""Shared helpers for tiny interactive CLI scripts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


@dataclass
class ConsoleIO:
    input_fn: InputFn = input
    output_fn: OutputFn = print

    def ask(self, prompt: str) -> str:
        return self.input_fn(prompt)

    def say(self, message: str) -> None:
        self.output_fn(message)


def parse_positive_int(raw: str) -> int | None:
    if not raw.isdigit():
        return None
    return int(raw)
