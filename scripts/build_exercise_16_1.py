"""Execute the official vibration CNN and verify predictions and offline HTML."""
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
    source = ROOT / "sessions/ch16/multimodal_health_monitoring.ipynb"
    output = ROOT / "outputs/ch16/exercise_16_1"
    notebook = nbformat.read(source, 4)
    nbformat.validate(notebook)
    client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    if sys.platform == "win32":
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    counts = [c.execution_count for c in notebook.cells if c.cell_type == "code"]
    assert counts == list(range(1, len(counts)+1))
    assert not any(o.output_type == "error" for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
    html, _ = HTMLExporter(embed_images=True, raw_template=(ROOT / "templates/notebook_export.html.j2").read_text(encoding="utf-8")).from_notebook_node(notebook)
    page = BeautifulSoup(html, "html.parser")
    for element in page.select("script, link[href^='http']"):
        element.decompose()
    images = page.select("img[src^='data:image/png;base64,']")
    assert len(images) == 2
    for item in images:
        with Image.open(BytesIO(base64.b64decode(item["src"].split(",", 1)[1]))) as im:
            im.verify()
        link = page.new_tag("a", href=item["src"], target="_blank", title="Grafik in Originalauflösung öffnen")
        item.wrap(link)
    nbformat.write(notebook, source)
    destination = output / "multimodal_health_monitoring.html"
    destination.write_text(str(page), encoding="utf-8")
    from sessions.ch16.multimodal import load_multimodal_data,DATA_PATH,RAW_SHA256,prepare_data
    from sklearn.metrics import confusion_matrix
    ts,img,labels,levels=load_multimodal_data(str(DATA_PATH))
    prepared=prepare_data(ts,img,labels,levels)
    pred=pd.read_csv(output/"predictions.csv")
    assert len(pred)==100 and pred.Index_0basiert.tolist()==prepared["test_indices"].tolist()
    assert np.array_equal(pred.Ist,labels[prepared["test_indices"]])
    probs=pred[["p_Normal","p_Warning","p_Critical"]].to_numpy()
    assert np.isfinite(probs).all() and (probs>=0).all() and (probs<=1).all()
    assert np.allclose(probs.sum(axis=1),1,atol=1e-6)
    assert np.array_equal(probs.argmax(axis=1),pred.Vorhersage)
    cm=pd.read_csv(output/"confusion_matrix.csv",index_col=0).to_numpy()
    assert np.array_equal(cm,confusion_matrix(pred.Ist,pred.Vorhersage,labels=[0,1,2]))
    scaling=json.loads((output/"scaling.json").read_text())
    for k,v in scaling.items():assert np.isclose(v,prepared[k],rtol=0,atol=1e-12)
    summary=json.loads((output/"summary.json").read_text())
    assert summary["correct"]==int((pred.Ist==pred.Vorhersage).sum())
    assert summary["epochs"]==30 and summary["batch_size"]==16 and summary["seed"]==42
    assert np.isclose(summary["accuracy"],np.trace(cm)/100)
    tables=pd.read_csv(output/"vibration_levels_vs_status.csv",header=[0,1],index_col=0)
    for kind,values in [("true health status",pred.Ist.to_numpy()),("predicted health status",pred.Vorhersage.to_numpy())]:
        expected=pd.crosstab(levels[prepared["test_indices"],1],values,colnames=["status"])
        actual=tables[kind];actual.columns=actual.columns.astype(int)
        assert np.array_equal(actual.to_numpy(),expected.to_numpy())
    class_counts=pd.read_csv(output/"class_counts.csv")
    for column,values in [("Gesamt",labels),("TRAIN",prepared["y_train"]),("TEST",prepared["y_test"])]:
        assert np.array_equal(class_counts[column],np.bincount(values,minlength=3))
    split=pd.read_csv(output/"split.csv")
    assert split.Index_0basiert.nunique()==500
    for part in ["train","test"]:
        assert split.loc[split.Split.eq(part.upper()),"Index_0basiert"].tolist()==prepared[part+"_indices"].tolist()
    def verify_file():return RAW_SHA256
    files = [source, destination] + sorted(output.glob("*.csv")) + sorted(output.glob("*.png")) + [output / "summary.json",output / "scaling.json"]
    manifest = {"validated_date": "2026-11-21", "status": "AWAITING HUMAN REVIEW", "ai_assistance": "Codex",
                "raw_sha256": verify_file(), "sequential_code_cells": len(counts), "embedded_images": 2,
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print(f"PASS: {len(counts)} fresh sequential cells; two embedded images; independent counts and raw SHA256 verified")
    if args.check_html:
        if (ROOT / ".tools/playwright").exists():
            os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".tools/playwright"))
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            for width in [900, 1400]:
                tab = browser.new_page(viewport={"width": width, "height": 1000}, offline=True)
                errors, failures = [], []
                tab.on("pageerror", lambda e: errors.append(str(e)))
                tab.on("requestfailed", lambda r: failures.append(r.url))
                tab.goto(destination.as_uri())
                assert tab.locator("img").count() == 2
                assert tab.locator("img").evaluate_all("xs => xs.every(x => x.complete && x.naturalWidth > 0)")
                assert not errors and not failures
                assert tab.evaluate("document.documentElement.scrollWidth <= innerWidth")
                screenshot = ROOT / f".tools/16_1_html/{width}.png"
                screenshot.parent.mkdir(parents=True, exist_ok=True)
                tab.screenshot(path=str(screenshot), full_page=True)
                tab.close()
                print(f"PASS offline HTML {width}px: image loaded; no page errors, failed requests or page overflow")
            browser.close()


if __name__ == "__main__":
    main()
