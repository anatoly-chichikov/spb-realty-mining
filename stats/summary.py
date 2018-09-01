import logging

import pandas as pd

from stats.filters import MonthlyRent
from stats.formatters import flat, price, square

logger = logging.getLogger(__name__)


class Statistics:

    def __init__(self, monthly: MonthlyRent) -> None:
        self._monthly = monthly

    def print(self) -> None:
        rows = self._monthly.rows()

        logger.info('АРЕНДА В САНКТ-ПЕТЕРБУРГЕ')

        self._general(rows)
        self._prices(rows)
        self._squares(rows)

    @staticmethod
    def _general(rows: pd.DataFrame) -> None:
        logger.info('> Общая информация:')
        logger.info('===> Всего предложений - %s', flat(len(rows)))
        logger.info('===> Комнаты - %s', flat(len(rows[rows['type.rooms'].isin(['r1', 'r2', 'r3'])])))
        logger.info('===> Однокомнатные и студии - %s', flat(len(rows[rows['type.rooms'].isin(['f1', 's'])])))
        logger.info('===> Двухкомнатные - %s', flat(len(rows[rows['type.rooms'].isin(['f2'])])))
        logger.info('===> Три и более комнат - %s', flat(len(rows[rows['type.rooms'].isin(['f3', 'f4', 'f5+'])])))
        logger.info('===> В новостройках - %s', flat(len(rows[(rows['options.house_state'] == 'new')])))
        logger.info('===> С хорошим ремонтом - %s', flat(len(rows[(rows['options.cool_renovation'] == True)])))
        logger.info('===> Можно с детьми - %s', flat(len(rows[(rows['options.allowed_children'] == True)])))
        logger.info('===> Можно с животными - %s', flat(len(rows[(rows['options.allowed_pets'] == True)])))

    @staticmethod
    def _prices(rows: pd.DataFrame) -> None:
        valuable = rows[rows['price.amount'] > 0.]['price.amount']

        logger.info('> Цена:')
        logger.info('===> Минимально возможная цена - %s', price(valuable.min()))
        logger.info('===> Максимальная цена - %s', price(valuable.max()))
        logger.info('===> Средняя цена - %s', price(valuable.mean()))
        logger.info('===> Половина предложений дешевле - %s', price(valuable.median()))
        logger.info('===> Большая часть (90%%) дешевле - %s', price(valuable.quantile(.9)))
        logger.info('===> Большая часть (90%%) дороже - %s', price(valuable.quantile(.1)))

    @staticmethod
    def _squares(rows: pd.DataFrame) -> None:
        valuable = rows[rows['options.size'] > 0.]['options.size']

        logger.info('> Площадь:')
        logger.info('===> Минимально возможная площадь - %s', square(valuable.min()))
        logger.info('===> Максимальная площадь - %s', square(valuable.max()))
        logger.info('===> Средняя площадь - %s', square(valuable.mean()))
        logger.info('===> Половина предложений меньше - %s', square(valuable.median()))
        logger.info('===> Большая часть (90%%) меньше - %s', square(valuable.quantile(.9)))
        logger.info('===> Большая часть (90%%) больше - %s', square(valuable.quantile(.1)))
