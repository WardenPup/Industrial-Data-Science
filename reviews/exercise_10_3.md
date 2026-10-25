# Exercise 10.3 review

Status: AWAITING HUMAN REVIEW
Human review: Pending

## Requirements and provenance

Official instructions and acceptance criteria: `docs/EXERCISE_10_3_REQUIREMENTS.md`.
Starting commit: merged main `40b31c64b88d9441be3ac9eb71433bdb49b7e4f9`.
PR #2 was merged only after explicit student merge authorization and inspection
of both successful current-head checks. Its commits and student text are preserved.

Codex performs requirements analysis, implementation and technical checks for 10.3.
No student review, feedback or approval of this exercise has been received.

## Verification

Actual local verification on 2026-10-26, Python 3.12.15, pandas 2.3.3,
Matplotlib 3.11.2, Seaborn 0.13.2, SciPy 1.18.1:

| Command | Actual outcome |
|---|---|
| `scripts/uv.cmd run --offline --locked python scripts/download_ai4i.py` | Existing official CSV SHA256 verified |
| `scripts/uv.cmd sync --offline --locked` | 107 installed packages checked |
| `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v` | Initially 17 passed; after the IQR regression test, all 18 passed |
| `scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_3.py` | 12 code cells executed sequentially; ten real notebook PNG outputs and ten embedded HTML figures |
| `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py` | Both tracked notebooks validated and executed in fresh kernels |
| `.venv/Scripts/python.exe .tools/check_exercise3_html.py` | Offline browser render succeeded; all ten images decoded; tables and page fit a 1400-pixel viewport |

The task-local HTML helper also captured representative page sections, which
Codex inspected. All ten PNG figures were separately inspected for titles,
units, labels, legends, clipping and interpretability. Histogram/box/violin
figures each contain all three measurement panels; the pairplot contains the
three-variable grid. PNG sizes/nonblank content and all ten manifest checksums
were verified. A fresh notebook rerun reproduces the saved PNG checksums.
No notebook error or stderr output is saved. The existing local TCP kernel
warning is still emitted externally during kernel startup.

### Actual computed results and limits

All 10000 rows are retained; `numeric` has only the three measurement columns.
Torque/speed is the strongest pair: Pearson −0.8750270863, Spearman −0.9164741739.
The scatter/pairplot shows a curved negative monotonic relation. Temperature
correlations are small, which is not proof of independence or no physical effect.
Torque is roughly symmetric/bell-shaped, speed right-skewed, and temperature
irregular/multihumped. No normality or causal claim is made.

IQR flags with explicit floating-point tolerance: 64 Torque, 418 speed, 0 air.
Skewness: −0.0095166 / 1.9931710 / 0.1142739 respectively.
Equal-width speed-bin counts: 8965 / 975 / 60; ten torque-bin counts sum to 10000.
Correlations, IQR statistics, counts and exact bin edges are saved as CSV/JSON.
The plotted regression is descriptive, without an inferential confidence band.
Bins, KDE bandwidth, overplotting, arbitrary row ordering and the synthetic
source constrain the interpretation. UDI is not a timestamp.

### Genuine correction during validation

The first execution generated all plots and passed its existing tests. Manual
numerical inspection then found that decimal values on theoretical IQR fences
were flagged because 12.8 differs from 12.800000000000011 (and likewise 67.2).
Four lower-boundary and one upper-boundary values changed the naive torque
count from 69 to 64. An explicit absolute 1e-10 comparison tolerance and a tiny
boxplot-whisker expansion resolve this; a new boundary regression test passes.
The notebook discloses the choices. Stripplot color contrast was improved.
No test failure or student feedback is invented; this was AI technical correction.

### Outputs and requirement coverage

`sessions/ch10/ai4i_seaborn.ipynb` is executed. `outputs/ch10/exercise_10_3/`
contains the HTML, ten named PNGs, plot manifest, IQR/correlation tables and
bin counts/edges. Every figure group and observation question from the official
assignment is covered; see `docs/EXERCISE_10_3_REQUIREMENTS.md`.
No PDF is generated because Exercise 10.3 does not request it. Exercise 10.4
and its Quarto reporting work have not begun. Hosted checks must be inspected
on the draft PR after push; local results do not imply hosted success.

## Questions for student review

1. Do all requested plots and three-variable panels appear clearly in the notebook/HTML?
2. Can you distinguish a boxplot from a KDE violin and explain why an IQR flag is not a proven error?
3. What do Pearson, Spearman and the curved point cloud each describe about torque/speed?
4. How do unequal bin counts, jitter, KDE bandwidth and overplotting affect interpretation?
5. Which conclusions are precluded by synthetic data, absent timestamps and purely descriptive analysis?

## Human review and approval

Pending. Do not merge 10.3, start 10.4 or submit coursework.
