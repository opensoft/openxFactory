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

import importlib.util
import subprocess

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
    """THE POINT THE PACKET LEFT TO REALIZATION, decided on measurement under
    the same-condition rule the delta states rather than on the resemblance.

    Three call sites emit `"unknown"` and they do not name one condition:
    `snapshot_registry.index_entry` projects an index entry whose recorded
    revision is absent while the repository is perfectly readable;
    `avatar_f0.cli._git_head` means `rev-parse HEAD` answered nothing, which IS
    the unreadable-repository condition; and `avatar_f0.cli._git_file_commit`
    returns it when `git log -1 -- <path>` succeeds and finds no commit, which
    means the repository is readable, HEAD resolves, and the named content has
    simply never been committed. Two spellings fold into one condition only if
    measurement shows ONE condition, and this measurement shows three — so
    `"unknown"` is declared as its own weakest member instead."""
    unknown = ps.declared(ps.UNKNOWN)
    assert unknown is not None
    assert unknown.condition == ps.UNESTABLISHED_REVISION
    assert unknown.condition != ps.UNREADABLE_REPOSITORY
    assert unknown.standing == ps.CANONICAL
    # the three measured call sites, still spelled as the decision read them
    registry = (REPO_ROOT / "scripts/ideation_dashboard/snapshot_registry.py"
                ).read_text(encoding="utf-8")
    assert 'self.source_revision or "unknown"' in registry
    lane = (REPO_ROOT / "experiments/avatar-brokered-call/src/avatar_f0/cli.py"
            ).read_text(encoding="utf-8")
    assert 'out.stdout.strip() or "unknown"' in lane


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
    assert len(report.results) == 66
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
