# Lambda function for quantum traveling salesman optimization
resource "aws_lambda_function" "quantum_optimizer" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "demo-quantum-optimizer-${random_string.suffix.result}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "quantum-optimizer.lambda_handler"
  runtime         = "python3.11"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE      = aws_dynamodb_table.results.name
      BRAKET_DEVICE_ARN   = var.braket_device_arn
      BRAKET_S3_BUCKET    = aws_s3_bucket.braket_results.bucket
      MAX_QUBITS         = var.max_quantum_qubits
      LOG_LEVEL          = "INFO"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.lambda_logs,
  ]

  tags = {
    Name = "demo-quantum-optimizer-${random_string.suffix.result}"
  }
}

# Create ZIP file for Lambda deployment
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda-src"
  output_path = "${path.module}/quantum-optimizer.zip"
  excludes    = ["__pycache__", "*.pyc"]
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.quantum_optimizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

# Lambda Layer for quantum dependencies
resource "aws_lambda_layer_version" "quantum_deps" {
  filename         = data.archive_file.layer_zip.output_path
  layer_name       = "demo-quantum-deps-${random_string.suffix.result}"
  description      = "Quantum computing dependencies for Braket"
  
  compatible_runtimes = ["python3.11"]
  
  source_code_hash = data.archive_file.layer_zip.output_base64sha256
}

# Create layer ZIP with dependencies
data "archive_file" "layer_zip" {
  type        = "zip"
  output_path = "${path.module}/quantum-layer.zip"
  
  source {
    content = templatefile("${path.module}/lambda-src/requirements.txt", {})
    filename = "requirements.txt"
  }
}
