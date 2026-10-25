# Chapter 10 requirements and scope

Source: [official Chapter 10](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), retrieved 2026-10-25.
This is a task inventory in our own words, not a copy of the manuscript.

| Exercise | Required outcome | Current scope |
|---|---|---|
| 10.1 | Install uv, initialize an isolated Python project, install NumPy and Matplotlib, plot the specified parametric curve and explain environment management | Human-approved; PR #1 merged on 2026-10-26 |
| 10.2 | Notebook with AI4I data, specified columns, first ten rows, statistics, torque line plot, different cell types, HTML/PDF exports | Technically validated and explicitly human-approved; merge permission withheld |
| 10.3 | Seaborn distribution, relationship and advanced plots; reasoned observations | Not started |
| 10.4 | Quarto report and notebook rendering to HTML/PDF, chunk options and presentation | Not started; Quarto/Pandoc/TeX setup deferred to this exercise |

For 10.1 the exact mathematical requirements are
`x = 16*sin(t)**3` and
`y = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)`.
The script uses `numpy.linspace` over one complete period, plots x against y,
and preserves equal axis scaling. No empirical dataset or experimental result is involved.

The original synthetic export check remains separate from Exercise 10.2.
AI4I acquisition and the 10.2 notebook were subsequently implemented after explicit
authorization. See `docs/EXERCISE_10_2_REQUIREMENTS.md` and `reviews/exercise_10_2.md`.
