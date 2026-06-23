"""binding-constraint — live demo (Streamlit Community Cloud).

Reads the committed report under reports/*.jsonl and shows, for a published
capex plan, which physical input is most likely to bind it: a ranked factor
distribution with severity and sourced evidence. No network, no secrets — runs
entirely off the committed fixture report.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/binding-constraint,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from binding_constraint.render import factor_label

REPO = Path(__file__).resolve().parent
REPORTS = REPO / "reports"


def load_records() -> tuple[list[dict], str]:
    files = sorted(REPORTS.glob("*.jsonl"))
    if not files:
        return [], ""
    latest = files[-1]
    records = [
        json.loads(line)
        for line in latest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return records, latest.stem


def usd_short(value: int) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.0f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.0f}M"
    return f"${value:,}"


st.set_page_config(page_title="binding-constraint", layout="wide")
st.title("binding-constraint")
st.caption(
    "for a published capex plan, which physical input is most likely to bind it — "
    "chip allocation, transformer lead time, water rights, skilled-trades labor, "
    "or permit timeline. ranked, with sourced evidence."
)

records, month = load_records()
if not records:
    st.warning("no report found under reports/*.jsonl")
    st.stop()

names = [r["project"]["name"] for r in records]
choice = (
    names[0]
    if len(records) == 1
    else st.selectbox("plan", names)
)
record = next(r for r in records if r["project"]["name"] == choice)

project = record["project"]
ranking = record["ranking"]
top = ranking[0]

st.subheader(f"{record['plan_name']}  ·  {month}")

c1, c2, c3 = st.columns(3)
c1.metric("announced capex", usd_short(project["announced_capex_usd"]))
c2.metric(
    "modal constraint",
    factor_label(top["factor_id"]),
    help="highest-probability binding factor for this plan",
)
c3.metric(
    "modal probability",
    f"{round(top['probability'] * 100)}%",
    help=f"~{top['severity_months']} month slip if it binds",
)

st.caption(
    f"firm {record['firm']}  ·  {project['geography']}  ·  "
    f"announced completion {project['announced_completion']}"
)

min_prob = st.slider("minimum probability", 0.0, 1.0, 0.0, 0.01)
rows = [
    {
        "rank": i,
        "factor": factor_label(item["factor_id"]),
        "probability": item["probability"],
        "severity (months)": item["severity_months"],
        "evidence rows": len(item["evidence"]),
    }
    for i, item in enumerate(ranking, start=1)
    if item["probability"] >= min_prob
]

st.dataframe(
    rows,
    use_container_width=True,
    hide_index=True,
    column_config={
        "probability": st.column_config.ProgressColumn(
            "probability", min_value=0.0, max_value=1.0, format="%.2f"
        )
    },
)

st.info(
    f"**most likely binding constraint:** {factor_label(top['factor_id'])} "
    f"({round(top['probability'] * 100)}%, ~{top['severity_months']} month slip). "
    f"{len(top['evidence'])} sourced evidence rows."
)

with st.expander(f"evidence for {factor_label(top['factor_id'])}"):
    for ev in top["evidence"]:
        st.markdown(f"- {ev['claim']}  \n  source: {ev['url']}  ·  retrieved {ev['retrieved_on']}")

st.caption(
    "v0.1 ships one TSMC Arizona fixture. the model + scoring live in "
    "`binding_constraint/`; this page reads the committed `reports/*.jsonl`. "
    "repo: github.com/AthenaTheOwl/binding-constraint"
)
