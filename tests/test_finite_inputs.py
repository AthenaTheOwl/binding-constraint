import pytest

from binding_constraint.io import DEFAULT_PLAN, DEFAULT_WEIGHTS, load_json
from binding_constraint.model import Plan, ValidationError, load_factor_scores
from binding_constraint.scoring import _rank_scores


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 10 ** 400])
def test_nonfinite_weights_fail_before_probability_normalization(value):
    plan = Plan.from_dict(load_json(DEFAULT_PLAN), "plan")
    weights = load_json(DEFAULT_WEIGHTS)
    weights["factor_scores"][0]["raw_weight"] = value
    with pytest.raises(ValidationError, match="finite"):
        load_factor_scores(weights, plan, "weights")


def test_large_finite_weights_normalize_without_overflowing_the_sum():
    plan = Plan.from_dict(load_json(DEFAULT_PLAN), "plan")
    weights = load_json(DEFAULT_WEIGHTS)
    for row in weights["factor_scores"]:
        row["raw_weight"] = 1e308
    scores = load_factor_scores(weights, plan, "weights")
    assert [probability for _, probability in _rank_scores(list(scores))] == [0.2] * 5
