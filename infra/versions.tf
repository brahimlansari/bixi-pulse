terraform {
  required_version = ">= 1.9"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }

  resource_provider_registrations = "none"
  resource_providers_to_register = [
    "Microsoft.KeyVault",
    "Microsoft.MachineLearningServices",
  ]
}