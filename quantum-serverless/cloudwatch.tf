# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/demo-quantum-optimizer-${random_string.suffix.result}"
  retention_in_days = 7  # Free tier: 5GB, 7 days retention

  tags = {
    Name = "demo-quantum-lambda-logs-${random_string.suffix.result}"
  }
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/demo-quantum-api-${random_string.suffix.result}"
  retention_in_days = 7

  tags = {
    Name = "demo-quantum-api-logs-${random_string.suffix.result}"
  }
}

# SNS Topic for cost alerts
resource "aws_sns_topic" "cost_alerts" {
  name = "demo-quantum-cost-alerts-${random_string.suffix.result}"

  tags = {
    Name = "demo-quantum-cost-alerts-${random_string.suffix.result}"
  }
}

# SNS Topic Subscription
resource "aws_sns_topic_subscription" "cost_alerts_email" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Cost Budget with alerts (higher threshold for quantum)
resource "aws_budgets_budget" "cost_alert" {
  name         = "demo-quantum-budget-${random_string.suffix.result}"
  budget_type  = "COST"
  limit_amount = tostring(var.cost_alert_threshold)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  time_period_start = "2024-01-01_00:00"

  cost_filter {
    name   = "TagKeyValue"
    values = ["Project$quantum"]
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
    Name = "demo-quantum-budget-${random_string.suffix.result}"
  }
}

# CloudWatch Dashboard for Quantum Metrics
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "demo-quantum-dashboard-${random_string.suffix.result}"

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
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.quantum_optimizer.function_name],
            [".", "Errors", ".", "."],
            [".", "Duration", ".", "."],
            [".", "Throttles", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Quantum Lambda Metrics"
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
          title   = "Quantum API Gateway Metrics"
          period  = 300
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 12
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/S3", "BucketSizeBytes", "BucketName", aws_s3_bucket.braket_results.bucket, "StorageType", "StandardStorage"],
            [".", "NumberOfObjects", ".", ".", ".", "AllStorageTypes"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Braket S3 Storage Metrics"
          period  = 86400
        }
      }
    ]
  })
}

# CloudWatch Alarm for high Lambda duration (quantum processing can be long)
resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "demo-quantum-lambda-duration-${random_string.suffix.result}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Average"
  threshold           = "600000"  # 10 minutes in milliseconds
  alarm_description   = "This metric monitors quantum lambda duration"
  alarm_actions       = [aws_sns_topic.cost_alerts.arn]

  dimensions = {
    FunctionName = aws_lambda_function.quantum_optimizer.function_name
  }

  tags = {
    Name = "demo-quantum-lambda-duration-alarm-${random_string.suffix.result}"
  }
}
