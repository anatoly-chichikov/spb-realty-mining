from parsers.parser import Parser


class FilterParser(Parser):
    """This is example class. There is no big purpose for it"""

    def parse(self, data):
        """
        Filter input data with only desired fields
        :param data: dictionary of a lot of things
        :return: list of dictionaries where key is one of
        defined fields and value is this field's value
        """
        return [{k: v for k, v in data.items() if k in self.fields_set}]
