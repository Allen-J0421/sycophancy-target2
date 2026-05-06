"""Shared helpers for interactive command-line scripts."""

from collections.abc import Callable

InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]


def write_message(output_func: OutputFunc, message: str) -> None:
    output_func(f"{message}\n")
