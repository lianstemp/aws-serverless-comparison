output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}"
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.quantum_optimizer.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.quantum_optimizer.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.results.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.results.arn
}

output "braket_s3_bucket" {
  description = "S3 bucket for Braket results"
  value       = aws_s3_bucket.braket_results.bucket
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "cost_budget_name" {
  description = "Name of the cost budget"
  value       = aws_budgets_budget.cost_alert.name
}

output "api_key_id" {
  description = "ID of the API key"
  value       = aws_api_gateway_api_key.main.id
  sensitive   = true
}

output "braket_device_arn" {
  description = "ARN of the Braket device being used"
  value       = var.braket_device_arn
}

output "test_curl_command" {
  description = "Sample curl command to test the API"
  value = format(
    "curl -X POST '%s/optimize' -H 'Content-Type: application/json' -H 'x-api-key: %s' -d '{\"cities\": [[0,0], [1,1], [2,0], [1,2]], \"algorithm\": \"qaoa\"}'",
    "https://${aws_api_gateway_rest_api.main.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}",
    aws_api_gateway_api_key.main.value
  )
  sensitive = true
}
