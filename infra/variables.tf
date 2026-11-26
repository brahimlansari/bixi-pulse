variable "location" {
  description = "Région Azure (autorisée par la politique de l'abonnement étudiant)."
  type        = string
  default     = "eastus2"
}

variable "resource_group_name" {
  description = "Groupe de ressources existant du projet."
  type        = string
  default     = "rg-bixi-pulse"
}

variable "suffix" {
  description = "Suffixe pour les noms qui doivent être uniques dans tout Azure."
  type        = string
  default     = "2611"
}