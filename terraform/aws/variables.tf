variable "environment" {
  type        = string
  description = "Target deployment environment (e.g. local, dev, prod-qe)"
  default     = "local"
}

variable "aws_region" {
  type        = string
  description = "AWS deployment region"
  default     = "us-east-1"
}

variable "use_localstack" {
  type        = bool
  description = "Set to true to point Terraform to LocalStack emulator"
  default     = true
}

variable "localstack_endpoint" {
  type        = string
  description = "LocalStack Gateway endpoint"
  default     = "http://localhost:4566"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "Availability zones for multi-AZ HA deployment"
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "cluster_name" {
  type        = string
  description = "Kubernetes cluster name"
  default     = "qe-ha-cluster"
}

variable "desired_node_count" {
  type        = number
  description = "Desired number of worker nodes"
  default     = 3
}

variable "min_node_count" {
  type        = number
  description = "Minimum number of worker nodes"
  default     = 3
}

variable "max_node_count" {
  type        = number
  description = "Maximum number of worker nodes"
  default     = 6
}

variable "alert_emails" {
  type        = list(string)
  description = "Emails subscribed to critical HA alerts"
  default     = []
}
