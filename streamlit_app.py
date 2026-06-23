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

# ---------------------------------------------------------------------------
# Run the real ranking engine live. This is not a viewer — the weight sliders
# below build FactorScore objects and call binding_constraint.scoring.build_records,
# the same function that produced the committed report. The engine normalizes the
# raw weights into a closed probability distribution and re-ranks the factors.
# Change a weight, watch the modal binding constraint move.
# ---------------------------------------------------------------------------
st.divider()
st.subheader("rank the constraints yourself")
st.caption(
    "drive the actual ranking engine — `binding_constraint.scoring.build_records` "
    "(via `_rank_scores`) — with your own factor weights. the engine normalizes them "
    "into a closed probability distribution; it's the live function, not a lookup."
)

try:
    from binding_constraint.model import (
        FACTOR_IDS,
        EvidenceItem,
        FactorScore,
        Plan,
        Project,
    )
    from binding_constraint.scoring import build_records

    # pull each factor's committed weight, severity and evidence from the loaded
    # report so the sliders start where the published diagnostic landed.
    committed = {item["factor_id"]: item for item in ranking}
    base_severity = {fid: int(committed[fid]["severity_months"]) for fid in FACTOR_IDS}
    base_evidence = {fid: committed[fid]["evidence"] for fid in FACTOR_IDS}

    st.markdown("**relative weight per candidate constraint** (the engine renormalizes to sum to 1.0)")
    weights: dict[str, float] = {}
    wcols = st.columns(len(FACTOR_IDS))
    # seed the sliders from the published raw weights, recovered from the
    # committed probabilities (probability ≈ raw_weight / sum, so any positive
    # scaling reproduces the same ranking — the published probs work directly).
    for col, fid in zip(wcols, FACTOR_IDS):
        with col:
            weights[fid] = st.slider(
                factor_label(fid),
                min_value=0.0,
                max_value=1.0,
                value=float(committed[fid]["probability"]),
                step=0.01,
                key=f"w-{fid}",
            )

    if sum(weights.values()) <= 0:
        st.warning("set at least one weight above zero so the engine has a positive distribution to normalize.")
    else:
        # a single-project plan carrying the user's geography/capex so build_records
        # produces a real record; the ranking only depends on the FactorScore weights.
        live_project = Project(
            project_id="user-plan",
            name="your plan",
            geography=project.get("geography", "—"),
            project_type=project.get("project_type", "datacenter"),
            announced_capex_usd=int(project.get("announced_capex_usd", 1)),
            announced_completion=project.get("announced_completion", "2027-01-01"),
            public_sources=tuple(project.get("public_sources", ["https://example.com"])),
        )
        live_plan = Plan(
            plan_id="user-plan",
            firm=record.get("firm", "your firm"),
            plan_name="your plan",
            retrieved_on="2026-06-22",
            projects=(live_project,),
        )
        factor_scores = tuple(
            FactorScore(
                project_id="user-plan",
                factor_id=fid,
                raw_weight=weights[fid],
                severity_months=base_severity[fid],
                evidence=tuple(
                    EvidenceItem(url=ev["url"], claim=ev["claim"], retrieved_on=ev["retrieved_on"])
                    for ev in base_evidence[fid]
                ),
            )
            for fid in FACTOR_IDS
        )
        live_records = build_records(live_plan, factor_scores, generated_on="2026-06-22")
        live_ranking = live_records[0]["ranking"]
        live_top = live_ranking[0]

        lc1, lc2 = st.columns(2)
        lc1.metric("modal constraint", factor_label(live_top["factor_id"]))
        lc2.metric(
            "modal probability",
            f"{round(live_top['probability'] * 100)}%",
            help=f"~{live_top['severity_months']} month slip if it binds",
        )

        st.dataframe(
            [
                {
                    "rank": i,
                    "factor": factor_label(it["factor_id"]),
                    "probability": it["probability"],
                    "severity (months)": it["severity_months"],
                }
                for i, it in enumerate(live_ranking, start=1)
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "probability": st.column_config.ProgressColumn(
                    "probability", min_value=0.0, max_value=1.0, format="%.2f"
                )
            },
        )
        st.success(
            f"**most likely binding constraint:** {factor_label(live_top['factor_id'])} "
            f"({round(live_top['probability'] * 100)}%, ~{live_top['severity_months']} month slip). "
            f"distribution sums to {live_records[0]['probability_sum']} across {len(live_ranking)} factors."
        )
        st.caption(
            "raise transformer lead time or water rights above labor and watch the modal "
            "constraint flip — the engine re-ranks and renormalizes live."
        )
except Exception as exc:  # pragma: no cover - defensive for cloud import differences
    st.info(f"interactive ranking needs the package importable ({exc}). the committed report above still renders.")

st.caption(
    "v0.1 ships one TSMC Arizona fixture. the model + scoring live in "
    "`binding_constraint/`; the table reads the committed `reports/*.jsonl` and the "
    "ranker above is the real engine. repo: github.com/AthenaTheOwl/binding-constraint"
)
