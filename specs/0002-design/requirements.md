# Requirements - 0002 Design

## Runtime

- **R-BC-011** The repo must run with the Python standard library plus pytest for tests.
- **R-BC-012** `python -m binding_constraint validate` must validate the default plan, factor scores, and checked-in report artifact.
- **R-BC-013** `python -m binding_constraint diagnose` must write a deterministic JSONL diagnostic.

## Fixture Scope

- **R-BC-014** v0.1 must include exactly one checked-in capex plan: TSMC Arizona.
- **R-BC-015** v0.1 must score exactly five candidate binding constraints: `chip-allocation`, `transformer-lead-time`, `water-rights`, `skilled-trades-labor`, and `permit-timeline`.
- **R-BC-016** Each factor score must carry at least three public evidence items.

## Output

- **R-BC-017** The default checked-in artifact must live at `reports/2026-06-tsmc-arizona.jsonl`.
- **R-BC-018** The report record must include the modal factor and the full probability ranking.
- **R-BC-019** The factor probabilities for each project must sum to 1.0 after normalization.

## Boundaries

- **R-BC-020** v0.1 must not use API keys, live fetch, pydantic, or external data services.
