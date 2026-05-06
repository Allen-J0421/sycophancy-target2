"""Shared helpers for tiny interactive CLI scripts."""

from collections.abc import Callable


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def parse_positive_int(raw: str) -> int | None:
    if not raw.isdigit():
        return None
    return int(raw)
