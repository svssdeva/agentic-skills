<!-- Source: https://www.skills.sh/wshobson/agents/python-performance-optimization -->
<!-- Install: npx skills add https://github.com/wshobson/agents --skill python-performance-optimization -->
---
name: python-performance-optimization
description: Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance.
---

# Python Performance Optimization

Comprehensive guide to profiling, analyzing, and optimizing Python code for better performance, including CPU profiling, memory optimization, and implementation best practices.

## When to Use This Skill

- Identifying performance bottlenecks in Python applications
- Reducing application latency and response times
- Optimizing CPU-intensive operations
- Reducing memory consumption and memory leaks
- Improving database query performance
- Optimizing I/O operations
- Speeding up data processing pipelines
- Implementing high-performance algorithms
- Profiling production applications

## Core Concepts

- **CPU Profiling**: Identify time-consuming functions
- **Memory Profiling**: Track memory allocation and leaks
- **Line Profiling**: Profile at line-by-line granularity
- **Call Graph**: Visualize function call relationships
- **Optimization Strategies**: Algorithmic, implementation, parallelization, caching, native extensions

### Performance Metrics

- **Execution Time**: How long operations take
- **Memory Usage**: Peak and average memory consumption
- **CPU Utilization**: Processor usage patterns
- **I/O Wait**: Time spent on I/O operations

## Quick Start

### Basic Timing

```python
import time

start = time.time()
# Your code here
result = sum(range(1000000))
elapsed = time.time() - start
print(f"Execution time: {elapsed:.4f} seconds")

# Better: use timeit for accurate measurements
import timeit

execution_time = timeit.timeit(
    "sum(range(1000000))",
    number=100
)
print(f"Average time: {execution_time/100:.6f} seconds")
```

## Profiling Tools

### cProfile — CPU Profiling

```python
import cProfile, pstats
from pstats import SortKey

profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats(SortKey.CUMULATIVE)
stats.print_stats(10)  # Top 10 functions
stats.dump_stats("profile_output.prof")
```

```bash
python -m cProfile -o output.prof script.py
python -m pstats output.prof
```

### line_profiler — Line-by-Line

```bash
pip install line-profiler
kernprof -l -v script.py  # after adding @profile decorator
```

### memory_profiler — Memory Usage

```bash
pip install memory-profiler
python -m memory_profiler script.py  # after adding @profile decorator
```

### py-spy — Production Profiling

```bash
pip install py-spy
py-spy top --pid 12345
py-spy record -o profile.svg --pid 12345
py-spy record -o profile.svg -- python script.py
```

## Key Optimization Patterns

### List Comprehensions vs Loops

```python
# Slow
result = []
for i in range(n):
    result.append(i**2)

# Fast
result = [i**2 for i in range(n)]

# Even faster for simple ops
result = list(map(lambda x: x**2, range(n)))
```

### Generator Expressions for Memory

```python
# Memory-intensive
total = sum([i**2 for i in range(1_000_000)])

# Memory-efficient (constant memory)
total = sum(i**2 for i in range(1_000_000))
```

### String Concatenation

```python
# Slow — O(n²)
result = ""
for item in items:
    result += str(item)

# Fast
result = "".join(str(item) for item in items)
```

### Dict Lookups vs List Searches

```python
# O(n) — slow for large collections
target in items_list

# O(1) — fast
target in items_dict
target in items_set
```

### Local Variable Access

```python
# Access a module-level name inside a tight loop? Cache it locally first
local_fn = some_module.expensive_lookup
for i in range(100_000):
    local_fn(i)
```

### Caching with lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    return sum(range(n))
```

## Best Practices

1. **Profile before optimizing** — measure to find real bottlenecks
2. **Focus on hot paths** — optimize code that runs most frequently
3. **Use appropriate data structures** — dict/set for O(1) lookups
4. **Avoid premature optimization** — clarity first
5. **Use built-in functions** — implemented in C
6. **Cache expensive computations** — `lru_cache`, Redis, etc.
7. **Batch I/O operations** — Reduce system calls
8. **Use generators** for large datasets
9. **Consider NumPy** for numerical operations
10. **Profile production code** — use py-spy for live systems

## Common Pitfalls

- Optimizing without profiling first
- Using global variables in tight loops
- Creating unnecessary copies of data
- Not using connection pooling for databases
- Ignoring algorithmic complexity (O(n²) beats optimization micro-tricks)
- Over-optimizing rare code paths
- Not considering memory usage
