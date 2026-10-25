"""Plot the parametric curve required in exercise 10.1.

Run from the project root: uv run python sessions/ch10/aufgabe_10_1.py
"""

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".tools/matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


def heart_coordinates(samples: int = 1001) -> tuple[NDArray, NDArray]:
    """Sample one full period, including both endpoints."""
    if isinstance(samples, bool) or not isinstance(samples, int) or samples < 3:
        raise ValueError("samples must be an integer >= 3")
    t = np.linspace(0.0, 2.0 * np.pi, samples)
    x = 16.0 * np.sin(t) ** 3
    y = 13.0 * np.cos(t) - 5.0 * np.cos(2 * t) - 2.0 * np.cos(3 * t) - np.cos(4 * t)
    return x, y


def save_plot(output: Path, samples: int = 1001) -> Path:
    """Save the curve with equal axis scaling, without opening a GUI."""
    x, y = heart_coordinates(samples)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 7), layout="constrained")
    ax.plot(x, y, color="crimson", linewidth=2)
    ax.set(title="Aufgabe 10.1 – Parametrische Herzkurve", xlabel="x(t)", ylabel="y(t)")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.3)
    try:
        fig.savefig(output, dpi=160)
    finally:
        plt.close(fig)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/ch10/aufgabe_10_1_herz.png")
    parser.add_argument("--samples", type=int, default=1001)
    args = parser.parse_args()
    print(f"Plot gespeichert: {save_plot(args.output, args.samples).resolve()}")


if __name__ == "__main__":
    main()
