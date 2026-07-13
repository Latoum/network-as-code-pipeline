# Network as Code Pipeline — Declarative ACI Fabric Automation

A working demonstration of the **Services-as-Code** operating model built on the open-source **[Cisco Network-as-Code](https://netascode.cisco.com)** toolchain: a declarative YAML source of truth, `nac-validate` pre-change gates, the NAC ACI Terraform module for deployment, and `nac-test` for post-change verification.

> Pattern drawn from my field experience designing "as-code" delivery models for large federal data-center environments.

## 🎯 Problem Statement

Network engineers spend their days **chasing state** — correlating dozens of controller UIs, CLI sessions, and monitoring tools to build a mental picture of the network. Changes ride on multi-page Method-of-Procedure documents, late-night all-hands calls, and slow rollbacks. Industry research attributes ~80% of outages to misconfiguration.

The fix is the same one software engineering found decades ago: **version-controlled intent, validation before deployment, and tests after it.**

## 🏗️ The Five-Stage Pipeline

Every change runs through the same stages — same gates, same audit trail:

```
1. Capture intent   →  YAML data model in Git (single source of truth)
2. Pre-change       →  nac-validate: Yamale schema + Python semantic rules
3. Human approval   →  Pull request review
4. Deploy           →  Terraform: netascode/nac-aci module renders YAML → ACI objects
5. Post-change      →  nac-test: Robot Framework assertions against the live fabric
```

The power of abstraction: a tenant that takes **200+ lines** of raw APIC API JSON becomes **6 lines of data**:

```yaml
apic:
  tenants:
    - name: DEMO
      vrfs:
        - name: VRF1
        - name: VRF2
```

## 📁 Repository Structure

```
├── .schema.yaml               # Yamale schema — nac-validate syntax gate
├── rules/                     # nac-validate semantic rules (Python Rule classes)
│   ├── 101_bd_vrf_defined.py
│   ├── 201_no_public_subnets.py
│   └── 301_unique_tenant_names.py
├── data/
│   └── apic/
│       ├── defaults.yaml      # Org-wide defaults
│       └── tenants.yaml       # Declarative tenant intent
├── terraform/
│   └── main.tf                # netascode/nac-aci/aci module — deploy stage
├── tests/
│   ├── test_validation.py     # Asserts nac-validate exit codes on good/bad data
│   └── fixtures/              # Known-bad YAML the gates must catch
└── .github/workflows/
    └── pipeline.yml           # CI: nac-validate → pytest → terraform validate
```

## 🚀 Quickstart

```bash
pip install -r requirements.txt

# Pre-change gate — the real netascode validator
nac-validate -s .schema.yaml -r rules/ data/apic/

# Prove the gates catch bad intent
pytest tests/ -v

# Deploy stage (requires an APIC; CI runs init/validate only)
export ACI_URL=https://apic.example.com ACI_USERNAME=admin ACI_PASSWORD=...
terraform -chdir=terraform init && terraform -chdir=terraform plan
```

Push a change to `data/` and the GitHub Actions pipeline runs the same gates automatically — a misconfigured VRF or a policy violation fails the build **before any device would be touched**. `nac-validate` exit codes make CI decisions unambiguous: `0` pass, `1` semantic violation, `2` schema/syntax error.

## 💡 Key Insights

- **Declarative beats imperative** — the NAC data model removes ordering, dependency, and reference complexity from the operator's head.
- **Validation layers stack** — Yamale schema catches format/syntax; Python `Rule` classes catch semantics and compliance. Each layer catches a class of error the previous can't.
- **The human stays in the loop** — the PR review is the one manual gate; everything else is automated.
- **As-code is the on-ramp to AI operations** — once the network lives as structured data in Git, LLM agents can read it, reason over it, and propose changes through the same gated pipeline. See my companion project: [network-ai-orchestration](https://github.com/Latoum/network-ai-orchestration).

## 🛠️ Toolchain

[nac-validate](https://github.com/netascode/nac-validate) · [nac-test](https://github.com/netascode/nac-test) · [terraform-aci-nac-aci](https://github.com/netascode/terraform-aci-nac-aci) · Terraform · Pytest · GitHub Actions

Post-change verification with `nac-test` (Robot Framework rendered via Jinja from the same YAML intent) requires a live ACI fabric, so it is documented as stage 5 but not executed in this repo's CI.

## ⚖️ Disclaimer

An independent demonstration project using the open-source [Network-as-Code](https://netascode.cisco.com) tooling (MPL-2.0/Apache-2.0 licensed). Not affiliated with, sponsored by, or endorsed by Cisco Systems. Cisco, ACI, and related marks are trademarks of Cisco Systems, Inc.

## 📫 Author

**Laith Atoum, D.Eng.** — [LinkedIn](https://www.linkedin.com/in/laithatoum) · [GitHub](https://github.com/Latoum)
