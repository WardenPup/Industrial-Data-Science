"""Render the scientific draft and notebook companion using Quarto + LuaLaTeX."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import nbformat

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
    paper_hash = hashlib.sha256(sources[0].read_bytes()).hexdigest()
    notebook_cells = [(c.cell_type, c.source) for c in nbformat.read(sources[1], as_version=4).cells]
    for source in sources:
        for fmt in ['html', 'pdf']:
            subprocess.run([quarto, 'render', str(source), '--to', fmt, '--execute'],
                           cwd=ROOT, env=env, check=True)
            OUTPUT.mkdir(parents=True, exist_ok=True)
            # Replace the finished file atomically: an open PDF viewer can hold
            # a memory mapping that prevents CopyFile2 overwriting it in place.
            target = OUTPUT / f'{source.stem}.{fmt}'
            temporary = target.with_suffix(target.suffix + '.tmp')
            shutil.copy2(PROJECT / '_rendered' / target.name, temporary)
            temporary.replace(target)
    assert paper_hash == hashlib.sha256(sources[0].read_bytes()).hexdigest()
    # Quarto --execute intentionally persists real outputs in this presentation
    # copy. Its source cells, and the original 10.3 notebook, must stay intact.
    notebook = nbformat.read(sources[1], as_version=4)
    assert notebook_cells == [(c.cell_type, c.source) for c in notebook.cells]
    code = [c for c in notebook.cells if c.cell_type == 'code']
    assert [c.execution_count for c in code] == list(range(1, len(code) + 1))
    assert not any(o.output_type == 'error' for c in code for o in c.outputs)
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
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
        producer = str(reader.metadata.producer)
        assert 'LuaTeX' in producer, producer
        text = ' '.join(' '.join(p.extract_text() for p in reader.pages).split())
        # PDF extraction may insert spaces between strongly kerned capital letters.
        assert 'AWAITINGFINALHUMANAPPROVAL' in ''.join(text.split())
        assert 'Drehmoment' in text and len(text) > 3000
        # QMD plots can be vector PDF graphics, so raster XObjects alone do not
        # count figures. Check generated LaTeX inclusions and captions as well.
        image_total = sum(len(list(p.images)) for p in reader.pages)
        tex = (PROJECT / f'{stem}.tex').read_text(encoding='utf-8')
        assert tex.count('\\includegraphics') == image_count
        if stem == 'paper':
            assert all(f'Abbildung {i}' in text for i in range(1, 4))
        else:
            assert image_total >= image_count, (stem, image_total)
            for heading in ['6. Paarweise Beziehungen', '7. Pearson-', '8. Jointplot']:
                matching = [p for p in reader.pages if heading in p.extract_text()]
                assert len(matching) == 1 and len(list(matching[0].images)) >= 1, heading
            assert 'Spearman-Rangkorrelation' in text
            assert 'Pearson-Heatmap' in text
        for path in [html_path, pdf_path]:
            entry = {'file': path.name, 'bytes': path.stat().st_size,
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            if path.suffix == '.pdf':
                entry.update({'pages': len(reader.pages), 'producer': producer})
            manifest['exports'].append(entry)
        print(f'PASS {stem}: {image_count} embedded HTML figures; {len(reader.pages)} PDF pages; {image_count} LaTeX figure inclusions ({image_total} raster XObjects)')
    (OUTPUT / 'validation_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: four Quarto exports; {len(code)} sequential notebook cells; source text unchanged; visual inspection still required')


if __name__ == '__main__':
    main()
