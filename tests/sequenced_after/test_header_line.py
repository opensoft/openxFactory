"""Feature `sequenced-after-header-line` (accept-sequenced-after-header-line):
the `sequenced_after:` LIFECYCLE HEADER LINE as a declaration equivalent to the
front-matter key.

Realizes this change's TWO ADDED `release-realization` requirements —
"Equivalent declaration sites for the ordered-delta parent declaration" and
"One parent declaration across both sites, and its retention" — on Brett Heap's
ruling of 2026-09-10 (verbatim "do door b") on codexFactory issue #268.

THE DELTA IS ALL-ADDED AND NOT A MODIFIED BLOCK, WHICH IS A CHECKED CONSTRAINT
RATHER THAN A PREFERENCE. The requirement this change extends
("Machine-readable ordered-delta parent declaration") belongs to
`add-sequenced-after-substrate`, which is RATIFIED and still ACTIVE — so its
requirements are NOT promoted in `openspec/specs/release-realization/spec.md`,
and a `## MODIFIED Requirements` block must target a PROMOTED requirement. The
relation is declared MECHANICALLY instead, by this change's own
`sequenced_after: [add-sequenced-after-substrate]` front matter.

THE MEASUREMENT THIS SUITE PROTECTS. codexFactory writes its lifecycle headers
UNFENCED — 49 of its 50 proposals — so eight `sequenced_after:` declarations its
authors wrote were invisible to a reader that parsed only inside a `---` fence,
and `corpus_sweep` reported `declaring=0` over a corpus with eight carriers.
The parent packet's claim that the field was machine-read was FALSE on
codexFactory main, and E-8 of `add-floor-regeneration-automation` (ratified
2026-09-06) named the two remedies it would not take: fence the whole corpus, or
correct the record. Door (b) is the third: teach the reader the header-line form,
so no proposal byte moves and no ratified chain position is disturbed.

THE WINDOW IS WHAT KEEPS THE REFUSAL FRONT MATTER WAS CHOSEN FOR. Beyond the
bounded lifecycle header window the same bytes are PROSE and declare nothing —
this capability's own text already refuses a mention as a parent link — so the
negative cases here (a body paragraph, an indented line, the legacy
`Sequenced-after:` prose header) are as load-bearing as the positive ones.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
LOADER_MODULE = ROOT / "scripts" / "frontmatter_strict.py"
SCOPE_MODULE = ROOT / "scripts" / "scope_globs.py"


def _load(path: Path, name: str):
    # Loaded under a name that is NOT `sequenced_after`: THIS DIRECTORY is a
    # package by that name (see `__init__.py`), and registering the script module
    # under the package's own name would replace the package in `sys.modules` and
    # abort collection of every sibling test module.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # dataclass field resolution needs this
    spec.loader.exec_module(module)
    return module


sa = _load(MODULE, "sequenced_after_substrate")
fms = _load(LOADER_MODULE, "frontmatter_strict")


def _unfenced(header: str, body: str = "\n## Why\n\nprose\n") -> str:
    """A proposal in codexFactory's shape: a title, then unfenced header lines."""
    return f"# Proposal: a-change\n\n{header}\n{body}"


def _fenced(front_matter: str, body: str = "\n# Proposal\n\nbody\n") -> str:
    return f"---\n{front_matter}\n---\n{body}"


# --- the header-line form DECLARES -------------------------------------------


def test_an_unfenced_header_line_declares_its_parents():
    raw = sa.read_declaration(_unfenced(
        "Status: ratified\n"
        "code_surface: codexFactory\n"
        "sequenced_after: [add-floor-addition-grace]"))
    assert raw == ["add-floor-addition-grace"]
    assert raw is not sa.ABSENT


def test_a_header_line_carries_a_multi_entry_flow_sequence():
    raw = sa.read_declaration(_unfenced(
        "Status: ratified\n"
        "sequenced_after: [add-regular-pr-council-clearance, "
        "add-floor-regeneration-automation]"))
    assert raw == ["add-regular-pr-council-clearance",
                   "add-floor-regeneration-automation"]


def test_a_header_line_root_claim_is_the_positive_empty_sequence():
    """`[]` is a ratification-covered ROOT CLAIM on this path too, and is still
    never equal to absence."""
    raw = sa.read_declaration(_unfenced("Status: draft\nsequenced_after: []"))
    assert raw == []
    assert raw is not sa.ABSENT
    assert sa._canonical(raw) != sa._canonical(sa.ABSENT)


def test_a_header_line_declaration_validates_and_resolves_like_the_fenced_form(
        tmp_path):
    """The whole point of door (b): the SAME grammar, resolution and cycle rules
    apply, so an unfenced corpus is validated rather than merely counted."""
    base = tmp_path / "openspec" / "changes"
    (base / "parent").mkdir(parents=True)
    (base / "parent" / "proposal.md").write_text(
        _unfenced("Status: ratified\nsequenced_after: []"), encoding="utf-8")
    (base / "child").mkdir(parents=True)
    (base / "child" / "proposal.md").write_text(
        _unfenced("Status: draft\nsequenced_after: [parent]"), encoding="utf-8")

    declaration = sa.validate_shape(sa.declaration_of(base / "child"))
    sa.validate_resolvable(tmp_path, declaration)
    sa.validate_acyclic(tmp_path, "child")
    # `chain_depth` counts HOPS: child -> parent is one, and the parent's `[]`
    # root claim is what terminates the walk rather than an absent field.
    assert sa.chain_depth(tmp_path, "child") == 1


def test_the_header_line_form_is_read_at_the_last_line_of_the_window():
    """The bound is inclusive: line `HEADER_WINDOW_LINES` is inside it."""
    window = fms.HEADER_WINDOW_LINES
    filler = "\n".join(f"Header{n}: value" for n in range(window - 1))
    text = f"{filler}\nsequenced_after: [parent]\n\nbody\n"
    assert text.splitlines()[window - 1] == "sequenced_after: [parent]"
    assert sa.read_declaration(text) == ["parent"]


# --- BEYOND THE WINDOW IT IS PROSE, AND PROSE DECLARES NOTHING ---------------


def test_the_first_line_beyond_the_window_does_not_declare():
    window = fms.HEADER_WINDOW_LINES
    filler = "\n".join(f"Header{n}: value" for n in range(window))
    text = f"{filler}\nsequenced_after: [parent]\n\nbody\n"
    assert text.splitlines()[window] == "sequenced_after: [parent]"
    assert sa.read_declaration(text) is sa.ABSENT


def test_a_body_paragraph_mentioning_the_field_declares_nothing():
    """Unbounded prose parsing is exactly what the front-matter rule protected
    against: a mention is not a parent link, and this capability's own text
    already says so."""
    text = _unfenced(
        "Status: ratified\ncode_surface: codexFactory",
        body="\n## Why\n\n" + "prose prose prose\n" * 20
             + "The vendored grammar reads\n"
             "sequenced_after: [add-transport-neutral-mcp-tool-contract]\n"
             "above, and the parent resolves.\n")
    assert "sequenced_after: [add-transport-neutral-mcp-tool-contract]" in text
    assert sa.read_declaration(text) is sa.ABSENT


def test_an_indented_field_line_is_not_a_header_line():
    """A header line sits at column 0. An indented line is a continuation of
    whatever precedes it, not a top-level declaration."""
    assert sa.read_declaration(_unfenced(
        "Status: ratified\n  sequenced_after: [parent]")) is sa.ABSENT


def test_the_legacy_prose_Sequenced_after_header_is_not_a_declaration():
    """`Sequenced-after:` is FREE TEXT NO SCHEMA VALIDATES — three archived
    openxFactory proposals carry it with prose after the ids. The admitted form
    is the FIELD'S OWN NAME, `sequenced_after:`, and the legacy header keeps the
    non-declaring standing the ratified requirement gave it."""
    text = _unfenced(
        "Status: ratified\n"
        "Sequenced-after: add-promotion-fidelity-check (both changes MODIFY "
        "`doc-health`'s \"Deterministic check families\")")
    assert sa.read_declaration(text) is sa.ABSENT
    assert sa.PROSE_HEADER.match(
        "Sequenced-after: add-promotion-fidelity-check (both changes MODIFY)")


# --- BOTH FORMS PRESENT ------------------------------------------------------


def test_both_forms_present_and_equal_are_one_declaration():
    raw = sa.read_declaration(_fenced(
        "code_surface: openxFactory\nsequenced_after: [parent]",
        body="\nsequenced_after: [parent]\n\nbody\n"))
    assert raw == ["parent"]


def test_both_sites_may_spell_one_reference_differently_and_still_agree():
    """The comparison is `_canonical`, the same one the retention gate uses, so a
    SELF-QUALIFIED entry and its bare form are ONE reference rather than a
    conflict. (An NFC-only difference is unreachable through this grammar: a
    change id is lower-kebab ASCII, so `parse_entry` refuses a non-ASCII entry
    before any normalization could matter — the equivalence that IS reachable is
    the repository qualifier's.)"""
    raw = sa.read_declaration(_fenced(
        f"sequenced_after: [{sa.DECLARING_REPOSITORY}:parent]",
        body="\nsequenced_after: [parent]\n\nbody\n"))
    assert raw == [f"{sa.DECLARING_REPOSITORY}:parent"]
    assert tuple(sa.validate_shape(raw).local_ids()) == ("parent",)


def test_entry_ORDER_is_significant_across_the_two_sites():
    """A frozen declaration is compared AS AUTHORED, so the same two parents in a
    different order are two different declarations and the conflict is refused."""
    with pytest.raises(sa.SequencedAfterError):
        sa.read_declaration(_fenced(
            "sequenced_after: [parent-one, parent-two]",
            body="\nsequenced_after: [parent-two, parent-one]\n\nbody\n"))


def test_both_forms_present_and_DIFFERENT_are_refused():
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.read_declaration(_fenced(
            "sequenced_after: [parent-one]",
            body="\nsequenced_after: [parent-two]\n\nbody\n"))
    message = str(excinfo.value)
    assert "declared TWICE" in message
    assert "parent-one" in message and "parent-two" in message


def test_a_root_claim_contradicted_by_a_header_line_is_refused():
    """The dangerous half of the conflict: `[]` in one site and a parent in the
    other. Preferring either site would let a change read as a root while its
    own document declares a parent."""
    with pytest.raises(sa.SequencedAfterError):
        sa.read_declaration(_fenced(
            "sequenced_after: []", body="\nsequenced_after: [parent]\n\nbody\n"))


def test_a_field_inside_the_fence_is_not_counted_a_second_time():
    """The fence's own lines are SKIPPED by the header-line scan, so a fenced
    declaration inside the window is one declaration and not a self-conflict."""
    assert fms.read_header_line(
        _fenced("sequenced_after: [parent]"), "sequenced_after"
    ) is fms.NO_HEADER_LINE
    assert sa.read_declaration(_fenced("sequenced_after: [parent]")) == ["parent"]


def test_an_opened_but_unclosed_fence_declares_nothing_on_EITHER_path():
    """Copilot's finding on PR #886, taken as a real defect and fixed.

    `fence_span` returns None for a fence that opens and never closes, so a naive
    scan would start at line 0 and take a header line out of a span the author
    plainly meant as FRONT MATTER — showing a reviewer fenced front matter while
    the reader read a header line out of it. It would also flip this module's
    existing, deliberate posture that a document with no well-formed fence "still
    reads as NO FRONT MATTER — which is fail-CLOSED here". Both paths now agree:
    the malformed document declares nothing, exactly as it did before this
    change. Measured at the time of the fix: ZERO of the 375 `proposal.md` files
    in both clones carries such a fence, so the corpus is unmoved either way —
    the fix is for the form, not for a document.
    """
    unclosed = ("---\n"
                "code_surface: openxFactory\n"
                "sequenced_after: [parent]\n"
                "\n# Proposal\n\nbody\n")
    assert fms.fence_span(fms.split_real_lines(unclosed)) is None
    assert fms.read_header_line(unclosed, "sequenced_after") is fms.NO_HEADER_LINE
    assert sa.read_declaration(unclosed) is sa.ABSENT
    # And the SAME bytes with the fence closed declare, on the fenced path, so
    # the refusal is about the malformation and not about the content.
    closed = unclosed.replace("sequenced_after: [parent]\n",
                              "sequenced_after: [parent]\n---\n", 1)
    assert sa.read_declaration(closed) == ["parent"]


def test_fence_lines_count_toward_the_window():
    """One window rule — the first N lines OF THE DOCUMENT — rather than a second
    window measured from wherever a fence happens to end."""
    window = fms.HEADER_WINDOW_LINES
    front = "\n".join(f"Header{n}: value" for n in range(window))
    text = _fenced(front, body="\nsequenced_after: [parent]\n\nbody\n")
    assert sa.read_declaration(text) is sa.ABSENT


# --- REFUSED FORMS ON THE HEADER-LINE PATH -----------------------------------


def test_two_header_lines_for_one_field_are_refused_as_the_duplicate_key():
    """Both matched lines reach `strict_load` together, so the refusal is the
    loader's OWN duplicate-key message and no second rule is written."""
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.read_declaration(_unfenced(
            "Status: ratified\n"
            "sequenced_after: [parent-one]\n"
            "sequenced_after: [parent-two]"))
    assert "duplicate key" in str(excinfo.value)


def test_a_block_sequence_attempt_on_the_header_line_is_refused_by_name():
    """An unfenced document supplies no closing delimiter, so a multi-line value
    has no defined end and a window boundary inside it would show a reader one
    declaration and authorize another. The author is told which form to use."""
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.read_declaration(_unfenced(
            "Status: ratified\nsequenced_after:\n  - parent-one\n  - parent-two"))
    message = str(excinfo.value)
    assert "SINGLE LINE" in message
    assert "`---` fence" in message


def test_a_valueless_header_line_with_no_continuation_is_present_but_null():
    """Presence is decided by the KEY, never by the value — so this is refused by
    `validate_shape` rather than read as absence, exactly as the fenced form is."""
    raw = sa.read_declaration(_unfenced("Status: ratified\nsequenced_after:"))
    assert raw is None
    assert raw is not sa.ABSENT
    with pytest.raises(sa.SequencedAfterError):
        sa.validate_shape(raw)


def test_the_strict_loader_refusals_reach_the_header_line_form():
    with pytest.raises(sa.SequencedAfterError) as excinfo:
        sa.read_declaration(_unfenced(
            "Status: ratified\nsequenced_after: [*alias]"))
    assert "alias" in str(excinfo.value)


def test_a_scalar_header_line_is_present_and_refused_by_shape_not_by_the_reader():
    """A SHAPE refusal does not raise out of the reader: the field is present, the
    raw value is returned, and `validate-sequenced-after.py` is what refuses it —
    the same split `classify_corpus` documents for the fenced form."""
    raw = sa.read_declaration(_unfenced("Status: ratified\nsequenced_after: parent"))
    assert raw == "parent"
    with pytest.raises(sa.SequencedAfterError):
        sa.validate_shape(raw)


# --- THE FREEZE: A LATE-ADDED DECLARATION IS CONTESTED, NEVER SILENT ---------


def test_a_declaration_added_after_ratification_is_a_contested_class_finding():
    """The disposition case the two codexFactory carriers use. Both sides of the
    comparison are read by the SAME reader, so a carrier whose header line was
    ALREADY THERE at its ratified head shows NO mutation — door (b) moves no
    bytes. A carrier whose line was ADDED afterwards flips ABSENT -> declared,
    and that is a MUTATION the gate must report rather than accept."""
    ratified = sa.read_declaration(_unfenced("Status: ratified\ncode_surface: x"))
    current = sa.read_declaration(
        _unfenced("Status: ratified\ncode_surface: x\nsequenced_after: [parent]"))
    assert ratified is sa.ABSENT
    assert current == ["parent"]

    problem = sa.retention_problem(ratified, current)
    assert problem is not None
    assert "mutated after ratification" in problem
    assert "contested-class act requiring an explicit disposition" in problem


def test_a_header_line_present_at_ratification_is_retained_not_mutated():
    """Door (b)'s central claim, asserted rather than argued: teaching the reader
    the form does not itself disturb a frozen chain position."""
    text = _unfenced("Status: ratified\nsequenced_after: [parent]")
    assert sa.retention_problem(sa.read_declaration(text),
                               sa.read_declaration(text)) is None


def test_moving_a_declaration_into_the_window_registers_as_a_mutation():
    """Moving the LINE is not a neutral reformat: outside the window the change
    declared nothing and inside it declares a parent, so the corpus act E-8 left
    open still needs its own disposition."""
    window = fms.HEADER_WINDOW_LINES
    filler = "\n".join(f"Header{n}: value" for n in range(window))
    outside = f"{filler}\nsequenced_after: [parent]\n\nbody\n"
    inside = f"sequenced_after: [parent]\n{filler}\n\nbody\n"
    assert sa.read_declaration(outside) is sa.ABSENT
    assert sa.read_declaration(inside) == ["parent"]
    assert sa.retention_problem(sa.read_declaration(outside),
                                sa.read_declaration(inside)) is not None


# --- THE LINE RULE AND THE WINDOW ARE HELD BY AGREEMENT, NOT BY CONVENTION ---


def test_the_window_number_equals_the_doc_health_status_scan_window():
    """`frontmatter_strict` restates the number instead of importing it, because
    this file is vendored into a repository with no `doc_health` package. The
    ratified remedy for a boundary an import cannot cross is an explicit
    agreement test — this is it."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from doc_health import corpus as dh_corpus
    finally:
        sys.path.pop(0)
    assert fms.HEADER_WINDOW_LINES == dh_corpus.STATUS_SCAN_LINES


@pytest.mark.parametrize("text", [
    "a\nb\nc",
    "a\r\nb\rc\n",
    "",
    "\n",
    "Status: draft\x0crest of the line\nsequenced_after: [parent]\n",
    "Status: draft more more\nsequenced_after: [parent]\n",
    "trailing\n\n",
])
def test_the_real_line_rule_agrees_with_the_doc_health_line_rule(text):
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from doc_health.lines import split_keepends
    finally:
        sys.path.pop(0)
    assert fms.split_real_lines(text) == [body for body, _e in split_keepends(text)]
    assert "".join(
        body + ending for body, ending in split_keepends(text)) == text


def test_an_exotic_separator_does_not_inflate_the_window():
    """`str.splitlines()` breaks on U+2028; a window counted that way is a window
    over FRAGMENTS. A declaration the writer plainly wrote inside the header must
    still be found."""
    header = "\n".join(
        [f"Header{n}: value continued continued" for n in range(6)])
    text = f"# Proposal\n\n{header}\nsequenced_after: [parent]\n\nbody\n"
    assert len(text.splitlines()) > fms.HEADER_WINDOW_LINES
    assert len(fms.split_real_lines(text)) <= fms.HEADER_WINDOW_LINES + 3
    assert sa.read_declaration(text) == ["parent"]


# --- THE ASYMMETRY IS ASSERTED, NOT LEFT TO THE READER'S TRUST ---------------


def test_scope_globs_is_NOT_read_from_a_header_line():
    """`scope_globs:` authorizes WHICH PATHS an autonomous merge may write, so a
    new place to declare it is a new place to widen a path grant. This change
    admits the header-line form for the POSITION field alone; widening the path
    field is a separate act needing its own ruling."""
    scope = _load(SCOPE_MODULE, "scope_globs")
    unfenced = _unfenced("Status: ratified\nscope_globs: [\"scripts/**\"]")
    assert scope.read_scope_globs(unfenced) is None    # fail-closed: no grant
    # And the fenced form is untouched, so the field still works exactly where
    # it is ratification-covered.
    assert scope.read_scope_globs(
        _fenced("scope_globs: [\"scripts/**\"]")) == ["scripts/**"]


# --- THE LIVE CORPUS IS UNMOVED BY THE CHANGE --------------------------------


def test_no_openxFactory_proposal_gains_or_loses_a_declaration():
    """Measured, not asserted: openxFactory's corpus carries ZERO unfenced
    `sequenced_after:` header lines, so this change's declaring population and
    every total derived from it are IDENTICAL before and after. The corpus that
    moves is codexFactory's, and it moves at ITS re-pin."""
    changes = ROOT / "openspec" / "changes"
    unfenced_carriers = []
    for proposal in sorted(changes.rglob("proposal.md")):
        text = proposal.read_text(encoding="utf-8")
        if fms.fence_span(fms.split_real_lines(text)) is not None:
            continue
        if fms.read_header_line(text, sa.FIELD) is not fms.NO_HEADER_LINE:
            unfenced_carriers.append(proposal.relative_to(ROOT).as_posix())
    assert unfenced_carriers == []
