"""CI tests for the nac-validate pre-change gate.

Runs the actual netascode toolchain (nac-validate) against the repo data
and against known-bad fixtures, asserting on documented exit codes:
0 = pass, 1 = semantic (rule) failure, 2 = syntax/schema failure.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIXTURES = Path(__file__).parent / "fixtures"


def nac_validate(*paths):
    return subprocess.run(
        ["nac-validate", "-s", str(ROOT / ".schema.yaml"), "-r", str(ROOT / "rules")]
        + [str(p) for p in paths],
        capture_output=True,
        text=True,
    )


def test_repo_data_passes():
    result = nac_validate(ROOT / "data" / "apic")
    assert result.returncode == 0, result.stdout + result.stderr


def test_schema_rejects_bad_tenant_name():
    result = nac_validate(FIXTURES / "bad_schema.yaml")
    assert result.returncode == 2, result.stdout + result.stderr


def test_rule_101_catches_undefined_vrf():
    result = nac_validate(FIXTURES / "bad_undefined_vrf.yaml")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "101" in result.stdout + result.stderr


def test_rule_201_catches_public_subnet():
    result = nac_validate(FIXTURES / "bad_public_subnet.yaml")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "201" in result.stdout + result.stderr
