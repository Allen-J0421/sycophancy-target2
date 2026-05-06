#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations
from dataclasses import dataclass, field

from cli_support import InputFn, OutputFn, parse_positive_int


@dataclass
class TodoShell:
    items: list[str] = field(default_factory=list)
    output_fn: OutputFn = print

    def print_commands(self) -> None:
        self.output_fn("Commands: add <text> | list | done <n> | quit\n")

    def add_item(self, text: str) -> None:
        self.items.append(text)
        self.output_fn(f"Added item #{len(self.items)}.\n")

    def list_items(self) -> None:
        if not self.items:
            self.output_fn("(empty)\n")
            return

        for index, text in enumerate(self.items, start=1):
            self.output_fn(f"  {index}. {text}")
        self.output_fn("")

    def mark_done(self, raw_index: str) -> None:
        index = parse_positive_int(raw_index)
        if index is None:
            self.output_fn("Usage: done <number from list>\n")
            return

        if index < 1 or index > len(self.items):
            self.output_fn("That line number does not exist.\n")
            return

        removed = self.items.pop(index - 1)
        self.output_fn(f"Removed: {removed}\n")

    def handle_command(self, line: str) -> bool:
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()

        match cmd:
            case "quit":
                self.output_fn("Goodbye.\n")
                return False
            case "add":
                if len(parts) < 2:
                    self.output_fn("Usage: add <text>\n")
                    return True
                self.add_item(parts[1])
                return True
            case "list":
                self.list_items()
                return True
            case "done":
                if len(parts) < 2:
                    self.output_fn("Usage: done <number from list>\n")
                    return True
                self.mark_done(parts[1])
                return True
            case _:
                self.output_fn("Unknown command.\n")
                return True

    def run(self, input_fn: InputFn = input) -> None:
        self.print_commands()

        while True:
            line = input_fn("todo> ").strip()
            if not line:
                continue

            if not self.handle_command(line):
                break


def print_commands(output_fn: OutputFn = print) -> None:
    TodoShell(output_fn=output_fn).print_commands()


def add_item(items: list[str], text: str, output_fn: OutputFn = print) -> None:
    TodoShell(items=items, output_fn=output_fn).add_item(text)


def list_items(items: list[str], output_fn: OutputFn = print) -> None:
    TodoShell(items=items, output_fn=output_fn).list_items()


def mark_done(
    items: list[str],
    raw_index: str,
    output_fn: OutputFn = print,
) -> None:
    TodoShell(items=items, output_fn=output_fn).mark_done(raw_index)


def handle_command(
    line: str,
    items: list[str],
    output_fn: OutputFn = print,
) -> bool:
    return TodoShell(items=items, output_fn=output_fn).handle_command(line)


def run_shell(
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    TodoShell(output_fn=output_fn).run(input_fn)


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
