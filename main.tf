# main.tf
provider "azurerm" {
    features {}
    subscription_id = "80a83f89-1022-4491-8116-5505e640a105"
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-azure-tables-poc"
  location = "eastus"
}

resource "azurerm_storage_account" "storage" {
  name                     = "storageaccountpoc123774"  # Must be globally unique
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_table" "table" {
  name                 = "mytable"
  storage_account_name = azurerm_storage_account.storage.name
}
