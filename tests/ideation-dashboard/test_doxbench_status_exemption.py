"""The `Status:`-exemption carve (`split-opendox-two-layer-product` § 2.4, OQ-1).

`doxbench_packet.py` used to do two jobs that belong on opposite sides of the
carve: it ASSEMBLES a bounded context packet (generic, and the primitive
openDox's own chat-turn route calls) and it READ this corpus's `Status:` header
against this corpus's lifecycle vocabulary through `doc_health.lines`
(openxFactory's, and only openxFactory's). The read now lives in
`doxbench_status_exemption.py`; everything else stayed.

FOUR THINGS THIS FILE PROVES, and they are deliberately different in kind:

  1. **NEUTRALITY.** The generic module names `doc_health` in no import
     statement at all, and the seam it does depend on sits at exactly ONE line
     — parsed out of the syntax tree, never grepped, for the reason
     `tests/import_scan.py` states at length.
  2. **CLOSURE.** All seven names the rail block exported are still reachable
     on `doxbench_packet`, they ARE the carved module's objects rather than
     copies, and the alias set cannot drift from what the carved module
     defines. This is what let every existing behavioural test stay unmodified.
  3. **PARITY.** The shipped reader answers what the PRE-SPLIT reader answered,
     over the fixture corpus, over real corpus documents, and — the check that
     matters most — over a whole assembled packet, compared as a source tuple
     and as rendered section bytes. The pre-split bodies are copied in verbatim
     below rather than described, the same idiom
     `test_mutation_reverting_lifecycle_status_alone_reproduces_the_divergence`
     uses to pin a defect it can no longer reach.
  4. **THE GUARDS TRAVELLED.** The wide ruling `align-status-reader-to-real-lines`
     is defended today by tests spelled `pk.lifecycle_status`. Those keep
     passing through the alias, but the alias is a bridge that goes away at the
     carve — so the agreement with `doc_health.corpus.parse_status`, including
     the synthetic exotic-separator fixture, is asserted HERE against the
     carved module directly, where it will still be true afterwards. Likewise
     the assembler's negative-space needle list is re-run over the new file, so
     splitting a module did not halve what that negative covers.

WHY THE READ DOES NOT GO THROUGH `classify()`, WHICH IS WHAT OQ-1 RECOMMENDED.
`corpus_adapter.Classification` carries kind, required fields, missing fields
and an unclassifiable reason — never a status VALUE — and RULING OQ-2
(2026-09-06, NO) bounds `classify` to exactly that. The rail needs the value,
and it runs over in-memory strings rather than documents a corpus holds. Both
gaps are reported to Brett rather than closed by widening a closed Protocol;
`test_the_carved_module_still_reaches_doc_health_directly` pins the shape that
was actually shipped, so a later ruling has something explicit to move.
"""

from __future__ import annotations

import ast
import dataclasses
import re
import sys

import pytest

from conftest import (  # noqa: F401  (sys.path side effect)
    NO_IMPLICIT_PUSH_MODULES,
    REPO_ROOT,
)

from import_scan import (  # noqa: E402
    imported_modules,
    names_a_forbidden_package,
)

from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_status_exemption as rail  # noqa: E402

# The fixture corpus and the packet-construction helpers are the ones the
# existing packet suite already uses. Imported rather than restated: a parity
# proof over a SECOND fixture corpus would prove parity over something no other
# test exercises.
from test_doxbench_packet import (  # noqa: E402
    _FORBIDDEN_MODULE_NEEDLES,
    DOC_A,
    DOC_B,
    DRAFT_TEXT,
    EVIDENCE_DRAFT,
    EVIDENCE_RATIFIED,
    FOREIGN_TEXT,
    OUTLINE,
    RATIFIED_TEXT,
    SCOPE,
    TURN,
    _boundary,
    _clock,
    _projection,
    _thread,
)

PACKET_MODULE = (REPO_ROOT / "scripts" / "ideation_dashboard"
                 / "doxbench_packet.py")
EXEMPTION_MODULE = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "doxbench_status_exemption.py")

#: Every name the pre-carve rail block defined. The packet module must still
#: answer all seven; the carved module must define all seven.
CARVED_NAMES: tuple[str, ...] = (
    "_STATUS_RE", "STATUS_SCAN_LINES", "EXEMPT_STATUSES", "_STATUS_DECORATORS",
    "lifecycle_status", "status_word", "is_compression_exempt",
)

#: Both spellings, always. `scripts/__init__.py` exists, so every package under
#: `scripts/` imports BOTH as a top-level name and as `scripts.<name>`, and a
#: one-spelling forbidden list is a hole — the reason
#: `tests/corpus-adapter/test_no_privileged_route.py:66-70` gives for its own.
FORBIDDEN_IN_THE_GENERIC_MODULE: tuple[str, ...] = (
    "doc_health", "scripts.doc_health",
    "corpus_adapter_openxfactory", "scripts.corpus_adapter_openxfactory",
)

SEAM_MODULE_NAME = "ideation_dashboard.doxbench_status_exemption"


# ===========================================================================
# 1 — NEUTRALITY: the generic module can travel
# ===========================================================================


def test_the_packet_module_imports_neither_the_checker_nor_the_home_adapter():
    """The property that makes `doxbench_packet.py` carveable at all.

    It is the packet-assembly primitive openDox's own chat-turn route calls, and
    openDox's tree has no `doc_health` and no `corpus_adapter_openxfactory` in
    it. An import of either here would make the module travel broken — which is
    exactly the fork `domain-descendant-boundary` forbids one level down, and
    the reason OQ-1 split the file rather than filing it whole."""
    offenders = [
        f"{PACKET_MODULE.name}:{line} imports {module!r}"
        for module, line in imported_modules(PACKET_MODULE)
        if names_a_forbidden_package(module, FORBIDDEN_IN_THE_GENERIC_MODULE)
    ]
    assert offenders == [], (
        "the generic packet module must import neither the repository's own "
        "document checker nor its own corpus adapter — both are openxFactory's "
        "and neither exists in openDox's tree. The `Status:` read that used to "
        "need one lives in `doxbench_status_exemption.py` now. Offending "
        f"imports: {offenders}")


def test_the_neutrality_scan_would_catch_the_imports_it_is_meant_to_catch(
        tmp_path):
    """The negative control, because the assertion above is a proof of ABSENCE.

    Five spellings, each one a thing somebody would plausibly write on the way
    to a quick fix — including the lazy function-local one, which
    `import_scan.imported_modules` reports exactly like a module-level import
    for the reason its own docstring gives."""
    doors = (
        "from doc_health.lines import split_keepends\n"
        "import doc_health\n"
        "from scripts.doc_health import corpus\n"
        "from corpus_adapter_openxfactory import home_corpus\n"
        "def lazy():\n"
        "    from doc_health.corpus import parse_status\n"
    )
    scratch = tmp_path / "would_be_offender.py"
    scratch.write_text(doors, encoding="utf-8")
    caught = [
        module for module, _line in imported_modules(scratch)
        if names_a_forbidden_package(module, FORBIDDEN_IN_THE_GENERIC_MODULE)
    ]
    assert len(caught) == 5, (
        f"the scan recognised {caught} — a real reintroduction of the checker "
        "dependency could slip past the assertion above")

    lawful = scratch.with_name("lawful.py")
    lawful.write_text("from ideation_dashboard.doxbench_hash import utf8_size\n",
                      encoding="utf-8")
    assert [
        module for module, _line in imported_modules(lawful)
        if names_a_forbidden_package(module, FORBIDDEN_IN_THE_GENERIC_MODULE)
    ] == [], "an in-package import must NOT be flagged"


def test_the_dependence_on_the_carved_rail_sits_at_exactly_one_line():
    """ONE readable point, which is the discipline `authoring._classify_proposal`
    states for its own function-local seam imports.

    Not a style preference: a module `__getattr__` that imported the rail
    itself, plus `exemption_rail` importing it again, would be two places to
    find and two places to change at the carve. `_status_exemption()` is the
    one, and everything else in the file goes through it."""
    seam_lines = [line for module, line in imported_modules(PACKET_MODULE)
                  if module == SEAM_MODULE_NAME]
    assert len(seam_lines) == 1, (
        f"expected exactly one import of {SEAM_MODULE_NAME!r} in "
        f"{PACKET_MODULE.name}; found it at lines {seam_lines}")


def test_the_carved_module_is_a_leaf_of_its_own_package():
    """It reads a header; it knows nothing about packets.

    The dependency runs one way — the assembler reaches the rail, never the
    reverse — so no import ordering between the two can become a cycle, and the
    rail can be lifted into the openxFactory-adapter column at § 3.1 without
    dragging the packet types along."""
    offenders = [
        f"{EXEMPTION_MODULE.name}:{line} imports {module!r}"
        for module, line in imported_modules(EXEMPTION_MODULE)
        if names_a_forbidden_package(
            module, ("ideation_dashboard", "scripts.ideation_dashboard"))
    ]
    assert offenders == [], (
        "the carved rail must not import back into the reader package: "
        f"{offenders}")


def test_the_carved_module_still_reaches_doc_health_directly():
    """OQ-1's RECOMMENDED route was `classify()`, and it does not exist.

    Pinned deliberately, and as a POSITIVE rather than an absence, so the gap
    the PR reports is a fact in the suite rather than a paragraph in a PR body.
    `Classification` carries no status value and RULING OQ-2 (2026-09-06, NO)
    bounds `classify` to kind and required fields, so routing this read through
    the adapter would mean widening a closed Protocol. When that is ruled on,
    this assertion is the thing that has to change, and it names what to
    change it to."""
    doc_health_lines = [line for module, line in imported_modules(EXEMPTION_MODULE)
                        if names_a_forbidden_package(
                            module, ("doc_health", "scripts.doc_health"))]
    assert len(doc_health_lines) == 1, (
        "the carved rail reads through the shared real-line primitive at "
        f"exactly one point; found {doc_health_lines}")

    from corpus_adapter import OPERATIONS, Classification
    assert "classify" in OPERATIONS
    fields = {field.name for field in dataclasses.fields(Classification)}
    assert "status" not in fields and "lifecycle_status" not in fields, (
        "a `Classification` that now carries a status VALUE is exactly the "
        "extension OQ-1 wanted and OQ-2 refused — if it has been ruled on, "
        "move this read onto it and delete this assertion rather than leaving "
        "both routes live")


# ===========================================================================
# 2 — CLOSURE: no caller and no existing test had to be edited
# ===========================================================================


@pytest.mark.parametrize("name", CARVED_NAMES)
def test_every_carved_name_still_answers_on_the_packet_module(name):
    """The alias is an ALIAS: the same object, not a second copy of it.

    Identity rather than equality on purpose. Two equal `frozenset`s would pass
    an equality check while being two places the exempt set lives, which is the
    co-authoritative-constant failure this repository repairs everywhere else."""
    assert getattr(pk, name) is getattr(rail, name)


def test_the_underscore_names_resolve_too():
    """`test_doxbench_packet.py`'s mutation check reads `pk._STATUS_RE`.

    A `__getattr__` guarded on `not name.startswith("_")` is the obvious
    shape and it would silently break the proof that the exotic-separator
    fixture pins the `align-status-reader-to-real-lines` defect — the test
    would error rather than fail, in a file nobody edited."""
    assert isinstance(pk._STATUS_RE, re.Pattern)
    assert pk._STATUS_DECORATORS == rail._STATUS_DECORATORS


def test_a_name_the_module_never_had_is_an_ordinary_attribute_error():
    with pytest.raises(AttributeError) as raised:
        pk.definitely_not_a_packet_name
    assert "doxbench_packet" in str(raised.value)
    assert "definitely_not_a_packet_name" in str(raised.value)


def test_the_alias_set_cannot_drift_from_what_the_carved_module_defines():
    """Both directions, because either drift is silent.

    A name added to the rail and not to the set would be unreachable through
    the module every caller uses; a name in the set the rail does not define
    would raise `AttributeError` from inside `__getattr__` at first access,
    which reads as "the packet module lost a name" rather than as the typo it
    would be."""
    declared = pk._STATUS_EXEMPTION_NAMES
    assert declared == frozenset(CARVED_NAMES)
    for name in declared:
        assert hasattr(rail, name), f"{name} is aliased but not defined"
    public = {name for name in vars(rail)
              if not name.startswith("__") and name not in {"annotations"}
              and getattr(vars(rail)[name], "__module__", rail.__name__)
              == rail.__name__}
    # `re` and `split_keepends` are imports, not the rail's own surface.
    public -= {"re", "split_keepends"}
    assert public <= declared, (
        f"the carved module defines {sorted(public - declared)}, which the "
        "packet module's alias set does not reach")


def test_the_packet_module_no_longer_defines_the_carved_names_itself():
    """Parsed, so the alias cannot quietly become a second copy.

    § 2.3's own derivation test does the same thing for
    `authoring.REQUIRED_HEADER_FIELDS`: keeping the NAME is only meaningful if
    the assignment is really gone."""
    tree = ast.parse(PACKET_MODULE.read_text(encoding="utf-8"),
                     filename=str(PACKET_MODULE))
    defined: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target,
                                                            ast.Name):
            defined.add(node.target.id)
    clashes = sorted(defined & set(CARVED_NAMES))
    assert clashes == [], (
        f"{PACKET_MODULE.name} defines {clashes} again — the carve is undone, "
        "and the two copies will drift the way every other pair of header "
        "readers in this corpus has")


def test_the_marking_mechanism_stayed_and_kept_its_signature():
    """`exemption_rail` is the generic half and it did NOT move.

    Marking a source with whatever status a reader reports is a thing any
    corpus's assembler does; only the READ is this corpus's. Its positional
    signature is asserted because `test_doxbench_memory_gateway.py` checks the
    realized rails-before-I/O claim by `getattr(pk, "exemption_rail")` and
    every caller passes `sources` positionally."""
    assert callable(pk.exemption_rail)
    assert not hasattr(rail, "exemption_rail")
    source = pk.PacketSource(ref=EVIDENCE_RATIFIED, kind=pk.SOURCE_EVIDENCE,
                             text=RATIFIED_TEXT, status=None,
                             compression_exempt=False)
    marked, = pk.exemption_rail((source,))
    assert marked.status == "ratified"
    assert marked.compression_exempt is True


def test_the_carved_module_is_inside_the_no_implicit_push_sweep():
    """§12 may widen §11's sweep, never narrow it — and splitting a swept
    module is a way of narrowing it that no assertion would have caught: both
    halves keep passing while half the code walked out of the negative."""
    assert "doxbench_status_exemption.py" in NO_IMPLICIT_PUSH_MODULES
    assert "doxbench_packet.py" in NO_IMPLICIT_PUSH_MODULES


@pytest.mark.parametrize("needle,label", _FORBIDDEN_MODULE_NEEDLES,
                         ids=[needle for needle, _ in _FORBIDDEN_MODULE_NEEDLES])
def test_the_carved_module_contains_no_forbidden_spelling(needle, label):
    """The assembler's own negative-space list, re-run over the new file.

    DERIVED, not copied: a hand-copied needle list is the co-authoritative
    constant this repository repairs everywhere else, and the copy that drifts
    is the one that stops catching things while still passing."""
    source = EXEMPTION_MODULE.read_text(encoding="utf-8")
    assert needle not in source, (
        f"{EXEMPTION_MODULE.name} must not contain {label}: {needle!r}")


def test_the_derived_needle_list_is_not_vacuous():
    assert len(_FORBIDDEN_MODULE_NEEDLES) >= 11, (
        "the needle list this file borrows has shrunk — check "
        "test_doxbench_packet.py before trusting the parametrized negative")


# ===========================================================================
# 3 — PARITY: the pre-split reader, copied verbatim, and compared
# ===========================================================================

# `origin/main`'s `doxbench_packet.py` lines 134-189, byte for byte, with only
# the names prefixed so the two can sit in one file. This is the ONLY honest
# way to prove a move changed nothing: the "before" has to still be runnable.
_PRE_SPLIT_STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$")
_PRE_SPLIT_STATUS_SCAN_LINES = 15
_PRE_SPLIT_EXEMPT_STATUSES = frozenset({"approved", "ratified", "standard"})
_PRE_SPLIT_STATUS_DECORATORS = "(·|,"


def _pre_split_lifecycle_status(text):
    from doc_health.lines import split_keepends
    if not isinstance(text, str):
        return None
    for body, _ending in split_keepends(text)[:_PRE_SPLIT_STATUS_SCAN_LINES]:
        match = _PRE_SPLIT_STATUS_RE.match(body)
        if match:
            return match.group(1)
    return None


def _pre_split_status_word(status):
    if status is None:
        return None
    value = status.strip().lower()
    for decorator in _PRE_SPLIT_STATUS_DECORATORS:
        value = value.split(decorator, 1)[0]
    parts = value.split()
    return parts[0] if parts else None


def _pre_split_is_compression_exempt(text):
    return _pre_split_status_word(
        _pre_split_lifecycle_status(text)) in _PRE_SPLIT_EXEMPT_STATUSES


PARITY_TEXTS: tuple[str, ...] = (
    RATIFIED_TEXT,
    DRAFT_TEXT,
    FOREIGN_TEXT,
    "Status: standard · promoted 2026-07-24\n\nbody\n",
    "Status: record · 2026-08-01T01:21Z (session of 2026-07-31)\n\nbody\n",
    "Status: record (in progress — accumulating)\n\nbody\n",
    "Status: brainstorm | staged\n\nbody\n",
    "Status: superseded by add-x\n\nbody\n",
    "Status: ratified (2026-08-01)\n\nbody\n",
    "Status:\n\nbody\n",
    "no header here\n",
    "",
    "# Doc\n\n" + "filler\n" * 40 + "Status: ratified\n",
    "Status: ratified\r\nKind: record\r\n\r\nCRLF body\r\n",
)


def test_the_four_constants_survived_the_move_unchanged():
    assert rail._STATUS_RE.pattern == _PRE_SPLIT_STATUS_RE.pattern
    assert rail.STATUS_SCAN_LINES == _PRE_SPLIT_STATUS_SCAN_LINES
    assert rail.EXEMPT_STATUSES == _PRE_SPLIT_EXEMPT_STATUSES
    assert rail._STATUS_DECORATORS == _PRE_SPLIT_STATUS_DECORATORS


@pytest.mark.parametrize("text", PARITY_TEXTS,
                         ids=[repr(t[:28]) for t in PARITY_TEXTS])
def test_the_carved_reader_answers_what_the_pre_split_reader_answered(text):
    assert rail.lifecycle_status(text) == _pre_split_lifecycle_status(text)
    assert (rail.is_compression_exempt(text)
            is _pre_split_is_compression_exempt(text))
    assert (rail.status_word(rail.lifecycle_status(text))
            == _pre_split_status_word(_pre_split_lifecycle_status(text)))


def test_a_non_string_is_still_not_a_status_rather_than_a_crash():
    for value in (None, 17, b"Status: ratified\n", ["Status: ratified"]):
        assert rail.lifecycle_status(value) is _pre_split_lifecycle_status(value)


def test_parity_holds_over_the_repositorys_own_documents():
    """The fixture texts are chosen; these are not. Same 80-document sample the
    existing agreement check reads, so the parity claim rests on the same
    evidence the drift check does."""
    checked = 0
    for path in sorted((REPO_ROOT / "docs").rglob("*.md"))[:80]:
        text = path.read_text(encoding="utf-8", errors="replace")
        assert rail.lifecycle_status(text) == _pre_split_lifecycle_status(text), path
        assert (rail.is_compression_exempt(text)
                is _pre_split_is_compression_exempt(text)), path
        checked += 1
    assert checked > 10, "the parity check needs real documents to be a check"


def _assembled_packet():
    threads = {key: _thread(key, turns=(TURN,)) for key in (DOC_A, DOC_B)}
    return pk.assemble_packet(
        projection=_projection(), scope=SCOPE, selected_key=DOC_A,
        loaded_keys=(DOC_A, DOC_B), query="packet assembler", threads=threads,
        knowledge=_boundary(), already_carried=(OUTLINE,), clock=_clock())


def test_a_whole_assembled_packet_is_identical_to_the_pre_split_assembly():
    """The parity proof that actually covers the shipped path.

    The packet is assembled through the real `assemble_packet`, then every
    source is RE-MARKED from its own text with the pre-split reader. Equal
    source tuples means the exemption rail placed exactly the same statuses and
    exemptions it did before the carve; equal section bytes means the rendering
    those markings drive — `EVIDENCE — <ref> [<status>] [<exemption>]` and the
    declaration block — is byte for byte what it was."""
    packet = _assembled_packet()
    assert packet.of_kind(pk.SOURCE_EVIDENCE), "the fixture must carry evidence"

    pre_split = dataclasses.replace(packet, sources=tuple(
        dataclasses.replace(
            source,
            status=_pre_split_lifecycle_status(source.text),
            compression_exempt=_pre_split_is_compression_exempt(source.text))
        for source in packet.sources))

    assert packet.sources == pre_split.sources
    assert pk.packet_sections(packet) == pk.packet_sections(pre_split)
    assert pk.declaration_text(packet) == pk.declaration_text(pre_split)

    # non-vacuity: the fixture really exercises both sides of the exemption
    marked = {source.ref: (source.status, source.compression_exempt)
              for source in packet.sources}
    assert marked[EVIDENCE_RATIFIED] == ("ratified", True)
    assert marked[EVIDENCE_DRAFT] == ("draft", False)


def test_the_parity_check_would_notice_a_reader_that_changed_its_answer():
    """The negative control for the packet-level parity above: a rail whose
    reader disagreed would produce a different source tuple AND different
    section bytes, so the assertion is not passing on shape alone."""
    packet = _assembled_packet()
    divergent = dataclasses.replace(packet, sources=tuple(
        dataclasses.replace(source, status="ratified", compression_exempt=True)
        for source in packet.sources))
    assert packet.sources != divergent.sources
    assert pk.packet_sections(packet) != pk.packet_sections(divergent)


# ===========================================================================
# 4 — THE GUARDS TRAVELLED: pointed at the carved module, not at the alias
# ===========================================================================


def test_the_carved_read_agrees_with_the_repositorys_own_corpus_reader():
    """`align-status-reader-to-real-lines`' agreement check, restated against
    the module that now performs the read.

    The existing one in `test_doxbench_packet.py` reaches it through the alias
    and is untouched. This one survives the alias's eventual removal, which is
    the point: a ratified wide ruling should not be defended only by a bridge
    that is scheduled to be demolished."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health.corpus import parse_status  # noqa: E402

    assert rail.STATUS_SCAN_LINES == 15
    checked = 0
    for path in sorted((REPO_ROOT / "docs").rglob("*.md"))[:80]:
        text = path.read_text(encoding="utf-8", errors="replace")
        assert rail.lifecycle_status(text) == parse_status(text), path
        checked += 1
    assert checked > 10, "the drift check needs real documents to be a check"


def test_the_carved_read_agrees_on_the_synthetic_exotic_separator_fixture():
    """The non-vacuous half, same fixture, same reason: this corpus carries no
    exotic line-boundary separator today, so the loop above alone would pass
    whether the two readers agreed on that input or not."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health.corpus import STATUS_SCAN_LINES, parse_status  # noqa: E402
    from doc_health.lines import split_keepends  # noqa: E402

    exotic = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(exotic * 2))
    text = f"# Doc\n\n{noise}tail\nStatus: staged\n"

    assert len(split_keepends(text)) <= STATUS_SCAN_LINES, \
        "fixture is broken: the real-line count must fit the window"
    assert len(text.splitlines()) > STATUS_SCAN_LINES, \
        "fixture is broken: the pseudo-line count must overrun the window"

    assert rail.lifecycle_status(text) == parse_status(text) == "staged"
    assert rail.lifecycle_status(text) == _pre_split_lifecycle_status(text)


def test_reverting_the_carved_reader_alone_still_reproduces_the_divergence():
    """The mutation check, moved onto the carved module. Reverting
    `lifecycle_status` to the pre-fix `str.splitlines()[:15]` idiom must still
    diverge from `corpus.parse_status` on that fixture — otherwise the fixture
    passes by accident and the carve quietly took the proof with it."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health.corpus import parse_status  # noqa: E402

    exotic = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(exotic * 2))
    text = f"# Doc\n\n{noise}tail\nStatus: staged\n"

    def _reverted(value):
        for line in value.splitlines()[:rail.STATUS_SCAN_LINES]:
            match = rail._STATUS_RE.match(line)
            if match:
                return match.group(1)
        return None

    assert rail.lifecycle_status(text) == parse_status(text) == "staged"
    assert _reverted(text) != parse_status(text), (
        "reverting the carved reader to splitlines() did not diverge from "
        "corpus.parse_status on this fixture — it is not pinned to the defect")
