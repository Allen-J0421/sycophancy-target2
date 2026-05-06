"""Helpers for CLI-focused tests."""

from collections.abc import Iterable


class ScriptIO:
    def __init__(self, responses: Iterable[str]):
        self._responses = iter(responses)
        self.outputs: list[str] = []

    def input(self, prompt: str) -> str:
        return next(self._responses)

    def output(self, message: str) -> None:
        self.outputs.append(message)
