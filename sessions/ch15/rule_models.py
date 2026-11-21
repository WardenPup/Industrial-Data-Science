"""Fixed exploratory rules and shallow TRAIN-only trees; no threshold tuning."""
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sessions.ch15.drilling_data import SUBGROUPS
from sessions.ch15.exploration import NUMERIC, CATEGORICAL

FEATURES = NUMERIC + CATEGORICAL
SEED = 42
# Positive CCF sample bounds previously exported in Exercise 15.2; inclusive.
CCF_BOUNDS = [(16.57,30.67),(440,813),(.108,.297),(62,243),(50.83,269.06),(0,100),(18.02,37.71)]

def predict_bef(data):
    return (data[NUMERIC[0]].le(22) & data["Cooling [%]"].le(25)).astype(int)

def predict_ccf(data):
    return pd.concat([data[c].between(lo,hi) for c,(lo,hi) in zip(NUMERIC,CCF_BOUNDS)],axis=1).all(axis=1).astype(int)

def predict_fwf(data):
    result = pd.Series(False,index=data.index)
    for material,vc,vf in [("K",16.67,149),("N",29.70,206),("P",21.99,127)]:
        result |= data.Material.eq(material) & data[NUMERIC[0]].le(vc) & data[NUMERIC[3]].ge(vf)
    return result.astype(int)

def predict_wdf(data):
    expected = data.Material.map({"P":"N","K":"H","N":"W"})
    return data["Drill Bit Type"].ne(expected).astype(int)

RULES = dict(zip(SUBGROUPS,[predict_bef,predict_ccf,predict_fwf,predict_wdf]))

def split_data(data):
    groups = pd.util.hash_pandas_object(data[FEATURES],index=False)
    train,test = next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=SEED).split(data,groups=groups))
    return train,test

def evaluate(data):
    train,test = split_data(data)
    rows=[]; predictions=[]; models={}; texts={}
    for flag in SUBGROUPS:
        preprocess=ColumnTransformer([("numeric","passthrough",NUMERIC),("category",OneHotEncoder(handle_unknown="ignore",sparse_output=False),CATEGORICAL)])
        model=make_pipeline(preprocess,DecisionTreeClassifier(max_depth=3,random_state=SEED))
        model.fit(data.iloc[train][FEATURES],data.iloc[train][flag])
        truth=data.iloc[test][flag].to_numpy()
        methods={"Regel":RULES[flag](data.iloc[test]).to_numpy(),"Baum":model.predict(data.iloc[test][FEATURES])}
        for name,pred in methods.items():
            tn,fp,fn,tp=confusion_matrix(truth,pred,labels=[0,1]).ravel()
            rows.append(dict(Fehlertyp=flag,Methode=name,TN=int(tn),FP=int(fp),FN=int(fn),TP=int(tp),Precision=precision_score(truth,pred,zero_division=0),Recall=recall_score(truth,pred,zero_division=0),F1=f1_score(truth,pred,zero_division=0)))
        predictions.append(pd.DataFrame({"ID":data.iloc[test].ID.to_numpy(),"Fehlertyp":flag,"Ist":truth,"Regel":methods["Regel"],"Baum":methods["Baum"]}))
        models[flag]=model
        texts[flag]=export_text(model[-1],feature_names=list(model[0].get_feature_names_out()),decimals=3)
    split=pd.DataFrame({"ID":data.ID,"Split":"TRAIN"});split.loc[split.index[test],"Split"]="TEST"
    counts=pd.DataFrame({"TRAIN":data.iloc[train][SUBGROUPS].sum(),"TEST":data.iloc[test][SUBGROUPS].sum()}).rename_axis("Fehlertyp").reset_index()
    return pd.DataFrame(rows),pd.concat(predictions,ignore_index=True),split,counts,models,texts
