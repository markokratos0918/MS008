class Person:
    def __init__(self, name, address, email, position):
        self.name = name
        self.address = address
        self.email = email
        self.position = position
      

    def show_info(self):
        base_info = f"{self.name}, {self.address}, {self.email}, {self.position}"
        return base_info

class Lecturer(Person):
    def __init__(self, name, address, email, position, salary):
        super().__init__(name, address, email, position)
        self.salary = salary
        
    def show_info(self):
        return super().show_info() + f", {self.salary}"

class Student(Person):
    def __init__(self, name, address, email, position, course):
        super().__init__(name, address, email, position)
        self.course = course
        
    def show_info(self):
        return super().show_info() + f", {self.course}"

class Staff(Person):
    def __init__(self, name, address, email, position, department):
        super().__init__(name, address, email, position)
        self.department = department
        
    def show_info(self):
        return super().show_info() + f", {self.department}"
        
class Admin(Person):

    def __init__(self, name, address, email, position, employees=None):
        super().__init__(name, address, email, position)
        self.employees = employees or []
            
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            
    def remove_emp(self, emp):
        if emp not in self.employees:
            self.employees.remove(emp)
            
    def print_emp(self):
        for emp in self.employees:
            print('--->', emp.show_info())

if __name__ == "__main__":
    
    #parent = Person("Marko", "39A Winstone Road", "marko@gmail.com")
    #print(parent.show_info())
    lec1 = Lecturer("Alejandro Boliviard", "43 Bovine Street", "alej@mail.com", "Lecturer",50000)
    stu1 = Student("James Gunn", "69 Cross Avenue", "jgunn@mail.com", "Student", "Data Science")
    staf1 = Staff("Bernardo Segundo", "245 Jupiter Drive", "bsegundo@mailcom", "Janitor", "General Services")
    admin1 = Admin("Dominus Magni", "39A Winstone Road", "dmagni@mail.com", "Super_User", [staf1])
    print(lec1.show_info())
    print(stu1.course)
    print(stu1.show_info())
    print(staf1.email)
    print(admin1.email)
    admin1.add_emp(lec1)
    admin1.print_emp()