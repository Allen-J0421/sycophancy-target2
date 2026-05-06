#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from cli_io import InputFn, OutputFn, write


@dataclass
class Command:
    name: str
    arg: str | None = None


def parse_command(line: str) -> Command | None:
    line = line.strip()
    if not line:
        return None

    parts = line.split(maxsplit=1)
    name = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None
    return Command(name=name, arg=arg)

class TodoList:
    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, text: str) -> int:
        self._items.append(text)
        return len(self._items)

    def is_empty(self) -> bool:
        return not self._items

    def list_lines(self) -> list[str]:
        return [f"  {i + 1}. {text}" for i, text in enumerate(self._items)]

    def done(self, n: int) -> str:
        if n < 1 or n > len(self._items):
            raise IndexError("That line number does not exist.")
        return self._items.pop(n - 1)


def run_shell(
    *,
    prompt: str = "todo> ",
    show_banner: bool = True,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    todos = TodoList()
    if show_banner:
        write(output_fn, "Commands: add <text> | list | done <n> | quit")
        write(output_fn)

    while True:
        try:
            line = input_fn(prompt)
        except (EOFError, KeyboardInterrupt):
            write(output_fn, "Goodbye.")
            write(output_fn)
            return

        cmd = parse_command(line)
        if cmd is None:
            continue

        if cmd.name == "quit":
            write(output_fn, "Goodbye.")
            write(output_fn)
            return

        if cmd.name == "add":
            if not cmd.arg:
                write(output_fn, "Usage: add <text>")
                write(output_fn)
                continue
            item_num = todos.add(cmd.arg)
            write(output_fn, f"Added item #{item_num}.")
            write(output_fn)
            continue

        if cmd.name == "list":
            if todos.is_empty():
                write(output_fn, "(empty)")
                write(output_fn)
                continue
            for line in todos.list_lines():
                write(output_fn, line)
            write(output_fn)
            continue

        if cmd.name == "done":
            if not cmd.arg or not cmd.arg.isdigit():
                write(output_fn, "Usage: done <number from list>")
                write(output_fn)
                continue
            try:
                removed = todos.done(int(cmd.arg))
            except IndexError as exc:
                write(output_fn, str(exc))
                write(output_fn)
                continue
            write(output_fn, f"Removed: {removed}")
            write(output_fn)
            continue

        write(output_fn, "Unknown command.")
        write(output_fn)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default="todo> ")
    parser.add_argument("--no-banner", action="store_true")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    args = build_parser().parse_args(argv)
    run_shell(
        prompt=args.prompt,
        show_banner=not args.no_banner,
        input_fn=input_fn,
        output_fn=output_fn,
    )


if __name__ == "__main__":
    main()
