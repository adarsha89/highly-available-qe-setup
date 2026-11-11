variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "local"
}

variable "account_id" {
  type        = string
  description = "AWS Account ID"
  default     = "000000000000"
}

variable "oidc_provider_arn" {
  type        = string
  description = "ARN of the EKS OIDC provider"
  default     = ""
}

variable "oidc_provider_url" {
  type        = string
  description = "URL of the EKS OIDC provider"
  default     = ""
}
