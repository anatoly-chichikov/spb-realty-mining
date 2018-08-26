import logging

from scrapy import Request
from scrapy.spiders import CrawlSpider

logger = logging.getLogger(__name__)


class Scrapper(CrawlSpider):
    name = 'realty-spb'

    allowed_domains = ['pin7.ru']
    start_urls = ['https://pin7.ru/online.php']

    page = 0

    def __init__(self, *a, **kw):
        self.pcode = kw['cookie']
        self.storage = kw['storage']
        super().__init__(*a, **kw)

    def parse(self, response):
        data = response.text

        if self.page > 0:
            result = [response.url + '\t' + data.replace('\n', '').replace('\r', '')]
            self.storage.append_data(result)

        self.page += 1

        return Request(
            url='https://pin7.ru/online.php?numpage=' + str(self.page),
            cookies={"pcode": self.pcode},
            callback=self.parse
        )
