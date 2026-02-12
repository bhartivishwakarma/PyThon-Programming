"""
CONCEPT: Memory-Mapped Files (mmap)
- Map file content to memory address space
- Access file like array/buffer
- Efficient for large files (don't load everything)
- Shared memory for IPC (Inter-Process Communication)
- OS handles paging (load/unload as needed)

Benefits:
- Fast random access
- Efficient for large files
- Shared memory IPC
- Lazy loading (only load what's used)
- Direct memory manipulation

Use Cases:
- Large file processing
- Database-like random access
- Shared memory communication
- Binary file manipulation
- Log file analysis
"""

import mmap
import os
import sys
import time
import struct

print("="*70)
print("Program 14: MEMORY-MAPPED FILES (mmap)")
print("="*70)

# Example 1: Basic mmap usage
print("\n1. BASIC MEMORY-MAPPED FILE:")
print("="*70)

filename = 'test_mmap.dat'

# Create file
print("Creating file...")
with open(filename, 'wb') as f:
    f.write(b'A' * 10000)

# Memory-map the file
print("Memory-mapping file...")
with open(filename, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    
    print(f"   File size: {len(mm)} bytes")
    print(f"   First 10 bytes: {mm[0:10]}")
    
    # Modify through mmap
    mm[0:5] = b'HELLO'
    print(f"   After modification: {mm[0:10]}")
    
    # Changes are written to file
    mm.flush()
    mm.close()

# Verify file was modified
with open(filename, 'rb') as f:
    print(f"   File content: {f.read(10)}")

# Example 2: Random access performance
print("\n2. RANDOM ACCESS PERFORMANCE:")
print("="*70)

# Create larger file
large_file = 'large_test.dat'
size = 10_000_000  # 10 MB

with open(large_file, 'wb') as f:
    f.write(b'X' * size)

# Regular file I/O
print("Regular file I/O:")
start = time.time()
with open(large_file, 'r+b') as f:
    for i in range(1000):
        offset = (i * 10000) % size
        f.seek(offset)
        data = f.read(100)
regular_time = time.time() - start
print(f"   Time: {regular_time:.4f} seconds")

# Memory-mapped file
print("\nMemory-mapped file:")
start = time.time()
with open(large_file, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    for i in range(1000):
        offset = (i * 10000) % size
        data = mm[offset:offset+100]
    mm.close()
mmap_time = time.time() - start
print(f"   Time: {mmap_time:.4f} seconds")

print(f"\nSpeedup: {regular_time / mmap_time:.2f}x faster")

# Example 3: Binary data structures
print("\n3. BINARY DATA STRUCTURES:")
print("="*70)

struct_file = 'structs.dat'

# Create file with struct data
class Record:
    FORMAT = 'I 20s f'  # unsigned int, 20 char string, float
    SIZE = struct.calcsize(FORMAT)
    
    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value
    
    def pack(self):
        name_bytes = self.name.encode('utf-8')[:20].ljust(20, b'\x00')
        return struct.pack(self.FORMAT, self.id, name_bytes, self.value)
    
    @staticmethod
    def unpack(data):
        id, name_bytes, value = struct.unpack(Record.FORMAT, data)
        name = name_bytes.decode('utf-8').rstrip('\x00')
        return Record(id, name, value)
    
    def __repr__(self):
        return f"Record(id={self.id}, name='{self.name}', value={self.value})"

# Write records
print("Writing records:")
records = [
    Record(1, "Alice", 95.5),
    Record(2, "Bob", 87.3),
    Record(3, "Charlie", 92.1),
]

with open(struct_file, 'wb') as f:
    for record in records:
        f.write(record.pack())
        print(f"   Written: {record}")

# Read using mmap
print("\nReading with mmap:")
with open(struct_file, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    
    num_records = len(mm) // Record.SIZE
    print(f"   Total records: {num_records}")
    
    # Random access to record 2
    offset = 1 * Record.SIZE
    record_data = mm[offset:offset + Record.SIZE]
    record = Record.unpack(record_data)
    print(f"   Record 2: {record}")
    
    # Modify record in place
    record.value = 99.9
    mm[offset:offset + Record.SIZE] = record.pack()
    mm.flush()
    
    mm.close()

# Verify modification
print("\nVerifying modification:")
with open(struct_file, 'rb') as f:
    f.seek(Record.SIZE)
    data = f.read(Record.SIZE)
    modified_record = Record.unpack(data)
    print(f"   Modified record: {modified_record}")

# Example 4: Shared memory between processes
print("\n4. SHARED MEMORY CONCEPT:")
print("="*70)

shared_file = 'shared.dat'

# Create shared memory file
with open(shared_file, 'wb') as f:
    f.write(b'\x00' * 1000)

print("Shared memory demo (single process):")

# Process 1 writes
with open(shared_file, 'r+b') as f:
    mm1 = mmap.mmap(f.fileno(), 0)
    mm1[0:12] = b'Hello World!'
    mm1.flush()
    print("   Process 1 wrote: 'Hello World!'")
    mm1.close()

# Process 2 reads
with open(shared_file, 'r+b') as f:
    mm2 = mmap.mmap(f.fileno(), 0)
    data = mm2[0:12]
    print(f"   Process 2 read: {data}")
    mm2.close()

# Example 5: Memory-mapped search
print("\n5. EFFICIENT SEARCHING:")
print("="*70)

search_file = 'search_data.txt'

# Create file with searchable content
content = '\n'.join([f"Line {i}: Some text here" for i in range(10000)])
with open(search_file, 'w') as f:
    f.write(content)

# Search with mmap
print("Searching for 'Line 5000':")
start = time.time()
with open(search_file, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    
    # Find pattern
    pattern = b'Line 5000'
    position = mm.find(pattern)
    
    if position != -1:
        # Get surrounding context
        line_start = mm.rfind(b'\n', 0, position) + 1
        line_end = mm.find(b'\n', position)
        line = mm[line_start:line_end]
        print(f"   Found at position {position}")
        print(f"   Line: {line.decode('utf-8')}")
    
    mm.close()

search_time = time.time() - start
print(f"   Search time: {search_time:.6f} seconds")

# Example 6: Memory view with mmap
print("\n6. MEMORYVIEW WITH MMAP:")
print("="*70)

# Create file
view_file = 'view_data.dat'
with open(view_file, 'wb') as f:
    f.write(bytearray(range(256)))

# Use memoryview for efficient access
with open(view_file, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    mv = memoryview(mm)
    
    print(f"Data size: {len(mv)} bytes")
    print(f"First 10 bytes: {list(mv[0:10])}")
    
    # Cast to different types
    mv_ints = mv.cast('I')  # unsigned ints
    print(f"As ints: {list(mv_ints[:5])}")
    
    mm.close()

# Example 7: Resizing memory-mapped files
print("\n7. RESIZING MMAP:")
print("="*70)

resize_file = 'resize_test.dat'

# Create initial file
with open(resize_file, 'wb') as f:
    f.write(b'A' * 100)

print("Initial size: 100 bytes")

# Resize by recreating mmap
with open(resize_file, 'r+b') as f:
    # Extend file
    f.seek(199)
    f.write(b'\x00')
    f.flush()
    
    # Create new mmap with new size
    mm = mmap.mmap(f.fileno(), 200)
    print(f"Resized to: {len(mm)} bytes")
    
    # Fill new space
    mm[100:200] = b'B' * 100
    mm.flush()
    mm.close()

# Example 8: Memory usage comparison
print("\n8. MEMORY USAGE COMPARISON:")
print("="*70)

import tracemalloc

large_file2 = 'memory_test.dat'
file_size = 50_000_000  # 50 MB

# Create large file
with open(large_file2, 'wb') as f:
    f.write(b'X' * file_size)

# Read entire file into memory
tracemalloc.start()
gc.collect()

with open(large_file2, 'rb') as f:
    data = f.read()

current, peak = tracemalloc.get_traced_memory()
full_read_memory = peak / 1024 / 1024
tracemalloc.stop()

del data
gc.collect()

# Memory-map file
tracemalloc.start()
gc.collect()

with open(large_file2, 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    # Access just a small part
    small_data = mm[0:1000]
    mm.close()

current, peak = tracemalloc.get_traced_memory()
mmap_memory = peak / 1024 / 1024
tracemalloc.stop()

print(f"File size: {file_size / 1024 / 1024:.1f} MB")
print(f"Full read memory: {full_read_memory:.2f} MB")
print(f"Mmap memory: {mmap_memory:.2f} MB")
print(f"Memory savings: {ful