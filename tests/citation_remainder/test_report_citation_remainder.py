"""THE CITATION REMAINDER, REPORTED — the report CLI's lane
(`packet-citation-report`, `add-citation-remainder-report` `tasks.md` § 2.1,
issue #1053).

EVERY SCENARIO THE DELTA STATES IS REALIZED BY A TEST BELOW WHOSE DOCSTRING
NAMES IT, and the five requirements are kept apart in five sections so a reader
checking coverage reads one place. The delta carries 63 `#### Scenario:` blocks
across 5 `### Requirement:` blocks, and each one's test names it verbatim in its
first line.

FIXTURES ARE THROWAWAY GIT TREES IN `tmp_path`, on `tests/packet_reference/`'s
stated precedent — *"a committed broken packet is a file every other sweep has
to be taught to ignore, while a scratch tree is read by this test alone"* — and
on three reasons of this subject's own. The population recipe is `git ls-files`,
so a committed fixture subdirectory would list THIS repository's files rather
than the fixture's; a nested `.git` cannot be committed at all; and `tests/` is
one of the population's three default exclusions, so a committed fixture buys
nothing a scratch tree does not. `git` is not one of the suite's guarded
binaries (`tests/hermeticity.py`'s `GUARDED_BINARIES`), so a real git inside
`tmp_path` is hermetic by the suite's own definition.

AND THIS DIRECTORY CARRIES NO `conftest.py`. `pytest.ini` anchors the rootdir at
the repository root, so `tests/conftest.py`'s hermeticity guard reaches here
without a local override, and a directory `conftest.py` would hijack the ambient
`conftest` module name — the one thing that file documents must not be done.

NO TEST ASSERTS A LITERAL COUNT AGAINST THE LIVE CORPUS. The corpus moves under
every merge that touches any citation anywhere, so the one live-corpus test at
the end asserts INVARIANTS — the arithmetic closes, every remainder entry names
a citing file, the class totals sum to the remainder, the AMBIGUOUS row is
present, the exit is 0 — and never a number. The reproduction of the evidence's
own figures is evidence taken once at a named commit, not a permanent assertion.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "report-citation-remainder.py"


def _load(name: str, path: Path):
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


report = _load("report_citation_remainder", SCRIPT)


# --------------------------------------------------------------------------
# FIXTURE HELPERS — a throwaway corpus, built with real git.
# --------------------------------------------------------------------------

def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True)


def new_repo(root: Path) -> Path:
    """A git tree with the changes root already in place.

    The identity is configured EXPLICITLY rather than inherited: the required
    `pytest-suite` job runs with `GIT_CONFIG_GLOBAL=/dev/null
    GIT_CONFIG_NOSYSTEM=1` and there is no ambient one to fall back on.
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / "openspec" / "changes").mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", ".")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.com")
    return root


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def packet(root: Path, change: str, *, files=("proposal.md",),
           archived: str | None = None, former_ids=()) -> Path:
    """One change packet directory, active or under a dated archive folder."""
    where = root / "openspec" / "changes"
    where = (where / "archive" / f"{archived}-{change}") if archived \
        else (where / change)
    where.mkdir(parents=True, exist_ok=True)
    for name in files:
        target = where / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# a fixture packet\n", encoding="utf-8")
    marker = "schema: spec-driven\ncreated: 2026-09-17\n"
    if former_ids:
        marker += "former_ids:\n" + "".join(f"  - {i}\n" for i in former_ids)
    (where / ".openspec.yaml").write_text(marker, encoding="utf-8")
    return where


def commit(root: Path, message: str = "fixture", gitlinks=()) -> str:
    """Stage the working tree and commit it.

    A MODE-160000 GITLINK IS STAGED AFTER `git add -A` AND NEVER BEFORE: the
    entry names a directory that does not stand in the working tree, so an
    `add -A` run afterwards reads it as a deletion and takes it straight back
    out of the index.
    """
    git(root, "add", "-A")
    for rel in gitlinks:
        sha = "0" * 39 + "1"
        git(root, "update-index", "--add", "--cacheinfo", f"160000,{sha},{rel}")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD").stdout.strip()


def run_json(root: Path, *args: str) -> dict:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = report.main([str(root), "--json", *args])
    assert code == 0, "the report exits successfully whatever it finds"
    return json.loads(buffer.getvalue())


def run_human(root: Path, *args: str) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = report.main([str(root), *args])
    assert code == 0
    return buffer.getvalue()


def entries(data: dict) -> dict:
    """Every listed token record, by token, in whichever grouping was asked."""
    if "tokens" in data:
        return {record["token"]: record for record in data["tokens"]}
    return {record["token"]: record
            for group in data["identities"] for record in group["tokens"]}


CITE = "openspec/changes"


# ==========================================================================
# REQUIREMENT: The citation remainder is reported
# ==========================================================================

def test_the_report_prints_the_head_the_population_pair_the_tokens_and_both_remainders(
        tmp_path) -> None:
    """Scenario: The report is taken over a corpus."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"Resolved: {CITE}/add-present/proposal.md\n"
          f"Dangling: {CITE}/add-absent/proposal.md\n")
    head = commit(root)

    data = run_json(root)
    text = run_human(root)

    assert data["head"] == head
    assert head in text
    population = data["population"]
    assert population["tracked_entries_in_scope"] >= 1
    assert population["files_read"] >= 1
    assert "tracked ENTRIES in scope" in text
    assert "FILES read" in text
    assert data["counts"]["distinct_tokens"] == 2
    assert data["counts"]["remainder_inclusive_tokens"] == 1
    assert data["counts"]["remainder_inclusive_identities"] == 1
    assert "INCLUSIVE remainder" in text and "TOKENS" in text
    assert "IDENTITIES" in text
    listed = entries(data)
    assert [o["path"] for o in listed[f"{CITE}/add-absent/proposal.md"]
            ["occurrences"]] == ["docs/notes.md"]
    assert "docs/notes.md:1" in text or "docs/notes.md:2" in text


def test_a_dirty_tree_is_declared_beside_the_head_and_the_reading_still_runs(
        tmp_path) -> None:
    """Scenario: The tree read is not clean at the head printed."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    head = commit(root)
    write(root, "docs/notes.md",
          f"{CITE}/add-absent/proposal.md\n{CITE}/add-other/proposal.md\n")

    data = run_json(root)
    text = run_human(root)

    assert data["head"] == head, "an uncommitted edit does not move the head"
    assert data["tree_unmodified_at_head"] is False
    assert "MODIFIED at this head" in data["tree_state"]
    assert "NOT a later point in the series" in data["tree_state"]
    assert "MODIFIED at this head" in text
    assert data["counts"]["remainder_inclusive_tokens"] == 2, \
        "the reading is still produced rather than refused"


def test_a_clean_tree_is_declared_unmodified_at_the_head_it_prints(
        tmp_path) -> None:
    """The other half of the dirty-state declaration: a clean tree says so.

    No scenario of its own; the declaration is a pair and a report that printed
    the sentence only when it was bad news would leave a reader unable to tell
    "clean" from "this build does not check".
    """
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert data["tree_unmodified_at_head"] is True
    assert "UNMODIFIED" in data["tree_state"]
    assert "UNMODIFIED" in run_human(root)


def test_an_identity_cited_by_several_tokens_counts_once_and_lists_every_token(
        tmp_path) -> None:
    """Scenario: One identity is cited by several tokens."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"one {CITE}/add-absent/proposal.md\n"
          f"two {CITE}/add-absent/design.md\n"
          f"three {CITE}/add-absent\n")
    commit(root)

    data = run_json(root)
    counts = data["counts"]
    assert counts["remainder_inclusive_tokens"] == 3
    assert counts["remainder_inclusive_identities"] == 1
    listed = entries(data)
    assert set(listed) == {f"{CITE}/add-absent",
                           f"{CITE}/add-absent/proposal.md",
                           f"{CITE}/add-absent/design.md"}
    text = run_human(root)
    assert "add-absent (3 tokens)" in text, \
        "grouping NESTS the tokens beneath the identity rather than collapsing"
    for token in listed:
        assert token in text


def test_one_identity_with_two_classed_tokens_keeps_two_entries_and_two_classes(
        tmp_path) -> None:
    """Scenario: One identity's tokens carry different classes."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md", f"{CITE}/add-absent/fixture.md\n")
    write(root, "docs/notes.md", f"see {CITE}/add-absent/walk-<DATE>.md\n")
    commit(root)

    data = run_json(root)
    listed = entries(data)
    fixture = listed[f"{CITE}/add-absent/fixture.md"]
    severed = listed[f"{CITE}/add-absent/walk-"]
    assert fixture["class"] == "fixture-path"
    assert severed["class"] == "truncated"
    assert fixture["identity"] == severed["identity"] == "add-absent"
    counts = data["counts"]
    assert counts["classes"]["fixture-path"] == 1
    assert counts["classes"]["truncated"] == 1
    assert counts["remainder_inclusive_identities"] == 1, \
        "the identity is still counted once"
    assert counts["remainder_inclusive_tokens"] == 2


def test_the_ambiguous_row_is_printed_at_zero_beside_every_other_outcome(
        tmp_path) -> None:
    """Scenario: No identity in the corpus is claimed by two packets."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"{CITE}/add-present/proposal.md and {CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    text = run_human(root)
    outcomes = data["counts"]["outcomes"]
    assert outcomes["ambiguous"] == 0
    assert "AMBIGUOUS                0" in text
    for row in ("RESOLVED", "DANGLING, identity half", "DANGLING, file half",
                "AMBIGUOUS", "NOT A PACKET REFERENCE"):
        assert row in text, "an omitted outcome is indistinguishable from zero"


def test_every_resolver_outcome_is_reported_under_the_name_the_rule_gives_it(
        tmp_path) -> None:
    """The four outcomes and the fifth answer, each its own row.

    No scenario of its own beyond the AMBIGUOUS one above; a report that
    collapsed any two of them would have thrown away the distinction its own
    remainder is defined by.
    """
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    packet(root, "add-halved")
    write(root, f"{CITE}/README.md", "the corpus's own readme\n")
    write(root, "docs/notes.md",
          f"a {CITE}/add-present/proposal.md\n"
          f"b {CITE}/add-absent/proposal.md\n"
          f"c {CITE}/add-halved/missing.md\n"
          f"d {CITE}/README.md\n")
    commit(root)

    outcomes = run_json(root)["counts"]["outcomes"]
    assert outcomes["resolved"] == 1
    assert outcomes["dangling_identity_half"] == 1
    assert outcomes["dangling_file_half"] == 1
    assert outcomes["not_a_packet_reference"] == 1
    assert outcomes["ambiguous"] == 0


def test_a_relocated_reference_is_counted_within_the_resolved_row(
        tmp_path) -> None:
    """RESOLVED carries the count of references that resolved somewhere other
    than the path they were spelled as — the rule working, and the one figure a
    reader weighing whether it earns its keep needs."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-moved", archived="2026-08-01")
    write(root, "docs/notes.md", f"{CITE}/add-moved/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert data["counts"]["outcomes"]["resolved"] == 1
    assert data["counts"]["outcomes"]["resolved_relocated"] == 1
    assert "resolved somewhere other than the path" in run_human(root)


# ==========================================================================
# REQUIREMENT: The reported population is derived from a stated recipe
# ==========================================================================

def test_a_tracked_entry_that_is_not_a_file_is_skipped_and_the_two_population_numbers_differ_by_it(
        tmp_path) -> None:
    """Scenario: Some tracked entries in scope are not files."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root, gitlinks=("installs/vendored",))

    data = run_json(root)
    population = data["population"]
    assert population["skipped_not_a_file"] == 1
    assert population["files_read"] == population["tracked_entries_in_scope"] - 1
    text = run_human(root)
    assert "tracked ENTRIES in scope" in text and "FILES read" in text
    assert population["arithmetic_closes"] is True


def test_a_symlink_whose_target_leaves_the_root_contributes_no_token(
        tmp_path) -> None:
    """Scenario: A tracked entry is a link whose target leaves the tree."""
    root = new_repo(tmp_path / "repo")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "theirs.md").write_text(f"{CITE}/add-elsewhere/proposal.md\n",
                                       encoding="utf-8")
    os.symlink(outside / "theirs.md", root / "linked.md")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    listed = entries(data)
    assert f"{CITE}/add-elsewhere/proposal.md" not in listed, \
        "text read from outside the root is not this corpus's citation"
    assert f"{CITE}/add-absent/proposal.md" in listed
    assert data["population"]["skipped_link_leaving_the_root"] == 1


def test_a_link_leaving_the_root_lands_in_its_own_skip_term_and_the_arithmetic_closes(
        tmp_path) -> None:
    """Scenario: A link that leaves the root is counted where the arithmetic
    can find it."""
    root = new_repo(tmp_path / "repo")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "theirs.md").write_text("nothing here\n", encoding="utf-8")
    os.symlink(outside / "theirs.md", root / "linked.md")
    write(root, "binary.dat", "placeholder\n")
    (root / "binary.dat").write_bytes(b"\xff\xfe not text\n")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root, gitlinks=("installs/vendored",))

    population = run_json(root)["population"]
    assert population["skipped_link_leaving_the_root"] == 1
    assert population["skipped_not_a_file"] == 1, "the gitlink, and only it"
    assert population["skipped_undecodable"] == 1
    assert population["tracked_entries_in_scope"] == (
        population["files_read"]
        + population["skipped_not_a_file"]
        + population["skipped_link_leaving_the_root"]
        + population["skipped_undecodable"])
    assert population["arithmetic_closes"] is True


def test_the_link_leaving_the_root_term_is_printed_even_where_it_is_zero(
        tmp_path) -> None:
    """Scenario: A link that leaves the root is counted where the arithmetic
    can find it — the clause that the term prints at zero."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert data["population"]["skipped_link_leaving_the_root"] == 0
    assert "skipped, link leaving the root 0" in run_human(root), \
        "a term omitted whenever nothing lands in it teaches readers not to " \
        "look for it"


def test_a_tracked_link_staying_inside_the_root_is_read_like_any_other_file(
        tmp_path) -> None:
    """Scenario: A tracked link stands inside the root."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/real.md", f"{CITE}/add-absent/proposal.md\n")
    os.symlink("real.md", root / "docs" / "alias.md")
    commit(root)

    data = run_json(root)
    population = data["population"]
    assert population["skipped_link_leaving_the_root"] == 0
    assert population["skipped_not_a_file"] == 0
    listed = entries(data)
    cited = {o["path"] for o
             in listed[f"{CITE}/add-absent/proposal.md"]["occurrences"]}
    assert cited == {"docs/real.md", "docs/alias.md"}


def test_a_refinement_prefix_matches_on_segment_boundaries_and_spares_the_sibling(
        tmp_path) -> None:
    """Scenario: A refinement's prefix has a sibling whose name begins the same
    way."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/dashboard/a.md", f"{CITE}/add-inside/proposal.md\n")
    write(root, "docs/dashboard_old/b.md", f"{CITE}/add-sibling/proposal.md\n")
    commit(root)

    listed = entries(run_json(root, "--exclude", "docs/dashboard"))
    assert f"{CITE}/add-inside/proposal.md" not in listed
    assert f"{CITE}/add-sibling/proposal.md" in listed, \
        "a bare string prefix would have swallowed the sibling"


def test_an_include_re_admits_an_excluded_prefix_beside_the_stated_population(
        tmp_path) -> None:
    """Scenario: A caller admits one excluded corpus."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "tests/fixtures/corpus.md", f"{CITE}/add-fixture/proposal.md\n")
    commit(root)

    default = run_json(root)
    widened = run_json(root, "--include", "tests/fixtures")
    assert f"{CITE}/add-fixture/proposal.md" not in entries(default)
    listed = entries(widened)
    assert f"{CITE}/add-fixture/proposal.md" in listed
    assert f"{CITE}/add-absent/proposal.md" in listed, \
        "an admission RE-ADMITS beside the stated population, never in place of it"
    assert (widened["population"]["files_read"]
            > default["population"]["files_read"])
    text = run_human(root, "--include", "tests/fixtures")
    assert "--include" in text and "tests/fixtures" in text
    assert "excluded" in text, "the population it actually used is stated too"


def test_an_exclude_wins_over_an_include_on_the_same_path_in_either_order(
        tmp_path) -> None:
    """Scenario: Two refinements name one path."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "tests/fixtures/corpus.md", f"{CITE}/add-fixture/proposal.md\n")
    commit(root)

    first = run_json(root, "--include", "tests/fixtures",
                     "--exclude", "tests/fixtures")
    second = run_json(root, "--exclude", "tests/fixtures",
                      "--include", "tests/fixtures")
    assert first["population"]["files_read"] == second["population"]["files_read"]
    assert set(entries(first)) == set(entries(second))
    assert f"{CITE}/add-fixture/proposal.md" not in entries(first)


def test_a_file_that_does_not_decode_is_skipped_counted_and_never_replacement_decoded(
        tmp_path) -> None:
    """Scenario: A tracked file in the population is not valid text."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    (root / "docs" / "blob.bin").write_bytes(
        b"\xff\xfe" + f"{CITE}/add-binary/proposal.md\n".encode("utf-8"))
    commit(root)

    data = run_json(root)
    assert data["population"]["skipped_undecodable"] == 1
    listed = entries(data)
    assert f"{CITE}/add-binary/proposal.md" not in listed, \
        "bytes that are not text can yield matches no record wrote"
    assert f"{CITE}/add-absent/proposal.md" in listed


def test_the_population_arithmetic_closes_entries_equal_files_plus_non_files_plus_undecodable(
        tmp_path) -> None:
    """Scenario: A tracked file in the population is not valid text — the
    closure half, now over all four terms."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    (root / "docs" / "blob.bin").write_bytes(b"\x00\xff\xfe")
    commit(root, gitlinks=("installs/vendored",))

    population = run_json(root)["population"]
    assert population["tracked_entries_in_scope"] == (
        population["files_read"] + population["skipped_not_a_file"]
        + population["skipped_link_leaving_the_root"]
        + population["skipped_undecodable"])
    assert "arithmetic" in run_human(root)


def test_the_three_default_exclusions_are_applied_and_named(tmp_path) -> None:
    """The three exclusions, each with its stated reason. No scenario of its
    own; the requirement names them in its body."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-kept/proposal.md\n")
    write(root, f"{CITE}/archive/2026-01-01-old/design.md",
          f"{CITE}/add-archived/proposal.md\n")
    write(root, "tests/corpus.md", f"{CITE}/add-tested/proposal.md\n")
    write(root, "specs/001-feat/plan.md", f"{CITE}/add-spec-kit/proposal.md\n")
    commit(root)

    listed = entries(run_json(root))
    assert f"{CITE}/add-kept/proposal.md" in listed
    for absent in ("add-archived", "add-tested", "add-spec-kit"):
        assert f"{CITE}/{absent}/proposal.md" not in listed
    text = run_human(root)
    assert "frozen record" in text
    assert "synthetic ids" in text
    assert "Spec Kit feats" in text


def test_a_sentence_terminal_full_stop_is_stripped_and_the_normalization_is_printed(
        tmp_path) -> None:
    """Scenario: A citation is followed by sentence punctuation."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"The rule is stated in {CITE}/add-present/proposal.md.\n")
    commit(root)

    data = run_json(root, "--all")
    listed = entries(data)
    record = listed[f"{CITE}/add-present/proposal.md"]
    assert record["status"] == "resolved"
    assert record["in_remainder"] is False, \
        "the record is not reported as carrying a dangling citation"
    assert "trailing-full-stop-stripped" in record["normalizations"]
    assert record["occurrences"][0]["raw"].endswith(".")
    assert "trailing-full-stop-stripped" in run_human(root, "--all")


def test_a_token_ending_in_a_hyphen_that_resolves_to_nothing_is_classed_truncated(
        tmp_path) -> None:
    """Scenario: A citation is severed across two source lines."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-sever-tail")
    write(root, "scripts/tool.py",
          'path = ("' + CITE + '/add-sever-"\n'
          '        "tail/proposal.md")\n')
    commit(root)

    listed = entries(run_json(root))
    severed = listed[f"{CITE}/add-sever-"]
    assert severed["class"] == "truncated"
    assert severed["status"] == "dangling"
    assert f"{CITE}/add-sever-tail/proposal.md" not in listed, \
        "the rejoined path is not reported as a second citation"


def test_a_token_ending_in_a_hyphen_that_resolves_keeps_its_resolved_outcome(
        tmp_path) -> None:
    """Scenario: A citation ends in a hyphen the packet id actually carries."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-trailing-")
    write(root, "docs/notes.md", f"see {CITE}/add-trailing-\n")
    commit(root)

    listed = entries(run_json(root, "--all"))
    record = listed[f"{CITE}/add-trailing-"]
    assert record["status"] == "resolved"
    assert record["class"] is None, \
        "a token that resolves is no remainder entry and takes no class"
    assert record["in_remainder"] is False


def test_a_token_ending_in_a_full_stop_that_resolves_keeps_its_resolved_outcome_and_is_never_stripped(
        tmp_path) -> None:
    """Scenario: A citation ends in a full stop the packet id actually
    carries."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-dotted.")
    write(root, "docs/notes.md", f"see {CITE}/add-dotted.\n")
    commit(root)

    listed = entries(run_json(root, "--all"))
    assert f"{CITE}/add-dotted" not in listed, "the full stop was not stripped"
    record = listed[f"{CITE}/add-dotted."]
    assert record["status"] == "resolved"
    assert record["normalizations"] == []
    assert record["class"] is None
    assert record["in_remainder"] is False


def test_a_token_ending_in_a_grammar_admitted_letter_digit_or_underscore_resolves_unstripped_and_unclassed(
        tmp_path) -> None:
    """Scenario: A citation ends in a character the grammar admits and no
    normalization names."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-underscore_")
    packet(root, "add-digit9")
    write(root, "docs/notes.md",
          f"a {CITE}/add-underscore_\nb {CITE}/add-digit9\n")
    commit(root)

    listed = entries(run_json(root, "--all"))
    for token in (f"{CITE}/add-underscore_", f"{CITE}/add-digit9"):
        record = listed[token]
        assert record["status"] == "resolved"
        assert record["normalizations"] == []
        assert record["class"] is None


def test_a_trailing_path_separator_is_stripped_unconditionally_and_dedups_onto_its_unslashed_sibling(
        tmp_path) -> None:
    """Scenario: A directory citation ends in a path separator."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"slashed {CITE}/add-present/\nbare {CITE}/add-present\n")
    commit(root)

    data = run_json(root, "--all")
    listed = entries(data)
    assert f"{CITE}/add-present/" not in listed
    record = listed[f"{CITE}/add-present"]
    assert record["status"] == "resolved", \
        "the separator is stripped whether or not the token resolves as extracted"
    assert "trailing-path-separator-stripped" in record["normalizations"]
    assert len(record["occurrences"]) == 2
    assert data["counts"]["distinct_tokens"] == 1, \
        "the stripped token and its unslashed sibling are ONE token"


def test_a_trailing_separator_on_a_dangling_citation_is_stripped_too(
        tmp_path) -> None:
    """The separator strip stays unconditional on a token that resolves to
    nothing, which is the other half of the dedup choice."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"slashed {CITE}/add-absent/\nbare {CITE}/add-absent\n")
    commit(root)

    data = run_json(root)
    assert data["counts"]["distinct_tokens"] == 1
    assert data["counts"]["remainder_inclusive_tokens"] == 1


def test_the_header_states_the_extraction_pattern_and_all_three_fixed_choices(
        tmp_path) -> None:
    """Scenario: A reading is compared against an earlier reading."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    reading = data["reading"]
    assert reading["extraction_pattern"] == (
        CITE + r"/[A-Za-z0-9][A-Za-z0-9._\-/]*")
    assert reading["choice_1_normalization_before_deduplication"] is True
    assert reading["choice_2_not_a_packet_reference_outside_the_remainder"] is True
    assert reading[
        "choice_3_cross_repository_flag_set_by_any_qualified_occurrence"] is True
    text = run_human(root)
    assert reading["extraction_pattern"] in text
    assert "choice (1)" in text and "choice (2)" in text and "choice (3)" in text


def test_a_committed_report_under_the_scanned_root_is_excluded_from_the_population(
        tmp_path) -> None:
    """Scenario: The report's own output is committed into the corpus."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "health/citation-remainder.md",
          f"| {CITE}/add-reported-once/proposal.md |\n"
          f"| {CITE}/add-reported-twice/proposal.md |\n")
    commit(root)

    listed = entries(run_json(root))
    assert f"{CITE}/add-reported-once/proposal.md" not in listed
    assert f"{CITE}/add-reported-twice/proposal.md" not in listed
    assert f"{CITE}/add-absent/proposal.md" in listed


def test_an_include_naming_the_output_path_is_refused_or_kept_excluded(
        tmp_path) -> None:
    """Scenario: A caller's refinement names the report's own output."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "health/citation-remainder.md",
          f"| {CITE}/add-reported-once/proposal.md |\n")
    commit(root)

    data = run_json(root, "--include", "health/citation-remainder.md")
    listed = entries(data)
    assert f"{CITE}/add-reported-once/proposal.md" not in listed, \
        "no refinement may switch the self-counting back on"
    assert data["population"]["refinement_named_output_path"] == [
        "health/citation-remainder.md"]
    assert "KEPT" in run_human(root, "--include", "health/citation-remainder.md")


def test_normalization_happens_before_deduplication(tmp_path) -> None:
    """Choice (1), asserted directly: one citation spelled two ways is ONE
    token."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"a {CITE}/add-absent/\nb {CITE}/add-absent\nc {CITE}/add-absent.\n")
    commit(root)

    data = run_json(root)
    assert data["counts"]["distinct_tokens"] == 1
    record = entries(data)[f"{CITE}/add-absent"]
    assert len(record["occurrences"]) == 3
    assert {o["raw"] for o in record["occurrences"]} == {
        f"{CITE}/add-absent/", f"{CITE}/add-absent", f"{CITE}/add-absent."}


def test_not_a_packet_reference_is_counted_beside_the_remainder_and_never_inside_it(
        tmp_path) -> None:
    """Choice (2), asserted directly: the rule handing a path back to its
    caller is never a citation the rule failed on."""
    root = new_repo(tmp_path / "repo")
    write(root, f"{CITE}/README.md", "the corpus's own readme\n")
    write(root, "docs/notes.md", f"see {CITE}/README.md\n")
    commit(root)

    data = run_json(root, "--all")
    assert data["counts"]["outcomes"]["not_a_packet_reference"] == 1
    assert data["counts"]["remainder_inclusive_tokens"] == 0
    assert entries(data)[f"{CITE}/README.md"]["in_remainder"] is False


def test_a_dot_segment_inside_a_citation_is_left_exactly_as_it_is(
        tmp_path) -> None:
    """A `/./` segment is left alone: the resolver's own `_normalised` already
    drops it, so this report has no second rule for it."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md", f"{CITE}/add-present/./proposal.md\n")
    commit(root)

    listed = entries(run_json(root, "--all"))
    assert f"{CITE}/add-present/./proposal.md" in listed
    assert listed[f"{CITE}/add-present/./proposal.md"]["status"] == "resolved"


def test_the_raw_path_absent_arithmetic_carries_all_five_terms(
        tmp_path) -> None:
    """The five-term identity, and the fifth term is not optional: a token the
    resolver declines to read as a packet reference at all can still have no
    path in the tree."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-moved", archived="2026-08-01")
    packet(root, "add-halved")
    write(root, "docs/notes.md",
          f"a {CITE}/add-moved/proposal.md\n"
          f"b {CITE}/add-absent/proposal.md\n"
          f"c {CITE}/add-halved/missing.md\n")
    commit(root)

    absent = run_json(root)["counts"]["raw_path_absent"]
    assert absent["closes"] is True
    assert absent["total"] == (absent["repaired_by_the_identity_rule"]
                               + absent["dangling_identity_half"]
                               + absent["dangling_file_half"]
                               + absent["ambiguous"]
                               + absent["not_a_packet_reference_with_no_raw_path"])
    assert absent["repaired_by_the_identity_rule"] == 1
    assert "raw-path-absent =" in run_human(root)


# ==========================================================================
# REQUIREMENT: A suspected cross-repository citation is flagged and never
# dropped
# ==========================================================================

def test_a_flagged_entry_stays_in_the_inclusive_remainder_and_the_filtered_count_prints_beside_it(
        tmp_path) -> None:
    """Scenario: A citation carries a repository qualifier nearby."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n"
          "\n\n\n"
          f"ours {CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    listed = entries(data)
    assert listed[f"{CITE}/add-theirs/proposal.md"]["flags"] == [
        "possibly-cross-repo"]
    counts = data["counts"]
    assert counts["remainder_inclusive_tokens"] == 2, "flagged, never dropped"
    assert counts["remainder_filtered_tokens"] == 1
    text = run_human(root)
    assert "INCLUSIVE remainder" in text and "FILTERED remainder" in text


def test_any_one_qualified_occurrence_sets_the_flag_for_the_token(
        tmp_path) -> None:
    """Scenario: A citation carries a repository qualifier nearby — choice (3),
    ANY and never ALL."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/one.md", f"codexFactory {CITE}/add-theirs/proposal.md\n")
    write(root, "docs/two.md", f"plain {CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert record["flags"] == ["possibly-cross-repo"]
    assert len(record["occurrences"]) == 2
    assert [o["signals"] for o in record["occurrences"]].count([]) == 1


def test_an_identity_with_one_flagged_and_one_unflagged_token_stays_in_the_filtered_identity_count(
        tmp_path) -> None:
    """Scenario: One identity's remainder tokens are part flagged and part
    not."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-mixed/one.md\n"
          f"\n\n\nplain {CITE}/add-mixed/two.md\n")
    commit(root)

    data = run_json(root)
    listed = entries(data)
    assert listed[f"{CITE}/add-mixed/one.md"]["flags"] == ["possibly-cross-repo"]
    assert listed[f"{CITE}/add-mixed/two.md"]["flags"] == []
    counts = data["counts"]
    assert counts["remainder_inclusive_identities"] == 1
    assert counts["remainder_filtered_identities"] == 1, \
        "one unflagged token is a citation this tree still answers for"
    assert counts["remainder_filtered_tokens"] == 1
    assert counts["remainder_inclusive_tokens"] == 2


def test_an_identity_whose_every_token_is_flagged_leaves_the_filtered_identity_count(
        tmp_path) -> None:
    """Scenario: Every one of an identity's remainder tokens is flagged."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-theirs/one.md\n"
          f"codexFactory {CITE}/add-theirs/two.md\n")
    commit(root)

    data = run_json(root)
    counts = data["counts"]
    assert counts["remainder_inclusive_tokens"] == 2
    assert counts["remainder_inclusive_identities"] == 1
    assert counts["remainder_filtered_tokens"] == 0
    assert counts["remainder_filtered_identities"] == 0


def test_the_filtered_count_and_its_identity_count_print_in_tokens_with_a_reconciling_arithmetic_row(
        tmp_path) -> None:
    """Scenario: The filtered reading is printed beside the inclusive one."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/theirs.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n")
    write(root, "docs/ours.md",
          f"plain {CITE}/add-absent/proposal.md\n")
    write(root, "docs/present.md",
          f"codexFactory {CITE}/add-present/proposal.md\n")
    commit(root)

    data = run_json(root)
    counts = data["counts"]
    assert counts["flagged_remainder_entries"] == 1
    assert counts["flagged_tokens_corpus_wide"] == 2, \
        "a flagged citation whose raw path stands here never entered the " \
        "remainder at all"
    assert counts["remainder_inclusive_tokens"] == (
        counts["remainder_filtered_tokens"]
        + counts["flagged_remainder_entries"])
    text = run_human(root)
    assert "2 inclusive = 1 filtered + 1 REMAINDER ENTRIES carrying the flag" \
        in text
    assert "FILTERED remainder       1 TOKENS" in text
    assert "filtered IDENTITIES      1 IDENTITIES" in text
    assert "never the arithmetic row's term" in text


def test_a_qualifier_outside_the_window_leaves_the_entry_unflagged_and_the_window_is_stated(
        tmp_path) -> None:
    """Scenario: The qualifier sits outside the window."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          "codexFactory is named here\n"
          "one\ntwo\nthree\nfour\n"
          f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert entries(data)[f"{CITE}/add-absent/proposal.md"]["flags"] == []
    assert data["reading"]["window_lines_above_the_citing_line"] == 3
    assert "the citing line plus the 3 lines above it" in run_human(root)


def test_a_qualifier_two_lines_above_flags_the_entry(tmp_path) -> None:
    """Scenario: The repository is named two lines above the citation."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          "codexFactory ships this\n"
          "an intervening line\n"
          f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["flags"] == ["possibly-cross-repo"]
    assert record["occurrences"][0]["signals"] == ["bare-qualifier-word"]


def test_a_qualifier_at_the_windows_own_far_edge_flags_the_entry(
        tmp_path) -> None:
    """The window's far edge — three lines above, still inside it.

    Owed by no scenario by name; `tasks.md` § 2.1 asks for the fixture and the
    edge is where an off-by-one lives.
    """
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          "codexFactory ships this\n"
          "one\ntwo\n"
          f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    assert entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]["flags"] \
        == ["possibly-cross-repo"]


def test_a_qualifier_four_lines_above_leaves_the_entry_unflagged_and_the_window_is_stated(
        tmp_path) -> None:
    """Scenario: The repository is named four lines above the citation."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          "codexFactory ships this\n"
          "one\ntwo\nthree\n"
          f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert entries(data)[f"{CITE}/add-absent/proposal.md"]["flags"] == []
    assert data["counts"]["flagged_tokens_corpus_wide"] == 0, \
        "the window is not widened for that entry or for any other"
    assert data["reading"]["window_lines_above_the_citing_line"] == 3


def test_a_path_joined_repository_prefix_flags_the_entry(tmp_path) -> None:
    """Scenario: A path-joined prefix names another repository."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"see LedgerxFactory/{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert record["occurrences"][0]["signals"] == ["path-joined-prefix"]
    assert record["flags"] == ["possibly-cross-repo"]


def test_a_path_joined_prefix_matches_the_segment_immediately_before_the_token(
        tmp_path) -> None:
    """Scenario: A path-joined prefix stands on a name boundary."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"see xFactories/LedgerxFactory/{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert "path-joined-prefix" in record["occurrences"][0]["signals"], \
        "an enclosing directory prefix does not prevent the match"


def test_a_longer_word_merely_ending_in_a_repository_name_fires_no_path_joined_signal(
        tmp_path) -> None:
    """Scenario: A longer word merely ends in a repository name."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"see myLedgerxFactory/{CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["occurrences"][0]["signals"] == []
    assert record["flags"] == []


def test_a_forge_url_naming_another_repository_flags_the_entry(
        tmp_path) -> None:
    """Scenario: A forge blob or tree URL carries the citation."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"https://github.com/opensoft/codexFactory/blob/main/"
          f"{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert "forge-url" in record["occurrences"][0]["signals"]
    assert record["flags"] == ["possibly-cross-repo"]


def test_a_forge_url_matches_the_repository_segment_and_never_the_owner_segment(
        tmp_path) -> None:
    """Scenario: A forge URL names the repository in its own segment."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"https://github.com/some-other-owner/OpsxFactory/tree/main/"
          f"{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert "forge-url" in record["occurrences"][0]["signals"], \
        "the owner segment need not be a vocabulary member"


def test_a_forge_url_naming_this_repository_fires_no_signal(tmp_path) -> None:
    """Scenario: A forge URL names this repository."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"https://github.com/opensoft/openxFactory/blob/main/"
          f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["occurrences"][0]["signals"] == []
    assert record["flags"] == []


def test_an_adjacent_qualifier_word_flags_the_entry(tmp_path) -> None:
    """Scenario: A bare qualifier word stands immediately before the token."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert record["occurrences"][0]["signals"] == ["bare-qualifier-word"]


def test_a_decorated_qualifier_word_in_another_case_flags_the_entry(
        tmp_path) -> None:
    """Scenario: A decorated qualifier word stands immediately before the
    token."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/emphasis.md",
          f"**CODEXFACTORY** `{CITE}/add-theirs/one.md`\n")
    write(root, "docs/quoted.md",
          f"see [ledgerxfactory] '{CITE}/add-theirs/two.md'\n")
    commit(root)

    listed = entries(run_json(root))
    for token in (f"{CITE}/add-theirs/one.md", f"{CITE}/add-theirs/two.md"):
        assert listed[token]["occurrences"][0]["signals"] == [
            "bare-qualifier-word"], token


def test_a_word_naming_a_repository_outside_the_vocabulary_fires_no_signal(
        tmp_path) -> None:
    """Scenario: The word before the token names a repository this
    specification does not."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"MedxFactory {CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["occurrences"][0]["signals"] == []
    assert record["flags"] == [], "the vocabulary is closed and not widened"


def test_a_custody_locator_scheme_flags_the_entry(tmp_path) -> None:
    """Scenario: The citation is written in a custody-locator scheme."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"the register at opsx:opensoft/{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert record["occurrences"][0]["signals"] == ["custody-locator-scheme"], \
        "no adjacent qualifier word is required before flagging it"


def test_the_custody_locator_prefix_carries_an_owner_segment(
        tmp_path) -> None:
    """Scenario: The custody-locator prefix carries an owner segment."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"opsx:another-owner/{CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert "custody-locator-scheme" in record["occurrences"][0]["signals"]


def test_the_same_scheme_prefix_introducing_something_that_is_not_a_locator_fires_nothing(
        tmp_path) -> None:
    """Scenario: The same scheme prefix introduces something that is not a
    locator."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"run opsx:convene over {CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["occurrences"][0]["signals"] == []


def test_a_trailing_repository_parenthetical_flags_the_entry(
        tmp_path) -> None:
    """Scenario: A trailing parenthetical names the repository."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"the twin at {CITE}/add-theirs/proposal.md (codexFactory)\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    assert record["occurrences"][0]["signals"] == ["trailing-parenthetical"]


def test_a_parenthetical_follows_the_token_with_at_most_one_space(
        tmp_path) -> None:
    """Scenario: A parenthetical follows the token with at most one space."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/glued.md",
          f"{CITE}/add-theirs/one.md(OpsxFactory)\n")
    write(root, "docs/spaced.md",
          f"{CITE}/add-theirs/two.md (openXwallet)\n")
    commit(root)

    listed = entries(run_json(root))
    for token in (f"{CITE}/add-theirs/one.md", f"{CITE}/add-theirs/two.md"):
        assert listed[token]["occurrences"][0]["signals"] == [
            "trailing-parenthetical"], token


def test_a_parenthetical_naming_this_repository_or_standing_further_off_fires_nothing(
        tmp_path) -> None:
    """Scenario: A parenthetical names this repository or stands further off."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/ours.md", f"{CITE}/add-absent/one.md (openxFactory)\n")
    write(root, "docs/far.md", f"{CITE}/add-absent/two.md  (codexFactory)\n")
    write(root, "docs/busy.md",
          f"{CITE}/add-absent/three.md (codexFactory, and more)\n")
    commit(root)

    listed = entries(run_json(root))
    for token in (f"{CITE}/add-absent/one.md", f"{CITE}/add-absent/two.md",
                  f"{CITE}/add-absent/three.md"):
        assert listed[token]["occurrences"][0]["signals"] == [], token
        assert listed[token]["flags"] == [], token


def test_the_report_offers_no_option_that_varies_the_window_or_the_signal_set(
        tmp_path) -> None:
    """THE WINDOW AND THE SIGNAL SET ARE PROPERTIES OF THE CAPABILITY AND NOT
    OF A RUN: both fixed, both closed, and no caller option varies either."""
    options = set()
    for action in report.parser()._actions:
        options.update(action.option_strings)
    for forbidden in ("--window", "--lines", "--reach", "--signals",
                      "--signal", "--repos", "--vocabulary", "--cross-repo"):
        assert forbidden not in options
    assert report.WINDOW_LINES_ABOVE == 3
    assert len(report.SIGNALS) == 5
    assert report.REPOSITORY_VOCABULARY == frozenset({
        "codexfactory", "opsxfactory", "ledgerxfactory", "openxwallet",
        "hermes-install", "xfactory-hermes-install"})


# ==========================================================================
# REQUIREMENT: The report classifies only what it can decide mechanically
# ==========================================================================

def test_an_occurrence_under_a_fixture_location_is_classed_fixture_path_with_its_evidence_named(
        tmp_path) -> None:
    """Scenario: The evidence is a path fact."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-absent/proposal.md"]
    assert record["class"] == "fixture-path"
    assert record["class_evidence"] == ["examples/demo.md"]
    assert "evidence: examples/demo.md" in run_human(root)


def test_every_occurrence_in_a_named_fixture_location_classes_the_entry_fixture_path(
        tmp_path) -> None:
    """Scenario: Every occurrence of an entry stands in a fixture location."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/a.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "ideation/dashboard/gate-records/b.md",
          f"{CITE}/add-absent/proposal.md\n")
    write(root, "contracts/policies/examples/c.yaml",
          f"cited: {CITE}/add-absent/proposal.md\n")
    write(root, "experiments/probe/tests/d.py",
          f"path = '{CITE}/add-absent/proposal.md'\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["class"] == "fixture-path"
    assert len(record["occurrences"]) == 4
    assert record["class_evidence"] == [
        "contracts/policies/examples/c.yaml",
        "examples/a.md",
        "experiments/probe/tests/d.py",
        "ideation/dashboard/gate-records/b.md"]


def test_one_occurrence_outside_every_fixture_location_denies_the_fixture_path_class(
        tmp_path) -> None:
    """Scenario: One occurrence of an entry stands outside the fixture
    locations."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/a.md", f"{CITE}/add-absent/proposal.md\n")
    write(root, "docs/prose.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/proposal.md"]
    assert record["class"] == "unclassified", \
        "the occurrence rule is ALL, never ANY"


def test_a_flag_never_enters_the_class_field_and_never_a_class_total(
        tmp_path) -> None:
    """Scenario: An entry carries a suspicion and a class at once."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-theirs/proposal.md"]
    assert record["class"] == "fixture-path", \
        "the class field keeps the class the evidence supports"
    assert record["flags"] == ["possibly-cross-repo"]
    classes = data["counts"]["classes"]
    assert sum(classes.values()) == data["counts"]["remainder_inclusive_tokens"]
    assert "possibly-cross-repo" not in classes


def test_a_normalization_class_beats_a_location_class(tmp_path) -> None:
    """Scenario: Two classes fit one entry."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md", f"{CITE}/add-absent/walk-<DATE>.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/walk-"]
    assert record["class"] == "truncated"
    assert record["class"] != "fixture-path"


def test_a_stripped_token_that_still_resolves_to_nothing_is_classed_truncated_not_punctuation_stripped(
        tmp_path) -> None:
    """Scenario: A token is both stripped and severed."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"see {CITE}/add-cut-.\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-cut-"]
    assert record["class"] == "truncated"
    assert record["class"] != "punctuation-stripped"
    assert "trailing-full-stop-stripped" in record["normalizations"], \
        "every normalization is reported whatever class the entry lands in"
    assert data["counts"]["classes"]["punctuation-stripped"] == 0


def test_a_longer_path_on_the_line_that_stands_in_the_tree_classes_the_entry_truncated(
        tmp_path) -> None:
    """Scenario: A longer path on the line ends with the token and stands in
    the tree."""
    root = new_repo(tmp_path / "repo")
    write(root, f"vendor/base/{CITE}/add-nested/proposal.md", "a fixture\n")
    write(root, "docs/manifest.yaml",
          f"source_path: vendor/base/{CITE}/add-nested/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-nested/proposal.md"]
    assert record["class"] == "truncated"
    assert record["class_evidence"] == [
        f"vendor/base/{CITE}/add-nested/proposal.md"]


def test_a_longer_path_on_the_line_that_stands_nowhere_classes_nothing_truncated(
        tmp_path) -> None:
    """Scenario: A longer path on the line ends with the token and stands
    nowhere."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/manifest.yaml",
          f"source_path: vendor/base/{CITE}/add-nested/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-nested/proposal.md"]
    assert record["class"] == "unclassified"


def test_a_placeholder_opening_after_the_token_classes_the_entry_truncated(
        tmp_path) -> None:
    """Scenario: The character after the token opens a placeholder."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"the walk record {CITE}/add-absent/walk<YYYY-MM-DD>.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/walk"]
    assert record["class"] == "truncated"
    assert record["status"] == "dangling"


def test_ordinary_prose_after_the_token_classes_nothing_truncated(
        tmp_path) -> None:
    """Scenario: The character after the token is ordinary prose."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"the walk record {CITE}/add-absent/walk, which is missing\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent/walk"]
    assert record["class"] == "unclassified"


def test_a_path_split_across_two_lines_that_rejoins_and_resolves_is_truncated(
        tmp_path) -> None:
    """Scenario: A path split across two source lines rejoins and resolves."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-split", files=("proposal.md",))
    write(root, "scripts/tool.py",
          'path = ("' + CITE + '/add-split/prop"\n'
          '        "osal.md")\n')
    commit(root)

    data = run_json(root)
    listed = entries(data)
    record = listed[f"{CITE}/add-split/prop"]
    assert record["class"] == "truncated"
    assert record["class_evidence"] == [f"{CITE}/add-split/proposal.md"]
    assert f"{CITE}/add-split/proposal.md" not in listed, \
        "the rejoined path is not reported as a second citation"


def test_a_path_split_across_two_lines_that_still_resolves_to_nothing_is_not_truncated(
        tmp_path) -> None:
    """Scenario: A path split across two source lines rejoins and still
    resolves to nothing."""
    root = new_repo(tmp_path / "repo")
    write(root, "scripts/tool.py",
          'path = ("' + CITE + '/add-nosplit/prop"\n'
          '        "osal.md")\n')
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-nosplit/prop"]
    assert record["class"] == "unclassified"
    assert record["status"] == "dangling"
    assert record["half"] == "identity", \
        "the entry is still reported with the resolver outcome it has"


def test_a_stripped_token_that_resolves_to_nothing_is_classed_punctuation_stripped(
        tmp_path) -> None:
    """Scenario: A stripped token still resolves to nothing."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"The rule is stated in {CITE}/add-absent/proposal.md.\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-absent/proposal.md"]
    assert record["class"] == "punctuation-stripped"
    assert "trailing-full-stop-stripped" in record["normalizations"]
    assert data["counts"]["classes"]["punctuation-stripped"] == 1


def test_a_token_that_resolves_once_stripped_is_reported_resolved_and_never_classed(
        tmp_path) -> None:
    """Scenario: A token resolves once its trailing character is stripped."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"The rule is stated in {CITE}/add-present/proposal.md.\n")
    commit(root)

    data = run_json(root, "--all")
    record = entries(data)[f"{CITE}/add-present/proposal.md"]
    assert record["status"] == "resolved"
    assert record["class"] is None, \
        "a token that resolves is no remainder entry at all"
    assert "trailing-full-stop-stripped" in record["normalizations"]
    assert data["counts"]["classes"]["punctuation-stripped"] == 0


def test_an_entry_needing_a_reading_of_intent_is_unclassified(
        tmp_path) -> None:
    """Scenario: The evidence is a fact about intent."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/design.md",
          f"a sketch of {CITE}/add-never-existed/proposal.md, perhaps\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-never-existed/proposal.md"]
    assert record["class"] == "unclassified"
    assert record["status"] == "dangling"


def test_the_class_vocabulary_is_closed_at_four_members(tmp_path) -> None:
    """Scenario: The evidence is a fact about intent — the closed vocabulary
    half."""
    assert report.CLASS_VOCABULARY == (
        "truncated", "punctuation-stripped", "fixture-path", "unclassified")
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert set(data["counts"]["classes"]) == set(report.CLASS_VOCABULARY)
    for record in entries(data).values():
        assert record["class"] in report.CLASS_VOCABULARY


def test_a_dangling_citation_names_its_half_identity_and_citing_files_and_proposes_no_spelling(
        tmp_path) -> None:
    """Scenario: A dangling citation is found."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-halved")
    write(root, "docs/notes.md",
          f"a {CITE}/add-halved/missing.md\nb {CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    listed = entries(data)
    file_half = listed[f"{CITE}/add-halved/missing.md"]
    assert file_half["half"] == "file"
    assert file_half["identity"] == "add-halved"
    assert [o["path"] for o in file_half["occurrences"]] == ["docs/notes.md"]
    identity_half = listed[f"{CITE}/add-absent/proposal.md"]
    assert identity_half["half"] == "identity"
    text = run_human(root)
    for forbidden in ("did you mean", "suggest", "--fix", "diff --git",
                      "corrected spelling"):
        assert forbidden not in text.lower()


def test_the_report_writes_no_file_it_read(tmp_path) -> None:
    """Scenario: A dangling citation is found — the no-edit half."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"a {CITE}/add-present/proposal.md\nb {CITE}/add-absent/x.md\n")
    commit(root)
    before = {path: path.read_bytes()
              for path in sorted(root.rglob("*"))
              if path.is_file() and ".git" not in path.parts}

    run_json(root)
    run_human(root, "--all", "--tokens")

    after = {path: path.read_bytes()
             for path in sorted(root.rglob("*"))
             if path.is_file() and ".git" not in path.parts}
    assert before == after
    assert git(root, "status", "--porcelain").stdout == ""


def test_the_half_file_outcome_is_not_respelled_as_a_fifth_class(
        tmp_path) -> None:
    """`half == file` is an OUTCOME the resolver already returns, not a member
    of the closed class vocabulary."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-halved")
    write(root, "docs/notes.md", f"{CITE}/add-halved/missing.md\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-halved/missing.md"]
    assert record["half"] == "file"
    assert record["class"] == "unclassified"
    assert "file-half" not in data["counts"]["classes"]


# ==========================================================================
# REQUIREMENT: The citation remainder report is advisory and gates nothing
# ==========================================================================

def test_a_remainder_of_any_size_still_exits_zero(tmp_path) -> None:
    """Scenario: The report finds a remainder."""
    root = new_repo(tmp_path / "repo")
    lines = "".join(f"{CITE}/add-absent-{n}/proposal.md\n" for n in range(40))
    write(root, "docs/notes.md", lines)
    commit(root)

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = report.main([str(root)])
    assert code == 0
    assert run_json(root)["counts"]["remainder_inclusive_tokens"] == 40


def test_a_root_that_is_not_a_git_work_tree_exits_non_zero_and_says_it_did_not_run(
        tmp_path, capsys) -> None:
    """Scenario: The report cannot run."""
    plain = tmp_path / "not-a-repo"
    plain.mkdir()

    code = report.main([str(plain)])
    captured = capsys.readouterr()
    assert code != 0
    assert "DID NOT RUN" in captured.err
    assert "No reading was taken" in captured.err
    assert "remainder" not in captured.out


def test_a_root_that_does_not_exist_exits_non_zero_and_says_it_did_not_run(
        tmp_path, capsys) -> None:
    """Scenario: The report cannot run — the unreadable-tree arm."""
    code = report.main([str(tmp_path / "nowhere")])
    assert code != 0
    assert "DID NOT RUN" in capsys.readouterr().err


def test_there_is_no_fail_on_flag(tmp_path) -> None:
    """Scenario: Somebody proposes to gate on the remainder.

    The instrument is `tests/former_id_arrival/`'s `test_there_is_no_bypass_flag`:
    enumerate every option string the parser returns and assert none of them
    converts a finding into a failure.
    """
    options = set()
    for action in report.parser()._actions:
        options.update(action.option_strings)
    assert options == {"-h", "--help", "--json", "--all", "--tokens",
                       "--history", "--include", "--exclude"}
    for forbidden in ("--fail-on", "--fail", "--strict", "--check", "--gate",
                      "--max", "--threshold", "--error-on", "--exit-code",
                      "--fix"):
        assert forbidden not in options
    assert "--fail-on" not in " ".join(
        action.help or "" for action in report.parser()._actions
        if action.option_strings and action.option_strings != ["-h", "--help"]
    ).replace("no `--fail-on`", ""), "no option offers one"


def test_a_findings_run_and_an_empty_run_exit_the_same_way(tmp_path) -> None:
    """The exit contract has two cases and not three: a remainder and no
    remainder are the same exit."""
    empty = new_repo(tmp_path / "empty")
    write(empty, "docs/notes.md", "no citations here\n")
    commit(empty)
    full = new_repo(tmp_path / "full")
    write(full, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(full)

    for root in (empty, full):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            assert report.main([str(root)]) == 0


# ==========================================================================
# THE OUTPUT CONTRACT — D2's shape, tested where the spec fixes behavior
# without giving it a scenario of its own.
# ==========================================================================

def test_the_human_table_never_headers_a_group_with_a_class_name(
        tmp_path) -> None:
    """CLASS IS NEVER A GROUPING LEVEL, in either grouping mode or either
    part."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md", f"{CITE}/add-absent/fixture.md\n")
    write(root, "docs/notes.md",
          f"see {CITE}/add-absent/walk-<DATE>.md\n"
          f"and {CITE}/add-other/proposal.md\n")
    commit(root)

    for mode in ([], ["--tokens"]):
        text = run_human(root, *mode)
        assert text.index("CLASSES (counted in TOKENS)") < text.index(
            "REMAINDER, ITEMIZED"), "the counts block precedes the itemized one"
        itemized = text[text.index("REMAINDER, ITEMIZED"):]
        for line in itemized.splitlines():
            stripped = line.strip()
            for name in report.CLASS_VOCABULARY:
                assert stripped != name, line
                assert not stripped.startswith(f"{name} ("), line


def test_grouping_by_token_lists_every_token_that_identity_grouping_lists(
        tmp_path) -> None:
    """`--tokens` changes the ORDER things are grouped in and never what is
    listed."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"a {CITE}/add-absent/one.md\nb {CITE}/add-absent/two.md\n"
          f"c {CITE}/add-other/three.md\n")
    commit(root)

    by_identity = run_json(root)
    by_token = run_json(root, "--tokens")
    assert set(entries(by_identity)) == set(entries(by_token))
    assert by_identity["grouping"] == "identity"
    assert by_token["grouping"] == "token"
    assert "identities" in by_identity and "tokens" in by_token


def test_the_json_token_object_carries_every_field_the_design_enumerates(
        tmp_path) -> None:
    """The `--json` object per token: `token`, `status`, `half`, `identity`,
    `remainder`, every occurrence as its own `{path:line, raw}` pair, `class`,
    and every flag as its own field."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-theirs/proposal.md"]
    for key in ("token", "status", "half", "identity", "remainder",
                "occurrences", "class", "flags"):
        assert key in record, key
    assert record["remainder"] == "proposal.md"
    occurrence = record["occurrences"][0]
    assert occurrence["at"] == "docs/notes.md:1"
    assert occurrence["path"] == "docs/notes.md" and occurrence["line"] == 1
    assert occurrence["raw"] == record["token"]


def test_the_json_token_object_carries_no_singular_raw_field(
        tmp_path) -> None:
    """`raw` IS A PER-OCCURRENCE VALUE AND NEVER A SINGULAR FIELD ON THE
    TOKEN."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"a {CITE}/add-absent/\nb {CITE}/add-absent\n")
    commit(root)

    record = entries(run_json(root))[f"{CITE}/add-absent"]
    assert "raw" not in record
    assert {o["raw"] for o in record["occurrences"]} == {
        f"{CITE}/add-absent/", f"{CITE}/add-absent"}


def test_the_human_itemized_entry_shows_a_raw_spelling_only_where_it_differs(
        tmp_path) -> None:
    """An occurrence with nothing to show is the ordinary case, not an
    omission."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md",
          f"a {CITE}/add-absent/\nb {CITE}/add-absent\n")
    commit(root)

    text = run_human(root)
    assert f"(raw: {CITE}/add-absent/)" in text
    assert f"(raw: {CITE}/add-absent)" not in text


def test_the_history_key_is_absent_rather_than_null_when_history_is_not_given(
        tmp_path) -> None:
    """The key is ABSENT, never `null`, when `--history` is not given, so two
    readings differing only in this key's presence are still the same series
    point."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    assert "history" not in data["identities"][0]
    for record in entries(data).values():
        assert "history" not in record
    assert "history:" not in run_human(root)


def test_history_is_probed_per_identity_and_carries_its_four_fields(
        tmp_path) -> None:
    """Under `--history`, each identity record carries `{probed, ever_tracked,
    first_commit, last_commit}` — and no `last_path`."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-was-here")
    commit(root, "the packet lands")
    subprocess.run(["rm", "-rf", str(root / "openspec" / "changes"
                                     / "add-was-here")], check=True)
    write(root, "docs/notes.md",
          f"a {CITE}/add-was-here/proposal.md\n"
          f"b {CITE}/add-never-here/proposal.md\n")
    commit(root, "the packet goes, the citations stay")

    data = run_json(root, "--history")
    by_identity = {group["identity"]: group for group in data["identities"]}
    was = by_identity["add-was-here"]["history"]
    never = by_identity["add-never-here"]["history"]
    assert was["probed"] is True and was["ever_tracked"] is True
    assert was["first_commit"] and was["last_commit"]
    assert "last_path" not in was
    assert never["ever_tracked"] is False
    assert never["first_commit"] is None and never["last_commit"] is None
    text = run_human(root, "--history")
    assert "history: never tracked" in text
    assert "history: tracked" in text


def test_history_never_changes_a_class_or_a_flag(tmp_path) -> None:
    """`--history` answers a different question and neither list was ever built
    to carry it."""
    root = new_repo(tmp_path / "repo")
    write(root, "examples/demo.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n")
    commit(root)

    without = entries(run_json(root))
    with_history = entries(run_json(root, "--history"))
    for token, record in without.items():
        assert with_history[token]["class"] == record["class"]
        assert with_history[token]["flags"] == record["flags"]


def test_all_lists_the_outcomes_the_default_only_counts(tmp_path) -> None:
    """`--all` also lists RESOLVED and NOT-A-PACKET-REFERENCE tokens."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, f"{CITE}/README.md", "the corpus's own readme\n")
    write(root, "docs/notes.md",
          f"a {CITE}/add-present/proposal.md\nb {CITE}/README.md\n"
          f"c {CITE}/add-absent/proposal.md\n")
    commit(root)

    default = entries(run_json(root))
    everything = entries(run_json(root, "--all"))
    assert set(default) == {f"{CITE}/add-absent/proposal.md"}
    assert f"{CITE}/add-present/proposal.md" in everything
    assert f"{CITE}/README.md" in everything


def test_both_formats_carry_the_same_headline_numbers(tmp_path) -> None:
    """A figure that differed between two formats of one run would be two
    readings nobody asked for."""
    root = new_repo(tmp_path / "repo")
    packet(root, "add-present")
    write(root, "docs/notes.md",
          f"codexFactory {CITE}/add-theirs/proposal.md\n"
          f"{CITE}/add-present/proposal.md\n{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    text = run_human(root)
    counts = data["counts"]
    assert f"distinct tokens          {counts['distinct_tokens']}" in text
    assert (f"INCLUSIVE remainder      "
            f"{counts['remainder_inclusive_tokens']} TOKENS") in text
    population = data["population"]
    assert (f"tracked ENTRIES in scope "
            f"{population['tracked_entries_in_scope']}") in text
    assert f"FILES read               {population['files_read']}" in text


def test_the_resolver_sentence_is_printed_verbatim_and_never_reworded(
        tmp_path) -> None:
    """D2 output rule 1: print the resolver's own `report` sentence, and do not
    re-write it in a second voice."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    data = run_json(root)
    record = entries(data)[f"{CITE}/add-absent/proposal.md"]
    assert "resolves to NOTHING in this tree" in record["report"]
    assert record["report"] in run_human(root)


def test_the_script_runs_as_a_command_and_prints_json_to_stdout(
        tmp_path) -> None:
    """`--json` is a BOOLEAN output-format flag taking no path: it writes to
    STDOUT and a caller redirects."""
    root = new_repo(tmp_path / "repo")
    write(root, "docs/notes.md", f"{CITE}/add-absent/proposal.md\n")
    commit(root)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(root), "--json"],
        capture_output=True, text=True)
    assert result.returncode == 0
    body = json.loads(result.stdout)
    assert body["counts"]["remainder_inclusive_tokens"] == 1


# ==========================================================================
# THE LIVE CORPUS — invariants only, never a count.
# ==========================================================================

@pytest.mark.skipif(not (REPO_ROOT / ".git").exists(),
                    reason="the live corpus needs this repository's own git")
def test_the_live_corpus_reading_holds_every_invariant_and_asserts_no_count(
        ) -> None:
    """The one live-corpus test: the arithmetic closes, every remainder entry
    names a citing file, the class totals sum to the remainder token total, the
    AMBIGUOUS row is present, and the exit is 0.

    NO COUNT IS ASSERTED. A count test goes red on every merge into `main` that
    touches any citation anywhere in the corpus, and the reproduction gate is
    evidence taken once at a named commit rather than a permanent assertion.
    """
    data = run_json(REPO_ROOT)
    population = data["population"]
    assert population["arithmetic_closes"] is True
    assert population["tracked_entries_in_scope"] == (
        population["files_read"] + population["skipped_not_a_file"]
        + population["skipped_link_leaving_the_root"]
        + population["skipped_undecodable"])
    counts = data["counts"]
    assert counts["raw_path_absent"]["closes"] is True
    assert "ambiguous" in counts["outcomes"]
    assert sum(counts["classes"].values()) == counts[
        "remainder_inclusive_tokens"]
    assert counts["remainder_inclusive_tokens"] == (
        counts["remainder_filtered_tokens"]
        + counts["flagged_remainder_entries"])
    assert counts["remainder_inclusive_identities"] <= counts[
        "remainder_inclusive_tokens"]
    for record in entries(data).values():
        assert record["occurrences"], record["token"]
        assert record["class"] in report.CLASS_VOCABULARY
        assert record["status"] in ("dangling", "ambiguous")


@pytest.mark.skipif(not (REPO_ROOT / ".git").exists(),
                    reason="the live corpus needs this repository's own git")
def test_the_report_mints_no_citation_token_of_its_own() -> None:
    """THE ACCEPTANCE CHECK THIS PACKET UNIQUELY OWES: the script is INSIDE the
    file population, so a citation-shaped string written in it would be a token
    the next run counts — the mechanism the design measured at +1 remainder for
    vendoring its own measurement instrument."""
    assert report.TOKEN_RE.findall(SCRIPT.read_text(encoding="utf-8")) == []
