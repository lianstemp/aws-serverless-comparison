import json
import boto3
import uuid
import time
import logging
import os
from typing import List, Tuple, Dict, Any
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for classical traveling salesman optimization.
    
    Expected input:
    {
        "cities": [[x1, y1], [x2, y2], ...],
        "algorithm": "nearest_neighbor" (optional, default)
    }
    """
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        cities = body.get('cities', [])
        algorithm = body.get('algorithm', 'nearest_neighbor')
        
        if not cities or len(cities) < 2:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'At least 2 cities are required',
                    'cities_provided': len(cities)
                })
            }
        
        # Start timing
        start_time = time.time()
        
        # Solve the traveling salesman problem
        if algorithm == 'nearest_neighbor':
            solution = nearest_neighbor_tsp(cities)
        elif algorithm == 'brute_force' and len(cities) <= 8:
            solution = brute_force_tsp(cities)
        else:
            solution = nearest_neighbor_tsp(cities)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Prepare result
        result = {
            'id': str(uuid.uuid4()),
            'algorithm': algorithm,
            'cities_count': len(cities),
            'route': solution['route'],
            'total_distance': float(solution['distance']),
            'execution_time_seconds': execution_time,
            'timestamp': int(time.time()),
            'cities': cities
        }
        
        # Store result in DynamoDB
        try:
            # Convert floats to Decimal for DynamoDB
            dynamodb_item = {
                'id': result['id'],
                'algorithm': result['algorithm'],
                'cities_count': result['cities_count'],
                'route': result['route'],
                'total_distance': Decimal(str(result['total_distance'])),
                'execution_time_seconds': Decimal(str(result['execution_time_seconds'])),
                'timestamp': result['timestamp'],
                'cities': result['cities']
            }
            
            table.put_item(Item=dynamodb_item)
            logger.info(f"Stored result with ID: {result['id']}")
            
        except Exception as e:
            logger.error(f"Failed to store result in DynamoDB: {str(e)}")
            # Continue without failing the request
        
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
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def calculate_distance(city1: List[float], city2: List[float]) -> float:
    """Calculate Euclidean distance between two cities."""
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5

def nearest_neighbor_tsp(cities: List[List[float]]) -> Dict[str, Any]:
    """
    Solve TSP using nearest neighbor heuristic.
    Time complexity: O(n^2)
    """
    if not cities:
        return {'route': [], 'distance': 0}
    
    n = len(cities)
    unvisited = set(range(1, n))
    route = [0]  # Start at city 0
    total_distance = 0
    
    current_city = 0
    
    while unvisited:
        nearest_city = min(unvisited, 
                         key=lambda city: calculate_distance(cities[current_city], cities[city]))
        
        total_distance += calculate_distance(cities[current_city], cities[nearest_city])
        route.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
    
    # Return to starting city
    total_distance += calculate_distance(cities[current_city], cities[0])
    route.append(0)
    
    return {
        'route': route,
        'distance': total_distance
    }

def brute_force_tsp(cities: List[List[float]]) -> Dict[str, Any]:
    """
    Solve TSP using brute force (only for small instances).
    Time complexity: O(n!)
    """
    from itertools import permutations
    
    if len(cities) <= 1:
        return {'route': list(range(len(cities))), 'distance': 0}
    
    n = len(cities)
    min_distance = float('inf')
    best_route = None
    
    # Try all permutations starting from city 0
    for perm in permutations(range(1, n)):
        route = [0] + list(perm) + [0]
        distance = sum(calculate_distance(cities[route[i]], cities[route[i+1]]) 
                      for i in range(len(route)-1))
        
        if distance < min_distance:
            min_distance = distance
            best_route = route
    
    return {
        'route': best_route,
        'distance': min_distance
    }
