# IAM role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "demo-classical-lambda-role-${random_string.suffix.result}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "demo-classical-lambda-role-${random_string.suffix.result}"
  }
}

# IAM policy for Lambda to write to CloudWatch Logs
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM policy for Lambda to access DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "demo-classical-lambda-dynamodb-policy-${random_string.suffix.result}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.results.arn,
          "${aws_dynamodb_table.results.arn}/index/*",
          aws_dynamodb_table.api_usage.arn,
          "${aws_dynamodb_table.api_usage.arn}/index/*"
        ]
      }
    ]
  })
}

# IAM role for cost budgets
resource "aws_iam_role" "budget_role" {
  name = "demo-classical-budget-role-${random_string.suffix.result}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "budgets.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "demo-classical-budget-role-${random_string.suffix.result}"
  }
}

# IAM policy for budget notifications
resource "aws_iam_role_policy" "budget_policy" {
  name = "demo-classical-budget-policy-${random_string.suffix.result}"
  role = aws_iam_role.budget_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.cost_alerts.arn
      }
    ]
  })
}
