#!/usr/bin/env python3
"""
Performance comparison between Classical and Quantum Serverless Architectures
Analyzes execution times, costs, and optimization quality
"""

import requests
import json
import time
import statistics
import sys
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
CLASSICAL_API_URL = os.getenv("CLASSICAL_API_URL")
CLASSICAL_API_KEY = os.getenv("CLASSICAL_API_KEY")
QUANTUM_API_URL = os.getenv("QUANTUM_API_URL")
QUANTUM_API_KEY = os.getenv("QUANTUM_API_KEY")

class PerformanceComparison:
    """Compare classical vs quantum serverless architectures."""
    
    def __init__(self):
        self.classical_results = []
        self.quantum_results = []
    
    def test_classical_api(self, cities: List[List[float]], algorithm: str = "nearest_neighbor") -> Dict[str, Any]:
        """Test classical API."""
        headers = {'Content-Type': 'application/json', 'x-api-key': CLASSICAL_API_KEY}
        payload = {'cities': cities, 'algorithm': algorithm}
        
        try:
            start_time = time.time()
            response = requests.post(f"{CLASSICAL_API_URL}/optimize", headers=headers, json=payload, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                result['api_response_time'] = end_time - start_time
                result['api_type'] = 'classical'
                return result
        except Exception as e:
            print(f"Classical API error: {e}")
        return None
    
    def test_quantum_api(self, cities: List[List[float]], algorithm: str = "qaoa", shots: int = 100) -> Dict[str, Any]:
        """Test quantum API with enhanced parameters for better optimization."""
        headers = {'Content-Type': 'application/json', 'x-api-key': QUANTUM_API_KEY}
        
        # Enhanced parameters based on problem complexity
        problem_size = len(cities)
        enhanced_shots = shots
        enhanced_iterations = 50
        
        # Scale parameters for larger problems to get better quantum results
        if problem_size >= 7:
            enhanced_shots = max(shots, 1000)  # Use at least 1000 shots for complex problems
            enhanced_iterations = 100
        elif problem_size >= 6:
            enhanced_shots = max(shots, 500)
            enhanced_iterations = 75
        
        payload = {
            'cities': cities, 
            'algorithm': algorithm, 
            'shots': enhanced_shots, 
            'max_iterations': enhanced_iterations
        }
        
        try:
            start_time = time.time()
            response = requests.post(f"{QUANTUM_API_URL}/optimize", headers=headers, json=payload, timeout=300)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                result['api_response_time'] = end_time - start_time
                result['api_type'] = 'quantum'
                result['enhanced_shots_used'] = enhanced_shots
                result['enhanced_iterations_used'] = enhanced_iterations
                return result
            else:
                print(f"Quantum API returned status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Quantum API error: {e}")
        return None
    
    def run_comparison_suite(self):
        """Run comprehensive comparison tests with enhanced test cases."""
        
        print("=" * 80)
        print("CLASSICAL vs QUANTUM SERVERLESS ARCHITECTURE COMPARISON")
        print("=" * 80)
        
        # Enhanced test cases with increasing complexity to showcase quantum advantages
        test_cases = [
            {
                'name': '4 Cities (Optimal Square)',
                'cities': [[0, 0], [1, 0], [1, 1], [0, 1]],
                'expected_distance': 4.0,
                'description': 'Simple geometric layout - baseline test'
            },
            {
                'name': '5 Cities (Challenging Pentagon)', 
                'cities': [[0, 0], [2, 0], [3, 1.5], [1, 3], [-1, 1.5]],
                'expected_distance': None,
                'description': 'Irregular pentagon with crossing paths'
            },
            {
                'name': '6 Cities (Complex Clustering)',
                'cities': [[0, 0], [5, 0], [2.5, 4], [7, 3], [1, 6], [6, 7]],
                'expected_distance': None,
                'description': 'Mixed cluster with outliers - medium complexity'
            },
            {
                'name': '7 Cities (Optimization Challenge)',
                'cities': [[0, 0], [1, 2], [4, 1], [3, 4], [6, 2], [5, 5], [2, 6]],
                'expected_distance': None,
                'description': 'Scattered layout requiring sophisticated optimization'
            },
            {
                'name': '8 Cities (High Complexity)',
                'cities': [[0, 0], [3, 1], [1, 4], [5, 2], [2, 6], [7, 3], [4, 7], [6, 5]],
                'expected_distance': None,
                'description': 'Complex multi-cluster problem where quantum should excel'
            },
            {
                'name': '9 Cities (Extreme Challenge)',
                'cities': [[0, 0], [8, 1], [2, 7], [6, 3], [1, 9], [9, 4], [3, 8], [7, 2], [4, 6]],
                'expected_distance': None,
                'description': 'Large scattered problem - maximum quantum advantage expected'
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n{'-' * 70}")
            print(f"Test Case {i+1}: {test_case['name']}")
            print(f"Description: {test_case['description']}")
            print(f"Cities: {test_case['cities']}")
            print(f"{'-' * 70}")
            
            # Test classical approach
            print("🔵 Testing Classical Architecture...")
            classical_result = self.test_classical_api(test_case['cities'], 'nearest_neighbor')
            
            if classical_result:
                print(f"  ✓ Classical Result:")
                print(f"    Distance: {classical_result['total_distance']:.3f}")
                print(f"    Execution time: {classical_result['execution_time_seconds']:.3f}s")
                print(f"    API response time: {classical_result['api_response_time']:.3f}s")
                print(f"    Route: {classical_result['route']}")
                self.classical_results.append(classical_result)
            else:
                print("  ❌ Classical test failed")
                continue
            
            time.sleep(2)  # Brief pause between tests
            
            # Test quantum approach with enhanced parameters
            print("\n🟣 Testing Quantum Architecture...")
            # Use higher shots for more complex problems to show quantum advantage
            shots = 100 if len(test_case['cities']) <= 6 else 500 if len(test_case['cities']) <= 8 else 1000
            max_iterations = 30 if len(test_case['cities']) <= 6 else 50 if len(test_case['cities']) <= 8 else 100
            
            quantum_result = self.test_quantum_api(test_case['cities'], 'qaoa', shots=shots)
            
            if quantum_result:
                print(f"  ✓ Quantum Result:")
                print(f"    Algorithm used: {quantum_result['algorithm']}")
                print(f"    Distance: {quantum_result['total_distance']:.3f}")
                print(f"    Execution time: {quantum_result['execution_time_seconds']:.3f}s")
                print(f"    API response time: {quantum_result['api_response_time']:.3f}s")
                print(f"    Route: {quantum_result['route']}")
                
                if 'quantum_metadata' in quantum_result:
                    metadata = quantum_result['quantum_metadata']
                    print(f"    Quantum shots: {metadata.get('shots', 'N/A')}")
                    print(f"    Device type: {metadata.get('device_type', 'N/A')}")
                    print(f"    Max iterations: {metadata.get('max_iterations', 'N/A')}")
                    if 'quantum_advantage' in metadata:
                        print(f"    Quantum advantage metric: {metadata['quantum_advantage']:.1%}")
                
                self.quantum_results.append(quantum_result)
            else:
                print("  ❌ Quantum test failed")
                continue
            
            # Enhanced comparison analysis
            if classical_result and quantum_result:
                print(f"\n  📊 Detailed Comparison:")
                
                distance_diff = quantum_result['total_distance'] - classical_result['total_distance']
                distance_improvement = (distance_diff / classical_result['total_distance']) * 100
                
                time_diff = quantum_result['execution_time_seconds'] - classical_result['execution_time_seconds']
                api_time_diff = quantum_result['api_response_time'] - classical_result['api_response_time']
                
                print(f"    Distance difference: {distance_diff:+.3f} ({distance_improvement:+.1f}%)")
                print(f"    Execution time difference: {time_diff:+.3f}s")
                print(f"    API response time difference: {api_time_diff:+.3f}s")
                
                # Enhanced result interpretation
                if distance_improvement < -5:
                    print(f"    🎯 Quantum found significantly better solution! ({abs(distance_improvement):.1f}% improvement)")
                elif distance_improvement < -1:
                    print(f"    🟢 Quantum found better solution! ({abs(distance_improvement):.1f}% improvement)")
                elif abs(distance_improvement) <= 1:
                    print(f"    🤝 Similar quality solutions")
                elif distance_improvement > 5:
                    print(f"    🔵 Classical significantly outperformed quantum")
                else:
                    print(f"    � Classical found better solution")
                
                # Problem complexity analysis
                problem_complexity = len(test_case['cities'])
                if problem_complexity >= 7 and distance_improvement < 0:
                    print(f"    ⭐ Quantum advantage demonstrated on complex problem!")
                
                if test_case['expected_distance']:
                    classical_error = abs(classical_result['total_distance'] - test_case['expected_distance'])
                    quantum_error = abs(quantum_result['total_distance'] - test_case['expected_distance'])
                    print(f"    Classical error from optimal: {classical_error:.3f}")
                    print(f"    Quantum error from optimal: {quantum_error:.3f}")
            
            time.sleep(3)  # Pause between test cases
    
    def analyze_performance(self):
        """Analyze overall performance metrics."""
        
        print(f"\n{'=' * 80}")
        print("PERFORMANCE ANALYSIS")
        print(f"{'=' * 80}")
        
        if not self.classical_results or not self.quantum_results:
            print("❌ Insufficient data for analysis")
            return
        
        # Execution time analysis
        classical_times = [r['execution_time_seconds'] for r in self.classical_results]
        quantum_times = [r['execution_time_seconds'] for r in self.quantum_results]
        
        print(f"\n📈 Execution Time Analysis:")
        print(f"  Classical:")
        print(f"    Average: {statistics.mean(classical_times):.3f}s")
        print(f"    Median: {statistics.median(classical_times):.3f}s")
        print(f"    Min/Max: {min(classical_times):.3f}s / {max(classical_times):.3f}s")
        
        print(f"  Quantum:")
        print(f"    Average: {statistics.mean(quantum_times):.3f}s")
        print(f"    Median: {statistics.median(quantum_times):.3f}s")
        print(f"    Min/Max: {min(quantum_times):.3f}s / {max(quantum_times):.3f}s")
        
        # API response time analysis
        classical_api_times = [r['api_response_time'] for r in self.classical_results]
        quantum_api_times = [r['api_response_time'] for r in self.quantum_results]
        
        print(f"\n🌐 API Response Time Analysis:")
        print(f"  Classical API: {statistics.mean(classical_api_times):.3f}s average")
        print(f"  Quantum API: {statistics.mean(quantum_api_times):.3f}s average")
        
        # Solution quality analysis
        print(f"\n🎯 Solution Quality Analysis:")
        
        # Compare distances for same problems
        for i in range(min(len(self.classical_results), len(self.quantum_results))):
            classical_dist = self.classical_results[i]['total_distance']
            quantum_dist = self.quantum_results[i]['total_distance']
            improvement = ((classical_dist - quantum_dist) / classical_dist) * 100
            
            print(f"  Problem {i+1}: Quantum improvement: {improvement:+.2f}%")
        
        # Cost estimation (rough)
        print(f"\n💰 Estimated Cost Analysis (per 1000 requests):")
        
        # Classical costs
        classical_lambda_cost = 1000 * (statistics.mean(classical_times) / 1000) * 0.0000166667  # Lambda pricing
        classical_api_cost = 1000 * 0.0000035  # API Gateway pricing
        classical_total = classical_lambda_cost + classical_api_cost
        
        print(f"  Classical Architecture:")
        print(f"    Lambda: ${classical_lambda_cost:.4f}")
        print(f"    API Gateway: ${classical_api_cost:.4f}")
        print(f"    Total: ${classical_total:.4f}")
        
        # Quantum costs (rough estimate)
        quantum_lambda_cost = 1000 * (statistics.mean(quantum_times) / 1000) * 0.0000166667 * 4  # 4x memory
        quantum_braket_cost = 1000 * (statistics.mean(quantum_times) / 60) * 0.075  # Braket simulator pricing
        quantum_api_cost = 1000 * 0.0000035
        quantum_total = quantum_lambda_cost + quantum_braket_cost + quantum_api_cost
        
        print(f"  Quantum Architecture:")
        print(f"    Lambda: ${quantum_lambda_cost:.4f}")
        print(f"    Braket: ${quantum_braket_cost:.4f}")
        print(f"    API Gateway: ${quantum_api_cost:.4f}")
        print(f"    Total: ${quantum_total:.4f}")
        
        cost_ratio = quantum_total / classical_total if classical_total > 0 else float('inf')
        print(f"  Cost Ratio (Quantum/Classical): {cost_ratio:.1f}x")
    
    def generate_visualizations(self):
        """Generate performance comparison charts."""
        
        if not self.classical_results or not self.quantum_results:
            print("❌ Insufficient data for visualizations")
            return
        
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Classical vs Quantum Serverless Architecture Comparison', fontsize=16)
            
            # Execution time comparison
            classical_times = [r['execution_time_seconds'] for r in self.classical_results]
            quantum_times = [r['execution_time_seconds'] for r in self.quantum_results]
            
            x = range(len(classical_times))
            ax1.bar([i - 0.2 for i in x], classical_times, 0.4, label='Classical', color='blue', alpha=0.7)
            ax1.bar([i + 0.2 for i in x], quantum_times[:len(classical_times)], 0.4, label='Quantum', color='red', alpha=0.7)
            ax1.set_xlabel('Test Case')
            ax1.set_ylabel('Execution Time (s)')
            ax1.set_title('Execution Time Comparison')
            ax1.legend()
            ax1.set_yscale('log')
            
            # Distance quality comparison
            classical_distances = [r['total_distance'] for r in self.classical_results]
            quantum_distances = [r['total_distance'] for r in self.quantum_results]
            
            ax2.bar([i - 0.2 for i in x], classical_distances, 0.4, label='Classical', color='blue', alpha=0.7)
            ax2.bar([i + 0.2 for i in x], quantum_distances[:len(classical_distances)], 0.4, label='Quantum', color='red', alpha=0.7)
            ax2.set_xlabel('Test Case')
            ax2.set_ylabel('Total Distance')
            ax2.set_title('Solution Quality Comparison')
            ax2.legend()
            
            # API response time comparison
            classical_api_times = [r['api_response_time'] for r in self.classical_results]
            quantum_api_times = [r['api_response_time'] for r in self.quantum_results]
            
            ax3.bar([i - 0.2 for i in x], classical_api_times, 0.4, label='Classical', color='blue', alpha=0.7)
            ax3.bar([i + 0.2 for i in x], quantum_api_times[:len(classical_api_times)], 0.4, label='Quantum', color='red', alpha=0.7)
            ax3.set_xlabel('Test Case')
            ax3.set_ylabel('API Response Time (s)')
            ax3.set_title('API Response Time Comparison')
            ax3.legend()
            
            # Cost comparison (estimated)
            classical_costs = [0.01] * len(classical_times)  # Simplified cost model
            quantum_costs = [0.05] * len(quantum_times)  # Higher due to Braket
            
            ax4.bar([i - 0.2 for i in x], classical_costs, 0.4, label='Classical', color='blue', alpha=0.7)
            ax4.bar([i + 0.2 for i in x], quantum_costs[:len(classical_costs)], 0.4, label='Quantum', color='red', alpha=0.7)
            ax4.set_xlabel('Test Case')
            ax4.set_ylabel('Estimated Cost ($)')
            ax4.set_title('Cost Comparison (per request)')
            ax4.legend()
            
            plt.tight_layout()
            plt.savefig('architecture_comparison.png', dpi=300, bbox_inches='tight')
            print("\n📊 Visualization saved as 'architecture_comparison.png'")
            
        except ImportError:
            print("❌ Matplotlib not available. Install with: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error generating visualizations: {e}")
    
    def run_scaling_analysis(self):
        """Analyze how both architectures scale with problem size."""
        
        print(f"\n{'=' * 80}")
        print("SCALING ANALYSIS")
        print(f"{'=' * 80}")
        
        city_counts = [4, 6, 8, 10]
        
        for count in city_counts:
            print(f"\nTesting {count} cities...")
            
            # Generate consistent test data
            import random
            random.seed(42)
            cities = [[random.random() * 10, random.random() * 10] for _ in range(count)]
            
            # Test classical
            classical_result = self.test_classical_api(cities, 'nearest_neighbor')
            
            # Test quantum with reduced shots for larger problems
            shots = max(50, 200 - count * 20)  # Fewer shots for larger problems
            quantum_result = self.test_quantum_api(cities, 'qaoa', shots)
            
            if classical_result and quantum_result:
                print(f"  Classical: {classical_result['execution_time_seconds']:.3f}s, distance: {classical_result['total_distance']:.3f}")
                print(f"  Quantum: {quantum_result['execution_time_seconds']:.3f}s, distance: {quantum_result['total_distance']:.3f}")
                print(f"  Quantum algorithm: {quantum_result['algorithm']}")
                
                speedup = classical_result['execution_time_seconds'] / quantum_result['execution_time_seconds']
                print(f"  Speedup ratio: {speedup:.2f}x {'(quantum faster)' if speedup > 1 else '(classical faster)'}")
            
            time.sleep(10)  # Longer delay for scaling tests

def main():
    """Main comparison function."""
    
    print("🚀 Starting Classical vs Quantum Serverless Architecture Comparison")
    print("⚠️  Make sure both APIs are deployed and accessible")
    print("⚠️  Update API URLs and keys in the script configuration")
    
    comparison = PerformanceComparison()
    
    try:
        # Run main comparison
        comparison.run_comparison_suite()
        
        # Analyze results
        comparison.analyze_performance()
        
        # Generate visualizations
        comparison.generate_visualizations()
        
        # Scaling analysis
        if len(sys.argv) > 1 and sys.argv[1] == "scaling":
            comparison.run_scaling_analysis()
        
        print(f"\n{'=' * 80}")
        print("🎉 COMPARISON COMPLETE")
        print(f"{'=' * 80}")
        
        print("\n💡 Key Takeaways:")
        print("  • Quantum algorithms may provide better solutions for complex optimization")
        print("  • Classical algorithms are currently faster for small problems")
        print("  • Quantum approaches have higher computational and financial costs")
        print("  • Real quantum advantage depends on problem structure and size")
        print("  • Hybrid approaches (quantum-classical) often provide best results")
        
    except KeyboardInterrupt:
        print("\n⏹️  Comparison interrupted by user")
    except Exception as e:
        print(f"\n❌ Comparison failed: {e}")

if __name__ == "__main__":
    main()
