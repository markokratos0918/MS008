"""
Week 11 - Activity 4: Implementing Doctest and Unittest in Python
Due date: 17.10.25 at midnight

Expense Tracker with hybrid testing
"""

import unittest
import doctest


# =============================================================================
# PART 1: THE EXPENSE CLASS
# =============================================================================

class Expense:
    """
    A simple class to store one expense.
    Think of it like a receipt: it has a description and an amount.
    
    Examples:
        >>> expense = Expense("Lunch", 12.50)
        >>> expense.description
        'Lunch'
        >>> expense.amount
        12.5
        
        >>> coffee = Expense("Coffee", 5.0)
        >>> coffee.description
        'Coffee'
    """
    
    def __init__(self, description, amount):
        """
        Create a new expense.
        
        Args:
            description: What you spent money on (like "Lunch" or "Gas")
            amount: How much you spent (like 12.50)
        """
        self.description = description
        self.amount = amount


# =============================================================================
# PART 2: THE EXPENSE TRACKER CLASS
# =============================================================================

class ExpenseTracker:
    """
    A class to keep track of all your expenses.
    Think of it like a notebook where you write down everything you spend.
    
    Examples:
        >>> tracker = ExpenseTracker()
        >>> tracker.add_expense("Lunch", 12.50)
        Added expense: Lunch - $12.50
        >>> tracker.add_expense("Book", 25.00)
        Added expense: Book - $25.00
        >>> tracker.total_expense()
        37.5
    """
    
    def __init__(self):
        """
        Start with an empty list of expenses.
        Like starting with a blank page in your notebook.
        """
        self.expenses = []
    
    def add_expense(self, description, amount):
        """
        Add a new expense to your tracker.
        
        Args:
            description: What you bought (string)
            amount: How much it cost (number)
        
        Examples:
            >>> tracker = ExpenseTracker()
            >>> tracker.add_expense("Coffee", 5.00)
            Added expense: Coffee - $5.00
            >>> tracker.add_expense("Movie", 15.00)
            Added expense: Movie - $15.00
            >>> len(tracker.expenses)
            2
        """
        # Create a new Expense object
        expense = Expense(description, amount)
        
        # Add it to our list
        self.expenses.append(expense)
        
        # Print a confirmation message
        print(f"Added expense: {description} - ${amount:.2f}")
    
    def total_expense(self):
        """
        Calculate how much you've spent in total.
        Adds up all the amounts from all expenses.
        
        Returns:
            The total amount spent (number)
        
        Examples:
            >>> tracker = ExpenseTracker()
            >>> tracker.total_expense()
            0
            
            >>> tracker.add_expense("Lunch", 10.00)
            Added expense: Lunch - $10.00
            >>> tracker.add_expense("Dinner", 20.00)
            Added expense: Dinner - $20.00
            >>> tracker.total_expense()
            30.0
        """
        # Start with zero
        total = 0
        
        # Add each expense amount to the total
        for expense in self.expenses:
            total += expense.amount
        
        return total
        
        # Note: The line above does the same as this shorter version:
        # return sum(expense.amount for expense in self.expenses)


# =============================================================================
# PART 3: UNIT TESTS - Testing with unittest
# =============================================================================

class TestExpense(unittest.TestCase):
    """
    Tests for the Expense class.
    Each test checks one specific thing about how Expense works.
    """
    
    def test_create_expense(self):
        """Check that we can create an Expense and it stores data correctly"""
        # Create an expense
        expense = Expense("Groceries", 50.00)
        
        # Check that the description is stored correctly
        self.assertEqual(expense.description, "Groceries")
        
        # Check that the amount is stored correctly
        self.assertEqual(expense.amount, 50.00)
    
    def test_expense_with_different_amounts(self):
        """Test creating expenses with different amounts"""
        # Small amount
        small = Expense("Gum", 1.25)
        self.assertEqual(small.amount, 1.25)
        
        # Large amount
        large = Expense("Rent", 1000.00)
        self.assertEqual(large.amount, 1000.00)
        
        # Zero amount (free item)
        free = Expense("Free sample", 0)
        self.assertEqual(free.amount, 0)


class TestExpenseTracker(unittest.TestCase):
    """
    Tests for the ExpenseTracker class.
    Each test checks one specific feature of the tracker.
    """
    
    def setUp(self):
        """
        This runs BEFORE each test.
        It creates a fresh, empty tracker for each test.
        """
        self.tracker = ExpenseTracker()
    
    def test_new_tracker_is_empty(self):
        """Check that a new tracker starts with no expenses"""
        # A new tracker should have 0 expenses
        self.assertEqual(len(self.tracker.expenses), 0)
        
        # Total should be 0
        self.assertEqual(self.tracker.total_expense(), 0)
    
    def test_add_one_expense(self):
        """Test adding a single expense"""
        # Add one expense
        self.tracker.add_expense("Lunch", 12.50)
        
        # Check we now have 1 expense
        self.assertEqual(len(self.tracker.expenses), 1)
        
        # Check the total is correct
        self.assertEqual(self.tracker.total_expense(), 12.50)
    
    def test_add_multiple_expenses(self):
        """Test adding several expenses"""
        # Add three expenses
        self.tracker.add_expense("Lunch", 12.50)
        self.tracker.add_expense("Book", 25.00)
        self.tracker.add_expense("Gas", 40.00)
        
        # Check we have 3 expenses
        self.assertEqual(len(self.tracker.expenses), 3)
        
        # Check the total: 12.50 + 25.00 + 40.00 = 77.50
        self.assertEqual(self.tracker.total_expense(), 77.50)
    
    def test_total_expense_calculation(self):
        """Test that total calculates correctly"""
        # Add expenses
        self.tracker.add_expense("Item 1", 10.00)
        self.tracker.add_expense("Item 2", 20.50)
        self.tracker.add_expense("Item 3", 5.25)
        
        # Calculate expected total
        expected = 10.00 + 20.50 + 5.25  # = 35.75
        
        # Check it matches
        self.assertEqual(self.tracker.total_expense(), expected)
    
    def test_example_from_original_code(self):
        """Test the exact example from the original assignment"""
        # This is from: if __name__ == "__main__" section
        self.tracker.add_expense("Lunch", 12.50)
        self.tracker.add_expense("Book", 25.00)
        self.tracker.add_expense("Rental", 100.00)
        
        # Check total: 12.50 + 25.00 + 100.00 = 137.50
        self.assertEqual(self.tracker.total_expense(), 137.50)


# =============================================================================
# PART 4: RUNNING THE TESTS
# =============================================================================

def run_doctests():
    """
    Run all the doctest examples (the ones in triple quotes with >>>)
    """
    print("=" * 70)
    print("RUNNING DOCTESTS")
    print("These are the examples in the docstrings (the ones with >>>)")
    print("=" * 70)
    
    # Run all doctests and get results
    results = doctest.testmod(verbose=True)
    
    print(f"\nDoctest Summary: {results.attempted} tests, {results.failed} failures")
    return results


def run_unittests():
    """
    Run all the unittest tests (the ones in test classes)
    """
    print("\n" + "=" * 70)
    print("RUNNING UNITTESTS")
    print("These are the formal unit tests in test classes")
    print("=" * 70)
    
    # Create a test suite with all our tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests from both test classes
    suite.addTests(loader.loadTestsFromTestCase(TestExpense))
    suite.addTests(loader.loadTestsFromTestCase(TestExpenseTracker))
    
    # Run the tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def show_summary(doctest_results, unittest_results):
    """
    Display a nice summary of all test results
    """
    print("\n" + "=" * 70)
    print("TESTING SUMMARY")
    print("=" * 70)
    
    # Doctest summary
    print(f"Doctests: {doctest_results.attempted} attempted, {doctest_results.failed} failed")
    
    # Unittest summary
    print(f"Unittests: {unittest_results.testsRun} run, "
          f"{len(unittest_results.failures)} failed, "
          f"{len(unittest_results.errors)} errors")
    
    # Calculate totals
    total_tests = doctest_results.attempted + unittest_results.testsRun
    total_failures = (doctest_results.failed + 
                     len(unittest_results.failures) + 
                     len(unittest_results.errors))
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Total Failures: {total_failures}")
    
    # Calculate success rate
    if total_tests > 0:
        success_rate = ((total_tests - total_failures) / total_tests * 100)
        print(f"Success Rate: {success_rate:.1f}%")
    
    print("=" * 70 + "\n")
    
    # Return True if all tests passed
    return doctest_results.failed == 0 and unittest_results.wasSuccessful()


def demo():
    """
    Show how the expense tracker works (the original example)
    """
    print("\n" + "=" * 70)
    print("EXPENSE TRACKER DEMO")
    print("This is the original example from the assignment")
    print("=" * 70 + "\n")
    
    # Create a tracker
    tracker = ExpenseTracker()
    
    # Add expenses
    tracker.add_expense("Lunch", 12.50)
    tracker.add_expense("Book", 25.00)
    tracker.add_expense("Rental", 100.00)
    
    # Show total
    print(f"\nTotal Expense: ${tracker.total_expense():.2f}")
    print("=" * 70 + "\n")


# =============================================================================
# PART 5: MAIN PROGRAM
# =============================================================================

if __name__ == "__main__":
    # First, show the demo
    demo()
    
    # Run doctests
    doctest_results = run_doctests()
    
    # Run unittests
    unittest_results = run_unittests()
    
    # Show summary
    all_passed = show_summary(doctest_results, unittest_results)
    
    # Exit with appropriate code (0 = success, 1 = failure)
    exit(0 if all_passed else 1)