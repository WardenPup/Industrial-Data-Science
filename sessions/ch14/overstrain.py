"""OSF feature engineering and fixed decision-tree comparisons."""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sessions.ch14.tool_wear import load_data, WEAR

TORQUE = "Torque [Nm]"
BASE = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", TORQUE, WEAR, "temp_diff", "power"]
GROUPS = {"Kursbasis": BASE, "+ Produkt": BASE + ["wearadjTorque"], "+ Produkt + Type": BASE + ["wearadjTorque", "Type_M", "Type_H"]}

def prepare(data):
    result = data.copy()
    result["temp_diff"] = result["Process temperature [K]"] - result["Air temperature [K]"]
    result["power"] = result[TORQUE] * result["Rotational speed [rpm]"] * 2*np.pi/60
    result["wearadjTorque"] = result[TORQUE] * result[WEAR]
    # Fixed categorical indicators: no ordering assumption and no fitted preprocessing.
    for variant in ["M", "H"]:
        result["Type_" + variant] = result.Type.eq(variant).astype(int)
    return result

def tree(depth):
    return DecisionTreeClassifier(max_depth=depth, random_state=42, min_samples_split=5, min_samples_leaf=5)

def scores(y, prediction):
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    return {"Fehler": int(fp+fn), "FP": int(fp), "FN": int(fn), "TP": int(tp), "F1": float(f1_score(y, prediction, zero_division=0))}

def analyze():
    data = prepare(load_data())
    y = data.OSF
    rows, models = [], {}
    # Official exploratory comparison, not an estimate of predictive performance.
    for name, columns in GROUPS.items():
        for depth in range(1, 9):
            model = tree(depth).fit(data[columns], y)
            rows.append({"Merkmale": name, "Tiefe": depth, **scores(y, model.predict(data[columns]))})
            models[name, depth] = model
    train, test = train_test_split(np.arange(len(data)), test_size=.2, stratify=y, random_state=42)
    # Depth 3 is specified by the course, fixed before inspecting TEST.
    heldout = []
    for name, columns in GROUPS.items():
        model = tree(3).fit(data.iloc[train][columns], y.iloc[train])
        heldout.append({"Merkmale": name, "Tiefe": 3, **scores(y.iloc[test], model.predict(data.iloc[test][columns]))})
    rule = data.wearadjTorque > data.Type.map({"L": 11000, "M": 12000, "H": 13000})
    summary = {"rows": len(data), "osf": int(y.sum()), "rule_mismatches": int((rule != y).sum()),
               "train_rows": len(train), "test_rows": len(test), "train_osf": int(y.iloc[train].sum()), "test_osf": int(y.iloc[test].sum()), "seed": 42}
    return data, pd.DataFrame(rows), pd.DataFrame(heldout), models, summary
