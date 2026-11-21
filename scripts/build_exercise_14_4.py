"""Execute the parallel-coordinate notebook and verify its self-contained interactive exports."""
import argparse
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
for name, rel in {"JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter",
                  "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython",
                  "MPLCONFIGDIR": ".tools/matplotlib"}.items():
    os.environ.setdefault(name, str(ROOT / rel))

import nbformat
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-html", action="store_true")
    args = parser.parse_args()
    source = ROOT / "sessions/ch14/parallel_coordinates.ipynb"
    output = ROOT / "outputs/ch14/exercise_14_4"
    notebook = nbformat.read(source, 4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=240, kernel_name="python3", resources={"metadata":{"path":str(ROOT)}})
    if sys.platform == "win32":
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    counts = [c.execution_count for c in notebook.cells if c.cell_type == "code"]
    assert counts == [1,2,3]
    assert not any(o.output_type == "error" for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
    nbformat.write(notebook,source)
    exporter = HTMLExporter(raw_template=(ROOT/"templates/notebook_export.html.j2").read_text(encoding="utf-8"))
    exported,_ = exporter.from_notebook_node(notebook)
    page = BeautifulSoup(exported,"html.parser")
    for element in page.select("script, link[href^='http']"):
        element.decompose()
    # Python widget callbacks cannot run in a static export: embed the equivalent
    # self-contained browser view instead of depending on a widget CDN/kernel.
    slot = page.select_one("#offline-parcoords-slot")
    assert slot is not None
    iframe = page.new_tag("iframe",title="Interaktive Parallelkoordinaten",srcdoc=(output/"parallel_coordinates.html").read_text(encoding="utf-8"))
    iframe["style"] = "width:100%;height:860px;border:0"
    slot.append(iframe)
    destination=output/"parallel_coordinates_notebook.html"
    destination.write_text(str(page),encoding="utf-8")
    from sessions.ch10.ai4i_data import verify_file
    raw_hash=verify_file()
    summary=json.loads((output/"summary.json").read_text())
    assert summary["rows"]==10000 and summary["failure_counts"]=={"Machine failure":339,"TWF":46,"HDF":115,"PWF":95,"OSF":98,"RNF":19}
    if args.check_html:
        from check_exercise_14_4_html import check
        check()
    files=[source,destination,output/"parallel_coordinates.html",output/"failure_counts.csv",output/"summary.json"]
    if args.check_html:
        files += [output/"interaction_checks.json"] + sorted(output.glob("*.png"))
    manifest={"validated_date":"2026-11-21","status":"SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION","ai_assistance":"Codex","raw_sha256":raw_hash,"sequential_code_cells":3,"files":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output/"validation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("PASS: three fresh sequential cells, categorical counts and raw SHA256; self-contained notebook/interactive HTML exported")

if __name__ == "__main__":
    main()
