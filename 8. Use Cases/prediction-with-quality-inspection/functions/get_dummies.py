import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class GetDummies(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.columns = None
        
    def fit(self, X, y=None):
        self.columns = pd.get_dummies(X, drop_first=True).columns
        return self

    def transform(self, X):
        X_new = pd.get_dummies(X, drop_first=True)
        return X_new.reindex(columns=self.columns, fill_value=0)