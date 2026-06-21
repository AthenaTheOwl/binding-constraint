# Design - 0002

## Shape

v0.1 uses a flat Python package at `binding_constraint/` so the module runs directly from the repo root:

```text
python -m binding_constraint validate
python -m binding_constraint diagnose --out reports/2026-06-tsmc-arizona.jsonl
```

The system uses JSON fixtures instead of YAML to keep the runtime dependency-free.

## Data Flow

1. `binding_constraint.io` reads `plans/tsmc-arizona.json` and `data/fixture_weights/tsmc-arizona.json`.
2. `binding_constraint.model` validates required fields, public URLs, ISO dates, factor coverage, and evidence counts.
3. `binding_constraint.scoring` normalizes curated raw weights into one closed probability distribution per project.
4. `binding_constraint.cli` writes or validates `reports/2026-06-tsmc-arizona.jsonl`.

## Report Format

The JSONL artifact has one line per project. The v0.1 fixture has one project, so the checked artifact has one line.

Each line includes:

- artifact version
- firm and plan identifiers
- project metadata
- modal factor
- full factor ranking
- probability sum
- evidence claims and source URLs

## Failure Mode

`validate` fails if fixture validation fails or if the checked-in report does not match a fresh deterministic render.
