"""
CONCEPT: Memory Profiling
- Measure memory consumption of Python objects
- Identify memory-heavy data structures
- Find memory leaks in long-running applications
- Optimize memory usage

Key Functions:
- sys.getsizeof() - Base object size
- Recursive calculation for nested structures
- Track references to avoid circular loops

Memory Considerations:
1. Python objects have overhead (pointers, reference counts)
2. Containers (list, dict) store references, not values
3. Strings are immutable and cached
4. Numbers are objects with overhead
"""

import sys
from typing import Any, Set

def get_object_size(obj: Any, seen: Set[int] = None) -> int:
    """
    Recursively calculate total size of an object including all referenced objects
    
    Args:
        obj: Object to measure
        seen: Set of object IDs already counted (prevents infinite loops)
    
    Returns:
        Total size in bytes
    """
    # Base size of the object
    size = sys.getsizeof(obj)
    
    # Initialize seen set on first call
    if seen is None:
        seen = set()
    
    # Get unique ID of object
    obj_id = id(obj)
    
    # If already counted, return 0 to avoid double-counting
    if obj_id in seen:
        return 0
    
    # Mark as seen
    seen.add(obj_id)
    
    # Handle different object types
    if isinstance(obj, dict):
        # Dictionaries: count keys and values
        size += sum([get_object_size(v, seen) for v in obj.values()])
        size += sum([get_object_size(k, seen) for k in obj.keys()])
        
    elif hasattr(obj, '__dict__'):
        # Custom objects: count their attributes
        size += get_object_size(obj.__dict__, seen)
        
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        # Iterables (list, tuple, set): count elements
        try:
            size += sum([get_object_size(i, seen) for i in obj])
        except TypeError:
            pass  # Some iterables can't be iterated multiple times
    
    return size

def format_bytes(size: int) -> str:
    """Format bytes into human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def analyze_memory(obj: Any, name: str = "Object"):
    """
    Analyze and print memory usage of an object
    """
    size = get_object_size(obj)
    base_size = sys.getsizeof(obj)
    
    print(f"\n{'='*60}")
    print(f"Memory Analysis: {name}")
    print(f"{'='*60}")
    print(f"Type: {type(obj).__name__}")
    print(f"Base Size: {format_bytes(base_size)} ({base_size:,} bytes)")
    print(f"Total Size: {format_bytes(size)} ({size:,} bytes)")
    
    if hasattr(obj, '__len__'):
        try:
            length = len(obj)
            print(f"Length: {length:,} items")
            if length > 0:
                avg_size = size / length
                print(f"Average per item: {format_bytes(avg_size)}")
        except TypeError:
            pass
    
    print(f"{'='*60}")

def compare_data_structures():
    """
    Compare memory usage of different data structures
    """
    print("\n" + "="*60)
    print("COMPARING DIFFERENT DATA STRUCTURES")
    print("="*60)
    
    # Lists
    small_list = [1, 2, 3]
    medium_list = list(range(100))
    large_list = list(range(10000))
    
    analyze_memory(small_list, "Small List (3 items)")
    analyze_memory(medium_list, "Medium List (100 items)")
    analyze_memory(large_list, "Large List (10,000 items)")
    
    # Dictionaries
    small_dict = {i: i**2 for i in range(10)}
    large_dict = {i: i**2 for i in range(1000)}
    
    analyze_memory(small_dict, "Small Dictionary (10 items)")
    analyze_memory(large_dict, "Large Dictionary (1,000 items)")
    
    # Strings
    short_string = "Hello"
    long_string = "Hello" * 1000
    
    analyze_memory(short_string, "Short String")
    analyze_memory(long_string, "Long String (5,000 chars)")
    
    # Tuples vs Lists (tuples use less memory)
    list_version = [i for i in range(1000)]
    tuple_version = tuple(i for i in range(1000))
    
    analyze_memory(list_version, "List (1,000 items)")
    analyze_memory(tuple_version, "Tuple (1,000 items)")
    
    list_size = get_object_size(list_version)
    tuple_size = get_object_size(tuple_version)
    savings = list_size - tuple_size
    print(f"\nMemory savings (tuple vs list): {format_bytes(savings)}")

def detect_memory_leak():
    """
    Demonstrate memory leak detection
    """
    print("\n" + "="*60)
    print("MEMORY LEAK DETECTION")
    print("="*60)
    
    class DataProcessor:
        def __init__(self):
            self.cache = []  # Potential memory leak if not cleared
        
        def process(self, data):
            # Each call adds to cache without clearing
            self.cache.append(data)
            return sum(data)
    
    processor = DataProcessor()
    
    print("\nProcessing data in loop...")
    for i in range(5):
        data = list(range(1000))
        processor.process(data)
        
        cache_size = get_object_size(processor.cache)
        print(f"Iteration {i+1}: Cache size = {format_bytes(cache_size)}")
    
    print("\nNotice: Cache grows with each iteration!")
    print("Solution: Clear cache periodically or use limited-size cache")

def nested_structure_analysis():
    """
    Analyze complex nested data structures
    """
    print("\n" + "="*60)
    print("NESTED STRUCTURE ANALYSIS")
    print("="*60)
    
    # Complex nested structure
    company = {
        'name': 'TechCorp',
        'employees': [
            {
                'id': i,
                'name': f'Employee_{i}',
                'projects': [f'Project_{j}' for j in range(10)],
                'skills': ['Python', 'JavaScript', 'SQL']
            }
            for i in range(100)
        ],
        'departments': {
            f'Dept_{i}': {
                'budget': 1000000,
                'staff_count': 50
            }
            for i in range(10)
        }
    }
    
    analyze_memory(company, "Complex Company Structure")
    
    # Break down by component
    analyze_memory(company['employees'], "Employees List")
    analyze_memory(company['departments'], "Departments Dict")
    analyze_memory(company['employees'][0], "Single Employee")

class MemoryHeavyClass:
    """Example class with significant memory usage"""
    def __init__(self, size):
        self.data = list(range(size))
        self.metadata = {i: f"item_{i}" for i in range(size//10)}
        self.name = f"Object with {size} items"

def object_comparison():
    """
    Compare memory usage of custom objects
    """
    print("\n" + "="*60)
    print("CUSTOM OBJECT MEMORY USAGE")
    print("="*60)
    
    obj_small = MemoryHeavyClass(100)
    obj_large = MemoryHeavyClass(10000)
    
    analyze_memory(obj_small, "Small Object (100 items)")
    analyze_memory(obj_large, "Large Object (10,000 items)")

# Run all demonstrations
print("MEMORY PROFILING DEMONSTRATION")
print("="*60)

compare_data_structures()
detect_memory_leak()
nested_structure_analysis()
object_comparison()

print("\n" + "="*60)
print("MEMORY PROFILING COMPLETE")
print("="*60)