import Algorithmia
import numpy as np
import pandas as pd
import joblib
from xgboost import XGBClassifier


client = Algorithmia.client()
    
def load_model():
    # Get file by name
    # Open file and load model
    file_path = 'data://rujual/ydata_demo/xgb_with_synth.joblib'
    model_path = client.file(file_path).getFile().name
    
    # # Open file and load model
    
    with open(model_path, 'rb') as f:
         model = joblib.load(f)
         print("model loaded")
    
    #model = joblib.load(model_path)
    return model
    
model = load_model()


def process_input(input):
    # Create numpy array from csv file passed as input in apply()
    
    file_url=str(input)
    
    if input.startswith('data:'):
        file_url = client.file(input).getFile().name
        
    return pd.read_csv(file_url)


def apply(input):
    data_sample = process_input(input)
    prediction = model.predict(data_sample)
    
    if(list(prediction)[0] == 1):
        return "Fraud"

    return "Genuine"