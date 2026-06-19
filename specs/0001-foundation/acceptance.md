# Acceptance — 0001 Foundation

"v0 done" means the following hold simultaneously.

## Artifacts present

- `schemas/capex-plan.schema.json` validates
- `schemas/factor-score.schema.json` validates
- `taxonomy/factors.yaml` lists exactly five factors
- `templates/diagnostic.md.j2` renders without errors
- `plans/<firm>.yaml` parses against the capex-plan schema
- `data/curated/<firm>/factor_scores.yaml` parses against the
  factor-score schema, with three or more evidence items per score
- `reports/2026-08-<firm>.md` exists and is rendered from the template

## Gates pass

Run from the repo root:

```
python -m pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py
python scripts/validate_decisions.py
```

All four exit zero.

## Manual review

- A reader unfamiliar with the firm can read the report and name the
  modal binding constraint within thirty seconds.
- Every factor section has at least three citations with public URLs.
- The headline does not use marketing words.
- The methodology footer points at the factor taxonomy and the DEC
  that justified the five-factor closure.

## Out of v0 acceptance

- The backtest harness exists as a skeleton; it does not yet produce
  a calibration number. That is spec 0003.
- The factor scores are hand-curated. Live ingest is spec 0003.
- The CLI runs end-to-end on one firm-plan. Multi-firm orchestration
  is spec 0002.
