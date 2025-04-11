import unittest
from core import some_function, SomeClass

class TestCore(unittest.TestCase):

    def test_some_function(self):
        # Test some_function with a sample input and expected output
        input_data = 'sample input'
        expected_output = 'expected output'
        result = some_function(input_data)
        self.assertEqual(result, expected_output)

    def test_some_function_with_edge_case(self):
        # Test some_function with an edge case
        input_data = 'edge case input'
        expected_output = 'edge case output'
        result = some_function(input_data)
        self.assertEqual(result, expected_output)

    def test_some_class_method(self):
        # Test a method from SomeClass
        obj = SomeClass()
        input_data = 'method input'
        expected_output = 'method output'
        result = obj.some_method(input_data)
        self.assertEqual(result, expected_output)

    def test_some_class_initialization(self):
        # Test the initialization of SomeClass
        obj = SomeClass('init param')
        self.assertEqual(obj.param, 'init param')

if __name__ == '__main__':
    unittest.main()