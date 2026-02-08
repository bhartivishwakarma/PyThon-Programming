"""
CONCEPT: Automatic attribute validation
LEARN: Enforce rules on class attributes
"""

class ValidationMeta(type):
    """Metaclass that validates class attributes"""
    
    def __new__(cls, name, bases, attrs):
        # Check that all methods have docstrings
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                if not attr_value.__doc__:
                    raise TypeError(
                        f"Method '{attr_name}' in class '{name}' must have a docstring"
                    )
        
        # Check for required class attributes
        required_attrs = attrs.get('_required_attributes', [])
        for required in required_attrs:
            if required not in attrs:
                raise TypeError(
                    f"Class '{name}' must define attribute '{required}'"
                )
        
        return super().__new__(cls, name, bases, attrs)

class ValidatedClass(metaclass=ValidationMeta):
    _required_attributes = ['version', 'author']
    
    version = "1.0"
    author = "John Doe"
    
    def process(self):
        """Process the data"""
        return "Processing..."
    
    def calculate(self, x, y):
        """Calculate sum of x and y"""
        return x + y

# This will raise an error - missing docstring
# class InvalidClass(metaclass=ValidationMeta):
#     def process(self):
#         return "No docstring!"

# This will raise an error - missing required attribute
# class IncompleteClass(metaclass=ValidationMeta):
#     _required_attributes = ['version', 'author']
#     version = "1.0"
#     # Missing 'author'

if __name__ == "__main__":
    obj = ValidatedClass()
    print(f"Version: {obj.version}")
    print(f"Author: {obj.author}")
    print(f"Result: {obj.calculate(5, 3)}")