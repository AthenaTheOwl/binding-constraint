from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from .model import FACTOR_IDS, FactorScore, Plan, Project, ValidationError


def build_records(plan: Plan, scores: tuple[FactorScore, ...], generated_on: str) -> list[dict]:
    by_project = _scores_by_project(scores)
    records = []
    for project in plan.projects:
        ranked = _rank_scores(by_project[project.project_id])
        records.append(_record_for_project(plan, project, ranked, generated_on))
    return records


def _scores_by_project(scores: tuple[FactorScore, ...]) -> dict[str, list[FactorScore]]:
    grouped: dict[str, list[FactorScore]] = {}
    for score in scores:
        grouped.setdefault(score.project_id, []).append(score)
    return grouped


def _rank_scores(scores: list[FactorScore]) -> list[tuple[FactorScore, float]]:
    scale = max((score.raw_weight for score in scores), default=0.0)
    if scale <= 0:
        raise ValidationError("factor raw weights must sum to a positive value")
    total = sum(score.raw_weight / scale for score in scores)
    factor_order = {factor_id: index for index, factor_id in enumerate(FACTOR_IDS)}
    ranked = sorted(scores, key=lambda score: (-score.raw_weight, factor_order[score.factor_id]))
    probabilities = [_round_probability((score.raw_weight / scale) / total) for score in ranked]
    if probabilities:
        probabilities[0] += Decimal(1) - sum(probabilities)
    return [(score, float(probability)) for score, probability in zip(ranked, probabilities)]


# Float division leaves ~1e-16 of noise, so a share that is exactly on a
# 4-decimal half (e.g. 0.0875 / 0.29375) can land just above or just below it
# depending on how the weights were scaled. Snapping to 12 decimals first
# removes that noise; the 4-decimal step then rounds half up deterministically,
# so rescaling every weight by the same constant reproduces the same numbers.
_SNAP = Decimal("1e-12")
_REPORTED = Decimal("0.0001")


def _round_probability(share: float) -> Decimal:
    snapped = Decimal(share).quantize(_SNAP, rounding=ROUND_HALF_UP)
    return snapped.quantize(_REPORTED, rounding=ROUND_HALF_UP)


def _record_for_project(
    plan: Plan,
    project: Project,
    ranked: list[tuple[FactorScore, float]],
    generated_on: str,
) -> dict:
    ranking = [score.to_ranking_dict(probability) for score, probability in ranked]
    return {
        "artifact_version": "0.1",
        "firm": plan.firm,
        "generated_on": generated_on,
        "modal_factor": ranking[0]["factor_id"],
        "plan_id": plan.plan_id,
        "plan_name": plan.plan_name,
        "probability_sum": round(sum(item["probability"] for item in ranking), 4),
        "project": {
            "announced_capex_usd": project.announced_capex_usd,
            "announced_completion": project.announced_completion,
            "geography": project.geography,
            "name": project.name,
            "project_id": project.project_id,
            "project_type": project.project_type,
            "public_sources": list(project.public_sources),
        },
        "ranking": ranking,
    }
