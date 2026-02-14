"""
CONCEPT: __slots__ Optimization
- By default, instances use __dict__ to store attributes
- __slots__ uses fixed-size array instead
- Significant memory savings for many instances
- Faster attribute access
- Trade-off: lose dynamic attribute creation

Memory Savings:
Without __slots__: ~280 bytes per instance
With __slots__: ~120 bytes per instance

When to Use:
✓ Many instances (1000+)
✓ Fixed set of attributes
✓ Memory-constrained
✗ Need dynamic attributes
✗ Few instances
"""

import sys
import time
import tracemalloc

print("="*70)
print("Program 16: __SLOTS__ OPTIMIZATION")
print("="*70)

# Example 1: Basic __slots__ usage
print("\n1. BASIC __SLOTS__:")
print("="*70)

class WithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Create instances
obj1 = WithoutSlots(1, 2)
obj2 = WithSlots(1, 2)

print(f"Without __slots__:")
print(f"   Size: {sys.getsizeof(obj1)} bytes")
print(f"   Has __dict__: {hasattr(obj1, '__dict__')}")

print(f"\nWith __slots__:")
print(f"   Size: {sys.getsizeof(obj2)} bytes")
print(f"   Has __dict__: {hasattr(obj2, '__dict__')}")

# Example 2: Dynamic attributes
print("\n2. DYNAMIC ATTRIBUTES:")
print("="*70)

obj1 = WithoutSlots(1, 2)
obj1.z = 3  # Can add new attribute
print(f"Without __slots__: Can add 'z' = {obj1.z}")

obj2 = WithSlots(1, 2)
try:
    obj2.z = 3  # Cannot add new attribute!
except AttributeError as e:
    print(f"With __slots__: Cannot add 'z' - {e}")

# Example 3: Memory savings with many instances
print("\n3. MEMORY SAVINGS (10,000 instances):")
print("="*70)

n = 10000

# Without __slots__
tracemalloc.start()
objects1 = [WithoutSlots(i, i*2) for i in range(n)]
current, peak = tracemalloc.get_traced_memory()
without_memory = peak / 1024 / 1024
tracemalloc.stop()

# With __slots__
tracemalloc.start()
objects2 = [WithSlots(i, i*2) for i in range(n)]
current, peak = tracemalloc.get_traced_memory()
with_memory = peak / 1024 / 1024
tracemalloc.stop()

print(f"Without __slots__: {without_memory:.2f} MB")
print(f"With __slots__: {with_memory:.2f} MB")
print(f"Savings: {without_memory - with_memory:.2f} MB ({(1 - with_memory/without_memory)*100:.1f}%)")

# Example 4: Attribute access speed
print("\n4. ATTRIBUTE ACCESS SPEED:")
print("="*70)

obj1 = WithoutSlots(10, 20)
obj2 = WithSlots(10, 20)

# Benchmark attribute access
iterations = 1_000_000

# Without __slots__
start = time.time()
for _ in range(iterations):
    _ = obj1.x
    _ = obj1.y
without_time = time.time() - start

# With __slots__
start = time.time()
for _ in range(iterations):
    _ = obj2.x
    _ = obj2.y
with_time = time.time() - start

print(f"Without __slots__: {without_time:.4f} seconds")
print(f"With __slots__: {with_time:.4f} seconds")
print(f"Speedup: {without_time / with_time:.2f}x faster")

# Example 5: __slots__ with inheritance
print("\n5. INHERITANCE WITH __SLOTS__:")
print("="*70)

class Base:
    __slots__ = ('a', 'b')
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Derived(Base):
    __slots__ = ('c',)  # Only new attributes
    
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c

obj = Derived(1, 2, 3)
print(f"Derived class:")
print(f"   a={obj.a}, b={obj.b}, c={obj.c}")
print(f"   Size: {sys.getsizeof(obj)} bytes")

# Example 6: __slots__ with default values
print("\n6. __SLOTS__ WITH DEFAULTS:")
print("="*70)

class WithDefaults:
    __slots__ = ('x', 'y', 'z')
    
    def __init__(self, x, y, z=100):
        self.x = x
        self.y = y
        self.z = z

obj = WithDefaults(1, 2)
print(f"Object: x={obj.x}, y={obj.y}, z={obj.z}")

# Example 7: __slots__ doesn't affect class variables
print("\n7. CLASS VARIABLES:")
print("="*70)

class WithClassVar:
    __slots__ = ('x',)
    class_var = "shared"
    
    def __init__(self, x):
        self.x = x

obj1 = WithClassVar(1)
obj2 = WithClassVar(2)

print(f"obj1.class_var: {obj1.class_var}")
print(f"obj2.class_var: {obj2.class_var}")
print(f"Same object: {obj1.class_var is obj2.class_var}")

# Example 8: Allowing __dict__ with __slots__
print("\n8. __SLOTS__ WITH __DICT__:")
print("="*70)

class Hybrid:
    __slots__ = ('x', 'y', '__dict__')  # Explicitly include __dict__
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = Hybrid(1, 2)
obj.z = 3  # Can add dynamic attributes now
print(f"Hybrid: x={obj.x}, y={obj.y}, z={obj.z}")
print(f"Size: {sys.getsizeof(obj)} bytes")

# Example 9: __slots__ with properties
print("\n9. __SLOTS__ WITH PROPERTIES:")
print("="*70)

class WithProperties:
    __slots__ = ('_x', '_y')
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if value < 0:
            raise ValueError("x must be positive")
        self._x = value
    
    @property
    def sum(self):
        return self._x + self._y

obj = WithProperties(10, 20)
print(f"x={obj.x}, sum={obj.sum}")

obj.x = 30
print(f"After x=30: x={obj.x}, sum={obj.sum}")

# Example 10: Real-world example - Point class
print("\n10. POINT CLASS COMPARISON:")
print("="*70)

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self):
        return (self.x**2 + self.y**2) ** 0.5

class OptimizedPoint2D:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self):
        return (self.x**2 + self.y**2) ** 0.5

# Create many points
n = 100000

tracemalloc.start()
points1 = [Point2D(i, i) for i in range(n)]
current, peak = tracemalloc.get_traced_memory()
normal_memory = peak / 1024 / 1024
tracemalloc.stop()

tracemalloc.start()
points2 = [OptimizedPoint2D(i, i) for i in range(n)]
current, peak = tracemalloc.get_traced_memory()
optimized_memory = peak / 1024 / 1024
tracemalloc.stop()

print(f"100,000 Point2D objects:")
print(f"   Normal: {normal_memory:.2f} MB")
print(f"   Optimized: {optimized_memory:.2f} MB")
print(f"   Savings: {normal_memory - optimized_memory:.2f} MB")

# Example 11: __slots__ pitfalls
print("\n11. __SLOTS__ PITFALLS:")
print("="*70)

class Base1:
    __slots__ = ('a',)

class Base2:
    __slots__ = ('b',)

# This will fail if both bases have __slots__
try:
    class MultipleInheritance(Base1, Base2):
        pass
except TypeError as e:
    print(f"Multiple inheritance error: {e}")

# Workaround: use empty __slots__ in one base
class Base3:
    __slots__ = ()  # Empty slots

class Derived2(Base1, Base3):
    __slots__ = ('c',)

print("\nWorkaround successful with empty __slots__")

# Example 12: Summary
print("\n12. __SLOTS__ SUMMARY:")
print("="*70)

print("""
✓ When to Use __slots__:
- Many instances (1000+)
- Fixed set of attributes
- Memory-constrained environment
- Performance-critical code
- Data classes with known fields

✗ When NOT to Use:
- Few instances (<100)
- Need dynamic attributes
- Heavy use of inheritance
- Rapid prototyping
- Unsure about attributes

Benefits:
- 40-50% memory savings per instance
- Faster attribute access (~20% faster)
- Prevents typos (no dynamic attributes)
- More explicit interface

Limitations:
- No dynamic attribute creation
- No weak references (unless '__weakref__' in slots)
- Multiple inheritance restrictions
- Slightly more complex

Best Practices:
1. Profile before optimizing
2. Use for data-heavy classes
3. Include '__weakref__' if needed
4. Include '__dict__' for flexibility
5. Document the decision
6. Test memory savings
7. Consider named tuples as alternative

Memory Comparison (typical):
- Regular instance: ~280 bytes
- With __slots__: ~120 bytes
- Savings: ~160 bytes per instance
- For 1M instances: ~160 MB saved
""")