from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .io import (
    DEFAULT_PLAN,
    DEFAULT_REPORT,
    DEFAULT_WEIGHTS,
    load_json,
    read_jsonl,
    read_text,
    serialize_jsonl,
    write_jsonl,
)
from .model import Plan, ValidationError, load_factor_scores
from .render import render_report
from .scoring import build_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m binding_constraint",
        description="Run the deterministic Binding Constraint fixture.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate default fixtures and checked report.")
    validate.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    validate.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    validate.add_argument("--report", type=Path, default=DEFAULT_REPORT)

    diagnose = subparsers.add_parser("diagnose", help="Render a JSONL diagnostic artifact.")
    diagnose.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    diagnose.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    diagnose.add_argument("--out", type=Path, default=DEFAULT_REPORT)
    diagnose.add_argument("--generated-on", default="2026-06-21")

    show = subparsers.add_parser(
        "show", help="Print the committed report as a ranked, readable table."
    )
    show.add_argument("--report", type=Path, default=DEFAULT_REPORT)

    return parser


def _load_records(plan_path: Path, weights_path: Path, generated_on: str) -> list[dict]:
    plan = Plan.from_dict(load_json(plan_path), context=str(plan_path))
    scores = load_factor_scores(load_json(weights_path), plan=plan, context=str(weights_path))
    return build_records(plan, scores, generated_on=generated_on)


def run_validate(args: argparse.Namespace) -> int:
    records = _load_records(args.plan, args.weights, generated_on="2026-06-21")
    expected = serialize_jsonl(records)
    actual = read_text(args.report)
    if actual != expected:
        raise ValidationError(
            f"{args.report} is stale; run `python -m binding_constraint diagnose --out {args.report}`"
        )
    print(f"validation ok: {args.report}")
    return 0


def run_diagnose(args: argparse.Namespace) -> int:
    records = _load_records(args.plan, args.weights, generated_on=args.generated_on)
    write_jsonl(args.out, records)
    print(f"wrote {args.out}")
    return 0


def run_show(args: argparse.Namespace) -> int:
    if not args.report.exists():
        raise ValidationError(
            f"{args.report} not found; run `python -m binding_constraint diagnose` first"
        )
    records = read_jsonl(args.report)
    if not records:
        raise ValidationError(f"{args.report} contains no report records")
    print(render_report(records))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            return run_validate(args)
        if args.command == "diagnose":
            return run_diagnose(args)
        if args.command == "show":
            return run_show(args)
    # OSError covers a missing/unreadable path or a directory passed as a file;
    # JSONDecodeError and plain ValueError cover malformed or wrong-shaped input.
    # ValidationError is a ValueError, so a single ValueError arm keeps its message.
    except (ValidationError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    parser.error(f"unknown command: {args.command}")
    return 2
