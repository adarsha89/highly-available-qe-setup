variable "environment" {
  type        = string
  description = "Target deployment environment (e.g. local, dev, prod-qe)"
  default     = "local"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones for multi-AZ high availability"
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "cluster_name" {
  type        = string
  description = "Name of the Kubernetes cluster using these subnets"
  default     = "qe-ha-cluster"
}

variable "single_nat_gateway" {
  type        = bool
  description = "Set to true for cost-saving/local testing; false for multi-AZ NAT HA"
  default     = true
}
