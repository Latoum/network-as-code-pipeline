from nac_validate import RuleBase


class Rule(RuleBase):
    id = "101"
    description = "Verify every bridge domain references a VRF defined in the same tenant"
    severity = "HIGH"

    @classmethod
    def match(cls, data):
        results = []
        for tenant in data.get("apic", {}).get("tenants", []):
            vrf_names = {v.get("name") for v in tenant.get("vrfs", [])}
            for bd in tenant.get("bridge_domains", []):
                if bd.get("vrf") not in vrf_names:
                    results.append(
                        f"apic.tenants[name={tenant.get('name')}].bridge_domains"
                        f"[name={bd.get('name')}].vrf - undefined VRF '{bd.get('vrf')}'"
                    )
        return results
