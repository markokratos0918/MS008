class Person:
    def __init__(self, name, address, email, position):
        self.name = name
        self.address = address
        self.email = email
        self.position = position
      

    def show_info(self):
        base_info = f"{self.name}, {self.address}, {self.email}, {self.position}"
        return base_info
    
    def greetings(self):
        print(f"Hello my name is {self.name} and I am your {self.position} for the day!")

class Lecturer(Person):
    def __init__(self, name, address, email, position, salary):
        super().__init__(name, address, email, position)
        self.salary = salary

    def greetings(self):
        print(f"Hello my name is {self.name} and I am your {self.position} for the day!")

class Student(Person):
    def __init__(self, name, address, email, position, salary):
        super().__init__(name, address, email, position)
        self.salary = salary

    def greetings(self):
         print(f"Hello my name is {self.name} and I am a student")

#Yes, we can add Course as class, but this cannot inherit the Person class methods.
#Course belongs to a different type of class and not a is-a type

class Course:
    pass

if __name__ == "__main__":
    
    #parent = Person("Marko", "39A Winstone Road", "marko@gmail.com")
    #print(parent.show_info())
    lec1 = Lecturer("Alejandro Boliviard", "43 Bovine Street", "alej@mail.com", "Lecturer",50000)
    lec1.greetings()
    stu1 = Student("James Gunn", "69 Cross Avenue", "jgunn@mail.com", "Student", "Data Science")
    stu1.greetings()