"""The twenty-third family: release-tag publication.

EVERY FIXTURE HERE IS A REAL GIT REPOSITORY WITH REAL TAGS, and that is the
point rather than an indulgence. This family's whole subject is the difference
between an annotated tag object and a lightweight ref, and between a published
ref and a local one — distinctions that exist in git and nowhere else. A fixture
that faked a tag as a string in a manifest would exercise the parser and prove
nothing about the family, so each repository below is initialised, committed to,
tagged and PUSHED TO AN ORIGIN, because `tag_ref` reads the published refs
deliberately.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from conftest import FakeGit, REPO_ROOT
from doc_health import ERROR, INFO, WARNING, Skip
from doc_health import release_tag_publication as rtp
from doc_health.corpus import RealGit

MANIFEST = rtp.MANIFEST


def _git(repo: Path, *args: str):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True)


def _repo(tmp_path: Path, name: str = "work") -> tuple[Path, Path]:
    """A working repository with an `origin` it can be pushed to.

    The origin is what makes the published-versus-local distinction real: every
    assertion about a tag existing goes through `ls-remote origin`, so a tag
    that is never pushed is genuinely invisible to the family, exactly as an
    unpushed tag is invisible to a consumer.
    """
    origin = tmp_path / f"{name}-origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)],
                   check=True, capture_output=True)
    repo = tmp_path / name
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)],
                   check=True, capture_output=True)
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "tag.gpgSign", "false")
    _git(repo, "remote", "add", "origin", str(origin))
    return repo, origin


def _declare(repo: Path, bundle: str | None, message: str) -> str:
    (repo / "contracts").mkdir(exist_ok=True)
    body = f"contract_bundle_version: {bundle}\n" if bundle else "other: 1\n"
    (repo / MANIFEST).write_text(body)
    _git(repo, "add", MANIFEST)
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _land(repo: Path, n: int) -> None:
    """`n` further first-parent landings that do not touch the manifest.

    Names continue from whatever is already there, so a second call adds new
    commits rather than rewriting the first call's files — an identical write
    stages nothing and `git commit` then fails, which is a test-harness bug
    that reads exactly like a family bug.
    """
    start = len(list(repo.glob("landing-*.md")))
    for i in range(start, start + n):
        (repo / f"landing-{i}.md").write_text(f"landing {i}\n")
        _git(repo, "add", f"landing-{i}.md")
        _git(repo, "commit", "-q", "-m", f"landing {i}")


def _push(repo: Path) -> None:
    _git(repo, "push", "-q", "origin", "main", "--tags")


def _check(repo: Path, threshold: int = rtp.DEFAULT_THRESHOLD):
    return rtp.check_repo("alphaFactory", repo, RealGit(), threshold)


# ----------------------------------------------------------- the tagged states

def test_an_annotated_tag_on_a_declaring_commit_is_quiet(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _git(repo, "tag", "-a", "contract-v2.0", "-m", "contract-v2.0 — additive")
    _land(repo, 3)
    _push(repo)
    assert _check(repo) == []


def test_a_tag_peeling_to_a_commit_that_declares_something_else_is_misplaced(tmp_path):
    repo, _ = _repo(tmp_path)
    wrong = _declare(repo, "contract-v1.9", "cut v1.9")
    _declare(repo, "contract-v2.0", "cut v2.0")
    # the tag names the CURRENT bundle but points at the previous release
    _git(repo, "tag", "-a", "contract-v2.0", wrong, "-m", "misplaced")
    _push(repo)
    findings = _check(repo)
    assert len(findings) == 1
    assert findings[0].severity == ERROR
    assert "MISPLACED" in findings[0].rule
    assert "contract-v1.9" in findings[0].rule
    # the serious state must not borrow the common one's words
    assert "no published annotated tag" not in findings[0].rule
    assert findings[0].resolution == "contested"


def test_a_lightweight_ref_does_not_satisfy_the_obligation(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _git(repo, "tag", "contract-v2.0")          # no -a: lightweight
    _push(repo)
    findings = _check(repo)
    assert len(findings) == 1
    assert findings[0].severity == ERROR
    assert "LIGHTWEIGHT" in findings[0].rule
    assert "no published annotated tag" not in findings[0].rule


def test_a_local_tag_that_was_never_pushed_does_not_count_as_published(tmp_path):
    """The published-refs rule, and the reason `tag_ref` reads the remote."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _land(repo, 2)
    _push(repo)
    _git(repo, "tag", "-a", "contract-v2.0", "-m", "local only")  # NOT pushed
    findings = _check(repo)
    assert len(findings) == 1
    assert findings[0].severity == WARNING
    assert "no published annotated tag" in findings[0].rule


# ------------------------------------------------------------- the distance arm

def test_the_declaring_commit_at_the_published_tip_is_quiet(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _push(repo)
    assert _check(repo) == []


def test_landings_within_the_threshold_warn_and_count_them(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _land(repo, 3)
    _push(repo)
    findings = _check(repo)
    assert len(findings) == 1
    assert findings[0].severity == WARNING
    assert "3 first-parent landing(s)" in findings[0].rule


def test_past_the_threshold_the_finding_is_an_error_and_says_not_published(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _land(repo, 7)
    _push(repo)
    findings = _check(repo)
    assert len(findings) == 1
    assert findings[0].severity == ERROR
    assert "NOT PUBLISHED" in findings[0].rule


def test_the_ruled_threshold_is_five(tmp_path):
    """N=5, ruled by Brett Heap 2026-08-31. Pinned as a value, not a mood: five
    landings warn and six error, so a silent edit of the constant reds here."""
    assert rtp.DEFAULT_THRESHOLD == 5
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.0", "cut v2.0")
    _land(repo, 5)
    _push(repo)
    assert _check(repo)[0].severity == WARNING
    _land(repo, 1)
    _push(repo)
    assert _check(repo)[0].severity == ERROR


# --------------------------------------------------------- floors and non-answers

def test_a_bundle_below_the_enforcement_line_is_not_reported(tmp_path):
    """`contract-v1.0`–`v1.6` carry no tags BY DESIGN. Seven permanent findings
    nobody may act on is how a report teaches its readers to stop reading it."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v1.6", "legacy")
    _land(repo, 9)
    _push(repo)
    assert _check(repo) == []


def test_the_enforcement_floor_is_inclusive_at_v1_7(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v1.7", "the first mandatory one")
    _land(repo, 9)
    _push(repo)
    findings = _check(repo)
    assert len(findings) == 1 and findings[0].severity == ERROR


def test_a_repository_declaring_no_bundle_skips_with_its_reason(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, None, "no bundle here")
    _push(repo)
    out = _check(repo)
    assert isinstance(out, Skip) and "no contract bundle declared" in out.reason


def test_an_unresolvable_published_main_skips_rather_than_finds(tmp_path):
    """Version control cannot answer, so the family declines to answer either —
    never a finding, which would report an absent tag it never looked for."""
    repo = tmp_path / "no-remote"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)],
                   check=True, capture_output=True)
    out = _check(repo)
    assert isinstance(out, Skip) and "published main" in out.reason


def test_unlistable_tag_refs_skip_rather_than_read_absence_as_an_answer():
    """`tag_ref` answering None is "the refs could not be listed", which is NOT
    the same fact as "there is no such tag" — the distinction #338 records the
    canonical verifier getting wrong, and the reason this family does not build
    on it."""
    class NoRefs(FakeGit):
        def tag_ref(self, repo, name):
            return None

        def ls_tree_paths(self, repo, ref, prefix):
            return []
    git = NoRefs(remotes={"r": "tip"},
                 blobs={("r", MANIFEST):
                        b"contract_bundle_version: contract-v2.0\n"})
    out = rtp.check_repo("alphaFactory", Path("r"), git)
    assert isinstance(out, Skip)
    assert "published refs for contract-v2.0 could not be consulted" in out.reason


# ------------------------------------------------------------- the family entry

def test_every_skipped_repository_contributes_its_reason_rather_than_silence(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, None, "no bundle")
    _push(repo)
    tagged, _ = _repo(tmp_path, "tagged")
    _declare(tagged, "contract-v2.0", "cut")
    _git(tagged, "tag", "-a", "contract-v2.0", "-m", "x")
    _push(tagged)

    class Ctx:
        repo_paths = {"alphaFactory": repo, "betaFactory": tagged}
        git = RealGit()

    out = rtp.fam_release_tag_publication(Ctx())
    assert [f.severity for f in out] == [INFO]
    assert "no contract bundle declared" in out[0].rule


def test_all_skipped_returns_one_family_level_skip(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, None, "no bundle")
    _push(repo)

    class Ctx:
        repo_paths = {"alphaFactory": repo}
        git = RealGit()

    assert isinstance(rtp.fam_release_tag_publication(Ctx()), Skip)


def test_no_repository_in_scope_is_a_skip_not_an_empty_pass():
    class Ctx:
        repo_paths = {}
        git = RealGit()

    assert isinstance(rtp.fam_release_tag_publication(Ctx()), Skip)


# ------------------------------------------------------- the self-gate, with control

def test_this_repository_reads_zero_and_the_probe_can_fire(tmp_path):
    """THE SELF-GATE. Every bundle from `contract-v1.7` is tagged, so the
    acceptance measurement over this repository is ZERO.

    THE POSITIVE CONTROL IS THE POINT. A probe that only reads zero cannot
    distinguish a clean corpus from a reader that answers nothing, so the same
    call is made against a tree constructed to be untagged and MUST fire.
    """
    class Ctx:
        repo_paths = {"openxFactory": Path(REPO_ROOT)}
        git = RealGit()

    over_the_real_tree = rtp.fam_release_tag_publication(Ctx())
    # A SKIP IS NOT A DEFECT AND IS NOT ASSERTED AWAY. This family reads the
    # PUBLISHED refs, so its answer depends on whether the checkout has fetched
    # the tip — an environment fact, not a corpus fact. What must hold over the
    # real tree is that it invents no defect: no `error`, no `warning`. The
    # skip path carries `info` and its reason, which is the honest answer when
    # the question could not be asked.
    if not isinstance(over_the_real_tree, Skip):
        assert [f for f in over_the_real_tree
                if f.severity in (ERROR, WARNING)] == []

    control, _ = _repo(tmp_path, "control")
    _declare(control, "contract-v2.0", "cut, never tagged")
    _land(control, 9)
    _push(control)

    class ControlCtx:
        repo_paths = {"controlFactory": control}
        git = RealGit()

    fired = rtp.fam_release_tag_publication(ControlCtx())
    assert [f.severity for f in fired] == [ERROR], (
        "the probe read zero over the real tree and must be shown capable of "
        "firing, or it proves nothing about the corpus")


# ------------------------------------- the recurrence this family exists to catch

def test_a_superseded_bundle_that_was_never_tagged_is_still_reported(tmp_path):
    """CODEX P1 ON PR #544, AND THE REASON THIS TEST EXISTS.

    The family first checked only the bundle the manifest CURRENTLY declares,
    which permanently missed the exact incident that motivated it: v2.3 is
    silent while its declaring commit is the tip, then v2.4 advances the
    manifest and the family starts checking v2.4 and never revisits the
    still-untagged v2.3. It would have read ZERO through the whole recurrence.
    """
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.3", "cut v2.3, never tagged")
    (repo / "contracts" / "releases").mkdir(parents=True, exist_ok=True)
    (repo / "contracts/releases/contract-v2.3.digests.yaml").write_text("x: 1\n")
    _git(repo, "add", "contracts/releases/contract-v2.3.digests.yaml")
    _git(repo, "commit", "-q", "-m", "v2.3 inventory")
    _declare(repo, "contract-v2.4", "cut v2.4")
    (repo / "contracts/releases/contract-v2.4.digests.yaml").write_text("y: 1\n")
    _git(repo, "add", "contracts/releases/contract-v2.4.digests.yaml")
    _git(repo, "commit", "-q", "-m", "v2.4 inventory")
    _git(repo, "tag", "-a", "contract-v2.4", "-m", "v2.4")
    _push(repo)

    findings = _check(repo)
    rules = " ".join(f.rule for f in findings)
    assert "contract-v2.3" in rules, (
        "the superseded, never-tagged bundle is invisible: the family checked "
        "only the current declaration, which is the recurrence it exists for")
    assert any(f.severity == ERROR for f in findings)


def test_an_unfetched_published_tip_skips_rather_than_reading_no_bundle(tmp_path):
    """THE #338 CONFLATION, GUARDED IN THIS FAMILY'S OWN READS.

    Found by running the family against this repository while `main` had
    advanced past the last fetch: it reported "no contract bundle declared"
    against a repository declaring `contract-v2.5`. `blobs_at` answers None PER
    PATH for a blob it cannot read, and "not fetched" is not an answer.
    """
    class Unfetched(FakeGit):
        def blobs_at(self, repo, commit, relpaths):
            return {p: None for p in relpaths}

    git = Unfetched(remotes={"r": "tip-not-here"})
    out = rtp.check_repo("alphaFactory", Path("r"), git)
    assert isinstance(out, Skip)
    assert "could not be read at the published tip" in out.reason
    assert "no contract bundle declared" not in out.reason
