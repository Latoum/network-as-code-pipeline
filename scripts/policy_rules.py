"""Custom policy rules — the semantics & compliance layer.

Schema validation answers "is this well-formed?"
Policy rules answer "is this allowed in OUR network?"
Each rule returns a list of violation strings (empty = pass).
"""
from __future__ import annotations


def rule_bd_vrf_must_exist(data: dict) -> list[str]:
    """Every bridge domain must reference a VRF defined in the same tenant."""
    violations = []
    for tenant in data.get("apic", {}).get("tenants", []):
        vrf_names = {v["name"] for v in tenant.get("vrfs", [])}
        for bd in tenant.get("bridge_domains", []):
            if bd.get("vrf") not in vrf_names:
                violations.append(
                    f"Tenant '{tenant['name']}': bridge domain '{bd['name']}' "
                    f"references undefined VRF '{bd.get('vrf')}'"
                )
    return violations


def rule_no_public_subnets(data: dict) -> list[str]:
    """Compliance: public subnets are not permitted in this environment."""
    violations = []
    for tenant in data.get("apic", {}).get("tenants", []):
        for bd in tenant.get("bridge_domains", []):
            for subnet in bd.get("subnets", []):
                if subnet.get("public"):
                    violations.append(
                        f"Tenant '{tenant['name']}': subnet '{subnet['ip']}' in "
                        f"'{bd['name']}' is marked public — policy forbids this"
                    )
    return violations


def rule_unique_tenant_names(data: dict) -> list[str]:
    """Tenant names must be unique across the data model."""
    seen, violations = set(), []
    for tenant in data.get("apic", {}).get("tenants", []):
        name = tenant.get("name")
        if name in seen:
            violations.append(f"Duplicate tenant name: '{name}'")
        seen.add(name)
    return violations


ALL_RULES = [rule_bd_vrf_must_exist, rule_no_public_subnets, rule_unique_tenant_names]
