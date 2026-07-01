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
from binding_constraint.model import (
    FACTOR_IDS,
    EvidenceItem,
    FactorScore,
    Plan,
    load_factor_scores,
)
from binding_constraint.render import headline, render_report
from binding_constraint.scoring import _rank_scores, build_records


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


# Golden-master lock on the whole rendered table. The display layer (bar width,
# USD short form, rank numbering, severity column) has no other pin, so any
# change to the columns or bar has to update this literal on purpose.
EXPECTED_RENDER = (
    "================================================================\n"
    "binding-constraint diagnostic  (2026-06-21)\n"
    "  plan : TSMC Arizona advanced semiconductor manufacturing site\n"
    "  firm : TSMC  |  capex : $65B\n"
    "  site : Phoenix, Arizona, United States\n"
    "  done : announced 2030-12-31\n"
    "----------------------------------------------------------------\n"
    "  #  factor                      p   slip  bar\n"
    "  1  skilled-trades labor      33%   18mo  #######-------------\n"
    "  2  water rights              24%   12mo  #####---------------\n"
    "  3  transformer lead time     18%    9mo  ####----------------\n"
    "  4  permit timeline           15%    6mo  ###-----------------\n"
    "  5  chip allocation           10%    4mo  ##------------------\n"
    "----------------------------------------------------------------\n"
    "  > Arizona advanced semiconductor manufacturing site (TSMC, $65B) "
    "is most likely bound by skilled-trades labor (33%, ~18 mo slip).\n"
    "================================================================"
)


def test_render_report_matches_golden() -> None:
    assert render_report(read_jsonl(DEFAULT_REPORT)) == EXPECTED_RENDER


def test_headline_pins_pct_slip_and_capex() -> None:
    records = read_jsonl(DEFAULT_REPORT)
    line = headline(records[0])
    assert "(33%, ~18 mo slip)" in line
    assert "$65B" in line


def _evidence() -> tuple[EvidenceItem, ...]:
    return tuple(
        EvidenceItem(url=f"https://example.test/{i}", claim="c", retrieved_on="2026-01-01")
        for i in range(3)
    )


def test_rank_scores_absorbs_rounding_residual_into_top() -> None:
    # Three equal weights round to 0.3333 each and sum to 0.9999, so the
    # closed-distribution correction (+0.0001) has to land on the top factor.
    ev = _evidence()
    scores = [
        FactorScore(project_id="p", factor_id="chip-allocation", raw_weight=1.0, severity_months=1, evidence=ev),
        FactorScore(project_id="p", factor_id="water-rights", raw_weight=1.0, severity_months=1, evidence=ev),
        FactorScore(project_id="p", factor_id="permit-timeline", raw_weight=1.0, severity_months=1, evidence=ev),
    ]
    probabilities = [probability for _, probability in _rank_scores(scores)]
    assert probabilities == [0.3334, 0.3333, 0.3333]
    assert sum(probabilities) == 1.0


def test_validate_reports_missing_plan_without_traceback(capsys) -> None:
    assert main(["validate", "--plan", "does-not-exist.json"]) == 1
    err = capsys.readouterr().err
    assert err.startswith("ERROR: ")
    assert "does-not-exist.json" in err


def test_diagnose_reports_non_object_plan_without_traceback(tmp_path, capsys) -> None:
    bad = tmp_path / "array.json"
    bad.write_text("[1, 2, 3]", encoding="utf-8")
    assert main(["diagnose", "--plan", str(bad)]) == 1
    err = capsys.readouterr().err
    assert err.startswith("ERROR: ")
    assert "must contain a JSON object" in err


def test_validate_reports_malformed_json_without_traceback(tmp_path, capsys) -> None:
    bad = tmp_path / "garbage.json"
    bad.write_text("not json", encoding="utf-8")
    assert main(["validate", "--plan", str(bad)]) == 1
    assert capsys.readouterr().err.startswith("ERROR: ")
