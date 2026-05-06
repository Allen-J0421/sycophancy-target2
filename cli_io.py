"""Shared helpers for interactive command-line scripts."""

from collections.abc import Callable

InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]


def read_prompt(input_func: InputFunc, prompt: str) -> str:
    return input_func(prompt).strip()


def write_message(output_func: OutputFunc, message: str) -> None:
    output_func(f"{message}\n")
