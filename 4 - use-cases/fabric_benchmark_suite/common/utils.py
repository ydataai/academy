from typing import Optional
from collections import defaultdict
import collections.abc
import importlib
import json
from pandas import read_csv
from pathlib import Path
from common.config import get_models_config, get_metrics_config, DATASET_PATH

def ndd():
    return defaultdict(ndd)

def ndd_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: ndd_to_dict(v) for k, v in d.items()}
    return d

def get_model_class(name):
    models_config = get_models_config()
    c = models_config[name]['class']
    module_path, cls_name = c.rsplit('.', 1)
    return get_class(module_path, cls_name)

def get_metric_class(name):
    metrics_config = get_metrics_config()
    c = metrics_config[name]['class']
    module_path, cls_name = c.rsplit('.', 1)
    return get_class(module_path, cls_name)

def get_class(path, class_):
    return getattr(importlib.import_module(path), class_)

def deep_update(mapping, *updating_mappings):
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping

def update_json_file(path, patch):
    from common.config import BASE_PATH
    p = Path(BASE_PATH) / path
    try:
        with open(p, 'r') as f:
            data = json.load(f)
    except Exception as e:
        data = {}
    if patch != {}:
        updated = deep_update(data, patch)
        with open(p, 'w') as f:
            f.write(json.dumps(updated, indent=4))

def load_dataframe(name: str, split: Optional[str] = None):
    if split is None:
        return read_csv(Path(DATASET_PATH) / f'{name}.csv')
    return read_csv(Path(DATASET_PATH) / f'{name}_{split}.csv')