terraform {
  required_version = ">= 1.8.0"

  required_providers {
    aci = {
      source  = "CiscoDevNet/aci"
      version = ">= 2.19.0"
    }
  }
}

# APIC credentials are supplied via environment variables in a real deployment:
#   ACI_URL, ACI_USERNAME, ACI_PASSWORD
provider "aci" {}

# Stage 4 — Deploy: the Network-as-Code ACI module renders the same YAML
# source of truth (validated by nac-validate in stage 2) into ACI objects.
module "aci" {
  source  = "netascode/nac-aci/aci"
  version = ">= 0.7.0"

  yaml_directories = ["../data/apic"]

  manage_tenants = true
}
