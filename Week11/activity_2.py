class Expense:
    '''Class to represent a single expense with description and amount.'''
    def __init__(self, description, amount):
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


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.add_expense("Lunch", 12.50)
    tracker.add_expense("Book", 25.00)
    tracker.add_expense("Rental", 100.00)
    print("Total Expense:", tracker.total_expense())  # Output: Total Expense: 137.5

