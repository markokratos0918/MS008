class Circle:
    def draw(self):
        return "Drawing a Circle"

class Square:
    def draw(self):
        return "Drawing a Square"
class Triangle:
    def draw(self):
        return "Drawing a Triangle"

class ShapeFactory:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle()
        if shape_type == "square":
            return Square()
        if shape_type == "triangle":
            return Triangle()
        else:
            return None


factory = ShapeFactory()
shape = factory.create_shape("triangle")   
print(shape.draw())  

#Ans. 
# The code becomes tightly coupled to specific classes. If you need to change the implementation or constructor of a class, you must update every place where it is instantiated.Using a Factory centralizes object creation, making your code more maintainable, flexible, and easier to test.
