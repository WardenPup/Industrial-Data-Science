"""Source integrity and schema checks for the official AI4I CSV."""

import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data/raw/ai4i2020.csv"
DATA_URL = "https://archive.ics.uci.edu/static/public/601/ai4i%2B2020%2Bpredictive%2Bmaintenance%2Bdataset.zip"
SHA256 = "dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e"
COLUMNS = ["UDI", "Torque [Nm]", "Rotational speed [rpm]", "Air temperature [K]"]


def verify_file(path: Path = DATA_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError("Run: uv run python scripts/download_ai4i.py")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError("AI4I checksum mismatch; preserve and inspect the file before replacing it")
    return digest


def validate_data(data: pd.DataFrame, expected_rows: int = 10000) -> None:
    if list(data.columns) != COLUMNS or len(data) != expected_rows:
        raise ValueError("Unexpected AI4I columns or row count")
    if data.isna().any().any() or not all(pd.api.types.is_numeric_dtype(data[c]) for c in COLUMNS):
        raise ValueError("AI4I selected columns must be numeric without missing values")
    if not data["UDI"].tolist() == list(range(1, expected_rows + 1)):
        raise ValueError("UDI must be the original unique sequence 1..N")


def load_ai4i(path: Path = DATA_PATH) -> pd.DataFrame:
    verify_file(path)
    data = pd.read_csv(path, usecols=COLUMNS).loc[:, COLUMNS]
    validate_data(data)
    return data
