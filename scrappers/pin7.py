import logging

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import CrawlSpider

logger = logging.getLogger(__name__)


class CrawlingTask:

    def __init__(self, storage, process):
        self._storage = storage
        self._process = process

    def await(self, cookie):
        self._process.crawl(PinSpider, cookie=cookie, storage=self._storage)
        self._process.start()


class PinSpider(CrawlSpider):
    name = 'realty-spb'

    allowed_domains = ['pin7.ru']
    start_urls = ['https://pin7.ru/online.php']

    _next = 0

    def __init__(self, *a, **kw):
        self._pcode = kw['cookie']
        self._storage = kw['storage']
        super().__init__(*a, **kw)

    def parse(self, response):
        data = response.text

        if self._next > 0:
            total = self._valid_total(data, response.url)

            if total < self._next:
                return

            self._storage.append_data([
                response.url + '\t' + data.replace('\n', '').replace('\r', '').replace('\t', ' ')
            ])
        else:
            self._storage.clean_data()

        self._next += 1

        return Request(
            url='https://pin7.ru/online.php?numpage=' + str(self._next),
            cookies={"pcode": self._pcode},
            callback=self.parse
        )

    def _valid_total(self, data, url):
        nav_blocks = BeautifulSoup(data, 'html.parser').select("table.tb_navi")

        if not nav_blocks:
            logger.error("{}".format(data))
            raise IOError("Invalid page: {}, no navigation blocks".format(url))

        all_nums = []

        for href in nav_blocks[0].select("a"):
            try:
                all_nums.append(int(href.getText()))
            except ValueError:
                pass

        total = max(all_nums)

        logger.info("Page valid: {}. {} pages left".format(url, total - self._next))

        return total
