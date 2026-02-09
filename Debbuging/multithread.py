"""
CONCEPT: Multi-threaded Debugging
- Debug programs with concurrent execution
- Track which thread is doing what
- Identify race conditions and synchronization issues
- Monitor shared resource access

Threading Challenges:
1. Race conditions - timing-dependent bugs
2. Deadlocks - threads waiting on each other
3. Data corruption - unsynchronized access
4. Difficult to reproduce - timing sensitive

Debugging Tools:
- Thread IDs in logs
- Timestamps for ordering
- Locks for synchronization
- Queues for safe data passing
"""

import threading
import logging
import time
from queue import Queue, Empty
import random

class ThreadDebugger:
    """
    Thread-safe debugger with comprehensive logging
    """
    def __init__(self, log_file='thread_debug.log'):
        # Configure logger
        self.logger = logging.getLogger('ThreadDebugger')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - Thread-%(thread)d(%(threadName)s) - '
            '%(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '[%(threadName)-12s] %(levelname)-8s %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Lock for synchronizing shared resources
        self.lock = threading.Lock()
        self.shared_counter = 0
    
    def worker(self, worker_id, queue):
        """
        Worker thread that processes items from queue
        """
        thread_id = threading.get_ident()
        self.logger.debug(f"Worker {worker_id} started (Thread ID: {thread_id})")
        
        items_processed = 0
        
        while True:
            try:
                # Get item from queue with timeout
                item = queue.get(timeout=1)
                
                if item is None:
                    self.logger.debug(f"Worker {worker_id} received shutdown signal")
                    break
                
                self.logger.info(f"Worker {worker_id} processing item: {item}")
                
                # Simulate work with random delay
                processing_time = random.uniform(0.1, 0.5)
                time.sleep(processing_time)
                
                # Process the item
                result = item * 2
                
                # Update shared counter (needs synchronization)
                with self.lock:
                    self.shared_counter += 1
                    counter_value = self.shared_counter
                
                self.logger.debug(
                    f"Worker {worker_id} completed item {item} -> {result} "
                    f"(took {processing_time:.3f}s, total processed: {counter_value})"
                )
                
                items_processed += 1
                queue.task_done()
                
            except Empty:
                self.logger.debug(f"Worker {worker_id} queue empty, waiting...")
                continue
            
            except Exception as e:
                self.logger.error(f"Worker {worker_id} error: {e}", exc_info=True)
                queue.task_done()
        
        self.logger.info(f"Worker {worker_id} terminated (processed {items_processed} items)")

def demonstrate_race_condition():
    """
    Demonstrate a race condition and how to debug it
    """
    print("\n" + "="*70)
    print("RACE CONDITION DEMONSTRATION")
    print("="*70)
    
    class UnsafeCounter:
        """Counter without thread safety"""
        def __init__(self):
            self.count = 0
        
        def increment_unsafe(self):
            """NOT thread-safe - race condition!"""
            temp = self.count
            time.sleep(0.0001)  # Simulate some processing
            self.count = temp + 1
        
        def increment_safe(self, lock):
            """Thread-safe with lock"""
            with lock:
                temp = self.count
                time.sleep(0.0001)
                self.count = temp + 1
    
    # Test unsafe version
    print("\nUnsafe increment (race condition):")
    unsafe_counter = UnsafeCounter()
    
    def unsafe_worker():
        for _ in range(100):
            unsafe_counter.increment_unsafe()
    
    threads = [threading.Thread(target=unsafe_worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Expected: 500, Got: {unsafe_counter.count}")
    print(f"Lost updates due to race condition: {500 - unsafe_counter.count}")
    
    # Test safe version
    print("\nSafe increment (with lock):")
    safe_counter = UnsafeCounter()
    lock = threading.Lock()
    
    def safe_worker():
        for _ in range(100):
            safe_counter.increment_safe(lock)
    
    threads = [threading.Thread(target=safe_worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Expected: 500, Got: {safe_counter.count}")

def demonstrate_deadlock_detection():
    """
    Demonstrate potential deadlock situation
    """
    print("\n" + "="*70)
    print("DEADLOCK DETECTION")
    print("="*70)
    
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    
    logger = logging.getLogger('DeadlockDemo')
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(threadName)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    def thread1_func():
        logger.info("Acquiring lock1...")
        with lock1:
            logger.info("Got lock1")
            time.sleep(0.1)
            
            logger.info("Trying to acquire lock2...")
            # This could deadlock if thread2 has lock2 and wants lock1
            with lock2:
                logger.info("Got lock2")
    
    def thread2_func():
        logger.info("Acquiring lock2...")
        with lock2:
            logger.info("Got lock2")
            time.sleep(0.1)
            
            logger.info("Trying to acquire lock1...")
            # This could deadlock if thread1 has lock1 and wants lock2
            with lock1:
                logger.info("Got lock1")
    
    print("\nNote: This might deadlock! (Ctrl+C to interrupt if it hangs)")
    print("Solution: Always acquire locks in the same order\n")
    
    # Comment out to avoid actual deadlock
    # t1 = threading.Thread(target=thread1_func, name="Thread-1")
    # t2 = threading.Thread(target=thread2_func, name="Thread-2")
    # t1.start()
    # t2.start()
    # t1.join(timeout=2)
    # t2.join(timeout=2)

def main():
    """
    Main demonstration of thread debugging
    """
    print("="*70)
    print("MULTI-THREADED DEBUGGING DEMONSTRATION")
    print("="*70)
    
    debugger = ThreadDebugger()
    queue = Queue()
    
    # Create worker threads
    num_workers = 3
    threads = []
    
    print(f"\nStarting {num_workers} worker threads...")
    
    for i in range(num_workers):
        t = threading.Thread(
            target=debugger.worker,
            args=(i, queue),
            name=f"Worker-{i}"
        )
        t.start()
        threads.append(t)
    
    # Add items to queue
    print("\nAdding items to queue...")
    num_items = 10
    for item in range(num_items):
        queue.put(item)
        debugger.logger.info(f"Main thread queued item: {item}")
    
    # Wait for all items to be processed
    print("\nWaiting for workers to complete...")
    queue.join()
    
    # Send shutdown signal to workers
    print("\nShutting down workers...")
    for _ in threads:
        queue.put(None)
    
    # Wait for all threads to finish
    for t in threads:
        t.join()
    
    print(f"\nAll workers completed!")
    print(f"Total items processed (shared counter): {debugger.shared_counter}")
    print(f"Check 'thread_debug.log' for detailed thread execution log")
    
    # Additional demonstrations
    demonstrate_race_condition()
    demonstrate_deadlock_detection()

if __name__ == "__main__":
    main()
    
    print("\n" + "="*70)
    print("MULTI-THREADED DEBUGGING COMPLETE")
    print("="*70)