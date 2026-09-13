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
    message = str(pytest.raises(
        cs.CodeSurfaceError, cs.parse_head, long_gloss).value)
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


# --- the YAML folding indicator, refused BY NAME ------------------------------


@pytest.mark.parametrize("indicator", [">-", "|", ">", "|-", ">+", "|2-"])
def test_a_block_scalar_declaration_is_refused_by_name(indicator):
    with pytest.raises(cs.CodeSurfaceError) as caught:
        cs.parse_head(f"{indicator}\n  openxFactory — the surface")
    message = str(caught.value)
    assert "YAML folding indicator" in message
    assert indicator in message


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


def test_the_derived_set_is_the_heads_identifiers_and_none_of_the_glosss():
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
    """THE CLI SURFACE. The refusal must reach the run, not only the module —
    and it reaches it as the scope gate's own exit 1 with the change id
    prefixed, which `validate_corpus` already does for every problem it
    prints."""
    root, declaration = _registered_scope_tree(tmp_path)
    result = subprocess.run(
        [sys.executable, str(SCOPE_VALIDATOR), str(root)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "c: " in result.stdout
    assert "NO REPOSITORY SET CAN BE DERIVED" in result.stdout


# --- the live corpus ----------------------------------------------------------


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
