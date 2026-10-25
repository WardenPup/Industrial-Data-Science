# Exercise 10.1 review

Status: APPROVED
Human review: Approved
Approval recorded: 2026-10-26 (Europe/Berlin), based on the student's explicit
written approval below and confirmation in the current request.
Merge authorization: Not granted. Exercise 10.2 remains unstarted.

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

Technical validation for the workflow-adoption change set was completed before
human review. The subsequent student review and fresh validation are recorded below.

## Human feedback

The student subsequently added the German verification and explicit approval
preserved below, and four answers in `sessions/ch10/aufgabe_10_1.md`.
The current request confirms that these are the student's manual contributions.
The original text was committed separately in `42cebaf` before AI status updates.
No additional student observations or independently measured results are inferred.

## Revisions

No code corrections were requested by the student. Codex reconciled stale
AI-written pending-status summaries after receiving approval. The student's
review and answers remain verbatim. QA infrastructure and earlier fixture
corrections remain AI technical work, not student contributions.

## Remaining review questions

1. Can you explain why one full period is sampled and x is plotted against y?
2. Do the exact formula, equal axis scaling and generated heart satisfy the task?
3. Can you explain the environment, dependency lock and numerical tests?
4. Are the AI disclosure and historical limitations sufficiently transparent?

## Approval

The student's explicit "Human Review: Approved" is accepted after fresh checks.
Approval is recorded on 2026-10-26; the earlier manual review's exact time was
not supplied and is not invented. This approval does not authorize merging.

## AI validation after human review (2026-10-26)

Codex compared both manually changed files against Git HEAD before editing.
The official task was freshly retrieved. The formula, `linspace` interval and
1001 samples, finite/closed/symmetric coordinates, equal aspect ratio, Agg backend,
output path and 160-DPI save configuration support the student's statements.
The PNG is 1120 × 1120; Pillow reports 159.9946 DPI because PNG density is stored
in integer pixels/metre, consistent with a requested 160 DPI.
Visual inspection confirmed the complete heart and readable labels.

Actual commands, all exit 0 unless explicitly described as a skip:

| Command | Result |
|---|---|
| `scripts/uv.cmd sync --offline --locked` | 103 installed packages checked |
| `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v` | All 9 tests passed |
| `scripts/uv.cmd run --offline --locked python sessions/ch10/aufgabe_10_1.py` | Required PNG generated |
| `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py` | Explicit SKIP: no tracked notebooks |
| `scripts/uv.cmd run --offline --locked python scripts/check_notebook_tools.py` | Synthetic kernel output 4; HTML and readable one-page PDF exported |
| `scripts/uv.cmd run --offline --locked python scripts/check_commit_messages.py --base origin/main` | All 3 preceding QA commits passed before the review commit |

The image size and DPI were additionally asserted using Pillow in a local Python
command. The fresh official-source comparison confirms all Exercise 10.1
requirements: uv project and isolation, NumPy/Matplotlib, prescribed parametric
plot and an explanation of the environment. No empirical result is claimed.

Discrepancies reported before proceeding: stale AI-written Pending/Not granted
summaries conflicted with the new approval and were reconciled here. The student's
wording that `.venv` creates the environment is a small terminology imprecision:
uv creates it; `.venv` contains it. A separate AI clarification was appended to
the solution, preserving the original answer. No mathematical discrepancy found.
The known kernel local-TCP warning persists; execution/export succeeded.
Hosted checks for the new commits must be read from PR #1, not inferred from
older successful runs. No merge or Exercise 10.2 work has been performed.

## Original student contribution (preserved verbatim)


Human Review – Aufgabe 10.1

Status: Freigegeben nach manueller Prüfung
KI-Unterstützung: Codex

Konkrete Prüfergebnisse

Skriptausführung: Das Skript wurde erfolgreich ausgeführt. Die Grafik wurde unter outputs/ch10/aufgabe_10_1_herz.png gespeichert.

Mathematische Formeln: Die Implementierung entspricht den vorgegebenen Gleichungen für x(t) und y(t). Mit np.linspace(0, 2π, 1001) wird eine vollständige Periode einschließlich der Endpunkte berechnet.

Kurvenschluss: Bei t = 0 und t = 2π ergeben sich dieselben Koordinaten (x ≈ 0, y = 5). Die Herzkurve ist somit geschlossen.

Visualisierung: Die ausgegebene Grafik zeigt eine symmetrische Herzform. Durch set_aspect("equal") werden beide Achsen im gleichen Maßstab dargestellt.

Dateiausgabe: Die Grafik wird mit 160 DPI gespeichert. Durch matplotlib.use("Agg") ist keine grafische Benutzeroberfläche erforderlich.

Codequalität: Die Funktionen heart_coordinates(), save_plot() und main() sind klar getrennt. Ungültige Werte für samples unter 3 werden mit einem ValueError abgefangen.

Ergebnis

Die überprüfte Lösung funktioniert wie erwartet. Es wurden keine offensichtlichen Fehler festgestellt.

Human Review: Approved
