# Exercise 10.1 review

Status: AWAITING_HUMAN_REVIEW
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

Executed locally during workflow adoption on 2026-10-25, using Python 3.12.15
and the locked project environment. Commands below use `scripts/uv.cmd` on Windows.

| Command | Actual result |
|---|---|
| `scripts/uv.cmd sync --offline --locked` | Exit 0; 103 installed packages checked |
| `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v` | Exit 0; 9 tests passed (4 mathematical/image tests and 5 QA tests) |
| `scripts/uv.cmd run --offline --locked python sessions/ch10/aufgabe_10_1.py` | Exit 0; PNG generated |
| `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py` | Exit 0; explicit SKIP, no tracked notebooks |
| `scripts/uv.cmd run --offline --locked python scripts/check_notebook_tools.py` | Exit 0; actual kernel output 4, HTML exported, readable one-page PDF |
| `scripts/uv.cmd run --offline --locked python scripts/check_commit_messages.py --base origin/main` | Exit 0; first two new commits checked before this evidence commit; baseline excluded |
| Workflow YAML parsed with PyYAML; contents permission asserted read-only | Exit 0 |
| `git diff --exit-code d243632 -- sessions/ch10 tests/test_aufgabe_10_1.py outputs/ch10 pyproject.toml uv.lock` | Exit 0; original solution, dependencies and output unchanged |

The generated heart was visually inspected: full closed curve, equal axis scaling,
legible labels, no clipping. The synthetic PDF was rendered with Poppler and visually
inspected: title, code and output readable. Outputs are tooling checks, not student review.

Failures and corrections: the initial staged whitespace check caught an extra final
blank line in AGENTS.md; corrected before commit. The first QA test run had one
error because an invalid-cell fixture triggered a nbformat internal TypeError.
The fixture now uses invalid metadata to test schema rejection; all nine tests
then passed. No failed run is reported as successful.

Kernel execution still emits the known warning about unencrypted local TCP transport.
No tracked exercise notebook, AI4I analysis or Exercise 10.2 is claimed as tested.
Hosted GitHub Actions results are pending until push; local YAML parsing alone
does not prove hosted execution. See the PR checks for the current hosted result.

Technical validation is complete for this local change set. Human review is pending.

## Human feedback

No exercise review feedback received. The request to add QA authorizes technical
work; it is not approval of the mathematical solution or generated code.

## Revisions

No human-review-driven revisions. QA infrastructure and test-fixture corrections
were made by Codex as technical implementation work, not as invented student feedback.

## Remaining review questions

1. Can you explain why one full period is sampled and x is plotted against y?
2. Do the exact formula, equal axis scaling and generated heart satisfy the task?
3. Can you explain the environment, dependency lock and numerical tests?
4. Are the AI disclosure and historical limitations sufficiently transparent?

## Approval

Not granted; no approval date. Exercise 10.2 remains unstarted.
