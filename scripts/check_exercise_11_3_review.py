"""Verify reviewed STL parameters, all stages, saved results and figure paths."""

import hashlib
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".tools/matplotlib"))
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from statsmodels.tsa.seasonal import STL

from sessions.ch11.imputation import load_smoothed_input, gap_table
from sessions.ch11.stl_imputation import stl_impute, STL_CONFIG, FIT_CONFIG
from sessions.ch11.stl_plots import seasonal_decompose_seaborn, plot_deseasonalized, plot_final_production, plot_long_gap


def main():
    expected_config = {"period": 52, "seasonal": 13, "trend": 101, "low_pass": 53, "robust": True}
    assert STL_CONFIG == expected_config and FIT_CONFIG == {"inner_iter": 2, "outer_iter": 15}
    frame, source = load_smoothed_input()
    original = source.copy()
    known = source.notna().to_numpy()
    assert len(source) == 1044 and known.sum() == 677 and (~known).sum() == 367
    with patch("sessions.ch11.stl_imputation.STL", wraps=STL) as invocation:
        stages, decomposition = stl_impute(source)
        assert invocation.call_args.kwargs == expected_config
    pd.testing.assert_series_equal(source, original)
    positions = np.arange(len(source))
    preliminary = np.interp(positions, positions[known], source.to_numpy()[known])
    np.testing.assert_allclose(stages.preliminary_linear, preliminary, rtol=1e-14)
    # Direct reference call checks invocation/configuration, not unknown truth.
    reference = STL(pd.Series(preliminary, index=source.index), **expected_config).fit(inner_iter=2, outer_iter=15)
    for column, attribute in [("trend", "trend"), ("seasonal", "seasonal"), ("residual", "resid")]:
        np.testing.assert_allclose(stages[column], getattr(reference, attribute), rtol=1e-12, atol=1e-10)
    deseasonalized = source.to_numpy() - stages.seasonal.to_numpy()
    assert np.array_equal(np.isnan(deseasonalized), ~known)
    completed = np.interp(positions, positions[known], deseasonalized[known])
    final = completed + stages.seasonal.to_numpy()
    final[known] = source.to_numpy()[known]
    np.testing.assert_allclose(stages.deseasonalized_gaps, deseasonalized, equal_nan=True)
    np.testing.assert_allclose(stages.deseasonalized_linear, completed, rtol=1e-12)
    np.testing.assert_allclose(stages.final_imputed, final, rtol=1e-12)
    assert np.array_equal(stages.final_imputed.to_numpy()[known], source.to_numpy()[known])
    assert np.isfinite(final).all() and not (final[~known] < 0).any()
    difference = np.abs(final[~known] - preliminary[~known])
    assert round(difference.mean(), 4) == 9.7462 and round(difference.max(), 4) == 75.2469
    reconstruction = np.max(np.abs(preliminary - stages.trend - stages.seasonal - stages.residual))
    assert reconstruction < 1e-9
    output = ROOT / "outputs/ch11/exercise_11_3"
    saved = pd.read_csv(ROOT / "data/processed/exercise_11_3_stages.csv", parse_dates=["Date"]).set_index("Date")
    assert saved.index.equals(source.index)
    np.testing.assert_allclose(saved, stages, equal_nan=True, rtol=1e-12, atol=1e-10)
    components = pd.read_csv(output / "components.csv", parse_dates=["Date"]).set_index("Date")
    np.testing.assert_allclose(components, stages[components.columns], rtol=1e-12, atol=1e-10)
    counts = pd.read_csv(output / "stage_missing_counts.csv", index_col=0).iloc[:, 0]
    pd.testing.assert_series_equal(counts, stages.isna().sum(), check_names=False)
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["rows"] == 1044 and summary["observed"] == 677
    assert summary["missing_input"] == summary["missing_deseasonalized"] == 367
    assert summary["missing_preliminary"] == summary["missing_final"] == summary["negative_imputed"] == 0
    assert summary["same_deseasonalized_mask"] and summary["observed_exactly_preserved"]
    assert summary["stl_config"] == expected_config and summary["fit_config"] == FIT_CONFIG
    np.testing.assert_allclose([summary["difference_from_linear_mean_abs_at_gaps"], summary["difference_from_linear_max_abs_at_gaps"]],
                               [difference.mean(), difference.max()], rtol=1e-12)
    np.testing.assert_allclose(summary["additive_reconstruction_max_abs"], reconstruction, rtol=1e-12, atol=1e-15)
    fig = seasonal_decompose_seaborn(decomposition, "Prüfung")
    for ax, column in zip(fig.axes, ["preliminary_linear", "trend", "seasonal", "residual"]):
        np.testing.assert_allclose(ax.lines[0].get_ydata(), stages[column])
    plt.close(fig)
    fig = plot_deseasonalized(stages)
    for ax, column in zip(fig.axes, ["smoothed_gaps", "deseasonalized_gaps"]):
        np.testing.assert_allclose(ax.lines[0].get_ydata(), stages[column], equal_nan=True)
    plt.close(fig)
    fig = plot_final_production(frame, stages)
    for ax, values in zip(fig.axes, [frame.pieces, source, stages.final_imputed.where(~known)]):
        np.testing.assert_allclose(ax.lines[0].get_ydata(), values, equal_nan=True)
    plt.close(fig)
    gaps = gap_table(source)
    gap = gaps.sort_values(["weeks", "start"], ascending=[False, True]).iloc[0]
    assert gap.weeks == 23 and str(gap.start.date()) == "2011-12-11" and str(gap.end.date()) == "2012-05-13"
    start, stop = source.index.get_loc(gap.start), source.index.get_loc(gap.end) + 1
    view = stages.iloc[start - 8:stop + 8]
    fig = plot_long_gap(stages)
    for line, column in zip(fig.axes[0].lines, ["preliminary_linear", "final_imputed"]):
        np.testing.assert_allclose(line.get_ydata(), view[column])
    expected_difference = (view.final_imputed - view.preliminary_linear).where(view.smoothed_gaps.isna())
    np.testing.assert_allclose(fig.axes[1].lines[0].get_ydata(), expected_difference, equal_nan=True)
    plt.close(fig)
    long_difference = (stages.final_imputed - stages.preliminary_linear).iloc[start:stop]
    assert long_difference.iloc[0] < 0 and (long_difference.iloc[8:] > 0).sum() > len(long_difference.iloc[8:]) / 2
    notebook = nbformat.read(ROOT / "sessions/ch11/production_stl_imputation.ipynb", as_version=4)
    code = [c for c in notebook.cells if c.cell_type == "code"]
    assert [c.execution_count for c in code] == list(range(1, 8))
    assert sum("image/png" in o.get("data", {}) for c in code for o in c.outputs) == 4
    table = next(o["data"]["text/html"] for o in code[5].outputs if "text/html" in o.get("data", {}))
    for row in BeautifulSoup(table, "html.parser").select("tbody tr"):
        name, value = row.th.get_text(strip=True), row.td.get_text(strip=True)
        if isinstance(summary[name], bool):
            assert value == str(summary[name])
        else:
            np.testing.assert_allclose(float(value), summary[name], rtol=5e-6, atol=1e-16)
    narrative = " ".join(c.source for c in notebook.cells if c.cell_type == "markdown")
    assert "nicht statistisch optimiert" in narrative and "Modellannahme" in narrative
    manifest = json.loads((output / "validation_manifest.json").read_text(encoding="utf-8"))
    for relative, digest in manifest["files"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    result = {"rows": 1044, "missing_input_and_deseasonalized": 367, "observed_exactly_preserved": 677,
              "missing_final": 0, "negative_imputed": 0, "stl_invocation_config": expected_config,
              "reconstruction_max_abs": float(reconstruction), "mean_absolute_method_difference": float(difference.mean()),
              "max_absolute_method_difference": float(difference.max()), "longest_gap_weeks": 23,
              "longest_gap_start": str(gap.start.date()), "longest_gap_end": str(gap.end.date()),
              "saved_tables_stages_plot_paths_and_10_hashes": "PASS"}
    (output / "human_review_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
