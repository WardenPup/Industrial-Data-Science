"""Publication-sized plots and calculations, reusing validated 10.2/10.3 logic."""

import matplotlib.pyplot as plt
import seaborn as sns

from sessions.ch10.ai4i_data import load_ai4i
from sessions.ch10.ai4i_eda import AIR, MEASUREMENTS, SPEED, TORQUE, iqr_summary

LABELS = {TORQUE: 'Drehmoment [Nm]', SPEED: 'Drehzahl [rpm]', AIR: 'Lufttemperatur [K]'}


def report_data():
    data = load_ai4i()
    measurements = data[MEASUREMENTS]
    return (data, measurements.describe(), measurements.corr(method='pearson'),
            measurements.corr(method='spearman'), iqr_summary(measurements))


def style():
    sns.set_theme(style='whitegrid', context='paper', font_scale=1.15)
    plt.rcParams.update({'figure.dpi': 160, 'savefig.dpi': 200})


def distributions(data):
    style()
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.7), layout='constrained')
    for ax, column in zip(axes, MEASUREMENTS):
        sns.histplot(data=data, x=column, bins=30, ax=ax, color='#286a86')
        ax.set(xlabel=LABELS[column], ylabel='Häufigkeit')
        ax.tick_params(labelsize=8)
    plt.show()


def boxes(data):
    style()
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.5), layout='constrained')
    for ax, column in zip(axes, MEASUREMENTS):
        sns.boxplot(data=data, y=column, ax=ax, whis=1.5 + 1e-12,
                    color='#90bcc6', fliersize=2, linewidth=0.9)
        ax.set(xlabel='', ylabel=LABELS[column])
    plt.show()


def relationship(data):
    style()
    fig, ax = plt.subplots(figsize=(6.4, 3.4), layout='constrained')
    points = ax.scatter(data[SPEED], data[TORQUE], c=data[AIR], cmap='viridis',
                        s=5, alpha=0.45, edgecolors='none', rasterized=True)
    ax.set(xlabel=LABELS[SPEED], ylabel=LABELS[TORQUE])
    fig.colorbar(points, ax=ax, label=LABELS[AIR])
    plt.show()


def correlation_table(pearson, spearman):
    rows = ['| Größenpaar | Pearson r | Spearman ρ |', '|:--|--:|--:|']
    for a, b, label in [(TORQUE, SPEED, 'Drehmoment / Drehzahl'),
                        (TORQUE, AIR, 'Drehmoment / Lufttemperatur'),
                        (SPEED, AIR, 'Drehzahl / Lufttemperatur')]:
        p = f'{pearson.loc[a, b]:.4f}'.replace('.', ',')
        s = f'{spearman.loc[a, b]:.4f}'.replace('.', ',')
        rows.append(f'| {label} | {p} | {s} |')
    return '\n'.join(rows)
