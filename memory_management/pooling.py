"""
CONCEPT: Object Pooling
- Pre-create and reuse expensive objects
- Reduces garbage collection pressure
- Improves performance by avoiding repeated allocation
- Common for: DB connections, threads, network sockets

Pool Strategies:
1. Fixed-size pool: Pre-allocate N objects
2. Dynamic pool: Grow as needed, up to max
3. Lazy pool: Create on demand
4. Timed expiration: Remove unused objects

Benefits:
- Faster object access
- Reduced memory fragmentation
- Predictable memory usage
- Less GC overhead
"""

import time
import threading
from queue import Queue, Empty
from contextlib import contextmanager

print("="*70)
print("Program 11: OBJECT POOLING AND REUSABILITY")
print("="*70)

# Example 1: Simple object pool
print("\n1. BASIC OBJECT POOL:")
print("="*70)

class ExpensiveObject:
    """Simulates an expensive-to-create object"""
    instance_count = 0
    
    def __init__(self):
        ExpensiveObject.instance_count += 1
        self.id = ExpensiveObject.instance_count
        # Simulate expensive initialization
        time.sleep(0.1)
        print(f"   Created ExpensiveObject-{self.id}")
        self.data = [0] * 10000
    
    def reset(self):
        """Reset object state for reuse"""
        self.data = [0] * 10000
    
    def use(self, value):
        """Simulate using the object"""
        self.data[0] = value

class SimplePool:
    def __init__(self, obj_class, size):
        print(f"Initializing pool with {size} objects...")
        start = time.time()
        self._pool = [obj_class() for _ in range(size)]
        elapsed = time.time() - start
        print(f"Pool created in {elapsed:.2f} seconds")
        self._available = self._pool.copy()
    
    def acquire(self):
        """Get an object from the pool"""
        if self._available:
            obj = self._available.pop()
            print(f"   Acquired object-{obj.id} from pool")
            return obj
        else:
            print(f"   Pool empty! Creating new object")
            return ExpensiveObject()
    
    def release(self, obj):
        """Return object to pool"""
        obj.reset()
        self._available.append(obj)
        print(f"   Released object-{obj.id} to pool")
    
    @property
    def available_count(self):
        return len(self._available)

# Test simple pool
pool = SimplePool(ExpensiveObject, 3)

print(f"\nUsing pool (available: {pool.available_count}):")
obj1 = pool.acquire()
obj1.use(100)

obj2 = pool.acquire()
obj2.use(200)

print(f"\nReleasing objects:")
pool.release(obj1)
pool.release(obj2)

print(f"\nPool status: {pool.available_count} available")

# Example 2: Thread-safe object pool
print("\n2. THREAD-SAFE POOL:")
print("="*70)

class ThreadSafePool:
    def __init__(self, obj_class, size):
        self._queue = Queue(maxsize=size)
        self._size = size
        self._lock = threading.Lock()
        
        # Pre-populate pool
        for _ in range(size):
            self._queue.put(obj_class())
    
    def acquire(self, timeout=None):
        """Get object with optional timeout"""
        try:
            obj = self._queue.get(timeout=timeout)
            return obj
        except Empty:
            raise RuntimeError("Pool exhausted")
    
    def release(self, obj):
        """Return object to pool"""
        obj.reset()
        try:
            self._queue.put_nowait(obj)
        except:
            pass  # Pool full, discard object
    
    @contextmanager
    def get_object(self):
        """Context manager for automatic return"""
        obj = self.acquire()
        try:
            yield obj
        finally:
            self.release(obj)

class PooledResource:
    def __init__(self):
        self.value = 0
    
    def reset(self):
        self.value = 0
    
    def process(self, data):
        self.value = data * 2
        return self.value

thread_pool = ThreadSafePool(PooledResource, 3)

print("Using thread-safe pool:")
with thread_pool.get_object() as obj:
    result = obj.process(10)
    print(f"   Processed: {result}")

# Example 3: Dynamic pool with max size
print("\n3. DYNAMIC POOL:")
print("="*70)

class DynamicPool:
    def __init__(self, obj_class, initial_size=2, max_size=10):
        self._obj_class = obj_class
        self._max_size = max_size
        self._pool = [obj_class() for _ in range(initial_size)]
        self._in_use = set()
        self._created_count = initial_size
    
    def acquire(self):
        """Acquire object, create new if needed"""
        if self._pool:
            obj = self._pool.pop()
            self._in_use.add(id(obj))
            print(f"   Reused object (pool: {len(self._pool)}, in use: {len(self._in_use)})")
            return obj
        elif self._created_count < self._max_size:
            obj = self._obj_class()
            self._created_count += 1
            self._in_use.add(id(obj))
            print(f"   Created new object (total: {self._created_count})")
            return obj
        else:
            raise RuntimeError(f"Pool at maximum size ({self._max_size})")
    
    def release(self, obj):
        """Return object to pool"""
        obj_id = id(obj)
        if obj_id in self._in_use:
            self._in_use.remove(obj_id)
            obj.reset()
            self._pool.append(obj)
            print(f"   Released (pool: {len(self._pool)}, in use: {len(self._in_use)})")

dynamic_pool = DynamicPool(PooledResource, initial_size=2, max_size=5)

print("Testing dynamic pool:")
objs = []
for i in range(4):
    obj = dynamic_pool.acquire()
    objs.append(obj)

print("\nReleasing objects:")
for obj in objs:
    dynamic_pool.release(obj)

# Example 4: Connection pool simulation
print("\n4. DATABASE CONNECTION POOL:")
print("="*70)

class DatabaseConnection:
    """Simulates a database connection"""
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.is_open = True
        print(f"   Opened connection-{conn_id}")
    
    def execute(self, query):
        if not self.is_open:
            raise RuntimeError("Connection closed")
        return f"Result of: {query}"
    
    def reset(self):
        """Reset connection state"""
        pass
    
    def close(self):
        self.is_open = False
        print(f"   Closed connection-{conn_id}")

class ConnectionPool:
    def __init__(self, size=5):
        self._connections = Queue(maxsize=size)
        self._size = size
        self._created = 0
        self._lock = threading.Lock()
    
    def _create_connection(self):
        """Create new connection"""
        with self._lock:
            self._created += 1
            return DatabaseConnection(self._created)
    
    @contextmanager
    def get_connection(self):
        """Get connection with automatic return"""
        # Try to get from pool
        try:
            conn = self._connections.get_nowait()
            print(f"   Got connection-{conn.conn_id} from pool")
        except Empty:
            if self._created < self._size:
                conn = self._create_connection()
            else:
                # Wait for available connection
                conn = self._connections.get()
                print(f"   Waited for connection-{conn.conn_id}")
        
        try:
            yield conn
        finally:
            conn.reset()
            self._connections.put(conn)
            print(f"   Returned connection-{conn.conn_id} to pool")

# Test connection pool
conn_pool = ConnectionPool(size=2)

print("Using connection pool:")
with conn_pool.get_connection() as conn:
    result = conn.execute("SELECT * FROM users")
    print(f"   Query result: {result}")

with conn_pool.get_connection() as conn:
    result = conn.execute("SELECT * FROM posts")
    print(f"   Query result: {result}")

# Example 5: Performance comparison
print("\n5. PERFORMANCE COMPARISON:")
print("="*70)

class HeavyObject:
    def __init__(self):
        self.data = [i**2 for i in range(10000)]
    
    def reset(self):
        pass
    
    def compute(self, x):
        return sum(self.data[:x])

# Without pooling
print("Without pooling:")
start = time.time()
for _ in range(100):
    obj = HeavyObject()
    result = obj.compute(100)
    del obj
time_no_pool = time.time() - start
print(f"   Time: {time_no_pool:.4f} seconds")

# With pooling
print("\nWith pooling:")
pool = SimplePool(HeavyObject, 10)
start = time.time()
for _ in range(100):
    obj = pool.acquire()
    result = obj.compute(100)
    pool.release(obj)
time_with_pool = time.time() - start
print(f"   Time: {time_with_pool:.4f} seconds")

speedup = time_no_pool / time_with_pool
print(f"\nSpeedup: {speedup:.2f}x faster with pooling")

# Example 6: Memory comparison
print("\n6. MEMORY USAGE COMPARISON:")
print("="*70)

import tracemalloc
import gc

# Without pooling
tracemalloc.start()
gc.collect()

objects = []
for _ in range(50):
    obj = HeavyObject()
    objects.append(obj)
    del obj

current, peak = tracemalloc.get_traced_memory()
no_pool_memory = peak / 1024 / 1024

tracemalloc.stop()
objects.clear()
gc.collect()

# With pooling
tracemalloc.start()
gc.collect()

pool = SimplePool(HeavyObject, 5)
for _ in range(50):
    obj = pool.acquire()
    pool.release(obj)

current, peak = tracemalloc.get_traced_memory()
with_pool_memory = peak / 1024 / 1024

tracemalloc.stop()

print(f"Memory without pooling: {no_pool_memory:.2f} MB")
print(f"Memory with pooling: {with_pool_memory:.2f} MB")
print(f"Memory saved: {no_pool_memory - with_pool_memory:.2f} MB")

# Example 7: Object pool best practices
print("\n7. POOL BEST PRACTICES:")
print("="*70)

print("""
✓ When to Use Object Pooling:
  • Object creation is expensive
  • Objects are reused frequently
  • Predictable object lifecycle
  • Need to limit resource count
  • Want to reduce GC pressure

✓ Pool Design Considerations:
  • Initial pool size (warm-up)
  • Maximum pool size (limit resources)
  • Thread safety (if needed)
  • Object validation before reuse
  • Idle object cleanup
  • Pool statistics/monitoring

✓ Good Candidates for Pooling:
  • Database connections
  • Thread objects
  • Network sockets
  • Large buffers/arrays
  • Expensive computations
  • File handles

✗ Poor Candidates:
  • Simple objects (int, str)
  • Objects with complex state
  • Rarely reused objects
  • Objects with side effects
  • Small, cheap objects
""")