"""
CONCEPT: Reference Counting
- Python tracks how many references point to each object
- When reference count reaches 0, memory is freed
- sys.getrefcount() returns the number of references
- del statement removes a reference

Reference Count Changes:
- Assignment: creates new reference
- Function call: temporary reference
- Container: reference from container
- del: removes reference
"""

import sys

print("="*70)
print("Program 2: REFERENCE COUNTING AND OBJECT LIFETIME")
print("="*70)

# Example 1: Basic reference counting
print("\n1. BASIC REFERENCE COUNTING:")
print("="*70)

a = [1, 2, 3]
print(f"Created list: {a}")
print(f"Reference count: {sys.getrefcount(a)}")
# Note: getrefcount() creates temporary reference, so count is +1

b = a
print(f"\nAfter b = a:")
print(f"Reference count: {sys.getrefcount(a)}")

c = a
print(f"\nAfter c = a:")
print(f"Reference count: {sys.getrefcount(a)}")

# Example 2: Deleting references
print("\n2. DELETING REFERENCES:")
print("="*70)

x = [10, 20, 30]
print(f"x = {x}, refs: {sys.getrefcount(x)}")

y = x
z = x
print(f"After y=x, z=x, refs: {sys.getrefcount(x)}")

del y
print(f"After del y, refs: {sys.getrefcount(x)}")

del z
print(f"After del z, refs: {sys.getrefcount(x)}")

# Example 3: References in containers
print("\n3. REFERENCES IN CONTAINERS:")
print("="*70)

obj = "Hello"
print(f"obj = '{obj}', refs: {sys.getrefcount(obj)}")

container = [obj, obj, obj]
print(f"After adding to list 3 times, refs: {sys.getrefcount(obj)}")

container.clear()
print(f"After list.clear(), refs: {sys.getrefcount(obj)}")

# Example 4: Function parameters
print("\n4. FUNCTION PARAMETERS:")
print("="*70)

def check_refs(param):
    print(f"   Inside function, refs: {sys.getrefcount(param)}")

data = [1, 2, 3]
print(f"Before function call, refs: {sys.getrefcount(data)}")
check_refs(data)
print(f"After function call, refs: {sys.getrefcount(data)}")

# Example 5: Object lifetime demonstration
print("\n5. OBJECT LIFETIME:")
print("="*70)

class MyClass:
    def __init__(self, name):
        self.name = name
        print(f"   Object '{self.name}' created")
    
    def __del__(self):
        print(f"   Object '{self.name}' deleted (destructor called)")

print("Creating obj1:")
obj1 = MyClass("Object-1")
print(f"Reference count: {sys.getrefcount(obj1)}")

print("\nCreating reference obj2 = obj1:")
obj2 = obj1
print(f"Reference count: {sys.getrefcount(obj1)}")

print("\nDeleting obj1:")
del obj1
print("(Object still exists because obj2 references it)")

print("\nDeleting obj2:")
del obj2
print("(Now object is destroyed)")

# Example 6: Reassignment
print("\n6. REASSIGNMENT:")
print("="*70)

class Tracker:
    counter = 0
    
    def __init__(self):
        Tracker.counter += 1
        self.id = Tracker.counter
        print(f"   Created: Tracker-{self.id}")
    
    def __del__(self):
        print(f"   Deleted: Tracker-{self.id}")

print("Creating x = Tracker():")
x = Tracker()

print("\nReassigning x = Tracker():")
x = Tracker()  # First object deleted, second created

print("\nDeleting x:")
del x

# Example 7: Circular references
print("\n7. CIRCULAR REFERENCES (MEMORY LEAK POTENTIAL):")
print("="*70)

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        print(f"   Created Node({value})")
    
    def __del__(self):
        print(f"   Deleted Node({self.value})")

print("Creating circular reference:")
node1 = Node(1)
node2 = Node(2)

node1.next = node2
node2.next = node1  # Circular reference!

print(f"\nnode1 refs: {sys.getrefcount(node1)}")
print(f"node2 refs: {sys.getrefcount(node2)}")

print("\nDeleting references:")
del node1
del node2
print("(Objects may not be deleted due to circular reference)")

# Force garbage collection
import gc
print("\nForcing garbage collection:")
gc.collect()

# Example 8: Weak references (avoiding circular references)
print("\n8. WEAK REFERENCES:")
print("="*70)

import weakref

obj = [1, 2, 3]
print(f"Strong reference: refs = {sys.getrefcount(obj)}")

weak_ref = weakref.ref(obj)
print(f"After weak reference: refs = {sys.getrefcount(obj)}")
print(f"Weak reference points to: {weak_ref()}")

del obj
print("\nAfter deleting strong reference:")
print(f"Weak reference now points to: {weak_ref()}")

# Example 9: Container ownership
print("\n9. CONTAINER OWNERSHIP:")
print("="*70)

shared_obj = {"data": "important"}
print(f"Created shared_obj, refs: {sys.getrefcount(shared_obj)}")

container1 = [shared_obj]
container2 = [shared_obj]
container3 = {"key": shared_obj}

print(f"After adding to 3 containers, refs: {sys.getrefcount(shared_obj)}")

del container1
print(f"After deleting container1, refs: {sys.getrefcount(shared_obj)}")

# Example 10: Memory efficiency comparison
print("\n10. MEMORY EFFICIENCY:")
print("="*70)

# Creating many references to same object
base_obj = list(range(1000000))
print(f"Large list created: {sys.getsizeof(base_obj)} bytes")

# Multiple references (no extra memory for object)
refs = [base_obj for _ in range(10)]
print(f"10 references created: {sys.getsizeof(refs)} bytes for list")
print(f"Original object refs: {sys.getrefcount(base_obj)}")

# vs Creating copies (lots of memory)
copies = [list(range(1000000)) for _ in range(10)]
total_size = sum(sys.getsizeof(c) for c in copies)
print(f"\n10 copies created: ~{total_size} bytes total")