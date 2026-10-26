"""Explicit, checksum-pinned acquisition of only the required original .ts files."""
import hashlib,json
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]

def main():
    source=json.loads((ROOT/"sessions/ch12/uwave_source.json").read_text())
    destination=ROOT/"data/raw/UWaveGestureLibrary";destination.mkdir(parents=True,exist_ok=True)
    if all((destination/n).exists() and hashlib.sha256((destination/n).read_bytes()).hexdigest()==h for n,h in source["files"].items()):
        print("PASS: existing UWaveGestureLibrary checksums");return
    with urlopen(source["url"],timeout=120) as response: data=response.read()
    with ZipFile(BytesIO(data)) as archive:
        for name,expected in source["files"].items():
            matches=[p for p in archive.namelist() if p.split("/")[-1]==name]
            assert len(matches)==1
            content=archive.read(matches[0]);assert hashlib.sha256(content).hexdigest()==expected
            temp=destination/(name+".tmp");temp.write_bytes(content);temp.replace(destination/name)
    print("PASS: original variable-length UWaveGestureLibrary splits downloaded and SHA256 verified")

if __name__=="__main__":main()
