# IAM role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "demo-quantum-lambda-role-${random_string.suffix.result}"

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
    Name = "demo-quantum-lambda-role-${random_string.suffix.result}"
  }
}

# IAM policy for Lambda to write to CloudWatch Logs
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM policy for Lambda to access DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "demo-quantum-lambda-dynamodb-policy-${random_string.suffix.result}"
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
          aws_dynamodb_table.experiments.arn,
          "${aws_dynamodb_table.experiments.arn}/index/*"
        ]
      }
    ]
  })
}

# IAM policy for Lambda to access Amazon Braket
resource "aws_iam_role_policy" "lambda_braket" {
  name = "demo-quantum-lambda-braket-policy-${random_string.suffix.result}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "braket:GetQuantumTask",
          "braket:CreateQuantumTask",
          "braket:CancelQuantumTask",
          "braket:SearchQuantumTasks",
          "braket:GetDevice",
          "braket:SearchDevices"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM policy for Lambda to access S3 bucket for Braket results
resource "aws_iam_role_policy" "lambda_s3" {
  name = "demo-quantum-lambda-s3-policy-${random_string.suffix.result}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.braket_results.arn,
          "${aws_s3_bucket.braket_results.arn}/*"
        ]
      }
    ]
  })
}

# IAM role for Braket service
resource "aws_iam_role" "braket_service_role" {
  name = "demo-quantum-braket-service-role-${random_string.suffix.result}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "braket.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "demo-quantum-braket-service-role-${random_string.suffix.result}"
  }
}

# IAM policy for Braket to access S3
resource "aws_iam_role_policy" "braket_s3" {
  name = "demo-quantum-braket-s3-policy-${random_string.suffix.result}"
  role = aws_iam_role.braket_service_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.braket_results.arn,
          "${aws_s3_bucket.braket_results.arn}/*"
        ]
      }
    ]
  })
}

# IAM role for cost budgets
resource "aws_iam_role" "budget_role" {
  name = "demo-quantum-budget-role-${random_string.suffix.result}"

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
    Name = "demo-quantum-budget-role-${random_string.suffix.result}"
  }
}

# IAM policy for budget notifications
resource "aws_iam_role_policy" "budget_policy" {
  name = "demo-quantum-budget-policy-${random_string.suffix.result}"
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
