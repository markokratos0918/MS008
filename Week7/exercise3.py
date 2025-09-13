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
