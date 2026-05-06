#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations
from dataclasses import dataclass, field

from cli_support import ConsoleIO, parse_positive_int


@dataclass
class TodoShell:
    items: list[str] = field(default_factory=list)
    io: ConsoleIO = field(default_factory=ConsoleIO)

    def print_commands(self) -> None:
        self.io.say("Commands: add <text> | list | done <n> | quit\n")

    def add_item(self, text: str) -> None:
        self.items.append(text)
        self.io.say(f"Added item #{len(self.items)}.\n")

    def list_items(self) -> None:
        if not self.items:
            self.io.say("(empty)\n")
            return

        for index, text in enumerate(self.items, start=1):
            self.io.say(f"  {index}. {text}")
        self.io.say("")

    def mark_done(self, raw_index: str) -> None:
        index = parse_positive_int(raw_index)
        if index is None:
            self.io.say("Usage: done <number from list>\n")
            return

        if index < 1 or index > len(self.items):
            self.io.say("That line number does not exist.\n")
            return

        removed = self.items.pop(index - 1)
        self.io.say(f"Removed: {removed}\n")

    def handle_command(self, line: str) -> bool:
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()

        match cmd:
            case "quit":
                self.io.say("Goodbye.\n")
                return False
            case "add":
                if len(parts) < 2:
                    self.io.say("Usage: add <text>\n")
                    return True
                self.add_item(parts[1])
                return True
            case "list":
                self.list_items()
                return True
            case "done":
                if len(parts) < 2:
                    self.io.say("Usage: done <number from list>\n")
                    return True
                self.mark_done(parts[1])
                return True
            case _:
                self.io.say("Unknown command.\n")
                return True

    def run(self) -> None:
        self.print_commands()

        while True:
            line = self.io.ask("todo> ").strip()
            if not line:
                continue

            if not self.handle_command(line):
                break


def print_commands(output_fn = print) -> None:
    TodoShell(io=ConsoleIO(output_fn=output_fn)).print_commands()


def add_item(items: list[str], text: str, output_fn = print) -> None:
    TodoShell(items=items, io=ConsoleIO(output_fn=output_fn)).add_item(text)


def list_items(items: list[str], output_fn = print) -> None:
    TodoShell(items=items, io=ConsoleIO(output_fn=output_fn)).list_items()


def mark_done(
    items: list[str],
    raw_index: str,
    output_fn = print,
) -> None:
    TodoShell(items=items, io=ConsoleIO(output_fn=output_fn)).mark_done(raw_index)


def handle_command(
    line: str,
    items: list[str],
    output_fn = print,
) -> bool:
    return TodoShell(items=items, io=ConsoleIO(output_fn=output_fn)).handle_command(line)


def run_shell(
    input_fn = input,
    output_fn = print,
) -> None:
    TodoShell(io=ConsoleIO(input_fn, output_fn)).run()


def main() -> None:
    run_shell()


if __name__ == "__main__":
    main()
