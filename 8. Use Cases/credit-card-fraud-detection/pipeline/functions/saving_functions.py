import pickle
from typing import Union
import pathlib
import os

def save_file(file, file_path: Union[str, pathlib.Path]):
    #file_path.parent.mkdir(exist_ok=True, parents=True)
    with open(file_path, 'w+b') as pickle_file:
        pickle.dump(file, pickle_file)


def read_file(file_path: Union[str, pathlib.Path]):
    with open(file_path, "rb") as handle:
        return pickle.load(handle)