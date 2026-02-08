"""
CONCEPT: Custom ABC implementation
LEARN: Enforce method implementation using metaclass
"""

class ABCMeta(type):
    """Custom Abstract Base Class metaclass"""
    
    def __new__(cls, name, bases, attrs):
        # Collect abstract methods from base classes
        abstract_methods = set()
        for base in bases:
            if hasattr(base, '_abstract_methods'):
                abstract_methods.update(base._abstract_methods)
        
        # Find new abstract methods in current class
        for attr_name, attr_value in attrs.items():
            if getattr(attr_value, '_is_abstract', False):
                abstract_methods.add(attr_name)
        
        # Remove implemented methods
        for attr_name in attrs:
            if attr_name in abstract_methods:
                if not getattr(attrs[attr_name], '_is_abstract', False):
                    abstract_methods.discard(attr_name)
        
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._abstract_methods = abstract_methods
        
        return new_class
    
    def __call__(cls, *args, **kwargs):
        if cls._abstract_methods:
            raise TypeError(
                f"Can't instantiate abstract class {cls.__name__} "
                f"with abstract methods: {', '.join(cls._abstract_methods)}"
            )
        return super(ABCMeta, cls).__call__(*args, **kwargs)

def abstractmethod(func):
    """Decorator to mark methods as abstract"""
    func._is_abstract = True
    return func

class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def describe(self):
        return f"A shape with area {self.area()}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# This will fail - incomplete implementation
# class IncompleteShape(Shape):
#     def area(self):
#         return 0
#     # Missing perimeter()

if __name__ == "__main__":
    circle = Circle(5)
    print(f"Circle area: {circle.area()}")
    print(f"Circle perimeter: {circle.perimeter()}")
    print(f"Description: {circle.describe()}")
    
    rectangle = Rectangle(4, 6)
    print(f"\nRectangle area: {rectangle.area()}")
    print(f"Rectangle perimeter: {rectangle.perimeter()}")
    
    # Try to create abstract class
    try:
        shape = Shape()
    except TypeError as e:
        print(f"\nError: {e}")