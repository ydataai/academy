from ydata.dataset import Dataset

def preprocess_data(df: Dataset):
    assert isinstance(df, Dataset), "Provided arguments should be of Dataset type."

    # Data Types
    DTYPES = {
    'station': 'str',
    'timestamp': 'datetime64[ns]',
    'speed': 'float',
    'direction': 'float'
    }

    # Subset relevant columns
    df = df.select_columns(list(DTYPES.keys()))

    # Convert to pandas and cast to correct data types
    df = df.to_pandas().astype(DTYPES)
    
    # Drop duplicates
    df = df.drop_duplicates()

    # Sort and set index, sort columns
    df = df.sort_values(by=['timestamp', 'station']).set_index('timestamp')
    df = df[['station', 'speed', 'direction']]

    # Split into train and holdout
    train = df[(df.index >= '2020-11-26') & (df.index < '2021-09-01')]
    holdout = df[df.index >= '2021-09-01']

    return train, holdout