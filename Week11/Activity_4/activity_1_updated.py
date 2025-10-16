"""
Week 11 - Activity 4: Implementing Doctest and Unittest in Python
Due date: 17.10.25 at midnight

Hybrid testing implementation combining unittest and doctest for comprehensive coverage.
"""

import unittest
import doctest
def add(x, y):
    """
    Add two numbers together.
    
    Args:
        x: First number
        y: Second number
    
    Returns:
        Sum of x and y
    
    Examples:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
        >>> add(0, 0)
        0
        >>> add(10.5, 2.5)
        13.0
    """
    return x + y


def subtract(x, y):
    """
    Subtract y from x.
    
    Args:
        x: Number to subtract from
        y: Number to subtract
    
    Returns:
        Difference of x and y
    
    Examples:
        >>> subtract(5, 3)
        2
        >>> subtract(0, 1)
        -1
        >>> subtract(10, 10)
        0
        >>> subtract(-5, -3)
        -2
    """
    return x - y


def multiply(x, y):
    """
    Multiply two numbers.
    
    Args:
        x: First number
        y: Second number
    
    Returns:
        Product of x and y
    
    Examples:
        >>> multiply(4, 3)
        12
        >>> multiply(-1, 5)
        -5
        >>> multiply(0, 100)
        0
        >>> multiply(2.5, 4)
        10.0
    """
    return x * y


def divide(x, y):
    """
    Divide x by y.
    
    Args:
        x: Numerator
        y: Denominator
    
    Returns:
        Quotient of x and y
    
    Raises:
        ValueError: If y is zero
    
    Examples:
        >>> divide(6, 3)
        2.0
        >>> divide(5, 2)
        2.5
        >>> divide(10, 4)
        2.5
        >>> divide(0, 5)
        0.0
        >>> divide(5, 0)
        Traceback (most recent call last):
            ...
        ValueError: Cannot divide by zero
    """
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

class TestMathOperations(unittest.TestCase):
    """Unit tests for math operations - provides detailed testing with edge cases"""
    
    def test_add(self):
        """Test addition with various inputs"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-5, -3), -8)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)
    
    def test_subtract(self):
        """Test subtraction with various inputs"""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 1), -1)
        self.assertEqual(subtract(10, 10), 0)
        self.assertEqual(subtract(-5, 3), -8)
        self.assertAlmostEqual(subtract(5.5, 2.2), 3.3, places=7)
    
    def test_multiply(self):
        """Test multiplication with various inputs"""
        self.assertEqual(multiply(4, 3), 12)
        self.assertEqual(multiply(-1, 5), -5)
        self.assertEqual(multiply(0, 100), 0)
        self.assertEqual(multiply(-2, -3), 6)
        self.assertAlmostEqual(multiply(2.5, 2), 5.0, places=7)
    
    def test_divide(self):
        """Test division with various inputs and error handling"""
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(5, 2), 2.5)
        self.assertEqual(divide(0, 5), 0)
        self.assertAlmostEqual(divide(1, 3), 0.333333, places=5)
        
        # Test division by zero
        with self.assertRaises(ValueError) as context:
            divide(5, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")
        
        with self.assertRaises(ValueError):
            divide(0, 0)


def run_doctests():
    """Run all doctests and return results"""
    print("=" * 70)
    print("RUNNING DOCTESTS")
    print("=" * 70)
    results = doctest.testmod(verbose=True)
    print(f"\nDoctest Summary: {results.attempted} tests, {results.failed} failures")
    return results


def run_unittests():
    """Run all unittests and return results"""
    print("\n" + "=" * 70)
    print("RUNNING UNITTESTS")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMathOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


def main():
    """
    Main function to run hybrid testing approach.
    Executes both doctests and unittests.
    """
    print("\n" + "=" * 70)
    print("HYBRID TESTING: DOCTEST + UNITTEST")
    print("=" * 70 + "\n")
    
    # Run doctests
    doctest_results = run_doctests()
    
    # Run unittests
    unittest_results = run_unittests()
    
    # Summary
    print("\n" + "=" * 70)
    print("TESTING SUMMARY")
    print("=" * 70)
    print(f"Doctests: {doctest_results.attempted} attempted, {doctest_results.failed} failed")
    print(f"Unittests: {unittest_results.testsRun} run, {len(unittest_results.failures)} failed, {len(unittest_results.errors)} errors")
    
    total_tests = doctest_results.attempted + unittest_results.testsRun
    total_failures = doctest_results.failed + len(unittest_results.failures) + len(unittest_results.errors)
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Total Failures: {total_failures}")
    print(f"Success Rate: {((total_tests - total_failures) / total_tests * 100):.1f}%")
    print("=" * 70 + "\n")
    
    # Return success status
    return doctest_results.failed == 0 and unittest_results.wasSuccessful()


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)