"""The declared sentinel vocabulary and the fifth outcome
(`declare-sentinel-pin-vocabulary`; two deltas, nineteen scenarios).

Every test here is pinned to a DEFECT rather than to a fix. The defects, all
measured on 2026-08-27 against `origin/main` at 45ba637a:

  A. SEVEN committed artifacts carried a non-commit value under a declared pin
     key and the verification READ NONE OF THEM. `_field_re` and `_VOCAB_RE`
     bound the value group to forty hex characters, so a sentinel produced no
     `PinSite` at all — not reachable, not orphaned, not lost, and not UNCOVERED
     either. The probe reported a fully verified class over seven artifacts
     whose central provenance claim nothing had read.
  B. `git_generation()` stamped `rev-parse HEAD` unconditionally, with no
     `status --porcelain`, no `diff --quiet` and no sentinel branch. Read a
     dirty corpus and the index claimed derivation from a tree the generator
     never saw — a pin that RESOLVES and lies, which no reachability check can
     catch because nothing about the commit is missing.
  C. THREE guards in `proposal-support.py` compared against the literal
     `"uncommitted"`, so they recognized one spelling of one condition.
     `git_blob_sha256(root, "uncommitted-worktree", "README.md")` raised
     `SupportError: invalid repository revision` — on the exact value six
     archived manifests carry, which made `verify` on any of them a crash.
  D. `"unknown"` and `"composed"` appeared in no governance document at all,
     so the defect branch would have reported the snapshot registry's and the
     avatar F0 lane's own output as defects on the day it was switched on.

The fixtures are real git repositories under `tmp_path`; no test mutates any
checkout on the machine, and the tests that read the real repository only read
it.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import pin_class as pc
from doc_health import pin_sentinels as ps


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


def _commit(repo, message="c"):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


MANIFEST_REL = ("openspec/changes/archive/2026-08-01-fixture/"
                "supporting-docs.manifest.yaml")


def _manifest(revision):
    """A proposal-support manifest — the member all seven real sentinel sites
    belong to. `None` omits the key entirely, which is the fourth state."""
    body = {"schema_version": 1, "kind": "proposal_support_manifest",
            "change_id": "fixture", "files": []}
    if revision is not None:
        body["source_revision"] = revision
    return yaml.safe_dump(body, sort_keys=False)


def value_repo(tmp_path, revision, *, name="repo"):
    """A repository whose one manifest carries `revision` under the pin key."""
    root = _init(tmp_path / name)
    _write(root, MANIFEST_REL, _manifest(revision))
    _commit(root)
    return root


def _bootstrap():
    """The cross-reference generator, loaded from its hyphenated path."""
    script = REPO_ROOT / "scripts" / "bootstrap-ideation-cross-reference.py"
    spec = importlib.util.spec_from_file_location("_xref_bootstrap", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _support():
    script = REPO_ROOT / "scripts" / "proposal-support.py"
    spec = importlib.util.spec_from_file_location("_support_guards", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corpus_repo(tmp_path, *, name="corpus"):
    """A repository shaped like the two globs `collect()` reads."""
    root = _init(tmp_path / name)
    _write(root, "ideation/brainstorm/one.md",
           "# One\n\nStatus: brainstorm\nTopics: alpha\n\n## Body\n\nx.\n")
    _write(root, "ideation/staging/topic/two.md",
           "# Two\n\nStatus: staged\nTopics: alpha\n\n## Body\n\nx.\n")
    _commit(root)
    return root


# =========================================================================
# the declaration itself
# =========================================================================

def test_every_member_states_a_condition_and_a_standing():
    """A sentinel whose meaning is not written down is a magic string, and a
    reader who meets it in an artifact learns only that somebody chose not to
    write a commit. The declaration refuses a member on the strength of its
    spelling being self-explanatory."""
    assert ps.declaration_defects() == ()
    for member in ps.SENTINELS:
        assert member.condition in ps.CONDITIONS, member.value
        assert member.standing in (ps.CANONICAL, ps.LEGACY), member.value
        assert member.note.strip(), member.value


def test_exactly_one_canonical_spelling_per_condition():
    """A legacy member without that marking is indistinguishable from a second
    canonical spelling, which is the drift the declaration exists to stop."""
    for condition in ps.CONDITIONS:
        canonical = [m for m in ps.members_for(condition)
                     if m.standing == ps.CANONICAL]
        assert len(canonical) == 1, (condition, canonical)
        assert ps.canonical_for(condition) is canonical[0]


def test_a_member_declared_without_a_condition_is_reported(monkeypatch):
    """The defect branch of the declaration check, exercised rather than
    asserted: a synthetic member with a condition nothing declares must be
    reported as an incomplete declaration."""
    broken = ps.SentinelMember(value="fixture-spelling", condition="no-such",
                               standing=ps.CANONICAL, emitters=(), note="x")
    monkeypatch.setattr(ps, "SENTINELS", ps.SENTINELS + (broken,))
    defects = ps.declaration_defects()
    assert any("fixture-spelling" in d and "no declared condition" in d
               for d in defects), defects


def test_the_declared_emitters_are_measured_rather_than_believed():
    """`emitters` is what exempts a member with no committed instance from the
    unused report, so a phantom emitter would keep a stale member alive on a
    claim nobody checked. Each declared location must exist and must actually
    reach for the value — by the literal or by this module's constant."""
    constants = {v: k for k, v in vars(ps).items()
                 if isinstance(v, str) and not k.startswith("_")}
    for member in ps.SENTINELS:
        for emitter in member.emitters:
            rel = emitter.split(" (")[0]
            path = REPO_ROOT / rel
            assert path.is_file(), f"{member.value}: no {rel}"
            text = path.read_text(encoding="utf-8")
            name = constants.get(member.value, "")
            assert (f'"{member.value}"' in text or f"'{member.value}'" in text
                    or (name and name in text)), \
                f"{rel} no longer emits {member.value!r}"


def test_two_spellings_naming_two_conditions_are_both_members(monkeypatch):
    """Q1, ruled 2026-08-27. `uncommitted-worktree` and `uncommitted` resemble
    each other in words and name different facts: one says the content is real
    and unreconstructible, the other says nothing about the content was
    established. Both are members, each canonical for its own condition, and
    NEITHER is marked legacy on the strength of the resemblance — folding the
    second into the first would silently restate every artifact carrying it."""
    dirty = ps.declared(ps.UNCOMMITTED_WORKTREE)
    unreadable = ps.declared(ps.UNCOMMITTED)
    assert dirty is not None and unreadable is not None
    assert dirty.condition != unreadable.condition
    assert dirty.condition == ps.DIRTY_WORKTREE
    assert unreadable.condition == ps.UNREADABLE_REPOSITORY
    assert dirty.standing == ps.CANONICAL
    assert unreadable.standing == ps.CANONICAL
    assert ps.CONDITIONS[dirty.condition] != ps.CONDITIONS[unreadable.condition]


def test_unknown_is_not_folded_into_the_unreadable_repository_condition():
    """THE POINT `declare-sentinel-pin-vocabulary` LEFT TO REALIZATION, decided
    on measurement under the same-condition rule the delta states rather than on
    the resemblance.

    Three call sites emitted `"unknown"` and they did not name one condition:
    `snapshot_registry.index_entry` projects an index entry whose recorded
    revision is absent while the repository is perfectly readable;
    `avatar_f0.cli._git_head` means `rev-parse HEAD` answered nothing, which IS
    the unreadable-repository condition; and `avatar_f0.cli._git_file_commit`
    returned it when `git log -1 -- <path>` succeeds and finds no commit, which
    means the repository is readable, HEAD resolves, and the named content has
    simply never been committed. Two spellings fold into one condition only if
    measurement shows ONE condition, and that measurement showed three — so
    `"unknown"` is declared as its own weakest member instead.

    THE MEMBERSHIP IS WHAT THIS TEST PINS, AND IT DID NOT MOVE WHEN THE SPLIT
    LANDED. `fix-pin-value-boundary-and-sentinel-split` sent the two avatar
    conditions to their stronger members; what that changes is which sites
    EMIT this one, which the split's own tests below measure. The reason the
    member exists — three conditions, not one — is the finding, and deleting it
    because the code moved would delete the evidence for the member."""
    unknown = ps.declared(ps.UNKNOWN)
    assert unknown is not None
    assert unknown.condition == ps.UNESTABLISHED_REVISION
    assert unknown.condition != ps.UNREADABLE_REPOSITORY
    assert unknown.standing == ps.CANONICAL
    # the projector's site, now reaching for the DECLARED constant rather than
    # retyping the spelling (Q3, ruled 2026-08-28)
    registry = (REPO_ROOT / "scripts/ideation_dashboard/snapshot_registry.py"
                ).read_text(encoding="utf-8")
    assert "self.source_revision or pin_sentinels.UNKNOWN" in registry
    assert 'self.source_revision or "unknown"' not in registry, (
        "the projector retypes the spelling again; a generator writing a "
        "declared member imports the name")


# =========================================================================
# the `"unknown"` split (`fix-pin-value-boundary-and-sentinel-split`, defect 3)
#
# THE DEFECT, re-measured 2026-08-28 against `origin/main` at `5314fac5`. The
# inherited record names THREE emission sites; there are FIVE, and one of them
# fired on TWO conditions by itself. `avatar_f0/cli.py:49` ran `subprocess.run`
# with no `check` and never read `out.returncode`, so a single `"unknown"` was
# reached by a SUCCESSFUL `git log` that found no commit for the path and by a
# FAILED one that produced nothing because it failed. Those are different facts
# and the vocabulary declares a different member for each, so the branch had to
# exist before either could be written honestly.
#
# EVERY CONDITION BELOW IS CONSTRUCTED, NEVER MOCKED. A test that patched the
# `CompletedProcess` would assert what this session believes git does; these
# build the repository state that produces the condition and let git answer.
# =========================================================================

def _executable_strings(path) -> set[str]:
    """Every string LITERAL a module evaluates, docstrings excluded.

    Read with `ast` rather than by counting substrings, because the difference
    that matters is between a spelling the code WRITES and a spelling the
    module EXPLAINS — and a source scan that cannot tell them apart makes
    writing the reasoning down a test failure, which is how a module ends up
    with an undocumented rule."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                              ast.AsyncFunctionDef))
                and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            docstrings.add(id(body[0].value))
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and id(node) not in docstrings}


def _avatar_cli():
    """The F0 harness CLI, loaded from its own tree.

    Loaded by path rather than imported, because `experiments/` is not on the
    test run's import path and putting it there would change what every other
    test in this suite can see."""
    root = REPO_ROOT / "experiments/avatar-brokered-call/src"
    if not (root / "avatar_f0" / "cli.py").is_file():
        pytest.skip(f"{root} carries no avatar_f0 harness")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from avatar_f0 import cli
    return cli


def test_a_successful_git_log_finding_no_commit_writes_the_dirty_tree_member(
        tmp_path):
    """CONDITION: the repository is readable, `HEAD` resolves, and the named
    content is held by NO COMMIT. That is `dirty-worktree` — the content is real
    and no commit name describes it — and its canonical spelling is
    `uncommitted-worktree`.

    Constructed by writing a file and NOT committing it, so `git log -1 --
    <path>` exits zero with empty output. Before the split this returned
    `"unknown"`, which asserts only that nobody wrote down which condition
    applied."""
    cli = _avatar_cli()
    repo = _init(tmp_path / "readable")
    _write(repo, "a.txt", "committed\n")
    _commit(repo, "one")
    (repo / "never-committed.txt").write_text("live content\n",
                                              encoding="utf-8")
    got = cli._git_file_commit(repo, "never-committed.txt")
    assert got == ps.UNCOMMITTED_WORKTREE
    member = ps.declared(got)
    assert member is not None and member.condition == ps.DIRTY_WORKTREE
    # and the honest half: a file that IS committed still gets its commit name
    assert re.fullmatch(r"[0-9a-f]{40}", cli._git_file_commit(repo, "a.txt"))


def test_a_failed_git_log_writes_the_unreadable_repository_member(tmp_path):
    """CONDITION: the path is not a repository at all, so `git log` exits
    non-zero and establishes nothing. Q2, ruled 2026-08-28: that is
    `unreadable-repository`, spelled `uncommitted`.

    THE RETURN CODE IS THE WHOLE POINT. Both this and the test above produce
    EMPTY STDOUT; without reading `out.returncode` they are indistinguishable,
    which is why one `"unknown"` covered both."""
    cli = _avatar_cli()
    not_a_repo = tmp_path / "plain"
    not_a_repo.mkdir()
    (not_a_repo / "a.txt").write_text("x\n", encoding="utf-8")
    probe = subprocess.run(
        ["git", "-C", str(not_a_repo), "log", "-1", "--format=%H", "--",
         "a.txt"], capture_output=True, text=True)
    assert probe.returncode != 0 and not probe.stdout.strip(), (
        "the fixture must produce a NON-ZERO exit with empty output, or it is "
        "not measuring the branch this test is about")
    got = cli._git_file_commit(not_a_repo, "a.txt")
    assert got == ps.UNCOMMITTED
    member = ps.declared(got)
    assert member is not None
    assert member.condition == ps.UNREADABLE_REPOSITORY
    assert got != ps.UNCOMMITTED_WORKTREE, (
        "an unreadable repository is a weaker statement than a dirty tree: "
        "nothing about the content was established, as against the content "
        "being real and held by no commit")


def test_a_raising_git_call_writes_the_unreadable_repository_member(
        tmp_path, monkeypatch):
    """The `except` return of BOTH helpers. The call did not complete at all —
    git absent, or the process could not be started — so nothing was
    established, which is the same condition a non-zero exit names.

    CONSTRUCTED BY MAKING GIT UNREACHABLE, not by raising into the harness and
    not by pointing at a missing directory. THE MISSING-DIRECTORY ROUTE WAS
    TRIED FIRST AND MEASURED WRONG: `git -C /does-not-exist log` does not raise,
    it exits 128, so that fixture exercised the return-code branch under this
    test's name and left the `except` return unproven. Emptying `PATH` makes
    `subprocess.run` raise `FileNotFoundError` for real, which is the condition
    a machine without git is actually in."""
    cli = _avatar_cli()
    repo = _init(tmp_path / "real")
    _write(repo, "a.txt", "x\n")
    _commit(repo, "one")
    # the fixture answers honestly BEFORE the environment is broken
    assert re.fullmatch(r"[0-9a-f]{40}", cli._git_file_commit(repo, "a.txt"))

    monkeypatch.setenv("PATH", "")
    with pytest.raises(FileNotFoundError):
        subprocess.run(["git", "--version"], capture_output=True)

    for got in (cli._git_file_commit(repo, "a.txt"), cli._git_head(repo)):
        assert got == ps.UNCOMMITTED
        assert ps.declared(got).condition == ps.UNREADABLE_REPOSITORY


def test_a_non_zero_exit_on_a_path_that_is_not_a_repository_is_the_same_member(
        tmp_path):
    """The neighbouring route, kept separate because it reaches a DIFFERENT
    branch: `git -C <missing>` exits 128 rather than raising, so this is the
    return-code branch and not the `except` one. Both name the same condition,
    which is why the split writes one member for the pair."""
    cli = _avatar_cli()
    missing = tmp_path / "does-not-exist"
    assert not missing.exists()
    probe = subprocess.run(
        ["git", "-C", str(missing), "log", "-1", "--format=%H", "--", "a.txt"],
        capture_output=True, text=True)
    assert probe.returncode != 0, "the fixture must exit non-zero"
    assert cli._git_file_commit(missing, "a.txt") == ps.UNCOMMITTED
    assert cli._git_head(missing) == ps.UNCOMMITTED


def test_both_head_returns_write_the_unreadable_repository_member(tmp_path):
    """`_git_head`'s two returns are ONE CONDITION WEARING TWO SPELLINGS: there
    is no success of `rev-parse HEAD` that answers empty, so an empty answer and
    an exception both mean the repository's revision could not be read.

    AND A THIRD SPELLING MEASURED AT REALIZATION. The packet reasoned that a
    failed `rev-parse HEAD` always produces nothing; measured against git, an
    UNBORN `HEAD` prints the literal string `HEAD` on stdout and exits non-zero,
    so the unguarded form returned `"HEAD"` — neither a commit name nor a
    declared sentinel, written where the repository's revision goes. The
    vocabulary already assigns the unborn case to this member by name, so
    reading the return code changed no ruled member; it stopped a third failure
    being spelled as a pin."""
    cli = _avatar_cli()

    unborn = tmp_path / "unborn"
    unborn.mkdir()
    _git(unborn, "init", "-q", "-b", "main")
    probe = subprocess.run(["git", "-C", str(unborn), "rev-parse", "HEAD"],
                           capture_output=True, text=True)
    assert probe.returncode != 0, "the fixture's HEAD must be unborn"
    assert probe.stdout.strip() == "HEAD", (
        "this git spells an unborn HEAD differently; the branch still has to "
        "refuse whatever it does print, so re-measure rather than delete")
    assert cli._git_head(unborn) == ps.UNCOMMITTED

    missing = tmp_path / "gone"
    assert not missing.exists()
    assert cli._git_head(missing) == ps.UNCOMMITTED

    plain = tmp_path / "plain"
    plain.mkdir()
    assert cli._git_head(plain) == ps.UNCOMMITTED

    for value in {cli._git_head(unborn), cli._git_head(missing),
                  cli._git_head(plain)}:
        assert ps.declared(value).condition == ps.UNREADABLE_REPOSITORY

    # and a readable repository still gets its own revision
    real = _init(tmp_path / "real")
    _write(real, "a.txt", "x\n")
    head = _commit(real, "one")
    assert cli._git_head(real) == head


def test_no_avatar_emission_site_writes_the_weakest_member_any_more(tmp_path):
    """THE SPLIT, ASSERTED AS A PROPERTY RATHER THAN SITE BY SITE. The
    declaration's own instruction is that a generator able to distinguish MUST
    NOT reach for `unknown`; the avatar harness can distinguish, so no condition
    it can reach may produce that member.

    THE SOURCE ASSERTION IS DELIBERATE AND IS THE MUTATION PIN. Collapsing any
    one branch back to the literal is invisible to a value assertion over the
    other branches, so the refusal is pinned at the declaration too — the same
    reasoning as the boundary's structural test."""
    cli = _avatar_cli()
    lane_path = (REPO_ROOT
                 / "experiments/avatar-brokered-call/src/avatar_f0/cli.py")
    lane = lane_path.read_text(encoding="utf-8")
    assert ps.UNKNOWN not in _executable_strings(lane_path), (
        "an avatar emission site still writes the weakest member; it can tell "
        "a dirty tree from an unreadable repository, so it must write the "
        "member the condition names")
    assert "out.returncode" in lane, (
        "the return-code branch is the prerequisite for the whole split: "
        "without it `git log` succeeding-with-nothing and failing-with-nothing "
        "are the same return")
    assert "pin_sentinels.UNCOMMITTED_WORKTREE" in lane
    assert "pin_sentinels.UNCOMMITTED" in lane

    # driven, not merely read: every condition the harness can produce
    repo = _init(tmp_path / "r")
    _write(repo, "a.txt", "x\n")
    _commit(repo, "one")
    (repo / "loose.txt").write_text("y\n", encoding="utf-8")
    produced = {
        cli._git_file_commit(repo, "loose.txt"),
        cli._git_file_commit(tmp_path / "nope", "a.txt"),
        cli._git_head(tmp_path / "nope"),
    }
    assert ps.UNKNOWN not in produced, produced
    assert produced == {ps.UNCOMMITTED_WORKTREE, ps.UNCOMMITTED}


def test_the_split_leaves_every_declared_member_with_an_emitter():
    """§ 3.6. A split that stranded a member would fail the declaration's own
    declaration-against-corpus direction, and the failure would surface as an
    unrelated regression somewhere else. `unused_sentinels()` must still report
    zero over the real corpus, and the emitter tuples must follow the split
    rather than describe the code before it."""
    unknown = ps.declared(ps.UNKNOWN)
    assert unknown.emitters == (
        "scripts/ideation_dashboard/snapshot_registry.py (index_entry)",), (
        "the weakest member keeps exactly the one site that genuinely cannot "
        "say more")
    avatar = ("experiments/avatar-brokered-call/src/avatar_f0/cli.py")
    dirty = ps.declared(ps.UNCOMMITTED_WORKTREE)
    unreadable = ps.declared(ps.UNCOMMITTED)
    assert any(e.startswith(avatar) for e in dirty.emitters), dirty.emitters
    assert any(e.startswith(avatar) for e in unreadable.emitters), \
        unreadable.emitters

    # the vocabulary is still internally consistent after the move
    assert ps.declaration_defects() == ()

    # and nothing was stranded, measured over the real corpus
    sites, _uncovered, _absent = pc.non_pin_sites(REPO_ROOT)
    unused = pc.unused_sentinels(sites)
    assert unused == (), (
        "a declared member is now neither carried by committed state nor "
        f"emitted by any declared emitter: {unused}")


def test_the_split_moves_no_committed_bytes():
    """§ 3.7. The split changes FUTURE output only: no committed artifact
    carries `"unknown"` under a swept key, so there is nothing to migrate and
    the class's legal-non-pin population does not move."""
    report = pc.verify(REPO_ROOT, allow_remote=False)
    legal = [r for r in report.non_pins if r.legal]
    values = sorted(r.site.value for r in legal)
    assert ps.UNKNOWN not in values, (
        "a committed artifact carries the weakest member under a pin key; the "
        "split would then owe a migration, and captured material is never "
        "edited after capture — declare the finding instead")
    assert set(values) <= {ps.UNCOMMITTED_WORKTREE, ps.NOT_APPLICABLE_AD_HOC,
                           ps.UNCOMMITTED, ps.COMPOSED}, values


def test_absence_is_recognized_and_is_not_a_member():
    """Q2, ruled 2026-08-27. An artifact carrying no pin key makes no claim,
    honest or otherwise, so it cannot be declared a spelling — and converting
    one into a sentinel after the fact would assert a condition nobody
    recorded."""
    assert not ps.is_declared_sentinel("")
    assert not ps.is_declared_sentinel(None)
    assert ps.declared(None) is None
    assert "NOT A MEMBER" in ps.ABSENT_KEY
    assert "REPAIRED NEVER" in ps.ABSENT_KEY


def test_a_near_miss_spelling_is_not_matched_to_a_declared_member():
    """A near-miss spelling is precisely the condition under which every
    consumer guarding on the exact string already fails, so guessing here would
    make the check agree with a consumer that crashes."""
    for near in ("uncommitted-worktre", "uncommitted_worktree",
                 "Uncommitted-Worktree", " uncommitted-worktree",
                 "uncommitted-worktrees", "not-applicable", "unknow",
                 "composed-view"):
        assert not ps.is_declared_sentinel(near), near


def test_the_declared_qualified_form_is_matched_and_only_that_form():
    """`compose_snapshots` seeds `composed` and then replaces it with
    `composed:<repo>@<ref>:<sha>,…`, so declaring only the bare spelling would
    have left the lane's real output undeclared. The prefix is DECLARED on the
    member rather than guessed at the comparison, which is what keeps this from
    being the near-miss matching the rule above refuses."""
    assert ps.is_declared_sentinel("composed")
    assert ps.is_declared_sentinel("composed:openxFactory@main:" + "a" * 40)
    assert not ps.is_declared_sentinel("composed-from")
    assert not ps.is_declared_sentinel("recomposed:x")


# =========================================================================
# the classification
# =========================================================================

def test_a_declared_sentinel_is_a_legal_non_pin_and_holds_nothing_open(
        tmp_path):
    """THE FIFTH OUTCOME. It is not reachable (no commit, so reporting it as
    reachable would claim a resolution nobody performed), not orphaned or lost
    (those say a NAMED commit cannot be found), not uncovered (the key IS
    declared and the sweep DID read the site) and not inconclusive (the clone
    answered perfectly). And it does NOT hold full verification open, because
    the artifact is conforming."""
    repo = value_repo(tmp_path, ps.UNCOMMITTED_WORKTREE)
    report = pc.verify(repo, allow_remote=False)

    assert len(report.legal_non_pins) == 1
    result = report.legal_non_pins[0]
    assert result.site.path == MANIFEST_REL
    assert result.site.key == "source_revision"
    assert result.site.value == ps.UNCOMMITTED_WORKTREE
    assert result.sentinel.condition == ps.DIRTY_WORKTREE

    assert report.undeclared_values == []
    assert report.orphans == [] and report.lost == []
    assert report.uncovered == () and report.uncovered_non_pins == ()
    assert report.inconclusive == []
    assert report.clean and report.fully_verified

    rendered = pc.render(report)
    assert "[non-pin]" in rendered
    assert "1 legal non-pin(s)" in report.summary()


def test_an_undeclared_non_commit_value_is_a_defect_naming_all_three(tmp_path):
    """The defect names the artifact, the key AND the value, and it holds the
    class open — an undeclared spelling has a remedy, unlike a recognized
    legacy absence."""
    repo = value_repo(tmp_path, "definitely-not-declared")
    report = pc.verify(repo, allow_remote=False)

    assert len(report.undeclared_values) == 1
    result = report.undeclared_values[0]
    assert result.sentinel is None
    assert result.site.path == MANIFEST_REL
    assert result.site.key == "source_revision"
    assert result.site.value == "definitely-not-declared"
    assert "UNDECLARED" in result.how
    assert report.legal_non_pins == []
    assert not report.clean and not report.fully_verified

    rendered = pc.render(report)
    assert MANIFEST_REL in rendered
    assert "definitely-not-declared" in rendered
    assert "source_revision" in rendered


@pytest.mark.parametrize("value", ["uncommitted-worktre", "UNCOMMITTED",
                                   "not-applicable", "compose"])
def test_a_near_miss_reaches_the_defect_branch_not_the_nearest_member(
        tmp_path, value):
    """The classification does not try to tell an invented spelling from a
    truncated object name from a member drifted by one character, because the
    remedy is identical for all three."""
    repo = value_repo(tmp_path / value, value)
    report = pc.verify(repo, allow_remote=False)
    assert report.legal_non_pins == []
    assert [r.site.value for r in report.undeclared_values] == [value]


def test_a_commit_shaped_value_is_untouched_by_the_classification(tmp_path):
    """The commit-shaped path keeps its regexes, its ref set and its verdicts,
    and no sentinel outcome is emitted for a commit name."""
    repo = _init(tmp_path / "commits")
    _write(repo, MANIFEST_REL, _manifest("0" * 40))
    _commit(repo)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _write(repo, MANIFEST_REL, _manifest(head))
    _commit(repo, "repin")

    report = pc.verify(repo, allow_remote=False)
    assert report.non_pins == ()
    assert [r.site.pin for r in report.results] == [head]
    assert [r.verdict for r in report.results] == [pc.PASS]


def test_an_absent_key_is_a_recognized_legacy_state_and_is_not_filled_in(
        tmp_path):
    """Q2 in the report rather than in the declaration: the absence is
    reported, it is reported DISTINCTLY from an undeclared spelling, it is not
    a vocabulary member, and it does not hold the class open — there is nothing
    for a red to ask for when the repair is `never`."""
    repo = value_repo(tmp_path, None)
    report = pc.verify(repo, allow_remote=False)

    assert len(report.absent_keys) == 1
    absence = report.absent_keys[0]
    assert absence.path == MANIFEST_REL
    assert absence.key == "source_revision"
    assert absence.member_id == "proposal-support-manifest"

    assert report.non_pins == ()          # absence is not a value
    assert report.undeclared_values == []
    assert report.legal_non_pins == []
    assert report.clean and report.fully_verified
    assert "[ABSENT]" in pc.render(report)
    assert "1 recognized legacy absence(s)" in report.summary()


def test_a_declared_member_nothing_carries_reports_as_unused(monkeypatch):
    """The second direction, and the unobvious one: a vocabulary that
    accumulates entries nobody writes becomes a place where a reader looks up a
    value, finds a plausible-sounding condition, and believes something about
    an artifact no generator has ever produced. Reporting it is not deleting
    it — a member with a declared emitter is exempt, because a condition may be
    declared before its first committed instance lands."""
    stale = ps.SentinelMember(value="fixture-never-written",
                              condition=ps.OUTSIDE_REPOSITORY,
                              standing=ps.LEGACY, emitters=(),
                              note="declared by a test and carried by nothing")
    with_emitter = ps.SentinelMember(value="fixture-emitted-not-committed",
                                     condition=ps.OUTSIDE_REPOSITORY,
                                     standing=ps.LEGACY,
                                     emitters=("scripts/proposal-support.py",),
                                     note="a generator writes it; nothing has "
                                          "been committed yet")
    monkeypatch.setattr(ps, "SENTINELS",
                        ps.SENTINELS + (stale, with_emitter))
    unused = pc.unused_sentinels([])
    assert stale in unused
    assert with_emitter not in unused
    assert all(m.emitters for m in ps.SENTINELS if m not in unused)


def test_a_sentinel_under_an_uncovered_key_is_two_findings(tmp_path):
    """A coverage gap in the declaration and the meaning of the value are
    separate findings, and neither is allowed to mask the other."""
    repo = _init(tmp_path / "uncovered")
    _write(repo, "ideation/dashboard/some-new-lane.yaml",
           yaml.safe_dump({"schema_version": 1,
                           "source_revision": ps.UNCOMMITTED_WORKTREE}))
    _commit(repo)
    report = pc.verify(repo, allow_remote=False)

    assert len(report.uncovered_non_pins) == 1
    assert report.uncovered_non_pins[0].value == ps.UNCOMMITTED_WORKTREE
    assert len(report.legal_non_pins) == 1
    assert report.legal_non_pins[0].site.member_id is None
    assert not report.clean       # the coverage gap is the defect, not the value


def test_a_key_name_quoted_in_prose_or_a_comment_is_not_a_site(tmp_path):
    """MEASURED, not anticipated. Widening the value group removes the accident
    that protected the key match — forty hex characters almost never follow a
    colon inside a sentence — so the key must stand at a MAPPING POSITION. Both
    shapes below are real: a folded `detail: >-` block quoting `commit:path`
    and a YAML comment quoting `` `commit:` above `` were the two false
    positives a naive widening reported over the real repository."""
    repo = _init(tmp_path / "prose")
    _write(repo, MANIFEST_REL,
           "schema_version: 1\n"
           "kind: proposal_support_manifest\n"
           "# the verifier compares against `source_revision:` above\n"
           "detail: >-\n"
           "  Live source_revision:path resolution of five stack.yaml blobs\n"
           "files: []\n")
    _commit(repo)
    report = pc.verify(repo, allow_remote=False)
    assert report.non_pins == ()
    assert report.uncovered_non_pins == ()
    # the key really is absent here, and THAT is what gets reported
    assert [a.path for a in report.absent_keys] == [MANIFEST_REL]


# =========================================================================
# the generator
# =========================================================================

def test_git_generation_writes_the_real_pin_on_a_clean_corpus(tmp_path):
    """THE DIRECTION PINNED AS HARD AS THE DIRTY ONE. On a clean corpus the
    behaviour is byte-identical to before the sentinel branch existed: the same
    `rev-parse HEAD`, under the same key, beside the same two siblings."""
    repo = corpus_repo(tmp_path)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    generation = _bootstrap().git_generation(repo)
    assert generation["source_revision"] == head
    assert set(generation) == {"source_revision", "generated_at",
                               "generator_version"}


def test_git_generation_writes_the_sentinel_on_a_dirty_corpus(tmp_path):
    """A pin stamped from `HEAD` while the generator reads a dirty tree names a
    commit that is perfectly reachable and perfectly wrong. The declared
    spelling for the condition goes in instead — and it is the CANONICAL one
    for the dirty-tree condition, not a string of this generator's invention."""
    repo = corpus_repo(tmp_path)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "ideation/brainstorm/one.md").write_text(
        "# One\n\nStatus: brainstorm\nTopics: alpha, beta\n\n## Body\n\ny.\n",
        encoding="utf-8")

    generation = _bootstrap().git_generation(repo)
    assert generation["source_revision"] == ps.UNCOMMITTED_WORKTREE
    assert generation["source_revision"] != head
    assert ps.declared(generation["source_revision"]).condition == \
        ps.DIRTY_WORKTREE
    assert ps.canonical_for(ps.DIRTY_WORKTREE).value == \
        generation["source_revision"]


def test_git_generation_sees_an_untracked_corpus_document(tmp_path):
    """`status --porcelain` rather than `diff --quiet`, and this is why: a
    brand-new brainstorm document is READ by `collect()`, changes the index and
    is held by no commit, while `diff` cannot see it at all."""
    repo = corpus_repo(tmp_path)
    _write(repo, "ideation/brainstorm/three.md",
           "# Three\n\nStatus: brainstorm\nTopics: alpha\n\n## Body\n\nz.\n")
    assert _bootstrap().git_generation(repo)["source_revision"] == \
        ps.UNCOMMITTED_WORKTREE


def test_git_generation_ignores_a_file_the_derivation_never_reads(tmp_path):
    """A SENTINEL IS NEVER A LICENCE TO SKIP A PIN THAT WAS AVAILABLE. The
    cleanliness check is scoped to the two globs `collect()` reads, so a dirty
    file elsewhere — including one a directory deeper than the glob — leaves
    the true pin in place."""
    repo = corpus_repo(tmp_path)
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _write(repo, "README.md", "unrelated edit\n")
    _write(repo, "ideation/brainstorm/inbox/deep.md", "not read by collect\n")
    assert _bootstrap().git_generation(repo)["source_revision"] == head


# =========================================================================
# the consumers
# =========================================================================

def test_the_guards_recognize_every_member_and_not_just_one_spelling():
    """THE MEASURED LATENT RAISE, closed. Before the guards consulted the
    declaration, `git_blob_sha256` answered None for `"uncommitted"` and RAISED
    `SupportError: invalid repository revision` for the other four — including
    `uncommitted-worktree`, which six archived manifests carry."""
    support = _support()
    for member in ps.SENTINELS:
        assert support.git_blob_sha256(REPO_ROOT, member.value,
                                       "README.md") is None, member.value
    assert support.git_blob_sha256(
        REPO_ROOT, "composed:openxFactory@main:" + "a" * 40,
        "README.md") is None


def test_an_undeclared_revision_still_raises():
    """The repair widens the guards to the declaration, not to anything that
    is not a commit: a value that is neither a commit name nor a declared
    member is still refused, which is the behaviour that catches a corrupt
    manifest."""
    support = _support()
    with pytest.raises(support.SupportError):
        support.git_blob_sha256(REPO_ROOT, "not-a-revision", "README.md")


def test_repo_revision_still_means_the_unreadable_repository(tmp_path):
    """`repo_revision` is deliberately UNCHANGED. It returns `"uncommitted"` on
    a non-zero exit from `rev-parse HEAD` and on nothing else, which is exactly
    the condition Q1 ruled that spelling names. It is not a dirty-tree stamp,
    and the dirty-tree branch is not added here: this mover already refuses to
    record a pin the content contradicts, so it has no untrue pin to repair."""
    support = _support()
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    assert support.repo_revision(outside) == ps.UNCOMMITTED
    assert ps.declared(support.repo_revision(outside)).condition == \
        ps.UNREADABLE_REPOSITORY

    inside = _init(tmp_path / "real")
    _write(inside, "a.md", "x\n")
    head = _commit(inside)
    assert support.repo_revision(inside) == head


# =========================================================================
# the real repository
# =========================================================================

def test_the_seven_committed_sentinels_all_classify_as_legal_non_pins():
    """The inventory the packet declared, re-measured here rather than
    inherited: six `uncommitted-worktree` and one `not-applicable-ad-hoc`, all
    archived, all inside the `proposal-support-manifest` member's globs, and
    every one of them INVISIBLE before this existed."""
    report = pc.verify(REPO_ROOT, allow_remote=False)
    values = sorted(r.site.value for r in report.legal_non_pins)
    assert values == ([ps.NOT_APPLICABLE_AD_HOC]
                      + [ps.UNCOMMITTED_WORKTREE] * 6), values
    assert all(r.site.member_id == "proposal-support-manifest"
               for r in report.legal_non_pins)
    assert all("openspec/changes/archive/" in r.site.path
               for r in report.legal_non_pins)


def test_the_three_truncated_manifests_are_recognized_absences():
    """The fourth state, named and never converted. All three are visibly
    truncated stubs inside archived packets, and none of them is filled in with
    a sentinel."""
    report = pc.verify(REPO_ROOT, allow_remote=False)
    paths = sorted(a.path for a in report.absent_keys)
    assert len(paths) == 3, paths
    assert all(p.startswith("openspec/changes/archive/") for p in paths)
    assert all(a.member_id == "proposal-support-manifest"
               for a in report.absent_keys)


def test_the_defect_branch_reports_nothing_against_committed_output():
    """THE SEEDING OBLIGATION (Q3), and the reason it is a requirement rather
    than a preference. A verification that launches by reporting a lane's own
    committed output as a defect teaches its readers that the finding is noise,
    and the first thing a reader does with a noisy finding is stop reading it.
    Every non-commit spelling the corpus carries under a declared pin key is
    resolved: declared where it names a real condition, or excluded by a
    declaration with a stated reason where the file makes no provenance claim
    about itself."""
    report = pc.verify(REPO_ROOT, allow_remote=False)
    assert report.undeclared_values == [], [
        (r.site.path, r.site.key, r.site.value)
        for r in report.undeclared_values]
    assert report.uncovered_non_pins == ()
    assert report.declaration_defects == ()


def test_the_lanes_that_emit_undeclared_spellings_are_seeded():
    """The two lanes Q3 named, checked at the VALUES rather than at the
    declaration: everything the snapshot registry and the avatar F0 lane can
    write into a pin key is a declared member, so the defect branch cannot flag
    their own output the day it is switched on."""
    for emitted in (ps.UNKNOWN, ps.COMPOSED,
                    "composed:openxFactory@main:" + "b" * 40):
        assert ps.is_declared_sentinel(emitted), emitted


def test_the_pin_counts_did_not_move_and_no_site_is_classified_twice():
    """§ 3.5's expected shape, asserted: the same site and member counts with
    the sentinel sites moved from INVISIBLE to legal non-pins, no new uncovered
    site, nothing vanished and nothing arrived. Read from the report rather
    than from a summary string, so a change to the rendering cannot silence it.

    The reachability VERDICTS are deliberately not asserted here: three of them
    resolve through the retention namespace on the remote, and this test runs
    with `allow_remote=False` so it answers the same way on a machine with no
    network. What it does assert is the separation the design turns on — the
    commit path and the classification path never see the same site."""
    report = pc.verify(REPO_ROOT, allow_remote=False)
    # 68, not the 66 this census landed with. A `supporting-docs/manifest.yaml`
    # carries a `source_revision`, and that key is a declared
    # `proposal-support-manifest` pin site — so EVERY manifest written moves this
    # number by one, by design. The 67th is `add-worker-enrollment-broker`'s,
    # written when the `worker-enrollment-broker` topic was promoted in full.
    #
    # THE 68TH IS THE FIRST THAT NO PROMOTION PRODUCED, and the distinction is
    # worth the two lines because the comment above used to say "every full
    # promotion" as though promotion were the only writer.
    # `add-signed-execution-chain` is tranche ONE of a three-tranche staged topic
    # whose remaining two tranches need both staged documents, so it selected
    # ZERO files and its manifest carries an empty `files` list. It exists
    # anyway, because `release-realization`'s "Origin retention at archive"
    # scenario expects a staged origin's readable support manifest to carry the
    # identical origin id and path, and a packet with no manifest gives that gate
    # nothing to read. A zero-selection manifest still pins a `source_revision`,
    # so it still lands here.
    #
    # Only the SITE count moves: the member count is unchanged because the class
    # already had other manifests in it, and `lost`/`uncovered`/`vanished`/
    # `arrived` are untouched. Note this test cannot see an uncommitted manifest —
    # `pc.verify` reads the committed tree — so a packet's own pre-commit run
    # passes and CI is where the count lands.
    assert len(report.results) == 68
    assert len({r.site.member_id for r in report.results}) == 23
    assert len(report.lost) == 1
    assert len(report.lost_awaiting_record) == 0
    assert report.uncovered == ()
    assert report.vanished == ()
    assert report.arrived == ()

    pinned = {(r.site.path, r.site.key, r.site.line) for r in report.results}
    classified = {(r.site.path, r.site.key, r.site.line)
                  for r in report.non_pins}
    assert pinned & classified == set()
    assert all(pc.FULL_SHA_RE.match(r.site.pin) for r in report.results)


def test_pin_class_still_loads_by_path_with_no_package():
    """MEASURED IN CI, NOT ANTICIPATED. `tests/review_lane_pin/
    test_review_lane_caller.py` loads `pin_class.py` with
    `spec_from_file_location` under a private name and NO package — deliberately,
    so it need not duplicate this directory's conftest `sys.path` insert — and
    its docstring states the constraint that the module stays stdlib-only and
    importable that way. A bare `from . import pin_sentinels` raised
    `ImportError: attempted relative import with no known parent package` there
    and reddened the full suite while this directory's own run stayed green.
    Asserted here as well, so the constraint is visible from the suite a
    realizer actually runs."""
    name = "_pin_class_no_package_probe"
    source = REPO_ROOT / "scripts/doc_health/pin_class.py"
    spec = importlib.util.spec_from_file_location(name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
        assert len(module.pin_sentinels.SENTINELS) == len(ps.SENTINELS)
        assert module.pin_sentinels.is_declared_sentinel(
            ps.UNCOMMITTED_WORKTREE)
    finally:
        sys.modules.pop(name, None)


def test_no_deterministic_check_family_is_added():
    """The verification rides the readiness-proof surface, exactly as the pin
    class does, and the family enumeration and its numerals are untouched. Same
    three-way shape the pin class's own test uses: no family names it, no
    `fam_*` function exists to be registered, and the registry cannot reach the
    module."""
    from doc_health import families
    assert not [f for f in families.FAMILIES if "sentinel" in f]
    assert not [name for name in dir(ps) if name.startswith("fam_")]
    source = (REPO_ROOT / "scripts/doc_health/families.py").read_text("utf-8")
    assert "pin_sentinels" not in source, (
        "the vocabulary must not be reachable from the family registry, or a "
        "later edit registers it as a family without deciding to")
