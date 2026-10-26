"""Assemble documented submission copies; preserve originals and scientific bytes."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "submission/final"
SNAPSHOT = "1d8c583186dfa8a9691204a6902a50f10c086a74"
NAMES = {
    "10.1": ("Isolierte Umgebung und Herzkurve", "sessions/ch10/aufgabe_10_1.md", None),
    "10.2": ("Jupyter und AI4I-Grundstatistik", "sessions/ch10/ai4i_explore.ipynb", "ai4i_explore"),
    "10.3": ("Explorative Analyse mit Seaborn", "sessions/ch10/ai4i_seaborn.ipynb", "ai4i_seaborn"),
    "10.4": ("Wissenschaftlicher Bericht mit Quarto", "reports/exercise_10_4/paper.qmd", "paper"),
    "11.1": ("Rollende Glättung mit erhaltener Lückenmaske", "sessions/ch11/production_smoothing.ipynb", "production_smoothing"),
    "11.2": ("Vergleich von sechs Imputationsmethoden", "sessions/ch11/production_imputation.ipynb", "production_imputation"),
    "11.3": ("Zweistufige STL-Imputation", "sessions/ch11/production_stl_imputation.ipynb", "production_stl_imputation"),
    "11.4": ("STL-basierte Ausreißerkandidaten", "sessions/ch11/production_outliers.ipynb", "production_outliers"),
    "12.1": ("Zeitreihen-Clustering: k-Means und KASBA", "sessions/ch12/gesture_clustering.ipynb", "gesture_clustering"),
    "12.2": ("Gestenklassifikation: DTW-3-NN und CNN", "sessions/ch12/uwave_classification.ipynb", "uwave_classification"),
    "12.3": ("Gestenklassifikation mit Time Series Forest", "sessions/ch12/uwave_forest.ipynb", "uwave_forest"),
    "12.4": ("Multivariate Energieregression", "sessions/ch12/appliances_regression.ipynb", "appliances_regression"),
}
AI = """# Autorenschaft und KI-Unterstützung

Verantwortlicher studentischer Autor: Nicolas Jacobs – MCI, Wintersemester 2026/27.
Codex unterstützte Implementierung, Korrekturen, Tests und technische Dokumentation.
ChatGPT unterstützte Verständnis, Interpretation, Reviewentwürfe und Arbeitsplanung.
Der Studierende bewertete Ergebnisse und dokumentierte seine fachlichen Entscheidungen.
Automatisierte Tests sind keine zusätzlichen unabhängigen menschlichen Prüfhandlungen.
Die erhaltenen Reviews und PRs dokumentieren die tatsächlichen Beiträge und Freigaben;
es wird keine ausschließlich studentische Codeautorschaft behauptet.
Die lehrveranstaltungsspezifische Zulässigkeit und vorgeschriebene Offenlegungsform
muss der Studierende vor Einreichung bestätigen; eine solche Bestätigung wurde
nicht bereitgestellt. Keine automatische Hochschuleinreichung durchgeführt.
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def closure(files):
    """Include actual local Python imports recursively, without unrelated exercises."""
    pending = list(files)
    while pending:
        rel = pending.pop()
        if rel.suffix != ".py":
            continue
        for node in ast.walk(ast.parse((ROOT / rel).read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("sessions."):
                target = Path(*node.module.split(".")).with_suffix(".py")
                targets = [target] if (ROOT / target).is_file() else [Path(*node.module.split("."), alias.name).with_suffix(".py") for alias in node.names]
                for target in targets:
                    if (ROOT / target).is_file() and target not in files:
                        files.add(target)
                        pending.append(target)
    return files


def chapter12(i):
    key = f"12.{i}"
    module = ["clustering", "classification", "forest", "regression"][i-1]
    source = ["gesture", "uwave", "uwave", "appliances"][i-1]
    dataset = ["GesturePebbleZ1", "UWaveGestureLibrary", "UWaveGestureLibrary", "AppliancesEnergy"][i-1]
    doc = ["GESTURE_PEBBLE", "UWAVE", "UWAVE", "APPLIANCES"][i-1]
    files = {Path(NAMES[key][1]), Path(f"sessions/ch12/{module}.py"),
             Path(f"sessions/ch12/{source}_source.json"), Path("sessions/__init__.py"),
             Path(f"scripts/build_exercise_12_{i}.py"), Path("templates/notebook_export.html.j2"),
             Path(f"docs/EXERCISE_12_{i}_REQUIREMENTS.md"), Path(f"docs/{doc}_SOURCE.md"),
             Path(f"reviews/exercise_12_{i}.md"), Path("pyproject.toml"), Path("uv.lock"), Path(".python-version")}
    files = closure(files)
    if i in (3, 4):
        files.add(Path("sessions/ch12/uwave_source.json"))  # shared classification module import
    if i == 3:
        files.add(Path("sessions/ch12/forest_reference.json"))
    files.update(p.relative_to(ROOT) for p in (ROOT / f"data/raw/{dataset}").glob("*.ts"))
    files.update(p.relative_to(ROOT) for p in (ROOT / f"outputs/ch12/exercise_12_{i}").iterdir() if p.is_file())
    members = {p.as_posix(): (ROOT / p).read_bytes() for p in sorted(files)}
    adjustments = []
    if i == 3:
        name = "sessions/ch12/forest_reference.json"
        original = subprocess.check_output(["git", "show", SNAPSHOT + ":" + name], cwd=ROOT)
        if original != members[name]:
            assert json.loads(original) == json.loads(members[name])
            adjustments.append({"file": name, "change": "restore checksum-pinned line endings only",
                                "before": sha(original), "after": sha(members[name])})
    if i == 4:
        name = "sessions/ch12/appliances_source.json"
        original = subprocess.check_output(["git", "show", SNAPSHOT + ":" + name], cwd=ROOT)
        if original != members[name]:
            assert json.loads(original) == json.loads(members[name])
            adjustments.append({"file": name, "change": "restore approved CRLF metadata bytes (technical commit 7eb767f)",
                                "before": sha(original), "after": sha(members[name])})
    # Match approved byte checksums, including original Windows line endings.
    manifest = json.loads(members[f"outputs/ch12/exercise_12_{i}/validation_manifest.json"])
    for name, digest in manifest["files"].items():
        data = members[name]
        if sha(data) != digest:
            alternatives = [data.replace(b"\r\n", b"\n"), data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")]
            restored = next((b for b in alternatives if sha(b) == digest), None)
            if restored is None:
                raise ValueError(f"Unexplained approved artifact drift: {name}")
            assert json.loads(data) == json.loads(restored), "Only JSON metadata line-ending restoration allowed"
            members[name] = restored
            adjustments.append({"file": name, "change": "restore checksum-pinned line endings only", "before": sha(data), "after": sha(restored)})
    if i == 3:
        reference = json.loads(members["sessions/ch12/forest_reference.json"])
        for name, digest in reference["files"].items():
            data = subprocess.check_output(["git", "show", reference["approved_commit"] + ":" + name], cwd=ROOT)
            assert sha(data) == digest
            members[name] = data  # standalone load_reference: no .git required
    return members, adjustments


def start_here(key, prefix):
    ch, i = key.split(".")
    title, central, stem = NAMES[key]
    central = prefix + central
    html = prefix + f"outputs/ch{ch}/exercise_{ch}_{i}/{stem}.html" if stem else None
    command = f"python scripts/build_exercise_{ch}_{i}.py" if key != "10.1" else "python sessions/ch10/aufgabe_10_1.py"
    source = "Keine externen Daten; analytische Herzkurve." if key == "10.1" else {
        "10": "AI4I 2020, UCI, CC BY 4.0; Herkunft/SHA256 in data/raw/README.md.",
        "11": "Synthetische Kurs-CSV; data/raw/PRODUCTION_SOURCE.md. Kurs CC BY-NC-SA 4.0; keine separat bestätigte CSV-Lizenz.",
        "12": "Herkunft, Rohdatenhashes und Lizenzgrenzen in docs/*_SOURCE.md und sessions/ch12/*_source.json. Gesture/UWave: keine separat bestätigte Datenlizenz; Appliances-Zenodo: CC BY 4.0.",
    }[ch]
    extra = "Für PDF-Neuerstellung: Chromium (10.2) bzw. Quarto 1.10.19 und LuaLaTeX/TeX Live 2026 (10.4); Details in README_ABGABE.md." if ch == "10" else ""
    limits = "Ein gegebener Split und Seed 42; keine allgemeine Überlegenheit. CNN-Zahlen können zwischen Windows/Linux abweichen; Laufzeiten sind nicht identisch." if ch == "12" else "Synthetische Daten bzw. analytisches Beispiel; methodische Grenzen in der Lösung. Keine beliebige plattformübergreifende Byteidentität neu erzeugter Exporte zugesichert."
    return f"""# Exercise {key} – {title}

Studentischer Autor: **Nicolas Jacobs – MCI**, Wintersemester 2026/27.
Abgabeaufbereitung: 27.10.2026; wissenschaftlich freigegebene Lösung, keine neue Studie.

Zuerst lesen: [{Path(central).name}]({central}).
""" + (f"Ohne Python: [{stem}.html]({html}) offline im Browser öffnen.\n" if html else f"Grafik: [{prefix}outputs/ch10/aufgabe_10_1_herz.png]({prefix}outputs/ch10/aufgabe_10_1_herz.png). Kein Notebook/HTML gefordert.\n") + f"""
Enthalten: Lösung/Code, zugehörige Ergebnisdateien und Grafiken, benötigte Daten
oder Datenhinweise, Python-Spezifikation und uv-Lockfile. Bestehende Reviewtexte
sind historische Originale; spätere Freigaben/Integration stehen im äußeren Prüfbericht.

## Reproduktion
ZIP vollständig entpacken. {('In `' + prefix.rstrip('/') + '` wechseln.') if prefix else 'Im entpackten Paketstamm arbeiten.'}
Python 3.12 (geprüft 3.12.15), uv (geprüft 0.13.5); Abhängigkeiten in
`pyproject.toml`/`uv.lock`, insbesondere NumPy, pandas, Matplotlib/Seaborn,
Jupyter/nbconvert; Kapitel 11 zusätzlich SciPy/statsmodels, Kapitel 12 aeon/PyTorch.
Nur die für diese Aufgabe importierten Pakete werden tatsächlich genutzt.

```text
uv sync --locked
uv run --locked {command}
```

Erstinstallation benötigt Internet. Die beigefügten Daten erlauben die Rechnung
danach offline. Notebook in VS Code/Jupyter mit diesem Environment öffnen.
{extra}
Keine unabhängige Neuinstallation aus diesem ZIP getestet; Prüfung mit vorhandener
Projektumgebung. Ergebnisse liegen unter `outputs/`, Kapitel 11 auch `data/processed/`.

Quelle/Lizenz: {source}
Grenzen: {limits}
KI-Unterstützung und Verantwortung: [AUTHORSHIP_AND_AI.md](AUTHORSHIP_AND_AI.md).
Keine automatische Hochschuleinreichung durchgeführt.
"""


def main():
    records = []
    for key in NAMES:
        ch, i = key.split(".")
        filename = f"Industrial_Data_Science_Exercise_{ch}_{i}.zip"
        original = ROOT / f"submission/chapter_{ch}/{filename}"
        prefix = f"exercise_10_{i}/" if ch == "10" else ""
        if ch != "12":
            approved = json.loads((ROOT / f"submission/chapter_{ch}/submission_manifest.json").read_text(encoding="utf-8"))["packages"]
            approved = next(p for p in approved if p["file"] == filename)
            assert sha(original.read_bytes()) == approved["sha256"]
            with zipfile.ZipFile(original) as z:
                assert z.testzip() is None
                members = {n: z.read(n) for n in z.namelist()}
            original_record = {"path": original.relative_to(ROOT).as_posix(), "sha256": sha(original.read_bytes()), "bytes": original.stat().st_size}
            adjustments = [{"change": "add START_HERE.md and AUTHORSHIP_AND_AI.md; all original member bytes unchanged"}]
        else:
            members, adjustments = chapter12(int(i))
            original_record = None
        members["START_HERE.md"] = start_here(key, prefix).encode("utf-8")
        members["AUTHORSHIP_AND_AI.md"] = AI.encode("utf-8")
        content = {n: {"bytes": len(b), "sha256": sha(b)} for n, b in sorted(members.items())}
        members["PACKAGE_CONTENTS.json"] = (json.dumps({"exercise": key, "snapshot": SNAPSHOT, "original_archive": original_record,
            "documented_adjustments": adjustments, "files": content}, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        destination = DEST / f"chapter_{ch}" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for name, data in sorted(members.items()):
                assert not any(part in {".git", ".venv", "__pycache__", ".tools"} for part in Path(name).parts)
                info = zipfile.ZipInfo(name, (2026, 10, 27, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, data)
        records.append({"exercise": key, "title": NAMES[key][0], "file": destination.relative_to(DEST).as_posix(),
            "bytes": destination.stat().st_size, "sha256": sha(destination.read_bytes()), "original_archive": original_record,
            "central_file": prefix + NAMES[key][1], "html": prefix + f"outputs/ch{ch}/exercise_{ch}_{i}/{NAMES[key][2]}.html" if NAMES[key][2] else None,
            "adjustments": adjustments, "files": content})
        print(f"BUILT {key}: {destination.stat().st_size} bytes", flush=True)
    (DEST / "package_manifest.json").write_text(json.dumps({"prepared": "2026-10-27", "snapshot": SNAPSHOT,
        "ai_assistance": "Codex", "uploaded": False, "packages": records}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DEST / "SHA256SUMS.txt").write_text("".join(r["sha256"] + "  " + r["file"] + "\n" for r in records), encoding="utf-8")


if __name__ == "__main__":
    main()
