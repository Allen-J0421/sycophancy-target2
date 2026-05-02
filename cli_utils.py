#!/usr/bin/env python3
"""Shared helpers for tiny interactive CLI scripts."""

from __future__ import annotations


def safe_input(prompt: str) -> str | None:
    """Like input(), but returns None on EOF / Ctrl-C."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None


def parse_int(text: str) -> int | None:
    """Parse a base-10 integer; return None if invalid."""
    text = text.strip()
    if not text:
        return None
    try:
        return int(text, 10)
    except ValueError:
        return None
