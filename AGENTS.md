# AGENTS.md — binding-constraint

Operating contract for AI agents (Claude, Codex, Cursor) working in this
repo. Conventions match the AthenaTheOwl portfolio so an agent already
trained on supplier-risk-rag-agent or chip-supply-chain-map recognizes
the shape.

## What this repo is

A diagnostic tool that names the binding physical constraint on a
published capex plan. Output is a written report per firm-plan, with
every claim sourced and every factor score quantified. The report is the
product; the engine exists to produce it.

This is not a dashboard. It is not a real-time tracker. It is a
periodic, citation-faithful diagnostic.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `plan-ingester` | Parses an announced capex plan YAML into typed projects |
| `factor-scorer` | Runs one constraint factor (chip, transformer, water, labor, permit) |
| `diagnostic-writer` | Synthesizes the per-project ranking into a Markdown report |
| `evidence-curator` | Attaches the three strongest evidence items to each factor score |
| `backtest-runner` | Scores past diagnostics against actual delivered capex |

These roles exist in the spec ledger; not all are implemented in v0.

## Voice constraints

- No marketing words. The banned set will live in
  `scripts/voice_lint.py::BANNED_FAIL` once the gate lands. Default to
  plain assertion; the data is the moat, the voice is the scaffolding.
- No antithetical reversals as a structural device.
- Every factor score in a report cites at least one public source.
- The binding-constraint verdict is a probability distribution over the
  five factors, not a single named factor. The headline names the modal
  factor; the body shows the full ranking.

## Gates (will land in spec 0002)

Planned local gates before pushing:

- `pytest`
- `voice_lint.py` on `reports/*.md`
- `spec_check.py` against `specs/`
- `validate_factor_scores.py` — every score has 3+ evidence items
- `backtest_calibration.py` — diagnostic Brier score must beat naive

## Out of scope

- Live data feeds. Quarterly refresh on cron, not push.
- Predicting whether a firm goes bankrupt. Capex-completion only.
- Private channel checks. Public data only; the discipline is in fusing
  what is already in the open.
- A "general consulting platform". This is one diagnostic, done well.
