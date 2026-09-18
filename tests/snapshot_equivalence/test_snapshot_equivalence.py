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
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify-snapshot-equivalence.py"
BASE_REPO = REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures" / "base-repo"

#: The vocabulary, restated as a LITERAL rather than imported. Asserting
#: `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology;
#: spelling it out is what makes a silent rename or reorder a test failure,
#: because an operator's runbook and a caller's branch both read these strings.
#:
#: FIVE NAMED KINDS AND ONE BLANKET, which is `verify-carve-conformance.py`'s
#: own shape (four named, `conformance-unreadable` blanket): the exit contract
#: is held by a `except Exception` that must render SOMETHING, and giving it
#: one of the five named codes would make the runner lie about the cause.
RATIFIED_CODES = (
    "equivalence-pre-ref-unreachable",
    "equivalence-pre-tree-unrenderable",
    "equivalence-reach-unavailable",
    "equivalence-profile-unregistered",
    "equivalence-digests-differ",
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
    done = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--verify",
         f"{CARVE_TAG}^{{commit}}"],
        capture_output=True, text=True, check=False)
    assert done.returncode == 0, (
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
                 "importor" + "skip")
    source = Path(__file__).read_text(encoding="utf-8")
    for spelling in forbidden:
        assert spelling not in source, (
            f"this suite spells {spelling!r}; EXPECT_SKIPPED is an exact sum "
            "and a conditional here would move it silently")
