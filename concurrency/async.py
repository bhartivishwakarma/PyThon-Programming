"""
CONCEPT: Async/await for I/O-bound tasks
LEARN: Asynchronous programming basics
"""

import asyncio
import time

async def fetch_url(url, delay):
    """Simulate fetching a URL"""
    print(f"🌐 Fetching {url}...")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"✓ Fetched {url}")
    return f"Content from {url}"

async def fetch_all_sequential(urls):
    """Fetch URLs one by one (slow)"""
    results = []
    for url, delay in urls:
        result = await fetch_url(url, delay)
        results.append(result)
    return results

async def fetch_all_concurrent(urls):
    """Fetch URLs concurrently (fast)"""
    tasks = [fetch_url(url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    print("=== ASYNC WEB SCRAPING ===\n")
    
    urls = [
        ("https://example.com/page1", 2),
        ("https://example.com/page2", 1),
        ("https://example.com/page3", 3),
        ("https://example.com/page4", 1),
        ("https://example.com/page5", 2),
    ]
    
    # Sequential
    print("METHOD 1: Sequential (one at a time)")
    start = time.time()
    await fetch_all_sequential(urls)
    sequential_time = time.time() - start
    print(f"Sequential time: {sequential_time:.2f}s\n")
    
    # Concurrent
    print("\nMETHOD 2: Concurrent (all at once)")
    start = time.time()
    await fetch_all_concurrent(urls)
    concurrent_time = time.time() - start
    print(f"Concurrent time: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time/concurrent_time:.2f}x faster!")

if __name__ == "__main__":
    asyncio.run(main())

"""
OUTPUT:
=== ASYNC WEB SCRAPING ===

METHOD 1: Sequential (one at a time)
🌐 Fetching https://example.com/page1...
✓ Fetched https://example.com/page1
🌐 Fetching https://example.com/page2...
✓ Fetched https://example.com/page2
...
Sequential time: 9.00s

METHOD 2: Concurrent (all at once)
🌐 Fetching https://example.com/page1...
🌐 Fetching https://example.com/page2...
🌐 Fetching https://example.com/page3...
🌐 Fetching https://example.com/page4...
🌐 Fetching https://example.com/page5...
✓ Fetched https://example.com/page2
✓ Fetched https://example.com/page4
✓ Fetched https://example.com/page1
✓ Fetched https://example.com/page5
✓ Fetched https://example.com/page3
Concurrent time: 3.00s
Speedup: 3.00x faster!

KEY CONCEPTS:
✓ async def - defines async function
✓ await - waits for async operation
✓ asyncio.gather() - runs multiple tasks concurrently
✓ Perfect for I/O-bound tasks (network, file operations)
"""