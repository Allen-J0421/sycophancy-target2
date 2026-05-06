#!/usr/bin/env python3
"""Interactive number guessing game (1–100, limited tries)."""

from __future__ import annotations

import argparse
import random

from cli_io import Argv, InputFn, OutputFn, write

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7


def parse_guess(raw: str, *, min_value: int = MIN_NUMBER, max_value: int = MAX_NUMBER) -> int:
    raw = raw.strip()
    if not raw.isdigit():
        raise ValueError("Please enter a positive whole number.")

    guess = int(raw)
    if guess < min_value or guess > max_value:
        raise ValueError(f"Out of range; stay between {min_value} and {max_value}.")

    return guess


def hint_for_guess(*, guess: int, secret: int) -> str:
    if guess < secret:
        return "Too low — try something larger."
    return "Too high — try something smaller."


def play_round(
    *,
    secret: int,
    tries: int = MAX_TRIES,
    min_value: int = MIN_NUMBER,
    max_value: int = MAX_NUMBER,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    write(output_fn, f"Guess an integer from {min_value} to {max_value}. You have {tries} tries.")
    write(output_fn)
    tries_left = tries

    while tries_left > 0:
        try:
            raw = input_fn(f"Tries left: {tries_left}. Your guess: ")
        except (EOFError, KeyboardInterrupt):
            write(output_fn, "Goodbye.")
            write(output_fn)
            return

        try:
            guess = parse_guess(raw, min_value=min_value, max_value=max_value)
        except ValueError as exc:
            write(output_fn, str(exc))
            write(output_fn)
            continue

        if guess == secret:
            write(output_fn, "Correct! You win.")
            write(output_fn)
            return

        write(output_fn, hint_for_guess(guess=guess, secret=secret))
        write(output_fn)
        tries_left -= 1

    write(output_fn, f"No tries left. The number was {secret}.")
    write(output_fn)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=MIN_NUMBER, dest="min_value")
    parser.add_argument("--max", type=int, default=MAX_NUMBER, dest="max_value")
    parser.add_argument("--tries", type=int, default=MAX_TRIES)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--secret", type=int, default=None)
    return parser


def main(
    argv: Argv = None,
    *,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    args = build_parser().parse_args(argv)
    if args.tries < 1:
        raise SystemExit("--tries must be >= 1")
    if args.min_value >= args.max_value:
        raise SystemExit("--min must be < --max")
    if args.secret is not None and not (args.min_value <= args.secret <= args.max_value):
        raise SystemExit("--secret must be within [--min, --max]")

    rng = random.Random(args.seed)
    secret = args.secret if args.secret is not None else rng.randint(args.min_value, args.max_value)

    play_round(
        secret=secret,
        tries=args.tries,
        min_value=args.min_value,
        max_value=args.max_value,
        input_fn=input_fn,
        output_fn=output_fn,
    )


if __name__ == "__main__":
    main()
