"""Render the scientific draft and notebook companion using Quarto + LuaLaTeX."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'reports/exercise_10_4'
OUTPUT = ROOT / 'outputs/ch10/exercise_10_4'


def main():
    local = ROOT / '.tools/quarto/bin/quarto.exe'
    quarto = str(local) if local.exists() else shutil.which('quarto')
    if not quarto:
        raise RuntimeError('Install Quarto 1.10.19; see reports/exercise_10_4/README.md')
    env = os.environ.copy()
    env.update({
        'QUARTO_PYTHON': sys.executable,
        'PYTHONPATH': str(ROOT),
        'MPLCONFIGDIR': str(ROOT / '.tools/matplotlib'),
        'JUPYTER_CONFIG_DIR': str(ROOT / '.jupyter'),
        'JUPYTER_DATA_DIR': str(ROOT / '.local/share/jupyter'),
        'JUPYTER_RUNTIME_DIR': str(ROOT / '.local/share/jupyter/runtime'),
        'IPYTHONDIR': str(ROOT / '.local/ipython'),
    })
    version = subprocess.check_output([quarto, '--version'], text=True, env=env).strip()
    if version != '1.10.19':
        raise RuntimeError(f'Expected Quarto 1.10.19; found {version}')
    sources = [PROJECT / 'paper.qmd', PROJECT / 'notebook_presentation.ipynb']
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for source in sources:
        for fmt in ['html', 'pdf']:
            subprocess.run([quarto, 'render', str(source), '--to', fmt, '--execute'],
                           cwd=ROOT, env=env, check=True)
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
    manifest = {'quarto': version, 'python': sys.version.split()[0],
                'engine': 'lualatex', 'source_sha256': before, 'exports': []}
    for stem, image_count in [('paper', 3), ('notebook_presentation', 10)]:
        html_path, pdf_path = OUTPUT / f'{stem}.html', OUTPUT / f'{stem}.pdf'
        page = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
        images = [im for im in page.find_all('img') if im.get('src', '').startswith('data:image/')]
        assert len(images) == image_count, (stem, len(images))
        assert not page.select('.citation.unresolved')
        if stem == 'paper':
            assert len(page.select('details.code-fold')) >= 1
            assert len(page.select('math')) >= 2
            assert len(page.select('#refs .csl-entry')) == 4
        reader = PdfReader(pdf_path)
        text = '\n'.join(p.extract_text() for p in reader.pages)
        assert 'AWAITING HUMAN REVIEW' in text
        assert 'Drehmoment' in text and len(text) > 3000
        # Actual PDF figure XObjects (not only references to image filenames).
        image_total = sum(len(list(p.images)) for p in reader.pages)
        assert image_total >= image_count, (stem, image_total)
        for path in [html_path, pdf_path]:
            manifest['exports'].append({'file': path.name, 'bytes': path.stat().st_size,
                                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        print(f'PASS {stem}: {image_count} embedded HTML figures; {len(reader.pages)} PDF pages; {image_total} PDF images')
    (OUTPUT / 'validation_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('PASS: four Quarto exports; source files unchanged; visual inspection still required')


if __name__ == '__main__':
    main()
