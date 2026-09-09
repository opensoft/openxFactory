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

import ast
import re
import subprocess

from collections import Counter
from pathlib import Path
from unittest import mock

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
# supersede-lost-pin-baseline — a declared loss is DISCHARGED by a superseding
# record, never by deleting the row
#
# The defect this half is pinned to is a SILENCING that was available and is
# not any more: with no discharge mechanism, the only way to make a class
# carrying a permanently lost pin report itself fully verified was to delete the
# declaration — which turns a measured, permanent defect into background noise
# and loses the measurement with it. The mechanism here restores full
# verification the other way: the governance act lands, the row CITES it, the
# verification goes and reads it, and the loss stays reported for ever.
# =========================================================================

SUPERSESSION_REL = ("openspec/changes/fixture-supersession/evidence/"
                    "pin-loss-supersession.yaml")


def _supersession_record(pin=None):
    """A minimal pin-loss supersession record. `pin=None` writes one that names
    NO pin, which is the stub case a citation must not be satisfied by."""
    body = {"schema_version": 1,
            "kind": "openxfactory-derivation-pin-loss-supersession",
            "status": "record",
            "change_id": "fixture-supersession"}
    if pin is not None:
        body["lost_pin"] = {"value": pin, "retention": "impossible"}
    return yaml.safe_dump(body, sort_keys=False)


def _fixture_loss(pin, **kw):
    kw.setdefault("path", READINESS_REL)
    kw.setdefault("key", "source_revision")
    kw.setdefault("measured", "fixture: measured unrecoverable for this test")
    kw.setdefault("owed", "a superseding record naming the loss")
    return pc.KnownLoss(pin=pin, **kw)


def test_a_declared_loss_awaiting_its_record_holds_full_verification_open(
        tmp_path, monkeypatch):
    """The state the register launched in, kept exactly. A row whose superseding
    record has not landed is LOST, is reported with its measurement and the act
    still OWED, does not redden the run — no code change repairs it — and does
    NOT let the class call itself fully verified."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    monkeypatch.setattr(pc, "KNOWN_LOSSES", (_fixture_loss(
        orphan, superseding_record=pc.SUPERSESSION_RECORD_PATHS),))

    report = _verify(repo)
    assert [r.verdict for r in report.results] == [pc.LOST]
    assert report.lost[0].discharge is None
    assert "OWED:" in report.lost[0].how
    assert report.clean, ("a loss no code change can repair must not redden an "
                          "unrelated run")
    assert report.lost_awaiting_record == report.lost
    assert not report.fully_verified


def test_a_declared_loss_with_a_committed_superseding_record_is_discharged(
        tmp_path, monkeypatch):
    """The act lands and the class is answerable again — WITHOUT the row moving.

    Three things are asserted together because the value is in their
    conjunction: the loss is still LOST and still carries its measurement, the
    report names where the discharging record stands, and `fully_verified` is
    True. A mechanism that produced the third by dropping the first two would be
    the silencing this replaces."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    _write(repo, SUPERSESSION_REL, _supersession_record(orphan))
    _commit(repo, "issue the superseding record")
    monkeypatch.setattr(pc, "KNOWN_LOSSES", (_fixture_loss(
        orphan, superseding_record=pc.SUPERSESSION_RECORD_PATHS,
        discharged="fixture: the standing the archived evidence keeps"),))

    report = _verify(repo)
    assert [r.verdict for r in report.results] == [pc.LOST]
    assert report.lost[0].discharge == SUPERSESSION_REL
    assert "DECLARED UNRECOVERABLE:" in report.lost[0].how
    assert "DISCHARGED:" in report.lost[0].how
    assert report.lost_awaiting_record == []
    assert report.fully_verified

    rendered = pc.render(report)
    assert "[LOST]" in rendered, "a discharged loss is still reported as lost"
    assert SUPERSESSION_REL in rendered
    assert "1 lost (declared unrecoverable, 0 awaiting" in rendered

    # ...and the record itself is a DECLARED non-member, so the pin it cites is
    # not swept as an undeclared pin site. Declared, not dodged by key choice.
    assert pc.non_member_reason(SUPERSESSION_REL) is not None
    assert report.uncovered == ()


def test_a_superseding_record_that_does_not_name_the_pin_discharges_nothing(
        tmp_path, monkeypatch):
    """MEASURED, NEVER TRUSTED. The row says where the record stands; the
    verification reads it there and requires it to name the pin it supersedes. A
    stub at the right path — or a record deleted after the row cited it — leaves
    the loss awaiting, which is the difference between a citation and a
    claim."""
    repo, _, orphan = orphaned_pin_repo(tmp_path)
    _write(repo, SUPERSESSION_REL, _supersession_record(None))
    _commit(repo, "a supersession record that supersedes nothing")
    loss = _fixture_loss(orphan,
                         superseding_record=pc.SUPERSESSION_RECORD_PATHS)
    monkeypatch.setattr(pc, "KNOWN_LOSSES", (loss,))

    assert pc.discharging_record(repo, "HEAD", loss) is None
    report = _verify(repo)
    assert report.lost[0].discharge is None
    assert not report.fully_verified

    # The uncommitted case, separately: a citation is not satisfied by a working
    # tree, because the verification reads COMMITTED state.
    _write(repo, SUPERSESSION_REL, _supersession_record(orphan))
    assert pc.discharging_record(repo, "HEAD", loss) is None


def test_a_row_naming_no_record_at_all_is_the_awaiting_state(tmp_path):
    """The default. A row that cites nothing awaits its act — there is no
    implicit discharge, and an empty citation never resolves itself."""
    loss = _fixture_loss("0" * 40)
    assert loss.superseding_record == ()
    assert loss.discharged == ""
    assert pc.discharging_record(tmp_path, "HEAD", loss) is None


def test_the_declared_loss_in_this_repository_cites_a_committed_record():
    """THE ACCEPTANCE SIGNAL for the discharge, asserted where it will decay.

    Every row that cites a record must cite one this repository actually
    carries — a dangling citation is worse than a blank one, because it reads as
    discharged. And the ONE row standing today is discharged: the governance act
    `govern-derived-pin-reachability` recorded as owed has landed, so the class
    is answerable over it. A future row may legitimately await its record; this
    asserts the state of the row that exists."""
    repo = Path(REPO_ROOT)
    paths = pc.committed_paths(repo, "HEAD")
    for loss in pc.KNOWN_LOSSES:
        if not loss.superseding_record:
            continue
        record = pc.discharging_record(repo, "HEAD", loss, paths=paths)
        assert record is not None, (
            f"the row for {loss.pin} cites {loss.superseding_record} and no "
            f"committed file there names the pin — a citation nobody can read "
            f"is not a discharge")
        assert loss.discharged, (
            f"the row for {loss.pin} cites {record} but states nothing about "
            f"what that record established")

    declared = pc.known_loss("66b14064bbd50d1af4e9585d10f8150f2bc352f0")
    assert declared is not None, "the unrecoverable US3 baseline stays declared"
    assert pc.discharging_record(repo, "HEAD", declared,
                                 paths=paths) is not None, (
        "this repository's one unrecoverable loss is discharged by the "
        "supersede-lost-pin-baseline record; if that record moved, the row's "
        "citation moves with it")


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


# =========================================================================
# ruling D-8(a) — historical evidence, and a rolling population
#
# The pin class launched asking ONE question of every member: does the
# revision this artifact names still resolve? `gate-intent-snapshot-rev`
# was the first row for which that question is the wrong one, and it
# arrived committed on 2026-09-08 with the live intent-plane dispatch
# exercise. Two properties, measured on the four real records:
#
#   D. A REFUSAL RECORD CITING AN UNRESOLVABLE REVISION IS THE RECORD
#      WORKING. `snapshot_rev_seen` is the revision the actor was LOOKING
#      AT, and the apply lane's whole job is to refuse an intent whose view
#      went stale — so this repository's 2026-08-15 refusal cites
#      `66ca33fd…` precisely because nothing can resolve it. Reported as an
#      orphan, it offers a repair route (retain the commit, or re-pin) that
#      would either change nothing or make the record state something
#      nobody read.
#   E. THE CENSUS OF A ROLLING POPULATION IS NOT A CONSTANT. Intents are
#      written on the dashboard's rolling branch, land through a custody PR
#      and are consumed, so `main` carries none at one revision and four at
#      the next. Frozen totals including them red on Monday and pass on
#      Tuesday with nothing drifted, and the only repair a reader can apply
#      is to bump the number.
# =========================================================================

GATE_INTENT_REL = ("ideation/dashboard/intents/pos-fixture-possible/"
                   "dispose-possible-20260908-000000-fixture.gate-intent.yaml")


def _gate_intent(pin, *, refusal="the viewed state is unverifiable"):
    """Shaped like the real refusal records: the revision the actor SAW, and
    the terminal status the apply lane wrote onto it."""
    return yaml.safe_dump(
        {"schema_version": 1, "kind": "gate-intent", "actor": "fixture",
         "verb": "dispose-possible",
         "target": {"possible_id": "pos-fixture-possible"},
         "args": {"outcome": "deferred"},
         "requested_at": "2026-09-08T00:00:00Z",
         "snapshot_rev_seen": pin, "status": "refused",
         "refusal_reason": refusal},
        sort_keys=False)


def _unreachable_commit(repo):
    """A commit NO REF REACHES, made the way the real orphans were: a side
    branch, a commit on it, the branch deleted. The object survives in this
    repository's own store, which is exactly why `cat-file` is not the probe."""
    _git(repo, "checkout", "-q", "-b", "side")
    _write(repo, "ideation/brainstorm/side.md", "# side\n\nStatus: brainstorm\n")
    sha = _commit(repo, "a view that later left the graph")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "branch", "-qD", "side")
    return sha


def _subject_markers(repo):
    for marker in pc.DECLARATION_SUBJECT_MARKERS:
        _write(repo, marker, "schema_version: 1\n")


def test_a_gate_intent_citing_a_view_no_ref_reaches_is_historical(tmp_path):
    """DEFECT (D), planted with a SYNTHETIC unreachable revision so the proof
    does not depend on the four real records staying where they are.

    The verdict is its own, beside reachable and orphaned rather than inside
    either: calling it reachable would claim a resolution nobody performed, and
    calling it an orphan would open a repair route for a record doing the one
    thing it exists to do. `clean` and `fully_verified` both hold."""
    repo, _ = reachable_pin_repo(tmp_path)
    unseen = _unreachable_commit(repo)
    _write(repo, GATE_INTENT_REL, _gate_intent(unseen))
    _commit(repo, "the gate console's refusal record lands")

    report = _verify(repo)
    [result] = [r for r in report.results
                if r.site.member_id == "gate-intent-snapshot-rev"]
    assert result.verdict == pc.HISTORICAL
    assert report.historical == [result]
    assert report.orphans == []
    assert report.clean
    assert report.fully_verified

    # THE SITE IS STILL SWEPT AND STILL SHAPE-CHECKED. What the exemption
    # removes is the resolution question, not the coverage one: an intent
    # carrying something that is not a 40-hex revision, or an intent sitting
    # outside the declared tree, is a finding as much as it ever was.
    assert pc.FULL_SHA_RE.match(result.site.pin)
    assert pc.path_matches(result.site.path,
                           ("ideation/dashboard/intents/**",))
    assert result.site.key == "snapshot_rev_seen"
    assert report.uncovered == ()

    # ...and it says WHY, in the report rather than in a commit message.
    assert "records the revision this artifact SAW" in result.how
    assert "no repair route is owed" in result.how
    assert "[hist]" in pc.render(report)


def test_the_same_unreachable_commit_still_orphans_outside_the_intents_tree(
        tmp_path):
    """THE DIFFERENTIAL, and the reason the exemption is declared on the CLASS
    rather than granted to the commit. One revision, two records citing it: the
    gate intent testifies to a view and is exempt, the readiness record claims a
    derivation and is not. If the exemption ever widened into "this commit is
    allowed to be gone", THIS is the test that reddens — and the widening is the
    only way the rule could quietly stop catching real orphans."""
    repo, _ = reachable_pin_repo(tmp_path)
    unseen = _unreachable_commit(repo)
    _write(repo, GATE_INTENT_REL, _gate_intent(unseen))
    _write(repo, READINESS_REL, _readiness_record(unseen))
    _commit(repo, "one revision, cited by both kinds of record")

    report = _verify(repo)
    verdicts = {r.site.member_id: r.verdict for r in report.results}
    assert verdicts["gate-intent-snapshot-rev"] == pc.HISTORICAL
    assert verdicts["ideation-readiness-run"] == pc.ORPHAN
    assert [r.site.member_id for r in report.orphans] == [
        "ideation-readiness-run"]
    assert not report.clean


def test_a_gate_intent_whose_view_main_still_reaches_is_reported_reachable(
        tmp_path):
    """A TRUE AND FREE OBSERVATION IS STILL MADE. The exemption is from OWING
    resolution, not from being asked: `main` is a local ancestry query, so an
    intent whose view is still in the graph reports PASS like anything else.
    Three of the four real records are in exactly this state, and reporting
    them HISTORICAL would throw away a fact the run already has."""
    repo, old = reachable_pin_repo(tmp_path)
    _write(repo, GATE_INTENT_REL, _gate_intent(old, refusal="index rejected"))
    _commit(repo, "a refusal whose view is still on main")

    report = _verify(repo)
    [result] = [r for r in report.results
                if r.site.member_id == "gate-intent-snapshot-rev"]
    assert result.verdict == pc.PASS
    assert "ancestor of" in result.how
    assert report.historical == []
    assert report.fully_verified


def test_the_historical_class_is_answered_without_consulting_the_remote(
        tmp_path):
    """THE PROPERTY THAT KEEPS A CONFORMING RECORD OFF THE UNANSWERED PILE.
    The retention namespace is a REMOTE read, and a machine that cannot perform
    it answers INCONCLUSIVE — which is honest for a pin that OWES resolution and
    wrong for one that does not, because it would hold `fully_verified` open on
    an artifact with nothing left to prove.

    Asserted DIFFERENTIALLY with `allow_remote=True` on a fixture that has no
    remote at all: the historical pin answers, the derivation pin cannot."""
    repo, _ = reachable_pin_repo(tmp_path)
    unseen = _unreachable_commit(repo)
    _write(repo, GATE_INTENT_REL, _gate_intent(unseen))
    _commit(repo, "only the historical pin is unreachable")

    report = pc.verify(repo, allow_remote=True)
    assert [r.verdict for r in report.results
            if r.site.member_id == "gate-intent-snapshot-rev"] == [
                pc.HISTORICAL]
    assert report.inconclusive == []
    assert report.fully_verified
    assert "NOT consulted for this class" in report.historical[0].how

    # ...and the contrast: the same unreachable revision under a MUST_RESOLVE
    # member DOES reach for the namespace, and says it could not be asked.
    _write(repo, READINESS_REL, _readiness_record(unseen))
    _commit(repo, "a derivation pin on the same revision")
    contrast = pc.verify(repo, allow_remote=True)
    assert [r.site.member_id for r in contrast.inconclusive] == [
        "ideation-readiness-run"]
    assert "could not be consulted" in contrast.inconclusive[0].how
    assert not contrast.fully_verified


def _init_named(root, branch):
    """`_init`, but on a branch NOT named `main` — the only way to make
    `pc.resolve_main` genuinely return `None` in a fixture rather than merely
    omitting a commit."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", branch)
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    return root


def test_a_main_less_clone_is_inconclusive_and_a_main_ed_one_is_historical_or_pass(
        tmp_path):
    """THE BUG (Copilot review, PR #816, `pin_class.py:~2170`): the historical
    branch answered every intent site HISTORICAL even when `main_ref is None`,
    reporting "not reached by main" on a question this branch never actually
    asked — a clone that resolves no `main` cannot ask whether `main` reaches
    anything. `main_ref is None` is the SAME "the branch half of the ref set
    could not be consulted" condition every MUST_RESOLVE member already
    answers INCONCLUSIVE with, and this member owes the identical answer:
    HISTORICAL is reserved for the concrete "asked of `main`, and not
    reached" outcome, never substituted for "there was no `main` to ask".

    ONE repository, THREE states, so a single fixture proves all three
    verdicts rather than three fixtures each proving one in isolation:
      1. no branch named `main` at all (and no `origin` remote either) ->
         INCONCLUSIVE.
      2. `main` created, reaching the cited revision -> PASS.
      3. a later intent citing a revision `main` (frozen at its creation
         point) will never reach -> HISTORICAL.
    """
    repo = _init_named(tmp_path / "no-main", "trunk")
    _write(repo, "ideation/brainstorm/one.md", "# one\n\nStatus: brainstorm\n")
    old = _commit(repo, "corpus, on a branch that is not main")
    _write(repo, GATE_INTENT_REL, _gate_intent(old))
    _commit(repo, "an intent citing the corpus commit")
    assert pc.resolve_main(repo) is None
    assert _git(repo, "remote").stdout.strip() == ""

    # 1. no `main` in this clone at all.
    report = _verify(repo)
    [result] = [r for r in report.results
                if r.site.member_id == "gate-intent-snapshot-rev"]
    assert result.verdict == pc.INCONCLUSIVE
    assert "no `main` in this clone" in result.how
    assert report.historical == []
    assert not report.fully_verified

    # 2. `main` now exists and reaches the revision the intent cites -> PASS.
    _git(repo, "branch", "-q", "main", "trunk")
    report = _verify(repo)
    [result] = [r for r in report.results
                if r.site.member_id == "gate-intent-snapshot-rev"]
    assert result.verdict == pc.PASS
    assert "ancestor of" in result.how

    # 3. `main` stays put; the corpus (and the intent's view of it) moves on
    # past it -> the new view is HISTORICAL, not merely unreached-because-
    # unasked.
    _write(repo, "ideation/brainstorm/two.md", "# two\n\nStatus: brainstorm\n")
    newer = _commit(repo, "corpus moves on, main does not")
    _write(repo, GATE_INTENT_REL, _gate_intent(newer))
    _commit(repo, "the intent's view moves past main's frozen tip")
    report = _verify(repo)
    [result] = [r for r in report.results
                if r.site.member_id == "gate-intent-snapshot-rev"]
    assert result.verdict == pc.HISTORICAL
    assert "it is not reached by" in result.how


GATE_INTENT_WRONG_KIND_REL = ("ideation/dashboard/intents/pos-fixture-possible/"
                              "not-a-gate-intent-20260908-000000.yaml")


def _gate_intent_wrong_kind(pin):
    """Same shape as `_gate_intent`, but declaring a DIFFERENT `kind` — the
    verifier finding (PR #816, `pin_class.py:~879-881`): the exemption keyed
    on the path glob plus `snapshot_rev_seen` alone would exempt ANY record —
    of any kind — dropped under this tree that happens to carry that field,
    whether or not it was ever a gate intent."""
    return yaml.safe_dump(
        {"schema_version": 1, "kind": "something-else", "actor": "fixture",
         "verb": "dispose-possible",
         "target": {"possible_id": "pos-fixture-possible"},
         "requested_at": "2026-09-08T00:00:00Z",
         "snapshot_rev_seen": pin, "status": "refused"},
        sort_keys=False)


def test_a_stray_record_of_a_different_kind_is_not_exempt(tmp_path):
    """THE TIGHTENED MATCH. A record under `ideation/dashboard/intents/**`
    carrying `snapshot_rev_seen` but a `kind` other than `gate-intent` must
    NOT inherit the historical exemption: it plants an unreachable revision
    the same way the genuine-defect fixture does, and asserts the site lands
    UNCOVERED — falling back to ordinary MUST_RESOLVE handling rather than
    being silently waved through — and that the class is no longer clean."""
    repo, _ = reachable_pin_repo(tmp_path)
    unseen = _unreachable_commit(repo)
    _write(repo, GATE_INTENT_WRONG_KIND_REL, _gate_intent_wrong_kind(unseen))
    _commit(repo, "a stray record under the intents tree, wrong kind")

    report = _verify(repo)
    assert [r for r in report.results
            if r.site.path == GATE_INTENT_WRONG_KIND_REL] == [], (
        "a record whose kind is not gate-intent must not be attributed to "
        "gate-intent-snapshot-rev at all")
    uncovered_paths = {s.path for s in report.uncovered}
    assert GATE_INTENT_WRONG_KIND_REL in uncovered_paths, (
        "a record of a kind other than gate-intent must not silently inherit "
        "gate-intent-snapshot-rev's historical exemption")
    assert not report.clean

    # THE GENUINE ARTICLE, IN THE SAME COMMIT, IS UNAFFECTED: the tightened
    # match narrows what counts as a gate intent, it does not touch how a real
    # one is judged.
    _write(repo, GATE_INTENT_REL, _gate_intent(unseen))
    _commit(repo, "and a real gate intent citing the same unreachable view")
    report = _verify(repo)
    [real] = [r for r in report.results
              if r.site.member_id == "gate-intent-snapshot-rev"]
    assert real.verdict == pc.HISTORICAL
    assert GATE_INTENT_WRONG_KIND_REL in {s.path for s in report.uncovered}


def test_uncovered_sites_only_rereads_text_for_the_requires_field_member(
        tmp_path):
    """Copilot review, PR #816, `pin_class.py:1727`. `uncovered_sites` used to
    fetch every candidate path's committed text a SECOND time (via
    `text_cache`) to resolve `covering_member`, even though `swept_sites`
    above it had already read the same file once to find the site — one
    extra `git show` per candidate path, paid even by the ordinary member
    that never consults that text at all. The fix reads it a second time
    ONLY when the site's already-matched member declares `requires_field`
    (today, only `gate-intent-snapshot-rev`).

    One repository, two commit-shaped sites: an ordinary readiness record and
    a real gate intent, spied with `committed_text` wrapped so every call and
    its path are observable."""
    repo, old = reachable_pin_repo(tmp_path)
    _write(repo, GATE_INTENT_REL, _gate_intent(old, refusal="index rejected"))
    _commit(repo, "an ordinary readiness record and a real gate intent")

    with mock.patch.object(pc, "committed_text",
                           wraps=pc.committed_text) as spy:
        pc.uncovered_sites(repo, "HEAD")
    counts = Counter(call.args[2] for call in spy.call_args_list)

    # The readiness record's matched member (`ideation-readiness-run`)
    # declares no `requires_field`: read once, by `swept_sites`, never again.
    assert counts[READINESS_REL] == 1
    # The gate intent's matched member (`gate-intent-snapshot-rev`) DOES
    # declare one (`kind`): read once by `swept_sites`, and once more to
    # confirm the companion field.
    assert counts[GATE_INTENT_REL] == 2


def test_non_pin_sites_resolution_loop_only_rereads_the_requires_field_member(
        tmp_path, monkeypatch):
    """Same defect, same fix, in the sibling caller named alongside it
    (`pin_class.py:~1913`): `non_pin_sites`' own uncovered-resolution loop
    must not re-read a candidate's text unless the matched member declares
    `requires_field`.

    `member_non_pin_sites` is stubbed to report nothing pre-classified, so
    every non-commit value `swept_non_pin_sites` finds is forced through the
    resolution loop under test rather than being screened out by the
    sibling's own (broader, requires_field-blind) pass first — isolating the
    exact code the review comment named."""
    repo, _ = reachable_pin_repo(tmp_path)
    _write(repo, READINESS_REL,
          _readiness_record("sentinel-not-a-commit-value"))
    _write(repo, GATE_INTENT_WRONG_KIND_REL,
          _gate_intent_wrong_kind("sentinel-not-a-commit-value-2"))
    _commit(repo, "a non-commit value under an ordinary key, and one under "
                 "the requires_field member's key on a wrong-kind record")

    monkeypatch.setattr(pc, "member_non_pin_sites",
                        lambda *a, **kw: ([], []))

    with mock.patch.object(pc, "committed_text",
                           wraps=pc.committed_text) as spy:
        classified, uncovered, absent = pc.non_pin_sites(repo, "HEAD")
    counts = Counter(call.args[2] for call in spy.call_args_list)

    # The ordinary member's file: read once, by `swept_non_pin_sites`, and
    # never again by the resolution loop.
    assert counts[READINESS_REL] == 1
    # The requires_field member's file: read once by `swept_non_pin_sites`,
    # and once more by the resolution loop to confirm the companion field —
    # which fails here (`kind: something-else`), so the site lands uncovered.
    assert counts[GATE_INTENT_WRONG_KIND_REL] == 2
    assert GATE_INTENT_WRONG_KIND_REL in {s.path for s in uncovered}


def test_a_rolling_member_carrying_nothing_is_not_reported_vanished(tmp_path):
    """DEFECT (E), first half. `main` legitimately carries no intent at all
    between custody PRs, and a row that reported VANISHED every time the queue
    drained would produce a finding that comes and goes with nothing drifting —
    which is how a REAL vanished row gets missed.

    Asserted DIFFERENTIALLY against a STANDING member removed the same way in
    the same repository, and the fixture wears the declaration-subject markers
    on purpose. `PIN_CLASS` describes openxFactory's own artifacts, so most rows
    legitimately match nothing in a small fixture; what has to be established is
    that DRAINING THE QUEUE moves nothing into the vanished set while deleting a
    standing artifact moves exactly its own row."""
    repo, old = reachable_pin_repo(tmp_path)
    _subject_markers(repo)
    _write(repo, GATE_INTENT_REL, _gate_intent(old))
    _commit(repo, "declaration-subject markers, and an intent in the queue")
    assert pc.is_declaration_subject(pc.committed_paths(repo))
    queued = {m.id for m in _verify(repo).vanished}
    assert "gate-intent-snapshot-rev" not in queued
    assert "ideation-readiness-run" not in queued

    _git(repo, "rm", "-q", "-r", "ideation/dashboard/intents")
    _commit(repo, "the queue drains: the intents are consumed")
    drained = {m.id for m in _verify(repo).vanished}
    assert drained == queued, (
        "draining the intent queue moved a row into the vanished set: "
        + ", ".join(sorted(drained - queued)))
    assert "gate-intent-snapshot-rev" not in drained

    _git(repo, "rm", "-q", READINESS_REL)
    _commit(repo, "and a STANDING member's artifact is deleted")
    after = {m.id for m in _verify(repo).vanished}
    assert after - drained == {"ideation-readiness-run"}


def test_a_rolling_member_leaves_the_frozen_census_and_nothing_else(tmp_path):
    """DEFECT (E), second half, and the boundary of the exclusion: rolling
    sites leave the ARITHMETIC and stay in everything else. They are still
    swept, still verified, still reported, and still bound by "no site is
    classified twice" — the census is the only place their motion is a
    problem."""
    repo, old = reachable_pin_repo(tmp_path)
    before = _verify(repo)
    frozen = pc.standing_census(before.results)

    _write(repo, GATE_INTENT_REL, _gate_intent(old))
    _commit(repo, "an intent lands, and the census must not move")
    after = _verify(repo)
    assert pc.standing_census(after.results) == frozen
    assert len(after.results) == len(before.results) + 1
    assert ({r.site.member_id for r in after.results}
            - {r.site.member_id for r in before.results}
            == {"gate-intent-snapshot-rev"})

    pinned = {(r.site.path, r.site.key, r.site.line) for r in after.results}
    classified = {(r.site.path, r.site.key, r.site.line)
                  for r in after.non_pins}
    assert pinned & classified == set()
    assert after.uncovered == ()
    assert after.clean


def test_the_rolling_exclusion_is_read_from_the_declaration(tmp_path):
    """One home for the exclusion, so a row promoted to ROLLING joins it
    without anybody editing a census by hand — the failure mode a list of ids
    retyped in a test exists to produce."""
    assert [m.id for m in pc.rolling_members()] == ["gate-intent-snapshot-rev"]
    assert all(m.population == pc.ROLLING for m in pc.rolling_members())
    assert set(pc.rolling_members()) <= set(pc.PIN_CLASS)


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
        assert member.reachability in {pc.MUST_RESOLVE,
                                       pc.HISTORICAL_EVIDENCE}
        assert member.population in {pc.STANDING, pc.ROLLING}
        if member.reachability == pc.HISTORICAL_EVIDENCE:
            # A row that stops owing resolution has taken itself out of the
            # check the whole class exists to run, so it says why IN THE ROW.
            # Asserted on the note rather than on a comment, because the note
            # is what the next reader is shown when the row is questioned.
            assert "HISTORICAL_EVIDENCE" in member.note, member.id
        if member.population == pc.ROLLING:
            assert "ROLLING" in member.note, member.id
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

    # HISTORICAL EVIDENCE IS NOT SILENTLY EXCUSED. Whatever this repository's
    # intent queue holds at the moment, every site in the class carries a
    # 40-hex revision and sits where the declaration says it does — the
    # exemption is from the RESOLUTION question alone, and the two checks that
    # survive it are asserted here rather than assumed (ruling D-8(a)).
    for result in report.historical:
        member = next(m for m in pc.PIN_CLASS
                      if m.id == result.site.member_id)
        assert member.reachability == pc.HISTORICAL_EVIDENCE
        assert pc.FULL_SHA_RE.match(result.site.pin)
        assert pc.path_matches(result.site.path, member.paths)
        assert pc.path_matches(result.site.path,
                               ("ideation/dashboard/intents/**",))
        assert not pc.reachable_from_main(repo, result.site.pin,
                                          report.main_ref), (
            "a historical pin main DOES reach is reported PASS, so a "
            "HISTORICAL verdict on a reachable revision means the branch that "
            "makes the free observation stopped running")

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


# =========================================================================
# doc-health — "A pin site is built only from a value that is a whole object
# name" (`fix-pin-value-boundary-and-sentinel-split`, defect 1)
#
# THE DEFECT THESE ARE PINNED TO, measured 2026-08-28 against `origin/main` at
# `5314fac5`. FOUR expressions in `pin_class` build pin sites and NONE of them
# carried a trailing hexadecimal boundary: `_field_re`, `_VOCAB_RE`, and the two
# prose members' own `pattern` strings. A sixty-four-character digest under a
# declared pin key therefore yielded a FABRICATED forty-character prefix — a
# value nobody wrote — and the verification judged that for reachability. Run
# end-to-end against a fixture whose digest's first forty characters name a REAL
# reachable commit, the pre-fix module reported `pass`: it certified a
# provenance claim the artifact never made.
#
# Every test below is a REFUSAL, and a refusal that stops refusing is invisible
# in an assertion about a value — which is why the last one reads the
# declaration structurally rather than checking one input.
# =========================================================================

def _sha256_shaped(prefix40: str) -> str:
    """A sixty-four-character hexadecimal value whose first forty characters are
    `prefix40`. The shape of a sha256 digest, which is what lands under a pin
    key when a generator stamps a blob or an image digest by mistake."""
    assert re.fullmatch(r"[0-9a-f]{40}", prefix40), prefix40
    return prefix40 + "0123456789abcdef01234567"


def digest_under_a_pin_key_repo(tmp_path, *, name="repo"):
    """A readiness record whose `source_revision` is a 64-hex DIGEST whose first
    forty characters name a real commit this repository's `main` reaches.

    THE COLLIDING CASE ON PURPOSE. A random prefix would resolve to nothing and
    the fix would look like it merely changed an ORPHAN into a defect; here the
    fabricated prefix RESOLVES, so the pre-fix behaviour is the worse of the two
    the delta names — a verification certifying a claim it never read."""
    repo = _init(tmp_path / name)
    _write(repo, "ideation/brainstorm/one.md", "# one\n\nStatus: brainstorm\n")
    real = _commit(repo, "corpus")
    digest = _sha256_shaped(real)
    _write(repo, READINESS_REL, _readiness_record(digest))
    _commit(repo, "a readiness record carrying a digest, not a commit name")
    return repo, real, digest


def test_a_digest_longer_than_an_object_name_builds_no_pin_site(tmp_path):
    """Delta scenario "A digest longer than an object name stands under a
    declared pin key". BOTH HALVES ARE ASSERTED SEPARATELY, because a test that
    only checked the absence of the pin would pass on a value silently dropped:
    no site is built, AND the whole value reaches the classification unshortened
    as a defect naming the artifact, the key and the value as written."""
    repo, real, digest = digest_under_a_pin_key_repo(tmp_path)
    report = _verify(repo)

    # half one: NOTHING commit-shaped was manufactured out of it
    assert report.results == (), (
        "a pin site was built from a value that is not a whole object name: "
        f"{[(r.site.pin, r.verdict) for r in report.results]}")
    assert report.orphans == [] and report.lost == []
    assert all(real not in s.pin for s in pc.member_sites(repo, "HEAD"))
    assert pc.swept_sites(repo, "HEAD") == []

    # half two: the value is HANDED ON WHOLE, not dropped
    assert len(report.undeclared_values) == 1, report.non_pins
    defect = report.undeclared_values[0]
    assert defect.site.value == digest            # unshortened, as written
    assert len(defect.site.value) == 64
    assert defect.site.path == READINESS_REL
    assert defect.site.key == "source_revision"
    assert defect.sentinel is None and not defect.legal
    assert "UNDECLARED" in defect.how
    # Q1, ruled 2026-08-28: it rides the EXISTING undeclared-non-commit finding
    # rather than earning a class of its own.
    assert report.uncovered == () and report.uncovered_non_pins == ()
    assert not report.clean


def test_the_fabricated_prefix_would_have_resolved_and_is_still_refused(
        tmp_path):
    """Delta scenario "The fabricated prefix would have resolved". THE WORSE OF
    THE TWO FAILURES: the first forty characters of this fixture's digest name a
    commit `main` reaches, so the pre-fix module answered PASS and certified a
    provenance claim the artifact never made. A coincidental resolution is not a
    reading of the artifact's claim."""
    repo, real, digest = digest_under_a_pin_key_repo(tmp_path)
    # the collision is REAL in this fixture rather than assumed
    assert digest.startswith(real)
    main_ref, _ = pc.resolve_main(repo)
    assert pc.reachable_from_main(repo, real, main_ref), (
        "the fixture's prefix must name a REACHABLE commit or this test is "
        "measuring the harmless failure instead of the dangerous one")

    report = _verify(repo)
    assert [r.verdict for r in report.results] == []
    assert not any(r.verdict == pc.PASS for r in report.results)
    assert not report.fully_verified
    rendered = pc.render(report)
    assert digest in rendered, (
        "the reader must be sent to the value the artifact actually holds")
    # and the prefix is never named ON ITS OWN — every occurrence of it in the
    # report is inside the whole value, which is the difference between telling
    # a reader what the file says and telling them what the parser composed.
    assert real not in rendered.replace(digest, ""), (
        "the report names a commit the artifact does not claim; a reader "
        "cannot find the subject of that finding by opening the file")


def test_a_whole_object_name_is_unaffected_in_every_serialization(tmp_path):
    """Delta scenario "A whole object name is unaffected". THE TASK THAT CATCHES
    AN OVER-TIGHT BOUNDARY, which is the fix's real failure mode: all six shapes
    measured at filing must still build the same site — bare, quoted, JSON,
    sequence item, comment-trailed, and each of the two prose forms."""
    pin = "a" * 8 + "1234567890abcdef1234567890abcdef"
    assert len(pin) == 40
    field = pc._field_re("source_revision")
    shapes = {
        "bare": f"source_revision: {pin}",
        "quoted": f'source_revision: "{pin}"',
        "json": f'  "source_revision": "{pin}",',
        "sequence item": f"  - source_revision: {pin}",
        "comment-trailed": f"source_revision: {pin}  # the pin",
    }
    for label, line in shapes.items():
        for name, rx in (("_field_re", field), ("_VOCAB_RE", pc._VOCAB_RE)):
            m = rx.search(line)
            assert m is not None, f"{name} no longer matches {label}: {line!r}"
            assert m.group(m.lastindex) == pin, f"{name} / {label}"

    prose = {m.id: m for m in pc.PIN_CLASS if m.pattern}
    assert set(prose) == {"cross-reference-rendered", "gate-action-record"}, (
        "a prose member was added or renamed; give it a line here and confirm "
        "its pattern carries the boundary")
    prose_lines = {
        "cross-reference-rendered": f"- Source revision: `{pin}`",
        "gate-action-record":
            f"  recipe: checked none · pinned none · at source_revision {pin}",
    }
    for member_id, line in prose_lines.items():
        m = prose[member_id].line_re().search(line)
        assert m is not None, f"{member_id} no longer matches {line!r}"
        assert m.group(1) == pin, member_id

    # and end-to-end: a conforming record still verifies exactly as before
    repo, old = reachable_pin_repo(tmp_path)
    report = _verify(repo)
    assert [r.site.pin for r in report.results] == [old]
    assert report.results[0].verdict == pc.PASS
    assert report.clean and report.fully_verified
    assert report.undeclared_values == []


def test_the_boundary_is_carried_by_every_site_building_expression():
    """Delta scenario "The boundary is stated once and applied everywhere a site
    is built" — Q4, ruled 2026-08-28: a STRUCTURAL assertion over the
    declaration rather than a value assertion over one input.

    WHY THIS TEST EXISTS AND WHY IT LOOKS LIKE THIS. Both fixes in this packet
    are REFUSALS, and this repository has measured that a value assertion can
    survive the mutation that removes one (the platform-inert-mutation lesson).
    So the property asserted here is over the SET of expressions that build
    sites: every one of them refuses an over-long hexadecimal run. A prose
    member added later with an unguarded `pattern` fails this test on the day it
    lands, which is what a boundary "stated once and applied everywhere" has to
    mean if it is coverage rather than a comment.

    IT PINS BEHAVIOUR, NOT THE SPELLING OF A REGEX: each expression is compiled
    and RUN against both widths, so a rewrite that keeps the property passes."""
    pin = "b" * 8 + "1234567890abcdef1234567890abcdef"
    digest = _sha256_shaped(pin)

    # every expression that builds a pin site, enumerated from the declaration
    # rather than listed by hand
    builders: dict[str, tuple] = {
        "_VOCAB_RE": (pc._VOCAB_RE, "source_revision: {v}"),
    }
    for key in sorted({m.key for m in pc.PIN_CLASS if m.key_form == "field"}):
        builders[f"_field_re({key!r})"] = (pc._field_re(key), key + ": {v}")
    for member in pc.PIN_CLASS:
        if not member.pattern:
            continue
        # the line each prose member's own pattern is written to read
        marker = ("- Source revision: `{v}`"
                  if member.id == "cross-reference-rendered"
                  else "  recipe: … at source_revision {v}")
        builders[f"PinMember({member.id}).line_re()"] = (
            member.line_re(), marker)

    assert len(builders) >= 4, builders

    unguarded = []
    for name, (rx, template) in builders.items():
        # the whole object name still builds
        conforming = rx.search(template.format(v=pin))
        assert conforming is not None, f"{name} refuses a whole object name"
        assert conforming.group(conforming.lastindex) == pin, name
        # the over-long run must not yield ANY value, let alone a prefix
        over_long = rx.search(template.format(v=digest))
        if over_long is not None:
            unguarded.append(
                f"{name} matched a 64-hex value and produced "
                f"{over_long.group(over_long.lastindex)!r}")
        # a 41-hex run is refused by the same rule, not by a length list
        assert rx.search(template.format(v=pin + "c")) is None, (
            f"{name} matched a 41-hex run; the rule is that the WHOLE value is "
            "an object name, not an enumeration of the widths somebody "
            "thought of")
    assert not unguarded, (
        "expression(s) that build a pin site carry no whole-object-name "
        "boundary — append `pin_class.HEX_BOUNDARY` to the value group:\n  "
        + "\n  ".join(unguarded))


def test_the_boundary_rule_has_one_home_in_the_module():
    """The guard is a NAMED CONSTANT rather than four retyped copies, so the
    module states the rule once and the structural test above has something to
    point a future author at. `LOOSE_SHA_RE`, whose comment stated the rule
    before any site builder carried it, is built from the same constant."""
    assert pc.HEX_BOUNDARY == r"(?![0-9a-fA-F])"
    assert pc.LOOSE_SHA_RE.pattern.endswith(pc.HEX_BOUNDARY)

    # No EXECUTABLE spelling of the guard other than the constant's own
    # declaration. Read with `ast` rather than by counting substrings, because
    # the two prose occurrences of it in this module are a comment and a
    # docstring — writing the rule down is exactly what those are for, and a
    # substring count cannot tell an explanation from a retyped copy.
    source = (Path(REPO_ROOT) / "scripts/doc_health/pin_class.py").read_text(
        encoding="utf-8")
    tree = ast.parse(source)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                docstrings.add(id(body[0].value))
    retyped = [
        node.lineno for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
        and pc.HEX_BOUNDARY in node.value and id(node) not in docstrings
        and node.lineno != _hex_boundary_lineno(tree)]
    assert not retyped, (
        "the boundary is retyped as a string literal at line(s) "
        f"{retyped}; it has ONE home, `HEX_BOUNDARY`, and every site builder "
        "names it rather than copying it")


def _hex_boundary_lineno(tree) -> int:
    """The line the constant is declared on — the one legal literal."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "HEX_BOUNDARY"
                for t in node.targets):
            return node.value.lineno
    raise AssertionError("pin_class declares no HEX_BOUNDARY constant")


def test_the_real_corpus_carries_nothing_the_boundary_reclassifies():
    """§ 2.5's claim, re-measured rather than carried: the fix moves no number
    in this repository's own report because no committed artifact carries an
    over-long hexadecimal value under a vocabulary key. A number that moves
    would be a finding, and this is where the next reader learns it did not."""
    repo, report = _real_report()
    long_hex = re.compile(
        r'(?<![A-Za-z0-9_])"?(' + "|".join(
            re.escape(k) for k in sorted(pc.PIN_KEY_VOCABULARY,
                                         key=len, reverse=True))
        + r')"?\s*:\s*"?([0-9a-fA-F]{41,})')
    offenders = []
    for path in pc.committed_paths(repo, report.rev):
        if not path.endswith(pc.SCAN_SUFFIXES):
            continue
        if not pc.path_matches(path, pc.SCAN_ROOTS):
            continue
        if pc.non_member_reason(path) is not None:
            continue
        text = pc.committed_text(repo, report.rev, path)
        if text is None:
            continue
        for n, line in enumerate(text.splitlines(), start=1):
            m = long_hex.search(line)
            if m:
                offenders.append(f"{path}:{n} ({m.group(1)}) -> {m.group(2)}")
    assert not offenders, (
        "committed artifact(s) now carry an over-long hexadecimal value under "
        "a pin key. Before this change each produced a FABRICATED forty-"
        "character pin; now each is an undeclared non-commit value, which is "
        "the honest reading and a real finding to resolve:\n  "
        + "\n  ".join(offenders))
