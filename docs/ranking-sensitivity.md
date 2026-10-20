# A normalized ranking still needs a sensitivity test

Method update: October 18, 2026. Proposed experiments below are not reported as executed results.

The engine normalizes curated factor weights in `binding_constraint/scoring.py`. The checked-in TSMC Arizona weights already sum to 1.0, so on the shipped case normalization returns them unchanged: each reported probability is the curated raw weight. Normalization changes the numbers only when the weights do not sum to one, as in the Streamlit what-if sliders, and it never changes the ranking, which sorts on the raw weights. A closed distribution is useful for comparing factors inside one diagnostic. Its sum of one does not establish calibration against completed projects. Multiplying every raw weight by the same constant leaves the ranking unchanged and adds no evidence.

A useful next experiment perturbs one factor at a time while holding the other four fixed. Record the smallest relative weight change that changes the modal factor. A close contest should carry that switch threshold beside the modal label. Keep evidence age and source quality separate from the numerical perturbation; additional citations to the same announcement do not create independent observations.

The implemented input gate now rejects NaN and infinity before normalization. Scale invariance of the ranking is now covered by a test; reported probabilities can still shift by 0.0001 at 4-decimal rounding ties. Remaining proposed checks are ties, near-ties, and a report that states the cohort and forecast horizon before using probability language. Recalibration requires observed completion outcomes and a held-out cohort. A score change caused only by new rubric weights should preserve the old report and explain the changed assumption.
