import logging

import pandas as pd

from storages.local import CsvStorage

logger = logging.getLogger(__name__)


class MonthlyRent:

    def __init__(self, csv: CsvStorage) -> None:
        self._csv = csv

    def rows(self) -> pd.DataFrame:
        rows = self._csv.read_data()

        return rows[
            (rows['address.district'].isin([
                'петроградский',
                'центральный',
                'адмиралтейский',
                'василеостровский',
                'московский',
                'приморский',
                'выборгский',
                'фрунзенский',
                'калининский',
                'невский',
                'красногвардейский',
                'кировский'
            ])) &
            (rows['type.rooms'] != 'o') &
            (rows['price.period'] == 'monthly') &
            (rows['type.action'] == 'rent_out')
        ]
