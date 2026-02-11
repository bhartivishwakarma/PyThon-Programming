"""
CONCEPT: Garbage Collection
- Automatic memory management for unreachable objects
- Handles circular references (reference counting can't)
- Generational garbage collection (3 generations)
- gc module provides control over garbage collector

Generations:
- Gen 0: Newest objects, collected most frequently
- Gen 1: Objects that survived 1 collection
- Gen 2: Oldest objects, collected least frequently

When to use gc.collect():
- After creating many temporary objects
- Before memory-intensive operations
- Debugging memory issues
"""

import gc
import sys

print("="*70)
print("Program 3: GARBAGE COLLECTION BASICS")
print("="*70)

# Example 1: Check if garbage collection is enabled
print("\n1. GARBAGE COLLECTOR STATUS:")
print("="*70)

print(f"GC enabled: {gc.isenabled()}")
print(f"GC thresholds: {gc.get_threshold()}")
print(f"GC counts (gen0, gen1, gen2): {gc.get_count()}")

# Example 2: Circular reference without GC
print("\n2. CIRCULAR REFERENCE EXAMPLE:")
print("="*70)

class CircularNode:
    instances = []
    
    def __init__(self, name):
        self.name = name
        self.ref = None
        CircularNode.instances.append(self)
        print(f"   Created: {name}")
    
    def __del__(self):
        print(f"   Destroyed: {self.name}")

print("Creating circular references:")
node_a = CircularNode("Node-A")
node_b = CircularNode("Node-B")

node_a.ref = node_b
node_b.ref = node_a

print(f"\nnode_a refs: {sys.getrefcount(node_a)}")
print(f"node_b refs: {sys.getrefcount(node_b)}")

print("\nDeleting references:")
del node_a
del node_b

print("\nObjects still in memory (circular reference)")
print(f"Instances in class list: {len(CircularNode.instances)}")

# Example 3: Force garbage collection
print("\n3. FORCING GARBAGE COLLECTION:")
print("="*70)

print(f"Before gc.collect():")
print(f"   Objects in gen0: {gc.get_count()[0]}")

collected = gc.collect()
print(f"\nAfter gc.collect():")
print(f"   Objects collected: {collected}")
print(f"   Objects in gen0: {gc.get_count()[0]}")

CircularNode.instances.clear()

# Example 4: Monitor garbage collection
print("\n4. MONITORING COLLECTIONS:")
print("="*70)

# Get current collection stats
stats = gc.get_stats()
print(f"Number of generations: {len(stats)}")

for i, stat in enumerate(stats):
    print(f"\nGeneration {i}:")
    print(f"   Collections: {stat['collections']}")
    print(f"   Collected: {stat['collected']}")
    print(f"   Uncollectable: {stat['uncollectable']}")

# Example 5: Garbage collection callback
print("\n5. GC CALLBACKS:")
print("="*70)

def gc_callback(phase, info):
    print(f"   GC {phase}: {info}")

# Set callback
gc.callbacks.append(gc_callback)

print("Creating garbage:")
for _ in range(100):
    x = [1, 2, 3]
    y = [4, 5, 6]
    x.append(y)
    y.append(x)

print("\nForcing collection:")
gc.collect()

gc.callbacks.clear()

# Example 6: Disable/Enable garbage collection
print("\n6. DISABLE/ENABLE GC:")
print("="*70)

print(f"GC enabled: {gc.isenabled()}")

print("\nDisabling GC:")
gc.disable()
print(f"GC enabled: {gc.isenabled()}")

print("\nCreating circular references (GC disabled):")
for i in range(5):
    a = []
    b = []
    a.append(b)
    b.append(a)

print(f"Objects in gen0: {gc.get_count()[0]}")

print("\nRe-enabling GC:")
gc.enable()
print(f"GC enabled: {gc.isenabled()}")

print("\nForcing collection:")
collected = gc.collect()
print(f"Collected: {collected} objects")

# Example 7: Finding unreachable objects
print("\n7. FINDING UNREACHABLE OBJECTS:")
print("="*70)

class Trackable:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Trackable({self.name})"

# Create garbage
print("Creating unreachable objects:")
for i in range(5):
    obj1 = Trackable(f"obj{i}_a")
    obj2 = Trackable(f"obj{i}_b")
    obj1.ref = obj2
    obj2.ref = obj1

# Find garbage
print("\nBefore collection:")
print(f"   Garbage objects: {len(gc.garbage)}")

gc.collect()

print(f"\nAfter collection:")
print(f"   Garbage objects: {len(gc.garbage)}")

# Example 8: Memory before/after collection
print("\n8. MEMORY IMPACT:")
print("="*70)

import tracemalloc

tracemalloc.start()

# Create lots of garbage
print("Creating 10,000 circular references...")
for _ in range(10000):
    a = [1, 2, 3]
    b = [4, 5, 6]
    a.append(b)
    b.append(a)

current, peak = tracemalloc.get_traced_memory()
print(f"Before GC: {current / 1024 / 1024:.2f} MB")

gc.collect()

current, peak = tracemalloc.get_traced_memory()
print(f"After GC:  {current / 1024 / 1024:.2f} MB")

tracemalloc.stop()

# Example 9: Generation thresholds
print("\n9. GENERATION THRESHOLDS:")
print("="*70)

threshold = gc.get_threshold()
print(f"Default thresholds: {threshold}")
print(f"   Gen0 threshold: {threshold[0]} objects")
print(f"   Gen1 threshold: {threshold[1]} collections")
print(f"   Gen2 threshold: {threshold[2]} collections")

print("\nSetting custom thresholds:")
gc.set_threshold(700, 10, 10)
print(f"New thresholds: {gc.get_threshold()}")

# Reset to default
gc.set_threshold(700, 10, 10)

# Example 10: Debug garbage collection
print("\n10. DEBUG MODE:")
print("="*70)

# Save original flags
original_flags = gc.get_debug()

print("Setting debug flags:")
gc.set_debug(gc.DEBUG_STATS)

print("\nCreating garbage with debug enabled:")
for _ in range(10):
    a = []
    b = []
    a.append(b)
    b.append(a)

gc.collect()

# Restore original flags
gc.set_debug(original_flags)

print("\nDebug mode disabled")