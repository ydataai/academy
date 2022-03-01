from ydata.dataset import Dataset


def preprocess_data(data: Dataset):
    return (data
        .to_pandas()
        .astype({'timestamp': 'datetime64[ns]'})
        .set_index('timestamp').sort_values(by=['timestamp', 'station'])
    )
