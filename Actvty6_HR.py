class Employee:
    def __init__(self, name, salary, job_title):
        self.name = name
        self.salary = salary
        self.job_title = job_title

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Job Title: {self.job_title}")
        print(f"Salary: ${self.salary:,.2f}")
        print("-" * 30)

    def give_raise(self, amount):
        self.salary += amount
        print(f"{self.name} has been given a raise of ${amount:,.2f}.")
        print(f"New Salary: ${self.salary:,.2f}")
        print("-" * 30)


# --- Create at least two employees ---
employee1 = Employee("Alice Johnson", 50000, "Software Engineer")
employee2 = Employee("Marko Dela Torre", 60000, "Field Support Technician")

# --- Display their information ---
employee1.display_info()
employee2.display_info()

# --- Give a raise to employee1 ---
employee1.give_raise(5000)

# --- Display updated information ---
employee1.display_info()