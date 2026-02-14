"""
CONCEPT: Memory Efficient Data Structures
- Different structures have different memory footprints
- Choosing the right one can save significant memory
- Consider access patterns and use cases

Memory Comparison (approximate per item):
list:           ~28 bytes + 8 bytes per item
tuple:          ~24 bytes + 8 bytes per item
dict:           ~240 bytes + 24 bytes per item
set:            ~224 bytes + 24 bytes per item
deque:          ~40 bytes + 8 bytes per item
array:          ~96 bytes + itemsize bytes per item

Specialized Collections:
- deque: Fast append/pop on both ends
- Counter: Count occurrences efficiently
- defaultdict: Avoid key checking
- namedtuple: Memory-efficient records
- ChainMap: Combine dicts without copying
"""

import sys
import time
from collections import deque, Counter, defaultdict, namedtuple, ChainMap
from dataclasses import dataclass
import array

print("="*70)
print("Program 21: MEMORY EFFICIENT DATA STRUCTURES")
print("="*70)

# Example 1: List vs Tuple vs Array
print("\n1. LIST VS TUPLE VS ARRAY:")
print("="*70)

n = 10000

# List
py_list = [i for i in range(n)]
list_size = sys.getsizeof(py_list)

# Tuple
py_tuple = tuple(range(n))
tuple_size = sys.getsizeof(py_tuple)

# Array
py_array = array.array('i', range(n))
array_size = sys.getsizeof(py_array)

print(f"Storing {n:,} integers:")
print(f"   List:  {list_size:,} bytes ({list_size/n:.2f} per item)")
print(f"   Tuple: {tuple_size:,} bytes ({tuple_size/n:.2f} per item)")
print(f"   Array: {array_size:,} bytes ({array_size/n:.2f} per item)")

print(f"\nMemory savings:")
print(f"   Tuple vs List: {list_size - tuple_size:,} bytes ({(1-tuple_size/list_size)*100:.1f}%)")
print(f"   Array vs List: {list_size - array_size:,} bytes ({(1-array_size/list_size)*100:.1f}%)")

# Example 2: Deque vs List for queues
print("\n2. DEQUE VS LIST FOR QUEUES:")
print("="*70)

n = 100000

# List as queue (inefficient)
print("List as queue:")
start = time.time()
queue_list = []
for i in range(n):
    queue_list.append(i)
for i in range(n):
    queue_list.pop(0)  # O(n) operation!
list_time = time.time() - start

# Deque as queue (efficient)
print("\nDeque as queue:")
start = time.time()
queue_deque = deque()
for i in range(n):
    queue_deque.append(i)
for i in range(n):
    queue_deque.popleft()  # O(1) operation!
deque_time = time.time() - start

print(f"\nPerformance ({n:,} operations):")
print(f"   List:  {list_time:.4f} seconds")
print(f"   Deque: {deque_time:.4f} seconds")
print(f"   Speedup: {list_time/deque_time:.2f}x faster")

# Memory comparison
queue_list = list(range(1000))
queue_deque = deque(range(1000))

print(f"\nMemory (1000 items):")
print(f"   List:  {sys.getsizeof(queue_list):,} bytes")
print(f"   Deque: {sys.getsizeof(queue_deque):,} bytes")

# Example 3: Dict vs DefaultDict
print("\n3. DICT VS DEFAULTDICT:")
print("="*70)

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Regular dict (manual key checking)
print("Regular dict:")
word_count = {}
for word in words:
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1
print(f"   {word_count}")

# DefaultDict (automatic initialization)
print("\nDefaultDict:")
word_count_dd = defaultdict(int)
for word in words:
    word_count_dd[word] += 1  # No key checking needed!
print(f"   {dict(word_count_dd)}")

# Memory comparison
dict_size = sys.getsizeof(word_count)
dd_size = sys.getsizeof(word_count_dd)

print(f"\nMemory:")
print(f"   Dict:        {dict_size} bytes")
print(f"   DefaultDict: {dd_size} bytes")

# Example 4: Counter for counting
print("\n4. COUNTER FOR EFFICIENT COUNTING:")
print("="*70)

data = ["red", "blue", "red", "green", "blue", "blue", "red"]

# Manual counting
print("Manual counting:")
manual_count = {}
for item in data:
    manual_count[item] = manual_count.get(item, 0) + 1
print(f"   {manual_count}")

# Counter (optimized for counting)
print("\nCounter:")
counter = Counter(data)
print(f"   {counter}")

# Counter-specific methods
print(f"\nMost common (2): {counter.most_common(2)}")
print(f"Total count: {sum(counter.values())}")

# Memory comparison
print(f"\nMemory:")
print(f"   Manual dict: {sys.getsizeof(manual_count)} bytes")
print(f"   Counter:     {sys.getsizeof(counter)} bytes")

# Example 5: NamedTuple vs Dict vs Class
print("\n5. NAMEDTUPLE VS DICT VS CLASS:")
print("="*70)

# Regular dict
dict_point = {'x': 10, 'y': 20, 'z': 30}

# Regular class
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class_point = Point(10, 20, 30)

# NamedTuple
PointTuple = namedtuple('Point', ['x', 'y', 'z'])
named_point = PointTuple(10, 20, 30)

# Dataclass
@dataclass
class PointDataclass:
    x: int
    y: int
    z: int

dc_point = PointDataclass(10, 20, 30)

# Memory comparison
print("Single point memory:")
print(f"   Dict:       {sys.getsizeof(dict_point)} bytes")
print(f"   Class:      {sys.getsizeof(class_point)} bytes")
print(f"   NamedTuple: {sys.getsizeof(named_point)} bytes")
print(f"   Dataclass:  {sys.getsizeof(dc_point)} bytes")

# Create many points
n = 10000
print(f"\n{n:,} points:")

dict_points = [{'x': i, 'y': i*2, 'z': i*3} for i in range(n)]
class_points = [Point(i, i*2, i*3) for i in range(n)]
named_points = [PointTuple(i, i*2, i*3) for i in range(n)]

dict_total = sum(sys.getsizeof(p) for p in dict_points)
class_total = sum(sys.getsizeof(p) for p in class_points)
named_total = sum(sys.getsizeof(p) for p in named_points)

print(f"   Dict:       {dict_total:,} bytes ({dict_total/n:.2f} per point)")
print(f"   Class:      {class_total:,} bytes ({class_total/n:.2f} per point)")
print(f"   NamedTuple: {named_total:,} bytes ({named_total/n:.2f} per point)")

# Example 6: Set operations and memory
print("\n6. SET OPERATIONS:")
print("="*70)

# List with duplicates
list_data = list(range(1000)) + list(range(500))
print(f"List with duplicates: {len(list_data)} items")
print(f"   Memory: {sys.getsizeof(list_data):,} bytes")

# Set (removes duplicates)
set_data = set(list_data)
print(f"\nSet (unique items): {len(set_data)} items")
print(f"   Memory: {sys.getsizeof(set_data):,} bytes")

# Frozenset (immutable set)
frozen_data = frozenset(list_data)
print(f"\nFrozenset: {len(frozen_data)} items")
print(f"   Memory: {sys.getsizeof(frozen_data):,} bytes")

# Set operations are fast
set1 = set(range(10000))
set2 = set(range(5000, 15000))

start = time.time()
intersection = set1 & set2
union = set1 | set2
difference = set1 - set2
set_time = time.time() - start

print(f"\nSet operations time: {set_time:.6f} seconds")
print(f"   Intersection: {len(intersection)} items")
print(f"   Union: {len(union)} items")
print(f"   Difference: {len(difference)} items")

# Example 7: ChainMap for combining dicts
print("\n7. CHAINMAP VS DICT MERGING:")
print("="*70)

dict1 = {f'key{i}': i for i in range(1000)}
dict2 = {f'key{i+1000}': i for i in range(1000)}
dict3 = {f'key{i+2000}': i for i in range(1000)}

# Merging dicts (creates copy)
print("Dict merging (copy):")
start = time.time()
merged = {**dict1, **dict2, **dict3}
merge_time = time.time() - start
merge_size = sys.getsizeof(merged)

print(f"   Time: {merge_time:.6f} seconds")
print(f"   Memory: {merge_size:,} bytes")

# ChainMap (no copy, references)
print("\nChainMap (references):")
start = time.time()
chained = ChainMap(dict1, dict2, dict3)
chain_time = time.time() - start
chain_size = sys.getsizeof(chained)

print(f"   Time: {chain_time:.6f} seconds")
print(f"   Memory: {chain_size:,} bytes")

print(f"\nMemory saved: {merge_size - chain_size:,} bytes")

# Example 8: Sparse data structures
print("\n8. SPARSE DATA STRUCTURES:")
print("="*70)

# Dense list (wasteful for sparse data)
dense = [0] * 10000
for i in [10, 100, 1000, 5000]:
    dense[i] = i

dense_size = sys.getsizeof(dense)
print(f"Dense list (10000 items, 4 non-zero):")
print(f"   Memory: {dense_size:,} bytes")

# Sparse dict (efficient for sparse data)
sparse = {10: 10, 100: 100, 1000: 1000, 5000: 5000}
sparse_size = sys.getsizeof(sparse)

print(f"\nSparse dict (4 items):")
print(f"   Memory: {sparse_size:,} bytes")

print(f"\nMemory saved: {dense_size - sparse_size:,} bytes ({(1-sparse_size/dense_size)*100:.1f}%)")

# Example 9: String interning in structures
print("\n9. STRING INTERNING IN STRUCTURES:")
print("="*70)

# Without interning
print("Without interning:")
users1 = [
    {'status': 'active', 'role': 'admin'},
    {'status': 'active', 'role': 'user'},
    {'status': 'active', 'role': 'user'},
] * 1000

# Count unique string objects
all_strings1 = []
for user in users1:
    all_strings1.extend(user.keys())
    all_strings1.extend(user.values())

unique_ids1 = len(set(id(s) for s in all_strings1))
print(f"   Unique string objects: {unique_ids1}")

# With interning
print("\nWith interning:")
status_active = sys.intern('status')
status_key = sys.intern('active')
role_key = sys.intern('role')
admin_val = sys.intern('admin')
user_val = sys.intern('user')

users2 = [
    {status_active: status_key, role_key: admin_val},
    {status_active: status_key, role_key: user_val},
    {status_active: status_key, role_key: user_val},
] * 1000

all_strings2 = []
for user in users2:
    all_strings2.extend(user.keys())
    all_strings2.extend(user.values())

unique_ids2 = len(set(id(s) for s in all_strings2))
print(f"   Unique string objects: {unique_ids2}")

# Example 10: Choosing the right structure
print("\n10. STRUCTURE SELECTION GUIDE:")
print("="*70)

class StructureAnalyzer:
    """Analyze best structure for use case"""
    
    @staticmethod
    def analyze_access_pattern(description):
        """Suggest best structure based on access pattern"""
        recommendations = {
            'sequential_access': 'Use list or tuple',
            'fast_membership': 'Use set',
            'key_value_lookup': 'Use dict',
            'ordered_unique': 'Use dict (Python 3.7+) or OrderedDict',
            'queue_fifo': 'Use deque',
            'queue_priority': 'Use heapq',
            'counting': 'Use Counter',
            'sparse_data': 'Use dict (not list)',
            'fixed_records': 'Use namedtuple or dataclass',
            'numeric_array': 'Use array.array',
        }
        return recommendations.get(description, 'Analyze requirements')
    
    @staticmethod
    def compare_structures(n=1000):
        """Compare common structures"""
        import tracemalloc
        
        results = {}
        
        # List
        tracemalloc.start()
        data = list(range(n))
        current, peak = tracemalloc.get_traced_memory()
        results['list'] = {'memory': peak, 'size': len(data)}
        tracemalloc.stop()
        
        # Tuple
        tracemalloc.start()
        data = tuple(range(n))
        current, peak = tracemalloc.get_traced_memory()
        results['tuple'] = {'memory': peak, 'size': len(data)}
        tracemalloc.stop()
        
        # Set
        tracemalloc.start()
        data = set(range(n))
        current, peak = tracemalloc.get_traced_memory()
        results['set'] = {'memory': peak, 'size': len(data)}
        tracemalloc.stop()
        
        # Dict
        tracemalloc.start()
        data = {i: i for i in range(n)}
        current, peak = tracemalloc.get_traced_memory()
        results['dict'] = {'memory': peak, 'size': len(data)}
        tracemalloc.stop()
        
        # Array
        tracemalloc.start()
        data = array.array('i', range(n))
        current, peak = tracemalloc.get_traced_memory()
        results['array'] = {'memory': peak, 'size': len(data)}
        tracemalloc.stop()
        
        return results

analyzer = StructureAnalyzer()

print("Access pattern recommendations:")
patterns = [
    'sequential_access',
    'fast_membership',
    'key_value_lookup',
    'queue_fifo',
    'counting',
    'numeric_array'
]

for pattern in patterns:
    rec = analyzer.analyze_access_pattern(pattern)
    print(f"   {pattern}: {rec}")

print(f"\nStructure comparison ({1000} items):")
results = analyzer.compare_structures(1000)

for name, data in sorted(results.items(), key=lambda x: x[1]['memory']):
    mem_kb = data['memory'] / 1024
    print(f"   {name:10s}: {mem_kb:6.2f} KB")

# Example 11: Memory-efficient iterators
print("\n11. MEMORY-EFFICIENT ITERATORS:")
print("="*70)

# Range vs List
print("Range vs List:")

# List (stores all values)
list_range = list(range(1000000))
list_size = sys.getsizeof(list_range)
print(f"   list(range(1000000)): {list_size:,} bytes")

# Range object (generates on demand)
range_obj = range(1000000)
range_size = sys.getsizeof(range_obj)
print(f"   range(1000000):       {range_size:,} bytes")

print(f"   Savings: {list_size - range_size:,} bytes")

# Itertools for memory efficiency
from itertools import islice, chain, repeat

print("\nItertools examples (lazy evaluation):")

# Infinite repeat
repeater = repeat('x', 1000)
print(f"   repeat('x', 1000): {sys.getsizeof(repeater)} bytes (not 1000 strings!)")

# Chain multiple iterables
chained = chain(range(100), range(100, 200), range(200, 300))
print(f"   chain(...): {sys.getsizeof(chained)} bytes")

# Example 12: Real-world case study
print("\n12. REAL-WORLD CASE STUDY - LOG ANALYZER:")
print("="*70)

class LogAnalyzer:
    """Memory-efficient log analyzer"""
    
    def __init__(self):
        # Use appropriate structures
        self.error_count = Counter()  # For counting errors
        self.recent_errors = deque(maxlen=100)  # Limited-size queue
        self.error_types = set()  # Unique error types
        self.hourly_stats = defaultdict(int)  # Auto-initialize
    
    def process_log_line(self, line):
        """Process a log line efficiently"""
        parts = line.split()
        
        if 'ERROR' in line:
            error_type = parts[2] if len(parts) > 2 else 'UNKNOWN'
            
            self.error_count[error_type] += 1
            self.recent_errors.append(line)
            self.error_types.add(error_type)
            
            # Extract hour
            hour = parts[0].split(':')[0] if parts else '00'
            self.hourly_stats[hour] += 1
    
    def get_memory_usage(self):
        """Calculate memory usage"""
        total = (
            sys.getsizeof(self.error_count) +
            sys.getsizeof(self.recent_errors) +
            sys.getsizeof(self.error_types) +
            sys.getsizeof(self.hourly_stats)
        )
        return total
    
    def get_report(self):
        """Get analysis report"""
        return {
            'total_errors': sum(self.error_count.values()),
            'unique_error_types': len(self.error_types),
            'most_common_errors': self.error_count.most_common(3),
            'memory_usage': self.get_memory_usage()
        }

# Simulate log processing
analyzer = LogAnalyzer()

print("Processing simulated logs...")
for i in range(10000):
    if i % 10 == 0:
        analyzer.process_log_line(f"{i%24:02d}:00:00 ERROR ConnectionError Failed")
    elif i % 15 == 0:
        analyzer.process_log_line(f"{i%24:02d}:00:00 ERROR TimeoutError Slow")

report = analyzer.get_report()

print(f"\nAnalysis Report:")
print(f"   Total errors: {report['total_errors']}")
print(f"   Unique types: {report['unique_error_types']}")
print(f"   Most common: {report['most_common_errors']}")
print(f"   Memory used: {report['memory_usage']:,} bytes")

# Example 13: Summary and decision tree
print("\n13. DATA STRUCTURE DECISION TREE:")
print("="*70)

print("""
Choosing the Right Data Structure:

📊 SEQUENTIAL ACCESS (iterate once):
   ✓ Generator / Iterator
   Example: (x for x in data)

📊 RANDOM ACCESS (need indexing):
   ✓ List (mutable) or Tuple (immutable)
   Example: data[index]

📊 MEMBERSHIP TESTING (x in container):
   ✓ Set or Dict
   Example: if item in myset

📊 KEY-VALUE MAPPING:
   ✓ Dict (general)
   ✓ DefaultDict (auto-initialize)
   ✓ Counter (counting)
   ✓ ChainMap (combine without copy)

📊 QUEUE OPERATIONS:
   ✓ Deque (both ends)
   ✓ Queue (thread-safe)
   ✓ heapq (priority)

📊 UNIQUE ITEMS:
   ✓ Set (mutable)
   ✓ Frozenset (immutable, hashable)

📊 NUMERIC DATA:
   ✓ array.array (homogeneous)
   ✓ numpy (if available)

📊 RECORDS/STRUCTS:
   ✓ NamedTuple (immutable, memory-efficient)
   ✓ Dataclass (mutable, type hints)
   ✓ Dict (flexible)

📊 SPARSE DATA:
   ✓ Dict (not list with zeros)

Memory Efficiency Ranking (best to worst):
1. Generator (lazy, no storage)
2. array.array (numeric data)
3. NamedTuple
4. Tuple
5. List
6. Set
7. Dict

Performance Characteristics:
                Access  Insert  Delete  Memory
List            O(1)    O(1)*   O(n)    Good
Tuple           O(1)    N/A     N/A     Better
Deque           O(n)    O(1)    O(1)    Good
Set             O(1)    O(1)    O(1)    Medium
Dict            O(1)    O(1)    O(1)    Medium
Array           O(1)    O(1)*   O(n)    Best

* Amortized

Best Practices:
1. Profile your specific use case
2. Consider access patterns
3. Choose immutable when possible
4. Use specialized collections
5. Avoid premature optimization
6. Document structure choice
7. Test with realistic data
8. Measure memory impact
""")