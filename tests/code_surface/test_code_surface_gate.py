"""`gate-code-surface-declarations` § 3: the `code_surface:` grammar gate.

`openspec validate` (the external CLI) cannot be extended, so the house wiring
is `scripts/validate-code-surface.py` plus `test_corpus_code_surface_validates`
below, which runs it over every active change on every pull request — the same
enforcement route the sibling `scripts/validate-target-release.py` and the other
`scripts/validate-*.py` contract validators use, and the reason § 3.7 edits no
workflow: the required `pytest-suite` already runs everything under `tests/`.

EVERY TREE HERE IS BUILT IN A TMPDIR AND JUDGED AGAINST A REGISTER BUILT BESIDE
IT, so a test can never be made green by editing the repository's own register,
and the corpus tests at the end are the only ones that read the real one.

THE THREE REQUIREMENTS THIS FILE PINS, by the delta's own titles: *Code-surface
declaration grammar is gated* (the head, the opener, the reserved `none`, the
block scalar, the repeat, absence, the archive), *The declared repository set is
derived from the head and never from the gloss* (the derivation, and § 3.5a's
fail-closed rule with one test per FORBIDDEN SUBSTITUTE), and *Standing
code-surface divergence is named in a closed register* (the shape refusals, the
enforced closed baseline, and the asymmetric stale status).
"""
from __future__ import annotations

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "code_surface.py"
SCOPE_MODULE = ROOT / "scripts" / "scope_globs.py"
VALIDATOR = ROOT / "scripts" / "validate-code-surface.py"
SCOPE_VALIDATOR = ROOT / "scripts" / "validate-scope-globs.py"
REGISTER = ROOT / "scripts" / "code-surface-register.yaml"


def _load(name: str, path: Path):
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


cs = _load("code_surface", MODULE)
sg = _load("scope_globs", SCOPE_MODULE)


# --- tree builders ------------------------------------------------------------


def _proposal(root: Path, change: str, front: str, archived: bool = False,
              body: str = "# Proposal\n") -> Path:
    where = root / "openspec" / "changes"
    if archived:
        where = where / "archive"
    folder = where / change
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "proposal.md"
    path.write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")
    return path


def _register(root: Path, entries: str = "register: []\n") -> Path:
    path = root / "register.yaml"
    path.write_text(entries, encoding="utf-8")
    return path


def _entry_text(change: str, declaration: str,
                klass: str = "list-runs-into-prose",
                cited_to: list[str] | None = None,
                why: str = "a reason",
                retires_when: str = "an event") -> str:
    """One well-formed register file, serialized rather than hand-spelled.

    The declarations these entries carry are ordinary prose with apostrophes,
    colons and em dashes in them, and a hand-spelled YAML scalar would make this
    helper a second YAML writer whose quoting bugs would read as gate failures.
    `safe_dump` is the writer; the MALFORMED cases below are spelled by hand on
    purpose, because a malformed file is the thing under test.
    """
    entry = {
        "change": change,
        "declaration": declaration,
        "class": klass,
        "why": why,
        "cited_to": list(cited_to) if cited_to is not None
        else ["a document § a section"],
        "retires_when": retires_when,
    }
    return yaml.safe_dump({"register": [entry]}, sort_keys=False,
                          allow_unicode=True, width=10_000)


def _run(root: Path, register: Path | None = None):
    argv = [sys.executable, str(VALIDATOR), str(root)]
    if register is not None:
        argv += ["--register", str(register)]
    return subprocess.run(argv, capture_output=True, text=True)


# --- the declared head: the grammar's own shape -------------------------------


def test_a_bare_repository_is_a_head():
    assert cs.parse_head("openxFactory").repositories == ("openxFactory",)


def test_a_gloss_after_an_em_dash_is_not_judged():
    head = cs.parse_head(
        "openxFactory — `scripts/code_surface.py` (NEW), and NOT codexFactory, "
        "whose companion change is authored there")
    assert head.repositories == ("openxFactory",)


def test_a_gloss_after_an_opening_parenthesis_is_not_judged():
    assert cs.parse_head(
        "xFactory (the aggregation repo; two workflow files)"
    ).repositories == ("xFactory",)


def test_a_gloss_after_a_full_stop_is_not_judged():
    assert cs.parse_head(
        "openxFactory. No contract bundle is cut."
    ).repositories == ("openxFactory",)


def test_an_en_dash_a_colon_and_a_semicolon_open_a_gloss_too():
    """The opener set is the one the corpus and the house style write, widened
    past the three the conforming 38 used only by the three the archive and the
    house style also use — so the gate cannot refuse a form the estate writes."""
    for declaration in ("openxFactory – the surface",
                        "openxFactory: the surface",
                        "openxFactory; the surface"):
        assert cs.parse_head(declaration).repositories == ("openxFactory",)


def test_an_owner_name_address_is_admitted_on_the_same_terms():
    assert cs.parse_head(
        "opensoft/LedgerxWallet — the overlay boundary"
    ).repositories == ("opensoft/LedgerxWallet",)


def test_both_identifier_spellings_may_share_one_head():
    assert cs.parse_head(
        "openxFactory, opensoft/Keycloak-Install — two surfaces"
    ).repositories == ("openxFactory", "opensoft/Keycloak-Install")


@pytest.mark.parametrize("separator", [", ", ",", " and ", " + ", ", and "])
def test_every_ratified_list_separator_is_admitted(separator):
    head = cs.parse_head(f"openxFactory{separator}codexFactory — a gloss")
    assert head.repositories == ("openxFactory", "codexFactory")


def test_a_head_with_no_gloss_at_all_is_admitted():
    """D0 counted two such records in the archive and none active; the grammar
    admits the form rather than requiring an explanation nobody owes."""
    assert cs.parse_head("openxFactory, codexFactory").repositories == (
        "openxFactory", "codexFactory")


def test_a_head_that_runs_into_prose_with_no_opener_is_refused():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("openxFactory, and it is THREE FILES at realization")
    assert "runs into prose" in str(caught.value)


def test_a_possessive_is_refused():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("openxFactory's half of this packet carries NO CODE — x")
    assert "runs into prose" in str(caught.value)


def test_an_apposition_is_refused():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("xFactory aggregation repo (.github/workflows/x.yml")
    assert "runs into prose" in str(caught.value)


def test_a_head_ending_on_a_separator_is_refused():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("openxFactory and ")
    assert "separator" in str(caught.value)


def test_a_declaration_that_opens_with_punctuation_is_refused():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("— openxFactory is the surface")
    assert "no repository identifier" in str(caught.value)


def test_the_refusal_quotes_the_declaration_but_does_not_print_all_of_it():
    """A finding names "the text the declaration carries" — and the widest of
    these runs to 11,678 bytes, so an unbounded echo would bury the finding in
    the gloss it is refusing to judge."""
    long_gloss = "openxFactory's " + ("word " * 4000)
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head(long_gloss)
    message = str(caught.value)
    assert len(message) < 1000
    assert "…" in message


# --- `none` is the sentinel and is reserved out of REPOSITORY IDENTIFIER ------
# D9 (a). `none` matches the repository-name shape like any other lowercase
# word, so a grammar that merely `or`-ed the two alternatives read
# `none, openxFactory` as a two-member list — a NON-EMPTY derived set for a
# change whose declaration says the surface is empty.


def test_a_bare_none_is_the_empty_surface():
    head = cs.parse_head("none")
    assert head.is_none and head.repositories == ()


def test_a_none_with_a_gloss_is_still_the_empty_surface():
    """Three of the four `none` carriers measured carry a gloss, and the delta
    admits it: the gloss is explanation and not declaration (D8.5)."""
    head = cs.parse_head(
        "none — this packet edits no runtime artifact in openxFactory or "
        "codexFactory, both of which the gloss names")
    assert head.is_none and head.repositories == ()


@pytest.mark.parametrize("declaration", [
    "none, openxFactory",
    "openxFactory and none",
    "openxFactory, none, codexFactory",
    "none and openxFactory — a gloss",
])
def test_a_mixed_none_head_is_refused_wherever_the_token_sits(declaration):
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head(declaration)
    message = str(caught.value)
    assert "sentinel `none`" in message
    assert "self-contradictory" in message


def test_the_sentinel_is_matched_exactly_and_None_capitalized_is_not_it():
    """A case-insensitive sentinel would read `None of this repository's …` —
    an ordinary way to start a sentence — as the empty surface. It is prose
    running into a declaration, and it is refused as such."""
    with pytest.raises(cs.CodeSurfaceError):
        cs.parse_head("None of this repository's runtime artifacts move")


# --- the YAML block-scalar indicator, refused BY NAME -------------------------
# BOTH STYLES, AND THEY ARE TWO: `|` is the LITERAL style and `>` the FOLDED one
# (YAML 1.2 § 8.1.2, § 8.1.3). The refusal says "block-scalar", which is the
# accurate term for the pair and the ratified requirement's own TITLE's; the
# delta's explanatory sentence calls both "folding indicators", and that slip is
# recorded rather than copied into the message a reader actually meets.


@pytest.mark.parametrize("indicator", [">-", "|", ">", "|-", ">+", "|2-"])
def test_a_block_scalar_declaration_is_refused_by_name(indicator):
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head(f"{indicator}\n  openxFactory — the surface")
    message = str(caught.value)
    assert "YAML block-scalar indicator" in message
    assert indicator in message
    # and it never labels the LITERAL style as a folding one, or vice versa
    assert "folding indicator" not in message


def test_the_block_scalar_refusal_is_not_merely_an_unreadable_head():
    """The requirement says the refusal SHALL say what it is, because the
    author who wrote those two characters was reaching for a structure this
    field does not have."""
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head(">-\n  openxFactory — the surface")
    assert "runs into prose" not in str(caught.value)
    assert "PROSE HEADER" in str(caught.value)


# --- reading the declaration --------------------------------------------------


def test_a_declared_field_is_present(tmp_path):
    proposal = _proposal(tmp_path, "c", "code_surface: openxFactory — a gloss")
    present, text = cs.declaration(proposal)
    assert present and text.startswith("openxFactory")


def test_an_undeclared_field_is_absent(tmp_path):
    proposal = _proposal(tmp_path, "c", "target_release: implemented")
    assert cs.declaration(proposal) == (False, None)


def test_a_document_with_no_fence_declares_nothing(tmp_path):
    folder = tmp_path / "openspec" / "changes" / "c"
    folder.mkdir(parents=True)
    path = folder / "proposal.md"
    path.write_text("# Proposal\n\ncode_surface: openxFactory\n",
                    encoding="utf-8")
    assert cs.declaration(path) == (False, None)


def test_a_repeated_declaration_is_refused_not_half_read(tmp_path):
    proposal = _proposal(
        tmp_path, "c",
        "code_surface: openxFactory\ncode_surface: codexFactory")
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.declaration(proposal)
    assert "more than once" in str(caught.value)


def test_a_repeated_declaration_is_a_finding_not_a_crash(tmp_path):
    _proposal(tmp_path, "c",
              "code_surface: openxFactory\ncode_surface: codexFactory")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "more than once" in result.stdout


def test_an_indented_gloss_line_is_a_gloss_and_not_a_repeat(tmp_path):
    """The repeat guard is anchored at column 0, which is the loader's own
    notion of a header line. An INDENTED continuation is gloss, and the
    requirement says judge the head and NEVER the gloss."""
    proposal = _proposal(
        tmp_path, "c",
        "code_surface: openxFactory — the field\n"
        "  code_surface: is what this field is called")
    present, text = cs.declaration(proposal)
    assert present
    assert cs.parse_head(text).repositories == ("openxFactory",)


def test_a_strict_loader_refusal_is_raised_not_swallowed(tmp_path):
    proposal = _proposal(tmp_path, "c",
                         "scope_globs: &a\n  R: ['x/**']\nother: *a")
    with pytest.raises(cs.CodeSurfaceError):
        cs.declaration(proposal)


# --- absence is the promoted default; present-but-empty is not ----------------


def test_declaring_nothing_takes_the_promoted_default(tmp_path):
    _proposal(tmp_path, "c", "target_release: implemented")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 active proposals, 0 declaring" in result.stdout


def test_a_present_but_empty_declaration_is_refused(tmp_path):
    _proposal(tmp_path, "c", "code_surface:\ntarget_release: implemented")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "with no value" in result.stdout


def test_the_empty_declarations_refusal_names_the_remedy():
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("")
    assert "OMITTING the key" in str(caught.value)


# --- the gate, end to end -----------------------------------------------------


def test_an_active_unreadable_head_is_refused(tmp_path):
    _proposal(tmp_path, "c",
              "code_surface: openxFactory, and it is THREE FILES at realization")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "openspec/changes/c/proposal.md" in result.stdout
    assert "runs into prose" in result.stdout


def test_the_finding_names_the_path_and_the_declaration_text(tmp_path):
    _proposal(tmp_path, "c", "code_surface: xFactory aggregation repo (x")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "openspec/changes/c/proposal.md" in result.stdout
    assert "xFactory aggregation repo" in result.stdout


def test_a_conforming_declaration_passes(tmp_path):
    _proposal(tmp_path, "c", "code_surface: openxFactory — a gloss")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 a repository list" in result.stdout


def test_a_none_declaration_passes(tmp_path):
    _proposal(tmp_path, "c", "code_surface: none (a doc-only change)")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 `none`" in result.stdout


def test_an_unreadable_proposal_is_reported_not_crashed(tmp_path):
    folder = tmp_path / "openspec" / "changes" / "c"
    folder.mkdir(parents=True)
    (folder / "proposal.md").write_bytes(
        b"---\ncode_surface: \xff\xfe\n---\n\n# Proposal\n")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "cannot be read" in result.stdout


# --- the archive is READ AND COUNTED and judged NEVER -------------------------


def test_an_archived_unreadable_head_is_not_a_finding(tmp_path):
    _proposal(tmp_path, "2026-01-01-old",
              "code_surface: openxFactory's half of this packet", archived=True)
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 of them outside the grammar" in result.stdout


def test_the_run_reports_how_many_such_records_the_archive_carries(tmp_path):
    _proposal(tmp_path, "2026-01-01-old",
              "code_surface: openxFactory's half", archived=True)
    _proposal(tmp_path, "2026-01-02-older", "code_surface: openxFactory — ok",
              archived=True)
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert ("archive (read, never judged): 2 proposals, 2 declaring, "
            "1 of them outside the grammar") in result.stdout


# --- the discovery walk cannot leave the scanned tree (§ 3.2a (ii)) -----------
# `Path.is_file()` FOLLOWS SYMLINKS, so the walk that FINDS proposals is as much
# an escape surface as the register path is. A proposal read from outside
# `REPO_ROOT` would be judged and named in a finding as though this tree carried
# it, and a DANGLING link is the same defect wearing the other face: the
# proposal vanishes and the tree is judged on a corpus it does not have. Neither
# is a judgment about the scanned tree, so a path that fails the anchored test is
# DROPPED rather than reported.


def test_a_symlinked_active_proposal_is_not_read(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / "proposal.md"
    external.write_text("---\ncode_surface: openxFactory's half\n---\n\n# X\n",
                        encoding="utf-8")
    root = tmp_path / "repo"
    folder = root / "openspec" / "changes" / "a-packet"
    folder.mkdir(parents=True)
    (folder / "proposal.md").symlink_to(external)
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 active proposals, 0 declaring" in result.stdout


def test_a_regular_proposal_inside_a_symlinked_change_directory_is_not_read(
        tmp_path):
    """The leaf being perfectly ordinary changes nothing: the escape is a
    property of the PATH, not of its last component."""
    outside = tmp_path / "outside" / "a-packet"
    outside.mkdir(parents=True)
    (outside / "proposal.md").write_text(
        "---\ncode_surface: openxFactory's half\n---\n\n# X\n",
        encoding="utf-8")
    root = tmp_path / "repo"
    changes = root / "openspec" / "changes"
    changes.mkdir(parents=True)
    (changes / "a-packet").symlink_to(outside, target_is_directory=True)
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 active proposals" in result.stdout


def test_a_dangling_active_proposal_symlink_is_skipped_and_never_crashes(
        tmp_path):
    root = tmp_path / "repo"
    folder = root / "openspec" / "changes" / "a-packet"
    folder.mkdir(parents=True)
    (folder / "proposal.md").symlink_to(tmp_path / "gone.md")
    _proposal(root, "b-packet", "code_surface: openxFactory — a gloss")
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 active proposals" in result.stdout


def test_a_symlinked_archived_proposal_is_not_counted(tmp_path):
    """The archive is READ AND COUNTED and never judged, so an escape there is
    a lie about what the archive carries rather than a false finding — and it is
    closed by the same call."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "proposal.md").write_text(
        "---\ncode_surface: openxFactory's half\n---\n\n# X\n",
        encoding="utf-8")
    root = tmp_path / "repo"
    folder = root / "openspec" / "changes" / "archive" / "2026-01-01-old"
    folder.mkdir(parents=True)
    (folder / "proposal.md").symlink_to(outside / "proposal.md")
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive (read, never judged): 0 proposals" in result.stdout


def test_a_regular_archived_proposal_in_a_symlinked_directory_is_not_counted(
        tmp_path):
    outside = tmp_path / "outside" / "2026-01-01-old"
    outside.mkdir(parents=True)
    (outside / "proposal.md").write_text(
        "---\ncode_surface: openxFactory's half\n---\n\n# X\n",
        encoding="utf-8")
    root = tmp_path / "repo"
    archive = root / "openspec" / "changes" / "archive"
    archive.mkdir(parents=True)
    (archive / "2026-01-01-old").symlink_to(outside, target_is_directory=True)
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive (read, never judged): 0 proposals" in result.stdout


def test_a_dangling_archived_proposal_symlink_is_skipped_and_never_crashes(
        tmp_path):
    root = tmp_path / "repo"
    folder = root / "openspec" / "changes" / "archive" / "2026-01-01-old"
    folder.mkdir(parents=True)
    (folder / "proposal.md").symlink_to(tmp_path / "gone.md")
    _proposal(root, "2026-01-02-older", "code_surface: openxFactory — ok",
              archived=True)
    result = _run(root, _register(root))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive (read, never judged): 1 proposals" in result.stdout


def test_repo_root_reached_via_a_symlink_still_finds_its_proposals(tmp_path):
    """THE BOUNDARY, PINNED EXPLICITLY — the negative that keeps the guard from
    over-refusing. `repo_root` is resolved on BOTH sides of the comparison, so a
    scan of a tree that is ITSELF reached through a symlink (a scratch tree
    under a symlinked `/tmp`, say) is an ordinary scan and not the escape."""
    real = tmp_path / "real"
    real.mkdir()
    _proposal(real, "a-packet", "code_surface: openxFactory — a gloss")
    _proposal(real, "2026-01-01-old", "code_surface: none", archived=True)
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    result = _run(link, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 active proposals" in result.stdout
    assert "archive (read, never judged): 1 proposals" in result.stdout


# --- a resolution that CANNOT ANSWER is still ANSWERED (#1074) ----------------
# `Path.resolve(strict=True)` signals a SYMLINK LOOP by raising `RuntimeError`,
# which is a subclass of NEITHER `OSError` NOR `ValueError`, so the clause that
# closes every escape above was open at exactly that failure and `_unescaped`
# RAISED where its own prose promises a DROP. Measured on `Python 3.12.3`, the
# version `.github/workflows/pytest-suite.yml` pins for the required check:
# `validate-code-surface.py` ended in a traceback rather than a report on a
# minimal tree whose `proposal.md` was a two-link `a -> b -> a` loop, and a
# traceback is neither a drop nor a finding — it is the gate refusing to report
# on the tree at all, the one outcome the guard's docstring was written to
# prevent. (`harden-path-escape-helpers-against-symlink-loops` § 3.2; the
# requirement is *A containment guard answers every resolution failure and
# raises none*.)


def _symlink_loop(directory: Path, name: str) -> Path:
    """An `a -> b -> a` two-link symlink loop at `directory / name`, BUILT AT
    TEST TIME AND NEVER COMMITTED.

    A committed loop is tracked as two ordinary git objects (mode `120000`) and
    would arrive through a pull request like any other file — which is why it is
    the shape these guards defend against — but as a FIXTURE it would be met by
    every recursive reader this estate runs, not only the guard under test, and
    a fixture that reds tools unrelated to the defect it proves is a second
    defect introduced to demonstrate the first. The packet's § 3.7 forbids it
    and *A symlink-loop proof is built at test time and never committed* is the
    rule.
    """
    a = directory / name
    b = directory / f"{name}--loop-b"
    a.symlink_to(b)
    b.symlink_to(a)
    return a


def test_a_symlink_loop_drops_the_candidate_in_all_three_positions(tmp_path):
    """THE GUARD ANSWERS IN EVERY POSITION THE LOOP CAN STAND IN. Against the
    unfixed clause (`except OSError:`) each of the three calls below RAISED
    `RuntimeError` out of `_unescaped` instead of returning `None`.

    THE THREE POSITIONS ARE THE REQUIREMENT'S OWN, and the second is the one a
    reviewer's intuition misses: the leaf is a perfectly ordinary name and
    ordinariness is a property of the ONE component it is asserted of, so a
    guard that reads the leaf learns nothing about what carried it there.

    THE THIRD POSITION IS A CLAIM ABOUT THE CANDIDATE AND NOT ABOUT A ROOT-SIDE
    READ. `candidate = repo_root / relative` already traverses the loop, so
    `candidate.resolve(strict=True)` raises and the root resolution on the NEXT
    line is never executed; what is proved is a candidate path whose failing
    component happens to be the root, which is the scenario's subject.
    (`harden-path-escape-helpers-against-symlink-loops` § 3.2, `design.md` D5.)
    """
    # (1) the CANDIDATE'S OWN LEAF is the loop
    leaf_root = tmp_path / "leaf"
    packet = leaf_root / "openspec" / "changes" / "a-packet"
    packet.mkdir(parents=True)
    loop = _symlink_loop(packet, "proposal.md")
    with pytest.raises(RuntimeError):
        loop.resolve(strict=True)  # the fixture is worth nothing if it does not
    assert cs._unescaped(
        leaf_root, Path("openspec/changes/a-packet/proposal.md")) is None

    # (2) a PARENT COMPONENT, above a leaf that is a perfectly ordinary name
    parent_root = tmp_path / "parent"
    parent_root.mkdir()
    _symlink_loop(parent_root, "openspec")
    assert cs._unescaped(
        parent_root, Path("openspec/changes/a-packet/proposal.md")) is None

    # (3) the SCANNED ROOT ITSELF is reached through the loop
    base = tmp_path / "base"
    base.mkdir()
    looped_root = _symlink_loop(base, "repo")
    assert cs._unescaped(looped_root, Path("proposal.md")) is None


# --- the register -------------------------------------------------------------


def test_a_missing_register_refuses(tmp_path):
    _proposal(tmp_path, "c", "code_surface: openxFactory — a gloss")
    result = _run(tmp_path, tmp_path / "absent.yaml")
    assert result.returncode == 2, result.stdout + result.stderr
    assert "CANNOT RUN" in result.stdout


def test_a_register_without_the_list_refuses(tmp_path):
    path = _register(tmp_path, "entries: []\n")
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "top-level `register:` list" in str(caught.value)


def test_an_entry_that_is_not_a_mapping_refuses(tmp_path):
    path = _register(tmp_path, "register:\n  - a string\n")
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "is not a mapping" in str(caught.value)


@pytest.mark.parametrize(
    "field", ["change", "declaration", "class", "why", "retires_when"])
def test_an_entry_missing_a_required_text_key_refuses(tmp_path, field):
    text = yaml.safe_load(_entry_text("c", "openxFactory's half"))
    del text["register"][0][field]
    path = _register(tmp_path, yaml.safe_dump(text, sort_keys=False))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert f"`{field}:`" in str(caught.value)


def test_an_entry_without_a_citation_refuses(tmp_path):
    text = yaml.safe_load(_entry_text("c", "openxFactory's half"))
    del text["register"][0]["cited_to"]
    path = _register(tmp_path, yaml.safe_dump(text, sort_keys=False))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "nobody's word" in str(caught.value)


def test_an_entry_with_an_empty_citation_list_refuses(tmp_path):
    path = _register(tmp_path, _entry_text("c", "x's half", cited_to=[]))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "cited_to" in str(caught.value)


def test_an_entry_whose_citation_is_a_bare_string_refuses(tmp_path):
    text = yaml.safe_load(_entry_text("c", "x's half"))
    text["register"][0]["cited_to"] = "a document"
    path = _register(tmp_path, yaml.safe_dump(text, sort_keys=False))
    with pytest.raises(cs.CodeSurfaceError):
        cs.load_register(path)


def test_an_entry_with_a_blank_citation_item_refuses(tmp_path):
    path = _register(tmp_path, _entry_text("c", "x's half", cited_to=["  "]))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "non-empty text" in str(caught.value)


def test_a_repeated_entry_refuses(tmp_path):
    text = yaml.safe_load(_entry_text("c", "x's half"))
    # DEEP-COPIED, because `safe_dump` emits a YAML ALIAS for a shared nested
    # object and the strict loader refuses an alias BEFORE it ever reaches the
    # repeat check — a test that shipped the shallow copy would pass on the
    # wrong refusal.
    text["register"].append(copy.deepcopy(text["register"][0]))
    path = _register(tmp_path, yaml.safe_dump(text, sort_keys=False))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "repeats" in str(caught.value)


@pytest.mark.parametrize("change", ["../elsewhere", "a/b", ".hidden"])
def test_an_entry_whose_change_reaches_a_path_refuses(tmp_path, change):
    path = _register(tmp_path, _entry_text(change, "x's half"))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "change-directory name" in str(caught.value)


def test_an_entry_with_a_class_outside_the_closed_set_refuses(tmp_path):
    path = _register(tmp_path, _entry_text("c", "x's half", klass="whatever"))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "not one of" in str(caught.value)


def test_every_declared_class_is_one_the_measurement_found():
    assert cs.REGISTER_CLASSES == (
        "block-scalar", "possessive", "apposition", "list-runs-into-prose")


# --- the register is REMOVABLE, NEVER ADDABLE --------------------------------
# The closure is ENFORCED and not merely declared: without the baseline a later
# pull request could append an entry and make any unreadable declaration pass
# with the gate green — the ratchet failing silently in the one direction that
# matters. The sibling's own bench found exactly this hole in the sibling's own
# register; this packet adopts the finding before paying for it again.


def test_an_entry_outside_the_closed_baseline_refuses(tmp_path):
    path = _register(tmp_path, _entry_text("c", "openxFactory's half"))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path, closed=(("c", cs.declaration_digest("other")),))
    assert "REMOVABLE, NEVER ADDABLE" in str(caught.value)


def test_an_entry_whose_declaration_moved_off_the_baseline_refuses(tmp_path):
    """An edit of one byte in a registered declaration changes its digest, so
    the entry no longer matches the baseline and the run refuses until the
    baseline moves with it — in the same pull request, where the diff shows the
    act."""
    path = _register(tmp_path, _entry_text("c", "openxFactory's half "))
    with pytest.raises(cs.CodeSurfaceError):
        cs.load_register(
            path, closed=(("c", cs.declaration_digest("openxFactory's half")),))


def test_a_baseline_wider_than_the_register_is_lawful(tmp_path):
    """Removal is lawful — a corrected declaration or an archived packet retires
    its entry — so a pair stays in the baseline after its entry goes. The
    baseline is a CEILING, never a floor."""
    path = _register(tmp_path, _entry_text("c", "openxFactory's half"))
    entries = cs.load_register(path, closed=(
        ("c", cs.declaration_digest("openxFactory's half")),
        ("gone", cs.declaration_digest("a retired declaration")),
    ))
    assert len(entries) == 1


def test_a_register_named_on_the_command_line_carries_no_house_baseline(
        tmp_path):
    """`--register PATH` is for a test tree or a consuming repository, and that
    repository's closure is its own record to keep."""
    path = _register(tmp_path, _entry_text("c", "openxFactory's half"))
    assert len(cs.load_register(path)) == 1


def test_the_house_register_is_within_its_own_closed_baseline():
    entries = cs.load_register(REGISTER)
    assert len(entries) == len(cs.CLOSED_REGISTER)


# --- the register PATH is the same escape the corpus walk closes (§ 3.2a (i)) -
# `Path.is_file()` and `Path.read_text()` BOTH follow symlinks, so a committed
# link at the register path — the default beside the module, or one named on
# `--register` — would let the gate consume exception data from outside the
# checkout, silently and differently per runner. The check runs UNCONDITIONALLY
# before `is_file()` or `read_text()`, so no branch treats a supplied path
# differently from the default and no branch can forget one of them.


def test_a_symlinked_register_refuses(tmp_path):
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    real = _register(real_dir, _entry_text("c", "x's half"))
    link = tmp_path / "register.yaml"
    link.symlink_to(real)
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(link)
    assert "symlink" in str(caught.value)


def test_a_symlinked_register_pointing_outside_the_tree_refuses(
        tmp_path, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside-code-surface-register")
    real = _register(outside, _entry_text("c", "x's half"))
    link = tmp_path / "register.yaml"
    link.symlink_to(real)
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(link)
    assert "symlink" in str(caught.value)


def test_a_dangling_register_symlink_refuses_as_a_symlink_not_a_crash(tmp_path):
    """A dangling link is the same defect wearing the other face:
    `is_symlink()` is true whether or not the target exists, so this refuses
    with the SAME message as a live one, never a bare `does not exist` and never
    an unhandled `OSError`."""
    link = tmp_path / "register.yaml"
    link.symlink_to(tmp_path / "gone.yaml")
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(link)
    assert "symlink" in str(caught.value)


def test_a_symlinked_register_named_on_the_command_line_refuses_end_to_end(
        tmp_path):
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    real = _register(real_dir, _entry_text("c", "x's half"))
    link = tmp_path / "register.yaml"
    link.symlink_to(real)
    result = _run(tmp_path, link)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "symlink" in result.stdout


def test_a_register_reached_through_a_symlinked_ancestor_refuses(
        tmp_path, tmp_path_factory):
    """A leaf-only check does not close it: `linkdir/register.yaml` has a
    perfectly ORDINARY leaf and `read_text()` still follows `linkdir`."""
    outside = tmp_path_factory.mktemp("outside-code-surface-ancestor")
    _register(outside, _entry_text("c", "x's half"))
    linkdir = tmp_path / "linkdir"
    linkdir.symlink_to(outside)
    path = linkdir / "register.yaml"
    assert not path.is_symlink()  # the leaf itself is perfectly ordinary
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(path)
    assert "symlink" in str(caught.value)


def test_a_register_reached_through_a_symlinked_ancestor_refuses_end_to_end(
        tmp_path, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside-code-surface-ancestor-cli")
    _register(outside, _entry_text("c", "x's half"))
    linkdir = tmp_path / "linkdir"
    linkdir.symlink_to(outside)
    result = _run(tmp_path, linkdir / "register.yaml")
    assert result.returncode == 2, result.stdout + result.stderr
    assert "symlink" in result.stdout


def test_a_dangling_ancestor_link_refuses_as_a_symlink_not_a_crash(tmp_path):
    linkdir = tmp_path / "linkdir"
    linkdir.symlink_to(tmp_path / "gone-dir")
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(linkdir / "register.yaml")
    assert "symlink" in str(caught.value)


def test_the_default_register_path_is_checked_by_the_same_guard(
        monkeypatch, tmp_path):
    """THE DEFAULT ARGUMENT IS THE SAME CODE, PINNED EXPLICITLY. A function
    default is bound once, at definition time, so patching the module-level
    `REGISTER_PATH` attribute alone would never reach a bare `load_register()`
    call; `__defaults__` is patched instead, to prove the exact no-argument call
    `scan()` (and so the pytest gate) makes is guarded too."""
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    real = _register(real_dir, _entry_text("c", "x's half"))
    link = tmp_path / "code-surface-register.yaml"
    link.symlink_to(real)
    monkeypatch.setattr(cs.load_register, "__defaults__", (link, None))
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register()
    assert "symlink" in str(caught.value)


# --- a registered declaration is REPORTED, and a stale entry REFUSES ---------
# The two refusals are asymmetric and stay so: an unreadable declaration the
# register does not name is a statement about the PROPOSAL (exit 1); a register
# entry that matches nothing is a statement about the REGISTER (exit 2).


def test_a_registered_declaration_is_reported_not_refused(tmp_path):
    declaration = "openxFactory, and it is THREE FILES at realization"
    _proposal(tmp_path, "c", f"code_surface: {declaration}")
    result = _run(tmp_path, _register(tmp_path, _entry_text("c", declaration)))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 named by the register" in result.stdout


def test_an_entry_that_matches_nothing_refuses(tmp_path):
    _proposal(tmp_path, "c", "code_surface: openxFactory — a gloss")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("gone", "openxFactory's half")))
    assert result.returncode == 2, result.stdout + result.stderr
    assert "matched NOTHING (stale)" in result.stdout


def test_an_entry_stops_matching_when_the_declaration_is_corrected(tmp_path):
    """The remedy IS the event that forces the re-examination: correcting the
    declaration retires the entry, and the run refuses until it is deleted."""
    _proposal(tmp_path, "c", "code_surface: openxFactory — corrected")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory, and it is corrected")))
    assert result.returncode == 2, result.stdout + result.stderr
    assert "stale" in result.stdout


def test_an_entry_whose_packet_archived_refuses(tmp_path):
    _proposal(tmp_path, "2026-01-01-c", "code_surface: openxFactory's half",
              archived=True)
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory's half")))
    assert result.returncode == 2, result.stdout + result.stderr
    assert "matched NOTHING (stale)" in result.stdout


def test_a_finding_and_a_stale_entry_are_both_reported(tmp_path):
    """Where BOTH occur the run prints both and exits 1, so neither is hidden
    by the other."""
    _proposal(tmp_path, "c", "code_surface: openxFactory's half")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("gone", "another unreadable head's text")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "matched NOTHING (stale)" in result.stdout
    assert "validation FAILED" in result.stdout


def test_a_stale_entry_and_a_finding_for_the_SAME_change_are_ONE_event(tmp_path):
    """THE TWO SECTIONS ARE CROSS-REFERENCED WHERE THEY NAME THE SAME CHANGE.

    Both refusals firing for one change is not two faults: the declaration was
    EDITED (so the entry recording the old text matches nothing) and the new
    text is off-grammar too (so it is a finding). Printed as two unrelated
    blocks, the obvious reading is "delete the stale entry" — which leaves the
    finding standing — and the other obvious reading, appending the new text,
    is the closure violation the baseline refuses. So the run says it is one
    event, above both blocks, and names both halves of the remedy.
    """
    _proposal(tmp_path, "c", "code_surface: openxFactory, and it is EDITED")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory, and it is the OLD text")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "SAME CHANGE" in result.stdout
    assert "one event, not two" in result.stdout
    assert "c: the register entry is stale AND the live declaration is "\
           "off-grammar" in result.stdout
    assert "CONFORM THE DECLARATION" in result.stdout
    assert "RE-REGISTER" in result.stdout
    assert "Do NOT just delete the entry" in result.stdout
    # the two asymmetric blocks are still printed, unchanged, beneath it
    assert "matched NOTHING (stale)" in result.stdout
    assert "validation FAILED" in result.stdout


def test_two_DIFFERENT_changes_are_NOT_cross_referenced(tmp_path):
    """The link is drawn only where the two reports name the SAME change: a
    stale entry for one packet and a finding against another are two facts and
    are left as two."""
    _proposal(tmp_path, "c", "code_surface: openxFactory's half")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("gone", "another unreadable head's text")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "SAME CHANGE" not in result.stdout
    assert "matched NOTHING (stale)" in result.stdout
    assert "validation FAILED" in result.stdout


# --- ...AND THE SAME-EVENT LINK IS KEYED ON THE FINDING'S CLASS ---------------
#
# `Report.findings` carries TWO classes: OFF_GRAMMAR (the document was read and
# its head is not admitted) and UNREADABLE (the document did not read at all --
# a strict-loader refusal, non-UTF-8 bytes, an I/O failure). Only the first can
# be the edited-declaration event. Keyed on the change id alone, a stale entry
# beside an UNREADABLE proposal was reported as "the declaration was edited
# without being brought into the grammar", which told an author to conform or
# RE-REGISTER text nobody can read -- and the claim is not merely unhelpful but
# unfounded, because nothing was read and whether the declaration changed at
# all is UNKNOWN.


def _unreadable_proposal(root: Path, change: str) -> Path:
    """A proposal whose BYTES are not UTF-8, so the strict loader refuses it and
    `declaration()` raises -- the UNREADABLE finding class, reached the way a
    real one is reached rather than by constructing a `Finding` by hand."""
    folder = root / "openspec" / "changes" / change
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "proposal.md"
    path.write_bytes(b"---\ncode_surface: \xff\xfe\n---\n\n# Proposal\n")
    return path


def test_the_finding_KIND_is_CARRIED_and_never_inferred_from_the_text(tmp_path):
    """The classes are a FIELD, not a guess. Read straight off `scan`, because
    the CLI behaviour below is only as sound as this distinction is."""
    _proposal(tmp_path, "readable", "code_surface: openxFactory's half")
    _unreadable_proposal(tmp_path, "broken")
    report = cs.scan(tmp_path, cs.load_register(_register(tmp_path)))
    assert {f.change: f.kind for f in report.findings} == {
        "readable": cs.OFF_GRAMMAR, "broken": cs.UNREADABLE}


def test_a_DECLARATION_whose_text_IS_the_sentinel_is_still_OFF_GRAMMAR(
        tmp_path):
    """WHY THE CLASS IS A FIELD AND NOT THE SENTINEL STRING. `<unreadable>` is
    a text a real declaration CAN carry, and it reaches `_excerpt` unchanged --
    so a consumer keying on `declaration == "<unreadable>"` would classify a
    document it READ as one it could not read, and give the wrong remedy in the
    one direction nothing else would catch. Keyed on `kind` it is what it is:
    the ordinary edited-declaration event."""
    _proposal(tmp_path, "c", "code_surface: <unreadable>")
    report = cs.scan(tmp_path, cs.load_register(_register(tmp_path)))
    assert [f.declaration for f in report.findings] == [
        cs.UNREADABLE_DECLARATION]                        # the TEXT collides...
    assert [f.kind for f in report.findings] == [cs.OFF_GRAMMAR]  # ...not the CLASS
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory, and it is the OLD text")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "SAME CHANGE" in result.stdout
    assert "CANNOT BE READ" not in result.stdout


def test_a_stale_entry_beside_an_UNREADABLE_proposal_is_NOT_the_edited_event(
        tmp_path):
    """THE DEFECT. A registered change whose proposal has become unreadable,
    its entry left standing. Before, this printed "one event, not two" and told
    the author to CONFORM or RE-REGISTER a declaration nobody can read."""
    _unreadable_proposal(tmp_path, "c")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory, and it is the OLD text")))
    assert result.returncode == 1, result.stdout + result.stderr
    # the edited-declaration event is NOT claimed...
    assert "SAME CHANGE" not in result.stdout
    assert "one event, not two" not in result.stdout
    assert "CONFORM THE DECLARATION" not in result.stdout
    assert "RE-REGISTER the new text" not in result.stdout
    # ...and the fact that IS true is stated in its place
    assert "CANNOT BE READ" in result.stdout
    assert "WHETHER THE DECLARATION CHANGED IS UNKNOWN" in result.stdout
    assert "do not RE-REGISTER text no reader can read" in result.stdout
    assert "MAKE THE DOCUMENT READABLE FIRST" in result.stdout
    # both asymmetric blocks still print beneath it, unchanged
    assert "matched NOTHING (stale)" in result.stdout
    assert "validation FAILED" in result.stdout


def test_the_unreadable_cross_reference_WARNS_OFF_DELETING_THE_ENTRY(tmp_path):
    """The stale block's own advice -- "delete the entry: the exception
    outlived its condition" -- is exactly what must NOT be done here, because
    the condition was never observed. The cross-reference says so, so the two
    lines cannot be read as agreeing."""
    _unreadable_proposal(tmp_path, "c")
    result = _run(tmp_path, _register(
        tmp_path, _entry_text("c", "openxFactory, and it is the OLD text")))
    assert ("Deleting the entry now would retire an exception on evidence "
            "nobody has") in result.stdout
    assert ("delete the entry: the exception outlived its condition"
            in result.stdout)                  # the generic line still prints


def test_an_UNREADABLE_proposal_with_NO_stale_entry_draws_NO_cross_reference(
        tmp_path):
    """The cross-reference is drawn only where a register entry is involved.
    An unreadable proposal on its own is one fact and stays one."""
    _unreadable_proposal(tmp_path, "c")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "SAME CHANGE" not in result.stdout
    assert "CANNOT BE READ" not in result.stdout
    assert "validation FAILED" in result.stdout


def test_BOTH_cross_references_at_once_stay_TWO_DISTINCT_EVENTS(tmp_path):
    """One change edited off-grammar, another unreadable, each with its own
    stale entry. The blocks stay separate, each names only its own change, and
    the edited one comes first because it is the actionable one."""
    _proposal(tmp_path, "edited", "code_surface: openxFactory, and it is EDITED")
    _unreadable_proposal(tmp_path, "broken")
    register = tmp_path / "register.yaml"
    register.write_text(yaml.safe_dump({"register": [
        {"change": ch, "declaration": "openxFactory, the OLD text of " + ch,
         "class": "list-runs-into-prose", "why": "a reason",
         "cited_to": ["a document section"], "retires_when": "an event"}
        for ch in ("edited", "broken")]}, sort_keys=False, allow_unicode=True,
        width=10_000), encoding="utf-8")
    result = _run(tmp_path, register)
    assert result.returncode == 1, result.stdout + result.stderr
    edited_line = result.stdout.split("SAME CHANGE")[1].splitlines()[1]
    unread_line = result.stdout.split("CANNOT BE READ")[1].splitlines()[1]
    # each block names ITS OWN change and not the other; matched on the
    # `  - <id>:` prefix rather than on the bare word, because the unreadable
    # block's own prose contains "edited-declaration event" by design.
    assert edited_line.startswith("  - edited:") and "broken:" not in edited_line
    assert unread_line.startswith("  - broken:") and "edited:" not in unread_line
    assert (result.stdout.index("SAME CHANGE")
            < result.stdout.index("CANNOT BE READ"))


def test_the_corpus_moves_between_drafting_and_landing(tmp_path):
    """THE REGISTER REQUIREMENT'S THIRD SCENARIO, PINNED AS ITS OWN SHAPE.

    *The corpus moves between drafting and landing*: "WHEN a proposal declaring
    an unreadable head lands on the main line after this packet's register was
    written and before the gate itself lands — THEN the register MUST be
    re-measured at the head the gate lands on, and the new carrier disposed of
    there; AND a register carried unchanged from the drafting tree MUST NOT be
    treated as evidence about the landing tree."

    The mechanism was realized and proven by hand at the landing (the register
    grew seven to eight for `encode-wallet-authority-rulings-r6-r12`), but no
    named test carried the scenario's own shape. This is that test: a register
    written at the drafting tree, a carrier that arrives afterwards, the
    unchanged register REFUSING to cover it, and the disposition — the entry AND
    its baseline pair, in one act — clearing the run.
    """
    drafting = "openxFactory, and it is THE DRAFTING CARRIER"
    arrival = "contracts/signed-execution-chain/digest-construction.schema.yaml"
    _proposal(tmp_path, "drafted", f"code_surface: {drafting}")

    # (a) the register as written at the drafting tree: one entry, and the run
    #     is clean on the tree it was measured against.
    register = _register(tmp_path, _entry_text("drafted", drafting))
    result = _run(tmp_path, register)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 named by the register" in result.stdout
    assert "0 outside the grammar" in result.stdout

    # (b) THE CORPUS MOVES: a proposal declaring an unreadable head lands after
    #     the register was written. The UNCHANGED register is not evidence
    #     about this tree — the run refuses, naming the new carrier and not the
    #     old one.
    _proposal(tmp_path, "arrived", f"code_surface: {arrival}")
    result = _run(tmp_path, register)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "1 outside the grammar" in result.stdout
    assert "openspec/changes/arrived/proposal.md" in result.stdout
    assert "openspec/changes/drafted/proposal.md" not in result.stdout

    # (c) THE NEW CARRIER IS DISPOSED OF AT THE LANDING HEAD: re-measured, then
    #     registered. Two entries, and the run is clean again.
    both = yaml.safe_dump({"register": [
        yaml.safe_load(_entry_text("drafted", drafting))["register"][0],
        yaml.safe_load(_entry_text("arrived", arrival))["register"][0],
    ]}, sort_keys=False, allow_unicode=True, width=10_000)
    result = _run(tmp_path, _register(tmp_path, both))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 named by the register" in result.stdout
    assert "0 outside the grammar" in result.stdout

    # (d) AND THE DISPOSITION COSTS A BASELINE EDIT IN THE SAME ACT, which is
    #     what keeps the register removable-never-addable while the corpus
    #     moves under it. Against the DRAFTING baseline the second entry is
    #     refused; only the baseline carrying BOTH pairs admits it.
    drafting_baseline = (("drafted", cs.declaration_digest(drafting)),)
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.load_register(_register(tmp_path, both), closed=drafting_baseline)
    assert "REMOVABLE, NEVER ADDABLE" in str(caught.value)
    landing_baseline = drafting_baseline + (
        ("arrived", cs.declaration_digest(arrival)),)
    assert len(cs.load_register(_register(tmp_path, both),
                                closed=landing_baseline)) == 2


def test_an_entry_authorizes_nothing_beyond_its_own_declaration(tmp_path):
    """An entry suspends the grammar's refusal for ONE declaration. A SECOND
    packet writing the same unreadable shape is refused on its own account."""
    declaration = "openxFactory, and it is THREE FILES"
    _proposal(tmp_path, "c", f"code_surface: {declaration}")
    _proposal(tmp_path, "d", f"code_surface: {declaration}")
    result = _run(tmp_path, _register(tmp_path, _entry_text("c", declaration)))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "openspec/changes/d/proposal.md" in result.stdout
    assert "openspec/changes/c/proposal.md" not in result.stdout


# --- § 3.5: the derived set comes from the HEAD and never from the gloss ------


def test_the_derived_set_is_the_head_and_never_the_gloss():
    front = {"code_surface":
             "openxFactory — and NOT codexFactory, whose companion change is "
             "authored there; the pin points at OpsxFactory and the workflow "
             "runs on GitHub with Postgres behind it"}
    assert sg.code_surface_repositories(front, change="c") == {"openxFactory"}


def test_a_multi_repository_head_derives_every_member():
    front = {"code_surface": "openxFactory and codexFactory (two surfaces)"}
    assert sg.code_surface_repositories(front, change="c") == {
        "openxFactory", "codexFactory"}


def test_a_none_head_derives_the_empty_set_and_the_gloss_adds_nothing():
    """A reader that returned the gloss's words for a `none` head would return a
    non-empty surface for a change that declared none, which inverts the very
    distinction the archive gate turns on."""
    front = {"code_surface":
             "none — this packet touches no runtime artifact in openxFactory, "
             "codexFactory or OpsxFactory"}
    assert sg.code_surface_repositories(front, change="c") == set()


def test_an_OMITTED_key_derives_the_EMPTY_SET_the_promoted_default_declares():
    """ABSENCE IS THE PROMOTED DEFAULT, AND THE DEFAULT DECLARES `none`.

    *Realization axis declaration* makes "a proposal without the declarations a
    doc-only change (`code_surface: none`, `target_release: implemented`) by
    default"; this packet's grammar requirement restates it ("ABSENCE IS THE
    PROMOTED DEFAULT AND SHALL NEVER BE A FINDING … a proposal that declares
    nothing declares the default"); and the derivation requirement rules the
    head the default declares ("WHERE THE HEAD IS `none` THE DERIVED SET SHALL
    BE EMPTY"). So an omitted key derives the EMPTY SET, by way of the default
    head it takes — and NOT the absence carrier, whose own population the next
    paragraph names: "a proposal [that] passes the gate only because the closed
    register names it — its head being one the grammar cannot read".
    """
    derived = sg.code_surface_repositories({"target_release": "implemented"},
                                           change="c")
    assert derived == set()
    assert not isinstance(derived, sg.NoDeclaredRepositories)


def test_an_OMITTED_key_beside_a_scope_is_the_ORDINARY_finding_against_the_scope(
        tmp_path):
    """And the consequence at the point of enforcement: the refusal is the
    ordinary cross-consistency one — a finding against the SCOPE, which names a
    repository the change declares no surface for — and NOT the fail-closed
    carrier's, which would send the author to correct a `code_surface:`
    declaration they never wrote."""
    front = {"scope_globs": {"codexFactory": ["scripts/**"]}}
    with pytest.raises(sg.ScopeGlobsError) as caught:
        sg.validate_scope_globs(
            front["scope_globs"],
            code_surface_repos=sg.code_surface_repositories(front, change="c"))
    message = str(caught.value)
    assert not isinstance(caught.value, sg.CodeSurfaceHeadError), message
    assert "not in code_surface" in message
    assert "NO REPOSITORY SET CAN BE DERIVED" not in message


def test_an_OMITTED_key_beside_a_scope_reds_the_scope_gate_END_TO_END(tmp_path):
    """The same fact through the CLI, so the default is pinned where an author
    meets it: exit 1 with the change id prefixed and the ORDINARY message, not
    the code-surface carrier's."""
    _proposal(tmp_path, "c",
              "target_release: implemented\n"
              "scope_globs:\n  codexFactory:\n    - 'scripts/**'")
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "c: " in result.stdout
    assert "not in code_surface" in result.stdout
    assert "NO REPOSITORY SET CAN BE DERIVED" not in result.stdout


def test_a_PRESENT_value_that_is_not_text_still_fails_closed():
    """The carrier keeps the arm it was built for. An omitted key is a
    declaration nobody wrote; a key PRESENT in a shape no reader can read is a
    declaration the author began and did not make, and the promoted default is
    available by omitting the key rather than by writing it unreadably."""
    derived = sg.code_surface_repositories(
        {"code_surface": ["openxFactory"]}, change="c")
    assert isinstance(derived, sg.NoDeclaredRepositories)
    assert "not text" in derived.detail
    with pytest.raises(sg.CodeSurfaceHeadError):
        sg.validate_scope_globs({"R": ["scripts/**"]},
                                code_surface_repos=derived)


def test_a_PRESENT_but_EMPTY_value_still_fails_closed():
    """`code_surface:` written with nothing after it is the refusal the grammar
    requirement states in terms ("a declaration present with no value SHALL be
    refused, because the author wrote the key and the default is available by
    omitting it"), and the consumer fails closed on it rather than reading the
    default the author did not take."""
    derived = sg.code_surface_repositories({"code_surface": ""}, change="c")
    assert isinstance(derived, sg.NoDeclaredRepositories)
    assert "with no value" in derived.detail


def test_the_absence_carrier_QUOTES_the_declaration_it_carries():
    """The carrier's `declaration` is carried TO BE READ: the refusal names the
    text the declaration carries, bounded to one line so the gloss it refuses to
    derive from cannot bury the refusal."""
    declaration = ("openxFactory, and it is THREE FILES " + "x " * 200).strip()
    derived = sg.code_surface_repositories(
        {"code_surface": declaration}, change="c", register=[])
    assert isinstance(derived, sg.NoDeclaredRepositories)
    excerpt = derived.excerpt()
    assert len(excerpt) <= 120
    assert excerpt.endswith("\u2026")
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs({"R": ["scripts/**"]},
                                code_surface_repos=derived)
    message = str(caught.value)
    assert excerpt in message
    # NAMED ONCE, NEVER TWICE: the head grammar's own refusal already quotes
    # the declaration, so the carrier does not print it a second time.
    assert message.count(excerpt) == 1


def test_the_absence_carrier_QUOTES_a_declaration_the_detail_does_NOT_carry():
    """The other side of "named once": the not-text arm's detail never quotes
    the value, so the refusal must — or it refuses a declaration without ever
    showing the author what it read."""
    derived = sg.code_surface_repositories(
        {"code_surface": ["openxFactory", "codexFactory"]}, change="c")
    assert isinstance(derived, sg.NoDeclaredRepositories)
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs({"R": ["scripts/**"]},
                                code_surface_repos=derived)
    assert derived.excerpt() in str(caught.value)
    assert "openxFactory" in str(caught.value)


def test_a_head_that_REPEATS_the_sentinel_NAMES_THE_DUPLICATE():
    """`none, none` refuses on the same rule as a mixed head, but it is not a
    mix: it reported "1 repository identifier(s) ()" — a miscount and an empty
    parenthetical where the reader looks for the name of the thing complained
    about. The duplicate is named instead."""
    for raw, times in (("none, none", 2), ("none and none", 2),
                       ("none, none, none", 3)):
        with pytest.raises(cs.CodeSurfaceError) as caught:
            cs.parse_head(raw)
        message = str(caught.value)
        assert f"repeats the empty-surface sentinel `none` {times} times" \
            in message, message
        assert "()" not in message, message
        assert "repository identifier(s)" not in message, message
    # and a head that really IS mixed still says so, naming the identifiers.
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head("openxFactory, none, codexFactory")
    assert "mixes the empty-surface sentinel `none` with 2 repository " \
           "identifier(s) (openxFactory, codexFactory)" in str(caught.value)


def test_a_structured_scope_naming_a_gloss_only_repository_is_refused(tmp_path):
    """The scenario, end to end: a scope key that appears in the GLOSS and not
    in the head is a scope naming a repository the change declares no
    realization surface for."""
    _proposal(
        tmp_path, "c",
        "code_surface: openxFactory — a companion change lands in codexFactory\n"
        "scope_globs:\n  codexFactory:\n    - 'scripts/**'")
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "not in code_surface" in result.stdout


def test_a_structured_scope_naming_the_declared_head_passes(tmp_path):
    _proposal(
        tmp_path, "c",
        "code_surface: openxFactory — a companion change lands in codexFactory\n"
        "scope_globs:\n  openxFactory:\n    - 'scripts/**'")
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_a_bare_iterable_still_works_as_a_head_derived_set():
    """`validate_scope_globs(..., code_surface_repos={"R"})` is what every
    shipped caller passes, and it keeps working unedited — read as a
    head-derived set carrying no registered-exception context."""
    sg.validate_scope_globs({"R": ["scripts/**"]}, code_surface_repos={"R"})
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_scope_globs({"S": ["scripts/**"]}, code_surface_repos={"R"})


# --- § 3.5a: FAIL CLOSED where the register carries the head ------------------
# A proposal the register names has NO head-derived set, so the cross-check
# REFUSES, naming BOTH the proposal and the entry. The two substitutes an
# implementer would otherwise reach for are forbidden BY NAME, and each gets its
# own refusal test: one proves the run must not grant a whole-declaration set,
# the other that it must not grant an empty one.


def _registered_scope_tree(tmp_path) -> tuple[Path, str]:
    declaration = ("openxFactory, and it is THREE FILES at realization, one of "
                   "them in codexFactory")
    _proposal(
        tmp_path, "c",
        f"code_surface: {declaration}\n"
        "scope_globs:\n  openxFactory:\n    - 'scripts/**'")
    return tmp_path, declaration


def test_a_registered_packet_declaring_a_scope_is_refused(tmp_path):
    root, declaration = _registered_scope_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "c" / "proposal.md")
    register = cs.load_register(_register(root, _entry_text("c", declaration)))
    carrier = sg.code_surface_repositories(front, change="c",
                                           register=register)
    assert isinstance(carrier, sg.NoDeclaredRepositories)
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs(front["scope_globs"],
                                code_surface_repos=carrier)
    message = str(caught.value)
    assert "c declares scope_globs" in message           # names the proposal
    assert "CLOSED code-surface register" in message      # names the entry
    assert "entry `c`" in message
    assert "list-runs-into-prose" in message


def test_the_refusal_forbids_the_whole_declaration_fallback_by_name(tmp_path):
    """FORBIDDEN SUBSTITUTE 1. Falling back to a set derived from the WHOLE
    declaration would re-admit the gloss as an authorization surface, which is
    the single defect this requirement exists to close. The proof is that a
    scope key the GLOSS names — and only the gloss — is refused rather than
    granted."""
    root, declaration = _registered_scope_tree(tmp_path)
    _proposal(
        root, "d",
        f"code_surface: {declaration}\n"
        "scope_globs:\n  codexFactory:\n    - 'scripts/**'")
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "d" / "proposal.md")
    register = cs.load_register(_register(root, _entry_text("d", declaration)))
    carrier = sg.code_surface_repositories(front, change="d",
                                           register=register)
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs(front["scope_globs"],
                                code_surface_repos=carrier)
    assert "does NOT fall back" in str(caught.value)
    # and the permissive reading is not merely unused — it is unreachable:
    # `codexFactory` IS a word of this declaration, and it is still refused.
    assert "codexFactory" in declaration


def test_the_refusal_forbids_the_empty_set_substitution_by_name(tmp_path):
    """FORBIDDEN SUBSTITUTE 2. An EMPTY set would make every scope key
    unnameable while reporting the fault in the WRONG PLACE — the author would
    read a refusal about their structured scope when the defect is in their code
    surface. The proof is the message: it is NOT the generic
    "names repository … not in code_surface"."""
    root, declaration = _registered_scope_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "c" / "proposal.md")
    register = cs.load_register(_register(root, _entry_text("c", declaration)))
    carrier = sg.code_surface_repositories(front, change="c",
                                           register=register)
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs(front["scope_globs"],
                                code_surface_repos=carrier)
    message = str(caught.value)
    assert "not in code_surface" not in message
    assert "does NOT substitute an empty set" in message
    assert "NO REPOSITORY SET CAN BE DERIVED" in message


def test_the_refusal_names_the_remedy(tmp_path):
    root, declaration = _registered_scope_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "c" / "proposal.md")
    register = cs.load_register(_register(root, _entry_text("c", declaration)))
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs(
            front["scope_globs"],
            code_surface_repos=sg.code_surface_repositories(
                front, change="c", register=register))
    assert "BRING THE DECLARATION INTO THE GRAMMAR" in str(caught.value)


def test_an_unreadable_head_the_register_does_not_name_also_fails_closed(
        tmp_path):
    """A declaration nobody registered has no head-derived set either, so the
    consumer fails closed there too — and says the register does not carry it,
    rather than implying an exception exists."""
    root, declaration = _registered_scope_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "c" / "proposal.md")
    carrier = sg.code_surface_repositories(front, change="c", register=[])
    assert carrier.register_entry is None
    with pytest.raises(sg.CodeSurfaceHeadError) as caught:
        sg.validate_scope_globs(front["scope_globs"],
                                code_surface_repos=carrier)
    assert "not carried by the closed code-surface register" in str(caught.value)


def test_the_absence_carrier_is_never_read_as_no_cross_check_asked_for(
        tmp_path):
    """`None` means "do not cross-check at all" (`validate_scope_globs` skips),
    which is exactly why the absence of a derivable set is a CARRIER: a `None`
    here would SKIP the check the requirement demands must REFUSE."""
    root, declaration = _registered_scope_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / "c" / "proposal.md")
    carrier = sg.code_surface_repositories(front, change="c", register=[])
    assert carrier is not None
    sg.validate_scope_globs(front["scope_globs"], code_surface_repos=None)


def test_a_registered_packet_declaring_a_scope_reds_the_scope_gate_end_to_end(
        tmp_path):
    """THE CLI SURFACE, WITH A LIVE REGISTER ENTRY PROPAGATING THROUGH IT.

    The refusal must reach the run, not only the module — and it must reach it
    NAMING THE ENTRY, which is the ratified requirement's own wording
    ("refused by the cross-consistency check, naming the proposal and its
    register entry"). THE REGISTER IS PASSED, and that is the point of the
    test rather than an incidental: without `--code-surface-register` the
    derivation loads the register beside the IMPORTED MODULE — this
    repository's own — which does not carry a change called `c`, so the run
    took the UNREGISTERED arm and this test proved the other one only by its
    name. That was a bench finding, and it is fixed on both sides: the CLI now
    takes a register for the tree it scans, and this test supplies one.
    """
    root, declaration = _registered_scope_tree(tmp_path)
    register = _register(root, _entry_text("c", declaration))
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root),
         "--code-surface-register", str(register)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "c: " in result.stdout
    assert "NO REPOSITORY SET CAN BE DERIVED" in result.stdout
    # THE ENTRY, NAMED — the half the house register could never have supplied.
    assert "CLOSED code-surface register" in result.stdout
    assert "entry `c`" in result.stdout
    assert "list-runs-into-prose" in result.stdout
    # and NOT the unregistered arm's wording.
    assert "not carried by the closed code-surface register" not in result.stdout


def test_an_UNREGISTERED_unreadable_head_reds_the_scope_gate_end_to_end(
        tmp_path):
    """The OTHER arm at the CLI, kept as its own test now that the one above
    exercises the registered one: an unreadable head no register names fails
    closed too, and says the register does not carry it rather than implying an
    exception exists."""
    root, _ = _registered_scope_tree(tmp_path)
    empty = _register(root)
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root),
         "--code-surface-register", str(empty)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "c: " in result.stdout
    assert "NO REPOSITORY SET CAN BE DERIVED" in result.stdout
    assert "not carried by the closed code-surface register" in result.stdout


def test_the_scope_gate_defaults_the_register_to_the_SCANNED_tree(tmp_path):
    """With no flag, the register is `REPO_ROOT/scripts/code-surface-register.yaml`
    when the scanned tree carries one — so a tree is judged against ITS OWN
    exceptions rather than against whichever file sits beside the imported
    module."""
    root, declaration = _registered_scope_tree(tmp_path)
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "code-surface-register.yaml").write_text(
        _entry_text("c", declaration), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "entry `c`" in result.stdout
    assert "not carried by the closed code-surface register" not in result.stdout


# --- THE REGISTER IS THE SCANNED TREE'S OR IT IS NOTHING ----------------------
#
# The step above resolves `REPO_ROOT/scripts/code-surface-register.yaml` when the
# scanned tree carries one. The two cases where it does NOT are these, and both
# used to end at `register=None`, which is the derivation's instruction to load
# the register BESIDE THE IMPORTED MODULE — this repository's own. A tree was
# then judged against exceptions it does not carry, silently, in a message that
# named an entry and told its author to delete it from a file they do not have.
# `scope_globs.NO_REGISTER` is the absence spelled as itself; `None` keeps its
# one meaning, and the CLI never passes it.


def _a_live_house_entry() -> dict:
    """One entry of THIS repository's own register, whose declaration is a
    SINGLE LINE so a fixture proposal can reproduce it verbatim as the prose
    header it is.

    READ FROM THE LIVE FILE RATHER THAN PASTED, so the probe cannot rot into a
    change id the house register stopped carrying and pass vacuously ever
    after: the day no entry qualifies, this raises instead.
    """
    for entry in cs.load_register(REGISTER):
        if "\n" not in entry["declaration"]:
            return entry
    raise AssertionError(
        "the house register carries no single-line declaration; these probes "
        "need one they can reproduce in a fixture proposal verbatim")


def _house_entry_tree(tmp_path) -> tuple[Path, dict]:
    """A tree carrying ONE proposal that reproduces a live house register
    entry — its change id AND its declaration — and NO register of its own.

    Every precondition that makes this a probe rather than a coincidence is
    asserted here: the declaration round-trips through the reader unchanged,
    the house register really would match it, and the tree really carries no
    `scripts/` of its own. Without the middle one the tests below would pass
    against the unfixed CLI too.
    """
    entry = _a_live_house_entry()
    _proposal(tmp_path, entry["change"],
              f"code_surface: {entry['declaration']}\n"
              "scope_globs:\n  openxFactory:\n    - 'scripts/**'")
    front = sg.read_front_matter(
        tmp_path / "openspec" / "changes" / entry["change"] / "proposal.md")
    assert front["code_surface"] == entry["declaration"]
    assert cs.register_entry_for(entry["change"], front["code_surface"],
                                 cs.load_register(REGISTER)) is not None
    assert not (tmp_path / "scripts").exists()
    return tmp_path, entry


def test_a_scanned_tree_with_NO_register_is_NOT_judged_against_the_HOUSE_one(
        tmp_path):
    """THE DEFECT, PINNED. A tree carrying no exception file at all was told
    its declaration is TOLERATED by the closed register — measured, before the
    fix, on this exact fixture:

        Its declaration is carried by the CLOSED code-surface register — entry
        `amend-kill-switch-to-declared-test-companion`, class `possessive`,
        retiring when the owning packet re-punctuates its declaration … and the
        entry MUST be deleted in that same pull request.

    None of that is about the tree being judged. The declaration is now refused
    as UNREGISTERED, which is the fact: nothing in that tree tolerates it.
    """
    root, entry = _house_entry_tree(tmp_path)
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NO REPOSITORY SET CAN BE DERIVED" in result.stdout
    assert "not carried by the closed code-surface register" in result.stdout
    # THE ASSERTIONS THAT FAIL ON A REVERT. `CLOSED` in capitals is the
    # tolerated arm's own wording and appears nowhere else; the entry name is
    # the house file's. (The entry's CLASS is deliberately not asserted on:
    # `possessive` and `apposition` are words the grammar's own refusal uses.)
    assert f"entry `{entry['change']}`" not in result.stdout
    assert "CLOSED code-surface register" not in result.stdout


def test_a_scanned_tree_register_that_CANNOT_BE_USED_refuses_not_falls_back(
        tmp_path):
    """A register PRESENT in the scanned tree and unusable REFUSES — the named
    flag's semantics, for the file the tree carries whether or not an operator
    typed its path. `code_surface.load_register`'s own rule is the authority
    ("a register that cannot be used REFUSES rather than being ignored"), and
    the direction the old comment missed is measured here: the fallback was not
    to nothing, it was to the register BESIDE THE VALIDATOR."""
    root, entry = _house_entry_tree(tmp_path)
    (root / "scripts").mkdir()
    (root / "scripts" / "code-surface-register.yaml").write_text(
        "register: [this is not a closed sequence\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "CANNOT RUN" in result.stdout
    assert "the scanned tree's code-surface register" in result.stdout
    assert "does NOT fall back" in result.stdout
    assert f"entry `{entry['change']}`" not in result.stdout
    assert "CLOSED code-surface register" not in result.stdout
    assert "Traceback" not in result.stderr, result.stderr


# --- THE DEFAULT PROBE ASKS PRESENCE, NOT SHAPE -------------------------------
#
# Resolving the scanned tree's register is TWO questions, and only the first
# belongs to the CLI: is there something at `scripts/code-surface-register.yaml`,
# and — if so — can it be used? `Path.is_file()` answers NEITHER cleanly. It
# FOLLOWS THE LINK and reports only "a regular file is readable at the end of
# this path", so a DANGLING SYMLINK and a DIRECTORY at that name both came back
# False and the scan proceeded with `NO_REGISTER` — the value that means NO
# ENTRY TOLERATES ANYTHING — about a tree that plainly carries something there.
# Both are `load_register` REFUSALS (the leaf link refused UNREAD by its symlink
# guard; the directory by that reader's own `is_file()` check), so the defect was
# a REFUSAL REPORTED AS A JUDGMENT: exit 1 against an empty register instead of
# exit 2, in the one direction the packet names — whether an entry tolerates a
# declaration is UNKNOWN when nothing could be read, never `no`.
#
# The probe is now `is_symlink() or exists()` (`os.path.lexists`) OVER the
# loader's own ancestor climb: present in ANY form — or reached through a symlink
# at ANY level — goes to `load_register`, and ABSENT WITH A CLEAN ANCESTRY is the
# only `NO_REGISTER`. That is the SAME BOUNDARY `--code-surface-register` has
# always had, where a named path is handed to the reader whatever shape it is in.
# The leaf half is measured below; the ancestor half, which the leaf cannot see
# at all, is `test_the_default_register_probe_asks_the_ANCESTRY_not_only_the_leaf`
# beneath it.


def _default_register_tree(tmp_path, shape: str) -> tuple[Path, Path]:
    """A tree whose one proposal carries an unreadable head, with
    `scripts/code-surface-register.yaml` in one of the five shapes a path can be
    in.

    WHEREVER BYTES ARE REACHABLE AT ALL THEY NAME THE CHANGE, which is what
    makes the register entry quoted in the output a measurement rather than a
    coincidence: the run names entry `c` only if that file was read, and the
    escaped-symlink case proves by its ABSENCE that bytes from outside the tree
    were not.
    """
    root, declaration = _registered_scope_tree(tmp_path)
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    default = scripts / "code-surface-register.yaml"
    if shape == "dangling-symlink":
        default.symlink_to(tmp_path / "nowhere" / "code-surface-register.yaml")
    elif shape == "symlink-to-a-real-file":
        outside = tmp_path / "outside"
        outside.mkdir()
        target = outside / "code-surface-register.yaml"
        target.write_text(_entry_text("c", declaration), encoding="utf-8")
        default.symlink_to(target)
    elif shape == "directory":
        default.mkdir()
    elif shape == "absent":
        pass
    elif shape == "regular-file":
        default.write_text(_entry_text("c", declaration), encoding="utf-8")
    else:  # pragma: no cover - the parametrization below is closed
        raise AssertionError(f"unknown shape {shape!r}")
    return root, default


@pytest.mark.parametrize(
    "shape, is_file_says, present, code, expected, forbidden",
    [
        # THE DEFECT, PINNED TWICE — the two shapes `is_file()` calls absent.
        ("dangling-symlink", False, True, 2,
         ("CANNOT RUN", "the scanned tree's code-surface register",
          "reached through a symlink", "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        ("directory", False, True, 2,
         ("CANNOT RUN", "the scanned tree's code-surface register",
          "cannot be used", "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        # ALREADY CLOSED, KEPT BESIDE THEM: `is_file()` follows the link and
        # says True, and the refusal comes from the reader either way.
        ("symlink-to-a-real-file", True, True, 2,
         ("CANNOT RUN", "reached through a symlink", "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        # THE ONLY `NO_REGISTER`: nothing there in any form.
        ("absent", False, False, 1,
         ("NO REPOSITORY SET CAN BE DERIVED",
          "not carried by the closed code-surface register"),
         ("CANNOT RUN", "entry `c`")),
        # AND THE ORDINARY CASE, so the parametrization measures the fix rather
        # than a validator that refuses everything.
        ("regular-file", True, True, 1,
         ("NO REPOSITORY SET CAN BE DERIVED", "CLOSED code-surface register",
          "entry `c`"),
         ("CANNOT RUN", "not carried by the closed code-surface register")),
    ])
def test_the_default_register_probe_is_PRESENCE_in_every_shape(
        tmp_path, shape, is_file_says, present, code, expected, forbidden):
    """Five shapes one path can be in, and the boundary each lands on.

    THE TWO PROBES ARE ASSERTED APART FIRST. `is_file_says` is what the old
    probe answered and `present` what the new one does; they DIVERGE on exactly
    the dangling symlink and the directory, which is why those two are the
    defect and why asserting the exit code alone would not have caught it.
    """
    root, default = _default_register_tree(tmp_path, shape)
    assert default.is_file() is is_file_says
    assert (default.is_symlink() or default.exists()) is present
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == code, result.stdout + result.stderr
    for text in expected:
        assert text in result.stdout, result.stdout
    for text in forbidden:
        assert text not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr


# --- AND IT ASKS THE ANCESTRY, NOT ONLY THE LEAF ------------------------------
#
# `load_register` refuses a register reached through a symlink AT THE LEAF OR AT
# ANY ANCESTOR, and the climb is UNANCHORED. The leaf probe above sees only the
# first half of that: with `REPO_ROOT/scripts` a symlink to a directory that does
# NOT carry `code-surface-register.yaml`, `is_symlink()` and `exists()` are BOTH
# false at the leaf, so the scan called the path ABSENT and judged the tree with
# `NO_REGISTER` — while THE SAME PATH named on `--code-surface-register` was
# refused (exit 2) by that ancestor guard. Two safety boundaries for one path,
# and the escape was in the direction the packet names: the tree let through is
# the one whose register DIRECTORY points outside the checkout.
#
# So the probe asks the ancestry FIRST, with `code_surface._has_symlinked_
# ancestor` — the loader's own function, imported rather than copied, because a
# second copy of the rule is a copy that drifts.


def _ancestor_linked_register_tree(tmp_path, shape: str) -> tuple[Path, Path]:
    """A tree whose one proposal carries an unreadable head, with
    `scripts/code-surface-register.yaml` reached — or not — through a SYMLINKED
    ANCESTOR.

    The register bytes, wherever they are reachable, name the change, so `entry
    `c`` in the output is a measurement: it appears only if the file was read,
    and its ABSENCE from the refusals proves bytes from the far side of a link
    were not.

    The returned root is the path the scan is HANDED, which for the deep shape
    is the link and not the directory it points at.
    """
    root, declaration = _registered_scope_tree(tmp_path)
    scripts = root / "scripts"
    if shape == "scripts-is-a-link-to-a-dir-WITHOUT-the-register":
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        scripts.symlink_to(elsewhere, target_is_directory=True)
    elif shape == "scripts-is-a-link-to-a-dir-WITH-the-register":
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "code-surface-register.yaml").write_text(
            _entry_text("c", declaration), encoding="utf-8")
        scripts.symlink_to(elsewhere, target_is_directory=True)
    elif shape == "the-repo-root-itself-is-a-link":
        scripts.mkdir()
        link = tmp_path / "repo-link"
        link.symlink_to(root, target_is_directory=True)
        root = link
    elif shape == "absent-under-a-clean-ancestry":
        scripts.mkdir()
    elif shape == "present-under-a-clean-ancestry":
        scripts.mkdir()
        (scripts / "code-surface-register.yaml").write_text(
            _entry_text("c", declaration), encoding="utf-8")
    else:  # pragma: no cover - the parametrization below is closed
        raise AssertionError(f"unknown shape {shape!r}")
    return root, root / "scripts" / "code-surface-register.yaml"


@pytest.mark.parametrize(
    "shape, leaf_present, ancestry_linked, code, expected, forbidden",
    [
        # THE DEFECT: an ancestor link with NOTHING at the leaf. Both halves of
        # the leaf probe say absent, and the reader refuses the very same path.
        ("scripts-is-a-link-to-a-dir-WITHOUT-the-register", False, True, 2,
         ("CANNOT RUN", "the scanned tree's code-surface register",
          "reached through a symlink", "any directory between it and the top",
          "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        # THE SAME ANCESTOR LINK ONE STEP HIGHER, where the leaf is likewise
        # nothing: the climb is UNANCHORED, so it sees this too.
        ("the-repo-root-itself-is-a-link", False, True, 2,
         ("CANNOT RUN", "reached through a symlink", "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        # ALREADY CLOSED, KEPT BESIDE THEM: the leaf probe reached this one on
        # its own, and the refusal is the same reader's.
        ("scripts-is-a-link-to-a-dir-WITH-the-register", True, True, 2,
         ("CANNOT RUN", "reached through a symlink", "does NOT fall back"),
         ("entry `c`", "NO REPOSITORY SET CAN BE DERIVED")),
        # THE ONLY `NO_REGISTER` LEFT: nothing at the leaf AND a clean ancestry.
        ("absent-under-a-clean-ancestry", False, False, 1,
         ("NO REPOSITORY SET CAN BE DERIVED",
          "not carried by the closed code-surface register"),
         ("CANNOT RUN", "entry `c`")),
        # AND THE ORDINARY TREE, so the climb is measured as a DISCRIMINATION
        # rather than as a validator that refuses everything.
        ("present-under-a-clean-ancestry", True, False, 1,
         ("NO REPOSITORY SET CAN BE DERIVED", "CLOSED code-surface register",
          "entry `c`"),
         ("CANNOT RUN", "not carried by the closed code-surface register")),
    ])
def test_the_default_register_probe_asks_the_ANCESTRY_not_only_the_leaf(
        tmp_path, shape, leaf_present, ancestry_linked, code, expected,
        forbidden):
    """Five paths, and the boundary each lands on once the ancestry is asked.

    THE TWO HALVES ARE ASSERTED APART FIRST. `leaf_present` is what
    `is_symlink() or exists()` answers and `ancestry_linked` what the loader's
    climb does; they DIVERGE on exactly the two dangling-below-a-link shapes,
    which is why those are the defect and why asserting the exit code alone
    would not have caught it — `absent-under-a-clean-ancestry` produces the very
    same leaf answer and must still be `NO_REGISTER`.
    """
    root, default = _ancestor_linked_register_tree(tmp_path, shape)
    assert (default.is_symlink() or default.exists()) is leaf_present
    assert cs._has_symlinked_ancestor(default) is ancestry_linked
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == code, result.stdout + result.stderr
    for text in expected:
        assert text in result.stdout, result.stdout
    for text in forbidden:
        assert text not in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr


@pytest.mark.parametrize("shape", [
    "scripts-is-a-link-to-a-dir-WITHOUT-the-register",
    "the-repo-root-itself-is-a-link",
    "scripts-is-a-link-to-a-dir-WITH-the-register",
])
def test_the_DEFAULT_and_the_NAMED_register_path_share_ONE_symlink_boundary(
        tmp_path, shape):
    """THE PARITY ITSELF, asserted as one path judged two ways rather than as
    two expectations written down separately.

    The documented claim for the default register is that it has "THE SAME
    BOUNDARY as `--code-surface-register`, whose named path is handed to
    `load_register` unconditionally". For a register below a symlinked ancestor
    that was false before the climb: named exited 2 "reached through a symlink",
    the default exited 1 and scanned on. Here the one path is run BOTH ways and
    the two runs must agree — same code, same refusal."""
    root, default = _ancestor_linked_register_tree(tmp_path, shape)
    by_default = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    by_name = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root),
         "--code-surface-register", str(default)],
        capture_output=True, text=True)
    assert by_default.returncode == 2, by_default.stdout + by_default.stderr
    assert by_name.returncode == by_default.returncode, by_name.stdout
    for text in ("CANNOT RUN", "reached through a symlink"):
        assert text in by_default.stdout, by_default.stdout
        assert text in by_name.stdout, by_name.stdout
    assert "Traceback" not in by_default.stderr, by_default.stderr
    assert "Traceback" not in by_name.stderr, by_name.stderr


def test_NO_REGISTER_is_the_absence_SPELLED_and_is_not_a_None(tmp_path):
    """The sentinel's own properties, pinned where they are relied on: it is
    NOT `None` (the derivation tests `is None`), it is EMPTY, and it is
    IMMUTABLE — one shared value that no caller can append an entry to."""
    assert sg.NO_REGISTER is not None
    assert len(sg.NO_REGISTER) == 0
    assert not isinstance(sg.NO_REGISTER, list)
    with pytest.raises(AttributeError):
        sg.NO_REGISTER.append({"change": "c"})          # type: ignore[attr-defined]


def test_the_derivation_reads_NO_REGISTER_and_None_as_TWO_DIFFERENT_FACTS(
        tmp_path):
    """THE SEPARATION ITSELF, at the module rather than at the CLI: ONE front
    matter, two register values, two different answers. `NO_REGISTER` yields a
    carrier naming NO entry; `None` still means "load the house register on
    demand" and yields the entry — which is what the CLI used to pass for a
    tree that is not this one."""
    root, entry = _house_entry_tree(tmp_path)
    front = sg.read_front_matter(
        root / "openspec" / "changes" / entry["change"] / "proposal.md")

    entry_less = sg.code_surface_repositories(
        front, change=entry["change"], register=sg.NO_REGISTER)
    assert isinstance(entry_less, sg.NoDeclaredRepositories)
    assert entry_less.register_entry is None

    house = sg.code_surface_repositories(
        front, change=entry["change"], register=None)
    assert isinstance(house, sg.NoDeclaredRepositories)
    assert house.register_entry is not None
    assert house.register_entry["change"] == entry["change"]


def test_an_operator_named_register_that_cannot_be_used_REFUSES_not_falls_back(
        tmp_path):
    """The sibling's semantics for a NAMED register: exit 2 and a named
    finding, never a silent fallback to some other tree's exceptions."""
    root, _ = _registered_scope_tree(tmp_path)
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root),
         "--code-surface-register", str(root / "no-such-register.yaml")],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "CANNOT RUN" in result.stdout
    assert "Traceback" not in result.stderr, result.stderr


# --- the live corpus ----------------------------------------------------------


def test_scan_with_NO_register_loads_the_HOUSE_register():
    """`scan(repo_root)` with no register is the branch every caller but the
    CLI takes, and it was untested. It loads the register beside the module —
    proved by equality with the same scan given that register explicitly, over
    the real tree, where the registered count is non-zero and so the two could
    differ."""
    implicit = cs.scan(ROOT)
    explicit = cs.scan(ROOT, cs.load_register(REGISTER))
    assert implicit == explicit
    assert implicit.registered, "the house register names nothing; " \
        "this test would pass vacuously"


def test_corpus_code_surface_validates():
    """THE GATE. Every active declaration in this repository is admitted — by
    the grammar, or by a live entry in the closed register. A new divergence
    reds the required `pytest-suite` with no workflow edit."""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_corpus_scope_globs_gate_still_passes_after_the_narrowing():
    """§ 3.5's after-run, pinned rather than recorded once: the narrowing is
    unobservable on the live corpus (no active proposal declares
    `scope_globs:`), which is what makes it landable without a sweep."""
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(ROOT)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_register_entry_names_a_live_active_change():
    """The register may not name a change that is absent or archived: an entry
    over an archived packet would be an exception for a document nobody may
    edit, and an entry over an absent one is stale by construction."""
    entries = cs.load_register(REGISTER)
    assert entries, "the register is empty; delete it rather than keeping a stub"
    for entry in entries:
        folder = ROOT / "openspec" / "changes" / entry["change"]
        assert (folder / "proposal.md").is_file(), entry["change"]


def test_every_register_entry_declares_a_known_class_and_a_citation():
    """Belt and braces over the LIVE register. `load_register` enforces the
    closed class set and the citation's shape for every tree, so this reads the
    module's own set rather than a second copy of it — a test that kept its own
    list would drift from the loader and stop being evidence about it."""
    for entry in cs.load_register(REGISTER):
        assert entry["class"] in cs.REGISTER_CLASSES, entry
        cited = entry.get("cited_to", [])
        assert isinstance(cited, list) and cited, entry["change"]
        assert all(isinstance(c, str) and c.strip() for c in cited), \
            entry["change"]


def test_every_register_entry_carries_the_live_declaration_byte_for_byte():
    """The entry records the declaration AS IT STANDS, and the match is on that
    text — so this is the same equality the gate makes, taken directly."""
    for entry in cs.load_register(REGISTER):
        proposal = (ROOT / "openspec" / "changes" / entry["change"]
                    / "proposal.md")
        present, text = cs.declaration(proposal)
        assert present, entry["change"]
        assert text == entry["declaration"], entry["change"]


def test_every_register_entry_names_a_declaration_the_grammar_really_refuses():
    """No entry may tolerate a head the grammar can read: an exception for a
    conforming declaration would be an exception for nothing, and would hide the
    day that declaration stopped conforming."""
    for entry in cs.load_register(REGISTER):
        with pytest.raises(cs.CodeSurfaceError):
            cs.parse_head(entry["declaration"])


def test_the_closed_baseline_is_exactly_the_registers_own_population():
    """The baseline is a CEILING and may be wider, but at the gate's landing it
    is the register's own population — so a divergence between the two here is a
    drift nobody declared."""
    entries = cs.load_register(REGISTER)
    assert {(e["change"], cs.declaration_digest(e["declaration"]))
            for e in entries} == set(cs.CLOSED_REGISTER)


def test_the_register_stays_under_the_strict_loaders_byte_ceiling():
    """The register carries every tolerated declaration VERBATIM, and one of
    them is 11,678 bytes, so the file is large by construction and is read
    through the same ceiling every front-matter block is. Measured rather than
    assumed, with the headroom named: a future entry that would cross the
    ceiling is a fact the gate should surface here rather than at a run."""
    size = len(REGISTER.read_text(encoding="utf-8").encode("utf-8"))
    ceiling = importlib.import_module("frontmatter_strict").CEILING_BYTES
    assert size < ceiling, (size, ceiling)
