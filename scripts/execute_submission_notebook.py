"""Execute an extracted notebook in a fresh project kernel without changing its source."""
import asyncio
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient

source = Path(sys.argv[1]).resolve()
notebook = nbformat.read(source, 4)
client = NotebookClient(notebook, timeout=900, kernel_name="python3", resources={"metadata": {"path": str(Path.cwd())}})
if sys.platform == "win32":
    with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
        runner.run(client.async_execute())
else:
    client.execute()
counts = [c.execution_count for c in notebook.cells if c.cell_type == "code"]
assert counts == list(range(1, len(counts)+1))
assert not any(o.output_type == "error" for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
output = Path.cwd() / ".tools/fresh_notebook.ipynb"
output.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(notebook, output)
print(f"PASS: {len(counts)} fresh sequential code cells; original notebook unchanged")
