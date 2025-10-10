import unittest


class Expense:
    '''Class to represent a single expense with description and amount.'''
    def __init__(self, description, amount):
        '''Initialize an expense with description and amount.'''
        self.description = description
        self.amount = amount

class ExpenseTracker:
    '''Class to track personal expenses.'''
    def __init__(self):
        self.expenses = []

    def add_expense(self, description, amount):
        '''Add a new expense.'''
        expense = Expense(description, amount)
        self.expenses.append(expense)
        print(f"Added expense: {description} - ${amount:.2f}")
    def total_expense(self):
        '''Calculate total expenses.'''
        return sum(expense.amount for expense in self.expenses)


class ExpenseTrackerTest:
    '''Class to track personal expenses.'''
    def __init__(self):
        '''Initialize the expense tracker with an empty list of expenses.'''
        self.expenses = []

    def add_expense(self, description, amount):
        '''Add a new expense.'''
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.expenses.append((description, amount))

    def total_expense(self):
        '''Calculate total expenses.'''
        return sum(amount for _, amount in self.expenses)
class TestExpenseTracker(unittest.TestCase):
    '''Unit tests for ExpenseTracker'''
    def setUp(self):
        '''Set up a new ExpenseTracker for each test'''
        self.tracker = ExpenseTrackerTest()

    def test_add_expense(self):
        '''Test adding an expense'''
        self.tracker.add_expense("Lunch", 15.50)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0], ("Lunch", 15.50))

    def test_total_expense(self):
        '''Test total expense calculation'''
        self.tracker.add_expense("Lunch", 15.50)
        self.tracker.add_expense("Coffee", 3.25)
        self.assertEqual(self.tracker.total_expense(), 18.75)

    def test_add_negative_expense(self):
        '''Test adding a negative expense raises ValueError'''
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Invalid", -5.00)

if __name__ == '__main__':
    tracker = ExpenseTracker()
    tracker.add_expense("Lunch", 12.50)
    tracker.add_expense("Book", 25.00)
    tracker.add_expense("Rental", 100.00)
    print("Total Expense:", tracker.total_expense())  # Output: Total Expense: 137.5
    unittest.main()