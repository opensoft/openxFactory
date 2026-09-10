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
    Refusal,
)
from home_factory import NEUTRAL_SHAPE, neutral_reader  # noqa: E402

# The vocabulary, restated as a LITERAL rather than imported. Asserting
# `MODULE.REFUSAL_CODES == MODULE.REFUSAL_CODES` would be a tautology; spelling
# it out is what makes a silent rename or reorder a test failure, because an
# operator's runbook and a caller's branch both read these strings.
RATIFIED_CODES = (
    "conformance-adapter-undeclared",
    "conformance-adapter-unresolvable",
    "conformance-corpus-missing",
    "conformance-check-failed",
    "conformance-unreadable",
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
    """"no `openspec/`, no `contracts/`" — read off the tree, not asserted."""
    offenders = [
        p.relative_to(CORPUS).as_posix()
        for p in CORPUS.rglob("*")
        if any(part in FORBIDDEN_PATH_PARTS for part in p.parts)]
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
