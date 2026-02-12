"""
CONCEPT: Memory Views and Buffer Protocol
- memoryview: Access object's internal buffer
- Buffer protocol: Expose internal memory
- Zero-copy operations: Share data without copying
- Efficient for: large arrays, bytes, binary data

Benefits:
- No data copying (faster)
- Reduced memory usage
- Direct memory manipulation
- Efficient slicing

Supported Types:
- bytes, bytearray
- array.array
- numpy arrays
- mmap objects
"""

import sys
import array
import time

print("="*70)
print("Program 12: MEMORY VIEWS AND BUFFER PROTOCOL")
print("="*70)

# Example 1: Basic memory view
print("\n1. BASIC MEMORYVIEW:")
print("="*70)

# Create bytearray
data = bytearray(b'Hello World')
print(f"Original data: {data}")
print(f"Data size: {sys.getsizeof(data)} bytes")

# Create memory view (no copy!)
mv = memoryview(data)
print(f"\nMemoryview: {mv}")
print(f"Memoryview size: {sys.getsizeof(mv)} bytes")
print(f"Points to same data: {mv.obj is data}")

# Modify through memory view
mv[0] = ord('J')
print(f"\nAfter mv[0] = 'J':")
print(f"Original data: {data}")
print(f"Memoryview reflects change")

# Example 2: Slicing without copying
print("\n2. ZERO-COPY SLICING:")
print("="*70)

# Regular slicing creates copy
data = bytearray(b'A' * 1000000)
print(f"Original data: {len(data)} bytes")

# Traditional slice (creates copy)
slice1 = data[100:200]
print(f"\nTraditional slice: {sys.getsizeof(slice1)} bytes")
print(f"Different object: {slice1 is not data}")

# Memory view slice (no copy!)
mv = memoryview(data)
slice2 = mv[100:200]
print(f"\nMemoryview slice: {sys.getsizeof(slice2)} bytes")
print(f"No copy made: references original data")

# Example 3: Performance comparison
print("\n3. PERFORMANCE COMPARISON:")
print("="*70)

# Create large data
large_data = bytearray(10_000_000)

# Traditional slicing
start = time.time()
for _ in range(1000):
    chunk = large_data[100:1100]
time_copy = time.time() - start
print(f"Traditional slicing: {time_copy:.4f} seconds")

# Memory view slicing
mv = memoryview(large_data)
start = time.time()
for _ in range(1000):
    chunk = mv[100:1100]
time_view = time.time() - start
print(f"Memoryview slicing: {time_view:.4f} seconds")

print(f"Speedup: {time_copy / time_view:.2f}x faster")

# Example 4: Multi-dimensional memory views
print("\n4. MULTI-DIMENSIONAL VIEWS:")
print("="*70)

# Create 2D array
data = bytearray(12)  # 3x4 matrix
for i in range(12):
    data[i] = i

# Create 2D memory view
mv = memoryview(data).cast('B', shape=(3, 4))

print("2D Memory view (3x4):")
for row in range(3):
    row_data = [mv[row, col] for col in range(4)]
    print(f"   Row {row}: {row_data}")

# Modify element
mv[1, 2] = 99
print(f"\nAfter mv[1, 2] = 99:")
print(f"Original data: {list(data)}")

# Example 5: Format specifications
print("\n5. FORMAT SPECIFICATIONS:")
print("="*70)

# Integer array
int_data = array.array('i', [1, 2, 3, 4, 5])
print(f"Integer array: {int_data}")
print(f"Item size: {int_data.itemsize} bytes")

mv = memoryview(int_data)
print(f"\nMemoryview info:")
print(f"   Format: {mv.format}")
print(f"   Item size: {mv.itemsize}")
print(f"   Shape: {mv.shape}")
print(f"   Strides: {mv.strides}")
print(f"   Length: {len(mv)}")

# Example 6: Converting between types
print("\n6. TYPE CASTING:")
print("="*70)

# Bytes as integers
data = bytearray(b'\x01\x02\x03\x04\x08\x07\x06\x05')
print(f"Bytes: {list(data)}")

# View as unsigned bytes
mv_bytes = memoryview(data).cast('B')
print(f"As bytes: {list(mv_bytes)}")

# View as unsigned shorts (2 bytes each)
mv_short = memoryview(data).cast('H')
print(f"As shorts: {list(mv_short)}")

# View as unsigned ints (4 bytes each)
mv_int = memoryview(data).cast('I')
print(f"As ints: {list(mv_int)}")

# Example 7: Sharing data between structures
print("\n7. DATA SHARING:")
print("="*70)

class DataBuffer:
    def __init__(self, size):
        self._buffer = bytearray(size)
    
    def get_view(self, start, end):
        """Get view of buffer segment"""
        return memoryview(self._buffer)[start:end]
    
    def write(self, offset, data):
        """Write data at offset"""
        mv = memoryview(self._buffer)[offset:offset+len(data)]
        mv[:] = data
    
    def read(self, offset, length):
        """Read data from offset"""
        return bytes(self._buffer[offset:offset+length])

# Create buffer
buffer = DataBuffer(100)

# Write data
buffer.write(10, b'Hello')
buffer.write(20, b'World')

# Read data
print(f"Read at 10: {buffer.read(10, 5)}")
print(f"Read at 20: {buffer.read(20, 5)}")

# Get view (no copy)
view = buffer.get_view(10, 25)
print(f"View [10:25]: {bytes(view)}")

# Example 8: Memory view with numpy-like operations
print("\n8. ARRAY OPERATIONS:")
print("="*70)

# Create integer array
arr = array.array('i', range(10))
print(f"Original array: {list(arr)}")

# Get memory view
mv = memoryview(arr)

# Slice and modify
mv_slice = mv[2:7]
print(f"Slice [2:7]: {list(mv_slice)}")

# Modify through slice
for i in range(len(mv_slice)):
    mv_slice[i] = mv_slice[i] * 10

print(f"After multiplication: {list(arr)}")

# Example 9: Binary data manipulation
print("\n9. BINARY DATA MANIPULATION:")
print("="*70)

# Create binary data
data = bytearray(16)

# Write header
mv = memoryview(data)
mv[0:4] = b'HEAD'  # Magic number
mv[4:8] = (1234).to_bytes(4, 'little')  # Version
mv[8:16] = b'12345678'  # Data

print(f"Binary structure: {data}")

# Read back
header = bytes(mv[0:4])
version = int.from_bytes(mv[4:8], 'little')
payload = bytes(mv[8:16])

print(f"   Header: {header}")
print(f"   Version: {version}")
print(f"   Payload: {payload}")

# Example 10: Memory efficient file processing
print("\n10. FILE PROCESSING WITH MMAP:")
print("="*70)

import mmap
import os

# Create test file
filename = 'test_mmap.dat'
with open(filename, 'wb') as f:
    f.write(b'A' * 10000)

# Memory-map the file
with open(filename, 'r+b') as f:
    # Create memory map
    mm = mmap.mmap(f.fileno(), 0)
    
    print(f"File size: {len(mm)} bytes")
    
    # Create memory view
    mv = memoryview(mm)
    
    # Read without loading entire file
    print(f"First 10 bytes: {bytes(mv[0:10])}")
    
    # Modify (writes to file!)
    mv[0:5] = b'HELLO'
    
    # Read back
    print(f"After modification: {bytes(mv[0:10])}")
    
    mm.close()

# Verify file was modified
with open(filename, 'rb') as f:
    print(f"File now starts with: {f.read(10)}")

# Cleanup
os.remove(filename)

# Example 11: Summary
print("\n11. MEMORYVIEW SUMMARY:")
print("="*70)

print("""
Benefits of Memory Views:
✓ Zero-copy operations (faster, less memory)
✓ Direct memory access
✓ Efficient slicing
✓ Multi-dimensional views
✓ Type casting without copying
✓ Shared data between objects

Use Cases:
- Large binary data processing
- Image/audio manipulation
- Network packet handling
- File I/O optimization
- Inter-process communication
- Array operations

When to Use:
✓ Large data (> 1MB)
✓ Frequent slicing operations
✓ Need to share data
✓ Binary format parsing
✓ Performance-critical code

When NOT to Use:
✗ Small data (< 1KB)
✗ Need immutable copies
✗ Simple string operations
✗ One-time operations
""")