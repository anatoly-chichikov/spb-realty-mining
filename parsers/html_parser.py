from parsers.parser import Parser

from bs4 import BeautifulSoup  # You can use any other library


class HtmlParser(Parser):

    def parse(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data)

        # Your code here: find an appropriate html element
        objects_list = soup.find('div', {'class': 'itemsList'})

        # Your code here
        return [dict()]
