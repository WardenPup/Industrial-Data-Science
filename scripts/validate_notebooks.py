"""Validate tracked notebooks and execute fresh copies; never overwrite sources."""

import asyncio
import os
from pathlib import Path
import subprocess
import sys

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def validate_notebook(notebook):
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code" and any(o.output_type == "error" for o in cell.outputs):
            raise ValueError("notebook contains a saved error output")


def main():
    for name, path in {
        "JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter",
        "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython",
        "MPLCONFIGDIR": ".tools/matplotlib",
    }.items():
        os.environ.setdefault(name, str(ROOT / path))
    paths = subprocess.check_output(["git", "ls-files", "-z", "--", "*.ipynb"], cwd=ROOT).decode().split("\0")
    paths = [p for p in paths if p]
    if not paths:
        print("SKIP: no tracked notebooks. Synthetic execution/export check is separate.")
        return
    for relative in paths:
        notebook = nbformat.read(ROOT / relative, as_version=4)
        validate_notebook(notebook)
        client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        if sys.platform == "win32":
            with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
                runner.run(client.async_execute())
        else:
            client.execute()
        validate_notebook(notebook)
        counts = [cell.execution_count for cell in notebook.cells
                  if cell.cell_type == "code" and cell.source.strip()]
        if counts != list(range(1, len(counts) + 1)):
            raise ValueError(f"nonsequential execution counts in {relative}: {counts}")
        output = ROOT / "outputs/tooling-smoke/notebooks" / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, output)
        print(f"PASS: validated and executed {relative}")


if __name__ == "__main__":
    main()
