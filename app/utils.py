import sys
import os
from pathlib import Path


tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))


from pandas.core.frame import DataFrame
import chardet
import pandas as pd


def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as rawdata:
        result = chardet.detect(rawdata.read(10000))
    return result["encoding"]


def overwrite_file(
    file_path: str, data_frame: DataFrame, new_file_name: str = None
) -> str:
    os.remove(file_path)
    if new_file_name:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_file_name)
    else:
        new_file_path = file_path
    data_frame.to_csv(new_file_path, sep="\t", index=False)

    return new_file_path


def filter(file_path: str, encoding: str, column: str, expected: str) -> DataFrame:
    data_frame = pd.read_csv(file_path, encoding=encoding, sep="\t")
    return data_frame[data_frame[column] == expected]
