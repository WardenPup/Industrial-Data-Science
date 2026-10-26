"""Reverify review claims independently against fresh saved outputs and plot paths."""

import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".tools/matplotlib"))
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator, make_interp_spline
from bs4 import BeautifulSoup

from sessions.ch11.imputation import load_smoothed_input, impute_series, METHODS
from sessions.ch11.imputation_plots import plot_imputation, plot_longest_gap


def main():
    frame, source = load_smoothed_input()
    original = source.copy()
    known = source.notna().to_numpy()
    assert len(source) == 1044 and known.sum() == 677 and (~known).sum() == 367
    positions = np.arange(len(source))
    x, y = positions[known], source.to_numpy()[known]
    results = pd.DataFrame({method: impute_series(source, method) for method in METHODS})
    pd.testing.assert_series_equal(source, original)
    output = ROOT / "outputs/ch11/exercise_11_2"
    saved = pd.read_csv(ROOT / "data/processed/exercise_11_2_imputed.csv", parse_dates=["Date"]).set_index("Date")
    assert saved.index.equals(source.index)
    np.testing.assert_allclose(saved.smoothed_gaps, source, equal_nan=True)
    for column in ["pieces", "pieces_gaps"]:
        np.testing.assert_allclose(saved[column], frame[column], equal_nan=True)
    references = {
        "ffill": y[np.searchsorted(x, positions, side="right") - 1],
        "bfill": y[np.searchsorted(x, positions, side="left")],
        "linear": np.interp(positions, x, y),
        "polynomial2": make_interp_spline(x, y, k=2)(positions),
        "polynomial5": make_interp_spline(x, y, k=5)(positions),
        "pchip": PchipInterpolator(x, y)(positions),
    }
    # Independent contiguous-gap scan, including first longest tie resolution.
    gaps = []
    start = None
    for index, observed in enumerate([*known, True]):
        if not observed and start is None:
            start = index
        if observed and start is not None:
            gaps.append((start, index))
            start = None
    assert len(gaps) == 32 and sum(b - a for a, b in gaps) == 367
    longest = max(gaps, key=lambda pair: pair[1] - pair[0])
    a, b = longest
    assert b - a == 23
    assert str(source.index[a].date()) == "2011-12-11"
    assert str(source.index[b - 1].date()) == "2012-05-13"
    saved_gaps = pd.read_csv(output / "gaps.csv", parse_dates=["start", "end"])
    assert len(saved_gaps) == len(gaps)
    for row, (left, right) in zip(saved_gaps.itertuples(), gaps):
        assert row.start == source.index[left] and row.end == source.index[right - 1]
        assert row.weeks == right - left
    summary = pd.read_csv(output / "method_summary.csv", index_col="method")
    outside_counts = {}
    for method in METHODS:
        values = results[method].to_numpy()
        assert np.isfinite(values).all()
        assert np.array_equal(values[known], source.to_numpy()[known])
        np.testing.assert_allclose(saved[f"imputed_{method}"], values, rtol=1e-14)
        np.testing.assert_allclose(values, references[method], rtol=1e-10, atol=1e-9)
        outside = sum(int(((values[left:right] < min(source.iloc[left - 1], source.iloc[right]) - 1e-9) |
                          (values[left:right] > max(source.iloc[left - 1], source.iloc[right]) + 1e-9)).sum())
                      for left, right in gaps)
        outside_counts[method] = outside
        row = summary.loc[method]
        assert row.filled == 367 and row.remaining == 0 and row.negative_imputed == 0
        assert row.outside_gap_anchors == outside
        np.testing.assert_allclose([row.imputed_min, row.imputed_max],
                                   [values[~known].min(), values[~known].max()], rtol=1e-14)
        fig = plot_imputation(frame, source, results[method], method)
        for ax, expected in zip(fig.axes, [frame.pieces, source, results[method].where(~known)]):
            np.testing.assert_allclose(ax.lines[0].get_ydata(), expected, equal_nan=True)
        plt.close(fig)
    assert outside_counts == {"ffill": 0, "bfill": 0, "linear": 0, "polynomial2": 78, "polynomial5": 189, "pchip": 0}
    assert (results["ffill"].iloc[a:b] == source.iloc[a - 1]).all()
    assert (results["bfill"].iloc[a:b] == source.iloc[b]).all()
    assert np.diff(results.pchip.iloc[a - 1:b + 1]).min() >= -1e-9
    fifth = results.polynomial5.iloc[a:b]
    assert fifth.min() < source.iloc[a - 1] and fifth.iloc[0] < source.iloc[a - 1]
    assert fifth.iloc[-1] > fifth.min()
    fig = plot_longest_gap(source, results)
    view = source.iloc[max(0, a - 8):min(len(source), b + 8)]
    for line, method in zip(fig.axes[0].lines, METHODS):
        np.testing.assert_allclose(line.get_ydata(), results.loc[view.index, method])
    plt.close(fig)
    notebook = nbformat.read(ROOT / "sessions/ch11/production_imputation.ipynb", as_version=4)
    cells = [c for c in notebook.cells if c.cell_type == "code"]
    assert [c.execution_count for c in cells] == list(range(1, 11))
    assert sum("image/png" in o.get("data", {}) for c in cells for o in c.outputs) == 7
    table_html = next(o["data"]["text/html"] for o in cells[1].outputs
                      if "text/html" in o.get("data", {}))
    table_rows = BeautifulSoup(table_html, "html.parser").select("tbody tr")
    assert len(table_rows) == 6
    for row, method in zip(table_rows, METHODS):
        assert row.th.get_text(strip=True) == METHODS[method]
        np.testing.assert_allclose([float(td.get_text()) for td in row.select("td")],
                                   summary.loc[method].to_numpy(), rtol=0, atol=0.000501)
    streams = "".join(o.get("text", "") for c in cells for o in c.outputs)
    for claim in ["Wochen: 1044; beobachtet: 677; fehlend: 367", "32; Länge: 3–23 Wochen",
                  "2011-12-11 bis 2012-05-13 (23 Wochen)"]:
        assert claim in streams, claim
    html = BeautifulSoup((output / "production_imputation.html").read_text(encoding="utf-8"), "html.parser")
    assert len(html.select('img[src^="data:image/png;base64,"]')) == 7
    saved_summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert saved_summary["missing_input"] == 367 and saved_summary["longest_gap_weeks"] == 23
    assert all(n == 0 for n in saved_summary["remaining_by_method"].values())
    manifest = json.loads((output / "validation_manifest.json").read_text(encoding="utf-8"))
    for relative, digest in manifest["files"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    result = {"rows": 1044, "filled_per_method": 367, "observed_unchanged_per_method": 677,
              "independent_method_references": "PASS", "outside_gap_anchors": outside_counts,
              "gap_blocks": 32, "longest_gap_weeks": 23,
              "longest_gap_start": str(source.index[a].date()), "longest_gap_end": str(source.index[b - 1].date()),
              "long_gap_left_anchor": source.iloc[a - 1], "long_gap_right_anchor": source.iloc[b],
              "long_gap_polynomial5_min": fifth.min(),
              "long_gap_polynomial2_smallest_step": float(np.diff(results.polynomial2.iloc[a - 1:b + 1]).min()),
              "plot_paths_and_saved_outputs": "PASS", "manifest_hashes": len(manifest["files"])}
    (output / "human_review_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
