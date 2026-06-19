# BindingConstraint

Cross-domain diagnostic that takes a Fortune 500 firm's announced multi-year capex plan and produces a probabilistic ranking of which physical input is most likely to be the binding constraint per project, when it bites, and by how much.

## What this is

A consulting-grade diagnostic tool. Given a published capex plan (a data
center campus, a fab, an EV factory, a hydrogen plant), it scores the
five candidate bottlenecks — chip allocation, transformer lead time,
water rights, skilled-trades labor, permit timeline — and produces a
written diagnostic with the binding constraint named, quantified, and
sourced.

The shape of the artifact is a public report per firm-plan. v0 ships
one report: TSMC Arizona, Intel Ohio, or Micron NY. The model behind it
is a probabilistic factor model where each factor draws on a separate
public dataset.

This repo is the diagnostic layer. GridSilicon, chip-supply-chain-map,
and FabRiskRADAR are the upstream data sources. Capex announcements are
where the work starts; the binding-constraint call is where it ends.

## Who uses it

CFOs and capex-strategy leads at firms with one billion dollars or more
in annual physical-infra capex. PE and infra-fund deal teams underwriting
the same plans. Insurance and surety carriers pricing project-completion
risk.

## Why now

Capex plans across data centers, fabs, EV factories, hydrogen plants,
biomanufacturing, and reshored manufacturing all share a skinny-
bottleneck shape. The press release names the dollar number. The binding
constraint is rarely capital; it is almost always something physical
that the press release ignored. No consultant has shipped a unified
diagnostic across these domains.

## Status

v0 scaffold; no implementation yet. The specs ledger names the first set
of requirements (R-BC-001 through R-BC-010). The first PR after this
scaffold lands the constraint taxonomy plus the report template.

## How to run

Placeholder; will land in spec 0002. v0 ships the constraint taxonomy,
the report template, and the first firm-plan diagnostic as a checked-in
Markdown artifact under `reports/`. No runtime is required to read the
artifact.

The eventual CLI shape (target for spec 0003):

```
python -m binding_constraint diagnose --plan plans/tsmc_arizona.yaml --out reports/2026-08-tsmc-arizona.md
```

## Layout

```
binding-constraint/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Future directories (named in specs, not created yet):

- `src/binding_constraint/` — diagnostic engine
- `src/factors/` — one module per constraint factor
- `plans/` — checked-in capex plan inputs in YAML
- `reports/` — published Markdown diagnostics
- `data/` — cached upstream datasets (gitignored)
- `eval/` — backtest harness against 2018-2025 announced-vs-delivered

## License

MIT. See [LICENSE](LICENSE).
