import unittest

from parsers.filter_parser import FilterParser


class TestFilterParser(unittest.TestCase):
    def test_parse(self):
        parser = FilterParser(['1', '3', '5'])
        parsed_data = parser.parse({'1': 1, '2': 2, '3': 3, '4': 4, '5': 5})
        self.assertEqual(len(parsed_data), 1)
        self.assertDictEqual(parsed_data[0], {'1': 1, '3': 3, '5': 5})


class TestHtmlParser(unittest.TestCase):

    def test_parse(self):
        # Your code here
        pass


if __name__ == '__main__':
    unittest.main()
