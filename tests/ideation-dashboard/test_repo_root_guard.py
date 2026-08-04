"""A wrong `--repo-root` REFUSES; it never serves an empty funnel (T092).

Brett hit this within minutes of starting the T092 acceptance pass. He was handed
a path from a different filesystem namespace — a container path, typed on the host
— and `cli.py generate` accepted it, projected NOTHING from it, wrote the
snapshot, printed `documents=0 clusters=0 possibles=0 …`, said "validation
SKIPPED — no reachable openxFactory checkout", and exited 0. Serving that
snapshot renders the dashboard's own empty-state copy — "a sparse funnel is an
honest funnel, not a broken one" — which is TRUE of an empty corpus and a lie
about a typo. Nothing in the pipeline could tell the two apart, because every
scan degrades quietly on purpose: a governed root that is not a directory is
skipped, a missing `openspec/changes` yields no changes, an undiscoverable
register yields no possibles.

Four behaviours are pinned here, each of which fails without its hunk:

  * `--repo-root` is REFUSED — on stderr, non-zero, with the resolved absolute
    path and what was looked for — before any scan and before the
    `OutputBoundary` write, so no snapshot file survives a refused run. One
    guard in the shared `_generate_and_write`, so `generate` and
    `generate-and-open` cannot diverge.
  * a root that IS a corpus but projects ZERO documents WARNS loudly and still
    succeeds: an empty corpus is legal, and failing on it would make an honestly
    empty repository unusable.
  * "validation SKIPPED" says WHY — it names BOTH roots the search walked up
    from (the OUTPUT path first, then `--repo-root`; see
    `test_snapshot_validation_launch.py`, which pins the fallback), so a skip
    blames neither on its own — instead of reading as routine.
  * `serve.py --checkout-root` (the same value under a second spelling) refuses a
    path that cannot be a checkout, and `_checkout_real` means what its name says.

Hermetic: the predicate is exercised over scratch trees under `tmp_path`, the one
corpus read is the tracked fixture repo (read-only; every write goes to
`tmp_path`), and the suite-wide guard makes the real `gh`/`nlm` unreachable. No
network, no real checkout is mutated.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION

from doc_health import corpus
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import corpus_root as corpus_root_mod
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot as snapshot_mod
from ideation_dashboard.corpus_root import (
    SCANNED_ROOTS, corpus_root_refusal, corpus_scan_defect,
)


def _corpus(root: Path, *, root_name: str = "ideation", document: str | None = None) -> Path:
    """A plausible corpus checkout in `tmp_path`: one of the scanned roots, and
    optionally a governed document inside it."""
    (root / root_name).mkdir(parents=True, exist_ok=True)
    if document is not None:
        (root / root_name / "note.md").write_text(document, encoding="utf-8")
    return root


DOC = ("# A note\n\nStatus: brainstorm\nKind: note\n"
       "Summary: a document the projection can see\nTopics: ideation-dashboard\n")


def _generate(tmp_path: Path, repo_root: Path | str, *extra: str) -> int:
    return cli_mod.main([
        "generate", "--repo-root", str(repo_root), "--repository", "fixture-repo",
        "--source-revision", PINNED_REVISION,
        "--output", str(tmp_path / "out" / "snapshot.json"), *extra])


# --------------------------------------------------------------------------
# the predicate: what the generator REALLY reads
# --------------------------------------------------------------------------

def test_the_scanned_roots_are_derived_from_the_doc_health_scan_not_transcribed():
    """The guard must accept every tree the projection can read anything from, or
    it would refuse a legal corpus. So the root set is DERIVED — the governed
    document roots `corpus.iter_doc_paths` walks, plus `openspec/`, which
    `generator._iter_changes` reads — and this pins the derivation rather than a
    copy of today's list: add a governed root to the doc-health scan and the guard
    accepts it with no edit here."""
    assert set(SCANNED_ROOTS) == {*corpus.GOVERNED_ROOTS, "openspec"}
    assert SCANNED_ROOTS == tuple(sorted(SCANNED_ROOTS))  # deterministic message


@pytest.mark.parametrize("root_name", SCANNED_ROOTS)
def test_any_single_scanned_root_makes_a_tree_plausible(tmp_path, root_name):
    """One scanned root is enough: `codexFactory` has no `contracts/`,
    `openxFactory` has no `apps/`, and a domain factory before its first staged
    topic has no `ideation/` — a predicate demanding a specific pair would refuse
    trees the projection reads perfectly well."""
    assert corpus_scan_defect(_corpus(tmp_path / root_name, root_name=root_name)) is None


def test_the_predicate_names_each_way_a_path_fails(tmp_path):
    missing = tmp_path / "not-here"
    file_path = tmp_path / "a-file"
    file_path.write_text("", encoding="utf-8")
    populated = tmp_path / "populated"
    (populated / "src").mkdir(parents=True)

    assert corpus_scan_defect(missing) == "the path does not exist"
    assert corpus_scan_defect(file_path) == "the path is not a directory"
    # existing, and NOT empty — the defect the old serve-side predicate missed
    assert corpus_scan_defect(populated) == (
        "the directory holds none of the roots a snapshot is projected from")
    assert corpus_scan_defect(BASE_REPO) is None


# --------------------------------------------------------------------------
# `generate` — refused before the write
# --------------------------------------------------------------------------

def test_generate_refuses_a_repo_root_from_another_namespace(tmp_path, capsys):
    """THE reproduction: the exact invocation that used to write an empty snapshot
    and exit 0."""
    rc = _generate(tmp_path, "/nonexistent/path/openxFactory")
    captured = capsys.readouterr()

    assert rc != 0
    assert "not a corpus checkout" in captured.err
    assert "/nonexistent/path/openxFactory" in captured.err
    # nothing at all on stdout: no `wrote …`, no counts to be misread as a result
    assert captured.out == ""
    assert not (tmp_path / "out").exists()


def test_generate_refuses_a_populated_directory_that_is_not_a_corpus(tmp_path, capsys):
    """The aggregation root above the checkout is the near-miss a human actually
    types: it exists, it is full of files, and it projects nothing."""
    wrong = tmp_path / "aggregation-root"
    (wrong / "xFactories").mkdir(parents=True)
    (wrong / "README.md").write_text("# not a corpus\n", encoding="utf-8")

    rc = _generate(tmp_path, wrong)
    err = capsys.readouterr().err

    assert rc != 0
    assert "holds none of the roots" in err
    assert not (tmp_path / "out").exists()


def test_generate_refuses_a_file(tmp_path, capsys):
    target = tmp_path / "snapshot-not-a-tree.json"
    target.write_text("{}", encoding="utf-8")

    assert _generate(tmp_path, target) != 0
    assert "not a directory" in capsys.readouterr().err


def test_the_refusal_names_the_resolved_path_what_it_wanted_and_a_correct_shape(
        tmp_path, capsys, monkeypatch):
    """The message is the whole fix: a human who reads it must be able to repair
    the invocation without reading the source. So it carries the RESOLVED absolute
    path (a relative one resolves against a cwd the reader may not share), every
    root it looked for, what the value has to be, and a runnable shape."""
    monkeypatch.chdir(tmp_path)
    assert _generate(tmp_path, "relative-and-absent") != 0
    err = capsys.readouterr().err

    assert str((tmp_path / "relative-and-absent").resolve()) in err
    for root in SCANNED_ROOTS:
        assert f"{root}/" in err
    assert "SERVED CHECKOUT" in err
    assert "namespace" in err          # the T092 cause, named
    assert "python3 scripts/ideation_dashboard/cli.py generate-and-open" in err
    assert "--repo-root <path to the corpus checkout>" in err
    # and it hardcodes nobody's filesystem: no home directory, no container path
    for leak in ("/home/", "/root/", "/srv/", "/workspace/", "/Users/"):
        assert leak not in err, f"the refusal hardcodes {leak}"


def test_the_refusal_is_one_guard_for_both_verbs():
    """`generate` and `generate-and-open` share `_generate_and_write`, and the
    guard lives THERE — not in each command — so a third caller cannot be added
    without it. Asserted on the shared function directly: the refusal raises out
    of it, ahead of the scan and the write (the output path here is unwritable by
    construction, so a hunk that guarded later would fail differently)."""
    args = cli_mod.build_parser().parse_args([
        "generate", "--repo-root", "/nonexistent/openxFactory",
        "--repository", "fixture-repo", "--output", "/nonexistent/snapshot.json"])
    with pytest.raises(cli_mod.RepoRootRefused) as refused:
        cli_mod._generate_and_write(args, Path("/nonexistent/snapshot.json"))
    assert "not a corpus checkout" in str(refused.value)


def test_generate_and_open_refuses_and_starts_no_server(tmp_path, capsys):
    """The verb a human actually runs (runbook §2). It must refuse before the
    server is built and the URL printed — a served empty funnel is the defect."""
    rc = cli_mod.main([
        "generate-and-open", "--repo-root", "/nonexistent/path/openxFactory",
        "--repository", "openxFactory", "--run-dir", str(tmp_path / "run"),
        "--no-open", "--no-serve"])
    captured = capsys.readouterr()

    assert rc != 0
    assert "not a corpus checkout" in captured.err
    # not even the run dir was minted, let alone a snapshot inside it
    assert not (tmp_path / "run").exists()
    assert not [ln for ln in captured.out.splitlines() if ln.startswith("http://")]


def test_a_real_corpus_is_not_refused(tmp_path, capsys):
    """The counter-check that keeps the guard honest: the fixture corpus still
    generates, still reports its counts, and still exits 0."""
    rc = _generate(tmp_path, BASE_REPO, "--no-validate")
    out = capsys.readouterr().out

    assert rc == 0
    written = tmp_path / "out" / "snapshot.json"
    assert written.is_file()
    snapshot = json.loads(written.read_text(encoding="utf-8"))
    assert snapshot["documents"], "the fixture corpus projects documents"
    assert "documents=0" not in out


# --------------------------------------------------------------------------
# an EMPTY corpus is legal — warned, never refused
# --------------------------------------------------------------------------

def test_an_empty_corpus_warns_loudly_and_still_succeeds(tmp_path, capsys):
    """The decision (item 3): a genuinely empty corpus is a legal state — a fresh
    repository, a domain factory before its first document — and a hard failure
    would make it unusable. But the guard proves only that the tree COULD be
    scanned, so the emptiness is stated on stderr, with the root that let the path
    through, and the human decides."""
    empty = _corpus(tmp_path / "fresh-repo")

    rc = _generate(tmp_path, empty, "--no-validate")
    captured = capsys.readouterr()

    assert rc == 0                                   # legal, not refused
    assert (tmp_path / "out" / "snapshot.json").is_file()
    assert "documents=0" in captured.out             # still reported plainly
    assert "ZERO documents" in captured.err
    assert str(empty.resolve()) in captured.err
    assert "ideation/" in captured.err               # why it was accepted
    assert "--repo-root" in captured.err             # the usual cause, named
    assert "WARNING" in captured.err and "not a failure" in captured.err


def test_a_corpus_with_documents_warns_about_nothing(tmp_path, capsys):
    populated = _corpus(tmp_path / "real-repo", document=DOC)

    assert _generate(tmp_path, populated, "--no-validate") == 0
    captured = capsys.readouterr()
    assert "documents=1" in captured.out
    assert "ZERO documents" not in captured.err


# --------------------------------------------------------------------------
# the validation skip says WHY (item 4)
# --------------------------------------------------------------------------

def test_the_validation_skip_names_the_directory_it_searched_and_the_reason(
        tmp_path, capsys):
    """The old line ("no reachable openxFactory checkout") read as routine and
    left the human believing the snapshot had been checked, while naming a
    checkout that was present and fine. The replacement leads with the
    consequence — NOT checked against the pinned schema — and names BOTH roots
    that were walked up from, because since `_locate_validator` neither one on
    its own is the reason (defect 8: the OUTPUT path is searched first, then
    `--repo-root`). Here neither reaches a validator, which is what a skip now
    means."""
    corpus_root = _corpus(tmp_path / "repo", document=DOC)
    out_dir = tmp_path / "out"

    rc = _generate(tmp_path, corpus_root)
    err = capsys.readouterr().err

    assert rc == 0                          # a skip is not a failure
    assert "NOT checked against the pinned schema" in err
    assert str(snapshot_mod.VALIDATOR_RELPATH) in err
    assert str(out_dir) in err               # WHERE it searched, first…
    assert str(corpus_root) in err           # …and where it fell back to
    assert snapshot_mod.find_validator(out_dir) is None, (
        "this test's premise: no validator is reachable from the output dir")
    assert snapshot_mod.find_validator(corpus_root) is None, (
        "…nor from --repo-root, which is why the skip is legitimate here")


# --------------------------------------------------------------------------
# serve.py: the same value under a second spelling (item 5)
# --------------------------------------------------------------------------

def test_serve_refuses_a_checkout_root_that_cannot_be_a_checkout(
        tmp_path, capsys, monkeypatch):
    """`--checkout-root` had the same hole in a different shape: accepted in
    silence, after which the dashboard came up — really came up, this test hung
    on `serve_forever` before the guard existed — with every checkout-bound
    affordance absent and `/source/` 404ing, and nothing said why. A path that
    does not exist can never be a served checkout, so it is refused before the
    socket is bound (`serve` is stubbed here to make "never reached" assertable
    rather than a timeout)."""
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    served: list[tuple] = []
    monkeypatch.setattr(serve_mod, "serve", lambda *a, **k: served.append((a, k)))

    rc = serve_mod.main(["--snapshot", str(snapshot),
                         "--checkout-root", "/nonexistent/openxFactory"])
    err = capsys.readouterr().err

    assert rc != 0
    assert served == [], "a refused --checkout-root must start no server"
    assert "--checkout-root is not a corpus checkout" in err
    assert "/nonexistent/openxFactory" in err
    assert "python3 scripts/ideation_dashboard/serve.py" in err


def test_serve_still_serves_the_hosted_empty_sentinel_but_says_what_is_off(
        tmp_path, capsys, monkeypatch):
    """The one legitimate non-corpus configuration: the served image mounts an
    empty directory so `_checkout_real` is false and the write-bearing affordances
    stay off. It must keep serving — and now says so, because on a LOCAL run the
    same state is a wrong path."""
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("{}", encoding="utf-8")
    sentinel = tmp_path / "srv-empty"
    sentinel.mkdir()
    served: list[tuple] = []
    monkeypatch.setattr(serve_mod, "serve",
                        lambda *a, **k: served.append((a, k)))

    rc = serve_mod.main(["--snapshot", str(snapshot),
                         "--checkout-root", str(sentinel)])
    err = capsys.readouterr().err

    assert rc == 0
    assert served, "the sentinel configuration must still serve"
    assert "is not a corpus checkout" in err
    assert "serving anyway" in err
    assert "no gate actions" in err and "no branch sessions" in err


def test_checkout_real_requires_a_corpus_not_merely_a_non_empty_directory(tmp_path):
    """`_checkout_real` gates the local gate/session affordances, and those
    affordances WRITE INTO the tree it approves. It used to mean "an existing,
    non-empty directory", so a wrong-but-populated path (a home directory, a
    workspace root, a sibling repository) turned them on; its docstring already
    promised a corpus checkout."""
    populated = tmp_path / "not-a-corpus"
    (populated / "src").mkdir(parents=True)
    (populated / "README.md").write_text("# something else\n", encoding="utf-8")
    empty = tmp_path / "srv-empty"
    empty.mkdir()

    assert serve_mod._checkout_real(BASE_REPO) is True
    assert serve_mod._checkout_real(_corpus(tmp_path / "fresh")) is True
    assert serve_mod._checkout_real(populated) is False   # the tightened case
    assert serve_mod._checkout_real(empty) is False       # the hosted sentinel
    assert serve_mod._checkout_real(tmp_path / "does-not-exist") is False


def test_the_predicate_costs_the_serving_path_no_new_dependency():
    """`_checkout_real` runs on EVERY `build_server`, the served image's included,
    and that image serves snapshots and scans nothing. So the predicate lives in a
    module whose imports are the standard library plus `doc_health.corpus` (which
    the serving path already uses) — reaching it through `generator` would have
    made PyYAML a startup requirement of a process that never parses YAML."""
    tree = ast.parse(Path(corpus_root_mod.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported == {"__future__", "pathlib", "doc_health"}, imported


def test_both_entrypoints_share_one_refusal_definition():
    """Two spellings, ONE predicate and ONE message body — a divergence here is a
    human learning the rule on one entrypoint and being surprised by the other."""
    repo_flag = corpus_root_refusal("/nonexistent/x", flag="--repo-root")
    checkout_flag = corpus_root_refusal("/nonexistent/x", flag="--checkout-root")
    assert repo_flag is not None and checkout_flag is not None
    assert repo_flag.replace("--repo-root", "@") == checkout_flag.replace(
        "--checkout-root", "@")
    assert corpus_root_refusal(BASE_REPO) is None
