#!/usr/bin/env python3
"""Pre-change validation gate: format -> syntax -> semantics -> compliance.

Runs BEFORE any device is touched. A non-zero exit code fails the CI pipeline.

Usage:
    python scripts/validate.py --schema schemas/tenant_schema.json \
                               --data data/apic/tenants.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).parent))
from policy_rules import ALL_RULES  # noqa: E402


def load_yaml(path: Path) -> dict:
    """Format gate: file must parse as YAML."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        sys.exit(f"FORMAT FAIL: {path} is not valid YAML:\n{exc}")


def validate_schema(data: dict, schema_path: Path) -> list[str]:
    """Syntax gate: data must conform to the JSON Schema."""
    schema = json.loads(schema_path.read_text())
    validator = Draft202012Validator(schema)
    return [
        f"SCHEMA: {'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
        for e in validator.iter_errors(data)
    ]


def validate_policy(data: dict) -> list[str]:
    """Semantics & compliance gate: org-specific rules."""
    violations = []
    for rule in ALL_RULES:
        violations.extend(f"POLICY [{rule.__name__}]: {v}" for v in rule(data))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    args = parser.parse_args()

    data = load_yaml(args.data)
    errors = validate_schema(data, args.schema) + validate_policy(data)

    if errors:
        print(f"❌ Validation FAILED — {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("✅ Validation passed: format, syntax, semantics, compliance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
