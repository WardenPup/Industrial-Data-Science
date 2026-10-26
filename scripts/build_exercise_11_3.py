"""Fresh STL notebook execution, additive/mask checks and offline static HTML."""

import asyncio
import base64
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
for name, relative in {
    "JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter",
    "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython",
    "MPLCONFIGDIR": ".tools/matplotlib",
}.items():
    os.environ.setdefault(name, str(ROOT / relative))

import nbformat
import numpy as np
import pandas as pd
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
from PIL import Image
from sessions.ch11.production import DATA, SHA256
from sessions.ch11.imputation import load_smoothed_input, INPUT_SHA256, impute_series
from sessions.ch11.stl_imputation import STL_CONFIG, FIT_CONFIG

FIGURES = ["01_stl_components", "02_deseasonalized_gaps", "03_final_imputation", "04_long_gap_comparison"]


def main():
    _, source_values = load_smoothed_input()
    source = ROOT / "sessions/ch11/production_stl_imputation.ipynb"
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=240, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    if sys.platform == "win32":
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    code = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert [cell.execution_count for cell in code] == list(range(1, len(code) + 1))
    assert not any(o.output_type == "error" for c in code for o in c.outputs)
    template = (ROOT / "templates/notebook_export.html.j2").read_text(encoding="utf-8")
    html, _ = HTMLExporter(embed_images=True, raw_template=template).from_notebook_node(notebook)
    page = BeautifulSoup(html, "html.parser")
    for element in page.select('script, link[href^="http"]'):
        element.decompose()
    images = page.select('img[src^="data:image/png;base64,"]')
    assert len(images) == 4
    for image in images:
        with Image.open(BytesIO(base64.b64decode(image["src"].split(",", 1)[1]))) as decoded:
            decoded.verify()
    output = ROOT / "outputs/ch11/exercise_11_3"
    processed = ROOT / "data/processed/exercise_11_3_stages.csv"
    stages = pd.read_csv(processed, parse_dates=["Date"]).set_index("Date")
    assert stages.index.equals(source_values.index)
    np.testing.assert_allclose(stages.smoothed_gaps, source_values, equal_nan=True)
    assert np.array_equal(stages.deseasonalized_gaps.isna(), source_values.isna())
    observed = source_values.notna()
    np.testing.assert_allclose(stages.final_imputed[observed], source_values[observed], rtol=1e-14)
    assert np.isfinite(stages.final_imputed).all()
    np.testing.assert_allclose(stages.trend + stages.seasonal + stages.residual,
                               stages.preliminary_linear, rtol=1e-12, atol=1e-9)
    np.testing.assert_allclose(stages.deseasonalized_gaps, source_values - stages.seasonal,
                               equal_nan=True, rtol=1e-12, atol=1e-9)
    completed = impute_series(source_values - stages.seasonal, "linear")
    np.testing.assert_allclose(stages.final_imputed[~observed],
                               (completed + stages.seasonal)[~observed], rtol=1e-12, atol=1e-9)
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["missing_input"] == summary["missing_deseasonalized"] == 367
    assert summary["observed"] == 677 and summary["missing_final"] == 0
    assert summary["observed_exactly_preserved"] and summary["same_deseasonalized_mask"]
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == SHA256
    nbformat.write(notebook, source)
    destination = output / "production_stl_imputation.html"
    destination.write_text(str(page), encoding="utf-8")
    files = [source, destination, processed, output / "components.csv",
             output / "stage_missing_counts.csv", output / "summary.json"]
    files += [output / f"{name}.png" for name in FIGURES]
    manifest = {"source_retrieved": "2026-10-26", "ai_assistance": "Codex",
                "human_review": "APPROVED – AWAITING FINAL MERGE AUTHORIZATION",
                "approval_date": "2026-10-26", "merge_authorized": False, "raw_sha256": SHA256,
                "approved_input_sha256": INPUT_SHA256, "stl_config": STL_CONFIG, "fit_config": FIT_CONFIG,
                "sequential_code_cells": len(code), "embedded_images": len(images),
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(code)} fresh sequential cells, four decoded embedded HTML images")
    print("PASS: 367 original gaps reused after deseasonalizing, 677 known values preserved, finite final result and additive identity")


if __name__ == "__main__":
    main()
