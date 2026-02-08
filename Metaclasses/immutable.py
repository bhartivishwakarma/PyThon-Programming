"""
CONCEPT: Creating immutable classes
LEARN: Freeze class instances after creation
"""

class ImmutableMeta(type):
    """Metaclass that makes instances immutable after __init__"""
    
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        
        # Freeze the instance
        instance._frozen = True
        
        return instance
    
    def __new__(cls, name, bases, attrs):
        # Override __setattr__ to prevent modifications
        def __setattr__(self, key, value):
            if hasattr(self, '_frozen') and self._frozen:
                raise AttributeError(
                    f"Cannot modify immutable instance of {self.__class__.__name__}"
                )
            object.__setattr__(self, key, value)
        
        # Override __delattr__ to prevent deletions
        def __delattr__(self, key):
            if hasattr(self, '_frozen') and self._frozen:
                raise AttributeError(
                    f"Cannot delete attributes from immutable instance"
                )
            object.__delattr__(self, key)
        
        attrs['__setattr__'] = __setattr__
        attrs['__delattr__'] = __delattr__
        
        return super().__new__(cls, name, bases, attrs)

class Point(metaclass=ImmutableMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

class Person(metaclass=ImmutableMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"

if __name__ == "__main__":
    # Create immutable point
    point = Point(3, 4)
    print(f"Point: {point}")
    print(f"Distance from origin: {point.distance_from_origin()}")
    
    # Try to modify (will fail)
    try:
        point.x = 10
    except AttributeError as e:
        print(f"\nError: {e}")
    
    # Create immutable person
    person = Person("Alice", 30)
    print(f"\nPerson: {person}")
    
    # Try to modify (will fail)
    try:
        person.age = 31
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Try to delete (will fail)
    try:
        del person.name
    except AttributeError as e:
        print(f"Error: {e}")