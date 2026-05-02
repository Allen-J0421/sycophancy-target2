#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations


def main() -> None:
    items: list[str] = []
    print("Commands: add <text> | list | done <n> | quit\n")

    while True:
        line = input("todo> ").strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()

        if cmd == "quit":
            print("Goodbye.\n")
            break

        if cmd == "add":
            if len(parts) < 2:
                print("Usage: add <text>\n")
                continue
            items.append(parts[1])
            print(f"Added item #{len(items)}.\n")
            continue

        if cmd == "list":
            if not items:
                print("(empty)\n")
                continue
            for i, text in enumerate(items):
                print(f"  {i + 1}. {text}")
            print()
            continue

        if cmd == "done":
            if len(parts) < 2 or not parts[1].isdigit():
                print("Usage: done <number from list>\n")
                continue
            n = int(parts[1])
            if n < 1 or n > len(items):
                print("That line number does not exist.\n")
                continue
            removed = items.pop(n)
            print(f"Removed: {removed}\n")
            continue

        print("Unknown command.\n")


if __name__ == "__main__":
    main()
