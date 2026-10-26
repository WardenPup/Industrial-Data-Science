"""Acquire the official Chapter 11 CSV once, verifying before atomic storage."""

import hashlib
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from sessions.ch11.production import DATA, URL, SHA256, load_production


def main():
    if DATA.exists():
        load_production()
        print("PASS: existing official production CSV checksum and schema")
        return
    with urlopen(URL, timeout=60) as response:
        content = response.read()
    if hashlib.sha256(content).hexdigest() != SHA256:
        raise ValueError("Download checksum mismatch; no data written")
    DATA.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA.with_suffix(".csv.part")
    temporary.write_bytes(content)
    temporary.replace(DATA)
    load_production()
    print("PASS: downloaded and verified official production CSV")


if __name__ == "__main__":
    main()
