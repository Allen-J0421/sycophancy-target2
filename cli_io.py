"""Shared command-line I/O helpers."""

from __future__ import annotations

from collections.abc import Callable


InputReader = Callable[[str], str]
MessageWriter = Callable[[str], None]


def print_message(message: str) -> None:
    print(message, end="")


def resolve_reader(reader: InputReader | None = None) -> InputReader:
    return input if reader is None else reader


def resolve_writer(writer: MessageWriter | None = None) -> MessageWriter:
    return print_message if writer is None else writer
