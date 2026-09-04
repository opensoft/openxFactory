"""The PARENT SEAL — the bounded source artifact the credential-free child
consumes (openxFactory `add-nightly-dashboard-refresh`, re-realization S2).

What each block here pins.

  * THE SEAL SET IS NOT THE DECISION SET. `snapshot.find_validator` walks UP
    for `openxFactory/scripts/validate-ideation-dashboard-contracts.py`, a
    TOP-LEVEL `scripts/*.py` that `CORPUS_BAKED_PATHS` does not name; the
    sparse-cone checkout the pre-seal child used carried it only as a side
    effect of cone mode. So the seal set adds it and the DECISION set must not
    follow, or `_same_scope` fires `REASON_SCOPE_CHANGED` against every
    recorded pin. Both halves are asserted, and the layout is proven by
    running the real `find_validator` over a real sealed tree rather than by
    restating the path.
  * THE REVISION IS PROVEN, NOT ASSERTED. `git archive` records the commit it
    was made from in a global extended pax header; the seal refuses unless
    that header equals the `source_head` it is about to record. After this
    change the child's own one-revision check reads two fields of one manifest
    and is tautological alone, so the parent holds the end that still touches
    a repository.
  * THE DIGEST RULE TRAVELS WITH THE ARTIFACT. `tree_digest` is recomputed here
    from the rule `TREE_DIGEST_SPEC` states, by an INDEPENDENT implementation,
    so the manifest's stated rule is provably the implemented one — that is
    what makes the child's (S3) recomputation authorable from the manifest.
  * EVERY REFUSAL LEAVES NO MANIFEST. A seal the parent could not stand behind
    must not be downloadable, so the refusal paths assert the absence of
    `manifest.json` and not merely a raised exception.
  * NOTHING HERE BUILDS OR PUSHES. `git` is the only binary the seal speaks;
    the tests assert that over the recorded argv, and `gh` is unreachable by
    the suite's own hermeticity guard (the recipe read is injected).

No network: the corpus is a real `git init` under `tmp_path` (git is not a
guarded binary — `nlm`/`gh`/`omp` are), and the recipe read is always injected.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path

import pytest

from ideation_dashboard import dashboard_refresh_lane as lane
from ideation_dashboard import snapshot as snapshot_mod
from ideation_dashboard.generator import is_rfc3339_datetime

CORRELATION = "dashboard-refresh-4242-1"
COMMITTED_AT = "2026-09-04T01:02:03+00:00"


def _instant(value: str) -> datetime:
    """The INSTANT a stamp denotes, not its spelling.

    `git show -s --format=%cI` renders a ZERO offset as `+00:00` on some git
    versions and as `Z` on others (measured: `+00:00` on git 2.43 locally,
    `Z` on the Actions runner), and the manifest records whatever git said
    VERBATIM — deliberately, because `--generated-at` is "recorded in the
    snapshot EXACTLY as given … never normalised". Both spellings are RFC 3339
    and both are accepted by `generator.is_rfc3339_datetime`, which is the
    property that matters; pinning one spelling would pin a git version."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
RECIPE_REV = "c" * 40
RECIPE_TEXT = "FROM python:3.12-slim\nCOPY openxFactory/docs /srv/source/docs\n"


# ---------------------------------------------------------------------------
# helpers — a real, tiny corpus repository, and a stub recipe read
# ---------------------------------------------------------------------------

def _git(repo: Path, *argv: str) -> str:
    """Real git, in a real temp repository — hermetic (no remote is ever named)
    and NEVER a skip: the suite pins its skip count exactly, so a git that
    would not run has to fail loudly here rather than turn this file into
    twenty silent skips that red the gate with the wrong reason.

    The committer date is FIXED so the `source_committed_at` assertions can
    name the value the child will pass to `--generated-at`, and the config
    files are neutralised so the developer's own git config cannot change it.
    """
    env = dict(os.environ, **{
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_AUTHOR_DATE": COMMITTED_AT, "GIT_COMMITTER_DATE": COMMITTED_AT})
    proc = subprocess.run(["git", "-C", str(repo), *argv],
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 0, \
        f"git {' '.join(argv)} failed: {proc.stderr.strip()[:400]}"
    return proc.stdout.strip()


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    """A corpus checkout holding every seal path the real one does, one file
    deep — including the top-level validator the trap is about."""
    repo = tmp_path / "openxFactory-src"
    repo.mkdir()
    _git(repo, "init", "--quiet", "-b", "main")
    for relpath in lane.CORPUS_SEAL_PATHS:
        target = repo / relpath
        if relpath.endswith(".py"):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("#!/usr/bin/env python3\nprint('ok')\n",
                              encoding="utf-8")
        else:
            target.mkdir(parents=True, exist_ok=True)
            (target / "a.md").write_text(f"# {relpath}\n", encoding="utf-8")
    # A path OUTSIDE the seal set, to prove the seal is bounded.
    (repo / "experiments").mkdir()
    (repo / "experiments" / "huge.bin").write_text("x" * 1024, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "corpus")
    return repo


def _decision(corpus_revision: str, **kw) -> dict:
    payload = {"build": True, "outcome": "build",
               "reason": lane.REASON_CORPUS_MOVED,
               "corpus_revision": corpus_revision,
               "recipe_revision": RECIPE_REV}
    payload.update(kw)
    return payload


def _seal(corpus: Path, seal_dir: Path, *, decision: dict | None = None,
          recipe: str | None = RECIPE_TEXT, **kw) -> dict:
    head = _git(corpus, "rev-parse", "HEAD")
    return lane.seal_source(
        corpus_checkout=corpus, seal_dir=seal_dir,
        correlation_id=kw.pop("correlation_id", CORRELATION),
        decision=decision if decision is not None else _decision(head),
        corpus_ref=kw.pop("corpus_ref", "HEAD"),
        read_recipe=(lambda: recipe),
        **kw)


class RecordingRunner:
    """Wraps the real runner and records every argv, so "the seal speaks git
    and nothing else" is asserted on the calls rather than on the source."""

    def __init__(self, inner=lane.subprocess_runner) -> None:
        self.inner = inner
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, argv, **kw):
        self.calls.append(tuple(str(a) for a in argv))
        return self.inner(argv, **kw)


# ---------------------------------------------------------------------------
# the seal set, and the trap PR #179 already paid for once
# ---------------------------------------------------------------------------

def test_the_seal_set_is_the_baked_set_plus_the_validator_and_nothing_else():
    added = set(lane.CORPUS_SEAL_PATHS) - set(lane.CORPUS_BAKED_PATHS)
    assert added == {lane.VALIDATOR_SEAL_PATH}
    assert set(lane.CORPUS_BAKED_PATHS) <= set(lane.CORPUS_SEAL_PATHS)
    # Sorted, like the baked tuple, because both are written into records that
    # compare scope for equality and two spellings would read as a change.
    assert list(lane.CORPUS_SEAL_PATHS) == sorted(lane.CORPUS_SEAL_PATHS)


def test_the_decision_scope_does_not_follow_the_seal_scope():
    """Widening `CORPUS_BAKED_PATHS` to the seal set would make `_same_scope`
    fire `REASON_SCOPE_CHANGED` against every recorded pin and force exactly
    one rebuild for nothing (design open question 7). So the decision scope is
    pinned to the baked set here, and the two are proven to differ."""
    assert lane.VALIDATOR_SEAL_PATH not in lane.CORPUS_BAKED_PATHS
    assert lane.CORPUS_BAKED_PATHS == (
        "contracts", "docs", "examples", "ideation", "openspec",
        "scripts/doc_health", "scripts/ideation_dashboard", "templates")
    recorded = lane.Provenance(
        corpus_repo=lane.DEFAULT_CORPUS_REPO, corpus_revision="a" * 40,
        corpus_scope=lane.CORPUS_BAKED_PATHS,
        recipe_repo=lane.DEFAULT_RECIPE_REPO, recipe_revision="b" * 40,
        recipe_scope=lane.RECIPE_BAKED_PATHS)
    unchanged = lane.decide_refresh(corpus_revision="a" * 40,
                                   recipe_revision="b" * 40, recorded=recorded)
    assert unchanged.reason == lane.REASON_UNCHANGED
    widened = lane.decide_refresh(corpus_revision="a" * 40,
                                  recipe_revision="b" * 40, recorded=recorded,
                                  corpus_scope=lane.CORPUS_SEAL_PATHS)
    assert widened.reason == lane.REASON_SCOPE_CHANGED    # the cost, measured


def test_the_sealed_layout_is_the_one_find_validator_walks_up_to(corpus, tmp_path):
    """Proven by running the REAL locator over a REAL sealed tree, from the
    directory the child hands `--repo-root`, rather than by restating a path:
    that walk is what PR #179 broke, and a path assertion would not have
    caught it."""
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    found = snapshot_mod.find_validator(seal / lane.SEAL_CORPUS_RELPATH)
    assert found is not None
    assert found == seal / lane.SEAL_CORPUS_RELPATH / lane.VALIDATOR_SEAL_PATH
    # And with the validator removed the locator finds nothing — i.e. the file
    # is load-bearing rather than incidental.
    found.unlink()
    assert snapshot_mod.find_validator(seal / lane.SEAL_CORPUS_RELPATH) is None


def test_a_seal_missing_the_validator_is_refused_at_the_seal(corpus, tmp_path):
    """Refused HERE, not three steps later at `--strict`: a validation that
    could not RUN is a strict failure with no finding to read, and the operator
    would be looking for a corpus defect that does not exist."""
    with pytest.raises(lane.SealRefused, match="validator would be unreachable"):
        _seal(corpus, tmp_path / "seal",
              seal_paths=tuple(lane.CORPUS_BAKED_PATHS))
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_seal_is_bounded_to_the_seal_paths(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert not (seal / lane.SEAL_CORPUS_RELPATH / "experiments").exists()
    prefixes = {relpath.split("/", 1)[0] for relpath in manifest["files"]}
    assert prefixes == {lane.SEAL_CORPUS_RELPATH, "recipe"}


# ---------------------------------------------------------------------------
# the manifest
# ---------------------------------------------------------------------------

def test_the_manifest_carries_every_field_the_child_reads(corpus, tmp_path):
    seal = tmp_path / "seal"
    head = _git(corpus, "rev-parse", "HEAD")
    manifest = _seal(corpus, seal)
    on_disk = json.loads((seal / lane.SEAL_MANIFEST_NAME).read_text(encoding="utf-8"))
    assert on_disk == manifest                      # written, not just returned
    assert manifest["schema_version"] == lane.SEAL_SCHEMA_VERSION
    assert manifest["kind"] == lane.SEAL_MANIFEST_KIND
    assert manifest["artifact_name"] == f"dashboard-image-source-{CORRELATION}"
    assert manifest["correlation_id"] == CORRELATION
    assert manifest["source_repo"] == lane.DEFAULT_CORPUS_REPO
    assert manifest["source_head"] == head
    assert manifest["corpus_revision"] == head
    assert manifest["corpus_baked_paths"] == list(lane.CORPUS_BAKED_PATHS)
    assert manifest["seal_paths"] == list(lane.CORPUS_SEAL_PATHS)
    assert manifest["recipe_repo"] == lane.DEFAULT_RECIPE_REPO
    assert manifest["recipe_revision"] == RECIPE_REV
    assert manifest["recipe_path"] == lane.RECIPE_DOCKERFILE_PATH
    assert manifest["recipe_relpath"] == lane.SEAL_RECIPE_RELPATH
    assert manifest["corpus_relpath"] == lane.SEAL_CORPUS_RELPATH
    assert manifest["digest_algorithm"] == "sha256"
    assert manifest["decision"]["reason"] == lane.REASON_CORPUS_MOVED
    assert (seal / manifest["recipe_relpath"]).read_text(encoding="utf-8") \
        == RECIPE_TEXT
    # The measurement open question 2 asks for, recorded on every seal rather
    # than reconstructed from a run log.
    assert manifest["file_count"] == len(manifest["files"]) > 0
    assert manifest["total_bytes"] > 0


def test_the_manifest_names_the_field_that_feeds_generated_at(corpus, tmp_path):
    """`--generated-at` must receive the SOURCE COMMIT's committer date, never
    a wall clock: `generation.generated_at` is defined as that date and the
    snapshot render is canonical precisely because nothing in it reads the
    clock. So the manifest names the field, and the parent's own wall clock
    lives under a different name that the named field is proven not to be."""
    manifest = _seal(corpus, tmp_path / "seal")
    assert manifest["generated_at_field"] == "source_committed_at"
    stamp = manifest[manifest["generated_at_field"]]
    assert is_rfc3339_datetime(stamp)               # the flag will accept it
    assert _instant(stamp) == _instant(COMMITTED_AT)   # the commit's own date
    assert manifest["sealed_at"] != stamp
    assert manifest["generated_at_field"] != "sealed_at"


def test_the_manifest_is_not_in_its_own_index(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert lane.SEAL_MANIFEST_NAME not in manifest["files"]
    assert all(not key.startswith("/") for key in manifest["files"])


# ---------------------------------------------------------------------------
# the tree digest — the rule the child (S3) recomputes
# ---------------------------------------------------------------------------

def _independent_tree_digest(seal: Path) -> str:
    """The rule `TREE_DIGEST_SPEC` states, implemented from the prose rather
    than by calling the module — which is what makes the spec, and therefore
    the child's implementation, verifiable."""
    lines = []
    for path in sorted(seal.rglob("*"), key=lambda p: p.as_posix()):
        if not path.is_file():
            continue
        relpath = path.relative_to(seal).as_posix()
        if relpath == "manifest.json":
            continue
        lines.append((relpath.encode("utf-8"),
                      hashlib.sha256(path.read_bytes()).hexdigest()))
    body = b"".join(f"{digest}  ".encode("ascii") + relpath + b"\n"
                    for relpath, digest in sorted(lines))
    return hashlib.sha256(body).hexdigest()


def test_the_tree_digest_is_the_rule_the_manifest_states(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert manifest["tree_digest"] == _independent_tree_digest(seal)
    assert "sha256" in manifest["tree_digest_spec"]
    assert "manifest.json" in manifest["tree_digest_spec"]


def test_the_tree_digest_is_order_independent_and_content_sensitive():
    index = {"b.txt": "b" * 64, "a.txt": "a" * 64, "d/c.txt": "c" * 64}
    reordered = {key: index[key] for key in reversed(list(index))}
    assert lane.tree_digest(index) == lane.tree_digest(reordered)
    moved = dict(index, **{"a.txt": "0" * 64})
    assert lane.tree_digest(moved) != lane.tree_digest(index)
    renamed = {("z.txt" if key == "a.txt" else key): value
               for key, value in index.items()}
    assert lane.tree_digest(renamed) != lane.tree_digest(index)


def test_the_tree_digest_of_one_revision_is_stable_across_two_seals(corpus, tmp_path):
    first = _seal(corpus, tmp_path / "one")
    second = _seal(corpus, tmp_path / "two")
    assert first["tree_digest"] == second["tree_digest"]
    assert first["files"] == second["files"]
    assert first["source_head"] == second["source_head"]


# ---------------------------------------------------------------------------
# the parent-side one-revision assertion (design open question 1)
# ---------------------------------------------------------------------------

def test_git_records_the_archive_revision_and_the_seal_reads_it_back(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")
    archive = tmp_path / "probe.tar"
    _git(corpus, "archive", "--format=tar", f"--output={archive}", head, "--",
         *lane.CORPUS_SEAL_PATHS)
    assert lane.git_archive_revision(archive) == head


def test_an_archive_naming_another_revision_is_refused(corpus, tmp_path, monkeypatch):
    """The whole point of the parent-side assertion: a seal whose bytes came
    from a commit other than the one the manifest would record must not exist,
    because nothing downstream could ever disprove the manifest."""
    other = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "git_archive_revision", lambda _path: "f" * 40)
    with pytest.raises(lane.SealRefused, match="recorded revision"):
        _seal(corpus, tmp_path / "seal", decision=_decision(other))
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_an_archive_with_no_recorded_revision_is_refused(corpus, tmp_path, monkeypatch):
    monkeypatch.setattr(lane, "git_archive_revision", lambda _path: None)
    with pytest.raises(lane.SealRefused, match="absent"):
        _seal(corpus, tmp_path / "seal")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("name, match", [
    ("/etc/cron.d/evil", "absolute member path"),
    ("../../etc/cron.d/evil", "traversing member path"),
    ("docs/../../escape.txt", "traversing member path"),
])
def test_a_member_path_that_could_escape_the_seal_is_refused(tmp_path, name, match):
    """Checked on the NAMES, before extraction, so it holds on BOTH extraction
    branches — the `data` filter would catch these on a modern interpreter, but
    the `TypeError` fallback for an interpreter without extraction filters
    would not, and "git produced the archive so its names are fine" is exactly
    the assumption an extraction hazard is made of (Copilot, PR #648)."""
    archive = tmp_path / "escape.tar"
    with tarfile.open(archive, "w") as handle:
        payload = b"pwned\n"
        member = tarfile.TarInfo(name)
        member.size = len(payload)
        handle.addfile(member, __import__("io").BytesIO(payload))
    with pytest.raises(lane.SealRefused, match=match):
        lane._extract_seal_archive(archive, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()


def test_a_non_regular_archive_entry_is_refused(tmp_path):
    archive = tmp_path / "linky.tar"
    with tarfile.open(archive, "w") as handle:
        member = tarfile.TarInfo("docs/elsewhere")
        member.type = tarfile.SYMTYPE
        member.linkname = "/etc/passwd"
        handle.addfile(member)
    with pytest.raises(lane.SealRefused, match="non-regular"):
        lane._extract_seal_archive(archive, tmp_path / "out")


# ---------------------------------------------------------------------------
# refusals — and every one of them leaves no manifest
# ---------------------------------------------------------------------------

def test_a_decision_that_asked_for_no_build_seals_nothing(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")
    for decision in ({"build": False, "outcome": "no_change",
                      "corpus_revision": head, "recipe_revision": RECIPE_REV},
                     {"outcome": "undecidable"},
                     {}):
        with pytest.raises(lane.SealRefused, match="nothing to seal"):
            _seal(corpus, tmp_path / "seal", decision=decision)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("bad", [
    {"corpus_revision": ""},
    {"corpus_revision": "abc1234"},           # abbreviated is not a full sha
    {"corpus_revision": "z" * 40},
    {"recipe_revision": None},
    {"recipe_revision": "HEAD"},
])
def test_a_malformed_decision_revision_is_refused(corpus, tmp_path, bad):
    decision = _decision(_git(corpus, "rev-parse", "HEAD"))
    decision.update(bad)
    with pytest.raises(lane.SealRefused, match="no usable"):
        _seal(corpus, tmp_path / "seal", decision=decision)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("bad", ["", "  ", "a/b", "a:b", 'a"b', "-leading",
                                 "x" * 121, "a\nb"])
def test_a_correlation_id_that_cannot_name_an_artifact_is_refused(bad):
    with pytest.raises(lane.SealRefused, match="cannot name an Actions artifact"):
        lane.seal_artifact_name(bad)


def test_the_correlation_id_is_canonicalized_once(corpus, tmp_path):
    """The artifact NAME and the manifest's `correlation_id` are compared
    against each other by the child, so a value with surrounding whitespace
    must be stripped for both or neither — otherwise the child refuses a
    perfectly good seal over a space (Copilot, PR #648)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, correlation_id=f"  {CORRELATION}\n")
    assert manifest["correlation_id"] == CORRELATION
    assert manifest["artifact_name"] == \
        f"{lane.SEAL_ARTIFACT_PREFIX}{manifest['correlation_id']}"
    assert lane.verify_seal(seal, correlation_id=CORRELATION) == []


def test_the_artifact_name_is_the_prefix_plus_the_correlation_id():
    assert lane.seal_artifact_name(CORRELATION) == \
        f"dashboard-image-source-{CORRELATION}"
    assert lane.SEAL_ARTIFACT_PREFIX == "dashboard-image-source-"


@pytest.mark.parametrize("recipe", [None, "", "   \n"])
def test_an_unreadable_recipe_is_refused(corpus, tmp_path, recipe):
    with pytest.raises(lane.SealRefused, match="could not read"):
        _seal(corpus, tmp_path / "seal", recipe=recipe)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_an_unresolvable_source_ref_is_refused(corpus, tmp_path):
    with pytest.raises(lane.SealRefused, match="could not resolve"):
        _seal(corpus, tmp_path / "seal", corpus_ref="origin/nope")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_failing_archive_is_refused_rather_than_half_sealed(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")

    def runner(argv, **kw):
        if "archive" in [str(a) for a in argv]:
            return lane.CommandResult(tuple(str(a) for a in argv), 128, "",
                                      "fatal: not a tree object")
        return lane.subprocess_runner(argv, **kw)

    with pytest.raises(lane.SealRefused, match="archive failed"):
        _seal(corpus, tmp_path / "seal", decision=_decision(head), runner=runner)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_intermediate_archive_is_never_part_of_the_artifact(corpus, tmp_path):
    """The tar is staged outside the seal AND outside the checkout: it is not
    part of the artifact, and a `.tar` swept into the `files` index would be an
    8-figure byte count the child downloads twice."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert [path.name for path in tmp_path.rglob("*.tar")] == []
    assert not any(key.endswith(".tar") for key in manifest["files"])


def test_a_non_empty_seal_directory_is_refused(corpus, tmp_path):
    """A seal is a FRESH tree, never an overlay on one. `files` is the
    authority on what the child must find, so a leftover from an earlier
    attempt would be indexed, digested and shipped as though the parent had
    sealed it."""
    seal = tmp_path / "seal"
    seal.mkdir()
    (seal / "leftover.txt").write_text("from an earlier attempt\n",
                                       encoding="utf-8")
    with pytest.raises(lane.SealRefused, match="not empty"):
        _seal(corpus, seal)
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


# ---------------------------------------------------------------------------
# the child's intake check (S3's reference implementation)
# ---------------------------------------------------------------------------

def test_a_good_seal_verifies(corpus, tmp_path):
    seal = tmp_path / "seal"
    head = _git(corpus, "rev-parse", "HEAD")
    _seal(corpus, seal)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


def test_verify_reports_an_absent_required_path(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = sorted(manifest["files"])[0]
    (seal / victim).unlink()
    problems = lane.verify_seal(seal)
    assert any(victim in problem and "absent" in problem for problem in problems)


def test_verify_reports_a_tampered_file(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = next(key for key in sorted(manifest["files"])
                  if key.endswith(".md"))
    (seal / victim).write_text("tampered\n", encoding="utf-8")
    assert any("sha256 mismatch" in problem and victim in problem
               for problem in lane.verify_seal(seal))


def test_verify_reports_a_digest_that_does_not_recompute(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["tree_digest"] = "0" * 64
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert any("tree_digest mismatch" in problem
               for problem in lane.verify_seal(seal))


def test_verify_reports_a_seal_that_is_not_the_dispatch(corpus, tmp_path):
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    problems = lane.verify_seal(seal, correlation_id="dashboard-refresh-9-9",
                                corpus_revision="a" * 40,
                                recipe_revision="b" * 40)
    assert len(problems) == 3
    assert any("correlation id mismatch" in problem for problem in problems)
    assert any("corpus revision mismatch" in problem for problem in problems)
    assert any("recipe revision mismatch" in problem for problem in problems)


@pytest.mark.parametrize("text", ["", "not json", "[]", '{"kind": "other"}'])
def test_verify_refuses_a_malformed_manifest(tmp_path, text):
    seal = tmp_path / "seal"
    seal.mkdir()
    (seal / lane.SEAL_MANIFEST_NAME).write_text(text, encoding="utf-8")
    assert lane.verify_seal(seal) != []


def test_verify_refuses_a_schema_version_it_cannot_read(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["schema_version"] = "9.0.0"
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert any("schema_version" in problem for problem in lane.verify_seal(seal))


def test_verify_refuses_a_seal_without_the_validator_or_the_recipe(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    validator_key = f"{lane.SEAL_CORPUS_RELPATH}/{lane.VALIDATOR_SEAL_PATH}"
    manifest["files"].pop(validator_key)
    manifest["files"].pop(lane.SEAL_RECIPE_RELPATH)
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert any(validator_key in problem for problem in problems)
    assert any("build recipe" in problem for problem in problems)


# ---------------------------------------------------------------------------
# the seal speaks git, and only git
# ---------------------------------------------------------------------------

def test_the_seal_speaks_only_git_and_never_builds_or_pushes(corpus, tmp_path):
    runner = RecordingRunner()
    _seal(corpus, tmp_path / "seal", runner=runner)
    assert runner.calls, "the seal made no subprocess call at all"
    for argv in runner.calls:
        assert argv[0] == "git", argv
    verbs = {argv[3] for argv in runner.calls if len(argv) > 3}
    assert verbs <= {"archive", "show", "rev-parse"}, verbs
    assert not hasattr(lane, "build_and_push")


# ---------------------------------------------------------------------------
# the CLI phase — the dispatch gate, and a refusal that never fails the run
# ---------------------------------------------------------------------------

def _seal_cli(tmp_path: Path, corpus: Path, *extra: str,
              decision: dict | None = None) -> dict | None:
    root = tmp_path / "aggregation"
    (root).mkdir(exist_ok=True)
    if decision is not None:
        (root / "dfr-decision.json").write_text(
            json.dumps(decision), encoding="utf-8")
    lane.main(["--repo-root", str(root), "--phase", "seal",
               "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
               "--decision-in", str(root / "dfr-decision.json"),
               "--seal-out", str(tmp_path / "seal"),
               "--seal-result-out", str(root / "seal-result.json"),
               "--correlation-id", CORRELATION, *extra])
    try:
        return json.loads((root / "seal-result.json").read_text(encoding="utf-8"))
    except OSError:
        return None


def test_the_seal_phase_exists_and_is_not_a_build_phase(tmp_path):
    """`--phase seal` is the ONE materialization phase this module offers, and
    `--phase build` — the retired raw-clone recipe — stays refused."""
    with pytest.raises(SystemExit):
        lane.main(["--repo-root", str(tmp_path), "--phase", "build"])


def test_the_seal_phase_refuses_an_absent_decision_without_failing_the_run(
        corpus, tmp_path):
    result = _seal_cli(tmp_path, corpus)          # no decision file written
    assert result["sealed"] is False
    assert "no usable parent decision" in result["reason"]
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_seal_phase_refuses_a_no_change_decision(corpus, tmp_path):
    result = _seal_cli(tmp_path, corpus,
                       decision={"build": False, "outcome": "no_change"})
    assert result["sealed"] is False
    assert "nothing to seal" in result["reason"]


def test_the_seal_phase_writes_the_dispatch_gate(corpus, tmp_path, monkeypatch):
    head = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "gh_read_file",
                        lambda *a, **kw: RECIPE_TEXT)
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is True
    assert result["reason"] is None
    assert result["artifact_name"] == f"dashboard-image-source-{CORRELATION}"
    assert result["source_head"] == head
    assert result["corpus_revision"] == head
    assert result["recipe_revision"] == RECIPE_REV
    assert _instant(result["source_committed_at"]) == _instant(COMMITTED_AT)
    assert is_rfc3339_datetime(result["source_committed_at"])
    assert len(result["tree_digest"]) == 64
    assert result["file_count"] > 0 and result["total_bytes"] > 0
    manifest = lane.read_seal_manifest(tmp_path / "seal")
    assert manifest["tree_digest"] == result["tree_digest"]
    assert lane.verify_seal(tmp_path / "seal", correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


def test_the_seal_phase_reports_a_refusal_as_a_gate_not_an_exception(
        corpus, tmp_path, monkeypatch):
    head = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "seal_source",
                        lambda **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is False
    assert result["reason"] == "RuntimeError: boom"


# ---------------------------------------------------------------------------
# the parent's own workflow stage — ordering, gating and the artifact's name
# ---------------------------------------------------------------------------

def _finalize_steps() -> list[dict]:
    import yaml
    from conftest import REPO_ROOT
    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml")
        .read_text(encoding="utf-8"))
    return workflow["jobs"]["finalize"]["steps"]


def _step_index(steps: list[dict], **match) -> int:
    for index, step in enumerate(steps):
        if all(step.get(key) == value for key, value in match.items()):
            return index
    raise AssertionError(f"no finalize step matching {match}")


def test_the_seal_step_runs_after_the_decision_and_before_the_dispatch():
    """The ordering IS the requirement: the seal must not run on a quiet night
    (the decision short-circuits first) and the child must not be dispatched
    against an artifact that does not exist yet."""
    steps = _finalize_steps()
    decide = _step_index(steps, id="dfr-decide")
    seal = _step_index(steps, id="dfr-seal")
    upload = _step_index(steps, id="dfr-upload")
    dispatch = _step_index(steps, id="dfr-dispatch")
    assert decide < seal < upload < dispatch


def test_the_seal_step_is_gated_on_movement_and_readiness():
    seal = _finalize_steps()[_step_index(_finalize_steps(), id="dfr-seal")]
    assert "steps.dfr-readiness.outputs.ready == 'true'" in seal["if"]
    assert "steps.dfr-decide.outputs.build == 'true'" in seal["if"]
    assert seal["continue-on-error"] is True     # a seal never fails the run
    run = seal["run"]
    assert "--phase seal" in run
    assert "--decision-in dfr-decision.json" in run
    assert "--seal-out dfr-seal" in run
    assert "--seal-result-out dfr-seal-result.json" in run
    assert '--correlation-id "$CORRELATION_ID"' in run


def test_the_upload_names_the_artifact_the_child_downloads():
    steps = _finalize_steps()
    upload = steps[_step_index(steps, id="dfr-upload")]
    assert upload["uses"].startswith("actions/upload-artifact@v4")
    with_ = upload["with"]
    assert with_["name"] == (
        "dashboard-image-source-"
        "${{ steps.dfr-readiness.outputs.correlation_id }}")
    assert with_["name"].startswith(lane.SEAL_ARTIFACT_PREFIX)
    # The seal's own output directory IS the uploaded path — one name, not two.
    seal = steps[_step_index(steps, id="dfr-seal")]
    assert f"--seal-out {with_['path']}" in seal["run"]
    # v4 drops dotfiles by default, and the manifest's index is the authority
    # on what the download must contain (design open question 3).
    assert with_["include-hidden-files"] is True
    assert with_["if-no-files-found"] == "error"
    assert int(with_["retention-days"]) <= 7


def test_the_dispatch_is_gated_on_a_seal_that_actually_uploaded():
    steps = _finalize_steps()
    dispatch = steps[_step_index(steps, id="dfr-dispatch")]
    assert "steps.dfr-seal.outputs.sealed == 'true'" in dispatch["if"]
    # `continue-on-error` makes the upload's CONCLUSION always success, so the
    # gate has to read its OUTCOME or a child could be dispatched against an
    # artifact that never uploaded.
    assert "steps.dfr-upload.outcome == 'success'" in dispatch["if"]


def test_an_unsealed_source_records_a_skip_rather_than_a_failure():
    steps = _finalize_steps()
    skip = steps[_step_index(
        steps, name="Ideation-dashboard image refresh — record skip (source not sealed)")]
    assert skip["continue-on-error"] is True
    assert "--skip-reason" in skip["run"]
    assert "steps.dfr-seal.outputs.sealed != 'true'" in skip["if"]
    assert "steps.dfr-upload.outcome != 'success'" in skip["if"]
    assert _step_index(steps, id="dfr-dispatch") > steps.index(skip)


def test_the_refresh_stage_materializes_nothing_by_a_worker_side_read():
    """The stage's own steps are the parent's. No step in it may introduce a
    second source materialization — the seal is the one place source crosses,
    and a `git clone` appearing anywhere in this stage would be the
    contradiction the re-realization exists to remove."""
    steps = _finalize_steps()
    first = _step_index(steps, id="dfr-readiness")
    stage = steps[first:_step_index(steps, id="dfr-dispatch") + 1]
    for step in stage:
        run = step.get("run") or ""
        assert "git clone" not in run, step.get("name")
        assert "GIT_SSH_COMMAND" not in run, step.get("name")
        assert "sparse-checkout" not in run, step.get("name")
