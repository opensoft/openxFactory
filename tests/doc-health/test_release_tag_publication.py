"""The twenty-third family: release-tag publication.

EVERY FIXTURE HERE IS A REAL GIT REPOSITORY WITH REAL TAGS, and that is the
point rather than an indulgence. This family's whole subject is the difference
between an annotated tag object and a lightweight ref, and between a published
ref and a local one — distinctions that exist in git and nowhere else. A fixture
that faked a tag as a string in a manifest would exercise the parser and prove
nothing about the family, so each repository below is initialised, committed to,
tagged and PUSHED TO AN ORIGIN, because `tag_ref` reads the published refs
deliberately.

THE SPENT STATE'S FIXTURES ARE THE SAME REPOSITORIES WITH A REAL CHANGELOG IN
THEM, for the same reason. The declaration is read from a BLOB AT THE PUBLISHED
TIP, so a fixture that handed the reader a string would never exercise the read
this state's own skip scenario is about. `_declare` therefore seeds
`contracts/CHANGELOG.md` on the first cut of every fixture repository, and
`_changelog` rewrites it with real `## contract-vX.Y` entries — which is what
makes the CONTAINMENT rule (a declaration is accepted only inside its
superseding bundle's own entry) testable at all.
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest

from conftest import FakeGit, REPO_ROOT
from doc_health import ERROR, INFO, WARNING, Skip
from doc_health import release_tag_publication as rtp
from doc_health import report
from doc_health.corpus import RealGit

MANIFEST = rtp.MANIFEST
CHANGELOG = rtp.CHANGELOG


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


_BASELINE_CHANGELOG = ("# Contract changelog\n\nNo bundle has been disposed "
                       "of here.\n")


def _declare(repo: Path, bundle: str | None, message: str) -> str:
    (repo / "contracts").mkdir(exist_ok=True)
    body = f"contract_bundle_version: {bundle}\n" if bundle else "other: 1\n"
    (repo / MANIFEST).write_text(body)
    _git(repo, "add", MANIFEST)
    if not (repo / CHANGELOG).exists():
        # THE CHANGELOG IS SEEDED ON THE FIRST CUT, NOT LEFT ABSENT, because
        # the family now reads it in the SAME `blobs_at` call as the manifest
        # and answers a blob it cannot read with a SKIP. A fixture with no
        # changelog is therefore a fixture the family declines to judge — which
        # is the correct behaviour and would make every other assertion in this
        # file vacuous. The baseline body carries NO declaration, so the
        # default state every pre-SPENT test asserts is unchanged.
        (repo / CHANGELOG).write_text(_BASELINE_CHANGELOG)
        _git(repo, "add", CHANGELOG)
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _cut(repo: Path, bundle: str, message: str | None = None) -> str:
    """Declare `bundle` AND write its release inventory.

    The inventory is what makes a bundle ENUMERABLE in `cut_bundles`, so
    "cut" and "declared" are two different fixture acts and this helper is the
    one that performs both. Every SPENT scenario turns on the difference.
    """
    (repo / "contracts/releases").mkdir(parents=True, exist_ok=True)
    inventory = f"contracts/releases/{bundle}.digests.yaml"
    (repo / inventory).write_text(f"bundle: {bundle}\n")
    _git(repo, "add", inventory)
    return _declare(repo, bundle, message or f"cut {bundle}")


def _spent_line(subject: str, superseding: str = "contract-v3.0", *,
                cause: str = "declared ADDITIVE over a refusing tree, which no "
                             "completion commit can cure",
                author: str = "Brett Heap", ruled: str = "2026-09-02",
                measurement: str = "PR #565 comment `5502452624`") -> str:
    """One line in the reserved form, built from its parts so that a test can
    remove exactly one element and assert the family names that element."""
    return (f"{rtp.SPENT_OPENER} `{subject}` — SUPERSEDED BY `{superseding}`"
            f" — CAUSE: {cause}"
            f" — RULED BY {author}, {ruled}"
            f" — MEASUREMENT: {measurement}")


def _changelog(repo: Path, entries, message: str = "changelog") -> None:
    """Write and commit a changelog from `[(entry bundle | None, [lines])]`.

    An `entry` of None writes its lines OUTSIDE any release entry, which is the
    only way to fixture a declaration with no containing entry at all.
    """
    out = ["# Contract changelog", ""]
    for entry, lines in entries:
        if entry is not None:
            out.append(f"## {entry} — 2026-09-02 (an entry)")
            out.append("")
        for line in lines:
            out.append(line)
            out.append("")
    (repo / CHANGELOG).write_text("\n".join(out) + "\n")
    _git(repo, "add", CHANGELOG)
    _git(repo, "commit", "-q", "-m", message)


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
                        b"contract_bundle_version: contract-v2.0\n",
                        # The changelog blob is supplied because the family
                        # reads it at the same commit and SKIPS on a blob it
                        # cannot read — without it this fixture would exercise
                        # the changelog guard instead of the tag-ref one.
                        ("r", CHANGELOG): b"# no declaration here\n"})
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


# ============================================================================
# THE THIRD STATE — SPENT (`declare-spent-bundle-state`, ratified 2026-09-02)
#
# THIRTEEN NEW SCENARIOS, AND EVERY ONE OF THEM CARRIES ITS POSITIVE CONTROL,
# which in this state's case is a single removal: the same fixture with the
# declaration taken out MUST return the superseded `error`. A test that only
# saw the `info` could not distinguish a working reader from a family that had
# stopped reporting the bundle for some other reason, and "main went green
# because an undeclared bundle started passing" is precisely the failure this
# state is built to make impossible.
# ============================================================================

# --------------------------------------------------- the reader, on its own

def test_the_reserved_form_parses_into_its_four_elements():
    text = ("# c\n\n## contract-v3.0 — 2026-09-02\n\n"
            + _spent_line("contract-v2.6") + "\n")
    read = rtp.read_spent_declarations(text.encode())
    assert set(read) == {"contract-v2.6"}
    decl = read["contract-v2.6"]
    assert decl.superseding == "contract-v3.0", (
        "the backticks are the FORM's, not the name's — a reader that kept "
        "them would never match a bundle name")
    assert decl.entry == "contract-v3.0"
    assert "completion commit" in decl.cause
    assert (decl.author, decl.date) == ("Brett Heap", "2026-09-02")
    assert "5502452624" in decl.measurement
    assert decl.missing == () and decl.defect is None and decl.count == 1


def test_the_reader_accepts_bytes_because_blobs_at_answers_bytes():
    """The module's own rule, one document over: `blobs_at` answers raw blob
    bytes, so every reader in this family takes bytes."""
    line = _spent_line("contract-v2.6")
    body = f"## contract-v3.0 — x\n\n{line}\n"
    assert (rtp.read_spent_declarations(body.encode())
            == rtp.read_spent_declarations(body))


def test_a_mis_encoded_byte_elsewhere_does_not_crash_the_read():
    body = ("## contract-v3.0 — x\n\nprose \xff\xfe more prose\n\n"
            + _spent_line("contract-v2.6") + "\n").encode("utf-8", "replace")
    assert "contract-v2.6" in rtp.read_spent_declarations(body)


def test_no_changelog_bytes_read_as_no_declaration_and_the_skip_is_the_caller_s():
    """The PURE reader answers `{}` for empty bytes. Turning "I could not read
    it" into a SKIP is `check_repo`'s job and is tested there — the two must
    not be the same function, or the conflation has nowhere to be caught."""
    assert rtp.read_spent_declarations(None) == {}
    assert rtp.read_spent_declarations(b"") == {}
    assert rtp.read_spent_declarations(b"## contract-v3.0\n\nno marker\n") == {}


def test_the_reserved_opener_not_completing_the_form_is_malformed_not_prose():
    """THE OPENER IS RESERVED. A line beginning with it that does not complete
    the form is a MALFORMED DECLARATION, never prose to be ignored — a family
    that fell back to "not a declaration" would let a typo in the record read
    as no record at all."""
    read = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{rtp.SPENT_OPENER} something informal\n"
        .encode())
    assert set(read) == {None}, (
        "a line with an unreadable SUBJECT is keyed under None, which is the "
        "one line of this state that names no bundle")
    assert "names no subject" in read[None].defect


def test_an_EMPTY_backtick_pair_carries_a_defect_and_not_a_bare_None():
    """FOUND IN SELF-REVIEW BEFORE THE BOTS. A line whose subject is an empty
    backtick pair keys under `None` like an unreadable one — and the finding
    the ladder raises for that key INTERPOLATES `declaration.defect`, so a
    `None` there would print the word "None" into a finding a human has to act
    on. Every `None`-keyed declaration therefore carries a defect string."""
    read = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{rtp.SPENT_OPENER} `` — CAUSE: c\n".encode())
    assert set(read) == {None}
    assert read[None].defect and "EMPTY backtick pair" in read[None].defect
    assert "None" not in read[None].defect


def test_a_misspelt_keyword_is_not_read_as_the_keyword():
    """`RULED BYE …` must not match `RULED BY` and yield the value `E …`. The
    two keywords that end in a letter rather than a colon need the boundary
    check the colon already gives the other two."""
    line = _spent_line("contract-v2.6").replace(" — RULED BY ", " — RULED BYE ")
    decl = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{line}\n".encode())["contract-v2.6"]
    assert "ruling" in decl.missing, decl
    assert decl.author is None and decl.date is None


def test_elements_OUT_OF_ORDER_are_malformed_rather_than_reported_missing():
    """The cause is right there; saying it is missing would send a reader
    looking for text the line already carries."""
    good = _spent_line("contract-v2.6")
    head, _, tail = good.partition(" — SUPERSEDED BY ")
    superseding, _, rest = tail.partition(" — CAUSE: ")
    cause, _, ruling = rest.partition(" — RULED BY ")
    swapped = (f"{head} — CAUSE: {cause} — SUPERSEDED BY {superseding}"
               f" — RULED BY {ruling}")
    decl = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{swapped}\n".encode())["contract-v2.6"]
    assert decl.defect and "does not define" in decl.defect
    refusal = rtp.spent_refusal(decl, "contract-v2.6",
                                {"contract-v2.6", "contract-v3.0"})
    assert "MALFORMED" in refusal and "OMITS" not in refusal


def test_an_omitted_element_is_NAMED_rather_than_making_the_line_unreadable():
    for dropped, owed in (("MEASUREMENT", "measurement of record"),
                          ("CAUSE", "cause"),
                          ("RULED BY", "ruling")):
        line = _spent_line("contract-v2.6")
        head, _, _ = line.partition(f" — {dropped}")
        read = rtp.read_spent_declarations(
            f"## contract-v3.0 — x\n\n{head}\n".encode())
        decl = read["contract-v2.6"]
        assert owed in decl.missing, (dropped, decl.missing)


def test_an_empty_element_counts_as_missing_not_as_present():
    line = _spent_line("contract-v2.6", cause="")
    decl = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{line}\n".encode())["contract-v2.6"]
    assert "cause" in decl.missing


def test_a_ruling_without_a_date_is_missing_its_date_specifically():
    line = _spent_line("contract-v2.6").replace(", 2026-09-02", "")
    decl = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{line}\n".encode())["contract-v2.6"]
    assert "ruling date" in decl.missing


def test_the_separator_is_reserved_WITHIN_the_line():
    """A CAUSE carrying the element separator splits the line into a segment
    the form does not define. Reported as malformed rather than guessed at:
    a family whose reading of a record depends on the record's punctuation is
    a family nobody can predict from its specification."""
    line = _spent_line("contract-v2.6", cause="one reason — and another")
    decl = rtp.read_spent_declarations(
        f"## contract-v3.0 — x\n\n{line}\n".encode())["contract-v2.6"]
    assert decl.defect and "separator is reserved" in decl.defect


def test_a_declaration_outside_every_release_entry_carries_no_entry():
    decl = rtp.read_spent_declarations(
        f"# c\n\n{_spent_line('contract-v2.6')}\n".encode())["contract-v2.6"]
    assert decl.entry is None


def test_two_declarations_naming_one_bundle_are_COUNTED_not_collapsed():
    body = (f"## contract-v3.0 — x\n\n{_spent_line('contract-v2.6')}\n\n"
            f"{_spent_line('contract-v2.6', cause='a second story')}\n")
    decl = rtp.read_spent_declarations(body.encode())["contract-v2.6"]
    assert decl.count == 2
    assert rtp.spent_refusal(decl, "contract-v2.6",
                             {"contract-v2.6", "contract-v3.0"})


# ------------------------------------------- the ladder, over real fixtures

def _spent_fixture(tmp_path: Path, name: str = "spent", *,
                   declaration: str | None = None,
                   entry: str = "contract-v3.0",
                   publish_successor: bool = True):
    """THE `contract-v2.6` SHAPE, as a fixture: a bundle cut and never tagged,
    a later bundle cut on top of it, and the declaration inside the later
    bundle's own changelog entry."""
    repo, _ = _repo(tmp_path, name)
    _cut(repo, "contract-v2.6")
    _cut(repo, "contract-v3.0")
    if publish_successor:
        _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    lines = [declaration] if declaration is not None else []
    _changelog(repo, [(entry, lines)])
    _push(repo)
    return repo


def test_a_superseded_bundle_declared_SPENT_with_a_published_successor_is_an_info(tmp_path):
    """THE ACCEPTED BAND, AND THE RED-FIRST PROOF IS THE SECOND HALF OF THIS
    TEST rather than a separate one, so the two readings can never drift: the
    SAME fixture, with the declaration removed, MUST return the `error`.

    This is `declare-spent-bundle-state` task 2.1's verification in test form.
    `main` goes green because `contract-v2.6` is EXPLICITLY DECLARED spent, and
    never because an undeclared bundle started passing.
    """
    repo = _spent_fixture(tmp_path, declaration=_spent_line("contract-v2.6"))
    findings = _check(repo)
    assert len(findings) == 1, [f.rule for f in findings]
    spent = findings[0]
    assert spent.severity == INFO
    assert spent.path == "contracts/releases/contract-v2.6.digests.yaml", (
        "the finding's identity is its PATH, and the per-bundle inventory is "
        "the one path unique to the bundle by construction")
    assert spent.resolution == "contested"
    assert "contract-v2.6 is SPENT" in spent.rule
    assert "contract-v3.0" in spent.rule
    assert CHANGELOG in spent.rule, "the reader is owed WHERE the record is"
    assert "Brett Heap, 2026-09-02" in spent.rule
    assert "EXTINGUISHED" in spent.rule and "MET" in spent.rule
    assert "SUPERSEDED without ever being published" not in spent.rule

    # THE POSITIVE CONTROL — the declaration removed, nothing else touched.
    bare = _spent_fixture(tmp_path, "control")
    control = _check(bare)
    assert [f.severity for f in control] == [ERROR]
    assert "SUPERSEDED without ever being published" in control[0].rule
    assert control[0].path == MANIFEST, (
        "the untouched arm keeps the identity it always had")


def test_a_SPENT_declaration_whose_successor_is_unpublished_is_ONE_warning(tmp_path):
    """PROVISIONAL IS NOT A REFUSAL, and it reports ONE finding, not two.

    Codex's round-3 P1: written as a non-acceptance, the ruled `warning` band
    was unreachable, because the fallback kept the superseded `error` for every
    declaration that was not accepted — so a conforming family would have
    reported BOTH through the successor's legitimate publication window,
    contradicting the ruling it encodes.
    """
    repo = _spent_fixture(tmp_path, declaration=_spent_line("contract-v2.6"),
                          publish_successor=False)
    findings = _check(repo)
    spent = [f for f in findings if "contract-v2.6" in f.rule]
    assert len(spent) == 1, [f.rule for f in spent]
    assert spent[0].severity == WARNING
    assert spent[0].path == "contracts/releases/contract-v2.6.digests.yaml"
    assert "UNPROVEN" in spent[0].rule
    assert "SUPERSEDED without ever being published" not in spent[0].rule

    # AND THE SUCCESSOR IS STILL GRADED ON ITS OWN ACCOUNT, which is what
    # bounds this band: the obligation moved rather than went away.
    successor = [f for f in findings if "contract-v3.0 is declared" in f.rule]
    assert len(successor) == 1 and successor[0].severity == WARNING


def test_a_SPENT_declaration_naming_a_successor_never_cut_is_refused(tmp_path):
    repo = _spent_fixture(
        tmp_path, declaration=_spent_line("contract-v2.6", "contract-v9.9"),
        entry="contract-v9.9")
    findings = _check(repo)
    refused = [f for f in findings if "NEVER CUT" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert refused[0].path == "contracts/releases/contract-v2.6.digests.yaml"
    # A BAD DECLARATION REMOVES NOTHING.
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_SPENT_declaration_naming_an_EARLIER_successor_is_refused(tmp_path):
    """OD-9, ADDED ON A CODEX P1 AND THE GUARD RATHER THAN AN EXTENSION OF IT.

    "Cut and published" is satisfiable BACKWARDS: a declaration for
    `contract-v2.6` written into `contract-v2.5`'s entry and naming
    `contract-v2.5` — cut, published, valid annotated tag on a declaring commit
    — passes every other mechanical check, and an untagged bundle would go
    quiet with NO replacement published at all.
    """
    repo, _ = _repo(tmp_path, "backwards")
    _cut(repo, "contract-v2.5")
    _git(repo, "tag", "-a", "contract-v2.5", "-m", "contract-v2.5")
    _cut(repo, "contract-v2.6")
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, [("contract-v2.5",
                       [_spent_line("contract-v2.6", "contract-v2.5")])])
    _push(repo)
    findings = _check(repo)
    refused = [f for f in findings if "NOT STRICTLY LATER" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert "walked around backwards" in refused[0].rule
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule], (
        "no untagged bundle goes quiet without a LATER published one")


def test_a_SPENT_declaration_whose_SUBJECT_was_never_cut_warns_on_the_changelog(tmp_path):
    """THE ONE FINDING OF THIS STATE WITH NO BUNDLE TO LAND ON, and the
    fail-closed behaviour a typo must not be able to defeat: the mistyped
    subject disposes nothing, and the bundle that really owes a tag is still
    reported."""
    repo = _spent_fixture(tmp_path,
                          declaration=_spent_line("contract-v2.66"))
    findings = _check(repo)
    orphan = [f for f in findings if "DISPOSES NOTHING" in f.rule]
    assert len(orphan) == 1
    assert orphan[0].severity == WARNING
    assert orphan[0].path == CHANGELOG
    assert "contract-v2.66" in orphan[0].rule
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_SPENT_declaration_omitting_an_element_is_refused_in_its_own_words(tmp_path):
    """"A malformed declaration is worse than none: it looks like a record" —
    so the refusal MUST NOT borrow the absent-tag words."""
    line = _spent_line("contract-v2.6")
    truncated, _, _ = line.partition(" — MEASUREMENT")
    repo = _spent_fixture(tmp_path, declaration=truncated)
    findings = _check(repo)
    refused = [f for f in findings if "OMITS an element" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert refused[0].path == "contracts/releases/contract-v2.6.digests.yaml"
    assert "measurement of record" in refused[0].rule
    assert "no published annotated tag" not in refused[0].rule
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_SPENT_declaration_outside_its_successor_s_entry_is_refused(tmp_path):
    """THE DECLARING ACT IS THE SUPERSEDING BUNDLE'S OWN CHANGELOG ENTRY — the
    act that spends a number is the LATER CUT that allocates its
    replacement."""
    repo = _spent_fixture(tmp_path, declaration=_spent_line("contract-v2.6"),
                          entry="contract-v2.6")
    findings = _check(repo)
    refused = [f for f in findings if "sits in the contract-v2.6 entry" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert "LATER CUT" in refused[0].rule
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_bundle_cannot_declare_ITSELF_spent(tmp_path):
    """A bundle that could declare itself spent could decline to be published,
    which is the whole of what this family refuses."""
    repo = _spent_fixture(
        tmp_path,
        declaration=_spent_line("contract-v2.6", "contract-v2.6"),
        entry="contract-v2.6")
    findings = _check(repo)
    refused = [f for f in findings if "cannot declare ITSELF" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert "decline to be published" in refused[0].rule


def test_two_SPENT_declarations_naming_one_bundle_accept_NEITHER(tmp_path):
    """Two records of one disposition is how they come to disagree."""
    repo = _spent_fixture(tmp_path, declaration=None)
    _changelog(repo, [("contract-v3.0",
                       [_spent_line("contract-v2.6"),
                        _spent_line("contract-v2.6", cause="a second story")])],
               "two declarations")
    _push(repo)
    findings = _check(repo)
    refused = [f for f in findings if "2 SPENT declarations" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert not [f for f in findings if f.severity == INFO]
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_two_different_bundles_each_declared_SPENT_carry_two_identities(tmp_path):
    """CODEX'S OTHER P1, AND A SINGLE-BUNDLE TEST CANNOT SEE THE DEFECT IT
    FOUND. On a shared path the two `info`s would share one
    `(family, repo, path)` key, so removing ONE declaration would leave the
    surviving finding holding the identity and the removal would be reported by
    nothing."""
    repo, _ = _repo(tmp_path, "two")
    _cut(repo, "contract-v2.6")
    _cut(repo, "contract-v2.8")
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, [("contract-v3.0",
                       [_spent_line("contract-v2.6"),
                        _spent_line("contract-v2.8")])])
    _push(repo)
    findings = _check(repo)
    infos = [f for f in findings if f.severity == INFO]
    assert len(infos) == 2, [f.rule for f in findings]
    assert {f.path for f in infos} == {
        "contracts/releases/contract-v2.6.digests.yaml",
        "contracts/releases/contract-v2.8.digests.yaml"}
    assert len({f.match_key() for f in infos}) == 2
    assert all(f.resolution == "contested" for f in infos)


def test_a_SPENT_declaration_naming_the_CURRENTLY_declared_bundle_is_refused(tmp_path):
    """A repository declaring a bundle it also calls spent asserts two
    incompatible things about one number — and that bundle MUST continue to be
    graded by distance exactly as it is today."""
    repo, _ = _repo(tmp_path, "current")
    _cut(repo, "contract-v3.0")
    _changelog(repo, [("contract-v3.0", [_spent_line("contract-v3.0")])])
    _land(repo, 7)
    _push(repo)
    findings = _check(repo)
    refused = [f for f in findings if "which is the bundle" in f.rule]
    assert len(refused) == 1 and refused[0].severity == ERROR
    assert refused[0].path == "contracts/releases/contract-v3.0.digests.yaml"
    graded = [f for f in findings if "NOT PUBLISHED" in f.rule]
    assert len(graded) == 1 and graded[0].severity == ERROR, (
        "the distance grading of the declared bundle is untouched")
    assert not [f for f in findings if f.severity == INFO]


def test_a_SPENT_declaration_does_not_quiet_a_MISPLACED_tag(tmp_path):
    """THE SPENT STATE REACHES THE ABSENT-TAG ARM AND NOTHING ELSE. A tag that
    exists and points wrongly is the condition this family already calls worse
    than absence."""
    repo, _ = _repo(tmp_path, "misplaced")
    elsewhere = _cut(repo, "contract-v2.5")
    _cut(repo, "contract-v2.6")
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v2.6", elsewhere, "-m", "misplaced")
    _changelog(repo, [("contract-v3.0", [_spent_line("contract-v2.6")])])
    _push(repo)
    findings = _check(repo)
    about = [f for f in findings if "contract-v2.6" in f.rule]
    assert len(about) == 1
    assert about[0].severity == ERROR and "MISPLACED" in about[0].rule
    assert about[0].path == MANIFEST
    assert not [f for f in findings if f.severity == INFO]
    # AND THE CONTROL: the same tree with contract-v2.5 also untagged shows the
    # v2.5 bundle taking the superseded error, so the fixture is not silent by
    # accident.
    assert [f for f in findings if "contract-v2.5 was cut and SUPERSEDED" in f.rule]


def test_a_SPENT_declaration_does_not_quiet_a_LIGHTWEIGHT_ref(tmp_path):
    repo, _ = _repo(tmp_path, "lightweight")
    _cut(repo, "contract-v2.6")
    _git(repo, "tag", "contract-v2.6")          # no -a: lightweight
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, [("contract-v3.0", [_spent_line("contract-v2.6")])])
    _push(repo)
    findings = _check(repo)
    about = [f for f in findings if "contract-v2.6" in f.rule]
    assert len(about) == 1
    assert about[0].severity == ERROR and "LIGHTWEIGHT" in about[0].rule
    assert not [f for f in findings if f.severity == INFO]


def test_an_unreadable_changelog_at_the_published_tip_SKIPS_naming_that_read():
    """THE #338 CONFLATION, ONE DOCUMENT OVER. "I could not read the changelog"
    and "the changelog carries no declaration" arrive identically from
    `blobs_at` and mean opposite things. Not fetched is not an answer, in
    either direction."""
    class NoChangelog(FakeGit):
        def ls_tree_paths(self, repo, ref, prefix):
            return []

    git = NoChangelog(
        remotes={"r": "tip"},
        tag_refs={},
        blobs={("r", MANIFEST): b"contract_bundle_version: contract-v2.0\n"})
    out = rtp.check_repo("alphaFactory", Path("r"), git)
    assert isinstance(out, Skip)
    assert CHANGELOG in out.reason
    assert "could not be read at the published tip" in out.reason
    assert "carrying no SPENT declaration" in out.reason
    # THE POSITIVE CONTROL: the same shim WITH the blob gets PAST this guard,
    # so the skip above is the changelog read's and not a broken fixture's.
    # (It then skips further down for a reason of its own — this shim declares
    # no first-parent walk — which is why the control asserts the REASON moved
    # rather than that no skip remains.)
    git.blobs[("r", CHANGELOG)] = b"# no declaration\n"
    control = rtp.check_repo("alphaFactory", Path("r"), git)
    assert isinstance(control, Skip) and CHANGELOG not in control.reason


def test_the_state_is_not_read_backwards_onto_published_or_legacy_bundles(tmp_path):
    """NO RETROFIT. The five bundles § Untagged Bundles After Enforcement Began
    records were all publishable and all published: they carry annotated tags
    on declaring commits and never reach this arm. Neither does any bundle
    below the enforcement line."""
    repo, _ = _repo(tmp_path, "noretro")
    _cut(repo, "contract-v1.5")                 # below the floor, no tag
    published = _cut(repo, "contract-v1.33")
    _git(repo, "tag", "-a", "contract-v1.33", published, "-m", "published")
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, [("contract-v3.0",
                       [_spent_line("contract-v1.5"),
                        _spent_line("contract-v1.33")])])
    _push(repo)
    findings = _check(repo)
    assert not [f for f in findings if f.severity == INFO], (
        "a declaration must not reach a published bundle or one below the "
        "floor: neither arm is the ABSENT arm")
    assert findings == [], [f.rule for f in findings]


# --------------------------------- OQ-3 and the per-bundle identity, proved

def _render(findings):
    return report.render(date(2026, 9, 2), findings, [], [], [], 0, [], [])


def test_a_contested_spent_info_that_vanishes_raises_an_uncited_resolution(tmp_path):
    """OQ-3, PROVED RATHER THAN INHERITED. `uncited_resolutions` is
    severity-agnostic as written, but it had never been exercised by a
    contested `info`; OD-5's whole class choice rests on it, so it is measured
    here. If this ever reds, the class choice returns to the owner as a
    question rather than being quietly dropped."""
    repo = _spent_fixture(tmp_path, declaration=_spent_line("contract-v2.6"))
    before = _check(repo)
    assert [f.severity for f in before] == [INFO]

    text = _render(before)
    keys, contested = report.parse_previous(text)
    assert contested == {before[0].match_key()}, (
        "an `info` classed contested must reach the contested set — the plan "
        "row carries the class for every severity")

    raised = report.uncited_resolutions([], contested, dispositions=set())
    assert [f.family for f in raised] == ["uncited-resolution"]
    assert raised[0].path == "contracts/releases/contract-v2.6.digests.yaml"


def test_removing_ONE_of_two_spent_declarations_raises_only_ITS_uncited_resolution(tmp_path):
    """THE CODEX REPAIR, PROVED WITH TWO BUNDLES — a single-bundle test cannot
    see the defect it found. On a shared path the surviving finding would hold
    the identity and the removal would be reported by nothing."""
    repo, _ = _repo(tmp_path, "twokeys")
    _cut(repo, "contract-v2.6")
    _cut(repo, "contract-v2.8")
    _cut(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, [("contract-v3.0",
                       [_spent_line("contract-v2.6"),
                        _spent_line("contract-v2.8")])])
    _push(repo)
    _, contested = report.parse_previous(_render(_check(repo)))
    assert len(contested) == 2

    # ONE declaration withdrawn; the other stands.
    _changelog(repo, [("contract-v3.0", [_spent_line("contract-v2.8")])],
               "withdraw one")
    _push(repo)
    after = _check(repo)
    raised = report.uncited_resolutions(after, contested, dispositions=set())
    assert [f.path for f in raised] == [
        "contracts/releases/contract-v2.6.digests.yaml"], (
        "exactly the withdrawn bundle's identity vanished, and exactly one "
        "uncited-resolution is owed")
    assert [f for f in after if f.severity == INFO]
    assert [f for f in after
            if "contract-v2.6 was cut and SUPERSEDED" in f.rule], (
        "and the bundle whose declaration was withdrawn is reported again")


def test_a_disposition_citing_the_change_silences_the_uncited_resolution(tmp_path):
    """The other half of the contested class, so the test above cannot be read
    as "a spent state can never be retired": a CITED resolution is accepted."""
    repo = _spent_fixture(tmp_path, declaration=_spent_line("contract-v2.6"))
    _, contested = report.parse_previous(_render(_check(repo)))
    key = next(iter(contested))
    assert report.uncited_resolutions([], contested,
                                      dispositions={key}) == []
