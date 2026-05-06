from __future__ import annotations

from collections.abc import Callable

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def write(output_fn: OutputFn, line: str = "") -> None:
    output_fn(line)

