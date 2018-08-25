import os

from storages.storage import Storage


class FileStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        if not os.path.exists(self.file_name):
            raise StopIteration

        with open(self.file_name) as f:
            for line in f:
                yield line.strip()

    def write_data(self, data_array):
        """
        :param data_array: collection of strings that
        should be written as lines
        """
        with open(self.file_name, 'w') as f:
            for line in data_array:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')

    def append_data(self, data):
        """
        :param data: string
        """
        with open(self.file_name, 'a') as f:
            for line in data:
                if line.endswith('\n'):
                    f.write(line)
                else:
                    f.write(line + '\n')
