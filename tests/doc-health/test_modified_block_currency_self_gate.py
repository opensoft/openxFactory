"""THE SELF-GATE: what the modified-block-currency family says about THIS repository.

`add-modified-block-currency-check`, Speckit feature
`021-modified-block-currency-self-gate` (packet § 4.1–4.5). F1
(`019-modified-block-currency-family`) built and registered the family; F2
(`020-modified-block-currency-fixtures`) built the regression catalogue. Both
assert over FIXTURE trees, which is the right shape for what they assert and
says nothing about the corpus the report a steward reads is computed over.

**Fixtures prove the RULES. This file proves the VERDICT.**

Every row the family draws over this checkout is asserted here by NAMED SUBJECT
— which change, which capability, which requirement, and for the gate-bearing
`warning` the omitted scenario title itself — because the packet's own § 4.1
forbids a bare count: a count assertion over a broken read fails with `0 != 10`,
which reads as a corpus change, while a floor plus named subjects fails saying
that discovery examined nothing.

THE FIGURES, AND THE PACKET'S ARE STALE. The packet's § 4.1 predicted
"1 scenario-arm finding, 11 carriage-ledger findings, 0 title-resolution
findings" from a spike taken at `9be81a40` over TWENTY-THREE MODIFIED blocks.
That tree no longer exists — `add-hermes-customer-subject-runtime-contract` and
`add-shared-identity-seeds` archived in between. **Re-measured at `76a2ad27`
over TWENTY-TWO blocks: +1 `warning`, +9 `info`, 0 unresolved, 0 ordering, 0
marker defects. RE-MEASURED AGAIN after merging `origin/main` at `175682e2`:
+1 `warning`, +8 `info` over the same twenty-two blocks** — one ledger subject
went away when PR #424 renamed a repository in canon and in the active delta
that quotes it, in one commit, which is the correct authoring move and exactly
what this arm is advisory about. The packet's numbers are history and are
recorded here as such; this file asserts what the tree produces. Orchestrator decision D1 in
`specs/021-modified-block-currency-self-gate/plan.md`, flagged for veto, and
that plan's § THE FIGURES is the single home for the table — nothing else
restates it.

§ 4.2 IS LIKEWISE STALE. It asks that this change's own § 2.1 block be asserted
"measured against `add-family-enumeration-check`'s outcome". That sibling
ARCHIVED at `f027d3b3` (PR #419) before F1 registered the family, so it is not
among this tree's active changes and there is no sibling outcome to measure
against. F1's T052 wrote the block against CANON for exactly that reason, and
`test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists`
asserts both halves — the basis that exists, and the sibling's absence.
Orchestrator decision D2.

WHAT F1's T057 DID NOT DO. F1's `tasks.md` records T057 —
`test_the_family_reads_its_own_packet_s_delta` — as done, and its hand-off says
"the own-packet assertion F3 § 4.2 wants is live". It is not: no function of
that name and no assertion of that content exists anywhere under `tests/`. This
file writes it. Nothing is duplicated because nothing existed. Orchestrator
decision D5, and F1 residue finding 6 after F2's five.

THREE INDEPENDENT GUARDS, and the independence is the design:

  1. THE RESOLVER — the tree measured is the tree this file lives in, confirmed
     by markers and cross-checked against `git rev-parse --show-toplevel`. A
     resolver pointed anywhere else fails before a finding is read. The defect
     this mirrors is `harden-ideation-readiness-check`'s: a bare ancestor walk
     "always terminated on the one shared checkout beneath the aggregation root,
     whatever repository the run was launched against", so an agent worktree's
     verdict was a verdict about another session's working tree.
  2. THE DISCOVERY FLOOR — the population of MODIFIED blocks is non-empty,
     asserted in its own test naming no severity, no change and no requirement.
     Delete every named-subject assertion below and this one still fails on a
     vacuous read.
  3. THE NAMED SUBJECTS — the `warning` by all four of its fields, the nine
     `info` as an exact SET, and the three empty classes by the module's own
     rule text with a positive control on each probe.

Guard 3 alone passes on a clean corpus read by a broken family (an empty finding
set is not an empty read). Guard 2 alone passes when every finding is wrong.
Guard 1 alone passes on the right tree read by a broken family. The mutation
round (`specs/021-modified-block-currency-self-gate/evidence/self-gate.md`)
targets one each.

THIS FILE IS EXPECTED TO FALL DUE. Its subjects are live corpus content. When
`add-composed-view-authoring` declares its rename with a `Removed from canon by`
marker — which the packet's § 6.3 already calls the correct disposition — the
`warning` vanishes and `test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else`
fails. That is designed behaviour, `_moved()` says so in every message, and
`quickstart.md` § WHEN THE GATE FAILS says what to do. If the family ever reads
ZERO over this tree, that is the DESIRED end state: assert zero by this same
named-subject mechanism and keep the floor, which is then the only assertion
distinguishing a clean corpus from a broken reader.
"""

from __future__ import annotations

import functools
import inspect
import re
import subprocess
import sys
from pathlib import Path

import pytest

from doc_health import INFO, WARNING, Skip
from doc_health import modified_block_currency as mbc
from doc_health import promotion_fidelity

from conftest import REPO_ROOT

# ============================================================================
# The repository under test, and why it is resolved rather than assumed
# ============================================================================

_MARKER_DIR = "openspec/changes"
_MARKER_FILE = "openspec/specs/doc-health/spec.md"


class UnresolvedRepository(Exception):
    """No checkout serves this proof — named, never merely absent.

    A distinct type rather than `AssertionError`, so the resolver's REFUSAL is
    distinguishable from a failing assertion inside a test. `pytest.raises`
    catching `AssertionError` would also catch a genuine bug in the test that
    provoked it.
    """


def _repo_under_test(under_test=None) -> Path:
    """The openxFactory checkout this run is a proof ABOUT.

    THE REPOSITORY UNDER TEST, AND NOTHING ELSE. If the base carries both
    markers it IS the subject; otherwise this RAISES with a message naming both
    markers and the path searched. There is deliberately **no ancestor walk, no
    environment variable and no fallback**.

    That is the first rung of `harden-ideation-readiness-check`'s resolution
    order and its failure mode, and only those. The rungs past the first exist
    there because that proof can legitimately be served by a SIBLING checkout;
    this one cannot — the family measures the checkout it is registered in, so a
    fallback to any other tree would produce a verdict about a repository nobody
    asked about. `test_ideation_readiness.py::_openxfactory_root` is not
    imported: its marker (`ideation/cross-reference.yaml`) is the wrong marker
    for this family, and its own comment records that three copies already exist
    deliberately as that packet's open Q3 — a fourth is not an improvement.

    NOT REVISION-ADDRESSED, and that is decision D4 rather than an omission. The
    ideation proof reads both sides out of `git archive` because its subject is
    an index that PINS `generation.source_revision`. This family has no pin: it
    measures the checkout by contract, and F1's
    `test_the_promoted_reader_cannot_reach_a_measurement_basis` asserts
    structurally that `promoted(root, capability)` has no ref, no git shim and
    no context to receive one. Revision-addressing here would measure a
    different subject from the one the report measures.
    """
    base = Path(under_test or Path(__file__).resolve().parents[2]).resolve()
    if (base / _MARKER_DIR).is_dir() and (base / _MARKER_FILE).is_file():
        return base
    raise UnresolvedRepository(
        f"NOT A MEASURABLE openxFactory CHECKOUT: {base} does not carry both "
        f"{_MARKER_DIR}/ (a directory) and {_MARKER_FILE} (a file). This "
        f"resolver does NOT walk up: an ancestor walk lands on the aggregation "
        f"checkout or another session's worktree, and a verdict about "
        f"repository A reported as though it were about repository B has "
        f"proved nothing about either "
        f"(harden-ideation-readiness-check). Point the gate at the checkout "
        f"that carries the family.")


ROOT = _repo_under_test()

_REMEASURE = ("python3 scripts/doc-health.py --single-repo . "
              "--family modified-block-currency")


def _moved(subject: str, detail: str) -> str:
    """THE FAILURE MESSAGE IS A DELIVERABLE (FR-016, SC-001).

    Every corpus-facing assertion in this file routes its message through here.
    A self-gate against a live corpus is a maintenance obligation, and a failure
    message that does not name the obligation converts the gate into an obstacle
    and gets it deleted rather than updated.
    """
    return (
        f"\nTHE CORPUS MOVED, most likely, and corpus movement is the EXPECTED "
        f"cause of this failure.\n"
        f"  tree measured : {ROOT}\n"
        f"  subject       : {subject}\n"
        f"  observed      : {detail}\n"
        f"WHAT TO DO: re-measure with `{_REMEASURE}` and update the named "
        f"subjects in this module, in the same commit, saying which subject "
        f"moved and why. If the family now reads ZERO over this tree, that is "
        f"the DESIRED end state — assert zero by this same named-subject "
        f"mechanism and keep the discovery floor, which is then the only "
        f"assertion distinguishing a clean corpus from a broken reader. "
        f"AT ZERO, RE-AIM THE MOVEMENT PIN TOO: its two vacuity guards in "
        f"`test_the_report_moves_only_in_this_family_s_lines` — "
        f"`assert f'### {{mbc.FAMILY}}' in differing` and `assert plan_moved` — "
        f"exist to stop the two report runs passing when they rendered the same "
        f"thing, and at zero findings they are TRUE of the desired state, so "
        f"they must become an assertion that the family's section reads its "
        f"skip/empty line identically in both runs. "
        f"See specs/021-modified-block-currency-self-gate/quickstart.md "
        f"§ WHEN THE GATE FAILS before editing anything.")


def _joined_source(module_or_text) -> str:
    """A module's source with adjacent string-literal SEAMS closed.

    The family writes its rule text as adjacent f-string literals, so a phrase
    that reads contiguously in the OUTPUT is split in the SOURCE:

        f"active MODIFIED block for {block.title!r} resolves to no promoted "
        f"requirement, no rename of its own, ..."

    The first cut of `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
    searched the raw source for `"resolves to no promoted requirement"` and its
    POSITIVE CONTROL failed — which is the control working: a probe nobody could
    find in the module is a probe that reads zero against any corpus. Joining the
    seams is what lets the probe be the phrase a reader sees in the report.
    """
    text = (module_or_text if isinstance(module_or_text, str)
            else inspect.getsource(module_or_text))
    return re.sub(r'"\s*\n\s*f?"', "", text)


def _code_only(text: str) -> str:
    r"""Source with docstrings AND whole-line comments removed.

    `_without_docstrings` alone was not enough, and the review caught it on this
    file's own prose: the fix for N2 was a COMMENT reading "adding `mbc.carried`
    to any docstring reddened the equality" — and that comment reddened the
    equality. A probe a comment can break is a probe on comments.

    Only comments that OWN THEIR LINE are stripped, so a `#` inside a string
    literal (the family compiles `r"^####\s+Scenario:"`) survives. Docstrings go
    first, so a triple-quoted block whose line happens to start with `#` is
    already gone by the time the comment pass runs.
    """
    return re.sub(r"(?m)^[ \t]*#.*$", "", _without_docstrings(text))


def _without_docstrings(text: str) -> str:
    """Source with every triple-quoted block removed — MATCHED ON USE, NOT ON MENTION.

    This is the third time this family's tests have learned the rule the hard
    way. F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis` failed
    its first run because `promoted`'s docstring NAMES the readers it refuses to
    use; and `test_the_family_reads_exactly_two_things_from_its_run_context`
    failed its first run here because `load_dispositions`'s docstring writes
    "`runner.main` guards the same read with `if ctx.agg_root`" — a sentence
    explaining the mechanism, not a use of it. A test that forbids DESCRIBING a
    rule is a bad test.
    """
    return re.sub(r'"""(?:.|\n)*?"""', "", text)


def _ctx(root: Path):
    """The family's run context, at the size the family actually reads.

    TWO ATTRIBUTES, AND THAT IS THE WHOLE SURFACE — MEASURED, not assumed.
    `ctx.repo_paths` is the only `ctx.` access in
    `scripts/doc_health/modified_block_currency.py`, and the context is handed
    to exactly one collaborator, `promotion_fidelity.load_dispositions`, which
    reads `agg_root` and nothing else. This is
    `test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves`'s
    pattern, and `test_the_family_reads_exactly_two_things_from_its_run_context`
    is what keeps it PROVABLY faithful rather than faithful-because-read-once.

    `agg_root=None` is not a convenience: it is the single-repo scope a PR
    self-gate runs in, in which `health/dispositions.yaml` lives at a root that
    does not exist and therefore no disposition can suppress anything. Asserted
    below, so the gate's silence about dispositions is understood rather than
    discovered.
    """
    class Ctx:
        repo_paths = {"openxFactory": root}
        agg_root = None
    return Ctx()


@functools.lru_cache(maxsize=1)
def _findings():
    """One real run of the family over this checkout, through its OWN entry point.

    Cached because six tests read it and determinism is already F1's
    (`test_two_runs_agree_byte_for_byte`); re-running it six times would be
    slower without asserting anything F1 does not.
    """
    return mbc.fam_modified_block_currency(_ctx(ROOT))


# ============================================================================
# The named subjects — MEASURED AT 76a2ad27
#
# These move when the corpus moves. That is not a defect: see the module
# docstring's last paragraph and quickstart.md § WHEN THE GATE FAILS. The ONE
# movement already known to be coming is `add-composed-view-authoring`
# declaring its rename with a `Removed from canon by` marker, which the
# packet's § 6.3 calls the correct disposition — on that day the warning
# vanishes and `_SCENARIO_SUBJECT` becomes None with the band asserted empty.
# ============================================================================

_SCENARIO_SUBJECT = (
    "add-composed-view-authoring",
    "ideation-dashboard",
    "Composed views are read-only with a repository jump",
    "Gate verbs hide on a composed view",
)

# The rename the omission actually is (packet § 6.3) — NOT a defect, and the
# reason the scenario arm launched advisory. Kept here because it is also the
# corpus's own containment case: canon's title is a substring of this one under
# the family's title normalization, and the family still reports it.
_RENAME_DESTINATION = "Tile-bound gate verbs hide on a composed view"

_LEDGER_SUBJECTS = {
    ("add-composed-view-authoring", "ideation-dashboard",
     "Composed views are read-only with a repository jump"),
    ("add-doxchat-model-intake", "ideation-dashboard",
     "doxBench model catalog and provider boundary"),
    # THE SELF-FINDING. Expected evidence that the family reads its own packet
    # (F1's O2, packet § 6.6) — never a regression, and never to be
    # dispositioned: a disposition here would hide the evidence.
    ("add-modified-block-currency-check", "doc-health",
     "Deterministic check families"),
    ("add-notebook-projection-identity", "lifecycle-notebook-projection",
     "The session namespace is reconciled against live sessions"),
    ("declare-client-standing-policy-contract", "client-layer-tuning",
     "Client content shapes are contract-validated"),
    ("qualify-avatar-live-voice", "avatar-client-lab",
     "Repository and ownership boundary"),
    ("qualify-avatar-live-voice", "avatar-client-runtime",
     "Redacted telemetry and latency evidence"),
    ("qualify-avatar-live-voice", "avatar-client-runtime",
     "Versioned neutral avatar-client contract kernel"),
    # REMOVED 2026-08-27 — ('qualify-avatar-live-voice',
    # 'repo-boundary-governance', 'Neutral avatar-client repository boundary').
    # THE FIRST TIME THIS GATE FELL DUE, AND IT FELL DUE ON ITS OWN PULL
    # REQUEST. PR #424 (`realize-pin-reachability`) landed on `main` while #427
    # was open; its commit `7e4e2f99` — "The client was extracted three weeks
    # early under another name, so canon learns to say openAvatar" — renamed
    # `xfactory-avatar-client` to `openAvatar` in BOTH canon and this active
    # delta, in one commit. So the block now carries all twelve of canon's
    # units and the family correctly reports nothing. Verified before deleting:
    # `mbc.carried` returns the UNCARRIED units, and it returns none here.
    # This is the designed behaviour end to end — real movement, detected by
    # name, remedied by re-measuring. `_moved()`'s message is what said so.
}

_OWN_DELTA = ("openspec/changes/add-modified-block-currency-check"
              "/specs/doc-health/spec.md")
_OWN_TITLE = "Deterministic check families"
_OWN_CANON = "openspec/specs/doc-health/spec.md"

# The two body sentences § 2.1's block does not carry — canon's wording, not the
# block's. The block says "twenty-two"; the finding names what CANON states.
_STALE_NUMERALS = ("twenty-one check families", "Four of the twenty-one")

# The sibling the packet's § 4.2 names as the basis. Archived before F1
# registered, which is why the basis is canon (decision D2).
_ARCHIVED_SIBLING = "add-family-enumeration-check"

_DELTA_PATH = re.compile(r"^openspec/changes/([^/]+)/specs/([^/]+)/spec\.md$")
_TITLE = re.compile(r"active MODIFIED block for (['\"])(.+?)\1")


def _subject(finding) -> tuple[str, str, str]:
    """A finding's named subject, read out of WHAT THE FAMILY WROTE.

    No second parser. The gate does not re-read the delta to work out which
    requirement a finding is about — it reads the path the family put on the
    finding and the title the family quoted in the rule. A gate that re-parsed
    the corpus would be proving something about the gate.

    STRICT ON BOTH HALVES: an unparseable path or an unquoted title RAISES
    rather than returning a partial subject, so a change to the family's rule
    wording fails here by name instead of silently emptying the compared set.
    """
    path = _DELTA_PATH.match(finding.path)
    if path is None:
        raise AssertionError(
            f"finding path {finding.path!r} is not of the family's own "
            f"{mbc.DELTA_GLOB!r} shape — the gate reads the family's output, "
            f"so a path shape change must fail here")
    title = _TITLE.search(finding.rule)
    if title is None:
        raise AssertionError(
            f"finding rule quotes no requirement title, so no subject can be "
            f"named: {finding.rule[:200]!r}")
    return path.group(1), path.group(2), title.group(2)


# ============================================================================
# 1. THE RESOLVER GUARD — the tree measured is the tree this file lives in
# ============================================================================


def test_the_repository_under_test_is_the_tree_this_test_file_lives_in():
    """GUARD 1. Every other assertion in this file reads the root resolved here,
    so a resolver that lands on the wrong tree makes every later green
    meaningless.

    Four independent confirmations, because "the right path" is exactly the kind
    of claim that is easy to satisfy accidentally: the test file's own location,
    both markers, `conftest.REPO_ROOT`'s agreement, and git's own answer for
    which tree this is. A worktree of the SAME repository has a different
    toplevel, which is what makes the last one bite.
    """
    here = Path(__file__).resolve().parents[2]
    assert ROOT == here, (
        f"the gate resolved {ROOT} but this test file lives in {here}")
    assert (ROOT / _MARKER_DIR).is_dir(), ROOT
    assert (ROOT / _MARKER_FILE).is_file(), ROOT
    assert Path(REPO_ROOT).resolve() == ROOT, (
        f"conftest.REPO_ROOT is {Path(REPO_ROOT).resolve()}, the gate resolved "
        f"{ROOT} — the suite and the gate must measure one tree")

    top = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert Path(top).resolve() == ROOT, (
        f"git says the tree at {ROOT} is really {top} — the gate is measuring "
        f"a path that is not its own checkout's root")


def test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up(
        tmp_path):
    """GUARD 1, THE OTHER HALF, AND IT IS KEPT RATHER THAN DISCARDED.

    A gate that only proves the right tree resolves cannot tell a correct
    resolver from a lucky one. `harden-ideation-readiness-check`'s defect was a
    resolver that SUCCEEDED on the wrong tree, so the assertion that carries the
    fix is that the wrong tree is REFUSED — including a tree wearing the
    AGGREGATION markers, which is what an ancestor walk actually lands on, and a
    subdirectory, which is where a walk in the other direction would start.

    THE AGGREGATION CASE IS A DECOY, NOT AN ANCESTOR, AND THAT IS A FIX. The
    first cut of this test searched `ROOT.parents` for a real checkout carrying
    `.gitmodules` and `xFactories/`, and asserted one was found — an assertion
    about the DEVELOPER'S FILESYSTEM, not about the resolver. It passes here
    (this worktree sits under the aggregation checkout) and FAILS in CI:
    `pytest-suite` runs against a bare `$GITHUB_WORKSPACE/openxFactory`
    checkout with no such ancestor, so the required check would have gone red on
    a green branch. Reproduced by the review, and by the CI-shape run recorded
    in `evidence/self-gate.md` § CI shape.

    The repository's standing answer to an environment-dependent proof is to
    SKIP it — `test_session_harness.py`:251 (`pytest.skip("no aggregation
    checkout reachable from this tree")`) and
    `test_aggregation_register_instance.py`:25-27 (`aggregation_scope =
    pytest.mark.skipif(... GITMODULES.is_file() ...)`). Both are right for a
    proof that NEEDS a real aggregation tree. This one does not: its content is
    "aggregation markers without the family markers are refused", and a
    `tmp_path` decoy states exactly that in every environment, with no skip and
    no filesystem assumption. Removing the dependence beats guarding it.
    """
    with pytest.raises(UnresolvedRepository) as exc:
        _repo_under_test(ROOT.parent)
    message = str(exc.value)
    assert _MARKER_DIR in message
    assert _MARKER_FILE in message
    assert str(ROOT.parent) in message
    assert "does NOT walk up" in message

    # THE AGGREGATION DECOY: the markers an aggregation checkout carries, and
    # NOT the markers this family needs. Wearing one set is not being the other.
    decoy = tmp_path / "xFactory"
    decoy.mkdir()
    (decoy / ".gitmodules").write_text(
        '[submodule "openxFactory"]\n\tpath = openxFactory\n', encoding="utf-8")
    (decoy / "xFactories").mkdir()
    (decoy / "installs").mkdir()
    assert (decoy / ".gitmodules").is_file() and (decoy / "xFactories").is_dir()
    with pytest.raises(UnresolvedRepository):
        _repo_under_test(decoy)

    # ...and downward: a subdirectory does not resolve to the tree above it.
    with pytest.raises(UnresolvedRepository):
        _repo_under_test(ROOT / "tests")


# ============================================================================
# 2. THE DISCOVERY FLOOR — no assertion here can pass on an empty read
# ============================================================================


def test_the_family_examined_at_least_one_modified_block_over_the_real_tree():
    """GUARD 2, AND IT NAMES NO SEVERITY, NO CHANGE AND NO REQUIREMENT.

    That independence is the point: delete every named-subject assertion in
    section 3 and this one still fails on a vacuous read, which is SC-003 and
    the mutation round's M1.

    A FLOOR, NOT A COUNT, and F1 paid for that lesson. Its
    `test_the_real_notes_this_corpus_carries_are_each_one_unit` first pinned
    `== 2` and "broke the moment `add-family-enumeration-check` archived and
    promoted its third note" — an exact pin makes an unrelated archive look like
    this family's regression. The corpus's MODIFIED-block population is nobody's
    invariant; that it is NON-EMPTY is.
    """
    blocks = mbc.active_blocks(ROOT)
    changes = sorted({b.change for b in blocks})
    capabilities = sorted({b.capability for b in blocks})
    assert blocks, (
        f"\nDISCOVERY EXAMINED 0 MODIFIED BLOCKS over {ROOT} using glob "
        f"{mbc.DELTA_GLOB!r}.\n"
        f"THIS IS NOT CORPUS MOVEMENT. No repository carrying active changes "
        f"reads zero here, so the family's DISCOVERY broke: check "
        f"`active_blocks`, `DELTA_GLOB`, the `archive/` exclusion and the "
        f"resolved root — not the named subjects below.")
    assert changes, "blocks were found but no change could be named"
    assert capabilities, "blocks were found but no capability could be named"


def test_the_family_returns_findings_and_not_a_skip_over_a_tree_that_carries_changes():
    """A `Skip` and an empty finding list are DIFFERENT STATES, and canon's skip
    rule is "cannot run", not "found nothing".

    This checkout carries `openspec/changes/`, so a skip here is a defect rather
    than a legitimate abstention — and asserting the two apart is what stops a
    skip being read as a clean corpus. F1's
    `test_a_scope_with_no_changes_directory_skips_with_its_reason` pins the
    other direction over a fixture.
    """
    out = _findings()
    assert not isinstance(out, Skip), (
        f"the family SKIPPED a tree that carries {_MARKER_DIR}/: "
        f"{getattr(out, 'reason', out)}")
    assert isinstance(out, list)


# ============================================================================
# 3. THE NAMED SUBJECTS — packet § 4.1, by name and never by count
# ============================================================================


def test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else():
    """PACKET § 4.1's gate-bearing finding, asserted by all four of its fields.

    The count and the subject are asserted TOGETHER on purpose. The count alone
    is vacuous (any one warning would satisfy it); the subject alone would pass
    beside a second unnoticed warning, and the scenario-title arm is the arm
    § 7.2's flip reserves — the one whose population must be discharged before
    it can enforce.

    ON "ONE COUNT ASSERTION", WHICH THIS FILE APPEARS TO EXCEED. The brief
    allowed exactly one count assertion — the movement pin (§ 4.5) — and five
    tests here nonetheless carry a `len(...) == 1`. That is the sanctioned
    reading rather than a drift from it: § 4.1's anti-vacuity rule forbids
    asserting a corpus fact BY a count, and each of these five asserts a
    NAMED SUBJECT and bounds its population in the same breath, which is
    strictly stronger than either half. A bare `len(warnings) == 1` would be the
    thing forbidden; `len(warnings) == 1 AND its four fields are these` cannot
    be satisfied by any finding but the named one. The movement pin is still the
    only place a count is the whole claim, and it is stated as a difference
    between two runs rather than as a total.

    THE OMITTED TITLE IS MATCHED EXACTLY, AND THE CORPUS SUPPLIES ITS OWN
    CONTAINMENT CASE. Canon states `Gate verbs hide on a composed view`; the
    block renames it to `Tile-bound gate verbs hide on a composed view`, which
    CONTAINS canon's title under the family's title normalization. A containment
    reading would have called the obligation carried and reported nothing —
    exactly #351's widening mechanism, and the reason the delta forbids
    containment. Asserted positively below, so this test also demonstrates the
    rule rather than merely relying on it.
    """
    change, capability, requirement, scenario = _SCENARIO_SUBJECT
    warnings = [f for f in _findings() if f.severity == WARNING]

    assert len(warnings) == 1, _moved(
        f"the scenario-title arm's population (expected exactly 1: "
        f"{change} / {scenario!r})",
        f"{len(warnings)} warning(s): "
        f"{[(_subject(f), f.rule[:80]) for f in warnings]}")

    assert _subject(warnings[0]) == (change, capability, requirement), _moved(
        f"the scenario-title arm's subject", f"reported {_subject(warnings[0])}")
    assert f"{scenario!r}" in warnings[0].rule, _moved(
        f"the omitted scenario title {scenario!r}",
        f"the finding names something else: {warnings[0].rule}")
    assert _RENAME_DESTINATION not in warnings[0].rule, (
        "the finding names the RENAME DESTINATION rather than canon's title; "
        "the arm reports what canon states and the block does not carry")

    # The containment case, made explicit: canon's title IS a substring of the
    # rename destination under the family's own title normalization, and the
    # family reports it anyway. Same-kind EXACT, never containment.
    assert mbc.norm(scenario) in mbc.norm(_RENAME_DESTINATION)
    assert mbc.norm(scenario) != mbc.norm(_RENAME_DESTINATION)


def test_every_carriage_ledger_finding_over_the_real_tree_is_named():
    """PACKET § 4.1's editorial arm, as an EXACT SET of nine named subjects.

    COMPARED WITH `==`, NOT `<=`, and the reason is the family's own subject: a
    subset comparison would let a newly lossy MODIFIED block land unreported,
    which is the defect this family exists to catch. Asserted loosely in the one
    place the assertion is about this repository, it would be worse than no
    assertion.

    Both directions fail by name — the symmetric difference is in the message —
    so an archive that removes a subject and a new proposal that adds one are
    both legible, and neither is mistaken for the other.
    """
    infos = [f for f in _findings() if f.severity == INFO]
    seen = {_subject(f) for f in infos}
    gone = _LEDGER_SUBJECTS - seen
    fresh = seen - _LEDGER_SUBJECTS

    assert not gone and not fresh, _moved(
        "the carriage-ledger population (9 named subjects at 76a2ad27)",
        f"{len(gone)} named subject(s) NO LONGER reported "
        f"{sorted(gone)}; {len(fresh)} unnamed subject(s) NEWLY reported "
        f"{sorted(fresh)}")

    # A subject collapse would let one finding stand in for two. The set
    # comparison above cannot see it; this can.
    assert len(infos) == len(seen), (
        f"{len(infos)} ledger findings collapsed to {len(seen)} subjects — two "
        f"findings share a (change, capability, requirement) triple, so the set "
        f"comparison above is no longer one-to-one")


def test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree():
    """THE THREE CLASSES THAT READ ZERO, each identified by the module's OWN
    wording and each with a POSITIVE CONTROL on its probe.

    An "absent from" assertion over a rule-text probe is precisely the shape
    F1's mutation round caught: "the `FAMILY_RESOLUTION` absence was documented
    in three places and asserted in none". A misspelled probe reads zero against
    any corpus and proves nothing, so each probe is first asserted to BE the
    module's own text. Get the probe wrong and this fails on the probe, not on
    the corpus.

    Zero here is a fact about this tree, not a structural guarantee: an
    unresolved title, an undecided two-writers group and a defective marker are
    all reportable, and the packet's § 6.7 measured the ordering arm at zero
    twice — once under the withdrawn date reading and once under the ruled
    by-declaration one.
    """
    source = _joined_source(mbc)
    unresolved_probe = "resolves to no promoted requirement"
    ordering_probe = "the ordering of MODIFIED blocks for"
    assert unresolved_probe in source, (
        f"probe {unresolved_probe!r} is not the module's own wording, so the "
        f"absence below would be vacuous")
    assert ordering_probe in source, (
        f"probe {ordering_probe!r} is not the module's own wording, so the "
        f"absence below would be vacuous")
    assert mbc._MARKER_ACTION in source

    findings = _findings()
    unresolved = [f for f in findings if unresolved_probe in f.rule]
    ordering = [f for f in findings if ordering_probe in f.rule]
    markers = [f for f in findings if f.action == mbc._MARKER_ACTION]

    assert unresolved == [], _moved(
        "the title-resolution class (0 at 76a2ad27)",
        f"{[_subject(f) for f in unresolved]}")
    assert ordering == [], _moved(
        "the two-writers ordering class (0 at 76a2ad27)",
        f"{[f.rule[:160] for f in ordering]}")
    assert markers == [], _moved(
        "the marker-defect class (0 at 76a2ad27)",
        f"{[f.rule[:160] for f in markers]}")

    # ...and the bands that gate a run do not move at all.
    assert [f for f in findings if f.severity not in (WARNING, INFO)] == [], (
        "this family launched advisory: every finding is `warning` or `info`, "
        "so a run configured --fail-on error is unaffected by construction")


# ============================================================================
# 4. THE OWN PACKET — packet § 4.2, and the assertion F1's T057 did not write
# ============================================================================


def _own_block():
    blocks = [b for b in mbc.active_blocks(ROOT) if b.delta_rel == _OWN_DELTA]
    assert len(blocks) == 1, _moved(
        f"this change's own MODIFIED block ({_OWN_DELTA})",
        f"{len(blocks)} block(s): {[b.title for b in blocks]}")
    return blocks[0]


def test_this_change_s_own_delta_is_among_the_blocks_the_family_examined():
    """PACKET § 4.2, AND THE ASSERTION F1's T057 CLAIMED AND DID NOT LAND.

    F1's `tasks.md`:235 records T057 — `test_the_family_reads_its_own_packet_s_delta`
    — as done, and its § Hand-off tells F3 the assertion "is live". It is not:

        $ grep -rn "reads_its_own_packet\\|its_own_packet" tests/
        $ echo $?
        1

    So this is written here rather than reused, and the discrepancy is recorded
    as F1 residue finding 6 (decision D5). The closest existing thing,
    F2's `test_the_packets_own_marker_templates_are_not_marker_form`, reads the
    same FILE for a different purpose and says nothing about discovery.

    WHY § 4.2 EXISTS AT ALL: without it, § 4.1 could pass because discovery
    quietly stopped at the packet's own delta. The one block in this tree whose
    content this change controls is the one it must be seen to read.
    """
    block = _own_block()
    assert block.title == _OWN_TITLE, _moved(
        f"the requirement title of this change's own block",
        f"the block under {_OWN_DELTA} is titled {block.title!r}")


def test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists():
    """WHICH DOCUMENT THE BLOCK IS MEASURED AGAINST — asserted, because the
    packet's answer is STALE (decision D2).

    § 4.2 asks that the block be asserted "measured against
    `add-family-enumeration-check`'s outcome". That sibling ARCHIVED at
    `f027d3b3` before F1 registered the family, so there is no sibling outcome
    in this tree; F1's T052 wrote the block against CANON for that reason. Both
    halves are asserted here — the basis that exists, and the sibling's absence
    — so the packet's wording is visibly HISTORY rather than silently unmet.

    THE ORDERING ARM IS ASSERTED TOO, not inferred from the finding count. The
    two-writers instance § 6.6 predicted required two ACTIVE writers on one
    requirement; with the sibling archived there is one writer, so no basis
    override may be applied. A build that substituted a basis here would compare
    the block against a document no reader can name, which is the defect
    `release-realization`'s ordered-deltas rule exists to prevent.
    """
    block = _own_block()
    basis, status = mbc.resolve(
        block, mbc.promoted(ROOT, block.capability), mbc.sibling_titles(ROOT))

    assert status == "canon", _moved(
        f"the measurement basis of this change's own block",
        f"resolve() returned status {status!r}")
    assert basis is not None and basis.spec_rel == _OWN_CANON, _moved(
        f"the basis document for {_OWN_TITLE!r}",
        f"resolved to {getattr(basis, 'spec_rel', None)!r}")

    # The sibling § 4.2 names: absent from active, present in the archive.
    assert not (ROOT / _MARKER_DIR / _ARCHIVED_SIBLING).exists(), (
        f"{_ARCHIVED_SIBLING} is ACTIVE again, so the packet's § 4.2 basis is "
        f"live after all and decision D2 must be revisited")
    archived = sorted((ROOT / _MARKER_DIR / "archive")
                      .glob(f"*-{_ARCHIVED_SIBLING}"))
    assert len(archived) == 1, (
        f"expected exactly one archived {_ARCHIVED_SIBLING}, found "
        f"{[p.name for p in archived]}")

    # No basis override, asserted through the ordering arm itself.
    blocks = mbc.active_blocks(ROOT)
    key = (block.capability, mbc.norm(block.title))
    group = [b for b in blocks
             if (b.capability, mbc.norm(b.title)) == key]
    override, ordering = mbc._arm_ordering(
        "openxFactory", group, mbc.declarations(ROOT, blocks))
    assert override == {}, _moved(
        "the absence of a two-writers basis override on this change",
        f"a basis was substituted: {sorted(override)}")
    assert ordering == [], _moved(
        "the ordering arm's silence on this change's requirement",
        f"{[f.rule[:160] for f in ordering]}")
    assert len(group) == 1, _moved(
        f"the number of active writers on {_OWN_TITLE!r}",
        f"{len(group)}: {sorted(b.change for b in group)} — with two ACTIVE "
        f"writers the by-declaration rule applies and this test's premise "
        f"changes")


def test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences():
    """THE SELF-FINDING: EXPECTED EVIDENCE, NEVER A REGRESSION.

    § 2.1's block moves canon's `twenty-one` to `twenty-two` and its
    `Four of the twenty-one` to `Four of the twenty-two`, so under this family's
    own same-kind exact rule it does not CARRY those two canon sentences and the
    ledger reports them. The packet predicted it (§ 6.6), F1's O2 recorded that
    the self-gate must treat it as evidence, and it MUST NOT be dispositioned —
    a disposition here would hide the proof that the family reads its own
    packet.

    THE QUOTED UNITS ARE CANON's WORDING, NOT THE BLOCK's. The finding names
    what canon states and the block does not restate, so `twenty-one` is the
    correct thing to find here and `twenty-two` would mean the arm had its
    direction reversed.
    """
    own = [f for f in _findings() if f.path == _OWN_DELTA]
    assert len(own) == 1, _moved(
        "the self-finding against this change's own § 2.1 block",
        f"{len(own)} finding(s): {[(f.severity, f.rule[:120]) for f in own]}")
    assert own[0].severity == INFO, _moved(
        "the severity of the self-finding (the editorial ledger, advisory)",
        f"{own[0].severity}")
    assert _subject(own[0]) == ("add-modified-block-currency-check",
                               "doc-health", _OWN_TITLE)

    for sentence in _STALE_NUMERALS:
        assert sentence in own[0].rule, _moved(
            f"the uncarried canon sentence {sentence!r}",
            f"the self-finding quotes: {own[0].rule}")


def test_no_disposition_can_apply_in_the_single_repo_scope_the_gate_runs_in():
    """THE INHERITED SINGLE-REPO CAVEAT, ASSERTED SO THE SILENCE IS UNDERSTOOD.

    `health/dispositions.yaml` lives at the AGGREGATION root and a
    `--single-repo` self-gate run has none, so no disposition applies in this
    scope. That is the pre-existing shape of the mechanism — `runner.main` guards
    the same read with `if ctx.agg_root` — and F1's A7 review finding was that it
    was documented in three places and asserted in none, which is why T045 pinned
    it there and why it is pinned here too.

    It matters specifically for the self-finding above: if a disposition COULD
    reach this scope, someone could quietly retire the evidence that the family
    reads its own packet, and this gate would go green on its absence.
    """
    ctx = _ctx(ROOT)
    assert ctx.agg_root is None
    assert promotion_fidelity.load_dispositions(ctx, mbc.FAMILY) == set()


# ============================================================================
# 5. THE MOVEMENT PIN — packet § 4.5, the one count assertion, as a DIFF
# ============================================================================

_HEADLINE = re.compile(
    r"^Findings: (\d+) critical, (\d+) error, (\d+) warning, (\d+) info")
_SECTION = re.compile(r"^(#{2,3}) ([A-Za-z][\w -]*)$")
_PREAMBLE = "(preamble)"


def _report(root: Path, out_dir: Path, skip: bool) -> str:
    """One single-repo report rendering of `root`, with or without this family.

    HERMETIC, and structurally rather than by luck. A `--single-repo` run sets
    `agg_root = None` (`runner.build_context`), and the runner's only `nlm` call
    site returns immediately in that case (`_real_notebook_dryrun`: `if agg_root
    is None ... return None`). `gh` and `omp`, the other two binaries
    `tests/hermeticity.py` guards, have no call site in the doc-health runner at
    all, and layer 2's in-process seams live in modules it never imports.

    The BEFORE-STATE IS THIS TREE WITH THE FAMILY SKIPPED — never another
    worktree's `main`. No other family's behaviour changed, so skipping this one
    is exactly the pre-registration report, and it is a rendering of the same
    corpus rather than of a different one.
    """
    out = out_dir / ("without.md" if skip else "with.md")
    cmd = [sys.executable, "scripts/doc-health.py",
           "--single-repo", str(root), "--report-out", str(out)]
    if skip:
        cmd += ["--skip-family", mbc.FAMILY]
    proc = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True)
    assert proc.returncode == 0, (
        f"{' '.join(cmd)} exited {proc.returncode}\n{proc.stderr[-2000:]}")
    return out.read_text(encoding="utf-8")


def _bands(text: str) -> tuple[int, int, int, int]:
    for line in text.splitlines():
        found = _HEADLINE.match(line)
        if found:
            return tuple(int(g) for g in found.groups())
    raise AssertionError("the report carries no `Findings:` headline line")


_REPORT_TITLE = "# Doc-Health Report"


def _sections(text: str) -> dict[str, list[str]]:
    """The report split at its own headings, with the DATED TITLE DROPPED.

    The report's H1 is `# Doc-Health Report — <date>`, which `_SECTION` does not
    match: its em dash falls outside the heading character class, so the line
    lands in `(preamble)` and is compared verbatim. The two report runs are ~7
    seconds apart, and a pair STRADDLING MIDNIGHT would render two different
    dates — failing `differing <= permitted` in `(preamble)` for a reason with
    nothing to do with this family. A once-a-day flake in a required check is
    still a flake.

    DROPPED RATHER THAN MATCHED. Widening `_SECTION` to swallow the title would
    also let it match `### Requirement: …`, which
    `test_the_gate_reaches_the_corpus_only_through_the_family` forbids on
    purpose: a pattern that parses openspec structure is a parser this gate must
    not own. So the title is removed by name, and the caller asserts BOTH
    reports carried one — the drop cannot hide a change it was not written for.
    """
    out: dict[str, list[str]] = {_PREAMBLE: []}
    current = _PREAMBLE
    for line in text.splitlines():
        if line.startswith(_REPORT_TITLE):
            continue
        heading = _SECTION.match(line)
        if heading:
            current = f"{heading.group(1)} {heading.group(2)}"
            out[current] = []
            continue
        out.setdefault(current, []).append(line)
    return out


def test_the_report_moves_only_in_this_family_s_lines(tmp_path):
    """PACKET § 4.5, AND THE ONLY COUNT ASSERTION IN THIS FILE.

    Stated as a DIFFERENCE between two renderings of THIS checkout differing
    only by `--skip-family modified-block-currency`. The literals `1` and `9`
    appear nowhere: the warning and info movements are compared against the
    family's OWN per-severity finding counts taken from the same tree in the
    same test, so this pins "the family's findings are the whole movement"
    rather than a total that rots.

    § 4.5 IS SELF-CONTRADICTORY AS WRITTEN and this implements the reading that
    makes sense. It asks for "+1 warning, +11 info ... headline unchanged" — but
    the headline is the line those counts are printed on, so a run that gains a
    warning cannot leave it unchanged. Read as: the `error` and `critical` BANDS
    do not move, so a run configured `--fail-on error` is unaffected by
    construction, and census / inventory / catalog are untouched.

    THREE PERMITTED SECTIONS, everything else byte-identical: `## Headline` (the
    counts line and the skipped-family notice), `### modified-block-currency`
    (this family's own rows) and `## Ranked Plan` (the same findings, ranked).
    """
    with_family = _report(ROOT, tmp_path, skip=False)
    without = _report(ROOT, tmp_path, skip=True)
    findings = _findings()
    mine_warning = len([f for f in findings if f.severity == WARNING])
    mine_info = len([f for f in findings if f.severity == INFO])

    a, b = _bands(without), _bands(with_family)
    movement = tuple(y - x for x, y in zip(a, b))
    assert movement == (0, 0, mine_warning, mine_info), (
        f"the report movement is not this family's findings and nothing else.\n"
        f"  without this family : {a}  (critical, error, warning, info)\n"
        f"  with this family    : {b}\n"
        f"  movement            : {movement}\n"
        f"  the family reports  : {mine_warning} warning, {mine_info} info\n"
        f"A moved `error` or `critical` band means a --fail-on run has newly "
        f"started failing, which is a release-blocking fact and not a test to "
        f"relax.")

    # The dated title `_sections` drops must have been THERE to drop — otherwise
    # the drop is silently swallowing a structural change to the report.
    for label, text in (("without", without), ("with", with_family)):
        assert any(line.startswith(_REPORT_TITLE)
                   for line in text.splitlines()), (
            f"the {label} report carries no {_REPORT_TITLE!r} line, so "
            f"`_sections` dropped nothing and its flake guard is now hiding a "
            f"real change in the report preamble")

    left, right = _sections(without), _sections(with_family)
    assert set(left) == set(right), (
        f"the report's section set moved: "
        f"{sorted(set(left) ^ set(right))}")

    permitted = {"## Headline", f"### {mbc.FAMILY}", "## Ranked Plan"}
    differing = {name for name in left if left[name] != right[name]}
    assert differing <= permitted, (
        f"the report moved OUTSIDE this family's lines, in "
        f"{sorted(differing - permitted)}. Census, inventory, catalog, "
        f"preflight and every other family's section must be byte-identical: "
        f"registering a twenty-second family may not disturb a shared reader.")
    assert f"### {mbc.FAMILY}" in differing, (
        "this family's own section did not move, so the comparison above is "
        "vacuous — the two runs rendered the same thing")

    # `## Headline`: only the counts line and this family's skip notice.
    head_moved = [line for line in
                  set(left["## Headline"]) ^ set(right["## Headline"])
                  if line.strip()]
    for line in head_moved:
        assert _HEADLINE.match(line) or mbc.FAMILY in line, (
            f"an unexpected line moved in the headline section: {line!r}")

    # `## Ranked Plan`: every moved row belongs to this family.
    plan_moved = [line for line in
                  set(left["## Ranked Plan"]) ^ set(right["## Ranked Plan"])
                  if line.strip()]
    assert plan_moved, "the ranked plan did not move, so this check is vacuous"
    for line in plan_moved:
        assert f"family={mbc.FAMILY}" in line, (
            f"a ranked-plan row not belonging to this family moved: {line!r}")


# ============================================================================
# 6. THE STRUCTURAL PINS — the gate's own faithfulness
# ============================================================================


def test_the_family_reads_exactly_two_things_from_its_run_context():
    """WHAT MAKES `_ctx`'s TWO-ATTRIBUTE STAND-IN PROVABLY FAITHFUL.

    "Faithful because I read the source once" is not a guarantee; this is. The
    surface exists at TWO LEVELS and both are pinned, because the first cut of
    this test covered only the first (analyze finding A4): the family's own
    module reads ONE context attribute, and it hands the context to exactly ONE
    collaborator, whose own read is one more.

    Widen the family's context read at either level and this test reds — which
    is the signal to widen the stand-in, rather than discovering the gap from a
    wrong verdict on a report nobody diffed.
    """
    source = _code_only(inspect.getsource(mbc))

    # BOTH SHAPES A CONTEXT READ CAN TAKE. The first cut matched only
    # `ctx.<attr>`, and a mutant adding `getattr(ctx, "git", None)` — which is
    # how the disposition reader itself spells its read — SURVIVED it. An
    # attribute probe that misses the safe spelling of an attribute access is
    # the probe, not the pin.
    reads = (set(re.findall(r"\bctx\.(\w+)", source))
             | set(re.findall(r'getattr\(\s*ctx\s*,\s*["\'](\w+)', source)))
    assert reads == {"repo_paths"}, sorted(reads)

    # EVERY CALLEE HANDED THE CONTEXT, counted as a SET rather than as one
    # name's occurrences. `source.count("load_dispositions(ctx") == 1` was the
    # first cut and it proved only that ONE known collaborator is called once —
    # a second `_new_reader(ctx)` beside it survived, which is exactly the
    # widening the stand-in has to hear about. The `(?<!def )` guard drops the
    # family's own `def fam_modified_block_currency(ctx):` signature.
    # `\(ctx\s*[,)]` — the CONTEXT OBJECT ITSELF, not an attribute of it. The
    # first cut used `\(ctx\b` and collected `sorted`, because `sorted(ctx.
    # repo_paths.items())` puts a word boundary right after `ctx`. Reading an
    # attribute is guard one's business; handing the whole object away is this
    # one's. The optional leading group catches `f(a, ctx)` as well as `f(ctx)`.
    callees = set(re.findall(
        r"(?<!def )\b(\w+)\((?:[^()]*,\s*)?ctx\s*[,)]", source))
    assert callees == {"load_dispositions"}, (
        f"the family hands its context to {sorted(callees)}; `_ctx`'s "
        f"two-attribute stand-in is only faithful while `load_dispositions` is "
        f"the one collaborator, so a new one must be read and pinned here")

    reader = _code_only(
        inspect.getsource(promotion_fidelity.load_dispositions))
    assert set(re.findall(r'getattr\(ctx,\s*"(\w+)"', reader)) == {"agg_root"}
    assert not re.search(r"\bctx\.\w+", reader), (
        "the disposition reader now reads a context attribute directly; "
        "`_ctx` must grow it")


def test_the_gate_reaches_the_corpus_only_through_the_family():
    """FR-001 ASSERTED STRUCTURALLY, not left to authoring discipline (analyze
    finding A3).

    A gate that re-parsed the corpus would prove something about the gate. So:
    every corpus read here goes through a named `mbc.*` public function from a
    declared allowlist, and this module's OWN regexes are exactly four, none of
    which can parse openspec requirement structure — proven by running each
    against a `### Requirement:` heading, a `#### Scenario:` heading and a
    scenario bullet.

    MATCHED ON USE, NOT ON MENTION, which is a lesson this test file inherited
    rather than learned: F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis`
    failed its first run because `promoted`'s docstring NAMES the readers it
    refuses to use. A grep for `## MODIFIED` here would fire on this file's own
    docstring, so the pin is on the patterns' BEHAVIOUR instead.
    """
    declared = {"_DELTA_PATH", "_TITLE", "_HEADLINE", "_SECTION"}
    mine = {name for name, value in globals().items()
            if isinstance(value, re.Pattern)}
    assert mine == declared, (
        f"this module's regex set moved: {sorted(mine ^ declared)}. A new "
        f"pattern here is a parser this gate should not own — read what the "
        f"family wrote instead.")

    structure = (
        "### Requirement: Deterministic check families",
        "#### Scenario: A run executes the check families",
        "- **WHEN** the deterministic pass runs",
        "**Removed from canon by add-a-change (2026-08-27):** `A unit.`",
    )
    for name in sorted(declared):
        pattern = globals()[name]
        for line in structure:
            assert not pattern.match(line), (name, line)
            assert not pattern.search(line), (name, line)

    allowed = {"active_blocks", "declarations", "fam_modified_block_currency",
               "norm", "promoted", "resolve", "sibling_titles",
               "DELTA_GLOB", "FAMILY", "_MARKER_ACTION", "_arm_ordering"}
    # OVER CODE, NOT OVER PROSE. This test's own docstring claimed "matched on
    # use" while doing the opposite: naming any family attribute in a docstring
    # or a comment anywhere in this file reddened the equality below. The review
    # caught it, and then the FIX for it reddened the equality the same way,
    # because the first `_code_only` did not strip comments either. A pin that
    # prose can break is a pin on prose.
    used = set(re.findall(r"\bmbc\.(\w+)", _code_only(
        inspect.getsource(sys.modules[__name__]))))
    assert "fam_modified_block_currency" in used, (
        "the gate must reach its verdict through the family's entry point")
    # `==`, NOT `<=`. The subset direction catches a new reach into the family;
    # equality also catches a DECLARATION nobody uses, which is how an allowlist
    # rots into a permission slip. Both directions name the difference.
    assert used == allowed, (
        f"reached but not declared: {sorted(used - allowed)}; declared but no "
        f"longer reached: {sorted(allowed - used)}")


def test_every_corpus_assertion_explains_what_to_do_when_the_corpus_moves():
    """FR-016 / SC-001: THE FAILURE MESSAGE IS A DELIVERABLE.

    `add-composed-view-authoring` declaring its rename is the disposition the
    packet's § 6.3 already calls correct, so this file's `warning` assertion is
    EXPECTED to fall due. An engineer who meets that failure with no instruction
    has to reverse-engineer whether the family broke, and the cheapest way out
    of that is to loosen the assertion — which is how a self-gate dies.

    So `_moved` names the tree, the subject, the expected cause, the re-measure
    command and the zero end state; and every corpus-facing test is asserted to
    route through it, because a message nothing uses is a comment.
    """
    message = _moved("a subject", "an observation")
    for phrase in (str(ROOT), "a subject", "an observation",
                   "THE CORPUS MOVED", _REMEASURE, "DESIRED end state",
                   "discovery floor", "quickstart.md"):
        assert phrase in message, phrase

    corpus_facing = (
        test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else,
        test_every_carriage_ledger_finding_over_the_real_tree_is_named,
        test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree,
        test_this_change_s_own_delta_is_among_the_blocks_the_family_examined,
        test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists,
        test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences,
    )
    for test in corpus_facing:
        body = inspect.getsource(test)
        assert "_moved(" in body, (
            f"{test.__name__} asserts live corpus content without routing its "
            f"failure through `_moved` — the next engineer to see it fail will "
            f"not be told what to do")
