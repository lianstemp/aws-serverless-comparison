# Classical Serverless Architecture

This project implements a classical serverless architecture using AWS services, designed to stay within the AWS Free Tier limits.

## Architecture Overview

```
Internet → API Gateway → Lambda → DynamoDB
                ↓
            CloudWatch Logs
```

## Components

- **API Gateway**: RESTful API with rate limiting and API key authentication
- **Lambda Function**: Python-based traveling salesman optimization
- **DynamoDB**: NoSQL database for storing optimization results
- **CloudWatch**: Logging and monitoring
- **Cost Budgets**: Alerts for cost management

## Free Tier Considerations

⚠️ **COST WARNING**: This project is designed for AWS Free Tier but monitor your usage:

- **API Gateway**: 1M requests/month (limited to 1000/month in usage plan)
- **Lambda**: 1M requests/month, 400k GB-seconds compute time
- **DynamoDB**: 25GB storage, 25 RCU/WCU
- **CloudWatch**: 5GB logs, 10 custom metrics
- **Cost Budget**: $5 alert threshold

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Python 3.11 (for local testing)

## Quick Start

1. **Clone and setup:**
   ```bash
   cd classical-serverless
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Update variables:**
   Edit `terraform.tfvars` and set your email for cost alerts:
   ```
   alert_email = "your-email@example.com"
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

- **POST** `/optimize` - Solve traveling salesman problem

### Request Format

```json
{
  "cities": [[0,0], [1,1], [2,0], [1,2]],
  "algorithm": "nearest_neighbor"
}
```

### Response Format

```json
{
  "id": "uuid",
  "algorithm": "nearest_neighbor",
  "cities_count": 4,
  "route": [0, 1, 3, 2, 0],
  "total_distance": 4.83,
  "execution_time_seconds": 0.001,
  "timestamp": 1640995200
}
```

## Algorithms

1. **Nearest Neighbor** (default): O(n²) heuristic algorithm
2. **Brute Force**: O(n!) exact algorithm (only for ≤8 cities)

## Monitoring

- **CloudWatch Dashboard**: Monitor Lambda and API Gateway metrics
- **Cost Alerts**: Email notifications at 80% and 100% of $5 budget
- **Logs**: Lambda execution logs with 7-day retention

## Terraform Workspaces

Use workspaces for environment isolation:

```bash
# Create development workspace
terraform workspace new dev
terraform workspace select dev
terraform apply

# Create staging workspace  
terraform workspace new staging
terraform workspace select staging
terraform apply
```

## Security Features

- API key authentication required
- IAM roles with least privilege access
- VPC endpoints (optional - uncomment in main.tf)
- DynamoDB encryption at rest

## Cost Optimization

- On-demand DynamoDB billing
- Minimal Lambda memory (128MB)
- Short Lambda timeout (3 seconds)
- Log retention limited to 7 days
- Usage plan limits API calls

## Cleanup

⚠️ **IMPORTANT**: Always destroy resources to avoid charges:

```bash
terraform destroy
```

Confirm all resources are deleted in AWS Console.

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure AWS credentials have sufficient permissions
2. **Resource Limits**: Check AWS service quotas in your region
3. **Cost Alerts**: Verify email subscription in SNS

### Terraform State

- State is stored locally in `terraform.tfstate`
- For production, use remote state (S3 + DynamoDB)
- Use workspaces for environment separation

## Development

### Local Testing

```bash
cd lambda-src
python3 -m pip install boto3
python3 -c "
import classical_optimizer
result = classical_optimizer.nearest_neighbor_tsp([[0,0], [1,1], [2,0]])
print(result)
"
```

### API Testing

```bash
# Using curl (replace with your API URL and key)
curl -X POST 'https://your-api-id.execute-api.us-east-1.amazonaws.com/demo/optimize' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: your-api-key' \
  -d '{"cities": [[0,0], [1,1], [2,0], [1,2]]}'
```

## Next Steps

Compare this classical implementation with the quantum-enhanced version in `../quantum-serverless/`

## License

This is a demo project for educational purposes.
