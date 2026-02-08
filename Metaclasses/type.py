"""
CONCEPT: type() is a metaclass
LEARN: Everything in Python is an object, even classes
"""

# Creating a class the normal way
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says Woof!"

# Creating the SAME class using type()
Dog2 = type('Dog2', (), {
    '__init__': lambda self, name: setattr(self, 'name', name),
    'bark': lambda self: f"{self.name} says Woof!"
})

if __name__ == "__main__":
    # Using normal class
    dog1 = Dog("Buddy")
    print(f"Dog1: {dog1.bark()}")
    print(f"Type of dog1: {type(dog1)}")
    print(f"Type of Dog class: {type(Dog)}")
    
    # Using type-created class
    dog2 = Dog2("Max")
    print(f"\nDog2: {dog2.bark()}")
    print(f"Type of dog2: {type(dog2)}")
    print(f"Type of Dog2 class: {type(Dog2)}")
    
    # Inspection
    print(f"\n--- Metaclass Investigation ---")
    print(f"Dog.__class__: {Dog.__class__}")
    print(f"Dog2.__class__: {Dog2.__class__}")
    print(f"type.__class__: {type.__class__}")