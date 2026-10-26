"""Plotting separate from calculations; course helper with German labels."""

import matplotlib.pyplot as plt
import seaborn as sns


def plot_production_data(df, orig_data_column, gap_column, imp_column=None):
    """Course helper adapted only for labels and returning its Figure.

    Source: Chapter 11, retrieved 2026-10-26 (see notebook).
    Explicit NaNs remain in line paths rather than being bridged by aggregation.
    """
    fig, axes = plt.subplots(3 if imp_column else 2, 1, figsize=(12, 7), sharex=True)
    for ax, column, title, color in zip(
        axes[:2], [orig_data_column, gap_column],
        ["Vollständige Reihe (ebenfalls mit Störungen)", "Reihe mit ursprünglichen Lücken"],
        ["grey", "black"],
    ):
        sns.lineplot(x=df.index, y=df[column], ax=ax, color=color, label=column)
        # Seaborn drops NaNs before drawing; restore the full path to show gaps.
        ax.lines[0].set_data(df.index, df[column])
        ax.set(title=title, ylabel="Stück pro Woche", xlabel="Datum")
    if imp_column is not None:
        values = df[imp_column].where(df[gap_column].isna())
        sns.lineplot(x=df.index, y=values, ax=axes[2], color="blue", label="Imputiert")
        axes[2].set(ylabel="Stück pro Woche", xlabel="Datum")
    fig.tight_layout()
    return fig


def plot_smoothing(frame):
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=False)
    windows = [frame, frame.loc["2018":"2019"]]
    for ax, data in zip(axes, windows):
        for column, label, color in [
            ("pieces_gaps", "Beobachtet mit Lücken", "0.65"),
            ("rolling_mean", "Mittelwert, 5 Wochen", "#d95f02"),
            ("rolling_median", "Median, 5 Wochen", "#0072b2"),
        ]:
            sns.lineplot(x=data.index, y=data[column], ax=ax, label=label, color=color, linewidth=1)
            ax.lines[-1].set_data(data.index, data[column])
        ax.set(ylabel="Stück pro Woche", xlabel="Datum")
    axes[0].set_title("Historische Glättung – vollständiger Zeitraum")
    axes[1].set_title("Fester Detailausschnitt 2018–2019 (keine Fensterauswahl anhand des Ausschnitts)")
    fig.tight_layout()
    return fig
