from __future__ import annotations

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
    total = sum(score.raw_weight for score in scores)
    if total <= 0:
        raise ValidationError("factor raw weights must sum to a positive value")
    factor_order = {factor_id: index for index, factor_id in enumerate(FACTOR_IDS)}
    ranked = sorted(scores, key=lambda score: (-score.raw_weight, factor_order[score.factor_id]))
    probabilities = [round(score.raw_weight / total, 4) for score in ranked]
    correction = round(1.0 - sum(probabilities), 4)
    if probabilities:
        probabilities[0] = round(probabilities[0] + correction, 4)
    return list(zip(ranked, probabilities))


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
