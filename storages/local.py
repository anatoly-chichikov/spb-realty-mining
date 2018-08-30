import logging
import os
from typing import Dict, List

import pandas as pd
from pandas.io.json import json_normalize

from storages.abstract import Storage

logger = logging.getLogger(__name__)


class CsvStorage(Storage):

    def __init__(self, file_name: str) -> None:
        self._file_name = file_name

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self._file_name)

    def write_data(self, data_rows: List[Dict]) -> None:
        pd.DataFrame(
            json_normalize(
                data_rows
            )
        ).to_csv(self._file_name, index=False)

    def append_data(self, data: None) -> None:
        raise NotImplementedError

    def clean_data(self) -> None:
        raise NotImplementedError


class FileStorage(Storage):

    def __init__(self, file_name: str) -> None:
        self._file_name = file_name

    def read_data(self) -> List[str]:
        if not os.path.exists(self._file_name):
            raise StopIteration

        with open(self._file_name) as f:
            return [line.strip() for line in f]

    def write_data(self, data_array: List[str]) -> None:
        with open(self._file_name, 'w') as f:
            for line in data_array:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')

    def append_data(self, data: List[str]) -> None:
        with open(self._file_name, 'a') as f:
            for line in data:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')

    def clean_data(self) -> None:
        if os.path.isfile(self._file_name):
            logger.info("Found old crawling data, removing... {}".format(self._file_name))
            os.remove(self._file_name)
