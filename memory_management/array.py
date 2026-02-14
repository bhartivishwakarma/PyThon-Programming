"""
CONCEPT: Array Module for Numeric Data
- array.array: Efficient storage for numeric types
- Stores raw binary data (like C arrays)
- Homogeneous: all elements same type
- Much smaller than Python lists

Type Codes:
'b' - signed char (1 byte)
'B' - unsigned char (1 byte)
'h' - signed short (2 bytes)
'H' - unsigned short (2 bytes)
'i' - signed int (4 bytes)
'I' - unsigned int (4 bytes)
'f' - float (4 bytes)
'd' - double (8 bytes)

Memory Comparison:
List of ints: ~28 bytes per integer
Array of ints: ~4 bytes per integer
Savings: ~85% less memory

When to Use:
✓ Large numeric datasets
✓ Homogeneous data
✓ Binary I/O
✓ Performance-critical
✗ Mixed types
✗ Small datasets
"""

import array
import sys
import time
import struct

print("="*70)
print("Program 18: ARRAY MODULE FOR NUMERIC DATA")
print("="*70)

# Example 1: Basic array usage
print("\n1. BASIC ARRAY USAGE:")
print("="*70)

# Create arrays with different type codes
int_array = array.array('i', [1, 2, 3, 4, 5])
float_array = array.array('f', [1.1, 2.2, 3.3, 4.4, 5.5])
double_array = array.array('d', [1.1, 2.2, 3.3, 4.4, 5.5])

print(f"Integer array ('i'): {int_array}")
print(f"   Type code: {int_array.typecode}")
print(f"   Item size: {int_array.itemsize} bytes")

print(f"\nFloat array ('f'): {float_array}")
print(f"   Item size: {float_array.itemsize} bytes")

print(f"\nDouble array ('d'): {double_array}")
print(f"   Item size: {double_array.itemsize} bytes")

# Example 2: Memory comparison - list vs array
print("\n2. MEMORY COMPARISON:")
print("="*70)

n = 10000

# Python list
python_list = [i for i in range(n)]
list_size = sys.getsizeof(python_list)
# Add size of integer objects
list_total = list_size + sum(sys.getsizeof(i) for i in python_list[:100]) * (n // 100)

# Array
int_array = array.array('i', range(n))
array_size = sys.getsizeof(int_array)

print(f"Storing {n:,} integers:")
print(f"\nPython list:")
print(f"   Container: {list_size:,} bytes")
print(f"   ~Total: {list_total:,} bytes")
print(f"   ~Per item: {list_total // n} bytes")

print(f"\nArray:")
print(f"   Total: {array_size:,} bytes")
print(f"   Per item: {int_array.itemsize} bytes")

savings = list_total - array_size
print(f"\nMemory saved: {savings:,} bytes ({(savings/list_total)*100:.1f}%)")

# Example 3: All type codes
print("\n3. TYPE CODE COMPARISON:")
print("="*70)

type_codes = [
    ('b', "signed char"),
    ('B', "unsigned char"),
    ('h', "signed short"),
    ('H', "unsigned short"),
    ('i', "signed int"),
    ('I', "unsigned int"),
    ('l', "signed long"),
    ('L', "unsigned long"),
    ('f', "float"),
    ('d', "double"),
]

print(f"{'Code':<6} {'Type':<20} {'Size':<6} {'Range'}")
print("-" * 70)

for code, name in type_codes:
    arr = array.array(code)
    print(f"{code:<6} {name:<20} {arr.itemsize} bytes")

# Example 4: Array operations
print("\n4. ARRAY OPERATIONS:")
print("="*70)

arr = array.array('i', [1, 2, 3])
print(f"Original: {arr}")

# Append
arr.append(4)
print(f"After append(4): {arr}")

# Extend
arr.extend([5, 6, 7])
print(f"After extend([5,6,7]): {arr}")

# Insert
arr.insert(0, 0)
print(f"After insert(0, 0): {arr}")

# Remove
arr.remove(3)
print(f"After remove(3): {arr}")

# Pop
value = arr.pop()
print(f"After pop(): {arr}, popped={value}")

# Reverse
arr.reverse()
print(f"After reverse(): {arr}")

# Example 5: Array slicing
print("\n5. ARRAY SLICING:")
print("="*70)

arr = array.array('i', range(10))
print(f"Original: {arr}")

# Slice operations
slice1 = arr[2:7]
print(f"arr[2:7]: {slice1}")
print(f"Type: {type(slice1)}")

# Negative indexing
slice2 = arr[-3:]
print(f"arr[-3:]: {slice2}")

# Step slicing
slice3 = arr[::2]
print(f"arr[::2]: {slice3}")

# Example 6: Converting between list and array
print("\n6. CONVERSION:")
print("="*70)

# List to array
python_list = [1, 2, 3, 4, 5]
arr = array.array('i', python_list)
print(f"List to array: {arr}")

# Array to list
back_to_list = arr.tolist()
print(f"Array to list: {back_to_list}")
print(f"Type: {type(back_to_list)}")

# From bytes
byte_data = bytes([1, 0, 0, 0, 2, 0, 0, 0])  # Two 4-byte ints
arr = array.array('i')
arr.frombytes(byte_data)
print(f"\nFrom bytes: {arr}")

# To bytes
byte_output = arr.tobytes()
print(f"To bytes: {byte_output}")

# Example 7: File I/O with arrays
print("\n7. FILE I/O:")
print("="*70)

filename = 'array_data.bin'

# Write array to file
write_arr = array.array('i', range(1000))
with open(filename, 'wb') as f:
    write_arr.tofile(f)
print(f"Written {len(write_arr)} integers to file")

# Read array from file
read_arr = array.array('i')
with open(filename, 'rb') as f:
    read_arr.fromfile(f, 1000)
print(f"Read {len(read_arr)} integers from file")
print(f"First 10: {read_arr[:10]}")

# Cleanup
import os
os.remove(filename)

# Example 8: Performance comparison
print("\n8. PERFORMANCE COMPARISON:")
print("="*70)

n = 1_000_000

# List operations
start = time.time()
lst = []
for i in range(n):
    lst.append(i)
total = sum(lst)
list_time = time.time() - start

# Array operations
start = time.time()
arr = array.array('i')
for i in range(n):
    arr.append(i)
total = sum(arr)
array_time = time.time() - start

print(f"Processing {n:,} integers:")
print(f"   List: {list_time:.4f} seconds")
print(f"   Array: {array_time:.4f} seconds")
print(f"   Ratio: {list_time/array_time:.2f}x")

# Example 9: Numerical computations
print("\n9. NUMERICAL COMPUTATIONS:")
print("="*70)

# Create large arrays
size = 1000000
arr1 = array.array('f', (i * 1.5 for i in range(size)))
arr2 = array.array('f', (i * 2.0 for i in range(size)))

print(f"Created two arrays of {size:,} floats")

# Element-wise operations
start = time.time()
result = array.array('f')
for a, b in zip(arr1, arr2):
    result.append(a + b)
comp_time = time.time() - start

print(f"Element-wise addition: {comp_time:.4f} seconds")
print(f"First 5 results: {result[:5]}")

# Example 10: Memory view with arrays
print("\n10. MEMORYVIEW WITH ARRAYS:")
print("="*70)

arr = array.array('i', range(100))
print(f"Array: {arr[:10]}...")

# Create memory view
mv = memoryview(arr)
print(f"\nMemoryview:")
print(f"   Format: {mv.format}")
print(f"   Item size: {mv.itemsize}")
print(f"   Shape: {mv.shape}")
print(f"   Size: {len(mv)}")

# Modify through memoryview
mv[0] = 999
print(f"\nAfter mv[0] = 999:")
print(f"   Array: {arr[:10]}...")

# Example 11: Signed vs unsigned
print("\n11. SIGNED VS UNSIGNED:")
print("="*70)

# Signed byte (-128 to 127)
signed = array.array('b', [127, -128, 0])
print(f"Signed byte ('b'): {signed}")

# Unsigned byte (0 to 255)
unsigned = array.array('B', [127, 128, 255])
print(f"Unsigned byte ('B'): {unsigned}")

# Overflow behavior
try:
    signed.append(128)  # Out of range
except OverflowError as e:
    print(f"\nOverflow error: {e}")

# Example 12: Buffer protocol
print("\n12. BUFFER PROTOCOL:")
print("="*70)

arr = array.array('i', [1, 2, 3, 4, 5])

# Pack to bytes using struct
packed = struct.pack('5i', *arr)
print(f"Packed to bytes: {packed}")
print(f"Size: {len(packed)} bytes")

# Unpack back
unpacked = struct.unpack('5i', packed)
print(f"Unpacked: {unpacked}")

# Direct buffer access
buffer = memoryview(arr)
print(f"\nBuffer view: {bytes(buffer)}")

# Example 13: Real-world use case - sensor data
print("\n13. SENSOR DATA EXAMPLE:")
print("="*70)

class SensorDataLogger:
    """Efficient storage of sensor readings"""
    
    def __init__(self):
        self.timestamps = array.array('I')  # unsigned int
        self.temperatures = array.array('f')  # float
        self.humidity = array.array('f')  # float
        self.pressure = array.array('f')  # float
    
    def add_reading(self, timestamp, temp, humid, press):
        """Add sensor reading"""
        self.timestamps.append(timestamp)
        self.temperatures.append(temp)
        self.humidity.append(humid)
        self.pressure.append(press)
    
    def get_reading(self, index):
        """Get reading at index"""
        return {
            'timestamp': self.timestamps[index],
            'temperature': self.temperatures[index],
            'humidity': self.humidity[index],
            'pressure': self.pressure[index]
        }
    
    def memory_usage(self):
        """Calculate memory usage"""
        total = (sys.getsizeof(self.timestamps) +
                sys.getsizeof(self.temperatures) +
                sys.getsizeof(self.humidity) +
                sys.getsizeof(self.pressure))
        return total
    
    def save(self, filename):
        """Save to binary file"""
        with open(filename, 'wb') as f:
            self.timestamps.tofile(f)
            self.temperatures.tofile(f)
            self.humidity.tofile(f)
            self.pressure.tofile(f)

# Simulate sensor data
logger = SensorDataLogger()

print("Logging 10,000 sensor readings:")
import random
for i in range(10000):
    logger.add_reading(
        timestamp=1700000000 + i,
        temp=20.0 + random.uniform(-5, 5),
        humid=50.0 + random.uniform(-10, 10),
        press=1013.0 + random.uniform(-20, 20)
    )

print(f"   Total readings: {len(logger.timestamps)}")
print(f"   Memory used: {logger.memory_usage():,} bytes")

# Show sample reading
sample = logger.get_reading(0)
print(f"\nSample reading:")
print(f"   Timestamp: {sample['timestamp']}")
print(f"   Temperature: {sample['temperature']:.2f}°C")
print(f"   Humidity: {sample['humidity']:.2f}%")
print(f"   Pressure: {sample['pressure']:.2f} hPa")

# Example 14: Comparison with numpy (conceptual)
print("\n14. ARRAY VS NUMPY (CONCEPT):")
print("="*70)

print("""
array.array:
✓ Built-in (no dependencies)
✓ Simple, lightweight
✓ Good for 1D numeric data
✓ File I/O support
✗ No vectorized operations
✗ No multi-dimensional
✗ Limited functionality

numpy.ndarray:
✓ Vectorized operations (fast!)
✓ Multi-dimensional arrays
✓ Rich mathematical functions
✓ Broadcasting, slicing
✗ External dependency
✗ Larger overhead for small data
✗ Overkill for simple use cases

Use array.array when:
- Simple numeric storage
- No complex operations needed
- Want to avoid dependencies
- 1D data is sufficient

Use numpy when:
- Complex calculations
- Multi-dimensional data
- Need vectorization
- Scientific computing
""")

# Example 15: Summary
print("\n15. ARRAY MODULE SUMMARY:")
print("="*70)

print("""
Type Codes Quick Reference:
Integer Types:
  'b' - signed byte      (-128 to 127)
  'B' - unsigned byte    (0 to 255)
  'h' - short            (-32768 to 32767)
  'i' - int              (-2147483648 to 2147483647)
  'l' - long             (platform dependent)

Float Types:
  'f' - float            (4 bytes, ~7 decimal digits)
  'd' - double           (8 bytes, ~15 decimal digits)

Memory Savings (typical):
List of integers:     ~28 bytes/element
Array of integers:    ~4 bytes/element
Savings:             ~85% less memory

Best Practices:
1. Use for homogeneous numeric data
2. Choose appropriate type code
3. Consider range and precision
4. Use tofile/fromfile for I/O
5. Combine with memoryview for efficiency
6. Profile memory savings
7. Document type codes used

Common Patterns:
# Sensor data
temperatures = array.array('f')

# Pixel data
pixels = array.array('B')

# Coordinates
x_coords = array.array('d')
y_coords = array.array('d')

# Binary data
data = array.array('B')
data.frombytes(binary_data)

When to Use:
✓ Large numeric datasets (>10K elements)
✓ Binary file I/O
✓ Memory-constrained environments
✓ Sensor/measurement data
✓ Pixel/image data (raw)
✓ Audio samples
✓ Network protocols

When NOT to Use:
✗ Mixed data types
✗ Small datasets (<100 elements)
✗ Need complex operations
✗ Multi-dimensional data
✗ Frequent type conversions
""")