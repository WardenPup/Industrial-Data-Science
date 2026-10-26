"""Fresh Exercise 11.2 execution, numerical invariants and static HTML export."""

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
from sessions.ch11.imputation import load_smoothed_input, METHODS, INPUT_SHA256


def main():
    _, smoothed = load_smoothed_input()
    source = ROOT / "sessions/ch11/production_imputation.ipynb"
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
    assert len(images) == 7
    for image in images:
        with Image.open(BytesIO(base64.b64decode(image["src"].split(",", 1)[1]))) as decoded:
            decoded.verify()
    assert not page.select('img[src^="http"], link[href^="http"], script')
    output = ROOT / "outputs/ch11/exercise_11_2"
    processed = ROOT / "data/processed/exercise_11_2_imputed.csv"
    exported = pd.read_csv(processed, parse_dates=["Date"]).set_index("Date")
    assert exported.index.equals(smoothed.index)
    np.testing.assert_allclose(exported.smoothed_gaps, smoothed, equal_nan=True)
    for method in METHODS:
        values = exported[f"imputed_{method}"]
        assert np.isfinite(values).all()
        np.testing.assert_allclose(values[smoothed.notna()], smoothed.dropna(), rtol=1e-14)
    positions = np.arange(len(smoothed))
    observed = smoothed.notna()
    linear_reference = np.interp(positions, positions[observed], smoothed[observed])
    np.testing.assert_allclose(exported.imputed_linear, linear_reference, rtol=1e-14)
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["missing_input"] == 367 and summary["gap_blocks"] == 32
    assert summary["longest_gap_weeks"] == 23
    assert all(value == 0 for value in summary["remaining_by_method"].values())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == SHA256
    nbformat.write(notebook, source)
    destination = output / "production_imputation.html"
    destination.write_text(str(page), encoding="utf-8")
    files = [source, destination, processed, output / "method_summary.csv",
             output / "gaps.csv", output / "summary.json"]
    files += [output / f"{name}.png" for name in [*METHODS, "longest_gap_comparison"]]
    manifest = {"retrieved_date": "2026-10-26", "ai_assistance": "Codex",
                "human_review": "AWAITING HUMAN REVIEW", "raw_sha256": SHA256,
                "approved_input_sha256": INPUT_SHA256,
                "sequential_code_cells": len(code), "embedded_images": len(images),
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(code)} sequential cells; 7 decoded embedded images; six methods fill 367 gaps")
    print("PASS: observed values and raw data preserved; independent linear reference and approved input hash match")


if __name__ == "__main__":
    main()
