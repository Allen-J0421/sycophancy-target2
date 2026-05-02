#!/usr/bin/env python3
"""Small helpers shared by the demo CLI scripts."""

from __future__ import annotations

from collections.abc import Callable


def say(message: str) -> None:
    print(message)
    print()


def prompt_line(prompt: str) -> str:
    return input(prompt).strip()


def run_prompt_loop(prompt: str, handle_line: Callable[[str], bool]) -> None:
    while True:
        line = prompt_line(prompt)
        if not line:
            continue

        if not handle_line(line):
            break


def parse_positive_int(raw: str) -> int | None:
    if not raw.isdigit():
        return None

    return int(raw)


def parse_command_line(line: str) -> tuple[str, str | None]:
    parts = line.split(maxsplit=1)
    if not parts:
        return "", None

    command = parts[0].lower()
    argument = parts[1].lstrip() if len(parts) > 1 else None
    return command, argument


def parse_int_in_bounds(
    raw: str,
    minimum: int,
    maximum: int,
    *,
    missing_error: str,
    out_of_range_error: str,
) -> tuple[int | None, str | None]:
    value = parse_positive_int(raw)
    if value is None:
        return None, missing_error
    if not minimum <= value <= maximum:
        return None, out_of_range_error

    return value, None


def parse_int_in_range(
    raw: str,
    minimum: int,
    maximum: int,
    *,
    range_text: str | None = None,
) -> tuple[int | None, str | None]:
    text = range_text or f"{minimum} to {maximum}"
    return parse_int_in_bounds(
        raw,
        minimum,
        maximum,
        missing_error="Please enter a positive whole number.",
        out_of_range_error=f"Out of range; stay between {text}.",
    )


def prompt_int_in_range(
    prompt: str,
    minimum: int,
    maximum: int,
    *,
    range_text: str | None = None,
) -> int | None:
    value, error = parse_int_in_range(
        prompt_line(prompt),
        minimum,
        maximum,
        range_text=range_text,
    )
    if error is not None:
        say(error)
        return None

    return value


def parse_list_index(
    raw: str,
    size: int,
    *,
    usage_text: str,
) -> tuple[int | None, str | None]:
    return parse_int_in_bounds(
        raw,
        1,
        size,
        missing_error=usage_text,
        out_of_range_error="That line number does not exist.",
    )
