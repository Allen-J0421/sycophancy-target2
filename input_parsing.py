"""Shared parsing helpers for command-line input."""

from __future__ import annotations


def parse_positive_int(raw: str) -> int | None:
    """Return a positive integer from text, or None when it is not valid."""
    stripped = raw.strip()
    if not stripped.isdigit():
        return None
    return int(stripped)
