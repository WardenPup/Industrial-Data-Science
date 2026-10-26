"""Exercise 11.2: imputation of the approved smoothed weekly series."""

import hashlib

import numpy as np
import pandas as pd

from sessions.ch11.production import load_production, smooth_with_gaps

METHODS = {
    "ffill": "Forward Fill", "bfill": "Backward Fill", "linear": "Linear",
    "polynomial2": "Polynom Grad 2", "polynomial5": "Polynom Grad 5", "pchip": "PCHIP",
}
# Canonical float64 little-endian values (NaN -> 0), followed by the NaN mask.
# Pinned from the approved 11.1 series at merge b7543e0; raw calendar checked by loader.
INPUT_SHA256 = "7db834208a47d1045b94afb2a91b14497b5970699f9eb2dd93320dc54640388c"


def input_digest(series):
    payload = np.nan_to_num(series.to_numpy(), nan=0).astype("<f8").tobytes()
    return hashlib.sha256(payload + series.isna().to_numpy().tobytes()).hexdigest()


def load_smoothed_input():
    frame = load_production()
    series = smooth_with_gaps(frame.pieces_gaps, window=5, aggregation="median")
    if input_digest(series) != INPUT_SHA256:
        raise ValueError("Smoothed input differs from approved Exercise 11.1")
    return frame, series.rename("smoothed_gaps")


def impute_series(series, method):
    """Fill only missing values; interpolation never extrapolates boundaries."""
    if method not in METHODS:
        raise ValueError("Unknown imputation method")
    if not isinstance(series.index, pd.DatetimeIndex) or not series.index.is_unique:
        raise ValueError("Expected a unique weekly DatetimeIndex")
    intervals = np.diff(series.index.to_numpy(dtype="datetime64[ns]"))
    if len(series) > 1 and not (intervals == np.timedelta64(7, "D")).all():
        raise ValueError("Expected ordered, equally spaced weekly observations")
    if method in {"ffill", "bfill"}:
        return getattr(series, method)()
    order = int(method[-1]) if method.startswith("polynomial") else None
    required = order + 1 if order else 2
    if series.notna().sum() < required:
        raise ValueError(f"{method} needs at least {required} observed values")
    kwargs = {"order": order} if order else {}
    return series.interpolate(method="polynomial" if order else method,
                              limit_area="inside", **kwargs)


def gap_table(series):
    """Contiguous original gaps and their immediate bounding observations."""
    rows = []
    missing = series.isna().to_numpy()
    edges = np.diff(np.r_[False, missing, False].astype(int))
    for start, stop in zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)):
        rows.append({"start": series.index[start], "end": series.index[stop - 1],
                     "weeks": int(stop - start),
                     "left": series.iloc[start - 1] if start else np.nan,
                     "right": series.iloc[stop] if stop < len(series) else np.nan})
    return pd.DataFrame(rows, columns=["start", "end", "weeks", "left", "right"])


def summarize_methods(series, results):
    """Diagnostics on originally missing weeks, never accuracy against pieces."""
    gaps = gap_table(series)
    missing = series.isna()
    rows = []
    for method in results:
        result = results[method]
        outside = 0
        for gap in gaps.itertuples():
            if pd.notna(gap.left) and pd.notna(gap.right):
                values = result.loc[gap.start:gap.end]
                low, high = sorted([gap.left, gap.right])
                outside += int(((values < low - 1e-9) | (values > high + 1e-9)).sum())
        filled = result[missing].dropna()
        rows.append({"method": method, "filled": len(filled), "remaining": int(result.isna().sum()),
                     "imputed_min": filled.min(), "imputed_max": filled.max(),
                     "negative_imputed": int((filled < 0).sum()), "outside_gap_anchors": outside})
    return pd.DataFrame(rows).set_index("method")
