# DynamoDB table for storing quantum optimization results
resource "aws_dynamodb_table" "results" {
  name           = "demo-quantum-results-${random_string.suffix.result}"
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

  attribute {
    name = "algorithm"
    type = "S"
  }

  global_secondary_index {
    name               = "timestamp-index"
    hash_key           = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "algorithm-index"
    hash_key           = "algorithm"
    projection_type    = "ALL"
  }

  point_in_time_recovery {
    enabled = false  # Disabled to stay within free tier
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = "demo-quantum-results-${random_string.suffix.result}"
  }
}

# DynamoDB table for quantum experiment metadata
resource "aws_dynamodb_table" "experiments" {
  name           = "demo-quantum-experiments-${random_string.suffix.result}"
  billing_mode   = "ON_DEMAND"
  hash_key       = "experiment_id"

  attribute {
    name = "experiment_id"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  global_secondary_index {
    name               = "status-index"
    hash_key           = "status"
    projection_type    = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name = "demo-quantum-experiments-${random_string.suffix.result}"
  }
}
