"""Pinned original XAI Drilling data and descriptive label checks for 15.1."""
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DATA_PATH=ROOT/"data/raw/XAI_Drilling_Dataset.csv"
URL="https://www.kaggle.com/api/v1/datasets/download/raphaelwallsberger/xai-drilling-dataset?datasetVersionNumber=1"
SHA256="e1dcc45f8821f7b96d923a253374150d5013cead40bc08b4bef33033aef0ab83"
MAIN="Main Failure"
SUBGROUPS=["BEF","CCF","FWF","WDF"]
TARGETS=[MAIN]+SUBGROUPS
COLUMNS=["ID","Cutting speed vc [m/min]","Spindle speed n [1/min]","Feed f [mm/rev]","Feed rate vf [mm/min]","Power Pc [kW]","Cooling [%]","Material","Drill Bit Type","Process Time [sec]"]+TARGETS

def verify_file(path=DATA_PATH):
    digest=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest!=SHA256:raise ValueError("XAI Drilling SHA256 mismatch: preserve and inspect original bytes")
    return digest

def load_data(path=DATA_PATH):
    verify_file(path)
    data=pd.read_csv(path)
    if list(data.columns)!=COLUMNS or data.shape!=(20000,15):raise ValueError("Unexpected drilling schema/shape")
    if data.isna().any().any() or data.ID.tolist()!=list(range(1,20001)):raise ValueError("Unexpected missing values/IDs")
    if data.select_dtypes("number").shape[1]!=13 or not np.isfinite(data.select_dtypes("number")).all().all():raise ValueError("Unexpected numeric types or nonfinite values")
    for flag in TARGETS:
        if not pd.api.types.is_integer_dtype(data[flag]) or not data[flag].isin([0,1]).all():raise ValueError("Expected binary integer flags")
    if set(data.Material)!={"K","N","P"} or set(data["Drill Bit Type"])!={"H","N","W"} or set(data["Cooling [%]"])!={0,25,50,75,100}:raise ValueError("Unexpected categorical levels")
    return data

def label_tables(data):
    labels=data[TARGETS]
    if labels.isna().any().any() or not labels.isin([0,1]).all().all():raise ValueError("Expected complete binary labels")
    sub_count=labels[SUBGROUPS].sum(axis=1)
    union=sub_count.gt(0).astype(int)
    counts=pd.DataFrame({"Ziel":TARGETS,"Markiert":labels.sum().to_numpy(dtype=int),"Nicht markiert":(labels==0).sum().to_numpy(dtype=int),"Anteil [%]":labels.mean().to_numpy()*100})
    cross=pd.crosstab(labels[MAIN],union).reindex(index=[0,1],columns=[0,1],fill_value=0)
    cross.index.name="Main Failure";cross.columns.name="Untergruppen-ODER"
    multiplicity=sub_count.value_counts().reindex(range(5),fill_value=0).rename_axis("Anzahl Untergruppen").reset_index(name="Zeilen")
    conflicts=data.loc[labels[MAIN].ne(union),["ID"]+TARGETS].copy()
    multiple=data.loc[sub_count.gt(1),["ID"]+TARGETS].copy()
    return counts,cross,multiplicity,conflicts,multiple
