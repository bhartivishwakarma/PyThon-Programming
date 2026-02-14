"""
CONCEPT: Circular References
- Circular reference: A → B → A
- Reference counting can't free circular structures
- Garbage collector detects and cleans cycles
- Can cause memory leaks if not handled

Problems:
- Objects kept alive unnecessarily
- Delayed cleanup (wait for GC)
- Memory leaks in long-running apps
- __del__ methods may not run

Solutions:
- Weak references (weakref)
- Manual cycle breaking
- Avoid circular structures
- Use context managers
- Regular gc.collect()
"""

import gc
import sys
import weakref

print("="*70)
print("Program 19: CIRCULAR REFERENCES DETECTION AND BREAKING")
print("="*70)

# Example 1: Simple circular reference
print("\n1. SIMPLE CIRCULAR REFERENCE:")
print("="*70)

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None
        print(f"   Created: {name}")
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

print("Creating circular reference:")
node1 = Node("A")
node2 = Node("B")

node1.ref = node2
node2.ref = node1  # Circular!

print(f"\nReference counts:")
print(f"   node1: {sys.getrefcount(node1)}")
print(f"   node2: {sys.getrefcount(node2)}")

print("\nDeleting references:")
del node1
del node2

print("Objects not deleted yet (circular reference)")

print("\nForcing garbage collection:")
collected = gc.collect()
print(f"Collected {collected} objects")

# Example 2: Detecting circular references
print("\n2. DETECTING CIRCULAR REFERENCES:")
print("="*70)

class TrackedNode:
    instances = []
    
    def __init__(self, name):
        self.name = name
        self.ref = None
        TrackedNode.instances.append(self)
        print(f"   Created: {name}")
    
    def __repr__(self):
        return f"TrackedNode({self.name})"

def find_circular_refs():
    """Find objects with circular references"""
    gc.collect()  # Clean up first
    
    circular = []
    for obj in gc.get_objects():
        if isinstance(obj, TrackedNode):
            # Get what refers to this object
            referrers = gc.get_referrers(obj)
            
            # Check if object's refs create cycle
            for ref in referrers:
                if hasattr(ref, '__dict__') and isinstance(ref, TrackedNode):
                    # Check if ref points back
                    if hasattr(obj, 'ref') and obj.ref is ref:
                        circular.append((obj, ref))
    
    return circular

print("Creating nodes:")
a = TrackedNode("A")
b = TrackedNode("B")
c = TrackedNode("C")

a.ref = b
b.ref = c
c.ref = a  # Creates cycle: A → B → C → A

print("\nSearching for circular references:")
cycles = find_circular_refs()

for obj1, obj2 in cycles:
    print(f"   Cycle: {obj1.name} → {obj2.name}")

# Cleanup
TrackedNode.instances.clear()
del a, b, c
gc.collect()

# Example 3: Parent-child circular reference
print("\n3. PARENT-CHILD CIRCULAR REFERENCE:")
print("="*70)

class Parent:
    def __init__(self, name):
        self.name = name
        self.children = []
        print(f"   Created Parent: {name}")
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self  # Circular!
    
    def __del__(self):
        print(f"   Deleted Parent: {self.name}")

class Child:
    def __init__(self, name):
        self.name = name
        self.parent = None
        print(f"   Created Child: {name}")
    
    def __del__(self):
        print(f"   Deleted Child: {self.name}")

print("Creating parent-child relationship:")
parent = Parent("Dad")
child1 = Child("Kid1")
child2 = Child("Kid2")

parent.add_child(child1)
parent.add_child(child2)

print(f"\nReference counts:")
print(f"   parent: {sys.getrefcount(parent)}")
print(f"   child1: {sys.getrefcount(child1)}")

print("\nDeleting references:")
del parent, child1, child2

print("Waiting for GC...")
gc.collect()

# Example 4: Breaking cycles manually
print("\n4. BREAKING CYCLES MANUALLY:")
print("="*70)

class ManagedNode:
    def __init__(self, name):
        self.name = name
        self.ref = None
        print(f"   Created: {name}")
    
    def break_cycle(self):
        """Manually break circular reference"""
        if self.ref:
            print(f"   Breaking {self.name} → {self.ref.name}")
            self.ref = None
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

print("Creating cycle:")
m1 = ManagedNode("M1")
m2 = ManagedNode("M2")
m1.ref = m2
m2.ref = m1

print("\nBreaking cycle:")
m1.break_cycle()
m2.break_cycle()

print("\nDeleting references:")
del m1, m2
print("Objects deleted immediately!")

# Example 5: Using weak references
print("\n5. USING WEAK REFERENCES:")
print("="*70)

class WeakNode:
    def __init__(self, name):
        self.name = name
        self._ref = None  # Will store weak reference
        print(f"   Created: {name}")
    
    @property
    def ref(self):
        """Get referenced node (might be None)"""
        if self._ref is None:
            return None
        return self._ref()  # Dereference weak ref
    
    @ref.setter
    def ref(self, node):
        """Set weak reference to node"""
        if node is None:
            self._ref = None
        else:
            self._ref = weakref.ref(node)
            print(f"   Weak ref: {self.name} → {node.name}")
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

print("Creating with weak references:")
w1 = WeakNode("W1")
w2 = WeakNode("W2")

w1.ref = w2  # Weak reference (doesn't prevent deletion)
# Don't create reverse reference

print(f"\nw1.ref points to: {w1.ref.name if w1.ref else 'None'}")

print("\nDeleting w2:")
del w2
gc.collect()

print(f"w1.ref points to: {w1.ref.name if w1.ref else 'None'}")

del w1

# Example 6: Double-linked list with weak refs
print("\n6. DOUBLE-LINKED LIST (WEAK REFS):")
print("="*70)

class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self._prev = None  # Weak reference
        print(f"   Created node: {value}")
    
    @property
    def prev(self):
        if self._prev is None:
            return None
        return self._prev()
    
    @prev.setter
    def prev(self, node):
        if node is None:
            self._prev = None
        else:
            self._prev = weakref.ref(node)
    
    def __del__(self):
        print(f"   Deleted node: {self.value}")

print("Creating double-linked list:")
node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)

# Link forward (strong)
node1.next = node2
node2.next = node3

# Link backward (weak)
node2.prev = node1
node3.prev = node2

print("\nTraversing forward:")
current = node1
while current:
    print(f"   Value: {current.value}")
    current = current.next

print("\nDeleting nodes:")
del node1, node2, node3
gc.collect()

# Example 7: Cache with weak values
print("\n7. CACHE WITH WEAK VALUES:")
print("="*70)

class CachedObject:
    def __init__(self, id):
        self.id = id
        print(f"   Created: {id}")
    
    def __del__(self):
        print(f"   Deleted: {id}")

# Bad cache (strong references)
print("Bad cache (strong references):")
bad_cache = {}

obj1 = CachedObject("obj1")
bad_cache["key1"] = obj1

del obj1  # Object NOT deleted (cache holds it)
print("Object still in cache")

bad_cache.clear()
gc.collect()

# Good cache (weak references)
print("\nGood cache (weak references):")
good_cache = weakref.WeakValueDictionary()

obj2 = CachedObject("obj2")
good_cache["key2"] = obj2

print(f"Cache size: {len(good_cache)}")

del obj2  # Object IS deleted
gc.collect()

print(f"Cache size after delete: {len(good_cache)}")

# Example 8: Closure circular reference
print("\n8. CLOSURE CIRCULAR REFERENCE:")
print("="*70)

class EventHandler:
    def __init__(self, name):
        self.name = name
        self.handlers = []
        print(f"   Created: {name}")
    
    def add_handler(self, func):
        self.handlers.append(func)
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

# Circular reference through closure
def create_circular_closure():
    handler = EventHandler("Handler1")
    
    def callback():
        # Closure captures 'handler'
        print(f"Callback for {handler.name}")
    
    handler.add_handler(callback)  # handler → callback → handler
    return handler

print("Creating circular closure:")
h = create_circular_closure()

print("\nDeleting handler:")
del h
print("Waiting for GC...")
gc.collect()

# Example 9: Detecting memory leaks from cycles
print("\n9. DETECTING MEMORY LEAKS:")
print("="*70)

class LeakyClass:
    count = 0
    
    def __init__(self):
        LeakyClass.count += 1
        self.id = LeakyClass.count
        self.ref = None
    
    def __repr__(self):
        return f"LeakyClass({self.id})"

def create_leak():
    """Create circular references"""
    objects = []
    for i in range(10):
        obj = LeakyClass()
        if objects:
            obj.ref = objects[-1]
            objects[-1].ref = obj
        objects.append(obj)
    return objects

print("Creating potential leak:")
initial_count = len(gc.get_objects())

leak = create_leak()

after_create = len(gc.get_objects())
print(f"   Objects before: {initial_count}")
print(f"   Objects after: {after_create}")
print(f"   New objects: {after_create - initial_count}")

print("\nDeleting references:")
del leak
gc.collect()

after_delete = len(gc.get_objects())
print(f"   Objects after delete: {after_delete}")
print(f"   Leaked: {after_delete - initial_count}")

# Example 10: Context manager for cycle breaking
print("\n10. CONTEXT MANAGER FOR CLEANUP:")
print("="*70)

from contextlib import contextmanager

class Resource:
    def __init__(self, name):
        self.name = name
        self.refs = []
        print(f"   Created: {name}")
    
    def add_ref(self, other):
        self.refs.append(other)
    
    def cleanup(self):
        print(f"   Cleaning up {self.name}")
        self.refs.clear()
    
    def __del__(self):
        print(f"   Deleted: {self.name}")

@contextmanager
def managed_resources(*resources):
    """Context manager that ensures cleanup"""
    try:
        yield resources
    finally:
        for resource in resources:
            resource.cleanup()

print("Using context manager:")
with managed_resources(
    Resource("R1"),
    Resource("R2"),
    Resource("R3")
) as (r1, r2, r3):
    # Create cycles
    r1.add_ref(r2)
    r2.add_ref(r3)
    r3.add_ref(r1)
    
    print("   Resources in use")

print("Context exited, cleanup automatic")

# Example 11: Summary and best practices
print("\n11. CIRCULAR REFERENCE SUMMARY:")
print("="*70)

print("""
Common Circular Reference Patterns:
1. Parent ↔ Child
2. Double-linked lists
3. Graph nodes
4. Observer pattern
5. Callbacks/closures
6. Cache with back-references

Detection Methods:
✓ gc.get_referrers(obj)
✓ gc.get_objects() scan
✓ Memory profiling over time
✓ Reference count analysis
✓ objgraph visualization

Breaking Cycles:
Method 1: Weak References
  - Use weakref.ref()
  - Use WeakValueDictionary
  - Use WeakKeyDictionary
  - Automatic cleanup

Method 2: Manual Breaking
  - Add cleanup() methods
  - Use context managers
  - Clear references in __del__
  - Call gc.collect() periodically

Method 3: Design Around It
  - Avoid bidirectional refs
  - Use IDs instead of refs
  - One-way relationships
  - Immutable structures

Prevention Strategies:
1. Use weak refs for back-pointers
2. Implement cleanup methods
3. Use context managers
4. Avoid capturing 'self' in closures
5. Document circular refs
6. Test with gc disabled
7. Profile memory over time

Best Practices:
✓ Prefer weak refs for back-pointers
✓ Document circular structures
✓ Implement explicit cleanup
✓ Use context managers
✓ Test memory cleanup
✓ Monitor long-running apps
✓ Use gc.set_debug() in development

Warning Signs:
⚠ Memory grows over time
⚠ Objects not deleted
⚠ __del__ not called
⚠ Increasing gc.get_count()
⚠ High gc collection times

Code Patterns:
# Good: Weak back-reference
class Child:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)

# Good: Manual cleanup
class Node:
    def cleanup(self):
        self.refs.clear()

# Good: Context manager
with managed_resources() as res:
    # Use resources
    pass  # Auto cleanup
""")