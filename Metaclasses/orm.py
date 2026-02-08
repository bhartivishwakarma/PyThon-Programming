"""
CONCEPT: Simple ORM implementation
LEARN: Database-like field validation using metaclass
"""

class Field:
    """Base field descriptor"""
    def __init__(self, field_type, required=True, default=None):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        if value is None and self.required:
            raise ValueError(f"{self.name} is required")
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be {self.field_type.__name__}, got {type(value).__name__}"
            )
        instance.__dict__[self.name] = value

class ModelMeta(type):
    """Metaclass for ORM-like models"""
    
    def __new__(cls, name, bases, attrs):
        # Collect all fields
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
        
        attrs['_fields'] = fields
        
        # Add validation method
        def validate(self):
            for field_name, field in self._fields.items():
                value = getattr(self, field_name)
                if value is None and field.required:
                    raise ValueError(f"Field {field_name} is required")
        
        attrs['validate'] = validate
        
        # Add to_dict method
        def to_dict(self):
            return {
                field_name: getattr(self, field_name)
                for field_name in self._fields.keys()
            }
        
        attrs['to_dict'] = to_dict
        
        return super().__new__(cls, name, bases, attrs)

class User(metaclass=ModelMeta):
    name = Field(str, required=True)
    age = Field(int, required=True)
    email = Field(str, required=False, default="no-email@example.com")
    is_active = Field(bool, required=False, default=True)
    
    def __init__(self, name, age, email=None, is_active=True):
        self.name = name
        self.age = age
        self.email = email
        self.is_active = is_active

if __name__ == "__main__":
    # Valid user
    user1 = User("Alice", 30, "alice@example.com")
    print(f"User: {user1.to_dict()}")
    
    # User with defaults
    user2 = User("Bob", 25)
    print(f"User: {user2.to_dict()}")
    
    # Validation
    try:
        user3 = User("Charlie", "not_a_number")  # Will raise TypeError
    except TypeError as e:
        print(f"Error: {e}")