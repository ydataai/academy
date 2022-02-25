"Utility methods for plotting in the calculated features quickstart notebook."
from typing import Union, Dict, List

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import pandas as pd

from ydata.dataset import Dataset

def _viz_revol_util(ax, sample: pd.DataFrame):
    "Plots the product of total credit limit and revolving credit utilization to the revolving credit balance."
    expected_revol_bal = sample.revol_util * sample.total_rev_hi_lim
    sns.scatterplot(x=expected_revol_bal, y=sample.revol_bal, s=150, ax=ax, color=ydata_colorlist()[0])
    ax.set(xscale="log", yscale="log")
    plt.setp(ax, xlabel = 'Predicted revolving balance, $')
    plt.setp(ax, ylabel = 'Expected revolving balance, $')
    lims = [min([ax.get_xlim(), ax.get_ylim()]), max([ax.get_xlim(), ax.get_ylim()])]
    ax.plot(lims, lims, 'k', alpha=0.75)
    ax.grid(False)
    ax.title.set_text(f'Revolving balance')

def _viz_total_pymnt(ax, sample: pd.DataFrame):
    "Compares the summation of the different pay components to the total payments."
    payments = pd.DataFrame({'Interest': [sample.total_rec_int.mean(), 0],
                            'Late fee': [sample.total_rec_late_fee.mean(), 0],
                            'Principal': [sample.total_rec_prncp.mean(), 0],
                            'Total Payment': [0, sample.total_pymnt.mean()]},
                            index=['Components', 'Total Payment'])
    set_custom_theme([4, 9, 1, 0])
    payments.plot(kind='bar', stacked=True, edgecolor='k', linewidth=1.5, width=1.0, ax=ax)
    ax.grid(False)
    plt.setp(ax, ylabel='Amount, $')
    ax.title.set_text(f'Breakdown of payment components in the dataset (average)')
    sns.despine(ax=ax, top=True, right=True, left=True, bottom=True)

def _viz_installment(ax, sample: pd.DataFrame):
    """Compares the expected payment schedule with the proposed installments of a random record in the sample."""
    record = sample.sample(n=1)
    term = 36 if record.term.values == '36m' else 60
    cumul_payed = [record.installment.values[0]*period for period in range(1,term+1)]
    loan_amnt = record.loan_amnt.values[0]
    p_interest = record.int_rate.values[0]/12  # Payed monthly
    expected_cumul = term*(loan_amnt*((p_interest*(1+p_interest)**term)/((1+p_interest)**term-1)))
    sns.barplot(ax = ax, x=list(range(1,term+1)), y=cumul_payed, color=ydata_colorlist()[0])
    xlabels = [item.get_text() for item in ax.get_xticklabels()]
    xlabels = [label if label in ['1', str(term)] else '' for label in xlabels]
    ax.set_xticklabels(xlabels)
    for patch in ax.patches:
        patch.set_width(0.95)
    ax.axhline(expected_cumul, label='Total due payment', color=ydata_colorlist()[8])
    ax.title.set_text('Randomly sampled loan schedule: {}$ loan, {:.1f}% interest {} month term'.format(loan_amnt, p_interest*12*100, term))
    ax.legend(loc='upper center')
    plt.setp(ax, ylabel='Cumulative payments, $')
    plt.setp(ax, xlabel = 'Time, months')
    sns.despine(ax=ax, top=True, right=True, left=True, bottom=True)

def viz_main(sample: Union[Dataset, pd.DataFrame], sample_name: str = 'Real Data'):
    set_custom_theme()
    if isinstance(sample, Dataset):
        sample = sample.to_pandas()
    fig, axs = plt.subplots(3, 1, constrained_layout=True, figsize=(12,16))
    _viz_revol_util(axs[0], sample)
    _viz_total_pymnt(axs[1], sample)
    _viz_installment(axs[2], sample)
    fig.suptitle(sample_name, fontweight='bold')
    fig.tight_layout(pad=2)
    plt.show()

def viz_side_by_side(samples: Dict[str, Dataset]):
    samples = {k:v.to_pandas() for k, v in samples.items()}
    fig = plt.figure(figsize=(26,28))
    gs = GridSpec(nrows=4,ncols=2, height_ratios = [0.0001,1,1,1])
    axs = [[plt.subplot(gs[j, i]) for j in range(4)] for i in range(2)]
    for i, (sample_name, sample) in enumerate(samples.items()):
        axs[i][0].axis('off')
        axs[i][0].set_title(sample_name, fontweight='bold')
        _viz_revol_util(axs[i][1], sample)
        _viz_total_pymnt(axs[i][2], sample)
        _viz_installment(axs[i][3], sample)
    fig.tight_layout(pad=0.5)
    plt.show()

def ydata_colorlist(n: int = None):
    """Returns a colorlist with the YData colors.
    Pass n to define a truncated color map (use less colors)"""
    colors = [
        "#830000",  # Dark red 0
        "#474747",  # Subheadlines 1
        "#FF6464",  # Error 2
        "#040404",  # Dominant hue 3
        "#FFFFFF",  # Primary color 4
        "#5FED5C",  # Success 5
        "#FFEA2D",  # Warning 6
        "#1298E3",  # Visual aid 7
        "#7A7A7A",  # Border dividers 8
        "#B8B8B8",  # Disabled states 9
        "#F5F5F5",  # Backgrounds, text on dark background 10
        "#E32212",  # Accent color 11
    ]
    if n and n>len(colors):
        n=len(colors)
    return colors[:n]

def set_custom_theme(color_idxs: List[int] = None):
    """Set a custom theme for the plots. Will default to the full palette.
    Args:
        color_idxs [List[int]]: if provided will use this list to subset and reorder the ydata_colorlist/palette"""
    palette = ydata_colorlist()
    if color_idxs:
        try:
            palette = [palette[i] for i in color_idxs]
        except IndexError:
            pass
    sns.set_theme(style='white', palette=palette, rc={"axes.grid": "False"})

plt.rcParams["figure.figsize"] = (18,6)
