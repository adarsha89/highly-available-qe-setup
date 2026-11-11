variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "local"
}

variable "cluster_name" {
  type        = string
  description = "Kubernetes cluster name"
  default     = "qe-ha-cluster"
}

variable "log_retention_days" {
  type        = number
  description = "Days to retain platform logs"
  default     = 30
}

variable "alert_emails" {
  type        = list(string)
  description = "Email addresses for critical platform alerts"
  default     = []
}
