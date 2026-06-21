# Acceptance - 0002 Design

Run from the repo root:

```text
python -m binding_constraint validate
python -m pytest
```

Acceptance requires:

- both commands exit zero
- `reports/2026-06-tsmc-arizona.jsonl` exists
- the report has a `modal_factor`
- the report ranks all five v0 factors
- every factor has at least three public evidence items
- no runtime command needs an API key or network call
