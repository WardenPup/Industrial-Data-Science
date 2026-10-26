"""Execute Exercise 11.1 in a fresh kernel and verify self-contained HTML."""

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
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
from PIL import Image
from sessions.ch11.production import load_production, DATA, SHA256


def main():
    load_production()
    source = ROOT / "sessions/ch11/production_smoothing.ipynb"
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=180, kernel_name="python3",
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
    # Static report: no interactive widgets or JavaScript math are required.
    # Keep embedded CSS/images; remove CDN loaders inherited from nbconvert.
    for element in page.select('script, link[href^="http"]'):
        element.decompose()
    html = str(page)
    images = page.select('img[src^="data:image/png;base64,"]')
    assert len(images) == 2
    for image in images:
        with Image.open(BytesIO(base64.b64decode(image["src"].split(",", 1)[1]))) as decoded:
            decoded.verify()
    assert not page.select('img[src^="http"], link[href^="http"], script[src^="http"]')
    output = ROOT / "outputs/ch11/exercise_11_1"
    nbformat.write(notebook, source)
    destination = output / "production_smoothing.html"
    destination.write_text(html, encoding="utf-8")
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["same_missing_mask"] and summary["missing_smoothed"] == 367
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == SHA256
    files = [source, destination, output / "01_original_and_gaps.png",
             output / "02_smoothing_comparison.png", output / "summary.json",
             ROOT / "data/processed/exercise_11_1_smoothed.csv"]
    manifest = {"source_retrieved": "2026-10-26", "ai_assistance": "Codex",
                "human_review": "AWAITING HUMAN REVIEW", "data_sha256": SHA256,
                "sequential_code_cells": len(code), "embedded_html_images": len(images),
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(code)} sequential cells; two decoded embedded HTML images; exact 367-gap mask; raw SHA256 unchanged")


if __name__ == "__main__":
    main()
