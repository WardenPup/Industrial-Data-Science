"""Fresh multivariate classification notebook, independent metric/weight checks and offline HTML."""

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
from sessions.ch12.classification import load_uwave, SOURCE, SEED, EPOCHS, GestureCNN

FIGURES = ["01_input_and_training", "02_confusion_matrices"]


def main():
    source = ROOT / "sessions/ch12/uwave_classification.ipynb"
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
    assert len(images) == 2
    for image in images:
        with Image.open(BytesIO(base64.b64decode(image["src"].split(",", 1)[1]))) as decoded:
            decoded.verify()
    output = ROOT / "outputs/ch12/exercise_12_2"
    import torch
    predictions=pd.read_csv(output/"predictions.csv",dtype={"true":str,"knn":str,"cnn":str})
    summary=json.loads((output/"summary.json").read_text())
    x_train,y_train=load_uwave("TRAIN")
    x_test,y_test=load_uwave("TEST")
    assert len(predictions)==320 and predictions["case"].tolist()==list(range(320))
    np.testing.assert_array_equal(predictions.true,y_test)
    mean=x_train.mean(axis=(0,2),keepdims=True)
    scale=x_train.std(axis=(0,2),ddof=0,keepdims=True)
    np.testing.assert_allclose(summary["train_channel_mean"],mean.ravel(),atol=1e-12)
    np.testing.assert_allclose(summary["train_channel_scale"],scale.ravel(),atol=1e-12)
    classes=summary["classes"]
    metrics=pd.read_csv(output/"metrics.csv").set_index("method")
    reports=pd.read_csv(output/"classification_report.csv",dtype={"class":str})
    for method,column in [("DTW 3-NN","knn"),("CNN","cnn")]:
        matrix=np.zeros((8,8),dtype=int)
        for true,predicted in zip(y_test,predictions[column]):matrix[classes.index(true),classes.index(predicted)]+=1
        np.testing.assert_array_equal(matrix,pd.read_csv(output/f"confusion_{column}.csv",index_col=0).to_numpy())
        tp=np.diag(matrix);support=matrix.sum(axis=1);predicted_count=matrix.sum(axis=0)
        recall=tp/support
        precision=np.divide(tp,predicted_count,out=np.zeros(8,dtype=float),where=predicted_count!=0)
        f1=np.divide(2*tp,support+predicted_count,out=np.zeros(8,dtype=float),where=support+predicted_count!=0)
        np.testing.assert_allclose(metrics.loc[method,["accuracy","balanced_accuracy","macro_f1"]].to_numpy(dtype=float),[tp.sum()/matrix.sum(),recall.mean(),f1.mean()],atol=1e-12)
        r=reports[reports.method==method].set_index("class").loc[classes]
        np.testing.assert_allclose(r[["precision","recall","f1-score","support"]].to_numpy(dtype=float),np.array([precision,recall,f1,support]).T,atol=1e-12)
    model=GestureCNN().eval()
    with np.load(output/"cnn_weights.npz",allow_pickle=False) as weights:
        model.load_state_dict({key:torch.from_numpy(weights[key].copy()) for key in weights.files})
    with torch.inference_mode():
        logits=model(torch.from_numpy(np.ascontiguousarray((x_test-mean)/scale,dtype=np.float32))).numpy()
    np.testing.assert_array_equal(np.asarray(classes)[logits.argmax(axis=1)],predictions.cnn)
    history=pd.read_csv(output/"cnn_training.csv")
    assert history.epoch.tolist()==list(range(1,EPOCHS+1)) and np.isfinite(history.train_cross_entropy).all()
    assert summary["missing"]==0 and summary["cnn_parameters"]==5000
    assert summary["raw_sha256"]==SOURCE["files"]
    print(metrics.to_string())
    nbformat.write(notebook, source)
    destination = output / "uwave_classification.html"
    destination.write_text(str(page), encoding="utf-8")
    files = [source, destination] + sorted(output.glob("*.csv")) + [output / "summary.json", output / "cnn_weights.npz"]
    files += [output / f"{name}.png" for name in FIGURES]
    from importlib.metadata import version
    manifest={"retrieved_date":"2026-10-26","ai_assistance":"Codex","human_review":"AWAITING HUMAN REVIEW","merge_authorized":False,
              "raw_sha256":SOURCE["files"],"seed":SEED,"fixed_epochs":EPOCHS,
              "packages":{name:version(name) for name in ["aeon","numpy","scipy","scikit-learn","numba","torch"]},
              "sequential_code_cells":len(code),"embedded_images":len(images),
              "files":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output/"validation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(f"PASS: {len(code)} fresh sequential cells, two decoded HTML images; original splits, TRAIN scaler, independent confusion-derived metrics and saved CNN predictions checked")



if __name__ == "__main__":
    main()
