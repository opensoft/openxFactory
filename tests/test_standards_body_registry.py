from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.standards_body_registry import (
    VERIFICATION_CLAIM_FIELD,
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

    def test_the_29_UNVERIFIED_current_bodies_are_reported_against(self) -> None:
        """The measurement the requirement's scope rests on, kept re-runnable.

        32 bodies carry `status: current`; 3 declare a verification date. If a
        later change re-verifies some of the other 29 these numbers move, and
        this test is where that shows up — but the SHAPE must not: a body
        without a verification claim is never reported against, because the
        registry's own header discloses those entries as working knowledge and
        the only ways to satisfy a `status`-keyed rule are to fabricate dates or
        to demote records whose currency is not in doubt.
        """
        document = load_registry(REGISTRY_PATH)
        bodies = document["bodies"]
        current = [b for b in bodies if b.get("status") == "current"]
        # Presence of the key is the claim, not its truthiness — mirrors the
        # validator's own rule in `registry_errors` (`VERIFICATION_CLAIM_FIELD
        # in body`). A truthiness test would silently drop a MALFORMED claim
        # (`verified_on: ""` or `verified_on:` null) into "not claiming",
        # exactly the escape `registry_errors` was fixed to close.
        claiming = [b for b in current if VERIFICATION_CLAIM_FIELD in b]

        assert len(current) == 32 and len(claiming) == 3
        assert {b["id"] for b in claiming} == {"itil5", "sfia", "apqc_pcf"}
        assert registry_errors(document) == [], (
            "no unverified legacy body is reported against — see the "
            "'An unverified legacy record is left as it stands' scenario")

    def test_unverified_override_requires_approver(self) -> None:
        document = load_registry(INVALID_OVERRIDE_FIXTURE)

        errors = registry_errors(document)

        assert any("operator_override.approved_by" in error for error in errors)


class TestVerificationClaimScope:
    """The obligation is keyed to the CLAIM, never to `status: current`."""

    def test_a_body_DECLARING_a_verification_date_owes_the_whole_record(
        self,
    ) -> None:
        errors = registry_errors(
            {"bodies": [{"id": "newcomer", "status": "current",
                         "verified_on": "2026-09-03"}]}
        )

        # All six the requirement names beside `id` — `steward` and `names` were
        # missing from the enforced set until 2026-09-03, so a body could claim
        # verification while saying nothing about who stewards it or what kind
        # of term it names, which is the conflation `names` exists to prevent.
        for field in ("steward", "names", "current_version", "source_url",
                      "confidence"):
            assert any(f"newcomer.{field}" in e for e in errors), field

    def test_an_EMPTY_verification_date_is_a_MALFORMED_claim_not_an_absent_one(
        self,
    ) -> None:
        """The shape most likely to be a mistake must not be the one that escapes.

        A truthiness test read `verified_on: ""` and `verified_on:` (null) as
        "makes no claim", so a half-written record slipped through while a
        record that never mentioned verification was held to nothing. Presence
        of the key is the claim.
        """
        for blank in ("", None):
            errors = registry_errors(
                {"bodies": [{"id": "newcomer", "status": "current",
                             "verified_on": blank}]}
            )
            assert any("newcomer.verified_on" in e for e in errors), blank
            assert any("newcomer.names" in e for e in errors), blank

    def test_a_body_CLAIMING_NOTHING_is_not_reported_against(self) -> None:
        # The 29 legacy entries' shape: current, sourced, but never re-read
        # against the body's own material. Inventing a date for it is the one
        # thing the registry's sourcing caveat forbids.
        assert registry_errors(
            {"bodies": [{"id": "legacy", "status": "current",
                         "source_url": "https://example.invalid",
                         "confidence": "medium"}]}
        ) == []

    def test_the_named_three_cannot_ESCAPE_by_dropping_the_claim(self) -> None:
        # Without the floor, deleting `verified_on` would move a verified body
        # out of scope — repairing the finding by withdrawing the assertion.
        errors = registry_errors(
            {"bodies": [{"id": "sfia", "status": "current",
                         "steward": "SFIA Foundation", "names": "skills",
                         "source_url": "https://example.invalid",
                         "current_version": "SFIA 9", "confidence": "high"}]}
        )

        assert any("sfia.verified_on" in e for e in errors)

    def test_a_verified_body_omitting_its_TERM_KIND_is_rejected(self) -> None:
        # `names` is the registry's load-bearing field — its header says the
        # bodies "do NOT all name the same kind of thing" and that conflating a
        # PROCESS with a ROLE "is how a crosswalk quietly overstates what a
        # worker is". A verified record without it is that conflation, waiting.
        errors = registry_errors(
            {"bodies": [{"id": "newcomer", "status": "current",
                         "steward": "Somebody", "current_version": "v1",
                         "source_url": "https://example.invalid",
                         "verified_on": "2026-09-03", "confidence": "high"}]}
        )

        assert [e for e in errors if "newcomer.names" in e]
        assert not [e for e in errors if "newcomer.steward" in e]


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

    def test_an_UNHASHABLE_key_neither_crashes_nor_escapes_the_check(
        self, tmp_path: Path
    ) -> None:
        """The duplicate scan must not raise `TypeError` on a structural key.

        YAML permits a sequence as a key and PyYAML constructs it as a `list`,
        which a bare `set` cannot hold. An earlier draft guarded the membership
        test and still called `set.add`, so the SCAN raised a bare `TypeError` —
        the wrong exception type, escaping past callers that catch
        `DuplicateRegistryKey`, and firing before any duplicate could be seen.

        A single structural key is still REFUSED, by PyYAML's own
        `construct_mapping` with `ConstructorError: found unhashable key`. That
        is `yaml.safe_load`'s behaviour and this loader does not change it — the
        assertion below pins the two readers AGREEING, which is what makes this
        a fix to our scan rather than a change of policy.
        """
        single = tmp_path / "structural-key.yaml"
        single.write_text("? [a, b]\n: value\n", encoding="utf-8")

        with pytest.raises(yaml.YAMLError):  # never TypeError, from our scan
            load_registry(single)
        with pytest.raises(yaml.YAMLError):  # and `safe_load` says the same
            yaml.safe_load(single.read_text(encoding="utf-8"))

        # REPEATED, and this is what the token buys: the duplicate scan runs
        # first, so the more specific of the two true statements is the one the
        # caller gets.
        repeated = tmp_path / "repeated-structural-key.yaml"
        repeated.write_text("? [a, b]\n: first\n? [a, b]\n: second\n",
                            encoding="utf-8")
        with pytest.raises(DuplicateRegistryKey):
            load_registry(repeated)

    def test_a_MALFORMED_registry_raises_YAMLError_and_not_something_else(
        self, tmp_path: Path
    ) -> None:
        """The exception class both call sites depend on.

        `scripts/validate-omnigent-contracts.py` degrades to an empty set and a
        named failure rather than a traceback, and it does that by catching
        `DuplicateRegistryKey` AND `yaml.YAMLError`. `DuplicateRegistryKey` is a
        `ValueError`, so neither `except` covers the other — which is why the
        class of everything ELSE that can go wrong is pinned here rather than
        assumed.
        """
        broken = tmp_path / "broken.yaml"
        broken.write_text("bodies:\n  - id: sfia\n   bad: indent\n",
                          encoding="utf-8")

        with pytest.raises(yaml.YAMLError):
            load_registry(broken)
        assert not isinstance(
            pytest.raises(yaml.YAMLError, load_registry, broken).value,
            DuplicateRegistryKey), "a parse error is not a duplicate-key finding"

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
