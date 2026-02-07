"""
CONCEPT: Using ThreadPoolExecutor for parallel tasks
LEARN: Thread pools for managing multiple tasks
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_image(image_name, processing_time):
    """Simulate image processing"""
    print(f"🖼️  Processing {image_name}...")
    time.sleep(processing_time)  # Simulate work
    result = f"{image_name} processed in {processing_time}s"
    print(f"✓ {result}")
    return result

if __name__ == "__main__":
    print("=== THREAD POOL IMAGE PROCESSING ===\n")
    
    # List of images to process
    images = [
        ("photo1.jpg", 2),
        ("photo2.jpg", 1),
        ("photo3.jpg", 3),
        ("photo4.jpg", 1),
        ("photo5.jpg", 2),
        ("photo6.jpg", 1),
    ]
    
    print("METHOD 1: Sequential Processing")
    start = time.time()
    for img_name, proc_time in images:
        process_image(img_name, proc_time)
    sequential_time = time.time() - start
    print(f"Sequential time: {sequential_time:.2f}s\n")
    
    print("\nMETHOD 2: Parallel Processing with ThreadPool")
    start = time.time()
    
    # Create thread pool with 3 workers
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        futures = [
            executor.submit(process_image, img_name, proc_time)
            for img_name, proc_time in images
        ]
        
        # Wait for all to complete
        results = [future.result() for future in as_completed(futures)]
    
    parallel_time = time.time() - start
    
    print(f"\n✓ Parallel time: {parallel_time:.2f}s")
    print(f"✓ Speedup: {sequential_time/parallel_time:.2f}x faster!")

"""
OUTPUT:
=== THREAD POOL IMAGE PROCESSING ===

METHOD 1: Sequential Processing
🖼️  Processing photo1.jpg...
✓ photo1.jpg processed in 2s
🖼️  Processing photo2.jpg...
✓ photo2.jpg processed in 1s
...
Sequential time: 10.00s

METHOD 2: Parallel Processing with ThreadPool
🖼️  Processing photo1.jpg...
🖼️  Processing photo2.jpg...
🖼️  Processing photo3.jpg...
✓ photo2.jpg processed in 1s
🖼️  Processing photo4.jpg...
...
✓ Parallel time: 4.00s
✓ Speedup: 2.50x faster!

KEY CONCEPTS:
✓ ThreadPoolExecutor - manages thread pool
✓ executor.submit() - submit task to pool
✓ as_completed() - process results as they finish
"""