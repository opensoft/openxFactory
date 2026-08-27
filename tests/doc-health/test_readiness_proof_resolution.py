"""The readiness derivation proof's own three properties
(`harden-ideation-readiness-check`; doc-health delta, nine scenarios).

Every test here is pinned to the DEFECT rather than to the fix. The three
defects, all measured on 2026-08-26 against `origin/main`:

  A. the proof resolved its subject by walking UP from the repository under
     test to the first ancestor holding `openxFactory/ideation/cross-reference.yaml`,
     which inside the aggregation workspace is always the ONE shared checkout —
     so every agent worktree proved a verdict about somebody else's tree;
  B. it read the index from a WORKING TREE, so a concurrent uncommitted edit in
     that shared checkout reddened every worktree on the machine while every
     isolated clone passed at every revision;
  C. an unresolvable `generation.source_revision` became `pytest.skip`, so the
     assertion had never executed in a fresh clone, and the skip's stated
     reason ("shallow clone?") was a conjecture that is FALSE in the one place
     it fires — `pytest-suite.yml` checks out at `fetch-depth: 0`.

The fixtures are real git repositories under `tmp_path`; no test touches any
checkout on the machine. The three resolver spellings are exercised TOGETHER
(`RESOLVERS`), because the hazard survives in whichever module is left behind.
"""

from __future__ import annotations

import subprocess

from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import corpus
from doc_health import ideation_readiness as ir

import test_derive_possibles as tdp
import test_ideation_readiness as tir
import test_readiness_dispatch as trd


# The three modules that each spell the resolver (packet § 2.1 / § 2.2). Q3 —
# whether they collapse into one shared fixture — is OPEN; until it is ruled,
# THIS is what keeps the three honest with one another.
RESOLVERS = {
    "test_ideation_readiness": tir,
    "test_derive_possibles": tdp,
    "test_readiness_dispatch": trd,
}

INDEX_REL = Path("ideation") / "cross-reference.yaml"

DOC_A = "ideation/brainstorm/alpha-one.md"
DOC_B = "ideation/brainstorm/alpha-two.md"


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=check)


def _doc_text(name, topic):
    return (f"# {name}\n\nStatus: brainstorm\nTopics: {topic}\n\n## Body\n\n"
            f"Body prose for {name} describing the recurring {topic} subject "
            "in enough depth to cluster.\n")


def _init_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    return root


def _write_corpus(root, topic="alpha"):
    (root / "ideation" / "brainstorm").mkdir(parents=True, exist_ok=True)
    (root / DOC_A).write_text(_doc_text("alpha-one.md", topic), "utf-8")
    (root / DOC_B).write_text(_doc_text("alpha-two.md", topic), "utf-8")


def _write_index(root, *, pin, entries):
    import yaml
    (root / INDEX_REL).write_text(
        yaml.safe_dump({"schema_version": 1, "kind": "ideation-cross-reference",
                        "repository": "openxFactory",
                        "generation": {"source_revision": pin,
                                       "generator_version": "fixture"},
                        "topic_entries": entries},
                       sort_keys=False, allow_unicode=True),
        encoding="utf-8")


def coherent_repo(root, *, pin=None):
    """A fixture repository whose COMMITTED index is true about its own corpus.

    Two commits, deliberately: the corpus lands first, and the index lands
    second pinning the corpus commit. The index file is therefore absent from
    the corpus it describes, exactly as a regenerated index is, and the proof's
    two revision-addressed sides are genuinely independent.

    `pin` overrides the pinned revision, which is how the unreachable-pin
    fixtures are built."""
    _init_repo(root)
    _write_corpus(root)
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "corpus")
    corpus_rev = _git(root, "rev-parse", "HEAD").stdout.strip()

    derived = ir.derive_clusters(corpus.load_docs("openxFactory", root))
    assert derived, "the fixture corpus must cluster, or it proves nothing"
    _write_index(root, pin=pin or corpus_rev, entries=derived)
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "index")
    return root, corpus_rev, derived


def skeletons(entries):
    return [{"id": e["id"], "name": e["name"], "topics": e["topics"],
             "tag_sources": sorted(e["tag_sources"]), "origin": e.get("origin"),
             "members": [{"path": m["path"], "matched_tags": m["matched_tags"],
                          "repository": m.get("repository")}
                         for m in e["members"]]}
            for e in entries]


def run_the_proof(repo, tmp_path):
    """The proof's own three steps, driven over a fixture repository: read the
    index from COMMITTED state, reconstruct the corpus at the revision that
    index pins, derive, compare. Uses the shipped helpers, so a regression in
    either of them fails here."""
    import yaml
    index_text, index_rev = tir._committed_index(repo)
    index = yaml.safe_load(index_text)
    pin = index["generation"]["source_revision"]
    tir._corpus_at_pin(repo, pin, tmp_path,
                       index_named=f"{(repo / INDEX_REL).as_posix()} at {index_rev}")
    derived = ir.derive_clusters(corpus.load_docs("openxFactory", tmp_path))
    return skeletons(derived) == skeletons(index["topic_entries"])


# =========================================================================
# Requirement 1 — the proof resolves the repository under test
# =========================================================================

def aggregation_layout(tmp_path):
    """The workspace shape that produced defect A: an aggregation root holding
    a checkout at `openxFactory/`, with the repository under test sitting
    BELOW it in a worktrees directory. The ancestor walk finds the sibling; the
    repository under test is what the run is actually about."""
    agg = tmp_path / "aggregation"
    sibling = agg / "openxFactory"
    under_test = agg / "worktrees" / "under-test"
    for root in (sibling, under_test):
        (root / "ideation").mkdir(parents=True)
        _write_index(root, pin="0" * 40, entries=[])
    (sibling / "scripts").mkdir(parents=True)
    (sibling / "scripts" / "validate-ideation-cross-reference.py").write_text(
        "# the sibling checkout's validator\n", encoding="utf-8")
    (under_test / "scripts").mkdir(parents=True)
    (under_test / "scripts" / "validate-ideation-cross-reference.py").write_text(
        "# the repository under test's own validator\n", encoding="utf-8")
    return agg, sibling, under_test


@pytest.mark.parametrize("module", sorted(RESOLVERS))
def test_the_repository_under_test_wins_over_an_ancestor_checkout(tmp_path,
                                                                  module):
    """Delta scenario "The proof runs from a worktree of the repository under
    test". Defect A directly: the ancestor ALSO carries an index here, which is
    the condition under which the old walk resolved it."""
    _, sibling, under_test = aggregation_layout(tmp_path)
    said = []
    resolved = RESOLVERS[module]._openxfactory_root(
        under_test, announce=said.append)
    assert resolved == under_test.resolve()
    assert resolved != sibling.resolve()
    assert said == [], "the first rung is not a fallback and says nothing"


@pytest.mark.parametrize("module", sorted(RESOLVERS))
def test_a_fallback_names_the_checkout_it_resolved_and_why(tmp_path, module):
    """Delta scenario "The repository under test cannot serve the proof": the
    fallback is reached only after the repository under test is tried, and the
    run records which checkout it took."""
    _, sibling, under_test = aggregation_layout(tmp_path)
    (under_test / INDEX_REL).unlink()          # the subject cannot serve it
    said = []
    resolved = RESOLVERS[module]._openxfactory_root(
        under_test, announce=said.append)
    assert resolved == sibling
    assert len(said) == 1
    spoken = said[0]
    assert RESOLVERS[module].ROOT_FALLBACK_MARKER in spoken
    assert str(sibling) in spoken                     # WHICH checkout
    assert str(under_test) in spoken                  # ...instead of which
    assert "carries no" in spoken                     # ...and WHY


@pytest.mark.parametrize("module", sorted(RESOLVERS))
def test_the_explicit_argument_and_the_env_override_precede_the_walk(
        tmp_path, module, monkeypatch):
    """The reach-further order design § 1 records, and it is the order already
    pinned for the renderer: explicit argument, then OPENXFACTORY_ROOT, then
    the walk."""
    _, sibling, under_test = aggregation_layout(tmp_path)
    (under_test / INDEX_REL).unlink()
    declared = tmp_path / "declared"
    explicit = tmp_path / "explicit"
    for root in (declared, explicit):
        (root / "ideation").mkdir(parents=True)
        _write_index(root, pin="0" * 40, entries=[])

    monkeypatch.setenv("OPENXFACTORY_ROOT", str(declared))
    assert RESOLVERS[module]._openxfactory_root(
        under_test, fallback=explicit, announce=lambda _: None) == explicit
    assert RESOLVERS[module]._openxfactory_root(
        under_test, announce=lambda _: None) == declared
    monkeypatch.delenv("OPENXFACTORY_ROOT")
    assert RESOLVERS[module]._openxfactory_root(
        under_test, announce=lambda _: None) == sibling


@pytest.mark.parametrize("module", sorted(RESOLVERS))
def test_no_checkout_at_all_is_reported_not_passed(tmp_path, module,
                                                   monkeypatch):
    """Delta scenario "No checkout can serve the proof": not performed, named,
    and never a pass."""
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    barren = tmp_path / "barren" / "deep"
    barren.mkdir(parents=True)
    assert RESOLVERS[module]._openxfactory_root(barren) is None
    with pytest.raises(pytest.skip.Exception) as skipped:
        RESOLVERS[module]._openxfactory_root_or_skip(barren)
    reason = str(skipped.value)
    assert "NOT PERFORMED" in reason
    assert str(barren) in reason
    assert "cross-reference.yaml" in reason


def test_the_validator_resolves_out_of_the_repository_under_test(tmp_path):
    """The delta's "every checkout the readiness surface reaches for" clause:
    `find_index_validator()` carried the identical walk and — measured
    2026-08-26 — returned the SHARED checkout's validator from an agent
    worktree. A proof that reads its subject from one checkout and its
    validator from another has proved nothing about either."""
    _, sibling, under_test = aggregation_layout(tmp_path)
    said = []
    own = ir.find_index_validator(under_test, announce=said.append)
    assert own == under_test / "scripts" / "validate-ideation-cross-reference.py"
    assert said == []

    own.unlink()
    borrowed = ir.find_index_validator(under_test, announce=said.append)
    assert borrowed == sibling / "scripts" / "validate-ideation-cross-reference.py"
    assert len(said) == 1 and str(sibling) in said[0]


def test_the_live_run_resolves_this_checkout_not_a_sibling():
    """The acceptance signal, asserted rather than merely observed: run from
    ANY worktree, the resolver answers THAT worktree. Before the fix this
    returned the shared checkout beneath the aggregation root."""
    if not (Path(REPO_ROOT) / INDEX_REL).is_file():
        pytest.skip(f"{REPO_ROOT} carries no {INDEX_REL.as_posix()} of its own")
    for module in sorted(RESOLVERS):
        assert RESOLVERS[module]._openxfactory_root() == Path(REPO_ROOT).resolve()
    validator = ir.find_index_validator()
    assert validator is not None
    assert validator.parent.parent == Path(REPO_ROOT).resolve()


@pytest.mark.parametrize("module", sorted(RESOLVERS))
def test_mutation_reverting_the_resolver_alone_reproduces_defect_a(tmp_path,
                                                                   module):
    """THE MUTATION CHECK (packet § 2.6, in the style of
    `test_mutation_reverting_parse_header_alone_reproduces_the_f5_divergence`).

    The pre-change resolver is spelled out below verbatim. Over the SAME
    fixture layout it resolves the ancestor checkout while the shipped resolver
    resolves the repository under test — so these tests are pinned to defect A
    and are not merely passing."""
    _, sibling, under_test = aggregation_layout(tmp_path)

    def reverted(base):                     # the resolver as it stood
        marker = Path("openxFactory") / "ideation" / "cross-reference.yaml"
        base = Path(base).resolve()
        for d in [base, *base.parents]:
            if (d / marker).is_file():
                return d / "openxFactory"
        return None

    assert reverted(under_test) == sibling, (
        "the fixture must reproduce the defect, or the mutation proves nothing")
    assert RESOLVERS[module]._openxfactory_root(
        under_test, announce=lambda _: None) == under_test.resolve()


# =========================================================================
# Requirement 2 — the comparison reads committed index state
# =========================================================================

def test_a_working_tree_edit_cannot_move_the_verdict(tmp_path):
    """Delta scenarios "Another session holds an uncommitted index edit" and
    "The change under review edits the index".

    Defect B measured: the shared checkout held an uncommitted index listing 67
    clusters against 253 derived, and every worktree on the machine went red
    over it. Here the working tree is mangled the same way and the verdict does
    not move, because the index is read at a named committed revision."""
    repo, corpus_rev, derived = coherent_repo(tmp_path / "repo")
    assert run_the_proof(repo, tmp_path / "clean-extract") is True

    _write_index(repo, pin=corpus_rev, entries=[])   # uncommitted, and wrong
    assert (repo / INDEX_REL).read_text("utf-8") != _git(
        repo, "show", f"HEAD:{INDEX_REL.as_posix()}").stdout
    assert run_the_proof(repo, tmp_path / "dirty-extract") is True, (
        "an uncommitted edit moved the verdict — the index was read from the "
        "working tree")

    text, rev = tir._committed_index(repo)
    assert "topic_entries: []" not in text
    assert rev == _git(repo, "rev-parse", "HEAD").stdout.strip()


def test_the_comparison_names_the_revision_it_read_the_index_at(tmp_path):
    """Delta scenario "The comparison assembles its two sides": the index at a
    NAMED committed revision of the repository under test, the corpus at the
    revision that index itself pins."""
    repo, corpus_rev, _ = coherent_repo(tmp_path / "repo")
    text, rev = tir._committed_index(repo)
    assert len(rev) == 40 and rev != corpus_rev     # HEAD, not the pin
    import yaml
    assert yaml.safe_load(text)["generation"]["source_revision"] == corpus_rev
    # ...and the read point is addressed BY NAME rather than by accident: ask
    # for the corpus commit, where the index did not yet exist, and the reader
    # says so about THAT revision instead of silently answering with another.
    with pytest.raises(pytest.fail.Exception) as failed:
        tir._committed_index(repo, "HEAD~1")
    assert corpus_rev[:12] in str(failed.value)


def test_an_index_that_is_not_committed_fails_rather_than_falling_back(
        tmp_path):
    """The committed read point fails closed. An index present only in a
    working tree is not proved — stated in the delta as the accepted trade, and
    enforced here so no future edit quietly restores the working-tree read."""
    repo = _init_repo(tmp_path / "repo")
    _write_corpus(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "corpus")
    _write_index(repo, pin="0" * 40, entries=[])     # never committed
    with pytest.raises(pytest.fail.Exception) as failed:
        tir._committed_index(repo)
    assert "not committed" in str(failed.value)


# =========================================================================
# Requirement 3 — an unreachable pinned revision fails the proof
# =========================================================================

ORPHAN = "f13a3b6007736292e1e157febef1ac733e534de9"   # the live instance, 2026-08-26

# A skip and a failure are BOTH raised outcomes, and telling them apart is the
# whole of requirement 3 — so both are caught and the verdict is asserted.
OUTCOMES = (pytest.fail.Exception, pytest.skip.Exception)


def test_an_unreachable_pin_in_a_complete_clone_fails(tmp_path):
    """Delta scenario "The pin is unreachable in a complete clone". THE
    FIXTURE IS THE LIVE DEFECT: `main`'s index pinned `f13a3b60`, a commit
    reachable from no ref, and the proof reported a skip — which is why the
    assertion had never run in a fresh clone."""
    repo, _, _ = coherent_repo(tmp_path / "repo", pin=ORPHAN)
    assert _git(repo, "rev-parse", "--is-shallow-repository").stdout.strip() \
        == "false"
    # BOTH outcomes are caught, then discriminated: were only `Failed` caught,
    # a regression back to the skip would report this test as SKIPPED — green
    # scoreboard, silent verification, which is defect C exactly.
    with pytest.raises(OUTCOMES) as caught:
        tir._corpus_at_pin(repo, ORPHAN, tmp_path / "out",
                           index_named=f"{(repo / INDEX_REL).as_posix()} at HEAD")
    assert isinstance(caught.value, pytest.fail.Exception), (
        f"an unreachable pin in a COMPLETE clone must FAIL the proof, not "
        f"{type(caught.value).__name__}: {caught.value}")
    reason = str(caught.value)
    assert ORPHAN in reason                       # names the pin
    assert "cross-reference.yaml" in reason       # ...and the index carrying it
    assert "COMPLETE" in reason
    assert "shallow clone?" not in reason         # never the old conjecture


def test_a_truncated_clone_skips_naming_the_truncation_it_observed(tmp_path):
    """Delta scenario "The clone is truncated": Q1's narrowed skip survives,
    and its reason names the truncation OBSERVED rather than conjectured."""
    repo, _, _ = coherent_repo(tmp_path / "repo")
    _write_corpus(repo, topic="beta")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "later")
    deep_rev = _git(repo, "rev-parse", "HEAD~2").stdout.strip()

    shallow = tmp_path / "shallow"
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--no-local",
                    f"file://{repo}", str(shallow)],
                   capture_output=True, check=True)
    assert _git(shallow, "rev-parse", "--is-shallow-repository").stdout.strip() \
        == "true"

    with pytest.raises(OUTCOMES) as caught:
        tir._corpus_at_pin(shallow, deep_rev, tmp_path / "out",
                           index_named="fixture index")
    assert isinstance(caught.value, pytest.skip.Exception), (
        f"a genuinely truncated clone keeps the narrowed skip (Q1, KEEP), not "
        f"{type(caught.value).__name__}: {caught.value}")
    reason = str(caught.value)
    assert "TRUNCATED CLONE" in reason
    assert "observed not conjectured" in reason
    assert deep_rev in reason


def test_a_resolvable_pin_runs_the_comparison(tmp_path):
    """Delta scenario "The pin resolves": no resolution branch may return a
    skip in place of a comparison that could have been performed."""
    repo, corpus_rev, derived = coherent_repo(tmp_path / "repo")
    out = tir._corpus_at_pin(repo, corpus_rev, tmp_path / "out",
                             index_named="fixture index")
    assert (out / DOC_A).is_file() and (out / DOC_B).is_file()
    assert not (out / INDEX_REL).exists(), (
        "the index landed AFTER the corpus commit; if it appears here the "
        "fixture's two sides are not independent")
    assert skeletons(ir.derive_clusters(
        corpus.load_docs("openxFactory", out))) == skeletons(derived)


def test_the_landed_index_pins_a_revision_this_repository_can_resolve():
    """The repair, asserted where it will decay: `ideation/cross-reference.yaml`
    must pin a revision the repository can actually reconstruct. This is the
    check that would have caught the orphaned pin the day the squash landed —
    it fails on `f13a3b60` in any clone that never fetched the source branch."""
    import yaml
    repo = Path(REPO_ROOT)
    if not (repo / INDEX_REL).is_file():
        pytest.skip(f"{repo} carries no {INDEX_REL.as_posix()} of its own")
    if _git(repo, "rev-parse", "--is-shallow-repository",
            check=False).stdout.strip() == "true":
        pytest.skip(f"{repo} is a shallow clone; reachability is a fact about "
                    "the clone here, not about the index")
    pin = yaml.safe_load((repo / INDEX_REL).read_text("utf-8"))[
        "generation"]["source_revision"]
    reachable = _git(repo, "merge-base", "--is-ancestor", pin, "HEAD",
                     check=False).returncode == 0
    assert reachable, (
        f"{INDEX_REL.as_posix()} pins {pin}, which is not an ancestor of HEAD "
        "— the index names a corpus state no reader can reconstruct from this "
        "history (re-pin it, as harden-ideation-readiness-check § 3 did)")
