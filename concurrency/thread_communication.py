"""
CONCEPT: Threads sharing data (UNSAFE version)
LEARN: Race conditions and why we need locks
"""

import threading
import time

# Shared variable (DANGER!)
counter = 0

def increment_counter(name, times):
    """Increment counter multiple times"""
    global counter
    
    for i in range(times):
        # Read current value
        current = counter
        
        # Simulate some processing
        time.sleep(0.0001)
        
        # Write new value
        counter = current + 1
        
        if i % 10000 == 0:
            print(f"{name}: Counter at {counter}")

if __name__ == "__main__":
    print("=== UNSAFE VERSION (Race Condition) ===\n")
    
    # Expected result: 100,000 (50,000 + 50,000)
    INCREMENTS = 50000
    
    # Create two threads
    thread1 = threading.Thread(target=increment_counter, args=("Thread-1", INCREMENTS))
    thread2 = threading.Thread(target=increment_counter, args=("Thread-2", INCREMENTS))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for completion
    thread1.join()
    thread2.join()
    
    print(f"\n✗ Final counter value: {counter}")
    print(f"✗ Expected: {INCREMENTS * 2}")
    print(f"✗ Lost updates: {(INCREMENTS * 2) - counter}")
    print("\n⚠️  This is a RACE CONDITION!")

"""
OUTPUT:
=== UNSAFE VERSION (Race Condition) ===

Thread-1: Counter at 1
Thread-2: Counter at 2
...

✗ Final counter value: 87,234  (varies each run!)
✗ Expected: 100,000
✗ Lost updates: 12,766

⚠️  This is a RACE CONDITION!

PROBLEM: Both threads read the same value, increment it, and write back
         causing lost updates!
"""