"""FLOOR PART 4 — the snapshot-equivalence run, and the runner that makes it
(`split-opendox-two-layer-product` § 5.5, design § D6 (4), RULED OQ-1).

THREE CLAIMS ARE UNDER TEST HERE AND THEY ARE DIFFERENT CLAIMS.

  1. **The floor holds**: the pre-split tree and the post-split stack render
     the SAME canonical snapshot over the same corpus. That is § D6 (4)'s own
     sentence, and it is asserted through the documented command line rather
     than through an imported function.
  2. **The run DISCRIMINATES**, which is the claim the first one rests on. A
     green run over one corpus proves the two sides agree about that corpus;
     it does not prove they would disagree about anything. So four corpus
     states are run in one invocation and TWO OF THEM MOVE THE DIGEST — an
     equal result is then a measurement rather than a constant. Both
     directions are needed: a state the projection correctly ignores must NOT
     move it either, or "equal" would only mean "nothing is read".
  3. **The runner REFUSES when the sides differ**, which nothing about a
     passing floor can demonstrate. Two mutation controls inject a difference
     — one on each side — and each is asserted to produce
     `equivalence-digests-differ` with both digests, both byte counts and a
     diff that NAMES the field. Delete the comparison and both go green, which
     is what makes this file evidence rather than decoration.

THE SCRIPT IS RUN AS A SUBPROCESS for behaviour and loaded by path only for
constants and for the two mutation controls —
`tests/carve_conformance/test_verify_carve_conformance.py`'s rule, adopted for
its reason: the documented way in is a command line, and a test of the imported
function proves the code executes rather than that the invocation an operator
will type succeeds and prints what its readers depend on.

NOTHING HERE SKIPS, EVER, and the last test in this file asserts it of this
file. `.github/workflows/pytest-suite.yml` pins `EXPECT_SKIPPED` as an EXACT
sum precisely because a directory that quietly turns into skips reports as a
green bar. This suite has no reason to want one: the gate's checkout is
`fetch-depth: 0` so `opendox-carve-0` is reachable, and it initialises both
legs recursively so the pinned stack is composable.

Hermetic: no network, no subprocess but this repository's own interpreter over
its own tree and `git archive` over its own object store, and every mutated
corpus is a `tmp_path` copy — a test that could damage the fixtures it asserts
on is a test that eventually does.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify-snapshot-equivalence.py"
BASE_REPO = (REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures"
             / "base-repo")

#: The vocabulary, restated as a LITERAL rather than imported. Asserting
#: `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology;
#: spelling it out is what makes a silent rename or reorder a test failure,
#: because an operator's runbook and a caller's branch both read these strings.
#:
#: SEVEN NAMED KINDS AND ONE BLANKET, which is
#: `verify-carve-conformance.py`'s own shape (four named,
#: `conformance-unreadable` blanket): the exit contract is held by a
#: `except Exception` that must render SOMETHING, and giving it one of the
#: named codes would make the runner lie about the cause.
RATIFIED_CODES = (
    "equivalence-pre-ref-unreachable",
    "equivalence-pre-tree-unrenderable",
    "equivalence-reach-unavailable",
    "equivalence-profile-unregistered",
    "equivalence-digests-differ",
    "equivalence-post-stack-unrenderable",
    "equivalence-object-store-incomplete",
    "equivalence-unreadable",
)

#: RULED (a) POST-SHED MODE (`#656` comment `5625573095`) froze the carve
#: digests at this tag and this commit, and FLOOR PART 1's `carve_commit` is
#: the same one. Restated here for the reason above: the default is a ratified
#: referent, not an implementation detail.
CARVE_TAG = "opendox-carve-0"
CARVE_COMMIT = "b075fd91dc8fced8e1373825ba80220c33536bae"

#: A second pre-shed ref, so the claim does not rest on one of them.
SECOND_PRE_REF = "contract-v3.7"

#: The document the corpus mutations below act on. It is the fixture's own
#: "legacy note", chosen because it carries no `Possible feats:` section and so
#: nothing else in the corpus cites it — a mutation to it moves what it should
#: move and nothing that would confuse the reading.
MUTABLE_DOC = "ideation/brainstorm/legacy-note.md"


def _load():
    spec = importlib.util.spec_from_file_location(
        "verify_snapshot_equivalence", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load()


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, check=False,
                          cwd=str(REPO_ROOT))


def _json_run(*args: str) -> dict:
    done = _run("--json", *args)
    assert done.stdout, f"no stdout; stderr was: {done.stderr}"
    return json.loads(done.stdout)


def _copy(base: Path, into: Path, name: str) -> Path:
    """One corpus state, as a copy. Never the fixture itself."""
    target = into / name
    shutil.copytree(base, target)
    return target


@pytest.fixture(scope="module")
def shipped() -> dict:
    """ONE default run, reused. It is the expensive one (an archive plus two
    renders) and four assertions want different parts of it."""
    return _json_run()


@pytest.fixture(scope="module")
def four_states(tmp_path_factory) -> dict:
    """The four corpus states, in ONE invocation, with their digests.

    The two that must NOT move the digest are a file the projection does not
    read and the corpus as it ships; the two that MUST are a document removed
    and a lifecycle `Status:` header changed. Built as copies under
    `tmp_path_factory`, so the shipped fixture is never touched.
    """
    root = tmp_path_factory.mktemp("corpus-states")
    shipped_state = _copy(BASE_REPO, root, "shipped")

    unread = _copy(BASE_REPO, root, "unread-file")
    (unread / "ideation" / "brainstorm" / "scratch.txt").write_text(
        "A file the projection does not read.\n", encoding="utf-8")

    dropped = _copy(BASE_REPO, root, "document-dropped")
    (dropped / MUTABLE_DOC).unlink()

    restatused = _copy(BASE_REPO, root, "status-changed")
    doc = restatused / MUTABLE_DOC
    doc.write_text(
        doc.read_text(encoding="utf-8").replace(
            "Status: brainstorm", "Status: staged", 1),
        encoding="utf-8")

    order = (shipped_state, unread, dropped, restatused)
    payload = _json_run(*[a for c in order for a in ("--corpus", str(c))])
    return {"payload": payload,
            "order": [p.name for p in order],
            "digests": [s["pre_sha256"] for s in payload["states"]]}


# ==========================================================================
# 1. the floor holds — § D6 (4)'s own sentence, through the command line
# ==========================================================================


def test_the_shipped_corpus_renders_the_same_bytes_on_both_sides():
    """The whole of FLOOR PART 4 for one corpus, as an operator runs it."""
    done = _run()
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("OK — 1 of 1 corpus state(s) equivalent"), \
        done.stdout
    assert CARVE_TAG in done.stdout
    assert CARVE_COMMIT[:12] in done.stdout


def test_the_verdict_names_every_input_the_evidence_line_quotes(shipped):
    """§ 8.2 owes one evidence line per floor part, and a line nobody can
    re-derive is a line nobody can check. Everything that line names has to
    come out of the run: which pre-split ref, which commit, which openXdox-code
    the post side actually rendered at, what was pinned, and the digest."""
    assert shipped["result"] == "ok"
    assert shipped["pre_ref"] == CARVE_TAG
    assert shipped["pre_commit"] == CARVE_COMMIT
    assert shipped["source_revision"] == MODULE.PINNED_SOURCE_REVISION
    assert shipped["repository"] == MODULE.REPOSITORY_NAME
    # The leg sha is the CHECKED-OUT one, so it is 40 hex characters or the
    # run refused before here — never a placeholder.
    assert len(shipped["openxdox_code"]) == 40, shipped["openxdox_code"]
    assert len(shipped["opendox_code"]) == 40, shipped["opendox_code"]
    state = shipped["states"][0]
    assert state["equivalent"] is True
    assert state["pre_sha256"] == state["post_sha256"]
    assert state["pre_bytes"] == state["post_bytes"] > 0
    assert Path(state["corpus"]) == BASE_REPO.resolve()


def test_all_four_corpus_states_are_equivalent_in_one_run(four_states):
    payload = four_states["payload"]
    assert payload["result"] == "ok"
    assert len(payload["states"]) == 4
    for state, name in zip(payload["states"], four_states["order"]):
        assert state["equivalent"] is True, (
            f"{name}: PRE {state['pre_sha256']} != POST "
            f"{state['post_sha256']}")


def test_two_of_the_four_states_move_the_digest(four_states):
    """THE RUN HAS TEETH, MEASURED RATHER THAN ASSUMED.

    An equal result over states that cannot differ would prove nothing about
    the projection. Two of these four states change what the snapshot says —
    a document removed and a lifecycle `Status:` header rewritten — and two do
    not, which is the second half of the same claim: a projection that read
    everything would move on the unread file too, and "equal" would then only
    mean "both sides ignore the corpus".
    """
    shipped_digest, unread, dropped, restatused = four_states["digests"]
    assert unread == shipped_digest, (
        "a file the projection does not read moved the digest")
    assert dropped != shipped_digest, (
        "dropping a document did not move the digest — the instrument is not "
        "reading the corpus")
    assert restatused != shipped_digest, (
        "changing a lifecycle Status: header did not move the digest")
    assert dropped != restatused, (
        "two different corpus changes produced the same digest")


# ==========================================================================
# 2. the mutation controls — the runner refuses when the sides differ
# ==========================================================================


def _mutated_post():
    """A post side that renders one extra token into ONE field.

    Re-serialized through the SAME canonical writer the runner compares, so
    the difference is the field and not the formatting — which is what lets
    the refusal's diff be read as a finding.
    """
    def render(stack, corpus, source_revision):
        generator, snapshot = stack
        snap = generator.generate_snapshot(
            corpus, MODULE.REPOSITORY_NAME, source_revision=source_revision,
            git=MODULE.FakeGit(head=source_revision))
        snap["generation"]["generator_version"] += "+mutant"
        return snapshot.canonical_bytes(snap)
    return render


def _mutated_pre(real):
    """A pre side whose repository name differs by one character.

    A same-length substitution, so the bytes stay valid JSON and the diff
    names `repository` rather than collapsing into "everything changed".
    """
    def render(tree, corpus, scratch, pre_ref, source_revision):
        raw = real(tree, corpus, scratch, pre_ref, source_revision)
        mutated = raw.replace(b'"fixture-repo"', b'"fixture-repM"', 1)
        assert mutated != raw, "the pre-side mutation did not apply"
        return mutated
    return render


def test_a_mutated_post_side_is_caught(monkeypatch):
    """Mutation control 1. If the pinned stack started projecting something
    the pre-split tree did not, this is the run that goes red."""
    monkeypatch.setattr(MODULE, "render_post", _mutated_post())
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = MODULE.main(["--json"])
    assert code == 2
    payload = json.loads(buffer.getvalue())
    assert payload["code"] == "equivalence-digests-differ"
    assert payload["pre_sha256"] != payload["post_sha256"]
    assert any("generator_version" in line for line in payload["diff"]), \
        payload["diff"][:20]


def test_a_mutated_pre_side_is_caught(monkeypatch):
    """Mutation control 2, on the other side. The two are not one test twice:
    a comparison written `post == post` would pass the first and fail this."""
    monkeypatch.setattr(MODULE, "render_pre",
                        _mutated_pre(MODULE.render_pre))
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = MODULE.main(["--json"])
    assert code == 2
    payload = json.loads(buffer.getvalue())
    assert payload["code"] == "equivalence-digests-differ"
    assert payload["pre_sha256"] != payload["post_sha256"]
    assert any("fixture-repM" in line for line in payload["diff"]), \
        payload["diff"][:20]


def test_the_difference_refusal_prints_both_digests_byte_counts_and_a_diff(
        monkeypatch, capsys):
    """A refusal that printed two hex strings would tell an operator that
    something moved and nothing about what."""
    monkeypatch.setattr(MODULE, "render_post", _mutated_post())
    code = MODULE.main([])
    assert code == 2
    rendered = capsys.readouterr().err
    assert "equivalence-digests-differ" in rendered
    assert rendered.count("sha256 ") >= 2
    assert " bytes," in rendered
    assert "@@" in rendered, "no unified diff in the refusal"
    assert "generator_version" in rendered
    assert "Remediation:" in rendered


# ==========================================================================
# 3. what "the pre-split tree" is — RULED (a), and not resting on one ref
# ==========================================================================


def test_the_default_pre_ref_is_the_published_carve_tag_and_resolves_here():
    """`opendox-carve-0` is FLOOR PART 1's own `carve_commit`, frozen by
    RULED (a) (`#656` comment `5625573095`). Asserted against git rather than
    trusted: a checkout that cannot resolve it is a checkout on which this
    whole suite is measuring something else."""
    assert MODULE.DEFAULT_PRE_REF == CARVE_TAG
    # Through the module's OWN scrubbed wrapper, not a bare `subprocess.run`:
    # an ambient `GIT_DIR` or alternate object directory would otherwise let
    # this supposedly hermetic assertion resolve the tag in ANOTHER repository
    # (Copilot, PR #1105 round 5).
    done = MODULE._git(REPO_ROOT, "rev-parse", "--verify", "--end-of-options",
                       f"{CARVE_TAG}^{{commit}}")
    assert done is not None and done.returncode == 0, (
        f"{CARVE_TAG} is not reachable in this checkout: {done.stderr}. "
        "pytest-suite.yml checks out with fetch-depth: 0 for this reason")
    assert done.stdout.strip() == CARVE_COMMIT


def test_a_second_pre_shed_ref_re_proves_the_same_digest(shipped):
    """The claim does not rest on one ref. `contract-v3.7` is a different
    pre-shed commit with a different `generator.py` blob, and it renders the
    identical snapshot — so the equivalence is a property of the projection
    and not of one tree's incidental state."""
    payload = _json_run("--pre-ref", SECOND_PRE_REF)
    assert payload["result"] == "ok"
    assert payload["pre_commit"] != CARVE_COMMIT
    assert payload["states"][0]["pre_sha256"] == \
        shipped["states"][0]["pre_sha256"]


# ==========================================================================
# 4. every refusal kind, through the command line
# ==========================================================================


def test_an_unknown_pre_ref_refuses_and_names_the_fetch_that_fixes_it():
    done = _run("--pre-ref", "no-such-ref-exists-here")
    assert done.returncode == 2
    assert "equivalence-pre-ref-unreachable" in done.stderr
    assert "git fetch --tags" in done.stderr


def test_a_post_shed_pre_ref_refuses_rather_than_reading_as_a_pass():
    """THE REFUSAL THIS FILE MOST NEEDS TO BE SURE OF. `main` and
    `contract-v4.0` carry an `ideation_dashboard` package WITHOUT its
    renderer, because that is what the § 5.2 shed did. A runner that treated
    "the tree I was pointed at cannot render" as anything but an operator
    error would let FLOOR PART 4 pass over a side that does not exist."""
    done = _run("--pre-ref", "HEAD")
    assert done.returncode == 2
    assert "equivalence-pre-tree-unrenderable" in done.stderr
    assert MODULE.GENERATOR_ROW in done.stderr
    assert "OK " not in done.stdout


def test_a_checkout_with_no_legs_refuses_by_name(tmp_path):
    """The post side is two PINS, and an uninitialized gitlink must refuse
    rather than degrade — `carved_reach`'s own rule, delegated to here.

    Driven by copying the runner and the resolver into a tree that has no
    legs, which is the shape a fresh clone with no `git submodule update` is
    in. The alternative — stubbing the resolver — would prove this file can
    monkeypatch rather than that the command line refuses.
    """
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    for name in ("verify-snapshot-equivalence.py", "carved_reach.py"):
        shutil.copy2(REPO_ROOT / "scripts" / name, scripts / name)
    done = subprocess.run(
        [sys.executable, str(scripts / "verify-snapshot-equivalence.py"),
         "--corpus", str(BASE_REPO)],
        capture_output=True, text=True, check=False, cwd=str(tmp_path))
    assert done.returncode == 2
    assert "equivalence-reach-unavailable" in done.stderr
    assert "git submodule update --init --recursive" in done.stderr


def test_an_unregistered_profile_refuses_and_names_the_registration():
    """§ 4.4's parameterization, from the other side. The arrived generator
    reads its status vocabulary through `domain_profile.current()`, so a
    process that registers none has no words to project and must say so
    rather than render openXdox's own."""
    done = _run("--no-register-profile")
    assert done.returncode == 2
    assert "equivalence-profile-unregistered" in done.stderr
    assert "DomainProfileNotRegistered" in done.stderr


def test_a_corpus_that_is_not_there_refuses_rather_than_comparing_nothing(
        tmp_path):
    """Silence must not read as a pass: two renders of an absent tree would
    agree, and agreeing about nothing is what this refusal exists to stop."""
    done = _run("--corpus", str(tmp_path / "no-corpus-here"))
    assert done.returncode == 2
    assert "equivalence-unreadable" in done.stderr
    assert "silence must not read as a pass" in done.stderr


# ==========================================================================
# 5. the runner's own contract
# ==========================================================================


def test_a_leg_off_its_pin_refuses_rather_than_rendering(monkeypatch):
    """The evidence line says the post side rendered AT THE PINNED
    openXdox-code, and this is what makes that true by construction.

    `carved_reach` imports out of the nested WORKTREE, so a leg left detached
    at some other commit — a bisect, a half-finished bump, a copied tree —
    renders perfectly well, and a runner that merely REPORTED the checked-out
    sha would make a true statement about a run nobody asked for. Driven by
    moving the RECORDED gitlink rather than the checkout, because the two
    comparisons are symmetric and only one of them can be staged in a test
    without touching a submodule.
    """
    real = MODULE.recorded_gitlink

    def moved(parent, path, outer=None):
        oid, source = real(parent, path, outer)
        if path == "code" and parent.name == "openXdox":
            return "0" * 40, source
        return oid, source

    monkeypatch.setattr(MODULE, "recorded_gitlink", moved)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.verify_pins()
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "0" * 40 in caught.value.detail
    assert "checked out at" in caught.value.detail


def test_a_gitlink_that_cannot_be_read_refuses_rather_than_passing(
        monkeypatch):
    """`carved_reach`'s own rule, one layer up: a query that went UNANSWERED is
    not an answer. Nothing was learned about the pin, so nothing may be claimed
    for it — and a runner that shrugged here would report a pin it never
    compared against anything."""
    monkeypatch.setattr(MODULE, "recorded_gitlink",
                        lambda parent, path, outer=None: (None, "HEAD"))
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.verify_pins()
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "records no gitlink" in caught.value.detail


def test_a_dirty_leg_worktree_refuses_because_the_tree_is_what_renders(
        monkeypatch):
    """The gitlink comparison is not enough on its own, and this is why.

    `carved_reach.module()` imports `openxdox.generator` off `openXdox/code/
    src` ON DISK, not out of git, so an uncommitted edit under a leg renders
    bytes that are not the pinned commit's while every sha comparison still
    passes and the verdict still names that commit — the same false evidence
    line one layer lower (Copilot, PR #1105 round 2).

    Driven through `worktree_dirt`, which is the seam, rather than by writing
    into a real submodule: a test that dirties a leg and is killed before its
    cleanup leaves every later run of this gate refusing, which is a worse
    failure than the one it would be proving.
    """
    monkeypatch.setattr(MODULE, "worktree_dirt",
                        lambda leg: [" M src/openxdox/generator.py"])
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.verify_pins()
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "DIRTY" in caught.value.detail
    assert "src/openxdox/generator.py" in caught.value.detail


def test_a_status_read_that_did_not_answer_is_not_read_as_clean(monkeypatch):
    """`None` is not "clean" — `carved_reach`'s rule, held one layer up. A
    status read that failed learned nothing, and a pin this runner could not
    verify is a pin it must not report."""
    monkeypatch.setattr(MODULE, "worktree_dirt", lambda leg: None)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.verify_pins()
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "went unmeasured" in caught.value.detail


def test_worktree_dirt_reads_a_real_repository_both_ways(tmp_path):
    """The seam the two tests above drive, measured against real git rather
    than assumed: clean answers `[]`, a stray file answers with it, and a
    directory that is no repository at all answers `None` — which is the
    distinction the refusals rest on."""
    repo = tmp_path / "leg"
    repo.mkdir()
    for args in (("init", "-q"), ("config", "user.email", "t@example.invalid"),
                 ("config", "user.name", "t")):
        assert MODULE._git(repo, *args).returncode == 0
    (repo / "a.txt").write_text("one\n", encoding="utf-8")
    assert MODULE._git(repo, "add", "a.txt").returncode == 0
    assert MODULE._git(repo, "commit", "-qm", "seed").returncode == 0
    assert MODULE.worktree_dirt(repo) == []
    (repo / "b.txt").write_text("stray\n", encoding="utf-8")
    dirt = MODULE.worktree_dirt(repo)
    assert dirt and any("b.txt" in entry for entry in dirt), dirt
    (repo / "b.txt").unlink()
    (repo / "a.txt").write_text("two\n", encoding="utf-8")
    dirt = MODULE.worktree_dirt(repo)
    assert dirt and any("a.txt" in entry for entry in dirt), dirt
    assert MODULE.worktree_dirt(tmp_path / "not-a-repository-at-all") is None


def test_the_git_scrub_covers_the_channel_that_propagates_dash_c(monkeypatch):
    """`GIT_CONFIG_PARAMETERS` is how `git -c` reaches a child process, so an
    ambient one would still alter these supposedly hermetic object reads
    (Copilot, PR #1105 round 2). Asserted over the built environment, not over
    the constant, because what matters is what the subprocess is handed."""
    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", "'core.abbrev=4'")
    monkeypatch.setenv("GIT_DIR", "/nowhere/else.git")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.abbrev")
    monkeypatch.setenv("GIT_ALTERNATE_OBJECT_DIRECTORIES", "/nowhere/objects")
    environment = MODULE._git_environment()
    for name in ("GIT_CONFIG_PARAMETERS", "GIT_DIR", "GIT_CONFIG_KEY_0",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        assert name not in environment, f"{name} survived the scrub"
    assert environment["GIT_CONFIG_NOSYSTEM"] == "1"
    assert environment["GIT_NO_REPLACE_OBJECTS"] == "1"
    # …and the scrub does not sterilise the rest of the environment: a run
    # that lost PATH would fail for a reason that is not about git.
    assert "PATH" in environment


def test_the_pins_this_run_reports_are_the_ones_it_verified(shipped):
    """Both levels of both legs — SIX mounts, not four — and the reported
    pair is a subset of them.

    The two `spec` mounts are here because `post_side_identity.leg_of()`
    matches the LONGEST verified pin root containing a module's file: without
    them a module arriving under `openDox/spec` (which a `re_destined:` block
    may lawfully do) resolved to the `openDox` ASSEMBLY ROOT, and the verdict
    then named the assembly's commit for a module the assembly does not
    contain — a verified pin, but the wrong one (Copilot, PR #1105 round 6).
    """
    pins = shipped["pins"]
    assert set(pins) == {"openDox", "openDox/code", "openDox/spec",
                         "openXdox", "openXdox/code", "openXdox/spec"}
    assert pins["openXdox/code"] == shipped["openxdox_code"]
    assert pins["openDox/code"] == shipped["opendox_code"]
    assert all(len(v) == 40 for v in pins.values()), pins


def test_a_pre_ref_that_begins_with_a_dash_is_a_revision_not_an_option():
    """`--pre-ref` is command-line input and reaches `git rev-parse`; without
    `--end-of-options` a leading-dash value is parsed as a git OPTION, and the
    runner's ref boundary is then whatever git makes of it (Copilot, PR
    #1105). It must refuse as an unreachable REF."""
    done = _run("--pre-ref=--not-a-ref")
    assert done.returncode == 2
    assert "equivalence-pre-ref-unreachable" in done.stderr
    assert "--not-a-ref" in done.stderr
    assert "unknown option" not in done.stderr.lower()


def test_the_archive_reads_the_resolved_commit_and_not_the_mutable_ref(
        monkeypatch):
    """One ref, resolved ONCE. A branch or a force-updated tag that moved
    between the resolution and the archive would leave the runner recording
    commit A while rendering commit B, and the evidence line would name a tree
    that never rendered (Copilot, PR #1105).
    SPIED AT THE `_git` LAYER, AND THE REAL EXTRACTOR IS KEPT (Copilot on
    #1105 @9ed3def3, suppressed). Replacing `extract_pre_tree()` left the
    `git archive` call it makes unexecuted, so a regression INSIDE that
    function — passing `pre_ref` where `pre_commit` belongs — would have left
    this test green while the invariant it names was broken."""
    archives: list[tuple[str, ...]] = []
    real_git = MODULE._git

    def recording(repo, *arguments, **kwargs):
        if arguments and arguments[0] == "archive":
            archives.append(arguments)
        return real_git(repo, *arguments, **kwargs)

    monkeypatch.setattr(MODULE, "_git", recording)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        assert MODULE.main(["--json"]) == 0
    payload = json.loads(buffer.getvalue())
    assert len(archives) == 1, archives
    # The revision `git archive` was handed, positionally: after
    # `archive --format=tar` and before the `--` separator.
    handed = archives[0][2]
    assert handed == payload["pre_commit"], (handed, payload["pre_commit"])
    assert len(handed) == 40 and handed != MODULE.DEFAULT_PRE_REF


def test_a_registration_failure_is_not_relabelled_as_no_profile(monkeypatch,
                                                                capsys):
    """`register_openxfactory()` raises `AlreadyRegistered` when some OTHER
    profile already holds the process, and the composite can refuse a
    malformed declaration. Neither is "no profile is registered", and a
    refusal that called them that would send an operator to run the
    registration that is already the problem (Copilot, PR #1105). They arrive
    as `equivalence-unreadable` NAMING the exception, which is what that code
    is for."""
    import opendox_host

    def already(*args, **kwargs):
        raise RuntimeError("AlreadyRegistered: another profile holds this "
                           "process")

    monkeypatch.setattr(opendox_host, "register_openxfactory", already)
    assert MODULE.main([]) == 2
    rendered = capsys.readouterr().err
    assert "equivalence-unreadable" in rendered
    assert "AlreadyRegistered" in rendered
    assert "equivalence-profile-unregistered" not in rendered


def test_every_git_read_is_scrubbed_bounded_and_replacement_free():
    """`GIT_DIR`, an alternate object directory or a replace ref can make a
    `<revision>:<path>` read answer out of another object store, and a partial
    clone whose promisor remote is unreachable can make it HANG — and this
    runner's whole claim is that it read ONE named tree, offline, in about a
    second (Copilot, PR #1105). Asserted over the SOURCE because the
    alternative proof needs a poisoned environment and a hung remote, and
    because what is being held is that NO read escapes the wrapper."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert source.count('subprocess.run(\n            ["git",') == 1, (
        "a `git` subprocess is being run outside `_git()`")
    assert '"--no-replace-objects"' in source
    assert "GIT_CONFIG_NOSYSTEM" in source
    assert "timeout=_GIT_TIMEOUT" in source
    # AND THE REF BOUNDARY, HELD HERE FOR A MEASURED REASON. No behavioural
    # difference is reachable today: git 2.43.0 answers `rev-parse --verify
    # --quiet` with exit 1 and EMPTY stderr for a leading-dash revision
    # whether or not the marker is present, because the `^{commit}` suffix
    # this runner appends already makes any option name unparseable. The
    # marker is kept so that a later edit which drops that suffix does not
    # silently drop the boundary with it — which is precisely a change no
    # behavioural test could see, and why this one is over the source.
    assert '"--end-of-options",\n                f"{pre_ref}^{{commit}}"' \
        in source, "the ref read lost its end-of-options marker"


def test_the_post_side_label_is_derived_from_the_resolved_modules(shipped):
    """`carved_reach.module()` answers from the MANIFEST ROW, and a
    `re_destined:` block can move a row to the other leg (RULED Q6, `#656`
    comment `5648044785`). A verdict that spelled the module names and the leg
    into its own text would then render the new modules and report the old
    leg — the evidence line naming a pin that did not render, by a route the
    pin checks cannot see (Copilot, PR #1105 round 3)."""
    assert shipped["post_leg"] in shipped["pins"], shipped["post_leg"]
    assert shipped["post_leg_commit"] == shipped["pins"][shipped["post_leg"]]
    assert "generator" in shipped["post_modules"]
    assert "snapshot" in shipped["post_modules"]
    assert shipped["post_leg_commit"][:12] in shipped["post_label"]
    # …and the source does not SPELL the answer anywhere the verdict reads it.
    source = SCRIPT.read_text(encoding="utf-8")
    verdict = source[source.index("def _print_ok"):source.index("def main")]
    assert "openxdox" not in verdict.lower(), (
        "the verdict line spells a leg or a module name instead of deriving "
        "it")


def test_the_post_side_label_follows_a_re_destination(monkeypatch):
    """The same property, driven: point the resolved generator at the OTHER
    leg and the label follows it rather than reporting openXdox."""
    real = MODULE.post_side_identity
    pins = {"openDox": "a" * 40, "openDox/code": "b" * 40,
            "openXdox": "c" * 40, "openXdox/code": "d" * 40}

    class Elsewhere:
        __name__ = "opendox.generator"
        __file__ = str(REPO_ROOT / "openDox" / "code" / "src" / "opendox"
                       / "generator.py")

    class Sibling:
        __name__ = "opendox.snapshot"
        __file__ = str(REPO_ROOT / "openDox" / "code" / "src" / "opendox"
                       / "snapshot.py")

    identity = real((Elsewhere(), Sibling()), pins)
    assert identity["post_leg"] == "openDox/code"
    assert identity["post_leg_commit"] == "b" * 40
    assert identity["post_legs"] == ["openDox/code"]
    assert "opendox.generator" in identity["post_label"]
    assert "openXdox" not in identity["post_label"]


def test_a_mixed_leg_stack_is_reported_as_one(monkeypatch):
    """`carved_reach.module()` resolves the generator row and the snapshot row
    INDEPENDENTLY and a `re_destined:` block is per row, so the two can
    legitimately arrive at different legs (RULED Q6, `#656` comment
    `5648044785`). Deriving one leg from the generator alone and printing it
    for both would make the evidence line false in exactly the case the
    derivation exists to survive (Copilot, PR #1105 round 4). A mixed stack is
    not refused — the manifest permits it — it is REPORTED."""
    pins = {"openDox": "a" * 40, "openDox/code": "b" * 40,
            "openXdox": "c" * 40, "openXdox/code": "d" * 40}

    class Generator:
        __name__ = "openxdox.generator"
        __file__ = str(REPO_ROOT / "openXdox" / "code" / "src" / "openxdox"
                       / "generator.py")

    class Snapshot:
        __name__ = "opendox.snapshot"
        __file__ = str(REPO_ROOT / "openDox" / "code" / "src" / "opendox"
                       / "snapshot.py")

    identity = MODULE.post_side_identity((Generator(), Snapshot()), pins)
    assert identity["post_legs"] == ["openXdox/code", "openDox/code"]
    assert "unresolved" not in identity["post_legs"]
    assert identity["post_module_legs"] == {
        "openxdox.generator": "openXdox/code",
        "opendox.snapshot": "openDox/code"}
    assert "d" * 12 in identity["post_label"]
    assert "b" * 12 in identity["post_label"]
    assert "MIXED-leg" in identity["post_label"]


def test_a_module_outside_every_verified_pin_root_refuses(tmp_path):
    """FAIL-CLOSED. A module resolving outside every verified pin root is a
    post side this run cannot name a commit for, and a verdict that printed a
    label with no sha while exiting 0 would be the "silence reads as a pass"
    failure the whole file is built to refuse (Copilot, PR #1105 round 5)."""
    pins = {"openDox": "a" * 40, "openDox/code": "b" * 40,
            "openXdox": "c" * 40, "openXdox/code": "d" * 40}

    class Elsewhere:
        __name__ = "somewhere.generator"
        __file__ = str(tmp_path / "somewhere" / "generator.py")

    class Sibling:
        __name__ = "openxdox.snapshot"
        __file__ = str(REPO_ROOT / "openXdox" / "code" / "src" / "openxdox"
                       / "snapshot.py")

    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.post_side_identity((Elsewhere(), Sibling()), pins)
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "somewhere.generator" in caught.value.detail
    assert "outside every verified pin root" in caught.value.detail


def test_a_correct_gitlink_with_a_wrong_checkout_refuses_too(monkeypatch):
    """The checkout comparison, driven on its OWN — the recorded gitlink left
    exactly as git reports it while `rev-parse HEAD` answers a different valid
    commit. The mutation sweep already proves the branch is live (deleting
    `checked_out != recorded` fails the suite), and this makes the case
    explicit rather than incidental (Copilot, PR #1105 round 5)."""
    real = MODULE._git
    other = "e" * 40

    def wrong_head(repo, *arguments, **kwargs):
        if arguments[:2] == ("rev-parse", "--verify") and "HEAD" in arguments:
            done = real(repo, *arguments, **kwargs)
            if done is not None and done.returncode == 0:
                done.stdout = other + "\n"
            return done
        return real(repo, *arguments, **kwargs)

    monkeypatch.setattr(MODULE, "_git", wrong_head)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.verify_pins()
    assert caught.value.code == "equivalence-reach-unavailable"
    assert other in caught.value.detail
    assert "records" in caught.value.detail


def test_a_source_revision_that_is_not_an_object_id_refuses():
    """Both sides stamp the snapshot with this value through an INJECTED git
    that resolves nothing, so without a shape check `--source-revision HEAD`
    renders, compares equal and exits 0 over a snapshot anchored to something
    that is not a commit (Copilot, PR #1105 round 3)."""
    for bad in ("HEAD", "main", "not-a-revision", "abcd123", ""):
        done = _run(f"--source-revision={bad}")
        assert done.returncode == 2, f"{bad!r} was accepted"
        assert "equivalence-unreadable" in done.stderr, bad
        assert "is not an object id" in done.stderr, bad
    # …and a sha-256 object id is accepted, because both widths are real.
    assert MODULE.OBJECT_ID.fullmatch("a" * 64) is not None
    assert MODULE.OBJECT_ID.fullmatch("A" * 40) is not None


def test_a_git_read_that_did_not_answer_is_not_a_missing_ref(monkeypatch):
    """`_git()` answers `None` for a timeout and for a git that could not be
    run, and neither has established that the ref is ABSENT. Telling an
    operator to `git fetch --tags` because a promisor remote hung sends them
    to fix the wrong thing (Copilot, PR #1105 round 3)."""
    monkeypatch.setattr(MODULE, "_git", lambda *a, **k: None)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.pre_ref_commit(CARVE_TAG, REPO_ROOT)
    assert caught.value.code == "equivalence-unreadable"
    assert "never learned whether that ref exists" in caught.value.detail


def test_a_formatting_only_difference_still_prints_a_diff(monkeypatch,
                                                          capsys):
    """`_pretty()` parses and re-serializes, which ERASES exactly the
    differences the byte comparison exists to catch at the margin — a trailing
    newline, indentation, key order. An `equivalence-digests-differ` whose
    diff is empty is the refusal without the half that makes it actionable
    (Copilot, PR #1105 round 3)."""
    real = MODULE.render_post

    def trailing_newline(stack, corpus, source_revision):
        return real(stack, corpus, source_revision) + b"\n"

    monkeypatch.setattr(MODULE, "render_post", trailing_newline)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        assert MODULE.main(["--json"]) == 2
    payload = json.loads(buffer.getvalue())
    assert payload["code"] == "equivalence-digests-differ"
    assert payload["pre_bytes"] + 1 == payload["post_bytes"]
    assert payload["diff"], "the diff is empty for a real byte difference"
    assert any("(raw)" in line or "differ in length alone" in line
               for line in payload["diff"]), payload["diff"][:10]


def test_an_archive_member_that_is_not_a_plain_file_is_refused(tmp_path):
    """The archive is extracted IN-PROCESS with every member checked, because
    `tar -x` was two holes at once: GNU tar reads `TAR_OPTIONS` out of the
    ambient environment, and a SYMLINK or path-escaping member would be
    written as given — which is how an archive reaches outside the directory
    that is supposed to contain it, defeating the isolation the whole
    measurement rests on (Copilot, PR #1105 round 7)."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as bundle:
        payload = b"x = 1\n"
        info = tarfile.TarInfo("scripts/ideation_dashboard/ok.py")
        info.size = len(payload)
        bundle.addfile(info, io.BytesIO(payload))
        link = tarfile.TarInfo("scripts/ideation_dashboard/escape.py")
        link.type = tarfile.SYMTYPE
        link.linkname = "/etc/passwd"
        bundle.addfile(link)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE._extract_safely(buffer.getvalue(), tmp_path / "out", "a-ref")
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert "escape.py" in caught.value.detail
    assert not (tmp_path / "out" / "scripts" / "ideation_dashboard"
                / "escape.py").exists()


def test_an_archive_member_escaping_the_directory_is_refused(tmp_path):
    """`..` in a member path, which is the other half of the same rule."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as bundle:
        payload = b"x = 1\n"
        info = tarfile.TarInfo("../outside.py")
        info.size = len(payload)
        bundle.addfile(info, io.BytesIO(payload))
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE._extract_safely(buffer.getvalue(), tmp_path / "out", "a-ref")
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert "escapes the extraction directory" in caught.value.detail
    assert not (tmp_path / "outside.py").exists()


def test_a_corpus_that_projects_no_documents_refuses(tmp_path):
    """An existing EMPTY directory is not a corpus. The `is_dir()` guard
    catches a path that is not there; it does not catch one that is there and
    empty, and both sides then render the same vacuous snapshot and compare
    equal — the precise false pass the guard exists to prevent, arriving
    through the case it does not cover (Copilot, PR #1105 round 7)."""
    empty = tmp_path / "not-a-corpus"
    empty.mkdir()
    done = _run("--corpus", str(empty))
    assert done.returncode == 2
    assert "equivalence-unreadable" in done.stderr
    assert "projected 0 document(s)" in done.stderr
    assert "silence must not read as a pass" in done.stderr


def test_the_shipped_corpus_projects_the_documents_it_is_compared_on(shipped):
    """…and the positive half, so the guard above cannot be satisfied by a
    corpus that projects nothing everywhere."""
    assert shipped["states"][0]["documents"] >= 1


def test_the_pre_child_is_bounded_and_a_timeout_is_a_refusal(monkeypatch):
    """`--pre-ref` accepts any pre-shed revision, so a renderer that loops
    would hang a REQUIRED gate rather than refuse. It was the only child
    without a bound (Copilot, PR #1105 round 7)."""
    assert MODULE._CHILD_TIMEOUT > 0

    def hang(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd="python3", timeout=MODULE._CHILD_TIMEOUT)

    monkeypatch.setattr(MODULE, "_run_pre_child", hang)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.render_pre(REPO_ROOT, BASE_REPO, REPO_ROOT, CARVE_TAG,
                          MODULE.PINNED_SOURCE_REVISION)
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert "did not finish rendering" in caught.value.detail
    # …and the real call carries the bound, so the refusal is reachable.
    source = SCRIPT.read_text(encoding="utf-8")
    assert "timeout=_CHILD_TIMEOUT" in source


def test_a_child_that_writes_no_output_cannot_reuse_the_previous_state(
        monkeypatch, tmp_path):
    """`--corpus` is repeatable and every state used to share ONE output
    file. A child that exited 0 WITHOUT writing would leave the previous
    state's bytes in place and this state would be compared against them —
    a measurement this runner did not take, reported as one it did (Copilot,
    PR #1105 round 8)."""
    real = MODULE._run_pre_child
    seen: list[str] = []

    def once(tree, corpus, out, source_revision):
        seen.append(str(out))
        if len(seen) == 1:
            return real(tree, corpus, out, source_revision)
        # exits 0, writes nothing
        return subprocess.CompletedProcess(args=["python3"], returncode=0,
                                           stdout="", stderr="")

    monkeypatch.setattr(MODULE, "_run_pre_child", once)
    second = tmp_path / "second"
    shutil.copytree(BASE_REPO, second)
    code = MODULE.main(["--corpus", str(BASE_REPO), "--corpus", str(second)])
    assert code == 2
    assert len(seen) == 2 and seen[0] != seen[1], (
        "the two states shared one output path")


def test_a_byte_only_difference_names_where_the_bytes_part_company(
        monkeypatch):
    """The last-resort diagnostic must not invent a cause. Both sides carrying
    distinct invalid UTF-8 that `decode(errors="replace")` flattens to the
    same text leaves every line-oriented diff empty, and the earlier wording
    then said they "differ in length alone" while printing two EQUAL lengths
    (Copilot, PR #1105 round 9)."""
    pre = b'{"a": "\xff", "documents": [1]}'
    post = b'{"a": "\xfe", "documents": [1]}'
    assert len(pre) == len(post)
    assert pre.decode("utf-8", "replace") == post.decode("utf-8", "replace")
    monkeypatch.setattr(MODULE, "projected_documents", lambda raw: 1)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.compare(pre, post, Path("/corpus"), "a-ref", "a-label")
    assert caught.value.code == "equivalence-digests-differ"
    rendered = "\n".join(caught.value.payload["diff"])
    assert "BYTE level" in rendered
    assert "first differing byte at offset" in rendered
    assert "differ in length alone" not in rendered


def test_the_git_environment_disables_the_system_attributes_file():
    """`GIT_ATTR_NOSYSTEM` was SCRUBBED and never SET, which is half a guard:
    dropping an inherited one only stops a caller DISABLING the system
    attributes file, and `git archive` then still consults `/etc/gitattributes`
    — where an `export-ignore` silently changes WHICH FILES the pre-split tree
    carries (Copilot on #1105 @9ed3def3, suppressed). The tree this runner
    reads must not vary with the host it is read on."""
    environment = MODULE._git_environment()
    assert environment["GIT_ATTR_NOSYSTEM"] == "1"
    assert environment["GIT_CONFIG_NOSYSTEM"] == "1"
    assert environment["GIT_NO_REPLACE_OBJECTS"] == "1"


def test_an_inherited_attr_nosystem_is_replaced_not_merely_dropped(
        monkeypatch):
    """…and a caller who sets it to `0` does not get it back."""
    monkeypatch.setenv("GIT_ATTR_NOSYSTEM", "0")
    assert MODULE._git_environment()["GIT_ATTR_NOSYSTEM"] == "1"


def test_the_post_render_is_bounded_and_a_timeout_is_a_named_refusal(
        monkeypatch):
    """The POST side runs IN THIS PROCESS on purpose — it is the only stack
    the process has imported, and the PRE side, the one that would collide
    with it, is already in a child of its own — so the PRE child's `timeout=`
    is not available to it. Without a watchdog a non-terminating regression in
    a FUTURE pinned leg (and the post side IS a pin that moves) hangs the
    required `pytest-suite` job until its own 35-minute limit instead of
    returning the refusal this file promises for every other failure (Copilot
    on #1105 @9ed3def3, suppressed)."""
    monkeypatch.setattr(MODULE, "_CHILD_TIMEOUT", 0.05)

    class Slow:
        def generate_snapshot(self, *args, **kwargs):
            time.sleep(5)
            raise AssertionError("the watchdog did not fire")

    class Unused:
        @staticmethod
        def canonical_bytes(snap):
            raise AssertionError("unreachable")

    started = time.monotonic()
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.render_post((Slow(), Unused()), BASE_REPO,
                           MODULE.PINNED_SOURCE_REVISION)
    assert time.monotonic() - started < 4, "the bound did not cut the render"
    assert caught.value.code == "equivalence-post-stack-unrenderable"
    assert "did not finish rendering" in caught.value.detail


def test_the_watchdog_is_disarmed_when_the_render_returns(monkeypatch):
    """A timer left armed would fire during whatever ran next — which in a
    suite is another test. The real render is used, so this is the ordinary
    path rather than a constructed one."""
    monkeypatch.setattr(MODULE, "_CHILD_TIMEOUT", 30)
    stack = MODULE.post_stack()
    MODULE.render_post(stack, BASE_REPO, MODULE.PINNED_SOURCE_REVISION)
    remaining, _interval = signal.getitimer(signal.ITIMER_REAL)
    assert remaining == 0.0, f"a timer is still armed for {remaining}s"


def test_a_renderer_that_catches_exception_cannot_swallow_the_watchdog(
        monkeypatch):
    """The renderer is PINNED THIRD-PARTY CODE, and an ordinary
    `except Exception:` inside it — a retry, a cleanup, a log-and-carry-on —
    must not consume the alarm and return as though the render had finished.
    The verdict would then be computed from whatever was half-built when the
    alarm landed, and the promised refusal would never arrive (Copilot on
    #1110). `_RenderTimeout` derives from `BaseException` for this."""
    monkeypatch.setattr(MODULE, "_CHILD_TIMEOUT", 0.05)

    class Swallowing:
        def generate_snapshot(self, *args, **kwargs):
            try:
                time.sleep(5)
            except Exception:  # noqa: BLE001 - exactly what a leg may do
                return "a snapshot built from nothing"
            raise AssertionError("the watchdog did not fire")

    class Unused:
        @staticmethod
        def canonical_bytes(snap):
            raise AssertionError("unreachable")

    started = time.monotonic()
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.render_post((Swallowing(), Unused()), BASE_REPO,
                           MODULE.PINNED_SOURCE_REVISION)
    assert time.monotonic() - started < 4, "the bound did not cut the render"
    assert caught.value.code == "equivalence-post-stack-unrenderable"


def test_the_bound_still_covers_the_canonicalization(monkeypatch):
    """`render_post()` promises canonical BYTES, and `canonical_bytes` is the
    snapshot leg's OWN code: disarming before it ran left a pinned leg free
    to hang the gate while SERIALIZING (Copilot on #1110). Read from inside
    the call, so it asserts the bound rather than the ordering of two
    lines."""
    monkeypatch.setattr(MODULE, "_CHILD_TIMEOUT", 30)
    seen = {}

    class Renderer:
        def generate_snapshot(self, *args, **kwargs):
            return "snap"

    class Serializer:
        @staticmethod
        def canonical_bytes(snap):
            seen["remaining"] = signal.getitimer(signal.ITIMER_REAL)[0]
            return b"bytes"

    rendered = MODULE.render_post((Renderer(), Serializer()), BASE_REPO,
                                  MODULE.PINNED_SOURCE_REVISION)
    assert rendered == b"bytes"
    assert seen["remaining"] > 0, "canonicalization ran outside the bound"


def test_a_canonicalization_that_hangs_is_the_same_named_refusal(monkeypatch):
    """…and end to end, not merely armed."""
    monkeypatch.setattr(MODULE, "_CHILD_TIMEOUT", 0.05)

    class Renderer:
        def generate_snapshot(self, *args, **kwargs):
            return "snap"

    class Slow:
        @staticmethod
        def canonical_bytes(snap):
            time.sleep(5)
            raise AssertionError("the watchdog did not fire")

    started = time.monotonic()
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.render_post((Renderer(), Slow()), BASE_REPO,
                           MODULE.PINNED_SOURCE_REVISION)
    assert time.monotonic() - started < 4, "the bound did not cut the render"
    assert caught.value.code == "equivalence-post-stack-unrenderable"


def test_a_tighter_caller_deadline_is_left_alone_rather_than_loosened():
    """A process gets ONE `ITIMER_REAL`, so arming ours over a caller's
    EARLIER deadline — `pytest-timeout` in its `signal` method, a supervising
    runner, a caller that bounded this whole verification — would silently
    LOOSEN the bound that caller set (Copilot on #1110, suppressed)."""
    def caller_handler(signum, frame):
        raise AssertionError("not expected to fire in this test")

    previous = signal.signal(signal.SIGALRM, caller_handler)
    signal.setitimer(signal.ITIMER_REAL, 30)
    try:
        assert MODULE.arm_render_watchdog(300) is None
        remaining = signal.getitimer(signal.ITIMER_REAL)[0]
        assert 29 < remaining <= 30, f"the caller's timer moved: {remaining}"
        assert signal.getsignal(signal.SIGALRM) is caller_handler
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def test_a_looser_caller_deadline_comes_back_with_what_is_left_of_it():
    """Where we DO arm, `disarm()` must put the caller's timer back at its
    REMAINING delay and not at its original one — restoring the full 30s
    would silently extend a deadline as surely as cancelling it removes
    one."""
    def caller_handler(signum, frame):
        raise AssertionError("not expected to fire in this test")

    previous = signal.signal(signal.SIGALRM, caller_handler)
    signal.setitimer(signal.ITIMER_REAL, 30)
    try:
        disarm = MODULE.arm_render_watchdog(0.5)
        assert disarm is not None
        assert signal.getitimer(signal.ITIMER_REAL)[0] <= 0.5
        time.sleep(0.05)
        disarm()
        remaining = signal.getitimer(signal.ITIMER_REAL)[0]
        assert 28 < remaining < 29.96, f"restored as {remaining}s"
        assert signal.getsignal(signal.SIGALRM) is caller_handler
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def test_a_caller_deadline_that_passed_comes_back_firing_not_cancelled():
    """Restoring a caller's timer with a delay of exactly `0` would CANCEL
    it. Our own alarm can be DEFERRED — CPython runs a handler only between
    bytecodes, so a leg inside a C extension holding the GIL delays it — and
    a deferral long enough carries the run past the caller's later deadline
    too. It comes back LATE, which is true, rather than never, which is
    not."""
    fired = []

    def caller_handler(signum, frame):
        fired.append(time.monotonic())

    previous = signal.signal(signal.SIGALRM, caller_handler)
    signal.setitimer(signal.ITIMER_REAL, 0.20)
    try:
        disarm = MODULE.arm_render_watchdog(0.05)
        assert disarm is not None
        try:
            time.sleep(0.10)  # our own alarm lands in here
        except MODULE._RenderTimeout:
            pass
        time.sleep(0.20)  # …and the caller's deadline passes meanwhile
        assert not fired, "our handler was the one installed"
        disarm()
        deadline = time.monotonic() + 3
        while not fired and time.monotonic() < deadline:
            time.sleep(0.01)
        assert fired, "the expired deadline was cancelled, not restored"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def test_the_dirty_leg_remediation_fits_the_dirt_it_reports(monkeypatch):
    """`git checkout -- .` restores TRACKED paths only and a plain `git stash`
    leaves untracked files behind, so for a `??` entry the first spelling sent
    an operator to a command that could not make the next run clean (Copilot
    on #1105 @9ed3def3, suppressed)."""
    cases = {
        (" M src/openxdox/generator.py",): ("checkout -- .", "stash -u"),
        ("?? src/openxdox/stray.py",): ("stash -u", None),
        (" M src/a.py", "?? src/b.py"): ("stash -u", None),
    }
    for dirt, (wanted, unwanted) in cases.items():
        monkeypatch.setattr(MODULE, "worktree_dirt",
                            lambda leg, d=list(dirt): d)
        with pytest.raises(MODULE.EquivalenceRefusal) as caught:
            MODULE.verify_pins()
        detail = caught.value.detail
        assert caught.value.code == "equivalence-reach-unavailable"
        assert wanted in detail, (dirt, detail)
        if unwanted is not None:
            assert unwanted not in detail, (dirt, detail)


def _seed(repo: Path) -> None:
    """A real repository with one commit, for the index tests below."""
    repo.mkdir(parents=True, exist_ok=True)
    for args in (("init", "-q"), ("config", "user.email", "t@example.invalid"),
                 ("config", "user.name", "t")):
        assert MODULE._git(repo, *args).returncode == 0
    (repo / "a.txt").write_text("one\n", encoding="utf-8")
    assert MODULE._git(repo, "add", "a.txt").returncode == 0
    assert MODULE._git(repo, "commit", "-qm", "seed").returncode == 0


def test_a_conflicted_index_refuses_rather_than_reading_a_merge_stage(
        tmp_path):
    """`git ls-files -s` lists stages 1, 2 and 3 during an unresolved merge,
    so reading the FIRST `160000` row takes the MERGE BASE's gitlink as the
    pin this repository records — a commit nobody has declared — and then
    refuses or passes on it. There is no recorded pin during a conflict
    (Copilot, PR #1105 round 3, owed since).

    Driven against a REAL index: `update-index --index-info` writes staged
    entries directly, which is what a conflicted merge leaves behind.
    """
    repo = tmp_path / "parent"
    _seed(repo)
    stages = "".join(
        f"160000 {str(n) * 40} {n}\tcode\n" for n in (1, 2, 3))
    done = subprocess.run(["git", "-C", str(repo), "update-index",
                           "--index-info"], input=stages, text=True,
                          capture_output=True, check=False)
    assert done.returncode == 0, done.stderr
    listed = MODULE._git(repo, "ls-files", "-s", "--", "code")
    assert "160000" in listed.stdout
    assert " 0\t" not in listed.stdout, "a stage-0 row survived"
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.recorded_gitlink(repo, "code")
    assert caught.value.code == "equivalence-reach-unavailable"
    assert "CONFLICTED" in caught.value.detail
    assert "stage 1" in caught.value.detail
    assert "1" * 12 in caught.value.detail


def test_a_stage_zero_gitlink_is_still_read_as_the_recorded_pin(tmp_path):
    """…and the ordinary case is untouched: one stage-0 row is the pin."""
    repo = tmp_path / "parent"
    _seed(repo)
    oid = "a" * 40
    assert MODULE._git(repo, "update-index", "--add", "--cacheinfo",
                       f"160000,{oid},code").returncode == 0
    recorded, source = MODULE.recorded_gitlink(repo, "code")
    assert recorded == oid
    assert source == "the index"


def test_a_nested_gitlink_is_read_from_the_outer_commit_not_the_index(
        tmp_path):
    """THE CHAIN IS RESOLVED FROM THE EXACT COMMIT BEING CLAIMED.

    The index-first rule is right for the pin THIS repository declares — a
    re-pin must be checkable before it is committed — and wrong one level
    down, where the question is what the commit the superproject records
    actually contains. A `code` gitlink staged inside `openDox` is in no
    commit openxFactory has declared, yet an index-first read there would
    take it as the recorded pin while `openDox`'s own HEAD still matched, so
    the level above stayed green (Copilot, PR #1105 round 10).
    """
    repo = tmp_path / "assembly"
    _seed(repo)
    committed, staged = "b" * 40, "c" * 40
    assert MODULE._git(repo, "update-index", "--add", "--cacheinfo",
                       f"160000,{committed},code").returncode == 0
    assert MODULE._git(repo, "commit", "-qm", "pin").returncode == 0
    outer = MODULE._git(repo, "rev-parse", "HEAD").stdout.strip()
    assert MODULE._git(repo, "update-index", "--cacheinfo",
                       f"160000,{staged},code").returncode == 0

    from_index, index_source = MODULE.recorded_gitlink(repo, "code")
    assert from_index == staged, "the index-first read is unchanged"
    assert index_source == "the index"

    from_commit, commit_source = MODULE.recorded_gitlink(repo, "code", outer)
    assert from_commit == committed, (
        "the nested read took the STAGED gitlink, which is in no commit the "
        "superproject records")
    assert outer[:12] in commit_source


def test_the_pin_chain_is_ordered_parents_before_their_children():
    """`verify_pins()` reads each nested gitlink out of the commit its
    PARENT's row just verified, so a child listed before its parent would
    raise `KeyError` — the ordering is load-bearing, not cosmetic."""
    seen: set[str] = {"."}
    for parent_rel, path in MODULE.LEG_GITLINKS:
        assert parent_rel in seen, f"{parent_rel} is listed after its child"
        seen.add(f"{parent_rel}/{path}".lstrip("./"))


def test_the_spec_mounts_are_pinned_so_a_module_there_names_its_own_leg():
    """`leg_of()` matches the LONGEST verified pin root containing a module's
    file. Without the `spec` mounts in the pin set, a module under
    `openDox/spec` — which a `re_destined:` block may lawfully put there —
    resolved to the `openDox` ASSEMBLY ROOT, and the verdict named the
    assembly's commit for a module the assembly does not contain: a verified
    pin, but the wrong one (Copilot, PR #1105 round 6, measured there)."""
    class Module:
        __name__ = "openxdox.spec_module"
        __file__ = str(MODULE.ROOT / "openDox" / "spec" / "thing.py")

    pins = {"openDox": "d" * 40, "openDox/code": "e" * 40,
            "openDox/spec": "f" * 40, "openXdox": "a" * 40,
            "openXdox/code": "b" * 40, "openXdox/spec": "c" * 40}
    identity = MODULE.post_side_identity((Module(),), pins)
    assert identity["post_leg"] == "openDox/spec"
    assert identity["post_leg_commit"] == "f" * 40
    # …and the cleanliness sweep follows the pin, for the same reason: a
    # module that arrives at a spec mount is IMPORTED off that tree, so an
    # uncommitted edit under it renders bytes that are not the commit the
    # verdict would name.
    assert "openDox/spec" in MODULE.IMPORTED_LEGS
    assert "openXdox/spec" in MODULE.IMPORTED_LEGS


def test_verify_pins_reads_each_nested_gitlink_from_its_parents_commit(
        monkeypatch):
    """The wiring, not just the helper: `verify_pins()` must HAND each nested
    row the commit the row above it verified. Reading the nested checkout's
    own HEAD or index there is the hole — a gitlink staged inside `openDox`
    is in no commit openxFactory has declared (Copilot, PR #1105 round 10)."""
    real = MODULE.recorded_gitlink
    calls: list[tuple[str, str, str | None]] = []

    def spy(parent, path, outer=None):
        calls.append((parent.name, path, outer))
        return real(parent, path, outer)

    monkeypatch.setattr(MODULE, "recorded_gitlink", spy)
    pins = MODULE.verify_pins()
    outers = {(parent, path): outer for parent, path, outer in calls}
    for parent, path in (("openDox", "code"), ("openDox", "spec"),
                         ("openXdox", "code"), ("openXdox", "spec")):
        assert outers[(parent, path)] == pins[parent], (
            f"{parent}/{path} was resolved from {outers[(parent, path)]}, "
            f"not from the {pins[parent]} its parent verified")
    assert outers[(MODULE.ROOT.name, "openDox")] is None, (
        "the superproject's own gitlinks stay index-first")


def test_the_git_environment_disables_lazy_fetching(monkeypatch):
    """A MEASUREMENT MUST NOT GO TO THE NETWORK IN THE MIDDLE OF ITSELF. In a
    partial clone a read of an absent blob fetches it from the promisor
    remote, so `git archive` hangs for as long as the network takes — or for
    ever — inside a runner whose contract is to refuse rather than hang
    (Copilot, PR #1105 round 6)."""
    assert MODULE._git_environment()["GIT_NO_LAZY_FETCH"] == "1"
    monkeypatch.setenv("GIT_NO_LAZY_FETCH", "0")
    assert MODULE._git_environment()["GIT_NO_LAZY_FETCH"] == "1"


def test_a_partial_clone_refuses_by_name_and_names_the_fetch(tmp_path):
    """END TO END, against a real `--filter=blob:none` clone.

    The reproduction is this runner's own case: archive a TAG whose blobs the
    checkout never materialized. Measured — with `GIT_NO_LAZY_FETCH=1` the
    archive fails rc 128 `fatal: could not fetch <oid> from promisor remote`;
    without it the same command exits 0 after a silent fetch. The old message
    called that a tree without a renderer and sent the operator to replace a
    good `--pre-ref` (Copilot, PR #1105 round 6).
    """
    origin = tmp_path / "origin"
    _seed(origin)
    assert MODULE._git(origin, "config", "uploadpack.allowFilter",
                       "true").returncode == 0
    for path in MODULE.ARCHIVE_PATHS:
        (origin / path).mkdir(parents=True, exist_ok=True)
        (origin / path / "generator.py").write_text("v1\n" * 400,
                                                    encoding="utf-8")
    assert MODULE._git(origin, "add", "-A").returncode == 0
    assert MODULE._git(origin, "commit", "-qm", "one").returncode == 0
    assert MODULE._git(origin, "tag", "-a", "carve-0", "-m",
                       "pre-split").returncode == 0
    pre_commit = MODULE._git(origin, "rev-parse",
                             "carve-0^{commit}").stdout.strip()
    for path in MODULE.ARCHIVE_PATHS:
        (origin / path / "generator.py").write_text("v2\n" * 400,
                                                    encoding="utf-8")
    assert MODULE._git(origin, "commit", "-qam", "two").returncode == 0

    # THE CLONE ITSELF MUST BE ALLOWED TO LAZY-FETCH: its checkout needs the
    # blobs of the tip. The runner sets `GIT_NO_LAZY_FETCH=1` on the PROCESS
    # (that is the guarantee), so this fixture strips it for the setup —
    # which is also the cheapest demonstration that the guard reaches every
    # child of this interpreter and not only the runner's own `_git()`.
    work = tmp_path / "work"
    setup_env = {name: value for name, value in os.environ.items()
                 if name != "GIT_NO_LAZY_FETCH"}
    done = subprocess.run(
        ["git", "clone", "-q", "--filter=blob:none",
         f"file://{origin}", str(work)], capture_output=True, text=True,
        check=False, env=setup_env)
    assert done.returncode == 0, done.stderr
    assert MODULE._git(work, "fetch", "-q", "--tags",
                       "origin").returncode == 0

    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.extract_pre_tree(pre_commit, work, tmp_path / "into",
                                "carve-0")
    assert caught.value.code == "equivalence-object-store-incomplete"
    assert "PARTIAL OR INCOMPLETE OBJECT STORE" in caught.value.detail
    assert f"fetch origin {pre_commit}" in caught.value.detail


def test_a_pathspec_failure_is_named_post_shed_and_not_an_object_store(
        tmp_path):
    """`git archive` fails BEFORE writing anything when no path matches, so a
    tree carrying neither archive path never reaches the per-row check and
    must be diagnosed here. It is a POST-SHED REF, and the remedy is another
    `--pre-ref` — not the fetch the object-store branch prescribes (Copilot,
    PR #1115: the fallback still called this the object store and told the
    operator to fetch before changing the ref, which is backwards)."""
    repo = tmp_path / "repo"
    _seed(repo)
    commit = MODULE._git(repo, "rev-parse", "HEAD").stdout.strip()
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.extract_pre_tree(commit, repo, tmp_path / "into", "HEAD")
    detail = caught.value.detail
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert "OBJECT STORE" not in detail, detail
    assert "fetch origin" not in detail, detail
    assert "post-shed" in detail
    assert MODULE.DEFAULT_PRE_REF in detail


def test_an_unclassified_archive_failure_claims_neither_diagnosis(
        monkeypatch, tmp_path):
    """The third condition — a permission error, a full disk, a git that
    broke in a way this file has not met — gets its stderr and both remedies
    as POSSIBILITIES. A confident wrong diagnosis is what the two classified
    branches exist to stop, so the fallback must not inherit one."""
    def broken(repo, *arguments, text=True):
        if arguments[0] == "archive":
            return subprocess.CompletedProcess(
                list(arguments), 128, b"",
                b"fatal: unable to create temporary file: No space left")
        return MODULE._git(repo, *arguments, text=text)

    monkeypatch.setattr(MODULE, "_git", broken)
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.extract_pre_tree("f" * 40, tmp_path, tmp_path / "into", "HEAD")
    detail = caught.value.detail
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert "No space left" in detail
    assert "cannot tell from that output" in detail
    assert "PARTIAL OR INCOMPLETE OBJECT STORE" not in detail


def test_the_sweep_sees_an_edit_that_status_reports_as_clean(tmp_path):
    """`assume-unchanged` and `skip-worktree` make git report an EDITED file
    as clean, so a leg carrying either can be edited with `status --porcelain`
    — the sweep's first spelling — answering nothing at all. A sweep that
    cannot see the state it asserts is not a sweep (Copilot, PR #1105 round
    6)."""
    leg = tmp_path / "leg"
    _seed(leg)
    assert MODULE._git(leg, "update-index", "--assume-unchanged",
                       "a.txt").returncode == 0
    (leg / "a.txt").write_text("edited behind the flag\n", encoding="utf-8")
    blind = MODULE._git(leg, "status", "--porcelain")
    assert blind.stdout.strip() == "", "git reported the edit after all"
    dirt = MODULE.worktree_dirt(leg)
    assert dirt, "the sweep saw nothing at all"
    assert any("a.txt" in row for row in dirt), dirt
    assert any(row[1] == "!" for row in dirt), dirt
    advice = MODULE._clean_advice(dirt, leg)
    assert "--no-assume-unchanged" in advice


def test_the_sweep_does_not_refuse_on_what_the_leg_itself_ignores(tmp_path):
    """The measured reason `--ignored` was rejected: this runner's OWN
    imports write `__pycache__` into the legs (3 and 4 entries, measured), so
    a sweep counting ignored files refuses on every run after the first."""
    leg = tmp_path / "leg"
    _seed(leg)
    (leg / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    assert MODULE._git(leg, "add", ".gitignore").returncode == 0
    assert MODULE._git(leg, "commit", "-qm", "ignore").returncode == 0
    (leg / "__pycache__").mkdir()
    (leg / "__pycache__" / "x.pyc").write_bytes(b"\x00")
    ignored = MODULE._git(leg, "status", "--porcelain", "--ignored")
    assert "__pycache__" in ignored.stdout, "the premise of this test"
    assert MODULE.worktree_dirt(leg) == []


def test_an_ignored_python_file_under_src_is_dirt_and_bytecode_is_not(
        tmp_path):
    """`--exclude-standard` drops EVERY ignored path, and an ignored `.py`
    under `src` is still perfectly importable — it can shadow a module or be
    imported outright — so excluding the whole class let a leg render bytes
    that are in no commit while the verdict named one (Copilot, PR #1115).
    The allowlist is exactly the bytecode this runner's own imports create:
    measured, the two code legs carry 45 and 21 ignored files under `src`
    and every one of them is a `__pycache__` `.pyc`."""
    leg = tmp_path / "leg"
    _seed(leg)
    (leg / "src").mkdir()
    (leg / "src" / "m.py").write_text("x = 1\n", encoding="utf-8")
    (leg / ".gitignore").write_text("__pycache__/\n*.pyc\nlocal_*.py\n",
                                    encoding="utf-8")
    assert MODULE._git(leg, "add", "src/m.py", ".gitignore").returncode == 0
    assert MODULE._git(leg, "commit", "-qm", "src").returncode == 0
    (leg / "src" / "__pycache__").mkdir()
    (leg / "src" / "__pycache__" / "m.cpython-312.pyc").write_bytes(b"\x00")
    assert MODULE.worktree_dirt(leg) == [], "the runner's own bytecode is dirt"

    (leg / "src" / "local_override.py").write_text("x = 2\n",
                                                   encoding="utf-8")
    blind = MODULE._git(leg, "status", "--porcelain")
    assert blind.stdout.strip() == "", "git reported the ignored file"
    dirt = MODULE.worktree_dirt(leg)
    assert dirt, "the ignored file was not reported at all"
    assert any(row.startswith("!!") for row in dirt), dirt
    assert any("local_override" in row for row in dirt), dirt
    advice = MODULE._clean_advice(dirt, leg)
    assert "clean -fdX" in advice


def test_a_sourceless_pyc_beside_the_modules_is_not_allowlisted(tmp_path):
    """The allowlist is `__pycache__/<name>.pyc` and NOT every `.pyc`: a
    sourceless `src/foo.pyc`, sitting where `foo.py` would sit, is an
    ordinary import candidate, so allowlisting the extension anywhere would
    have admitted a module this runner did not check (Copilot, PR #1115;
    SonarCloud `python:S5850` on the same unparenthesised alternation, which
    is what that rule usually means)."""
    leg = tmp_path / "leg"
    _seed(leg)
    (leg / "src").mkdir()
    (leg / "src" / "m.py").write_text("x = 1\n", encoding="utf-8")
    (leg / ".gitignore").write_text("*.pyc\n__pycache__/\n", encoding="utf-8")
    assert MODULE._git(leg, "add", "src/m.py", ".gitignore").returncode == 0
    assert MODULE._git(leg, "commit", "-qm", "src").returncode == 0
    (leg / "src" / "__pycache__").mkdir()
    (leg / "src" / "__pycache__" / "m.cpython-312.pyc").write_bytes(b"\x00")
    assert MODULE.worktree_dirt(leg) == []
    (leg / "src" / "shadow.pyc").write_bytes(b"\x00")
    dirt = MODULE.worktree_dirt(leg)
    assert any("shadow.pyc" in row for row in dirt), dirt


def test_the_refusal_names_which_archive_path_the_tree_lacks(tmp_path):
    """`git archive` fails as soon as ONE pathspec matches nothing, so a
    refusal that said the tree carried NEITHER path was inaccurate for a tree
    that had shed one of them (Copilot, PR #1115)."""
    repo = tmp_path / "repo"
    _seed(repo)
    kept, shed = MODULE.ARCHIVE_PATHS
    (repo / kept).mkdir(parents=True)
    (repo / kept / "generator.py").write_text("x = 1\n", encoding="utf-8")
    assert MODULE._git(repo, "add", "-A").returncode == 0
    assert MODULE._git(repo, "commit", "-qm", "half").returncode == 0
    commit = MODULE._git(repo, "rev-parse", "HEAD").stdout.strip()
    with pytest.raises(MODULE.EquivalenceRefusal) as caught:
        MODULE.extract_pre_tree(commit, repo, tmp_path / "into", "HEAD")
    detail = caught.value.detail
    assert caught.value.code == "equivalence-pre-tree-unrenderable"
    assert f"carries {kept} but NOT {shed}" in detail, detail
    assert "NEITHER" not in detail


def test_the_hidden_flag_remedy_restores_the_edit_it_reveals(tmp_path):
    """Clearing the flag is HALF the remedy: the edit it was hiding then
    shows up as an ordinary modification and the promised re-run refuses a
    second time (Copilot, PR #1115)."""
    advice = MODULE._clean_advice(["h! src/m.py"], tmp_path / "leg")
    assert "--no-assume-unchanged" in advice
    assert "checkout --" in advice or "stash" in advice
    assert "reveals the edit rather than removing it" in advice


def test_the_no_network_guard_reaches_the_shared_reader(monkeypatch):
    """This file's `_git()` is not the whole measurement.
    `carved_reach._git_run()` is a SHARED reader with its own sanitizer, and
    that sanitizer builds from `os.environ` minus a scrub list which does not
    carry this name — so a manifest or tree read on the POST side could still
    lazy-fetch from a promisor remote in a partial clone, in the half of the
    run this file does not issue the git commands for (Copilot, PR #1115)."""
    import carved_reach
    monkeypatch.delenv("GIT_NO_LAZY_FETCH", raising=False)
    assert "GIT_NO_LAZY_FETCH" not in carved_reach._sanitized_git_environment()
    MODULE.post_stack(register_profile=False)
    assert os.environ["GIT_NO_LAZY_FETCH"] == "1"
    assert carved_reach._sanitized_git_environment()[
        "GIT_NO_LAZY_FETCH"] == "1"
    assert "GIT_NO_LAZY_FETCH" not in carved_reach._SCRUBBED_GIT_ENVIRONMENT


def test_the_sweep_reads_the_import_surface_and_the_untracked_files(tmp_path):
    """The two halves that do carry: a tracked edit under `src`, and an
    untracked file that is not ignored."""
    leg = tmp_path / "leg"
    _seed(leg)
    (leg / "src").mkdir()
    (leg / "src" / "m.py").write_text("x = 1\n", encoding="utf-8")
    assert MODULE._git(leg, "add", "src/m.py").returncode == 0
    assert MODULE._git(leg, "commit", "-qm", "src").returncode == 0
    assert MODULE.worktree_dirt(leg) == []
    (leg / "src" / "m.py").write_text("x = 2\n", encoding="utf-8")
    (leg / "src" / "stray.py").write_text("", encoding="utf-8")
    dirt = MODULE.worktree_dirt(leg)
    assert any(row.startswith(" M") and "m.py" in row for row in dirt), dirt
    assert any(row.startswith("??") and "stray.py" in row
               for row in dirt), dirt


def test_the_legs_are_probed_before_the_stack_is_composed(monkeypatch,
                                                          capsys):
    """Composing the stack installs a meta-path finder, mutates the import
    system for the rest of the process, and writes `__pycache__` INTO the leg
    whose cleanliness the next check asserts. Doing all that to discover a
    submodule directory is empty is work with side effects performed to reach
    a worse message (Copilot, PR #1105 round 6)."""
    def composed(*args, **kwargs):
        raise AssertionError("the stack was composed before the probe")

    monkeypatch.setattr(MODULE, "post_stack", composed)
    monkeypatch.setattr(MODULE, "unmaterialized_legs",
                        lambda: ["/nowhere/openDox/code — no such directory"])
    assert MODULE.main([]) == 2
    rendered = capsys.readouterr().err
    assert "equivalence-reach-unavailable" in rendered
    assert "not materialized" in rendered
    assert "git submodule update" in rendered


def test_the_materialization_probe_names_each_shape_it_finds(monkeypatch,
                                                             tmp_path):
    """Three states, and they are different remedies: a mount that is not
    there, one that is an empty directory (recorded and never initialized —
    a clone without `--recurse-submodules`), and one with no `.git` at all (a
    copied source tree, for which no pin can be verified)."""
    monkeypatch.setattr(MODULE, "ROOT", tmp_path)
    for parent_rel, path in MODULE.LEG_GITLINKS:
        (tmp_path / parent_rel / path).mkdir(parents=True, exist_ok=True)
        (tmp_path / parent_rel / path / ".git").write_text("gitdir: x\n",
                                                           encoding="utf-8")
    assert MODULE.unmaterialized_legs() == []
    shutil.rmtree(tmp_path / "openDox" / "code")
    copied = tmp_path / "openXdox" / "code"
    (copied / "src").mkdir()
    (copied / ".git").unlink()
    for child in (tmp_path / "openDox" / "spec").iterdir():
        child.unlink()
    absent = "\n".join(MODULE.unmaterialized_legs())
    assert "no such directory" in absent
    assert "EMPTY directory" in absent
    assert "no `.git`" in absent


def test_the_evidence_carries_the_unpinned_half_of_the_composition(shipped):
    """The post side is composed out of ROOT's `carved_reach.py`,
    `opendox_host.py` and the § 4.4 profile — none of them pinned by the
    gitlinks the verdict names — so two runs can differ by them alone while
    every pinned leg matches. Carried, never refused on: this is the tree the
    runner is EDITED in (Copilot, PR #1105 round 4)."""
    assert len(shipped["root_revision"]) == 40, shipped["root_revision"]
    assert shipped["root_worktree"] in ("clean", "dirty")
    assert isinstance(shipped["root_worktree_entries"], int)
    rendered = _run().stdout
    assert "composed in" in rendered
    assert shipped["root_revision"][:12] in rendered


def test_an_unreadable_root_status_is_unknown_and_not_clean(monkeypatch):
    """`carved_reach`'s rule, held for the evidence too: a read that failed
    learned nothing, and "clean" is a claim."""
    monkeypatch.setattr(MODULE, "_git", lambda *a, **k: None)
    state = MODULE.superproject_state()
    assert state["root_revision"] == "unknown"
    assert state["root_worktree"] == "unknown"
    assert state["root_worktree_entries"] is None


def test_the_pre_child_is_given_its_inputs_by_name_not_by_position(
        monkeypatch, tmp_path):
    """argv is the one channel where a value's POSITION decides how it is
    read: the program goes to `-c`, so everything after it is `sys.argv[1:]`
    and a mis-ordered or empty element silently shifts the unpack — the
    corpus becoming the output path. Environment entries are read BY NAME,
    and a missing name raises `KeyError` in the child rather than rendering
    something else (Copilot, PR #1105 round 10; SonarCloud
    `pythonsecurity:S8705`)."""
    seen = {}

    def spy(argv, **kwargs):
        seen["argv"] = argv
        seen["env"] = kwargs.get("env")
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(MODULE.subprocess, "run", spy)
    MODULE._run_pre_child(tmp_path / "tree", tmp_path / "corpus",
                          tmp_path / "out.json", "d" * 40)
    assert seen["argv"][-1] == MODULE._PRE_RENDER_PROGRAM, (
        "something still trails the program in argv")
    assert seen["argv"][1:3] == ["-I", "-c"]
    assert seen["env"]["EQUIVALENCE_CORPUS"] == str(tmp_path / "corpus")
    assert seen["env"]["EQUIVALENCE_OUT"] == str(tmp_path / "out.json")
    assert seen["env"]["EQUIVALENCE_REVISION"] == "d" * 40
    assert "PATH" in seen["env"], "the ambient environment was sterilised"


def test_the_pre_render_program_reads_no_argv():
    """…and the child's own half of that: it reads six names, not a tuple."""
    program = MODULE._PRE_RENDER_PROGRAM
    assert "sys.argv" not in program
    for name in ("SCRIPTS", "CORPUS", "OUT", "REVISION", "DATE",
                 "REPOSITORY"):
        assert f'os.environ["EQUIVALENCE_{name}"]' in program


def test_the_refusal_vocabulary_is_exactly_the_ratified_one():
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES


def test_a_code_outside_the_vocabulary_cannot_be_raised_at_all():
    """The vocabulary is ENFORCED and not merely declared — the stronger
    guarantee `verify-carve-conformance.py` took after Copilot found that
    pinning the constant catches a rename of the CONSTANT and not a raise site
    that invented a code the tuple never held."""
    with pytest.raises(ValueError) as caught:
        MODULE.EquivalenceRefusal("equivalence-invented", "no such code")
    assert "ratified refusal codes" in str(caught.value)
    for code in RATIFIED_CODES:
        assert MODULE.EquivalenceRefusal(code, "d").code == code


def test_every_refusal_code_appears_in_the_script_source():
    """A code declared and never raised is a promise the script does not
    keep."""
    source = SCRIPT.read_text(encoding="utf-8")
    for code in RATIFIED_CODES:
        assert source.count(f'"{code}"') >= 2, (
            f"{code} appears once — declared in the tuple and raised nowhere")


def test_the_exit_status_is_only_ever_zero_or_two():
    """Enforced at the one place that owns it, so the contract does not rest
    on a reader auditing every raise site."""
    for args in ((), ("--pre-ref", "HEAD"), ("--pre-ref", "not-a-ref"),
                 ("--no-register-profile",),
                 ("--corpus", "/dev/null"),
                 ("--json", "--pre-ref", "not-a-ref")):
        done = _run(*args)
        assert done.returncode in (0, 2), (
            f"{args} exited {done.returncode}; this runner has no exit 1")


def test_an_unexpected_failure_arrives_as_a_named_refusal_not_a_traceback(
        monkeypatch, capsys):
    """The blanket `except Exception`, exercised rather than read."""
    def explode(*args, **kwargs):
        raise MemoryError("boom")
    monkeypatch.setattr(MODULE, "render_post", explode)
    code = MODULE.main([])
    assert code == 2
    rendered = capsys.readouterr().err
    assert "equivalence-unreadable" in rendered
    assert "MemoryError: boom" in rendered
    assert "Traceback" not in rendered


def test_a_watchdog_that_escapes_render_post_still_holds_the_exit_contract(
        monkeypatch, capsys):
    """`_RenderTimeout` is a `BaseException` now, and `main()`'s blanket
    guard is `Exception` ON PURPOSE, so a timeout landing in the sliver
    between the guarded render and `disarm()` would leave a traceback and
    EXIT 1 — a status this file's docstring says does not exist."""
    def late(*args, **kwargs):
        raise MODULE._RenderTimeout(0.05)

    monkeypatch.setattr(MODULE, "render_post", late)
    code = MODULE.main([])
    assert code == 2
    rendered = capsys.readouterr().err
    assert "equivalence-post-stack-unrenderable" in rendered
    assert "Traceback" not in rendered


def test_the_source_revision_is_pinned_on_both_sides_and_is_load_bearing(
        shipped):
    """§ 3.2's hazard, asserted from both ends.

    LOAD-BEARING: moving the anchor moves the digest, so it is a projected
    field and not decoration. ON BOTH SIDES: the two still agree at the moved
    anchor, which is what proves the injection reaches the archived tree as
    well as the pinned stack. Unpinned — the state this exists to prevent —
    the post side reads the checkout's HEAD through `RealGit` and the pre
    side, an archive rather than a repository, reads `unknown`.
    """
    assert MODULE.PINNED_SOURCE_REVISION == "abcd1234" * 5
    moved = _json_run("--source-revision", "deadbeef" * 5)
    assert moved["result"] == "ok"
    assert moved["states"][0]["equivalent"] is True
    assert moved["states"][0]["pre_sha256"] != \
        shipped["states"][0]["pre_sha256"]


def test_the_injected_git_carries_the_runs_own_anchor(monkeypatch):
    """The injected git and the explicit `source_revision` are the SAME anchor,
    and TODAY NOTHING ELSE WOULD NOTICE IF THEY WERE NOT.

    Measured at the pinned leg with a recording git: given an explicit
    `source_revision`, `generate_snapshot` calls `commit_date(corpus,
    revision)` exactly once and NEVER `head_sha`, so a `FakeGit` built with
    the class default rather than with the run's revision is indistinguishable
    in the rendered bytes. That is precisely why it is asserted here rather
    than left to the digests: the day any field is derived from HEAD again — it
    was, before the explicit argument existed — a runner whose injected git
    disagreed with its own argument would report a difference that is about
    the runner and not about the projection.
    """
    built: list[str] = []

    class Recording(MODULE.FakeGit):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            built.append(self.head_sha(None))

    monkeypatch.setattr(MODULE, "FakeGit", Recording)
    moved = "deadbeef" * 5
    MODULE.render_post(MODULE.post_stack(), BASE_REPO, moved)
    assert built == [moved], (
        f"render_post injected a git anchored at {built} and rendered at "
        f"{moved}; the two must be one anchor")


def test_this_suite_never_skips():
    """`pytest-suite.yml` pins `EXPECT_SKIPPED` as an EXACT sum and says in
    terms why: a directory that silently turns into skips is "a green bar,
    indistinguishable from a pass". This suite has no conditional it could
    stand down on — the tag is reachable at `fetch-depth: 0` and the gate
    initialises both legs recursively — so the absence is asserted rather
    than intended.

    The forbidden spellings are BUILT rather than written, so that asserting
    them does not put them in the file being scanned.
    """
    forbidden = ("pytest" + ".skip", "pytest" + ".xfail", "skip" + "if",
                 "importor" + "skip",
                 # THE MARKER FORMS, AND THEY ARE A DIFFERENT SPELLING: a
                 # decorator written as the marker attribute contains none of
                 # the four bare forms above as a substring, so a set without
                 # these two would stay green while the workflow's exact skip
                 # count moved (Copilot, PR #1105). Every entry is BUILT for
                 # the reason the docstring gives, and no comment here may
                 # write one out either — this test scans its own file, and a
                 # comment quoting a forbidden spelling fails it (measured).
                 "mark" + ".skip", "mark" + ".xfail",
                 # AND THE `unittest` SPELLINGS, which this repository does
                 # use — `tests/proposal-support/test_proposal_support.py`
                 # carries a `skipUnless` (Copilot, PR #1105 round 9). The
                 # prefix covers `skip`, `skipIf` and `skipUnless` in one
                 # entry, and none of the bare forms above matches any of
                 # them.
                 "unittest" + ".skip")
    source = Path(__file__).read_text(encoding="utf-8")
    for spelling in forbidden:
        assert spelling not in source, (
            f"this suite spells {spelling!r}; EXPECT_SKIPPED is an exact sum "
            "and a conditional here would move it silently")
