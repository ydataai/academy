
from pandas import DataFrame
from ydata.connectors import GCSConnector
from imputation import resample_station_data


def meter_statistics(original: DataFrame, feature: str = 'speed'):
    
    # Calculate the date of first meter reading
    start_date = original.dropna().index.min()

    # Percentage of NaNs from training data
    full_year = resample_station_data(original)[feature]
    pct_nan = full_year.isna().sum() / len(full_year)
    
    # Longest consecutive observations (in days)
    feat = full_year[full_year.index > start_date]
    obs_groups = feat.isna().cumsum()[feat.notna()]
    max_observed = obs_groups.groupby(obs_groups).agg(len).max() / 24

    # Longest missing after start_date
    na_groups = feat.notna().cumsum()[feat.isna()]
    max_missing = na_groups.groupby(na_groups).agg(len).max() / 24

    #return start_date, pct_nan, max_observed, max_missing

    print(f"""Meter Statistics:
    First observed value: {start_date}
    Missing percentage: {pct_nan:.2%}
    Longest consecutive observations: {max_observed:.1f}
    Longest missing period (after start date): {max_missing:.1f}
    """)


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
