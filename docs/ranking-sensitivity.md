# A normalized ranking still needs a sensitivity test

Method update: October 18, 2026. Proposed experiments below are not reported as executed results.

The engine normalizes curated factor weights in `binding_constraint/scoring.py`. A closed distribution is useful for comparing factors inside one diagnostic. Its sum of one does not establish calibration against completed projects. Multiplying every raw weight by the same constant leaves the ranking unchanged and adds no evidence.

A useful next experiment perturbs one factor at a time while holding the other four fixed. Record the smallest relative weight change that changes the modal factor. A close contest should carry that switch threshold beside the modal label. Keep evidence age and source quality separate from the numerical perturbation; additional citations to the same announcement do not create independent observations.

The implemented input gate now rejects NaN and infinity before normalization. Remaining proposed checks are scale invariance, ties, near-ties, and a report that states the cohort and forecast horizon before using probability language. Recalibration requires observed completion outcomes and a held-out cohort. A score change caused only by new rubric weights should preserve the old report and explain the changed assumption.

## References

- https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
- https://github.com/3orionkings/ai-product-team/blob/main/workflows/process-change.md
