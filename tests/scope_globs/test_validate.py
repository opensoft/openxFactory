"""Feature `scope-globs-validate` (add-structured-scope-substrate tasks 3.1-3.4):
dialect conformance + cross-consistency, wired into a house validator that the
pytest gate runs over the live corpus.

`openspec validate` (the external CLI) cannot be extended, so the house wiring is
`scripts/validate-scope-globs.py` plus `test_corpus_scope_globs_all_validate`
below, which runs it over every active change on every PR — the same enforcement
route the other `scripts/validate-*.py` contract validators use.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "scope_globs.py"
VALIDATOR = ROOT / "scripts" / "validate-scope-globs.py"


def _load():
    spec = importlib.util.spec_from_file_location("scope_globs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sg = _load()


# --- dialect conformance -----------------------------------------------------


def test_conformant_scope_validates():
    sg.validate_scope_globs(
        {"openxFactory": ["scripts/**", "openspec/specs/**", "docs/a?.md"]},
        code_surface_repos={"openxFactory"},
    )


@pytest.mark.parametrize("bad", ["**", "*", "**/*", "/**", "./**"])
def test_universal_patterns_are_rejected(bad):
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["scripts/**", bad]}, code_surface_repos={"R"})
    assert bad in str(exc.value)


def test_leading_slash_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["/scripts/**"]}, code_surface_repos={"R"})
    assert "/scripts/**" in str(exc.value)


def test_negation_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs({"R": ["!scripts/**"]}, code_surface_repos={"R"})
    assert "!scripts/**" in str(exc.value)


def test_complement_denylist_key_is_rejected():
    for key in ("path_denylist", "except_paths", "codeowners_complement"):
        with pytest.raises(sg.ScopeGlobsError) as exc:
            sg.validate_scope_globs({key: ["scripts/**"]}, code_surface_repos={key})
        assert key in str(exc.value)


# --- cross-consistency with code_surface -------------------------------------


def test_scope_repo_absent_from_code_surface_is_rejected():
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.validate_scope_globs(
            {"codexFactory": ["scripts/**"]}, code_surface_repos={"openxFactory"}
        )
    assert "codexFactory" in str(exc.value)


def test_code_surface_repo_without_scope_is_fine():
    # code_surface may name a repo scope_globs omits; that repo is simply not
    # provenance-eligible. Not an error.
    sg.validate_scope_globs(
        {"openxFactory": ["scripts/**"]},
        code_surface_repos={"openxFactory", "codexFactory"},
    )


# --- floor-agnostic ----------------------------------------------------------


def test_validator_is_floor_agnostic_a_floor_named_glob_passes():
    # `.github/**` and `openspec/changes/**` are typical never-clearable floor
    # members; the neutral validator MUST still accept them (the floor override
    # is a check-time concern of the downstream verifier, never a validate error).
    sg.validate_scope_globs(
        {"R": [".github/**", "openspec/changes/**"]}, code_surface_repos={"R"}
    )


# --- house wiring: the validator runs green over the live corpus --------------


def test_corpus_scope_globs_all_validate():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_flags_a_malformed_change(tmp_path):
    change = tmp_path / "openspec" / "changes" / "bad-change"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        "---\ncode_surface: R\nscope_globs:\n  R:\n    - '**'\n---\n\n# bad\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "bad-change" in result.stdout
    assert "**" in result.stdout


# --- the corpus walk is PATH-BOUNDED (gate-code-surface-declarations) ---------
#
# `Path.is_dir()` and `Path.is_file()` FOLLOW SYMLINKS, so the plain walk these
# tests replaced read a symlinked `proposal.md` — or an ordinary one inside a
# symlinked CHANGE DIRECTORY — as an active proposal of the scanned tree. Once
# the cross-consistency check became a CODE-SURFACE CONSUMER that mattered in a
# new way: the escaped document supplied the `code_surface:` declaration the
# scope key is checked against AND matched the register entry the refusal names,
# so bytes outside the tree could grant an authorization the tree never declared.
# Discovery now runs through `code_surface._proposals`, whose every candidate
# path goes through the anchored `_unescaped` check, and an escaped path is
# DROPPED — never reported — because neither face of the escape is a judgment
# about the scanned tree, which is the only thing this gate may make.

CODE_SURFACE_MODULE = ROOT / "scripts" / "code_surface.py"
FRONTMATTER_MODULE = ROOT / "scripts" / "frontmatter_strict.py"

#: A head the ratified grammar CANNOT read, so a register entry is the only
#: thing that could tolerate it — which is what makes it the probe for whether
#: an escaped document reaches the register at all.
_UNREADABLE_HEAD = ("openxFactory, and it is THREE FILES at realization, one "
                    "of them in codexFactory")

#: A scope naming a repository the code surface does NOT — the ORDINARY
#: cross-consistency refusal, used as the probe for "was this document read?",
#: because a dropped document and a conforming one differ by EXIT CODE.
_ESCAPED_PROPOSAL = (
    "---\ncode_surface: openxFactory\n"
    "scope_globs:\n  codexFactory:\n    - 'scripts/**'\n---\n\n# Proposal\n")


def _register_naming(path: Path, change: str, declaration: str) -> Path:
    import yaml
    path.write_text(yaml.safe_dump({"register": [{
        "change": change, "declaration": declaration,
        "class": "list-runs-into-prose", "why": "a reason",
        "cited_to": ["a document § a section"], "retires_when": "an event",
    }]}, sort_keys=False, allow_unicode=True, width=10_000), encoding="utf-8")
    return path


def _scan(root: Path, register: Path | None = None):
    argv = [sys.executable, str(VALIDATOR), str(root)]
    if register is not None:
        argv += ["--code-surface-register", str(register)]
    return subprocess.run(argv, capture_output=True, text=True)


def test_a_SYMLINKED_proposal_is_NOT_read_by_the_corpus_walk(tmp_path):
    """The leaf is the link. Measured BEFORE the guard: this exact tree exited
    1 naming `x` and its cross-consistency fault — proof the bytes were read."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    root = tmp_path / "tree"
    change = root / "openspec" / "changes" / "x"
    change.mkdir(parents=True)
    (change / "proposal.md").symlink_to(outside / "proposal.md")
    result = _scan(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "x" not in result.stdout.split("passed")[0]
    assert "codexFactory" not in result.stdout


def test_a_proposal_in_a_SYMLINKED_CHANGE_DIRECTORY_is_NOT_read(tmp_path):
    """The leaf is a REGULAR FILE and the escape is an ancestor, which the
    leaf's own `is_symlink()` cannot see — the reason the check is anchored and
    resolves the whole path rather than testing one component."""
    outside = tmp_path / "outside" / "x"
    outside.mkdir(parents=True)
    (outside / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    assert not (outside / "proposal.md").is_symlink()   # the leaf is ordinary
    root = tmp_path / "tree"
    (root / "openspec" / "changes").mkdir(parents=True)
    (root / "openspec" / "changes" / "x").symlink_to(outside)
    result = _scan(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "codexFactory" not in result.stdout


def test_an_ESCAPED_proposal_supplies_NEITHER_a_declaration_NOR_a_register_match(
        tmp_path):
    """THE DEFECT IN ONE TEST. The escaped document carries a head the grammar
    cannot read, and the SCANNED TREE'S OWN REGISTER names it — so before the
    guard the refusal quoted outside bytes and named entry `c` as tolerating
    them. Both halves are now unreachable."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "proposal.md").write_text(
        f"---\ncode_surface: {_UNREADABLE_HEAD}\n"
        "scope_globs:\n  openxFactory:\n    - 'scripts/**'\n---\n\n# P\n",
        encoding="utf-8")
    root = tmp_path / "tree"
    change = root / "openspec" / "changes" / "c"
    change.mkdir(parents=True)
    (change / "proposal.md").symlink_to(outside / "proposal.md")
    register = _register_naming(tmp_path / "register.yaml", "c",
                                _UNREADABLE_HEAD)
    result = _scan(root, register)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO REPOSITORY SET CAN BE DERIVED" not in result.stdout
    assert "CLOSED code-surface register" not in result.stdout
    assert "entry `c`" not in result.stdout


def test_an_ORDINARY_proposal_is_STILL_read(tmp_path):
    """The guard drops escapes and nothing else: the same document, written in
    place rather than linked in, is read and judged."""
    change = tmp_path / "openspec" / "changes" / "x"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    result = _scan(tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "x: scope_globs names repository 'codexFactory'" in result.stdout


def test_a_tree_REACHED_THROUGH_A_SYMLINK_still_finds_its_own_proposals(
        tmp_path):
    """`repo_root` is resolved on BOTH sides, so a scratch tree that is itself
    reached through a link (a `/tmp` symlink, a linked checkout) is not
    mistaken for the escape — the failure mode that would make the guard
    unusable in exactly the trees it is tested in."""
    real = tmp_path / "real"
    change = real / "openspec" / "changes" / "x"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    linked = tmp_path / "linked"
    linked.symlink_to(real)
    result = _scan(linked)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "x: scope_globs names repository 'codexFactory'" in result.stdout


def test_the_two_gates_walk_THE_SAME_CORPUS(tmp_path):
    """THE INVARIANT THE FIX BUYS, asserted directly rather than inferred from
    two exit codes: the scope gate's discovery IS `code_surface._proposals`, so
    the two gates cannot come to judge two different corpora that agree until a
    symlink separates them."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    root = tmp_path / "tree"
    ordinary = root / "openspec" / "changes" / "ordinary"
    ordinary.mkdir(parents=True)
    (ordinary / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    escaped = root / "openspec" / "changes" / "escaped"
    escaped.mkdir(parents=True)
    (escaped / "proposal.md").symlink_to(outside / "proposal.md")
    (root / "openspec" / "changes" / "linked-dir").symlink_to(outside)

    sys.path.insert(0, str(ROOT / "scripts"))
    cs = _load_by_location("code_surface", CODE_SURFACE_MODULE)
    vsg = _load_by_location("validate_scope_globs_cli", VALIDATOR)
    mine = vsg._active_proposals(root)
    theirs = cs._proposals(root, archived=False)
    assert mine == theirs
    assert [p.parent.name for p in mine] == ["ordinary"]


def _load_by_location(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _sibling_less_gate(tmp_path: Path) -> Path:
    """`validate-scope-globs.py` beside ONLY the two modules codexFactory
    vendors — no `code_surface.py`."""
    gate = tmp_path / "gate"
    gate.mkdir()
    for source in (VALIDATOR, MODULE, FRONTMATTER_MODULE):
        (gate / source.name).write_bytes(source.read_bytes())
    assert not (gate / "code_surface.py").exists()
    return gate


def test_the_corpus_scan_REFUSES_when_the_GUARDING_SIBLING_IS_ABSENT(tmp_path):
    """A GUARD THAT SILENTLY DISAPPEARS IS A FAIL-CLOSED BECOMING A FAIL-OPEN.
    Without the sibling the walk cannot be path-bounded, so the scan refuses in
    this CLI's own "CANNOT RUN … exit 2" shape and names the file to copy —
    rather than falling back to the unguarded walk that was the defect."""
    gate = _sibling_less_gate(tmp_path)
    change = tmp_path / "tree" / "openspec" / "changes" / "x"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(_ESCAPED_PROPOSAL, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(gate / "validate-scope-globs.py"),
         str(tmp_path / "tree")], capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "CANNOT RUN" in result.stdout
    assert "code_surface.py" in result.stdout
    assert "does NOT fall back to an unguarded walk" in result.stdout
    assert "Traceback" not in result.stderr


def test_the_ARCHIVE_GATE_still_runs_with_NO_code_surface_sibling(tmp_path):
    """THE CLAIM THE REFUSAL ABOVE NARROWED, PINNED. The scope-retention freeze
    reads `scope_globs:` on both sides and nothing else, so it needs no
    `code_surface` — which is what the corrected docstring now claims, instead
    of the old blanket "this CLI must keep running without the sibling".

    IT DOES NEED `sequenced_after`, to locate the ratified-side proposal by
    change id at a ref — so that one is copied in and `code_surface.py` still
    is not. Written WITHOUT it first, this test failed on the `sequenced_after`
    refusal, which is how the docstring's first wording ("sibling-free") was
    caught overclaiming and narrowed to the sibling it is actually about."""
    gate = _sibling_less_gate(tmp_path)
    sequenced = ROOT / "scripts" / "sequenced_after.py"
    (gate / sequenced.name).write_bytes(sequenced.read_bytes())
    assert not (gate / "code_surface.py").exists()
    repo = tmp_path / "repo"
    change = repo / "openspec" / "changes" / "add-example"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        "---\ncode_surface: openxFactory\n"
        "scope_globs:\n  openxFactory:\n    - scripts/**\n---\n\n# Example\n",
        encoding="utf-8")
    env = {**_os_environ(), "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e"}
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "ratified"],
                   check=True, env=env)
    result = subprocess.run(
        [sys.executable, str(gate / "validate-scope-globs.py"),
         "--archive-gate", str(change), "--ratified-ref", "HEAD"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "scope-retention gate passed" in result.stdout


def _os_environ():
    import os
    return dict(os.environ)


def test_a_SYMLINKED_DEFAULT_REGISTER_is_not_used_by_the_scan(tmp_path):
    """THE OTHER LINE THE BENCH FLAGGED, PINNED AS ALREADY CLOSED.
    `REPO_ROOT/scripts/code-surface-register.yaml` is probed with `is_file()`,
    which follows symlinks and answers True for a link pointing outside the
    tree — but the probe grants nothing, because `code_surface.load_register`
    refuses a register that is a symlink OR has a symlinked ANCESTOR, and that
    guard is UNANCHORED and so strictly stronger than the path-boundary check.
    The unnamed default then falls back exactly as documented. The proof is the
    refusal's wording: the escaped register's entry `c` is NOT named."""
    outside = tmp_path / "outside"
    outside.mkdir()
    _register_naming(outside / "code-surface-register.yaml", "c",
                      _UNREADABLE_HEAD)
    root = tmp_path / "tree"
    change = root / "openspec" / "changes" / "c"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        f"---\ncode_surface: {_UNREADABLE_HEAD}\n"
        "scope_globs:\n  openxFactory:\n    - 'scripts/**'\n---\n\n# P\n",
        encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts" / "code-surface-register.yaml").symlink_to(
        outside / "code-surface-register.yaml")
    assert (root / "scripts" / "code-surface-register.yaml").is_file()  # follows
    result = _scan(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NO REPOSITORY SET CAN BE DERIVED" in result.stdout
    assert "entry `c`" not in result.stdout
    assert "not carried by the closed code-surface register" in result.stdout
