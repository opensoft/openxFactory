"""Repo-context tests for the client-identity-roster contract family.

What lives here and why. The packaged corpus under
`examples/client-identity-roster/` proves every RECORD-INTERNAL rule: a single
file can be refused for what it says about itself. It cannot prove anything
about the repository AROUND a fragment — whether a gate obligation resolves,
whether a consent citation resolves and is in force, whether a fragment sits at
its declared placement, or what the process EXITS with. Those are measured here,
against repositories built in `tmp_path` from inline templates (the
`tests/conformance-gate/test_conformance_checks.py` `make_repo` idiom).

The eight fixture repositories, and the discrimination each belongs to:

  1. CONFORMANT, exit 0 — and deliberately the hardest clean case. It carries
     TWO fragments for TWO clients whose entries share the WHOLE uniqueness
     tuple, which is how the FRAGMENT SCOPE of uniqueness is MEASURED rather
     than asserted: a cross-fragment comparison would report them as a
     duplicate and re-kill the per-blast-radius-unit flaw from the other
     direction. It also carries a `retired` entry whose consent citation
     resolves to a TERMINATED instrument present in the repo, so the
     lifecycle exemption is measured clean. It is the discrimination partner of
     fixtures 2, 4, 6 and 8.
  2. `mutate` with no ratified capability, NONZERO — the roster delta's own
     gate-exit scenario. Its packaged sibling proves the FINDING
     record-internally; only a repo can prove the EXIT.
  3. NO fragment, exit 0 + an explicit notice — absence is never a finding, and
     no expected entry set is derived from any inventory.
  4. UNRESOLVABLE GATE OBLIGATION, nonzero. The repo carries a real gate as
     well, so the finding proves NON-RESOLUTION rather than an empty tree.
  5. MISPLACEMENT — the roster kind at `tenants/stray.yaml`, outside
     `credentials/` entirely.
  6. UNRESOLVABLE CONSENT CITATION, nonzero. The repo carries a real instrument
     in force, so again the finding proves non-resolution and not an empty tree.
  7. NESTED MISPLACEMENT — a fragment INSIDE the declared directory but not a
     DIRECT CHILD of it, so it is invisible to the flat validating glob. This is
     the harder placement case and the arm a directory-PREFIX reading of the
     rule would leave covered by nothing; fixture 5 is caught by any reading.
  8. AN ENDED INSTRUMENT CITED BY A NON-RETIRED ENTRY, nonzero with the
     IN-FORCE code and deliberately NOT the resolution code — the citation
     RESOLVES, so the fixture can only fail for its own reason.

Plus the assertions that have no other home: the killed-flaw discrimination over
the packaged corpus in ONE run, the synthetic multi-surface representability
fixture and its own discrimination, the entry field list against the ratified
one, and the negative guarantee that no module in this feature derives an
expected entry set from any inventory.
"""

from __future__ import annotations

import ast
import copy
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate-client-identity-roster.py"
EXAMPLES = REPO_ROOT / "examples" / "client-identity-roster"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


roster = _load(SCRIPT, "validate_client_identity_roster")
SCHEMA = roster.load_yaml(roster.SCHEMA_PATH)
VALIDATOR = roster.Draft202012Validator(SCHEMA, format_checker=roster.FormatChecker())
VOCAB = roster.Vocabularies(SCHEMA)


def findings_for(doc) -> tuple[list[str], list[str]]:
    """(codes, lines) for ONE document, record-internal rules and schema."""
    return roster.record_findings(doc, VALIDATOR, VOCAB)


def run_validator(target: Path) -> subprocess.CompletedProcess:
    """The REAL measurement of an exit code: the module run as a process."""
    return subprocess.run([sys.executable, str(SCRIPT), str(target)],
                          capture_output=True, text=True)


def codes_in(stdout: str) -> set[str]:
    out = set()
    for line in stdout.splitlines():
        if line.startswith("ERROR [") and "]" in line:
            out.add(line[len("ERROR ["):line.index("]")])
    return out


# --------------------------------------------------------------------------
# repository builder
# --------------------------------------------------------------------------

TENANT = "11111111-1111-1111-1111-111111111111"
OTHER_TENANT = "22222222-2222-2222-2222-222222222222"


def entry(**over) -> dict:
    base = {
        "identity_ref": "demo-bc-identity",
        "identity_kind": "entra_app_registration",
        "home_tenant": TENANT,
        "principal_locations": [TENANT],
        "residency_model": "client_tenant_single",
        "admission_surface": "business_central",
        "duty": "observing",
        "blast_radius_unit": "unit_a",
        "authority_class_intended": "observe",
        "authority_class_achieved": "observe",
        "granted_permissions": [
            {"id": "Demo.Read.All", "achieves": "observe",
             "reaches": ["business_central"]},
        ],
        "admission": [
            {"surface": "business_central",
             "act": "per-environment application user created",
             "achieved_scope": "Unit A environment",
             "enforcement_mode": "provider_enforced",
             "evidence_ref": {"repo": "opensoft/DemoxFactory",
                              "path": "tenants/demo-admission-evidence-v1.yaml"},
             "verified_at": "2026-08-01T00:00:00Z",
             "exceeds_governed_unit": False},
        ],
        "per_unit_principal_available": {"business_central": True},
        "lifecycle_state": "enrolled",
        "standing_credential_attestation": {
            "no_standing_credential": True,
            "attested_at": "2026-08-01T00:00:00Z",
        },
        "ratified_by": "demoxfactory:demo-observation-capability",
        "consent_ref": "demo-consent-v1",
    }
    base.update(over)
    return base


def fragment(client_ref: str, entries: list[dict], *,
             units: dict | None = None, duties: dict | None = None) -> dict:
    return {
        "schema_version": 1,
        "kind": "xfactory_client_identity_roster",
        "client_ref": client_ref,
        "client_tenant": TENANT,
        "domain": "demoxfactory",
        "legend": {
            "blast_radius_units": units or {"unit_a": "Unit A"},
            "duties": duties or {"observing": "Read-only observation"},
        },
        "entries": entries,
    }


def instrument(instrument_id: str, status: str) -> dict:
    # Only the three fields the roster validator reads. Consent-instrument
    # conformance is that family's own validator's business; this fixture
    # exists to be RESOLVED against, nothing more.
    return {"schema_version": 1, "kind": "xfactory_consent_instrument",
            "instrument_id": instrument_id, "status": status}


WORKFLOW = {
    "schema_version": 1,
    "kind": "xfactory_workflow",
    "workflow": {
        "id": "demo_workflow",
        "gates": [
            {"id": "demo_out_of_unit_refusal", "description": "refuses an out-of-unit target"},
            {"id": "demo_change_review", "description": "review gate"},
        ],
    },
}


def make_repo(tmp_path: Path, name: str, files: dict[str, dict]) -> Path:
    """Write `{relative path: document}` into a fresh repository directory."""
    root = tmp_path / name
    for rel, doc in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
    root.mkdir(parents=True, exist_ok=True)
    return root


PLACEMENT = "credentials/client-identity-roster"


# --------------------------------------------------------------------------
# fixture 1 — conformant, and the hardest clean case
# --------------------------------------------------------------------------

def conformant_files() -> dict[str, dict]:
    excess_entry = entry(declared_excess={
        "provider_reason": "no narrower selector exists on this act",
        "bound_mechanism": "the deterministic surface refuses out-of-unit targets",
        "gate_obligation": "demo_out_of_unit_refusal",
        "enforcement_test_ref": "tests/demo/test_out_of_unit_refusal.py",
    })
    retired = entry(identity_ref="demo-bc-identity-retired",
                    blast_radius_unit="unit_b",
                    lifecycle_state="retired",
                    consent_ref="demo-consent-ended-v1")
    twin = entry()  # the SAME whole tuple, in ANOTHER client's fragment
    return {
        # Two fragments, two clients, entries sharing the WHOLE tuple.
        f"{PLACEMENT}/client-a.yaml": fragment(
            "client-a", [excess_entry, retired],
            units={"unit_a": "Unit A", "unit_b": "Unit B"}),
        f"{PLACEMENT}/client-b.yaml": fragment("client-b", [twin]),
        "workflows/demo.yaml": WORKFLOW,
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
        "consent/demo-consent-ended.yaml": instrument("demo-consent-ended-v1",
                                                      "terminated"),
    }


def test_fixture_1_conformant_repo_exits_zero(tmp_path):
    """Exit 0 — including the two-client identical-tuple pair and the retired
    entry citing a terminated instrument. This is the discrimination partner of
    fixtures 2, 4, 6 and 8: everything they break resolves here."""
    repo = make_repo(tmp_path, "conformant", conformant_files())
    result = run_validator(repo)
    assert result.returncode == 0, result.stdout
    assert "2 roster record(s) checked" in result.stdout
    assert not codes_in(result.stdout)


def test_fixture_1_uniqueness_is_scoped_within_a_fragment(tmp_path):
    """The measurement that guards the per-blast-radius-unit flaw from the
    OTHER direction: two clients' entries with the SAME whole tuple are not a
    duplicate, because the tuple carries no client and the legend binds free
    tokens per fragment."""
    repo = make_repo(tmp_path, "scoped", conformant_files())
    a = yaml.safe_load((repo / PLACEMENT / "client-a.yaml").read_text())
    b = yaml.safe_load((repo / PLACEMENT / "client-b.yaml").read_text())
    key_a = roster.identity_key(a["domain"], a["entries"][0])
    key_b = roster.identity_key(b["domain"], b["entries"][0])
    assert key_a == key_b, "the fixture must actually share the whole tuple"
    assert "duplicate-identity-key" not in codes_in(run_validator(repo).stdout)


def test_fixture_1_retired_entry_may_cite_an_ended_instrument(tmp_path):
    """The lifecycle exemption, measured clean rather than asserted: the
    ratified cascade runs withdrawal or termination THROUGH to retirement while
    the record is kept, so an ended instrument is the EXPECTED state beside a
    retired entry."""
    repo = make_repo(tmp_path, "retired-ok", conformant_files())
    out = run_validator(repo).stdout
    assert "consent-instrument-not-in-force" not in codes_in(out)
    assert "unresolvable-consent-citation" not in codes_in(out)


# --------------------------------------------------------------------------
# fixture 2 — the gate EXIT a packaged file cannot prove
# --------------------------------------------------------------------------

def test_fixture_2_mutate_without_ratified_capability_exits_nonzero(tmp_path):
    bad = entry(identity_ref="demo-bc-writer",
                authority_class_intended="mutate",
                authority_class_achieved="mutate",
                granted_permissions=[{"id": "Demo.ReadWrite.All",
                                      "achieves": "mutate",
                                      "reaches": ["business_central"]}],
                ratified_by="demo-mutation-capability")
    repo = make_repo(tmp_path, "no-capability", {
        f"{PLACEMENT}/client-a.yaml": fragment("client-a", [bad]),
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "mutate-without-ratified-capability" in codes_in(result.stdout)


# --------------------------------------------------------------------------
# fixture 3 — absence, and the negative guarantee
# --------------------------------------------------------------------------

def test_fixture_3_no_fragment_exits_zero_with_an_explicit_notice(tmp_path):
    repo = make_repo(tmp_path, "no-fragment", {"workflows/demo.yaml": WORKFLOW})
    result = run_validator(repo)
    assert result.returncode == 0, result.stdout
    assert "absence:" in result.stdout
    assert "publishes no credentials/client-identity-roster/ directory" in result.stdout
    assert "0 roster record(s) checked" in result.stdout


def test_fixture_3b_empty_placement_directory_also_exits_zero(tmp_path):
    """The directory present and empty is the same non-finding as the directory
    absent — the complement of the absence case, so neither arm can regress
    into a completeness rule unnoticed."""
    repo = make_repo(tmp_path, "empty-placement", {"workflows/demo.yaml": WORKFLOW})
    (repo / PLACEMENT).mkdir(parents=True)
    result = run_validator(repo)
    assert result.returncode == 0, result.stdout
    assert "publishes no fragment" in result.stdout


# --------------------------------------------------------------------------
# fixture 4 — an unresolvable gate obligation
# --------------------------------------------------------------------------

def test_fixture_4_unresolvable_gate_obligation_exits_nonzero(tmp_path):
    bad = entry(declared_excess={
        "provider_reason": "no narrower selector exists on this act",
        "bound_mechanism": "the deterministic surface refuses out-of-unit targets",
        "gate_obligation": "demo_gate_that_does_not_exist",
        "enforcement_test_ref": "tests/demo/test_out_of_unit_refusal.py",
    })
    repo = make_repo(tmp_path, "unresolvable-gate", {
        f"{PLACEMENT}/client-a.yaml": fragment("client-a", [bad]),
        # A REAL gate is present, so the finding proves non-resolution rather
        # than an empty workflows/ tree.
        "workflows/demo.yaml": WORKFLOW,
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "unresolvable-gate-obligation" in codes_in(result.stdout)
    assert "demo_out_of_unit_refusal" in result.stdout, \
        "the finding must show the gates it DID find, or it cannot be told " \
        "apart from an empty tree"


# --------------------------------------------------------------------------
# fixtures 5 and 7 — the two arms of misplacement
# --------------------------------------------------------------------------

def test_fixture_5_misplaced_outside_credentials_exits_nonzero(tmp_path):
    repo = make_repo(tmp_path, "stray", {
        "tenants/stray.yaml": fragment("client-a", [entry()]),
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "misplaced-roster-instance" in codes_in(result.stdout)
    assert "tenants/stray.yaml" in result.stdout


def test_fixture_7_nested_instance_is_misplaced_and_not_merely_unvalidated(tmp_path):
    """The HARDER placement arm. A directory-PREFIX reading of the rule would
    tolerate this file in the sweep, and the flat validating glob would never
    reach it — covered by nothing. The predicate is EXACT-PATH, so the two
    passes are exact complements over one `*.y*ml` universe."""
    repo = make_repo(tmp_path, "nested", {
        f"{PLACEMENT}/sub/client-a.yaml": fragment("client-a", [entry()]),
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "misplaced-roster-instance" in codes_in(result.stdout)
    assert "sub/client-a.yaml" in result.stdout
    # And it is genuinely invisible to the validating pass, which is why the
    # sweep has to catch it.
    assert "0 roster record(s) checked" in result.stdout


# --------------------------------------------------------------------------
# fixtures 6 and 8 — the two arms of consent resolution
# --------------------------------------------------------------------------

def test_fixture_6_unresolvable_consent_citation_exits_nonzero(tmp_path):
    bad = entry(consent_ref="demo-consent-that-does-not-exist")
    repo = make_repo(tmp_path, "unresolvable-consent", {
        f"{PLACEMENT}/client-a.yaml": fragment("client-a", [bad]),
        # A real instrument IS present, so the finding proves non-resolution.
        "consent/demo-consent-v1.yaml": instrument("demo-consent-v1", "executed"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "unresolvable-consent-citation" in codes_in(result.stdout)
    assert "consent-instrument-not-in-force" not in codes_in(result.stdout)


def test_fixture_8_ended_instrument_cited_by_a_non_retired_entry(tmp_path):
    """Fails for its OWN reason and no other: this citation RESOLVES, so the
    resolution code cannot fire and only the lifecycle-scoped in-force rule can.
    Its partner is fixture 1's retired entry, which cites the same instrument
    and is clean."""
    bad = entry(lifecycle_state="enrolled", consent_ref="demo-consent-ended-v1")
    repo = make_repo(tmp_path, "ended-instrument", {
        f"{PLACEMENT}/client-a.yaml": fragment("client-a", [bad]),
        "consent/demo-consent-ended.yaml": instrument("demo-consent-ended-v1",
                                                      "terminated"),
    })
    result = run_validator(repo)
    assert result.returncode == 1, result.stdout
    assert "consent-instrument-not-in-force" in codes_in(result.stdout)
    assert "unresolvable-consent-citation" not in codes_in(result.stdout)


# --------------------------------------------------------------------------
# 4.6 — THE KILLED-FLAW DISCRIMINATION, in ONE run over the packaged corpus
# --------------------------------------------------------------------------

def test_discrimination_per_unit_and_duty_pairs_pass_while_the_alias_pair_is_refused():
    """SC-002, as a single test so that a rule broad enough to catch all three
    cannot pass. The two GENUINE pairs live in one packaged fragment and the
    ALIAS pair in one packaged negative; all three are adjudicated here, by one
    validator, in one run.

    A rule that ignored `achieved_scope` would refuse the per-unit pair. A rule
    that ignored `granted_permissions` or `duty_separation_rationale` would
    refuse the duty pair. A rule requiring more than the three ratified
    predicates would let the alias pair through. Only the ratified conjunction
    produces these three verdicts together.
    """
    ledgerx = roster.load_yaml(
        EXAMPLES / "client-identity-roster-farheap-ledgerx.example.yaml")
    alias = roster.load_yaml(
        EXAMPLES / "negative" / "alias-pair-observationally-identical.yaml")

    entries = ledgerx["entries"]
    by_ref_and_unit = {(e["identity_ref"], e["blast_radius_unit"]): e for e in entries}

    # The GENUINE PER-UNIT PAIR: one identity, two governed units, differing in
    # achieved scope.
    per_unit = [e for e in entries
                if e["identity_ref"] == "ledgerx-farheap-bc-provisioner"]
    assert len(per_unit) == 2, by_ref_and_unit.keys()
    assert per_unit[0]["blast_radius_unit"] != per_unit[1]["blast_radius_unit"]
    assert roster.admission_set(per_unit[0]) != roster.admission_set(per_unit[1])

    # The GENUINE DUTY PAIR: same governed unit, different duty, different
    # permissions, and each declaring the rationale.
    duty_pair = [e for e in entries if e["blast_radius_unit"] == "lx_rehearsal_01"]
    assert len(duty_pair) == 2
    assert duty_pair[0]["duty"] != duty_pair[1]["duty"]
    assert roster.permission_set(duty_pair[0]) != roster.permission_set(duty_pair[1])
    assert all(e.get("duty_separation_rationale") for e in duty_pair)

    # VERDICT 1 and 2 — both genuine pairs, ZERO findings, in one document.
    codes, lines = findings_for(ledgerx)
    assert codes == [], lines

    # VERDICT 3 — the alias pair, REFUSED, in the same run of the same rules.
    alias_codes, alias_lines = findings_for(alias)
    assert "alias-pair-observationally-identical" in alias_codes, alias_lines

    # And the alias pair really is the near-miss: it differs from a genuine
    # pair only by having nothing that distinguishes it.
    a, b = alias["entries"]
    assert roster.permission_set(a) == roster.permission_set(b)
    assert roster.admission_set(a) == roster.admission_set(b)
    assert not a.get("duty_separation_rationale")
    assert not b.get("duty_separation_rationale")


def test_discrimination_a_rationale_alone_cures_the_alias_pair():
    """The third predicate, measured on its own. The alias negative is
    observationally identical AND differs solely in a free token, so only the
    absence of a `duty_separation_rationale` is holding the finding up —
    declaring one makes the same record clean. Without this, the packaged corpus
    exercises predicates 1 and 2 only, because every genuine packaged pair
    already fails predicate 1."""
    alias = roster.load_yaml(
        EXAMPLES / "negative" / "alias-pair-observationally-identical.yaml")
    cured = copy.deepcopy(alias)
    cured["entries"][0]["duty_separation_rationale"] = \
        "the two units are governed separately by ratified policy"
    codes, lines = findings_for(cured)
    assert codes == [], lines


# --------------------------------------------------------------------------
# 4.9 — the synthetic multi-surface representability fixture
# --------------------------------------------------------------------------

MULTI_SURFACE = FIXTURES / "multi-surface-reader-representability.yaml"


def test_multi_surface_representability_fixture_validates_clean():
    """Killed-flaw (a): an entry whose provider-forced reach spans a second
    admission surface, with that breadth DECLARED, validates with ZERO findings.
    The ratified requirement is CONDITIONAL, so the contract must carry the
    capability even while no in-vocabulary instance exists."""
    doc = roster.load_yaml(MULTI_SURFACE)
    codes, lines = findings_for(doc)
    assert codes == [], lines
    e = doc["entries"][0]
    assert e["admission_surface"] == "business_central"
    assert e["declared_excess"]["spanned_surfaces"] == ["exchange"]
    assert sorted(e["per_unit_principal_available"]) == ["business_central", "exchange"]
    assert sorted({a["surface"] for a in e["admission"]}) == ["business_central",
                                                              "exchange"]
    assert sorted(e["granted_permissions"][0]["reaches"]) == ["business_central",
                                                              "exchange"]


def test_multi_surface_fixture_is_refused_without_its_declaration():
    """The discrimination that proves the fixture measures the rules rather than
    passing vacuously: remove `spanned_surfaces[]` and NOTHING else, and the
    same record is refused — on the permission side AND the act side, which are
    two independent rules over the same evidence."""
    doc = roster.load_yaml(MULTI_SURFACE)
    del doc["entries"][0]["declared_excess"]["spanned_surfaces"]
    codes, lines = findings_for(doc)
    assert "undeclared-reach" in codes, lines
    assert "undeclared-act-surface" in codes, lines


def test_multi_surface_fixture_declares_itself_synthetic():
    """Ruling A-16 item 1 and the amended FR-017: this is the ONE deliberately
    hypothetical artifact in the feature, and it says so, dated, with both
    halves of the falsification cited and its authorization named."""
    header = MULTI_SURFACE.read_text(encoding="utf-8")
    header = header[:header.index("schema_version:")]
    assert "SYNTHETIC" in header
    assert "2026-08-15" in header
    assert "MUST NOT BE INSTANTIATED FROM" in header
    assert "business-central-administration/spec.md" in header
    assert "exchange-administration/spec.md" in header
    assert "amendment-record-2026-08-15b.md" in header
    # The provider_reason is a REPRESENTABILITY PLACEHOLDER naming the header,
    # never an asserted provider fact — the distinction the relocation turns on.
    reason = roster.load_yaml(MULTI_SURFACE)["entries"][0]["declared_excess"]["provider_reason"]
    assert "SYNTHETIC PLACEHOLDER" in reason
    assert "header" in reason


# --------------------------------------------------------------------------
# 1.5 — the ratified entry field list, which MUST NOT be reduced
# --------------------------------------------------------------------------

# FR-001's list, verbatim, so a later refactor cannot quietly drop
# `granted_permissions[]` or `admission[]`.
FR001_ENTRY_FIELDS = {
    "identity_ref", "identity_kind", "home_tenant", "principal_locations",
    "residency_model", "admission_surface", "duty", "blast_radius_unit",
    "authority_class_intended", "authority_class_achieved",
    "granted_permissions", "admission", "declared_excess",
    "per_unit_principal_available", "lifecycle_state",
    "standing_credential_attestation", "ratified_by", "consent_ref",
    # The enumerated additions, each of which exists because a ratified rule
    # cannot be evaluated without it.
    "provider_object_ref", "duty_separation_rationale",
    "vendor_tenant_multi_obligations",
}

FR001_OPTIONAL_ENTRY_FIELDS = {
    "declared_excess", "provider_object_ref", "duty_separation_rationale",
    "vendor_tenant_multi_obligations",
}

FR001_FRAGMENT_FIELDS = {
    "schema_version", "kind", "client_ref", "client_tenant", "domain",
    "legend", "entries",
}


def test_entry_field_list_matches_the_ratified_one():
    declared = set(SCHEMA["$defs"]["roster_entry"]["properties"])
    assert declared == FR001_ENTRY_FIELDS


def test_every_non_optional_entry_field_is_required():
    required = set(SCHEMA["$defs"]["roster_entry"]["required"])
    assert required == FR001_ENTRY_FIELDS - FR001_OPTIONAL_ENTRY_FIELDS


def test_fragment_field_list_matches_the_ratified_one():
    declared = set(SCHEMA["$defs"]["roster_fragment"]["properties"])
    assert declared == FR001_FRAGMENT_FIELDS
    assert "client_tenant" in SCHEMA["$defs"]["roster_fragment"]["required"]


def test_vendor_tenant_multi_obligations_are_required_only_by_residency():
    """The five obligations are an `if/then` on `residency_model` IN THE SCHEMA
    and not only in the validator, so a validator refactor cannot lose them —
    and residency branches on NOTHING else, in particular on no authority
    class."""
    branch = SCHEMA["$defs"]["roster_entry"]
    assert branch["if"]["properties"]["residency_model"]["const"] == "vendor_tenant_multi"
    assert branch["then"]["required"] == ["vendor_tenant_multi_obligations"]
    assert "authority_class" not in yaml.dump({"if": branch["if"],
                                               "then": branch["then"]})


# --------------------------------------------------------------------------
# SC-014 — every closed refusal names its set AND its extension route
# --------------------------------------------------------------------------

CLOSED_SET_NEGATIVES = {
    "admission-surface-out-of-vocabulary.yaml": "admission_surface",
    "destructive-authority-class.yaml": "authority_class",
    "residency-model-out-of-vocabulary.yaml": "residency_model",
    "enforcement-mode-out-of-vocabulary.yaml": "enforcement_mode",
    "lifecycle-state-out-of-vocabulary.yaml": "lifecycle_state",
    "identity-kind-out-of-vocabulary.yaml": "identity_kind",
    "drift-finding-status-out-of-vocabulary.yaml": "drift_status",
}


@pytest.mark.parametrize("name,vocab", sorted(CLOSED_SET_NEGATIVES.items()))
def test_closed_set_refusals_name_the_set_and_the_route(name, vocab):
    """SEVEN closed vocabularies, seven refusal probes — no closed set in this
    family ships without one, and each refusal names the set AND the extension
    route, because a refusal that names neither leaves a domain with nowhere to
    go."""
    codes, lines = findings_for(roster.load_yaml(EXAMPLES / "negative" / name))
    named = [ln for ln in lines
             if f"closed {vocab} vocabulary" in ln and "Extension route:" in ln]
    assert named, lines


def test_every_closed_vocabulary_has_a_registered_refusal_probe():
    """The count, asserted rather than trusted: a set added to the schema with
    no probe fails here."""
    sets_in_schema = {"admission_surface", "authority_class", "residency_model",
                      "enforcement_mode", "lifecycle_state", "identity_kind",
                      "drift_status"}
    assert set(roster.EXTENSION_ROUTE) == sets_in_schema
    assert set(CLOSED_SET_NEGATIVES.values()) == sets_in_schema


# --------------------------------------------------------------------------
# FR-016 — one negative confirmation per named rule, all sixteen homed
# --------------------------------------------------------------------------

# The rule -> home table, walked against what is actually on disk. Thirteen are
# packaged files; two are repo-shaped, because a single packaged file cannot
# express a rule about its own repository context; and ONE lives in the
# cross-domain doc-health corpus, because a rule about two domains' fragments
# cannot be expressed inside either one.
FR016_HOMES: dict[str, str] = {
    "cross-domain shared identity":
        "tests/doc-health/fixtures/client-identity-composition/",
    "undeclared reach": "packaged:undeclared-reach.yaml",
    "unverified admission act counted as access":
        "packaged:unverified-act-counted-as-access.yaml",
    "achieved authority exceeding intended without a declared excess":
        "packaged:achieved-exceeds-intended-undeclared.yaml",
    "an unresolvable gate obligation": "repo:fixture 4",
    "a missing enforcement test": "packaged:missing-enforcement-test.yaml",
    "provider-enforced claim with no per-unit principal":
        "packaged:provider-enforced-without-per-unit-principal.yaml",
    "vendor-homed registration declared client-resident":
        "packaged:vendor-homed-declared-client-resident.yaml",
    "mutate entry with no ratified capability":
        "packaged:mutate-without-ratified-capability.yaml",
    "false standing-credential attestation":
        "packaged:false-standing-credential-attestation.yaml",
    "a proposed destructive class": "packaged:destructive-authority-class.yaml",
    "out-of-vocabulary admission surface":
        "packaged:admission-surface-out-of-vocabulary.yaml",
    "an entry with no consent instrument":
        "packaged:entry-without-consent-instrument.yaml",
    "a genuine full-tuple duplicate": "packaged:full-tuple-duplicate.yaml",
    "a roster instance outside the declared placement": "repo:fixtures 5 and 7",
    "an alias pair": "packaged:alias-pair-observationally-identical.yaml",
}


def test_every_fr016_named_rule_has_a_negative_confirmation():
    assert len(FR016_HOMES) == 16
    packaged = [h.split(":", 1)[1] for h in FR016_HOMES.values()
                if h.startswith("packaged:")]
    repo_shaped = [h for h in FR016_HOMES.values() if h.startswith("repo:")]
    assert len(packaged) == 13
    assert len(repo_shaped) == 2
    for name in packaged:
        assert (EXAMPLES / "negative" / name).is_file(), name
        assert name in roster.EXPECTED_NEGATIVE_FINDINGS, name
    # The sixteenth home is the cross-domain corpus, which a later phase
    # creates; the assertion binds the moment it lands rather than being
    # silently satisfied by its absence.
    cross_domain = REPO_ROOT / FR016_HOMES["cross-domain shared identity"]
    if cross_domain.exists():
        assert any(cross_domain.rglob("*.y*ml"))


# --------------------------------------------------------------------------
# 4.7 — the negative guarantee (SC-013), asserted at SOURCE level
# --------------------------------------------------------------------------

FEATURE_MODULES = [
    REPO_ROOT / "scripts" / "validate-client-identity-roster.py",
    REPO_ROOT / "scripts" / "doc_health" / "client_identity_composition.py",
]

# Markers of an expected-entry-set derivation. Checked against CODE with
# docstrings stripped, because the modules' own prose states the guarantee and
# a naive text search would match the promise instead of a breach of it.
INVENTORY_MARKERS = ("requirements.yaml", "xfactory_credential_requirements",
                     "credential_requirements", "expected_entries",
                     "expected_entry_set", "missing_entry", "missing_entries")


def _code_without_docstrings(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)


def test_no_module_derives_an_expected_entry_set_from_any_inventory():
    """SC-013's NEGATIVE guarantee. Absence is never a finding here — not a
    missing fragment, not a missing entry — and the way that stays true is that
    no code path anywhere in this feature can even NAME an inventory to derive
    an expectation from. The checklist pass and the analyze pass should both
    look for such a path and find nothing; this test is where "and find
    nothing" is measured."""
    checked = 0
    for module in FEATURE_MODULES:
        if not module.is_file():
            continue  # a later phase's module; the assertion binds when it lands
        checked += 1
        code = _code_without_docstrings(module)
        for marker in INVENTORY_MARKERS:
            assert marker not in code, f"{module.name} names {marker!r} in code"
    assert checked, "no feature module was found to check"


# Names that WRITE. A module that never calls any of them cannot mutate a
# roster fragment, a permission set or an admission record, whatever its prose
# claims. `replace` is discriminated by ARITY rather than excluded: `str.replace`
# takes two arguments and mutates nothing, while `Path.replace(target)` takes one
# and is a rename — the loophole a bare name-denylist would leave open.
WRITE_CAPABLE_CALLS = frozenset({
    "write_text", "write_bytes", "writelines", "write", "truncate", "touch",
    "mkdir", "makedirs", "unlink", "remove", "removedirs", "rmdir", "rmtree",
    "rename", "renames", "symlink_to", "hardlink_to", "chmod", "chown",
    "copy", "copy2", "copyfile", "copytree", "move",
    "dump", "dump_all", "safe_dump", "safe_dump_all",
})

# Modules whose mere IMPORT would put a mutation or a provider call within
# reach. FR-029 forbids a provider call and SC-011 forbids a network reach, and
# both are enforced structurally here rather than by reading the code's promises.
FORBIDDEN_IMPORTS = frozenset({
    "os", "shutil", "subprocess", "socket", "http", "ftplib", "smtplib",
    "requests", "httpx", "urllib", "urllib.request", "azure", "msal",
    "msgraph", "boto3",
})


def test_no_feature_module_writes_anything_and_the_drift_path_only_records():
    """FR-027 and US6's Independent Test, measured at SOURCE LEVEL — the point
    the task list makes about this requirement is that A SCHEMA DESCRIPTION IS
    NOT A VERIFICATION. Recording a drift finding must mutate nothing: not the
    roster fragment it cites, not a permission set, not an admission record.

    The guarantee is proven three ways over every module in this feature, so a
    later author cannot reintroduce a write by a route the other two miss:

      1. no WRITE-CAPABLE call name appears (with `replace` discriminated by
         arity, so `Path.replace`'s rename cannot hide behind `str.replace`);
      2. every `open()` is a READ — no mode argument carrying `w`, `a`, `x` or
         `+` anywhere in the feature;
      3. no module imports `os`, `shutil`, `subprocess`, a network module or a
         provider SDK, so a mutation or a provider call is not merely unused but
         OUT OF REACH (FR-029, SC-011).

    The drift path is covered by the same three, which is what "reads and
    records only" means operationally: a finding is a value returned to the
    caller, never a byte written anywhere."""
    checked = 0
    for module in FEATURE_MODULES:
        if not module.is_file():
            continue
        checked += 1
        tree = ast.parse(module.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    assert root not in FORBIDDEN_IMPORTS, (
                        f"{module.name} imports {alias.name!r}, which puts a "
                        f"write or a provider call within reach")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                assert root not in FORBIDDEN_IMPORTS, (
                    f"{module.name} imports from {node.module!r}, which puts a "
                    f"write or a provider call within reach")
            elif isinstance(node, ast.Call):
                func = node.func
                name = (func.attr if isinstance(func, ast.Attribute)
                        else func.id if isinstance(func, ast.Name) else "")
                assert name not in WRITE_CAPABLE_CALLS, (
                    f"{module.name}:{node.lineno} calls {name!r} — this feature "
                    f"records findings and writes nothing (FR-027)")
                if name == "replace" and len(node.args) == 1:
                    raise AssertionError(
                        f"{module.name}:{node.lineno} calls a one-argument "
                        f"replace(), which is Path.replace's rename")
                if name == "open":
                    mode = None
                    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                        mode = node.args[1].value
                    for kw in node.keywords:
                        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                            mode = kw.value.value
                    if mode is not None:
                        assert not set(str(mode)) & set("wax+"), (
                            f"{module.name}:{node.lineno} opens for writing "
                            f"with mode {mode!r}")
    assert checked, "no feature module was found to check"


def test_the_validator_states_the_negative_guarantee_in_its_own_docstring():
    """A guarantee nobody wrote down is a guarantee the next author deletes."""
    doc = roster.__doc__ or ""
    assert "IT ENFORCES NO COMPLETENESS RULE" in doc
    assert "credentials/requirements.yaml" in doc


# --------------------------------------------------------------------------
# the self-test itself, and its five failure modes
# --------------------------------------------------------------------------

def test_packaged_corpus_self_test_is_strict_and_green():
    """Layer 1, from the outside: four positives clean, thirty-one negatives
    refused for their REGISTERED reason, detail-pinned where the code alone
    would be too coarse."""
    result = run_validator(REPO_ROOT)
    assert result.returncode == 0, result.stdout
    assert ("4 positive example(s) confirmed clean, 31 negative example(s) "
            "confirmed refused") in result.stdout


def test_every_negative_on_disk_is_registered_and_every_registration_has_a_file():
    on_disk = {p.name for p in (EXAMPLES / "negative").glob("*.yaml")}
    registered = set(roster.EXPECTED_NEGATIVE_FINDINGS)
    assert on_disk == registered
    assert len(on_disk) == 31


def test_every_negative_raises_its_registered_code_and_no_other_rule_code():
    """Fail-for-its-own-reason, measured file by file. A negative may also raise
    the generic `schema` code — the rule engine runs to completion whether or
    not the schema already refused the document, which is the whole reason the
    named refusals exist at all — but it may raise no OTHER rule's code, or it
    would be proving two things and nothing in particular."""
    for name, (code, detail) in sorted(roster.EXPECTED_NEGATIVE_FINDINGS.items()):
        codes, lines = findings_for(roster.load_yaml(EXAMPLES / "negative" / name))
        assert code in codes, f"{name}: expected {code}, got {sorted(set(codes))}"
        stray = sorted(set(codes) - {code, "schema"})
        assert not stray, f"{name} also raised {stray}"
        if detail is not None:
            assert any(f"[{code}]" in ln and detail in ln for ln in lines), \
                f"{name}: pinned detail {detail!r} missing from {lines}"


def test_a_schema_invalid_negative_still_raises_its_named_code():
    """The structural reason the rule engine runs to completion. Most of this
    corpus's negatives are ALSO schema-visible — a value outside a closed set, a
    missing admission list, a destructive class — and a raw jsonschema message
    names neither the closed vocabulary nor the extension route the refusals are
    required to name. A validator that returned at the first schema failure
    would leave those named refusals existing nowhere, and their expectations
    table entries unregisterable."""
    both = 0
    for name, (code, _) in sorted(roster.EXPECTED_NEGATIVE_FINDINGS.items()):
        codes, _lines = findings_for(roster.load_yaml(EXAMPLES / "negative" / name))
        if "schema" in codes:
            assert code in codes, (
                f"{name} is refused by the schema and its NAMED rule never "
                f"ran — the refusal would exist nowhere")
            both += 1
    assert both >= 10, f"only {both} negatives exercise the schema/rule overlap"


@pytest.fixture
def sandbox(tmp_path) -> Path:
    """A THROWAWAY copy of this checkout's validator, schema and packaged
    corpus, so the self-test's own failure modes can be broken and measured
    without touching the real corpus. The script derives its root from its own
    location, so a copy at `<tmp>/scripts/` reads `<tmp>/examples/`."""
    root = tmp_path / "sandbox"
    (root / "scripts").mkdir(parents=True)
    (root / "contracts" / "schemas").mkdir(parents=True)
    shutil.copy2(SCRIPT, root / "scripts" / SCRIPT.name)
    shutil.copy2(roster.SCHEMA_PATH,
                 root / "contracts" / "schemas" / roster.SCHEMA_PATH.name)
    shutil.copytree(EXAMPLES, root / "examples" / "client-identity-roster")
    return root


def run_sandbox(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / SCRIPT.name), str(root)],
        capture_output=True, text=True)


def test_sandbox_is_green_before_anything_is_broken(sandbox):
    """The control. Without it, each failure-mode test below could be passing
    because the copy was broken rather than because the mode fired."""
    result = run_sandbox(sandbox)
    assert result.returncode == 0, result.stdout


def test_failure_mode_a_registered_probe_with_no_file(sandbox):
    (sandbox / "examples" / "client-identity-roster" / "negative"
     / "undeclared-reach.yaml").unlink()
    out = run_sandbox(sandbox).stdout
    assert "negative-missing" in codes_in(out)


def test_failure_mode_b_file_with_no_registration(sandbox):
    neg = sandbox / "examples" / "client-identity-roster" / "negative"
    shutil.copy2(neg / "undeclared-reach.yaml", neg / "not-registered.yaml")
    out = run_sandbox(sandbox).stdout
    assert "negative-unregistered" in codes_in(out)


def test_failure_mode_c_a_negative_that_passes(sandbox):
    target = (sandbox / "examples" / "client-identity-roster" / "negative"
              / "undeclared-reach.yaml")
    target.write_text(yaml.dump(fragment("client-a", [entry()]), sort_keys=False),
                      encoding="utf-8")
    out = run_sandbox(sandbox).stdout
    assert "negative-should-fail" in codes_in(out)


def test_failure_mode_d_a_negative_that_fails_for_the_wrong_reason(sandbox):
    """The mode that matters most: a fixture still red, still failing, and
    proving something other than the rule it is registered against."""
    target = (sandbox / "examples" / "client-identity-roster" / "negative"
              / "undeclared-reach.yaml")
    doc = fragment("client-a", [entry(lifecycle_state="dormant")])
    target.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
    out = run_sandbox(sandbox).stdout
    assert "negative-wrong-reason" in codes_in(out)


def test_failure_mode_e_the_code_fires_without_its_pinned_detail(sandbox):
    """The pin is what makes a coarse code prove a specific refusal. Here the
    destructive-class code still fires — on the ACHIEVED field instead of the
    INTENDED one — and the pinned detail no longer matches, so the fixture no
    longer proves what it was registered to prove."""
    target = (sandbox / "examples" / "client-identity-roster" / "negative"
              / "destructive-authority-class.yaml")
    doc = fragment("client-a", [entry(authority_class_achieved="destroy")])
    target.write_text(yaml.dump(doc, sort_keys=False), encoding="utf-8")
    out = run_sandbox(sandbox).stdout
    assert "negative-detail-mismatch" in codes_in(out)
    # ...and it is the PIN that caught it, not the code: the code still fires.
    assert "the code alone is too coarse" in out
