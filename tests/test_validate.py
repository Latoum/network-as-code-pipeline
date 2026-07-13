"""Test suite for the pre-change validation engine."""
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from policy_rules import (  # noqa: E402
    rule_bd_vrf_must_exist,
    rule_no_public_subnets,
    rule_unique_tenant_names,
)
from validate import validate_schema  # noqa: E402

SCHEMA = ROOT / "schemas" / "tenant_schema.json"


def good_data():
    with open(ROOT / "data" / "apic" / "tenants.yaml") as f:
        return yaml.safe_load(f)


def test_repo_data_passes_schema():
    assert validate_schema(good_data(), SCHEMA) == []


def test_repo_data_passes_all_policies():
    data = good_data()
    assert rule_bd_vrf_must_exist(data) == []
    assert rule_no_public_subnets(data) == []
    assert rule_unique_tenant_names(data) == []


def test_schema_catches_bad_tenant_name():
    data = {"apic": {"tenants": [{"name": "bad name with spaces!"}]}}
    assert validate_schema(data, SCHEMA)


def test_policy_catches_undefined_vrf():
    data = {"apic": {"tenants": [{
        "name": "T1", "vrfs": [{"name": "A"}],
        "bridge_domains": [{"name": "bd1", "vrf": "MISSING"}],
    }]}}
    violations = rule_bd_vrf_must_exist(data)
    assert len(violations) == 1 and "MISSING" in violations[0]


def test_policy_catches_public_subnet():
    data = {"apic": {"tenants": [{
        "name": "T1", "vrfs": [{"name": "A"}],
        "bridge_domains": [{"name": "bd1", "vrf": "A",
                            "subnets": [{"ip": "1.1.1.1/24", "public": True}]}],
    }]}}
    assert rule_no_public_subnets(data)


def test_policy_catches_duplicate_tenants():
    data = {"apic": {"tenants": [{"name": "T1"}, {"name": "T1"}]}}
    assert rule_unique_tenant_names(data)
