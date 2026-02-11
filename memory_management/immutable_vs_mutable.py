"""
CONCEPT: Immutable vs Mutable Objects

Immutable Objects:
- Cannot be changed after creation
- Operations create new objects
- Examples: int, float, str, tuple, frozenset
- Safe for dictionary keys and set elements
- Thread-safe by nature

Mutable Objects:
- Can be modified after creation
- Operations modify in-place
- Examples: list, dict, set, bytearray
- Cannot be dictionary keys
- Need synchronization in threads

Memory Implications:
- Immutable: More objects created, but can be shared safely
- Mutable: Fewer objects, but need careful copying
"""

import sys

print("="*70)
print("Program 6: IMMUTABLE VS MUTABLE OBJECTS")
print("="*70)

# Example 1: Integer (immutable)
print("\n1. INTEGERS (IMMUTABLE):")
print("="*70)

x = 100
print(f"x = 100, id = {id(x)}")

x = x + 1
print(f"x = 101, id = {id(x)} (new object created)")

y = 100
print(f"y = 100, id = {id(y)}")
print(f"x and y point to same 100? {id(100) == id(y)}")

# Example 2: String (immutable)
print("\n2. STRINGS (IMMUTABLE):")
print("="*70)

s = "hello"
print(f"s = 'hello', id = {id(s)}")

s = s + " world"
print(f"s = 'hello world', id = {id(s)} (new object)")

original = "Python"
modified = original.upper()
print(f"\noriginal = 'Python', id = {id(original)}")
print(f"modified = 'PYTHON', id = {id(modified)}")
print(f"original unchanged: {original}")

# Example 3: Tuple (immutable)
print("\n3. TUPLES (IMMUTABLE):")
print("="*70)

t = (1, 2, 3)
print(f"t = {t}, id = {id(t)}")

# Can't modify tuple
# t[0] = 999  # This would raise TypeError

# Concatenation creates new tuple
t = t + (4, 5)
print(f"t = {t}, id = {id(t)} (new tuple)")

# Tuple with mutable element
t2 = ([1, 2], 3)
print(f"\nt2 = {t2}, id = {id(t2)}")
print(f"t2[0] id = {id(t2[0])}")

t2[0].append(999)  # Can modify the list inside
print(f"After t2[0].append(999): {t2}")
print(f"t2 id unchanged: {id(t2)}")
print(f"t2[0] id unchanged: {id(t2[0])}")

# Example 4: List (mutable)
print("\n4. LISTS (MUTABLE):")
print("="*70)

lst = [1, 2, 3]
print(f"lst = {lst}, id = {id(lst)}")

lst.append(4)
print(f"After append: {lst}, id = {id(lst)} (same object)")

lst[0] = 999
print(f"After lst[0] = 999: {lst}, id = {id(lst)} (same object)")

# Example 5: Dictionary (mutable)
print("\n5. DICTIONARIES (MUTABLE):")
print("="*70)

d = {'a': 1, 'b': 2}
print(f"d = {d}, id = {id(d)}")

d['c'] = 3
print(f"After adding key: {d}, id = {id(d)} (same object)")

d['a'] = 999
print(f"After modifying value: {d}, id = {id(d)} (same object)")

# Example 6: Function parameters
print("\n6. FUNCTION PARAMETERS:")
print("="*70)

def modify_immutable(x):
    print(f"   Before: x = {x}, id = {id(x)}")
    x = x + 10
    print(f"   After:  x = {x}, id = {id(x)} (new object)")
    return x

def modify_mutable(lst):
    print(f"   Before: lst = {lst}, id = {id(lst)}")
    lst.append(999)
    print(f"   After:  lst = {lst}, id = {id(lst)} (same object)")

num = 5
print(f"Calling modify_immutable({num}):")
result = modify_immutable(num)
print(f"Outside: num = {num} (unchanged)")

my_list = [1, 2, 3]
print(f"\nCalling modify_mutable({my_list}):")
modify_mutable(my_list)
print(f"Outside: my_list = {my_list} (changed!)")

# Example 7: Using immutable as dict keys
print("\n7. DICTIONARY KEYS:")
print("="*70)

# Valid keys (immutable)
valid_dict = {
    42: "integer key",
    "hello": "string key",
    (1, 2): "tuple key",
}
print("Valid keys (immutable):")
for key in valid_dict.keys():
    print(f"   {key} ({type(key).__name__})")

# Invalid keys (mutable)
try:
    invalid_dict = {
        [1, 2]: "list key"  # TypeError!
    }
except TypeError as e:
    print(f"\nCannot use list as key: {e}")

# Example 8: Memory efficiency
print("\n8. MEMORY EFFICIENCY:")
print("="*70)

# String concatenation (creates many objects)
s = ""
for i in range(5):
    s = s + str(i)
    print(f"   Iteration {i}: id = {id(s)}")

print(f"Final string: '{s}'")

# Better: use list (mutable) then join
parts = []
for i in range(5):
    parts.append(str(i))
result = "".join(parts)
print(f"\nUsing list: '{result}' (more efficient)")

# Example 9: Frozenset (immutable set)
print("\n9. FROZENSET (IMMUTABLE SET):")
print("="*70)

fs = frozenset([1, 2, 3])
print(f"frozenset: {fs}, id = {id(fs)}")

# Can use as dict key
dict_with_frozenset = {fs: "frozen set key"}
print(f"Can be dict key: {dict_with_frozenset}")

# Regular set (mutable) cannot
try:
    s = {1, 2, 3}
    bad_dict = {s: "set key"}
except TypeError as e:
    print(f"\nRegular set cannot be key: {e}")

# Example 10: Custom immutable class
print("\n10. CUSTOM IMMUTABLE CLASS:")
print("="*70)

class ImmutablePoint:
    __slots__ = ('_x', '_y')  # Prevent __dict__ creation
    
    def __init__(self, x, y):
        object.__setattr__(self, '_x', x)
        object.__setattr__(self, '_y', y)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __setattr__(self, name, value):
        raise AttributeError("ImmutablePoint is immutable")
    
    def __repr__(self):
        return f"ImmutablePoint({self._x}, {self._y})"

p = ImmutablePoint(10, 20)
print(f"Point: {p}, id = {id(p)}")

try:
    p.x = 30
except AttributeError as e:
    print(f"Cannot modify: {e}")

# Can use as dict key
points_dict = {p: "origin"}
print(f"\nCan use as dict key: {points_dict}")