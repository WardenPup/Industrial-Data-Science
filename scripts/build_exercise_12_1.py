"""Fresh gesture clustering notebook execution, split/metric checks and offline HTML."""

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
from sessions.ch12.clustering import load_gestures, SOURCE, SEED, LENGTH

FIGURES = ["01_data_exploration", "02_cluster_centers", "03_class_cluster_counts", "04_msm_example"]


def main():
    source = ROOT / "sessions/ch12/gesture_clustering.ipynb"
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=900, kernel_name="python3",
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
    output = ROOT / "outputs/ch12/exercise_12_1"
    from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
    assignments = pd.read_csv(output / "assignments.csv", dtype={"class":str})
    metrics = pd.read_csv(output / "metrics.csv")
    for _,row in metrics.iterrows():
        subset = assignments[(assignments.method==row.method)&(assignments.split==row.split)]
        raw, labels = load_gestures(row.split)
        assert len(subset)==len(raw)==row.n
        np.testing.assert_array_equal(subset["class"], labels)
        assert subset["case"].tolist()==list(range(len(raw)))
        np.testing.assert_allclose(row.ARI,adjusted_rand_score(labels,subset.cluster),atol=1e-12)
        np.testing.assert_allclose(row.NMI,normalized_mutual_info_score(labels,subset.cluster),atol=1e-12)
        assert row.clusters_used==subset.cluster.nunique() and row.n_iter<=30
    summary=json.loads((output/"summary.json").read_text())
    assert summary["train"]==132 and summary["test"]==172 and summary["missing"]==0
    assert summary["raw_sha256"]==SOURCE["files"]
    print(metrics[["method","split","ARI","NMI","n_iter"]].to_string(index=False))
    nbformat.write(notebook, source)
    destination = output / "gesture_clustering.html"
    destination.write_text(str(page), encoding="utf-8")
    files = [source, destination] + sorted(output.glob("*.csv")) + [output / "summary.json"]
    files += [output / f"{name}.png" for name in FIGURES]
    from importlib.metadata import version
    manifest={"retrieved_date":"2026-10-26","ai_assistance":"Codex","human_review":"Feedback provided; final human approval pending",
              "scientific_review_date":"2026-10-26","merge_authorized":False,
              "raw_sha256":SOURCE["files"],"seed":SEED,"resampled_length":LENGTH,
              "packages":{name:version(name) for name in ["aeon","numpy","scipy","scikit-learn","numba"]},
              "sequential_code_cells":len(code),"embedded_images":len(images),
              "files":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output/"validation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(f"PASS: {len(code)} fresh sequential cells, four decoded HTML images, both original splits and independent ARI/NMI recalculation")



if __name__ == "__main__":
    main()
