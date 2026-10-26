"""TRAIN-only multivariate DTW kNN/CNN comparison; metrics kept separate."""
from pathlib import Path
from time import perf_counter
import hashlib,json
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from aeon.datasets import load_from_ts_file
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,confusion_matrix,classification_report

ROOT=Path(__file__).resolve().parents[2]
SOURCE=json.loads(Path(__file__).with_name("uwave_source.json").read_text())
SEED=42
EPOCHS=60
BATCH_SIZE=16
LEARNING_RATE=.001
KNN_PARAMS={"n_neighbors":3,"weights":"uniform","distance":"dtw","distance_params":{"window":.1},"n_jobs":1}


def validate_series(x):
    x=np.asarray(x)
    if x.ndim!=3 or min(x.shape)<1 or x.shape[2]<2 or not np.isfinite(x).all():
        raise ValueError("Expected finite nonempty (cases,channels,timepoints)")
    return x


def load_uwave(split):
    if split not in {"TRAIN","TEST"}:raise ValueError("Expected TRAIN or TEST")
    name=f"UWaveGestureLibrary_{split}.ts";path=ROOT/"data/raw/UWaveGestureLibrary"/name
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SOURCE["files"][name]:raise ValueError("Raw UWave checksum mismatch")
    x,y=load_from_ts_file(path)
    validate_series(x)
    if list(x.shape)!=SOURCE["splits"][split]["shape"]:raise ValueError("Unexpected multivariate split shape")
    return x,np.asarray(y)


def fit_scaler(x_train):
    x=validate_series(x_train).astype(np.float64)
    mean=x.mean(axis=(0,2),keepdims=True)
    scale=x.std(axis=(0,2),ddof=0,keepdims=True)
    return mean,np.where(scale>0,scale,1.)


def transform(x,scaler):
    x=validate_series(x)
    mean,scale=scaler
    if mean.shape!=(1,x.shape[1],1) or scale.shape!=mean.shape or not np.isfinite(mean).all() or not np.isfinite(scale).all() or (scale<=0).any():
        raise ValueError("Incompatible TRAIN scaler")
    return np.ascontiguousarray((x-mean)/scale,dtype=np.float32)


class GestureCNN(nn.Module):
    def __init__(self,channels=3,n_classes=8):
        super().__init__()
        self.layers=nn.Sequential(nn.Conv1d(channels,16,7,padding="same"),nn.ReLU(),nn.MaxPool1d(2),
            nn.Conv1d(16,32,5,padding="same"),nn.ReLU(),nn.AdaptiveAvgPool1d(8),nn.Flatten(),nn.Linear(32*8,n_classes))
    def forward(self,x):return self.layers(x)


def fit_cnn(x_train,y_encoded,n_classes,epochs=EPOCHS,seed=SEED):
    x=validate_series(x_train)
    y=np.asarray(y_encoded)
    if len(y)!=len(x) or y.ndim!=1 or not np.issubdtype(y.dtype,np.integer) or y.min()<0 or y.max()>=n_classes:
        raise ValueError("Invalid encoded TRAIN labels")
    if not isinstance(epochs,int) or isinstance(epochs,bool) or epochs<1:raise ValueError("Positive integer epoch count required")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(seed)
    model=GestureCNN(x.shape[1],n_classes).cpu()
    optimizer=torch.optim.Adam(model.parameters(),lr=LEARNING_RATE)
    loss_function=nn.CrossEntropyLoss()
    generator=torch.Generator().manual_seed(seed)
    loader=DataLoader(TensorDataset(torch.as_tensor(x,dtype=torch.float32),torch.as_tensor(y,dtype=torch.long)),
                      batch_size=BATCH_SIZE,shuffle=True,generator=generator,num_workers=0)
    history=[]
    model.train()
    for epoch in range(epochs):
        total=0.
        for values,labels in loader:
            optimizer.zero_grad()
            loss=loss_function(model(values),labels)
            if not torch.isfinite(loss):raise ValueError("Nonfinite CNN loss")
            loss.backward();optimizer.step()
            total+=float(loss.detach())*len(labels)
        history.append({"epoch":epoch+1,"train_cross_entropy":total/len(y)})
    model.eval()
    return model,pd.DataFrame(history)


def fit_classifiers(x_train,y_train):
    """No TEST data or TEST labels accepted by the training API."""
    x_train=validate_series(x_train);y_train=np.asarray(y_train)
    if y_train.ndim!=1 or len(y_train)!=len(x_train):raise ValueError("TRAIN labels mismatch")
    classes,encoded=np.unique(y_train,return_inverse=True)
    scaler=fit_scaler(x_train);x=transform(x_train,scaler)
    knn=KNeighborsTimeSeriesClassifier(**KNN_PARAMS)
    start=perf_counter();knn.fit(x,y_train);knn_seconds=perf_counter()-start
    start=perf_counter();cnn,history=fit_cnn(x,encoded,len(classes));cnn_seconds=perf_counter()-start
    return {"knn":knn,"cnn":cnn,"classes":classes,"scaler":scaler,"history":history,
            "fit_seconds":{"DTW 3-NN":knn_seconds,"CNN":cnn_seconds}}


def predict_classifiers(fitted,x_test):
    """One final prediction per method; no labels or optimization here."""
    x=transform(x_test,fitted["scaler"])
    start=perf_counter();knn=fitted["knn"].predict(x);knn_seconds=perf_counter()-start
    start=perf_counter()
    with torch.inference_mode():logits=fitted["cnn"](torch.from_numpy(x)).numpy()
    cnn=fitted["classes"][logits.argmax(axis=1)]
    cnn_seconds=perf_counter()-start
    return {"DTW 3-NN":knn,"CNN":cnn},{"DTW 3-NN":knn_seconds,"CNN":cnn_seconds},logits


def evaluate(y_true,predictions,classes):
    y_true=np.asarray(y_true);rows=[];matrices={};reports=[]
    if not np.isin(y_true,classes).all():raise ValueError("Unknown TEST class")
    for name,predicted in predictions.items():
        predicted=np.asarray(predicted)
        if predicted.shape!=y_true.shape or not np.isin(predicted,classes).all():raise ValueError("Invalid prediction labels")
        rows.append({"method":name,"accuracy":accuracy_score(y_true,predicted),
                     "balanced_accuracy":balanced_accuracy_score(y_true,predicted),
                     "macro_f1":f1_score(y_true,predicted,labels=classes,average="macro",zero_division=0)})
        matrices[name]=confusion_matrix(y_true,predicted,labels=classes)
        report=classification_report(y_true,predicted,labels=classes,output_dict=True,zero_division=0)
        reports.extend({"method":name,"class":str(label),**report[str(label)]} for label in classes)
    return pd.DataFrame(rows),matrices,pd.DataFrame(reports)
