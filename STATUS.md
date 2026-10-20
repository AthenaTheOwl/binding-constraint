# Status

## Current state

v0.1 is runnable as a local Python module.

Implemented:

- default TSMC Arizona capex-plan fixture
- five-factor curated scoring fixture
- deterministic JSONL report artifact
- CLI commands: `validate` and `diagnose`
- pytest coverage for fixture validation, probability closure, and deterministic report rendering
- reported probabilities are exact under rescaling of all weights, including shares that sit on a 4-decimal rounding half

## Known limits

- Factor weights are curated fixtures.
- The output artifact is JSONL only.
- There is one firm-plan and one project.
- Backtest calibration is not implemented.

## Next feature queue

- Add schema files that mirror the current runtime validators.
- Add Markdown report rendering from the JSONL diagnostic artifact.
- Add calibration tests once a backtest fixture set exists.
