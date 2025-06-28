# Quantum-Enhanced Serverless Architecture - AWS Demo

This project demonstrates a quantum-enhanced serverless architecture using AWS services including Amazon Braket, designed with cost controls and monitoring.

## Architecture Overview

```
Internet → API Gateway → Lambda → Amazon Braket Simulator → Lambda → DynamoDB
                ↓               ↓
            CloudWatch      S3 (Results)
```

## Components

- **API Gateway**: RESTful API with restrictive rate limiting
- **Lambda Function**: Python-based quantum optimization using Braket SDK
- **Amazon Braket**: Quantum computing service (simulator only for cost control)
- **DynamoDB**: NoSQL database for storing optimization results and experiments
- **S3**: Storage for Braket quantum task results
- **CloudWatch**: Enhanced monitoring for quantum workloads

## ⚠️ IMPORTANT COST WARNINGS

This project involves quantum computing services that can incur significant costs:

- **Amazon Braket Simulator**: $0.075 per minute (SV1 simulator)
- **Lambda**: Increased memory (512MB) and timeout (15 minutes)
- **API Gateway**: Limited to 100 requests/month to control quantum usage
- **Cost Budget**: $20 alert threshold (quantum processing is expensive)

**ALWAYS monitor your AWS billing dashboard when using this project!**

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Python 3.11 (for local testing)
- Understanding of quantum computing concepts

## Quick Start

1. **Clone and setup:**
   ```bash
   cd quantum-serverless
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Update variables:**
   Edit `terraform.tfvars` and set your email for cost alerts:
   ```
   alert_email = "your-email@example.com"
   cost_alert_threshold = 20
   ```

3. **Deploy infrastructure:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Test the API:**
   ```bash
   # Get the API URL and key from outputs
   terraform output test_curl_command
   ```

## Usage

### API Endpoints

- **POST** `/optimize` - Solve traveling salesman problem using quantum algorithms

### Request Format

```json
{
  "cities": [[0,0], [1,1], [2,0], [1,2]],
  "algorithm": "qaoa",
  "shots": 1000,
  "max_iterations": 50
}
```

### Response Format

```json
{
  "id": "uuid",
  "experiment_id": "experiment-uuid",
  "algorithm": "qaoa",
  "cities_count": 4,
  "route": [0, 1, 3, 2, 0],
  "total_distance": 4.83,
  "execution_time_seconds": 45.2,
  "quantum_metadata": {
    "algorithm": "QAOA",
    "shots": 1000,
    "device_type": "simulator",
    "task_arn": "arn:aws:braket:...",
    "quantum_advantage": 0.15
  }
}
```

## Quantum Algorithms

1. **QAOA** (Quantum Approximate Optimization Algorithm): Good for combinatorial problems
2. **VQE** (Variational Quantum Eigensolver): Optimization with variational approach
3. **Classical Fallback**: Automatic fallback for large problem sizes

## Braket Integration

### Supported Devices

- **SV1 Simulator** (default): State vector simulator, up to 34 qubits
- **DM1 Simulator**: Density matrix simulator with noise modeling
- **TN1 Simulator**: Tensor network simulator for larger circuits

### Cost Control

- Uses simulator only (no real quantum hardware)
- Automatic fallback to classical for problems > 10 qubits
- API rate limiting to prevent excessive usage
- S3 lifecycle policies for result cleanup

## Monitoring & Observability

### CloudWatch Dashboard

Monitor quantum-specific metrics:
- Lambda execution times (quantum algorithms take longer)
- Braket task status and costs
- S3 storage for quantum results
- API usage patterns

### Cost Alerts

- Email alerts at 80% of $20 budget
- Forecasted cost alerts
- Tagged resource filtering for accurate tracking

### Experiment Tracking

- DynamoDB table for experiment metadata
- Track algorithm performance and quantum advantage
- TTL-based cleanup of old experiments

## Security & Permissions

### IAM Roles

- **Lambda Role**: Braket, DynamoDB, S3, CloudWatch access
- **Braket Service Role**: S3 access for result storage
- Least privilege principle applied

### Quantum-Specific Security

- Device ARN restrictions in environment variables
- S3 bucket encryption for quantum results
- No public access to quantum data

## Development & Testing

### Local Testing

```bash
cd lambda-src
pip install -r requirements.txt

# Test classical algorithm
python3 -c "
import quantum_optimizer
cities = [[0,0], [1,1], [2,0]]
result = quantum_optimizer.classical_fallback_tsp(cities)
print(f'Classical result: {result}')
"
```

### API Testing

```bash
# Test QAOA algorithm
curl -X POST 'https://your-api-id.execute-api.us-east-1.amazonaws.com/demo/optimize' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-api-key' \
  -d '{
    "cities": [[0,0], [1,1], [2,0], [1,2]], 
    "algorithm": "qaoa",
    "shots": 100
  }'

# Test VQE algorithm
curl -X POST 'https://your-api-id.execute-api.us-east-1.amazonaws.com/demo/optimize' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-api-key' \
  -d '{
    "cities": [[0,0], [1,1], [2,0]], 
    "algorithm": "vqe",
    "shots": 500,
    "max_iterations": 30
  }'
```

## Real Quantum Integration

To use actual quantum hardware (⚠️ **VERY EXPENSIVE**):

1. Update `braket_device_arn` in terraform.tfvars:
   ```
   # IonQ device (example)
   braket_device_arn = "arn:aws:braket:us-east-1::device/qpu/ionq/Harmony"
   
   # Rigetti device (example)  
   braket_device_arn = "arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-3"
   ```

2. Increase cost alert threshold significantly
3. Monitor billing closely

## Performance Comparison

Compare with classical implementation:
```bash
cd ../comparison-tests
python3 performance-comparison.py
```

## Terraform Workspaces

Use workspaces for different quantum experiments:

```bash
# Create quantum experiment workspace
terraform workspace new quantum-exp-1
terraform workspace select quantum-exp-1
terraform apply -var="max_quantum_qubits=6"

# Create larger experiment workspace
terraform workspace new quantum-exp-2  
terraform workspace select quantum-exp-2
terraform apply -var="max_quantum_qubits=12"
```

## Troubleshooting

### Common Issues

1. **Braket Service Quotas**: Check AWS service quotas for Braket
2. **Lambda Timeout**: Quantum algorithms may need longer timeouts
3. **Memory Issues**: Quantum simulators require more memory
4. **Cost Overruns**: Monitor Braket usage closely

### Quantum-Specific Issues

1. **Circuit Depth**: Too deep circuits may fail on NISQ devices
2. **Qubit Limits**: Simulator vs hardware qubit restrictions
3. **Calibration**: Real hardware requires recalibration periods

## Cleanup

⚠️ **CRITICAL**: Always destroy resources to avoid ongoing charges:

```bash
terraform destroy
```

Verify in AWS Console:
- All Lambda functions deleted
- S3 buckets emptied and deleted
- DynamoDB tables deleted
- Braket tasks cancelled

## Cost Optimization Tips

1. **Use Simulators**: Avoid real quantum hardware for development
2. **Limit Problem Size**: Keep qubit count low
3. **Batch Requests**: Combine multiple small problems
4. **Monitor Usage**: Set up comprehensive cost alerts
5. **Clean Up**: Delete S3 results regularly

## Educational Resources

- [Amazon Braket Documentation](https://docs.aws.amazon.com/braket/)
- [Quantum Computing Basics](https://qiskit.org/textbook/)
- [QAOA Tutorial](https://qiskit.org/documentation/tutorials/algorithms/01_qaoa.html)

## Next Steps

1. Compare performance with `../classical-serverless/`
2. Experiment with different quantum algorithms
3. Analyze quantum advantage metrics
4. Scale to larger optimization problems

## License

This is a demo project for educational purposes. Use at your own cost risk.
