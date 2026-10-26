"""TRAIN-only aeon interval forest and immutable Exercise 12.2 comparison."""
import hashlib
import json
from io import StringIO
from pathlib import Path
import subprocess
from time import perf_counter

import numpy as np
import pandas as pd
from aeon.classification.interval_based import TimeSeriesForestClassifier

from sessions.ch12.classification import fit_scaler, transform, validate_series

ROOT = Path(__file__).resolve().parents[2]
CONFIG = dict(n_estimators=200, n_intervals="sqrt", min_interval_length=3,
              time_limit_in_minutes=None, random_state=42, n_jobs=1)


def fit_forest(x_train, y_train):
    """No TEST argument: preprocessing and all tree fits use TRAIN only."""
    x = validate_series(x_train)
    y = np.asarray(y_train)
    if y.ndim != 1 or len(y) != len(x) or len(np.unique(y)) < 2:
        raise ValueError("At least two aligned TRAIN classes required")
    start = perf_counter()
    scaler = fit_scaler(x)
    model = TimeSeriesForestClassifier(**CONFIG)
    model.fit(transform(x, scaler), y)
    return model, scaler, perf_counter() - start


def predict_forest(model, scaler, x_test):
    """Time the official predict; probabilities are a separate diagnostic call."""
    x = transform(x_test, scaler)
    start = perf_counter()
    labels = model.predict(x)
    seconds = perf_counter() - start
    probabilities = model.predict_proba(x)
    if not np.isfinite(probabilities).all() or (probabilities < 0).any():
        raise ValueError("Invalid forest probabilities")
    np.testing.assert_allclose(probabilities.sum(axis=1), 1, atol=1e-12)
    # Installed aeon BaseIntervalForest uses first argmax for exact ties.
    expected = model.classes_[probabilities.argmax(axis=1)]
    np.testing.assert_array_equal(labels, expected)
    return labels, probabilities, seconds


def load_reference(y_test):
    """Use all approved TEST predictions unchanged; reject drift or reordering."""
    reference = json.loads((ROOT / "sessions/ch12/forest_reference.json").read_text())
    verified = {}
    for name, digest in reference["files"].items():
        # CI reexecutes 12.2 first: times and line endings can change locally.
        # Verify the immutable approved bytes in Git, and current scientific values.
        data = (subprocess.check_output(["git", "show", reference["approved_commit"]+":"+name], cwd=ROOT)
                if (ROOT / ".git").exists() else (ROOT / name).read_bytes())
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Approved reference changed: {name}")
        approved = pd.read_csv(StringIO(data.decode("utf-8")), dtype=str)
        current = pd.read_csv(ROOT / name, dtype=str)
        keep = [c for c in approved.columns if c not in ["fit_seconds", "predict_seconds"]]
        assert approved[keep].shape == current[keep].shape
        for column in keep:
            try:
                a = pd.to_numeric(approved[column])
                b = pd.to_numeric(current[column])
            except ValueError:
                np.testing.assert_array_equal(approved[column], current[column])
            else:
                np.testing.assert_allclose(a, b, atol=1e-12, rtol=1e-12)
        verified[name] = data
    table = pd.read_csv(StringIO(verified["outputs/ch12/exercise_12_2/predictions.csv"].decode("utf-8")),
                        dtype={"true": str, "knn": str, "cnn": str})
    np.testing.assert_array_equal(table["case"], np.arange(len(y_test)))
    np.testing.assert_array_equal(table.true, y_test)
    return table, reference


def interval_statistics(values):
    """Population std and OLS slope per sample index, not per physical second."""
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or len(values) < 3 or not np.isfinite(values).all():
        raise ValueError("Finite interval with at least three samples required")
    t = np.arange(len(values), dtype=float)
    centered = t - t.mean()
    return np.array([values.mean(), values.std(ddof=0),
                     centered @ (values - values.mean()) / (centered @ centered)])


def first_interval(model, prepared_train):
    """Inspect actual first sampled interval, not an invented illustrative feature."""
    records = model.intervals_[0][0].intervals_[:3]
    start, end, channel, _, dilation = records[0]
    values = prepared_train[0, channel, start:end:dilation]
    manual = interval_statistics(values)
    actual = np.array([record[3](values[None, :])[0] for record in records])
    np.testing.assert_allclose(manual, actual, atol=1e-6, rtol=1e-6)
    return dict(start=int(start), end_exclusive=int(end), channel=int(channel),
                dilation=int(dilation), mean=float(manual[0]), std=float(manual[1]),
                slope=float(manual[2]))
