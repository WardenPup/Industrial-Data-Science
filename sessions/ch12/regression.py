"""Three fixed time-series regressors; TEST is excluded from all training APIs."""
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from aeon.datasets import load_regression
from aeon.regression.distance_based import KNeighborsTimeSeriesRegressor
from aeon.regression.interval_based import TimeSeriesForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sessions.ch12.classification import fit_scaler, transform, validate_series

ROOT = Path(__file__).resolve().parents[2]
SOURCE = json.loads(Path(__file__).with_name('appliances_source.json').read_text())
SEED, EPOCHS = 42, 60
KNN_CONFIG = dict(n_neighbors=3, weights='uniform', distance='dtw',
                  distance_params={'window': .1}, n_jobs=1)
FOREST_CONFIG = dict(n_estimators=200, n_intervals='sqrt', min_interval_length=3,
                     random_state=SEED, n_jobs=1, time_limit_in_minutes=None)


def load_appliances(split):
    if split not in {'TRAIN', 'TEST'}: raise ValueError('Expected TRAIN or TEST')
    name = f'AppliancesEnergy_{split}.ts'
    path = ROOT / 'data/raw/AppliancesEnergy' / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != SOURCE['files'][name]:
        raise ValueError('Original data checksum mismatch')
    # Files must already be present and verified: this call never downloads implicitly.
    x, y = load_regression('AppliancesEnergy', split=split.lower(),
                            extract_path=str(ROOT / 'data/raw'))
    x = validate_series(x); y = validate_targets(y, len(x))
    if list(x.shape) != SOURCE['splits'][split]['shape']:
        raise ValueError('Unexpected AppliancesEnergy shape')
    return x, y


def validate_targets(y, cases):
    y = np.asarray(y, dtype=float)
    if y.shape != (cases,) or not np.isfinite(y).all():
        raise ValueError('Finite aligned scalar targets required')
    return y


class EnergyCNN(nn.Module):
    def __init__(self, channels=24):
        super().__init__()
        self.layers = nn.Sequential(nn.Conv1d(channels,16,7,padding='same'), nn.ReLU(),
            nn.MaxPool1d(2), nn.Conv1d(16,32,5,padding='same'), nn.ReLU(),
            nn.AdaptiveAvgPool1d(8), nn.Flatten(), nn.Linear(256,1))
    def forward(self, x): return self.layers(x).squeeze(-1)


def fit_cnn(x_train, y_train, epochs=EPOCHS, seed=SEED):
    x = validate_series(x_train); y = validate_targets(y_train, len(x))
    if not isinstance(epochs,int) or isinstance(epochs,bool) or epochs < 1:
        raise ValueError('Positive integer epochs required')
    mean, scale = float(y.mean()), float(y.std(ddof=0))
    if scale == 0: scale = 1.
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True); torch.manual_seed(seed)
    model = EnergyCNN(x.shape[1]).cpu()
    optimizer = torch.optim.Adam(model.parameters(), lr=.001)
    loader = DataLoader(TensorDataset(torch.as_tensor(x,dtype=torch.float32),
        torch.as_tensor((y-mean)/scale,dtype=torch.float32)), batch_size=16, shuffle=True,
        generator=torch.Generator().manual_seed(seed), num_workers=0)
    history=[]; model.train()
    for epoch in range(epochs):
        total=0.
        for values, targets in loader:
            optimizer.zero_grad(); loss=nn.functional.mse_loss(model(values),targets)
            if not torch.isfinite(loss): raise ValueError('Nonfinite CNN loss')
            loss.backward(); optimizer.step(); total+=float(loss.detach())*len(values)
        history.append({'epoch':epoch+1,'train_standardized_mse':total/len(x)})
    model.eval()
    return model,(mean,scale),pd.DataFrame(history)


def fit_regressors(x_train, y_train):
    x_train=validate_series(x_train); y=validate_targets(y_train,len(x_train))
    scaler=fit_scaler(x_train); x=transform(x_train,scaler)
    models={}; seconds={}
    for name, model in [('DTW 3-NN',KNeighborsTimeSeriesRegressor(**KNN_CONFIG)),
                         ('Time Series Forest',TimeSeriesForestRegressor(**FOREST_CONFIG))]:
        start=perf_counter(); model.fit(x,y); seconds[name]=perf_counter()-start; models[name]=model
    start=perf_counter();cnn,target_scaler,history=fit_cnn(x,y);seconds['CNN']=perf_counter()-start
    models['CNN']=cnn
    return dict(models=models,scaler=scaler,target_scaler=target_scaler,
                history=history,fit_seconds=seconds)


def predict_regressors(fitted, x_test):
    x=transform(x_test,fitted['scaler']); predictions={}; seconds={}
    for name,model in fitted['models'].items():
        start=perf_counter()
        if name=='CNN':
            with torch.inference_mode(): predicted=model(torch.from_numpy(x)).numpy()
            mean,scale=fitted['target_scaler']; predicted=predicted.astype(float)*scale+mean
        else: predicted=model.predict(x)
        seconds[name]=perf_counter()-start
        predictions[name]=validate_targets(predicted,len(x))
    return predictions,seconds


def evaluate_regressors(y_true, predictions):
    y=validate_targets(y_true,len(y_true));rows=[]
    for name,predicted in predictions.items():
        p=validate_targets(predicted,len(y))
        rows.append(dict(method=name,rmse=root_mean_squared_error(y,p),mae=mean_absolute_error(y,p)))
    return pd.DataFrame(rows)
