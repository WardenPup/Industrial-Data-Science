"""Execute all 10.3 analyses and verify the required HTML/image outputs."""

import asyncio
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
for name, relative in {
    "JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter",
    "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython",
    "MPLCONFIGDIR": ".tools/matplotlib",
}.items():
    os.environ.setdefault(name, str(ROOT / relative))

import nbformat
from bs4 import BeautifulSoup
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from PIL import Image, ImageStat
from scripts.validate_notebooks import validate_notebook
from sessions.ch10.ai4i_data import load_ai4i
from sessions.ch10.ai4i_eda import PLOTS


def main():
    load_ai4i()
    source = ROOT / "sessions/ch10/ai4i_seaborn.ipynb"
    notebook = nbformat.read(source, as_version=4)
    validate_notebook(notebook)
    client = NotebookClient(notebook, timeout=240, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    if sys.platform == "win32":
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    validate_notebook(notebook)
    code = [c for c in notebook.cells if c.cell_type == "code"]
    assert [c.execution_count for c in code] == list(range(1, len(code) + 1))
    images = [o for c in code for o in c.outputs if "image/png" in o.get("data", {})]
    assert len(images) == len(PLOTS)
    output = ROOT / "outputs/ch10/exercise_10_3"
    manifest = []
    for name in PLOTS:
        path = output / f"{name}.png"
        with Image.open(path) as im:
            assert min(im.size) >= 500
            assert max(ImageStat.Stat(im.convert("RGB")).stddev) > 10
            manifest.append({"file": path.name, "width": im.width, "height": im.height,
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    (output / "plot_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    nbformat.write(notebook, source)
    template = (ROOT / "templates/notebook_export.html.j2").read_text(encoding="utf-8")
    html, _ = HTMLExporter(embed_images=True, raw_template=template).from_notebook_node(notebook)
    page = BeautifulSoup(html, "html.parser")
    embedded = [im for im in page.find_all("img") if im.get("src", "").startswith("data:image/png;base64,")]
    assert len(embedded) == len(PLOTS)
    (output / "ai4i_seaborn.html").write_text(html, encoding="utf-8")
    print(f"PASS: {len(code)} sequential code cells; {len(images)} real plot outputs; 10 embedded HTML figures")
    print("No PDF generated: Exercise 10.3 does not require it.")


if __name__ == "__main__":
    main()
