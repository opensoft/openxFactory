"""THE BLOB WALK REACHES ALL FOUR FREE STRINGS, AND THE THIRD OUTCOME EXITS 3.

Two invariants that the packaged corpus proves only by example, pinned here so
a regression names itself:

1. **The extended `walk_strings` reach** (task 3.5). Siting
   `custody_rederivations` OUTSIDE `custody` — which ruling D9's closure
   required — moved the entry's unbounded free strings beyond `check_custody`'s
   blob-shape walk, the family's only "wherever it hides" guard. The walk was
   extended over the whole entry minus its two digests. The packaged negatives
   cover `ruling_ref` and `recorded_by`; this file covers all FOUR free strings
   and every blob predicate, so a narrowing of the walk fails here first.

2. **The exit-status vocabulary** (task 3.4b). Brett Heap ruled the number on
   2026-09-09, in session, by multiple-choice selection, verbatim *"Exit 3 =
   needs a human decision (Recommended)"*, over the declined *"Exit 1, same as
   findings"* and *"Exit 0, report only"*. The PRECEDENCE — errors dominate — is
   his confirmed ruling of the same day. All three exits are asserted, not just
   the new one, because a vocabulary is only pinned if its boundaries are.
"""

from __future__ import annotations

import importlib.util
import hashlib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-consent-instruments.py"
WITHHELD = ROOT / "examples" / "consent-instrument" / "withheld" / \
    "custody-content-class-withheld.yaml"
BROKEN = ROOT / "examples" / "consent-instrument" / "negative" / \
    "custody-chain-broken-link.yaml"

#: The four UNBOUNDED FREE STRINGS in an entry. The two digests are excluded
#: from the walk (they are the only long opaque values an entry legitimately
#: carries) and `commit`, `at`, `diff_class` and `reason` are each already
#: bounded by a pattern, a format or a closed enumeration.
FREE_STRINGS = ("previous_locator", "observed_locator", "ruling_ref",
                "recorded_by")

#: One per predicate in `blob_shapes`.
BLOBS = {
    "base64-run": "Q" * 240,
    "data-uri": "data:text/plain;base64,bGFuZQ==",
    "pdf-magic": "%PDF-1.7 spurious",
    "multi-line": "first line\nsecond line",
}


def _load():
    spec = importlib.util.spec_from_file_location(
        "validate_consent_instruments_outcomes", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("field", FREE_STRINGS)
@pytest.mark.parametrize("shape", sorted(BLOBS))
def test_the_walk_reaches_every_free_string(field: str, shape: str) -> None:
    module = _load()
    doc = yaml.safe_load(WITHHELD.read_text(encoding="utf-8"))
    doc["custody_rederivations"][0][field] = BLOBS[shape]

    findings = module.Findings()
    module.check_custody_rederivations(findings, "probe", doc)

    codes = module.codes_of(findings.errors)
    assert "embedded-original-content" in codes, (
        f"a {shape} blob in custody_rederivations[0].{field} was not caught — "
        f"the walk no longer reaches every free string in the entry, which is "
        f"the guard the sibling siting owed (task 3.5)"
    )
    assert any(f"custody_rederivations[0].{field}" in line
               for line in findings.errors), (
        "the finding does not name the field it fired on"
    )


@pytest.mark.parametrize("field", ("previous_sha256", "observed_sha256"))
def test_the_walk_skips_the_two_digests(field: str) -> None:
    """A 64-hex digest is a long opaque value the entry legitimately carries."""
    module = _load()
    doc = yaml.safe_load(WITHHELD.read_text(encoding="utf-8"))
    doc["custody_rederivations"][0][field] = hashlib.sha256(b"x").hexdigest()

    findings = module.Findings()
    module.check_custody_rederivations(findings, "probe", doc)
    assert "embedded-original-content" not in module.codes_of(findings.errors)


def test_the_withheld_exit_status_is_a_single_named_constant() -> None:
    """Brett Heap's ruling of 2026-09-09 lives in exactly one place."""
    module = _load()
    assert module.EXIT_NEEDS_DECISION == 3, (
        "the withheld exit status moved. It is Brett Heap's ruling of "
        "2026-09-09 — \"Exit 3 = needs a human decision (Recommended)\" — and "
        "it is held in ONE constant precisely so a re-ruling moves one line"
    )


def test_a_sound_content_entry_withholds_and_does_not_error() -> None:
    module = _load()
    doc = yaml.safe_load(WITHHELD.read_text(encoding="utf-8"))
    findings = module.Findings()
    module.check_custody_rederivations(findings, "probe", doc)

    assert not findings.errors, findings.errors
    assert "custody-content-class-withheld" in module.codes_of(findings.withheld)
    assert module.report(findings, strict=True) == module.EXIT_NEEDS_DECISION


def test_errors_dominate_a_withholding() -> None:
    """PRECEDENCE, confirmed by the architect 2026-09-09.

    A malformed record is not a decision for a human to take — it is a record to
    fix, and the fix belongs to whoever maintains the chain rather than to
    whoever would re-execute the instrument. So exit 1, not 3.
    """
    module = _load()
    findings = module.Findings()
    findings.withhold("custody-content-class-withheld", "probe: withholds")
    findings.error("custody-chain-broken-link", "probe: and is also malformed")
    assert module.report(findings, strict=True) == 1


def test_a_clean_record_still_exits_zero() -> None:
    module = _load()
    assert module.report(module.Findings(), strict=True) == 0


def test_a_broken_chain_does_not_withhold() -> None:
    """A `content` entry on a broken chain is a BROKEN CHAIN first.

    Withholding says "the evidence re-derived perfectly and shows the referent
    moved". That claim cannot be made about a chain whose internal legs fail, so
    the reader is sent to the break rather than to a re-execution.
    """
    module = _load()
    doc = yaml.safe_load(BROKEN.read_text(encoding="utf-8"))
    doc["custody_rederivations"][-1]["diff_class"] = "content"
    findings = module.Findings()
    module.check_custody_rederivations(findings, "probe", doc)
    assert findings.errors
    assert not findings.withheld
