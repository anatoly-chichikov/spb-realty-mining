import logging

import pandas as pd
from pandas.io.json import json_normalize

from storages.storage import Storage

logger = logging.getLogger(__name__)


class CsvStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        return pd.read_csv(self.file_name)

    def write_data(self, data_rows):
        """
        :param data_rows: collection of dicts that
        should be written as csv rows
        """
        pd.DataFrame(
            json_normalize(
                data_rows
            )
        ).to_csv(self.file_name, index=False)

    def append_data(self, data):
        raise NotImplementedError

    def clean_data(self):
        raise NotImplementedError
