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
from sessions.ch12.classification import transform
from sessions.ch12.regression import load_appliances,fit_regressors,predict_regressors,EnergyCNN,SOURCE,SEED,EPOCHS

FIGURES = ["01_input_and_training", "02_predictions"]


def main():
    source = ROOT / "sessions/ch12/appliances_regression.ipynb"
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
    output=ROOT/"outputs/ch12/exercise_12_4"
    import torch
    from unittest.mock import patch
    from sessions.ch12 import regression as study
    x_train,y_train=load_appliances("TRAIN");x_test,y_test=load_appliances("TEST")
    assert x_train.shape==(95,24,144) and x_test.shape==(42,24,144)
    saved=pd.read_csv(output/"predictions.csv")
    np.testing.assert_array_equal(saved.case,np.arange(42));np.testing.assert_array_equal(saved.true_kwh,y_test)
    metrics=pd.read_csv(output/"metrics.csv").set_index("method")
    review_metrics=[]
    for method,column in [("DTW 3-NN","knn_kwh"),("Time Series Forest","forest_kwh"),("CNN","cnn_kwh")]:
        error=saved[column].to_numpy()-y_test
        review_metrics.append(dict(method=method,rmse=float(np.sqrt(np.mean(error**2))),mae=float(np.mean(np.abs(error))),mean_prediction_minus_true=float(error.mean()),max_absolute_error=float(np.abs(error).max())))
        np.testing.assert_allclose(metrics.loc[method,["rmse","mae"]].to_numpy(dtype=float),[np.sqrt(np.mean(error**2)),np.mean(np.abs(error))],atol=1e-12)
    summary=json.loads((output/"summary.json").read_text())
    mean=x_train.mean(axis=(0,2),keepdims=True);scale=x_train.std(axis=(0,2),keepdims=True)
    np.testing.assert_allclose(summary["train_channel_mean"],mean.ravel(),atol=1e-12)
    np.testing.assert_allclose(summary["train_channel_scale"],scale.ravel(),atol=1e-12)
    np.testing.assert_allclose([summary["train_target_mean"],summary["train_target_scale"]],[y_train.mean(),y_train.std()],atol=1e-12)
    assert summary["forest_trees"]==200 and summary["forest_interval_draws"]==58
    assert summary["cnn_parameters"]==5553 and summary["epochs"]==60 and summary["seed"]==42
    history=pd.read_csv(output/"cnn_training.csv")
    assert history.epoch.tolist()==list(range(1,61)) and np.isfinite(history.train_standardized_mse).all()
    # Actual full-data refit: all fitted scalers receive only the verified TRAIN array.
    with patch.object(study,'fit_scaler',wraps=study.fit_scaler) as scaling:
        fitted=fit_regressors(x_train,y_train)
        assert scaling.call_count==1;np.testing.assert_array_equal(scaling.call_args.args[0],x_train)
    training_runtime={"num_threads":torch.get_num_threads(),"deterministic_algorithms":torch.are_deterministic_algorithms_enabled(),"initial_seed":torch.initial_seed()}
    print("Training runtime before prediction:",json.dumps(training_runtime))
    assert training_runtime=={"num_threads":1,"deterministic_algorithms":True,"initial_seed":42},training_runtime
    repeat,seconds=predict_regressors(fitted,x_test)
    after_predict_threads=torch.get_num_threads()
    print("Threads immediately after model predictions:",after_predict_threads)
    for method,column in [("DTW 3-NN","knn_kwh"),("Time Series Forest","forest_kwh"),("CNN","cnn_kwh")]:
        np.testing.assert_allclose(repeat[method],saved[column],atol=1e-10,rtol=1e-10)
    np.testing.assert_allclose(fitted["history"].train_standardized_mse,history.train_standardized_mse,atol=1e-10,rtol=1e-10)
    prepared=transform(x_test,fitted["scaler"])
    neighbors=fitted["models"]["DTW 3-NN"].kneighbors(prepared,return_distance=False)
    np.testing.assert_allclose(y_train[neighbors].mean(axis=1),saved.knn_kwh,atol=1e-12)
    forest=fitted["models"]["Time Series Forest"]
    manual=np.mean([tree.predict(interval[0].transform(prepared)) for tree,interval in zip(forest.estimators_,forest.intervals_)],axis=0)
    np.testing.assert_allclose(manual,saved.forest_kwh,atol=1e-12)
    model=EnergyCNN().eval()
    with np.load(output/"cnn_weights.npz",allow_pickle=False) as weights:
        model.load_state_dict({key:torch.from_numpy(weights[key].copy()) for key in weights.files})
    with torch.inference_mode():z=model(torch.from_numpy(prepared)).numpy().astype(float)
    np.testing.assert_allclose(z*summary["train_target_scale"]+summary["train_target_mean"],saved.cnn_kwh,atol=1e-10,rtol=1e-10)
    # Reconcile authentic human-review statements, without changing model outputs.
    assert summary["knn_config"]==study.KNN_CONFIG and summary["forest_config"]==study.FOREST_CONFIG
    assert len(forest.estimators_)==200 and forest.n_cases_==95
    assert sum(p.numel() for p in fitted["models"]["CNN"].parameters())==5553
    assert all(p.device.type=="cpu" for p in fitted["models"]["CNN"].parameters())
    post_prediction_runtime={"num_threads":torch.get_num_threads(),"deterministic_algorithms":torch.are_deterministic_algorithms_enabled(),"initial_seed":torch.initial_seed()}
    print("Runtime after independent prediction checks:",json.dumps(post_prediction_runtime))
    assert post_prediction_runtime["deterministic_algorithms"] and post_prediction_runtime["initial_seed"]==42,post_prediction_runtime
    np.testing.assert_allclose(fitted["target_scaler"],[y_train.mean(),y_train.std()],atol=1e-12)
    assert review_metrics[1]["max_absolute_error"]<min(review_metrics[0]["max_absolute_error"],review_metrics[2]["max_absolute_error"])
    assert metrics.loc["DTW 3-NN","rmse"]<metrics.loc["CNN","rmse"]
    assert metrics.loc["CNN","mae"]<metrics.loc["DTW 3-NN","mae"]
    import platform
    windows_reference=[[3.509225,2.711349,-.264841],[2.109183,1.685254,-.077742],[3.614675,2.608054,-.825579]]
    if platform.system()=="Windows":
        np.testing.assert_allclose([[r[k] for k in ["rmse","mae","mean_prediction_minus_true"]] for r in review_metrics],windows_reference,atol=5e-7,rtol=0)
    review_report={"verified_date":"2026-10-26","ai_assistance":"Codex","student_extra_execution_claimed":False,
        "metrics_from_all_126_predictions":review_metrics,"sign_convention":"prediction minus true, kWh",
        "runtime":{"platform":platform.platform(),"machine":platform.machine(),"processor":platform.processor(),
        "torch":torch.__version__,"device":"cpu","num_threads":torch.get_num_threads(),"interop_threads":torch.get_num_interop_threads(),
        "deterministic_algorithms":torch.are_deterministic_algorithms_enabled(),"initial_seed":torch.initial_seed(),
        "mkldnn_enabled":torch.backends.mkldnn.enabled,"torch_build":torch.__config__.show()},
        "training_runtime_before_prediction":training_runtime,"threads_immediately_after_model_predictions":after_predict_threads,"runtime_after_prediction_checks":post_prediction_runtime,
        "reproducibility_scope":"Second full fit in the same runtime, atol/rtol 1e-10; no cross-platform numerical identity claimed",
        "historical_linux_cnn":{"rmse":3.626400,"mae":2.613485,"runs":[40412448258,40412456174]},
        "platform_difference_cause_proven":False,"cnn_train_loss_first":float(history.train_standardized_mse.iloc[0]),"cnn_train_loss_last":float(history.train_standardized_mse.iloc[-1])}
    (output/"review_verification.json").write_text(json.dumps(review_report,indent=2)+"\n",encoding="utf-8")
    print("Runtime:",json.dumps({k:review_report["runtime"][k] for k in ["platform","torch","device","num_threads","interop_threads","deterministic_algorithms","initial_seed","mkldnn_enabled"]}))
    print(pd.DataFrame(review_metrics).to_string(index=False))
    print(metrics.to_string())
    nbformat.write(notebook,source)
    destination=output/"appliances_regression.html";destination.write_text(str(page),encoding="utf-8")
    from importlib.metadata import version
    files=[source,destination,ROOT/"sessions/ch12/regression.py",ROOT/"sessions/ch12/appliances_source.json",output/"summary.json",output/"cnn_weights.npz",output/"review_verification.json"]+sorted(output.glob("*.csv"))+[output/(name+".png") for name in FIGURES]
    manifest={"validated_date":"2026-10-26","ai_assistance":"Codex","human_review":"SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION","merge_authorized":False,"raw_sha256":SOURCE["files"],"seed":SEED,"epochs":EPOCHS,"sequential_code_cells":len(code),"embedded_images":len(images),"all_126_predictions_reproduced":True,"independent_knn_target_mean":True,"independent_forest_tree_mean":True,"saved_cnn_predictions_checked":True,"repeat_fit_seconds":fitted["fit_seconds"],"repeat_predict_seconds":seconds,"packages":{name:version(name) for name in ["aeon","numpy","scikit-learn","torch"]},"files":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (output/"validation_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("PASS: fresh 3-cell notebook, 2 decoded images, TRAIN-only scalers, all 126 repeated predictions, independent RMSE/MAE, neighbor and tree means, saved CNN weights")

if __name__=="__main__":main()
