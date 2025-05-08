"""
    Utilities for Imputation of Missing Values.
"""

from typing import List, Optional

from pandas import DataFrame, Grouper, Timestamp, concat, date_range
from ydata.dataset import Dataset
from ydata.preprocessing.scaling import NumericalFactors
from ydata.utils.formats import read_json
from numpy import nan

# Preprocessing

def resample(df: DataFrame, ts_col: str, ts_freq: str, partition_by: Optional[str] = None):
        """Resample a DataFrame for a specific frequency. Combined resampled with entity is optional.

        Args:
            df (DataFrame)
            ts_col (str): timestamp column
            ts_freq (str): timestamp frequency for which to resample
            partition_by (str): entity column

        Returns:
            df (DataFrame): indexed by timestamp
        """
        if partition_by is not None:
            df = ( df
                .copy().sort_values(by=[partition_by, ts_col])

                .reset_index().set_index([partition_by, ts_col])
                .groupby( [ Grouper(level=partition_by), Grouper(level=ts_col, freq=ts_freq)])
                .mean()
                .sort_index().reset_index(level=partition_by)
            )
        else:
            df = ( df
                .copy().sort_values(by=[ts_col])
                .reset_index().set_index([ts_col])
                .groupby( [Grouper(level=ts_col, freq=ts_freq) ] )
                .mean().sort_index()
                )
        return df

def resample_station_data(df: DataFrame, partition_by: str = 'station', start_ts='2020-09-01', end_ts='2021-09-01', ts_freq='H'):
    """Resamples the data for each device with missing and observed values.

    Steps:
        1. For each device, creates a full sequence between start_ts and end_ts by a given frequency ts_freq
        2. Resamples the original data for the same frequency
        3. Joins the observed values when available.
    """

    def create_timeseries_index(start_ts: str, end_ts: str, freq: str = 'H'):
        "Generates a DatetimeIndex from start_ts to end_ts, with given frequency."
        start_ts, end_ts = Timestamp(start_ts), Timestamp(end_ts)
        index = date_range(start=start_ts, end=end_ts, freq=freq)
        index.name = 'timestamp'
        return index

    index = create_timeseries_index(start_ts=start_ts, end_ts=end_ts)

    # Create a DataFrame of all partitions with the full index
    all_data = []
    for partition in sorted(set(df[partition_by])):
        full = DataFrame(index=index)
        full['station'] = partition
        all_data.append(full)
    data = concat(all_data).reset_index().set_index(['timestamp', 'station'])

    # Resample the original values
    resampled = resample(df, partition_by=partition_by, ts_col='timestamp', ts_freq=ts_freq).reset_index().set_index(['timestamp','station'])
    data = data.join(resampled).reset_index().set_index('timestamp')
    return data

def data_boundaries(data: DataFrame, replace_na=False):
    "Ensures data boundaries on windspeed and winddirection."
    df = data.copy()

    df.loc[df['speed'] < 0, 'speed'] = nan if replace_na else 0    # guarantees speed is not negative
    df.loc[df['speed'] > 20, 'speed'] = nan if replace_na else 20  # maximum windspeed
    df.loc[df['direction'] > 360, 'direction'] = nan if replace_na else 360
    df.loc[df['direction'] < 0, 'direction'] = nan if replace_na else 0
    return df

def resample(df: DataFrame, ts_col: str, ts_freq: str, partition_by: Optional[str] = None):
        """Resample a DataFrame for a specific frequency. Combined resampled with entity is optional.

        Args:
            df (DataFrame)
            ts_col (str): timestamp column
            ts_freq (str): timestamp frequency for which to resample
            partition_by (str): entity column

        Returns:
            df (DataFrame): indexed by timestamp
        """
        if partition_by is not None:
            df = ( df
                .copy().sort_values(by=[partition_by, ts_col])

                .reset_index().set_index([partition_by, ts_col])
                .groupby( [ Grouper(level=partition_by), Grouper(level=ts_col, freq=ts_freq)])
                .mean()
                .sort_index().reset_index(level=partition_by)
            )
        else:
            df = ( df
                .copy().sort_values(by=[ts_col])
                .reset_index().set_index([ts_col])
                .groupby( [Grouper(level=ts_col, freq=ts_freq) ] )
                .mean().sort_index()
                )
        return df

def resample_station_data(df: DataFrame, partition_by: str = 'station', start_ts='2020-09-01', end_ts='2021-09-01', ts_freq='H'):
    """Resamples the data for each device with missing and observed values.

    Steps:
        1. For each device, creates a full sequence between start_ts and end_ts by a given frequency ts_freq
        2. Resamples the original data for the same frequency
        3. Joins the observed values when available.
    """

    def create_timeseries_index(start_ts: str, end_ts: str, freq: str = 'H'):
        "Generates a DatetimeIndex from start_ts to end_ts, with given frequency."
        start_ts, end_ts = Timestamp(start_ts), Timestamp(end_ts)
        index = date_range(start=start_ts, end=end_ts, freq=freq)
        index.name = 'timestamp'
        return index

    index = create_timeseries_index(start_ts=start_ts, end_ts=end_ts)

    # Create a DataFrame of all partitions with the full index
    all_data = []
    for partition in sorted(set(df[partition_by])):
        full = DataFrame(index=index)
        full['station'] = partition
        all_data.append(full)
    data = concat(all_data).reset_index().set_index(['timestamp', 'station'])

    # Resample the original values
    resampled = resample(df, partition_by=partition_by, ts_col='timestamp', ts_freq=ts_freq).reset_index().set_index(['timestamp','station'])
    data = data.join(resampled).reset_index().set_index('timestamp')
    return data

def data_boundaries(data: DataFrame, replace_na=False):
    "Ensures data boundaries on windspeed and winddirection."
    df = data.copy()

    df.loc[df['speed'] < 0, 'speed'] = nan if replace_na else 0    # guarantees speed is not negative
    df.loc[df['speed'] > 20, 'speed'] = nan if replace_na else 20  # maximum windspeed
    df.loc[df['direction'] > 360, 'direction'] = nan if replace_na else 360
    df.loc[df['direction'] < 0, 'direction'] = nan if replace_na else 0
    return df


# Factors
def load_factors(fpath):
    "Loads factors from a JSON into a NumericalFactors."
    def keys_as_ints(d: dict):
        "Cast dictionary keys as integers."
        return {int(k): v for (k, v) in d.items()}

    if isinstance(fpath, str):
      factors = read_json(fpath)
    else:
      factors = fpath

    factors = {k: keys_as_ints(v) for (k,v) in factors.items()}  # cast keys of month to integers
    nf = NumericalFactors(groupby='month', factors=factors)
    return nf


# Cold Start

def get_cold_start_meters(data: DataFrame):
    "Returns a list of meters without observed values"
    nan_count = data.groupby('station').agg(['count']).sum(axis=1)
    return nan_count[nan_count==0].index.to_list()

def get_proxy_data(proxy_stations: dict, data: DataFrame) -> dict:
    "Returns a dict mapping of cold-start station to a DataFrame of proxy_data."
    proxy_data = {}
    for cold_start_meter, proxy_meters in proxy_stations.items():
        proxy_data[cold_start_meter] = data[data['station'].isin(proxy_meters)]
    return proxy_data

