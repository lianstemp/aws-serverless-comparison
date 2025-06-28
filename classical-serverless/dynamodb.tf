# DynamoDB table for storing optimization results
resource "aws_dynamodb_table" "results" {
  name           = "demo-classical-results-${random_string.suffix.result}"
  billing_mode   = "ON_DEMAND"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  global_secondary_index {
    name               = "timestamp-index"
    hash_key           = "timestamp"
    projection_type    = "ALL"
  }

  point_in_time_recovery {
    enabled = false  # Disabled to stay within free tier
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = "demo-classical-results-${random_string.suffix.result}"
  }
}

# DynamoDB table for tracking API usage (optional)
resource "aws_dynamodb_table" "api_usage" {
  name           = "demo-classical-api-usage-${random_string.suffix.result}"
  billing_mode   = "ON_DEMAND"
  hash_key       = "api_key"
  range_key      = "date"

  attribute {
    name = "api_key"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name = "demo-classical-api-usage-${random_string.suffix.result}"
  }
}
