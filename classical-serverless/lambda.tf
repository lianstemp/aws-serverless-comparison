# Lambda function for classical traveling salesman optimization
resource "aws_lambda_function" "classical_optimizer" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "demo-classical-optimizer-${random_string.suffix.result}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "classical-optimizer.lambda_handler"
  runtime         = "python3.11"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.results.name
      LOG_LEVEL      = "INFO"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.lambda_logs,
  ]

  tags = {
    Name = "demo-classical-optimizer-${random_string.suffix.result}"
  }
}

# Create ZIP file for Lambda deployment
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda-src/classical-optimizer.py"
  output_path = "${path.module}/classical-optimizer.zip"
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.classical_optimizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}
