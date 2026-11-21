"""Course 16.1 data preparation and the prescribed vibration CNN frame."""
import hashlib
import json
from pathlib import Path
import urllib.request
import numpy as np
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

ROOT=Path(__file__).resolve().parents[2]
DATA_PATH=ROOT/"data/raw/sss3_multimodal.json"
DATA_URL="https://noxthot.github.io/ws26_industrial_datascience_manuscript/data/assets/act2/selfstudysessions/sss3_multimodal.json"
RAW_SHA256="3f7a7e52bd2b0efd0f3af43b07efa2c05620589a09d67d82519598f6f99d6d03"
NAMES=["Normal","Warning","Critical"]
SEED=42

def load_multimodal_data(source: str=DATA_URL):
    content=urllib.request.urlopen(source).read() if str(source).startswith("http") else Path(source).read_bytes()
    if hashlib.sha256(content).hexdigest()!=RAW_SHA256:raise ValueError("Original multimodal JSON checksum mismatch")
    data=json.loads(content)
    arrays=tuple(np.array(data[k]) for k in ["time_series","images","labels","levels"])
    for values,shape in zip(arrays,[(500,80),(500,32,32),(500,),(500,2)]):
        if values.shape!=shape or not np.isfinite(values).all():raise ValueError("Unexpected shape or nonfinite data")
    if not np.isin(arrays[2],[0,1,2]).all() or not np.isin(arrays[3],[0,1,2]).all():raise ValueError("Unexpected status/level")
    return arrays

def prepare_data(ts_data,img_data,labels,levels):
    train_indices,test_indices=train_test_split(np.arange(len(labels)),test_size=.2,random_state=42,stratify=labels)
    result={"train_indices":train_indices,"test_indices":test_indices}
    for name,values in [("ts",ts_data),("img",img_data),("y",labels),("levels",levels)]:
        result[name+"_train"],result[name+"_test"]=values[train_indices],values[test_indices]
    for name in ["ts","img"]:
        mean,std=result[name+"_train"].mean(),result[name+"_train"].std()
        if not std>0:raise ValueError("Zero training standard deviation")
        result[name+"_mean"],result[name+"_std"]=float(mean),float(std)
        for part in ["train","test"]:
            norm=(result[name+"_"+part]-mean)/std
            result[name+"_"+part+"_norm"]=norm
            result[name+"_"+part+"_tensor"]=torch.FloatTensor(norm).unsqueeze(1)
    result["y_train_tensor"]=torch.LongTensor(result["y_train"])
    return result

class TimeSeriesCNN(nn.Module):
    """Exact Table 16.2: 32 features followed by three class logits."""
    def __init__(self):
        super().__init__()
        self.features=nn.Sequential(
            nn.Conv1d(1,16,kernel_size=5,padding="same"),nn.ReLU(),nn.MaxPool1d(2),
            nn.Conv1d(16,32,kernel_size=5,padding="same"),nn.ReLU(),nn.MaxPool1d(2),
            nn.AvgPool1d(20),nn.Flatten(),nn.Linear(32,32),nn.ReLU(),nn.Dropout(.3))
        self.classifier=nn.Linear(32,3)
    def forward(self,x):return self.classifier(self.features(x))

def train_model(model: nn.Module,loader: DataLoader,epochs: int)->nn.Module:
    """Official reusable frame: default Adam, cross entropy and TRAIN batches."""
    optimizer=optim.Adam(model.parameters())
    criterion=nn.CrossEntropyLoss()
    model.train()
    for _ in range(epochs):
        for *inputs,targets in loader:
            optimizer.zero_grad()
            loss=criterion(model(*inputs),targets)
            loss.backward()
            optimizer.step()
    model.eval()
    return model

def predict_proba(model: nn.Module,*inputs: torch.Tensor)->np.ndarray:
    with torch.no_grad():return torch.softmax(model(*inputs),dim=1).numpy()
