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


def _declare(repo: Path, bundle: str | None, message: str) -> str:
    """A cut: the manifest declares `bundle`, and a changelog exists to read.

    THE CHANGELOG IS SEEDED HERE BECAUSE IT IS NOW A SECOND READ AT THE SAME
    COMMIT (`declare-spent-bundle-state`). `blobs_at` answers None per path for
    a blob it cannot read, and the family turns that into a SKIP naming the read
    rather than into "there is no SPENT declaration" — so a fixture with no
    `contracts/CHANGELOG.md` would skip every scenario below instead of
    exercising it. Seeded once and only if absent, so `_changelog` can replace
    it with real entries without this helper overwriting them on the next cut.
    """
    (repo / "contracts").mkdir(exist_ok=True)
    body = f"contract_bundle_version: {bundle}\n" if bundle else "other: 1\n"
    (repo / MANIFEST).write_text(body)
    paths = [MANIFEST]
    if not (repo / CHANGELOG).exists():
        (repo / CHANGELOG).write_text("# Contract changelog\n")
        paths.append(CHANGELOG)
    _git(repo, "add", *paths)
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _inventory(repo: Path, *bundles: str) -> None:
    """A release inventory per bundle — the machine-readable fact that a bundle
    was CUT, which is what makes it enumerable at all and, since OD-5, what
    gives every finding of the SPENT state a path unique to its bundle."""
    (repo / "contracts" / "releases").mkdir(parents=True, exist_ok=True)
    for bundle in bundles:
        (repo / rtp.inventory_path(bundle)).write_text(f"bundle: {bundle}\n")
        _git(repo, "add", rtp.inventory_path(bundle))
    _git(repo, "commit", "-q", "-m", f"inventories: {', '.join(bundles)}")


def _spent_line(subject: str | None = "contract-v2.6",
                superseding: str | None = "contract-v3.0",
                cause: str | None = "never verifiable and additive over a "
                                    "refusing tree",
                author: str | None = "Brett Heap",
                ruled_on: str | None = "2026-09-02",
                measurement: str | None = "PR #565 comment 5502452624") -> str:
    """The reserved single-line form, with any element omittable.

    ONE BUILDER FOR THE FORM, so a test that omits an element differs from a
    test that supplies it by exactly that element and nothing else — and so a
    change to the form is made in one place rather than in fourteen literals
    that would then disagree about what the form is.
    """
    subject_part = f" `{subject}`" if subject is not None else ""
    line = f"**SPENT BUNDLE:**{subject_part}"
    if superseding is not None:
        line += f" — SUPERSEDED BY `{superseding}`"
    if cause is not None:
        line += f" — CAUSE: {cause}"
    if author is not None or ruled_on is not None:
        ruling = ", ".join(p for p in (author, ruled_on) if p is not None)
        line += f" — RULED BY {ruling}"
    if measurement is not None:
        line += f" — MEASUREMENT: {measurement}"
    return line


def _changelog(repo: Path, *entries: tuple[str, list[str]]) -> None:
    """`contracts/CHANGELOG.md` as `## <bundle>` entries carrying body lines.

    The ENTRY a declaration sits in is what decides whether the act was
    performed by the cut that allocated the replacement, so the fixture has to
    be able to put one line in one entry and another in another.
    """
    text = ["# Contract changelog", ""]
    for bundle, body in entries:
        text.append(f"## {bundle} — 2026-09-02 (a cut)")
        text.append("")
        text.extend(body)
        text.append("")
    (repo / CHANGELOG).write_text("\n".join(text) + "\n")
    _git(repo, "add", CHANGELOG)
    _git(repo, "commit", "-q", "-m", "changelog")


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
                        # The changelog read has to ANSWER for this fixture to
                        # reach the tag arm at all: a blob it cannot read is a
                        # skip naming that read, which is the scenario one test
                        # below and not this one.
                        ("r", CHANGELOG): b"# Contract changelog\n"})
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


# ============================================================ the SPENT state
#
# `declare-spent-bundle-state`, ratified 2026-09-02 by Brett Heap; openxFactory
# issue #575. THE THIRD STATE between *published* and *owes a tag*, entered ONLY
# by an explicit reserved-form declaration in `contracts/CHANGELOG.md` at the
# published tip and refused by every absence. Every fixture below is a real git
# repository for the reason the module header gives: the successor guard turns
# on the difference between an annotated tag object and a lightweight ref, and
# between a published ref and a local one.

# ---------------------------------------------------------------- the reader

def test_the_reserved_form_reads_five_elements_and_its_containing_entry():
    """The reader, as a pure function from changelog BYTES.

    Bytes in, per the module's own rule: `blobs_at` answers raw blob bytes
    because the release inventory's identity is computed over them, and a
    reader that demanded text would make its caller name a canonicalization.
    """
    doc = "\n".join([
        "# Contract changelog",
        "",
        "## contract-v3.0 — 2026-09-02 (BREAKING)",
        "",
        "### `contract-v2.6` disposition",
        "",
        _spent_line(),
        "",
        "## contract-v2.6 — 2026-09-01 (additive)",
        "",
        "left exactly as written",
    ])
    declarations = rtp.parse_spent_declarations(doc.encode("utf-8"))
    assert len(declarations) == 1
    got = declarations[0]
    assert got.subject == "contract-v2.6"
    assert got.superseding == "contract-v3.0"
    assert got.cause == "never verifiable and additive over a refusing tree"
    assert got.author == "Brett Heap"
    assert got.ruled_on == "2026-09-02"
    assert got.measurement == "PR #565 comment 5502452624"
    # THE CONTAINING ENTRY, which is what makes the act the SUPERSEDING bundle's
    # own and not the spent bundle's — a bundle that could declare itself spent
    # could decline to be published.
    assert got.entry == "contract-v3.0"
    assert got.missing == ()


def test_a_line_carrying_the_opener_and_nothing_else_names_every_missing_element():
    """REJECT RATHER THAN SKIP. The opener is RESERVED, so a line that begins
    with it and completes nothing is a MALFORMED DECLARATION rather than prose
    to be ignored: a malformed declaration is worse than none because it looks
    like a record."""
    got = rtp.parse_spent_declarations("**SPENT BUNDLE:**\n")
    assert len(got) == 1
    assert got[0].subject is None
    assert set(got[0].missing) == {
        "the superseding bundle", "the cause", "the ruling",
        "the measurement of record"}


def test_an_em_dash_inside_the_cause_does_not_move_which_element_is_missing():
    """THE READER IS LABEL-ANCHORED AND NEVER A SPLIT ON THE SEPARATOR.

    Splitting a declaration on " — " reads a cause carrying an em dash as three
    elements and then names the WRONG element as the missing one — handing an
    author the wrong repair for a defect that is right there. The cause below
    carries two em dashes and one element is genuinely absent.
    """
    line = _spent_line(cause="never verifiable — five mismatches — and additive",
                       measurement=None)
    got = rtp.parse_spent_declarations(line)[0]
    assert got.cause == "never verifiable — five mismatches — and additive"
    assert got.missing == ("the measurement of record",)


def test_the_ruling_is_one_element_with_two_halves_named_apart():
    """A clause carrying only one half is named for the half it is MISSING,
    because the repair for an absent date is not the repair for an absent
    author."""
    no_date = rtp.parse_spent_declarations(_spent_line(ruled_on=None))[0]
    assert no_date.missing == ("the ruling's date",)
    assert no_date.author is None and no_date.ruled_on is None
    no_author = rtp.parse_spent_declarations(_spent_line(author=None))[0]
    assert no_author.missing == ("the ruling's author",)
    absent = rtp.parse_spent_declarations(
        _spent_line(author=None, ruled_on=None))[0]
    assert absent.missing == ("the ruling",)


def test_junk_spliced_between_the_subject_and_the_form_is_malformed():
    """The gap the form admits is the separator and nothing else, so a line
    that reads plausibly and carries something extra is REFUSED rather than
    accepted on the strength of its labels."""
    line = _spent_line().replace(
        "`contract-v2.6` — SUPERSEDED BY",
        "`contract-v2.6` (probably) — SUPERSEDED BY")
    got = rtp.parse_spent_declarations(line)[0]
    assert "the reserved form's own shape" in got.missing


def test_no_declaration_at_all_reads_as_no_declarations():
    """An empty read is not an error: a changelog with no SPENT line is the
    steady state of every repository in the estate but one."""
    assert rtp.parse_spent_declarations(b"# Contract changelog\n") == []
    assert rtp.parse_spent_declarations(None) == []


# ------------------------------------------------- the containment boundaries
#
# THE CONTAINMENT RULE IS THE GUARD THE RATIFIED REQUIREMENT LEANS ON HARDEST:
# a declaration is accepted only where the entry CONTAINING it is the entry of
# the bundle it names. Every way of closing an entry the reader does not know
# about is therefore an ACCEPT — the declaration keeps the previous release
# entry's authority and quiets the `error` this family exists to raise. Ten such
# escapes were measured (PR #584's five bot rounds, compared against this module
# in that PR's 2026-09-02 17:05Z comment), and the tests below pin the rule as
# ONE TABLE plus the cases that table cannot express, rather than as a regex a
# reader must re-derive.

# A NON-BREAKING SPACE, NAMED RATHER THAN TYPED. Three rows below turn on
# U+00A0 being present, and a literal one in this file is a character an
# editor, a formatter or a copy-paste can normalise to an ordinary space —
# after which those rows would pass for the WRONG REASON, testing a plain
# `## contract-v3.0` heading and proving nothing about the rule they exist
# for. An escape cannot be normalised silently.
NBSP = "\u00a0"


def _entry_under(*between: str, base: str = "contract-v2.9") -> str | None:
    """The entry a declaration reads as sitting in, with `between` standing
    between the base entry's heading and the declaration.

    THE BASE IS NOT THE SUPERSEDING BUNDLE, DELIBERATELY. With `contract-v3.0`
    as both, "the candidate closed the entry" and "the candidate closed it and
    reopened it as v3.0" are the same observation — which is how the first two
    containment escapes survived tests written over them.
    """
    doc = "\n".join(["# Contract changelog", "",
                     f"## {base} — 2026-09-02 (a cut)", "",
                     *between, "", _spent_line()])
    read = rtp.parse_spent_declarations(doc.encode("utf-8"))
    assert len(read) == 1, "the fixture must yield exactly one declaration"
    return read[0].entry


BOUNDARY_TABLE = [
    # (what stands between the entry heading and the declaration, the entry
    #  the declaration is then contained by, why this row exists)
    ((), "contract-v2.9", "nothing between: the entry is simply open"),
    (("### `contract-v2.6` disposition",), "contract-v2.9",
     "H3 does NOT close, and this row is LOAD-BEARING: this repository's own "
     "reserved line lives inside exactly such a subsection"),
    (("#### deeper still",), "contract-v2.9", "nor does H4"),
    (("###",), "contract-v2.9", "nor an empty H3"),
    (("## Deprecations",), None,
     "a non-release H2 closes and opens nothing (Codex R1 P1)"),
    (("## contract-v3.0 — 2026-09-02 (a cut)",), "contract-v3.0",
     "a release H2 closes and OPENS its own"),
    (("## contract-v3.0.1",), None,
     "a longer name is not the v3.0 entry (Codex R2 P1)"),
    (("## contract-v3.0-notes",), None, "nor is a suffixed one"),
    (("## contract-v3.01",), "contract-v3.01",
     "but contract-v3.01 IS a well-formed name (major 3, minor 01) and opens "
     "its own entry; a declaration under it is refused for naming a DIFFERENT "
     "bundle, which is the honest reason"),
    (("# Notes",), None, "a level-one heading closes too (Codex R3 P1)"),
    (("#",), None, "including an empty one"),
    (("##",), None, "and an empty H2, which is a legal ATX heading"),
    (("  ## Notes",), None,
     "two leading spaces is still a heading under CommonMark (Codex R4 P1)"),
    (("   ## contract-v3.0 — a cut",), "contract-v3.0",
     "three too, and it still opens"),
    (("    ## Notes",), "contract-v2.9",
     "FOUR is an indented code block and is no heading at all — the other "
     "side of the same rule"),
    (("Notes", "=====",), None, "a Setext H1 closes (Codex, late)"),
    (("Notes", "-----",), None, "and a Setext H2"),
    (("", "-----",), "contract-v2.9",
     "but a run of dashes after a BLANK line is a thematic break, not an "
     "underline — over-closing past this point would refuse a declaration "
     "written correctly below a horizontal rule"),
    (("***", "---",), "contract-v2.9",
     "nor after a THEMATIC BREAK, where both lines are breaks and neither is "
     "a heading (Codex P2, round 1 on PR #589)"),
    (("___", "===",), "contract-v2.9", "in any of the three break characters"),
    (("===", "---",), None,
     "an underline-SHAPED line that underlined NOTHING is paragraph text, and "
     "the run below it IS a heading (Codex P1, round 2 on PR #589 — the hole "
     "the round-1 fix opened by excluding on syntax rather than on effect)"),
    (("Title", "===", "---",), None,
     "but a run below an underline that really DID underline is not a second "
     "heading, and the entry was already closed by the first"),
    (("| a | b |", "|---|---|",), "contract-v2.9",
     "and a table rule is not an underline either"),
    (("contract-v3.0", "=============",), None,
     "a Setext heading CLOSES and never OPENS: the requirement names `##` "
     "entries, and under-opening is the fail-closed half"),
    (("#550 example — validates green under the extended schemas", ),
     "contract-v2.9",
     "real text in this repository's changelog, and no heading: `#` followed "
     "immediately by a non-space is none"),
    ((f"##{NBSP}contract-v3.0 — a cut",), "contract-v2.9",
     "a NON-BREAKING SPACE after the marker is not CommonMark's space-or-tab, "
     "so the line is paragraph text and opens NO entry — it opened a "
     "FICTITIOUS one before (Codex P1, round 3 on PR #589)"),
    ((f"##{NBSP}Deprecations",), "contract-v2.9",
     "and the same line closes nothing either, which is the other half of the "
     "same rule rather than a second one"),
    ((f"## contract-v3.0{NBSP}notes",), None,
     "nor is a version token followed by a Unicode space a COMPLETE token; it "
     "closes, as any `##` heading does, and opens nothing"),
    (("##\tcontract-v3.0 — a cut",), "contract-v3.0",
     "but a TAB is CommonMark's separator and must still OPEN — the control "
     "against narrowing `\\s` all the way to a literal space, which is the "
     "hole the fix for the row above could have opened"),
    (("#\tNotes",), None, "and a tab-separated H1 must still CLOSE"),
]


@pytest.mark.parametrize("between,entry,why", BOUNDARY_TABLE,
                         ids=[row[2][:48] for row in BOUNDARY_TABLE])
def test_exactly_which_lines_close_a_changelog_entry_is_pinned(between, entry,
                                                               why):
    """ONE TABLE FOR THE WHOLE RULE. Each row is a line that may stand between
    a release entry's heading and a declaration, and the entry the declaration
    is then contained by — `None` meaning no entry at all, which is a
    containment refusal rather than a silent inheritance of the previous
    release's authority.

    The table is its own positive control: it carries the rows where the entry
    STAYS OPEN alongside those where it closes, so it cannot be satisfied by a
    reader that closes on everything any more than by one that closes on
    nothing.
    """
    assert _entry_under(*between) == entry, why


def test_a_fenced_block_is_opaque_to_headings_and_to_declarations():
    """THE ONE ESCAPE THE LIVE DOCUMENT COULD ALREADY HIT — `contracts/
    CHANGELOG.md` carries a fenced block — and the rule is stated in BOTH
    directions because it is fail-closed in both.

    A fenced `## contract-v3.0` must not reopen an entry (measured: it did, and
    a declaration under a later `## Notes` then read as contained by the v3.0
    entry and was ACCEPTED), and a declaration shown as an EXAMPLE inside a
    fence must not spend a bundle. A real declaration hidden inside a fence
    therefore does not count — which leaves the superseded `error` standing
    rather than quieting it, and is why the suppression is safe to extend to
    the reserved opener.
    """
    # a heading inside a fence opens nothing: the declaration stays in v2.9's
    fenced_heading = _entry_under("```markdown", "## contract-v3.0", "```")
    assert fenced_heading == "contract-v2.9"

    # and closes nothing either
    assert _entry_under("~~~text", "## Deprecations", "~~~") == "contract-v2.9"

    # a declaration INSIDE a fence is not a declaration at all
    documented = "\n".join(["## contract-v3.0 — a cut", "", "```markdown",
                            _spent_line(), "```", ""])
    assert rtp.parse_spent_declarations(documented) == []

    # THE CLOSER IS NOT MERELY ANOTHER OPENER: ```` ```markdown ```` opens and
    # does not close, so an info string cannot end the block early and let the
    # lines after it be read as prose.
    still_open = "\n".join(["## contract-v3.0 — a cut", "", "```",
                            "```markdown", _spent_line(), "```", ""])
    assert rtp.parse_spent_declarations(still_open) == []

    # a shorter run of the same character does not close a longer fence, and a
    # different character does not close it at all
    assert rtp.parse_spent_declarations(
        "\n".join(["````", "```", "~~~~", _spent_line()])) == []


def test_a_backtick_in_a_backtick_fences_info_string_opens_no_fence():
    """CODEX P1, ROUND 1 ON PR #589 — and a reader ONE FENCE OUT OF PHASE with
    the document is worse than one that tracks no fences at all.

    CommonMark forbids a backtick in a BACKTICK fence's info string, so
    ```` ```bad`info ```` opens nothing. A reader that thinks it does then reads
    the next bare ```` ``` ```` as a CLOSER while the document reads it as an
    OPENER: every boundary between them is swallowed as code, and the
    declaration inside the real fence is read as a record. Measured before the
    fix: ACCEPTED, from under a `## Notes` heading, inside a code block.

    A TILDE fence's info string MAY carry backticks, and that is the positive
    control: the rule must be the backtick form's alone, or it would stop tilde
    fences from opening at all and hand the escape back the other way.
    """
    out_of_phase = "\n".join([
        "## contract-v3.0 — a cut", "",
        "```bad`info",          # opens NO fence
        "still prose", "",
        "## Notes",             # a real boundary the reader must not swallow
        "", "```",              # the REAL opener
        _spent_line(), "```", ""])
    assert rtp.parse_spent_declarations(out_of_phase) == [], (
        "the declaration sits inside a real code fence, under a non-release "
        "heading, and was ACCEPTED before this rule existed")

    # the control: a tilde fence's info string may carry backticks, and it
    # still opens
    tilde = "\n".join(["## contract-v3.0 — a cut", "", "~~~ok`info",
                       _spent_line(), "~~~", ""])
    assert rtp.parse_spent_declarations(tilde) == []

    # and the other control: the same backtick line is PROSE now, so a
    # declaration after it is read normally
    prose = "\n".join(["## contract-v3.0 — a cut", "", "```bad`info", "",
                       _spent_line()])
    read = rtp.parse_spent_declarations(prose)
    assert len(read) == 1 and read[0].entry == "contract-v3.0"

    # AND THE POSITIVE CONTROL: outside every fence, the same line reads.
    closed = "\n".join(["## contract-v3.0 — a cut", "", "```yaml",
                        "bundle: contract-v3.0", "```", "", _spent_line()])
    read = rtp.parse_spent_declarations(closed)
    assert len(read) == 1 and read[0].entry == "contract-v3.0"


# THE SEPARATORS `str.splitlines()` BREAKS ON AND COMMONMARK DOES NOT, named
# rather than typed for the reason `NBSP` is: a literal U+2028 in a source file
# is a character a tool can normalise, after which the rows below would pass
# over an ordinary newline and prove nothing.
SPLITLINES_ONLY = (
    ("U+2028 LINE SEPARATOR", "\u2028"),
    ("U+2029 PARAGRAPH SEPARATOR", "\u2029"),
    ("U+0085 NEXT LINE", "\u0085"),
    ("VT", "\v"),
    ("FF", "\f"),
    ("FS", "\x1c"),
    ("GS", "\x1d"),
    ("RS", "\x1e"),
)


@pytest.mark.parametrize("name,separator", SPLITLINES_ONLY,
                         ids=[row[0] for row in SPLITLINES_ONLY])
def test_only_commonmark_line_endings_break_a_line(name, separator):
    """CODEX P1, ROUND 4 ON PR #589 — round 1's class one layer down, in the
    LINE SPLITTER rather than in the opener pattern.

    ```` ```bad<U+2028>`info ```` is ONE line to CommonMark and an INVALID
    backtick opener, its info string carrying a backtick. `str.splitlines()`
    hands the reader ```` ```bad ```` as a VALID opener instead, and the reader
    is one fence out of phase again: the `## Notes` boundary is swallowed as
    code, the next bare fence closes the fictitious block while opening a real
    one, and the declaration inside the real block is read under the earlier
    entry. Measured ACCEPTED for every separator in this table.
    """
    doc = "\n".join(["## contract-v3.0 — a cut", "",
                     "```bad" + separator + "`info", "prose", "",
                     "## Notes", "", "```", _spent_line(), "```", ""])
    assert rtp.parse_spent_declarations(doc) == [], (
        f"{name} broke a line CommonMark does not break, putting the reader "
        f"one fence out of phase with the document")


@pytest.mark.parametrize("name,ending", [("LF", "\n"), ("CRLF", "\r\n"),
                                         ("lone CR", "\r")],
                         ids=["LF", "CRLF", "lone CR"])
def test_the_three_line_endings_commonmark_does_recognise_still_work(name,
                                                                     ending):
    """THE CONTROL FOR THE HOLE THE FIX ABOVE COULD OPEN, which on this guard is
    not a hypothetical: narrowing the splitter invites narrowing it to `\n`
    alone, and a CRLF document would then carry a stray `\r` at the end of
    every line — where it would defeat the fence closer's `[ \t]*$`, the ATX
    lookahead's `[ \t]|$`, and the Setext underline's own anchor, all at once
    and silently.

    Both directions under each ending, because a splitter that broke only the
    reading half would look correct from the accepting half.
    """
    contained = ending.join(["## contract-v3.0 — a cut", "", _spent_line()])
    read = rtp.parse_spent_declarations(contained)
    assert len(read) == 1 and read[0].entry == "contract-v3.0", (
        f"a declaration in a {name} document is not read as contained")

    fenced = ending.join(["## contract-v3.0 — a cut", "", "```",
                          _spent_line(), "```", ""])
    assert rtp.parse_spent_declarations(fenced) == [], (
        f"the fence rule does not hold in a {name} document")


# ------------------- COMMONMARK'S BLANK LINE, WHICH IS SPACES AND TABS ONLY
#
# ROUND 3'S LESSON ARRIVING IN THE BLANK-LINE TEST RATHER THAN IN A PATTERN —
# Copilot, round 11 on PR #589. `str.strip()` is Python's and strips every
# Unicode space; CommonMark's blank line is *"a line containing no characters,
# or a line containing only spaces (U+0020) or tabs (U+0009)"*. Escapes rather
# than literals, for the reason `NBSP` and `SPLITLINES_ONLY` give.

NOT_BLANK_TO_COMMONMARK = (
    ("U+00A0 NO-BREAK SPACE", NBSP),
    ("U+2028 LINE SEPARATOR", "\u2028"),
    ("VT", "\v"),
    ("FF", "\f"),
)


@pytest.mark.parametrize("name,char", NOT_BLANK_TO_COMMONMARK,
                         ids=[row[0] for row in NOT_BLANK_TO_COMMONMARK])
def test_a_line_of_unicode_space_is_paragraph_content_not_a_blank_line(name,
                                                                      char):
    """AN UNDER-CLOSING ESCAPE, WHICH IS THE DIRECTION THIS GUARD EXISTS TO
    CLOSE — and it lived in the one predicate that was still Python's.

    A line holding only U+00A0 is PARAGRAPH CONTENT to CommonMark, so the run of
    `=` below it is a Setext underline and a real heading that CLOSES the entry.
    Read as blank by `str.strip()`, it made `after_paragraph` false, the `===`
    stopped being an underline, the entry never closed, and the declaration
    below was **ACCEPTED** under an entry CommonMark places it outside of.
    Measured for every character in this table.
    """
    doc = "\n".join(["## contract-v3.0 — a cut", "", char, "===", "",
                      _spent_line()])
    read = rtp.parse_spent_declarations(doc)
    assert len(read) == 1 and read[0].entry is None, (
        f"a line of {name} was read as blank, so the Setext heading below it "
        f"stopped closing the entry")

    # AND THE SAME CHARACTER INSIDE A PARAGRAPH, because the escape does not
    # need the line to be alone: a paragraph continued by such a line is still
    # a paragraph, and the `===` still underlines it.
    inside = "\n".join(["## contract-v3.0 — a cut", "", "Notes", char, "===",
                         "", _spent_line()])
    read = rtp.parse_spent_declarations(inside)
    assert len(read) == 1 and read[0].entry is None, (
        f"a paragraph continued by a line of {name} stopped being a paragraph")


BLANK_TO_COMMONMARK = (
    ("an empty line", ""),
    ("spaces", "   "),
    ("tabs", "\t\t"),
    ("spaces and tabs", "  \t "),
)


@pytest.mark.parametrize("name,line", BLANK_TO_COMMONMARK,
                         ids=[row[0] for row in BLANK_TO_COMMONMARK])
def test_a_line_of_spaces_or_tabs_is_still_a_blank_line(name, line):
    """THE CONTROL FOR THE HOLE THIS FIX COULD OPEN, and it is a real one: a
    blankness test narrowed too far would make every indented empty line
    paragraph content, so a `===` below one would become a Setext heading and
    CLOSE an entry CommonMark keeps open — a FALSE REFUSAL of a correctly
    contained declaration. `strip(" \t")` is exactly CommonMark's class and
    nothing narrower."""
    doc = "\n".join(["## contract-v3.0 — a cut", "", line, "===", "",
                      _spent_line()])
    read = rtp.parse_spent_declarations(doc)
    assert len(read) == 1 and read[0].entry == "contract-v3.0", (
        f"{name} stopped being a blank line, so the `===` below it closed an "
        f"entry CommonMark leaves open")


# --------------------------------------- RAW HTML: NOT PARSED, REFUSED
#
# THE INVERSION, RULED BY BRETT HEAP 2026-09-03 ON A MEASURED TAIL. Three
# review rounds tried to model CommonMark's raw HTML blocks so a fence-shaped
# line inside one could not put the reader out of phase, and each fix produced
# the next finding — the single-line block, the mismatched kind-1 closer, the
# opener's whitespace class, the case of the kind-4 letter. The reader now
# RECOGNIZES an opener and REFUSES: an `error` on the changelog, and no
# declaration below that line is read.
#
# WHAT THAT BUYS IS A CHANGE OF DIRECTION, and it is the whole argument. Under
# the fidelity reading a line of prose mistaken for HTML swallowed a boundary
# SILENTLY; here an over-recognized line produces a VISIBLE error an author
# repairs by moving one line. Fail-closed by construction rather than by
# fidelity.

RAW_HTML_OPENERS = (
    ("kind 1 <pre>", "<pre>"),
    ("kind 1 <script>", "<script>"),
    ("kind 1 with an attribute", "<pre class=x>"),
    ("kind 2 comment", "<!-- x -->"),
    ("kind 3 processing instruction", "<?php ?>"),
    ("kind 4 declaration", "<!DOCTYPE html>"),
    ("kind 5 CDATA", "<![CDATA[x]]>"),
    ("kind 6 <div>", "<div>"),
    ("kind 6 closing tag", "</div>"),
    ("kind 7 any complete tag", "<mytag>"),
    # CommonMark's kind 6 admits the END OF LINE after the tag name, so a bare
    # `<div` really is an opener — a row rather than a footnote, because the
    # first draft of this table had it on the other side.
    ("kind 6 with no closing bracket", "<div"),
    # THE WIDER READING OF AN AMBIGUOUS KIND, AND IT REVERSES ROUND 7. Kind 4
    # is `<!` plus an UPPERCASE letter in GFM 0.29 and any letter in CommonMark
    # 0.30; round 7 narrowed to uppercase because the wider class made the
    # reader more opaque than GitHub's renderer, which under the FIDELITY
    # reading swallowed boundaries silently. Under THIS reading the narrower
    # class is the unsafe one — an uppercase-only reader would read PAST a real
    # block the day cmark-gfm moves to 0.30 — so the widening is carried
    # deliberately and pinned here.
    ("kind 4 lowercase, per CommonMark 0.30", "<!doctype html>"),
)


@pytest.mark.parametrize("name,opener", RAW_HTML_OPENERS,
                         ids=[row[0] for row in RAW_HTML_OPENERS])
def test_the_read_stops_at_a_raw_html_opener_and_says_so(name, opener):
    """NO DECLARATION BELOW A RAW HTML OPENER IS READ, and the line is
    reported. Note that the declaration below is WELL FORMED and correctly
    contained — it would be ACCEPTED without the opener above it, which is what
    makes this fail-closed rather than merely strict."""
    doc = "\n".join(["## contract-v3.0 — a cut", "", opener, "",
                     _spent_line()])
    read = rtp.read_changelog(doc)
    assert read.declarations == [], (
        f"a declaration below {name} was read, and this reader has no model of "
        f"what a renderer makes of the lines below it")
    assert read.raw_html is not None and read.raw_html[0] == 3

    # THE CONTROL: the identical declaration WITHOUT the opener is accepted, so
    # the assertion above is about the raw HTML and not about the fixture.
    without = "\n".join(["## contract-v3.0 — a cut", "", "", "",
                         _spent_line()])
    control = rtp.read_changelog(without)
    assert len(control.declarations) == 1
    assert control.declarations[0].entry == "contract-v3.0"
    assert control.raw_html is None


NOT_RAW_HTML = (
    ("a paragraph that merely starts with '<'", "<not a tag at all"),
    ("a bare left angle bracket", "<"),
    ("a name that is no tag", "<divx"),
    ("a sentence containing an inline tag", "text <b>bold</b> more"),
    ("a backtick-quoted tag in prose", "the `<pre>` element"),
)


@pytest.mark.parametrize("name,line", NOT_RAW_HTML,
                         ids=[row[0] for row in NOT_RAW_HTML])
def test_prose_that_is_not_an_html_opener_does_not_stop_the_read(name, line):
    """OVER-RECOGNITION IS THE SAFE ERROR HERE, BUT IT IS STILL AN ERROR — a
    finding a reader cannot predict is its own defect, and a changelog that
    mentions `<pre>` in a sentence must not be refused. The patterns stay
    CommonMark's; only the direction they fail in has changed."""
    doc = "\n".join(["## contract-v3.0 — a cut", "", line, "", _spent_line()])
    read = rtp.read_changelog(doc)
    assert read.raw_html is None, f"{name} was refused as raw HTML"
    assert len(read.declarations) == 1
    assert read.declarations[0].entry == "contract-v3.0"


def test_kind_7_is_not_gated_on_whether_a_paragraph_is_open():
    """THE SECOND NARROWING THE INVERSION REVERSES, and the one that costs
    something. CommonMark forbids a kind-7 block from interrupting a paragraph,
    so `<mytag>` on the line below prose is INLINE html and the line is prose —
    and the removed state machine tracked exactly that, because under the
    fidelity reading calling it a block swallowed the boundary below it.

    Tracking it means carrying parser state, which is what this reading gives
    up. The cost is one more VISIBLE error where CommonMark would have read
    prose, which is the direction this rule is willing to be wrong in; the cost
    of the alternative was a SILENT accept.
    """
    doc = "\n".join(["## contract-v3.0 — a cut", "", "some prose", "<mytag>",
                      "", _spent_line()])
    read = rtp.read_changelog(doc)
    assert read.raw_html is not None and read.raw_html[0] == 4
    assert read.declarations == [], (
        "a bare complete tag below paragraph content is refused, not read — "
        "this reader does not know whether a paragraph is open")

    # THE CONTROL: the same document without that line IS read, so the refusal
    # is about the tag and not about prose above a declaration.
    without = "\n".join(["## contract-v3.0 — a cut", "", "some prose", "",
                          "", _spent_line()])
    control = rtp.read_changelog(without)
    assert control.raw_html is None
    assert len(control.declarations) == 1
    assert control.declarations[0].entry == "contract-v3.0"


# THE KIND-7 UNQUOTED ATTRIBUTE VALUE, ROUND 12 (Copilot on PR #589). A `mytag`
# name is used rather than `div` or another `_HTML_TYPE6_TAGS` member — a kind
# 6 tag matches on the tag name alone, with no `$` anchor, so it would match
# regardless of anything this fix touches and would exercise nothing. A digit
# placed right after the separator makes the token boundary observable either
# way, because a bare digit can never itself open an attribute name: the
# opener is recognized only when the character before the digit stayed inside
# the unquoted value token rather than ending it.
#
# CommonMark's whitespace is SPACE, TAB, VT, FF, CR or LF — nothing else.
# U+00A0 (no-break space) and U+2028 (line separator) are in Python's `\s` but
# are not CommonMark whitespace, so they stay inside the token; a real
# CommonMark space, tab, VT or FF ends it, and what follows must then parse as
# a new attribute name, which a bare digit cannot.
UNQUOTED_ATTR_VALUE_TOKENS = (
    ("U+00A0 stays inside the token", "\N{NO-BREAK SPACE}", True),
    ("U+2028 stays inside the token", "\N{LINE SEPARATOR}", True),
    ("a plain letter run, the control", "z", True),
    ("a space splits the token", " ", False),
    ("a tab splits the token", "\t", False),
    ("a vertical tab splits the token", "\v", False),
    ("a form feed splits the token", "\f", False),
)


@pytest.mark.parametrize("name,infix,is_opener", UNQUOTED_ATTR_VALUE_TOKENS,
                         ids=[row[0] for row in UNQUOTED_ATTR_VALUE_TOKENS])
def test_unquoted_attribute_value_token_uses_commonmarks_whitespace_class(
        name, infix, is_opener):
    """`_HTML_ATTR`'s unquoted-value token must exclude CommonMark's
    whitespace class and nothing wider, so a character CommonMark does not
    treat as whitespace stays inside one token while one it does treat as
    whitespace ends it — see the comment above `_HTML_ATTR` for the round-12
    finding this corrects."""
    doc = "\n".join(["## contract-v3.0 — a cut", "",
                      f"<mytag class=a{infix}5>", "", _spent_line()])
    read = rtp.read_changelog(doc)
    if is_opener:
        assert read.raw_html is not None and read.raw_html[0] == 3, (
            f"{name}: expected a kind-7 opener")
        assert read.declarations == []
    else:
        assert read.raw_html is None, (
            f"{name}: the split token should not have matched an opener")
        assert len(read.declarations) == 1
        assert read.declarations[0].entry == "contract-v3.0"


def test_an_html_opener_inside_a_fence_is_an_example_and_not_an_opener():
    """FENCES REMAIN THE ONLY OPAQUE REGION, so the form of a raw HTML block may
    be DOCUMENTED without being PERFORMED — exactly as the reserved SPENT opener
    may be."""
    doc = "\n".join(["## contract-v3.0 — a cut", "", "```html", "<pre>",
                     "```", "", _spent_line()])
    read = rtp.read_changelog(doc)
    assert read.raw_html is None
    assert len(read.declarations) == 1
    assert read.declarations[0].entry == "contract-v3.0"


def test_declarations_above_a_raw_html_opener_still_stand():
    """The read stops AT the opener, not because of it: everything above was
    read as prose and prose is what it is."""
    doc = "\n".join(["## contract-v3.0 — a cut", "", _spent_line(), "",
                     "<div>", "", _spent_line(subject="contract-v2.7")])
    read = rtp.read_changelog(doc)
    assert [d.subject for d in read.declarations] == ["contract-v2.6"]
    assert read.raw_html is not None


def test_raw_html_is_one_contested_error_on_the_changelog(tmp_path):
    """THE REFUSAL IS REPORTED, NOT SILENT — and the bundle a declaration below
    the opener WOULD have quieted goes on being reported, which is the whole of
    what fail-closed means here."""
    repo = _spent_fixture(tmp_path, line="<div>\n\n" + _spent_line())
    findings = _check(repo)
    raw = [f for f in findings if f.path == CHANGELOG]
    assert len(raw) == 1 and raw[0].severity == ERROR
    # THE RULING'S OWN WORDS, so the message cannot drift away from what was
    # ruled: "unparseable construct: raw HTML; the SPENT reader refuses to read
    # past it".
    assert "UNPARSEABLE CONSTRUCT: RAW HTML" in raw[0].rule
    assert "REFUSES TO READ PAST" in raw[0].rule
    assert "line 7" in raw[0].rule and "'<div>'" in raw[0].rule
    assert raw[0].resolution == "contested"
    assert raw[0].action == rtp._RAW_HTML_ACTION

    # AND THE SUPERSEDED ERROR STANDS BESIDE IT — no `info`, nothing quieted.
    assert not [f for f in findings if f.severity == INFO]
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_this_repositorys_changelog_carries_no_raw_html():
    """The live corpus, which is what makes the refusal free: this estate's
    changelog has never used raw HTML, so the rule costs it nothing today and
    reds the moment it would start to."""
    live = (Path(REPO_ROOT) / CHANGELOG).read_bytes()
    assert rtp.read_changelog(live).raw_html is None


def test_this_repositorys_live_declaration_survives_every_boundary_rule():
    """THE LIVE READ, AND IT IS THE POINT OF THE HARDENING RATHER THAN A
    FORMALITY: a boundary rule tightened past this document would refuse the
    declaration that makes `main` green, and every rule above was chosen so
    that it does not.

    `contracts/CHANGELOG.md` is read FROM DISK so that inserting a heading
    above the reserved line reds a test rather than silently flipping the
    family from `info` to `error`.
    """
    live = (Path(REPO_ROOT) / CHANGELOG).read_bytes()
    text = live.decode("utf-8")

    # BY SUBJECT, NOT BY POSITION (Copilot, round 1 on PR #589). A second
    # legitimate declaration for a different bundle would land here one day,
    # and this test must red for a containment defect rather than for the
    # estate having spent a second number.
    by_subject = {d.subject: d for d in rtp.parse_spent_declarations(live)}
    assert "contract-v2.6" in by_subject
    spent = by_subject["contract-v2.6"]
    assert spent.entry == "contract-v3.0"
    assert spent.missing == ()

    # THE ANTI-OVER-READ GUARD, which is what a bare count was standing in for
    # and which this states properly: the form written INSIDE this document's
    # own fenced block adds NO declaration. A reader that over-read the live
    # document would gain one here.
    #
    # SPLICED AT THE START OF THE FENCED CONTENT, not at a byte offset into the
    # opener line — Copilot's round-2 finding, and it was right: this document's
    # first fence is ```` ```yaml ````, so an offset splice put the reserved
    # opener mid-line where NO reader would have read it, and the assertion
    # passed whatever the fence rule did. The line below is a REAL line inside
    # the fenced region, and the test is asserted to be non-vacuous by finding
    # that same line accepted once the fence is taken away.
    #
    # SPLIT WITH `rtp._lines`, NOT `str.splitlines()` — Copilot's round-12
    # finding: the parser's own line splitter is CommonMark's line endings and
    # no others, so a splice built with `splitlines()` could land at a line
    # boundary the parser does not recognize, testing a document the parser
    # never sees.
    lines = rtp._lines(text)
    opener = next(i for i, line in enumerate(lines)
                  if line.startswith("```"))
    hidden = _spent_line(subject="contract-v9.9",
                         superseding=lines[0].split()[-1])
    inside = "\n".join(lines[:opener + 1] + [hidden] + lines[opener + 1:])
    assert "contract-v9.9" not in {
        d.subject for d in rtp.parse_spent_declarations(inside)}, (
        "the reserved form inside this document's fenced block was read as a "
        "record, which would let a documented example spend a bundle")
    # NON-VACUITY: the identical line, at the identical place, with the fence
    # opener removed, IS read — so the assertion above is about the fence and
    # not about the splice having landed somewhere unreadable.
    unfenced = "\n".join(lines[:opener] + [hidden] + lines[opener + 1:])
    assert "contract-v9.9" in {
        d.subject for d in rtp.parse_spent_declarations(unfenced)}, (
        "the spliced line is unreadable for some reason other than the fence, "
        "so the guard above proves nothing")

    # AND THE POSITIVE CONTROL: one non-release heading spliced in above the
    # declaration and the containment is gone. A live read that could only ever
    # answer "contained" would prove nothing about the rule.
    spliced = text.replace(rtp.SPENT_OPENER,
                           "## Deprecations\n\n" + rtp.SPENT_OPENER, 1)
    control = {d.subject: d for d in rtp.parse_spent_declarations(spliced)}
    assert control["contract-v2.6"].entry is None


def test_a_declaration_under_a_non_release_heading_is_refused_end_to_end(tmp_path):
    """THE ESCAPE AT THE FINDING LEVEL, not the parse level — which is where it
    mattered. A declaration attributed to the previous release entry matched the
    bundle it named, so the containment check passed and the
    superseded-and-never-published `error` was replaced by an `info`."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    # the declaration sits after a NON-RELEASE section of the v3.0 entry, so it
    # is contained by no entry at all
    _changelog(repo,
               ("contract-v3.0", ["a cut", "", "## Deprecations", "",
                                  _spent_line()]),
               ("contract-v2.6", ["left exactly as written"]))
    _push(repo)

    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "sits inside no bundle's changelog entry" in refusal[0].rule
    assert "LATER CUT" in refusal[0].rule
    assert not [f for f in findings if f.severity == INFO], (
        "the declaration was accepted from outside its superseding bundle's "
        "entry, which is the escape this test exists for")
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule], (
        "and the finding the family exists to raise must stand")


# ------------------------------------------------- ACCEPTED: the one `info`

def _spent_fixture(tmp_path, *, publish_successor=True, declaration=True,
                   line=None, name="spent"):
    """v2.6 cut and never tagged; v3.0 cut on top of it and (by default) tagged.

    The estate's own shape, which is the point: this is `contract-v2.6` and
    `contract-v3.0` with the names kept, so a reader of a failure here is
    looking at the case the state was built for.
    """
    repo, _ = _repo(tmp_path, name)
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    if declaration:
        _changelog(repo,
                   ("contract-v3.0", ["### `contract-v2.6` disposition", "",
                                      line or _spent_line()]),
                   ("contract-v2.6", ["left exactly as written"]))
    else:
        _changelog(repo,
                   ("contract-v3.0", ["### `contract-v2.6` disposition", "",
                                      "nothing machine-readable here"]),
                   ("contract-v2.6", ["left exactly as written"]))
    if publish_successor:
        _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _push(repo)
    return repo


def test_a_declared_spent_bundle_with_a_published_successor_is_one_contested_info(tmp_path):
    """THE ACCEPTED STATE, and it is RECORDED rather than SILENT — ruled by
    Brett Heap 2026-09-02 on an alternative that was put to him and declined.

    A reader who finds `contracts/releases/contract-v2.6.digests.yaml` with no
    matching tag is owed the answer where they are looking, and an `info` has a
    finding key where silence does not.
    """
    findings = _check(_spent_fixture(tmp_path))
    assert [f.severity for f in findings] == [INFO]
    spent = findings[0]
    # THE PATH IS THE FINDING'S IDENTITY (OD-5, as amended on a Codex P1). Not
    # the manifest, which every other finding of this family shares, and not the
    # changelog, which two spent bundles would share.
    assert spent.path == "contracts/releases/contract-v2.6.digests.yaml"
    assert spent.path != MANIFEST and spent.path != CHANGELOG
    assert spent.resolution == "contested"
    assert "contract-v2.6" in spent.rule and "contract-v3.0" in spent.rule
    assert CHANGELOG in spent.rule
    assert "Brett Heap" in spent.rule and "2026-09-02" in spent.rule
    # AND IT MUST NOT READ AS THE OBLIGATION HAVING BEEN MET.
    assert "EXTINGUISHED" in spent.rule
    assert "no published annotated tag" in spent.rule
    assert "was cut and SUPERSEDED without ever being published" not in spent.rule


def test_the_accepted_info_carries_its_own_action_and_never_the_absent_tag_one(tmp_path):
    """The action is spelled out here rather than compared with the module's
    constant: a test asserting `f.action == rtp._SPENT_ACCEPTED_ACTION` passes
    whatever that constant is mutated to."""
    findings = _check(_spent_fixture(tmp_path))
    assert findings[0].action == (
        "no action, and this is NOT the tag obligation having been met — it "
        "was EXTINGUISHED, by an owner act, at the cost of a version number, "
        "and the record says which; the state is permanent, and never edit the "
        "manifest, the changelog or the inventory to stop it being reported")
    assert findings[0].action != rtp._ABSENT_ACTION
    assert findings[0].action != rtp._SUPERSEDED_ACTION


def test_removing_the_declaration_returns_the_superseded_error(tmp_path):
    """THE RED-FIRST PROOF, and the whole reason this state is safe.

    `main` goes green because `contract-v2.6` is EXPLICITLY DECLARED spent,
    never because an undeclared bundle started passing. The same tree with the
    declaration removed must report the `error` again, in the same words it
    always did — silence is never a declaration.
    """
    declared = _check(_spent_fixture(tmp_path, name="declared"))
    assert [f.severity for f in declared] == [INFO]

    silent = _check(_spent_fixture(tmp_path, declaration=False, name="silent"))
    assert [f.severity for f in silent] == [ERROR]
    assert "contract-v2.6 was cut and SUPERSEDED without ever being published" \
        in silent[0].rule
    assert silent[0].path == MANIFEST
    assert silent[0].action == rtp._SUPERSEDED_ACTION


# ------------------------------------------------- PROVISIONAL: the `warning`

def test_an_unpublished_successor_is_one_warning_and_not_two(tmp_path):
    """PROVISIONAL RATHER THAN REFUSED — ruled a `warning`, so a conforming
    family reporting BOTH it and the superseded `error` would be contradicting
    the ruling it was written to encode.

    Nothing is lost by the suppression: the successor is the bundle the manifest
    now declares, so it is graded by the DISTANCE arm on its own account, and
    the obligation has MOVED onto the successor rather than been discharged.
    """
    repo = _spent_fixture(tmp_path, publish_successor=False)
    findings = _check(repo)
    spent = [f for f in findings if "contract-v2.6" in f.rule]
    assert len(spent) == 1, "one finding is reported for this bundle, not two"
    assert spent[0].severity == WARNING
    assert spent[0].path == "contracts/releases/contract-v2.6.digests.yaml"
    assert "UNPROVEN" in spent[0].rule
    assert spent[0].action == (
        "publish the SUPERSEDING bundle's annotated tag at the commit the "
        "versioning policy's rule identifies; a bundle is not published until "
        "its tag exists, so until then this supersession is a claim and not "
        "evidence — and the superseding bundle is graded on its own account "
        "meanwhile")
    # THE SUCCESSOR'S OWN FINDING IS NOT SUPPRESSED, which is what bounds the
    # band: past the successor's threshold the estate carries an `error` again,
    # on the bundle that owes the tag.
    successor = [f for f in findings
                 if "contract-v3.0" in f.rule and f.path == MANIFEST]
    assert successor, ("the successor must be graded on its own account, or "
                       "the provisional band is bounded by patience")


def test_the_provisional_band_is_bounded_by_the_successors_own_grading(tmp_path):
    """Past the successor's own threshold the estate carries an ERROR again —
    on the bundle that owes the tag, which is where the obligation moved."""
    repo = _spent_fixture(tmp_path, publish_successor=False)
    _land(repo, 9)
    _push(repo)
    findings = _check(repo)
    successor = [f for f in findings if f.path == MANIFEST]
    assert [f.severity for f in successor] == [ERROR]
    assert "NOT PUBLISHED" in successor[0].rule
    spent = [f for f in findings if "contract-v2.6" in f.rule]
    assert [f.severity for f in spent] == [WARNING]


# ------------------------------------------------------ REFUSED: the `error`s

def test_a_successor_this_repository_never_cut_errors_and_the_superseded_error_stands(tmp_path):
    """Retiring a number by pointing at one that does not exist is the abuse
    this state is most exposed to, so the refusal REMOVES NOTHING.

    The declaration sits in `contract-v9.9`'s OWN entry, so the containing-entry
    rule is satisfied and the finding is about the bundle being uncut rather
    than about where the line was written — the two refusals are apart, and a
    fixture that failed the earlier one would prove nothing about this one.
    """
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo,
               ("contract-v9.9", [_spent_line(superseding="contract-v9.9")]),
               ("contract-v3.0", ["a cut"]))
    _push(repo)

    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert refusal[0].path == "contracts/releases/contract-v2.6.digests.yaml"
    assert "never cut" in refusal[0].rule
    superseded = [f for f in findings if "SUPERSEDED without ever being "
                                         "published" in f.rule]
    assert len(superseded) == 1 and superseded[0].severity == ERROR
    assert superseded[0].path == MANIFEST


def test_a_successor_that_is_not_strictly_later_is_walked_around_backwards(tmp_path):
    """OD-9, FOUND BY CODEX ON PR #578 AGAINST THE RATIFIED SHAPE.

    "Cut and published" is satisfiable by an EARLIER already-published bundle:
    a declaration for `contract-v2.6` written into `contract-v2.5`'s entry and
    naming `contract-v2.5`, which was cut, is published, and carries a valid
    annotated tag. Without the ordering half, an untagged bundle goes quiet with
    NO replacement published at all.
    """
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.5", "cut v2.5")
    _inventory(repo, "contract-v2.5")
    _git(repo, "tag", "-a", "contract-v2.5", "-m", "contract-v2.5")
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo,
               ("contract-v3.0", ["a cut"]),
               ("contract-v2.5", [_spent_line(superseding="contract-v2.5")]))
    _push(repo)

    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "STRICTLY LATER" in refusal[0].rule
    assert "backwards" in refusal[0].rule
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule], (
        "no untagged bundle goes quiet without a LATER published one")
    assert not [f for f in findings if f.severity == INFO]


def test_a_declaration_omitting_an_element_names_it_and_is_never_absent_tag_words(tmp_path):
    """A malformed declaration is worse than none: it looks like a record. So
    the finding names WHICH element is missing and refuses the declaration, and
    it must not borrow the absent-tag words for the omission."""
    repo = _spent_fixture(tmp_path, line=_spent_line(measurement=None))
    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "the measurement of record" in refusal[0].rule
    assert "no published annotated tag" not in refusal[0].rule
    assert refusal[0].action != rtp._ABSENT_ACTION
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_declaration_outside_its_superseding_bundles_entry_is_refused(tmp_path):
    """THE DECLARING ACT IS THE SUPERSEDING BUNDLE'S OWN CHANGELOG ENTRY, and
    that answers who may declare a bundle spent: the act costs a version number
    and is performed by a release cut."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    # written into the SPENT bundle's OWN entry: a bundle that could declare
    # itself spent could decline to be published.
    _changelog(repo,
               ("contract-v3.0", ["a cut"]),
               ("contract-v2.6", [_spent_line()]))
    _push(repo)

    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "sits inside contract-v2.6's changelog entry" in refusal[0].rule
    assert "LATER CUT" in refusal[0].rule
    assert not [f for f in findings if f.severity == INFO]
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_two_declarations_naming_one_bundle_accept_none_of_them(tmp_path):
    """Two records of one disposition is how they come to disagree — and ONE
    finding is reported for the pair, not one per member, because the defect is
    that there are two."""
    repo = _spent_fixture(tmp_path, line="\n".join([_spent_line(),
                                                    _spent_line()]))
    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "2 SPENT declarations" in refusal[0].rule
    assert not [f for f in findings if f.severity == INFO]
    assert [f for f in findings
            if "SUPERSEDED without ever being published" in f.rule]


def test_a_declaration_whose_subject_was_never_cut_disposes_nothing(tmp_path):
    """THE ONE FINDING OF THIS STATE WITH NO PER-BUNDLE INVENTORY TO LAND ON.

    A mistyped subject leaves the REAL bundle undeclared and still reported,
    which is the fail-closed behaviour a typo must not be able to defeat.
    """
    repo = _spent_fixture(tmp_path, line=_spent_line(subject="contract-v2.66"))
    findings = _check(repo)
    orphan = [f for f in findings if f.path == CHANGELOG]
    assert len(orphan) == 1 and orphan[0].severity == WARNING
    assert "contract-v2.66" in orphan[0].rule
    assert "disposes nothing" in orphan[0].rule
    assert orphan[0].action == (
        "correct the SUBJECT of the SPENT declaration in "
        "contracts/CHANGELOG.md: as written it names a bundle this repository "
        "never cut, so it disposes nothing, and the bundle it was meant to "
        "name is still reported by this family")
    # AND THE REAL BUNDLE IS STILL REPORTED.
    assert [f for f in findings
            if "contract-v2.6 was cut and SUPERSEDED" in f.rule]
    assert not [f for f in findings if f.severity == INFO]


def test_a_declaration_naming_the_currently_declared_bundle_is_refused(tmp_path):
    """A repository declaring a bundle it also calls spent asserts two
    incompatible things about one number — and that bundle goes on being graded
    by distance exactly as it is today."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v3.0", "cut v3.0, never tagged")
    _inventory(repo, "contract-v3.0")
    _land(repo, 3)
    _changelog(repo, ("contract-v3.0", [_spent_line(subject="contract-v3.0",
                                                    superseding="contract-v3.0")]))
    _push(repo)

    findings = _check(repo)
    refusal = [f for f in findings if "REFUSED" in f.rule]
    assert len(refusal) == 1 and refusal[0].severity == ERROR
    assert "incompatible" in refusal[0].rule
    assert refusal[0].path == "contracts/releases/contract-v3.0.digests.yaml"
    graded = [f for f in findings if f.path == MANIFEST]
    assert [f.severity for f in graded] == [WARNING]
    assert "first-parent landing(s)" in graded[0].rule
    assert not [f for f in findings if f.severity == INFO]


# ------------------------------------------------------------- the scope rule

def test_a_spent_declaration_does_not_quiet_a_misplaced_tag(tmp_path):
    """THE SPENT STATE REACHES THE ABSENT-TAG ARM AND NOTHING ELSE. It answers
    "this number will never be published", not "whatever ref exists under this
    name is acceptable" — and a tag that exists and points wrongly is the
    condition this family already calls worse than absence."""
    repo, _ = _repo(tmp_path)
    wrong = _declare(repo, "contract-v2.5", "cut v2.5")
    _inventory(repo, "contract-v2.5")
    _declare(repo, "contract-v2.6", "cut v2.6")
    _inventory(repo, "contract-v2.6")
    _git(repo, "tag", "-a", "contract-v2.6", wrong, "-m", "misplaced")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v2.5", wrong, "-m", "contract-v2.5")
    _changelog(repo, ("contract-v3.0", [_spent_line()]),
               ("contract-v2.6", ["left as written"]))
    _push(repo)

    findings = _check(repo)
    misplaced = [f for f in findings if "MISPLACED" in f.rule]
    assert len(misplaced) == 1 and misplaced[0].severity == ERROR
    assert misplaced[0].path == MANIFEST
    assert misplaced[0].resolution == "contested"
    assert not [f for f in findings if f.severity == INFO]


def test_a_spent_declaration_does_not_quiet_a_lightweight_ref(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v2.6", "cut v2.6")
    _inventory(repo, "contract-v2.6")
    _git(repo, "tag", "contract-v2.6")          # no -a: lightweight
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, ("contract-v3.0", [_spent_line()]))
    _push(repo)

    findings = _check(repo)
    assert [f.severity for f in findings] == [ERROR]
    assert "LIGHTWEIGHT" in findings[0].rule
    assert "no published annotated tag" not in findings[0].rule


def test_the_state_is_not_read_backwards_onto_a_published_bundle(tmp_path):
    """`contract-v2.6` is the FIRST bundle of this kind in the estate's history,
    and a state introduced for one instance must not acquire a second by being
    applied to cases that were only late. The five under § Untagged Bundles
    After Enforcement Began were all publishable and all published: they carry
    annotated tags on declaring commits and never reach this arm at all."""
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v1.33", "cut v1.33, tagged late")
    _inventory(repo, "contract-v1.33")
    _git(repo, "tag", "-a", "contract-v1.33", "-m", "retro-published")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, ("contract-v3.0",
                      [_spent_line(subject="contract-v1.33")]))
    _push(repo)

    # The declaration is well formed and its subject is simply not in this arm:
    # a retro-published bundle is PUBLISHED, and the state adds nothing to it.
    assert _check(repo) == []


def test_a_bundle_below_the_enforcement_line_gains_no_spent_finding(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v1.6", "legacy, untagged BY DESIGN")
    _inventory(repo, "contract-v1.6")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, ("contract-v3.0", [_spent_line(subject="contract-v1.6")]))
    _push(repo)
    assert _check(repo) == []


# ------------------------------------------------------------ the second read

class _NoChangelog(FakeGit):
    """A tip whose `contracts/manifest.yaml` reads and whose
    `contracts/CHANGELOG.md` does not — `blobs_at`'s PER-PATH None.

    `ls_tree_paths` has to ANSWER for this shim to reach the changelog guard at
    all, because that guard now sits BELOW the inventory listing: it is gated on
    whether any bundle is IN SCOPE, and the set of cut bundles is half of that
    question. Declared bundle is a parameter so the same shim serves the
    in-scope case and the below-floor control.
    """

    def __init__(self, declared="contract-v2.0", **kwargs):
        super().__init__(**kwargs)
        self._declared = declared

    def blobs_at(self, repo, commit, relpaths):
        body = f"contract_bundle_version: {self._declared}\n".encode()
        return {p: (body if p == MANIFEST else None) for p in relpaths}

    def ls_tree_paths(self, repo, ref, prefix):
        return []


def test_an_unreadable_changelog_at_the_published_tip_skips(tmp_path):
    """THE #338 CONFLATION, ONE DOCUMENT OVER — and this family has already
    been caught by it once. The absence of a declaration this run could not
    LOOK FOR is not the absence of a declaration, in either direction."""
    out = rtp.check_repo("alphaFactory", Path("r"),
                         _NoChangelog(remotes={"r": "tip"}))
    assert isinstance(out, Skip)
    assert "contracts/CHANGELOG.md could not be read at the published tip" \
        in out.reason
    assert "not the same fact as there being none" in out.reason
    # AND IT NAMES WHAT IT DECLINED TO ANSWER FOR, which is the bundle in scope
    # rather than the repository — the skip is the SPENT read's, not the
    # family's.
    assert "contract-v2.0" in out.reason


def test_a_below_floor_repository_with_no_changelog_is_not_newly_skipped(tmp_path):
    """THE FLOOR HOLDS ABOVE THE SPENT READ (Copilot, PR #584 round 3).

    Standing above `parse_bundle`, the changelog guard fired before the bundle
    was known, so a repository declaring `contract-v1.6` and holding no
    `contracts/CHANGELOG.md` — which this family had always answered with
    silence, the floor being what it is — became a silent "not checked"
    instead. A guard for the SPENT read must not change the answer for a
    repository that has no bundle the state could apply to.

    THE POSITIVE CONTROL IS THE SAME SHIM ONE VERSION UP: with an in-scope
    bundle declared the skip is still owed and still taken, so this test cannot
    pass by the guard having been deleted.
    """
    below = rtp.check_repo("alphaFactory", Path("r"),
                           _NoChangelog(declared="contract-v1.6",
                                        remotes={"r": "tip"}))
    assert below == [], (
        "a below-floor repository with no changelog is answered as it always "
        "was — the SPENT read has nothing here it could change")

    in_scope = rtp.check_repo("alphaFactory", Path("r"),
                              _NoChangelog(declared="contract-v1.7",
                                           remotes={"r": "tip"}))
    assert isinstance(in_scope, Skip) and CHANGELOG in in_scope.reason, (
        "the guard must still decline the read for a bundle in scope, or this "
        "test would pass over a deleted guard")


BELOW_FLOOR_STATES = (
    ("live-bundle", "`contract-v1.6`", "`contract-v1.6`", "contract-v1.6"),
    ("wrong-entry", "`contract-v1.6`", "`contract-v3.0`", "contract-v3.0"),
    ("successor-never-cut", "`contract-v1.6`", "`contract-v9.9`",
     "contract-v3.0"),
)


@pytest.mark.parametrize("state,subject,superseding,declared",
                         BELOW_FLOOR_STATES,
                         ids=[row[0] for row in BELOW_FLOOR_STATES])
def test_no_refusal_state_fires_for_a_below_floor_subject(state, subject,
                                                          superseding,
                                                          declared):
    """EVERY state, not just the orphan one. Measured before the change: a
    legacy repository declaring `contract-v1.6` and naming it spent emitted a
    `live-bundle` error, and malformed and wrong-entry below-floor declarations
    emitted theirs — each on an inventory path for a bundle this family does
    not grade."""
    line = (f"**SPENT BUNDLE:** {subject} — SUPERSEDED BY {superseding} — "
            f"CAUSE: c — RULED BY B, 2026-09-02 — MEASUREMENT: m")
    doc = f"## contract-v1.6 — x\n\n{line}\n"
    decls = rtp.parse_spent_declarations(doc)
    findings, candidates = rtp._refusal_findings(
        "alphaFactory", decls, {"contract-v1.6"}, declared)
    assert findings == [], f"a below-floor subject still produced {state}"
    assert candidates == {}, (
        "and it must not become an acceptance candidate either")


def test_a_malformed_below_floor_declaration_is_silent_but_a_shapeless_one_is_not():
    """THE HOLE THE EXCLUSION ABOVE COULD OPEN, pinned in both directions.

    `_below_floor` is FALSE for a name of the wrong shape and for no name at
    all, and that gap is the whole distinction: `contract-v1.3` is an
    out-of-scope NAME and leaves the sweep, while `not-a-bundle` and a line
    carrying the reserved opener and nothing else are DEFECTS and stay in it.
    """
    below = rtp.parse_spent_declarations(
        "## contract-v3.0 — x\n\n**SPENT BUNDLE:** `contract-v1.3`\n")
    findings, _ = rtp._refusal_findings("alphaFactory", below,
                                        {"contract-v3.0"}, "contract-v3.0")
    assert findings == []

    for line, expected in (("**SPENT BUNDLE:** `not-a-bundle`", WARNING),
                           ("**SPENT BUNDLE:**", ERROR)):
        decls = rtp.parse_spent_declarations(f"## contract-v3.0 — x\n\n{line}\n")
        findings, _ = rtp._refusal_findings("alphaFactory", decls,
                                            {"contract-v3.0"}, "contract-v3.0")
        assert [f.severity for f in findings] == [expected], (
            f"{line!r} is a defect and must stay in the sweep")


def test_a_failed_batch_read_names_both_members_it_asked_for(tmp_path):
    """`blobs_at` collapses to None only when GIT ITSELF failed, which fails the
    whole two-member batch — so a message naming one document sends an operator
    to a file when NEITHER was obtained. The per-path None is the other return
    shape and has its own guard, in its own words, one test above."""
    class NoGit(FakeGit):
        def blobs_at(self, repo, commit, relpaths):
            return None

    out = rtp.check_repo("alphaFactory", Path("r"), NoGit(remotes={"r": "tip"}))
    assert isinstance(out, Skip)
    assert MANIFEST in out.reason and CHANGELOG in out.reason
    assert "NEITHER document was obtained" in out.reason


def test_a_below_floor_subject_raises_no_orphan_warning(tmp_path):
    """A BELOW-FLOOR SUBJECT LEAVES THE WHOLE REFUSAL SWEEP, not one branch of
    it — Codex's round-7 P2 on PR #589, which was right that exempting only the
    orphan arm was half a rule.

    The enforcement floor says this family reports NOTHING about a bundle under
    `contract-v1.7`, so a declaration naming one disposes nothing whatever its
    shape, and every other refusal state would be a finding about a bundle this
    family may not speak of.

    THE POSITIVE CONTROL IS A SUBJECT OF THE WRONG SHAPE, which still reaches
    the arm — that is a defect in the record rather than an out-of-scope name,
    and the two must not be collapsed into one test that passes by silencing
    both.
    """
    repo, _ = _repo(tmp_path)
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(repo, ("contract-v3.0", [_spent_line(subject="contract-v1.3")]))
    _push(repo)
    assert _check(repo) == []

    other, _ = _repo(tmp_path, "shape")
    _declare(other, "contract-v3.0", "cut v3.0")
    _inventory(other, "contract-v3.0")
    _git(other, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    _changelog(other, ("contract-v3.0", [_spent_line(subject="not-a-bundle")]))
    _push(other)
    orphan = [f for f in _check(other) if f.path == CHANGELOG]
    assert len(orphan) == 1 and orphan[0].severity == WARNING
    assert "not-a-bundle" in orphan[0].rule


# --------------------------------------------------- two bundles, two identities

def _two_spent(tmp_path, *, second_declaration=True, name="two"):
    """`contract-v2.6` AND `contract-v2.7`, each spent under its own successor.

    A SINGLE-BUNDLE TEST CANNOT SEE THE DEFECT CODEX FOUND. On a shared path the
    two findings would carry ONE `(family, repo, path)` identity, so removing
    one declaration would leave the surviving finding holding the key and the
    removal would be reported by nothing.
    """
    repo, _ = _repo(tmp_path, name)
    _declare(repo, "contract-v2.6", "cut v2.6, never tagged")
    _inventory(repo, "contract-v2.6")
    _declare(repo, "contract-v2.7", "cut v2.7, never tagged")
    _inventory(repo, "contract-v2.7")
    _declare(repo, "contract-v2.8", "cut v2.8")
    _inventory(repo, "contract-v2.8")
    _git(repo, "tag", "-a", "contract-v2.8", "-m", "contract-v2.8")
    _declare(repo, "contract-v3.0", "cut v3.0")
    _inventory(repo, "contract-v3.0")
    _git(repo, "tag", "-a", "contract-v3.0", "-m", "contract-v3.0")
    second = ([_spent_line(subject="contract-v2.7",
                           superseding="contract-v2.8")]
              if second_declaration else ["withdrawn"])
    _changelog(repo,
               ("contract-v3.0", [_spent_line()]),
               ("contract-v2.8", second))
    _push(repo)
    return repo


def test_two_bundles_declared_spent_carry_two_infos_with_different_identities(tmp_path):
    """ONE `info` PER SPENT BUNDLE, each on that bundle's OWN inventory."""
    findings = _check(_two_spent(tmp_path))
    infos = [f for f in findings if f.severity == INFO]
    assert len(infos) == 2
    assert {f.path for f in infos} == {
        "contracts/releases/contract-v2.6.digests.yaml",
        "contracts/releases/contract-v2.7.digests.yaml"}
    assert len({f.match_key() for f in infos}) == 2, (
        "a shared path would let one spent bundle's removal hide behind the "
        "other's surviving finding")
    assert {f.resolution for f in infos} == {"contested"}


def test_removing_one_of_two_declarations_re_raises_that_bundle_alone(tmp_path):
    """OQ-3, PROVED RATHER THAN INHERITED, and proved with TWO bundles.

    `report.uncited_resolutions` is severity-agnostic as written, but it had
    never been exercised by a contested `info`. If it turned out severity-gated
    somewhere in `parse_previous`, OD-5's class choice would return to Brett as
    an open question rather than being quietly dropped — so the round trip is
    run end to end, through a rendered report, not asserted about the code.
    """
    from datetime import date

    from doc_health import report

    before = _check(_two_spent(tmp_path, name="before"))
    rendered = report.render(date(2026, 9, 2), before, [], [], [], 1, [], [])
    _, contested = report.parse_previous(rendered, announce=None)
    assert ("release-tag-publication", "alphaFactory",
            "contracts/releases/contract-v2.7.digests.yaml") in contested, (
        "a contested `info` must reach the ranked plan and be readable back, "
        "or OD-5's class choice buys nothing")

    after = _check(_two_spent(tmp_path, second_declaration=False,
                              name="after"))
    raised = report.uncited_resolutions(after, contested, dispositions=set())
    assert [f.severity for f in raised] == [ERROR]
    assert raised[0].family == "uncited-resolution"
    assert raised[0].path == "contracts/releases/contract-v2.7.digests.yaml", (
        "the withdrawn bundle's own identity is what is re-raised, and the "
        "surviving one's is not")


def test_a_withdrawn_spent_declaration_is_re_raised_as_an_uncited_resolution(tmp_path):
    """The single-bundle half of the same proof: the way to make the state stop
    being reported is to delete the inventory or the declaration, and both are
    the *"never edit the manifest, the changelog or the inventory to match the
    absence"* this family already prescribes."""
    from datetime import date

    from doc_health import report

    before = _check(_spent_fixture(tmp_path, name="withdrawn-before"))
    rendered = report.render(date(2026, 9, 2), before, [], [], [], 1, [], [])
    _, contested = report.parse_previous(rendered, announce=None)
    after = _check(_spent_fixture(tmp_path, declaration=False,
                                  name="withdrawn-after"))
    raised = report.uncited_resolutions(after, contested, dispositions=set())
    assert [f.severity for f in raised] == [ERROR]
    assert raised[0].path == "contracts/releases/contract-v2.6.digests.yaml"


def test_a_declaration_with_no_readable_subject_is_a_changelog_error(tmp_path):
    """AN ORCHESTRATOR DECISION, TAKEN FAIL-CLOSED AND RECORDED (realization
    2026-09-02, awaiting Brett's affirmation).

    The requirement gives the changelog path to exactly one finding — a
    declaration whose SUBJECT names a bundle this repository never cut, at
    `warning` — and is silent on a line whose subject cannot be READ at all,
    which has no per-bundle inventory to land on either. That line is strictly
    WORSE than a mistyped-but-readable subject: it names nothing, so nothing can
    be checked about it, and the opener is reserved precisely so such a line is
    a malformed declaration rather than prose. It is therefore an `error` on
    `contracts/CHANGELOG.md` and NOT the orphan `warning` — the fail-closed
    reading of a silence.
    """
    repo = _spent_fixture(tmp_path, line="**SPENT BUNDLE:** no subject here")
    findings = _check(repo)
    malformed = [f for f in findings if f.path == CHANGELOG]
    assert len(malformed) == 1
    assert malformed[0].severity == ERROR, (
        "an unreadable subject is not the orphan-subject warning: that one "
        "names a bundle and this one names nothing")
    assert "MALFORMED" in malformed[0].rule
    assert "reserved opener" in malformed[0].rule
    # AND THE REAL BUNDLE IS UNTOUCHED BY IT.
    assert [f for f in findings
            if "contract-v2.6 was cut and SUPERSEDED" in f.rule]
    assert not [f for f in findings if f.severity == INFO]
