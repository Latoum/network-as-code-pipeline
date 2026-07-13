from nac_validate import RuleBase


class Rule(RuleBase):
    id = "201"
    description = "Verify no subnet is marked public (environment compliance policy)"
    severity = "HIGH"

    @classmethod
    def match(cls, data):
        results = []
        for tenant in data.get("apic", {}).get("tenants", []):
            for bd in tenant.get("bridge_domains", []):
                for subnet in bd.get("subnets", []):
                    if subnet.get("public"):
                        results.append(
                            f"apic.tenants[name={tenant.get('name')}].bridge_domains"
                            f"[name={bd.get('name')}].subnets[ip={subnet.get('ip')}]"
                            " - public subnets are not permitted"
                        )
        return results
