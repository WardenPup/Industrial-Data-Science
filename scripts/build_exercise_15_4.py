"""Execute the rule/tree comparison and verify prediction statistics and offline HTML."""
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
    source = ROOT / "sessions/ch15/rule_models.ipynb"
    output = ROOT / "outputs/ch15/exercise_15_4"
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
    assert len(images) == 1
    for item in images:
        with Image.open(BytesIO(base64.b64decode(item["src"].split(",", 1)[1]))) as im:
            im.verify()
        link = page.new_tag("a", href=item["src"], target="_blank", title="Grafik in Originalauflösung öffnen")
        item.wrap(link)
    nbformat.write(notebook, source)
    destination = output / "rule_models.html"
    destination.write_text(str(page), encoding="utf-8")
    from sessions.ch15.drilling_data import DATA_PATH,verify_file,SUBGROUPS
    data=pd.read_csv(DATA_PATH)
    from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
    from sessions.ch15.rule_models import FEATURES, RULES
    predictions=pd.read_csv(output/"predictions.csv")
    metrics=pd.read_csv(output/"metrics.csv")
    split=pd.read_csv(output/"split.csv")
    test_ids=split.loc[split.Split.eq("TEST"),"ID"]
    assert len(metrics)==8 and len(predictions)==4*len(test_ids)
    train_data=data.loc[data.ID.isin(split.loc[split.Split.eq("TRAIN"),"ID"])]
    test_data=data.loc[data.ID.isin(test_ids)]
    assert not set(map(tuple,train_data[FEATURES].to_numpy())) & set(map(tuple,test_data[FEATURES].to_numpy()))
    for flag in SUBGROUPS:
        part=predictions.loc[predictions.Fehlertyp.eq(flag)]
        assert part.ID.tolist()==test_data.ID.tolist()
        assert np.array_equal(part.Ist,test_data[flag])
        assert np.array_equal(part.Regel,RULES[flag](test_data))
        for name in ["Regel","Baum"]:
            row=metrics.loc[metrics.Fehlertyp.eq(flag)&metrics.Methode.eq(name)].iloc[0]
            actual=confusion_matrix(part.Ist,part[name],labels=[0,1]).ravel()
            assert np.array_equal(row[["TN","FP","FN","TP"]].to_numpy(),actual)
            for key,fun in [("Precision",precision_score),("Recall",recall_score),("F1",f1_score)]:
                assert np.isclose(row[key],fun(part.Ist,part[name],zero_division=0))
    files = [source, destination] + sorted(output.glob("*.csv")) + sorted(output.glob("*.png")) + sorted(output.glob("tree_*.txt")) + [output / "summary.json"]
    manifest = {"validated_date": "2026-11-21", "status": "AWAITING HUMAN REVIEW", "ai_assistance": "Codex",
                "raw_sha256": verify_file(), "sequential_code_cells": len(counts), "embedded_images": 1,
                "files": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output / "validation_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print(f"PASS: {len(counts)} fresh sequential cells; one embedded image; independent counts and raw SHA256 verified")
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
                assert tab.locator("img").count() == 1
                assert tab.locator("img").evaluate_all("xs => xs.every(x => x.complete && x.naturalWidth > 0)")
                assert not errors and not failures
                assert tab.evaluate("document.documentElement.scrollWidth <= innerWidth")
                screenshot = ROOT / f".tools/15_4_html/{width}.png"
                screenshot.parent.mkdir(parents=True, exist_ok=True)
                tab.screenshot(path=str(screenshot), full_page=True)
                tab.close()
                print(f"PASS offline HTML {width}px: image loaded; no page errors, failed requests or page overflow")
            browser.close()


if __name__ == "__main__":
    main()
