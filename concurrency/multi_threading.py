"""
CONCEPT: Running multiple threads simultaneously
LEARN: How threads execute concurrently
"""

import threading
import time

def count_numbers(thread_name, start, end):
    """Count from start to end"""
    print(f"{thread_name} starting to count from {start} to {end}")
    
    for i in range(start, end + 1):
        print(f"{thread_name}: {i}")
        time.sleep(0.5)  # Simulate work
    
    print(f"{thread_name} finished!")

if __name__ == "__main__":
    # Create 3 threads that count different ranges
    threads = []
    
    # Thread 1: counts 1-5
    t1 = threading.Thread(target=count_numbers, args=("Thread-A", 1, 5))
    threads.append(t1)
    
    # Thread 2: counts 10-15
    t2 = threading.Thread(target=count_numbers, args=("Thread-B", 10, 15))
    threads.append(t2)
    
    # Thread 3: counts 100-105
    t3 = threading.Thread(target=count_numbers, args=("Thread-C", 100, 105))
    threads.append(t3)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    print(f"\n✓ All counting complete!")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"(Sequential would take ~15 seconds, concurrent took ~3 seconds)")

"""
OUTPUT (interleaved):
Thread-A starting to count from 1 to 5
Thread-B starting to count from 10 to 15
Thread-C starting to count from 100 to 105
Thread-A: 1
Thread-B: 10
Thread-C: 100
Thread-A: 2
Thread-B: 11
Thread-C: 101
...
"""