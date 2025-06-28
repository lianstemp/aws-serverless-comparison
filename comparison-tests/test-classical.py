#!/usr/bin/env python3
"""
Test script for Classical Serverless Architecture
Tests the traveling salesman optimization API
"""

import requests
import json
import time
import sys
from typing import List, Dict, Any

# Configuration - Update these with your actual values
API_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/demo"
API_KEY = "your-api-key-here"

def test_classical_api(cities: List[List[float]], algorithm: str = "nearest_neighbor") -> Dict[str, Any]:
    """Test the classical optimization API."""
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
    
    payload = {
        'cities': cities,
        'algorithm': algorithm
    }
    
    try:
        print(f"Testing classical API with {len(cities)} cities...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/optimize",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            result['api_response_time'] = end_time - start_time
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def run_classical_tests():
    """Run a suite of classical optimization tests."""
    
    print("=" * 60)
    print("CLASSICAL SERVERLESS ARCHITECTURE TESTS")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            'name': 'Small TSP (4 cities)',
            'cities': [[0, 0], [1, 1], [2, 0], [1, 2]],
            'algorithm': 'nearest_neighbor'
        },
        {
            'name': 'Medium TSP (6 cities)', 
            'cities': [[0, 0], [1, 1], [2, 0], [1, 2], [3, 1], [2, 3]],
            'algorithm': 'nearest_neighbor'
        },
        {
            'name': 'Brute Force (5 cities)',
            'cities': [[0, 0], [1, 0], [2, 0], [1, 1], [1, -1]],
            'algorithm': 'brute_force'
        },
        {
            'name': 'Large TSP (10 cities)',
            'cities': [
                [0, 0], [1, 1], [2, 0], [1, 2], [3, 1],
                [2, 3], [4, 2], [3, 4], [5, 3], [4, 5]
            ],
            'algorithm': 'nearest_neighbor'
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Cities: {test_case['cities']}")
        print(f"Algorithm: {test_case['algorithm']}")
        
        result = test_classical_api(test_case['cities'], test_case['algorithm'])
        
        if result:
            print(f"✓ Success!")
            print(f"  Route: {result['route']}")
            print(f"  Distance: {result['total_distance']:.3f}")
            print(f"  Execution time: {result['execution_time_seconds']:.3f}s")
            print(f"  API response time: {result['api_response_time']:.3f}s")
            
            results.append({
                'test_name': test_case['name'],
                'success': True,
                'result': result
            })
        else:
            print(f"✗ Failed!")
            results.append({
                'test_name': test_case['name'],
                'success': False,
                'result': None
            })
        
        # Small delay between tests
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if successful_tests:
        print("\nPerformance Metrics:")
        avg_exec_time = sum(r['result']['execution_time_seconds'] for r in successful_tests) / len(successful_tests)
        avg_api_time = sum(r['result']['api_response_time'] for r in successful_tests) / len(successful_tests)
        
        print(f"  Average execution time: {avg_exec_time:.3f}s")
        print(f"  Average API response time: {avg_api_time:.3f}s")
    
    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test['test_name']}")
    
    return results

def benchmark_classical():
    """Run performance benchmarks."""
    
    print("\n" + "=" * 60)
    print("CLASSICAL PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    # Benchmark with increasing city counts
    city_counts = [4, 6, 8, 10, 12]
    
    for count in city_counts:
        # Generate random cities in a unit square
        import random
        random.seed(42)  # Reproducible results
        cities = [[random.random(), random.random()] for _ in range(count)]
        
        print(f"\nBenchmarking {count} cities...")
        
        result = test_classical_api(cities, 'nearest_neighbor')
        
        if result:
            print(f"  Distance: {result['total_distance']:.3f}")
            print(f"  Time: {result['execution_time_seconds']:.3f}s")
        else:
            print(f"  Failed!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "benchmark":
            benchmark_classical()
        else:
            print("Usage: python test-classical.py [benchmark]")
    else:
        run_classical_tests()
        benchmark_classical()
