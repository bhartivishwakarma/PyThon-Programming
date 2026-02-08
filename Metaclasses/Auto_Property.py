"""
CONCEPT: Automatic property creation
LEARN: Transform attributes into properties automatically
"""

class AutoPropertyMeta(type):
    """Metaclass that converts _private attributes to properties"""
    
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        
        for attr_name, attr_value in attrs.items():
            new_attrs[attr_name] = attr_value
            
            # Convert _private attributes to properties
            if attr_name.startswith('_') and not attr_name.startswith('__'):
                prop_name = attr_name[1:]  # Remove leading underscore
                
                # Create getter
                def make_getter(attr):
                    def getter(self):
                        return getattr(self, attr)
                    return getter
                
                # Create setter
                def make_setter(attr):
                    def setter(self, value):
                        setattr(self, attr, value)
                    return setter
                
                new_attrs[prop_name] = property(
                    make_getter(attr_name),
                    make_setter(attr_name)
                )
        
        return super().__new__(cls, name, bases, new_attrs)

class Person(metaclass=AutoPropertyMeta):
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._email = None
    
    def display(self):
        return f"{self._name} is {self._age} years old"

if __name__ == "__main__":
    person = Person("Alice", 30)
    
    # Access via auto-created properties
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    
    # Set via properties
    person.email = "alice@example.com"
    print(f"Email: {person.email}")
    
    # Still works with methods
    print(person.display())