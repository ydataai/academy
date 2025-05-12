import pandas as pd
from pickle import load, dump

#Function to load the training set
def load_sets(path: str):
    with open(path, 'rb') as f:
        return load(f)
    
def pickle_sets(df: pd.DataFrame, y: pd.Series, path:str):
    dataset = (df, y)
    
    with open(path, 'wb') as f:
        dump(dataset, f)