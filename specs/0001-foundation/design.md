# Design — 0001 Foundation

## Shape

binding-constraint is a Python package that turns a capex plan YAML
into a Markdown diagnostic report. The engine is a probabilistic factor
model. Each factor is an independent scoring module; the diagnostic
writer composes their outputs into a per-project ranking.

The architecture has three layers:

1. **Ingest.** `src/binding_constraint/ingest/` reads a capex-plan
   YAML, validates it against `schemas/capex-plan.schema.json`, emits
   a typed `Plan` object.
2. **Score.** `src/binding_constraint/factors/` holds one module per
   factor. Each module exposes `score(project) -> FactorScore`. A
   factor score is a probability that this factor is the binding
   constraint, plus a severity in months, plus three or more evidence
   items.
3. **Render.** `src/binding_constraint/render/` consumes the per-
   project factor scores and the report template, emits a Markdown
   diagnostic under `reports/`.

## Data flow

```
plans/<firm>.yaml
   |
   v
[ingest.load_plan]  ->  Plan
   |
   v
[factors.chip_allocation.score]      ----+
[factors.transformer_lead_time.score] ----+
[factors.water_rights.score]          ----+--> [render.diagnostic]
[factors.skilled_trades_labor.score]  ----+        |
[factors.permit_timeline.score]       ----+        v
                                              reports/<date>-<firm>.md
```

## Factor independence

Factors are scored independently in v0. The probabilities do not
sum to one across factors; a project can have two roughly-equally-
binding constraints. The diagnostic writer reports the full ranking
and the headline names the modal factor.

The closure to exactly five factors is a v0 simplification. Hydrogen-
plant capex would need a sixth factor for electrolyzer supply;
biomanufacturing would need a seventh for fill-finish capacity. Spec
0002 may expand the set or fork per-domain factor packs; the call is
deferred.

## Upstream data sources

Each factor module owns its data ingest. In v0 the ingesters are
stubbed; the factor scores are hand-curated for the first firm-plan
and the evidence items are checked-in URLs. Spec 0003 replaces the
hand curation with live ingest from:

- chip-allocation: chip-supply-chain-map exports
- transformer-lead-time: trade-press tracking plus GridSilicon
- water-rights: state water-board dockets via puc-docket-rag
- skilled-trades-labor: BLS plus state apprenticeship registries
- permit-timeline: county and state permit dockets

## Backtest

`eval/backtest.py` scores past diagnostics against announced-vs-
delivered capex from 2018-2025. Calibration is Brier score on factor-
occurrence (did the named binding constraint actually bind). v0 ships
the harness skeleton plus the cohort definition; the first
calibration run happens once three diagnostics exist.

## Out of v0 scope

- Live data refresh
- Multi-firm cross-comparison
- A web frontend
- LLM-generated factor scores (factors are hand-curated in v0; the
  engine is the report renderer)
