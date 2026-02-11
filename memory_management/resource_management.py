"""
CONCEPT: Context Managers and Resource Management

Context Manager Protocol:
__enter__(self): Setup, return resource
__exit__(self, exc_type, exc_val, exc_tb): Cleanup

Benefits:
- Automatic resource cleanup
- Exception-safe
- Prevents resource leaks
- Clean, readable code

Common Use Cases:
- File handling
- Database connections
- Locks
- Network connections
- Custom resources
"""

import sys
from contextlib import contextmanager

print("="*70)
print("Program 9: CONTEXT MANAGERS AND RESOURCE MANAGEMENT")
print("="*70)

# Example 1: File handling with context manager
print("\n1. FILE HANDLING:")
print("="*70)

# Bad: Manual file handling (easy to forget close)
print("Without context manager:")
file = open('temp.txt', 'w')
file.write("Hello World")
# If exception occurs here, file never closes!
file.close()
print("   File closed manually")

# Good: Context manager ensures cleanup
print("\nWith context manager:")
with open('temp.txt', 'w') as file:
    file.write("Hello World")
    # File automatically closed after this block
print("   File automatically closed")

# Example 2: Custom context manager class
print("\n2. CUSTOM CONTEXT MANAGER CLASS:")
print("="*70)

class ManagedResource:
    def __init__(self, name):
        self.name = name
        print(f"   Creating resource: {name}")
    
    def __enter__(self):
        print(f"   Entering context: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"   Exiting context: {self.name}")
        print(f"   Cleaning up: {self.name}")
        if exc_type:
            print(f"   Exception occurred: {exc_type.__name__}")
        return False  # Don't suppress exceptions
    
    def do_something(self):
        print(f"   Working with: {self.name}")

print("Using custom context manager:")
with ManagedResource("Database Connection") as resource:
    resource.do_something()
print("   (Cleanup happened automatically)")

# Example 3: Context manager with exception
print("\n3. EXCEPTION HANDLING:")
print("="*70)

print("Context manager with exception:")
try:
    with ManagedResource("File Handle") as resource:
        resource.do_something()
        raise ValueError("Something went wrong!")
except ValueError as e:
    print(f"   Caught: {e}")
print("   (Cleanup still happened!)")

# Example 4: contextlib.contextmanager decorator
print("\n4. CONTEXTMANAGER DECORATOR:")
print("="*70)

@contextmanager
def managed_resource(name):
    # Setup (before yield)
    print(f"   Acquiring: {name}")
    resource = f"Resource-{name}"
    
    try:
        yield resource  # Provide resource to with block
    finally:
        # Cleanup (after yield)
        print(f"   Releasing: {name}")

print("Using @contextmanager decorator:")
with managed_resource("Memory Buffer") as res:
    print(f"   Using: {res}")

# Example 5: Multiple context managers
print("\n5. MULTIPLE CONTEXT MANAGERS:")
print("="*70)

@contextmanager
def timer(name):
    import time
    print(f"   Starting: {name}")
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"   Finished: {name} ({elapsed:.4f}s)")

print("Nested context managers:")
with timer("Outer Operation"):
    with timer("Inner Operation"):
        import time
        time.sleep(0.1)
        print("   Doing work...")

# Python 3.1+: Multiple context managers in one line
print("\nMultiple in one line:")
with timer("Operation A"), timer("Operation B"):
    print("   Working...")

# Example 6: Memory tracking context manager
print("\n6. MEMORY TRACKING CONTEXT MANAGER:")
print("="*70)

@contextmanager
def memory_tracker(operation_name):
    import tracemalloc
    
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    
    print(f"   Starting: {operation_name}")
    
    try:
        yield
    finally:
        snapshot2 = tracemalloc.take_snapshot()
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"   Memory used: {current / 1024:.2f} KB")
        print(f"   Peak memory: {peak / 1024:.2f} KB")
        
        tracemalloc.stop()

print("Tracking memory usage:")
with memory_tracker("Create Large List"):
    data = [i for i in range(100000)]

# Example 7: Lock management
print("\n7. LOCK MANAGEMENT:")
print("="*70)

import threading

class SharedResource:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    @contextmanager
    def locked_access(self):
        print(f"   Acquiring lock...")
        self.lock.acquire()
        try:
            print(f"   Lock acquired")
            yield self
        finally:
            self.lock.release()
            print(f"   Lock released")

shared = SharedResource()

print("Using lock context manager:")
with shared.locked_access() as resource:
    resource.value += 10
    print(f"   Modified value: {resource.value}")

# Example 8: Temporary attribute change
print("\n8. TEMPORARY CHANGES:")
print("="*70)

@contextmanager
def temporary_attr(obj, attr, value):
    """Temporarily change object attribute"""
    original = getattr(obj, attr)
    print(f"   Changing {attr}: {original} -> {value}")
    setattr(obj, attr, value)
    
    try:
        yield obj
    finally:
        setattr(obj, attr, original)
        print(f"   Restored {attr}: {value} -> {original}")

class Config:
    debug = False

config = Config()
print(f"Initial debug: {config.debug}")

with temporary_attr(config, 'debug', True):
    print(f"   Inside context: debug = {config.debug}")

print(f"After context: debug = {config.debug}")

# Example 9: Redirect stdout
print("\n9. REDIRECT STDOUT:")
print("="*70)

@contextmanager
def redirect_stdout(filename):
    """Redirect stdout to file"""
    import sys
    original_stdout = sys.stdout
    
    with open(filename, 'w') as f:
        sys.stdout = f
        print(f"   Redirecting output to {filename}")
        try:
            yield
        finally:
            sys.stdout = original_stdout

print("Before redirection")
with redirect_stdout('output.txt'):
    print("This goes to file")
    print("This also goes to file")
print("After redirection")
print("   (Check output.txt for redirected content)")

# Example 10: Resource pool
print("\n10. RESOURCE POOL:")
print("="*70)

class ResourcePool:
    def __init__(self, create_func, pool_size=3):
        self.create_func = create_func
        self.pool = [create_func() for _ in range(pool_size)]
        self.in_use = set()
    
    @contextmanager
    def acquire(self):
        if not self.pool:
            raise RuntimeError("Pool exhausted")
        
        resource = self.pool.pop()
        self.in_use.add(id(resource))
        print(f"   Acquired resource (pool: {len(self.pool)}, in use: {len(self.in_use)})")
        
        try:
            yield resource
        finally:
            self.in_use.remove(id(resource))
            self.pool.append(resource)
            print(f"   Released resource (pool: {len(self.pool)}, in use: {len(self.in_use)})")

# Create pool of lists
pool = ResourcePool(lambda: [], pool_size=2)

print("Using resource pool:")
with pool.acquire() as res1:
    res1.append(1)
    print(f"   Working with resource: {res1}")
    
    with pool.acquire() as res2:
        res2.append(2)
        print(f"   Working with resource: {res2}")

print("\nAll resources returned to pool")

# Example 11: Summary
print("\n11. CONTEXT MANAGER BENEFITS:")
print("="*70)

print("""
Why Use Context Managers:
✓ Automatic resource cleanup
✓ Exception-safe (cleanup happens even with errors)
✓ Prevents resource leaks
✓ Cleaner code (no try-finally boilerplate)
✓ Consistent resource management

When to Use:
- File handling
- Database connections
- Network sockets
- Locks and synchronization
- Temporary state changes
- Resource pools
- Memory tracking
- Custom cleanup logic

Best Practices:
1. Always use 'with' for files
2. Create context managers for custom resources
3. Use @contextmanager for simple cases
4. Implement __enter__/__exit__ for complex cases
5. Always cleanup in __exit__ or finally
6. Document what resources are managed
""")