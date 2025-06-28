# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/demo-classical-optimizer-${random_string.suffix.result}"
  retention_in_days = 7  # Free tier: 5GB, 7 days retention

  tags = {
    Name = "demo-classical-lambda-logs-${random_string.suffix.result}"
  }
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/demo-classical-api-${random_string.suffix.result}"
  retention_in_days = 7

  tags = {
    Name = "demo-classical-api-logs-${random_string.suffix.result}"
  }
}

# SNS Topic for cost alerts
resource "aws_sns_topic" "cost_alerts" {
  name = "demo-classical-cost-alerts-${random_string.suffix.result}"

  tags = {
    Name = "demo-classical-cost-alerts-${random_string.suffix.result}"
  }
}

# SNS Topic Subscription
resource "aws_sns_topic_subscription" "cost_alerts_email" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Cost Budget with alerts
resource "aws_budgets_budget" "cost_alert" {
  name         = "demo-classical-budget-${random_string.suffix.result}"
  budget_type  = "COST"
  limit_amount = tostring(var.cost_alert_threshold)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  time_period_start = "2024-01-01_00:00"

  cost_filter {
    name   = "TagKeyValue"
    values = ["Project$classical"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 100
    threshold_type            = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }

  tags = {
    Name = "demo-classical-budget-${random_string.suffix.result}"
  }
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "demo-classical-dashboard-${random_string.suffix.result}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.classical_optimizer.function_name],
            [".", "Errors", ".", "."],
            [".", "Duration", ".", "."],
            [".", "Throttles", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Lambda Metrics"
          period  = 300
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/ApiGateway", "Count", "ApiName", aws_api_gateway_rest_api.main.name],
            [".", "Latency", ".", "."],
            [".", "4XXError", ".", "."],
            [".", "5XXError", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "API Gateway Metrics"
          period  = 300
        }
      }
    ]
  })
}
