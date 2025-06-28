#!/usr/bin/env python3
"""
Test script for Quantum-Enhanced Serverless Architecture
Tests the quantum traveling salesman optimization API
"""

import requests
import json
import time
import sys
from typing import List, Dict, Any

# Configuration - Update these with your actual values
API_URL = "https://your-quantum-api-id.execute-api.us-east-1.amazonaws.com/demo"
API_KEY = "your-quantum-api-key-here"

def test_quantum_api(cities: List[List[float]], algorithm: str = "qaoa", shots: int = 1000, max_iterations: int = 50) -> Dict[str, Any]:
    """Test the quantum optimization API."""
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
    
    payload = {
        'cities': cities,
        'algorithm': algorithm,
        'shots': shots,
        'max_iterations': max_iterations
    }
    
    try:
        print(f"Testing quantum API with {len(cities)} cities using {algorithm}...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/optimize",
            headers=headers,
            json=payload,
            timeout=300  # Longer timeout for quantum processing
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

def run_quantum_tests():
    """Run a suite of quantum optimization tests."""
    
    print("=" * 60)
    print("QUANTUM-ENHANCED SERVERLESS ARCHITECTURE TESTS")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            'name': 'QAOA Small (4 cities)',
            'cities': [[0, 0], [1, 1], [2, 0], [1, 2]],
            'algorithm': 'qaoa',
            'shots': 100,
            'max_iterations': 20
        },
        {
            'name': 'VQE Small (4 cities)', 
            'cities': [[0, 0], [1, 1], [2, 0], [1, 2]],
            'algorithm': 'vqe',
            'shots': 100,
            'max_iterations': 20
        },
        {
            'name': 'QAOA Medium (6 cities)',
            'cities': [[0, 0], [1, 1], [2, 0], [1, 2], [3, 1], [2, 3]],
            'algorithm': 'qaoa',
            'shots': 200,
            'max_iterations': 30
        },
        {
            'name': 'Classical Fallback (12 cities)',
            'cities': [
                [0, 0], [1, 1], [2, 0], [1, 2], [3, 1], [2, 3],
                [4, 2], [3, 4], [5, 3], [4, 5], [6, 4], [5, 6]
            ],
            'algorithm': 'qaoa',  # Should fallback to classical
            'shots': 100,
            'max_iterations': 20
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Cities: {len(test_case['cities'])} cities")
        print(f"Algorithm: {test_case['algorithm']}")
        print(f"Shots: {test_case['shots']}")
        
        result = test_quantum_api(
            test_case['cities'], 
            test_case['algorithm'],
            test_case['shots'],
            test_case['max_iterations']
        )
        
        if result:
            print(f"✓ Success!")
            print(f"  Actual algorithm used: {result['algorithm']}")
            print(f"  Route: {result['route']}")
            print(f"  Distance: {result['total_distance']:.3f}")
            print(f"  Execution time: {result['execution_time_seconds']:.3f}s")
            print(f"  API response time: {result['api_response_time']:.3f}s")
            
            # Print quantum metadata if available
            if 'quantum_metadata' in result and result['quantum_metadata']:
                metadata = result['quantum_metadata']
                print(f"  Quantum metadata:")
                print(f"    Device type: {metadata.get('device_type', 'N/A')}")
                print(f"    Shots: {metadata.get('shots', 'N/A')}")
                if 'quantum_advantage' in metadata:
                    print(f"    Quantum advantage: {metadata['quantum_advantage']:.3f}")
                if 'task_arn' in metadata:
                    print(f"    Task ARN: {metadata['task_arn']}")
            
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
        
        # Longer delay between quantum tests to avoid rate limiting
        time.sleep(5)
    
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
        
        # Separate quantum vs classical fallback results
        quantum_results = [r for r in successful_tests if r['result']['algorithm'] != 'classical_fallback']
        classical_results = [r for r in successful_tests if r['result']['algorithm'] == 'classical_fallback']
        
        if quantum_results:
            avg_quantum_time = sum(r['result']['execution_time_seconds'] for r in quantum_results) / len(quantum_results)
            avg_quantum_api_time = sum(r['result']['api_response_time'] for r in quantum_results) / len(quantum_results)
            print(f"  Quantum algorithms:")
            print(f"    Average execution time: {avg_quantum_time:.3f}s")
            print(f"    Average API response time: {avg_quantum_api_time:.3f}s")
        
        if classical_results:
            avg_classical_time = sum(r['result']['execution_time_seconds'] for r in classical_results) / len(classical_results)
            print(f"  Classical fallback:")
            print(f"    Average execution time: {avg_classical_time:.3f}s")
    
    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test['test_name']}")
    
    return results

def benchmark_quantum_algorithms():
    """Run performance benchmarks for different quantum algorithms."""
    
    print("\n" + "=" * 60)
    print("QUANTUM ALGORITHM COMPARISON")
    print("=" * 60)
    
    # Fixed test problem
    cities = [[0, 0], [1, 1], [2, 0], [1, 2], [3, 1]]
    
    algorithms = [
        {'name': 'QAOA', 'algorithm': 'qaoa', 'shots': 100},
        {'name': 'VQE', 'algorithm': 'vqe', 'shots': 100},
        {'name': 'Classical', 'algorithm': 'classical_fallback', 'shots': 1}
    ]
    
    for alg in algorithms:
        print(f"\nTesting {alg['name']} algorithm...")
        
        result = test_quantum_api(
            cities, 
            alg['algorithm'],
            alg['shots'],
            30
        )
        
        if result:
            print(f"  Distance: {result['total_distance']:.3f}")
            print(f"  Time: {result['execution_time_seconds']:.3f}s")
            print(f"  Algorithm used: {result['algorithm']}")
        else:
            print(f"  Failed!")

def test_quantum_scaling():
    """Test how quantum algorithms scale with problem size."""
    
    print("\n" + "=" * 60)
    print("QUANTUM SCALING TEST")
    print("=" * 60)
    
    city_counts = [4, 6, 8, 10]  # Limited by qubit constraints
    
    for count in city_counts:
        # Generate random cities
        import random
        random.seed(42)
        cities = [[random.random() * 10, random.random() * 10] for _ in range(count)]
        
        print(f"\nTesting {count} cities with QAOA...")
        
        result = test_quantum_api(cities, 'qaoa', shots=50, max_iterations=20)
        
        if result:
            print(f"  Algorithm used: {result['algorithm']}")
            print(f"  Distance: {result['total_distance']:.3f}")
            print(f"  Time: {result['execution_time_seconds']:.3f}s")
            
            if result['algorithm'] == 'classical_fallback':
                print(f"  ⚠️  Fell back to classical (too many cities for quantum)")
        else:
            print(f"  Failed!")
        
        # Longer delay for scaling tests
        time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "algorithms":
            benchmark_quantum_algorithms()
        elif sys.argv[1] == "scaling":
            test_quantum_scaling()
        else:
            print("Usage: python test-quantum.py [algorithms|scaling]")
    else:
        run_quantum_tests()
        benchmark_quantum_algorithms()
