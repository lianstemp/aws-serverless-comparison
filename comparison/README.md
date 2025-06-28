# AWS Serverless Comparison Tests

Performance comparison tools for Classical vs Quantum Serverless Architectures.

## Installation

```bash
poetry install
```

## Usage

### Test Classical API
```bash
poetry run test-classical
poetry run test-classical benchmark
```

### Test Quantum API  
```bash
poetry run test-quantum
poetry run test-quantum algorithms
poetry run test-quantum scaling
```

### Performance Comparison
```bash
poetry run performance-comparison
```

## Configuration

Copy `.env.example` to `.env` and fill in your API URLs and keys:

```bash
cp .env.example .env
```

Then edit `.env` with your actual values.
