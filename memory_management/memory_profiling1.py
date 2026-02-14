"""
CONCEPT: Production Memory Profiling
- Profile with minimal performance impact
- Detect memory leaks in live systems
- Monitor trends over time
- Alert on anomalies
- Diagnostic snapshots

Challenges:
- Can't add significant overhead
- Need continuous monitoring
- Large data volumes
- Can't stop production
- Must be actionable

Strategies:
- Sampling (not continuous)
- Periodic snapshots
- Threshold-based alerts
- Incremental tracking
- Out-of-band analysis
"""

import tracemalloc
import gc
import sys
import time
import threading
from collections import deque
from datetime import datetime

print("="*70)
print("Program 20: MEMORY PROFILING IN PRODUCTION")
print("="*70)

# Example 1: Lightweight memory monitor
print("\n1. LIGHTWEIGHT MEMORY MONITOR:")
print("="*70)

class MemoryMonitor:
    """Minimal overhead memory monitoring"""
    
    def __init__(self, sample_interval=60):
        self.sample_interval = sample_interval
        self.samples = deque(maxlen=100)  # Keep last 100 samples
        self.running = False
        self.thread = None
    
    def start(self):
        """Start monitoring in background thread"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
        print(f"   Memory monitoring started (interval: {self.sample_interval}s)")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("   Memory monitoring stopped")
    
    def _monitor(self):
        """Background monitoring loop"""
        while self.running:
            # Take sample
            sample = {
                'timestamp': datetime.now(),
                'rss': self._get_memory_usage(),
                'objects': len(gc.get_objects()),
                'gc_count': gc.get_count()
            }
            self.samples.append(sample)
            
            time.sleep(self.sample_interval)
    
    def _get_memory_usage(self):
        """Get current memory usage (simplified)"""
        # In real production, use psutil or /proc/self/status
        gc.collect()
        return len(gc.get_objects()) * 100  # Simplified estimate
    
    def get_stats(self):
        """Get current statistics"""
        if not self.samples:
            return None
        
        latest = self.samples[-1]
        
        if len(self.samples) > 1:
            oldest = self.samples[0]
            growth = latest['rss'] - oldest['rss']
            growth_rate = growth / len(self.samples)
        else:
            growth = 0
            growth_rate = 0
        
        return {
            'current_rss': latest['rss'],
            'objects': latest['objects'],
            'gc_count': latest['gc_count'],
            'samples': len(self.samples),
            'growth': growth,
            'growth_rate': growth_rate
        }
    
    def check_thresholds(self, max_rss=None, max_growth_rate=None):
        """Check if thresholds exceeded"""
        stats = self.get_stats()
        if not stats:
            return []
        
        alerts = []
        
        if max_rss and stats['current_rss'] > max_rss:
            alerts.append(f"RSS exceeds threshold: {stats['current_rss']} > {max_rss}")
        
        if max_growth_rate and stats['growth_rate'] > max_growth_rate:
            alerts.append(f"Growth rate exceeds threshold: {stats['growth_rate']:.2f}")
        
        return alerts

# Test the monitor
monitor = MemoryMonitor(sample_interval=1)
monitor.start()

print("\nSimulating work:")
for i in range(5):
    # Simulate some work
    data = [x for x in range(10000)]
    time.sleep(1.5)
    
    stats = monitor.get_stats()
    if stats:
        print(f"   Sample {i+1}: RSS={stats['current_rss']:,}, Objects={stats['objects']:,}")

monitor.stop()

# Example 2: Sampling profiler
print("\n2. SAMPLING PROFILER:")
print("="*70)

class SamplingProfiler:
    """Sample memory allocations periodically"""
    
    def __init__(self, sample_rate=0.01):  # 1% of operations
        self.sample_rate = sample_rate
        self.samples = []
        self.enabled = False
    
    def enable(self):
        """Enable profiling"""
        self.enabled = True
        tracemalloc.start()
        print(f"   Sampling profiler enabled (rate: {self.sample_rate*100}%)")
    
    def disable(self):
        """Disable profiling"""
        self.enabled = False
        tracemalloc.stop()
        print("   Sampling profiler disabled")
    
    def maybe_sample(self):
        """Maybe take a sample (based on sample rate)"""
        import random
        if self.enabled and random.random() < self.sample_rate:
            current, peak = tracemalloc.get_traced_memory()
            self.samples.append({
                'timestamp': datetime.now(),
                'current': current,
                'peak': peak
            })
    
    def get_report(self):
        """Get profiling report"""
        if not self.samples:
            return "No samples collected"
        
        avg_current = sum(s['current'] for s in self.samples) / len(self.samples)
        avg_peak = sum(s['peak'] for s in self.samples) / len(self.samples)
        
        return {
            'samples': len(self.samples),
            'avg_current': avg_current / 1024 / 1024,  # MB
            'avg_peak': avg_peak / 1024 / 1024,  # MB
        }

profiler = SamplingProfiler(sample_rate=0.1)  # 10% for demo
profiler.enable()

print("\nSimulating operations:")
for i in range(100):
    # Simulate operation
    data = list(range(1000))
    profiler.maybe_sample()

report = profiler.get_report()
print(f"\nProfiling report:")
print(f"   Samples: {report['samples']}")
print(f"   Avg current: {report['avg_current']:.2f} MB")
print(f"   Avg peak: {report['avg_peak']:.2f} MB")

profiler.disable()

# Example 3: Memory leak detector
print("\n3. MEMORY LEAK DETECTOR:")
print("="*70)

class LeakDetector:
    """Detect memory leaks by tracking growth"""
    
    def __init__(self, window_size=10, threshold=1.5):
        self.window_size = window_size
        self.threshold = threshold
        self.snapshots = deque(maxlen=window_size)
    
    def take_snapshot(self):
        """Take memory snapshot"""
        gc.collect()
        
        snapshot = {
            'timestamp': datetime.now(),
            'objects': len(gc.get_objects()),
            'types': self._count_by_type()
        }
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def _count_by_type(self):
        """Count objects by type"""
        from collections import defaultdict
        counts = defaultdict(int)
        
        for obj in gc.get_objects():
            counts[type(obj).__name__] += 1
        
        return dict(counts)
    
    def detect_leak(self):
        """Detect if memory is leaking"""
        if len(self.snapshots) < self.window_size:
            return None
        
        # Compare first and last snapshot
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        growth_ratio = last['objects'] / first['objects']
        
        if growth_ratio > self.threshold:
            # Find which types grew most
            growing_types = []
            
            for type_name in last['types']:
                if type_name in first['types']:
                    old_count = first['types'][type_name]
                    new_count = last['types'][type_name]
                    
                    if new_count > old_count * 1.5:  # 50% growth
                        growing_types.append({
                            'type': type_name,
                            'old': old_count,
                            'new': new_count,
                            'growth': new_count - old_count
                        })
            
            # Sort by growth
            growing_types.sort(key=lambda x: x['growth'], reverse=True)
            
            return {
                'detected': True,
                'growth_ratio': growth_ratio,
                'total_objects': last['objects'],
                'growing_types': growing_types[:5]  # Top 5
            }
        
        return {'detected': False}

detector = LeakDetector(window_size=5, threshold=1.3)

print("Taking snapshots:")
for i in range(7):
    # Simulate leak
    leak = [list(range(1000)) for _ in range(100)]
    
    snapshot = detector.take_snapshot()
    print(f"   Snapshot {i+1}: {snapshot['objects']:,} objects")
    
    time.sleep(0.1)

print("\nChecking for leaks:")
result = detector.detect_leak()

if result and result['detected']:
    print(f"   ⚠️  LEAK DETECTED!")
    print(f"   Growth ratio: {result['growth_ratio']:.2f}x")
    print(f"   Total objects: {result['total_objects']:,}")
    print(f"\n   Growing types:")
    for item in result['growing_types']:
        print(f"      {item['type']}: {item['old']} → {item['new']} (+{item['growth']})")
else:
    print("   ✓ No leak detected")

# Example 4: Threshold-based alerting
print("\n4. THRESHOLD-BASED ALERTING:")
print("="*70)

class MemoryAlerter:
    """Alert on memory thresholds"""
    
    def __init__(self):
        self.thresholds = {
            'warning': 100_000,  # objects
            'critical': 200_000
        }
        self.alerts_sent = {
            'warning': [],
            'critical': []
        }
    
    def check(self):
        """Check current memory against thresholds"""
        gc.collect()
        current_objects = len(gc.get_objects())
        
        alerts = []
        
        if current_objects > self.thresholds['critical']:
            if not self._recently_alerted('critical'):
                alerts.append({
                    'level': 'CRITICAL',
                    'message': f"Object count: {current_objects:,}",
                    'timestamp': datetime.now()
                })
                self.alerts_sent['critical'].append(datetime.now())
        
        elif current_objects > self.thresholds['warning']:
            if not self._recently_alerted('warning'):
                alerts.append({
                    'level': 'WARNING',
                    'message': f"Object count: {current_objects:,}",
                    'timestamp': datetime.now()
                })
                self.alerts_sent['warning'].append(datetime.now())
        
        return alerts
    
    def _recently_alerted(self, level, window=300):
        """Check if alert sent recently (within window seconds)"""
        if not self.alerts_sent[level]:
            return False
        
        last_alert = self.alerts_sent[level][-1]
        elapsed = (datetime.now() - last_alert).total_seconds()
        
        return elapsed < window

alerter = MemoryAlerter()

print("Simulating memory growth:")
temp_data = []

for i in range(3):
    # Grow memory
    temp_data.extend([list(range(1000)) for _ in range(5000)])
    
    alerts = alerter.check()
    
    if alerts:
        for alert in alerts:
            print(f"   🚨 [{alert['level']}] {alert['message']}")
    else:
        print(f"   ✓ Check {i+1}: OK")
    
    time.sleep(0.1)

# Cleanup
temp_data.clear()
gc.collect()

# Example 5: Periodic snapshot with comparison
print("\n5. PERIODIC SNAPSHOT COMPARISON:")
print("="*70)

class SnapshotManager:
    """Manage periodic memory snapshots"""
    
    def __init__(self):
        self.snapshots = {}
        tracemalloc.start()
    
    def take_snapshot(self, name):
        """Take named snapshot"""
        snapshot = tracemalloc.take_snapshot()
        self.snapshots[name] = snapshot
        print(f"   Snapshot '{name}' taken")
    
    def compare(self, snapshot1_name, snapshot2_name, top_n=5):
        """Compare two snapshots"""
        if snapshot1_name not in self.snapshots:
            return f"Snapshot '{snapshot1_name}' not found"
        
        if snapshot2_name not in self.snapshots:
            return f"Snapshot '{snapshot2_name}' not found"
        
        snapshot1 = self.snapshots[snapshot1_name]
        snapshot2 = self.snapshots[snapshot2_name]
        
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        print(f"\n   Comparing '{snapshot1_name}' → '{snapshot2_name}':")
        print(f"   Top {top_n} memory changes:")
        
        for i, stat in enumerate(stats[:top_n], 1):
            print(f"      {i}. {stat}")
    
    def cleanup(self):
        """Cleanup snapshots"""
        self.snapshots.clear()
        tracemalloc.stop()

manager = SnapshotManager()

print("Taking baseline snapshot:")
manager.take_snapshot('baseline')

print("\nAllocating memory:")
data1 = [list(range(10000)) for _ in range(100)]
manager.take_snapshot('after_allocation_1')

print("\nAllocating more:")
data2 = {i: list(range(1000)) for i in range(500)}
manager.take_snapshot('after_allocation_2')

manager.compare('baseline', 'after_allocation_1')
manager.compare('after_allocation_1', 'after_allocation_2')

manager.cleanup()

# Example 6: Production-ready monitoring class
print("\n6. PRODUCTION MEMORY MONITOR:")
print("="*70)

class ProductionMemoryMonitor:
    """Complete production monitoring solution"""
    
    def __init__(self, config=None):
        self.config = config or {
            'sample_interval': 60,
            'snapshot_interval': 300,
            'alert_threshold': 1.5,
            'history_size': 1000
        }
        
        self.history = deque(maxlen=self.config['history_size'])
        self.snapshots = {}
        self.running = False
        self.thread = None
    
    def start(self):
        """Start monitoring"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        tracemalloc.start()
        print("   Production monitor started")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.thread:
            self.thread.join()
        tracemalloc.stop()
        print("   Production monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        last_snapshot = time.time()
        
        while self.running:
            # Take sample
            sample = self._take_sample()
            self.history.append(sample)
            
            # Periodic snapshot
            if time.time() - last_snapshot > self.config['snapshot_interval']:
                self._take_snapshot()
                last_snapshot = time.time()
            
            # Check for issues
            self._check_issues(sample)
            
            time.sleep(self.config['sample_interval'])
    
    def _take_sample(self):
        """Take memory sample"""
        current, peak = tracemalloc.get_traced_memory()
        
        return {
            'timestamp': datetime.now(),
            'current': current,
            'peak': peak,
            'objects': len(gc.get_objects())
        }
    
    def _take_snapshot(self):
        """Take full snapshot"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.snapshots[timestamp] = tracemalloc.take_snapshot()
    
    def _check_issues(self, sample):
        """Check for memory issues"""
        if len(self.history) < 10:
            return
        
        # Check growth trend
        recent = list(self.history)[-10:]
        growth = (recent[-1]['current'] - recent[0]['current']) / recent[0]['current']
        
        if growth > self.config['alert_threshold']:
            self._alert('GROWTH', f"Memory grew {growth*100:.1f}% in last 10 samples")
    
    def _alert(self, alert_type, message):
        """Send alert"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n   🚨 [{timestamp}] {alert_type}: {message}")
    
    def get_report(self):
        """Get current status report"""
        if not self.history:
            return "No data"
        
        latest = self.history[-1]
        
        return {
            'current_mb': latest['current'] / 1024 / 1024,
            'peak_mb': latest['peak'] / 1024 / 1024,
            'objects': latest['objects'],
            'samples': len(self.history),
            'snapshots': len(self.snapshots)
        }

# Demo (abbreviated)
prod_monitor = ProductionMemoryMonitor(config={
    'sample_interval': 1,
    'snapshot_interval': 3,
    'alert_threshold': 0.2,  # 20% for demo
    'history_size': 100
})

print("Starting production monitor (5 seconds):")
prod_monitor.start()

# Simulate work with growth
for i in range(5):
    data = [list(range(10000)) for _ in range(50)]
    time.sleep(1)

prod_monitor.stop()

report = prod_monitor.get_report()
print(f"\nFinal report:")
print(f"   Current: {report['current_mb']:.2f} MB")
print(f"   Peak: {report['peak_mb']:.2f} MB")
print(f"   Objects: {report['objects']:,}")
print(f"   Samples: {report['samples']}")
print(f"   Snapshots: {report['snapshots']}")

# Example 7: Summary
print("\n7. PRODUCTION PROFILING SUMMARY:")
print("="*70)

print("""
Production Monitoring Strategies:

1. Lightweight Sampling
   ✓ Low overhead (<1% CPU)
   ✓ Sample periodically (60s+)
   ✓ Keep limited history
   ✓ Aggregate metrics

2. Threshold Alerts
   ✓ Define warning/critical levels
   ✓ Alert on sustained growth
   ✓ Rate-limit alerts
   ✓ Actionable messages

3. Periodic Snapshots
   ✓ Full snapshots every 5-15 min
   ✓ Compare over time
   ✓ Identify leak sources
   ✓ Store for analysis

4. Trend Analysis
   ✓ Track growth rate
   ✓ Detect gradual leaks
   ✓ Baseline comparison
   ✓ Seasonal patterns

5. Minimal Impact
   ✓ Sample, don't trace everything
   ✓ Background threads
   ✓ Limit history size
   ✓ Async processing

Best Practices:
- Start with sampling (not continuous)
- Set realistic thresholds
- Alert on trends, not spikes
- Keep diagnostics separate
- Test monitoring overhead
- Have runbooks for alerts
- Rotate/archive snapshots
- Monitor the monitor!

Metrics to Track:
📊 RSS (Resident Set Size)
📊 Object count
📊 GC collections
📊 Growth rate
📊 Peak usage
📊 Type distribution

Alert Conditions:
🚨 Sustained growth (>20% over time)
🚨 Threshold exceeded
🚨 Abnormal GC frequency
🚨 Specific type explosion
🚨 Failed allocations

Tools:
- tracemalloc (built-in)
- gc module
- psutil (RSS, system memory)
- memory_profiler (development)
- py-spy (sampling profiler)
- Custom monitoring

Production Checklist:
□ Minimal overhead (<1% CPU)
□ Configurable sampling rate
□ Threshold-based alerts
□ Historical trending
□ Automated analysis
□ Integration with monitoring
□ Runbooks for alerts
□ Diagnostic snapshots
□ Log rotation
□ Performance tested
""")