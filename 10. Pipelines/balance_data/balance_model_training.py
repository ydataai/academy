import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
#Using XGBOOST model to train the model
from xgboost import XGBClassifier

from sklearn.metrics import (f1_score, precision_score, recall_score, roc_auc_score, accuracy_score)

from sklearn.model_selection import train_test_split

from ydata.metadata import Metadata
from ydata.dataset import Dataset

from ydata.synthesizers.regular import RegularSynthesizer

def augment_minority(X: pd.DataFrame, sample_size:int ,label:str, train: True) -> pd.DataFrame:
    aux_X = X.copy()
    min_X = aux_X[aux_X[label]==1].drop(label, axis=1)
    
    print(min_X.shape)
    
    dataset = Dataset(min_X)
    metadata = Metadata(dataset)

    if train:
        synth = RegularSynthesizer()
        synth.fit(dataset, metadata)
        synth.save('synth')
    else:
        synth=RegularSynthesizer.load('synth')
        
    synth_sample = synth.sample(sample_size)
    synth_sample = synth_sample.to_pandas()
    
    synth_sample[label] = 1
    aug_data = pd.concat([synth_sample, X], axis=0)
    return aug_data.drop(label, axis=1), aug_data[label]

def train_model(X: pd.DataFrame, 
                label:str, 
                augmentation=True,
                train_synth:bool=True,
                sample_size: int = None) -> pd.DataFrame:
    
    print(sample_size)
    
    y = X[label]
    X = X.drop(label, axis=1)
    
    X_train, X_test, y_train,y_test = train_test_split(X, y, test_size=0.20, shuffle=True)
    
    if augmentation:
        X_train[label] = y_train
        if sample_size is None or sample_size==0:
            sample_size = len(X_train[X_train[label]==0])-len(X_train[X_train[label]=='1'])
        X_train, y_train = augment_minority(X_train, sample_size=sample_size, label=label, train=train_synth)
    
    print(f'Size training: {len(X_train)}')
    print(f'Size test: {len(X_test)}')
    
    models=[DummyClassifier(), RandomForestClassifier(), AdaBoostClassifier(), XGBClassifier()]

    results = []
    trained_models = {}

    for model in models:
        model_name = type(model).__name__
        print(f'Model training: {model_name}')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        trained_models[model_name] = model
        results.append({'model': model_name, 
                      'f1_score': f1_score(y_test, y_pred),
                      'recall': recall_score(y_test, y_pred),
                      'precision': precision_score(y_test, y_pred),
                      'roc_auc': roc_auc_score(y_test, y_pred),
                      'accuracy': accuracy_score(y_test, y_pred)})
    return pd.DataFrame(results), trained_models, sample_size