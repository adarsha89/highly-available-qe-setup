variable "environment" {
  type        = string
  description = "Target deployment environment"
  default     = "local"
}

variable "azure_region" {
  type        = string
  description = "Azure region for deployment"
  default     = "eastus"
}

variable "use_emulator" {
  type        = bool
  description = "Set to true for local testing with Azurite"
  default     = false
}

variable "resource_group_name" {
  type        = string
  description = "Name of the Azure resource group"
  default     = "rg-qe-ha-platform"
}

variable "vnet_address_space" {
  type        = string
  description = "Address space for Azure VNet"
  default     = "10.10.0.0/16"
}

variable "cluster_name" {
  type        = string
  description = "Name of the AKS cluster"
  default     = "qe-ha-aks-cluster"
}

variable "node_count" {
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
  description = "Emails subscribed to critical alerts"
  default     = []
}
