# System Map

## Runtime Path

```text
plans/tsmc-arizona.json
data/fixture_weights/tsmc-arizona.json
        |
        v
binding_constraint.model
        |
        v
binding_constraint.scoring
        |
        v
reports/2026-06-tsmc-arizona.jsonl
```

## Modules

- `binding_constraint/cli.py` owns `validate` and `diagnose`.
- `binding_constraint/model.py` holds dataclasses and pydantic-free validation.
- `binding_constraint/scoring.py` groups project scores, normalizes probabilities, and builds JSONL records.
- `binding_constraint/io.py` centralizes default fixture paths and JSONL serialization.

There is no separate report module in v0.1. Report artifact construction is split between
`binding_constraint/scoring.py` and `binding_constraint/io.py`.

## Determinism Contract

- Fixture input is local JSON.
- Evidence items are checked-in source URLs and claims.
- No network calls are made.
- `validate` recomputes the default report and fails if the checked-in JSONL artifact is stale.
