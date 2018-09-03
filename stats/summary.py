import abc
import logging
from typing import Iterable

logger = logging.getLogger(__name__)


class Summary(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stats(self) -> None:
        raise NotImplementedError


class Statistics:

    def __init__(
            self,
            summaries: Iterable[Summary],
    ) -> None:
        self._summaries = summaries

    def print(self) -> None:
        logger.info('АРЕНДА В САНКТ-ПЕТЕРБУРГЕ')

        for summary in self._summaries:
            logger.info('======================================>>>')
            summary.stats()
