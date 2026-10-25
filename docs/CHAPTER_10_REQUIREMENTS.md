# Chapter 10 requirements and scope

Source: [official Chapter 10](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), retrieved 2026-10-25.
This is a task inventory in our own words, not a copy of the manuscript.

| Exercise | Required outcome | Current scope |
|---|---|---|
| 10.1 | Install uv, initialize an isolated Python project, install NumPy and Matplotlib, plot the specified parametric curve and explain environment management | Implemented; numerical and image checks required before commit |
| 10.2 | Notebook with AI4I data, specified columns, first ten rows, statistics, torque line plot, different cell types, HTML/PDF exports | Blocked on user review of 10.1; no solution started |
| 10.3 | Seaborn distribution, relationship and advanced plots; reasoned observations | Not started |
| 10.4 | Quarto report and notebook rendering to HTML/PDF, chunk options and presentation | Not started; Quarto/Pandoc/TeX setup deferred to this exercise |

For 10.1 the exact mathematical requirements are
`x = 16*sin(t)**3` and
`y = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)`.
The script uses `numpy.linspace` over one complete period, plots x against y,
and preserves equal axis scaling. No empirical dataset or experimental result is involved.

Jupyter installation and a synthetic export check are workspace infrastructure,
not a start on Exercise 10.2. No AI4I dataset is downloaded or analyzed.
