"""Execute Exercise 10.2 in a fresh kernel and export its actual outputs."""

import asyncio
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for name, relative in {
    "JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter",
    "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython",
    "MPLCONFIGDIR": ".tools/matplotlib", "PLAYWRIGHT_BROWSERS_PATH": ".tools/playwright",
}.items():
    os.environ.setdefault(name, str(ROOT / relative))
sys.path.insert(0, str(ROOT))

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter, WebPDFExporter
from pypdf import PdfReader
from sessions.ch10.ai4i_data import load_ai4i
from scripts.validate_notebooks import validate_notebook


def main():
    load_ai4i()  # Fail early on missing/changed source data.
    source = ROOT / "sessions/ch10/ai4i_explore.ipynb"
    notebook = nbformat.read(source, as_version=4)
    validate_notebook(notebook)
    client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    if sys.platform == "win32":
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    validate_notebook(notebook)
    counts = [c.execution_count for c in notebook.cells if c.cell_type == "code"]
    assert counts == list(range(1, len(counts) + 1))
    assert {c.cell_type for c in notebook.cells} == {"code", "markdown", "raw"}
    images = [o for c in notebook.cells if c.cell_type == "code" for o in c.outputs
              if "image/png" in o.get("data", {})]
    assert len(images) == 1, "The actual plot must be embedded in a notebook output"
    nbformat.write(notebook, source)
    output = ROOT / "outputs/ch10/exercise_10_2"
    output.mkdir(parents=True, exist_ok=True)
    template = (ROOT / "templates/notebook_export.html.j2").read_text(encoding="utf-8")
    html, _ = HTMLExporter(embed_images=True, raw_template=template).from_notebook_node(notebook)
    assert "data:image/png;base64," in html and "Rotational speed" in html
    (output / "ai4i_explore.html").write_text(html, encoding="utf-8")
    pdf, _ = WebPDFExporter(raw_template=template).from_notebook_node(notebook)
    pdf_path = output / "ai4i_explore.pdf"
    pdf_path.write_bytes(pdf)
    reader = PdfReader(pdf_path)
    text = " ".join(page.extract_text() for page in reader.pages)
    assert "Torque" in text and "Rotational speed" in text and "Grundstatistik" in text
    assert sum(len(page.images) for page in reader.pages) >= 1, "PDF must include the plot image"
    assert all("error" != o.output_type for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
    print(f"PASS: {len(counts)} code cells executed in order; HTML with embedded image; PDF {len(reader.pages)} pages")
    print(output)


if __name__ == "__main__":
    main()
