"""
CONCEPT: String Interning
- Store only one copy of each distinct string
- Multiple references point to same object
- Automatic for identifiers (variable names)
- Manual with sys.intern() for other strings

Memory Savings:
- Each unique string stored once
- References use 8 bytes (pointer)
- String overhead: ~50+ bytes per string
- Savings = (string_size + overhead) * (copies - 1)

When to Intern:
✓ Many duplicate strings
✓ Long-lived strings (not temporary)
✓ Dictionary keys
✓ Configuration values
✗ Temporary strings
✗ Unique strings
✗ Very large strings (>1KB)
"""

import sys
import gc

print("="*70)
print("Program 17: sys.intern() AND STRING OPTIMIZATION")
print("="*70)

# Example 1: Automatic interning
print("\n1. AUTOMATIC INTERNING:")
print("="*70)

# Identifiers are automatically interned
s1 = "hello"
s2 = "hello"
print(f"Identifier strings:")
print(f"   s1: id={id(s1)}")
print(f"   s2: id={id(s2)}")
print(f"   Same object: {s1 is s2}")

# Strings with special characters may not be interned
s3 = "hello world!"
s4 = "hello world!"
print(f"\nStrings with spaces:")
print(f"   s3: id={id(s3)}")
print(f"   s4: id={id(s4)}")
print(f"   Same object: {s3 is s4}")

# Computed strings usually not interned
s5 = "hel" + "lo"
s6 = "hel" + "lo"
print(f"\nComputed strings:")
print(f"   s5: id={id(s5)}")
print(f"   s6: id={id(s6)}")
print(f"   Same object: {s5 is s6}")

# Example 2: Manual interning
print("\n2. MANUAL INTERNING WITH sys.intern():")
print("="*70)

# Before interning
s1 = "Python Programming Language"
s2 = "Python Programming Language"
print(f"Before interning:")
print(f"   s1: id={id(s1)}")
print(f"   s2: id={id(s2)}")
print(f"   Same object: {s1 is s2}")

# After interning
s3 = sys.intern("Python Programming Language")
s4 = sys.intern("Python Programming Language")
print(f"\nAfter interning:")
print(f"   s3: id={id(s3)}")
print(f"   s4: id={id(s4)}")
print(f"   Same object: {s3 is s4}")

# Example 3: Memory savings calculation
print("\n3. MEMORY SAVINGS CALCULATION:")
print("="*70)

# Without interning
print("Without interning (1000 copies):")
strings_without = []
for _ in range(1000):
    strings_without.append("Configuration Value String")

# Count unique objects
unique_ids = len(set(id(s) for s in strings_without))
total_size = sum(sys.getsizeof(s) for s in strings_without)

print(f"   Unique objects: {unique_ids}")
print(f"   Total memory: {total_size:,} bytes")

# With interning
print("\nWith interning (1000 copies):")
strings_with = []
interned = sys.intern("Configuration Value String")
for _ in range(1000):
    strings_with.append(interned)

unique_ids = len(set(id(s) for s in strings_with))
total_size = sum(sys.getsizeof(s) for s in strings_with)

print(f"   Unique objects: {unique_ids}")
print(f"   Total memory: {total_size:,} bytes")

# Calculate savings
savings = sum(sys.getsizeof(s) for s in strings_without) - sum(sys.getsizeof(s) for s in strings_with)
print(f"\nMemory saved: {savings:,} bytes")

# Example 4: Dictionary keys optimization
print("\n4. DICTIONARY KEYS OPTIMIZATION:")
print("="*70)

# Without interning - many dicts with same keys
print("Without interning:")
dicts_without = []
for i in range(1000):
    dicts_without.append({
        'username': f'user{i}',
        'email': f'user{i}@example.com',
        'status': 'active',
        'role': 'user'
    })

# Count unique key objects
all_keys = []
for d in dicts_without:
    all_keys.extend(d.keys())
unique_key_ids = len(set(id(k) for k in all_keys))
print(f"   Unique key objects: {unique_key_ids}")

# With interning
print("\nWith interning:")
# Intern the keys
username_key = sys.intern('username')
email_key = sys.intern('email')
status_key = sys.intern('status')
role_key = sys.intern('role')

dicts_with = []
for i in range(1000):
    dicts_with.append({
        username_key: f'user{i}',
        email_key: f'user{i}@example.com',
        status_key: 'active',
        role_key: 'user'
    })

all_keys = []
for d in dicts_with:
    all_keys.extend(d.keys())
unique_key_ids = len(set(id(k) for k in all_keys))
print(f"   Unique key objects: {unique_key_ids}")

# Example 5: Comparison speed improvement
print("\n5. COMPARISON SPEED:")
print("="*70)

import time

# Without interning
s1 = "A very long string for comparison testing" * 10
s2 = "A very long string for comparison testing" * 10

iterations = 1_000_000
start = time.time()
for _ in range(iterations):
    result = (s1 == s2)
without_time = time.time() - start

print(f"Without interning (== comparison): {without_time:.4f} seconds")

# With interning (can use 'is' instead)
s3 = sys.intern("A very long string for comparison testing" * 10)
s4 = sys.intern("A very long string for comparison testing" * 10)

start = time.time()
for _ in range(iterations):
    result = (s3 is s4)
with_time = time.time() - start

print(f"With interning ('is' comparison): {with_time:.4f} seconds")
print(f"Speedup: {without_time / with_time:.2f}x faster")

# Example 6: Interning in data structures
print("\n6. INTERNING IN DATA STRUCTURES:")
print("="*70)

class ConfigManager:
    """Configuration manager with interned keys"""
    
    def __init__(self):
        self._configs = []
        # Pre-intern common keys
        self._keys = {
            'host': sys.intern('host'),
            'port': sys.intern('port'),
            'database': sys.intern('database'),
            'username': sys.intern('username'),
            'password': sys.intern('password')
        }
    
    def add_config(self, **kwargs):
        """Add configuration with interned keys"""
        config = {}
        for key, value in kwargs.items():
            interned_key = self._keys.get(key, sys.intern(key))
            config[interned_key] = value
        self._configs.append(config)
    
    def get_memory_usage(self):
        """Calculate memory usage"""
        total = sum(sys.getsizeof(c) for c in self._configs)
        return total

# Test with many configs
manager = ConfigManager()

print("Adding 1000 configurations:")
for i in range(1000):
    manager.add_config(
        host='localhost',
        port=5432,
        database=f'db_{i}',
        username='admin',
        password='secret'
    )

memory = manager.get_memory_usage()
print(f"   Memory used: {memory:,} bytes")

# Example 7: String pool visualization
print("\n7. STRING POOL VISUALIZATION:")
print("="*70)

def analyze_string_pool(strings):
    """Analyze string interning"""
    unique_objects = {}
    for s in strings:
        obj_id = id(s)
        if obj_id not in unique_objects:
            unique_objects[obj_id] = {'string': s, 'count': 0}
        unique_objects[obj_id]['count'] += 1
    
    return unique_objects

# Create strings
strings = []
for _ in range(10):
    strings.append(sys.intern("error"))
    strings.append(sys.intern("warning"))
    strings.append(sys.intern("info"))

pool = analyze_string_pool(strings)

print(f"String pool analysis:")
for obj_id, info in pool.items():
    print(f"   '{info['string']}': {info['count']} references → id={obj_id}")

# Example 8: Interning with JSON data
print("\n8. JSON DATA INTERNING:")
print("="*70)

import json

json_data = '''
[
    {"status": "active", "type": "user", "level": "admin"},
    {"status": "active", "type": "user", "level": "member"},
    {"status": "inactive", "type": "user", "level": "guest"},
    {"status": "active", "type": "user", "level": "member"}
]
'''

# Without interning
print("Without interning:")
data = json.loads(json_data)
all_strings = []
for item in data:
    all_strings.extend(item.keys())
    all_strings.extend(str(v) for v in item.values())

unique_ids = len(set(id(s) for s in all_strings))
print(f"   Unique string objects: {unique_ids}")

# With interning
print("\nWith interning:")
data = json.loads(json_data)
interned_data = []

for item in data:
    interned_item = {
        sys.intern(k): sys.intern(str(v))
        for k, v in item.items()
    }
    interned_data.append(interned_item)

all_strings = []
for item in interned_data:
    all_strings.extend(item.keys())
    all_strings.extend(item.values())

unique_ids = len(set(id(s) for s in all_strings))
print(f"   Unique string objects: {unique_ids}")

# Example 9: Enum-like values
print("\n9. ENUM-LIKE VALUES:")
print("="*70)

class Status:
    """Status constants with interning"""
    ACTIVE = sys.intern('ACTIVE')
    INACTIVE = sys.intern('INACTIVE')
    PENDING = sys.intern('PENDING')
    SUSPENDED = sys.intern('SUSPENDED')

class User:
    def __init__(self, name, status):
        self.name = name
        self.status = status

# Create many users
users = []
for i in range(1000):
    status = Status.ACTIVE if i % 2 == 0 else Status.INACTIVE
    users.append(User(f"user{i}", status))

# Check that status strings are shared
status_ids = set(id(u.status) for u in users)
print(f"Created {len(users)} users")
print(f"Unique status objects: {len(status_ids)}")
print("(Should be 2: ACTIVE and INACTIVE)")

# Example 10: Automatic cleanup of interned strings
print("\n10. INTERNED STRING LIFETIME:")
print("="*70)

# Interned strings are never garbage collected
# They stay in intern table until program ends

def create_interned_strings():
    """Create some interned strings"""
    s1 = sys.intern("temporary_string_1")
    s2 = sys.intern("temporary_string_2")
    return s1, s2

print("Creating interned strings:")
str1, str2 = create_interned_strings()
id1, id2 = id(str1), id(str2)

print(f"   str1 id: {id1}")
print(f"   str2 id: {id2}")

# Delete references
del str1, str2
gc.collect()

# Create same strings again
str3 = sys.intern("temporary_string_1")
str4 = sys.intern("temporary_string_2")

print(f"\nAfter deletion and recreation:")
print(f"   str3 id: {id(str3)} (same as str1: {id(str3) == id1})")
print(f"   str4 id: {id(str4)} (same as str2: {id(str4) == id2})")
print("\nInterned strings persist in memory!")

# Example 11: Real-world use case - Log processing
print("\n11. LOG PROCESSING USE CASE:")
print("="*70)

class LogProcessor:
    """Process logs with interned level strings"""
    
    def __init__(self):
        self.logs = []
        # Pre-intern log levels
        self.levels = {
            'DEBUG': sys.intern('DEBUG'),
            'INFO': sys.intern('INFO'),
            'WARNING': sys.intern('WARNING'),
            'ERROR': sys.intern('ERROR'),
            'CRITICAL': sys.intern('CRITICAL')
        }
    
    def add_log(self, level, message):
        """Add log entry with interned level"""
        interned_level = self.levels.get(level, sys.intern(level))
        self.logs.append({
            'level': interned_level,
            'message': message
        })
    
    def count_by_level(self):
        """Count logs by level (fast with 'is')"""
        counts = {}
        for log in self.logs:
            level = log['level']
            counts[level] = counts.get(level, 0) + 1
        return counts

processor = LogProcessor()

# Add many logs
import random
levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

print("Adding 10,000 log entries:")
for i in range(10000):
    level = random.choice(levels)
    processor.add_log(level, f"Log message {i}")

counts = processor.count_by_level()
print("\nLog level counts:")
for level, count in counts.items():
    print(f"   {level}: {count}")

# Check that levels are shared
level_ids = set(id(log['level']) for log in processor.logs)
print(f"\nUnique level objects: {len(level_ids)}")

# Example 12: Performance in large datasets
print("\n12. LARGE DATASET PERFORMANCE:")
print("="*70)

import time
import tracemalloc

n = 100000

# Without interning
tracemalloc.start()
start = time.time()

data_without = []
for i in range(n):
    data_without.append({
        'status': 'active',
        'type': 'standard',
        'category': 'general'
    })

without_time = time.time() - start
current, peak = tracemalloc.get_traced_memory()
without_memory = peak / 1024 / 1024
tracemalloc.stop()

# With interning
tracemalloc.start()
start = time.time()

status_key = sys.intern('status')
type_key = sys.intern('type')
category_key = sys.intern('category')
active_val = sys.intern('active')
standard_val = sys.intern('standard')
general_val = sys.intern('general')

data_with = []
for i in range(n):
    data_with.append({
        status_key: active_val,
        type_key: standard_val,
        category_key: general_val
    })

with_time = time.time() - start
current, peak = tracemalloc.get_traced_memory()
with_memory = peak / 1024 / 1024
tracemalloc.stop()

print(f"Creating {n:,} dictionaries:")
print(f"\nWithout interning:")
print(f"   Time: {without_time:.4f} seconds")
print(f"   Memory: {without_memory:.2f} MB")

print(f"\nWith interning:")
print(f"   Time: {with_time:.4f} seconds")
print(f"   Memory: {with_memory:.2f} MB")

print(f"\nSavings:")
print(f"   Time: {(without_time - with_time):.4f} seconds")
print(f"   Memory: {(without_memory - with_memory):.2f} MB")

# Example 13: Summary and best practices
print("\n13. STRING INTERNING SUMMARY:")
print("="*70)

print("""
When to Use String Interning:
✓ Many duplicate strings (100+)
✓ Dictionary keys in many dicts
✓ Enum-like constant values
✓ Configuration keys
✓ Log levels/categories
✓ Status strings
✓ Long-lived strings
✓ Frequently compared strings

When NOT to Use:
✗ Unique strings
✗ Temporary strings
✗ User input (unbounded)
✗ Very large strings (>1KB)
✗ Few duplicates (<10)

Benefits:
- Memory savings: ~50-60 bytes per duplicate
- Faster comparison: 'is' vs '==' 
- Dictionary lookup speedup
- Reduced string objects

Limitations:
- Interned strings never freed
- Intern table overhead
- Not automatic for all strings
- No benefit for unique strings

Best Practices:
1. Intern at creation time (not runtime)
2. Pre-intern known constants
3. Use for dictionary keys
4. Intern in __init__ or module level
5. Document interned attributes
6. Don't intern user input
7. Profile memory savings
8. Consider memory vs speed trade-off

Pattern:
# Module level constants
STATUS_ACTIVE = sys.intern('ACTIVE')
STATUS_INACTIVE = sys.intern('INACTIVE')

# Use throughout application
user.status = STATUS_ACTIVE

Memory Formula:
savings = (string_size + 50) * (num_copies - 1)
Example: 20-char string, 1000 copies
savings = (20 + 50) * 999 = ~70 KB
""")