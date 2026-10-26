"""Build four Chapter 10 upload ZIPs from a merged Git snapshot; never upload."""

import argparse
import asyncio
import base64
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
if ROOT.name == '.tools':
    ROOT = ROOT.parent
OUTPUT = ROOT / 'submission/chapter_10'
QA = ROOT / '.tools/chapter10_submission_qa'
DATA_SHA = 'dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e'
COURSE = 'https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html'
COMMON = ['pyproject.toml', 'uv.lock', 'uv.toml', '.python-version', 'scripts/uv.cmd']
INITIALIZERS = ['sessions/__init__.py', 'sessions/ch10/__init__.py']


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def readme(number, revision):
    payload = {
        1: 'Python-Skript und deutsche Herleitung unter `sessions/ch10/`; fertige Herzkurve unter `outputs/ch10/aufgabe_10_1_herz.png`. Keine externen Daten und kein Notebook erforderlich.',
        2: 'Notebook `sessions/ch10/ai4i_explore.ipynb`; gleichnamige HTML- und PDF-Exporte, Drehmomentgrafik und Grundstatistik unter `outputs/ch10/exercise_10_2/`.',
        3: 'Notebook `sessions/ch10/ai4i_seaborn.ipynb`; gleichnamiger HTML-Export, zehn Diagrammgruppen und berechnete CSV-/JSON-Tabellen unter `outputs/ch10/exercise_10_3/`. Aufgabe 10.3 verlangt keinen PDF-Export.',
        4: 'Editierbarer Bericht `reports/exercise_10_4/paper.qmd` und Begleitnotebook `reports/exercise_10_4/notebook_presentation.ipynb`, Quarto-Konfiguration, Quellen und Stile. HTML/PDF beider Dokumente, Figuren, Tabellen, Validierungsmanifest und TeX-Paketrevisionen liegen unter `outputs/ch10/exercise_10_4/`.',
    }[number]
    commands = ['uv sync --locked']
    if number == 1:
        commands += ['uv run --locked python sessions/ch10/aufgabe_10_1.py']
    else:
        if number == 2:
            commands += ['$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD/.tools/playwright"',
                         'uv run --locked playwright install chromium']
        commands += [f'uv run --locked python scripts/build_exercise_10_{number}.py']
    text = f'''# Aufgabe 10.{number} – Abgabepaket

Quellstand: `{revision}` (gemergtes Kapitel 10).
Aufgabenquelle: {COURSE}, gelesen am 26.10.2026.

Dieses ZIP ist die einzelne Abgabedatei für Aufgabe 10.{number}. Nach dem Entpacken
in den Paketstamm `exercise_10_{number}` wechseln. Die ursprünglichen relativen
Projektpfade sind erhalten. {payload}

## Reproduktion

Voraussetzung: uv (geprüft: 0.13.5) und Python 3.12; die genaue Python-Version
steht in `.python-version`. Abhängigkeiten ausschließlich projektlokal über
`uv sync --locked` aus dem beigefügten Lockfile installieren. Keine globalen
Python-Pakete erforderlich. Die ersten Paket-/Werkzeugdownloads benötigen Internet.
Windows/PowerShell, aus dem entpackten Paketstamm:

```powershell
'''+ '\n'.join(commands) + '''
```

Die Python-Aufrufe gelten auch unter Linux/macOS. Umgebungsvariablen dort mit
`export` setzen. `scripts/uv.cmd` ist ein Windows-Wrapper für installiertes uv;
es werden keine uv-/Python-Binärwerkzeuge oder virtuellen Umgebungen mitgeliefert.
'''
    if number in (2, 3):
        text += '''
Die unmittelbar benötigten Exportskripte und die ursprüngliche HTML-Vorlage
sind beigefügt. `scripts/validate_notebooks.py` stellt deren importierte
Notebook-Prüffunktion bereit; das Hilfsmodul nicht separat starten.
Das Notebook enthält ausgeführte Outputs und seinen fertigen HTML-Export.
'''
    if number == 4:
        text += '''
Zusätzlich Quarto 1.10.19 und LuaLaTeX (TeX Live 2026, LuaHBTeX 1.24.0) mit den
dokumentierten Paketen installieren. Quarto muss als `quarto` im PATH erreichbar
sein. Der Builder rendert unter `reports/exercise_10_4/_rendered/` und kopiert
fertige Exporte nach `outputs/ch10/exercise_10_4/`. Beide Quellen werden frisch
ausgeführt. Das Notebook enthält ausgeführte Outputs und seinen HTML-/PDF-Export.
TeX-Pakete sind dokumentiert, aber nicht hermetisch gesperrt; bitidentische neu
erzeugte PDFs auf beliebigen Rechnern werden nicht behauptet.
'''
    text += '''
## Transparenz

Codex unterstützte Entwicklung, Dokumentation, Aufbereitung und technische QA.
Studentische fachliche Reviews und ausdrückliche Freigaben sind im erhaltenen
Projektverlauf dokumentiert. Eine unabhängige studentische Testausführung oder
alleinige studentische Codeautorschaft wird nicht behauptet. Das Paket ist lokal
vorbereitet und noch nicht an die Hochschule übermittelt. Interne GitHub-/Commit-
und Werkzeugtests sind ausgeschlossen; beigefügte Skripte dienen unmittelbar
der Ausführung beziehungsweise Reproduktion der Lösung.
'''
    if number > 1:
        text += f'''
## Datenquelle, Lizenz und Grenzen

AI4I 2020 Predictive Maintenance Dataset [Dataset]. (2020).
UCI Machine Learning Repository. https://doi.org/10.24432/C5HS5C .
https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
Lizenz: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ .
Offizielle Quellen-/Lizenzangaben erneut geprüft am 26.10.2026.
`data/raw/ai4i2020.csv` ist die unveränderte Originaldatei, 522048 Bytes,
SHA256 `{DATA_SHA}`. Herkunft zusätzlich in `data/raw/README.md`.
Die Analyse nutzt die beigefügten verifizierten Daten ohne weiteren Datendownload.
Die Daten sind synthetisch; UDI ist keine Zeitvariable, Korrelation keine
Kausalität, IQR-Markierungen sind keine bewiesenen Mess- oder Maschinenfehler.
'''
    return text.encode('utf-8')


def select_paths(number, tracked):
    files = set(COMMON)
    if number == 1:
        files.update(['sessions/ch10/aufgabe_10_1.py', 'sessions/ch10/aufgabe_10_1.md',
                      'outputs/ch10/aufgabe_10_1_herz.png'])
    else:
        files.update(INITIALIZERS + ['sessions/ch10/ai4i_data.py', 'data/raw/README.md'])
        if number >= 3:
            files.add('sessions/ch10/ai4i_eda.py')
        if number in (2, 3):
            files.update([f'scripts/build_exercise_10_{number}.py', 'scripts/validate_notebooks.py',
                          'templates/notebook_export.html.j2'])
            files.add('sessions/ch10/ai4i_explore.ipynb' if number == 2 else 'sessions/ch10/ai4i_seaborn.ipynb')
        else:
            files.update(['sessions/ch10/report_10_4.py', 'scripts/build_exercise_10_4.py'])
            files.update(['reports/exercise_10_4/'+n for n in
                          ['paper.qmd', 'notebook_presentation.ipynb', '_quarto.yml',
                           'references.bib', 'styles.css']])
        prefix = f'outputs/ch10/exercise_10_{number}/'
        files.update(p for p in tracked if p.startswith(prefix) and Path(p).suffix in
                     {'.html', '.pdf', '.png', '.csv', '.json', '.tsv'})
    assert files <= set(tracked), sorted(files - set(tracked))
    return sorted(files)


def check_archive(path, entries):
    import nbformat
    from PIL import Image, ImageStat
    from pypdf import PdfReader
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names)) == len(entries)
        for entry in entries:
            name = entry['path']
            pure = PurePosixPath(name)
            assert not pure.is_absolute() and '..' not in pure.parts and ':' not in name
            assert not any(x in pure.parts for x in ['.git', '.venv', '__pycache__', '.tools'])
            assert pure.suffix not in {'.exe', '.dll', '.log', '.tmp', '.pyc', '.tex', '.zip'}
            data = archive.read(name)
            assert digest(data) == entry['sha256']
            if name.endswith('.ipynb'):
                notebook = nbformat.reads(data.decode('utf-8'), 4)
                nbformat.validate(notebook)
                code = [c for c in notebook.cells if c.cell_type == 'code']
                assert [c.execution_count for c in code] == list(range(1, len(code)+1))
                assert not any(o.output_type == 'error' for c in code for o in c.outputs)
                assert any(n.endswith('/'+pure.stem+'.html') for n in names)
                for c in code:
                    for o in c.outputs:
                        if 'image/png' in o.get('data', {}):
                            with Image.open(BytesIO(base64.b64decode(o.data['image/png']))) as im:
                                im.verify()
            if name.endswith('.png'):
                with Image.open(BytesIO(data)) as im:
                    assert min(im.size) > 100
                    assert max(ImageStat.Stat(im.convert('RGB')).stddev) > 0
            if name.endswith('.pdf'):
                reader = PdfReader(BytesIO(data))
                assert len(reader.pages) > 0
                assert all(p.extract_text().strip() for p in reader.pages)
            if name.endswith('ai4i2020.csv'):
                assert digest(data) == DATA_SHA


def runtime_check(archives):
    import nbformat
    from nbclient import NotebookClient
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader
    QA.mkdir(parents=True, exist_ok=True)
    for name, relative in {'JUPYTER_CONFIG_DIR': '.jupyter', 'JUPYTER_DATA_DIR': '.local/share/jupyter',
                           'JUPYTER_RUNTIME_DIR': '.local/share/jupyter/runtime',
                           'IPYTHONDIR': '.local/ipython', 'MPLCONFIGDIR': '.tools/matplotlib',
                           'PLAYWRIGHT_BROWSERS_PATH': '.tools/playwright'}.items():
        os.environ[name] = str(ROOT / relative)
    checks = []
    for item in archives:
        with zipfile.ZipFile(OUTPUT/item['file']) as archive:
            archive.extractall(QA)
        package = QA / item['root']
        if item['exercise'] != '10.1':
            probe = ('from pathlib import Path; import sys; sys.path.insert(0, '+repr(str(package))+
                     '); from sessions.ch10.ai4i_data import ROOT, load_ai4i; '
                     'assert ROOT.resolve()==Path.cwd().resolve(); assert load_ai4i().shape==(10000,4)')
            subprocess.run([sys.executable, '-I', '-c', probe], cwd=package, check=True)
        for path in sorted(package.rglob('*.ipynb')):
            nb = nbformat.read(path, 4)
            client = NotebookClient(nb, timeout=240, kernel_name='python3',
                                    resources={'metadata': {'path': str(package)}})
            if sys.platform == 'win32':
                with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
                    runner.run(client.async_execute())
            else:
                client.execute()
            assert not any(o.output_type == 'error' for c in nb.cells if c.cell_type == 'code' for o in c.outputs)
            checks.append({'exercise': item['exercise'], 'notebook': path.relative_to(package).as_posix(),
                           'executed_cells': sum(c.cell_type == 'code' for c in nb.cells), 'result': 'PASS'})
        if item['exercise'] == '10.1':
            subprocess.run([sys.executable, 'sessions/ch10/aufgabe_10_1.py', '--output',
                            str(QA/'executed_heart.png')], cwd=package, check=True, capture_output=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for item in archives:
            package = QA / item['root']
            for path in sorted(package.rglob('*.html')):
                page = browser.new_page(viewport={'width': 1400, 'height': 1100})
                page.route('https://**/*', lambda route: route.abort())
                page.route('http://**/*', lambda route: route.abort())
                page.goto(path.as_uri(), wait_until='load')
                assert page.evaluate('''() => [...document.images].every(i => i.complete && i.naturalWidth > 0)''')
                expected = 3 if path.stem == 'paper' else (1 if path.stem == 'ai4i_explore' else 10)
                assert page.locator('img').count() == expected
                assert page.locator('.citation.unresolved').count() == 0
                page.screenshot(path=str(QA/f"{item['root']}-{path.stem}.png"))
                page.close()
                checks.append({'exercise': item['exercise'], 'html': path.relative_to(package).as_posix(),
                               'decoded_images': expected, 'offline': True, 'result': 'PASS'})
            for path in sorted(package.rglob('*.pdf')):
                prefix = QA/f"{item['root']}-{path.stem}-page"
                subprocess.run(['pdftoppm', '-scale-to', '1100', '-png', str(path), str(prefix)], check=True)
                checks.append({'exercise': item['exercise'], 'pdf': path.relative_to(package).as_posix(),
                               'pages': len(PdfReader(path).pages), 'rendered_all_pages': True, 'result': 'PASS'})
            print(f"PASS archive runtime/offline previews: {item['exercise']}", flush=True)
        browser.close()
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-ref', default='HEAD')
    args = parser.parse_args()
    assert git('branch', '--show-current').decode().strip() == 'main', 'Run only after ordered merges on main'
    revision = git('rev-parse', args.source_ref).decode().strip()
    for number in range(1, 5):
        assert 'Status: APPROVED' in git('show', f'{revision}:reviews/exercise_10_{number}.md').decode() or \
               'Status: **APPROVED**' in git('show', f'{revision}:reviews/exercise_10_{number}.md').decode()
    epoch = int(git('show', '-s', '--format=%ct', revision).decode())
    stamp = datetime.fromtimestamp(epoch, timezone.utc).timetuple()[:6]
    tracked = git('ls-tree', '-r', '--name-only', revision).decode().splitlines()
    raw = (ROOT/'data/raw/ai4i2020.csv').read_bytes()
    assert digest(raw) == DATA_SHA and len(raw) == 522048
    OUTPUT.mkdir(parents=True, exist_ok=True)
    archives = []
    for number in range(1, 5):
        folder = f'exercise_10_{number}'
        filename = f'Industrial_Data_Science_Exercise_10_{number}.zip'
        files = {p: git('show', f'{revision}:{p}') for p in select_paths(number, tracked)}
        files['README_ABGABE.md'] = readme(number, revision)
        if number > 1:
            files['data/raw/ai4i2020.csv'] = raw
        entries = []
        with zipfile.ZipFile(OUTPUT/filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(files.items()):
                target = f'{folder}/{name}'
                info = zipfile.ZipInfo(target, stamp)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
                entries.append({'path': target, 'bytes': len(data), 'sha256': digest(data)})
        check_archive(OUTPUT/filename, entries)
        archives.append({'exercise': f'10.{number}', 'file': filename, 'root': folder,
                         'bytes': (OUTPUT/filename).stat().st_size,
                         'sha256': digest((OUTPUT/filename).read_bytes()), 'entries': entries})
    checks = runtime_check(archives)
    manifest = {'source_commit': revision, 'prepared_date': '2026-10-26',
                'uploaded': False, 'submission_authorized': False,
                'rules': 'User-supplied university rules: one file per exercise; ZIP for multiple files; HTML for every notebook; PDF where required.',
                'official_assignment': COURSE, 'source_retrieved': '2026-10-26',
                'qa_actor': 'Codex', 'runtime_python': sys.version.split()[0],
                'packages': archives, 'checks': checks}
    (OUTPUT/'submission_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    lines = ['# Kapitel 10 – geprüfte Abgabedateien', '', f'Quellcommit: `{revision}`.',
             'Erstellt und technisch geprüft: 26.10.2026 durch Codex.',
             '**Noch nicht hochgeladen. Universitätseinreichung nicht autorisiert.**', '',
             'Es sind ausschließlich die folgenden vier ZIP-Dateien für die vier Aufgaben vorgesehen.',
             'Checkliste und Manifest sind lokale Begleitnachweise, keine zusätzlichen Abgabedateien.', '',
             '- [x] Aufgaben 10.1–10.4 enthalten fachlich freigegebene Lösungen aus main.',
             '- [x] Genau eine ZIP-Datei pro Aufgabe; CRC, sichere Pfade und vollständige Inhaltslisten geprüft.',
             '- [x] Jedes Notebook enthält reale Outputs und besitzt einen HTML-Export.',
             '- [x] Erforderliche PDF-Exporte: 10.2 sowie beide Dokumente von 10.4.',
             '- [x] Rohdaten unverändert, CC-BY-4.0-Quelle und SHA256 dokumentiert.',
             '- [x] pyproject.toml, uv.lock und Python-Version für Reproduktion enthalten.',
             '- [x] Keine Umgebungen, Caches, Git-Metadaten, Binärwerkzeuge oder unnötigen internen Entwicklungsskripte enthalten; Reproduktionsskripte sind direkt relevant.',
             '- [x] Alle drei entpackten Notebooks frisch ausgeführt; Herzskript separat ausgeführt.',
             '- [x] Vier HTML-Dateien offline geöffnet, 1/10/3/10 Bilder dekodiert.',
             '- [x] Alle drei PDFs vollständig geöffnet und mit Poppler nach PNG gerendert.',
             '- [ ] Ausdrückliche Genehmigung zum tatsächlichen Upload erhalten.', '',
             'Die öffentlich zugänglichen Aufgaben-/Einführungsseiten enthalten keine zusätzlichen Portal-',
             'Abgaberegeln. Die im Nutzerauftrag genannten Hochschulregeln wurden angewendet.',
             'Dateigrößenlimits, Fristen und zusätzliche Namensvorgaben wurden nicht bereitgestellt.',
             'TeX ist nicht hermetisch gesperrt; lokaler Jupyter-TCP-Hinweis bleibt bekannt.', '']
    for item in archives:
        lines += [f"## {item['exercise']} – {item['file']}", '',
                  f"{item['bytes']} Bytes; SHA256 `{item['sha256']}`.", '', '```text']
        lines += [entry['path'] for entry in item['entries']]
        lines += ['```', '']
    (OUTPUT/'CHECKLIST.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'source_commit': revision, 'archives': [{k:v for k,v in a.items() if k != 'entries'} for a in archives],
                      'runtime_checks': len(checks), 'uploaded': False}, indent=2))


if __name__ == '__main__':
    main()
