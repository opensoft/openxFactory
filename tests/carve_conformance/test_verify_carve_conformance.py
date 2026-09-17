"""FLOOR PART 3 — the neutral conformance corpus, and the runner that puts a
reader through it (`split-opendox-two-layer-product` § 3.7, design § D6 (3)).

THREE CLAIMS ARE UNDER TEST HERE AND THEY ARE DIFFERENT CLAIMS.

  1. **The corpus is neutral**, which is § 3.7's own wording: "no `openspec/`,
     no `contracts/`, no lifecycle headers". That is a property of the FILES,
     asserted here rather than inside the checks, because a neutral module
     cannot name the words it exists to be free of — the same reason
     `tests/corpus-adapter/fixtures/README.md` sits outside `neutral/`.
  2. **openxFactory's own adapter passes it**, through the documented
     command line and not through an imported function. § 3.7 calls that "the
     only mechanical proof that the home corpus has no privileged route".
  3. **The corpus has TEETH**, which is the claim the other two rest on. A
     green run over one well-behaved reader proves that reader behaves; it
     does not prove the corpus would catch one that does not. So six
     deliberately non-conformant readers are defined below and each is
     asserted to FAIL the specific check that exists to catch it. Delete a
     check and its mutation goes green, which is what makes this file
     evidence rather than decoration. The seed suite
     (`tests/corpus-adapter/test_conformance.py`) established the doctrine
     with two such readers; this file owes more of them because it owns more
     checks.

THE SEVENTH READER IS NOT A MUTATION BUT A PROPERTY. `ForeignRefusal` raises
its OWN exception class over its OWN refusal type — the situation at every
carved destination, each of which holds a replica of the interface module and
therefore a different class object with the same name. It must PASS. An
`isinstance` test against openxFactory's copy would report it as having raised
something unrelated, turning a conformant reader into a red run for a reason
that is about Python's module identity and nothing to do with the corpus.

  4. **A TRANSPOSED corpus is PROVEN faithful, never trusted** — RULED Q-F1
     (a) (Brett Heap, 2026-09-17, `#656` comment `5714365086`). A destination
     whose corpus is git HISTORY cannot address the corpus as it ships, so
     the ruling lets that destination lay the same documents down in the
     storage form its reader addresses and hand the result in with
     `--corpus`. Section 5 below holds that permission to its price: a
     genuine bare-repository transposition, built by this file's own
     `git_history_factory.transpose()` and read back by a reader that has no
     working tree to fall back on, passes the fidelity proof AND all
     seventeen checks; and three transpositions that changed a byte, dropped
     a document and added one are each refused BY NAME before a check runs.
     A test that used the home reader over a COPY of the fixtures would
     exercise the comparison and never the case the ruling was written for,
     so both are here and only the first is evidence for the ruling.

THE SCRIPT IS RUN AS A SUBPROCESS for behaviour and loaded by path only for
constants — `tests/carve_arrival/test_verify_carve_arrival.py`'s rule, adopted
for its reason: the documented way in is a command line, and a test of the
imported function proves the code executes rather than that the invocation an
operator will type succeeds and prints what its readers depend on.

Hermetic: no network, no subprocess but this repository's own interpreter over
its own tree, and nothing is written outside `tmp_path`. The one check that
would touch the corpus (a write-back that writes the tree) runs over a COPY in
`tmp_path`, because a test that could damage the fixtures it asserts on is a
test that eventually does.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify-carve-conformance.py"
CORPUS = REPO_ROOT / "tests" / "corpus-adapter" / "fixtures"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

import carve_conformance as CC  # noqa: E402
from corpus_adapter import (  # noqa: E402
    CORPUS_ABSENT,
    CORPUS_READ_ONLY,
    DOCUMENT_UNKNOWN,
    CorpusRef,
    CorpusRefused,
    Document,
    Refusal,
)
from home_factory import NEUTRAL_SHAPE, neutral_reader  # noqa: E402
#: The reader whose corpus is git HISTORY, and the transposition it
#: addresses — RULED Q-F1 (a)'s evidence. Section 5 is the only user.
import git_history_factory as GH  # noqa: E402

# The vocabulary, restated as a LITERAL rather than imported. Asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology; spelling
# it out is what makes a silent rename or reorder a test failure, because an
# operator's runbook and a caller's branch both read these strings.
RATIFIED_CODES = (
    "conformance-adapter-undeclared",
    "conformance-adapter-unresolvable",
    "conformance-corpus-missing",
    "conformance-corpus-unfaithful",
    "conformance-check-failed",
    "conformance-unreadable",
)

#: The check set, restated as a LITERAL for `RATIFIED_CODES`' reason and not
#: imported: `CC.CHECKS == CC.CHECKS` is a tautology, and these identifiers
#: leave the process — they are the `--json` payload's `outcomes[].check` and
#: the names a refusal lists — so a silent rename or reorder has to fail
#: somewhere. `test_every_declared_check_actually_runs` proves the tuple is
#: what a RUN emits; this proves the tuple is what was agreed.
RATIFIED_CHECKS = (
    "structural-conformance",
    "resolve-populated",
    "list-population",
    "list-stable",
    "read-round-trip",
    "classify-population",
    "classify-reports-unrecognizable",
    "check-severities",
    "empty-is-an-answer",
    "read-only-declared-at-resolution",
    "absent-refuses",
    "unreadable-refuses",
    "unknown-scope-refuses",
    "unknown-document-refuses",
    "unknown-revision-refuses",
    "write-back-refuses-read-only",
    "write-back-leaves-the-tree",
)

#: § 3.7's own words for what the corpus must not carry, and the lifecycle
#: header word `document-lifecycle.md` defines. Named HERE, on the home side,
#: for the reason the module docstring gives.
FORBIDDEN_PATH_PARTS = ("openspec", "contracts")
LIFECYCLE_HEADER = "Status:"

HOME_INVOCATION = ("--destination", "openxfactory", "--dest-root",
                   str(REPO_ROOT), "--adapter", "home_factory:neutral_reader",
                   "--sys-path", "tests/carve_conformance")


def _load():
    spec = importlib.util.spec_from_file_location(
        "verify_carve_conformance", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = _load()


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, check=False,
                          cwd=str(REPO_ROOT))


def _locations(root: Path) -> dict[str, str]:
    """The four states, named off the runner's own constants so that renaming
    one in the script and not here cannot leave this file testing a corpus the
    operator's command line does not use."""
    return {"populated": str(root / MODULE.POPULATED),
            "empty": str(root / MODULE.EMPTY),
            "unreadable": str(root / MODULE.UNREADABLE),
            "absent": str(root / MODULE.ABSENT)}


def _outcomes(factory, root: Path = CORPUS):
    return CC.run(factory, **_locations(root))


def _failed(factory, root: Path = CORPUS) -> set[str]:
    _, _, failed = CC.verdict(_outcomes(factory, root))
    return set(failed)


# ==========================================================================
# 1. the corpus is neutral — § 3.7's own words
# ==========================================================================


def test_the_corpus_carries_no_governed_directory_anywhere_in_its_paths():
    """No `openspec/` and no `contracts/` — read off the tree, not asserted.

    The scan is over paths RELATIVE to the corpus. An absolute one would
    carry every parent directory of the checkout, so a clone under a
    directory that happened to be called `contracts` would fail a test about
    the corpus for a reason that has nothing to do with it — and the offender
    list this reports is relative already, so the two would disagree about
    what was even being examined.
    """
    offenders = [
        p.relative_to(CORPUS).as_posix()
        for p in CORPUS.rglob("*")
        if any(part in FORBIDDEN_PATH_PARTS
               for part in p.relative_to(CORPUS).parts)]
    assert offenders == [], (
        "the neutral conformance corpus carries a governed directory: "
        f"{offenders}. § 3.7's corpus is one 'with no openspec/, no "
        "contracts/' precisely so that a reader authored for a corpus with "
        "neither is not quietly required to know them")


def test_no_document_in_the_corpus_carries_a_lifecycle_header():
    """The third of § 3.7's three exclusions, and the least visible.

    `neutral/` is scanned; `fixtures/README.md` is DELIBERATELY not, and the
    exclusion is the fixtures README's own stated design — it is documentation
    ABOUT the corpus and "the neutral corpus must not contain the words it
    exists to prove a reader does not need", so the explanation lives outside
    the thing explained.
    """
    offenders = []
    for path in sorted((CORPUS / "neutral").rglob("*")):
        if not path.is_file():
            continue
        head = path.read_text(encoding="utf-8").splitlines()[
            :NEUTRAL_SHAPE.header_scan_lines]
        if any(line.startswith(LIFECYCLE_HEADER) for line in head):
            offenders.append(path.relative_to(CORPUS).as_posix())
    assert offenders == [], (
        f"a corpus document carries a lifecycle header: {offenders}. The "
        "corpus's header vocabulary is its own two fields and belongs to no "
        "governed repository")


def test_the_corpus_is_where_the_manifest_says_it_is():
    """The corpus is NOT relocated, and this is the guard on that.

    Eleven rows of `docs/opendox-carve-manifest.yaml` name these exact paths
    as `not_moved / replicated_at_destination`. A well-meant tidy-up that
    moved the fixtures under this directory would leave those rows pointing at
    nothing and give the floor two corpora, which is the one shape "every
    destination passes IT" cannot survive.
    """
    assert MODULE.CORPUS_RELPATH == "tests/corpus-adapter/fixtures"
    for name in (MODULE.POPULATED, MODULE.EMPTY):
        assert (CORPUS / name).is_dir(), f"{name} is not at {CORPUS}"
    assert (CORPUS / MODULE.UNREADABLE).is_file()
    assert not (CORPUS / MODULE.ABSENT).exists()


def test_the_checks_module_carries_no_home_vocabulary():
    """`scripts/carve_conformance.py` is held to the INTERFACE's own bar.

    `tests/corpus-adapter/test_no_home_vocabulary.py` scans the interface over
    its whole source text because "that file travels to openDox and is what
    every implementer of the standard reads". Every word of that reasoning is
    true of this module too — every destination runs it — so the same scan is
    applied here rather than a weaker one.
    """
    sys.path.insert(0, str(REPO_ROOT / "tests" / "corpus-adapter"))
    try:
        spec = importlib.util.spec_from_file_location(
            "no_home_vocabulary",
            REPO_ROOT / "tests" / "corpus-adapter" /
            "test_no_home_vocabulary.py")
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
    finally:
        sys.path.pop(0)
    source = (REPO_ROOT / "scripts" / "carve_conformance.py").read_text(
        encoding="utf-8")
    hits = guard.offending(source, shapes=guard.PATH_SHAPES)
    assert hits == [], (
        f"scripts/carve_conformance.py carries home vocabulary: "
        f"{sorted(set(hits))}")


def test_the_checks_module_imports_only_the_interface_and_the_standard_library():
    """The other half of neutrality, and it is read by parsing.

    A destination runs this module while holding none of openxFactory. An
    import of anything but `corpus_adapter` and the standard library would
    make that impossible, and prose saying so is not a guard.
    """
    tree = ast.parse((REPO_ROOT / "scripts" / "carve_conformance.py").read_text(
        encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            imported.add((node.module or "").split(".")[0])
    allowed = set(sys.stdlib_module_names) | {"corpus_adapter"}
    assert imported <= allowed, (
        f"scripts/carve_conformance.py imports {sorted(imported - allowed)}, "
        "which a destination running the corpus would have to hold")


# ==========================================================================
# 2. openxFactory's own adapter passes it — the documented invocation
# ==========================================================================


def test_the_home_adapter_passes_the_whole_corpus_through_the_command_line():
    """§ 3.7's third destination, and the run that makes the other two
    measurable rather than rhetorical."""
    done = _run(*HOME_INVOCATION)
    assert done.returncode == 0, (
        f"the home adapter did not pass:\n{done.stdout}\n{done.stderr}")
    assert done.stdout.startswith("OK "), done.stdout
    assert "passed the neutral conformance corpus" in done.stdout


def test_the_home_run_reports_every_declared_check_as_json():
    done = _run(*HOME_INVOCATION, "--json")
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "ok"
    assert payload["destination"] == "openxfactory"
    assert payload["failed"] == []
    assert payload["checks_run"] == payload["checks_declared"] == len(CC.CHECKS)
    assert [o["check"] for o in payload["outcomes"]] == list(CC.CHECKS)


def test_the_check_set_is_exactly_the_ratified_one():
    """The tuple is what was AGREED. Its sibling below proves the tuple is
    what a run EMITS, and the pair is what makes a silent rename fail: either
    alone lets a coordinated edit through."""
    assert CC.CHECKS == RATIFIED_CHECKS


def test_every_declared_check_actually_runs():
    """`CHECKS` is a promise and this is the thing that keeps it.

    A check named in the tuple and never emitted would read as coverage this
    corpus does not have; one emitted and not named would escape the closure.
    """
    outcomes = _outcomes(neutral_reader)
    assert [o.check for o in outcomes] == list(CC.CHECKS)


def test_ten_positives_and_seven_negative_confirmations():
    """The floor's own phrase is "positives plus negative confirmations", and
    the split is asserted so that a corpus which quietly lost its teeth — every
    negative deleted, every positive kept — fails here rather than passing
    everywhere."""
    negatives = [c for c in CC.CHECKS
                 if c.endswith("-refuses") or c.startswith("write-back-")]
    assert len(negatives) == 7, negatives
    assert len(CC.CHECKS) - len(negatives) == 10


# ==========================================================================
# 3. the teeth — each mutation fails the check that exists to catch it
# ==========================================================================


class _Wrapped:
    """Delegates everything to a real reader; a subclass breaks ONE thing.

    Composition and not a hand-written stub, because a stub that implemented
    the interface from scratch would fail the corpus for a hundred reasons and
    prove nothing about the one check under test.

    THE SIX METHODS ARE SPELLED OUT RATHER THAN FORWARDED BY `__getattr__`,
    and finding out why is worth recording for whoever writes a reader next.
    Since CPython 3.12 a `runtime_checkable` protocol's `isinstance` reads
    attributes with `inspect.getattr_static`, deliberately, so that the check
    cannot be satisfied by a descriptor or a `__getattr__` that fabricates
    names on demand. A delegating wrapper therefore does NOT satisfy
    `CorpusAdapter` however faithfully it forwards — measured here: the
    forwarding version failed `structural-conformance` and nothing else. The
    corpus was right and the wrapper was wrong, which is the outcome a
    mutation harness is supposed to have.
    """

    def __init__(self, name: str, location: str) -> None:
        self._inner = neutral_reader(name, location)

    def resolve(self, ref):
        return self._inner.resolve(ref)

    def list_documents(self, corpus, scope=CC.SCOPE_ALL):
        return self._inner.list_documents(corpus, scope)

    def read(self, corpus, document, revision=None):
        return self._inner.read(corpus, document, revision)

    def classify(self, corpus, document):
        return self._inner.classify(corpus, document)

    def check(self, corpus, subjects=None):
        return self._inner.check(corpus, subjects)

    def write_back(self, corpus, document, content, *, actor,
                   basis_revision, reason=""):
        return self._inner.write_back(corpus, document, content, actor=actor,
                                      basis_revision=basis_revision,
                                      reason=reason)


class EmptyOnAbsent(_Wrapped):
    """The degradation the seam's second requirement is written against: an
    absent corpus answered with a resolution and an empty listing."""

    def resolve(self, ref):
        try:
            return self._inner.resolve(ref)
        except Exception:  # noqa: BLE001
            return self._inner.resolve(
                replace(ref, location=str(CORPUS / "empty")))


class WideningScope(_Wrapped):
    """A scope nobody declared, quietly served as everything."""

    def list_documents(self, corpus, scope=CC.SCOPE_ALL):
        return self._inner.list_documents(corpus, CC.SCOPE_ALL)


class FallbackRevision(_Wrapped):
    """A revision this reader cannot serve, silently answered with one it
    can — bytes that answer a question nobody asked."""

    def read(self, corpus, document, revision=None):
        return self._inner.read(corpus, document, None)


class OmitsUnrecognizable(_Wrapped):
    """The other half of "REPORTED, not omitted": the document this reader
    cannot classify simply does not appear."""

    def list_documents(self, corpus, scope=CC.SCOPE_ALL):
        listed = self._inner.list_documents(corpus, scope)
        return tuple(d for d in listed
                     if self._inner.classify(corpus, d).kind is not None)


class TreeWriting(_Wrapped):
    """A write-back that writes the corpus tree — refused "even where the
    bytes would be identical", and here they are not even that."""

    def write_back(self, corpus, document, content, *, actor,
                   basis_revision, reason=""):
        (Path(corpus.location) / "notes" / "written-by-the-reader").write_bytes(
            content)
        from corpus_adapter import WriteReceipt
        return WriteReceipt(correlation_id="invented", dispatched_to="itself")


class _ForeignRefused(Exception):
    """A destination's OWN refusal class: same shape, different object."""

    def __init__(self, refusal) -> None:
        self.refusal = refusal
        super().__init__(refusal.kind)


class ForeignRefusal(_Wrapped):
    """Conformant, and it raises a class this repository has never seen."""

    def resolve(self, ref):
        try:
            return self._inner.resolve(ref)
        except Exception as exc:  # noqa: BLE001
            refusal = getattr(exc, "refusal", None)
            if refusal is None:
                raise
            raise _ForeignRefused(
                Refusal(kind=refusal.kind, subject=refusal.subject,
                        detail=refusal.detail)) from None

    def write_back(self, corpus, document, content, *, actor,
                   basis_revision, reason=""):
        raise _ForeignRefused(
            Refusal(kind=CORPUS_READ_ONLY, subject=corpus.ref.name,
                    detail="this corpus declares no governed write path"))


@pytest.mark.parametrize("reader,expected", [
    (EmptyOnAbsent, "absent-refuses"),
    (WideningScope, "unknown-scope-refuses"),
    (FallbackRevision, "unknown-revision-refuses"),
    (OmitsUnrecognizable, "classify-reports-unrecognizable"),
])
def test_a_non_conformant_reader_fails_the_check_that_exists_to_catch_it(
        reader, expected):
    failed = _failed(reader)
    assert expected in failed, (
        f"{reader.__name__} passed {expected!r}; that check is what stands "
        f"between this corpus and a reader that looks right and is not. "
        f"It failed only: {sorted(failed)}")


def test_a_reader_that_writes_the_tree_is_caught_twice(tmp_path):
    """Over a COPY, because this mutation genuinely writes."""
    corpus = tmp_path / "fixtures"
    shutil.copytree(CORPUS, corpus)
    failed = _failed(TreeWriting, corpus)
    assert "write-back-refuses-read-only" in failed
    assert "write-back-leaves-the-tree" in failed, (
        "the tree moved and the corpus did not notice. The refusal check and "
        "the tree check are two checks on purpose: a reader can refuse and "
        "write anyway, and a reader can write and call it a receipt")
    assert (corpus / "neutral" / "notes" / "written-by-the-reader").exists(), \
        "the mutation did not actually write, so this case proved nothing"


def test_a_reader_raising_its_own_refusal_class_still_passes():
    """The cross-repository property, and the reason refusals are read
    structurally. Every carved destination holds its own copy of the interface
    module; an `isinstance` against this one would fail a conformant reader."""
    outcomes = _outcomes(ForeignRefusal)
    passed, total, failed = CC.verdict(outcomes)
    assert failed == (), (
        f"a reader raising its own refusal class was reported non-conformant "
        f"on {list(failed)}. That is Python module identity, not the corpus")
    assert passed == total == len(CC.CHECKS)


def test_the_structural_refusal_reader_is_genuinely_foreign():
    """Guards the guard: if `_ForeignRefused` were ever made a subclass of the
    interface's own exception, the case above would pass for the wrong
    reason."""
    from corpus_adapter import CorpusRefused
    assert not issubclass(_ForeignRefused, CorpusRefused)
    assert CC._refusal_of(
        _ForeignRefused(Refusal(CORPUS_ABSENT, "s", "d"))) == CORPUS_ABSENT


def test_a_reader_that_is_not_a_reader_fails_structural_conformance():
    """The cheapest mutation and the one most likely to arrive by accident."""
    failed = _failed(lambda name, location: object())
    assert "structural-conformance" in failed
    assert "resolve-populated" in failed


def test_a_reader_whose_corpus_does_not_resolve_reports_the_rest_as_unreached():
    """Not as passing. A run that could not resolve has measured nothing, and
    a corpus that reported sixteen greens over it would be worse than one that
    reported nothing at all."""
    class NeverResolves(_Wrapped):
        def resolve(self, ref):
            raise RuntimeError("no")

    outcomes = _outcomes(NeverResolves)
    assert [o.check for o in outcomes] == list(CC.CHECKS)
    assert all(not o.passed for o in outcomes
               if o.check != "structural-conformance")
    assert any("not reached" in o.detail for o in outcomes)


# ==========================================================================
# 4. the runner's own contract
# ==========================================================================


def test_the_refusal_vocabulary_is_exactly_the_ratified_one():
    assert MODULE.REFUSAL_CODES == RATIFIED_CODES


def test_a_code_outside_the_vocabulary_cannot_be_raised_at_all():
    """The vocabulary is ENFORCED and not merely declared.

    Copilot's finding on this pull request: `REFUSAL_CODES` was declared and
    never read, the same shape `verify-carve-arrival.py` and
    `validate-carve-manifest.py` both carry. Pinning the constant by a test
    catches a rename of the CONSTANT; it does not catch a raise site that
    invented a code the tuple never held. This runner takes the stronger
    guarantee at the one place every refusal passes through.
    """
    with pytest.raises(ValueError) as caught:
        MODULE.ConformanceRefusal("conformance-invented", "no such code")
    assert "ratified refusal codes" in str(caught.value)
    for code in RATIFIED_CODES:
        assert MODULE.ConformanceRefusal(code, "d").code == code


def test_every_refusal_code_appears_in_the_script_source():
    """A code declared and never raised is a promise the script does not
    keep."""
    source = SCRIPT.read_text(encoding="utf-8")
    for code in RATIFIED_CODES:
        assert source.count(f'"{code}"') >= 2, (
            f"{code} appears once — declared in the tuple and raised nowhere")


def test_the_seat_holding_pass_answers_before_any_destination_has_a_reader():
    """A BRANCH and never a `pytest.skip`: a skip reports as a green bar, and
    `pytest-suite.yml` pins the skip count exactly."""
    done = _run()
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("NO DESTINATION"), done.stdout
    assert "openxfactory" in done.stdout


def test_the_seat_holding_pass_lists_the_checks_as_json():
    done = _run("--json")
    assert done.returncode == 0
    payload = json.loads(done.stdout)
    assert payload["result"] == "no-destination"
    assert payload["checks"] == list(CC.CHECKS)
    assert "opendox_code" in payload["destinations"]
    assert "openxfactory" in payload["destinations"]


def test_a_destination_with_no_declared_reader_refuses_and_does_not_pass():
    """The measured state of three of the four carved legs, and the one
    refusal this file most needs to be sure of: silence must not read as a
    pass."""
    done = _run("--destination", "opendox_code", "--dest-root", str(REPO_ROOT))
    assert done.returncode == 2
    assert "conformance-adapter-undeclared" in done.stderr
    assert "OK " not in done.stdout


def test_a_misspelled_destination_refuses_rather_than_holding_the_seat():
    done = _run("--destination", "opendox_kode", "--dest-root", str(REPO_ROOT))
    assert done.returncode == 2
    assert "conformance-unreadable" in done.stderr


def test_a_reader_that_cannot_be_imported_names_the_roots_it_looked_in():
    done = _run("--destination", "openxfactory", "--dest-root", str(REPO_ROOT),
                "--adapter", "no_such_module:nope")
    assert done.returncode == 2
    assert "conformance-adapter-unresolvable" in done.stderr
    assert "Roots searched" in done.stderr


def test_an_adapter_without_a_colon_refuses():
    done = _run("--destination", "openxfactory", "--dest-root", str(REPO_ROOT),
                "--adapter", "home_factory")
    assert done.returncode == 2
    assert "conformance-adapter-unresolvable" in done.stderr


def test_a_factory_name_the_module_does_not_carry_lists_what_it_does():
    done = _run("--destination", "openxfactory", "--dest-root", str(REPO_ROOT),
                "--adapter", "home_factory:no_such_factory",
                "--sys-path", "tests/carve_conformance")
    assert done.returncode == 2
    assert "conformance-adapter-unresolvable" in done.stderr
    assert "neutral_reader" in done.stderr


def test_a_factory_that_is_not_callable_refuses(tmp_path):
    (tmp_path / "flat.py").write_text("NOT_CALLABLE = 3\n", encoding="utf-8")
    done = _run("--destination", "openxfactory", "--dest-root", str(tmp_path),
                "--adapter", "flat:NOT_CALLABLE")
    assert done.returncode == 2
    assert "conformance-adapter-unresolvable" in done.stderr


def test_a_missing_corpus_refuses_before_any_reader_is_blamed(tmp_path):
    done = _run(*HOME_INVOCATION, "--corpus", str(tmp_path / "nowhere"))
    assert done.returncode == 2
    assert "conformance-corpus-missing" in done.stderr


def test_a_partial_corpus_refuses_rather_than_running_fewer_checks(tmp_path):
    corpus = tmp_path / "fixtures"
    shutil.copytree(CORPUS, corpus)
    shutil.rmtree(corpus / "empty")
    done = _run(*HOME_INVOCATION, "--corpus", str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-missing" in done.stderr


def test_a_failing_reader_refuses_with_the_check_named(tmp_path):
    """End to end through the command line: the runner has to turn a failed
    check into an exit-2 refusal that NAMES it, or an operator reading a red
    run learns nothing they can act on."""
    (tmp_path / "broken.py").write_text(
        "def factory(name, location):\n    return object()\n",
        encoding="utf-8")
    done = _run("--destination", "openxfactory", "--dest-root", str(tmp_path),
                "--adapter", "broken:factory")
    assert done.returncode == 2
    assert "conformance-check-failed" in done.stderr
    assert "structural-conformance" in done.stderr


def test_the_exit_status_is_only_ever_zero_or_two():
    """Enforced at the one place that owns it, so the contract does not rest
    on a reader auditing every raise site."""
    for args in ((), HOME_INVOCATION,
                 ("--destination", "opendox_code", "--dest-root",
                  str(REPO_ROOT)),
                 ("--destination", "openxfactory", "--dest-root", "/dev/null"),
                 ("--destination", "openxfactory", "--dest-root",
                  str(REPO_ROOT), "--adapter", "home_factory")):
        done = _run(*args)
        assert done.returncode in (0, 2), (
            f"{args} exited {done.returncode}; this runner has no exit 1")


def test_an_unexpected_failure_arrives_as_a_named_refusal_not_a_traceback(
        tmp_path):
    (tmp_path / "explode.py").write_text(
        "def factory(name, location):\n    raise MemoryError('boom')\n",
        encoding="utf-8")
    done = _run("--destination", "openxfactory", "--dest-root", str(tmp_path),
                "--adapter", "explode:factory")
    assert done.returncode == 2
    assert "conformance-unreadable" in done.stderr
    assert "Traceback" not in done.stderr


def test_an_import_root_is_not_left_on_the_path_for_the_next_destination():
    """Two destinations in one session must not be able to import each
    other's modules. That would be the privileged route arriving by accident,
    which is the one failure mode this whole corpus exists to detect."""
    before = list(sys.path)
    with pytest.raises(MODULE.ConformanceRefusal):
        MODULE.resolve_factory("no_such_module:nope", REPO_ROOT, [])
    assert sys.path == before
    MODULE.resolve_factory("home_factory:neutral_reader", REPO_ROOT,
                           ["tests/carve_conformance"])
    assert sys.path == before


def test_a_second_destinations_module_is_not_reused_from_sys_modules(
        tmp_path):
    """`sys.path` is not the only cache a second destination can inherit
    from the first in one session. `importlib.import_module` also caches by
    NAME in `sys.modules`, and restoring `sys.path` alone does not undo
    that. The plausible case is exact rather than contrived:
    `home_factory.py` is documented as "the worked example a destination
    copies", and a destination that copies the file keeps its module name
    too — so two destinations resolved in one process, each declaring
    `--adapter home_factory:neutral_reader`, are exactly the collision this
    test builds by hand.

    Two directories here each declare a DIFFERENT `home_factory.py`. The
    second resolution must read the SECOND destination's bytes; if it
    instead returns the first destination's already-imported module object,
    a destination under test would silently be measured against some other
    destination's reader.
    """
    before = sys.modules.get("home_factory")
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "home_factory.py").write_text(
        "def neutral_reader(name, location):\n    return 'first'\n",
        encoding="utf-8")
    (second / "home_factory.py").write_text(
        "def neutral_reader(name, location):\n    return 'second'\n",
        encoding="utf-8")
    factory_one = MODULE.resolve_factory("home_factory:neutral_reader",
                                         first, [])
    assert factory_one("irrelevant", "irrelevant") == "first"
    factory_two = MODULE.resolve_factory("home_factory:neutral_reader",
                                         second, [])
    assert factory_two("irrelevant", "irrelevant") == "second", (
        "the second destination's resolve_factory call returned the FIRST "
        "destination's cached module — sys.modules leaked across the "
        "session the same way an unrestored sys.path would have")
    assert sys.modules.get("home_factory") is before, (
        "a resolve_factory call must leave sys.modules exactly as it found "
        "it, the same restraint already held for sys.path")


def test_a_dotted_adapters_parent_package_is_not_reused_either(tmp_path):
    """Eviction by name alone is not enough for a DOTTED `--adapter`: a
    Copilot follow-up on this same fix named the gap precisely. Importing
    `pkg.reader` caches `pkg` in `sys.modules` on the way, and evicting only
    `module_name` and its submodules leaves that PARENT untouched — a second
    destination also declaring `pkg.reader` would then import against the
    FIRST destination's already-cached `pkg` package (whose `__path__` still
    points at the first destination's tree) rather than resolving `pkg`
    fresh off the second destination's roots. Two directories here each
    declare their own `pkg/__init__.py` and `pkg/reader.py`, so the failure
    mode this reproduces is the leaf test above one level up the chain.
    """
    first = tmp_path / "first"
    second = tmp_path / "second"
    for root, tag in ((first, "first"), (second, "second")):
        pkg = root / "pkg"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        (pkg / "reader.py").write_text(
            f"def factory(name, location):\n    return {tag!r}\n",
            encoding="utf-8")
    before_pkg = sys.modules.get("pkg")
    before_reader = sys.modules.get("pkg.reader")

    factory_one = MODULE.resolve_factory("pkg.reader:factory", first, [])
    assert factory_one("irrelevant", "irrelevant") == "first"
    factory_two = MODULE.resolve_factory("pkg.reader:factory", second, [])
    assert factory_two("irrelevant", "irrelevant") == "second", (
        "the second destination's resolve_factory call imported against "
        "the FIRST destination's cached PARENT PACKAGE — evicting the leaf "
        "module alone does not undo that")

    assert sys.modules.get("pkg") is before_pkg
    assert sys.modules.get("pkg.reader") is before_reader


# ==========================================================================
# 5. a TRANSPOSED corpus is proven faithful, never trusted — RULED Q-F1 (a)
#    (Brett Heap, 2026-09-17, openxFactory #656 comment 5714365086)
# ==========================================================================


def _transposed(tmp_path: Path, fixtures: Path | None = None) -> Path:
    """A genuine bare-repository transposition of the corpus.

    `git_history_factory.transpose()` is the thing under test as much as the
    runner is: it is what a destination whose corpus is history has to do in
    order to be measured at all, and every case below runs through it rather
    than around it.
    """
    return GH.transpose(fixtures or CORPUS, tmp_path / "transposed")


def _mutated_fixtures(tmp_path: Path) -> Path:
    """A writable copy of the shipped corpus, so a mutation can be made to a
    transposition's SOURCE without ever touching the fixtures themselves."""
    source = tmp_path / "source"
    shutil.copytree(CORPUS, source)
    return source


def test_a_git_transposition_passes_fidelity_and_the_whole_corpus(tmp_path):
    """RULED Q-F1 (a), end to end and through the documented command line.

    The reader here has NO working tree: every byte it serves comes out of a
    bare repository's history through `cat-file`. That is the case the ruling
    was written for, and the run has to reach all seventeen checks — a
    fidelity proof that passed and then measured nothing would be the floor
    ticked by a gate that never fired.
    """
    corpus = _transposed(tmp_path)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus))
    assert done.returncode == 0, f"{done.stdout}\n{done.stderr}"
    assert "TRANSPOSED and FAITHFUL" in done.stdout, done.stdout
    assert f"{CC.SEED_EXPECTATION.documents} document(s)" in done.stdout
    assert f"17 of {len(CC.CHECKS)} check(s)" in done.stdout, done.stdout


def test_the_transposition_is_history_and_not_a_working_tree(tmp_path):
    """Guards the guard. If `transpose()` ever copied files beside the
    repository, the case above would pass while proving nothing about a
    reader whose corpus is history — which is the whole of what it is for."""
    corpus = _transposed(tmp_path)
    populated = corpus / MODULE.POPULATED
    assert (populated / "HEAD").is_file(), "not a repository at all"
    for key in ("notes/alpha.md", "notes/beta.md", "papers/gamma.md"):
        assert not (populated / key).exists(), (
            f"{key} is a FILE in the transposition; a bare repository has no "
            "working tree and this reader would not have to read history")
    # and the bytes really are reachable, only through git
    reader = GH.reader("populated", str(populated))
    resolved = reader.resolve(CorpusRef(name="populated",
                                        location=str(populated)))
    keys = [d.key for d in reader.list_documents(resolved)]
    assert keys == ["notes/alpha.md", "notes/beta.md", "papers/gamma.md"]
    assert (CORPUS / MODULE.POPULATED / "notes" / "alpha.md").read_bytes() == \
        reader.read(resolved, reader.list_documents(resolved)[0]).content


def test_the_transpositions_digest_is_the_shipped_corpus_table(tmp_path):
    """The value the verdict carries is not decorative: an operator pasting
    that line into a pull request must be able to recompute it from the
    fixtures, and the two must be the same number."""
    corpus = _transposed(tmp_path)
    expected = MODULE.fingerprint_digest(
        MODULE.document_fingerprint(CORPUS / MODULE.POPULATED))
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus), "--json")
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    record = payload["transposition"]
    assert record is not None
    assert record["path"] == str(corpus)
    assert record["shipped"] == str(CORPUS)
    assert record["documents"] == 3
    assert record["proven"] is True
    assert record["digest"] == expected
    # the revision it was PROVEN at rides in the evidence, and a git
    # transposition has one: the bare repository's own HEAD.
    assert record["revision"] == GH._git(
        "rev-parse", "HEAD", cwd=corpus / MODULE.POPULATED
    ).stdout.decode().strip()
    assert record["revision_confirmed"] is True, (
        "the run never re-proved the corpus after the seventeen checks")
    assert record["served_digest"] == expected, (
        "the reader served a different table from the one the corpus holds, "
        "and the run still passed")


def test_the_reference_table_is_read_off_the_files_and_keyed_by_posix_path():
    """The reference side has no reader in it, and the key spelling is
    load-bearing: it is what a transposition's keys are compared WITH."""
    table = MODULE.document_fingerprint(CORPUS / MODULE.POPULATED)
    assert sorted(table) == ["notes/alpha.md", "notes/beta.md",
                             "papers/gamma.md"]
    for key, digest in table.items():
        import hashlib
        assert digest == hashlib.sha256(
            (CORPUS / MODULE.POPULATED / key).read_bytes()).hexdigest()


def test_the_table_digest_depends_on_the_pairing_and_not_on_the_order():
    """Two properties at once, and each has a way of being wrong. A digest
    that moved with dict order would make the verdict's value unusable as
    evidence; one that ignored WHICH key carried WHICH content would report
    two different corpora as the same one."""
    a = {"notes/alpha.md": "aa", "papers/gamma.md": "bb"}
    assert MODULE.fingerprint_digest(a) == MODULE.fingerprint_digest(
        {"papers/gamma.md": "bb", "notes/alpha.md": "aa"})
    swapped = {"notes/alpha.md": "bb", "papers/gamma.md": "aa"}
    assert MODULE.fingerprint_digest(a) != MODULE.fingerprint_digest(swapped)
    # and the separator between a key and its digest carries its weight: drop
    # it and a key that ENDS where the next value BEGINS produces the same
    # byte stream as a shorter key with a longer value, so two different
    # corpora would be reported under one number.
    assert MODULE.fingerprint_digest({"ab": "c" * 64}) != \
        MODULE.fingerprint_digest({"a": "b" + "c" * 64})


def test_a_transposition_with_one_byte_changed_refuses_and_names_the_key(
        tmp_path):
    """The mutation the whole proof exists for, and the one a destination
    could make by accident: the same three documents, one byte different."""
    source = _mutated_fixtures(tmp_path)
    document = source / MODULE.POPULATED / "notes" / "alpha.md"
    document.write_bytes(document.read_bytes() + b"x")
    corpus = _transposed(tmp_path, source)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-unfaithful" in done.stderr
    assert "notes/alpha.md" in done.stderr
    assert "bytes differ" in done.stderr


def test_a_transposition_that_dropped_a_document_refuses_and_names_it(
        tmp_path):
    source = _mutated_fixtures(tmp_path)
    (source / MODULE.POPULATED / "papers" / "gamma.md").unlink()
    corpus = _transposed(tmp_path, source)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-unfaithful" in done.stderr
    assert "papers/gamma.md" in done.stderr
    assert "does not serve" in done.stderr
    assert "list-population" not in done.stderr, (
        "a dropped document was reported as the READER listing too few. It "
        "is the CORPUS that is wrong, and blaming the reader for it is how a "
        "destination ends up editing a conformant reader to match a broken "
        "transposition")


def test_a_transposition_that_added_a_document_refuses_and_names_it(tmp_path):
    source = _mutated_fixtures(tmp_path)
    (source / MODULE.POPULATED / "notes" / "delta.md").write_text(
        "Type: note\nTitle: Delta\n\n# Delta\n", encoding="utf-8")
    corpus = _transposed(tmp_path, source)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-unfaithful" in done.stderr
    assert "notes/delta.md" in done.stderr
    assert "does not hold" in done.stderr


def test_the_fidelity_proof_runs_BEFORE_the_seventeen(tmp_path):
    """The order is the claim, so it is measured rather than asserted in
    prose. This transposition is wrong in a way that ALSO fails a check —
    the header line that carries `alpha.md`'s kind is gone, so the corpus's
    1/1/1 classification shape becomes 0/1/2 — and the refusal that comes
    back must be about the CORPUS. A run that named `classify-population`
    would have measured a reader against a corpus nobody compared, which is
    the exact reading RULED Q-F1 (a) cannot afford.
    """
    source = _mutated_fixtures(tmp_path)
    document = source / MODULE.POPULATED / "notes" / "alpha.md"
    document.write_bytes(document.read_bytes().replace(b"Type: note\n", b""))
    corpus = _transposed(tmp_path, source)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-unfaithful" in done.stderr
    assert "conformance-check-failed" not in done.stderr
    assert "classify-population" not in done.stderr


def test_the_default_run_is_not_called_a_transposition():
    """The shipped corpus compared with itself proves nothing and is not
    claimed: the default path is byte-for-byte the behaviour it had."""
    done = _run(*HOME_INVOCATION, "--json")
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["transposition"] is None
    human = _run(*HOME_INVOCATION)
    assert "TRANSPOSED" not in human.stdout, human.stdout


def test_the_shipped_corpus_named_explicitly_is_still_not_a_transposition():
    """`--corpus <the fixtures>` is the same corpus spelled out, and the
    proof keys off the RESOLVED path rather than off the flag being absent."""
    done = _run(*HOME_INVOCATION, "--corpus", str(CORPUS), "--json")
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["transposition"] is None


def test_a_copy_at_another_path_is_proven_rather_than_trusted(tmp_path):
    """Not every non-shipped corpus is a bare repository, and the proof is
    not about git: a plain COPY at another path is compared too, and passes
    for the same reason the transposition does — the same keys, the same
    bytes."""
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)
    done = _run(*HOME_INVOCATION, "--corpus", str(corpus), "--json")
    assert done.returncode == 0, done.stderr
    record = json.loads(done.stdout)["transposition"]
    assert record["proven"] is True and record["documents"] == 3


def test_a_document_the_reader_lists_and_will_not_serve_is_unfaithful(
        tmp_path):
    """A transposition can lie by omission as well as by content: a key in
    the listing whose bytes cannot be produced is a document the corpus does
    not carry, whatever the listing says. The seventeen would not catch this
    one — `read-round-trip` reads the FIRST document only."""
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)

    class WontServeTheLast(_Wrapped):
        def read(self, corpus_, document, revision=None):
            if document.key.endswith("gamma.md"):
                raise CorpusRefused(Refusal(
                    kind=DOCUMENT_UNKNOWN, subject=document.key,
                    detail="withheld by this test"))
            return self._inner.read(corpus_, document, revision)

    with pytest.raises(MODULE.ConformanceRefusal) as caught:
        MODULE.prove_transposition(
            WontServeTheLast, str(corpus / MODULE.POPULATED), corpus, CORPUS)
    assert caught.value.code == "conformance-corpus-unfaithful"
    assert "papers/gamma.md" in caught.value.detail
    assert "will not serve it" in caught.value.detail


def test_a_reader_that_cannot_resolve_is_handed_to_the_seventeen(tmp_path):
    """The one case the proof does NOT refuse, and the reason is reported
    rather than swallowed: where resolution or listing raises there is
    nothing to compare, and the seventeen checks say so far better than one
    line here could (`resolve-populated` failing, the rest not reached)."""
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)

    class NeverResolves(_Wrapped):
        def resolve(self, ref):
            raise RuntimeError("no")

    record = MODULE.prove_transposition(
        NeverResolves, str(corpus / MODULE.POPULATED), corpus, CORPUS)
    assert record["proven"] is False
    assert "RuntimeError" in record["reason"]
    assert record["digest"] == MODULE.fingerprint_digest(
        MODULE.document_fingerprint(CORPUS / MODULE.POPULATED))


def test_seventeen_green_over_an_unproven_transposition_still_refuses(
        tmp_path):
    """The last gate, and it is fail-closed on purpose.

    A factory whose FIRST construction raises and whose later ones do not
    leaves the proof unable to compare anything while the seventeen all
    pass — every ordinary reader fails a check in that state, so this is the
    one shape that could otherwise print `OK` over a corpus nobody proved
    faithful. It refuses instead, and the refusal says which corpus.
    """
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)
    (tmp_path / "flaky.py").write_text(
        "import home_factory\n"
        "_seen = []\n"
        "def factory(name, location):\n"
        "    _seen.append(name)\n"
        "    if len(_seen) == 1:\n"
        "        raise RuntimeError('the first construction fails')\n"
        "    return home_factory.neutral_reader(name, location)\n",
        encoding="utf-8")
    done = _run("--destination", "openxfactory", "--dest-root",
                str(tmp_path), "--adapter", "flaky:factory",
                "--sys-path", str(REPO_ROOT / "tests" / "carve_conformance"),
                "--corpus", str(corpus))
    assert done.returncode == 2
    assert "conformance-corpus-unfaithful" in done.stderr
    assert "seventeen checks passed" in done.stderr
    assert str(corpus) in done.stderr


def test_a_transposition_is_named_in_the_refusal_payload(tmp_path):
    """`--json` on a refusal has to say WHICH corpus was refused against, or
    a caller branching on the code has to parse the prose to find out."""
    source = _mutated_fixtures(tmp_path)
    (source / MODULE.POPULATED / "papers" / "gamma.md").unlink()
    corpus = _transposed(tmp_path, source)
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "git_history_factory:reader",
                "--sys-path", "tests/carve_conformance", "--corpus",
                str(corpus), "--json")
    assert done.returncode == 2
    payload = json.loads(done.stdout)
    assert payload["code"] == "conformance-corpus-unfaithful"
    assert payload["corpus"] == str(corpus)


def test_the_corpus_missing_refusal_admits_a_transposition_outside_a_checkout(
        tmp_path):
    """The sentence RULED Q-F1 (a) made wrong, and the reason it is a test.

    The refusal's CONDITION was always right — the directory is not there —
    but its prose told an operator to "point --corpus at a checkout that
    carries it", and a transposition lawfully lives in a temporary directory
    that is no checkout at all. An operator who reads that sentence and
    concludes the ruling is unimplementable has been told the wrong thing by
    a message nobody tested.
    """
    done = _run(*HOME_INVOCATION, "--corpus", str(tmp_path / "nowhere"))
    assert done.returncode == 2
    assert "conformance-corpus-missing" in done.stderr
    assert "TRANSPOSITION" in done.stderr
    assert "need not sit inside any checkout" in done.stderr


# ==========================================================================
# 6. Copilot's round-1 findings, each with the case that would have caught it
# ==========================================================================


def test_a_transposition_that_moves_UNDER_the_run_is_caught_afterwards(
        tmp_path):
    """Copilot round 1: the proof resolves and reads the corpus, and
    `carve_conformance.run` then resolves it again off the same path — so a
    corpus that moved between those two calls would have been measured at a
    revision nobody proved while the verdict said FAITHFUL. The window is
    closed by re-proving after the seventeen, which is the discipline
    `write-back-leaves-the-tree` already uses one level down.

    The transposition here is advanced to a DIFFERENT commit carrying the
    SAME three documents at the same bytes, so the content table is
    unchanged and only the revision comparison can catch it.
    """
    corpus = _transposed(tmp_path)
    populated = corpus / MODULE.POPULATED
    before = MODULE.prove_transposition(
        GH.reader, str(populated), corpus, CORPUS)
    assert before["proven"] is True and before["revision"]

    tree = GH._git("rev-parse", "HEAD^{tree}", cwd=populated
                   ).stdout.decode().strip()
    moved = GH._git("commit-tree", tree, "-p", before["revision"], "-m",
                    "an unrelated commit", cwd=populated
                    ).stdout.decode().strip()
    GH._git("update-ref", "refs/heads/main", moved, cwd=populated)
    assert moved != before["revision"]

    with pytest.raises(MODULE.ConformanceRefusal) as caught:
        MODULE.confirm_transposition_unmoved(
            GH.reader, str(populated), corpus, CORPUS, before)
    assert caught.value.code == "conformance-corpus-unfaithful"
    assert "moved UNDER the measurement" in caught.value.detail
    assert before["revision"] in caught.value.detail
    assert moved in caught.value.detail


def test_content_that_moves_under_a_corpus_with_no_revision_is_caught_too(
        tmp_path):
    """The other half, and the reason the re-proof is a whole PROOF rather
    than a revision comparison: a directory corpus reports `revision=None`
    (the interface permits it), so comparing revisions alone would be vacuous
    exactly where the bytes are easiest to change. Re-proving catches it and
    names the document, which no digest-to-digest line could."""
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)
    populated = corpus / MODULE.POPULATED
    before = MODULE.prove_transposition(
        neutral_reader, str(populated), corpus, CORPUS)
    assert before["proven"] is True and before["revision"] is None

    document = populated / "notes" / "alpha.md"
    document.write_bytes(document.read_bytes() + b"x")

    with pytest.raises(MODULE.ConformanceRefusal) as caught:
        MODULE.confirm_transposition_unmoved(
            neutral_reader, str(populated), corpus, CORPUS, before)
    assert caught.value.code == "conformance-corpus-unfaithful"
    assert "notes/alpha.md" in caught.value.detail
    assert "bytes differ" in caught.value.detail


def test_the_mismatch_reports_WHOLE_digests_and_not_prefixes(tmp_path):
    """Copilot round 1: a mismatch a reader cannot recompute from the failure
    output is a claim rather than a measurement, and twelve hex characters is
    not something anybody can check a sha256 against."""
    import hashlib
    corpus = tmp_path / "copy"
    shutil.copytree(CORPUS, corpus)
    document = corpus / MODULE.POPULATED / "notes" / "alpha.md"
    was = (CORPUS / MODULE.POPULATED / "notes" / "alpha.md").read_bytes()
    document.write_bytes(was + b"x")
    done = _run(*HOME_INVOCATION, "--corpus", str(corpus))
    assert done.returncode == 2
    assert hashlib.sha256(was).hexdigest() in done.stderr, (
        "the corpus's own digest was truncated")
    assert hashlib.sha256(was + b"x").hexdigest() in done.stderr, (
        "the served digest was truncated")


def test_every_refusal_payload_names_the_RESOLVED_corpus(tmp_path):
    """Copilot round 1: `args.corpus` is `null` on a default run and an
    uncanonicalized relative path when one was given, while a successful
    summary carries the resolved path — so a caller comparing the two would
    be comparing different spellings of one directory, or nothing at all."""
    # (a) the default run, where the flag is absent entirely
    done = _run("--destination", "openxfactory", "--dest-root",
                str(REPO_ROOT), "--adapter", "no_such_module:nope", "--json")
    assert done.returncode == 2
    assert json.loads(done.stdout)["corpus"] == str(CORPUS)
    # (b) a RELATIVE --corpus, which must arrive resolved
    relative = Path(tmp_path.name)   # never exists under REPO_ROOT
    done = _run(*HOME_INVOCATION, "--corpus", str(relative), "--json")
    assert done.returncode == 2
    payload = json.loads(done.stdout)
    assert payload["code"] == "conformance-corpus-missing"
    assert payload["corpus"] == str((REPO_ROOT / relative).resolve())
    assert payload["corpus"] != str(relative)


def test_the_transposition_fixture_ignores_an_ambient_git_pointer(
        tmp_path, monkeypatch):
    """Hermeticity, and it is the one environment dependence a file that
    WRITES COMMITS cannot afford: `GIT_DIR` would override every `cwd=` in
    the fixture and aim its plumbing at whatever repository the process was
    started in. Set one at a repository that must not move, and measure."""
    decoy = tmp_path / "decoy"
    GH._git("init", "--quiet", "--bare", "--initial-branch=main", str(decoy))
    before = sorted(p.name for p in decoy.rglob("*") if p.is_file())
    monkeypatch.setenv("GIT_DIR", str(decoy))
    monkeypatch.setenv("GIT_WORK_TREE", str(tmp_path))
    corpus = _transposed(tmp_path)
    record = MODULE.prove_transposition(
        GH.reader, str(corpus / MODULE.POPULATED), corpus, CORPUS)
    assert record["proven"] is True, record["reason"]
    assert sorted(p.name for p in decoy.rglob("*") if p.is_file()) == before, (
        "the transposition wrote into the repository GIT_DIR named")


# ==========================================================================
# 7. Copilot's round-2 findings
# ==========================================================================


def test_a_reader_that_serves_ANOTHER_revision_is_unfaithful(tmp_path):
    """Copilot round 2: the proof keyed only on the bytes, so a reader could
    resolve one revision and serve another — a working tree, an older commit
    — and still be recorded FAITHFUL. `CorpusAdapter.read`'s own contract is
    that `revision=None` means the revision the corpus was resolved at, and
    `Document.revision` reports which one it was; the seventeen checks never
    inspect that field, so this is the only place it is held."""
    corpus = _transposed(tmp_path)
    populated = corpus / MODULE.POPULATED

    class ServesAnotherRevision:
        def __init__(self, name, location):
            self._inner = GH.reader(name, location)

        def resolve(self, ref):
            return self._inner.resolve(ref)

        def list_documents(self, corpus_, scope=CC.SCOPE_ALL):
            return self._inner.list_documents(corpus_, scope)

        def read(self, corpus_, document, revision=None):
            got = self._inner.read(corpus_, document, revision)
            return Document(id=got.id, content=got.content,
                            revision="a-revision-nobody-asked-for")

    with pytest.raises(MODULE.ConformanceRefusal) as caught:
        MODULE.prove_transposition(
            ServesAnotherRevision, str(populated), corpus, CORPUS)
    assert caught.value.code == "conformance-corpus-unfaithful"
    assert "a-revision-nobody-asked-for" in caught.value.detail
    assert "notes/alpha.md" in caught.value.detail


def test_a_corpus_path_that_cannot_RESOLVE_refuses_rather_than_tracebacks(
        tmp_path):
    """Copilot round 2: hoisting the `--corpus` resolution above the catch-all
    `try` put a `Path.resolve()` `OSError` — a symlink loop is the exact case
    — outside the exit contract, where it would have arrived as a traceback
    and exit 1. This runner has no exit 1."""
    loop = tmp_path / "loop"
    loop.symlink_to(tmp_path / "loop2")
    (tmp_path / "loop2").symlink_to(loop)
    done = _run(*HOME_INVOCATION, "--corpus", str(loop), "--json")
    assert done.returncode == 2, done.stderr
    assert "Traceback" not in done.stderr
    payload = json.loads(done.stdout)
    assert payload["result"] == "refused"
    assert payload["code"] in MODULE.REFUSAL_CODES
    # nothing was resolvable, so the payload names what the operator typed
    assert payload["corpus"] == str(loop)


def test_the_fixture_reads_the_history_it_wrote_and_not_a_REPLACEMENT(
        tmp_path):
    """Copilot round 2: git plumbing honours replacement refs, so an ambient
    one could make `ls-tree` / `cat-file` serve objects OTHER than the ones
    the transposition wrote — the fixture would then prove a history it never
    laid down. Every git reader this repository owns passes
    `--no-replace-objects` for exactly this reason."""
    corpus = _transposed(tmp_path)
    populated = corpus / MODULE.POPULATED
    real = GH._git("rev-parse", "HEAD:notes/alpha.md", cwd=populated
                   ).stdout.decode().strip()
    impostor = GH._git("hash-object", "-w", "--stdin", cwd=populated,
                       stdin=b"Type: note\nTitle: Not alpha at all\n"
                       ).stdout.decode().strip()
    assert GH._git("replace", "-f", real, impostor, cwd=populated
                   ).returncode == 0

    # the replacement IS in force for a reader that does not disable it
    import subprocess as sp
    swapped = sp.run(["git", "-C", str(populated), "cat-file", "blob",
                      f"HEAD:notes/alpha.md"], capture_output=True,
                     check=False)
    assert b"Not alpha at all" in swapped.stdout, (
        "the replacement ref did not take, so this case proved nothing")

    record = MODULE.prove_transposition(
        GH.reader, str(populated), corpus, CORPUS)
    assert record["proven"] is True, record["reason"]
