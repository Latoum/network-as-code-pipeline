from nac_validate import RuleBase


class Rule(RuleBase):
    id = "301"
    description = "Verify tenant names are unique across the data model"
    severity = "MEDIUM"

    @classmethod
    def match(cls, data):
        results, seen = [], set()
        for tenant in data.get("apic", {}).get("tenants", []):
            name = tenant.get("name")
            if name in seen:
                results.append(f"apic.tenants[name={name}] - duplicate tenant name")
            seen.add(name)
        return results
