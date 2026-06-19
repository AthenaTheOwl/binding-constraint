# Tasks — 0001 Foundation

Checkbox tasks ordered for the first two to three PRs after the
scaffold.

## PR 1 — Schemas, taxonomy, report template

- [ ] Write `schemas/capex-plan.schema.json` per R-BC-001
- [ ] Write `schemas/factor-score.schema.json` per R-BC-003
- [ ] Write `taxonomy/factors.yaml` enumerating the five v0 factors
- [ ] Write `templates/diagnostic.md.j2` per R-BC-005
- [ ] Add `decisions/DEC-BC-001-v0-firm-plan-choice.md`
- [ ] Add `scripts/validate_schemas.py` skeleton
- [ ] Add `scripts/voice_lint.py` skeleton with empty banlist

## PR 2 — First firm-plan ingest and hand-curated factor scores

- [ ] Write `plans/<firm>.yaml` for the chosen v0 firm-plan
- [ ] Hand-curate factor scores for each project in
      `data/curated/<firm>/factor_scores.yaml`
- [ ] Implement `src/binding_constraint/ingest/load_plan.py`
- [ ] Implement `src/binding_constraint/render/diagnostic.py`
- [ ] Generate the first report at `reports/2026-08-<firm>.md`
- [ ] Run voice_lint on the report; fix any failures
- [ ] Wire CLI entry: `python -m binding_constraint diagnose --plan ... --out ...`

## PR 3 — Backtest skeleton and DEC ledger

- [ ] Write `eval/backtest.py` skeleton per design.md
- [ ] Define the 2018-2025 announced-vs-delivered cohort in
      `eval/cohort.yaml`
- [ ] Add `scripts/validate_decisions.py` skeleton
- [ ] Document the cohort selection in DEC-BC-002
- [ ] Update README.md install + run section once the CLI exists
