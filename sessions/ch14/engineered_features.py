"""Fixed HDF/PWF feature comparisons with TRAIN-only decision-tree fits."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sessions.ch14.tool_wear import load_data
from sessions.ch14.overstrain import tree, scores

BASE = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]
FEATURES = {"HDF": "temp_diff", "PWF": "power"}
DEPTHS = tuple(range(1, 9))
SEED = 42

def prepare(data):
    result = data.copy()
    result["temp_diff"] = result["Process temperature [K]"] - result["Air temperature [K]"]
    result["power"] = result["Torque [Nm]"] * result["Rotational speed [rpm]"] * 2*np.pi/60
    return result

def analyze():
    data = prepare(load_data())
    rows, predictions, split_rows, counts = [], [], [], []
    for target, feature in FEATURES.items():
        y = data[target]
        train, test = train_test_split(np.arange(len(data)), test_size=.2, stratify=y, random_state=SEED)
        counts.append({"Ziel": target, "Gesamt": len(y), "Positive": int(y.sum()), "TRAIN": len(train), "TRAIN positiv": int(y.iloc[train].sum()), "TEST": len(test), "TEST positiv": int(y.iloc[test].sum())})
        for label, indices in [("TRAIN", train), ("TEST", test)]:
            split_rows.extend({"Ziel": target, "UDI": int(data.iloc[i].UDI), "Split": label} for i in indices)
        fixed = pd.DataFrame({"Ziel": target, "UDI": data.iloc[test].UDI.to_numpy(), "Wahr": y.iloc[test].to_numpy()})
        for variant, columns in [("Basis", BASE), ("+ Merkmal", BASE + [feature])]:
            for depth in DEPTHS:
                model = tree(depth).fit(data.iloc[train][columns], y.iloc[train])
                for label, indices in [("TRAIN", train), ("TEST", test)]:
                    prediction = model.predict(data.iloc[indices][columns])
                    rows.append({"Ziel": target, "Variante": variant, "Merkmal": feature if variant != "Basis" else "keines", "Tiefe": depth, "Split": label, **scores(y.iloc[indices], prediction)})
                    if depth == 3 and label == "TEST":
                        fixed[variant] = prediction
        predictions.append(fixed)
    return data, pd.DataFrame(rows), pd.concat(predictions, ignore_index=True), pd.DataFrame(split_rows), pd.DataFrame(counts)
