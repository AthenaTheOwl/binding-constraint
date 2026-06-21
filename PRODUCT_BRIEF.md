# Product Brief

Binding Constraint v0.1 is a fixture-based diagnostic for one published capex plan: TSMC Arizona.

The product answer is a sourced JSONL report. For each project, the engine ranks five possible binding constraints:

- `chip-allocation`
- `transformer-lead-time`
- `water-rights`
- `skilled-trades-labor`
- `permit-timeline`

The v0.1 fixture is deterministic. It reads checked-in public-source evidence and curated weights, validates the shape, normalizes the factor weights into a probability distribution, and writes `reports/2026-06-tsmc-arizona.jsonl`.

Out of scope for v0.1:

- live data fetch
- private evidence
- API keys
- web UI
- multi-firm comparison
