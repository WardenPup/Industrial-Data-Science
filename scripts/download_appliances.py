"""Explicit acquisition of the checksum-pinned official regression splits."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
def main():
    source=json.loads((ROOT/'sessions/ch12/appliances_source.json').read_text())
    dest=ROOT/'data/raw/AppliancesEnergy';dest.mkdir(parents=True,exist_ok=True)
    for name,expected in source['files'].items():
        path=dest/name
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('Existing raw file changed: '+name)
            continue
        with urlopen(source['urls'][name],timeout=90) as response:data=response.read()
        if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Source checksum mismatch')
        temp=dest/(name+'.tmp');temp.write_bytes(data);temp.replace(path)
    print('PASS: original AppliancesEnergy TRAIN/TEST SHA256 verified')
if __name__=='__main__':main()
