"""Fresh outlier notebook execution, raw-data/threshold checks and static HTML."""

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
from sessions.ch11.stl_imputation import STL_CONFIG, FIT_CONFIG

FIGURES = ["01_original_outliers", "02_residual_thresholds"]


def main():
    source = ROOT / "sessions/ch11/production_outliers.ipynb"
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
    assert len(images) == 2
    for image in images:
        with Image.open(BytesIO(base64.b64decode(image["src"].split(",", 1)[1]))) as decoded:
            decoded.verify()
    output = ROOT / "outputs/ch11/exercise_11_4"
    from sessions.ch11.production import load_production
    table = pd.read_csv(output / "components.csv", index_col="Date", parse_dates=True)
    raw = load_production().pieces
    np.testing.assert_allclose(table.pieces, raw, rtol=1e-14)
    residual = table.residual.to_numpy()
    mean = np.sum(residual)/len(residual)
    std = np.sqrt(np.sum((residual-mean)**2)/(len(residual)-1))
    expected = np.abs(residual-mean) > 3*std
    assert np.array_equal(table.outlier_candidate, expected)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["outlier_candidates"] == int(expected.sum())
    np.testing.assert_allclose(table.trend+table.seasonal+table.residual, raw, atol=1e-10)
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == SHA256
    nbformat.write(notebook, source)
    destination = output / "production_outliers.html"
    destination.write_text(str(page), encoding="utf-8")
    files = [source, destination, output / "components.csv", output / "outlier_candidates.csv", output / "summary.json"]
    files += [output / f"{name}.png" for name in FIGURES]
    manifest = {"source_retrieved": "2026-10-26", "ai_assistance": "Codex",
                "human_review": "APPROVED – AWAITING FINAL MERGE AUTHORIZATION",
                "approval_date": "2026-10-26", "merge_authorized": False, "raw_sha256": SHA256,
                "stl_config": STL_CONFIG, "fit_config": FIT_CONFIG,
                "sequential_code_cells": len(code), "embedded_images": len(images),
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(code)} fresh sequential cells, two decoded embedded images; {int(expected.sum())} candidates; raw hash and residual threshold independently checked")


if __name__ == "__main__":
    main()
