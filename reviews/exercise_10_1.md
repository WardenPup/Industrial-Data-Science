# Exercise 10.1 review

Status: DRAFT
Human review: Pending

## Requirements and acceptance criteria

Source: [official Exercise 10.1](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html).
Requirements were retrieved on 2026-10-25 in the preceding setup work;
see `docs/CHAPTER_10_REQUIREMENTS.md`. This record adopts the new workflow
after implementation; it is not evidence of a pre-implementation review.

- uv provides an isolated, reproducible Python project with NumPy and Matplotlib.
- A script samples a complete period with `numpy.linspace` and plots
  `x=16*sin(t)**3`, `y=13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)`.
- Verify independent known points, closure, symmetry, finite values and PNG export.
- Explain environment isolation, lockfile, parameterization and plot interpretation.
- Verify the generated plot visually; no empirical results are involved.
- No university submission format or deadline is established by this record.
  Never submit automatically.

## Existing implementation and provenance

Baseline: `d243632ee80ec73bd066b113a81f24cca8850a9a`, already on main before this
workflow was requested. It contains the genuine setup, code, tests and plot.
No commits are split, backdated, amended or relabelled as earlier development phases.
The PR adds prospective QA and review evidence; it cannot retrospectively gate
the original code's inclusion on main.

Codex generated the implementation and documentation and ran technical checks in
the preceding conversation. The configured Git account appears in baseline Git
metadata; this does not establish independent student authorship or human review.
Current AI contributions: workflow rules, templates, CI, validation and evidence.

## Verification for this workflow adoption

Not run yet for this change set. Prior checks are documented in `docs/STATUS.md`;
they are not substituted for the forthcoming validation of the new QA tooling.

## Human feedback

No exercise review feedback received. The request to add QA authorizes technical
work; it is not approval of the mathematical solution or generated code.

## Revisions

No human-review-driven revisions. New QA infrastructure will be recorded as such.

## Remaining review questions

1. Can you explain why one full period is sampled and x is plotted against y?
2. Do the exact formula, equal axis scaling and generated heart satisfy the task?
3. Can you explain the environment, dependency lock and numerical tests?
4. Are the AI disclosure and historical limitations sufficiently transparent?

## Approval

Not granted; no approval date. Exercise 10.2 remains unstarted.
