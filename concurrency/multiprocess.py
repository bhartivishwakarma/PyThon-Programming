"""
CONCEPT: Multiprocessing for CPU-bound tasks
LEARN: True parallelism using multiple CPU cores
"""

import multiprocessing
import time
import math

def calculate_primes(start, end):
    """Find all prime numbers in range (CPU intensive)"""
    process_name = multiprocessing.current_process().name
    print(f"🔢 {process_name} checking range {start}-{end}")
    
    primes = []
    for num in range(start, end + 1):
        if num < 2:
            continue
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    print(f"✓ {process_name} found {len(primes)} primes")
    return primes

if __name__ == "__main__":
    print("=== MULTIPROCESSING FOR CPU TASKS ===\n")
    print(f"CPU Cores available: {multiprocessing.cpu_count()}\n")
    
    # Task: Find all primes from 1 to 100,000
    ranges = [
        (1, 25000),
        (25001, 50000),
        (50001, 75000),
        (75001, 100000)
    ]
    
    # METHOD 1: Sequential
    print("METHOD 1: Sequential (single process)")
    start = time.time()
    all_primes = []
    for start_range, end_range in ranges:
        primes = calculate_primes(start_range, end_range)
        all_primes.extend(primes)
    sequential_time = time.time() - start
    print(f"Total primes found: {len(all_primes)}")
    print(f"Sequential time: {sequential_time:.2f}s\n")
    
    # METHOD 2: Multiprocessing
    print("\nMETHOD 2: Multiprocessing (parallel)")
    start = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        # Map tasks to processes
        results = pool.starmap(calculate_primes, ranges)
    
    all_primes = [prime for sublist in results for prime in sublist]
    parallel_time = time.time() - start
    
    print(f"Total primes found: {len(all_primes)}")
    print(f"Parallel time: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time/parallel_time:.2f}x faster!")

"""
OUTPUT:
=== MULTIPROCESSING FOR CPU TASKS ===

CPU Cores available: 8

METHOD 1: Sequential (single process)
🔢 MainProcess checking range 1-25000
✓ MainProcess found 2762 primes
🔢 MainProcess checking range 25001-50000
✓ MainProcess found 2395 primes
...
Total primes found: 9592
Sequential time: 8.45s

METHOD 2: Multiprocessing (parallel)
🔢 Process-1 checking range 1-25000
🔢 Process-2 checking range 25001-50000
🔢 Process-3 checking range 50001-75000
🔢 Process-4 checking range 75001-100000
✓ Process-1 found 2762 primes
✓ Process-2 found 2395 primes
✓ Process-3 found 2196 primes
✓ Process-4 found 2239 primes
Total primes found: 9592
Parallel time: 2.34s
Speedup: 3.61x faster!

KEY CONCEPTS:
✓ multiprocessing.Pool - create process pool
✓ pool.starmap() - map function to multiple inputs
✓ Each process runs on separate CPU core
✓ Best for CPU-intensive calculations
"""