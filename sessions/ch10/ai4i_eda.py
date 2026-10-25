"""Small, testable descriptive helpers; no mutation or row removal."""

from itertools import combinations

import numpy as np
import pandas as pd

from sessions.ch10.ai4i_data import COLUMNS

MEASUREMENTS = COLUMNS[1:]
TORQUE, SPEED, AIR = MEASUREMENTS
SEED = 42
PLOTS = ["01_line", "02_histograms", "03_boxplots", "04_violins", "05_scatter",
         "06_pairplot", "07_heatmap", "08_joint_regression", "09_strip", "10_count"]


def iqr_summary(values: pd.DataFrame) -> pd.DataFrame:
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    spread = q3 - q1
    lower, upper = q1 - 1.5 * spread, q3 + 1.5 * spread
    # Decimal measurements on a theoretical fence must not be flagged because
    # 12.8 and 12.800000000000011 differ in floating-point representation.
    tolerance = 1e-10
    flagged = (values < lower - tolerance) | (values > upper + tolerance)
    return pd.DataFrame({"q1": q1, "q3": q3, "lower_fence": lower, "upper_fence": upper,
                         "flagged_count": flagged.sum(),
                         "skewness": values.skew(), "minimum": values.min(), "maximum": values.max()})


def add_bins(data: pd.DataFrame):
    result = data.copy()
    result["speed_band"], speed_edges = pd.cut(
        result[SPEED], bins=3, labels=["low", "medium", "high"], include_lowest=True, retbins=True
    )
    result["torque_band"], torque_edges = pd.cut(
        result[TORQUE], bins=10, include_lowest=True, retbins=True
    )
    if result[["speed_band", "torque_band"]].isna().any().any():
        raise ValueError("Every observation must have both bin assignments")
    return result, {"speed_edges": speed_edges.tolist(), "torque_edges": torque_edges.tolist()}


def strongest_pair(correlation: pd.DataFrame):
    pairs = [(a, b, float(correlation.loc[a, b])) for a, b in combinations(correlation.columns, 2)]
    return max(pairs, key=lambda pair: abs(pair[2]))


def pearson_reference(x, y):
    """Independent NumPy reference used to check pandas' correlation calculation."""
    return float(np.corrcoef(x, y)[0, 1])
