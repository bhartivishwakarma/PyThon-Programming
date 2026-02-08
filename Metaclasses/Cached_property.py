"""
CONCEPT: Automatic caching for expensive properties
LEARN: Performance optimization with metaclass
"""

class CachedProperty:
    """Descriptor for cached properties"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Check if value is cached
        cache_attr = f'_cached_{self.name}'
        if not hasattr(instance, cache_attr):
            # Compute and cache the value
            value = self.func(instance)
            setattr(instance, cache_attr, value)
            print(f"Computed and cached: {self.name}")
        else:
            print(f"Retrieved from cache: {self.name}")
        
        return getattr(instance, cache_attr)
    
    def __set__(self, instance, value):
        raise AttributeError("Can't set cached property")

class CachingMeta(type):
    """Metaclass that converts properties to cached properties"""
    
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        
        for attr_name, attr_value in attrs.items():
            # Convert methods marked with @property to cached properties
            if isinstance(attr_value, property):
                new_attrs[attr_name] = CachedProperty(attr_value.fget)
            else:
                new_attrs[attr_name] = attr_value
        
        return super().__new__(cls, name, bases, new_attrs)

class DataProcessor(metaclass=CachingMeta):
    def __init__(self, data):
        self.data = data
    
    @property
    def total(self):
        print("  -> Computing total...")
        import time
        time.sleep(1)  # Simulate expensive operation
        return sum(self.data)
    
    @property
    def average(self):
        print("  -> Computing average...")
        import time
        time.sleep(1)
        return sum(self.data) / len(self.data)
    
    @property
    def max_value(self):
        print("  -> Computing max...")
        import time
        time.sleep(1)
        return max(self.data)

if __name__ == "__main__":
    processor = DataProcessor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print("First access to total:")
    print(f"Total: {processor.total}")
    
    print("\nSecond access to total:")
    print(f"Total: {processor.total}")
    
    print("\nFirst access to average:")
    print(f"Average: {processor.average}")
    
    print("\nSecond access to average:")
    print(f"Average: {processor.average}")