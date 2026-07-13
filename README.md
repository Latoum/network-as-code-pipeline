# Network as Code Pipeline — Declarative ACI Fabric Automation

A working demonstration of the **Services-as-Code** operating model: manage a data-center fabric the way software teams manage code — a declarative YAML source of truth, automated pre-change validation, and post-change verification, all wired into a CI pipeline.

> Pattern drawn from my field experience designing "as-code" delivery models for large federal data-center environments. All code and content here is original demonstration material.

## 🎯 Problem Statement

Network engineers spend their days **chasing state** — correlating dozens of controller UIs, CLI sessions, and monitoring tools to build a mental picture of the network. Changes ride on multi-page Method-of-Procedure documents, late-night all-hands calls, and slow rollbacks. Industry research attributes ~80% of outages to misconfiguration.

The fix is the same one software engineering found decades ago: **version-controlled intent, validation before deployment, and tests after it.**

## 🏗️ Approach

Every change flows through the same five stages — same gates, same audit trail:

```
1. Capture intent   →  YAML data model in Git (single source of truth)
2. Pre-change       →  Schema + policy validation (before touching any device)
3. Human approval   →  Pull request review
4. Deploy           →  Terraform / API push to the fabric
5. Post-change      →  Assert live state matches YAML intent
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
├── data/
│   └── apic/
│       ├── defaults.yaml      # Org-wide defaults (naming suffixes, best practices)
│       └── tenants.yaml       # Declarative tenant intent
├── schemas/
│   └── tenant_schema.json     # JSON Schema — format & syntax gate
├── scripts/
│   ├── validate.py            # Pre-change: schema + policy validation
│   └── policy_rules.py        # Custom policy rules (semantics & compliance)
├── tests/
│   └── test_validate.py       # Pytest suite for the validation engine
└── .github/workflows/
    └── pipeline.yml           # CI: lint → validate → test on every push/PR
```

## 🚀 Quickstart

```bash
pip install -r requirements.txt

# Validate the data model (pre-change gate)
python scripts/validate.py --schema schemas/tenant_schema.json --data data/apic/tenants.yaml

# Run the test suite
pytest tests/ -v
```

Push a change to `data/` and the GitHub Actions pipeline runs the same gates automatically — a misconfigured VRF or a policy violation fails the build **before any device would be touched**.

## 💡 Key Insights

- **Declarative beats imperative** — describing intended state removes ordering, dependency, and reference complexity from the operator's head.
- **Validation layers stack**: format → syntax → semantics → compliance. Each catches a class of error the previous can't.
- **The human stays in the loop** — the PR review is the one manual gate; everything else is automated.
- **As-code is the on-ramp to AI operations** — once the network lives as structured data in Git, LLM agents can read it, reason over it, and propose changes through the same gated pipeline. See my companion project: [network-ai-orchestration](https://github.com/Latoum/network-ai-orchestration).

## 🛠️ Tech Stack

Python · PyYAML · JSON Schema · Pytest · GitHub Actions · Terraform concepts (Cisco ACI provider pattern)

## ⚖️ Disclaimer

This is an independent, original demonstration project. It is not affiliated with, sponsored by, or endorsed by Cisco Systems. Cisco, ACI, and related marks are trademarks of Cisco Systems, Inc. Concepts like Network-as-Code are documented publicly at [netascode.cisco.com](https://netascode.cisco.com).

## 📫 Author

**Laith Atoum, D.Eng.** — [LinkedIn](https://www.linkedin.com/in/laithatoum) · [GitHub](https://github.com/Latoum)
