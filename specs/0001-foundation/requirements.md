# Requirements — 0001 Foundation

Numbered requirements for the v0 scaffold of binding-constraint. The
R-BC-* prefix is the brand tag and will appear in every downstream
spec, decision, and gate.

## Core

- **R-BC-001** The repo ships a typed schema for a capex plan input
  under `schemas/capex-plan.schema.json`. Fields: firm, project name,
  geography, announced capex USD, announced energization or completion
  date, project type enum.
- **R-BC-002** The repo defines exactly five constraint factors in v0:
  `chip-allocation`, `transformer-lead-time`, `water-rights`,
  `skilled-trades-labor`, `permit-timeline`. The set is closed in v0;
  expansions require a DEC entry.
- **R-BC-003** The repo ships a constraint-factor schema under
  `schemas/factor-score.schema.json`. Fields: factor id, project id,
  probability (0..1) of being the binding constraint, severity (months
  of delay if it binds), evidence items.
- **R-BC-004** Every factor score must carry at least three evidence
  items. Each item has a public URL, a one-line claim, and a
  retrieved-on date.

## Reports

- **R-BC-005** The repo ships a report template under
  `templates/diagnostic.md.j2` that renders one capex plan into a
  Markdown diagnostic with a headline, a binding-constraint ranking
  table, per-factor evidence sections, and a methodology footer.
- **R-BC-006** The first checked-in report covers one publicly-disclosed
  firm-plan (TSMC Arizona, Intel Ohio, or Micron NY). The choice is
  recorded in DEC-BC-001.

## Discipline

- **R-BC-007** Every claim in a report cites a source URL inline. The
  voice-lint gate fails the report if any factor section has zero
  citations.
- **R-BC-008** The diagnostic produces a probability distribution over
  the five factors per project. It does not collapse to a single
  factor in the structured output; the headline only names the modal
  factor.
- **R-BC-009** A backtest harness scores past diagnostics against
  actual delivered capex from 2018-2025. v0 ships the harness skeleton;
  the calibration metric is Brier on factor-occurrence.

## Governance

- **R-BC-010** Architectural choices are recorded in
  `decisions/DEC-BC-NNN-<slug>.md`. The first decision (DEC-BC-001)
  picks the v0 firm-plan and justifies the five-factor closure.
