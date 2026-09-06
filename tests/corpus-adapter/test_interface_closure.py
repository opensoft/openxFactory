"""The interface is CLOSED at six operations, and the home adapter offers no
seventh.

`corpus-adapter-seam`'s fourth requirement, second scenario: "WHEN an adapter
implementation over `openxFactory`'s corpus offers an operation the interface
does not declare, THEN the operation is either promoted into the interface for
every implementation or removed, and it is not kept as a local extension."
That is a statement about a SET, so it is testable as one — twice: once against
the Protocol's own membership, and once against the concrete class's public
surface, parsed rather than introspected so a method that fails to import is
still counted.

The pattern is `doxbench_model.WorkbenchModelPort`'s, whose docstring says why:
"Exactly three members -- nothing else -- so a ``__protocol_attrs__`` reader can
prove the surface never grew a second provider verb by accident."

`runtime_checkable` protocols with non-method members support `isinstance()` but
not `issubclass()`. All six members here are methods, so both work; the test
below pins that property rather than trusting it, because a `@property` added
later would silently take `issubclass` away from every consumer.
"""

from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

from corpus_adapter import OPERATIONS, DESIGN_NAMES, CorpusAdapter  # noqa: E402

PACKAGE = REPO_ROOT / "scripts" / "corpus_adapter_openxfactory"
ADAPTER_MODULE = PACKAGE / "adapter.py"
PACKAGE_INIT = PACKAGE / "__init__.py"
IMPLEMENTATION = "OpenxFactoryCorpusAdapter"

#: The signatures as landed. Pinned as TEXT because the seam's whole value is
#: that an implementation authored in another repository can conform without
#: importing anything from this one — which it can only do against a shape
#: somebody has written down. When openDox ratifies these for real, this is the
#: table the ratified text is compared with.
SIGNATURES = {
    "resolve": "(self, ref: 'CorpusRef') -> 'ResolvedCorpus'",
    "list_documents":
        "(self, corpus: 'ResolvedCorpus', scope: 'str' = 'all') "
        "-> 'tuple[DocumentId, ...]'",
    "read":
        "(self, corpus: 'ResolvedCorpus', document: 'DocumentId', "
        "revision: 'str | None' = None) -> 'Document'",
    "classify":
        "(self, corpus: 'ResolvedCorpus', document: 'DocumentId') "
        "-> 'Classification'",
    "check":
        "(self, corpus: 'ResolvedCorpus', "
        "subjects: 'tuple[DocumentId, ...] | None' = None) "
        "-> 'tuple[Finding, ...]'",
    "write_back":
        "(self, corpus: 'ResolvedCorpus', document: 'DocumentId', "
        "content: 'bytes', *, actor: 'str', basis_revision: 'str', "
        "reason: 'str' = '') -> 'WriteReceipt'",
}


def public_methods(source: str, class_name: str) -> set[str]:
    """Public method names declared on one class, from the syntax tree.

    Parsed rather than introspected so the answer does not depend on the module
    importing, and so a method added inside an `if TYPE_CHECKING:` or a
    conditional branch is counted exactly like any other. `__init__` is excluded
    — construction is not an operation the interface declares, and every
    implementation needs one.
    """
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for member in node.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and not member.name.startswith("_"):
                    found.add(member.name)
    return found


def test_the_protocol_declares_exactly_the_six_operations():
    assert len(OPERATIONS) == 6, (
        f"the interface is six operations wide (design D2: list, read, write "
        f"back, check, plus classify and resolve); OPERATIONS holds "
        f"{len(OPERATIONS)}")
    assert sorted(CorpusAdapter.__protocol_attrs__) == sorted(OPERATIONS), (
        "the Protocol's members and OPERATIONS have diverged — one of them was "
        "edited alone. Growing the surface is deliberately a two-file act: "
        f"protocol={sorted(CorpusAdapter.__protocol_attrs__)} "
        f"OPERATIONS={sorted(OPERATIONS)}")
    assert sorted(DESIGN_NAMES) == sorted(OPERATIONS), (
        "every operation carries its design-table name, so a reader of design "
        "D2's four-row table can find each row in code")


def test_every_member_is_a_method_so_isinstance_and_issubclass_both_work():
    for name in OPERATIONS:
        member = getattr(CorpusAdapter, name)
        assert callable(member) and not isinstance(member, property), (
            f"{name} is not a method. A `runtime_checkable` Protocol with a "
            "non-method member supports isinstance() but NOT issubclass(), so "
            "adding one silently removes a check every consumer may be making")


def test_the_signatures_are_the_ones_that_landed():
    """A change to an argument is a change to the standard openDox will ratify.

    It is allowed to happen — the in-tree interface is PROVISIONAL — but it is
    not allowed to happen quietly, because an implementation in another
    repository conforms to this text and to nothing else."""
    landed = {name: str(inspect.signature(getattr(CorpusAdapter, name)))
              for name in OPERATIONS}
    assert landed == SIGNATURES, (
        "the interface's signatures moved. If that is intended, move this table "
        "with them IN THE SAME DIFF and say so in the change that does it; a "
        "consumer outside this repository has nothing else to conform to. "
        f"landed={landed}")


def test_the_home_adapter_declares_no_seventh_operation():
    """Requirement 4, scenario 2, as a set comparison over parsed source."""
    declared = public_methods(ADAPTER_MODULE.read_text(encoding="utf-8"),
                              IMPLEMENTATION)
    assert declared == set(OPERATIONS), (
        f"{IMPLEMENTATION} must offer the interface's six operations and no "
        "others — an operation available only to the home corpus is the "
        "'local extension' the requirement forbids, and it is what turns the "
        "seam back into the repository it was extracted from wearing an "
        f"interface. extra={sorted(declared - set(OPERATIONS))} "
        f"missing={sorted(set(OPERATIONS) - declared)}")


def test_the_package_exports_exactly_two_public_names():
    """Everything else in the package is construction detail.

    A caller that reaches past these two is reaching for openxFactory's corpus
    by a route the interface does not define, which is scenario 1 of the same
    requirement — and `test_no_privileged_route.py` is the scan that catches it.
    """
    tree = ast.parse(PACKAGE_INIT.read_text(encoding="utf-8"))
    exported = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "__all__"
                for t in node.targets):
            exported = tuple(elt.value for elt in node.value.elts)
    assert exported == (IMPLEMENTATION, "home_corpus"), (
        f"the package's declared public surface is {exported!r}; it must be "
        f"exactly ({IMPLEMENTATION!r}, 'home_corpus')")


def test_the_scanner_would_catch_a_seventh_operation():
    """A negative control, because the assertion above is a proof of ABSENCE.

    If `public_methods` had a hole — a decorated method it skipped, a nested
    class it descended into by accident — the test above would be green over an
    adapter that HAD grown a private door, and nobody would know."""
    grown = (
        "class OpenxFactoryCorpusAdapter:\n"
        "    def __init__(self): ...\n"
        "    def resolve(self): ...\n"
        "    def promoted_specs(self):\n"
        "        'the home-only convenience the requirement forbids'\n"
        "    def _private(self): ...\n"
    )
    found = public_methods(grown, IMPLEMENTATION)
    assert found == {"resolve", "promoted_specs"}, (
        f"the scanner saw {sorted(found)}: it must count `promoted_specs`, "
        "must not count `__init__`, and must not count a private helper")
    assert found - set(OPERATIONS) == {"promoted_specs"}
