"""Course plotting helpers with German labels and explicit gap/estimate paths."""

import matplotlib.pyplot as plt
import seaborn as sns

from sessions.ch11.production_plots import plot_production_data
from sessions.ch11.imputation import gap_table


def seasonal_decompose_seaborn(decomposed_ts, title):
    """Chapter 11 helper adapted for German labels and returning the figure."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    for ax, values, label in zip(axes, [decomposed_ts.observed, decomposed_ts.trend,
                                       decomposed_ts.seasonal, decomposed_ts.resid],
                                 ["Vorläufig linear ergänzte Reihe", "Trend", "Saison", "Residuum"]):
        sns.lineplot(x=values.index, y=values.values, ax=ax, label=label)
        ax.set(title=label, xlabel="Datum", ylabel="Stück pro Woche")
    fig.suptitle(title + " (unterschiedliche y-Skalen)")
    fig.tight_layout()
    return fig


def plot_deseasonalized(stages):
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    for ax, column, title in zip(axes, ["smoothed_gaps", "deseasonalized_gaps"],
                                 ["Geglättete Eingabe mit ursprünglichen Lücken", "Saisonbereinigte Eingabe – gleiche Lücken"]):
        sns.lineplot(x=stages.index, y=stages[column], ax=ax, label=title)
        ax.lines[0].set_data(stages.index, stages[column])
        ax.set(title=title, ylabel="Stück pro Woche", xlabel="Datum")
    fig.tight_layout()
    return fig


def plot_final_production(frame, stages):
    data = frame[["pieces"]].join(stages[["smoothed_gaps", "final_imputed"]])
    fig = plot_production_data(data, "pieces", "smoothed_gaps", "final_imputed")
    fig.axes[2].lines[0].set_data(data.index, data.final_imputed.where(data.smoothed_gaps.isna()))
    for ax, label in zip(fig.axes, ["Vollständige Kursreihe pieces – keine fehlerfreie Referenz",
                                    "Freigegebener 5-Wochen-Median mit Lücken",
                                    "Nur ergänzte Wochen: saisonbereinigt linear, danach Saison addiert"]):
        ax.set(title=label, ylabel="Stück pro Woche", xlabel="Datum")
        ax.lines[0].set_label(label.split(" – ")[0])
        ax.legend(loc="upper left")
    fig.set_size_inches(12, 9)
    fig.tight_layout()
    return fig


def plot_long_gap(stages):
    gaps = gap_table(stages.smoothed_gaps)
    gap = gaps.sort_values(["weeks", "start"], ascending=[False, True]).iloc[0]
    start = stages.index.get_loc(gap.start)
    stop = stages.index.get_loc(gap.end) + 1
    view = stages.iloc[max(0, start - 8):min(len(stages), stop + 8)]
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    for column, label in [("preliminary_linear", "Einfach linear"), ("final_imputed", "STL-gestützt")]:
        sns.lineplot(x=view.index, y=view[column], ax=axes[0], label=label)
    sns.scatterplot(x=view.index, y=view.smoothed_gaps, ax=axes[0], label="Bekannter Median", color="black", s=25)
    difference = (view.final_imputed - view.preliminary_linear).where(view.smoothed_gaps.isna())
    sns.lineplot(x=view.index, y=difference, ax=axes[1], label="STL-gestützt minus linear")
    axes[1].lines[0].set_data(view.index, difference)
    for ax in axes:
        ax.axvspan(gap.start, gap.end, color="grey", alpha=0.12)
        ax.set(ylabel="Stück pro Woche", xlabel="Datum")
    axes[0].set_title(f"Erste längste Lücke: {int(gap.weeks)} Wochen – zwei Schätzungen, kein Genauigkeitsvergleich")
    axes[1].set_title("Differenz ausschließlich an ursprünglich fehlenden Wochen")
    fig.tight_layout()
    return fig
