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
