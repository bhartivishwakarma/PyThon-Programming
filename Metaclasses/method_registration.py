"""
CONCEPT: Automatic method registration
LEARN: Track and register methods dynamically
"""

class RegistryMeta(type):
    """Metaclass that maintains a registry of all methods"""
    
    def __new__(cls, name, bases, attrs):
        # Create registry for this class
        registry = {
            'public_methods': [],
            'private_methods': [],
            'magic_methods': []
        }
        
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                if attr_name.startswith('__') and attr_name.endswith('__'):
                    registry['magic_methods'].append(attr_name)
                elif attr_name.startswith('_'):
                    registry['private_methods'].append(attr_name)
                else:
                    registry['public_methods'].append(attr_name)
        
        attrs['_method_registry'] = registry
        
        # Add a class method to display registry
        def show_methods(cls):
            print(f"\n=== Methods in {cls.__name__} ===")
            print(f"Public: {cls._method_registry['public_methods']}")
            print(f"Private: {cls._method_registry['private_methods']}")
            print(f"Magic: {cls._method_registry['magic_methods']}")
        
        attrs['show_methods'] = classmethod(show_methods)
        
        return super().__new__(cls, name, bases, attrs)

class Calculator(metaclass=RegistryMeta):
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
    
    def _validate(self, x):
        return isinstance(x, (int, float))
    
    def __str__(self):
        return "Calculator instance"

class AdvancedCalculator(Calculator):
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        return x / y if y != 0 else None

if __name__ == "__main__":
    Calculator.show_methods()
    AdvancedCalculator.show_methods()
    
    calc = Calculator()
    print(f"\nAddition: {calc.add(5, 3)}")