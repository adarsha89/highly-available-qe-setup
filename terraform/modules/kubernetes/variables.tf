variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "local"
}

variable "cluster_name" {
  type        = string
  description = "Name of the Kubernetes cluster"
  default     = "qe-ha-cluster"
}

variable "cluster_version" {
  type        = string
  description = "Kubernetes control plane version"
  default     = "1.30"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the cluster is deployed"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs spanning multiple AZs for HA node placement"
}

variable "cluster_role_arn" {
  type        = string
  description = "IAM Role ARN for the EKS control plane"
}

variable "node_role_arn" {
  type        = string
  description = "IAM Role ARN for worker nodes"
}

variable "instance_types" {
  type        = list(string)
  description = "EC2 instance types for the node group"
  default     = ["m5.large"]
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
