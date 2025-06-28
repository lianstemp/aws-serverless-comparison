import json
import boto3
import uuid
import time
import logging
import os
import asyncio
from typing import List, Tuple, Dict, Any, Optional
from decimal import Decimal
import numpy as np

# Configure logging
logger = logging.getLogger()
logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
braket = boto3.client('braket')
s3 = boto3.client('s3')

# Environment variables
table_name = os.getenv('DYNAMODB_TABLE')
experiments_table_name = table_name.replace('results', 'experiments')
braket_device_arn = os.getenv('BRAKET_DEVICE_ARN')
s3_bucket = os.getenv('BRAKET_S3_BUCKET')
max_qubits = int(os.getenv('MAX_QUBITS', '10'))

# Initialize tables
results_table = dynamodb.Table(table_name)
experiments_table = dynamodb.Table(experiments_table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for quantum traveling salesman optimization.
    
    Expected input:
    {
        "cities": [[x1, y1], [x2, y2], ...],
        "algorithm": "qaoa" | "vqe" | "classical_fallback",
        "shots": 1000 (optional),
        "max_iterations": 100 (optional)
    }
    """
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        cities = body.get('cities', [])
        algorithm = body.get('algorithm', 'qaoa')
        shots = body.get('shots', 1000)
        max_iterations = body.get('max_iterations', 50)
        
        if not cities or len(cities) < 2:
            return error_response(400, 'At least 2 cities are required', len(cities))
        
        if len(cities) > max_qubits:
            logger.warning(f"Too many cities ({len(cities)}) for quantum algorithm, falling back to classical")
            algorithm = 'classical_fallback'
        
        # Start timing
        start_time = time.time()
        experiment_id = str(uuid.uuid4())
        
        # Log experiment start
        log_experiment(experiment_id, 'STARTED', algorithm, len(cities))
        
        # Solve the traveling salesman problem
        try:
            if algorithm == 'qaoa':
                solution = qaoa_tsp(cities, shots, max_iterations, experiment_id)
            elif algorithm == 'vqe':
                solution = vqe_tsp(cities, shots, max_iterations, experiment_id)
            elif algorithm == 'classical_fallback':
                solution = classical_fallback_tsp(cities)
            else:
                solution = qaoa_tsp(cities, shots, max_iterations, experiment_id)  # Default to QAOA
            
            log_experiment(experiment_id, 'COMPLETED', algorithm, len(cities))
            
        except Exception as e:
            logger.error(f"Algorithm execution failed: {str(e)}")
            log_experiment(experiment_id, 'FAILED', algorithm, len(cities))
            # Fallback to classical algorithm
            solution = classical_fallback_tsp(cities)
            algorithm = 'classical_fallback'
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Prepare result
        result = {
            'id': str(uuid.uuid4()),
            'experiment_id': experiment_id,
            'algorithm': algorithm,
            'cities_count': len(cities),
            'route': solution['route'],
            'total_distance': float(solution['distance']),
            'execution_time_seconds': execution_time,
            'timestamp': int(time.time()),
            'cities': cities,
            'quantum_metadata': solution.get('quantum_metadata', {}),
            'device_arn': braket_device_arn if algorithm != 'classical_fallback' else None
        }
        
        # Store result in DynamoDB
        store_result(result)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return error_response(500, 'Internal server error', str(e))

def qaoa_tsp(cities: List[List[float]], shots: int, max_iterations: int, experiment_id: str) -> Dict[str, Any]:
    """
    Solve TSP using Quantum Approximate Optimization Algorithm (QAOA).
    
    Note: This is a simplified implementation for demonstration.
    In a real scenario, you would use Braket SDK with proper quantum circuits.
    """
    try:
        # For demo purposes, we'll simulate quantum computation
        # In a real implementation, you would:
        # 1. Convert TSP to QUBO (Quadratic Unconstrained Binary Optimization)
        # 2. Create QAOA circuit with proper ansatz
        # 3. Submit to Braket quantum device/simulator
        
        logger.info(f"Starting QAOA optimization for {len(cities)} cities")
        
        # Simulate quantum task submission
        task_metadata = simulate_braket_task(experiment_id, 'QAOA', shots)
        
        # For now, use classical algorithm with quantum-inspired randomness
        solution = quantum_inspired_tsp(cities, shots)
        
        # Add quantum metadata
        solution['quantum_metadata'] = {
            'algorithm': 'QAOA',
            'shots': shots,
            'max_iterations': max_iterations,
            'task_arn': task_metadata.get('task_arn'),
            'device_type': 'simulator',
            'quantum_advantage': calculate_quantum_advantage(solution, cities)
        }
        
        return solution
        
    except Exception as e:
        logger.error(f"QAOA algorithm failed: {str(e)}")
        raise

def vqe_tsp(cities: List[List[float]], shots: int, max_iterations: int, experiment_id: str) -> Dict[str, Any]:
    """
    Solve TSP using Variational Quantum Eigensolver (VQE).
    """
    try:
        logger.info(f"Starting VQE optimization for {len(cities)} cities")
        
        # Simulate quantum task submission
        task_metadata = simulate_braket_task(experiment_id, 'VQE', shots)
        
        # For now, use classical algorithm with quantum-inspired optimization
        solution = quantum_inspired_tsp(cities, shots)
        
        # Add quantum metadata
        solution['quantum_metadata'] = {
            'algorithm': 'VQE',
            'shots': shots,
            'max_iterations': max_iterations,
            'task_arn': task_metadata.get('task_arn'),
            'device_type': 'simulator',
            'convergence_info': {
                'iterations': np.random.randint(10, max_iterations),
                'final_energy': float(solution['distance']) * -1  # Negative energy minimization
            }
        }
        
        return solution
        
    except Exception as e:
        logger.error(f"VQE algorithm failed: {str(e)}")
        raise

def classical_fallback_tsp(cities: List[List[float]]) -> Dict[str, Any]:
    """
    Classical traveling salesman algorithm as fallback.
    """
    return nearest_neighbor_tsp(cities)

def quantum_inspired_tsp(cities: List[List[float]], shots: int) -> Dict[str, Any]:
    """
    Classical algorithm with quantum-inspired randomization.
    """
    best_solution = None
    best_distance = float('inf')
    
    # Run multiple iterations to simulate quantum sampling
    iterations = min(shots // 100, 50)  # Don't run too many iterations
    
    for _ in range(iterations):
        # Add quantum-inspired randomness to starting city
        start_city = np.random.randint(0, len(cities))
        solution = nearest_neighbor_tsp_from_start(cities, start_city)
        
        if solution['distance'] < best_distance:
            best_distance = solution['distance']
            best_solution = solution
    
    return best_solution

def nearest_neighbor_tsp(cities: List[List[float]]) -> Dict[str, Any]:
    """Standard nearest neighbor TSP algorithm."""
    return nearest_neighbor_tsp_from_start(cities, 0)

def nearest_neighbor_tsp_from_start(cities: List[List[float]], start_city: int) -> Dict[str, Any]:
    """Nearest neighbor TSP starting from a specific city."""
    if not cities:
        return {'route': [], 'distance': 0}
    
    n = len(cities)
    unvisited = set(range(n))
    unvisited.remove(start_city)
    route = [start_city]
    total_distance = 0
    
    current_city = start_city
    
    while unvisited:
        nearest_city = min(unvisited, 
                         key=lambda city: calculate_distance(cities[current_city], cities[city]))
        
        total_distance += calculate_distance(cities[current_city], cities[nearest_city])
        route.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
    
    # Return to starting city
    total_distance += calculate_distance(cities[current_city], cities[start_city])
    route.append(start_city)
    
    return {
        'route': route,
        'distance': total_distance
    }

def calculate_distance(city1: List[float], city2: List[float]) -> float:
    """Calculate Euclidean distance between two cities."""
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5

def simulate_braket_task(experiment_id: str, algorithm: str, shots: int) -> Dict[str, Any]:
    """
    Simulate Braket quantum task submission.
    In a real implementation, this would submit actual quantum circuits.
    """
    task_arn = f"arn:aws:braket:us-east-1:123456789012:quantum-task/{experiment_id}"
    
    # Simulate task metadata
    metadata = {
        'task_arn': task_arn,
        'device_arn': braket_device_arn,
        'algorithm': algorithm,
        'shots': shots,
        'status': 'COMPLETED',
        'created_at': time.time()
    }
    
    logger.info(f"Simulated Braket task: {task_arn}")
    return metadata

def calculate_quantum_advantage(solution: Dict[str, Any], cities: List[List[float]]) -> float:
    """
    Calculate a simulated quantum advantage metric.
    In real scenarios, this would compare quantum vs classical performance.
    """
    # Simulate quantum advantage as a percentage improvement
    # This is just for demonstration - real quantum advantage is problem-dependent
    classical_baseline = len(cities) * 0.1  # Simulated classical algorithm overhead
    quantum_speedup = max(0.1, classical_baseline - len(cities) * 0.05)
    return quantum_speedup / classical_baseline

def log_experiment(experiment_id: str, status: str, algorithm: str, cities_count: int):
    """Log experiment metadata to DynamoDB."""
    try:
        experiments_table.put_item(
            Item={
                'experiment_id': experiment_id,
                'status': status,
                'algorithm': algorithm,
                'cities_count': cities_count,
                'timestamp': int(time.time()),
                'ttl': int(time.time() + 86400 * 30)  # 30 days TTL
            }
        )
    except Exception as e:
        logger.error(f"Failed to log experiment: {str(e)}")

def store_result(result: Dict[str, Any]):
    """Store optimization result in DynamoDB."""
    try:
        # Convert floats to Decimal for DynamoDB
        dynamodb_item = {
            'id': result['id'],
            'experiment_id': result['experiment_id'],
            'algorithm': result['algorithm'],
            'cities_count': result['cities_count'],
            'route': result['route'],
            'total_distance': Decimal(str(result['total_distance'])),
            'execution_time_seconds': Decimal(str(result['execution_time_seconds'])),
            'timestamp': result['timestamp'],
            'cities': result['cities'],
            'quantum_metadata': result['quantum_metadata'],
            'device_arn': result['device_arn']
        }
        
        results_table.put_item(Item=dynamodb_item)
        logger.info(f"Stored result with ID: {result['id']}")
        
    except Exception as e:
        logger.error(f"Failed to store result in DynamoDB: {str(e)}")
        raise

def error_response(status_code: int, error: str, details: Any = None) -> Dict[str, Any]:
    """Generate error response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': error,
            'details': details
        })
    }
