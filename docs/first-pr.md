# First PR

The literal first PR after this scaffold. The goal is the schema set,
the factor taxonomy, and the report template — no data, no rendering
yet. That comes in PR 2.

## Files this PR adds

- `schemas/capex-plan.schema.json`
  - JSON Schema draft 2020-12
  - Required fields: `firm`, `projects[]`
  - Each project: `id`, `name`, `geography`, `announced_capex_usd`,
    `announced_completion_date`, `project_type`
  - `project_type` is an enum: `data-center`, `fab`, `ev-factory`,
    `hydrogen-plant`, `biomanufacturing`, `reshored-manufacturing`
- `schemas/factor-score.schema.json`
  - Required fields: `factor_id`, `project_id`,
    `binding_probability`, `severity_months`, `evidence[]`
  - `factor_id` is an enum matching `taxonomy/factors.yaml`
  - `evidence[]` requires three or more items, each with `url`,
    `claim`, `retrieved_on`
- `taxonomy/factors.yaml`
  - Five entries: `chip-allocation`, `transformer-lead-time`,
    `water-rights`, `skilled-trades-labor`, `permit-timeline`
  - Each entry has `id`, `name`, `description`, `default_data_sources[]`
- `templates/diagnostic.md.j2`
  - Jinja2 template; consumes a `Plan` and a list of `FactorScore`
  - Renders headline, ranking table, per-factor sections, methodology
    footer
- `decisions/DEC-BC-001-v0-firm-plan-choice.md`
  - Names the v0 firm-plan (TSMC Arizona OR Intel Ohio OR Micron NY)
  - Justifies the choice on data availability and public-disclosure
    quality
  - Justifies the closure to exactly five factors for v0
- `scripts/validate_schemas.py`
  - Loads every file under `schemas/` and confirms it parses as JSON
    Schema
  - Loads every file under `data/curated/` and `plans/` (if any) and
    validates against the matching schema
- `scripts/voice_lint.py`
  - Stub with the BANNED_FAIL banlist seeded from the portfolio voice
    spec
  - Scans `reports/*.md` and `decisions/*.md`

## Verification

```
python -m pytest        # no tests yet; the runner exits clean
python scripts/validate_schemas.py
python scripts/voice_lint.py
```

All three exit zero. The DEC file is readable as Markdown and the
schemas parse with `jsonschema` from the standard ecosystem.

## What this PR does not do

- No factor scoring code. That is PR 2.
- No report rendering. That is PR 2.
- No backtest harness. That is PR 3.
- No CLI entry point. The package skeleton exists but `python -m
  binding_constraint` is not yet wired.
