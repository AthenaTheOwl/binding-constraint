# binding-constraint

TSMC is putting $65B into a fab in Phoenix and means to finish by 2030. Five things can stop it. binding-constraint says it's the welders — skilled-trades labor, 33%, about eighteen months of slip — and ranks the other four behind them.

## What it does

A capex plan is a promise about physical inputs. Chips, transformers, water rights, tradespeople, permits. The press release names the dollar figure; it does not tell you which of those inputs runs out first. binding-constraint takes a published plan, scores five candidate constraints against checked-in public evidence, and names the one most likely to bind — the modal factor — while keeping the full distribution in the report body.

The report is the product. The engine exists to validate the evidence, normalize curated fixture weights into a probability distribution, and write one sourced artifact you can read without touching the network. v0.1 ships a single checked-in case, TSMC Arizona, scored across the five factors. The model and the scorer are the point; the data is one fixture.

## Try it

`show` reads the committed report and prints the ranked distribution with a one-line verdict. No network, no keys, exits 0:

```text
python -m binding_constraint show
```

```
================================================================
binding-constraint diagnostic  (2026-06-21)
  plan : TSMC Arizona advanced semiconductor manufacturing site
  firm : TSMC  |  capex : $65B
  site : Phoenix, Arizona, United States
  done : announced 2030-12-31
----------------------------------------------------------------
  #  factor                      p   slip  bar
  1  skilled-trades labor      33%   18mo  #######-------------
  2  water rights              24%   12mo  #####---------------
  3  transformer lead time     18%    9mo  ####----------------
  4  permit timeline           15%    6mo  ###-----------------
  5  chip allocation           10%    4mo  ##------------------
----------------------------------------------------------------
  > Arizona advanced semiconductor manufacturing site (TSMC, $65B) is most likely bound by skilled-trades labor (33%, ~18 mo slip).
================================================================
```

The factor at the top is the one to watch. Everything below it is a problem you get to have only if you solve the one above.

## Live demo

A read-only Streamlit page (`streamlit_app.py`) renders the same committed report: the ranked factor distribution, the severity, and the sourced evidence behind the modal constraint. It reads `reports/*.jsonl` directly — no network, no secrets.

```text
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud -> New app -> repo `AthenaTheOwl/binding-constraint`,
branch `main`, main file `streamlit_app.py`.

<!-- live-url: -->

## How it connects

binding-constraint is the constraint layer over the same buildout the rest of the cluster tracks:

- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) — scores how much of an announced datacenter load is real versus still living on a form.
- [chip-supply-chain-map](https://github.com/AthenaTheOwl/chip-supply-chain-map) / [fab-risk-radar](https://github.com/AthenaTheOwl/fab-risk-radar) — the silicon side: where the chips actually come from, and what threatens the fabs that make them.
- [interconnect-alpha](https://github.com/AthenaTheOwl/interconnect-alpha) — the survival model for whether a queued project ever reaches commercial operation.

## Run it in full

```text
python -m binding_constraint validate
python -m binding_constraint diagnose --out reports/2026-06-tsmc-arizona.jsonl
python -m pytest
```

`validate` recomputes the default report and fails if `reports/2026-06-tsmc-arizona.jsonl` is stale.

## Layout

```text
binding_constraint/   cli, model, scoring, io
plans/                tsmc-arizona.json — the published plan
data/fixture_weights/ the curated factor weights
reports/              2026-06-tsmc-arizona.jsonl — the one row v0.1 ships
specs/  tests/  docs/
```

Boundaries for v0.1: no API keys, no live fetch, no private-source checks, no web UI beyond the read-only Streamlit page. Future directories named by the foundation spec — `schemas/`, `templates/`, `eval/` (a backtest harness against 2018-2025 announced-vs-delivered) — are not built yet.

## License

MIT. See [LICENSE](LICENSE).
