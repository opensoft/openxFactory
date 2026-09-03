from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.standards_body_registry import (
    DuplicateRegistryKey,
    load_registry,
    registry_errors,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "contracts" / "policies" / "standards-bodies.yaml"
INVALID_OVERRIDE_FIXTURE = (
    ROOT / "tests" / "fixtures-standards-body-registry-unqualified-override.yaml"
)


def _bodies() -> dict[str, dict[str, object]]:
    # `load_registry`, never `yaml.safe_load`: the registry is exactly the file
    # whose duplicate key this loader exists to refuse, and a test that read it
    # the permissive way would be green on the document the defect produces.
    document = load_registry(REGISTRY_PATH)
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

    def test_the_sfia_licensing_source_SURVIVES_the_current_publication_source(
        self,
    ) -> None:
        """Both URLs are readable, and they are DIFFERENT keys.

        The regression this pins: the entry once carried `source_url` twice, so
        `yaml.safe_load` returned the publication page and the licensing
        evidence D2 exists to preserve was gone from every reader while still
        printed in the file. Asserting `licence_page` alone would not catch a
        relapse — the assertion that matters is that the current-publication
        source is the OTHER value, so one key can never be standing in for both.
        """
        sfia = _bodies()["sfia"]

        assert sfia["source_url"] == "https://sfia-online.org/en/sfia-9"
        assert sfia["licence_page"] == (
            "https://sfia-online.org/en/about-sfia/licensing-sfia/"
            "using-and-licensing-sfia"
        )
        assert sfia["operator_override"]["conflicting_source"].strip() == (
            sfia["licence_page"]
        ), "the override's conflicting source IS the licensing page it overrides"

    def test_apqc8_includes_it_process_scope_and_attribution(self) -> None:
        apqc = _bodies()["apqc_pcf"]
        scopes = apqc["crosswalk_scopes"]

        assert apqc["current_version"].startswith("Cross-Industry PCF 8.0")
        assert "8.0 Manage Information Technology (IT)" in scopes
        assert apqc["attribution_required"]

    def test_current_registry_metadata_is_valid(self) -> None:
        document = load_registry(REGISTRY_PATH)

        assert registry_errors(document) == []

    def test_unverified_override_requires_approver(self) -> None:
        document = load_registry(INVALID_OVERRIDE_FIXTURE)

        errors = registry_errors(document)

        assert any("operator_override.approved_by" in error for error in errors)


class TestRegistryLoader:
    """The loader arm — the class of defect no post-parse check can reach."""

    def test_a_duplicate_key_is_REFUSED_rather_than_silently_collapsed(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "registry.yaml"
        path.write_text(
            "schema_version: 1\nkind: standards_body_registry\nbodies:\n"
            "  - id: sfia\n"
            "    source_url: https://sfia-online.org/en/about-sfia/licensing-sfia\n"
            "    source_url: https://sfia-online.org/en/sfia-9\n",
            encoding="utf-8",
        )

        # `yaml.safe_load` is green on the same bytes and answers with the LAST
        # value, which is precisely the failure: the permissive reader cannot
        # tell a repaired registry from a broken one.
        assert (
            yaml.safe_load(path.read_text(encoding="utf-8"))["bodies"][0]["source_url"]
            == "https://sfia-online.org/en/sfia-9"
        )

        with pytest.raises(DuplicateRegistryKey) as caught:
            load_registry(path)
        assert "source_url" in str(caught.value)
        assert "line 6" in str(caught.value), "the refusal names where to look"

    def test_a_duplicate_NESTED_key_is_refused_too(self, tmp_path: Path) -> None:
        # Nesting must not smuggle a duplicate past a top-level check: a repeat
        # inside `operator_override` discards a value exactly as well.
        path = tmp_path / "registry.yaml"
        path.write_text(
            "bodies:\n  - id: sfia\n    operator_override:\n"
            "      approved_by: Brett Heap\n"
            "      approved_by: somebody else\n",
            encoding="utf-8",
        )

        with pytest.raises(DuplicateRegistryKey):
            load_registry(path)

    def test_a_registry_with_no_duplicate_loads_unchanged(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "registry.yaml"
        path.write_text(
            "schema_version: 1\nbodies:\n  - id: sfia\n    confidence: high\n",
            encoding="utf-8",
        )

        assert load_registry(path) == {
            "schema_version": 1,
            "bodies": [{"id": "sfia", "confidence": "high"}],
        }
