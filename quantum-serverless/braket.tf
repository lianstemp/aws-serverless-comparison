# S3 bucket for Braket quantum task results
resource "aws_s3_bucket" "braket_results" {
  bucket = "demo-quantum-braket-results-${random_string.suffix.result}"

  tags = {
    Name = "demo-quantum-braket-results-${random_string.suffix.result}"
  }
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "braket_results" {
  bucket = aws_s3_bucket.braket_results.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 bucket server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "braket_results" {
  bucket = aws_s3_bucket.braket_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 bucket public access block
resource "aws_s3_bucket_public_access_block" "braket_results" {
  bucket = aws_s3_bucket.braket_results.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 bucket lifecycle configuration to manage costs
resource "aws_s3_bucket_lifecycle_configuration" "braket_results" {
  bucket = aws_s3_bucket.braket_results.id

  rule {
    id     = "quantum_results_lifecycle"
    status = "Enabled"

    filter {
      prefix = ""
    }

    expiration {
      days = 30  # Delete objects after 30 days to control costs
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }
  }
}

# Braket quantum computing service configuration
# Note: There's no direct Terraform provider for Braket resources,
# so we'll manage device selection through environment variables
