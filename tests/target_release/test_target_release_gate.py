"""`gate-realization-axis-vocabulary` § 3: the `target_release:` vocabulary gate.

`openspec validate` (the external CLI) cannot be extended, so the house wiring
is `scripts/validate-target-release.py` plus
`test_corpus_target_release_validates` below, which runs it over every active
change on every pull request — the same enforcement route the other
`scripts/validate-*.py` contract validators use.

EVERY TREE HERE IS BUILT IN A TMPDIR AND JUDGED AGAINST A REGISTER BUILT BESIDE
IT, so a test can never be made green by editing the repository's own register,
and the two corpus tests at the end are the only ones that read the real one.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "target_release.py"
VALIDATOR = ROOT / "scripts" / "validate-target-release.py"
REGISTER = ROOT / "scripts" / "target-release-register.yaml"


def _load():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("target_release", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


tr = _load()


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


def _run(root: Path, register: Path | None = None):
    argv = [sys.executable, str(VALIDATOR), str(root)]
    if register is not None:
        argv += ["--register", str(register)]
    return subprocess.run(argv, capture_output=True, text=True)


def _entry(change: str, token: str, cited_to: str = "    cited_to:\n"
                                                 "      - a document § a section\n",
           klass: str = "deferred-allocation") -> str:
    return (f"register:\n"
            f"  - change: {change}\n"
            f"    token: \"{token}\"\n"
            f"    class: {klass}\n"
            f"    why: a reason\n"
            f"{cited_to}"
            f"    retires_when: an event\n")


# --- the value token ----------------------------------------------------------


def test_a_bare_token_is_the_value():
    assert tr.value_token("implemented") == "implemented"


def test_a_gloss_after_the_token_is_not_judged():
    assert tr.value_token(
        "implemented (the openxFactory main line). No bundle is cut."
    ) == "implemented"


def test_a_trailing_stop_is_stripped():
    assert tr.value_token("none.") == "none"


def test_a_multi_line_declaration_is_read_from_its_first_word():
    assert tr.value_token("contract-v1.45 — the bundle\nand a second line") \
        == "contract-v1.45"


def test_an_empty_declaration_has_no_token():
    assert tr.value_token("") is None
    assert tr.value_token("   ") is None
    assert tr.value_token(None) is None


# --- reading the declaration --------------------------------------------------


def test_a_declared_field_is_present(tmp_path):
    path = _proposal(tmp_path, "c", "code_surface: none\ntarget_release: implemented")
    assert tr.declaration(path) == (True, "implemented")


def test_an_undeclared_field_is_absent(tmp_path):
    path = _proposal(tmp_path, "c", "code_surface: none")
    assert tr.declaration(path) == (False, None)


def test_a_document_with_no_fence_declares_nothing(tmp_path):
    folder = tmp_path / "openspec" / "changes" / "c"
    folder.mkdir(parents=True)
    path = folder / "proposal.md"
    path.write_text("# Proposal\n\ntarget_release: implemented\n", encoding="utf-8")
    assert tr.declaration(path) == (False, None)


# Copilot's round 2 on #963 (thread `PRRT_kwDOTAvnrs6heTP2`): a repeated PROSE
# header is JOINED by the shared loader, not refused as a duplicate key, so a
# block with two conflicting declarations tokenized as the first one.


def test_a_repeated_declaration_is_refused_not_half_read(tmp_path):
    path = _proposal(
        tmp_path, "c",
        "code_surface: R\ntarget_release: implemented (the main line)\n"
        "target_release: none")
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.declaration(path)
    assert "more than once" in str(caught.value)


def test_a_repeated_declaration_is_a_finding_not_a_crash(tmp_path):
    _proposal(tmp_path, "twice",
              "code_surface: R\ntarget_release: implemented\n"
              "target_release: none")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "twice/proposal.md" in result.stdout
    assert "more than once" in result.stdout
    assert "Traceback" not in result.stderr


def test_an_indented_gloss_line_is_a_gloss_and_not_a_repeat(tmp_path):
    """An INDENTED line is a continuation of the gloss, never a declaration —
    the loader's own `_TOP_LEVEL` anchors a header at column 0, and the
    requirement says judge the token and never the gloss."""
    path = _proposal(
        tmp_path, "c",
        "code_surface: R\ntarget_release: implemented\n"
        "  target_release: the main line, spelled out")
    assert tr.declaration(path) == (True, "implemented")


def test_one_declaration_with_a_multi_line_gloss_is_still_fine(tmp_path):
    path = _proposal(
        tmp_path, "c",
        "code_surface: R\ntarget_release: implemented (the main line).\n"
        "  No contract bundle is cut and no digest set moves.")
    assert tr.declaration(path) == (True, "implemented")


def test_a_strict_loader_refusal_is_raised_not_swallowed(tmp_path):
    path = _proposal(
        tmp_path, "c",
        "code_surface: R\ntarget_release: implemented\n"
        "scope_globs:\n  R:\n    - 'a/**'\nscope_globs:\n  R:\n    - 'b/**'")
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.declaration(path)
    assert "duplicate key" in str(caught.value)


# --- resolving a named release ------------------------------------------------


def test_a_release_resolves_against_the_registry(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "contract-v9.9.digests.yaml").write_text("{}\n", encoding="utf-8")
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (True, True)


def test_a_release_shaped_name_with_no_inventory_does_not_resolve(tmp_path):
    (tmp_path / "contracts" / "releases").mkdir(parents=True)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (False, True)


# Copilot on #963, post-freeze (thread `PRRT_kwDOTAvnrs6hgEM5`): `Path.is_file()`
# follows symlinks, so a committed symlinked digest inventory — including one
# pointing outside the tree — was treated as an estate-defined release. The
# guard is `scripts/hermes_runtime_validation/release.py`'s own
# (`RepoSource.exists`), restated here rather than imported.


def test_a_symlinked_inventory_does_not_resolve(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    real = tmp_path / "elsewhere.digests.yaml"
    real.write_text("{}\n", encoding="utf-8")
    (releases / "contract-v9.9.digests.yaml").symlink_to(real)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (False, True)


def test_a_symlinked_inventory_pointing_outside_the_tree_does_not_resolve(
        tmp_path, tmp_path_factory):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    outside = tmp_path_factory.mktemp("outside") / "elsewhere.digests.yaml"
    outside.write_text("{}\n", encoding="utf-8")
    (releases / "contract-v9.9.digests.yaml").symlink_to(outside)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (False, True)


def test_a_regular_inventory_still_resolves_beside_a_symlinked_one(tmp_path):
    """The refusal is per-candidate, not a registry-wide fallback: a symlink
    for one token does not make a REGULAR inventory for another refuse."""
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "contract-v9.9.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    real = tmp_path / "elsewhere.digests.yaml"
    real.write_text("{}\n", encoding="utf-8")
    (releases / "contract-v8.8.digests.yaml").symlink_to(real)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (True, True)
    assert tr.resolves_as_release("contract-v8.8", tmp_path) == (False, True)


# Copilot on #963, round 7, post-merge (thread `PRRT_kwDOTAvnrs6hgYZd`):
# `Path.is_dir()` ALSO follows symlinks, so a committed `contracts/releases`
# DIRECTORY symlink pointing outside the tree let an external inventory pass
# — the directory resolved as present, the file behind it was reached
# THROUGH the symlink and so was never itself a symlink, and the
# per-candidate guard above never saw anything to refuse. The directory is
# now checked for symlink-ness too (`_registry_present`), and a symlinked
# directory is treated the SAME AS NO REGISTRY AT ALL: `registry_present`
# reports False, so the note a bare tree gets is the note a symlinked tree
# gets, and an external inventory sitting behind the symlink can no longer
# make one token resolve differently from another.


def test_a_symlinked_registry_directory_is_treated_as_absent(
        tmp_path, tmp_path_factory):
    outside = tmp_path_factory.mktemp("outside-registry-dir")
    (outside / "contract-v9.9.digests.yaml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "contracts").mkdir()
    (tmp_path / "contracts" / "releases").symlink_to(outside)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (True, False)


def test_a_symlinked_registry_directory_contents_grant_no_extra_trust(
        tmp_path, tmp_path_factory):
    """Before the fix this returned `(True, True)`: the symlinked directory
    resolved as PRESENT and the external file — a REGULAR file, reached only
    through the symlinked parent — passed the per-candidate symlink check. An
    EMPTY symlinked directory now resolves identically to one holding a
    matching inventory, proving the external file's presence changed
    nothing — the directory's own symlink-ness is what decides."""
    with_file = tmp_path_factory.mktemp("outside-registry-with-file")
    (with_file / "contract-v9.9.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    empty = tmp_path_factory.mktemp("outside-registry-empty")

    with_file_root = tmp_path / "with-file"
    (with_file_root / "contracts").mkdir(parents=True)
    (with_file_root / "contracts" / "releases").symlink_to(with_file)

    empty_root = tmp_path / "empty"
    (empty_root / "contracts").mkdir(parents=True)
    (empty_root / "contracts" / "releases").symlink_to(empty)

    assert tr.resolves_as_release("contract-v9.9", with_file_root) \
        == tr.resolves_as_release("contract-v9.9", empty_root) \
        == (True, False)


# Copilot on #963, round 9 (thread `PRRT_kwDOTAvnrs6hhqDO`): checking only the
# LEAF directory's symlink-ness closes the escape at that one component and
# leaves every ANCESTOR open — `contracts/` itself being the symlink reaches
# the identical escape through a `contracts/releases` that is a perfectly
# ordinary, unsymlinked path, because ordinariness is a property of the ONE
# component checked and says nothing about what carried a reader there.
# `_registry_present` now compares the registry's fully RESOLVED real path
# against `repo_root`'s own resolved real path with the literal
# `contracts/releases` suffix appended, which catches a symlink at ANY
# component between the two, not only at the registry directory's own name.


def test_a_symlinked_ancestor_directory_is_also_treated_as_absent(
        tmp_path, tmp_path_factory):
    """`contracts/` itself is the symlink this time, not `releases/`. Before
    this fix `contracts/releases` was a perfectly ordinary path reached
    through it — a REAL directory, holding a REAL file — and resolved exactly
    like an estate-defined registry."""
    outside = tmp_path_factory.mktemp("outside-contracts-dir")
    (outside / "releases").mkdir()
    (outside / "releases" / "contract-v9.9.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    (tmp_path / "contracts").symlink_to(outside)
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (True, False)


def test_repo_root_itself_being_reached_via_a_symlink_is_not_the_escape(
        tmp_path, tmp_path_factory):
    """`repo_root` itself is resolved on BOTH sides of the comparison, so its
    own symlink-ness cancels out rather than being mistaken for an escape:
    this is not the vulnerability class the finding named — a caller handed a
    symlinked `repo_root` is trusting that path already — and a registry that
    is otherwise perfectly ordinary beneath it still resolves."""
    outside = tmp_path_factory.mktemp("outside-root")
    (outside / "contracts" / "releases").mkdir(parents=True)
    (outside / "contracts" / "releases" / "contract-v9.9.digests.yaml"
     ).write_text("{}\n", encoding="utf-8")
    root = tmp_path / "root"
    root.symlink_to(outside)
    assert tr.resolves_as_release("contract-v9.9", root) == (True, True)


# Copilot's round 3 on #963 (thread `PRRT_kwDOTAvnrs6heq2s`): the shape was
# two-component only, while the estate's own inventory schema admits two OR
# three — latent while the shape was consulted only where no registry exists,
# and a live refusal once it became the first test in every branch.


def test_the_release_id_shape_is_the_estates_own():
    """`RELEASE_ID_RE` is the inventory schema's `bundle_tag` pattern, restated
    (this module must judge a tree with no `contracts/`). A drift here is this
    test, not a release refused at a gate."""
    schema = yaml.safe_load(
        (ROOT / tr.RELEASE_ID_SCHEMA).read_text(encoding="utf-8"))
    assert tr.RELEASE_ID_RE.pattern == schema["$defs"]["bundle_tag"]["pattern"]


def test_a_three_component_release_resolves_against_the_registry(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "contract-v1.2.3.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    assert tr.resolves_as_release("contract-v1.2.3", tmp_path) == (True, True)


def test_a_three_component_release_shape_is_accepted_with_no_registry(tmp_path):
    assert tr.resolves_as_release("contract-v1.2.3", tmp_path) == (True, False)


def test_a_four_component_release_name_is_still_refused(tmp_path):
    (tmp_path / "contracts" / "releases").mkdir(parents=True)
    assert tr.resolves_as_release("contract-v1.2.3.4", tmp_path) == (False, True)


def test_an_active_three_component_release_passes(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "contract-v1.2.3.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    _proposal(tmp_path, "cut", "code_surface: R\ntarget_release: contract-v1.2.3")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 a named release" in result.stdout


def test_with_no_registry_the_shape_is_accepted(tmp_path):
    assert tr.resolves_as_release("contract-v9.9", tmp_path) == (True, False)
    assert tr.resolves_as_release("none", tmp_path) == (False, False)


def test_a_tree_with_no_registry_SAYS_it_is_judging_on_shape_alone(tmp_path):
    """The shape-only fallback is a WEAKER judgment and the run must not hide
    it: `registry_present` is False and the report says so in words, so a green
    run in a tree with no `contracts/releases/` cannot be read as evidence that
    the estate defines the release."""
    _proposal(tmp_path, "cut", "code_surface: R\ntarget_release: contract-v9.9")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "accepted on its SHAPE alone" in result.stdout


def test_a_tree_with_a_registry_does_not_print_the_shape_note(tmp_path):
    (tmp_path / "contracts" / "releases").mkdir(parents=True)
    _proposal(tmp_path, "doc", "code_surface: none")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SHAPE alone" not in result.stdout


def test_the_gate_prints_the_shape_note_when_the_registry_is_a_symlink(
        tmp_path, tmp_path_factory):
    """End to end: the gate treats a symlinked `contracts/releases` exactly
    as it treats a tree with no registry at all — same note, same passing
    result — rather than trusting whatever the symlink resolves to."""
    outside = tmp_path_factory.mktemp("outside-registry-e2e")
    (outside / "contract-v9.9.digests.yaml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "contracts").mkdir()
    (tmp_path / "contracts" / "releases").symlink_to(outside)
    _proposal(tmp_path, "cut", "code_surface: R\ntarget_release: contract-v9.9")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "accepted on its SHAPE alone" in result.stdout


# --- the token is shape-checked BEFORE it can become a path -------------------
# Copilot's round on #963 (thread `PRRT_kwDOTAvnrs6heJ1R`): with a registry
# present the resolver used to interpolate the token straight into the lookup,
# so a traversing or non-release token could resolve against a file outside
# `contracts/releases/`. These pin the guard in BOTH branches.


def test_a_traversing_token_never_escapes_the_release_registry(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    # planted OUTSIDE the registry, exactly where `../` would land
    (tmp_path / "contracts" / "elsewhere.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    assert tr.resolves_as_release("../elsewhere", tmp_path) == (False, True)


def test_an_absolute_token_never_becomes_a_path(tmp_path):
    (tmp_path / "contracts" / "releases").mkdir(parents=True)
    assert tr.resolves_as_release("/etc/passwd", tmp_path) == (False, True)


def test_a_planted_inventory_under_a_non_release_name_does_not_resolve(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "none.digests.yaml").write_text("{}\n", encoding="utf-8")
    assert tr.resolves_as_release("none", tmp_path) == (False, True)


def test_a_traversing_token_is_refused_with_no_registry_too(tmp_path):
    assert tr.resolves_as_release("../elsewhere", tmp_path) == (False, False)


def test_an_active_traversing_release_token_is_refused_end_to_end(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (tmp_path / "contracts" / "elsewhere.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    _proposal(tmp_path, "escape",
              "code_surface: R\ntarget_release: ../elsewhere")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "escape/proposal.md" in result.stdout
    assert "`../elsewhere`" in result.stdout
    assert "Traceback" not in result.stderr


def test_an_archived_traversing_token_is_counted_and_never_judged(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (tmp_path / "contracts" / "elsewhere.digests.yaml").write_text(
        "{}\n", encoding="utf-8")
    _proposal(tmp_path, "2026-01-01-old",
              "code_surface: R\ntarget_release: ../elsewhere", archived=True)
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 of them outside the vocabulary" in result.stdout


# --- the register -------------------------------------------------------------


def test_a_missing_register_refuses(tmp_path):
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(tmp_path / "absent.yaml")
    assert "does not exist" in str(caught.value)


def test_a_register_without_the_list_refuses(tmp_path):
    path = _register(tmp_path, "schema_version: 1\n")
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "`register:` list" in str(caught.value)


def test_an_entry_missing_a_required_key_refuses(tmp_path):
    path = _register(
        tmp_path,
        "register:\n  - change: c\n    token: \"x\"\n"
        "    class: deferred-allocation\n    why: w\n"
        "    cited_to:\n      - a document\n")
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "retires_when" in str(caught.value)


def test_a_repeated_entry_refuses(tmp_path):
    path = _register(tmp_path, _entry("c", "x") + _entry("c", "x").split("\n", 1)[1])
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "repeats" in str(caught.value)


# --- the entry's CITATION is enforced at the load -----------------------------
# Copilot's round on #963 (thread `PRRT_kwDOTAvnrs6heJ2G`): the requirement has
# every standing entry carry a citation, but the loader did not ask for one — so
# only a test over THIS repository's register did, and a consuming tree (or a
# later entry) could grandfather a declaration on nobody's word.


def test_an_entry_without_a_citation_refuses(tmp_path):
    path = _register(tmp_path, _entry("c", "x", cited_to=""))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "cited_to" in str(caught.value)


def test_an_entry_with_an_empty_citation_list_refuses(tmp_path):
    path = _register(tmp_path, _entry("c", "x", cited_to="    cited_to: []\n"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "cited_to" in str(caught.value)


def test_an_entry_whose_citation_is_a_bare_string_refuses(tmp_path):
    path = _register(
        tmp_path, _entry("c", "x", cited_to="    cited_to: a document\n"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "cited_to" in str(caught.value)


def test_an_entry_with_a_non_string_citation_item_refuses(tmp_path):
    path = _register(
        tmp_path, _entry("c", "x", cited_to="    cited_to:\n      - 17\n"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "cited_to" in str(caught.value)
    assert "(1)" in str(caught.value)


def test_an_entry_with_a_blank_citation_item_refuses(tmp_path):
    path = _register(
        tmp_path,
        _entry("c", "x", cited_to="    cited_to:\n      - a doc\n      - \"  \"\n"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "cited_to" in str(caught.value)
    assert "(2)" in str(caught.value)


# --- the same class, swept: a name that reaches a path, and a closed set ------


def test_an_entry_whose_change_is_a_path_refuses(tmp_path):
    path = _register(tmp_path, _entry("../../elsewhere", "x"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "change-directory name" in str(caught.value)


def test_an_entry_whose_change_carries_a_separator_refuses(tmp_path):
    path = _register(tmp_path, _entry("a/b", "x"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "change-directory name" in str(caught.value)


def test_an_entry_with_a_class_outside_the_closed_set_refuses(tmp_path):
    path = _register(tmp_path, _entry("c", "x", klass="invented-here"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path)
    assert "invented-here" in str(caught.value)
    assert "CLOSED" in str(caught.value)


# --- the register is REMOVABLE, NEVER ADDABLE ---------------------------------
# Copilot's round 2 on #963 (threads `PRRT_kwDOTAvnrs6heTQF` and
# `PRRT_kwDOTAvnrs6heTPk`): the requirement SHALLs a CLOSED register, but every
# new `(change, token)` pair was accepted, so a later pull request could append
# an exception and keep the gate green without touching the specification.


def test_an_entry_outside_the_closed_baseline_refuses(tmp_path):
    path = _register(tmp_path, _entry("newcomer", "invented"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path, closed=(("legacy", "next"),))
    assert "CLOSED baseline" in str(caught.value)
    assert "newcomer" in str(caught.value)


def test_an_entry_whose_token_moved_off_the_baseline_refuses(tmp_path):
    path = _register(tmp_path, _entry("legacy", "later"))
    with pytest.raises(tr.TargetReleaseError) as caught:
        tr.load_register(path, closed=(("legacy", "next"),))
    assert "CLOSED baseline" in str(caught.value)


def test_a_baseline_wider_than_the_register_is_lawful(tmp_path):
    """Removal is the ONE lawful direction, so the baseline outlives the entry
    and a shrunken register must load clean."""
    path = _register(tmp_path, _entry("legacy", "next"))
    entries = tr.load_register(
        path, closed=(("legacy", "next"), ("retired", "gone")))
    assert [e["change"] for e in entries] == ["legacy"]


def test_a_register_named_on_the_command_line_carries_no_house_baseline(tmp_path):
    """`--register` serves the tests and a consuming tree; binding those to
    THIS repository's baseline would refuse every register but this one."""
    path = _register(tmp_path, _entry("some-other-tree-change", "whatever"))
    assert [e["change"] for e in tr.load_register(path)] \
        == ["some-other-tree-change"]


def test_the_house_register_is_within_its_own_closed_baseline():
    """THE RATCHET, over the real file: `load_register()` with no argument
    binds `CLOSED_REGISTER`, so this refuses the moment an entry is appended
    without the module edit that declares the act."""
    entries = tr.load_register()
    pairs = {(e["change"], e["token"]) for e in entries}
    assert pairs <= set(tr.CLOSED_REGISTER)


# --- the gate, end to end -----------------------------------------------------


def test_an_active_off_vocabulary_declaration_is_refused(tmp_path):
    _proposal(tmp_path, "bad-change", "code_surface: R\ntarget_release: none")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "bad-change/proposal.md" in result.stdout
    assert "`none`" in result.stdout


def test_an_active_implemented_declaration_passes(tmp_path):
    _proposal(tmp_path, "good-change", "code_surface: R\ntarget_release: implemented")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


def test_an_archived_off_vocabulary_declaration_is_not_a_finding(tmp_path):
    _proposal(tmp_path, "2026-01-01-old", "code_surface: R\ntarget_release: none",
              archived=True)
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 of them outside the vocabulary" in result.stdout
    assert "2026-01-01-old" not in result.stdout


def test_a_named_release_passes(tmp_path):
    releases = tmp_path / "contracts" / "releases"
    releases.mkdir(parents=True)
    (releases / "contract-v9.9.digests.yaml").write_text("{}\n", encoding="utf-8")
    _proposal(tmp_path, "cut", "code_surface: R\ntarget_release: contract-v9.9")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 a named release" in result.stdout


def test_a_release_name_that_resolves_to_nothing_is_refused(tmp_path):
    (tmp_path / "contracts" / "releases").mkdir(parents=True)
    _proposal(tmp_path, "cut", "code_surface: R\ntarget_release: contract-v9.9")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "contract-v9.9.digests.yaml" in result.stdout


def test_declaring_nothing_takes_the_promoted_default(tmp_path):
    _proposal(tmp_path, "doc-only", "code_surface: none")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 declaring" in result.stdout


def test_an_empty_declaration_is_refused(tmp_path):
    _proposal(tmp_path, "empty", "code_surface: R\ntarget_release:")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "no value" in result.stdout


def test_an_unreadable_proposal_is_reported_not_crashed(tmp_path):
    _proposal(
        tmp_path, "refused",
        "code_surface: R\ntarget_release: implemented\n"
        "scope_globs:\n  R:\n    - 'a/**'\nscope_globs:\n  R:\n    - 'b/**'")
    result = _run(tmp_path, _register(tmp_path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "refused/proposal.md" in result.stdout
    assert "cannot be read" in result.stdout
    assert "Traceback" not in result.stderr


def test_a_registered_declaration_is_reported_not_refused(tmp_path):
    _proposal(tmp_path, "legacy", "code_surface: R\ntarget_release: next bundle")
    result = _run(tmp_path, _register(tmp_path, _entry("legacy", "next")))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 named by the register" in result.stdout


def test_an_entry_that_matches_nothing_refuses(tmp_path):
    _proposal(tmp_path, "legacy", "code_surface: R\ntarget_release: implemented")
    result = _run(tmp_path, _register(tmp_path, _entry("legacy", "next")))
    assert result.returncode == 2, result.stdout + result.stderr
    assert "stale" in result.stdout
    assert "legacy" in result.stdout


def test_an_entry_stops_matching_when_the_token_moves(tmp_path):
    _proposal(tmp_path, "legacy", "code_surface: R\ntarget_release: later bundle")
    result = _run(tmp_path, _register(tmp_path, _entry("legacy", "next")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "`later`" in result.stdout
    assert "stale" in result.stdout


def test_a_finding_and_a_stale_entry_are_both_reported(tmp_path):
    _proposal(tmp_path, "bad", "code_surface: R\ntarget_release: none")
    _proposal(tmp_path, "fine", "code_surface: R\ntarget_release: implemented")
    result = _run(tmp_path, _register(tmp_path, _entry("fine", "next")))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "stale" in result.stdout
    assert "bad/proposal.md" in result.stdout


def test_a_missing_register_refuses_the_run(tmp_path):
    _proposal(tmp_path, "c", "code_surface: R\ntarget_release: implemented")
    result = _run(tmp_path, tmp_path / "absent.yaml")
    assert result.returncode == 2, result.stdout + result.stderr
    assert "CANNOT RUN" in result.stdout


# --- the live corpus ----------------------------------------------------------


def test_corpus_target_release_validates():
    """THE GATE. Every active declaration in this repository is admitted."""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_register_entry_names_a_live_active_change():
    """The register may not name a change that is absent or archived: an entry
    over an archived packet would be an exception for a document nobody may
    edit, and an entry over an absent one is stale by construction."""
    entries = tr.load_register(REGISTER)
    assert entries, "the register is empty; delete it rather than keeping a stub"
    for entry in entries:
        folder = ROOT / "openspec" / "changes" / entry["change"]
        assert (folder / "proposal.md").is_file(), entry["change"]


def test_every_register_entry_declares_a_known_class_and_a_citation():
    """Belt and braces over the LIVE register. `load_register` now enforces the
    closed class set and the citation's shape for every tree, so this reads the
    module's own set rather than a second copy of it — a test that kept its own
    list would drift from the loader and stop being evidence about it."""
    for entry in tr.load_register(REGISTER):
        assert entry["class"] in tr.REGISTER_CLASSES, entry
        cited = entry.get("cited_to", [])
        assert isinstance(cited, list) and cited, entry["change"]
        assert all(isinstance(c, str) and c.strip() for c in cited), entry["change"]
