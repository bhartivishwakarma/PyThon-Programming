"""
CONCEPT: Shallow Copy vs Deep Copy

Shallow Copy (copy.copy()):
- Creates new container object
- Fills with references to same child objects
- Changes to nested objects affect both copies
- Faster, uses less memory

Deep Copy (copy.deepcopy()):
- Creates new container object
- Recursively copies all nested objects
- Completely independent copies
- Slower, uses more memory

When to use which:
- Shallow: Flat structures, read-only nested objects
- Deep: Nested mutable structures, complete independence needed
"""

import copy
import sys

print("="*70)
print("Program 4: SHALLOW COPY VS DEEP COPY")
print("="*70)

# Example 1: Shallow copy of simple list
print("\n1. SHALLOW COPY - SIMPLE LIST:")
print("="*70)

original = [1, 2, 3, 4, 5]
shallow = copy.copy(original)

print(f"Original: {original}, id: {id(original)}")
print(f"Shallow:  {shallow}, id: {id(shallow)}")
print(f"Same object? {original is shallow}")

# Modify shallow copy
shallow.append(6)
print(f"\nAfter shallow.append(6):")
print(f"Original: {original}")
print(f"Shallow:  {shallow}")
print("Note: Original unchanged (different objects)")

# Example 2: Shallow copy of nested list
print("\n2. SHALLOW COPY - NESTED LIST:")
print("="*70)

original = [[1, 2], [3, 4], [5, 6]]
shallow = copy.copy(original)

print(f"Original: {original}, id: {id(original)}")
print(f"Shallow:  {shallow}, id: {id(shallow)}")

# Check inner lists
print(f"\nInner list [0]:")
print(f"   original[0] id: {id(original[0])}")
print(f"   shallow[0] id:  {id(shallow[0])}")
print(f"   Same object? {original[0] is shallow[0]}")

# Modify inner list
shallow[0].append(999)
print(f"\nAfter shallow[0].append(999):")
print(f"Original: {original}")
print(f"Shallow:  {shallow}")
print("Note: Both changed! (shared inner lists)")

# Example 3: Deep copy of nested list
print("\n3. DEEP COPY - NESTED LIST:")
print("="*70)

original = [[1, 2], [3, 4], [5, 6]]
deep = copy.deepcopy(original)

print(f"Original: {original}, id: {id(original)}")
print(f"Deep:     {deep}, id: {id(deep)}")

# Check inner lists
print(f"\nInner list [0]:")
print(f"   original[0] id: {id(original[0])}")
print(f"   deep[0] id:     {id(deep[0])}")
print(f"   Same object? {original[0] is deep[0]}")

# Modify inner list
deep[0].append(999)
print(f"\nAfter deep[0].append(999):")
print(f"Original: {original}")
print(f"Deep:     {deep}")
print("Note: Only deep copy changed (independent objects)")

# Example 4: Dictionary shallow copy
print("\n4. DICTIONARY - SHALLOW COPY:")
print("="*70)

original = {
    'name': 'John',
    'scores': [90, 85, 88],
    'address': {'city': 'NYC', 'zip': '10001'}
}

shallow = original.copy()  # or copy.copy(original)

print(f"Original: {original}")
print(f"Shallow:  {shallow}")

# Modify nested list
shallow['scores'].append(95)
print(f"\nAfter modifying scores in shallow copy:")
print(f"Original scores: {original['scores']}")
print(f"Shallow scores:  {shallow['scores']}")
print("Note: Both changed!")

# Example 5: Dictionary deep copy
print("\n5. DICTIONARY - DEEP COPY:")
print("="*70)

original = {
    'name': 'Jane',
    'scores': [92, 88, 90],
    'address': {'city': 'LA', 'zip': '90001'}
}

deep = copy.deepcopy(original)

# Modify nested dict
deep['address']['city'] = 'San Francisco'
deep['scores'].append(95)

print(f"\nAfter modifying deep copy:")
print(f"Original: {original}")
print(f"Deep:     {deep}")
print("Note: Only deep copy changed!")

# Example 6: Custom objects
print("\n6. CUSTOM OBJECTS:")
print("="*70)

class Person:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends
    
    def __repr__(self):
        return f"Person({self.name}, friends={self.friends})"

person1 = Person("Alice", ["Bob", "Charlie"])
shallow_person = copy.copy(person1)
deep_person = copy.deepcopy(person1)

print(f"Original: {person1}")
print(f"Shallow:  {shallow_person}")
print(f"Deep:     {deep_person}")

# Modify friends list
shallow_person.friends.append("David")
deep_person.friends.append("Eve")

print(f"\nAfter modifications:")
print(f"Original: {person1}")
print(f"Shallow:  {shallow_person}")
print(f"Deep:     {deep_person}")

# Example 7: List slicing vs copy
print("\n7. LIST SLICING (SHALLOW COPY):")
print("="*70)

original = [[1, 2], [3, 4]]

# Three ways to shallow copy
copy1 = original[:]  # Slicing
copy2 = list(original)  # Constructor
copy3 = copy.copy(original)  # copy.copy()

print("All create shallow copies:")
print(f"original[0] is copy1[0]: {original[0] is copy1[0]}")
print(f"original[0] is copy2[0]: {original[0] is copy2[0]}")
print(f"original[0] is copy3[0]: {original[0] is copy3[0]}")

# Example 8: Performance comparison
print("\n8. PERFORMANCE COMPARISON:")
print("="*70)

import time

# Create large nested structure
large_data = [[i] * 100 for i in range(1000)]

# Shallow copy timing
start = time.time()
for _ in range(100):
    shallow = copy.copy(large_data)
shallow_time = time.time() - start

# Deep copy timing
start = time.time()
for _ in range(100):
    deep = copy.deepcopy(large_data)
deep_time = time.time() - start

print(f"Shallow copy: {shallow_time:.4f} seconds")
print(f"Deep copy:    {deep_time:.4f} seconds")
print(f"Deep copy is {deep_time/shallow_time:.2f}x slower")

# Example 9: Memory usage
print("\n9. MEMORY USAGE:")
print("="*70)

original = [[1, 2, 3] * 100 for _ in range(100)]

shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(f"Original size: {sys.getsizeof(original)} bytes")
print(f"Shallow size:  {sys.getsizeof(shallow)} bytes")
print(f"Deep size:     {sys.getsizeof(deep)} bytes")

print(f"\nTotal deep copy size (recursive):")
deep_total = sys.getsizeof(deep) + sum(sys.getsizeof(item) for item in deep)
print(f"   ~{deep_total} bytes")

# Example 10: When shallow copy is enough
print("\n10. WHEN TO USE WHICH:")
print("="*70)

# Shallow copy is enough for immutable nested objects
data1 = [(1, 2), (3, 4), (5, 6)]  # Tuples are immutable
shallow1 = copy.copy(data1)
print("Immutable nested objects - Shallow copy OK:")
print(f"   data1[0] is shallow1[0]: {data1[0] is shallow1[0]}")

# Deep copy needed for mutable nested objects
data2 = [[1, 2], [3, 4], [5, 6]]  # Lists are mutable
deep2 = copy.deepcopy(data2)
print("\nMutable nested objects - Deep copy needed:")
print(f"   data2[0] is deep2[0]: {data2[0] is deep2[0]}")

print("\nGuidelines:")
print("   • Shallow copy: Flat structures, immutable nested objects")
print("   • Deep copy: Nested mutable structures, need independence")