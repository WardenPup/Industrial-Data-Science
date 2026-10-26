"""Checksum-pinned weekly data and retrospective, gap-preserving smoothing."""

import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/raw/sss1_production_data.csv"
URL = "https://noxthot.github.io/ws26_industrial_datascience_manuscript/data/assets/act1/selfstudysessions/sss1_production_data.csv"
SHA256 = "6310fd9e1fb081929f29715716dca3c433780a09d69c3a422df253a2d9aca494"


def load_production(path=DATA):
    """Load unchanged official data; never silently download during analysis."""
    path = Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Production CSV checksum mismatch")
    frame = pd.read_csv(path, parse_dates=["Date"]).set_index("Date")
    if list(frame.columns) != ["pieces", "pieces_gaps"]:
        raise ValueError("Unexpected production schema")
    expected = pd.date_range("2005-01-02", "2024-12-29", freq="W-SUN", name="Date")
    if not frame.index.equals(expected):
        raise ValueError("Expected unique, ordered weekly Sunday dates")
    if frame.pieces.isna().any() or frame.pieces_gaps.isna().sum() != 367:
        raise ValueError("Unexpected missing-data structure")
    return frame


def smooth_with_gaps(series, window=5, aggregation="median"):
    """Centered historical smoothing; missing source weeks stay missing."""
    if not isinstance(window, int) or isinstance(window, bool) or window < 1 or window % 2 == 0:
        raise ValueError("window must be a positive odd integer")
    if aggregation not in {"median", "mean"}:
        raise ValueError("aggregation must be median or mean")
    rolling = series.rolling(window, center=True, min_periods=1)
    return getattr(rolling, aggregation)().where(series.notna())
