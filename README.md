# BindingConstraint

BindingConstraint is a deterministic Python diagnostic that takes a published capex plan and ranks which physical input is most likely to bind the plan.

The v0.1 slice ships one checked-in case: TSMC Arizona. It scores five candidate constraints and writes one JSONL report artifact.

## What this is

The report is the product. The engine exists to validate checked-in public evidence, normalize curated fixture weights, and emit a sourced artifact that can be reviewed without network access.

The five v0 factors are:

- `chip-allocation`
- `transformer-lead-time`
- `water-rights`
- `skilled-trades-labor`
- `permit-timeline`

The headline field names the modal factor. The report body keeps the full probability distribution.

## Status

v0.1 runnable fixture. The repo validates and renders one deterministic diagnostic for TSMC Arizona using checked-in public-source evidence and curated factor weights.

## How to run

From the repo root:

```text
python -m binding_constraint validate
python -m binding_constraint diagnose --out reports/2026-06-tsmc-arizona.jsonl
python -m pytest
```

`validate` recomputes the default report and fails if `reports/2026-06-tsmc-arizona.jsonl` is stale.

## Layout

```text
binding-constraint/
  README.md
  LICENSE
  AGENTS.md
  PRODUCT_BRIEF.md
  SYSTEM_MAP.md
  STATUS.md
  binding_constraint/
    __init__.py
    __main__.py
    cli.py
    io.py
    model.py
    scoring.py
  plans/
    tsmc-arizona.json
  data/
    fixture_weights/
      tsmc-arizona.json
  reports/
    2026-06-tsmc-arizona.jsonl
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
    0002-design/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  tests/
    test_binding_constraint.py
  docs/
    first-pr.md
```

Future directories named by the foundation spec:

- `schemas/` - JSON schema versions of the runtime validators
- `templates/` - Markdown report templates
- `eval/` - backtest harness against 2018-2025 announced-vs-delivered

## Boundaries

- no API keys
- no live fetch
- no private-source checks
- no web UI in v0.1

## License

MIT. See [LICENSE](LICENSE).
