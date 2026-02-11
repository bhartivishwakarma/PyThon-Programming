"""
CONCEPT: Memory Leaks and Detection
- Memory leak: memory that's allocated but never freed
- Causes: circular references, forgotten globals, large caches
- Detection: tracemalloc, gc, memory profilers

Common Leak Sources:
1. Circular references without __del__
2. Global variables holding references
3. Unbounded caches
4. Event handlers not unregistered
5. Closures capturing large objects

Detection Tools:
- tracemalloc: Built-in memory tracking
- gc.get_objects(): All tracked objects
- sys.getsizeof(): Object size
- memory_profiler: Line-by-line profiling
"""

import gc
import sys
import tracemalloc

print("="*70)
print("Program 5: MEMORY LEAKS AND DETECTION")
print("="*70)

# Example 1: Detecting memory growth
print("\n1. BASIC MEMORY TRACKING:")
print("="*70)

tracemalloc.start()

# Take snapshot before
snapshot1 = tracemalloc.take_snapshot()

# Allocate memory
data = []
for i in range(10000):
    data.append([i] * 100)

# Take snapshot after
snapshot2 = tracemalloc.take_snapshot()

# Compare snapshots
stats = snapshot2.compare_to(snapshot1, 'lineno')

print("Top 3 memory allocations:")
for stat in stats[:3]:
    print(f"   {stat}")

current, peak = tracemalloc.get_traced_memory()
print(f"\nCurrent memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory:    {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()

# Example 2: Memory leak - circular reference
print("\n2. MEMORY LEAK - CIRCULAR REFERENCE:")
print("="*70)

class LeakyNode:
    instances = []
    
    def __init__(self, data):
        self.data = data
        self.ref = None
        LeakyNode.instances.append(self)

print("Creating circular references:")
initial_count = len(gc.get_objects())

for i in range(1000):
    node1 = LeakyNode(i)
    node2 = LeakyNode(i + 1000)
    node1.ref = node2
    node2.ref = node1

final_count = len(gc.get_objects())
print(f"Objects before: {initial_count}")
print(f"Objects after:  {final_count}")
print(f"Leaked objects: {final_count - initial_count}")

# Clean up
LeakyNode.instances.clear()
gc.collect()

# Example 3: Memory leak - global cache
print("\n3. MEMORY LEAK - UNBOUNDED CACHE:")
print("="*70)

# Bad: Unbounded cache
class BadCache:
    _cache = {}
    
    @classmethod
    def get(cls, key):
        if key not in cls._cache:
            cls._cache[key] = [key] * 1000  # Large object
        return cls._cache[key]

print("Filling bad cache:")
tracemalloc.start()

for i in range(1000):
    BadCache.get(i)

current, _ = tracemalloc.get_traced_memory()
print(f"Memory used: {current / 1024 / 1024:.2f} MB")
print(f"Cache size: {len(BadCache._cache)} items")

tracemalloc.stop()
BadCache._cache.clear()

# Example 4: Fixed cache with size limit
print("\n4. FIXED - BOUNDED CACHE:")
print("="*70)

from collections import OrderedDict

class GoodCache:
    def __init__(self, max_size=100):
        self._cache = OrderedDict()
        self._max_size = max_size
    
    def get(self, key):
        if key not in self._cache:
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)  # Remove oldest
            self._cache[key] = [key] * 1000
        return self._cache[key]

print("Filling good cache (max 100 items):")
cache = GoodCache(max_size=100)

tracemalloc.start()

for i in range(1000):
    cache.get(i)

current, _ = tracemalloc.get_traced_memory()
print(f"Memory used: {current / 1024 / 1024:.2f} MB")
print(f"Cache size: {len(cache._cache)} items (capped at 100)")

tracemalloc.stop()

# Example 5: Detecting specific object leaks
print("\n5. TRACKING SPECIFIC OBJECTS:")
print("="*70)

class TrackedObject:
    instances = []
    
    def __init__(self, name):
        self.name = name
        TrackedObject.instances.append(self)
        print(f"   Created: {name}")
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

print("Creating objects:")
obj1 = TrackedObject("obj1")
obj2 = TrackedObject("obj2")
obj3 = TrackedObject("obj3")

print(f"\nActive instances: {len(TrackedObject.instances)}")

print("\nDeleting obj1 and obj2:")
del obj1
del obj2

print(f"Active instances: {len(TrackedObject.instances)}")

# Clean up
TrackedObject.instances.clear()
del obj3
gc.collect()

# Example 6: Memory profiling function
print("\n6. FUNCTION MEMORY PROFILING:")
print("="*70)

def profile_memory(func):
    """Decorator to profile memory usage"""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        
        result = func(*args, **kwargs)
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"\n   Function: {func.__name__}")
        print(f"   Current: {current / 1024:.2f} KB")
        print(f"   Peak:    {peak / 1024:.2f} KB")
        
        tracemalloc.stop()
        return result
    return wrapper

@profile_memory
def create_large_list():
    return [i for i in range(100000)]

@profile_memory
def create_large_dict():
    return {i: i**2 for i in range(100000)}

print("Profiling create_large_list:")
create_large_list()

print("\nProfiling create_large_dict:")
create_large_dict()

# Example 7: Weak references to avoid leaks
print("\n7. WEAK REFERENCES:")
print("="*70)

import weakref

class Resource:
    def __init__(self, name):
        self.name = name
        print(f"   Resource '{name}' created")
    
    def __del__(self):
        print(f"   Resource '{name}' deleted")

# Strong reference (prevents garbage collection)
print("Strong reference:")
resource = Resource("important")
strong_ref = resource
del resource
print("   Resource still exists (strong_ref holds it)")
del strong_ref
print("   Now deleted")

# Weak reference (doesn't prevent garbage collection)
print("\nWeak reference:")
resource = Resource("temporary")
weak_ref = weakref.ref(resource)
print(f"   Weak ref points to: {weak_ref()}")

del resource
gc.collect()
print(f"   After deletion, weak ref: {weak_ref()}")

# Example 8: Finding all instances of a class
print("\n8. FINDING LEAKED INSTANCES:")
print("="*70)

class MyClass:
    def __init__(self, value):
        self.value = value

# Create instances
instances = [MyClass(i) for i in range(5)]

# Find all MyClass instances
all_objects = gc.get_objects()
my_class_objects = [obj for obj in all_objects if isinstance(obj, MyClass)]

print(f"Found {len(my_class_objects)} MyClass instances")
print(f"Values: {[obj.value for obj in my_class_objects]}")

# Example 9: Memory leak in closure
print("\n9. CLOSURE MEMORY LEAK:")
print("="*70)

def create_closure_leak():
    large_data = [i for i in range(100000)]
    
    def inner():
        # Captures large_data even if not used
        return "Hello"
    
    return inner

print("Creating closures with captured data:")
tracemalloc.start()

funcs = [create_closure_leak() for _ in range(10)]

current, _ = tracemalloc.get_traced_memory()
print(f"Memory used: {current / 1024 / 1024:.2f} MB")

tracemalloc.stop()

# Example 10: Memory leak detection summary
print("\n10. LEAK DETECTION CHECKLIST:")
print("="*70)

print("""
✓ Use tracemalloc for memory tracking
✓ Monitor gc.get_objects() count
✓ Check for circular references
✓ Limit cache sizes
✓ Use weak references when appropriate
✓ Profile with memory_profiler
✓ Clean up event handlers
✓ Avoid capturing large objects in closures
✓ Use context managers for resources
✓ Regularly run gc.collect() in long-running apps
""")