"""Course-helper figures adapted locally for Exercise 11.2 only."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sessions.ch11.production_plots import plot_production_data
from sessions.ch11.imputation import METHODS, gap_table


def plot_imputation(frame, smoothed, result, method):
    data = frame[["pieces"]].copy()
    data["smoothed_gaps"] = smoothed
    data["imputed"] = result
    fig = plot_production_data(data, "pieces", "smoothed_gaps", "imputed")
    # The course helper displays only imputed positions on its third axis.
    # Restore the complete NaN-bearing path so distinct gaps are not connected.
    fig.axes[2].lines[0].set_data(data.index, result.where(smoothed.isna()))
    fig.axes[0].set_title("Vollständige Kursreihe pieces – keine fehlerfreie Referenz")
    fig.axes[1].set_title("Freigegebener 5-Wochen-Median aus 11.1 mit Lücken")
    fig.axes[2].set_title(f"Nur ergänzte Wochen: {METHODS[method]}")
    for ax, label in zip(fig.axes, ["pieces", "Median mit Lücken", METHODS[method]]):
        ax.lines[0].set_label(label)
        ax.legend(loc="upper left")
        ax.set(ylabel="Stück pro Woche", xlabel="Datum")
    fig.set_size_inches(12, 9)
    fig.tight_layout()
    return fig


def plot_longest_gap(smoothed, results):
    gaps = gap_table(smoothed)
    gap = gaps.sort_values(["weeks", "start"], ascending=[False, True]).iloc[0]
    view = smoothed.loc[gap.start - pd.Timedelta(weeks=8):gap.end + pd.Timedelta(weeks=8)]
    fig, ax = plt.subplots(figsize=(12, 5))
    for method, label in METHODS.items():
        sns.lineplot(x=view.index, y=results.loc[view.index, method], ax=ax, label=label, linewidth=1.4)
    sns.scatterplot(x=view.index, y=view, ax=ax, color="black", s=25, label="Beobachteter Median")
    ax.axvspan(gap.start, gap.end, color="grey", alpha=0.12, label="Ursprüngliche Lücke")
    ax.set(title=f"Methodenvergleich an der ersten längsten Lücke ({int(gap.weeks)} Wochen)",
           xlabel="Datum", ylabel="Stück pro Woche")
    ax.legend(ncol=2)
    fig.tight_layout()
    return fig
