#!/usr/bin/env python3
"""
Performance Profiling and Benchmarking Tool

Provides CPU profiling, memory profiling, and benchmarking capabilities
for identifying performance bottlenecks in Python code.
"""

import cProfile
import pstats
import io
import argparse
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import tracemalloc


class PerformanceProfiler:
    """Performance profiling and analysis tool."""

    def __init__(self, output_dir: str = "perf_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}

    def profile_cpu(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile CPU usage using cProfile.

        Args:
            func: Function to profile
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Dictionary containing profiling results
        """
        print("[+] Profiling CPU usage...")

        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        profiler.disable()

        # Save stats to file
        stats_file = self.output_dir / "cpu_profile.stats"
        profiler.dump_stats(str(stats_file))

        # Generate human-readable report
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.strip_dirs()
        ps.sort_stats('cumulative')
        ps.print_stats(50)  # Top 50 functions

        report = s.getvalue()

        # Save report
        report_file = self.output_dir / "cpu_profile.txt"
        with open(report_file, 'w') as f:
            f.write(report)

        # Extract top hotspots
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.strip_dirs()
        ps.sort_stats('cumulative')

        hotspots = []
        for func_info in ps.stats.items()[:10]:
            filename, line, func_name = func_info[0]
            cumtime = func_info[1][3]
            ncalls = func_info[1][0]

            hotspots.append({
                "function": func_name,
                "file": filename,
                "line": line,
                "cumulative_time": round(cumtime, 4),
                "calls": ncalls
            })

        execution_time = end_time - start_time

        print(f"  Execution time: {execution_time:.4f}s")
        print(f"  Results saved to: {report_file}")

        return {
            "execution_time": round(execution_time, 4),
            "hotspots": hotspots,
            "profile_file": str(stats_file),
            "report_file": str(report_file)
        }

    def profile_memory(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile memory usage using tracemalloc.

        Args:
            func: Function to profile
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Dictionary containing memory profiling results
        """
        print("[+] Profiling memory usage...")

        tracemalloc.start()

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        # Get top memory consumers
        top_stats = snapshot.statistics('lineno')

        memory_hotspots = []
        for stat in top_stats[:10]:
            memory_hotspots.append({
                "file": stat.traceback.format()[0] if stat.traceback else "unknown",
                "size_mb": round(stat.size / 1024 / 1024, 4),
                "count": stat.count
            })

        # Save report
        report_file = self.output_dir / "memory_profile.txt"
        with open(report_file, 'w') as f:
            f.write(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB\n")
            f.write(f"Current memory usage: {current / 1024 / 1024:.2f} MB\n\n")
            f.write("Top 10 memory consumers:\n")
            for i, stat in enumerate(top_stats[:10], 1):
                f.write(f"\n#{i}: {stat.traceback.format()[0] if stat.traceback else 'unknown'}\n")
                f.write(f"  Size: {stat.size / 1024 / 1024:.2f} MB\n")
                f.write(f"  Count: {stat.count}\n")

        execution_time = end_time - start_time

        print(f"  Peak memory: {peak / 1024 / 1024:.2f} MB")
        print(f"  Execution time: {execution_time:.4f}s")
        print(f"  Results saved to: {report_file}")

        return {
            "execution_time": round(execution_time, 4),
            "peak_memory_mb": round(peak / 1024 / 1024, 2),
            "current_memory_mb": round(current / 1024 / 1024, 2),
            "memory_hotspots": memory_hotspots,
            "report_file": str(report_file)
        }

    def benchmark(self, func: Callable, iterations: int = 100, *args, **kwargs) -> Dict[str, Any]:
        """
        Benchmark function performance over multiple iterations.

        Args:
            func: Function to benchmark
            iterations: Number of iterations to run
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Dictionary containing benchmark results
        """
        print(f"[+] Benchmarking function ({iterations} iterations)...")

        times = []

        for i in range(iterations):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)

        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        # Calculate percentiles
        sorted_times = sorted(times)
        p50 = sorted_times[len(sorted_times) // 2]
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]

        # Save report
        report_file = self.output_dir / "benchmark.txt"
        with open(report_file, 'w') as f:
            f.write(f"Benchmark Results ({iterations} iterations)\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Average time:  {avg_time*1000:.4f} ms\n")
            f.write(f"Minimum time:  {min_time*1000:.4f} ms\n")
            f.write(f"Maximum time:  {max_time*1000:.4f} ms\n")
            f.write(f"Median (p50):  {p50*1000:.4f} ms\n")
            f.write(f"p95:           {p95*1000:.4f} ms\n")
            f.write(f"p99:           {p99*1000:.4f} ms\n")
            f.write(f"\nThroughput:    {1/avg_time:.2f} ops/sec\n")

        print(f"  Average: {avg_time*1000:.4f} ms")
        print(f"  p95: {p95*1000:.4f} ms")
        print(f"  Throughput: {1/avg_time:.2f} ops/sec")
        print(f"  Results saved to: {report_file}")

        return {
            "iterations": iterations,
            "avg_time_ms": round(avg_time * 1000, 4),
            "min_time_ms": round(min_time * 1000, 4),
            "max_time_ms": round(max_time * 1000, 4),
            "p50_ms": round(p50 * 1000, 4),
            "p95_ms": round(p95 * 1000, 4),
            "p99_ms": round(p99 * 1000, 4),
            "throughput_ops_sec": round(1 / avg_time, 2),
            "report_file": str(report_file)
        }

    def profile_script(self, script_path: str) -> Dict[str, Any]:
        """
        Profile a Python script file.

        Args:
            script_path: Path to Python script to profile

        Returns:
            Dictionary containing profiling results
        """
        print(f"[+] Profiling script: {script_path}")

        script_path = Path(script_path)
        if not script_path.exists():
            return {"error": f"Script not found: {script_path}"}

        # Read script
        with open(script_path) as f:
            code = f.read()

        # Compile code
        try:
            compiled = compile(code, str(script_path), 'exec')
        except SyntaxError as e:
            return {"error": f"Syntax error in script: {e}"}

        # Profile execution
        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.time()
        try:
            exec(compiled, {"__name__": "__main__"})
        except Exception as e:
            profiler.disable()
            return {"error": f"Script execution failed: {e}"}

        end_time = time.time()
        profiler.disable()

        # Save stats
        stats_file = self.output_dir / f"{script_path.stem}_profile.stats"
        profiler.dump_stats(str(stats_file))

        # Generate report
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.strip_dirs()
        ps.sort_stats('cumulative')
        ps.print_stats(50)

        report_file = self.output_dir / f"{script_path.stem}_profile.txt"
        with open(report_file, 'w') as f:
            f.write(s.getvalue())

        execution_time = end_time - start_time

        print(f"  Execution time: {execution_time:.4f}s")
        print(f"  Results saved to: {report_file}")

        return {
            "script": str(script_path),
            "execution_time": round(execution_time, 4),
            "profile_file": str(stats_file),
            "report_file": str(report_file)
        }

    def save_results(self, filename: str = "performance_results.json"):
        """Save all results to JSON file."""
        output_file = self.output_dir / filename
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nAll results saved to: {output_file}")


def example_function():
    """Example function for demonstration."""
    # Simulate some work
    total = 0
    for i in range(1000000):
        total += i
    return total


def main():
    parser = argparse.ArgumentParser(
        description="Performance profiling and benchmarking tool"
    )
    parser.add_argument(
        "--script",
        help="Path to Python script to profile"
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Run CPU profiling on example function"
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Run memory profiling on example function"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark on example function"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
        help="Number of benchmark iterations (default: 100)"
    )
    parser.add_argument(
        "-o", "--output",
        default="perf_results",
        help="Output directory (default: perf_results)"
    )

    args = parser.parse_args()

    profiler = PerformanceProfiler(args.output)

    if args.script:
        profiler.results["script_profile"] = profiler.profile_script(args.script)
    elif args.cpu:
        profiler.results["cpu"] = profiler.profile_cpu(example_function)
    elif args.memory:
        profiler.results["memory"] = profiler.profile_memory(example_function)
    elif args.benchmark:
        profiler.results["benchmark"] = profiler.benchmark(example_function, args.iterations)
    else:
        print("No profiling mode selected. Use --help for usage information.")
        print("\nRunning all profiles on example function...")
        profiler.results["cpu"] = profiler.profile_cpu(example_function)
        profiler.results["memory"] = profiler.profile_memory(example_function)
        profiler.results["benchmark"] = profiler.benchmark(example_function, args.iterations)

    profiler.save_results()


if __name__ == "__main__":
    main()
