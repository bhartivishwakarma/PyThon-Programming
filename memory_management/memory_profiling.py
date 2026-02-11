"""
CONCEPT: Memory Profiling Tools

Built-in Tools:
- tracemalloc: Track memory allocations
- sys.getsizeof(): Get object size
- gc: Garbage collector interface

External Tools:
- memory_profiler: Line-by-line memory usage
- objgraph: Visualize object references
- pympler: Memory measurement toolkit
- guppy3: Heap analysis

When to Profile:
- Memory grows over time
- Out of memory errors
- Performance optimization
- Finding memory leaks
"""

import sys
import tracemalloc
import gc
from collections import defaultdict

print("="*70)
print("Program 8: MEMORY PROFILING TOOLS")
print("="*70)

# Example 1: tracemalloc basics
print("\n1. TRACEMALLOC BASICS:")
print("="*70)

tracemalloc.start()

# Allocate memory
data1 = [i for i in range(10000)]
data2 = {i: i**2 for i in range(5000)}

# Get current memory
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024:.2f} KB")
print(f"Peak memory: {peak / 1024:.2f} KB")

# Get top allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("\nTop 3 allocations:")
for stat in top_stats[:3]:
    print(f"   {stat}")

tracemalloc.stop()

# Example 2: Comparing snapshots
print("\n2. SNAPSHOT COMPARISON:")
print("="*70)

tracemalloc.start()

# First snapshot
snapshot1 = tracemalloc.take_snapshot()

# Allocate more memory
big_list = []
for i in range(5000):
    big_list.append([i] * 100)

# Second snapshot
snapshot2 = tracemalloc.take_snapshot()

# Compare
stats = snapshot2.compare_to(snapshot1, 'lineno')

print("Memory changes:")
for stat in stats[:3]:
    print(f"   {stat}")

tracemalloc.stop()

# Example 3: Filtering snapshots
print("\n3. FILTERING SNAPSHOTS:")
print("="*70)

tracemalloc.start()

# Create various objects
strings = ["string" + str(i) for i in range(1000)]
numbers = [i for i in range(10000)]
dicts = [{"key": i} for i in range(500)]

snapshot = tracemalloc.take_snapshot()

# Filter by traceback
import tracemalloc

# Get statistics
stats = snapshot.statistics('lineno')

print("Filtered allocations:")
for stat in stats[:3]:
    print(f"\n   {stat}")
    for line in stat.traceback.format():
        print(f"      {line}")

tracemalloc.stop()

# Example 4: sys.getsizeof() for various objects
print("\n4. OBJECT SIZE ANALYSIS:")
print("="*70)

def get_size(obj, name="Object"):
    size = sys.getsizeof(obj)
    print(f"{name:20s}: {size:,} bytes")
    return size

# Various object types
get_size(42, "int")
get_size(3.14, "float")
get_size("Hello World", "string")
get_size([1, 2, 3], "list (3 items)")
get_size([1] * 100, "list (100 items)")
get_size({i: i for i in range(10)}, "dict (10 items)")
get_size(set(range(100)), "set (100 items)")

# Complex object
complex_obj = {
    'data': [1, 2, 3] * 1000,
    'metadata': {'name': 'test', 'version': 1}
}
get_size(complex_obj, "complex dict")

# Example 5: Custom deep size function
print("\n5. DEEP SIZE CALCULATION:")
print("="*70)

def get_deep_size(obj, seen=None):
    """
    Recursively calculate total size of object and all referenced objects
    """
    size = sys.getsizeof(obj)
    
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum(get_deep_size(v, seen) for v in obj.values())
        size += sum(get_deep_size(k, seen) for k in obj.keys())
    elif hasattr(obj, '__dict__'):
        size += get_deep_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        try:
            size += sum(get_deep_size(i, seen) for i in obj)
        except TypeError:
            pass
    
    return size

# Test deep size
nested_dict = {
    'level1': {
        'level2': {
            'level3': [1, 2, 3] * 100
        }
    },
    'data': list(range(1000))
}

shallow = sys.getsizeof(nested_dict)
deep = get_deep_size(nested_dict)

print(f"Shallow size: {shallow:,} bytes")
print(f"Deep size: {deep:,} bytes")

# Example 6: Memory by object type
print("\n6. MEMORY BY OBJECT TYPE:")
print("="*70)

def analyze_memory_by_type():
    """Analyze memory usage by object type"""
    type_stats = defaultdict(lambda: {'count': 0, 'size': 0})
    
    for obj in gc.get_objects():
        obj_type = type(obj).__name__
        type_stats[obj_type]['count'] += 1
        try:
            type_stats[obj_type]['size'] += sys.getsizeof(obj)
        except:
            pass
    
    # Sort by total size
    sorted_types = sorted(
        type_stats.items(),
        key=lambda x: x[1]['size'],
        reverse=True
    )
    
    print("Top 10 types by memory usage:")
    for i, (obj_type, stats) in enumerate(sorted_types[:10], 1):
        print(f"{i:2d}. {obj_type:15s}: {stats['count']:6d} objects, "
              f"{stats['size']:10,} bytes")

analyze_memory_by_type()

# Example 7: Function memory profiler
print("\n7. FUNCTION PROFILER:")
print("="*70)

def memory_profiler(func):
    """Decorator to profile function memory usage"""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        
        # Before
        snapshot1 = tracemalloc.take_snapshot()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # After
        snapshot2 = tracemalloc.take_snapshot()
        
        # Stats
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        print(f"\nMemory profile for {func.__name__}():")
        current, peak = tracemalloc.get_traced_memory()
        print(f"   Current: {current / 1024:.2f} KB")
        print(f"   Peak: {peak / 1024:.2f} KB")
        
        if stats:
            print(f"   Top allocation: {stats[0]}")
        
        tracemalloc.stop()
        return result
    
    return wrapper

@memory_profiler
def create_large_structure():
    return {i: [i] * 100 for i in range(1000)}

@memory_profiler
def process_strings():
    return [str(i) * 100 for i in range(1000)]

# Test profiled functions
create_large_structure()
process_strings()

# Example 8: Memory growth detector
print("\n8. MEMORY GROWTH DETECTION:")
print("="*70)

class MemoryMonitor:
    def __init__(self):
        self.samples = []
    
    def sample(self):
        """Take a memory sample"""
        current, peak = tracemalloc.get_traced_memory()
        self.samples.append(current)
    
    def analyze(self):
        """Analyze memory growth"""
        if len(self.samples) < 2:
            return
        
        print(f"Samples taken: {len(self.samples)}")
        print(f"Initial memory: {self.samples[0] / 1024:.2f} KB")
        print(f"Final memory: {self.samples[-1] / 1024:.2f} KB")
        print(f"Growth: {(self.samples[-1] - self.samples[0]) / 1024:.2f} KB")
        
        # Detect trend
        if self.samples[-1] > self.samples[0] * 1.5:
            print("⚠️  Significant memory growth detected!")

tracemalloc.start()
monitor = MemoryMonitor()

# Simulate work with memory growth
for i in range(5):
    monitor.sample()
    # Allocate memory
    data = [list(range(1000)) for _ in range(100)]

monitor.analyze()
tracemalloc.stop()

# Example 9: Reference counting analysis
print("\n9. REFERENCE COUNTING:")
print("="*70)

def analyze_references(obj, name="Object"):
    """Analyze reference count"""
    count = sys.getrefcount(obj)
    print(f"{name}: {count} references")
    
    # Find referring objects
    referrers = gc.get_referrers(obj)
    print(f"   Referred by {len(referrers)} objects")
    
    for ref in referrers[:3]:  # Show first 3
        print(f"      {type(ref).__name__}")

my_list = [1, 2, 3]
analyze_references(my_list, "my_list")

container = {'data': my_list}
analyze_references(my_list, "my_list (in container)")

# Example 10: Summary and best practices
print("\n10. PROFILING BEST PRACTICES:")
print("="*70)

print("""
Profiling Workflow:
1. Identify suspect code
2. Use tracemalloc for allocation tracking
3. Take snapshots before/after operations
4. Compare snapshots to find leaks
5. Use gc.get_objects() for object analysis
6. Profile with memory_profiler for line-level detail
7. Visualize with objgraph if needed
8. Fix identified issues
9. Re-profile to verify
10. Monitor in production

Tools Summary:
✓ tracemalloc: Built-in, allocation tracking
✓ sys.getsizeof(): Quick object size
✓ gc module: Garbage collector interface
✓ memory_profiler: Line-by-line profiling
✓ objgraph: Visualization
✓ pympler: Comprehensive toolkit
""")