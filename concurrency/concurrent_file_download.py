"""
CONCEPT: Concurrent file downloads
LEARN: Practical use of threading for I/O tasks
"""

import threading
import time
import random
from queue import Queue

def download_file(url, file_id, result_queue):
    """Simulate downloading a file"""
    print(f"📥 Starting download: {url}")
    
    # Simulate download time (1-5 seconds)
    download_time = random.uniform(1, 5)
    
    # Simulate progress
    for progress in [25, 50, 75, 100]:
        time.sleep(download_time / 4)
        print(f"   {url}: {progress}% complete")
    
    result = {
        'file_id': file_id,
        'url': url,
        'time': download_time,
        'status': 'success'
    }
    
    result_queue.put(result)
    print(f"✓ Completed: {url} ({download_time:.2f}s)")

def download_manager(urls, max_concurrent=3):
    """Manage concurrent downloads with thread pool"""
    result_queue = Queue()
    active_threads = []
    completed = []
    
    print(f"Starting download manager ({max_concurrent} concurrent downloads)\n")
    
    for i, url in enumerate(urls):
        # Wait if too many active threads
        while len(active_threads) >= max_concurrent:
            active_threads = [t for t in active_threads if t.is_alive()]
            time.sleep(0.1)
        
        # Start new download
        thread = threading.Thread(
            target=download_file,
            args=(url, i, result_queue)
        )
        thread.start()
        active_threads.append(thread)
    
    # Wait for all to complete
    for thread in active_threads:
        thread.join()
    
    # Collect results
    while not result_queue.empty():
        completed.append(result_queue.get())
    
    return completed

if __name__ == "__main__":
    print("=== CONCURRENT FILE DOWNLOADER ===\n")
    
    # List of files to download
    files_to_download = [
        "https://example.com/file1.zip",
        "https://example.com/file2.zip",
        "https://example.com/file3.zip",
        "https://example.com/file4.zip",
        "https://example.com/file5.zip",
        "https://example.com/file6.zip",
    ]
    
    # Sequential download (baseline)
    print("METHOD 1: Sequential Download")
    print("-" * 50)
    start = time.time()
    
    for i, url in enumerate(files_to_download):
        result_queue = Queue()
        download_file(url, i, result_queue)
    
    sequential_time = time.time() - start
    print(f"\nSequential time: {sequential_time:.2f}s\n\n")
    
    # Concurrent download
    print("METHOD 2: Concurrent Download (3 at a time)")
    print("-" * 50)
    start = time.time()
    
    results = download_manager(files_to_download, max_concurrent=3)
    
    concurrent_time = time.time() - start
    
    print(f"\n\n{'='*50}")
    print("DOWNLOAD SUMMARY")
    print("="*50)
    print(f"Total files: {len(results)}")
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Concurrent time: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time/concurrent_time:.2f}x faster")
    print(f"\nAll downloads: SUCCESS ✓")

"""
OUTPUT:
=== CONCURRENT FILE DOWNLOADER ===

METHOD 1: Sequential Download
--------------------------------------------------
📥 Starting download: https://example.com/file1.zip
   https://example.com/file1.zip: 25% complete
   https://example.com/file1.zip: 50% complete
   https://example.com/file1.zip: 75% complete
   https://example.com/file1.zip: 100% complete
✓ Completed: https://example.com/file1.zip (3.24s)
...
Sequential time: 18.45s


METHOD 2: Concurrent Download (3 at a time)
--------------------------------------------------
Starting download manager (3 concurrent downloads)

📥 Starting download: https://example.com/file1.zip
📥 Starting download: https://example.com/file2.zip
📥 Starting download: https://example.com/file3.zip
   https://example.com/file2.zip: 25% complete
   https://example.com/file1.zip: 25% complete
   https://example.com/file3.zip: 25% complete
...
✓ Completed: https://example.com/file2.zip (2.31s)
📥 Starting download: https://example.com/file4.zip
...


==================================================
DOWNLOAD SUMMARY
==================================================
Total files: 6
Sequential time: 18.45s
Concurrent time: 7.12s
Speedup: 2.59x faster

All downloads: SUCCESS ✓
"""