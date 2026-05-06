"""Shared helpers for tiny interactive CLI scripts."""

from collections.abc import Callable


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def parse_positive_int(raw: str) -> int | None:
    try:
        value = int(raw)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value
