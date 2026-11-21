"""Acquire official public Kaggle version 1 without credentials; verify original CSV."""
import hashlib
import io
from pathlib import Path
import sys
import urllib.request
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sessions.ch15.drilling_data import DATA_PATH,URL,SHA256,verify_file

def main():
    if DATA_PATH.exists():
        verify_file();print("PASS existing original XAI Drilling checksum; no download");return
    with urllib.request.urlopen(URL,timeout=60) as response:archive=response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as z:raw=z.read("XAI_Drilling_Dataset.csv")
    if hashlib.sha256(raw).hexdigest()!=SHA256:raise ValueError("Official version differs from pinned CSV")
    DATA_PATH.parent.mkdir(parents=True,exist_ok=True)
    with DATA_PATH.open("xb") as f:f.write(raw)
    print(f"PASS official public Kaggle version 1; {len(raw)} original bytes; SHA256 verified")
if __name__=="__main__":main()
