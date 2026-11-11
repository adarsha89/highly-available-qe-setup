variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "local"
}

variable "account_id" {
  type        = string
  description = "AWS Account ID or unique identifier"
  default     = "000000000000"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where EFS mount targets reside"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for multi-AZ EFS mount targets"
}

variable "backup_retention_days" {
  type        = number
  description = "Number of days to retain disaster recovery backups"
  default     = 90
}

variable "force_destroy_buckets" {
  type        = bool
  description = "Allow destruction of non-empty S3 buckets in non-production environments"
  default     = true
}
