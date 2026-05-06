"""Helpers for CLI-focused tests."""

from collections.abc import Callable, Iterable


InputFn = Callable[[str], str]


def make_script_io(responses: Iterable[str]) -> tuple[InputFn, list[str]]:
    iterator = iter(responses)
    outputs: list[str] = []

    def input_fn(prompt: str) -> str:
        return next(iterator)

    return input_fn, outputs
