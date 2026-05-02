#!/usr/bin/env python3
"""Shared helpers for tiny interactive CLI scripts."""

from __future__ import annotations


def safe_input(prompt: str) -> str | None:
    """Like input(), but returns None on EOF / Ctrl-C."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None

