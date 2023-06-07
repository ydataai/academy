from ydata.metadata import Metadata
from ydata.dataset import Dataset
from ydata.utils.data_types import DataType
from typing import List, Tuple
from pandas import DataFrame as pdDataFrame
import pandas as pd


# Import Preprocessing Functionality
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    LabelEncoder,
    OrdinalEncoder,
)

def get_target_and_predictor_variables(df: pdDataFrame, target_variable: str) -> Tuple:
    if target_variable in df.columns:
        target_variable = df.pop(target_variable).to_numpy()
        return target_variable, df.to_numpy()


def remove_columns(metadata, dataset, unwanted_columns) -> Tuple[Metadata, Dataset]:
    sel_columns = list(set(metadata.columns) - set(unwanted_columns))
    return metadata[sel_columns], dataset[sel_columns]


def get_datatypes(metadata) -> dict:
    return {k: v.datatype for k, v in metadata.columns.items()}

def split_X_target(dataset, metadata, target):
    pred_cols = [col for col in metadata.columns if col != target]
    X = dataset.to_pandas()
    X = X.dropna(0)
    target = X[target]
    X = X[pred_cols]
    
    metadata = metadata[pred_cols]
    return X, target, metadata

def transform_features(df, metadata):

    ct = ColumnTransformer(
        [
            (
                "hotencoder",
                OneHotEncoder(drop="if_binary"),
                metadata.categorical_vars,
            ),
            (
                "scaler",
                StandardScaler(),
                metadata.numerical_vars,
            ),
        ],
        remainder="passthrough",
    )

    transformed_df = ct.fit_transform(df)
    
    return transformed_df, ct
