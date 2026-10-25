"""Execute a synthetic notebook and export HTML/PDF; no Exercise 10.2 data."""

import os
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".tools/playwright"))
os.environ.setdefault("JUPYTER_CONFIG_DIR", str(ROOT / ".jupyter"))
os.environ.setdefault("JUPYTER_DATA_DIR", str(ROOT / ".local/share/jupyter"))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(ROOT / ".local/share/jupyter/runtime"))
os.environ.setdefault("IPYTHONDIR", str(ROOT / ".local/ipython"))

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter, WebPDFExporter
from pypdf import PdfReader


def main():
    output = ROOT / "outputs/tooling-smoke"
    output.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(
                "# Notebook tooling check\nSynthetic environment check, not Exercise 10.2."
            ),
            nbformat.v4.new_code_cell("value = 2 + 2\nassert value == 4\nprint(value)"),
        ],
        metadata={"kernelspec": {"display_name": "Python 3 (project)",
                                 "language": "python", "name": "python3"}},
    )
    client = NotebookClient(notebook, timeout=60, kernel_name="python3")
    if sys.platform == "win32":
        # ZMQ needs add_reader; keep the browser's default Proactor loop unchanged.
        with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
            runner.run(client.async_execute())
    else:
        client.execute()
    assert notebook.cells[1].outputs[0].text.strip() == "4"
    nbformat.write(notebook, output / "tooling_check.ipynb")
    html, _ = HTMLExporter().from_notebook_node(notebook)
    assert "Notebook tooling check" in html
    (output / "tooling_check.html").write_text(html, encoding="utf-8")
    pdf, _ = WebPDFExporter().from_notebook_node(notebook)
    pdf_path = output / "tooling_check.pdf"
    pdf_path.write_bytes(pdf)
    reader = PdfReader(pdf_path)
    assert len(reader.pages) >= 1
    assert "Notebook tooling check" in "".join(p.extract_text() for p in reader.pages)
    print(f"PASS: kernel executed; HTML exported; PDF readable ({len(reader.pages)} page(s)).")
    print(output)


if __name__ == "__main__":
    main()
