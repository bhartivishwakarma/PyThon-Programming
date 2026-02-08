"""
CONCEPT: Creating your first metaclass
LEARN: How to control class creation
"""

class SimpleMeta(type):
    """A simple metaclass that adds a class attribute"""
    
    def __new__(cls, name, bases, attrs):
        print(f"Creating class: {name}")
        print(f"Base classes: {bases}")
        print(f"Attributes: {list(attrs.keys())}")
        
        # Add a new attribute to every class
        attrs['created_by'] = 'SimpleMeta'
        attrs['class_id'] = id(cls)
        
        return super().__new__(cls, name, bases, attrs)

# Using the metaclass
class MyClass(metaclass=SimpleMeta):
    def __init__(self, value):
        self.value = value
    
    def display(self):
        return f"Value: {self.value}"

class AnotherClass(metaclass=SimpleMeta):
    pass

if __name__ == "__main__":
    obj = MyClass(42)
    print(f"\nObject value: {obj.display()}")
    print(f"Created by: {MyClass.created_by}")
    print(f"Class ID: {MyClass.class_id}")
    
    obj2 = AnotherClass()
    print(f"\nAnother class created by: {AnotherClass.created_by}")