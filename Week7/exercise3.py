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
#shape = factory.create_shape("triangle")   
shape = factory.create_shape("circle") 
print(shape.draw())  

#Ans. 
#The problem possible will majhe the Object creation logic is repeated throughout the codebase, making maintenance harder. and increasing the risk of inconsistencis.
# Using a Factory centralizes object creation, making your code more maintainable, flexible, and easier to test.
