"""
CONCEPT: Weak References
- Normal reference: Prevents object deletion
- Weak reference: Allows garbage collection
- Object can be deleted even if weak refs exist
- Useful for: caches, observers, callbacks

Types:
- weakref.ref(): Single weak reference
- WeakValueDictionary: Dict with weak values
- WeakKeyDictionary: Dict with weak keys
- WeakSet: Set with weak references

Benefits:
- Prevent memory leaks in caches
- Automatic cleanup
- No circular reference issues
- Observer pattern without leaks
"""

import weakref
import gc
import sys

print("="*70)
print("Program 13: WEAK REFERENCES AND CACHING")
print("="*70)

# Example 1: Strong vs weak references
print("\n1. STRONG VS WEAK REFERENCES:")
print("="*70)

class MyObject:
    def __init__(self, name):
        self.name = name
        print(f"   Created: {name}")
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

# Strong reference
print("Strong reference:")
obj = MyObject("StrongRef")
print(f"Reference count: {sys.getrefcount(obj)}")

del obj
gc.collect()
print("Object still exists until garbage collected")

# Weak reference
print("\nWeak reference:")
obj = MyObject("WeakRef")
weak_ref = weakref.ref(obj)

print(f"Weak ref alive: {weak_ref() is not None}")
print(f"Strong ref count: {sys.getrefcount(obj)}")

del obj
gc.collect()

print(f"After del obj:")
print(f"Weak ref alive: {weak_ref() is not None}")
print(f"Weak ref points to: {weak_ref()}")

# Example 2: Weak reference callbacks
print("\n2. WEAK REFERENCE CALLBACKS:")
print("="*70)

def callback(ref):
    print(f"   Callback: Object being deleted")

obj = MyObject("CallbackObj")
weak_ref = weakref.ref(obj, callback)

print("Deleting object:")
del obj
gc.collect()

# Example 3: WeakValueDictionary cache
print("\n3. WEAKVALUEDICTIONARY CACHE:")
print("="*70)

class ExpensiveObject:
    def __init__(self, id):
        self.id = id
        print(f"   Created expensive object: {id}")
    
    def __del__(self):
        print(f"   Cleaned up: {id}")

# Bad: Regular dict cache (memory leak!)
print("Regular dict cache (memory leak):")
regular_cache = {}

obj1 = ExpensiveObject("obj1")
regular_cache['key1'] = obj1

del obj1  # Object NOT deleted (cache holds reference)
gc.collect()
print(f"   Cache size: {len(regular_cache)}")

regular_cache.clear()
gc.collect()

# Good: Weak dict cache (auto cleanup)
print("\nWeakValueDictionary cache:")
weak_cache = weakref.WeakValueDictionary()

obj2 = ExpensiveObject("obj2")
weak_cache['key2'] = obj2

print(f"   Cache size: {len(weak_cache)}")

del obj2  # Object IS deleted (weak reference)
gc.collect()

print(f"   Cache size after del: {len(weak_cache)}")

# Example 4: Object cache with automatic cleanup
print("\n4. SMART CACHE IMPLEMENTATION:")
print("="*70)

class SmartCache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
        self._stats = {'hits': 0, 'misses': 0, 'cleanups': 0}
    
    def get(self, key, factory):
        """Get object from cache or create new"""
        if key in self._cache:
            self._stats['hits'] += 1
            print(f"   Cache HIT: {key}")
            return self._cache[key]
        else:
            self._stats['misses'] += 1
            print(f"   Cache MISS: {key}")
            obj = factory(key)
            self._cache[key] = obj
            return obj
    
    def cleanup(self):
        """Force cleanup of dead references"""
        # Weak dict auto-cleans, but we can check
        before = len(self._cache)
        gc.collect()
        after = len(self._cache)
        cleaned = before - after
        self._stats['cleanups'] += cleaned
        return cleaned
    
    def stats(self):
        return self._stats.copy()

# Test smart cache
cache = SmartCache()

print("Using smart cache:")
obj1 = cache.get('user:1', lambda k: ExpensiveObject(k))
obj2 = cache.get('user:1', lambda k: ExpensiveObject(k))  # Cache hit!

print(f"\nobj1 is obj2: {obj1 is obj2}")

# Delete reference
del obj1, obj2
cleaned = cache.cleanup()
print(f"\nCleaned {cleaned} objects")

print(f"\nCache stats: {cache.stats()}")

# Example 5: WeakSet for observer pattern
print("\n5. WEAKSET - OBSERVER PATTERN:")
print("="*70)

class Observable:
    def __init__(self):
        self._observers = weakref.WeakSet()
    
    def add_observer(self, observer):
        self._observers.add(observer)
        print(f"   Added observer: {observer.name}")
    
    def remove_observer(self, observer):
        self._observers.discard(observer)
        print(f"   Removed observer: {observer.name}")
    
    def notify(self, message):
        print(f"\n   Notifying {len(self._observers)} observers:")
        for observer in self._observers:
            observer.update(message)

class Observer:
    def __init__(self, name):
        self.name = name
    
    def update(self, message):
        print(f"      {self.name} received: {message}")

# Test observer pattern
subject = Observable()

obs1 = Observer("Observer1")
obs2 = Observer("Observer2")

subject.add_observer(obs1)
subject.add_observer(obs2)

subject.notify("Hello!")

# Delete observer
print("\nDeleting Observer1:")
del obs1
gc.collect()

subject.notify("Still here?")

# Example 6: Weak reference proxy
print("\n6. WEAK REFERENCE PROXY:")
print("="*70)

class Resource:
    def __init__(self, name):
        self.name = name
        print(f"   Created: {name}")
    
    def __del__(self):
        print(f"   Deleted: {self.name}")
    
    def do_work(self):
        return f"Working: {self.name}"

# Create proxy
obj = Resource("ProxyTarget")
proxy = weakref.proxy(obj)

print(f"Using proxy: {proxy.do_work()}")
print(f"Proxy name: {proxy.name}")

# Delete original
print("\nDeleting original:")
del obj
gc.collect()

try:
    proxy.do_work()
except ReferenceError as e:
    print(f"   ReferenceError: {e}")

# Example 7: Weak key dictionary
print("\n7. WEAKEYKICTIONARY:")
print("="*70)

class User:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"User({self.name})"

# Map users to their data (without preventing deletion)
user_data = weakref.WeakKeyDictionary()

user1 = User("Alice")
user2 = User("Bob")

user_data[user1] = {"score": 100, "level": 5}
user_data[user2] = {"score": 200, "level": 10}

print(f"User data size: {len(user_data)}")
print(f"Alice's data: {user_data[user1]}")

# Delete user
print("\nDeleting Alice:")
del user1
gc.collect()

print(f"User data size: {len(user_data)}")

# Example 8: Cached property with weak refs
print("\n8. CACHED PROPERTY:")
print("="*70)

class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.cache = weakref.WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        if instance not in self.cache:
            print(f"   Computing: {self.func.__name__}")
            value = self.func(instance)
            self.cache[instance] = value
        else:
            print(f"   Using cached: {self.func.__name__}")
        
        return self.cache[instance]

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @CachedProperty
    def expensive_result(self):
        # Simulate expensive computation
        return sum(x**2 for x in self.data)

# Test cached property
proc1 = DataProcessor(range(1000))

print("First access:")
result1 = proc1.expensive_result

print("\nSecond access:")
result2 = proc1.expensive_result

print(f"\nResults equal: {result1 == result2}")

# Example 9: Memory comparison
print("\n9. MEMORY USAGE COMPARISON:")
print("="*70)

import tracemalloc

class CachedObject:
    def __init__(self, id):
        self.id = id
        self.data = [0] * 10000

# Regular cache
tracemalloc.start()

regular = {}
objects = []

for i in range(100):
    obj = CachedObject(i)
    objects.append(obj)
    regular[i] = obj

# Keep objects alive
current, peak = tracemalloc.get_traced_memory()
regular_memory = peak / 1024 / 1024

tracemalloc.stop()
regular.clear()
objects.clear()
gc.collect()

# Weak cache
tracemalloc.start()

weak = weakref.WeakValueDictionary()
objects = []

for i in range(100):
    obj = CachedObject(i)
    objects.append(obj)
    weak[i] = obj

# Objects kept alive by 'objects' list
current, peak = tracemalloc.get_traced_memory()
weak_memory = peak / 1024 / 1024

# Clear references
objects.clear()
gc.collect()

# Cache auto-cleaned
weak_cache_size = len(weak)

tracemalloc.stop()

print(f"Regular cache memory: {regular_memory:.2f} MB")
print(f"Weak cache memory: {weak_memory:.2f} MB")
print(f"Weak cache after cleanup: {weak_cache_size} items")

# Example 10: Best practices
print("\n10. WEAK REFERENCE BEST PRACTICES:")
print("="*70)

print("""
When to Use Weak References:
✓ Caches (avoid memory leaks)
✓ Observer pattern (auto cleanup)
✓ Circular references (break cycles)
✓ Parent-child relationships
✓ Event handlers/callbacks
✓ Temporary object tracking

When NOT to Use:
✗ Need guaranteed object lifetime
✗ Objects with no other strong refs
✗ Performance-critical hot paths
✗ Small, simple caches

Weak Reference Types:
- weakref.ref(): Basic weak reference
- weakref.proxy(): Transparent proxy
- WeakValueDictionary: Cache by key
- WeakKeyDictionary: Data by object
- WeakSet: Set of objects
- WeakMethod: Bound method reference

Common Pitfalls:
⚠ Weak refs to immutable objects (int, str) don't work
⚠ Check if() before accessing weak ref
⚠ Object may be deleted between check and use
⚠ Callbacks must not revive object

Best Practices:
1. Use WeakValueDictionary for caches
2. Always check if weak ref is alive
3. Use callbacks for cleanup
4. Combine with strong refs when needed
5. Document weak ref behavior
""")