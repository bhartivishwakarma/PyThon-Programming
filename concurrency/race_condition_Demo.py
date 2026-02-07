"""
CONCEPT: Demonstrating race conditions
LEARN: What can go wrong without synchronization
"""

import threading
import time

class Counter:
    def __init__(self):
        self.value = 0
    
    def increment_unsafe(self):
        """Unsafe increment (race condition)"""
        # Read
        temp = self.value
        # Simulate some work
        time.sleep(0.00001)
        # Write
        self.value = temp + 1
    
    def increment_safe(self):
        """Safe increment with lock"""
        with self.lock:
            temp = self.value
            time.sleep(0.00001)
            self.value = temp + 1

def test_unsafe():
    """Test without lock - shows race condition"""
    counter = Counter()
    threads = []
    
    for i in range(100):
        t = threading.Thread(target=counter.increment_unsafe)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return counter.value

def test_safe():
    """Test with lock - correct result"""
    counter = Counter()
    counter.lock = threading.Lock()
    threads = []
    
    for i in range(100):
        t = threading.Thread(target=counter.increment_safe)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return counter.value

if __name__ == "__main__":
    print("=== RACE CONDITION DEMONSTRATION ===\n")
    
    print("❌ Test 1: WITHOUT Lock (Unsafe)")
    print("-" * 40)
    results_unsafe = []
    for run in range(5):
        result = test_unsafe()
        results_unsafe.append(result)
        print(f"   Run {run+1}: Expected 100, Got {result} {'✗' if result != 100 else '✓'}")
    
    print(f"\n   Inconsistent results: {len(set(results_unsafe))} different values")
    print(f"   This is a RACE CONDITION!")
    
    print("\n\n✅ Test 2: WITH Lock (Safe)")
    print("-" * 40)
    results_safe = []
    for run in range(5):
        result = test_safe()
        results_safe.append(result)
        print(f"   Run {run+1}: Expected 100, Got {result} ✓")
    
    print(f"\n   Consistent results: {len(set(results_safe))} value(s)")
    print(f"   Problem solved with locks!")

"""
OUTPUT:
=== RACE CONDITION DEMONSTRATION ===

❌ Test 1: WITHOUT Lock (Unsafe)
----------------------------------------
   Run 1: Expected 100, Got 89 ✗
   Run 2: Expected 100, Got 93 ✗
   Run 3: Expected 100, Got 87 ✗
   Run 4: Expected 100, Got 91 ✗
   Run 5: Expected 100, Got 88 ✗

   Inconsistent results: 5 different values
   This is a RACE CONDITION!


✅ Test 2: WITH Lock (Safe)
----------------------------------------
   Run 1: Expected 100, Got 100 ✓
   Run 2: Expected 100, Got 100 ✓
   Run 3: Expected 100, Got 100 ✓
   Run 4: Expected 100, Got 100 ✓
   Run 5: Expected 100, Got 100 ✓

   Consistent results: 1 value(s)
   Problem solved with locks!

LESSON LEARNED:
✗ Race conditions cause unpredictable results
✓ Always use locks for shared mutable data
"""