"""
CONCEPT: Memory Optimization Techniques

Techniques:
1. __slots__: Reduce class memory overhead
2. Generators: Lazy evaluation, no list storage
3. array module: Efficient numeric arrays
4. String interning: Reuse string objects
5. Object pooling: Reuse expensive objects
6. Weak references: Don't prevent GC

When to optimize:
- Large number of instances
- Memory-constrained environments
- Processing large datasets
- Long-running applications
"""

import sys
import array

print("="*70)
print("Program 7: MEMORY OPTIMIZATION TECHNIQUES")
print("="*70)

# Example 1: __slots__ for memory savings
print("\n1. __SLOTS__ OPTIMIZATION:")
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

# Compare sizes
obj1 = WithoutSlots(1, 2)
obj2 = WithSlots(1, 2)

print(f"Without __slots__: {sys.getsizeof(obj1)} bytes")
print(f"With __slots__:    {sys.getsizeof(obj2)} bytes")

# Create many instances
objects_without = [WithoutSlots(i, i*2) for i in range(1000)]
objects_with = [WithSlots(i, i*2) for i in range(1000)]

size_without = sum(sys.getsizeof(obj) for obj in objects_without)
size_with = sum(sys.getsizeof(obj) for obj in objects_with)

print(f"\n1000 instances:")
print(f"Without __slots__: {size_without:,} bytes")
print(f"With __slots__:    {size_with:,} bytes")
print(f"Savings: {size_without - size_with:,} bytes ({(1 - size_with/size_without)*100:.1f}%)")

# Example 2: Generators vs Lists
print("\n2. GENERATORS VS LISTS:")
print("="*70)

# List - stores all values in memory
def create_list(n):
    return [i**2 for i in range(n)]

# Generator - computes values on demand
def create_generator(n):
    return (i**2 for i in range(n))

n = 100000

my_list = create_list(n)
my_gen = create_generator(n)

print(f"List of {n:,} items: {sys.getsizeof(my_list):,} bytes")
print(f"Generator: {sys.getsizeof(my_gen)} bytes")

# Generator example
def fibonacci_list(n):
    """Returns list of first n Fibonacci numbers"""
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def fibonacci_gen(n):
    """Generates first n Fibonacci numbers"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fib_list = fibonacci_list(100)
fib_gen = fibonacci_gen(100)

print(f"\nFibonacci list: {sys.getsizeof(fib_list)} bytes")
print(f"Fibonacci generator: {sys.getsizeof(fib_gen)} bytes")

# Example 3: array module vs list
print("\n3. ARRAY MODULE:")
print("="*70)

# List of integers
int_list = [i for i in range(10000)]

# Array of integers
int_array = array.array('i', range(10000))

print(f"List of 10,000 integers: {sys.getsizeof(int_list):,} bytes")
print(f"Array of 10,000 integers: {sys.getsizeof(int_array):,} bytes")
print(f"Savings: {sys.getsizeof(int_list) - sys.getsizeof(int_array):,} bytes")

# Array is more memory efficient for numeric data
print(f"\nArray element size: {int_array.itemsize} bytes")

# Example 4: String interning
print("\n4. STRING INTERNING:")
print("="*70)

import sys

# Automatic interning for identifiers
s1 = "hello"
s2 = "hello"
print(f"Automatic interning: s1 is s2 = {s1 is s2}")

# Manually intern strings
s3 = "hello world!"
s4 = "hello world!"
print(f"\nBefore interning: s3 is s4 = {s3 is s4}")

s3 = sys.intern(s3)
s4 = sys.intern(s4)
print(f"After interning: s3 is s4 = {s3 is s4}")

# Memory savings with repeated strings
strings_without = ["user_" + str(i % 100) for i in range(10000)]
strings_with = [sys.intern("user_" + str(i % 100)) for i in range(10000)]

size_without = sum(sys.getsizeof(s) for s in strings_without)
size_with = sum(sys.getsizeof(s) for s in strings_with)

print(f"\n10,000 strings (100 unique):")
print(f"Without interning: {size_without:,} bytes")
print(f"With interning: {size_with:,} bytes")

# Example 5: Object pooling
print("\n5. OBJECT POOLING:")
print("="*70)

class ExpensiveObject:
    def __init__(self):
        self.data = [0] * 10000  # Simulate expensive creation
    
    def reset(self):
        self.data = [0] * 10000

class ObjectPool:
    def __init__(self, size):
        self._pool = [ExpensiveObject() for _ in range(size)]
        self._available = self._pool.copy()
    
    def acquire(self):
        if self._available:
            return self._available.pop()
        return ExpensiveObject()  # Create new if pool empty
    
    def release(self, obj):
        obj.reset()
        self._available.append(obj)

# Without pooling
print("Without pooling (create/destroy each time):")
for _ in range(5):
    obj = ExpensiveObject()
    # Use object
    del obj

# With pooling
print("\nWith pooling (reuse objects):")
pool = ObjectPool(3)

for _ in range(5):
    obj = pool.acquire()
    # Use object
    pool.release(obj)

print("Pool reuses expensive objects")

# Example 6: Lazy evaluation
print("\n6. LAZY EVALUATION:")
print("="*70)

class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Compute value only once
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def expensive_computation(self):
        print("   Computing expensive result...")
        return sum(x**2 for x in self.data)

processor = DataProcessor(range(1000000))
print("Created processor (computation not done yet)")

print("\nFirst access:")
result1 = processor.expensive_computation

print("\nSecond access (cached):")
result2 = processor.expensive_computation

# Example 7: Using bytearray for mutable bytes
print("\n7. BYTEARRAY VS BYTES:")
print("="*70)

# bytes (immutable)
b = bytes(10000)
print(f"bytes object: {sys.getsizeof(b):,} bytes")

# bytearray (mutable)
ba = bytearray(10000)
print(f"bytearray object: {sys.getsizeof(ba):,} bytes")

# Modifying
ba[0] = 255  # In-place modification
# b[0] = 255  # Would raise TypeError

# Example 8: Reusing iterators
print("\n8. ITERATOR REUSE:")
print("="*70)

def process_data_list():
    """Creates list (stores in memory)"""
    data = [i**2 for i in range(100000)]
    return sum(data), max(data), min(data)

def process_data_gen():
    """Uses generators (computed on demand)"""
    gen1 = (i**2 for i in range(100000))
    gen2 = (i**2 for i in range(100000))
    gen3 = (i**2 for i in range(100000))
    return sum(gen1), max(gen2), min(gen3)

import time

start = time.time()
process_data_list()
list_time = time.time() - start

start = time.time()
process_data_gen()
gen_time = time.time() - start

print(f"List approach: {list_time:.4f} seconds")
print(f"Generator approach: {gen_time:.4f} seconds")

# Example 9: Memory-efficient counting
print("\n9. EFFICIENT COUNTING:")
print("="*70)

from collections import Counter

# Method 1: Store all items
items1 = []
for i in range(1000000):
    items1.append(i % 1000)

counts1 = {}
for item in items1:
    counts1[item] = counts1.get(item, 0) + 1

# Method 2: Count directly
counts2 = Counter()
for i in range(1000000):
    counts2[i % 1000] += 1

print(f"Store then count: {sys.getsizeof(items1):,} bytes (list)")
print(f"Direct counting: {sys.getsizeof(counts2):,} bytes (Counter)")

# Example 10: Summary
print("\n10. OPTIMIZATION SUMMARY:")
print("="*70)

print("""
✓ Use __slots__ for classes with many instances
✓ Prefer generators over lists for large sequences
✓ Use array.array for numeric data
✓ Intern frequently used strings
✓ Pool expensive objects
✓ Lazy evaluation for expensive computations
✓ Use appropriate data structures
✓ Avoid unnecessary copying
✓ Profile before optimizing
✓ Balance readability with optimization
""")