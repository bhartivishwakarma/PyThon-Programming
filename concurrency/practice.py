"""
CONCEPT: Producer-Consumer pattern with Queue
LEARN: Thread-safe communication using queues
"""

import threading
import queue
import time
import random

def producer(q, name, num_items):
    """Produce items and put them in queue"""
    for i in range(num_items):
        item = f"Item-{i+1}"
        print(f"🏭 {name} producing: {item}")
        q.put(item)  # Thread-safe operation
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"🏭 {name} finished producing!")

def consumer(q, name, timeout=5):
    """Consume items from queue"""
    while True:
        try:
            # Wait up to 'timeout' seconds for an item
            item = q.get(timeout=timeout)
            print(f"   🛒 {name} consuming: {item}")
            time.sleep(random.uniform(0.2, 0.7))  # Simulate processing
            q.task_done()  # Mark item as processed
        except queue.Empty:
            print(f"   🛒 {name} timed out - no more items")
            break

if __name__ == "__main__":
    print("=== PRODUCER-CONSUMER PATTERN ===\n")
    
    # Create a queue with max size of 5
    work_queue = queue.Queue(maxsize=5)
    
    # Create producer threads
    producer1 = threading.Thread(
        target=producer, 
        args=(work_queue, "Producer-1", 5)
    )
    producer2 = threading.Thread(
        target=producer, 
        args=(work_queue, "Producer-2", 5)
    )
    
    # Create consumer threads
    consumer1 = threading.Thread(
        target=consumer, 
        args=(work_queue, "Consumer-1")
    )
    consumer2 = threading.Thread(
        target=consumer, 
        args=(work_queue, "Consumer-2")
    )
    
    # Start all threads
    producer1.start()
    producer2.start()
    consumer1.start()
    consumer2.start()
    
    # Wait for producers to finish
    producer1.join()
    producer2.join()
    
    # Wait for queue to be empty
    work_queue.join()
    
    # Wait for consumers to finish
    consumer1.join()
    consumer2.join()
    
    print("\n✓ All production and consumption complete!")

"""
OUTPUT:
=== PRODUCER-CONSUMER PATTERN ===

🏭 Producer-1 producing: Item-1
   🛒 Consumer-1 consuming: Item-1
🏭 Producer-2 producing: Item-1
   🛒 Consumer-2 consuming: Item-1
🏭 Producer-1 producing: Item-2
...

✓ All production and consumption complete!

KEY CONCEPTS:
✓ queue.Queue() - thread-safe queue
✓ q.put() - add item to queue
✓ q.get() - remove item from queue (blocks if empty)
✓ q.task_done() - signal item processing complete
"""