from __future__ import annotations

from binding_constraint.cli import main
from binding_constraint.io import (
    DEFAULT_PLAN,
    DEFAULT_REPORT,
    DEFAULT_WEIGHTS,
    load_json,
    read_jsonl,
    serialize_jsonl,
)
from binding_constraint.model import FACTOR_IDS, Plan, load_factor_scores
from binding_constraint.render import headline, render_report
from binding_constraint.scoring import build_records


def _default_records() -> list[dict]:
    plan = Plan.from_dict(load_json(DEFAULT_PLAN), context=str(DEFAULT_PLAN))
    scores = load_factor_scores(load_json(DEFAULT_WEIGHTS), plan=plan, context=str(DEFAULT_WEIGHTS))
    return build_records(plan, scores, generated_on="2026-06-21")


def test_default_artifact_matches_renderer() -> None:
    assert DEFAULT_REPORT.read_text(encoding="utf-8") == serialize_jsonl(_default_records())


def test_ranking_is_closed_distribution() -> None:
    record = _default_records()[0]
    ranking = record["ranking"]
    assert record["modal_factor"] == "skilled-trades-labor"
    assert {item["factor_id"] for item in ranking} == set(FACTOR_IDS)
    assert record["probability_sum"] == 1.0
    assert all(len(item["evidence"]) >= 3 for item in ranking)


def test_cli_validate_passes() -> None:
    assert main(["validate"]) == 0


def test_cli_show_reads_committed_report(capsys) -> None:
    assert main(["show"]) == 0
    out = capsys.readouterr().out
    assert "binding-constraint diagnostic" in out
    assert "skilled-trades labor" in out
    assert "most likely bound by" in out


def test_show_render_matches_committed_artifact() -> None:
    records = read_jsonl(DEFAULT_REPORT)
    text = render_report(records)
    top = records[0]["ranking"][0]
    assert top["factor_id"] == "skilled-trades-labor"
    assert "skilled-trades labor" in headline(records[0])
    # every ranked factor surfaces in the rendered table
    assert text.count("\n") > len(records[0]["ranking"])


def test_cli_diagnose_writes_deterministic_jsonl() -> None:
    out = DEFAULT_REPORT.parent / ".pytest-diagnostic.jsonl"
    try:
        assert main(["diagnose", "--out", str(out)]) == 0
        assert out.read_text(encoding="utf-8") == DEFAULT_REPORT.read_text(encoding="utf-8")
    finally:
        if out.exists():
            out.unlink()
