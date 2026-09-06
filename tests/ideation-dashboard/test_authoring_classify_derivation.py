"""The create gate's header answer comes from `classify`, and it is the SAME answer.

`split-opendox-two-layer-product` § 2.3: "`authoring.py`'s
`REQUIRED_HEADER_FIELDS` — today co-authoritative with
`doc_health.corpus.STATUS_SCAN_LINES` — becomes a CLASSIFY response rather than
a constant." Design § D2 names the operation it becomes: "what KIND is this
document, and which fields does its kind require".

A migration like this has exactly two ways to go wrong, and there is a test here
for each.

  1. **It changes an answer.** The create gate refuses submissions; a field list
     that quietly grew refuses documents that were fine yesterday, and one that
     quietly shrank admits documents the corpus will report as broken later.
     `test_the_migrated_gate_answers_identically_over_the_whole_governed_corpus`
     measures the new answer against the frozen pre-migration one
     (`tests/header_contract_oracle.py`) over every document the corpus holds —
     not a sample, because the population is small enough to take whole and a
     sample is a claim about the part it did not read.

  2. **It does not actually migrate.** A constant left in place, or a constant
     copied under a new name, passes every parity above trivially. So two
     independent proofs of the DIRECTION: this module is parsed for an
     assignment that must not exist, and `classify` is made to answer
     differently — through the interface, with the real classifier over a
     different table — after which the gate must answer differently too. If the
     value were still authored here, that second test would go green while
     changing nothing, which is precisely what it exists to prevent.

WHY THE MUTATION IS A PERMANENT TEST AND NOT A ONE-OFF CHECK. A hand-run
mutation proves the parity had teeth on the day it was run. This repository has
already paid for the other kind — `align-status-reader-to-real-lines` records a
reviewer reverting two conversions at once with the whole suite still green —
so the control lives in the file and runs on every CI run.
"""

from __future__ import annotations

import ast
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

import header_contract_oracle as oracle
from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import corpus_adapter_openxfactory as adapter_package  # noqa: E402
from corpus_adapter import CorpusRef  # noqa: E402
from corpus_adapter_openxfactory import OpenxFactoryCorpusAdapter  # noqa: E402
from corpus_adapter_openxfactory.home import HOME_SHAPE  # noqa: E402
from doc_health import corpus  # noqa: E402
from ideation_dashboard import authoring  # noqa: E402

AUTHORING = REPO_ROOT / "scripts" / "ideation_dashboard" / "authoring.py"

#: A header block nothing in this repository declares, so an answer carrying it
#: can only have come from the table the mutation put there.
MUTANT_FIELDS: tuple[str, ...] = ("Provenance", "Custodian")

#: A body complete under the REAL contract and empty of both mutant fields —
#: the discriminating input: the true answer is `[]`, the mutant answer is both.
COMPLETE_BODY = (
    "# Complete — Brainstorm\n"
    "\n"
    "Status: brainstorm\n"
    "Kind: note\n"
    "Summary: a body complete under the contract this corpus declares\n"
    "Topics: parity\n"
    "Repository context: openxFactory\n"
    "Captured: 2026-09-06\n"
)


def _governed_documents() -> list[Path]:
    """Every document this corpus holds, both scopes, as repo-relative paths."""
    return sorted({*corpus.iter_doc_paths(REPO_ROOT),
                   *corpus.iter_lifecycle_paths(REPO_ROOT)})


# -- 1. the answer is unchanged ---------------------------------------------


def test_the_migrated_gate_answers_identically_over_the_whole_governed_corpus():
    """Byte-for-byte parity with the pre-§ 2.3 answer, over the whole tree.

    The gate is path-agnostic — it always asked what the ideation header block
    obliges, whatever the caller was about to write — so the oracle is a
    like-for-like comparison on any document text, and every governed document
    is a free real-world fixture: headers at line one, headers at the end of the
    window, headers absent, values empty, exotic separators, non-ASCII bodies.
    """
    documents = _governed_documents()
    assert len(documents) >= 500, (
        f"only {len(documents)} documents found under {REPO_ROOT} — the parity "
        "is not being measured over the real corpus; check the walk before "
        "trusting a green result")

    divergences = []
    for relative in documents:
        text = (REPO_ROOT / relative).read_text(encoding="utf-8",
                                                errors="replace")
        migrated = authoring.missing_required_headers(text)
        before = oracle.missing_required_headers(text)
        if migrated != before:
            divergences.append(f"{relative}: {before} -> {migrated}")

    assert divergences == [], (
        "asking `classify` changed the create gate's answer on real documents. "
        "§ 2.3 is a re-derivation of one contract, not a change to it — a "
        "field list that grew refuses captures that were lawful yesterday, and "
        "one that shrank admits documents the corpus will report as broken "
        f"later. Divergences: {divergences[:10]}")


def test_the_oracle_still_discriminates():
    """Non-vacuity for the parity above: the oracle must be able to disagree.

    A parity over a corpus where every document happens to answer `[]` would
    pass with either implementation, including a broken one. This asserts the
    population actually exercises both outcomes.
    """
    answers = [oracle.missing_required_headers(
        (REPO_ROOT / relative).read_text(encoding="utf-8", errors="replace"))
        for relative in _governed_documents()]
    assert any(answer == [] for answer in answers), (
        "no governed document is header-complete — the parity never exercises "
        "the passing case")
    assert any(answer for answer in answers), (
        "every governed document is header-complete — the parity never "
        "exercises the reporting case")


def test_the_gate_still_reports_the_fields_in_the_contract_order():
    """The order is part of the answer: the refusal message lists them."""
    assert authoring.missing_required_headers("# Bare\n") == list(oracle.FIELDS)


# -- 2. the value is derived, not authored ----------------------------------


def test_authoring_no_longer_assigns_the_field_block_anywhere():
    """Parsed, not grepped: the module still NAMES the constant in prose.

    Its docstrings record what the name used to be and why it is now an alias,
    and that documentation is how the migration stays reviewable. What must not
    exist is an ASSIGNMENT — a constant under the old name, or the same tuple
    under a new one, either of which would make every parity in this file a
    tautology.
    """
    tree = ast.parse(AUTHORING.read_text(encoding="utf-8"), filename=str(AUTHORING))
    assigned: list[str] = []
    literal_blocks: list[str] = []
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and target.id == "REQUIRED_HEADER_FIELDS":
                assigned.append(f"line {node.lineno}")
        value = getattr(node, "value", None)
        if isinstance(value, (ast.Tuple, ast.List)):
            names = {element.value for element in value.elts
                     if isinstance(element, ast.Constant)
                     and isinstance(element.value, str)}
            if set(oracle.FIELDS) <= names:
                literal_blocks.append(f"line {node.lineno}")

    assert assigned == [], (
        "`REQUIRED_HEADER_FIELDS` is assigned in authoring.py again "
        f"({assigned}) — § 2.3 makes it a `classify` response, and an "
        "assignment restores the constant the task removes")
    assert literal_blocks == [], (
        "the header block is written out as a literal in authoring.py "
        f"({literal_blocks}) — a constant under another name is the same "
        "co-authoritative constant")


def _mutant_home_corpus(location=None, *, verdict_groups=None):
    """`home_corpus`, over a corpus whose declared header block is different.

    The REAL adapter class and the REAL classifier, constructed from a shape
    whose required-field table says something else — so what this substitutes is
    the corpus's ANSWER, not the machinery that produces it. Anything the gate
    still gets right after this is something the gate is holding on its own.
    """
    shape = replace(HOME_SHAPE, required_fields_by_kind={None: MUTANT_FIELDS})
    path = Path(location) if location is not None else REPO_ROOT
    return (OpenxFactoryCorpusAdapter(shape),
            CorpusRef(name=path.name, location=str(path)))


def test_a_different_classify_answer_changes_the_gate(monkeypatch):
    """THE MUTATION CONTROL. Change the corpus's answer; the gate must follow.

    `COMPLETE_BODY` is header-complete under the real contract, so the true
    answer is `[]`. Under the mutant table the same body is missing both mutant
    fields. A gate still holding its own list answers `[]` here and fails.
    """
    assert authoring.missing_required_headers(COMPLETE_BODY) == [], (
        "the fixture must be header-complete under the REAL contract, or the "
        "mutation below proves nothing")

    monkeypatch.setattr(adapter_package, "home_corpus", _mutant_home_corpus)

    assert authoring.missing_required_headers(COMPLETE_BODY) == \
        list(MUTANT_FIELDS), (
        "the create gate did not follow the corpus's answer — it is still "
        "applying a field list of its own, which is the constant § 2.3 removes")
    assert authoring.required_header_fields() == MUTANT_FIELDS
    assert authoring.REQUIRED_HEADER_FIELDS == MUTANT_FIELDS, (
        "the compatibility alias must be the corpus's answer at the moment it "
        "is asked, not a value captured at import")


def test_the_alias_is_restored_once_the_mutation_is_lifted():
    """The mutation above is not sticky: nothing caches the answer.

    A cached first answer would make the alias a constant again, one call later
    than before, and would make the test above pass for the wrong reason.
    """
    assert authoring.REQUIRED_HEADER_FIELDS == oracle.FIELDS
    assert authoring.required_header_fields() == oracle.FIELDS


def test_the_alias_names_the_module_when_the_attribute_is_genuinely_absent():
    """PEP 562's other half: an unknown name still raises, and says which."""
    try:
        authoring.NO_SUCH_CONSTANT
    except AttributeError as exc:
        assert "authoring" in str(exc) and "NO_SUCH_CONSTANT" in str(exc)
    else:                                        # pragma: no cover - a failure
        raise AssertionError("a missing attribute must raise AttributeError")


# -- 3. the route is the interface's, not a private door --------------------


def test_the_gate_reaches_the_corpus_only_through_the_two_public_names():
    """`corpus-adapter-seam` requirement 4, at this module's own boundary.

    `tests/corpus-adapter/test_no_privileged_route.py` scans all of `scripts/`
    for this; the assertion is repeated HERE, on the one module § 2.3 makes a
    consumer, because this is the file where the shortcut would be written —
    `from corpus_adapter_openxfactory.classify import absent_fields` is one line
    shorter than the route this module takes and would answer the same question
    by a door the interface does not define.
    """
    tree = ast.parse(AUTHORING.read_text(encoding="utf-8"), filename=str(AUTHORING))
    bound = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and not node.level:
            if node.module.split(".")[0] in {"corpus_adapter_openxfactory",
                                             "scripts"}:
                bound.extend(alias.name for alias in node.names)
                assert node.module in {"corpus_adapter_openxfactory"}, (
                    f"line {node.lineno} imports {node.module!r} — the package's "
                    "submodules are not a route this consumer may take")
    assert bound == ["home_corpus"], (
        f"authoring.py binds {bound} out of the adapter package; the only name "
        "it needs is `home_corpus`")


def test_the_proposal_is_staged_where_the_header_contract_applies():
    """The staged key must sit under the tree the block governs.

    The gate is path-agnostic by design — it asks the same question whatever
    the caller is about to write — and it stays that way only because the
    proposal is presented at a key the contract covers. A key outside it would
    make `classify` correctly answer "no fields obliged here", and the gate
    would silently stop refusing anything.
    """
    assert authoring.PROPOSAL_KEY.startswith(authoring.IDEATION_PREFIX)
    assert authoring.PROPOSAL_KEY.endswith(".md")
    assert HOME_SHAPE.obliged_prefixes == (authoring.IDEATION_PREFIX,), (
        "the tree the corpus obliges the block over and the tree the create "
        "path writes into must be the same tree")


def test_the_gate_leaves_nothing_behind(tmp_path, monkeypatch):
    """A corpus of one is a THROWAWAY: no residue in the corpus, none in TMP."""
    monkeypatch.setenv("TMPDIR", str(tmp_path))
    monkeypatch.setattr("tempfile.tempdir", None, raising=False)
    assert tempfile.gettempdir() == str(tmp_path), (
        "the redirect did not take, so this test would pass over an empty "
        "directory it never wrote to")
    before = sorted(tmp_path.iterdir())
    authoring.missing_required_headers(COMPLETE_BODY)
    assert sorted(tmp_path.iterdir()) == before, (
        "the staged proposal outlived the question it was asked to answer")
