import matplotlib.gridspec as gridspec
import matplotlib.pylab as pl
from matplotlib.pyplot import (legend, subplots, suptitle, tick_params,
                               tight_layout, thetagrids, show)
from pandas import DataFrame, cut
from statsmodels.graphics.tsaplots import plot_acf

from results import add_hour_month_season, calculate_metrics_byperiod
from itertools import accumulate
from collections import deque

NOTEBOOK_FIG_SIZE = (24,7)


import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def plot_timeseries(data: DataFrame, feature: str = 'speed', title:str='', save_path=None, plt_show:bool = False):
    "Line plot of a times-series."
    assert isinstance(data, DataFrame), 'Data must be a pandas DataFrame.'
    assert feature in data.columns, "Feature must exist in data columns."
    ts = data[feature]
    fig, ax = subplots(1, 1, figsize=NOTEBOOK_FIG_SIZE)
    ts.plot(use_index=True, linewidth=0.8, c='#a62419', ax=ax)
    suptitle(title, fontsize=24, fontweight='bold')
    show()

def compare_acf(original: DataFrame, reconstructed: DataFrame, feature:str='speed',
            n_lags: int=24, title:str = ''):
    """Given two pandas dataframes the autocorrelation function is plotted."""
    real_ts, synth_ts = original[feature].dropna(), reconstructed[feature].dropna()
    n_lags = min(len(real_ts)/2-1, n_lags)
    fig, axs = subplots(1, 2, sharex=True, figsize=NOTEBOOK_FIG_SIZE)
    plot_acf(real_ts, ax=axs[0], lags=n_lags, title='Original')
    axs[0].set_xlabel('Lag Number')
    axs[0].set_ylabel('Autocorrelation')
    plot_acf(synth_ts, ax=axs[1], lags=n_lags, title='Reconstructed')
    axs[1].set_xlabel('Lag Number')
    axs[1].set_ylabel('Autocorrelation')
    suptitle(title, fontsize=24, fontweight='bold')
    return axs

def plot_hist(original: DataFrame, reconstructed: DataFrame, feature:str='speed', title:str='', x_label:str='', y_label:str=''):
    """Given two Pandas dataframes with real data and synthetic samples both histograms are plotted."""

    real_ts, synth_ts = original[feature].dropna(), reconstructed[feature].dropna()
    fig, axs = subplots(1, 1, sharex=True, figsize=NOTEBOOK_FIG_SIZE)

    # Plot original
    axs.hist(real_ts, label='Original', bins=50, alpha=0.2, density=True, histtype='barstacked', color='grey')
    real_ts.plot.kde(ax=axs, legend=False, label='_nolegend_', color='grey')

    # Plot reconstructed
    axs.hist(synth_ts, label='Reconstructed', bins=50, alpha=0.2, density=True, histtype='barstacked', color='red')
    synth_ts.plot.kde(ax=axs, legend=False, label='_nolegend_', color='red')

    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_visible(False)
    axs.spines['left'].set_visible(False)
    axs.legend(loc='upper right')

    axs.set_xlabel(feature, fontsize=12)
    axs.set_ylabel('Distribution', fontsize=12)
    suptitle(title, fontsize=16)
    show()

def plot_multicolor_line(original: DataFrame, reconstructed: DataFrame, feature: str='speed', title:str=''):

    orig_ts, recn_ts = original[feature], reconstructed[feature]

    fig, ax = subplots(1, 1, figsize=NOTEBOOK_FIG_SIZE)
    recn_ts.plot(use_index=True, linewidth=0.5, ax=ax, c='black', alpha=1, label='reconstructed')
    orig_ts.plot(linewidth=0.4, c='#a62419', ax=ax, label='original')
    #ax.set_ylim([0,10])
    suptitle(title, fontsize=24, fontweight='bold')
    legend()
    show()

def plot_hist(original: DataFrame, reconstructed: DataFrame, feature:str='speed', title:str='', x_label:str='', y_label:str=''):
    """Given two Pandas dataframes with real data and synthetic samples both histograms are plotted."""

    real_ts, synth_ts = original[feature].dropna(), reconstructed[feature].dropna()
    fig, axs = subplots(1, 1, sharex=True, figsize=NOTEBOOK_FIG_SIZE)

    # Plot original
    axs.hist(real_ts, label='Original', bins=50, alpha=0.2, density=True, histtype='barstacked', color='grey')
    real_ts.plot.kde(ax=axs, legend=False, label='_nolegend_', color='grey')

    # Plot reconstructed
    axs.hist(synth_ts, label='Reconstructed', bins=50, alpha=0.2, density=True, histtype='barstacked', color='red')
    synth_ts.plot.kde(ax=axs, legend=False, label='_nolegend_', color='red')

    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_visible(False)
    axs.spines['left'].set_visible(False)
    axs.legend(loc='upper right')

    axs.set_xlabel(feature, fontsize=12)
    axs.set_ylabel('Distribution', fontsize=12)
    suptitle(title, fontsize=24, fontweight='bold')
    show()

def compare_lags(original: DataFrame, reconstructed: DataFrame, feature: str = 'speed',
            title:str='1st Hour and 1st Day Differences - Distribution Overlap'):
    """Given two Pandas dataframes with real data and synthetic samples both histograms are plotted."""

    real_ts, synth_ts = original[feature], reconstructed[feature]
    real_ts_1lag = ( real_ts.shift(1) - real_ts)[1:]
    synth_ts_1lag = ( synth_ts.shift(1) - synth_ts)[1:]
    real_ts_24lag = ( real_ts.shift(24) - real_ts)[24:]
    synth_ts_24lag = ( synth_ts.shift(24) - synth_ts)[24:]

    fig, axs = subplots(1, 2, sharex=True, figsize=NOTEBOOK_FIG_SIZE)

    hist_kwargs = {'bins': 50, 'alpha': 0.2, 'density': True, 'histtype': 'barstacked'}
    synth_kwargs = {'label': 'Reconstructed', 'color': 'red'}
    real_kwargs = {'label': 'Original', 'color': 'grey'}
    kde_kwargs = {'legend': False, 'label': '_nolegend_'}


    axs[0].hist(synth_ts_1lag, **hist_kwargs, **synth_kwargs)
    synth_ts_1lag.plot.kde(ax=axs[0], **kde_kwargs, color='red')

    axs[0].hist(real_ts_1lag, **hist_kwargs, **real_kwargs)
    real_ts_1lag.plot.kde(ax=axs[0], **kde_kwargs, color='grey')

    axs[1].hist(synth_ts_24lag, **hist_kwargs, **synth_kwargs)
    synth_ts_24lag.plot.kde(ax=axs[1], **kde_kwargs, color='red')

    axs[1].hist(real_ts_24lag, **hist_kwargs, **real_kwargs)
    real_ts_24lag.plot.kde(ax=axs[1], **kde_kwargs, color='grey')

    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.legend(loc='upper right')

        # Labels and Ticks
        ax.set_ylabel('Density', fontsize=16)
        ax.xaxis.set_tick_params(labelsize=16)
        ax.yaxis.set_tick_params(labelsize=16)
        ax.yaxis.set_ticklabels(["{:.0%}".format(i) for i in ax.get_yticks()])

    axs[0].set_title('1st Difference', fontsize=18)
    axs[1].set_title('1 Day Differences', fontsize=18)

    suptitle(title, fontsize=22, fontweight='bold')
    show()

def plot_metric_byperiod(original: DataFrame, reconstructed: DataFrame, feature: str = 'speed', metric: str = 'mean'):
    """
    Function to plot line plots on a metric ['mean','median','min','max'] over a period ['season','month','hour'].
    The datasets are supposed to contain the following columns ['season','month','hour'] and one variable that can
    be windspeed or whatever. You have to specify it in the "feature", standard value is "windspeed".
    Args:
        original (pd.DataFrame): DataFrame of real data with following columns ['season','month','hour'].
        reconstructed (pd.DataFrame):  DataFrame of reconstructed data with following columns ['season','month','hour'].
        feature (str): The column we want to calculate the metric over. Standard to 'windspeed'
        metric (str): Can be one of those ['mean','median','min','max']
    """

    title_font, subtitle_font, labelsize = 18, 15, 12

    original, reconstructed = add_hour_month_season(original.copy()), add_hour_month_season(reconstructed.copy())

    results_first_data = calculate_metrics_byperiod(original, ['season', 'month', 'hour'], [metric], feature)
    results_second_data = calculate_metrics_byperiod(reconstructed, ['season', 'month', 'hour'], [metric], feature)

    color_real = 'black'
    color_synth = '#E32212'

    gs = gridspec.GridSpec(2, 2)
    fig = pl.figure(figsize=(14, 7))
    ax1 = pl.subplot(gs[0, 0])  # row 0, col 0
    ax1.set_title(f'{metric.capitalize()} {feature} per season', fontsize=subtitle_font)
    ax1.set_ylabel(feature.capitalize(), fontsize=labelsize, weight='bold')
    ax1.set_xlabel('Season', fontsize=labelsize, weight='bold')
    pl.plot(results_first_data['season'][metric], color=color_real, linewidth=2, label='Original')
    pl.plot(results_second_data['season'][metric], color=color_synth, linewidth=3, label='Reconstructed')
    pl.xticks(range(1, 5))

    ax2 = pl.subplot(gs[0, 1])  # row 0, col 1
    pl.plot(results_first_data['month'][metric], color=color_real, linewidth=2, label='Original')
    pl.plot(results_second_data['month'][metric], color=color_synth, linewidth=3, label='Reconstructed')
    ax2.set_title(f'{metric.capitalize()} {feature} per month', fontsize=subtitle_font)
    ax2.set_xlabel('Month', fontsize=labelsize, weight='bold')
    ax2.set_ylabel(feature.capitalize(), fontsize=labelsize, weight='bold')
    pl.xticks(range(1, 13))

    ax3 = pl.subplot(gs[1, :])  # row 1, span all columns
    pl.plot(results_first_data['hour'][metric], color=color_real, linewidth=2, label='Original')
    pl.plot(results_second_data['hour'][metric], color=color_synth, linewidth=3, label='Reconstructed')
    ax3.set_xlabel('Hour', fontsize=labelsize, weight='bold')
    ax3.set_ylabel(feature.capitalize(), fontsize=labelsize, weight='bold')
    ax3.set_title(f'{metric.capitalize()} {feature} per hour', fontsize=subtitle_font)
    pl.xticks(range(0, 24))

    tight_layout(pad=5, h_pad=3)
    tick_params(axis='both', labelsize=labelsize)

    fig.suptitle(f'{metric.capitalize()} per season, month and hour', fontsize=title_font, weight='bold')
    show()


def polar_graph(original: DataFrame, reconstructed: DataFrame, title='Polar Graphs of Wind Speed and Direction'):
    """
    Here creates two polar graph side by side. One for the real one for the generated.
    What the function is expecting is 2 dataframes. The columns should be: ['windspeed','winddirection'].
    Also the windspeed is expected to be in km/h. (multiplied by 3.6).
    Args:
        real: pd.DataFrame real one
        generated: pd.Dataframe generated one
    """
    import numpy as np
    real = original.copy()
    generated = reconstructed.copy()

    N = 8
    theta, width = np.linspace(0.0, 2 * np.pi, N, endpoint=False, retstep=True)
    data_theta, _ = np.linspace(0.0, 2 * np.pi, N * 2, endpoint=False, retstep=True)
    windspeed_bins = [0, 1, 5, 12, 19, 28, 38, 50, 999]
    windspeed_labels = ['>0', '>1', '>5', '>12', '>19', '>28', '>38', '>50']
    winddirection_bins = [x for x in range(0, 361, 45)]
    colors = ['#FF7276', '#CB4154', '#b7091d', '#a5081a', '#920717', '#800614', '#6e0511', '#6e0511']

    fig, ax = subplots(1,2, subplot_kw={'projection': 'polar'}, figsize=NOTEBOOK_FIG_SIZE)
    thetagrids(range(0, 360, 45), ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'))
    for i, data in enumerate([real, generated]):
        data.speed = cut(data.speed, bins=windspeed_bins, labels=windspeed_labels)
        data.direction = cut(data.direction, bins=winddirection_bins, labels=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        grouped = data.groupby(['speed', 'direction']).size()
        dataframe_list = [y.reset_index(drop=True) for x, y in grouped.groupby(level=0)]
        bottoms = [x for x in accumulate(dataframe_list)]
        bottoms = deque(bottoms)
        bottoms.appendleft(0)

        for j in range(len(dataframe_list)):
            ax[i].bar(data_theta[1::2], dataframe_list[j], width=width - 0.03, bottom=bottoms[j], color=colors[j],
                   label=windspeed_labels[j])

        ax[i].set_theta_zero_location("N")
        ax[i].set_theta_direction(-1)

    legend(loc='lower center', bbox_to_anchor=(0.8, 1.05), ncol=3, fancybox=True, shadow=True, title = 'Windspeed Groups in km/h')

    ax[0].set_title('Original')
    ax[1].set_title('Reconstructed')
    fig.tight_layout(pad=1.5)
    suptitle(title, fontweight='bold', fontsize=20)
    show()
