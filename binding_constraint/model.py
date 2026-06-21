from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


FACTOR_IDS = (
    "chip-allocation",
    "transformer-lead-time",
    "water-rights",
    "skilled-trades-labor",
    "permit-timeline",
)


class ValidationError(ValueError):
    """Raised when fixture data fails the v0.1 contract."""


def _require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{context} must be an object")
    return value


def _require_keys(data: dict[str, Any], keys: tuple[str, ...], context: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise ValidationError(f"{context} missing required keys: {', '.join(missing)}")


def _require_text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value


def _require_date(value: Any, context: str) -> str:
    text = _require_text(value, context)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context} must be an ISO date") from exc
    return text


def _require_public_url(value: Any, context: str) -> str:
    text = _require_text(value, context)
    if not text.startswith(("https://", "http://")):
        raise ValidationError(f"{context} must be a public URL")
    return text


def _require_number(value: Any, context: str, minimum: float = 0.0) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationError(f"{context} must be a number")
    number = float(value)
    if number < minimum:
        raise ValidationError(f"{context} must be >= {minimum}")
    return number


@dataclass(frozen=True)
class EvidenceItem:
    url: str
    claim: str
    retrieved_on: str

    @classmethod
    def from_dict(cls, value: Any, context: str) -> "EvidenceItem":
        data = _require_mapping(value, context)
        _require_keys(data, ("url", "claim", "retrieved_on"), context)
        return cls(
            url=_require_public_url(data["url"], f"{context}.url"),
            claim=_require_text(data["claim"], f"{context}.claim"),
            retrieved_on=_require_date(data["retrieved_on"], f"{context}.retrieved_on"),
        )

    def to_dict(self) -> dict[str, str]:
        return {"claim": self.claim, "retrieved_on": self.retrieved_on, "url": self.url}


@dataclass(frozen=True)
class Project:
    project_id: str
    name: str
    geography: str
    project_type: str
    announced_capex_usd: int
    announced_completion: str
    public_sources: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Any, context: str) -> "Project":
        data = _require_mapping(value, context)
        _require_keys(
            data,
            (
                "project_id",
                "name",
                "geography",
                "project_type",
                "announced_capex_usd",
                "announced_completion",
                "public_sources",
            ),
            context,
        )
        sources = data["public_sources"]
        if not isinstance(sources, list) or not sources:
            raise ValidationError(f"{context}.public_sources must be a non-empty list")
        capex = _require_number(data["announced_capex_usd"], f"{context}.announced_capex_usd", minimum=1.0)
        return cls(
            project_id=_require_text(data["project_id"], f"{context}.project_id"),
            name=_require_text(data["name"], f"{context}.name"),
            geography=_require_text(data["geography"], f"{context}.geography"),
            project_type=_require_text(data["project_type"], f"{context}.project_type"),
            announced_capex_usd=int(capex),
            announced_completion=_require_date(data["announced_completion"], f"{context}.announced_completion"),
            public_sources=tuple(
                _require_public_url(source, f"{context}.public_sources[{index}]")
                for index, source in enumerate(sources)
            ),
        )


@dataclass(frozen=True)
class Plan:
    plan_id: str
    firm: str
    plan_name: str
    retrieved_on: str
    projects: tuple[Project, ...]

    @classmethod
    def from_dict(cls, value: Any, context: str) -> "Plan":
        data = _require_mapping(value, context)
        _require_keys(data, ("plan_id", "firm", "plan_name", "retrieved_on", "projects"), context)
        projects = data["projects"]
        if not isinstance(projects, list) or not projects:
            raise ValidationError(f"{context}.projects must be a non-empty list")
        parsed = tuple(Project.from_dict(item, f"{context}.projects[{index}]") for index, item in enumerate(projects))
        project_ids = [project.project_id for project in parsed]
        if len(project_ids) != len(set(project_ids)):
            raise ValidationError(f"{context}.projects has duplicate project_id values")
        return cls(
            plan_id=_require_text(data["plan_id"], f"{context}.plan_id"),
            firm=_require_text(data["firm"], f"{context}.firm"),
            plan_name=_require_text(data["plan_name"], f"{context}.plan_name"),
            retrieved_on=_require_date(data["retrieved_on"], f"{context}.retrieved_on"),
            projects=parsed,
        )


@dataclass(frozen=True)
class FactorScore:
    project_id: str
    factor_id: str
    raw_weight: float
    severity_months: int
    evidence: tuple[EvidenceItem, ...]

    @classmethod
    def from_dict(cls, value: Any, context: str) -> "FactorScore":
        data = _require_mapping(value, context)
        _require_keys(data, ("project_id", "factor_id", "raw_weight", "severity_months", "evidence"), context)
        factor_id = _require_text(data["factor_id"], f"{context}.factor_id")
        if factor_id not in FACTOR_IDS:
            raise ValidationError(f"{context}.factor_id must be one of: {', '.join(FACTOR_IDS)}")
        evidence = data["evidence"]
        if not isinstance(evidence, list) or len(evidence) < 3:
            raise ValidationError(f"{context}.evidence must contain at least three items")
        return cls(
            project_id=_require_text(data["project_id"], f"{context}.project_id"),
            factor_id=factor_id,
            raw_weight=_require_number(data["raw_weight"], f"{context}.raw_weight"),
            severity_months=int(_require_number(data["severity_months"], f"{context}.severity_months")),
            evidence=tuple(
                EvidenceItem.from_dict(item, f"{context}.evidence[{index}]")
                for index, item in enumerate(evidence)
            ),
        )

    def to_ranking_dict(self, probability: float) -> dict[str, Any]:
        return {
            "evidence": [item.to_dict() for item in self.evidence],
            "factor_id": self.factor_id,
            "probability": probability,
            "severity_months": self.severity_months,
        }


def load_factor_scores(value: dict[str, Any], plan: Plan, context: str) -> tuple[FactorScore, ...]:
    _require_keys(value, ("plan_id", "factor_scores"), context)
    plan_id = _require_text(value["plan_id"], f"{context}.plan_id")
    if plan_id != plan.plan_id:
        raise ValidationError(f"{context}.plan_id does not match {plan.plan_id}")
    items = value["factor_scores"]
    if not isinstance(items, list) or not items:
        raise ValidationError(f"{context}.factor_scores must be a non-empty list")
    scores = tuple(FactorScore.from_dict(item, f"{context}.factor_scores[{index}]") for index, item in enumerate(items))
    _validate_factor_coverage(scores, plan, context)
    return scores


def _validate_factor_coverage(scores: tuple[FactorScore, ...], plan: Plan, context: str) -> None:
    project_ids = {project.project_id for project in plan.projects}
    seen: dict[str, set[str]] = {project_id: set() for project_id in project_ids}
    for score in scores:
        if score.project_id not in project_ids:
            raise ValidationError(f"{context} has score for unknown project_id {score.project_id}")
        if score.factor_id in seen[score.project_id]:
            raise ValidationError(f"{context} repeats {score.factor_id} for {score.project_id}")
        seen[score.project_id].add(score.factor_id)
    required = set(FACTOR_IDS)
    for project_id, factors in seen.items():
        if factors != required:
            missing = sorted(required - factors)
            extra = sorted(factors - required)
            details = []
            if missing:
                details.append(f"missing {', '.join(missing)}")
            if extra:
                details.append(f"extra {', '.join(extra)}")
            raise ValidationError(f"{context} coverage for {project_id} is invalid: {'; '.join(details)}")
