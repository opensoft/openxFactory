"""THE PER-SHAPE TABLE, HELD TO THE SHAPE GUARDS IT TRACKS.

`extend-prose-tagging-target-to-pinned-capabilities` task 3.3(p): the adapter's
required-member table is CODE the resolver is reviewed with — the record never
selects the code that judges it — but it is code that can drift from the
verifiers it was measured against, so a TWO-LEG EQUIVALENCE TEST pins it over
each real `pinned_contract_manifest` record in `contracts/`, and not over
fixtures alone.

LEG A, THE RECORD LEG, entirely inside the adapter: it ACCEPTS each real record
as it stands; for every member `m` IN the table for that record's shape it
REFUSES the record with `m` removed AND NAMES `m`; and for every top-level
member of that record that is NEITHER in the table NOR the `kind:`
discriminator it STILL ACCEPTS the record without it. So the table is neither
WIDER nor NARROWER than declared. THE TABLE IS THE ONE FOR THAT RECORD: shape
(a)'s product-identity entry requires the spelling THAT record's own verifier
reads (`PRODUCT_IDENTITY_BY_PIN`, keyed by the pin id the marker named), so
`submodule_path` is a table member of `contracts/openxwallet-pin.yaml` and
`source_repository` one of its NINE non-table members — and removing either is
a different assertion, which is what the two arms below check. `kind:` is EXEMPT from the second arm and is a
member of no shape's table, because `kind: pinned_contract_manifest` is the
PRECONDITION the pinned arm gates on BEFORE any shape is selected: a record
without it is not a record of the kind a pinned target may name, so deleting it
asks about a different record rather than about the table.

LEG B, THE GUARD LEG, which is what holds the table to the VERIFIERS rather than
to itself: for each table member whose verifier exposes an IMPORTABLE,
SOURCE-FREE guard, the test imports that verifier at its FIXED, AUTHORED path —
never a path any record names — and CALLS that guard on an in-memory copy of the
record with `m` deleted, asserting it RAISES. Where the refusal is reachable only
inside `verify()` and cannot be run source-free — measured, exactly `files:`
under shape (a), once per shape-(a) verifier — the table entry carries a MEASURED
CITATION and this test RE-READS the cited line of the cited script, a read of the
verifier rather than a run of it.

NEITHER LEG ASSERTS SUFFICIENCY. The adapter's judgement is NECESSARY for the
shape's full verifier and by design NOT SUFFICIENT for it; the measured case is
`scripts/validate-openreposhape-pin.py`'s source-dependent `pin-surface-
undeclared`, which no shape guard can reach. `test_the_adapter_is_necessary_and_
not_sufficient_and_the_boundary_is_named` is where that boundary is stated.

This module also carries task 3.3(l)'s MISSING+MALFORMED matrix at the grain the
table is written — per shape, per member — beside the family-level cases in
`test_tag_hygiene_pinned_targets.py`, which assert that the finding names the
shape, the member and the root.
"""

from __future__ import annotations

import ast
import copy
import importlib.util
from pathlib import Path

import pytest
import yaml

from import_scan import imported_modules

from doc_health import pin_shapes as ps

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = REPO_ROOT / "contracts"

#: A lockfile path the one two-argument guard JOINS and never opens
#: (`validate-openspec-cli-pin.py:744`), so the guard leg stays source-free.
_PIN_PATH = CONTRACTS / "openspec-cli-pin.yaml"


def _records() -> dict:
    """Every real `pinned_contract_manifest` record this tree carries, by pin
    id. `contracts/review-lane-pin.yaml` is `kind: pinned_workflow` and is not
    one of them — the admissible set tracks the KIND, not the presence of a
    pin-shaped file."""
    found = {}
    for path in sorted(CONTRACTS.glob("*-pin.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(record, dict) and record.get("kind") == ps.KIND:
            found[path.name[: -len("-pin.yaml")]] = record
    return found


RECORDS = _records()


def _tracked_table(pin_id: str, record: dict):
    """The table for THAT record: one (member, spelling, citation) row per table
    entry, at the RECORD GRAIN.

    Both halves come from the adapter's own CODE-FIXED maps, keyed by the pin id
    and never by anything the record says: the citation from the verifier
    `TRACKED_VERIFIERS` names for that pin, and the spelling shape (a)'s
    product-identity entry requires from `required_spellings` — which reads
    `PRODUCT_IDENTITY_BY_PIN`. The two are independently authored and must agree,
    which is what the assertion below checks as it goes."""
    verifier = ps.TRACKED_VERIFIERS[pin_id]
    shape = ps.judge(record, pin_id).shape
    rows = []
    for member in shape.required:
        required = ps.required_spellings(member, pin_id)
        for index, citation in enumerate(member.citations):
            if citation.script != verifier:
                continue
            spelling = (member.spellings[index] if len(member.spellings) > 1
                        else member.spellings[0])
            assert spelling in required, (
                f"{pin_id}: the citation names {spelling} but the table "
                f"requires {required} — the two code-fixed maps disagree")
            rows.append((member, spelling, citation))
    return shape, rows


def _load_verifier(script: str):
    """The verifier at its FIXED, AUTHORED path, imported the way
    `tests/openxwallet_pin/`, `tests/openreposhape_pin/`, `tests/opendox_pin/`
    and `tests/openxdox_pin/` already import theirs. Each guards its CLI behind
    `if __name__ == "__main__":`, so the import starts no work."""
    path = REPO_ROOT / script
    spec = importlib.util.spec_from_file_location(
        path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _without(record: dict, *members: str) -> dict:
    copied = copy.deepcopy(record)
    for member in members:
        copied.pop(member, None)
    return copied


# --------------------------------------------------------------------------
# The measurement the two legs range over
# --------------------------------------------------------------------------

def test_the_admissible_set_is_the_five_records_of_that_kind():
    assert sorted(RECORDS) == ["opendox", "openreposhape", "openspec-cli",
                               "openxdox", "openxwallet"]
    workflow = yaml.safe_load(
        (CONTRACTS / "review-lane-pin.yaml").read_text(encoding="utf-8"))
    assert workflow["kind"] == "pinned_workflow"


def test_the_table_ranges_over_twenty_nine_member_entries_split_twenty_seven_two():
    """The MEASURED SPLIT, pinned as a number so a table that grew or shrank
    reds here rather than drifting: 29 member entries across the five records,
    27 of them reachable through an importable source-free guard and TWO — both
    `files` under shape (a), one per shape-(a) verifier — on the citation
    route."""
    entries = guarded = cited = 0
    for pin_id, record in RECORDS.items():
        _shape, rows = _tracked_table(pin_id, record)
        entries += len(rows)
        guarded += sum(1 for _m, _s, c in rows if c.guard)
        cited += sum(1 for _m, _s, c in rows if c.guard is None)
    assert (entries, guarded, cited) == (29, 27, 2)


def test_each_records_own_shape_is_the_one_the_measurement_named():
    assert {pin_id: ps.judge(record, pin_id).shape.key
            for pin_id, record in RECORDS.items()} == {
        "openxwallet": "a", "openreposhape": "a",
        "opendox": "b", "openxdox": "b", "openspec-cli": "c"}


def test_a_multi_spelling_entry_carries_one_citation_per_spelling():
    """The invariant `_tracked_table` reads the identity entry by: where an entry
    admits two spellings, its citations are PARALLEL to them, so the row for a
    given verifier names the spelling THAT verifier reads — and every spelling
    `PRODUCT_IDENTITY_BY_PIN` requires is one of that entry's own, so the two
    code-fixed maps cannot name different members."""
    multi = 0
    for shape in ps.SHAPES:
        for member in shape.required:
            if len(member.spellings) > 1:
                multi += 1
                assert len(member.citations) == len(member.spellings)
                assert set(ps.PRODUCT_IDENTITY_BY_PIN.values()) <= set(
                    member.spellings)
    assert multi == 1, "shape (a)'s product identity is the only such entry"
    assert set(ps.PRODUCT_IDENTITY_BY_PIN) <= set(ps.TRACKED_VERIFIERS)


# --------------------------------------------------------------------------
# LEG A — the record leg
# --------------------------------------------------------------------------

@pytest.mark.parametrize("pin_id", sorted(RECORDS))
def test_record_leg_the_adapter_accepts_each_real_record(pin_id):
    verdict = ps.judge(RECORDS[pin_id], pin_id)
    assert verdict.accepted, verdict.render()


@pytest.mark.parametrize("pin_id", sorted(RECORDS))
def test_record_leg_removing_any_table_member_refuses_and_names_it(pin_id):
    """Arm 1: the table is not WIDER than declared. THE MEMBER REMOVED IS THE
    ONE SPELLING THAT RECORD'S OWN VERIFIER READS, not an alternation of two:
    `contracts/openxwallet-pin.yaml` carries BOTH product-identity spellings, so
    an entry satisfied by either would accept it with `submodule_path` deleted
    while `verify-openxwallet-pin.py:194` refuses it — the adapter NARROWER than
    the guard it tracks, which is the exact defect this leg exists to catch."""
    record = RECORDS[pin_id]
    _shape, rows = _tracked_table(pin_id, record)
    for _member, spelling, _citation in rows:
        verdict = ps.judge(_without(record, spelling), pin_id)
        assert not verdict.accepted, f"{pin_id}: {spelling} removal accepted"
        assert verdict.names(spelling), (
            f"{pin_id}: the refusal does not name {spelling}: "
            f"{verdict.render()}")


@pytest.mark.parametrize("pin_id", sorted(RECORDS))
def test_record_leg_removing_any_other_member_still_accepts(pin_id):
    """Arm 2: the table is not NARROWER than declared. Every top-level member
    that is neither in the table nor the `kind:` discriminator may go, and the
    record still resolves at the adapter — `verify_pin:` and `schema_version:`
    among them, neither being part of the shape this grammar requires, and
    `source_repository` on `contracts/openxwallet-pin.yaml`, which is non-table
    FOR THAT RECORD because its verifier reads `submodule_path` instead."""
    record = RECORDS[pin_id]
    _shape, rows = _tracked_table(pin_id, record)
    table = {spelling for _m, spelling, _c in rows}
    others = [member for member in record
              if member != "kind" and member not in table]
    for member in others:
        verdict = ps.judge(_without(record, member), pin_id)
        assert verdict.accepted, (
            f"{pin_id}: removing the non-table member {member} refused the "
            f"record: {verdict.render()}")


def test_record_leg_ranges_over_the_thirty_eight_members_measured():
    """THE LISTS the design measured, not merely their sum: THIRTY-EIGHT
    top-level members across the five records are neither table entries nor
    `kind:`, and design D-2 / task 3.3(p) name every one of them. Asserting the
    NAMES is what makes `source_repository`'s place readable — it is non-table on
    `contracts/openxwallet-pin.yaml` (whose verifier reads `submodule_path`) and
    a TABLE member on `contracts/openreposhape-pin.yaml` (whose verifier reads
    it), which one number could not tell apart."""
    measured = {}
    for pin_id, record in RECORDS.items():
        _shape, rows = _tracked_table(pin_id, record)
        table = {spelling for _m, spelling, _c in rows}
        measured[pin_id] = sorted(m for m in record
                                  if m != "kind" and m not in table)
    assert measured == {
        "openxwallet": ["carve_commit", "contract_bundle_tag",
                        "digest_algorithm", "digest_source",
                        "pinned_by_commit_only", "resync_runbook",
                        "schema_version", "source_repository", "verify_pin"],
        "openreposhape": ["digest_algorithm", "doctrine",
                          "pinned_by_commit_only", "schema_version",
                          "source_url", "verify_pin"],
        "opendox": ["carve_commit", "migration", "resync_runbook",
                    "schema_version", "source_repository", "verify_pin"],
        "openxdox": ["carve_commit", "resync_runbook", "schema_version",
                     "source_repository", "verify_pin"],
        "openspec-cli": ["consumer_entrypoint", "dispositions",
                         "integrity_algorithm", "pinned_invocation",
                         "registry", "resync_runbook", "rollback",
                         "schema_version", "source_repository", "source_url",
                         "tarball", "verify_pin"],
    }
    assert [len(names) for names in measured.values()] .count(0) == 0
    assert sum(len(names) for names in measured.values()) == 38


def test_record_leg_the_kind_discriminator_is_exempt_and_in_no_table():
    """`kind:` is the precondition, gated on before any shape is selected, so it
    is a member of no shape's table and arm 2 does not range over it."""
    for shape in ps.SHAPES:
        assert "kind" not in {s for m in shape.required for s in m.spellings}
        assert "kind" not in {s for m in shape.optional for s in m.spellings}


# --------------------------------------------------------------------------
# LEG B — the guard leg
# --------------------------------------------------------------------------

def _call_guard(module, guard: str, record: dict):
    function = getattr(module, guard)
    if guard == "pinned_lockfile":
        # Pure despite its `pin_path` argument: it JOINS `pin_path.parent /
        # name` and opens nothing.
        return function(record, _PIN_PATH)
    return function(record)


@pytest.mark.parametrize("pin_id", sorted(RECORDS))
def test_guard_leg_each_cited_guard_refuses_the_record_without_its_member(
        pin_id):
    record = RECORDS[pin_id]
    _shape, rows = _tracked_table(pin_id, record)
    checked = 0
    for member, spelling, citation in rows:
        if citation.guard is None:
            continue
        module = _load_verifier(citation.script)
        stripped = _without(record, *member.spellings)
        with pytest.raises(Exception) as caught:
            _call_guard(module, citation.guard, stripped)
        assert type(caught.value).__name__ == "PinRefusal", (
            f"{citation.script}:{citation.guard} raised "
            f"{type(caught.value).__name__} rather than refusing")
        checked += 1
    assert checked == len([1 for _m, _s, c in rows if c.guard])


@pytest.mark.parametrize("pin_id", sorted(RECORDS))
def test_guard_leg_every_cited_line_still_reads_the_member_it_was_measured_from(
        pin_id):
    """A citation is a MEASUREMENT, so the test re-measures it: the cited line of
    the cited script still reads the member the table says it refuses. A
    verifier that moved its guard moves this test."""
    record = RECORDS[pin_id]
    _shape, rows = _tracked_table(pin_id, record)
    for _member, spelling, citation in rows:
        line = (REPO_ROOT / citation.script).read_text(
            encoding="utf-8").splitlines()[citation.line - 1]
        assert f'pin.get("{spelling}")' in line, (
            f"{citation.script}:{citation.line} no longer reads {spelling}: "
            f"{line.strip()!r}")


def test_guard_leg_the_two_citation_route_entries_still_hold_their_refusal():
    """THE REMAINING TWO ARE `files` UNDER SHAPE (a), one per shape-(a)
    verifier: that refusal reads THE RECORD ALONE but sits inside `verify()`
    BEHIND the source checks, so it cannot be CALLED source-free. Its table entry
    carries a MEASURED CITATION instead, and this asserts the cited line of the
    cited script still holds that text — a READ of the verifier rather than a run
    of it, so a verifier change moves the test."""
    cited = [(member, citation)
             for shape in ps.SHAPES for member in shape.required
             for citation in member.citations if citation.guard is None]
    assert len(cited) == 2
    for member, citation in cited:
        assert member.spellings == ("files",)
        assert citation.quote == (
            "the pin lists no `files:` members, so it pins no bytes")
        line = (REPO_ROOT / citation.script).read_text(
            encoding="utf-8").splitlines()[citation.quote_line - 1]
        assert citation.quote in line, (
            f"{citation.script}:{citation.quote_line} no longer holds the "
            f"refusal the table cites: {line.strip()!r}")
    assert sorted(c.script for _m, c in cited) == [
        "scripts/validate-openreposhape-pin.py",
        "scripts/verify-openxwallet-pin.py"]


def test_the_adapter_is_necessary_and_not_sufficient_and_the_boundary_is_named():
    """NEITHER LEG ASSERTS SUFFICIENCY, and this is where that is stated.

    `pinned_by_commit_only:` is NOT shape-guard-required — both shape-(a)
    verifiers read it with an absent-is-empty default — so the adapter ACCEPTS
    `contracts/openreposhape-pin.yaml` without it. The FULL verifier does not:
    `pin-surface-undeclared` compares the declared surface against the files the
    RESOLVED SOURCE carries, and the 45 path-only entries are what keep it quiet.
    That check is SOURCE-DEPENDENT and outside this resolver's contract by
    design, so this test asserts the record RESOLVES AT THE ADAPTER and asserts
    NOTHING about what the full verifier would say about it against a real
    source — which is why the full verifier is READ here and never run."""
    record = RECORDS["openreposhape"]
    assert "pinned_by_commit_only" in record
    assert ps.judge(_without(record, "pinned_by_commit_only"),
                    "openreposhape").accepted
    source = (REPO_ROOT / "scripts"
              / "validate-openreposhape-pin.py").read_text(encoding="utf-8")
    assert "pin-surface-undeclared" in source
    assert "source.paths()" in source
    # ...and the same shape of negative for the published artifact.
    assert ps.judge(_without(RECORDS["openspec-cli"], "dispositions"),
                    "openspec-cli").accepted


# --------------------------------------------------------------------------
# (l) — the MISSING + MALFORMED matrix, per shape and per member
# --------------------------------------------------------------------------

def _base(shape_key: str) -> dict:
    if shape_key == "a":
        return {"kind": ps.KIND, "revision_kind": "commit", "commit": "0" * 40,
                "submodule_path": "productX",
                "files": [{"path": "contracts/manifest.yaml",
                           "sha256": "a" * 64}],
                "pinned_by_commit_only": ["docs/README.md"]}
    if shape_key == "b":
        return {"kind": ps.KIND, "revision_kind": "commit", "commit": "0" * 40,
                "submodule_path": "productX", "digest_algorithm": "sha256",
                "digest_definition": "sorted-ls-tree-r-v1",
                "digests": {"tree_sha256": "a" * 64}}
    integrity = "sha512-" + "A" * 86 + "=="
    return {"kind": ps.KIND, "revision_kind": "package_integrity",
            "version": "1.12.0", "integrity": integrity, "shasum": "b" * 40,
            "package": "@vendor/product",
            "lockfile": "product.package-lock.json",
            "lockfile_integrity": integrity, "lockfile_packages": 80,
            "binary": "product"}


MALFORMED = {
    "revision_kind": "tag",
    "commit": "abc123",
    "submodule_path": "",
    "source_repository": "noslash",
    "files": [{"path": "contracts/manifest.yaml"}],
    "digest_algorithm": "sha1",
    "digest_definition": "some-other-definition-v2",
    "digests": "not a mapping",
    "version": "^1.12.0",
    "integrity": "sha512-not base64",
    "shasum": "not-forty-hex",
    "package": "Not A Package",
    "lockfile": "nested/product.package-lock.json",
    "lockfile_integrity": "sha512-not base64",
    "lockfile_packages": "many",
    "binary": "bin/product",
}


@pytest.mark.parametrize("shape_key", ["a", "b", "c"])
def test_every_required_member_of_every_shape_is_refused_missing(shape_key):
    """One MISSING case per shape-guard-required member, and the POSITIVE first
    so the matrix cannot pass vacuously over a base the adapter already
    refuses."""
    shape = {s.key: s for s in ps.SHAPES}[shape_key]
    base = _base(shape_key)
    assert ps.judge(base).accepted, ps.judge(base).render()
    for member in shape.required:
        verdict = ps.judge(_without(base, *member.spellings))
        assert not verdict.accepted
        assert verdict.names(member.spellings[0]), verdict.render()


@pytest.mark.parametrize("shape_key", ["a", "b", "c"])
def test_every_required_member_of_every_shape_is_refused_malformed(shape_key):
    """One MALFORMED case per member, because "present" is not the test — the
    scenario requires each member PRESENT AND OF THE FORM ITS SHAPE GUARD
    REQUIRES. The two shape-(b) definition members matter for their own reason:
    each verifier refuses a value other than the one it implements, a definition
    it cannot compute being an unanswerable question rather than a finding about
    a tree."""
    shape = {s.key: s for s in ps.SHAPES}[shape_key]
    base = _base(shape_key)
    for member in shape.required:
        spelling = member.spellings[0]
        broken = copy.deepcopy(base)
        broken[spelling] = MALFORMED[spelling]
        verdict = ps.judge(broken)
        assert not verdict.accepted, f"{shape_key}/{spelling} accepted"
        assert verdict.names(spelling), verdict.render()


def test_the_nested_tree_digest_is_its_own_missing_and_malformed_case():
    base = _base("b")
    without = copy.deepcopy(base)
    without["digests"] = {"other": "value"}
    assert ps.judge(without).names("digests.tree_sha256")
    broken = copy.deepcopy(base)
    broken["digests"] = {"tree_sha256": "not-sixty-four-hex"}
    assert ps.judge(broken).names("digests.tree_sha256")


def test_shape_a_judges_its_two_lists_by_two_rules_and_not_by_one():
    """The scenario *A source pin enumerates its members in two different
    forms*: `files:` entries are MAPPINGS carrying a `path` and its `sha256`,
    `pinned_by_commit_only:` entries are PATH-ONLY STRINGS, and a test demanding
    a digest of the second would reject `contracts/openxwallet-pin.yaml:104-110`
    itself."""
    base = _base("a")
    assert ps.judge(base).accepted

    # a `files:` entry that is a mapping carrying NO `sha256` is REFUSED
    broken = copy.deepcopy(base)
    broken["files"] = [{"path": "contracts/manifest.yaml"}]
    assert ps.judge(broken).names("files")
    # ...and one that is not a mapping at all
    broken["files"] = ["contracts/manifest.yaml"]
    assert ps.judge(broken).names("files")
    # ...and an empty list, and a non-sequence
    for value in ([], {"path": "x"}, "contracts/manifest.yaml"):
        broken["files"] = value
        assert ps.judge(broken).names("files")

    # a `pinned_by_commit_only:` entry that is a PATH-ONLY STRING is ACCEPTED
    accepted = copy.deepcopy(base)
    accepted["pinned_by_commit_only"] = ["docs/a.md", "docs/b.md"]
    assert ps.judge(accepted).accepted
    # ...ABSENT is accepted too, and is NOT reported as a missing member
    assert ps.judge(_without(base, "pinned_by_commit_only")).accepted
    # ...a MAPPING entry is the wrong form and is REFUSED
    for value in ([{"path": "docs/a.md"}], {"a": 1}, "docs/a.md"):
        broken = copy.deepcopy(base)
        broken["pinned_by_commit_only"] = value
        assert ps.judge(broken).names("pinned_by_commit_only"), value


def test_pinned_by_commit_only_treats_every_falsey_value_as_empty():
    """(PR #1040 fix round 1, R4). Both shape-(a) verifiers read
    `pin.get("pinned_by_commit_only") or []` (`verify-openxwallet-pin.py:443`,
    `validate-openreposhape-pin.py:487`): every FALSEY value — not only
    absence — is EMPTY and admitted, so an adapter refusing `None` or `""`
    would be WIDER than the guard it tracks. `None` and `[]` are ACCEPTED; a
    mapping and a scalar string are still refused, MALFORMED, neither being a
    list."""
    base = _base("a")
    assert ps.judge(dict(base, pinned_by_commit_only=None)).accepted
    assert ps.judge(dict(base, pinned_by_commit_only=[])).accepted
    for value in ({"a": 1}, "docs/a.md"):
        verdict = ps.judge(dict(base, pinned_by_commit_only=value))
        assert not verdict.accepted
        assert any(f.member == "pinned_by_commit_only" and f.defect == ps.MALFORMED
                   for f in verdict.failures), verdict.render()


def test_shape_c_judges_dispositions_as_absent_is_empty_and_refuses_a_non_list():
    base = _base("c")
    assert ps.judge(base).accepted                      # absent
    accepted = dict(base, dispositions=[])
    assert ps.judge(accepted).accepted                  # present and empty
    refused = dict(base, dispositions="not a list")
    assert ps.judge(refused).names("dispositions")


def test_dispositions_null_is_accepted_and_a_mapping_is_refused_malformed():
    """(PR #1040 fix round 1, R5). `validate-openspec-cli-pin.py:801-803`
    treats `raw is None` as empty (`if raw is None: return []`), so an adapter
    refusing `dispositions: null` would be WIDER than the guard it tracks."""
    base = _base("c")
    assert ps.judge(dict(base, dispositions=None)).accepted
    verdict = ps.judge(dict(base, dispositions={"a": 1}))
    assert not verdict.accepted
    assert any(f.member == "dispositions" and f.defect == ps.MALFORMED
               for f in verdict.failures), verdict.render()


def test_the_product_identity_entry_has_two_regimes_keyed_on_the_pin_id():
    """Shape (a)'s entry is EXACTLY ONE product-identity member, and AT THE
    RECORD GRAIN it resolves to that record's own verifier's set — which the
    adapter reaches through its own code-fixed `PRODUCT_IDENTITY_BY_PIN`, keyed
    by the pin id the marker named, never by a member of the record.

    KNOWN PIN: that spelling and no other. The record carrying only the OTHER
    spelling is refused naming the one its verifier reads, and the other
    spelling is a non-table member — present or absent, it changes nothing.

    UNKNOWN PIN — a fixture, an added `contracts/<anything>-pin.yaml`, a future
    product this checker has measured no guards for: the ALTERNATION, because
    neither spelling can be preferred without a verifier to prefer it by. Either
    satisfies the entry and a record carrying NEITHER is refused, which is the
    INTERSECTION the design names ("would admit a record naming no product at
    all"). The UNION is refused in both regimes: no record must carry both.
    """
    assert ps.PRODUCT_IDENTITY_BY_PIN == {"openxwallet": "submodule_path",
                                          "openreposhape": "source_repository"}
    neither = _without(_base("a"), "submodule_path")
    submodule = dict(neither, submodule_path="productX")
    host = dict(neither, source_repository="opensoft/productX")

    # KNOWN PIN — the submodule-mounted one
    assert ps.judge(submodule, "openxwallet").accepted
    assert ps.judge(host, "openxwallet").names("submodule_path")
    assert not ps.judge(host, "openxwallet").accepted
    assert ps.judge(dict(submodule, source_repository="opensoft/productX"),
                    "openxwallet").accepted
    # ...and a `source_repository` of the WRONG form is not judged at all for
    # this pin: its verifier never reads that member.
    assert ps.judge(dict(submodule, source_repository="noslash"),
                    "openxwallet").accepted

    # KNOWN PIN — the host-resolved one
    assert ps.judge(host, "openreposhape").accepted
    assert ps.judge(submodule, "openreposhape").names("source_repository")
    assert ps.judge(dict(host, source_repository="noslash"),
                    "openreposhape").names("source_repository")

    # UNKNOWN PIN — the alternation
    for unknown in (None, "some-future-product"):
        assert ps.judge(submodule, unknown).accepted
        assert ps.judge(host, unknown).accepted
        assert not ps.judge(neither, unknown).accepted
        assert ps.judge(neither, unknown).names(
            "submodule_path or source_repository")
        assert ps.judge(dict(neither, source_repository="noslash"),
                        unknown).names("source_repository")


def test_an_unknown_pin_carrying_both_identity_spellings_is_accepted_not_refused():
    """(PR #1040 round 4, RULED STANDS.) D-2's "EXACTLY ONE product-identity
    member" describes the TABLE ENTRY — the required set holds one such member,
    resolved per record — not a prohibition on a record CARRYING the other
    spelling as an extra top-level member. "The UNION would refuse
    openxwallet-pin.yaml" is about REQUIRING both, not about refusing their
    co-presence: the real openxwallet record carries BOTH spellings today, and
    neither shape-(a) verifier refuses a record for carrying the one it does not
    read. An adapter refusing a both-present record would therefore be WIDER
    than the guards, which is the defect the two-leg test forbids. For an
    UNKNOWN pin the alternation admits either or both and refuses only
    NEITHER."""
    record = dict(_base("a"), submodule_path="vendor/x",
                  source_repository="opensoft/x")
    assert ps.judge(record, pin_id="fixture-unknown").accepted
    assert ps.judge(record).accepted
    neither = {k: v for k, v in record.items()
               if k not in ("submodule_path", "source_repository")}
    verdict = ps.judge(neither, pin_id="fixture-unknown")
    assert not verdict.accepted and verdict.names("submodule_path or source_repository")


def test_a_record_matching_no_shape_and_an_unknown_revision_kind_are_invalid():
    """AND the UNKNOWN cases. `contracts/evil-pin.yaml` carrying `kind`,
    `revision_kind: commit` and a well-formed `commit` AND NOTHING ELSE
    satisfies a top-level-referent check, matches NEITHER commit-pinned shape,
    and MUST NOT resolve a pinned target — a file added to `contracts/` cannot
    admit an arbitrary pinned target by carrying a label or a partial member
    set."""
    evil = {"kind": ps.KIND, "revision_kind": "commit", "commit": "0" * 40}
    verdict = ps.judge(evil)
    assert not verdict.accepted
    assert {failure.shape for failure in verdict.failures} == {
        ps.SHAPE_A.title, ps.SHAPE_B.title}

    unknown = dict(_base("a"), revision_kind="snapshot")
    assert ps.judge(unknown).names("revision_kind")
    assert ps.judge({"kind": ps.KIND}).names("revision_kind")
    assert not ps.judge("not a mapping").accepted


def test_the_mixed_record_is_refused_naming_both_shapes_tried():
    """A record carrying BOTH a whole-tree `digests.tree_sha256` AND a `files:`
    list matches neither (a) nor (b): `neutral-product-pin`'s ratified text is
    SILENT on the whole-tree shape, so the mixture is admitted by no text and
    fails closed on that capability's own refusal rule rather than resolving on
    the strength of whichever half is complete."""
    mixed = dict(_base("b"), files=[{"path": "contracts/manifest.yaml",
                                     "sha256": "a" * 64}])
    verdict = ps.judge(mixed)
    assert not verdict.accepted
    assert [(failure.shape, failure.member, failure.defect)
            for failure in verdict.failures] == [
        (ps.SHAPE_A.title, "digests.tree_sha256", ps.MIXED),
        (ps.SHAPE_B.title, "files", ps.MIXED)]


# --------------------------------------------------------------------------
# the enumeration prerequisite, at the adapter grain
# --------------------------------------------------------------------------

def test_the_enumeration_is_one_named_member_and_not_a_search():
    """The resolver reads ONE member and nothing else: it does not go looking
    for `files:`, `digests:` or `pinned_members:` and read capability names out
    of them, because none of those is a capability list and guessing between
    them is exactly the non-determinism the prerequisite exists to remove."""
    record = _base("a")
    assert ps.enumeration(record).state == ps.ABSENT
    assert ps.enumeration(record).names == ()
    assert ps.enumeration(dict(record, capabilities=["one", "two-part"])) \
        .names == ("one", "two-part")
    for broken in ("scalar", {"a": 1}, None, [], ["Not A Name"], [3]):
        assert ps.enumeration(dict(record, capabilities=broken)).state \
            == ps.MALFORMED, broken


def test_enumeration_refuses_an_item_carrying_a_trailing_newline():
    """(PR #1040 fix round 1, R6). `CAPABILITY_RE.match` with a trailing `$`
    admits a trailing newline — `"openxwallet\\n"`, exactly what a YAML block
    scalar can carry — so the resolver must use `fullmatch` instead."""
    record = _base("a")
    item = "openxwallet\n"
    verdict = ps.enumeration(dict(record, capabilities=[item]))
    assert verdict.state == ps.MALFORMED
    assert repr(item) in verdict.detail


# --------------------------------------------------------------------------
# the adapter's own purity
# --------------------------------------------------------------------------

def test_the_adapter_reads_the_record_and_nothing_else():
    """PURE AND NON-EXECUTING, asserted structurally rather than promised: the
    module imports only the standard library names its forms need, and its
    syntax tree carries no call that could open, run or import anything. A
    record that chooses which code judges it is a record that judges itself, and
    the adapter is the one place that cannot happen.

    PARSED, NOT GREPPED, for the reason `tests/import_scan.py` gives in its own
    docstring: this module NAMES `subprocess` and `verify()` in PROSE, saying
    what it does not do, and a substring scan calls that documentation a
    violation — which makes the pressure to go green a pressure to delete true
    documentation."""
    path = REPO_ROOT / "scripts" / "doc_health" / "pin_shapes.py"
    imported = {module for module, _line in imported_modules(path)}
    assert imported <= {"base64", "binascii", "re", "dataclasses", "typing",
                        "__future__"}, imported

    # The BUILTINS a pure adapter may not reach for, matched on the bare name a
    # call to a builtin actually has. `re.compile` is an ATTRIBUTE call on an
    # imported module and is not one of these — which is why the two are checked
    # apart rather than by one name set.
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__",
                       "input", "breakpoint", "globals", "getattr", "setattr"}
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    builtin_calls = {node.func.id for node in ast.walk(tree)
                     if isinstance(node, ast.Call)
                     and isinstance(node.func, ast.Name)}
    assert not builtin_calls & forbidden_calls, builtin_calls & forbidden_calls
    # The two assertions together are the whole property: with no import outside
    # those six and no builtin escape hatch, there is nothing in this module's
    # scope that could reach a file, a process or another module — every
    # attribute call it makes is on one of those six or on a value its caller
    # handed it.
