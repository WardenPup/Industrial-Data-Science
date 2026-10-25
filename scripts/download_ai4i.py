"""Fetch the official UCI archive, verify its CSV, and preserve raw bytes."""

import hashlib
import io
from pathlib import Path
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from sessions.ch10.ai4i_data import DATA_PATH, DATA_URL, SHA256, verify_file


def main():
    if DATA_PATH.exists():
        verify_file()
        print("PASS: existing official AI4I CSV checksum verified; no download needed")
        return
    with urllib.request.urlopen(DATA_URL, timeout=60) as response:
        archive_bytes = response.read()
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        csv_bytes = archive.read("ai4i2020.csv")
    if hashlib.sha256(csv_bytes).hexdigest() != SHA256:
        raise ValueError("Downloaded CSV differs from the documented source snapshot")
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create avoids replacing data created concurrently by another process.
    with DATA_PATH.open("xb") as target:
        target.write(csv_bytes)
    print(f"PASS: official AI4I CSV downloaded, {len(csv_bytes)} bytes; SHA256 verified")


if __name__ == "__main__":
    main()
