"""
CONCEPT: Object Identity and id()
- id() returns unique identifier (memory address) of an object
- Identity: whether two variables reference the same object
- Equality: whether two objects have the same value

is vs ==:
- 'is' compares identity (same object in memory)
- '==' compares values (content equality)

Python Optimizations:
- Small integers (-5 to 256) are cached (same id)
- String interning for some strings
- Singleton objects (None, True, False)
"""

import sys

print("="*70)
print("Program 1: OBJECT IDENTITY WITH id()")
print("="*70)

# Example 1: Basic id() usage
print("\n1. BASIC OBJECT IDENTITY:")
print("="*70)

a = 100
b = 100
c = 200

print(f"a = 100, id(a) = {id(a)}")
print(f"b = 100, id(b) = {id(b)}")
print(f"c = 200, id(c) = {id(c)}")
print(f"\na is b: {a is b} (same object)")
print(f"a == b: {a == b} (same value)")

# Example 2: Integer caching (-5 to 256)
print("\n2. INTEGER CACHING:")
print("="*70)

x = 256
y = 256
print(f"x = 256, y = 256")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"x is y: {x is y} (cached)")

x = 257
y = 257
print(f"\nx = 257, y = 257")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"x is y: {x is y} (not cached)")

# Example 3: String interning
print("\n3. STRING INTERNING:")
print("="*70)

s1 = "hello"
s2 = "hello"
print(f"s1 = 'hello', s2 = 'hello'")
print(f"id(s1) = {id(s1)}")
print(f"id(s2) = {id(s2)}")
print(f"s1 is s2: {s1 is s2} (interned)")

s3 = "hello world"
s4 = "hello world"
print(f"\ns3 = 'hello world', s4 = 'hello world'")
print(f"id(s3) = {id(s3)}")
print(f"id(s4) = {id(s4)}")
print(f"s3 is s4: {s3 is s4} (may or may not be interned)")

# Example 4: Lists (mutable objects)
print("\n4. MUTABLE OBJECTS (LISTS):")
print("="*70)

list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print(f"list1 = {list1}, id = {id(list1)}")
print(f"list2 = {list2}, id = {id(list2)}")
print(f"list3 = list1, id = {id(list3)}")

print(f"\nlist1 is list2: {list1 is list2} (different objects)")
print(f"list1 == list2: {list1 == list2} (same values)")
print(f"list1 is list3: {list1 is list3} (same object)")

# Modify list1
list1.append(4)
print(f"\nAfter list1.append(4):")
print(f"list1 = {list1}")
print(f"list3 = {list3} (also changed!)")
print(f"list2 = {list2} (unchanged)")

# Example 5: None, True, False (singletons)
print("\n5. SINGLETON OBJECTS:")
print("="*70)

a = None
b = None
print(f"a = None, b = None")
print(f"id(a) = {id(a)}")
print(f"id(b) = {id(b)}")
print(f"a is b: {a is b} (singleton)")

x = True
y = True
print(f"\nx = True, y = True")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"x is y: {x is y} (singleton)")

# Example 6: Object size with sys.getsizeof()
print("\n6. OBJECT SIZE IN MEMORY:")
print("="*70)

objects = [
    (42, "integer"),
    (3.14, "float"),
    ("hello", "string"),
    ([1, 2, 3], "list"),
    ((1, 2, 3), "tuple"),
    ({"a": 1}, "dict"),
    ({1, 2, 3}, "set")
]

for obj, name in objects:
    print(f"{name:10s}: {sys.getsizeof(obj)} bytes, id: {id(obj)}")

# Example 7: Assignment vs Copy
print("\n7. ASSIGNMENT VS COPY:")
print("="*70)

original = [1, 2, 3]
assigned = original  # Just assigns reference
copied = original.copy()  # Creates new list

print(f"original: {original}, id: {id(original)}")
print(f"assigned: {assigned}, id: {id(assigned)}")
print(f"copied:   {copied}, id: {id(copied)}")

print(f"\noriginal is assigned: {original is assigned}")
print(f"original is copied: {original is copied}")

# Example 8: Function parameter passing
print("\n8. FUNCTION PARAMETER PASSING:")
print("="*70)

def modify_list(lst):
    print(f"   Inside function, id(lst) = {id(lst)}")
    lst.append(999)

my_list = [1, 2, 3]
print(f"Before: my_list = {my_list}, id = {id(my_list)}")
modify_list(my_list)
print(f"After:  my_list = {my_list}, id = {id(my_list)}")
print("Note: List was modified in place (same object)")

# Example 9: Immutable vs Mutable
print("\n9. IMMUTABLE VS MUTABLE:")
print("="*70)

# Immutable (int)
a = 10
print(f"a = 10, id(a) = {id(a)}")
a = a + 1
print(f"a = 11, id(a) = {id(a)} (new object created)")

# Mutable (list)
lst = [1, 2, 3]
print(f"\nlst = {lst}, id(lst) = {id(lst)}")
lst.append(4)
print(f"lst = {lst}, id(lst) = {id(lst)} (same object)")

# Example 10: Tracking object references
print("\n10. REFERENCE COUNTING:")
print("="*70)

import sys

obj = [1, 2, 3]
print(f"obj = {obj}")
print(f"Reference count: {sys.getrefcount(obj)}")

ref1 = obj
print(f"After ref1 = obj: {sys.getrefcount(obj)}")

ref2 = obj
print(f"After ref2 = obj: {sys.getrefcount(obj)}")

del ref1
print(f"After del ref1: {sys.getrefcount(obj)}")

del ref2
print(f"After del ref2: {sys.getrefcount(obj)}")