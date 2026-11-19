"""Verify extracted final archives without changing approved project artifacts."""
import argparse
import base64
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile

import nbformat
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from pypdf import PdfReader
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "submission/final"
QA = ROOT / ".tools/final_submission_qa"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = Path(name)
    return not p.is_absolute() and ".." not in p.parts and not any(x in {".git", ".venv", "__pycache__", ".tools"} for x in p.parts)


def privacy(name, data):
    if Path(name).suffix not in {".py", ".md", ".html", ".json", ".ipynb", ".toml", ".qmd", ".yml", ".txt", ".ts"}:
        return []
    text = data.decode("utf-8", errors="replace")
    if name.endswith(".html"):
        soup = BeautifulSoup(text, "html.parser")
        for im in soup.select("img[src^='data:']"):
            im["src"] = "embedded image omitted from text scan"
        text = str(soup)
    elif name.endswith(".ipynb"):
        # Binary image strings are not executable credentials or contact text.
        nb = json.loads(text)
        for cell in nb.get("cells", []):
            for out in cell.get("outputs", []):
                for key in list(out.get("data", {})):
                    if key.startswith("image/"):
                        out["data"][key] = "image omitted from text scan"
        text = json.dumps(nb, ensure_ascii=False)
    patterns = {
        "personal_absolute_path": r"[A-Za-z]:[\\/]{1,4}(?:Users|DOCUMENTS)[\\/]",
        "private_key": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        "github_token": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
        "api_key": r"\bsk-[A-Za-z0-9]{24,}",
        "email": r"[A-Za-z0-9._%+-]{1,80}@[A-Za-z0-9.-]{1,100}\.[A-Za-z]{2,12}\b",
    }
    # Only category/count/path in reports; never expose a suspected credential.
    return [{"file": name, "category": k, "count": len(re.findall(p, text))}
            for k, p in patterns.items() if re.search(p, text)]


def archive_check(record):
    path = FINAL / record["file"]
    assert digest(path.read_bytes()) == record["sha256"]
    destination = QA / record["exercise"].replace(".", "_")
    destination.mkdir(parents=True, exist_ok=True)
    findings = []
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist()))
        assert all(safe_name(n) for n in z.namelist())
        contents = json.loads(z.read("PACKAGE_CONTENTS.json"))
        assert set(z.namelist()) == set(contents["files"]) | {"PACKAGE_CONTENTS.json"}
        for name, info in contents["files"].items():
            data = z.read(name)
            assert digest(data) == info["sha256"] and len(data) == info["bytes"]
            findings.extend(privacy(name, data))
        if record["original_archive"]:
            original = ROOT / record["original_archive"]["path"]
            assert digest(original.read_bytes()) == record["original_archive"]["sha256"]
            with zipfile.ZipFile(original) as old:
                assert all(old.read(n) == z.read(n) for n in old.namelist())
                assert set(z.namelist()) - set(old.namelist()) == {"START_HERE.md", "AUTHORSHIP_AND_AI.md", "PACKAGE_CONTENTS.json"}
        help_text = z.read("START_HERE.md").decode("utf-8")
        assert "Nicolas Jacobs" in help_text and record["central_file"] in help_text
        z.extractall(destination)
    root = destination / ("exercise_" + record["exercise"].replace(".", "_")) if record["exercise"].startswith("10.") else destination
    assert (root / "uv.lock").is_file() and (root / "pyproject.toml").is_file()
    python_spec = (root / ".python-version").read_text().strip()
    assert python_spec.startswith("3.12")
    # A previous execution may leave diagnostic notebooks in .tools; only
    # submitted archive members belong to this completeness check.
    notebooks = [destination / n for n in contents["files"] if n.endswith(".ipynb")]
    for notebook in notebooks:
        nb = nbformat.read(notebook, 4)
        nbformat.validate(nb)
        assert not any(o.output_type == "error" for c in nb.cells if c.cell_type == "code" for o in c.outputs)
        assert list(root.rglob(notebook.stem + ".html")), notebook
    pdfs = []
    for pdf in [destination / n for n in contents["files"] if n.endswith(".pdf")]:
        reader = PdfReader(pdf)
        assert all(page.extract_text().strip() for page in reader.pages)
        pdfs.append({"file": pdf.relative_to(root).as_posix(), "pages": len(reader.pages)})
    # Source data and imported references must verify outside .git as well.
    for source in (root / "sessions/ch12").glob("*_source.json"):
        metadata = json.loads(source.read_text())
        for name, sha in metadata.get("files", {}).items():
            candidates = list((root / "data/raw").rglob(name))
            if candidates:
                assert len(candidates) == 1 and digest(candidates[0].read_bytes()) == sha
    return root, {"exercise": record["exercise"], "zip_sha256": record["sha256"], "archive_crc_and_member_hashes": "PASS",
        "original_member_preservation": "PASS" if record["original_archive"] else "not applicable; approved Chapter 12 files",
        "notebooks": len(notebooks), "pdfs": pdfs, "python_spec": python_spec, "privacy_findings": findings}


def browser_check(root, key):
    checks = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for html in sorted(root.rglob("*.html")):
            raw = html.read_text(encoding="utf-8")
            soup = BeautifulSoup(raw, "html.parser")
            for im in soup.select('img[src^="data:image/png;base64,"]'):
                with Image.open(BytesIO(base64.b64decode(im["src"].split(",", 1)[1]))) as image:
                    image.verify()
            for width in (900, 1400):
                page = browser.new_page(viewport={"width": width, "height": 1000}, offline=True)
                errors, failed = [], []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("requestfailed", lambda req: failed.append({"url_type": req.url.split(":", 1)[0], "failure": req.failure}))
                page.goto(html.as_uri())
                page.wait_for_load_state("load")
                images = page.locator("img").count()
                loaded = page.locator("img").evaluate_all("xs => xs.every(x => x.complete && x.naturalWidth > 0)")
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                shot = QA / "screenshots" / key / (html.stem + f"_{width}.png")
                shot.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(shot), full_page=True)
                checks.append({"html": html.relative_to(root).as_posix(), "width": width, "images": images,
                    "all_images_loaded": loaded, "page_errors": errors, "failed_requests": failed, "horizontal_page_overflow": overflow})
                assert loaded and not errors, checks[-1]
                page.close()
        browser.close()
    return checks


def compare_csv(root, before):
    checked = []
    for rel, data in before.items():
        if not rel.endswith(".csv") or not (root / rel).is_file():
            continue
        a = pd.read_csv(BytesIO(data), dtype=str)
        b = pd.read_csv(root / rel, dtype=str)
        assert list(a.columns) == list(b.columns) and a.shape == b.shape, rel
        for col in a.columns:
            if col in {"fit_seconds", "predict_seconds"}:
                continue
            try:
                x = pd.to_numeric(a[col]).to_numpy(dtype=float)
                y = pd.to_numeric(b[col]).to_numpy(dtype=float)
            except (ValueError, TypeError):
                np.testing.assert_array_equal(a[col].fillna(""), b[col].fillna(""), err_msg=rel)
            else:
                np.testing.assert_allclose(x, y, atol=1e-9, rtol=1e-9, equal_nan=True, err_msg=rel)
        checked.append(rel)
    return checked


def execute(root, key):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(root)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
    for name, rel in {"JUPYTER_CONFIG_DIR": ".jupyter", "JUPYTER_DATA_DIR": ".local/share/jupyter", "JUPYTER_RUNTIME_DIR": ".local/share/jupyter/runtime", "IPYTHONDIR": ".local/ipython", "MPLCONFIGDIR": ".tools/matplotlib"}.items():
        env[name] = str(root / rel)
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".tools/playwright")
    before = {p.relative_to(root).as_posix(): p.read_bytes() for parent in (root / "outputs", root / "data/processed") if parent.exists() for p in parent.rglob("*.csv")}
    if key == "10.1":
        command = [sys.executable, "sessions/ch10/aufgabe_10_1.py"]
    elif key == "10.4":
        # Quarto PDF/HTML originals are preserved; execute its notebook copy freshly.
        helper = ROOT / "scripts/execute_submission_notebook.py"
        command = [sys.executable, str(helper), "reports/exercise_10_4/notebook_presentation.ipynb"]
    else:
        command = [sys.executable, "scripts/build_exercise_" + key.replace(".", "_") + ".py"]
    start = time.perf_counter()
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", timeout=1500)
    log = result.stdout + result.stderr
    (QA / (key.replace(".", "_") + "_execution.log")).write_text(log, encoding="utf-8")
    record = {"command": [Path(command[0]).name, *command[1:]], "returncode": result.returncode, "seconds": round(time.perf_counter()-start, 3),
              "shared_existing_environment": True, "clean_dependency_installation": "NOT RUN",
              "warnings": [line for line in log.splitlines() if any(w in line.lower() for w in ("warning", "unencrypted", "deprecated", "traceback", "error:"))]}
    if result.returncode == 0:
        record["scientific_csv_comparison"] = compare_csv(root, before)
        record["fresh_notebook_cells"] = {p.relative_to(root).as_posix(): [c.execution_count for c in nbformat.read(p,4).cells if c.cell_type == "code"] for p in root.rglob("*.ipynb")}
    else:
        record["error_tail"] = log[-2500:]
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exercise", nargs="*")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    QA.mkdir(parents=True, exist_ok=True)
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".tools/playwright")
    records = json.loads((FINAL / "package_manifest.json").read_text(encoding="utf-8"))["packages"]
    results = []
    for record in records:
        key = record["exercise"]
        if args.exercise and key not in args.exercise:
            continue
        root, report = archive_check(record)
        report["offline_html"] = browser_check(root, key)
        if args.execute:
            report["execution"] = execute(root, key)
        (QA / (key.replace(".", "_") + "_verification.json")).write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
        results.append(report)
        print(f"CHECKED {key}: archive/extraction/HTML; execution={report.get('execution', {}).get('returncode', 'NOT RUN')}; privacy findings={len(report['privacy_findings'])}", flush=True)
    if any(r.get("execution", {}).get("returncode", 0) for r in results):
        raise SystemExit("At least one extracted execution failed; see per-exercise report")


if __name__ == "__main__":
    main()
