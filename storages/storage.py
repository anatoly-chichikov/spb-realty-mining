import abc


class Storage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_data(self):
        raise NotImplementedError

    @abc.abstractmethod
    def write_data(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def append_data(self, data):
        raise NotImplementedError
