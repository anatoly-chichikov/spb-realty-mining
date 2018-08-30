import abc
from typing import Any


class Storage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_data(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def write_data(self, data: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def append_data(self, data: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clean_data(self) -> None:
        raise NotImplementedError
