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
from sessions.ch12.classification import load_uwave, SOURCE, transform
from sessions.ch12.forest import CONFIG, fit_forest, predict_forest, load_reference, first_interval

FIGURES = ["01_interval", "02_comparison"]


def main():
    source = ROOT / "sessions/ch12/uwave_forest.ipynb"
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
    output = ROOT / "outputs/ch12/exercise_12_3"
    predictions=pd.read_csv(output/"predictions.csv",dtype={"true":str,"knn":str,"cnn":str,"forest":str})
    x_train,y_train=load_uwave("TRAIN");x_test,y_test=load_uwave("TEST")
    baseline,reference=load_reference(y_test)
    np.testing.assert_array_equal(predictions[["case","true","knn","cnn"]],baseline)
    metrics=pd.read_csv(output/"metrics.csv").set_index("method")
    reports=pd.read_csv(output/"classification_report.csv",dtype={"class":str})
    classes=sorted(np.unique(y_train));manual_matrices={}
    for method,column in [("DTW 3-NN","knn"),("CNN","cnn"),("Time Series Forest","forest")]:
        matrix=np.zeros((8,8),dtype=int)
        for true,predicted in zip(y_test,predictions[column]):matrix[classes.index(true),classes.index(predicted)]+=1
        manual_matrices[method]=matrix
        tp=np.diag(matrix);support=matrix.sum(axis=1);count=matrix.sum(axis=0)
        precision=np.divide(tp,count,out=np.zeros(8,dtype=float),where=count>0)
        recall=tp/support;f1=2*tp/(support+count)
        np.testing.assert_allclose(metrics.loc[method,["accuracy","balanced_accuracy","macro_f1","correct"]].to_numpy(dtype=float),[tp.sum()/320,recall.mean(),f1.mean(),tp.sum()],atol=1e-12)
        r=reports[reports.method==method].set_index("class").loc[classes]
        np.testing.assert_allclose(r[["precision","recall","f1-score","support"]],np.array([precision,recall,f1,support]).T,atol=1e-12)
    np.testing.assert_array_equal(manual_matrices["Time Series Forest"],pd.read_csv(output/"confusion_forest.csv",index_col=0))
    # A second full fit also verifies that execution order/state did not determine results.
    model,scaler,fit_seconds=fit_forest(x_train,y_train)
    repeat,probs,predict_seconds=predict_forest(model,scaler,x_test)
    np.testing.assert_array_equal(repeat,predictions.forest)
    np.testing.assert_allclose(probs,pd.read_csv(output/"forest_probabilities.csv"),atol=1e-12)
    summary=json.loads((output/"summary.json").read_text())
    np.testing.assert_allclose(summary["train_mean"],x_train.mean(axis=(0,2)),atol=1e-12)
    np.testing.assert_allclose(summary["train_scale"],x_train.std(axis=(0,2)),atol=1e-12)
    assert summary["config"]==CONFIG and len(model.estimators_)==summary["actual_trees"]==200
    assert model.total_intervals_==summary["interval_draws"]==30
    assert summary["unique_intervals_per_tree"]==[len(t[0].intervals_)//3 for t in model.intervals_]
    assert summary["example"]==first_interval(model,transform(x_train,scaler))
    # Independently average every fitted tree's probabilities on its own transformed data.
    prepared=transform(x_test,scaler)
    averaged=np.mean([tree.predict_proba(interval[0].transform(prepared)) for tree,interval in zip(model.estimators_,model.intervals_)],axis=0)
    np.testing.assert_allclose(averaged,probs,atol=1e-12)
    paired=pd.read_csv(output/"paired_comparison.csv").set_index("reference")
    for method,column in [("DTW 3-NN","knn"),("CNN","cnn")]:
        old=predictions[column].to_numpy()==y_test;new=repeat==y_test
        assert paired.loc[method].tolist()==[int((old&new).sum()),int((~old&new).sum()),int((old&~new).sum()),int((~old&~new).sum())]
    print(metrics.to_string())
    nbformat.write(notebook,source)
    destination=output/"uwave_forest.html";destination.write_text(str(page),encoding="utf-8")
    from importlib.metadata import version
    files=[source,destination,ROOT/"sessions/ch12/forest.py",ROOT/"sessions/ch12/forest_reference.json",output/"summary.json"]+sorted(output.glob("*.csv"))+[output/(name+".png") for name in FIGURES]
    manifest={"validated_date":"2026-10-26","ai_assistance":"Codex","human_review":"AWAITING HUMAN REVIEW – NOT MERGED","merge_authorized":False,"raw_sha256":SOURCE["files"],"reference":reference,"config":CONFIG,"sequential_code_cells":len(code),"embedded_images":len(images),"all_320_forest_predictions_reproduced":True,"independent_tree_probability_aggregation":True,"repeat_fit_seconds":fit_seconds,"repeat_predict_seconds":predict_seconds,"packages":{name:version(name) for name in ["aeon","numpy","scikit-learn"]},"files":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output/"validation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("PASS: 3 fresh sequential cells, 2 decoded images; reference hashes, all metrics/reports/paired counts, TRAIN scaler, 320 repeated predictions and 200-tree probability aggregation")

if __name__=="__main__":main()
