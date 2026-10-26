"""Prepare Chapter 11 archives from approved main; verify copies by fresh execution."""
from pathlib import Path
import ast,base64,hashlib,json,os,subprocess,sys,zipfile
from io import BytesIO
import nbformat
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'submission/chapter_11'
SNAPSHOT='d117c40d303a2b2d9c47c8bd2a15ff1d8a3d1f3c'
NOTEBOOKS=['production_smoothing','production_imputation','production_stl_imputation','production_outliers']


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def closure(texts):
    modules=set()
    for text in texts:
        for node in ast.walk(ast.parse(text)):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith('sessions.ch11.'):
                modules.add(node.module)
    files=set()
    while modules:
        module=modules.pop();path=Path(*module.split('.')).with_suffix('.py')
        if path in files: continue
        files.add(path)
        text=(ROOT/path).read_text(encoding='utf-8')
        for node in ast.walk(ast.parse(text)):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith('sessions.ch11.'):
                modules.add(node.module)
    return files


def main():
    # Refuse mixed snapshots after later exercises change the environment.
    protected=["sessions/ch11","outputs/ch11","reviews","pyproject.toml","uv.lock",".python-version"]
    if subprocess.check_output(["git","diff",SNAPSHOT,"--",*protected],cwd=ROOT):
        raise RuntimeError("Packaging requires the approved snapshot; use a separate checkout of "+SNAPSHOT)
    DEST.mkdir(parents=True,exist_ok=True)
    records=[]
    for i,name in enumerate(NOTEBOOKS,1):
        nbpath=Path('sessions/ch11')/(name+'.ipynb')
        nb=nbformat.read(ROOT/nbpath,4)
        files={nbpath,Path('scripts')/f'build_exercise_11_{i}.py',Path('templates/notebook_export.html.j2'),
               Path('data/raw/sss1_production_data.csv'),Path('data/raw/PRODUCTION_SOURCE.md'),
               Path('pyproject.toml'),Path('uv.lock'),Path('.python-version'),
               Path(f'docs/EXERCISE_11_{i}_REQUIREMENTS.md'),Path(f'reviews/exercise_11_{i}.md')}
        texts=[c.source for c in nb.cells if c.cell_type=='code']
        texts.append((ROOT/'scripts'/f'build_exercise_11_{i}.py').read_text(encoding='utf-8'))
        files |= closure(texts)
        files.add(Path('sessions/ch11/__init__.py'))
        files |= {p.relative_to(ROOT) for p in (ROOT/f'outputs/ch11/exercise_11_{i}').glob('*') if p.is_file()}
        files |= {p.relative_to(ROOT) for p in (ROOT/'data/processed').glob(f'exercise_11_{i}_*.csv')}
        readme=f'''# Aufgabe 11.{i} – Abgabevorbereitung

Wissenschaftlich freigegebener und integrierter Snapshot: {SNAPSHOT}.
KI-Unterstützung: Codex; unveränderter studentischer Review unter reviews/.
Offizielle Quelle: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
Abruf 26.10.2026. Kein Upload erfolgt. Notebook und Offline-HTML liegen unter
sessions/ch11 und outputs/ch11/exercise_11_{i}. Keine PDF-Pflicht.

## Reproduktion
ZIP in einen eigenen Ordner entpacken. Python und uv sind externe Voraussetzungen;
keine installierten Programme werden mitgeliefert. Im entpackten Projektstamm:

    uv sync --locked
    uv run --locked python scripts/build_exercise_11_{i}.py

Das benötigt zur Erstinstallation Paketnetzwerkzugang. Die anschließende Rechnung
nutzt ausschließlich die beigefügten Rohdaten, keine erneute Datenabfrage.
HTML direkt im Browser öffnen; Bilder sind eingebettet. Die Originaldaten bleiben
unverändert. Datenquelle, SHA256 und tatsächliche Lizenzgrenzen stehen in
 data/raw/PRODUCTION_SOURCE.md (Kursquelle CC BY-NC-SA 4.0, keine separat
bestätigte CSV-Lizenz). Synthetische Daten, keine fehlerfreie Ground Truth.
Parameter, Grenzen und Ergebnisse siehe Notebook; ältere Statusfelder im Review
belegen die Entwicklung, der oben genannte Merge-Snapshot belegt die Integration.
'''
        filename=f'Industrial_Data_Science_Exercise_11_{i}.zip'
        with zipfile.ZipFile(DEST/filename,'w',zipfile.ZIP_DEFLATED) as archive:
            for rel in sorted(files):
                assert not any(part in {'.venv','.git','__pycache__','.tools'} for part in rel.parts)
                archive.write(ROOT/rel,rel.as_posix())
            archive.writestr('README_SUBMISSION.md',readme)
        extracted=ROOT/f'.tools/submission11_verify/11_{i}'
        extracted.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(DEST/filename) as archive:
            assert archive.testzip() is None
            members={x.filename:{'bytes':x.file_size,'sha256':hashlib.sha256(archive.read(x)).hexdigest()} for x in archive.infolist()}
            archive.extractall(extracted)
        # All imports/data are resolved from the extracted package; shared installed env only.
        env=os.environ.copy()
        for var,relative in {'JUPYTER_CONFIG_DIR':'.jupyter','JUPYTER_DATA_DIR':'.local/share/jupyter','JUPYTER_RUNTIME_DIR':'.local/share/jupyter/runtime','IPYTHONDIR':'.local/ipython','MPLCONFIGDIR':'.tools/matplotlib'}.items():
            env[var]=str(extracted/relative);Path(env[var]).mkdir(parents=True,exist_ok=True)
        result=subprocess.run([sys.executable,str(extracted/'scripts'/f'build_exercise_11_{i}.py')],cwd=extracted,env=env,text=True,capture_output=True)
        (ROOT/f'.tools/submission11_verify/11_{i}.log').write_text(result.stdout+result.stderr,encoding='utf-8')
        assert result.returncode==0,result.stderr
        original_summary=json.loads((ROOT/f'outputs/ch11/exercise_11_{i}/summary.json').read_text())
        repeated_summary=json.loads((extracted/f'outputs/ch11/exercise_11_{i}/summary.json').read_text())
        assert original_summary==repeated_summary
        html=extracted/f'outputs/ch11/exercise_11_{i}/{name}.html'
        page=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser')
        images=page.select('img[src^="data:image/png;base64,"]')
        assert len(images)==[2,7,4,2][i-1]
        assert not page.select('img[src^="http"],script[src^="http"],link[href^="http"]')
        for image in images:
            with Image.open(BytesIO(base64.b64decode(image['src'].split(',',1)[1]))) as im: im.verify()
        record={'exercise':f'11.{i}','file':filename,'bytes':(DEST/filename).stat().st_size,'sha256':digest(DEST/filename),
                'members':members,'verification':{'crc':'PASS','extracted_fresh_execution':'PASS','same_summary':'PASS','decoded_html_images':len(images),'environment':'shared project .venv, locked approved environment; no fresh dependency installation claimed'}}
        records.append(record)
        print(f'PASS 11.{i}: {len(members)} archive members; extracted fresh kernel, same summary, {len(images)} decoded HTML images',flush=True)
    manifest={'source_commit':SNAPSHOT,'prepared':'2026-10-26','ai_assistance':'Codex','uploaded':False,'packages':records}
    (DEST/'submission_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DEST/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['file']+'\n' for r in records),encoding='utf-8')
    lines=['# Kapitel 11 – Abgabecheckliste','',f'Freigegebener integrierter Snapshot: `{SNAPSHOT}`. Kein Upload.','',
           'Vier offizielle Aufgaben (11.1–11.4), alle fachlich freigegeben und regulär integriert.',
           'ZIP-CRC, jedes Mitglied, Rohdaten, vollständige Modulabhängigkeiten und Exporte geprüft.',
           'Alle vier Archive tatsächlich entpackt und Notebooks mit dem bestehenden gesperrten Projekt-Environment frisch ausgeführt; Ergebnis-JSON identisch.',
           'Keine neue Installation aus dem Archiv behauptet. Erneuter Aufbau benötigt uv/Python und initial Paketnetzwerkzugang.',
           'Enthaltene Quelldateien und Einzelprüfsummen: submission_manifest.json.','']
    for r in records:
        lines += [f'## {r["exercise"]}: {r["file"]}',f'SHA256: `{r["sha256"]}`','',*[f'- `{p}`' for p in r['members']], '']
    (DEST/'CHECKLIST.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__': main()
