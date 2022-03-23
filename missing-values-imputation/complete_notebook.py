import matplotlib.gridspec as gridspec
import matplotlib.pylab as pl
from matplotlib.pyplot import (legend, subplots, suptitle, tick_params,
                               tight_layout, thetagrids, show)
from pandas import DataFrame, cut

def add_hour_month_season(data):
    data['hour'] = data.index.hour
    data['month'] = data.index.month
    data['season'] = (data['month'] % 12 + 3) // 3
    return data

def calculate_metrics_byperiod(df, agg_col: list, metrics: list, col_to_group='speed'):
    results = dict()
    for col in agg_col:
        results[col] = dict()
        for metric in metrics:
            if metric == 'mean':
                agg_df = df.groupby(col).mean()[[col_to_group]]
            elif metric == 'max':
                agg_df = df.groupby(col).max()[[col_to_group]]
            elif metric == 'min':
                agg_df = df.groupby(col).min()[[col_to_group]]
            elif metric == 'median':
                agg_df = df.groupby(col).median()[[col_to_group]]
            else:
                raise ValueError('The provided metric is not supported.')

            results[col][metric] = agg_df
    return results

from itertools import accumulate
from collections import deque

NOTEBOOK_FIG_SIZE = (24,7)


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
    pl.legend()

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



if __name__ == '__main__':
    import pandas as pd

    train = pd.read_csv(r'C:\Users\SpamU\Documents\GitHub\academy\missing-values-imputation\train_allmeters.csv', index_col=0)
    train.index = pd.DatetimeIndex(train.index)
    reconstructed = pd.read_csv(r'C:\Users\SpamU\Documents\GitHub\academy\missing-values-imputation\whole_year_reconstructed.csv', index_col=0)
    reconstructed.index = pd.DatetimeIndex(reconstructed.index)

    list(set(train.station))
    plot_metric_byperiod(train[train['station']=='kebribeyah'], reconstructed[reconstructed['station']=='kebribeyah'])
