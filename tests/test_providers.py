import unittest
from providers import DataProvider

class TestDataProvider(unittest.TestCase):

    def setUp(self):
        self.provider = DataProvider()

    def test_initialization(self):
        self.assertIsInstance(self.provider, DataProvider)

    def test_get_data(self):
        data = self.provider.get_data()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)

    def test_data_content(self):
        data = self.provider.get_data()
        if data:
            self.assertTrue(all(isinstance(item, dict) for item in data))

    def test_data_format(self):
        data = self.provider.get_data()
        if data:
            for item in data:
                self.assertIn('id', item)
                self.assertIn('value', item)

    def test_data_values(self):
        data = self.provider.get_data()
        if data:
            for item in data:
                self.assertIsInstance(item['id'], int)
                self.assertIsInstance(item['value'], (int, float, str))

if __name__ == '__main__':
    unittest.main()