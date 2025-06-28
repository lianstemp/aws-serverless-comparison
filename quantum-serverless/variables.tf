variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "demo"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "quantum"
}

variable "cost_alert_threshold" {
  description = "Cost alert threshold in USD"
  type        = number
  default     = 20
}

variable "alert_email" {
  description = "Email for cost alerts"
  type        = string
  default     = "admin@example.com"
}

variable "api_throttle_rate" {
  description = "API Gateway throttle rate (requests per second)"
  type        = number
  default     = 5
}

variable "api_throttle_burst" {
  description = "API Gateway throttle burst limit"
  type        = number
  default     = 10
}

variable "api_quota_limit" {
  description = "Monthly API quota limit"
  type        = number
  default     = 100
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 900  # 15 minutes for quantum processing
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 512  # More memory for quantum computations
}

variable "braket_device_arn" {
  description = "ARN of the Braket device (simulator recommended)"
  type        = string
  default     = "arn:aws:braket:::device/quantum-simulator/amazon/sv1"
}

variable "max_quantum_qubits" {
  description = "Maximum number of qubits for quantum optimization"
  type        = number
  default     = 10
}
