# AWS Serverless Architecture Comparison: Classical vs Quantum

This repository contains two complete Terraform projects demonstrating the evolution from classical to quantum-enhanced serverless architectures on AWS, designed for educational comparison and cost-controlled experimentation.

## 🏗️ Project Structure

```
AWSSUMMIT/
├── classical-serverless/          # Classical serverless implementation
│   ├── main.tf                   # Core Terraform configuration
│   ├── variables.tf              # Input variables
│   ├── outputs.tf                # Output values
│   ├── lambda.tf                 # Lambda function configuration
│   ├── api-gateway.tf            # API Gateway setup
│   ├── dynamodb.tf               # DynamoDB tables
│   ├── iam.tf                    # IAM roles and policies
│   ├── cloudwatch.tf             # Monitoring and cost alerts
│   ├── terraform.tfvars.example  # Example variables
│   ├── lambda-src/
│   │   └── classical-optimizer.py # Classical TSP optimization
│   └── README.md                 # Classical architecture guide
│
├── quantum-serverless/           # Quantum-enhanced serverless implementation
│   ├── main.tf                   # Core Terraform configuration
│   ├── variables.tf              # Input variables (quantum-specific)
│   ├── outputs.tf                # Output values
│   ├── lambda.tf                 # Lambda with quantum dependencies
│   ├── api-gateway.tf            # API Gateway setup
│   ├── dynamodb.tf               # Enhanced DynamoDB schema
│   ├── braket.tf                 # Amazon Braket integration
│   ├── iam.tf                    # Extended IAM for Braket
│   ├── cloudwatch.tf             # Quantum-aware monitoring
│   ├── terraform.tfvars.example  # Example quantum variables
│   ├── lambda-src/
│   │   ├── quantum-optimizer.py  # Quantum TSP optimization
│   │   └── requirements.txt      # Quantum dependencies
│   └── README.md                 # Quantum architecture guide
│
├── comparison-tests/             # Performance comparison tools
│   ├── test-classical.py         # Classical API testing
│   ├── test-quantum.py           # Quantum API testing
│   └── performance-comparison.py # Comprehensive comparison
│
└── README.md                     # This file
```

## 🎯 Architecture Comparison

### Classical Serverless Architecture
- **API Gateway** → **Lambda** → **DynamoDB**
- Traditional optimization algorithms
- Optimized for cost and speed
- Free tier friendly ($5 budget)

### Quantum-Enhanced Serverless Architecture  
- **API Gateway** → **Lambda** → **Amazon Braket** → **Lambda** → **DynamoDB**
- Quantum optimization algorithms (QAOA, VQE)
- Higher computational capabilities
- Controlled costs ($20 budget)

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Terraform >= 1.0
- Python 3.11
- Understanding of quantum computing (for quantum project)

### Deploy Classical Architecture

```bash
cd classical-serverless
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your email
terraform init
terraform apply
```

### Deploy Quantum Architecture

```bash
cd quantum-serverless
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your email and settings
terraform init
terraform apply
```

### Run Comparisons

```bash
cd comparison-tests
# Update API URLs and keys in test files
python3 test-classical.py
python3 test-quantum.py
python3 performance-comparison.py
```

## 💡 Key Differences

| Aspect | Classical | Quantum-Enhanced |
|--------|-----------|------------------|
| **Algorithms** | Nearest Neighbor, Brute Force | QAOA, VQE, Classical Fallback |
| **Lambda Memory** | 128MB | 512MB |
| **Lambda Timeout** | 3 seconds | 15 minutes |
| **Cost Budget** | $5/month | $20/month |
| **API Limits** | 1000 requests/month | 100 requests/month |
| **Dependencies** | Standard libraries | Quantum computing libraries |
| **Use Case** | Production-ready | Research and experimentation |

## 🧪 Optimization Algorithms

### Classical Algorithms
1. **Nearest Neighbor**: O(n²) greedy heuristic
2. **Brute Force**: O(n!) exact solution (≤8 cities)

### Quantum Algorithms
1. **QAOA**: Quantum Approximate Optimization Algorithm
2. **VQE**: Variational Quantum Eigensolver  
3. **Classical Fallback**: Automatic fallback for large problems

## 💰 Cost Analysis

### Classical Architecture (per 1000 requests)
- **Lambda**: ~$0.002
- **API Gateway**: ~$0.0035
- **DynamoDB**: ~$0.001 (free tier)
- **Total**: ~$0.007

### Quantum Architecture (per 1000 requests)
- **Lambda**: ~$0.008 (4x memory)
- **API Gateway**: ~$0.0035
- **Braket Simulator**: ~$1.25 (1 minute average)
- **DynamoDB**: ~$0.001
- **S3**: ~$0.001
- **Total**: ~$1.26 (180x higher)

## 📊 Performance Expectations

### Classical Performance
- **Execution Time**: 0.001-0.1 seconds
- **Scalability**: Handles 20+ cities efficiently
- **Solution Quality**: Good heuristic solutions
- **Reliability**: 99.9% success rate

### Quantum Performance  
- **Execution Time**: 10-300 seconds (simulator)
- **Scalability**: Limited to ~10 qubits currently
- **Solution Quality**: Potentially optimal for some problems
- **Reliability**: 90-95% (quantum noise, fallbacks)

## 🔬 Educational Value

This comparison demonstrates:

1. **Quantum Computing Integration**: Real-world quantum cloud services
2. **Cost Management**: Quantum computing cost considerations
3. **Algorithm Comparison**: Classical vs quantum optimization
4. **Serverless Evolution**: How architectures adapt for new technologies
5. **Practical Limitations**: Current quantum computing constraints

## ⚠️ Important Warnings

### Cost Management
- **Monitor AWS billing closely** when using quantum services
- Set up budget alerts and spending limits
- Use simulators only for learning (avoid real quantum hardware)
- Consider AWS Free Tier limitations

### Technical Limitations
- Quantum advantage is problem-dependent
- Current quantum computers are noisy (NISQ era)
- Simulator limitations vs real quantum hardware
- Network latency affects quantum task submission

### Security Considerations
- API keys and quantum algorithms may be sensitive
- Quantum computations could be visible in logs
- Consider data encryption for quantum results

## 🎓 Learning Path

1. **Start with Classical**: Deploy and understand classical architecture
2. **Study Quantum Basics**: Learn QAOA and VQE concepts
3. **Deploy Quantum**: Set up quantum-enhanced architecture
4. **Run Comparisons**: Use provided test scripts
5. **Experiment**: Try different algorithms and problem sizes
6. **Analyze Results**: Compare performance and costs

## 🛠️ Customization

### Adding New Algorithms
- Extend Lambda functions with new optimization methods
- Update API schemas for additional parameters
- Add monitoring for new algorithm metrics

### Scaling Considerations
- Use Step Functions for complex quantum workflows
- Consider SQS for quantum task queuing
- Implement caching for expensive quantum computations

### Production Adaptations
- Add authentication beyond API keys
- Implement proper error handling and retries
- Set up multi-region deployments
- Add comprehensive logging and alerting

## 🤝 Contributing

This is an educational project. Suggested improvements:
- Additional quantum algorithms
- Better cost optimization strategies
- Enhanced monitoring dashboards
- More comprehensive test suites

## 📚 Resources

### AWS Documentation
- [Amazon Braket](https://docs.aws.amazon.com/braket/)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [AWS API Gateway](https://docs.aws.amazon.com/apigateway/)

### Quantum Computing
- [Qiskit Textbook](https://qiskit.org/textbook/)
- [QAOA Tutorial](https://qiskit.org/documentation/tutorials/algorithms/01_qaoa.html)
- [Quantum Optimization](https://arxiv.org/abs/1411.4028)

### Serverless Architecture
- [Serverless Patterns](https://serverlessland.com/patterns)
- [AWS Well-Architected Serverless](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/)

## 🧹 Cleanup

Always destroy resources after experimentation:

```bash
# Destroy quantum architecture first (higher costs)
cd quantum-serverless
terraform destroy

# Then destroy classical architecture
cd ../classical-serverless  
terraform destroy

# Verify in AWS Console that all resources are deleted
```

## 📄 License

This project is for educational purposes. Use at your own risk and cost.

---

**Remember**: Quantum computing is still experimental. Use these projects for learning and research, not production workloads. Always monitor your AWS costs when experimenting with quantum services.
