# API Gateway REST API
resource "aws_api_gateway_rest_api" "main" {
  name        = "demo-classical-api-${random_string.suffix.result}"
  description = "Classical Serverless Optimization API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "demo-classical-api-${random_string.suffix.result}"
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "optimize" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "optimize"
}

# API Gateway Method
resource "aws_api_gateway_method" "optimize_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.optimize.id
  http_method   = "POST"
  authorization = "NONE"
  api_key_required = true
}

# API Gateway Integration
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.optimize.id
  http_method = aws_api_gateway_method.optimize_post.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.classical_optimizer.invoke_arn
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_method.optimize_post,
    aws_api_gateway_integration.lambda_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.optimize.id,
      aws_api_gateway_method.optimize_post.id,
      aws_api_gateway_integration.lambda_integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway Stage
resource "aws_api_gateway_stage" "main" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "demo"

  tags = {
    Name = "demo-classical-stage-${random_string.suffix.result}"
  }
}

# API Gateway Usage Plan
resource "aws_api_gateway_usage_plan" "main" {
  name         = "demo-classical-usage-plan-${random_string.suffix.result}"
  description  = "Usage plan for classical serverless API"

  api_stages {
    api_id = aws_api_gateway_rest_api.main.id
    stage  = aws_api_gateway_stage.main.stage_name
  }

  quota_settings {
    limit  = var.api_quota_limit
    period = "MONTH"
  }

  throttle_settings {
    rate_limit  = var.api_throttle_rate
    burst_limit = var.api_throttle_burst
  }

  tags = {
    Name = "demo-classical-usage-plan-${random_string.suffix.result}"
  }
}

# API Gateway API Key
resource "aws_api_gateway_api_key" "main" {
  name        = "demo-classical-api-key-${random_string.suffix.result}"
  description = "API key for classical serverless optimization"

  tags = {
    Name = "demo-classical-api-key-${random_string.suffix.result}"
  }
}

# API Gateway Usage Plan Key
resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.main.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.main.id
}

# Method Response
resource "aws_api_gateway_method_response" "optimize_200" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.optimize.id
  http_method = aws_api_gateway_method.optimize_post.http_method
  status_code = "200"
}

# Integration Response
resource "aws_api_gateway_integration_response" "optimize_200" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.optimize.id
  http_method = aws_api_gateway_method.optimize_post.http_method
  status_code = aws_api_gateway_method_response.optimize_200.status_code

  depends_on = [aws_api_gateway_integration.lambda_integration]
}
