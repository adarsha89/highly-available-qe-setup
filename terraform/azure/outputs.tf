output "resource_group_name" {
  value       = azurerm_resource_group.qe_rg.name
  description = "Resource Group Name"
}

output "cluster_name" {
  value       = azurerm_kubernetes_cluster.qe_aks.name
  description = "AKS Cluster Name"
}

output "cluster_fqdn" {
  value       = azurerm_kubernetes_cluster.qe_aks.fqdn
  description = "AKS API FQDN"
}

output "kube_config_raw" {
  value       = azurerm_kubernetes_cluster.qe_aks.kube_config_raw
  sensitive   = true
  description = "Raw kubeconfig for AKS cluster"
}

output "storage_account_name" {
  value       = azurerm_storage_account.qe_storage.name
  description = "Storage Account for artifacts and backups"
}
