class Student:
    def __init__(self, name, age):
        self.name = name       # public
        self._age = age        # protected
        self.__grade = 'A'     # private

    def get_grade(self):
        return self.__grade

    def get_grade(self):
        return self.__grade

    #new method added
    def set_grade(self, new_grade):
        if new_grade in ['A', 'B', 'C', 'D', 'F']:
            self.__grade = new_grade
            print(f"Grade updated to {self.__grade}")
        else:
            print("Invalid grade. Please use 'A', 'B', 'C', 'D', or 'F'.")

    def updated_info(self):
        self.__grade = "A+"
        print(f"Grade boosted to {self.__grade}")
    
# New class that inherits from Student
class GraduateStudent(Student):
    def __init__(self, name, age, thesis_title):
        super().__init__(name, age)   # call parent constructor
        self.thesis_title = thesis_title  # public attribute

    def show_details(self):
        # Public attribute: accessible directly
        print(f"Name: {self.name}")  

        # Protected attribute: accessible in subclass (not recommended, but possible)
        print(f"Age: {self._age}")    

        # Private attribute: cannot be accessed directly -> use getter instead
        print(f"Grade: {self.get_grade()}")  

        # Thesis info (specific to GraduateStudent)
        print(f"Thesis: {self.thesis_title}")

        
# s = Student('Ali', 20)
# print(s.name)         # accessible
# # print(s._age)         # discouraged
# # print(s.get_grade())  # correct way
# s = Student('Ali', 20)
# print(f"Initial grade: {s.get_grade()}")  # Output: Initial grade: A

# # Using the new method to change the grade
# s.set_grade('B')  # Output: Grade updated to B
# print(f"New grade: {s.get_grade()}")      # Output: New grade: B

# # Attempting to set an invalid grade
# s.set_grade('E')  # Output: Invalid grade. Please use 'A', 'B', 'C', 'D', or 'F'.

# # Attempting to access the private attribute directly will result in an error
# try:
#     print(s.__grade)
# except AttributeError as e:
#     print(f"\nError: {e}")  # Output: Error: 'Student' object has no attribute '__grade'


# # Added another class to show the use of public and protected attributes
# g = GraduateStudent("Sara", 25, "AI in Robotics")

# # Accessing details
# g.show_details()

# # Changing grade via setter
# g.set_grade("B")
# print(f"Updated Grade (via getter): {g.get_grade()}")

# # Direct access
# print("\nDirect access:")
# print(g.name)      #  allowed (public)
# print(g._age)      #  allowed but discouraged (protected)

# try:
#     print(g.get_grade)  # error (private)
# except AttributeError as e:
#     print(f"Error: {e}")

# test
s = Student('Ali', 20)
print(f"Initial grade: {s.get_grade()}")  # Output: A

# Using updated_info to upgrade the grade
s.updated_info()  
print(f"New grade after boost: {s.get_grade()}")  # Output: A+

