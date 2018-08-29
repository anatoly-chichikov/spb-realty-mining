import logging
import os

from storages.storage import Storage

logger = logging.getLogger(__name__)


class FileStorage(Storage):

    def __init__(self, file_name):
        self._file_name = file_name

    def read_data(self):
        if not os.path.exists(self._file_name):
            raise StopIteration

        with open(self._file_name) as f:
            for line in f:
                yield line.strip()

    def write_data(self, data_array):
        with open(self._file_name, 'w') as f:
            for line in data_array:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')

    def append_data(self, data):
        with open(self._file_name, 'a') as f:
            for line in data:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')

    def clean_data(self):
        if os.path.isfile(self._file_name):
            logger.info("Found old crawling data, removing... {}".format(self._file_name))
            os.remove(self._file_name)
