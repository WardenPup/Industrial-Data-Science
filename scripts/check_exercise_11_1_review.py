"""Independently check the numerical student-review claims and saved outputs."""

import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".tools/matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, str(ROOT))
from sessions.ch11.production import load_production, smooth_with_gaps, SHA256
from sessions.ch11.production_plots import plot_production_data, plot_smoothing


def main():
    frame = load_production()
    values = frame.pieces_gaps.to_numpy()
    expected = {name: np.full(len(values), np.nan) for name in ["median", "mean"]}
    support = []
    # Explicit positional five-week windows, independent of pandas rolling.
    for index, value in enumerate(values):
        if np.isnan(value):
            continue
        window = values[max(0, index - 2):min(len(values), index + 3)]
        finite = sorted(window[~np.isnan(window)].tolist())
        size = len(finite)
        support.append(size)
        expected["mean"][index] = sum(finite) / size
        expected["median"][index] = (finite[(size - 1) // 2] + finite[size // 2]) / 2
    assert len(frame) == 1044 and len(support) == 677
    assert frame.index[0] == pd.Timestamp("2005-01-02")
    assert frame.index[-1] == pd.Timestamp("2024-12-29")
    assert frame.pieces.isna().sum() == 0
    assert np.isnan(values).sum() == 367
    counts = {n: support.count(n) for n in range(1, 6)}
    assert counts == {1: 2, 2: 4, 3: 59, 4: 56, 5: 556}
    maximum = (frame.pieces - frame.pieces_gaps).abs().max()
    assert round(maximum, 3) == 9.729
    assert f"{367 / 1044 * 100:.2f}" == "35.15"
    processed = pd.read_csv(ROOT / "data/processed/exercise_11_1_smoothed.csv",
                            parse_dates=["Date"]).set_index("Date")
    for column in ["pieces", "pieces_gaps"]:
        np.testing.assert_allclose(processed[column], frame[column], equal_nan=True)
    for method in expected:
        result = smooth_with_gaps(frame.pieces_gaps, 5, method)
        np.testing.assert_allclose(result, expected[method], rtol=1e-14, equal_nan=True)
        np.testing.assert_allclose(processed[f"rolling_{method}"], expected[method],
                                   rtol=1e-14, equal_nan=True)
        assert np.array_equal(np.isnan(result), np.isnan(values))
        frame[f"rolling_{method}"] = result
    # Verify actual plotted line data retain missing positions on every axis.
    first = plot_production_data(frame, "pieces", "pieces_gaps")
    for ax, column in zip(first.axes, ["pieces", "pieces_gaps"]):
        np.testing.assert_allclose(ax.lines[0].get_ydata(), frame[column], equal_nan=True)
    second = plot_smoothing(frame)
    for ax, data in zip(second.axes, [frame, frame.loc["2018":"2019"]]):
        for line, column in zip(ax.lines, ["pieces_gaps", "rolling_mean", "rolling_median"]):
            np.testing.assert_allclose(line.get_ydata(), data[column], equal_nan=True)
    plt.close("all")
    output = ROOT / "outputs/ch11/exercise_11_1"
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary == {
        "rows": 1044, "missing_original": 367, "missing_smoothed": 367,
        "same_missing_mask": True, "window_weeks": 5, "centered": True,
        "observed_windows_with_at_most_two_values": 6, "data_sha256": SHA256,
    }
    notebook = nbformat.read(ROOT / "sessions/ch11/production_smoothing.ipynb", as_version=4)
    code = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert [cell.execution_count for cell in code] == [1, 2, 3, 4]
    streams = "".join(o.get("text", "") for c in code for o in c.outputs)
    for claim in ["1044 Wochen; 2005-01-02 bis 2024-12-29", "367 (35.15%)", "9.729"]:
        assert claim in streams, claim
    support_output = next(o["data"]["text/html"] for o in code[2].outputs
                          if "text/html" in o.get("data", {}))
    rows = BeautifulSoup(support_output, "html.parser").select("tbody tr")
    saved_counts = {int(float(row.th.get_text())): int(row.td.get_text()) for row in rows}
    assert saved_counts == counts
    html = BeautifulSoup((output / "production_smoothing.html").read_text(encoding="utf-8"), "html.parser")
    assert len(html.select('img[src^="data:image/png;base64,"]')) == 2
    assert not html.select('script, link[href^="http"], img[src^="http"]')
    manifest = json.loads((output / "validation_manifest.json").read_text(encoding="utf-8"))
    for relative, sha in manifest["files"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == sha, relative
    result = {"rows": len(frame), "observed": len(support), "missing": 367,
              "missing_percent": 367 / 1044 * 100, "max_absolute_column_difference": maximum,
              "support_counts": counts, "same_mask_median_and_mean": True,
              "independent_window_comparison": "PASS", "notebook_and_html": "PASS"}
    (output / "human_review_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
