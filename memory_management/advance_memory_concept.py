"""
CONCEPT: Advanced Memory Concepts

Copy-on-Write (COW):
- Share memory until modification needed
- Common in forked processes
- Saves memory for read-only data

String Interning:
- Reuse identical string objects
- Automatic for identifiers
- Manual with sys.intern()

Integer Caching:
- Small integers (-5 to 256) are cached
- Single object per value
- Fast comparison and memory efficient

Object Identity:
- 'is' checks identity (same object)
- '==' checks equality (same value)
- id() returns memory address
"""

import sys

print("="*70)
print("Program 10: ADVANCED MEMORY CONCEPTS")
print("="*70)

# Example 1: Integer caching detailed
print("\n1. INTEGER CACHING (-5 to 256):")
print("="*70)

# Cached integers
print("Cached integers (-5 to 256):")
for val in [-5, 0, 100, 256]:
    a = val
    b = val
    print(f"   {val}: id(a)={id(a)}, id(b)={id(b)}, same? {a is b}")

# Non-cached integers
print("\nNon-cached integers (>256):")
for val in [257, 1000, 10000]:
    a = val
    b = val
    print(f"   {val}: id(a)={id(a)}, id(b)={id(b)}, same? {a is b}")

# Why caching matters
print("\nMemory savings from caching:")
cached_list = [100] * 10000
non_cached_list = [257] * 10000

# Check if all references are same object
all_same_cached = all(id(x) == id(cached_list[0]) for x in cached_list)
all_same_non = all(id(x) == id(non_cached_list[0]) for x in non_cached_list)

print(f"   [100] * 10000: All same object? {all_same_cached}")
print(f"   [257] * 10000: All same object? {all_same_non}")

# Example 2: String interning details
print("\n2. STRING INTERNING:")
print("="*70)

# Automatic interning (identifiers)
s1 = "hello"
s2 = "hello"
print(f"Identifier strings:")
print(f"   'hello': {id(s1) == id(s2)} (interned)")

# Strings with spaces/special chars may not intern
s3 = "hello world"
s4 = "hello world"
print(f"\n   'hello world': {id(s3) == id(s4)} (may not intern)")

# Computed strings usually don't intern
s5 = "hel" + "lo"
s6 = "hel" + "lo"
print(f"   'hel' + 'lo': {id(s5) == id(s6)} (computed)")

# Manual interning
s7 = sys.intern("hello world!")
s8 = sys.intern("hello world!")
print(f"\nManual interning:")
print(f"   sys.intern('hello world!'): {id(s7) == id(s8)} (interned)")

# Example 3: String interning memory savings
print("\n3. STRING INTERNING MEMORY SAVINGS:")
print("="*70)

# Without interning
words_without = []
for _ in range(10000):
    words_without.append("Python")

# With interning
word_interned = sys.intern("Python")
words_with = []
for _ in range(10000):
    words_with.append(sys.intern("Python"))

print(f"10,000 copies of 'Python':")
print(f"   Without interning: {len(set(id(w) for w in words_without))} unique objects")
print(f"   With interning: {len(set(id(w) for w in words_with))} unique objects")

# Memory usage
size_without = sum(sys.getsizeof(w) for w in words_without[:100])
size_with = sum(sys.getsizeof(w) for w in words_with[:100])

print(f"\nMemory for 100 strings:")
print(f"   Without interning: {size_without} bytes")
print(f"   With interning: {size_with} bytes")

# Example 4: Copy-on-write demonstration
print("\n4. COPY-ON-WRITE CONCEPT:")
print("="*70)

# Lists don't use COW in CPython, but concept demonstration
original = [1, 2, 3, 4, 5]
reference = original  # Just a reference

print(f"Original: id={id(original)}")
print(f"Reference: id={id(reference)}")
print(f"Same object: {original is reference}")

# Shallow copy creates new object
import copy
shallow = copy.copy(original)
print(f"\nShallow copy: id={id(shallow)}")
print(f"Different object: {original is not shallow}")

# Modifying reference affects original
reference.append(6)
print(f"\nAfter reference.append(6):")
print(f"   Original: {original}")
print(f"   Reference: {reference}")

# Example 5: Tuple interning
print("\n5. TUPLE INTERNING:")
print("="*70)

# Small tuples of small integers may be interned
t1 = (1, 2, 3)
t2 = (1, 2, 3)
print(f"Small tuple (1,2,3): {id(t1) == id(t2)} (may intern)")

# Larger tuples usually not interned
t3 = tuple(range(100))
t4 = tuple(range(100))
print(f"Large tuple (0-99): {id(t3) == id(t4)} (usually not interned)")

# Example 6: None, True, False singletons
print("\n6. SINGLETON OBJECTS:")
print("="*70)

# None is always the same object
a = None
b = None
print(f"None: id(a)={id(a)}, id(b)={id(b)}, same? {a is b}")

# True and False are singletons
t1 = True
t2 = True
print(f"True: id(t1)={id(t1)}, id(t2)={id(t2)}, same? {t1 is t2}")

f1 = False
f2 = False
print(f"False: id(f1)={id(f1)}, id(f2)={id(f2)}, same? {f1 is f2}")

# Example 7: Memory layout of objects
print("\n7. MEMORY LAYOUT:")
print("="*70)

class SimpleClass:
    def __init__(self, value):
        self.value = value

obj1 = SimpleClass(100)
obj2 = SimpleClass(100)

print(f"Two instances of SimpleClass:")
print(f"   obj1: id={id(obj1)}, value id={id(obj1.value)}")
print(f"   obj2: id={id(obj2)}, value id={id(obj2.value)}")
print(f"   Same instance: {obj1 is obj2}")
print(f"   Same value object: {id(obj1.value) == id(obj2.value)} (cached int)")

# Example 8: List reuse
print("\n8. LIST MEMORY REUSE:")
print("="*70)

# Creating new list
list1 = [1, 2, 3]
id1 = id(list1)
print(f"list1: {list1}, id={id1}")

# Deleting and creating new
del list1
list2 = [4, 5, 6]
id2 = id(list2)
print(f"list2: {list2}, id={id2}")
print(f"Reused memory: {id1 == id2}")

# Example 9: String concatenation inefficiency
print("\n9. STRING CONCATENATION:")
print("="*70)

import time

# Inefficient: creates many intermediate strings
start = time.time()
s = ""
for i in range(1000):
    s = s + "a"  # Creates new string each time
time_concat = time.time() - start

# Efficient: uses list then join
start = time.time()
parts = []
for i in range(1000):
    parts.append("a")
s = "".join(parts)
time_join = time.time() - start

print(f"String concatenation:")
print(f"   + operator: {time_concat:.6f} seconds")
print(f"   join(): {time_join:.6f} seconds")
print(f"   join is {time_concat/time_join:.2f}x faster")

# Example 10: Practical optimization guide
print("\n10. MEMORY OPTIMIZATION GUIDE:")
print("="*70)

print("""
Interning Strategy:
✓ Automatic for identifiers/literals
✓ Manually intern frequently used strings
✓ Don't intern large strings
✓ Don't intern temporary strings

Integer Caching:
✓ Automatic for -5 to 256
✓ Use when possible (counters, indices)
✓ Don't rely on caching for >256

Object Reuse:
✓ Use object pools for expensive objects
✓ Reuse lists by clearing instead of creating new
✓ Cache computed values
✓ Use weak references when appropriate

String Building:
✓ Use join() for concatenating many strings
✓ Use f-strings for formatting
✓ Avoid repeated concatenation in loops

General Rules:
1. Profile before optimizing
2. Know when objects are shared
3. Use 'is' for identity, '==' for equality
4. Understand immutability implications
5. Consider memory vs speed tradeoffs
""")

# Example 11: Bonus - Empty container singletons
print("\n11. EMPTY CONTAINER CACHING:")
print("="*70)

# Empty tuples are cached
t1 = ()
t2 = ()
print(f"Empty tuple: {t1 is t2}")

# Empty frozensets are cached
fs1 = frozenset()
fs2 = frozenset()
print(f"Empty frozenset: {fs1 is fs2}")

# Empty lists are NOT cached (mutable)
l1 = []
l2 = []
print(f"Empty list: {l1 is l2}")

# Empty dicts are NOT cached (mutable)
d1 = {}
d2 = {}
print(f"Empty dict: {d1 is d2}")

print("""
Pattern:
✓ Immutable empty containers: cached
✗ Mutable empty containers: not cached
""")