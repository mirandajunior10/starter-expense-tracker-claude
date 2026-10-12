"""The ``top`` command: show the largest expenses, biggest first."""

from __future__ import annotations

from .list_cmd import format_expense

NAME = "top"
HELP = "Show the N largest expenses, biggest first"
DEFAULT_LIMIT = 3


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"How many expenses to show (default {DEFAULT_LIMIT})",
    )


def handle(args, store) -> int:
    if args.limit < 1:
        print(f"error: limit must be a positive integer, got {args.limit}")
        return 1

    expenses = store.load()
    if not expenses:
        print("No expenses found.")
        return 0

    # sorted() is stable, so equal amounts keep their original (id) order.
    largest = sorted(expenses, key=lambda e: e.amount_cents, reverse=True)
    for expense in largest[: args.limit]:
        print(format_expense(expense))
    return 0
