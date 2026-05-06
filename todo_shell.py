#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from dataclasses import dataclass


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


def main() -> None:
    todos = TodoList()
    print("Commands: add <text> | list | done <n> | quit\n")

    while True:
        cmd = parse_command(input("todo> "))
        if cmd is None:
            continue

        if cmd.name == "quit":
            print("Goodbye.\n")
            break

        if cmd.name == "add":
            if not cmd.arg:
                print("Usage: add <text>\n")
                continue
            item_num = todos.add(cmd.arg)
            print(f"Added item #{item_num}.\n")
            continue

        if cmd.name == "list":
            if todos.is_empty():
                print("(empty)\n")
                continue
            for line in todos.list_lines():
                print(line)
            print()
            continue

        if cmd.name == "done":
            if not cmd.arg or not cmd.arg.isdigit():
                print("Usage: done <number from list>\n")
                continue
            try:
                removed = todos.done(int(cmd.arg))
            except IndexError as exc:
                print(f"{exc}\n")
                continue
            print(f"Removed: {removed}\n")
            continue

        print("Unknown command.\n")


if __name__ == "__main__":
    main()
