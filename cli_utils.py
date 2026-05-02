#!/usr/bin/env python3
"""Small helpers shared by the demo CLI scripts."""

from __future__ import annotations


def say(message: str) -> None:
    print(message)
    print()


def prompt_line(prompt: str) -> str:
    return input(prompt).strip()


def parse_positive_int(raw: str) -> int | None:
    if not raw.isdigit():
        return None

    return int(raw)


def parse_command_line(line: str) -> tuple[str, str | None]:
    parts = line.split(maxsplit=1)
    if not parts:
        return "", None

    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None
    return command, argument


def parse_int_in_range(
    raw: str,
    minimum: int,
    maximum: int,
    *,
    range_text: str | None = None,
) -> tuple[int | None, str | None]:
    value = parse_positive_int(raw)
    if value is None:
        return None, "Please enter a positive whole number."

    if value < minimum or value > maximum:
        text = range_text if range_text is not None else f"{minimum} to {maximum}"
        return None, f"Out of range; stay between {text}."

    return value, None
