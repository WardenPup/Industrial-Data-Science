"""Descriptive TWF checks on the unchanged AI4I source; no model fitting."""
from pathlib import Path

import numpy as np
import pandas as pd

from sessions.ch10.ai4i_data import DATA_PATH, verify_file

WEAR = "Tool wear [min]"
FLAGS = ["Machine failure", "TWF", "HDF", "PWF", "OSF", "RNF"]


def load_data(path: Path = DATA_PATH):
    """Reuse the existing hash guard, but retain all original columns."""
    verify_file(path)
    data = pd.read_csv(path)
    if data.shape != (10000, 14) or data.isna().any().any() or data.duplicated().any():
        raise ValueError("Unexpected AI4I shape, missing values or duplicate rows")
    if data.UDI.tolist() != list(range(1, 10001)):
        raise ValueError("Original row identifiers required")
    if set(data.Type) != {"L", "M", "H"}:
        raise ValueError("Unexpected product variants")
    for col in FLAGS:
        if not pd.api.types.is_integer_dtype(data[col]) or not data[col].isin([0, 1]).all():
            raise ValueError(f"Expected binary integer flag: {col}")
    numeric = data.select_dtypes(include="number")
    if numeric.shape[1] != 12 or not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("Unexpected numeric types or nonfinite values")
    return data


def wear_tables(data):
    """Count inclusive source interval and the fixed course split, without mutation."""
    wear, twf = data[WEAR], data["TWF"]
    if (not pd.api.types.is_integer_dtype(wear) or wear.isna().any()
            or (wear < 0).any() or twf.isna().any() or not twf.isin([0, 1]).all()):
        raise ValueError("Expected nonnegative integer wear and binary TWF")

    def count_rows(groups):
        return pd.DataFrame([
            {"Bereich": label, "Datensätze": int(mask.sum()),
             "TWF=1": int(twf[mask].sum()), "TWF=0": int((twf[mask] == 0).sum())}
            for label, mask in groups
        ])

    bands = count_rows([("< 200 min", wear < 200),
                        ("200–240 min (einschließlich)", wear.between(200, 240)),
                        ("> 240 min", wear > 240)])
    threshold = count_rows([("≤ 202,5 min", wear <= 202.5),
                            ("> 202,5 min", wear > 202.5)])
    outside = data.loc[twf.eq(1) & ~wear.between(200, 240),
                       ["UDI", WEAR, "TWF", "Machine failure"]].copy()
    return bands, threshold, outside
