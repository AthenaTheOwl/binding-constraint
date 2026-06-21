from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAN = ROOT / "plans" / "tsmc-arizona.json"
DEFAULT_WEIGHTS = ROOT / "data" / "fixture_weights" / "tsmc-arizona.json"
DEFAULT_REPORT = ROOT / "reports" / "2026-06-tsmc-arizona.jsonl"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def serialize_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records)


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(serialize_jsonl(records), encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
