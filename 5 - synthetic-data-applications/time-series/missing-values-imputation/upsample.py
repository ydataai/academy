"""
    Utilities for upsampling temporal data.
"""

from pandas import DataFrame, date_range, concat
from ydata.utils.upsampling import random_walk_upsample

def upsample_stations(data: DataFrame):
    "From a DataFrame of stations and (windspeed, winddirection) measurements, converts from hourly to 15minutes frequency."
    upsampled = []
    for device, device_data in data.groupby('station'):
        values_ = random_walk_upsample(device_data[['speed', 'direction']], n_upsample=3)  # upsample numericals only
        # index is similar to original but with higher frequency
        values_.index = date_range(start=device_data.index.min(), end=device_data.index.max(), freq='15T', name='timestamp')
        values_['station'] = device                                         # restore device info
    upsampled.append(values_[['station', 'speed', 'direction']])    # ensure order   
    return concat(upsampled)