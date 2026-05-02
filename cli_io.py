"""Shared command-line I/O helpers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


InputReader = Callable[[str], str]
MessageWriter = Callable[[str], None]


def print_message(message: str) -> None:
    print(message, end="")


def resolve_reader(reader: InputReader | None = None) -> InputReader:
    return input if reader is None else reader


def resolve_writer(writer: MessageWriter | None = None) -> MessageWriter:
    return print_message if writer is None else writer


@dataclass(frozen=True)
class CliIO:
    reader: InputReader
    writer: MessageWriter

    @classmethod
    def resolve(
        cls,
        reader: InputReader | None = None,
        writer: MessageWriter | None = None,
    ) -> CliIO:
        return cls(resolve_reader(reader), resolve_writer(writer))

    def read(self, prompt: str) -> str:
        return self.reader(prompt)

    def write(self, message: str) -> None:
        self.writer(message)
