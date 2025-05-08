import os
import json
from pathlib import Path
import importlib

BASE_PATH = Path(os.environ.get('PIPELINE_MOUNT', './'))

CREDENTIAL_FOLDER = "HACK ME VIA ENV VARIABLE"
CREDENTIALS_PATH = Path(CREDENTIAL_FOLDER) / "gcs_credentials.json"

OUTPUT_PATH = BASE_PATH / 'output'
DATASET_PATH = BASE_PATH / 'output/datasets'
SAMPLES_PATH = BASE_PATH / 'output/samples'
MODELS_PATH = BASE_PATH / 'output/models'
ANALYSIS_PATH = BASE_PATH / 'output/analysis'
ANALYSIS_RAW_PATH = BASE_PATH / 'output/analysis/raw'
ANALYSIS_REPORTS_PATH = BASE_PATH / 'output/analysis/reports'
ANALYSIS_PLOTS_PATH = BASE_PATH / 'output/analysis/plots'
DOWNLOADED_DATASETS = BASE_PATH / 'input/datasets'
CONFIG_PATH = BASE_PATH / 'config'

ALL_FOLDERS = [CONFIG_PATH, DATASET_PATH, MODELS_PATH, DOWNLOADED_DATASETS, SAMPLES_PATH, ANALYSIS_PATH, ANALYSIS_RAW_PATH, ANALYSIS_REPORTS_PATH, ANALYSIS_PLOTS_PATH]

def create_experiment_folders(folders=ALL_FOLDERS):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
def load_config(config_path):
    f = open(config_path)
    return json.load(f)
    
def get_datsets_config(config_path = Path(CONFIG_PATH) / 'datasets.json'):
     return load_config(config_path)
    
def get_models_config(config_path = Path(CONFIG_PATH) / 'models.json'):
     return load_config(config_path)
    
def get_analysis_config(config_path = Path(CONFIG_PATH) / 'analysis.json'):
    data = load_config(config_path)
    for k, v in data['output_files'].items():
        data['output_files'][k] = BASE_PATH / v
    return data
    
def get_metrics_config(config_path = Path(CONFIG_PATH) / 'metrics.json'):
    from ydata.utils.data_types import DataType
    metrics_config = load_config(config_path)
    for nbundle, bundle in  metrics_config.items():
        for ntype, type_data in bundle.items():
            for k, v in type_data['metrics'].items():
                module_path, cls_name =  v['class'].rsplit('.', 1)
                v['class'] = getattr(importlib.import_module(module_path), cls_name)
                if 'datatype' in v:
                    v['datatype'] = DataType[v['datatype'].upper()]
    return metrics_config