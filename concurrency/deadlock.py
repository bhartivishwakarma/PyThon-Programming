"""
CONCEPT: Deadlock and how to prevent it
LEARN: Circular waiting and lock ordering
"""

import threading
import time

# Shared resources
resource_A = threading.Lock()
resource_B = threading.Lock()

def task1_deadlock():
    """This can cause deadlock"""
    print("Task 1: Trying to acquire Resource A...")
    with resource_A:
        print("Task 1: Acquired Resource A")
        time.sleep(0.1)  # Simulate work
        
        print("Task 1: Trying to acquire Resource B...")
        with resource_B:
            print("Task 1: Acquired Resource B")
            print("Task 1: Done!")

def task2_deadlock():
    """This can cause deadlock"""
    print("Task 2: Trying to acquire Resource B...")
    with resource_B:
        print("Task 2: Acquired Resource B")
        time.sleep(0.1)  # Simulate work
        
        print("Task 2: Trying to acquire Resource A...")
        with resource_A:
            print("Task 2: Acquired Resource A")
            print("Task 2: Done!")

def task1_safe():
    """Fixed version - consistent lock ordering"""
    print("Task 1: Trying to acquire Resource A...")
    with resource_A:
        print("Task 1: Acquired Resource A")
        time.sleep(0.1)
        
        print("Task 1: Trying to acquire Resource B...")
        with resource_B:
            print("Task 1: Acquired Resource B")
            print("Task 1: Done!")

def task2_safe():
    """Fixed version - consistent lock ordering"""
    print("Task 2: Trying to acquire Resource A (same order)...")
    with resource_A:
        print("Task 2: Acquired Resource A")
        time.sleep(0.1)
        
        print("Task 2: Trying to acquire Resource B...")
        with resource_B:
            print("Task 2: Acquired Resource B")
            print("Task 2: Done!")

if __name__ == "__main__":
    print("="*50)
    print("DEADLOCK DEMONSTRATION")
    print("="*50)
    
    print("\n⚠️  SCENARIO 1: DEADLOCK (will hang)")
    print("-" * 50)
    print("Starting two tasks with different lock order...")
    print("(Press Ctrl+C to stop if it hangs)\n")
    
    t1 = threading.Thread(target=task1_deadlock)
    t2 = threading.Thread(target=task2_deadlock)
    
    t1.start()
    t2.start()
    
    # Wait max 3 seconds
    t1.join(timeout=3)
    t2.join(timeout=3)
    
    if t1.is_alive() or t2.is_alive():
        print("\n❌ DEADLOCK DETECTED!")
        print("   Task 1 holds A, wants B")
        print("   Task 2 holds B, wants A")
        print("   Both waiting forever...\n")
    else:
        print("\n✓ Both tasks completed (got lucky!)\n")
    
    # Reset locks
    resource_A = threading.Lock()
    resource_B = threading.Lock()
    
    print("\n\n✅ SCENARIO 2: SAFE (same lock order)")
    print("-" * 50)
    print("Starting two tasks with SAME lock order...\n")
    
    t1 = threading.Thread(target=task1_safe)
    t2 = threading.Thread(target=task2_safe)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n✓ Both tasks completed successfully!")
    
    print("\n\n" + "="*50)
    print("HOW TO PREVENT DEADLOCK")
    print("="*50)
    print("1. Always acquire locks in the SAME ORDER")
    print("2. Use timeout on lock acquisition")
    print("3. Avoid holding multiple locks when possible")
    print("4. Use lock-free data structures when possible")

"""
OUTPUT:
==================================================
DEADLOCK DEMONSTRATION
==================================================

⚠️  SCENARIO 1: DEADLOCK (will hang)
--------------------------------------------------
Starting two tasks with different lock order...
(Press Ctrl+C to stop if it hangs)

Task 1: Trying to acquire Resource A...
Task 1: Acquired Resource A
Task 2: Trying to acquire Resource B...
Task 2: Acquired Resource B
Task 1: Trying to acquire Resource B...
Task 2: Trying to acquire Resource A...

❌ DEADLOCK DETECTED!
   Task 1 holds A, wants B
   Task 2 holds B, wants A
   Both waiting forever...


✅ SCENARIO 2: SAFE (same lock order)
--------------------------------------------------
Starting two tasks with SAME lock order...

Task 1: Trying to acquire Resource A...
Task 1: Acquired Resource A
Task 1: Trying to acquire Resource B...
Task 1: Acquired Resource B
Task 1: Done!
Task 2: Trying to acquire Resource A (same order)...
Task 2: Acquired Resource A
Task 2: Trying to acquire Resource B...
Task 2: Acquired Resource B
Task 2: Done!

✓ Both tasks completed successfully!

==================================================
HOW TO PREVENT DEADLOCK
==================================================
1. Always acquire locks in the SAME ORDER
2. Use timeout on lock acquisition
3. Avoid holding multiple locks when possible
4. Use lock-free data structures when possible
"""