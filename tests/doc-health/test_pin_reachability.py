"""Derivation-pin reachability across the declared artifact class
(`govern-derived-pin-reachability`; sixteen scenarios across three deltas).

Every test here is pinned to a DEFECT rather than to a fix. The defects, all
measured on 2026-08-27 against `origin/main`:

  A. THREE committed artifacts pinned commits no ref reached. Two were the
     readiness records `harden-ideation-readiness-check` left behind when it
     repaired the index and stopped; the third — a proposal-support manifest
     inside an archived packet — belonged to a whole GENERATOR FAMILY the
     packet's own inventory never swept, and nothing in this repository had
     ever looked at it.
  B. A FOURTH pin is orphaned AND UNRECOVERABLE, under the key
     `us3_baseline_commit` that no sweep vocabulary knew. A renamed key is a
     silent loss of coverage, and a silent loss of coverage looks exactly like a
     clean run.
  C. In an agent worktree sharing an object store with the checkout that made
     them, all three of (A) answer `commit` to `git cat-file -t` while no ref
     reaches them — so a probe written against the object store reports this
     repository clean. Reachability is a fact about REFS.

The fixtures are real git repositories under `tmp_path`; no test mutates any
checkout on the machine, and the two tests that read the real repository only
read it. The reachability fixtures include a genuinely isolated `--no-local`
clone, because the sibling packet's realization proved the shared-object-store
hazard is real and that isolated clones are the only honest venue for (C).
"""

from __future__ import annotations

import re
import subprocess

from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import families
from doc_health import ideation_readiness as ir
from doc_health import pin_class as pc

import test_ideation_readiness as tir


# =========================================================================
# fixtures
# =========================================================================

def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=check)


def _init(root):
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    return root


def _write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


READINESS_REL = ("health/ideation-readiness/2026-08-24/"
                 "fixture-run-20260824.yaml")


def _readiness_record(pin, *, status="record"):
    return yaml.safe_dump(
        {"schema_version": 1, "kind": "ideation_readiness_run",
         "status": status, "run_id": "fixture-run-20260824",
         "source_revision": pin, "envelopes": [], "scored_clusters": []},
        sort_keys=False)


def orphaned_pin_repo(tmp_path, *, name="repo", status="record"):
    """A repository whose committed readiness record pins a commit NO REF
    REACHES, built the way the real one was: a side branch, a commit on it, the
    branch deleted. The object survives in this repository's own store — which
    is the point, and is why `cat-file` is not the probe."""
    repo = _init(tmp_path / name)
    _write(repo, "ideation/brainstorm/one.md", "# one\n\nStatus: brainstorm\n")
    base = _commit(repo, "corpus")

    _git(repo, "checkout", "-q", "-b", "side")
    _write(repo, "ideation/brainstorm/two.md", "# two\n\nStatus: brainstorm\n")
    orphan = _commit(repo, "side work")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "branch", "-qD", "side")

    _write(repo, READINESS_REL, _readiness_record(orphan, status=status))
    _commit(repo, "readiness record pinning the side commit")
    return repo, base, orphan


def reachable_pin_repo(tmp_path, *, name="repo"):
    """A record pinning an ANCESTOR of `main` that is not its tip — the ordinary
    condition of every derivation record between regenerations."""
    repo = _init(tmp_path / name)
    _write(repo, "ideation/brainstorm/one.md", "# one\n\nStatus: brainstorm\n")
    old = _commit(repo, "corpus")
    _write(repo, READINESS_REL, _readiness_record(old))
    _commit(repo, "readiness record pinning the corpus commit")
    _write(repo, "ideation/brainstorm/two.md", "# two\n\nStatus: brainstorm\n")
    _commit(repo, "corpus moves on")
    return repo, old


def _verify(repo, **kw):
    """The class verification with the retention namespace consulted LOCALLY
    only. Fixtures have no remote, and a fixture that reached for one would be
    testing the network rather than the rule."""
    kw.setdefault("allow_remote", False)
    return pc.verify(repo, **kw)


# =========================================================================
# ideation-cross-reference requirement 1 — a committed pin stays resolvable
# =========================================================================

def test_a_reachable_but_stale_pin_emits_no_finding(tmp_path):
    """Delta scenario "The pin names an older commit that main still reaches",
    and the doc-health scenario "A declared member's pin is reachable but
    stale". Staleness between regenerations is LEGAL, and the whole requirement
    turns on not converting an age comparison into a reachability finding."""
    repo, old = reachable_pin_repo(tmp_path)
    report = _verify(repo)
    assert [r.site.pin for r in report.results] == [old]
    assert report.results[0].verdict == pc.PASS
    assert report.orphans == []
    assert report.clean and report.fully_verified
    # ...and it is genuinely STALE, or the fixture proves nothing.
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() != old


def test_an_orphaned_pin_is_reported_as_a_defect_naming_artifact_and_pin(
        tmp_path):
    """Delta scenario "The pin names a commit no ref reaches", and the
    doc-health scenario "A pin-carrying artifact outside the index is
    orphaned" — the artifact here is a `health/` record, NOT the index, which is
    the coverage gap the class exists to close."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    report = _verify(repo)
    assert len(report.orphans) == 1
    site = report.orphans[0].site
    assert site.pin == orphan
    assert site.path == READINESS_REL
    assert site.key == "source_revision"
    assert not report.clean and not report.fully_verified

    verdict, reason, _ = ir.verify_pin_reachability(repo, allow_remote=False)
    assert verdict == ir.PIN_PROBE_FAIL
    assert orphan in reason
    assert READINESS_REL in reason
    assert "COMPLETE clone" in reason
    assert "shallow clone?" not in reason        # never the old conjecture
    # The repair route is named where the finding fires: this artifact is a
    # `record`, so retention — never an edit to the pin.
    assert "RETENTION" in reason
    assert "refs/retention/pins" in reason


def test_the_object_store_surviving_the_commit_is_not_a_defence(tmp_path):
    """THE PROBE-SHAPE MUTATION CHECK (defect C). `git cat-file -t` SUCCEEDS for
    the orphan in the repository that made it, and a probe written against that
    would report this fixture — and the real repository — clean. The refs-based
    probe reports the defect in both the origin fixture and a genuinely isolated
    `--no-local` clone, and the two verdicts agree while `cat-file` disagrees."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    assert _git(repo, "cat-file", "-t", orphan).stdout.strip() == "commit", (
        "the fixture must reproduce the hazard, or the mutation proves nothing")

    clone = tmp_path / "isolated"
    subprocess.run(["git", "clone", "-q", "--no-local", f"file://{repo}",
                    str(clone)], capture_output=True, check=True)
    assert _git(clone, "cat-file", "-t", orphan, check=False).returncode != 0

    for where in (repo, clone):
        report = _verify(where)
        assert [r.verdict for r in report.orphans] == [pc.ORPHAN]
        assert report.orphans[0].site.pin == orphan
    # ...and the REVERTED probe would have passed the origin fixture.
    assert pc.reachable_from_main(repo, orphan, "refs/heads/main") is False


def test_a_pin_reachable_only_through_the_retention_namespace_passes(tmp_path):
    """Delta scenario "The pin resolves only through a retention ref". This is
    the intended END STATE for this repository's three retained pins, not a
    tolerated one: the record keeps its original pin, unedited, and the COMMIT
    is what was made reachable."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    before = (repo / READINESS_REL).read_text("utf-8")

    _git(repo, "update-ref", pc.retention_ref(orphan), orphan)
    report = _verify(repo)
    assert report.orphans == []
    assert report.results[0].verdict == pc.PASS
    assert "retained" in report.results[0].how
    assert pc.retention_ref(orphan) in report.results[0].how
    # main still does not reach it, and that is the point rather than a residue.
    assert pc.reachable_from_main(repo, orphan, "refs/heads/main") is False
    assert (repo / READINESS_REL).read_text("utf-8") == before, (
        "retention repairs the COMMIT; the record's bytes must not move")


@pytest.mark.parametrize("ref_name", [
    "refs/heads/keepalive",                     # a branch parked on the object
    "refs/tags/keepalive",                      # a tag parked on the object
    "refs/retention/da9bf3b7",                  # right family, wrong shape
    "refs/retention/pins/keepalive",            # right namespace, chosen name
    "refs/remotes/origin-retention/orphan",     # this checkout really has two
])
def test_a_ref_outside_the_computed_namespace_does_not_green_a_pin(tmp_path,
                                                                   ref_name):
    """Delta scenario "The pin resolves only through a retention ref", second
    bullet: a retention ref under ANY OTHER NAME must not satisfy the
    requirement, because a ref whose name cannot be derived from the pin is not
    predictably reachable. Parametrized over the shapes that actually occur,
    including the leftover remote-tracking refs this repository's shared
    checkout carries from a since-deleted remote."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    _git(repo, "update-ref", ref_name, orphan)
    report = _verify(repo)
    assert len(report.orphans) == 1, (
        f"{ref_name} greened a pin nobody can find from the pin's own name")
    assert report.orphans[0].site.pin == orphan


def test_a_retention_ref_must_point_at_the_commit_its_name_states(tmp_path):
    """The ref's own name states which commit it exists to keep, so no separate
    declaration can drift from it — which only holds if the pointer is checked.
    A ref named for X pointing at Y retains nothing."""
    repo, base, orphan = orphaned_pin_repo(tmp_path)
    _git(repo, "update-ref", pc.retention_ref(orphan), base)   # wrong target
    report = _verify(repo)
    assert len(report.orphans) == 1
    assert "rather than at the commit its name states" in report.orphans[0].how

    _git(repo, "update-ref", pc.retention_ref(orphan), orphan)  # corrected
    assert _verify(repo).orphans == []


def test_the_retention_namespace_is_computed_from_the_pin_not_chosen():
    """Q3's grammar, asserted rather than described: one ref per retained
    commit, named for the full forty-character object name."""
    pin = "da9bf3b7d0ee1d86d2d437d42a715c238dddce4b"
    assert pc.retention_ref(pin) == f"refs/retention/pins/{pin}"
    assert pc.RETENTION_NAMESPACE == "refs/retention/pins"
    for bad in ("", "da9bf3b7", pin.upper(), pin + "0", "main"):
        with pytest.raises(ValueError):
            pc.retention_ref(bad)


def test_the_retention_namespace_is_consulted_on_the_remote(tmp_path):
    """A LOCAL ref does not satisfy requirement 2 — a pin whose reachability
    depends on one machine's object store is unreachable by every other reader —
    so the published ref has to be consultable from a clone that does not carry
    it. No default refspec fetches `refs/retention/*`, so this is a REMOTE read,
    and it is proved over a `file://` origin rather than over the network."""
    origin, _, orphan = orphaned_pin_repo(tmp_path, name="origin")
    _git(origin, "update-ref", pc.retention_ref(orphan), orphan)

    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", f"file://{origin}", str(clone)],
                   capture_output=True, check=True)
    assert _git(clone, "rev-parse", "--verify", "--quiet",
                pc.retention_ref(orphan), check=False).returncode != 0, (
        "a clone that already carried the retention ref would prove nothing "
        "about the remote consult")

    where, detail = pc.retention_holder(clone, orphan)
    assert where == "remote" and pc.retention_ref(orphan) in detail
    assert pc.verify(clone).orphans == []

    # ...and with the namespace excluded by request, the same pin is a defect:
    # the remote half is load-bearing, not decorative.
    assert len(pc.verify(clone, allow_remote=False).orphans) == 1


def test_a_truncated_clone_reports_against_the_clone_not_the_artifact(
        tmp_path):
    """Delta scenario "A truncated clone cannot resolve a conforming pin", and
    the doc-health scenario "The clone cannot answer the question": the
    condition is reported against the CLONE, naming the truncation actually
    observed, and the artifact is not recorded as carrying an unreachable pin on
    the strength of a local absence."""
    repo, old = reachable_pin_repo(tmp_path, name="deep")
    for extra in ("three", "four"):
        _write(repo, f"ideation/brainstorm/{extra}.md",
               f"# {extra}\n\nStatus: brainstorm\n")
        _commit(repo, extra)

    shallow = tmp_path / "shallow"
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--no-local",
                    f"file://{repo}", str(shallow)],
                   capture_output=True, check=True)
    truncated, observed = pc.is_truncated(shallow)
    assert truncated and "is-shallow-repository" in observed

    report = _verify(shallow)
    assert report.orphans == [], (
        "a pin `main` reaches is not a defect because this clone did not fetch "
        "it")
    assert [r.verdict for r in report.results] == [pc.INCONCLUSIVE]
    assert "TRUNCATED CLONE, observed not conjectured" in report.results[0].how
    assert not report.fully_verified

    verdict, reason, _ = ir.verify_pin_reachability(shallow,
                                                    allow_remote=False)
    assert verdict == ir.PIN_PROBE_SKIP
    assert "observed not conjectured" in reason
    assert old in reason


def test_a_retention_namespace_that_cannot_be_consulted_is_not_a_pass(
        tmp_path):
    """An unaskable question is not an affirmative answer. Where the remote
    cannot be reached at all, a pin `main` does not reach is INCONCLUSIVE — the
    verdict a reader can act on — rather than either a false green or a defect
    blamed on the artifact."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    _git(repo, "remote", "add", "origin",
         str(tmp_path / "no-such-repository"))
    report = pc.verify(repo, allow_remote=True)
    assert [r.verdict for r in report.results] == [pc.INCONCLUSIVE]
    assert "could not be performed" in report.results[0].how
    assert not report.fully_verified
    assert report.orphans == []


# =========================================================================
# ideation-cross-reference requirement 2 — a record is repaired by retention
# =========================================================================

def test_a_records_repair_route_is_retention_and_refuses_a_pin_edit():
    """Delta scenarios "A record's pin is orphaned and the object is still
    recoverable" and "A record's pin is edited in place". The route is a
    property of the ARTIFACT, not a preference: a `record` cannot be re-pinned
    without falsifying it."""
    member = next(m for m in pc.PIN_CLASS if m.id == "ideation-readiness-run")
    route = pc.repair_route(member, status="record")
    assert route.startswith("RETENTION")
    assert "refs/retention/pins/<full-sha>" in route
    assert "computed from the pin" in route
    assert "refused" in route and "did not read" in route


def test_an_immutable_manifest_inside_an_archived_packet_takes_the_same_route():
    """The third orphan's artifact carries no lifecycle `Status:` header at all,
    so a status-only rule would have routed it to a re-pin — an edit to an
    ARCHIVED packet. Its immutability is a property of where it lives."""
    member = next(m for m in pc.PIN_CLASS
                  if m.id == "proposal-support-manifest")
    assert pc.repair_route(member, status=None).startswith("RETENTION")


def test_a_generated_projections_route_is_reproduction_not_retention():
    """Delta scenario "A generated projection's pin is orphaned": re-derive and
    re-pin, under the reproduction obligation. Nothing about a regenerable
    projection is immutable evidence, so the record-retention route is not owed
    for it."""
    member = next(m for m in pc.PIN_CLASS if m.id == "cross-reference-index")
    route = pc.repair_route(member)
    assert route.startswith("REPRODUCTION")
    assert "BYTE-FOR-BYTE" in route
    assert "without regeneration is refused" in route


def test_a_measured_members_route_names_the_measurement_not_bytes():
    """The two-tier shape: byte-for-byte where a tool defines derivation, a
    NAMED MEASUREMENT where none does. Demanding bytes universally would make
    the requirement unsatisfiable for most of the class."""
    member = next(m for m in pc.PIN_CLASS if m.id == "spec-traceability")
    route = pc.repair_route(member)
    assert "NAMED MEASUREMENT" in route
    assert "BYTE-FOR-BYTE" not in route


def test_the_declared_unrecoverable_loss_is_still_unrecoverable():
    """Delta scenario "A record's pin is orphaned and the object is
    unrecoverable", RE-MEASURED rather than trusted.

    `KNOWN_LOSSES` is the one place this module accepts an orphan without a
    repair, so the declaration has to keep earning it. If the object turns out
    to be recoverable — someone finds a clone, a fork advertises it — then
    RETENTION is the route and this row is stale, and this test says so instead
    of letting a stale exemption stand. The governance act it names is still
    owed and is deliberately not performed by code."""
    repo = Path(REPO_ROOT)
    if pc.resolve_main(repo) is None:
        pytest.skip(f"{repo} resolves no `main`; reachability is a fact about "
                    "the clone here")
    assert pc.KNOWN_LOSSES, "the register is the mechanism; an empty one is fine"
    for loss in pc.KNOWN_LOSSES:
        assert pc.FULL_SHA_RE.match(loss.pin)
        assert loss.measured and loss.owed
        present = _git(repo, "cat-file", "-e", f"{loss.pin}^{{commit}}",
                       check=False).returncode == 0
        assert not present, (
            f"{loss.pin} IS present in this object store, so it is recoverable "
            f"and retention is the route: publish {pc.retention_ref(loss.pin)} "
            f"and delete this KNOWN_LOSSES row (the window closes without "
            f"notice — see {loss.path})")


# =========================================================================
# release-realization requirement 3 — a rewrite re-derives the pins it orphans
# =========================================================================

def test_a_hand_moved_pin_whose_body_does_not_reproduce_is_refused(tmp_path):
    """Delta scenario "A pin is moved by hand without regeneration" — the exact
    act that produced this repository's second orphan. At the moment of that
    edit the new pin was a perfectly reachable branch tip, so a
    reachability-only rule PASSES it. Reproduction does not."""
    repo = _init(tmp_path / "index-repo")
    _write(repo, "ideation/brainstorm/alpha-one.md",
           "# alpha-one.md\n\nStatus: brainstorm\nTopics: alpha\n\n## Body\n\n"
           "Body prose describing the recurring alpha subject in depth.\n")
    _write(repo, "ideation/brainstorm/alpha-two.md",
           "# alpha-two.md\n\nStatus: brainstorm\nTopics: alpha\n\n## Body\n\n"
           "Body prose describing the recurring alpha subject in depth.\n")
    corpus_rev = _commit(repo, "corpus")

    from doc_health import corpus as corpus_mod
    derived = ir.derive_clusters(corpus_mod.load_docs("openxFactory", repo))
    assert derived, "the fixture corpus must cluster, or it proves nothing"

    def write_index(pin):
        _write(repo, "ideation/cross-reference.yaml", yaml.safe_dump(
            {"schema_version": 1, "kind": "ideation-cross-reference",
             "repository": "openxFactory",
             "generation": {"source_revision": pin,
                            "generator_version": "fixture"},
             "topic_entries": derived}, sort_keys=False, allow_unicode=True))

    write_index(corpus_rev)
    _commit(repo, "index")
    ok, detail = ir.index_reproduces_at(repo, corpus_rev)
    assert ok is True, detail

    # The corpus moves, and the pin is HAND-MOVED to the new tip with no
    # regeneration. The new pin is perfectly reachable.
    _write(repo, "ideation/brainstorm/beta-one.md",
           "# beta-one.md\n\nStatus: brainstorm\nTopics: beta\n\n## Body\n\n"
           "Body prose describing the recurring beta subject in depth.\n")
    _write(repo, "ideation/brainstorm/beta-two.md",
           "# beta-two.md\n\nStatus: brainstorm\nTopics: beta\n\n## Body\n\n"
           "Body prose describing the recurring beta subject in depth.\n")
    moved_to = _commit(repo, "corpus moves on")
    write_index(moved_to)
    _commit(repo, "pin moved by hand, body untouched")

    assert pc.reachable_from_main(repo, moved_to, "refs/heads/main") is True, (
        "the fixture must reproduce the defect: the hand-moved pin has to be "
        "REACHABLE, or this test proves only that unreachable pins fail")
    assert _verify(repo).orphans == []

    ok, detail = ir.index_reproduces_at(repo, moved_to)
    assert ok is False, (
        "a reachable pin whose body was never regenerated was accepted — "
        "reachability is not evidence that the body matches the state it "
        f"claims. {detail}")
    assert "does NOT reproduce" in detail
    assert moved_to in detail


def test_reproduction_that_cannot_be_asked_is_neither_pass_nor_fail(tmp_path):
    """Where the pinned state is gone, reproduction was NOT ASKED. Returning
    False there would blame the body for a question nobody could put."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    _write(repo, "ideation/cross-reference.yaml", yaml.safe_dump(
        {"schema_version": 1, "kind": "ideation-cross-reference",
         "generation": {"source_revision": orphan}, "topic_entries": []},
        sort_keys=False))
    _commit(repo, "index pinning the orphan")
    clone = tmp_path / "isolated-repro"
    subprocess.run(["git", "clone", "-q", "--no-local", f"file://{repo}",
                    str(clone)], capture_output=True, check=True)
    ok, detail = ir.index_reproduces_at(clone, orphan)
    assert ok is None
    assert "NOT ASKED rather than answered" in detail


def test_only_the_index_pair_claims_byte_comparable_reproduction():
    """The landing obligation is DEFINED by reproduction, and the class states
    which members can answer it in bytes at all. Four do; the rest owe a named
    measurement. This is the boundary that keeps requirement 3 satisfiable —
    demanding bytes universally would silently oblige a generator for every
    artifact family in the inventory."""
    tool = {m.id for m in pc.tool_defined_members()}
    assert {"cross-reference-index", "cross-reference-rendered"} <= tool
    assert "spec-traceability" not in tool
    assert "proposal-support-manifest" not in tool
    # ...and every tool-defined member that is CURRENT is one of the index pair;
    # the others are future dashboard snapshots whose builder does re-derive.
    current_tool = {m.id for m in pc.tool_defined_members()
                    if m.presence == pc.CURRENT}
    assert current_tool == {"cross-reference-index",
                            "cross-reference-rendered"}


def test_the_landing_obligation_is_discoverable_where_it_binds(tmp_path):
    """`tasks.md` § 2.8: requirement 3 is STATED, NOT AUTOMATED — a landing is
    performed by humans and merge buttons, and a branch-side check would have to
    run BEFORE the rewrite, because after it the state a regeneration would read
    is gone. What the realization owes is that the obligation is DISCOVERABLE at
    the moment it binds. It is: the probe's failure text names the route the
    artifact's own class allows, rather than leaving a reader to find the rule."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    verdict, reason, _ = ir.verify_pin_reachability(repo, allow_remote=False)
    assert verdict == ir.PIN_PROBE_FAIL
    assert "REPAIR ROUTES:" in reason
    assert "RETENTION" in reason
    assert orphan in reason


# =========================================================================
# doc-health requirement 4 — the DECLARATION is checked, both directions
# =========================================================================

def test_an_artifact_whose_pin_no_declared_member_covers_is_reported(tmp_path):
    """Delta scenario "An artifact carries a pin no declared class covers". The
    fixture is the real defect class: a NEW generator lands an artifact in a
    swept area under a vocabulary key, and no member covers it."""
    repo, _, _ = orphaned_pin_repo(tmp_path)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _write(repo, "health/new-lane/2026-08-27/run.yaml",
           f"schema_version: 1\nkind: new_lane_run\nstatus: record\n"
           f"source_revision: {head}\n")
    _commit(repo, "a lane nobody declared")

    report = _verify(repo)
    uncovered = [s for s in report.uncovered]
    assert len(uncovered) == 1
    assert uncovered[0].path == "health/new-lane/2026-08-27/run.yaml"
    assert uncovered[0].key == "source_revision"
    assert uncovered[0].pin == head
    assert not report.clean, (
        "the run MUST NOT report the class as fully verified with a coverage "
        "gap standing")
    assert not report.fully_verified

    verdict, reason, _ = ir.verify_pin_reachability(repo, allow_remote=False)
    assert verdict == ir.PIN_PROBE_FAIL
    assert "health/new-lane/2026-08-27/run.yaml" in reason
    assert "no declared class member covers" in reason


def test_a_declared_member_whose_artifact_vanished_is_reported(tmp_path):
    """The other direction of declaration drift: a registry row left behind by
    a deletion. A declaration that is only ever checked one way rots in the
    other.

    Asserted DIFFERENTIALLY, and the fixture wears the declaration-subject
    markers on purpose. `PIN_CLASS` is a statement about openxFactory's own
    artifacts, so most rows legitimately match nothing in a small fixture; what
    the test has to establish is that removing THIS artifact moves THIS row into
    the vanished set and nothing else with it."""
    repo, old = reachable_pin_repo(tmp_path)
    for marker in pc.DECLARATION_SUBJECT_MARKERS:
        _write(repo, marker, "schema_version: 1\n")
    _commit(repo, "declaration-subject markers")
    before = {m.id for m in _verify(repo).vanished}
    assert "ideation-readiness-run" not in before

    _git(repo, "rm", "-q", READINESS_REL)
    _commit(repo, "the lane's records are removed")
    after = {m.id for m in _verify(repo).vanished}
    assert after - before == {"ideation-readiness-run"}
    assert not _verify(repo).clean


def test_the_vanished_direction_is_answered_only_for_its_own_repository(
        tmp_path):
    """An absent artifact means something only in the repository the
    declaration describes. Answered anywhere else, every row would "vanish" and
    the report would be noise a reader learns to ignore — which is how a real
    vanished row gets missed."""
    repo, _ = reachable_pin_repo(tmp_path, name="not-openxfactory")
    paths = pc.committed_paths(repo)
    assert not pc.is_declaration_subject(paths)
    assert _verify(repo).vanished == ()
    assert _verify(repo).clean


def test_a_future_member_that_starts_carrying_pins_is_reported(tmp_path):
    """The arrival case the four schema-declared members exist for: the day a
    dashboard snapshot index lands committed, its pins join the class, and
    nobody will remember to promote the row. The run says so."""
    repo, old = reachable_pin_repo(tmp_path)
    assert _verify(repo).arrived == ()

    _write(repo, "health/ideation-dashboard/openxFactory-snapshot.json",
           '{\n  "kind": "ideation-dashboard-snapshot",\n'
           f'  "source_revision": "{old}"\n}}\n')
    _commit(repo, "the first committed snapshot lands")
    arrived = {m.id for m, _ in _verify(repo).arrived}
    assert "ideation-dashboard-snapshot" in arrived
    assert not _verify(repo).clean


def test_every_current_member_of_the_declared_class_is_carried_somewhere():
    """The declaration measured against the real repository, forward direction:
    every row declared CURRENT matches a committed artifact, and every FUTURE
    row still has no committed instance. This is the test that fails the day a
    generator is retired or a future member arrives."""
    repo = Path(REPO_ROOT)
    if pc.resolve_main(repo) is None:
        pytest.skip(f"{repo} resolves no `main`")
    report = pc.verify(repo)
    assert report.vanished == (), (
        "declared CURRENT member(s) match no committed artifact: "
        + ", ".join(m.id for m in report.vanished))
    assert report.arrived == (), (
        "declared FUTURE member(s) now carry committed pins; promote the row: "
        + ", ".join(m.id for m, _ in report.arrived))


def test_no_deterministic_check_family_is_added_by_this_verification():
    """The doc-health scenario's second bullet, and packet OD-2. Asserted
    STRUCTURALLY rather than by counting: a count breaks the day an unrelated
    change registers a family, and what matters is that this verification
    registers none and cannot be registered by accident.

    The enumeration requirement is the one requirement every new family must
    restate in full, and a `MODIFIED` block replaces its counterpart wholesale —
    so a family added here would put canon's family list at the mercy of archive
    order beside `add-modified-block-currency-check`'s own restatement. A
    verification that needs no family declines the hazard entirely."""
    assert not [f for f in families.FAMILIES if "pin-reach" in f]
    assert not [f for f in families.FAMILIES if f.startswith("derived-pin")]
    assert not [name for name in dir(pc) if name.startswith("fam_")]
    source = (Path(REPO_ROOT) / "scripts/doc_health/families.py").read_text(
        "utf-8")
    assert "pin_class" not in source, (
        "the class verification must not be reachable from the family registry, "
        "or a later edit registers it as a family without deciding to")


# =========================================================================
# the declaration's own mechanics
# =========================================================================

@pytest.mark.parametrize("glob,path,expected", [
    ("openspec/changes/*/evidence/f0-*.yaml",
     "openspec/changes/x/evidence/f0-results.yaml", True),
    ("openspec/changes/*/evidence/f0-*.yaml",
     "openspec/changes/archive/x/evidence/f0-results.yaml", False),
    ("ideation/dashboard/gate-records/**/*.gate-action.yaml",
     "ideation/dashboard/gate-records/a/b/c.gate-action.yaml", True),
    ("health/ideation-readiness/*/*.yaml",
     "health/ideation-readiness/2026-08-24/a/b.yaml", False),
    ("ideation/brainstorm/**/routing.yaml",
     "ideation/brainstorm/inbox/XFI-2026-001/routing.yaml", True),
    ("ideation/brainstorm/**/routing.yaml",
     "ideation/brainstorm/routing.yaml", True),
])
def test_a_single_star_does_not_cross_a_path_separator(glob, path, expected):
    """`fnmatch`'s `*` crosses `/`, so a member glob delegated to it would have
    a wider scope than it reads — `openspec/changes/*/evidence/` would silently
    swallow the archive. The archived members are declared separately ON PURPOSE
    so the scope is visible in the declaration."""
    assert pc.path_matches(path, (glob,)) is expected


def test_a_key_name_matches_as_a_key_not_as_a_substring():
    """THE DEFECT THE FIRST REAL-REPOSITORY RUN FOUND. Without a key boundary,
    `commit` matches the tail of `consumer_commit`, and the hermes handoff
    receipt's CROSS-REPOSITORY consumer pin was reported as a repo-local orphan.
    A substring match on a key name is not a key."""
    line = '  consumer_commit: 85e476b0d29ce1f63a21d1b1e59519cca8ace92b'
    assert pc._field_re("commit").search(line) is None
    assert pc._field_re("consumer_commit").search(line) is not None
    # ...both serializations, and the same guard in the sweep vocabulary.
    assert pc._field_re("commit").search(
        '  commit: 85e476b0d29ce1f63a21d1b1e59519cca8ace92b') is not None
    assert pc._field_re("commit").search(
        '    "commit": "85e476b0d29ce1f63a21d1b1e59519cca8ace92b",'
    ) is not None
    assert pc._VOCAB_RE.search(line).group(1) == "consumer_commit"


def test_locality_is_read_out_of_the_artifact_where_the_artifact_declares_it():
    """The delta's locality clause: only repo-local pins are answerable against
    this repository's refs. A routing record's entries name their OWN
    repository, and a hub record pinning a Ledgerx brainstorm must not be
    answered here. One file, two localities — and the block walk must not read
    the NEXT entry's repository."""
    member = next(m for m in pc.PIN_CLASS if m.id == "ideation-routing-source")
    text = ("sources:\n"
            "  - repository: xFactories/LedgerxFactory\n"
            "    path: ideation/brainstorm/a.md\n"
            "    revision: " + "a" * 40 + "\n"
            "  - repository: openxFactory\n"
            "    path: ideation/brainstorm/b.md\n"
            "    revision: " + "b" * 40 + "\n")
    sites = pc._sites_in(text, member, "ideation/brainstorm/x/routing.yaml")
    assert [(s.pin[0], s.locality) for s in sites] == [
        ("a", pc.CROSS_REPOSITORY), ("b", pc.REPO_LOCAL)]
    assert "xFactories/LedgerxFactory" in sites[0].locality_why

    # A JSON record whose locality key follows the pin, and is spelled `repo`.
    baseline = next(m for m in pc.PIN_CLASS
                    if m.id == "neutrality-drift-baseline")
    json_text = ('{\n  "commit": "' + "c" * 40 + '",\n'
                 '  "repo": "codexFactory",\n  "schema_version": 1\n}\n')
    site = pc._sites_in(json_text, baseline,
                        "health/neutrality-drift/baseline/x.json")[0]
    assert site.locality == pc.CROSS_REPOSITORY
    assert "codexFactory" in site.locality_why


def test_the_declaration_has_no_duplicate_rows_and_states_every_field():
    """A registry is only an authority if it is well formed. Cheap, and it is
    how a copy-paste row that shadows another gets caught before it silently
    covers a path the original was meant to."""
    ids = [m.id for m in pc.PIN_CLASS]
    assert len(ids) == len(set(ids))
    keyed = [(m.id, m.key) for m in pc.PIN_CLASS]
    assert len(keyed) == len(set(keyed))
    for member in pc.PIN_CLASS:
        assert member.paths and member.key and member.note
        assert member.key_form in {"field", "prose"}
        assert member.reproduction in {pc.TOOL_DEFINED, pc.MEASURED}
        assert member.locality in {pc.REPO_LOCAL, pc.CROSS_REPOSITORY}
        assert member.presence in {pc.CURRENT, pc.FUTURE}
        if member.key_form == "prose":
            assert member.pattern, "a prose member must state its own pattern"
    for row in pc.NON_MEMBERS:
        assert row.paths and len(row.reason) > 40


def test_the_two_prose_members_are_lifted_out_of_prose():
    """The pins a key-name scanner misses, exercised on the real spellings: the
    rendered index line and a gate-action `notes:` sentence."""
    rendered = next(m for m in pc.PIN_CLASS
                    if m.id == "cross-reference-rendered")
    sha = "4e57009c0a1aed9bdbe3c0f6cc5ca948e15ec8cc"
    got = rendered.line_re().search(f"- Source revision: `{sha}`")
    assert got and got.group(1) == sha

    action = next(m for m in pc.PIN_CLASS if m.id == "gate-action-record")
    prose = ("notes: 'staging workbench scope: staged x · keyword-lens\n"
             f"  recipe: checked none · pinned none · at source_revision {sha}'")
    hits = [m.group(1) for m in action.line_re().finditer(prose)]
    assert hits == [sha]


# =========================================================================
# the real repository — the proof that decays if anything moves
# =========================================================================

def _real_report():
    repo = Path(REPO_ROOT)
    if pc.resolve_main(repo) is None:
        pytest.skip(f"{repo} resolves no `main` "
                    f"({', '.join(pc.MAIN_REF_ORDER)}); reachability is a fact "
                    "about the clone here, not about any artifact")
    truncated, observed = pc.is_truncated(repo)
    if truncated:
        pytest.skip(f"{repo} cannot answer the question: {observed}")
    report = pc.verify(repo)
    # The retention half of the ref set is a REMOTE read, so a machine with no
    # network answers "I could not ask" rather than "there is no such ref". That
    # is an environment condition, not a defect in an artifact, and the honest
    # outcome is a skip. It is NOT allowed to be a silent one: the precondition
    # itself is asserted by
    # `test_this_repository_can_consult_the_retention_namespace`, which fails
    # loudly once, so a lost proof is never a green scoreboard.
    unaskable = [r for r in report.inconclusive
                 if "could not be consulted" in r.how]
    if unaskable:
        pytest.skip(
            "the retention namespace could not be consulted, so "
            f"{len(unaskable)} pin(s) are unanswerable here rather than "
            f"unreachable: {unaskable[0].how}")
    return repo, report


def test_this_repository_resolves_the_main_half_of_the_ref_set():
    """A GUARD AGAINST THE SILENT-SKIP CLASS, and it FAILS rather than skips.

    Every real-repository proof below degrades to a skip when no `main` ref
    resolves, and a suite full of skips is how seven proofs went unrun for a
    packet's entire life — the defect `harden-ideation-readiness-check` was
    filed over. So the precondition itself is asserted: if a clone or a CI
    checkout stops providing `main`, THIS test says so once, loudly, instead of
    six others quietly reporting SKIPPED on a green scoreboard.

    `actions/checkout@v4` at `fetch-depth: 0` fetches every head into
    `refs/remotes/origin/*`, so the first spelling is present in CI; a plain
    `git clone` provides it too."""
    repo = Path(REPO_ROOT)
    resolved = pc.resolve_main(repo)
    assert resolved is not None, (
        f"{repo} resolves none of {pc.MAIN_REF_ORDER}, so the branch half of "
        "the ref set cannot be consulted and every reachability proof in this "
        "module degrades to a skip. Fetch `main`, or fix the checkout that "
        "stopped providing it — do not leave the proofs skipping.")
    ref, sha = resolved
    assert ref in pc.MAIN_REF_ORDER
    assert pc.FULL_SHA_RE.match(sha)
    truncated, observed = pc.is_truncated(repo)
    if truncated:
        pytest.skip(f"{repo} is genuinely truncated, which is a fact about the "
                    f"clone rather than a configuration defect: {observed}")


def test_this_repository_can_consult_the_retention_namespace():
    """THE SECOND PRECONDITION, and it FAILS rather than skips for the same
    reason the first one does.

    Three of this repository's pins resolve ONLY through
    `refs/retention/pins/<full-sha>`, no default refspec fetches that namespace,
    and so the check is a REMOTE read. A machine that cannot perform it answers
    "I could not ask" — which `_real_report` correctly turns into a skip,
    because it is a fact about the environment. Asserted here so that fact is
    stated ONCE, loudly, instead of six proofs going quiet: a suite that reports
    SKIPPED where it used to report the pins conforming has lost a proof, and
    losing proofs silently is the defect this whole packet descends from."""
    repo = Path(REPO_ROOT)
    if pc.resolve_main(repo) is None:
        pytest.skip(f"{repo} resolves no `main`; see the precondition above")
    found, detail = pc.remote_retention_refs(repo)
    assert found is not None, (
        f"the retention half of the ref set is unreachable from {repo}: "
        f"{detail}. Three committed pins resolve only through it, so every "
        "real-repository proof in this module degrades to a skip until this "
        "works. Restore network access to `origin`, or fetch the namespace "
        f"locally (`git fetch origin '{pc.RETENTION_NAMESPACE}/*:"
        f"{pc.RETENTION_NAMESPACE}/*'`).")
    assert len(found) >= 3, (
        f"{detail} — this repository has published three retention refs; a "
        "namespace that advertises fewer has lost one, and a lost retention ref "
        "orphans the record that pins it")
    for ref, sha in found.items():
        assert ref == pc.retention_ref(sha), (
            f"{ref} points at {sha}, which is not the commit its name states — "
            "a retention ref whose name cannot be derived from its target "
            "retains nothing a reader can find")


def test_every_declared_repo_local_pin_in_this_repository_resolves():
    """THE ACCEPTANCE SIGNAL, asserted where it will decay. Every repo-local pin
    the declared class carries resolves against `main` or through its own
    computed retention ref — including the three that resolve ONLY through the
    namespace, which is the intended end state for them rather than a tolerated
    one. This is the check that would have caught all four orphans on the day
    each landed."""
    repo, report = _real_report()
    assert report.orphans == [], "\n".join(
        [f"{r.site.named()} — {r.how}" for r in report.orphans])
    assert report.uncovered == (), "\n".join(
        s.named() for s in report.uncovered)
    assert report.clean

    retained = [r for r in report.results if r.verdict == pc.PASS
                and "retained" in r.how]
    assert len(retained) >= 3, (
        "the three retention-resolved pins are the packet's worked example; "
        f"found {len(retained)}: {[r.site.pin for r in retained]}")
    for result in retained:
        assert pc.retention_ref(result.site.pin) in result.how
        assert not pc.reachable_from_main(repo, result.site.pin,
                                          report.main_ref), (
            "a retained pin that main ALSO reaches proves nothing about the "
            "namespace")


def test_every_committed_commit_shaped_value_that_resolves_is_covered():
    """THE VOCABULARY'S OWN COVERAGE, measured rather than assumed — and the
    test that would have caught `us3_baseline_commit`.

    Every 40-hex token in every swept committed file is resolved against the
    object database, and every one that IS a commit must be covered by a
    declared member. A key nobody enumerated is exactly how a real pin goes
    unswept, and enumerating the KEYS is guesswork where resolving the VALUES is
    a measurement.

    ITS LIMIT IS STATED: a pin whose object is already gone does not resolve, so
    this direction cannot find it. That is why `us3_baseline_commit` had to be
    found by enumerating key names once, by hand, and why the row it produced
    lives in the declaration where the next reader will see it."""
    repo, _ = _real_report()
    paths = pc.committed_paths(repo)
    declared = {(s.path, s.pin) for s in pc.member_sites(repo, "HEAD",
                                                         paths=paths)}
    candidates: dict[str, set[str]] = {}
    for path in paths:
        if not path.endswith(pc.SCAN_SUFFIXES):
            continue
        if not pc.path_matches(path, pc.SCAN_ROOTS):
            continue
        if pc.non_member_reason(path) is not None:
            continue
        text = pc.committed_text(repo, "HEAD", path)
        if text is None:
            continue
        for token in set(pc.LOOSE_SHA_RE.findall(text)):
            candidates.setdefault(token, set()).add(path)

    tokens = sorted(candidates)
    batch = subprocess.run(["git", "-C", str(repo), "cat-file",
                            "--batch-check"],
                           input="\n".join(tokens) + "\n",
                           capture_output=True, text=True)
    uncovered = []
    for line in batch.stdout.splitlines():
        parts = line.split()
        if len(parts) < 2 or parts[1] != "commit":
            continue
        for path in sorted(candidates[parts[0]]):
            if (path, parts[0]) not in declared:
                uncovered.append(f"{path} carries commit {parts[0]}")
    assert not uncovered, (
        "committed artifact(s) carry a value that RESOLVES TO A COMMIT of this "
        "repository and no declared class member covers it — declare the "
        "member, or declare the file a non-member with a reason:\n  "
        + "\n  ".join(uncovered))


def test_the_landed_index_reproduces_from_the_corpus_at_its_own_pin():
    """Requirement 3's reproduction obligation on the one member whose tooling
    defines derivation, run against the real repository. `harden-ideation-
    readiness-check` proved its re-pin this way at three revisions; this keeps
    the property asserted rather than re-established each time somebody
    wonders."""
    repo, _ = _real_report()
    index_rel = "ideation/cross-reference.yaml"
    if not (repo / index_rel).is_file():
        pytest.skip(f"{repo} carries no {index_rel} of its own")
    pin = yaml.safe_load(
        pc.committed_text(repo, "HEAD", index_rel))["generation"][
            "source_revision"]
    ok, detail = ir.index_reproduces_at(repo, pin)
    if ok is None:
        pytest.skip(detail)
    assert ok is True, detail


def test_the_rendered_twin_pins_the_same_revision_as_the_yaml_index():
    """The prose member is not decorative: a projection whose pin disagrees with
    its source claims to have been derived from a different state than the
    artifact it renders."""
    repo, report = _real_report()
    pins = {s.member_id: s.pin for s in
            pc.member_sites(repo, report.rev)
            if s.member_id in {"cross-reference-index",
                               "cross-reference-rendered"}}
    if len(pins) < 2:
        pytest.skip(f"{repo} does not carry both halves of the index pair")
    assert pins["cross-reference-index"] == pins["cross-reference-rendered"]


def test_the_readiness_records_keep_the_pins_they_were_captured_with():
    """Requirement 2's claim, demonstrated on the instances that forced it: the
    two readiness records are BYTE-IDENTICAL to capture on their pin line, and
    the repair happened to the COMMIT rather than to them. The literals are
    spelled out because a test that read the pin out of the file it is checking
    would pass after somebody edited both."""
    repo, report = _real_report()
    expected = {
        "health/ideation-readiness/2026-08-24/"
        "brainstorm-packet-migration-20260824.yaml":
            "da9bf3b7d0ee1d86d2d437d42a715c238dddce4b",
        "health/ideation-readiness/2026-08-24/"
        "brainstorm-packet-migration-final-20260824.yaml":
            "f13a3b6007736292e1e157febef1ac733e534de9",
    }
    got = {s.path: s.pin for s in pc.member_sites(repo, report.rev)
           if s.member_id == "ideation-readiness-run"}
    for path, pin in expected.items():
        if path not in got:
            pytest.skip(f"{path} is not committed in {repo}")
        assert got[path] == pin, (
            f"{path} no longer carries the pin it was captured with. A record "
            "is repaired by RETENTION, never by editing the pin — an edit here "
            "makes the record state something the run did not read.")
        result = next(r for r in report.results if r.site.path == path)
        assert result.verdict == pc.PASS
        assert pc.retention_ref(pin) in result.how


def test_the_report_says_which_ref_set_it_consulted():
    """A verdict a reader cannot audit is not evidence. The rendering names the
    `main` ref, the retention namespace, and what it observed about the clone —
    which is also how a STALE remote-tracking ref is diagnosed rather than
    disposed."""
    _, report = _real_report()
    rendered = pc.render(report)
    assert report.main_ref in rendered
    assert pc.RETENTION_NAMESPACE in rendered
    assert report.truncation in rendered
    assert re.search(r"\d+ declared pin sites across \d+ class members",
                     rendered)


def test_the_resolver_this_probe_shares_with_the_readiness_proof_agrees():
    """The probe rides the READINESS PROOF SURFACE (OD-2), so it must resolve
    the same repository that proof does. A probe that answered about a sibling
    checkout would be the defect `harden-ideation-readiness-check` fixed,
    reintroduced one module over."""
    if not (Path(REPO_ROOT) / "ideation" / "cross-reference.yaml").is_file():
        pytest.skip(f"{REPO_ROOT} carries no index of its own")
    assert tir._openxfactory_root() == Path(REPO_ROOT).resolve()
    _, _, report = ir.verify_pin_reachability(REPO_ROOT)
    assert report.rev == _git(Path(REPO_ROOT), "rev-parse", "HEAD"
                              ).stdout.strip()
