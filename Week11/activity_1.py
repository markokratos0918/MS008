#Develop a test unit for the *, -, / and % functions

import unittest

def add(x, y):
    '''Add two numbers'''
    return x + y
def subtract(x, y):
    '''Subtract two numbers'''
    return x - y
def multiply(x, y):
    '''Multiply two numbers'''
    return x * y
def divide(x, y):

    '''Divide two numbers'''
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
class TestMathOperations(unittest.TestCase):
    def test_add(self):
        '''Test addition'''
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    def test_subtract(self):
        '''Test subtraction'''
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 1), -1)
    def test_multiply(self):
        '''Test multiplication'''
        self.assertEqual(multiply(4, 3), 12)
        self.assertEqual(multiply(-1, 5), -5)
    def test_divide(self):
        '''Test division'''
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(5, 2), 2.5)
        with self.assertRaises(ValueError):
            divide(5, 0)

if __name__ == '__main__':
      unittest.main()