import logging
from typing import List, Dict

from bs4 import BeautifulSoup

from parsers.pin7_cleanings import clean_row
from storages.local import FileStorage, CsvStorage

logger = logging.getLogger(__name__)


class ParsedPages:

    def __init__(self, file: FileStorage, csv: CsvStorage) -> None:
        self._file = file
        self._csv = csv

    def save(self) -> None:
        result = []

        for row in self._file.read_data():
            (url, text) = row.split('\t')

            result.extend(
                PinPage(url, text).rows()
            )

        logger.info("All pages have been parsed: {} rows found".format(len(result)))

        self._csv.write_data(result)


class PinPage:

    def __init__(self, url: str, page: str) -> None:
        self._url = url
        self._page = page

    def rows(self) -> List[Dict]:
        result = []

        soup = BeautifulSoup(self._page, 'html.parser')

        for br in soup.find_all("br"):
            br.replace_with("\n")

        rows = soup.select('tr[class^="trm_0"]')
        number = 1

        for row in rows:
            try:
                result.append(clean_row(row))
                number += 1
            except Exception as e:
                logger.exception('Failed on %s. Row %s. %s', self._url, number, str(e))
                logger.error(row)

        logger.info("Url parsed: {}, found rows: {}".format(self._url, len(result)))

        return result
