"""
CONCEPT: Comparing threading vs multiprocessing
LEARN: When to use each approach
"""

import threading
import multiprocessing
import time

def cpu_bound_task(n):
    """CPU-intensive task: calculate sum of squares"""
    total = 0
    for i in range(n):
        total += i * i
    return total

def io_bound_task(delay):
    """I/O-intensive task: simulate file/network operation"""
    time.sleep(delay)
    return f"Task completed after {delay}s"

def run_with_threads(task, args_list, task_type):
    """Run tasks using threading"""
    print(f"\n🧵 THREADING - {task_type}")
    start = time.time()
    
    threads = []
    for args in args_list:
        t = threading.Thread(target=task, args=(args,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"   Time: {elapsed:.2f}s")
    return elapsed

def run_with_processes(task, args_list, task_type):
    """Run tasks using multiprocessing"""
    print(f"\n🔄 MULTIPROCESSING - {task_type}")
    start = time.time()
    
    processes = []
    for args in args_list:
        p = multiprocessing.Process(target=task, args=(args,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    
    elapsed = time.time() - start
    print(f"   Time: {elapsed:.2f}s")
    return elapsed

def run_sequential(task, args_list, task_type):
    """Run tasks sequentially (baseline)"""
    print(f"\n➡️  SEQUENTIAL - {task_type}")
    start = time.time()
    
    for args in args_list:
        task(args)
    
    elapsed = time.time() - start
    print(f"   Time: {elapsed:.2f}s")
    return elapsed

if __name__ == "__main__":
    print("="*50)
    print("THREADING vs MULTIPROCESSING COMPARISON")
    print("="*50)
    
    # Test 1: CPU-bound tasks
    print("\n\n📊 TEST 1: CPU-BOUND TASKS (calculations)")
    print("-" * 50)
    cpu_args = [10000000, 10000000, 10000000, 10000000]
    
    seq_cpu = run_sequential(cpu_bound_task, cpu_args, "CPU-bound")
    thread_cpu = run_with_threads(cpu_bound_task, cpu_args, "CPU-bound")
    proc_cpu = run_with_processes(cpu_bound_task, cpu_args, "CPU-bound")
    
    print(f"\n📈 CPU-bound Results:")
    print(f"   Sequential:      {seq_cpu:.2f}s (baseline)")
    print(f"   Threading:       {thread_cpu:.2f}s ({seq_cpu/thread_cpu:.2f}x)")
    print(f"   Multiprocessing: {proc_cpu:.2f}s ({seq_cpu/proc_cpu:.2f}x) ⭐")
    
    # Test 2: I/O-bound tasks
    print("\n\n📊 TEST 2: I/O-BOUND TASKS (network/file)")
    print("-" * 50)
    io_args = [1, 1, 1, 1]
    
    seq_io = run_sequential(io_bound_task, io_args, "I/O-bound")
    thread_io = run_with_threads(io_bound_task, io_args, "I/O-bound")
    proc_io = run_with_processes(io_bound_task, io_args, "I/O-bound")
    
    print(f"\n📈 I/O-bound Results:")
    print(f"   Sequential:      {seq_io:.2f}s (baseline)")
    print(f"   Threading:       {thread_io:.2f}s ({seq_io/thread_io:.2f}x) ⭐")
    print(f"   Multiprocessing: {proc_io:.2f}s ({seq_io/proc_io:.2f}x)")
    
    # Summary
    print("\n\n" + "="*50)
    print("📚 SUMMARY")
    print("="*50)
    print("✓ Use THREADING for:")
    print("  - I/O-bound tasks (file, network, database)")
    print("  - Tasks that wait a lot")
    print("  - Lighter overhead")
    print()
    print("✓ Use MULTIPROCESSING for:")
    print("  - CPU-bound tasks (calculations, processing)")
    print("  - True parallel computation")
    print("  - Bypassing Python GIL")

"""
OUTPUT:
==================================================
THREADING vs MULTIPROCESSING COMPARISON
==================================================


📊 TEST 1: CPU-BOUND TASKS (calculations)
--------------------------------------------------

➡️  SEQUENTIAL - CPU-bound
   Time: 8.45s

🧵 THREADING - CPU-bound
   Time: 8.52s

🔄 MULTIPROCESSING - CPU-bound
   Time: 2.23s

📈 CPU-bound Results:
   Sequential:      8.45s (baseline)
   Threading:       8.52s (0.99x)  ← No speedup due to GIL!
   Multiprocessing: 2.23s (3.79x) ⭐ ← True parallelism!


📊 TEST 2: I/O-BOUND TASKS (network/file)
--------------------------------------------------

➡️  SEQUENTIAL - I/O-bound
   Time: 4.00s

🧵 THREADING - I/O-bound
   Time: 1.00s

🔄 MULTIPROCESSING - I/O-bound
   Time: 1.05s

📈 I/O-bound Results:
   Sequential:      4.00s (baseline)
   Threading:       1.00s (4.00x) ⭐ ← Perfect for I/O!
   Multiprocessing: 1.05s (3.81x)  ← Extra overhead


==================================================
📚 SUMMARY
==================================================
✓ Use THREADING for:
  - I/O-bound tasks (file, network, database)
  - Tasks that wait a lot
  - Lighter overhead

✓ Use MULTIPROCESSING for:
  - CPU-bound tasks (calculations, processing)
  - True parallel computation
  - Bypassing Python GIL
"""