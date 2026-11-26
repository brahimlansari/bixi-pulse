data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "project" {
  name = var.resource_group_name
}

data "azurerm_log_analytics_workspace" "logs" {
  name                = "workspace-rgbixipulselwCg"
  resource_group_name = data.azurerm_resource_group.project.name
}

locals {
  tags = {
    project    = "bixi-pulse"
    managed_by = "terraform"
  }
}

resource "azurerm_application_insights" "ml" {
  name                = "appi-bixi-pulse-ml"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.project.name
  workspace_id        = data.azurerm_log_analytics_workspace.logs.id
  application_type    = "web"
  tags                = local.tags
}

resource "azurerm_key_vault" "ml" {
  name                       = "kv-bixi-pulse-${var.suffix}"
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.project.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  rbac_authorization_enabled = true
  tags                       = local.tags
}

resource "azurerm_storage_account" "ml" {
  name                            = "stbixipulseml${var.suffix}"
  location                        = var.location
  resource_group_name             = data.azurerm_resource_group.project.name
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  tags                            = local.tags
}

resource "azurerm_machine_learning_workspace" "main" {
  name                    = "mlw-bixi-pulse"
  location                = var.location
  resource_group_name     = data.azurerm_resource_group.project.name
  application_insights_id = azurerm_application_insights.ml.id
  key_vault_id            = azurerm_key_vault.ml.id
  storage_account_id      = azurerm_storage_account.ml.id
  tags                    = local.tags

  identity {
    type = "SystemAssigned"
  }
}