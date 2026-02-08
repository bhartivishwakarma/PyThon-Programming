"""
CONCEPT: Automatic performance tracking for all methods
LEARN: Method execution time monitoring and statistics
"""

import time
import functools
from collections import defaultdict

class PerformanceStats:
    """Store performance statistics for methods"""
    def __init__(self):
        self.call_count = 0
        self.total_time = 0
        self.min_time = float('inf')
        self.max_time = 0
        self.call_history = []
    
    def add_call(self, duration):
        self.call_count += 1
        self.total_time += duration
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.call_history.append(duration)
    
    def average_time(self):
        return self.total_time / self.call_count if self.call_count > 0 else 0
    
    def __repr__(self):
        return (f"PerformanceStats(calls={self.call_count}, "
                f"avg={self.average_time():.4f}s, "
                f"min={self.min_time:.4f}s, "
                f"max={self.max_time:.4f}s)")

class PerformanceMonitorMeta(type):
    """Metaclass that monitors performance of all methods"""
    
    def __new__(cls, name, bases, attrs):
        # Create performance tracking dictionary
        performance_data = defaultdict(PerformanceStats)
        
        # Wrap all callable methods
        for attr_name, attr_value in list(attrs.items()):
            if callable(attr_value) and not attr_name.startswith('_'):
                attrs[attr_name] = cls._wrap_method(attr_value, attr_name, performance_data)
        
        attrs['_performance_data'] = performance_data
        
        # Add reporting methods
        def get_performance_report(self):
            """Get performance report for all methods"""
            report = f"\n{'='*60}\n"
            report += f"Performance Report for {self.__class__.__name__}\n"
            report += f"{'='*60}\n"
            
            for method_name, stats in sorted(self._performance_data.items()):
                report += f"\n{method_name}:\n"
                report += f"  Calls: {stats.call_count}\n"
                report += f"  Total Time: {stats.total_time:.4f}s\n"
                report += f"  Average Time: {stats.average_time():.4f}s\n"
                report += f"  Min Time: {stats.min_time:.4f}s\n"
                report += f"  Max Time: {stats.max_time:.4f}s\n"
            
            return report
        
        def reset_performance_stats(self):
            """Reset all performance statistics"""
            self._performance_data.clear()
        
        def get_method_stats(self, method_name):
            """Get stats for a specific method"""
            return self._performance_data.get(method_name)
        
        attrs['get_performance_report'] = get_performance_report
        attrs['reset_performance_stats'] = reset_performance_stats
        attrs['get_method_stats'] = get_method_stats
        
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def _wrap_method(method, method_name, performance_data):
        """Wrap a method to track its performance"""
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = method(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                performance_data[method_name].add_call(duration)
        
        return wrapper

class DataProcessor(metaclass=PerformanceMonitorMeta):
    def __init__(self):
        self.data = []
    
    def load_data(self, size):
        """Simulate loading data"""
        time.sleep(0.1)
        self.data = list(range(size))
        return len(self.data)
    
    def process_data(self):
        """Simulate processing data"""
        time.sleep(0.2)
        total = sum(self.data)
        return total
    
    def analyze_data(self):
        """Simulate analyzing data"""
        time.sleep(0.15)
        if not self.data:
            return {}
        return {
            'mean': sum(self.data) / len(self.data),
            'max': max(self.data),
            'min': min(self.data)
        }
    
    def save_results(self, results):
        """Simulate saving results"""
        time.sleep(0.05)
        return True

class Calculator(metaclass=PerformanceMonitorMeta):
    def add(self, x, y):
        time.sleep(0.01)
        return x + y
    
    def multiply(self, x, y):
        time.sleep(0.02)
        return x * y
    
    def power(self, base, exp):
        time.sleep(0.03)
        return base ** exp
    
    def factorial(self, n):
        time.sleep(0.05)
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

if __name__ == "__main__":
    # Test DataProcessor
    print("Testing DataProcessor...")
    processor = DataProcessor()
    
    processor.load_data(100)
    processor.process_data()
    processor.analyze_data()
    processor.save_results({'status': 'complete'})
    
    # Call methods multiple times
    for _ in range(3):
        processor.load_data(50)
        processor.process_data()
    
    print(processor.get_performance_report())
    
    # Test Calculator
    print("\n\nTesting Calculator...")
    calc = Calculator()
    
    calc.add(5, 3)
    calc.add(10, 20)
    calc.multiply(4, 7)
    calc.multiply(3, 9)
    calc.power(2, 10)
    calc.factorial(5)
    calc.factorial(10)
    
    print(calc.get_performance_report())
    
    # Get specific method stats
    print("\n\nSpecific method statistics:")
    add_stats = calc.get_method_stats('add')
    print(f"Add method: {add_stats}")