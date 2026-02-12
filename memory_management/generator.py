"""
CONCEPT: Generator Memory Efficiency
- Generator: Function that yields values one at a time
- Iterator: Object with __iter__() and __next__()
- Lazy evaluation: Compute only when needed
- Memory efficient: Don't store entire sequence

Generator vs List:
List: [x**2 for x in range(n)]  # All in memory
Generator: (x**2 for x in range(n))  # One at a time

Benefits:
- Reduced memory usage
- Can represent infinite sequences
- Faster startup time
- Better for pipelines


Use Cases:
- Large file processing
- Infinite sequences
- Data pipelines
- Streaming data
"""

import sys
import time
import tracemalloc

print("="*70)
print("Program 15: GENERATOR MEMORY EFFICIENCY")
print("="*70)

# Example 1: Basic generator vs list
print("\n1. GENERATOR VS LIST:")
print("="*70)

# List comprehension (all in memory)
list_comp = [x**2 for x in range(10)]
print(f"List: {list_comp}")
print(f"List size: {sys.getsizeof(list_comp)} bytes")

# Generator expression (one at a time)
gen_exp = (x**2 for x in range(10))
print(f"\nGenerator: {gen_exp}")
print(f"Generator size: {sys.getsizeof(gen_exp)} bytes")

# Consume generator
print(f"Generator values: {list(gen_exp)}")

# Example 2: Memory usage comparison
print("\n2. MEMORY USAGE COMPARISON:")
print("="*70)

n = 1_000_000

# List
tracemalloc.start()
list_data = [x for x in range(n)]
current, peak = tracemalloc.get_traced_memory()
list_memory = peak / 1024 / 1024
tracemalloc.stop()

# Generator
tracemalloc.start()
gen_data = (x for x in range(n))
# Consume it
for _ in gen_data:
    pass
current, peak = tracemalloc.get_traced_memory()
gen_memory = peak / 1024 / 1024
tracemalloc.stop()

print(f"List memory: {list_memory:.2f} MB")
print(f"Generator memory: {gen_memory:.2f} MB")
print(f"Memory saved: {list_memory - gen_memory:.2f} MB ({(1 - gen_memory/list_memory)*100:.1f}%)")

# Example 3: Generator function
print("\n3. GENERATOR FUNCTION:")
print("="*70)

def count_up_to(n):
    """Generator that counts from 1 to n"""
    count = 1
    while count <= n:
        print(f"   Yielding {count}")
        yield count
        count += 1

print("Creating generator:")
counter = count_up_to(5)
print(f"Type: {type(counter)}")

print("\nConsuming generator:")
for num in counter:
    print(f"   Received: {num}")

# Example 4: Fibonacci generator (infinite)
print("\n4. INFINITE SEQUENCE:")
print("="*70)

def fibonacci():
    """Generate Fibonacci sequence indefinitely"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print("First 10 Fibonacci numbers:")
fib = fibonacci()
for i, num in enumerate(fib):
    if i >= 10:
        break
    print(f"   F({i}) = {num}")

# Example 5: File processing generator
print("\n5. FILE PROCESSING:")
print("="*70)

# Create test file
filename = 'test_lines.txt'
with open(filename, 'w') as f:
    for i in range(10000):
        f.write(f"Line {i}: Some data here\n")

def read_lines(filename):
    """Generator to read file line by line"""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

def process_lines(lines):
    """Generator to process lines"""
    for line in lines:
        if 'Line 500' in line:
            yield line.upper()

# Memory-efficient pipeline
print("Processing large file:")
lines = read_lines(filename)
processed = process_lines(lines)

# Only loads one line at a time!
for i, line in enumerate(processed):
    if i >= 5:  # Show first 5
        break
    print(f"   {line}")

import os
os.remove(filename)

# Example 6: Generator pipeline
print("\n6. GENERATOR PIPELINE:")
print("="*70)

def numbers(n):
    """Generate numbers 0 to n-1"""
    for i in range(n):
        yield i

def square(nums):
    """Square each number"""
    for n in nums:
        yield n ** 2

def even_only(nums):
    """Filter even numbers"""
    for n in nums:
        if n % 2 == 0:
            yield n

# Build pipeline
print("Pipeline: numbers → square → even_only")
pipeline = even_only(square(numbers(10)))
result = list(pipeline)
print(f"Result: {result}")

# Example 7: Generator with send()
print("\n7. GENERATOR WITH SEND:")
print("="*70)

def running_average():
    """Calculate running average"""
    total = 0
    count = 0
    average = None
    
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)  # Prime the generator

print("Adding values:")
print(f"   After 10: {avg.send(10)}")
print(f"   After 20: {avg.send(20)}")
print(f"   After 30: {avg.send(30)}")

# Example 8: Generator state
print("\n8. GENERATOR STATE:")
print("="*70)

def stateful_gen():
    """Generator with internal state"""
    state = {"count": 0, "sum": 0}
    
    while True:
        value = yield state
        state["count"] += 1
        state["sum"] += value

gen = stateful_gen()
next(gen)  # Prime

print("Tracking state:")
for val in [5, 10, 15]:
    state = gen.send(val)
    print(f"   Sent {val}: count={state['count']}, sum={state['sum']}")

# Example 9: Performance comparison
print("\n9. PERFORMANCE COMPARISON:")
print("="*70)

n = 10_000_000

# List approach
print("List approach:")
start = time.time()
data = [x for x in range(n)]
sum_list = sum(data)
list_time = time.time() - start
print(f"   Time: {list_time:.4f} seconds")

# Generator approach
print("\nGenerator approach:")
start = time.time()
data = (x for x in range(n))
sum_gen = sum(data)
gen_time = time.time() - start
print(f"   Time: {gen_time:.4f} seconds")

print(f"\nSpeedup: {list_time / gen_time:.2f}x")
print(f"(Note: Similar times, but generator uses less memory)")

# Example 10: Generator class (iterator protocol)
print("\n10. ITERATOR CLASS:")
print("="*70)

class Countdown:
    """Custom iterator using iterator protocol"""
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print("Custom iterator:")
counter = Countdown(5)
for num in counter:
    print(f"   {num}")

# Example 11: Generator delegation (yield from)
print("\n11. GENERATOR DELEGATION:")
print("="*70)

def gen1():
    yield 1
    yield 2

def gen2():
    yield 3
    yield 4

def combined():
    """Delegate to multiple generators"""
    yield from gen1()
    yield from gen2()

print("Combined generators:")
for val in combined():
    print(f"   {val}")

# Example 12: Real-world example - log parser
print("\n12. LOG PARSER EXAMPLE:")
print("="*70)

def parse_log_file(filename):
    """Generator to parse log file"""
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(' - ')
            if len(parts) >= 3:
                yield {
                    'timestamp': parts[0],
                    'level': parts[1],
                    'message': parts[2]
                }

def filter_errors(logs):
    """Filter ERROR level logs"""
    for log in logs:
        if log['level'] == 'ERROR':
            yield log

# Create test log
log_file = 'test.log'
with open(log_file, 'w') as f:
    f.write("2024-01-01 10:00:00 - INFO - Application started\n")
    f.write("2024-01-01 10:05:00 - ERROR - Connection failed\n")
    f.write("2024-01-01 10:10:00 - INFO - Retrying connection\n")
    f.write("2024-01-01 10:15:00 - ERROR - Timeout occurred\n")

# Process logs efficiently
print("Processing logs:")
logs = parse_log_file(log_file)
errors = filter_errors(logs)

for error in errors:
    print(f"   {error['timestamp']}: {error['message']}")

os.remove(log_file)

# Example 13: Summary
print("\n13. GENERATOR SUMMARY:")
print("="*70)

print("""
When to Use Generators:
✓ Large datasets (>100K items)
✓ Streaming data
✓ Infinite sequences
✓ File processing
✓ Data pipelines
✓ Memory-constrained environments

Generator Benefits:
- Memory efficient (one item at a time)
- Lazy evaluation (compute on demand)
- Can represent infinite sequences
- Composable (build pipelines)
- Cleaner code (no manual state)

Generator Patterns:
1. Generator expression: (x for x in seq)
2. Generator function: def gen(): yield x
3. Generator class: __iter__ and __next__
4. Generator delegation: yield from other_gen()

Best Practices:
1. Use generators for large sequences
2. Build pipelines with multiple generators
3. Prime generators before send()
4. Document if generator is consumed
5. Use generator expressions when possible
6. Close generators if needed (gen.close())
7. Handle StopIteration appropriately

Performance Tips:
- Generators: low memory, good for streaming
- Lists: fast random access, all in memory
- Use generators for one-pass operations
- Use lists when need multiple passes
- Combine with itertools for efficiency
""")