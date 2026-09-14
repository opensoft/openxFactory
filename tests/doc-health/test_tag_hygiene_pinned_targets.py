"""The PINNED TARGET ARM of `fam_tag_hygiene`, case by case.

`extend-prose-tagging-target-to-pinned-capabilities` (ratified 2026-09-12 and
re-ruled to FAIL CLOSED 2026-09-13 — openxFactory #992, comment 5649935136)
admits `target=pinned:<pin-id>/<capability>` in a candidate marker and resolves
it only where ALL THREE prerequisites hold. Task 3.3 lists the cases (a)-(p) the
realization owes; this module carries (a)-(o) and
`test_pin_shape_adapter.py` carries (p), the two-leg equivalence test, plus the
per-shape missing/malformed matrix (l) asks for at the member grain.

WHERE EACH CASE LIVES, AND WHY TWO KINDS OF FIXTURE. The LIVE cases — a record
that resolves, one that enumerates nothing, one that enumerates without the
name, five malformed enumerations, an unresolvable pin id, a record of another
kind, five incomplete records, five lexically malformed values and the
`supersedes` refusal — are a committed corpus under
`fixtures/tag-hygiene-pinned/`, read by ONE run of the family, exactly as
`fixtures/tag-hygiene/` drives the family's older cases. It is a SEPARATE corpus
so `test_tag_hygiene`'s own assertions over the older tree stay true, unchanged.

The cases that need a tree no repository should carry — a symlink out of
`contracts/`, a `contracts` that is itself a symlink, a corrupt record, a second
resolution root — are built in `tmp_path`. Committing a broken symlink or
invalid YAML into `tests/` would make every repository-wide sweep read it, and
the thing under test is the arm's behaviour rather than the bytes' address.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
import yaml

from conftest import AS_OF, FakeGit, make_ctx

from doc_health import DEFAULT_THRESHOLDS, ERROR
from doc_health import corpus
from doc_health import families
from doc_health.families import FAMILIES
from doc_health.runner import Context

FIXTURE_CONTRACTS = (Path(__file__).resolve().parent / "fixtures"
                     / "tag-hygiene-pinned" / "alpha" / "contracts")


# --------------------------------------------------------------------------
# harness
# --------------------------------------------------------------------------

def _context(roots: dict) -> Context:
    """A `Context` over arbitrary roots, built exactly as `conftest.make_ctx`
    builds one over a fixture family — same loader, same fields — so a tmp tree
    and a committed corpus reach the family by one route."""
    docs, capabilities, change_ids = [], {}, {}
    for name, path in roots.items():
        docs.extend(corpus.load_docs(name, path))
        capabilities[name] = corpus.spec_capabilities(path)
        change_ids[name] = corpus.change_ids(path)
    return Context(repo_paths=dict(roots), docs=docs,
                   capabilities=capabilities, change_ids=change_ids,
                   git=FakeGit(), thresholds=dict(DEFAULT_THRESHOLDS),
                   as_of=AS_OF, agg_root=None)


def _repo(root: Path, records: dict | None = None,
          docs: dict | None = None) -> Path:
    """A miniature repository: `contracts/<name>` records and `docs/<name>`
    documents. A record given as a mapping is dumped; a record given as a string
    is written verbatim, which is how the corrupt cases carry bytes no dumper
    would produce."""
    (root / "contracts").mkdir(parents=True, exist_ok=True)
    (root / "docs").mkdir(parents=True, exist_ok=True)
    for name, body in (records or {}).items():
        text = body if isinstance(body, str) else yaml.safe_dump(
            body, sort_keys=False)
        (root / "contracts" / name).write_text(text, encoding="utf-8")
    for name, body in (docs or {}).items():
        (root / "docs" / name).write_text(body, encoding="utf-8")
    return root


def _doc(*targets: str, title: str = "Fixture") -> str:
    blocks = "\n".join(
        f"<!-- xspec:candidate target={target} -->\nprose\n"
        "<!-- /xspec:candidate -->\n" for target in targets)
    return f"# {title}\n\nStatus: draft\n\n{blocks}"


def _shape_a(**extra) -> dict:
    record = {"schema_version": 1, "kind": "pinned_contract_manifest",
              "revision_kind": "commit", "commit": "0" * 40,
              "submodule_path": "productX",
              "files": [{"path": "contracts/manifest.yaml",
                         "sha256": "a" * 64}],
              "capabilities": ["wallet-carve"]}
    record.update(extra)
    return record


def _run(ctx) -> list:
    result = FAMILIES["tag-hygiene"](ctx)
    assert isinstance(result, list), "the family completed rather than skipping"
    return result


def _rules(findings, path: str | None = None) -> list[str]:
    return sorted(f.rule for f in findings
                  if path is None or f.path == path)


class _Spy:
    """Records every call and forwards to the real function — the read surface,
    instrumented. Assertions about "nothing was read" are made against
    `self.calls` rather than against a finding's text, because the boundary
    under test is that the seam was never reached."""

    def __init__(self, real):
        self.real, self.calls = real, []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.real(*args, **kwargs)


@pytest.fixture
def seams(monkeypatch):
    """The arm's three seams: the boundary precondition, the candidate
    resolution (the ONLY place a pin-record path is constructed) and the ONLY
    place a pin record is read."""
    spies = {name: _Spy(getattr(families, name))
             for name in ("boundary_dir", "resolve_in_root",
                          "_pin_record_text")}
    for name, spy in spies.items():
        monkeypatch.setattr(families, name, spy)
    return spies


@pytest.fixture(scope="module")
def corpus_findings():
    """Every finding ONE run of the family over the committed pinned corpus
    emits — the live half of cases (a)-(i) and (l)."""
    return _run(make_ctx("tag-hygiene-pinned"))


# --------------------------------------------------------------------------
# (c), (i), (l) positives, (n) second — THE TARGETS THAT RESOLVE
# --------------------------------------------------------------------------

def test_a_listed_capability_resolves_and_emits_nothing(corpus_findings):
    """(c) PRESENT AND NAMES — the only shape in which a pinned target resolves
    at all — beside (i) the unchanged in-tree form, (l)'s three shape positives
    and (n)'s second case. Six markers in one document, and the document emits
    NOTHING: the shape-(b) record carrying neither per-file list resolves and
    its absent lists are NOT reported as missing members; the shape-(c) record
    carrying no `dispositions:` resolves; the shape-(a) record carrying no
    `pinned_by_commit_only:` resolves, both verifiers reading that member with
    an absent-is-empty default, so a table demanding it would refuse a record
    those guards admit — and this case asserts only that the record RESOLVES AT
    THE ADAPTER, asserting nothing about what a full verifier would say about it
    against a real source."""
    assert _rules(corpus_findings, "docs/resolving.md") == []


def test_the_in_tree_arm_is_unchanged_and_never_judges_a_pinned_value():
    """(i). The older corpus reaches the same findings it always did, and the
    in-tree remedy string appears against no pinned target anywhere: a
    well-formed `pinned:` value exists under no `openspec/specs/` directory, so
    an unnarrowed in-tree arm would report every one of them."""
    older = _run(make_ctx("tag-hygiene"))
    assert sorted(f.rule for f in older if "unresolved target=" in f.rule) == [
        "unresolved target=ghost-capability at line 7"]
    in_tree_remedy = ("name a capability under openspec/specs/ or an active "
                      "change (document-lifecycle grammar)")
    pinned = _run(make_ctx("tag-hygiene-pinned"))
    assert [f.rule for f in pinned if f.action == in_tree_remedy] == []


# --------------------------------------------------------------------------
# (a), (d), (g) — THE ENUMERATION PREREQUISITE'S FOUR STATES
# --------------------------------------------------------------------------

def test_an_absent_enumeration_does_not_resolve_and_names_the_publishers_act(
        corpus_findings):
    """(a), the FAIL-CLOSED case the re-ruling of 2026-09-13 put in place of the
    filing's "emits nothing". The record is otherwise VALID AND COMPLETE for its
    shape; the finding names THAT RECORD, the ROOT it resolved against, and the
    PUBLISHER's act — never `openspec/specs/`, never an active change, and never
    an invented list written into this repository's own copy of the pin."""
    found = [f for f in corpus_findings if f.path == "docs/enumeration-absent.md"]
    assert len(found) == 1
    assert found[0].severity == ERROR
    assert found[0].rule == (
        "unresolved pinned target=pinned:absent-enumeration/wallet-carve at "
        "line 5: contracts/absent-enumeration-pin.yaml in root alpha carries "
        "no capabilities: enumeration")
    assert found[0].action == (
        "the publisher adds capabilities: to the pin record through a "
        "neutral-product-pin change (document-lifecycle grammar)")


def test_a_capability_the_enumeration_does_not_carry_names_the_enumeration(
        corpus_findings):
    """(d) PRESENT AND DOES NOT NAME. The finding names the enumeration itself,
    so the reader can see the closed list the name was checked against."""
    found = [f for f in corpus_findings if f.path == "docs/enumeration-omits.md"]
    assert len(found) == 1
    assert found[0].rule == (
        "unresolved pinned target=pinned:named-capability/ghost-capability at "
        "line 5: contracts/named-capability-pin.yaml in root alpha enumerates "
        "wallet-carve, second-capability")
    assert found[0].action == (
        "name a capability the pin record's capabilities: enumeration carries "
        "(document-lifecycle grammar)")


def test_every_malformed_enumeration_shape_is_its_own_finding(corpus_findings):
    """(g), all five shapes — a scalar, a mapping, a null, an EMPTY SEQUENCE
    (its own case, since it satisfies "a sequence of well-formed names"
    vacuously) and a sequence carrying an item that is not a capability name.

    AND (a) AND (g) REACH THE SAME OUTCOME BY TWO FINDINGS, WHICH THIS ASSERTS
    IN BOTH DIRECTIONS: the malformed text is not the absent text and the
    remedies differ — a malformed member is REPAIRED by whoever wrote it, an
    absent one is PUBLISHED by the pinned product's publisher, and a finding
    that named the wrong one would send the reader to the wrong act."""
    found = [f for f in corpus_findings
             if f.path == "docs/enumeration-malformed.md"]
    assert len(found) == 5
    repair = ("repair the pin record's capabilities: member to a non-empty "
              "sequence of capability names (document-lifecycle grammar)")
    assert {f.action for f in found} == {repair}
    assert sorted(f.rule.split("malformed — ")[1] for f in found) == [
        "it carries 'Wallet_Carve', which is not a capability name",
        "it is NoneType and not a sequence",
        "it is an empty sequence",
        "it is dict and not a sequence",
        "it is str and not a sequence",
    ]
    publisher = ("the publisher adds capabilities: to the pin record through a "
                 "neutral-product-pin change (document-lifecycle grammar)")
    assert publisher not in {f.action for f in found}
    assert all("carries no capabilities: enumeration" not in f.rule
               for f in found)


# --------------------------------------------------------------------------
# (b), (f), (l) — THE PIN ITSELF
# --------------------------------------------------------------------------

def test_an_unresolvable_pin_id_names_the_pin_registry(corpus_findings):
    """(b). The remedy names the PIN REGISTRY rather than `openspec/specs/` or
    an active change, and the finding names the root or roots searched — under
    two roots a bare "no pin record" sentence cannot be acted on, and under one
    the named root is what makes a `--single-repo` difference readable."""
    found = [f for f in corpus_findings if f.path == "docs/no-such-pin.md"]
    assert len(found) == 1
    assert found[0].rule == (
        "unresolved pinned target=pinned:ghost-product/wallet-carve at line 5: "
        "no contracts/ghost-product-pin.yaml under root(s) alpha")
    assert found[0].action == (
        "name a pin the registry under contracts/ carries "
        "(document-lifecycle grammar)")


def test_a_record_of_another_kind_does_not_resolve(corpus_findings):
    """(f). `kind: pinned_workflow` pins executable governance code rather than
    a product whose units are capabilities, so it has no capability set for the
    name to be about — and the arm gates on the kind BEFORE any shape is
    selected, which is why the finding is the kind's and not a shape's."""
    found = [f for f in corpus_findings if f.path == "docs/wrong-kind.md"]
    assert len(found) == 1
    assert found[0].rule == (
        "pinned target=pinned:workflow-kind/wallet-carve at line 5: "
        "contracts/workflow-kind-pin.yaml in root alpha declares kind "
        "'pinned_workflow', not pinned_contract_manifest")
    assert found[0].action == (
        "name a neutral-product pin rather than a pin-shaped record of another "
        "kind (document-lifecycle grammar)")


def test_an_invalid_pin_names_the_shape_tried_the_member_and_the_root(
        corpus_findings):
    """(l) at the FINDING grain — the referent cases a kind-only test leaves
    open, the record that names the hole this list closes, and the MIXTURE.

    `contracts/evil-pin.yaml` carries a kind, `revision_kind: commit` and a
    well-formed commit AND NOTHING ELSE: it satisfies a top-level-referent
    check, matches NEITHER commit-pinned shape, and MUST NOT resolve a pinned
    target. The mixed record carries both a whole-tree `digests.tree_sha256` and
    a `files:` list and is refused NAMING BOTH SHAPES TRIED, no ratified text
    admitting the mixture. The per-member missing/malformed matrix for all three
    shapes is in `test_pin_shape_adapter.py`, at the grain the table is
    written."""
    found = {f.rule.split(" for target=")[1].split(" at line")[0]: f
             for f in corpus_findings if f.path == "docs/invalid-pin.md"}
    assert sorted(found) == [
        "pinned:evil/wallet-carve", "pinned:kind-only/wallet-carve",
        "pinned:mixed-shape/wallet-carve", "pinned:no-commit/wallet-carve",
        "pinned:no-integrity/wallet-carve"]
    complete = ("complete the pin record for its record shape through a "
                "neutral-product-pin change (document-lifecycle grammar)")
    assert {f.action for f in found.values()} == {complete}
    for finding in found.values():
        assert "in root alpha" in finding.rule

    evil = found["pinned:evil/wallet-carve"].rule
    assert "shape (a) the enumerated commit-pinned source pin: " \
           "`submodule_path or source_repository` missing" in evil
    assert "shape (b) the whole-tree digest commit-pinned source pin: " \
           "`submodule_path` missing" in evil

    assert found["pinned:kind-only/wallet-carve"].rule.endswith(
        "— `revision_kind` missing")
    for name in ("no-commit", "no-integrity"):
        assert "`commit` missing" in found[f"pinned:{name}/wallet-carve"].rule \
            or "`integrity` missing" in found[f"pinned:{name}/wallet-carve"].rule

    mixed = found["pinned:mixed-shape/wallet-carve"].rule
    assert "shape (a) the enumerated commit-pinned source pin: " \
           "`digests.tree_sha256` mixed" in mixed
    assert "shape (b) the whole-tree digest commit-pinned source pin: " \
           "`files` mixed" in mixed


# --------------------------------------------------------------------------
# (e) — THE SUPERSEDES REFUSAL
# --------------------------------------------------------------------------

def test_a_supersedes_spec_carrying_the_reserved_prefix_is_refused(
        corpus_findings):
    """(e), asserted VERBATIM rather than as "a finding": the scenario *A
    supersedes marker carries the reserved pinned prefix* requires the finding
    to STATE that the pinned form is admitted only in a candidate marker's
    `target=` attribute, and the generic unresolved-`supersedes` action would
    satisfy a laxer test while violating it."""
    found = [f for f in corpus_findings
             if f.path == "docs/supersedes-pinned.md"]
    assert len(found) == 1
    assert found[0].rule == (
        "supersedes spec=pinned:named-capability/wallet-carve carries the "
        "reserved pinned: prefix at line 5")
    assert found[0].action == (
        "the pinned form is admitted only in a candidate marker's target= "
        "attribute (document-lifecycle grammar)")


# --------------------------------------------------------------------------
# (h) — THE LEXICAL GRAMMAR, BEFORE ANY PATH IS BUILT
# --------------------------------------------------------------------------

def test_a_lexically_malformed_value_builds_no_path_and_reads_nothing(seams):
    """(h). Five values that fail the grammar — an extra `/` segment, a
    traversal component, an upper-case component, an empty component and a
    dotted one — each a malformed-pinned-target finding, AND the test asserts on
    the READ SURFACE that no pin-record path was constructed and no file was
    read for any of them. Validating AFTER building a path is how
    `pinned:../../etc/passwd/x` would become a read outside the pin registry,
    which is the defect this case exists to prevent, so "it reported a finding"
    is not enough."""
    findings = _run(make_ctx("tag-hygiene-pinned"))
    malformed = [f for f in findings if f.path == "docs/malformed-value.md"]
    assert len(malformed) == 5
    assert {f.action for f in malformed} == {
        "spell a pinned target pinned:<pin-id>/<capability>, two kebab-case "
        "components (document-lifecycle grammar)"}
    assert sorted(f.rule.split("target=")[1].split(" at line")[0]
                  for f in malformed) == [
        "pinned:../x/y", "pinned:Upper/case", "pinned:dotted.name/x",
        "pinned:one/two/three", "pinned:x/"]

    # Nothing in the arm's read surface ever saw any of the five: not a
    # boundary check, not a candidate resolution, not a read.
    for spy in seams.values():
        for args, _kwargs in spy.calls:
            assert not any("one" in str(a) or "Upper" in str(a)
                           or "dotted" in str(a) for a in args), args
    resolved = [args[0] for args, _ in seams["resolve_in_root"].calls]
    for name in ("one", "two", "three", "Upper", "dotted.name", "..", "x/"):
        assert not any(name in str(claimed) for claimed in resolved)


# --------------------------------------------------------------------------
# (k) — A RECORD THAT EXISTS BUT IS CORRUPT
# --------------------------------------------------------------------------

@pytest.mark.parametrize("shape,name,body", [
    ("a", "alpha-pin.yaml", "kind: pinned_contract_manifest\n  files: [\n"),
    ("b", "beta-pin.yaml", "- not\n- a\n- mapping\n"),
    ("c", "gamma-pin.yaml",
     "schema_version: 1\nrevision_kind: package_integrity\nversion: 1.12.0\n"),
])
def test_a_corrupt_record_is_a_controlled_finding_and_the_run_completes(
        tmp_path, shape, name, body):
    """(k), one case per shape: invalid YAML where a shape-(a) record was
    intended, a non-mapping document where a shape-(b) one was, and a mapping
    with no `kind` where a shape-(c) one was. The resolver reads a registry file
    it did not write, so the family OWNS the failure rather than propagating it:
    each is a tag-hygiene finding, the target does not resolve, and the run
    COMPLETES rather than raising out of the family."""
    pin_id = name[: -len("-pin.yaml")]
    root = _repo(tmp_path / "alpha", records={name: body},
                 docs={"case.md": _doc(f"pinned:{pin_id}/wallet-carve")})
    findings = _run(_context({"alpha": root}))
    assert len(findings) == 1, findings
    assert findings[0].severity == ERROR
    assert findings[0].action == (
        "repair the pin record so it reads as a mapping carrying a kind: "
        "(document-lifecycle grammar)")
    assert f"contracts/{name} in root alpha" in findings[0].rule
    assert shape in "abc"


def test_a_non_utf8_record_is_a_controlled_finding_and_the_run_completes(
        tmp_path):
    """(k), one more shape: a record whose BYTES are not valid UTF-8 at all.
    `Path.read_text(encoding="utf-8")` raises `UnicodeDecodeError` — a
    `UnicodeError`, not an `OSError` — and `_pin_record_text` must catch it the
    same way it catches an unreadable file, so the family OWNS the failure
    rather than propagating it out of the run."""
    name = "invalid-utf8-pin.yaml"
    pin_id = name[: -len("-pin.yaml")]
    root = _repo(tmp_path / "alpha",
                 docs={"case.md": _doc(f"pinned:{pin_id}/wallet-carve")})
    (root / "contracts" / name).write_bytes(b"\xff\xfe\x00kind: x\n")
    findings = _run(_context({"alpha": root}))
    assert len(findings) == 1, findings
    assert findings[0].severity == ERROR
    assert findings[0].action == (
        "repair the pin record so it reads as a mapping carrying a kind: "
        "(document-lifecycle grammar)")
    assert f"contracts/{name} in root alpha" in findings[0].rule


# --------------------------------------------------------------------------
# (m) — CONTAINMENT: FOUR ESCAPES AND A POSITIVE
# --------------------------------------------------------------------------

def test_a_candidate_symlink_leaving_the_repository_is_refused(tmp_path):
    """(m), escape 1 of 4 — THE CANDIDATE'S. A `contracts/<pin-id>-pin.yaml`
    that resolves OUTSIDE the repository is refused rather than followed, and
    the refusal names the root."""
    outside = tmp_path / "elsewhere" / "planted-pin.yaml"
    outside.parent.mkdir(parents=True)
    outside.write_text(yaml.safe_dump(_shape_a()), encoding="utf-8")
    root = _repo(tmp_path / "alpha",
                 docs={"case.md": _doc("pinned:planted/wallet-carve")})
    (root / "contracts" / "planted-pin.yaml").symlink_to(outside)

    findings = _run(_context({"alpha": root}))
    assert [f.rule for f in findings] == [
        "pinned target=pinned:planted/wallet-carve at line 5: "
        "contracts/planted-pin.yaml resolves outside root alpha's contracts/ "
        "directory"]
    assert findings[0].action == (
        "keep the pin record inside its root's contracts/ directory rather "
        "than a symlink out of it (document-lifecycle grammar)")


def test_a_candidate_symlink_inside_the_repository_but_outside_contracts_is_refused(
        tmp_path):
    """(m), escape 2 of 4 — the one `resolve_in_tree`'s REPOSITORY question
    passes and the `contracts/` question refuses:
    `contracts/foo-pin.yaml -> ../openspec/specs/...` stays inside the
    repository and still leaves the registry."""
    root = _repo(tmp_path / "alpha",
                 docs={"case.md": _doc("pinned:planted/wallet-carve")})
    inside = root / "openspec" / "specs" / "planted-pin.yaml"
    inside.parent.mkdir(parents=True)
    inside.write_text(yaml.safe_dump(_shape_a()), encoding="utf-8")
    (root / "contracts" / "planted-pin.yaml").symlink_to(
        Path("..") / "openspec" / "specs" / "planted-pin.yaml")

    findings = _run(_context({"alpha": root}))
    assert len(findings) == 1
    assert "resolves outside root alpha's contracts/ directory" \
        in findings[0].rule


@pytest.mark.parametrize("where", ["inside", "outside"])
def test_a_contracts_directory_that_is_itself_a_symlink_refuses_for_that_root(
        tmp_path, seams, where):
    """(m), escapes 3 and 4 of 4 — THE BOUNDARY'S OWN, and they are not
    reachable by any candidate check. An implementation comparing the candidate
    against `(root / "contracts").resolve()` ACCEPTS AND READS a file outside
    the lexical registry in both, the redirection having moved the boundary
    rather than been caught by it.

    So the arm refuses FOR THAT ROOT — the honest grain, since every pinned
    target that would resolve through it is affected — and the test asserts on
    the read surface that NO CANDIDATE WAS RESOLVED and NOTHING WAS READ, not
    merely that a finding was emitted."""
    root = tmp_path / "alpha"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "case.md").write_text(
        _doc("pinned:planted/wallet-carve"), encoding="utf-8")
    real = (root / "registry") if where == "inside" else (tmp_path / "registry")
    real.mkdir(parents=True)
    (real / "planted-pin.yaml").write_text(yaml.safe_dump(_shape_a()),
                                           encoding="utf-8")
    (root / "contracts").symlink_to(real, target_is_directory=True)

    findings = _run(_context({"alpha": root}))
    assert [f.rule for f in findings] == [
        "pinned target=pinned:planted/wallet-carve at line 5: root alpha has a "
        "contracts that is a SYMLINK; a boundary that can be redirected is not "
        "a boundary, so no candidate is resolved through it"]
    assert findings[0].action == (
        "make the resolution root's contracts/ a real directory rather than a "
        "redirection (document-lifecycle grammar)")
    assert seams["boundary_dir"].calls, "the precondition was asked"
    assert seams["resolve_in_root"].calls == [], "no candidate was resolved"
    assert seams["_pin_record_text"].calls == [], "nothing was read"


def test_an_ordinary_contracts_directory_passes_the_precondition(
        tmp_path, seams):
    """(m), the FIFTH and POSITIVE case: a real, non-redirecting `contracts/`
    passes the precondition and the target resolves normally — so the four
    refusals above are refusals of the defect and not of the mechanism."""
    root = _repo(tmp_path / "alpha",
                 records={"planted-pin.yaml": _shape_a()},
                 docs={"case.md": _doc("pinned:planted/wallet-carve")})
    findings = _run(_context({"alpha": root}))
    assert findings == []
    assert len(seams["boundary_dir"].calls) == 1
    assert len(seams["resolve_in_root"].calls) == 1
    assert len(seams["_pin_record_text"].calls) == 1


def test_the_boundary_is_checked_before_any_candidate_is(tmp_path, seams):
    """(m)'s ORDER, asserted as an order rather than inferred from an outcome:
    across a run carrying both a good root and a redirected one, every
    `boundary_dir` call precedes the `resolve_in_root` call it gates."""
    root = _repo(tmp_path / "alpha",
                 records={"planted-pin.yaml": _shape_a()},
                 docs={"case.md": _doc("pinned:planted/wallet-carve")})
    order = []
    for name in ("boundary_dir", "resolve_in_root"):
        spy = seams[name]
        real = spy.real

        def record(*args, _name=name, _real=real, **kwargs):
            order.append(_name)
            return _real(*args, **kwargs)
        spy.real = record
    _run(_context({"alpha": root}))
    assert order == ["boundary_dir", "resolve_in_root"]


def test_a_malformed_claimed_path_is_a_controlled_refusal_not_a_traceback(
        tmp_path):
    """(PR #1040 fix round 3, R1). `Path.resolve()` raises `ValueError`
    ("embedded null byte") on a claimed path carrying NUL, which a YAML
    registration can supply; the helper promises a refusal tuple, so it maps
    that to `UNRESOLVABLE` too. Asserted on the helper: a MARKER cannot carry
    NUL — the lexical grammar refuses it before any path exists."""
    import pin_containment as pc
    root = tmp_path / "alpha"
    (root / "contracts").mkdir(parents=True)
    target, refusal = pc.resolve_in_root("contracts/a\x00b-pin.yaml", root)
    assert target is None
    assert refusal[0] == pc.UNRESOLVABLE


def test_the_package_imports_by_its_dotted_path_without_sys_path_injection():
    """(PR #1040 fix round 3, R2). This repository's own tests reach the
    package as `scripts.doc_health.*` (tests/ideation-dashboard/
    test_route_extension.py); a module-level bare `from pin_containment import`
    would fail that import at load time whenever `scripts/` is not on
    `sys.path`, so the resolver falls back to the package-relative spelling. A
    fresh interpreter from the repository root, no PYTHONPATH, is the proof."""
    import subprocess
    import sys
    repo_root = Path(__file__).resolve().parents[2]
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    proc = subprocess.run(
        [sys.executable, "-c",
         "import scripts.doc_health.families as f; print(f.PINNED_PREFIX)"],
        cwd=repo_root, env=env, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "pinned:"


def test_a_self_looping_symlink_record_cannot_be_resolved_and_reads_nothing(
        tmp_path, seams):
    """(m), the SYMLINK LOOP — `Path.resolve()` raises `RuntimeError` on a
    self-referencing symlink (Python 3.12), which `resolve_in_root` must catch
    and turn into a refusal rather than letting it escape the family. The read
    seam is never reached: a target that cannot be resolved is not a candidate
    to read."""
    root = _repo(tmp_path / "alpha",
                 docs={"case.md": _doc("pinned:loop/wallet-carve")})
    os.symlink("loop-pin.yaml", root / "contracts" / "loop-pin.yaml")

    findings = _run(_context({"alpha": root}))
    assert [f.rule for f in findings] == [
        "pinned target=pinned:loop/wallet-carve at line 5: "
        "contracts/loop-pin.yaml in root alpha cannot be resolved "
        "(unresolvable)"]
    assert findings[0].action == (
        "keep the pin record inside its root's contracts/ directory rather "
        "than a symlink out of it (document-lifecycle grammar)")
    assert seams["_pin_record_text"].calls == [], "nothing was read"


# --------------------------------------------------------------------------
# (n) — `verify_pin:` IS NEVER FOLLOWED
# --------------------------------------------------------------------------

def test_an_arbitrary_verify_pin_path_is_never_opened_imported_or_run(
        tmp_path, seams, monkeypatch):
    """(n) FIRST. A record whose `verify_pin:` names an arbitrary in-tree path
    has that path NEVER opened, imported or run — asserted by instrumenting the
    read, import and exec surfaces, not by reading a finding text, since the
    boundary is that the path is not touched. A record that chooses which code
    judges it is a record that judges itself."""
    planted = tmp_path / "alpha" / "scripts" / "arbitrary.py"
    planted.parent.mkdir(parents=True)
    planted.write_text("raise SystemExit('this must never run')\n",
                       encoding="utf-8")
    root = _repo(tmp_path / "alpha",
                 records={"openxwallet-pin.yaml": _shape_a(
                     verify_pin="scripts/arbitrary.py",
                     capabilities=["openxwallet"])},
                 docs={"case.md": _doc("pinned:openxwallet/openxwallet")})

    ran = []
    monkeypatch.setattr(subprocess, "run",
                        lambda *a, **k: ran.append(("run", a)))
    import importlib.util
    monkeypatch.setattr(importlib.util, "spec_from_file_location",
                        lambda *a, **k: ran.append(("import", a)))
    monkeypatch.setattr(importlib, "import_module",
                        lambda *a, **k: ran.append(("import_module", a)))

    findings = _run(_context({"alpha": root}))
    assert ran == []
    read = [str(args[0]) for args, _ in seams["_pin_record_text"].calls]
    assert read == [str(root / "contracts" / "openxwallet-pin.yaml")]
    assert all("arbitrary.py" not in path for path in read)
    # The target still RESOLVES — the disagreement stands beside it.
    assert [f.rule for f in findings] == [
        "pinned target=pinned:openxwallet/openxwallet at line 5: "
        "contracts/openxwallet-pin.yaml in root alpha names verify_pin "
        "'scripts/arbitrary.py', not the scripts/verify-openxwallet-pin.py "
        "this checker tracks for it"]


def test_the_tracked_verify_pin_value_is_no_finding_and_the_target_resolves():
    """(n) SECOND. Where `verify_pin:` carries THE VALUE THE ADAPTER HOLDS for
    that record, a record complete for its shape AND satisfying the enumeration
    prerequisites RESOLVES with NO finding from this arm — `verify_pin:` being
    neither part of the required shape nor a resolution prerequisite. A test
    that refused such a record would encode the opposite of D-2 and reject valid
    pins. Driven by the committed corpus's `openxwallet-pin.yaml`, whose
    `verify_pin:` is the tracked value."""
    record = yaml.safe_load(
        (FIXTURE_CONTRACTS / "openxwallet-pin.yaml").read_text())
    assert record["verify_pin"] == "scripts/verify-openxwallet-pin.py"
    findings = _run(make_ctx("tag-hygiene-pinned"))
    assert [f for f in findings if f.path == "docs/resolving.md"] == []


def test_a_differing_verify_pin_is_reported_beside_an_unresolved_target(
        tmp_path, seams):
    """(n) THIRD. Where the value DIFFERS from what the adapter holds, the pass
    emits the DISAGREEMENT FINDING — still without touching the path — and where
    a prerequisite ALSO fails, the target is unresolved for THAT reason and the
    disagreement is reported BESIDE it: a disagreement about which code would
    judge the record is no fact about the record's shape.

    The three cases are separate because the first's arbitrary path IS a
    differing value, so one case asserting both "the verdict is unchanged by
    that member's value" and "a differing value is a finding" would contradict
    itself."""
    root = _repo(tmp_path / "alpha",
                 records={"openxwallet-pin.yaml": _shape_a(
                     verify_pin="scripts/validate-openreposhape-pin.py",
                     capabilities=None)},
                 docs={"case.md": _doc("pinned:openxwallet/openxwallet")})
    findings = _run(_context({"alpha": root}))
    assert len(findings) == 2
    assert any("names verify_pin 'scripts/validate-openreposhape-pin.py'"
               in f.rule for f in findings)
    assert any("capabilities: enumeration in "
               "contracts/openxwallet-pin.yaml (root alpha) is malformed"
               in f.rule for f in findings)
    read = [str(args[0]) for args, _ in seams["_pin_record_text"].calls]
    assert read == [str(root / "contracts" / "openxwallet-pin.yaml")]


# --------------------------------------------------------------------------
# (o) — TWO ROOTS
# --------------------------------------------------------------------------

def _two_roots(tmp_path, *, in_own_root: bool):
    alpha = _repo(tmp_path / "alpha",
                  records=({"planted-pin.yaml": _shape_a(
                      capabilities=["own-root-capability"])}
                      if in_own_root else {}),
                  docs={"case.md": _doc("pinned:planted/wallet-carve")})
    openx = _repo(tmp_path / "openxFactory",
                  records={"planted-pin.yaml": _shape_a(
                      capabilities=["openxfactory-root-capability"])})
    return alpha, openx


def test_a_pinned_target_resolves_under_an_aggregate_runs_second_root(
        tmp_path):
    """(o)(i). The record exists only in the `openxFactory` root and a document
    of the other repository names it: the target is judged against THAT root by
    the same precedence the in-tree capability arm uses, and the finding NAMES
    that root."""
    alpha, openx = _two_roots(tmp_path, in_own_root=False)
    findings = _run(_context({"alpha": alpha, "openxFactory": openx}))
    assert len(findings) == 1
    assert findings[0].rule == (
        "unresolved pinned target=pinned:planted/wallet-carve at line 5: "
        "contracts/planted-pin.yaml in root openxFactory enumerates "
        "openxfactory-root-capability")


def test_the_documents_own_repositorys_record_is_the_one_read(tmp_path):
    """(o)(ii). Where BOTH roots carry a record for the same `<pin-id>`, the
    document's own repository's record is the one read — the in-tree arm's
    precedence, unchanged and invented nowhere."""
    alpha, openx = _two_roots(tmp_path, in_own_root=True)
    findings = _run(_context({"alpha": alpha, "openxFactory": openx}))
    assert len(findings) == 1
    assert findings[0].rule.endswith(
        "contracts/planted-pin.yaml in root alpha enumerates "
        "own-root-capability")


def test_a_single_repository_run_has_one_root_and_does_not_widen_it(tmp_path):
    """(o)(iii), THE SINGLE-ROOT NEGATIVE. The same document read by a
    `--single-repo` run of its own repository, the record existing only in the
    `openxFactory` root: the target does NOT resolve, the finding NAMES THE ONE
    ROOT SEARCHED, and the pass does not widen its root set to reach the record.

    (i) is not this case's contradiction: what is unchanged across scopes is the
    ORDER, not the outcome, an aggregate run simply carrying a second root that
    a single-repository run does not have."""
    alpha, _openx = _two_roots(tmp_path, in_own_root=False)
    findings = _run(_context({"alpha": alpha}))
    assert [f.rule for f in findings] == [
        "unresolved pinned target=pinned:planted/wallet-carve at line 5: no "
        "contracts/planted-pin.yaml under root(s) alpha"]
