import json

def save_json(data, fpath):
    "Stores data as a JSON in the provided filepath."
    with open(fpath, 'w') as f:
        json.dump(data, f)