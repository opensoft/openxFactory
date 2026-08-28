"""Positive + fail-closed negative coverage for ``qualify-avatar-live-voice``
§6.2 — Fork 4 Option C's two artifacts, as enforced by
``scripts/validate-avatar-client.py``:

* ``check_synthetic_evaluation_corpus`` — task 6.2.1's synthetic
  model-versus-model corpus: every scenario's failure maps to a RATIFIED
  ROLLBACK-A trigger, every class x domain cell is covered, every ratified
  trigger is reachable, and the declared coverage totals are recomputed.
* ``check_ephemeral_processing_envelope`` — tasks 6.2.2 and 6.2.4: the frozen
  three consent purposes, the four reserved retention classes, §7.9's ruled
  retention window and reference, withdrawal onto the existing ``revoked``
  outcome with a reachability proof that resolves, and the non-shadowing
  guarantee held as an OPERATIONAL control with ``enforced_by_schema: false``.

EVERY NEGATIVE IS A MUTATION OF THE REAL ARTIFACT, on the shape the sibling
``test_section7_pinned_values.py`` established: the shipped files are copied
into a tmp tree, one field is moved, and the check runs against that tree with
the module-level ``AVC`` monkeypatched to it. The positive case therefore
proves the SHIPPED artifacts pass, and each negative proves the check would
have noticed the specific edit it names.

THE MUTATION THIS MODULE EXISTS FOR is ``envelope_shadow_claimed_enforced``.
Task 6.2.4's whole content is that NO schema field forbids a second-model
shadow today and that "claiming otherwise would be false". A later editor who
flips ``enforced_by_schema`` to ``true`` would be writing exactly that false
claim into the artifact that records the guarantee, and nothing else in the
tree would notice.
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts" / "validate-avatar-client.py"
REAL_AVC = REPOSITORY_ROOT / "contracts" / "avatar-client"


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_avatar_client", ENTRYPOINT)
    assert spec and spec.loader, f"cannot load validator at {ENTRYPOINT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()

# The artifacts the §6.2 checks read. The three registries and the checklist are
# copied because BOTH checks deliberately read their facts from the surface that
# already owns them rather than from a constant here: ROLLBACK-A's trigger
# vocabulary out of the canary policy, the frozen purposes and the reserved
# retention classes out of their registries, and §7.9's retention window out of
# the checklist. A check that reads another file is only proved by having that
# file in the tree — and mutating it is itself a case worth having.
COPIED = (
    "synthetic-evaluation-corpus.yaml",
    "canary-ephemeral-processing-envelope.yaml",
    "canary-cohort-and-rollback-policy.yaml",
    "internal-live-activation-checklist.yaml",
    "registries/consent-purposes.registry.yaml",
    "registries/retention-classes.registry.yaml",
    "registries/session-outcomes.registry.yaml",
)

CORPUS = "synthetic-evaluation-corpus.yaml"
ENVELOPE = "canary-ephemeral-processing-envelope.yaml"

# Captured at import time, before any test runs — see the sibling module's note.
_BASELINE_BYTES = {name: (REAL_AVC / name).read_bytes() for name in COPIED}


@pytest.fixture(scope="session", autouse=True)
def repository_artifacts_are_never_mutated():
    """Session teardown: every mutation below edits a copy under `tmp_path`, and
    none of them may reach the repository. Order-independent by construction."""
    yield
    drifted = sorted(name for name in COPIED
                     if (REAL_AVC / name).read_bytes() != _BASELINE_BYTES[name])
    assert not drifted, (
        f"shipped artifact(s) {drifted} were MUTATED during this session; the "
        f"mutations in this module must edit the tmp tree only. Restore with "
        f"`git checkout -- contracts/avatar-client/`")


def _messages(findings) -> str:
    return "\n".join(findings.errors)


def _tree(tmp_path: Path) -> Path:
    avc = tmp_path / "avatar-client"
    avc.mkdir()
    for name in COPIED:
        target = avc / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REAL_AVC / name, target)
    return avc


def _rewrite(avc: Path, name: str, mutate: Callable[[dict], Any]) -> None:
    doc = yaml.safe_load((avc / name).read_text())
    mutate(doc)
    (avc / name).write_text(yaml.safe_dump(doc, sort_keys=False))


def _run(monkeypatch, avc: Path, check: str):
    monkeypatch.setattr(VALIDATOR, "AVC", avc)
    findings = VALIDATOR.Findings()
    if check == "corpus":
        VALIDATOR.check_synthetic_evaluation_corpus(findings)
    else:
        VALIDATOR.check_ephemeral_processing_envelope(findings)
    return findings


def _scenario(doc: dict, sid: str) -> dict:
    return next(s for s in doc["scenarios"] if s["scenario_id"] == sid)


def _shadow(doc: dict) -> dict:
    return next(c for c in doc["operational_controls"]
                if c["control"] == "single_model_on_live_canary_audio")


# ---------------------------------------------------------------------------
# The positive: the artifacts as shipped.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("check", ["corpus", "envelope"])
def test_shipped_artifacts_pass(tmp_path, monkeypatch, check):
    findings = _run(monkeypatch, _tree(tmp_path), check)
    assert findings.errors == [], _messages(findings)


def test_absent_artifacts_are_skipped_not_failed(tmp_path, monkeypatch):
    """Both checks guard on presence so the validator stays green at every phase
    checkpoint — the same discipline every sibling §7 check follows."""
    empty = tmp_path / "avatar-client"
    empty.mkdir()
    for check in ("corpus", "envelope"):
        assert _run(monkeypatch, empty, check).errors == []


# ---------------------------------------------------------------------------
# 6.2.1 — the corpus.
# ---------------------------------------------------------------------------

def test_a_trigger_outside_rollback_a_is_caught(tmp_path, monkeypatch):
    """THE CORPUS'S CENTRAL CLAIM. `evaluate_safety_signal` answers an
    unrecognised trigger with `REFUSED_UNKNOWN_TRIGGER` — a NON-tripping
    verdict — so a scenario carrying an invented trigger fails SILENTLY at
    canary time: the evaluation reports a failure and the ring does not abort."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: _scenario(d, "SEC-GEN-SAF-02")
             ["emits_on_failure"].__setitem__("trigger", "failed_safety_evaluation"))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("not one of ROLLBACK-A's ratified triggers" in e
               for e in findings.errors), _messages(findings)


def test_the_vocabulary_is_read_from_the_policy_not_mirrored(tmp_path, monkeypatch):
    """Narrowing ROLLBACK-A's trigger list IN THE POLICY must invalidate the
    corpus scenarios that emit the dropped triggers. That is the proof the check
    reads the ratified vocabulary rather than a copy inside the validator: a
    mirrored list would keep agreeing with itself."""
    avc = _tree(tmp_path)

    def narrow(doc: dict) -> None:
        entry = next(c for c in doc["rollback_policy"]["classes"]
                     if c["id"] == "ROLLBACK-A")
        entry["triggers"] = [t for t in entry["triggers"] if t != "redaction_finding"]

    _rewrite(avc, "canary-cohort-and-rollback-policy.yaml", narrow)
    findings = _run(monkeypatch, avc, "corpus")
    assert any("'redaction_finding'" in e and "not one of ROLLBACK-A" in e
               for e in findings.errors), _messages(findings)


def test_an_unreadable_policy_fails_closed(tmp_path, monkeypatch):
    """A corpus checked against nothing is a corpus that was not checked."""
    avc = _tree(tmp_path)
    (avc / "canary-cohort-and-rollback-policy.yaml").unlink()
    findings = _run(monkeypatch, avc, "corpus")
    assert any("cannot be read" in e for e in findings.errors), _messages(findings)


def test_an_uncovered_class_domain_cell_is_caught(tmp_path, monkeypatch):
    """Condition 7 requires five classes to pass for three domains. A missing
    cell is a condition-7 claim with nothing behind it."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: d.__setitem__(
        "scenarios", [s for s in d["scenarios"]
                      if s["cell"] != "handoff/LedgerxFactory"]))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("no scenario covers cell 'handoff/LedgerxFactory'" in e
               for e in findings.errors), _messages(findings)


def test_an_unreachable_ratified_trigger_is_caught(tmp_path, monkeypatch):
    """§6.3.3 proved the safety trip for all EIGHT recorded triggers. A corpus
    that can only produce seven leaves a proven path unexercised."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: d.__setitem__(
        "scenarios",
        [s for s in d["scenarios"]
         if s["emits_on_failure"]["trigger"] != "secret_scan_finding"]))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("no scenario can produce ROLLBACK-A trigger 'secret_scan_finding'"
               in e for e in findings.errors), _messages(findings)


def test_a_stale_coverage_total_is_recomputed(tmp_path, monkeypatch):
    """A summary that disagrees with its corpus is how an edited corpus keeps an
    old claim."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS,
             lambda d: d["coverage"].__setitem__("scenarios_total", 45))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("coverage.scenarios_total records 45" in e
               for e in findings.errors), _messages(findings)


def test_a_stale_per_class_count_is_recomputed(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: d["coverage"]["scenarios_by_class"]
             .__setitem__("handoff", 9))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("coverage.scenarios_by_class" in e
               for e in findings.errors), _messages(findings)


def test_a_declared_class_trigger_list_must_match_its_scenarios(tmp_path, monkeypatch):
    avc = _tree(tmp_path)

    def widen(doc: dict) -> None:
        entry = next(c for c in doc["classes"] if c["id"] == "handoff")
        entry["triggers"] = ["failed_handoff_evaluation", "redaction_finding"]

    _rewrite(avc, CORPUS, widen)
    findings = _run(monkeypatch, avc, "corpus")
    assert any("class 'handoff' declares triggers" in e
               for e in findings.errors), _messages(findings)


def test_a_corpus_that_stops_being_synthetic_is_caught(tmp_path, monkeypatch):
    """Fork 4 Option C's FIRST clause. A corpus admitting tenant data is not the
    corpus the ruling permits, whatever else it gets right."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS,
             lambda d: d["synthesis"].__setitem__("tenant_data", "sampled"))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("synthesis.tenant_data" in e for e in findings.errors), \
        _messages(findings)


def test_committed_audio_would_be_caught(tmp_path, monkeypatch):
    """Rendering to audio is a §5/canary-time act of the RUN. A corpus that
    recorded otherwise would be committing media this ring has no retention
    class for."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: d["synthesis"]["audio_synthesis"]
             .__setitem__("status", "rendered_and_committed"))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("audio_synthesis.status" in e for e in findings.errors), \
        _messages(findings)


def test_a_scenario_routed_to_the_wrong_rollback_class_is_caught(tmp_path, monkeypatch):
    """ROLLBACK-B blocks new sessions and lets in-flight legs drain. A safety
    evaluation routed there would answer a safety breach by leaving the breached
    session running."""
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: _scenario(d, "SEC-MEDX-SAF-01")
             ["emits_on_failure"].__setitem__("rollback_class", "ROLLBACK-B"))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("names rollback_class 'ROLLBACK-B'" in e
               for e in findings.errors), _messages(findings)


def test_a_signal_that_misreports_its_own_class_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS, lambda d: _scenario(d, "SEC-LEDX-BLK-01")
             ["emits_on_failure"].__setitem__("scenario_class", "safety"))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("emits scenario_class 'safety'" in e
               for e in findings.errors), _messages(findings)


def test_a_scenario_with_no_script_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, CORPUS,
             lambda d: _scenario(d, "SEC-GEN-EXV-01").__setitem__("script", []))
    findings = _run(monkeypatch, avc, "corpus")
    assert any("carries no scripted exchange" in e
               for e in findings.errors), _messages(findings)


# ---------------------------------------------------------------------------
# 6.2.4 — the non-shadowing guarantee stays OPERATIONAL.
# ---------------------------------------------------------------------------

def test_claiming_the_schema_forbids_a_shadow_is_caught(tmp_path, monkeypatch):
    """THE MUTATION THIS MODULE EXISTS FOR. No schema field forbids a
    second-model shadow today; recording `enforced_by_schema: true` would write
    the false claim task 6.2.4 exists to refuse, and it is the kind of edit that
    looks like an improvement."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: _shadow(d).__setitem__("enforced_by_schema", True))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("claiming otherwise would be false" in e
               for e in findings.errors), _messages(findings)


def test_an_unnamed_enforcing_flag_owner_is_caught(tmp_path, monkeypatch):
    """Task 6.2.4 requires the enforcing contract flag to be NAMED as
    pilot-hardening work. An unowned deferral is a gap nobody inherits."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: _shadow(d)["enforcing_contract_flag"]
             .__setitem__("owner_change", "some-future-change"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("avatar-pilot-hardening" in e for e in findings.errors), \
        _messages(findings)


def test_a_flag_marked_built_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: _shadow(d)["enforcing_contract_flag"]
             .__setitem__("status", "implemented"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("!= 'deferred'; it is not built" in e
               for e in findings.errors), _messages(findings)


def test_dropping_the_control_entirely_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d.__setitem__(
        "operational_controls",
        [c for c in d["operational_controls"]
         if c["control"] != "single_model_on_live_canary_audio"]))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("no operational control named" in e
               for e in findings.errors), _messages(findings)


# ---------------------------------------------------------------------------
# 6.2.2 — the envelope's consent, classes, retention and withdrawal.
# ---------------------------------------------------------------------------

def test_a_fourth_media_purpose_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d["consent"]["media_leg_purposes"].append(
        {"id": "avatar.evaluation_audio", "why": "invented for evaluation"}))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("media_leg_purposes" in e for e in findings.errors), \
        _messages(findings)


def test_the_purpose_count_is_read_from_the_registry(tmp_path, monkeypatch):
    """Growing the REGISTRY must make the envelope's recorded count wrong. That
    is the proof the count is recomputed rather than mirrored — and the frozen
    count of 3 is exactly what task 6.2.3 confirms by inspection."""
    avc = _tree(tmp_path)
    _rewrite(avc, "registries/consent-purposes.registry.yaml",
             lambda d: d["members"].append(
                 {"id": "avatar.evaluation_audio", "description": "invented"}))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("frozen_purpose_count" in e for e in findings.errors), \
        _messages(findings)


def test_an_evaluation_specific_purpose_admitted_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d["consent"]["new_evaluation_purpose"]
             .__setitem__("admitted", True))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("ALV-007-S03" in e for e in findings.errors), _messages(findings)


def test_a_stricter_purpose_that_falls_back_is_caught(tmp_path, monkeypatch):
    """A stricter term that silently degrades to the neutral pair was never
    obtained. The reference is optional to DECLARE, never to SATISFY."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: d["consent"]["optional_stricter_domain_purpose"]
             .__setitem__("unresolved_reference_effect", "fall_back_to_neutral"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("unresolved_reference_effect" in e
               for e in findings.errors), _messages(findings)


def test_permitting_a_reserved_retention_class_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: d["data_classes"]["permitted"].append("audio"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("data_classes.permitted" in e for e in findings.errors), \
        _messages(findings)
    assert any("reserved class" in e for e in findings.errors), \
        _messages(findings)


def test_narrowing_the_never_instantiated_list_is_caught(tmp_path, monkeypatch):
    """All FOUR reserved classes, read from the registry's own `reserved:`
    block. `video` is the one §7.9's narrower ruled list omits, so dropping it
    here is the edit that would otherwise pass unnoticed."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d["data_classes"]["never_instantiated"]
             .__setitem__("classes", ["audio", "full_transcript",
                                      "independent_transcription"]))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("the registry's reserved set" in e
               for e in findings.errors), _messages(findings)


def test_the_reserved_set_is_read_from_the_registry(tmp_path, monkeypatch):
    """Unreserving a class IN THE REGISTRY must make the envelope's list wrong,
    which is what proves the check reads the registry rather than a constant."""
    avc = _tree(tmp_path)
    _rewrite(avc, "registries/retention-classes.registry.yaml",
             lambda d: d.__setitem__(
                 "reserved", [m for m in d["reserved"] if m["id"] != "video"]))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("the registry's reserved set" in e
               for e in findings.errors), _messages(findings)


def test_a_retention_window_that_drifts_from_the_ruling_is_caught(tmp_path, monkeypatch):
    """Two artifacts carrying the same 90 days is two places for it to drift.
    The envelope cites the checklist's §7.9 block; it does not re-rule it."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: d["retention"].__setitem__("window_days", 30))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("retention.window_days" in e for e in findings.errors), \
        _messages(findings)


def test_a_retention_reference_that_drifts_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d["retention"].__setitem__(
        "policy_ref", "avatar.internal_live.canary.structured_record.retention.v2"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("retention.policy_ref" in e for e in findings.errors), \
        _messages(findings)


def test_an_invented_withdrawal_outcome_is_caught(tmp_path, monkeypatch):
    """Withdrawal maps onto the EXISTING revoked outcome. A new token would
    reopen the closed `session-outcomes` registry this change leaves alone."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: d["withdrawal"].__setitem__("maps_to_outcome", "withdrawn"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("maps_to_outcome" in e for e in findings.errors), \
        _messages(findings)
    assert any("released session-outcomes registry" in e
               for e in findings.errors), _messages(findings)


def test_withdrawal_declared_unreachable_mid_speech_is_caught(tmp_path, monkeypatch):
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE,
             lambda d: d["withdrawal"].__setitem__("reachable_mid_speech", False))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("STAY REACHABLE" in e for e in findings.errors), \
        _messages(findings)


def test_a_reachability_proof_that_does_not_resolve_is_caught(tmp_path, monkeypatch):
    """A reachability claim whose proof is a filename nobody wrote is not a
    proof. The fixture is resolved on disk and its `fixture_id` compared, so a
    rename cannot quietly orphan the citation."""
    avc = _tree(tmp_path)
    _rewrite(avc, ENVELOPE, lambda d: d["withdrawal"]["reachability_proof"]
             .__setitem__("fixture", "examples/avatar-first-ui/fixtures/"
                                     "deterministic/does-not-exist.yaml"))
    findings = _run(monkeypatch, avc, "envelope")
    assert any("the proof is a filename" in e for e in findings.errors), \
        _messages(findings)
