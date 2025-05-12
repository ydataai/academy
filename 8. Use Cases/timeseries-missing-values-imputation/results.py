from pandas import DataFrame
from imputation import resample_station_data

class Styling:
  """
  Helper class for print messages.
  """
  PRIORITIES = {
    0: "\u001b[38;5;1m",
    1: "\u001b[38;5;209m",
    2: "\u001b[38;5;11m",
    3: "\u001b[38;5;69m"
  }
  ENDC = '\033[0m'
  BOLD = '\033[1m'

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

    print(f"""\n {Styling.BOLD}Meter Statistics: {Styling.ENDC} \n
        {Styling.PRIORITIES[2]} Date of the first observed value:{Styling.ENDC} {start_date}
        {Styling.PRIORITIES[2]} Missing percentage:{Styling.ENDC} {pct_nan:.2%}
        {Styling.PRIORITIES[2]} Longest consecutive observations:{Styling.ENDC} {max_observed:.0f} days
        {Styling.PRIORITIES[2]} Longest missing period (after start date):{Styling.ENDC} {max_missing:.0f} days \n
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
