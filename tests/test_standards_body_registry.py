from __future__ import annotations

from pathlib import Path

import yaml

from scripts.standards_body_registry import registry_errors

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "contracts" / "policies" / "standards-bodies.yaml"
INVALID_OVERRIDE_FIXTURE = (
    ROOT / "tests" / "fixtures-standards-body-registry-unqualified-override.yaml"
)


def _bodies() -> dict[str, dict[str, object]]:
    document = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {str(body["id"]): body for body in document["bodies"]}


class TestStandardsBodyRegistry:
    def test_itil5_is_current_without_replacing_itil4(self) -> None:
        bodies = _bodies()

        assert "itil4" in bodies
        assert bodies["itil5"]["status"] == "current"
        assert bodies["itil5"]["current_version"] == "ITIL Version 5"

    def test_sfia9_override_is_explicit(self) -> None:
        sfia = _bodies()["sfia"]

        assert sfia["current_version"] == "SFIA 9"
        assert sfia["redistribution_permitted_in_product_config"] == "yes"
        override = sfia["operator_override"]
        assert override["status"] == "unverified"
        assert override["approved_by"] == "Brett Heap"

    def test_apqc8_includes_it_process_scope_and_attribution(self) -> None:
        apqc = _bodies()["apqc_pcf"]
        scopes = apqc["crosswalk_scopes"]

        assert apqc["current_version"].startswith("Cross-Industry PCF 8.0")
        assert "8.0 Manage Information Technology (IT)" in scopes
        assert apqc["attribution_required"]

    def test_current_registry_metadata_is_valid(self) -> None:
        document = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))

        assert registry_errors(document) == []

    def test_unverified_override_requires_approver(self) -> None:
        document = yaml.safe_load(INVALID_OVERRIDE_FIXTURE.read_text(encoding="utf-8"))

        errors = registry_errors(document)

        assert any("operator_override.approved_by" in error for error in errors)
