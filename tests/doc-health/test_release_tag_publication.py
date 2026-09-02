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

def test_an_unreadable_changelog_at_the_published_tip_skips(tmp_path):
    """THE #338 CONFLATION, ONE DOCUMENT OVER — and this family has already
    been caught by it once. The absence of a declaration this run could not
    LOOK FOR is not the absence of a declaration, in either direction."""
    class NoChangelog(FakeGit):
        def blobs_at(self, repo, commit, relpaths):
            return {p: (b"contract_bundle_version: contract-v2.0\n"
                        if p == MANIFEST else None)
                    for p in relpaths}

    out = rtp.check_repo("alphaFactory", Path("r"),
                         NoChangelog(remotes={"r": "tip"}))
    assert isinstance(out, Skip)
    assert "contracts/CHANGELOG.md could not be read at the published tip" \
        in out.reason
    assert "not the same fact as there being none" in out.reason


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
