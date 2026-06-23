from __future__ import annotations

from typing import Any

FACTOR_LABELS = {
    "chip-allocation": "chip allocation",
    "transformer-lead-time": "transformer lead time",
    "water-rights": "water rights",
    "skilled-trades-labor": "skilled-trades labor",
    "permit-timeline": "permit timeline",
}


def factor_label(factor_id: str) -> str:
    return FACTOR_LABELS.get(factor_id, factor_id)


def _usd_short(value: int) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.0f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.0f}M"
    return f"${value:,}"


def headline(record: dict[str, Any]) -> str:
    project = record["project"]
    top = record["ranking"][0]
    pct = round(top["probability"] * 100)
    return (
        f"{project['name']} ({record['firm']}, {_usd_short(project['announced_capex_usd'])}) "
        f"is most likely bound by {factor_label(top['factor_id'])} "
        f"({pct}%, ~{top['severity_months']} mo slip)."
    )


def ranking_rows(record: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for rank, item in enumerate(record["ranking"], start=1):
        rows.append(
            {
                "rank": rank,
                "factor": factor_label(item["factor_id"]),
                "probability": item["probability"],
                "severity_months": item["severity_months"],
                "evidence_count": len(item["evidence"]),
            }
        )
    return rows


def _bar(probability: float, width: int = 20) -> str:
    filled = round(probability * width)
    return "#" * filled + "-" * (width - filled)


def render_report(records: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for record in records:
        project = record["project"]
        lines.append("=" * 64)
        lines.append(f"binding-constraint diagnostic  ({record['generated_on']})")
        lines.append(f"  plan : {record['plan_name']}")
        lines.append(f"  firm : {record['firm']}  |  capex : {_usd_short(project['announced_capex_usd'])}")
        lines.append(f"  site : {project['geography']}")
        lines.append(f"  done : announced {project['announced_completion']}")
        lines.append("-" * 64)
        lines.append(f"  {'#':<2} {'factor':<22} {'p':>6} {'slip':>6}  bar")
        for row in ranking_rows(record):
            prob = row["probability"]
            lines.append(
                f"  {row['rank']:<2} {row['factor']:<22} "
                f"{prob * 100:>5.0f}% {row['severity_months']:>4}mo  {_bar(prob)}"
            )
        lines.append("-" * 64)
        lines.append("  > " + headline(record))
        lines.append("=" * 64)
    return "\n".join(lines)
