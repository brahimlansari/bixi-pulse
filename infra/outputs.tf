output "workspace_name" {
  value = azurerm_machine_learning_workspace.main.name
}

output "workspace_id" {
  value = azurerm_machine_learning_workspace.main.id
}

output "mlflow_tracking_uri" {
  description = "Adresse du serveur MLflow du workspace, à copier dans .env."
  value       = "azureml://${var.location}.api.azureml.ms/mlflow/v1.0${azurerm_machine_learning_workspace.main.id}"
}