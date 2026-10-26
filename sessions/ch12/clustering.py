"""Reproducible clustering of unchanged variable-length GesturePebbleZ1 data."""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
import pandas as pd
from aeon.datasets import load_from_ts_file
from aeon.clustering import KASBA, TimeSeriesKMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

ROOT=Path(__file__).resolve().parents[2]
SOURCE=json.loads((Path(__file__).with_name("gesture_source.json")).read_text())
SEED=42
LENGTH=128


def load_gestures(split):
    if split not in {"TRAIN","TEST"}: raise ValueError("split must be TRAIN or TEST")
    filename=f"GesturePebbleZ1_{split}.ts"
    path=ROOT/"data/raw/GesturePebbleZ1"/filename
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SOURCE["files"][filename]:
        raise ValueError("Raw gesture checksum mismatch")
    series,labels=load_from_ts_file(path)
    if len(series)!={"TRAIN":132,"TEST":172}[split]: raise ValueError("Unexpected split size")
    for values in series:
        if values.shape[0]!=1 or values.shape[1]<2 or not np.isfinite(values).all():
            raise ValueError("Expected finite univariate variable-length observations")
    return series,np.asarray(labels)


def resample_normalize(series,length=LENGTH):
    """Relative-time interpolation then per-case z-normalization; no test fitting."""
    if not isinstance(length,int) or isinstance(length,bool) or length<2:
        raise ValueError("length must be integer >=2")
    result=[]
    for values in series:
        values=np.asarray(values,dtype=float)
        if values.ndim!=2 or values.shape[0]!=1 or values.shape[1]<2 or not np.isfinite(values).all():
            raise ValueError("Need finite (1,L) input with L>=2")
        row=np.interp(np.linspace(0,1,length),np.linspace(0,1,values.shape[1]),values[0])
        std=row.std(ddof=0)
        result.append((row-row.mean())/std if std>0 else np.zeros_like(row))
    if not result: raise ValueError("Empty collection")
    return np.asarray(result)[:,None,:]


def msm_matrix(x,y,c=1.):
    """Small univariate educational MSM dynamic program, not the clustering engine."""
    x,y=np.asarray(x,dtype=float),np.asarray(y,dtype=float)
    if x.ndim!=1 or y.ndim!=1 or not len(x) or not len(y) or not np.isfinite(x).all() or not np.isfinite(y).all() or not np.isfinite(c) or c<=0:
        raise ValueError("Finite nonempty 1D sequences and positive cost required")
    def cost(v,a,b):
        return c if min(a,b)<=v<=max(a,b) else c+min(abs(v-a),abs(v-b))
    d=np.zeros((len(x),len(y)))
    d[0,0]=abs(x[0]-y[0])
    for i in range(1,len(x)): d[i,0]=d[i-1,0]+cost(x[i],x[i-1],y[0])
    for j in range(1,len(y)): d[0,j]=d[0,j-1]+cost(y[j],x[0],y[j-1])
    for i in range(1,len(x)):
        for j in range(1,len(y)):
            d[i,j]=min(d[i-1,j-1]+abs(x[i]-y[j]),d[i-1,j]+cost(x[i],x[i-1],y[j]),d[i,j-1]+cost(y[j],x[i],y[j-1]))
    return d


def run_experiment():
    train,y_train=load_gestures("TRAIN")
    test,y_test=load_gestures("TEST")
    x_train,x_test=resample_normalize(train),resample_normalize(test)
    models={"Euclidean k-means":TimeSeriesKMeans(n_clusters=6,distance="euclidean",averaging_method="mean",init="kmeans++",n_init=3,max_iter=30,random_state=SEED,n_jobs=1),
            "KASBA (MSM)":KASBA(n_clusters=6,distance="msm",distance_params={"c":1.},max_iter=30,random_state=SEED)}
    metrics=[];assignments=[]
    for name,model in models.items():
        started=perf_counter();model.fit(x_train);fit_seconds=perf_counter()-started
        started=perf_counter();test_labels=model.predict(x_test);predict_seconds=perf_counter()-started
        for split,y,labels in [("TRAIN",y_train,model.labels_),("TEST",y_test,test_labels)]:
            metrics.append({"method":name,"split":split,"n":len(y),"ARI":float(adjusted_rand_score(y,labels)),"NMI":float(normalized_mutual_info_score(y,labels)),
                            "clusters_used":int(len(np.unique(labels))),"fit_seconds":fit_seconds,"predict_seconds":predict_seconds,"n_iter":int(model.n_iter_)})
            assignments.extend({"method":name,"split":split,"case":i,"class":str(y[i]),"cluster":int(label)} for i,label in enumerate(labels))
    return (train,test),(x_train,x_test),models,pd.DataFrame(metrics),pd.DataFrame(assignments)
