# Azure Root Module - High Availability QE Platform Orchestration

# 1. Resource Group
resource "azurerm_resource_group" "qe_rg" {
  name     = var.resource_group_name
  location = var.azure_region

  tags = {
    Environment = var.environment
    Platform    = "QE-HA"
    ManagedBy   = "Terraform"
  }
}

# 2. Virtual Network & Subnets
resource "azurerm_virtual_network" "qe_vnet" {
  name                = "${var.environment}-qe-vnet"
  location            = azurerm_resource_group.qe_rg.location
  resource_group_name = azurerm_resource_group.qe_rg.name
  address_space       = [var.vnet_address_space]
}

resource "azurerm_subnet" "aks_subnet" {
  name                 = "aks-nodes-subnet"
  resource_group_name  = azurerm_resource_group.qe_rg.name
  virtual_network_name = azurerm_virtual_network.qe_vnet.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space, 4, 0)]
}

# 3. Azure Kubernetes Service (AKS HA Cluster)
resource "azurerm_kubernetes_cluster" "qe_aks" {
  name                = var.cluster_name
  location            = azurerm_resource_group.qe_rg.location
  resource_group_name = azurerm_resource_group.qe_rg.name
  dns_prefix          = "${var.environment}-aks"
  kubernetes_version  = "1.30"

  default_node_pool {
    name                = "agentpool"
    node_count          = var.node_count
    vm_size             = "Standard_D4s_v5"
    vnet_subnet_id      = azurerm_subnet.aks_subnet.id
    enable_auto_scaling = true
    min_count           = var.min_node_count
    max_count           = var.max_node_count
    zones               = ["1", "2", "3"] # Multi-AZ placement for HA

    upgrade_settings {
      max_surge = "33%"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    Environment = var.environment
  }
}

# 4. Azure Storage Account (Blob Containers for Test Artifacts and Velero DR)
resource "azurerm_storage_account" "qe_storage" {
  name                     = replace("${var.environment}qestorage${substr(uuid(), 0, 4)}", "-", "")
  resource_group_name      = azurerm_resource_group.qe_rg.name
  location                 = azurerm_resource_group.qe_rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS" # Geo-Redundant Storage for Disaster Recovery

  blob_properties {
    versioning_enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

resource "azurerm_storage_container" "artifacts" {
  name                  = "qe-artifacts"
  storage_account_name  = azurerm_storage_account.qe_storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "backups" {
  name                  = "qe-velero-backups"
  storage_account_name  = azurerm_storage_account.qe_storage.name
  container_access_type = "private"
}

# 5. Azure Monitor Action Group for HA Incident Notifications
resource "azurerm_monitor_action_group" "qe_alerts" {
  name                = "${var.environment}-qe-critical-alerts"
  resource_group_name = azurerm_resource_group.qe_rg.name
  short_name          = "qe-alerts"

  dynamic "email_receiver" {
    for_each = var.alert_emails
    content {
      name          = "alert-receiver-${email_receiver.key}"
      email_address = email_receiver.value
    }
  }
}
