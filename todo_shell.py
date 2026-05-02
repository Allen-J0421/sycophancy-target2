#!/usr/bin/env python3
"""Tiny interactive todo list: add, list, done, quit."""

from __future__ import annotations

from cli_utils import parse_int, safe_input


class TodoApp:
    def __init__(self) -> None:
        self.items: list[str] = []

    def run(self) -> None:
        print("Commands: add <text> | list | done <n> | quit\n")

        while True:
            line = safe_input("todo> ")
            if line is None:
                print("\nGoodbye.\n")
                break

            line = line.strip()
            if not line:
                continue

            cmd, arg = self._parse(line)
            match cmd:
                case "quit":
                    print("Goodbye.\n")
                    break
                case "add":
                    self._cmd_add(arg)
                case "list":
                    self._cmd_list()
                case "done":
                    self._cmd_done(arg)
                case _:
                    print("Unknown command.\n")

    def _parse(self, line: str) -> tuple[str, str | None]:
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        return cmd, arg

    def _cmd_add(self, text: str | None) -> None:
        if not text:
            print("Usage: add <text>\n")
            return
        self.items.append(text)
        print(f"Added item #{len(self.items)}.\n")

    def _cmd_list(self) -> None:
        if not self.items:
            print("(empty)\n")
            return
        for i, text in enumerate(self.items):
            print(f"  {i + 1}. {text}")
        print()

    def _cmd_done(self, n_raw: str | None) -> None:
        if not n_raw:
            print("Usage: done <number from list>\n")
            return

        n = parse_int(n_raw)
        if n is None or n < 1:
            print("Usage: done <number from list>\n")
            return
        if n > len(self.items):
            print("That line number does not exist.\n")
            return
        removed = self.items.pop(n - 1)
        print(f"Removed: {removed}\n")


def main() -> None:
    TodoApp().run()


if __name__ == "__main__":
    main()
