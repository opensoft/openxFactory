"""Refresh-lane tests (openxFactory add-nightly-dashboard-refresh §5).

The lane's contract, and what each block here pins:

  * §5.2 THE NO-CHANGE DECISION IS ON INPUT REVISIONS, BEFORE THE BUILD, and
    the tests assert the ORDERING structurally — that the build callable was
    never invoked — because an outcome-only assertion ("no PR was opened")
    passes even when the build ran.
  * §5.2 (d) the self-churn regression: the served plane's repository advancing
    for an unrelated reason — including this lane's OWN previously merged pin —
    must NOT rebuild. A tip-versus-tip realization would make every landed pin
    force the next night's build, so these tests also assert that every
    recipe-side revision query the lane issues is PATH-SCOPED.
  * §5.2a the provenance round-trip over the REAL overlay file: the block the
    lane writes parses back to the same two revisions and the surrounding human
    prose survives. That comment is load-bearing state now.
  * §5.3 the produced diff is envelope-shaped: the `digest:` line and its
    adjacent comment inside the one `images:` entry, and nothing else.
  * §5.4 the snapshot `source_revision` and the baked corpus revision are
    asserted EQUAL by the lane, so the two-revision trap is detectable.
  * §5.1 the refresh-status artifact: every outcome class, bounded detail, and
    the invariant that a status-write failure does not fail the lane.

Nothing here builds an image, contacts a registry, or touches a cluster: every
shell-out is behind an injected runner, and the decision core is a pure
function the tests call directly.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

from conftest import FIXTURES

from ideation_dashboard import dashboard_refresh_lane as lane

OVERLAY_FIXTURE = FIXTURES / "dox-aks-qa-kustomization.yaml"
IMAGE = lane.DEFAULT_IMAGE

CORPUS_A = "a" * 40
CORPUS_B = "b" * 40
RECIPE_A = "c" * 40
RECIPE_B = "d" * 40
HEAD_A = "e" * 40
DIGEST_OLD = "sha256:" + "1" * 64
DIGEST_NEW = "sha256:" + "2" * 64


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _prov(corpus: str = CORPUS_A, recipe: str = RECIPE_A, **kw) -> lane.Provenance:
    return lane.Provenance(
        corpus_repo=lane.DEFAULT_CORPUS_REPO, corpus_revision=corpus,
        corpus_scope=lane.CORPUS_BAKED_PATHS,
        recipe_repo=lane.DEFAULT_RECIPE_REPO, recipe_revision=recipe,
        recipe_scope=lane.RECIPE_BAKED_PATHS, **kw)


def _overlay_with_provenance(prov: lane.Provenance | None = None,
                             digest: str = DIGEST_OLD) -> str:
    """The real overlay, pinned to `digest` and carrying `prov` (or left as the
    hand-written bootstrap prose when `prov` is None)."""
    text = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    if prov is None:
        return text
    return lane.rewrite_pin(text, IMAGE, digest, prov)


class RecordingBuild:
    """Stands in for the worker's build+push. Records every invocation so a
    no-change night can be proven to have made NONE."""

    def __init__(self, result: lane.BuildResult | None = None) -> None:
        self.calls: list[object] = []
        self.result = result or lane.BuildResult(
            True, None, digest=DIGEST_NEW, tag="refresh-test",
            source_revision=HEAD_A, corpus_revision=CORPUS_B)

    def __call__(self, plan=None):
        self.calls.append(plan)
        return self.result


def _inputs(*, corpus=CORPUS_A, recipe=RECIPE_A, prov=None, digest=DIGEST_OLD,
            overlay: str | None = None, errors=()) -> lane.CurrentInputs:
    text = overlay if overlay is not None else _overlay_with_provenance(prov, digest)
    return lane.CurrentInputs(
        corpus_revision=corpus, recipe_revision=recipe, overlay_text=text,
        pinned_digest=lane.read_pinned_digest(text, IMAGE),
        recorded=lane.read_pinned_provenance(text, IMAGE), errors=list(errors))


def _status(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# §5.2 the decision — pure, and before anything is built
# ---------------------------------------------------------------------------

def test_matching_inputs_decide_no_change():
    decision = lane.decide_refresh(corpus_revision=CORPUS_A,
                                   recipe_revision=RECIPE_A,
                                   recorded=_prov())
    assert decision.build is False
    assert decision.no_change
    assert decision.reason == lane.REASON_UNCHANGED
    # Auditable: the decision names both matching revisions beside the recorded
    # ones it compared against.
    comparands = decision.comparands()
    assert comparands["corpus"]["current_revision"] == CORPUS_A
    assert comparands["corpus"]["recorded_revision"] == CORPUS_A
    assert comparands["corpus"]["matched"] is True
    assert comparands["recipe"]["matched"] is True


def test_a_no_change_night_never_reaches_the_build(tmp_path):
    """THE structural assertion: not "no PR was opened" but "the build callable
    was never invoked", so no checkout, no snapshot generation, no docker build
    and no push can have happened."""
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(prov=_prov()), build=build,
        build_plan=object())
    assert build.calls == []                      # nothing was built
    assert outcome.result == lane.RESULT_NO_CHANGE
    assert outcome.built_digest is None
    assert outcome.pin_path is None and outcome.pr_body_path is None
    # and the recorded outcome NAMES the revisions that matched
    payload = _status(outcome.status_path)
    assert payload["result"] == "no_change"
    assert payload["inputs"]["corpus"]["current_revision"] == CORPUS_A
    assert payload["inputs"]["corpus"]["recorded_revision"] == CORPUS_A
    assert payload["inputs"]["recipe"]["current_revision"] == RECIPE_A
    assert payload["inputs"]["recipe"]["recorded_revision"] == RECIPE_A
    assert CORPUS_A[:12] in payload["reason"]


def test_corpus_movement_builds(tmp_path):
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(corpus=CORPUS_B, prov=_prov()), build=build,
        build_plan=object())
    assert len(build.calls) == 1
    assert outcome.decision.reason == lane.REASON_CORPUS_MOVED
    assert outcome.result == lane.RESULT_OK
    assert outcome.built_digest == DIGEST_NEW


def test_recipe_movement_builds_even_with_a_static_corpus(tmp_path):
    """Why the predicate carries TWO revisions: a Dockerfile change alters the
    image with the corpus untouched and would otherwise be invisible."""
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(recipe=RECIPE_B, prov=_prov()), build=build,
        build_plan=object())
    assert len(build.calls) == 1
    assert outcome.decision.reason == lane.REASON_RECIPE_MOVED
    assert outcome.result == lane.RESULT_OK


def test_absent_provenance_is_a_bootstrap_build(tmp_path):
    """The hand-pinned bootstrap image: prose, no machine block. Treated as
    CHANGED — the lane builds once and its pin establishes the record."""
    build = RecordingBuild()
    inputs = _inputs(prov=None)                    # the real, hand-written pin
    assert inputs.recorded is None
    outcome = lane.run_refresh_lane(tmp_path, inputs=inputs, build=build,
                                    build_plan=object(),
                                    pin_out=tmp_path / "pin")
    assert len(build.calls) == 1
    assert outcome.decision.bootstrap is True
    assert outcome.decision.reason == lane.REASON_BOOTSTRAP
    # ...and the pin it produces carries a PARSEABLE record for later runs.
    reparsed = lane.read_pinned_provenance(
        outcome.pin_path.read_text(encoding="utf-8"), IMAGE)
    assert reparsed is not None
    assert reparsed.corpus_revision == CORPUS_B    # the build's own re-read
    assert reparsed.recipe_revision == RECIPE_A


@pytest.mark.parametrize("mangle", [
    lambda lines: [l for l in lines if "corpus-revision" not in l],   # missing key
    lambda lines: [l.replace("v1", "v99") for l in lines],            # unknown version
    lambda lines: lines + [lines[2]],                                 # duplicate key
    lambda lines: [l.replace("a" * 40, "not-a-sha") for l in lines],  # bad revision
    lambda lines: [l for l in lines if "corpus-scope" not in l],      # no scope
])
def test_unparseable_provenance_parses_to_none(mangle):
    lines = lane.render_provenance(_prov())
    assert lane.parse_provenance(lines) is not None
    assert lane.parse_provenance(mangle(list(lines))) is None


def test_unparseable_provenance_builds_rather_than_skipping(tmp_path):
    overlay = _overlay_with_provenance(_prov()).replace(
        "xf-refresh-provenance: v1", "xf-refresh-provenance: v99")
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(tmp_path, inputs=_inputs(overlay=overlay),
                                    build=build, build_plan=object())
    assert len(build.calls) == 1
    assert outcome.decision.reason == lane.REASON_BOOTSTRAP


def test_a_scope_change_forces_a_build():
    """Two runs that scoped their inputs differently asked different questions,
    so equality of their answers would be meaningless."""
    recorded = _prov()
    decision = lane.decide_refresh(
        corpus_revision=CORPUS_A, recipe_revision=RECIPE_A, recorded=recorded,
        corpus_scope=("contracts", "docs"))
    assert decision.build is True
    assert decision.reason == lane.REASON_SCOPE_CHANGED


def test_an_unreadable_input_skips_and_is_not_reported_as_no_change(tmp_path):
    """"I could not look" is not "nothing moved": recording it as no_change
    would silently freeze the served plane."""
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(recipe=None, prov=_prov(),
                                 errors=["could not read the recipe revision"]),
        build=build, build_plan=object())
    assert build.calls == []
    assert outcome.result == lane.RESULT_SKIPPED
    assert outcome.decision.undecidable
    assert lane.REASON_UNRESOLVED in outcome.reason
    payload = _status(outcome.status_path)
    assert payload["result"] == "skipped"
    assert payload["inputs"]["recipe"]["current_revision"] is None


def test_the_readiness_skip_reads_no_input_at_all(tmp_path):
    """Fail-closed, and deliberately with NO hosted fallback: the build and the
    push belong to the host that holds the registry binding."""
    build = RecordingBuild()

    def _explode():
        raise AssertionError("an unready worker must read no input")

    outcome = lane.run_refresh_lane(tmp_path, read_inputs=_explode, build=build,
                                    skip_reason="worker_offline")
    assert build.calls == []
    assert outcome.result == lane.RESULT_SKIPPED
    assert outcome.reason == "worker_offline"


def test_output_digest_equality_cannot_be_the_predicate():
    """Structural: the decision takes no digest, by ANY name, so a future edit
    cannot quietly reintroduce the banned predicate through an argument. And
    equality of the two digests on a run that built anyway is a NOTE."""
    params = set(inspect.signature(lane.decide_refresh).parameters)
    assert not any("digest" in name for name in params), params
    assert lane.digest_note(DIGEST_NEW, DIGEST_OLD) is None
    assert "curiosity" in lane.digest_note(DIGEST_NEW, DIGEST_NEW)


# ---------------------------------------------------------------------------
# §5.2 (d) the self-churn regression — the guard against tip-versus-tip
# ---------------------------------------------------------------------------

class FakeWorld:
    """A fake git/gh runner. The served plane's TIP has advanced (a previously
    merged pin by this very lane) while its BAKED INPUTS have not moved."""

    def __init__(self, *, corpus_revision: str, recipe_baked: str,
                 recipe_tip: str, overlay: str) -> None:
        self.corpus_revision = corpus_revision
        self.recipe_baked = recipe_baked
        self.recipe_tip = recipe_tip
        self.overlay = overlay
        self.argvs: list[tuple[str, ...]] = []

    def __call__(self, argv, *, cwd=None, env=None):
        argv = tuple(str(a) for a in argv)
        self.argvs.append(argv)
        joined = " ".join(argv)
        if argv[0] == "git" and "fetch" in argv:
            return lane.CommandResult(argv, 0, "", "")
        if argv[0] == "git" and "log" in argv:
            return lane.CommandResult(argv, 0, self.corpus_revision + "\n", "")
        if argv[0] == "gh" and "contents/" in joined:
            return lane.CommandResult(argv, 0, self.overlay, "")
        if argv[0] == "gh" and "/commits" in joined:
            # A tip query is a `commits` request with NO path filter. The lane
            # must never issue one; if it does, hand it the ADVANCED tip so the
            # regression is loud rather than silent.
            scoped = any(a.startswith("path=") for a in argv)
            sha = self.recipe_baked if scoped else self.recipe_tip
            return lane.CommandResult(argv, 0, json.dumps([
                {"sha": sha, "commit": {"committer": {"date": "2026-08-21T00:00:00Z"}}}
            ]), "")
        raise AssertionError(f"unexpected command: {joined}")

    def revision_queries(self) -> list[tuple[str, ...]]:
        return [a for a in self.argvs if a[0] == "gh" and "/commits" in " ".join(a)]


def test_an_unrelated_commit_on_the_served_plane_does_not_rebuild(tmp_path):
    """The regression the old tip-versus-tip predicate would have failed: this
    lane's own merged pin advances Omnigent-Install `main`, so a tip comparison
    would force a rebuild every night forever."""
    overlay = _overlay_with_provenance(_prov(CORPUS_A, RECIPE_A))
    world = FakeWorld(corpus_revision=CORPUS_A, recipe_baked=RECIPE_A,
                      recipe_tip="f" * 40, overlay=overlay)
    build = RecordingBuild()

    def _read():
        return lane.read_current_inputs(
            corpus_checkout=tmp_path / "openxFactory", runner=world)

    outcome = lane.run_refresh_lane(tmp_path, read_inputs=_read, build=build,
                                    build_plan=object())
    assert build.calls == []                      # NOT rebuilt
    assert outcome.result == lane.RESULT_NO_CHANGE
    assert outcome.decision.recipe_revision == RECIPE_A
    assert outcome.decision.recipe_revision != world.recipe_tip
    # ...and structurally: every revision query the lane made was PATH-SCOPED,
    # so no realization here can be reading a branch tip.
    queries = world.revision_queries()
    assert queries, "the lane asked the served plane no revision question"
    for argv in queries:
        assert any(a.startswith("path=") for a in argv), argv


def test_the_corpus_revision_is_path_scoped_not_the_branch_tip(tmp_path):
    world = FakeWorld(corpus_revision=CORPUS_A, recipe_baked=RECIPE_A,
                      recipe_tip="f" * 40, overlay=_overlay_with_provenance(_prov()))
    revision = lane.git_baked_input_revision(tmp_path, lane.CORPUS_BAKED_PATHS,
                                             ref="origin/main", runner=world)
    assert revision == CORPUS_A
    argv = world.argvs[-1]
    assert argv[:6] == ("git", "-C", str(tmp_path), "log", "-1", "--format=%H")
    assert "--" in argv
    assert set(lane.CORPUS_BAKED_PATHS) <= set(argv)


def test_the_baked_input_scope_is_exactly_what_the_dockerfile_copies():
    """The eight paths, and deliberately not `tests/` or `experiments/`
    (169 MB, referenced by zero docs)."""
    assert lane.CORPUS_BAKED_PATHS == (
        "contracts", "docs", "examples", "ideation", "openspec",
        "scripts/doc_health", "scripts/ideation_dashboard", "templates")
    assert lane.RECIPE_BAKED_PATHS == ("containers/ideation-dashboard",)
    assert "experiments" not in lane.CORPUS_BAKED_PATHS
    assert "tests" not in lane.CORPUS_BAKED_PATHS


# ---------------------------------------------------------------------------
# §5.2a provenance round-trip, over the REAL overlay file
# ---------------------------------------------------------------------------

def test_provenance_round_trips():
    prov = _prov(source_revision=HEAD_A, tag="refresh-20260822-010203",
                 generated_at="2026-08-22T01:02:03Z", run_id="12345")
    parsed = lane.parse_provenance(lane.render_provenance(prov))
    assert parsed == prov


def test_provenance_round_trips_through_the_real_overlay():
    original = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    assert lane.read_pinned_provenance(original, IMAGE) is None, (
        "the bootstrap pin's comment is human PROSE carrying no machine block — "
        "so the first lane run is a bootstrap build by construction")
    prov = _prov(source_revision=HEAD_A, tag="refresh-20260822-010203")
    rewritten = lane.rewrite_pin(original, IMAGE, DIGEST_NEW, prov)
    parsed = lane.read_pinned_provenance(rewritten, IMAGE)
    assert parsed is not None
    assert parsed.corpus_revision == CORPUS_A
    assert parsed.recipe_revision == RECIPE_A
    assert parsed.corpus_scope == lane.CORPUS_BAKED_PATHS
    assert lane.read_pinned_digest(rewritten, IMAGE) == DIGEST_NEW
    # The surrounding human prose survives — the comment serves a reader and a
    # parser at once.
    assert "account-menu-r2 build" in rewritten
    assert "generated --strict from that same checkout" in rewritten


def test_a_second_rewrite_replaces_the_block_rather_than_stacking_it():
    original = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    once = lane.rewrite_pin(original, IMAGE, DIGEST_NEW, _prov())
    twice = lane.rewrite_pin(once, IMAGE, DIGEST_OLD,
                             _prov(CORPUS_B, RECIPE_B))
    assert twice.count("xf-refresh-provenance") == 1
    parsed = lane.read_pinned_provenance(twice, IMAGE)
    assert (parsed.corpus_revision, parsed.recipe_revision) == (CORPUS_B, RECIPE_B)
    assert lane.read_pinned_digest(twice, IMAGE) == DIGEST_OLD


# ---------------------------------------------------------------------------
# §5.3 the produced diff is envelope-shaped
# ---------------------------------------------------------------------------

def test_the_produced_diff_is_the_digest_line_and_its_adjacent_comment():
    original = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    prov = _prov(source_revision=HEAD_A, tag="refresh-20260822-010203")
    rewritten = lane.rewrite_pin(original, IMAGE, DIGEST_NEW, prov)

    before = original.splitlines()
    after = rewritten.splitlines()
    entry = lane.find_pin_entry(original, IMAGE)

    # Everything OUTSIDE the one entry is byte-identical.
    assert before[:entry.start] == after[:entry.start]
    tail_before = before[entry.end:]
    assert after[len(after) - len(tail_before):] == tail_before

    added = [l for l in after if l not in before]
    removed = [l for l in before if l not in after]
    # Every changed line is either the digest value or a comment.
    for line in added + removed:
        stripped = line.strip()
        assert stripped.startswith("digest:") or stripped.startswith("#"), line
    assert any(l.strip() == f"digest: {DIGEST_NEW}" for l in added)
    assert any(l.strip() == f"digest: {entry.digest}" for l in removed)

    # No image entry added or removed, no name:/newTag: change, and the other
    # blocks of the one file are untouched.
    def _keys(lines, key):
        return [l.strip() for l in lines if l.strip().startswith(key)]

    assert _keys(before, "- name:") == _keys(after, "- name:")
    assert _keys(before, "name:") == _keys(after, "name:")
    assert _keys(before, "newTag:") == _keys(after, "newTag:")
    assert _keys(before, "- path:") == _keys(after, "- path:")
    assert _keys(before, "namespace:") == _keys(after, "namespace:")
    assert before.count("resources:") == after.count("resources:")
    assert len(_keys(after, "digest:")) == len(_keys(before, "digest:"))


def test_the_other_image_entries_keep_their_digests():
    original = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    others = [name for name in (
        "acropensoftxfactoryqa.azurecr.io/dox-auth",
        "acropensoftxfactoryqa.azurecr.io/intent-inbox",
        "acropensoftxfactoryqa.azurecr.io/dispatch-token-minter")]
    rewritten = lane.rewrite_pin(original, IMAGE, DIGEST_NEW, _prov())
    for name in others:
        assert (lane.read_pinned_digest(rewritten, name)
                == lane.read_pinned_digest(original, name))


def test_rewriting_an_absent_entry_raises_rather_than_widening():
    original = OVERLAY_FIXTURE.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        lane.rewrite_pin(original, "acropensoftxfactoryqa.azurecr.io/nope",
                         DIGEST_NEW, _prov())


def test_the_pr_body_is_a_courtesy_and_says_so():
    body = lane.render_pr_body(prov=_prov(), digest=DIGEST_NEW,
                               previous_digest=DIGEST_OLD, tag="refresh-x",
                               source_revision=HEAD_A,
                               run_url="https://example.invalid/run/1")
    assert CORPUS_A in body and RECIPE_A in body
    assert DIGEST_NEW in body and DIGEST_OLD in body
    assert HEAD_A in body
    assert "COURTESY restatement" in body
    assert "not this description" in body


# ---------------------------------------------------------------------------
# §5.4 one revision, not two
# ---------------------------------------------------------------------------

def test_verify_one_revision_rejects_a_two_revision_image():
    lane.verify_one_revision(HEAD_A, HEAD_A)              # equal: fine
    with pytest.raises(lane.OneRevisionViolation):
        lane.verify_one_revision(HEAD_A, CORPUS_A)
    with pytest.raises(lane.OneRevisionViolation):
        lane.verify_one_revision(None, HEAD_A)


class FakeBuildWorld:
    """git/docker/az, faked. Records every argv so the tests can assert what
    the build did and — more importantly — what it did NOT do."""

    def __init__(self, *, head: str, snapshot_revision: str | None,
                 strict_ok: bool = True, snapshot_path: Path | None = None) -> None:
        self.head = head
        self.snapshot_revision = snapshot_revision
        self.strict_ok = strict_ok
        self.snapshot_path = snapshot_path
        self.argvs: list[tuple[str, ...]] = []

    def __call__(self, argv, *, cwd=None, env=None):
        argv = tuple(str(a) for a in argv)
        self.argvs.append(argv)
        joined = " ".join(argv)
        if argv[0] == "git" and "rev-parse" in argv:
            return lane.CommandResult(argv, 0, self.head + "\n", "")
        if argv[0] == "git" and "log" in argv:
            return lane.CommandResult(argv, 0, CORPUS_B + "\n", "")
        if argv[0] == "git":
            return lane.CommandResult(argv, 0, "", "")
        if "ideation_dashboard.cli" in joined:
            if not self.strict_ok:
                return lane.CommandResult(argv, 1, "",
                                          "validation FAILED — 1 warning(s)")
            out = Path(argv[argv.index("--output") + 1])
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({
                "generation": {"source_revision": self.snapshot_revision}}),
                encoding="utf-8")
            return lane.CommandResult(argv, 0, "validation: 0 error(s)", "")
        if argv[0] == "docker" and argv[1] == "push":
            return lane.CommandResult(argv, 0, f"latest: digest: {DIGEST_NEW} size: 1",
                                      "")
        if argv[0] in ("docker", "az"):
            return lane.CommandResult(argv, 0, "", "")
        raise AssertionError(f"unexpected command: {joined}")

    def ran(self, *needles) -> bool:
        return any(all(n in " ".join(a) for n in needles) for a in self.argvs)


def _plan(tmp_path: Path) -> lane.BuildPlan:
    return lane.BuildPlan(context_root=tmp_path / "ctx",
                          dockerfile=tmp_path / "Dockerfile",
                          corpus_url="https://example.invalid/openxFactory.git")


def test_the_build_asserts_one_revision_before_it_builds(tmp_path):
    """A mismatch between the snapshot's source_revision and the checkout HEAD
    the corpus was baked from stops the build — the image is never produced."""
    world = FakeBuildWorld(head=HEAD_A, snapshot_revision=CORPUS_A)
    result = lane.build_and_push(_plan(tmp_path), runner=world)
    assert result.ok is False
    assert "one-revision assertion failed" in result.reason
    assert not world.ran("docker", "build")
    assert not world.ran("docker", "push")


def test_the_build_publishes_when_the_two_revisions_are_one(tmp_path):
    world = FakeBuildWorld(head=HEAD_A, snapshot_revision=HEAD_A)
    result = lane.build_and_push(_plan(tmp_path), runner=world)
    assert result.ok is True
    assert result.digest == DIGEST_NEW
    assert result.source_revision == HEAD_A
    assert result.corpus_revision == CORPUS_B
    # the recipe: a FRESH sparse checkout, --strict generation from THAT
    # checkout, then the build — in that order.
    assert world.ran("git", "clone", "--filter=blob:none")
    assert world.ran("sparse-checkout", "set", "scripts/ideation_dashboard")
    assert world.ran("ideation_dashboard.cli", "generate", "--strict")
    assert world.ran("docker", "build")
    assert world.ran("docker", "push")
    order = [i for i, argv in enumerate(world.argvs)
             if "--strict" in argv or (argv[0] == "docker" and argv[1] == "build")]
    generate_at = next(i for i, argv in enumerate(world.argvs) if "--strict" in argv)
    build_at = next(i for i, argv in enumerate(world.argvs)
                    if argv[0] == "docker" and argv[1] == "build")
    assert generate_at < build_at, order


def test_strict_failure_publishes_nothing(tmp_path):
    world = FakeBuildWorld(head=HEAD_A, snapshot_revision=HEAD_A, strict_ok=False)
    result = lane.build_and_push(_plan(tmp_path), runner=world)
    assert result.ok is False
    assert result.strict_failed is True
    assert not world.ran("docker", "build")
    assert not world.ran("docker", "push")
    assert not world.ran("az", "acr")


# ---------------------------------------------------------------------------
# §5.1 the refresh-status artifact
# ---------------------------------------------------------------------------

def test_status_artifact_for_the_ok_outcome(tmp_path):
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(corpus=CORPUS_B, prov=_prov()), build=build,
        build_plan=object(), pin_out=tmp_path / "pin")
    payload = _status(outcome.status_path)
    assert payload["kind"] == "ideation-dashboard-refresh-status"
    assert payload["lane"] == lane.LANE
    assert payload["result"] == "ok"
    assert payload["built_digest"] == DIGEST_NEW
    assert payload["pinned_digest"] == DIGEST_OLD
    assert payload["tag"] == "refresh-test"
    assert payload["source_revision"] == HEAD_A
    assert payload["decision"] == "build"
    assert payload["inputs"]["corpus"]["repository"] == lane.DEFAULT_CORPUS_REPO
    assert payload["inputs"]["recipe"]["repository"] == lane.DEFAULT_RECIPE_REPO
    assert payload["generated_at"].endswith("Z")
    assert outcome.status_path.name == "refresh-status.json"
    assert outcome.status_path.parent.name == "ideation-dashboard"


def test_status_artifact_for_the_strict_failed_outcome(tmp_path):
    def _build(plan=None):
        return lane.BuildResult(False, "snapshot generation failed under --strict",
                                strict_failed=True,
                                detail=[f"line {n}" for n in range(200)])

    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(corpus=CORPUS_B, prov=_prov()), build=_build,
        build_plan=object(), pin_out=tmp_path / "pin")
    payload = _status(outcome.status_path)
    assert payload["result"] == "strict_failed"
    assert "--strict" in payload["reason"]
    assert payload["built_digest"] is None
    assert payload["pull_request"] is None
    assert len(payload["detail"]) == lane.DETAIL_CAP      # bounded detail
    # nothing published, and no pin proposal rendered
    assert outcome.pin_path is None
    assert not (tmp_path / "pin").exists()


def test_every_outcome_class_is_reachable_and_annotated(tmp_path):
    seen = {}
    for name, kwargs in {
        lane.RESULT_NO_CHANGE: dict(inputs=_inputs(prov=_prov()),
                                    build=RecordingBuild(), build_plan=object()),
        lane.RESULT_OK: dict(inputs=_inputs(corpus=CORPUS_B, prov=_prov()),
                             build=RecordingBuild(), build_plan=object()),
        lane.RESULT_SKIPPED: dict(skip_reason="worker_offline"),
        lane.RESULT_STRICT_FAILED: dict(
            inputs=_inputs(corpus=CORPUS_B, prov=_prov()),
            build=lambda plan=None: lane.BuildResult(False, "rejected",
                                                     strict_failed=True),
            build_plan=object()),
    }.items():
        outcome = lane.run_refresh_lane(tmp_path / name, **kwargs)
        seen[name] = outcome.result
        annotation = outcome.annotation()
        assert annotation.startswith("::notice::") or \
            annotation.startswith("::warning::")
        assert lane.LANE in annotation
    assert seen == {
        lane.RESULT_NO_CHANGE: lane.RESULT_NO_CHANGE,
        lane.RESULT_OK: lane.RESULT_OK,
        lane.RESULT_SKIPPED: lane.RESULT_SKIPPED,
        lane.RESULT_STRICT_FAILED: lane.RESULT_STRICT_FAILED,
    }
    # A skip is never silent: it annotates as a warning, not a notice.
    skip = lane.run_refresh_lane(tmp_path / "skip2", skip_reason="stale_heartbeat")
    assert skip.annotation().startswith("::warning::")


def test_the_pull_request_reference_is_recorded_on_the_delivered_status(tmp_path):
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(corpus=CORPUS_B, prov=_prov()), build=build,
        build_plan=object())
    out_dir = outcome.status_path.parent
    assert _status(outcome.status_path)["pull_request"] is None
    assert lane.record_pull_request(out_dir, "opensoft/Omnigent-Install#9") is True
    assert _status(outcome.status_path)["pull_request"] == \
        "opensoft/Omnigent-Install#9"
    # No reference, or no artifact, is a False — never an exception.
    assert lane.record_pull_request(out_dir, None) is False
    assert lane.record_pull_request(tmp_path / "absent", "x#1") is False


def test_the_record_pr_cli_phase_patches_the_delivered_status(tmp_path):
    """The `--phase record-pr` seam the workflow calls after its cross-repo
    branch delivery knows the pin PR reference. It is the only CLI-reachable way
    to satisfy task 4.7's "pull-request reference when one exists" field, because
    the PR is opened by the workflow AFTER the pin phase wrote the status."""
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(
        tmp_path, inputs=_inputs(corpus=CORPUS_B, prov=_prov()), build=build,
        build_plan=object())
    out_dir = outcome.status_path.parent
    assert _status(outcome.status_path)["pull_request"] is None
    # The CLI is void and always exits 0 (never raises), like the snapshot lane.
    rel = str(out_dir.relative_to(tmp_path))
    lane.main(["--repo-root", str(tmp_path), "--out-dir", rel,
               "--phase", "record-pr",
               "--pull-request", "opensoft/Omnigent-Install#42"])
    assert _status(outcome.status_path)["pull_request"] == \
        "opensoft/Omnigent-Install#42"
    # A missing reference is a no-op, never a failure.
    lane.main(["--repo-root", str(tmp_path), "--out-dir", rel,
               "--phase", "record-pr"])
    assert _status(outcome.status_path)["pull_request"] == \
        "opensoft/Omnigent-Install#42"


def test_a_status_write_failure_does_not_fail_the_lane(tmp_path):
    """The status artifact is diagnostic. Its own failure must never take the
    run down."""
    blocked = tmp_path / "health"
    blocked.write_text("not a directory", encoding="utf-8")
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(tmp_path, inputs=_inputs(prov=_prov()),
                                    build=build, build_plan=object())
    assert outcome.result == lane.RESULT_NO_CHANGE
    assert outcome.status_path is None
    assert build.calls == []


# ---------------------------------------------------------------------------
# §4.9/§4.10 the report section, and the one-run lag stated rather than hidden
# ---------------------------------------------------------------------------

def test_the_report_section_says_whose_outcome_it_names(tmp_path):
    build = RecordingBuild()
    outcome = lane.run_refresh_lane(tmp_path, inputs=_inputs(prov=_prov()),
                                    build=build, build_plan=object())
    status = _status(outcome.status_path)
    status["run_id"] = "111"
    section = lane.render_report_section(status, this_run_id="222")
    assert section.startswith(lane.REPORT_HEADING)
    assert "PREVIOUS run (111)" in section
    assert "no_change" in section
    assert "matched" in section
    # and when the recorded run IS this run, it says so instead
    same = lane.render_report_section(status, this_run_id="111")
    assert "this run (111)" in same


def test_the_report_section_reports_a_stuck_chain():
    section = lane.render_report_section(
        {"result": "ok", "run_id": "1", "built_digest": DIGEST_NEW,
         "tag": "t", "pinned_digest": DIGEST_OLD},
        this_run_id="2", stuck_pull_request="opensoft/Omnigent-Install#7")
    assert "STUCK CHAIN" in section
    assert "opensoft/Omnigent-Install#7" in section
    assert lane.DEFAULT_PIN_BRANCH in section


def test_the_report_section_is_honest_when_nothing_has_been_delivered():
    section = lane.render_report_section(None)
    assert "No refresh-status artifact has been delivered yet" in section


def test_appending_the_report_section_never_raises(tmp_path):
    report = tmp_path / "report.md"
    report.write_text("# Doc-health 2026-08-22\n", encoding="utf-8")
    assert lane.append_report_section(report, lane.render_report_section(None))
    assert lane.REPORT_HEADING in report.read_text(encoding="utf-8")
    # a report path that cannot be written is a False, never an exception
    assert lane.append_report_section(tmp_path / "nope" / "x.md", "x") is False


def test_an_unhandled_error_is_a_recorded_skip_not_a_failure(tmp_path):
    def _boom():
        raise RuntimeError("the world moved")

    outcome = lane.run_refresh_lane(tmp_path, read_inputs=_boom,
                                    build=RecordingBuild(), build_plan=object())
    assert outcome.result == lane.RESULT_SKIPPED
    assert "RuntimeError" in outcome.reason
    assert _status(outcome.status_path)["result"] == "skipped"
