# Exercise 10.2 review

Status: AWAITING HUMAN REVIEW
Human review: Pending

## Requirements

See `docs/EXERCISE_10_2_REQUIREMENTS.md` for the official source, acceptance
criteria and limits. Requirements were freshly retrieved on 2026-10-26.

## Provenance and contributions

Starting point: merged main `5c2ac0d1d53253430f4cf5ae579c4c11d50ba54e`.
PR #1 was merged only after the user's explicit permission and verification
of both successful GitHub checks. Original commits and student text are preserved.

Codex performs requirements analysis, notebook implementation and automated
verification for 10.2. No student review of this exercise has been received.

## Automated verification

Actually executed on 2026-10-26 in the locked Python 3.12.15 environment
(pandas 2.3.3, Matplotlib 3.11.2):

| Command | Actual outcome |
|---|---|
| `scripts/uv.cmd run --locked python scripts/download_ai4i.py` | Download succeeded; CSV SHA256 verified; 522048 bytes |
| Same downloader with `--offline` after acquisition | Existing local source verified, no download needed |
| `scripts/uv.cmd sync --offline --locked` | 105 installed packages checked |
| `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v` | All 13 tests passed |
| `scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_2.py` | All 6 code cells executed in sequence, all three cell types present, HTML and 5-page PDF generated |
| `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py` | Tracked 10.2 notebook schema validated and executed in a fresh kernel |

A temporary JupyterLab process was actually launched from `.venv`, authenticated
`/lab` returned HTTP 200, and the process was then stopped. The web UI was not
manually operated. Kernel execution still prints the known local-TCP warning.

Computed results: 10000 rows × 4 selected columns; no missing values; unique UDI
sequence 1..10000. Torque mean 39.98691 Nm, minimum 3.8 and maximum 76.6 Nm.
These are calculations on the pinned synthetic source, not human observations.
`head(10)` and `describe()` appear in the executed notebook and exports.

Generated files under `outputs/ch10/exercise_10_2/`:
`ai4i_explore.html`, `ai4i_explore.pdf`, `torque_over_udi.png`,
`summary_statistics.csv`. The HTML embeds the actual plot; the build asserts a
PNG notebook output and an image in the PDF, in addition to checking PDF text.
All five PDF pages were rendered with Poppler and inspected. Tables, wrapped
code, plot and review questions are readable without cropped code lines.

### Failures and technical corrections

The first export showed only a textual Figure representation because the Agg
backend had no inline image formatter. Visual inspection caught this even though
the first weak HTML image-string check passed. The notebook now explicitly
embeds its saved PNG using IPython Image; stronger checks require that real output
and an image in the PDF. The strengthened check failed before the notebook
correction and passed after it. A shell-quoted edit attempt also failed and was
replaced by a file-based edit; no failed attempt is treated as successful.
Long code lines were initially clipped in PDF; an export template now wraps them
and keeps tables intact. The corrected exports were regenerated and reinspected.
An initial dependency-add invocation through the batch wrapper misinterpreted
version comparison characters; direct uv execution installed pandas successfully.

These are AI implementation/verification corrections, not invented student feedback.
Hosted CI for the final branch is recorded separately in the draft PR after push.

## Manual review questions

1. Do the four columns, first ten rows and statistics match the official task?
2. Can you explain UDI versus a timestamp and the dataset's synthetic nature?
3. Can you distinguish Code, Markdown and Raw in the actual notebook?
4. Are the HTML/PDF tables and torque plot readable, and can you reproduce them?

## Student feedback and revisions

No feedback or review-driven revisions received. The implementation request
is authorization to work, not approval of the eventual solution.

## Approval

Not granted. Do not merge 10.2, start 10.3 or submit coursework.
