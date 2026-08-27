"""F2's regression-fixture catalogue for the modified-block-currency family.

`add-modified-block-currency-check`, Speckit feature
`020-modified-block-currency-fixtures`. **This file is NOT a second copy of
F1's rules.** F1 (`test_modified_block_currency.py`, 97 tests) already realizes
every scenario of the ratified delta; the mapping from packet § 3 to F1's tests
lives in `specs/020-modified-block-currency-fixtures/contracts/coverage-audit.md`
and eight of its eighteen rows are `satisfied` there and deliberately have no
test here. What is here is the nine rows that are not.

**No behaviour is added to the module by this file.** If a fixture below
reported something the delta forbids, that would be a defect in F1's
implementation and its own task — never a fixture adjusted until it agreed.

## The two reconstructions are REAL TEXT, recovered from this repository

- **`fixtures/modified-block-currency-history-351/`** — issue #351.
  `add-doxchat-model-intake`'s MODIFIED block for `doxBench model catalog and
  provider boundary` as it stood before its repair, against the canon of
  2026-08-25. Both recovered at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`,
  the parent of the repair `f68261f7` (merged `87d0b95a`, PR #358).
- **`fixtures/modified-block-currency-history-329/`** — issue #329.
  `add-release-inventory-drift-check`'s MODIFIED block for `Deterministic check
  families`, restating ONE of canon's eight scenarios while its own ADDED
  requirement brings SEVEN, so the file-level count stays flat at eight.
  Both recovered at `d5f447e89cf619fd12113bcf03525468ece4470d`, the parent of
  the archive `38b548d4` (merged `b03b9992`, PR #331).

`test_the_reconstructed_fixtures_are_the_history_they_claim` re-derives both
from git, so the claim is checked rather than asserted. Each tree's `README.md`
carries the runnable `git show` lines.

## The other five trees are SYNTHESIZED, and say so

`merge-gut`, `tokens`, `rewrap`, `fence` and `name-order` invent their text,
because this corpus carries no instance of any of those five shapes — which is
itself the reason the rules are worth pinning before one arrives. Each tree's
`README.md` says `SYNTHESIZED` on line 3.

## THE TWO ASSERTION CLASSES, and why every test pairs them

The ledger renders each unit truncated to `_QUOTE_WIDTH` (140) characters, so a
clause late in a long sentence is absent from the rendered finding BY DESIGN.

- **U-class** — asserted on the `Unit` objects the comparison returns
  (`_units`, which mirrors `_arm_ledger`'s kind filter). Used for full clause
  text and for kind discrimination.
- **F-class** — asserted on the emitted `Finding`'s `rule`, `severity`, `path`,
  `repo`, `family`. Used to prove the ARM fired, on the right path, naming the
  right subject.

Neither alone is enough: F-class alone passes over a build that reported the
WRONG units; U-class alone passes over a build whose arms never emit.

**Counts are never the assertion** (orchestrator decision D3) except where the
count IS the rule under test. That exception list has one home:
`specs/020-modified-block-currency-fixtures/data-model.md` § 4.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from doc_health import INFO, WARNING, Skip
from doc_health import modified_block_currency as mbc
from doc_health.promotion_fidelity import norm as norm_title

from conftest import FIXTURES, REPO_ROOT, make_ctx


# --------------------------------------------------------- the shared harness
#
# `ALL_TREES` is DERIVED, never listed. A hardcoded list rots the moment F3 or
# a later change adds a tree, and it rots silently — the partition invariant and
# the determinism sweep would simply stop covering the new one.

ALL_TREES = sorted(p.name for p in FIXTURES.glob("modified-block-currency*")
                   if p.is_dir())

# The trees THIS feature adds, in audit-row order. Used by the provenance and
# no-error sweeps, which must not silently shrink if a tree is deleted.
NEW_TREES = (
    "modified-block-currency-history-351",   # A1  · § 3.1   · reconstructed
    "modified-block-currency-history-329",   # A2  · § 3.2   · reconstructed
    "modified-block-currency-merge-gut",     # A3  · § 3.3   · synthesized
    "modified-block-currency-tokens",        # A6  · § 3.5   · synthesized
    "modified-block-currency-rewrap",        # A7  · § 3.6   · synthesized
    "modified-block-currency-fence",         # A11 · § 3.7d  · synthesized
    "modified-block-currency-name-order",    # A15 · § 3.10  · synthesized
)


def _tree(name):
    """The family's output over one fixture tree — a finding list, or a `Skip`."""
    return mbc.fam_modified_block_currency(make_ctx(name))


def _root(tree, repo):
    return FIXTURES / tree / repo


def _units(tree, repo, capability, requirement,
           kinds=(mbc.BODY, mbc.SCENARIO_BULLET)):
    """U-CLASS: the canon units of `requirement` the block does not carry.

    **Both sides are filtered to `kinds` BEFORE `carried`, exactly as
    `_arm_ledger` does.** Unfiltered this returns the union of the ledger's set
    and the title arm's — measured at 24 of 36 on the #329 tree against the
    ledger's 17 of 28 — so a U-class assertion would be reading a different set
    from the F-class finding it is paired with (research R15).
    """
    root = _root(tree, repo)
    basis = mbc.promoted(root, capability)[norm_title(requirement)]
    block = next(b for b in mbc.active_blocks(root)
                 if norm_title(b.title) == norm_title(requirement))
    return mbc.carried([u for u in basis.units if u.kind in kinds],
                       [u for u in block.units if u.kind in kinds])


def _texts(units):
    return [u.text for u in units]


# THE FIVE FINDING CLASSIFIERS.
#
# Each key is a fragment of ONE arm's own f-string and of no other's, and the
# set is verified to partition every finding over every tree
# (`test_every_finding_falls_into_exactly_one_class`).
#
# **NOT keyed on "declaration".** Measured: that key matches 3 findings across
# TWO classes — one marker defect ("a declaration that does not describe the
# block") and both blocks of the mutual-declaration ordering pair ("2
# declarations stand between them, and mutual declaration decides nothing").
# F1's own `_ledger` helper had to be narrowed away from the same trap.
CLASSIFIERS = {
    "titles": lambda r: "omits" in r and "scenarios" in r,
    "ledger": lambda r: "does not carry" in r and "body units" in r,
    "marker": lambda r: "carries a" in r and "marker by" in r,
    "ordering": lambda r: "the ordering of MODIFIED blocks" in r,
    "resolution": lambda r: "resolves to no promoted requirement" in r,
}


def _of(findings, cls):
    return [f for f in findings if CLASSIFIERS[cls](f.rule)]


def _for(findings, requirement):
    return [f for f in findings if repr(requirement) in f.rule]


# ---------------------------------------------------- the catalogue invariants


def test_the_tree_enumeration_finds_every_tree():
    """`ALL_TREES` is derived by glob, and this asserts the glob against an
    independent directory read. A hardcoded list would rot silently the next
    time a tree is added, taking the partition and determinism sweeps with it."""
    on_disk = sorted(p.name for p in FIXTURES.iterdir()
                     if p.is_dir() and p.name.startswith("modified-block-currency"))
    assert ALL_TREES == on_disk
    assert len(ALL_TREES) >= 13, ALL_TREES          # F1's six + this feature's seven
    for tree in NEW_TREES:
        assert tree in ALL_TREES, tree


def test_every_finding_falls_into_exactly_one_class():
    """DECISION O2 — the invariant that pays for re-spelling F1's `_titles` and
    `_ledger` in a second file.

    A cross-test-file import would depend on pytest's `prepend` import mode
    putting this directory on `sys.path`, which this suite should not start
    relying on. This is the stronger property anyway: every finding of every
    tree lands in exactly one class, so an arm's wording drifting in EITHER file
    fails loudly instead of silently reclassifying.
    """
    seen = 0
    for tree in ALL_TREES:
        out = _tree(tree)
        if isinstance(out, Skip):
            continue
        for f in out:
            seen += 1
            hits = [k for k, fn in CLASSIFIERS.items() if fn(f.rule)]
            assert len(hits) == 1, (tree, hits, f.rule[:120])
    assert seen > 20, f"only {seen} findings — discovery is broken, not clean"


def test_the_naive_declaration_key_would_collide():
    """The measurement behind the comment on `CLASSIFIERS`, kept as a test so
    the reason survives a refactor of the comment.

    `"declaration"` is the obvious key for the marker class and it is wrong: it
    reaches the mutual-declaration ORDERING finding too. Recording this as an
    executable fact is what stops a later session "simplifying" the keys back.
    """
    hit_classes = set()
    for tree in ALL_TREES:
        out = _tree(tree)
        if isinstance(out, Skip):
            continue
        for f in out:
            if "declaration" in f.rule:
                hit_classes |= {k for k, fn in CLASSIFIERS.items() if fn(f.rule)}
    assert hit_classes == {"marker", "ordering"}, hit_classes


# ============================================================================
# US1 · row A1 · packet § 3.1 — THE #351 TRUE POSITIVE, RECONSTRUCTED
#
# `add-doxchat-model-intake` was written 2026-08-21 against a pre-`02a71d6e`
# canon and was, on 2026-08-25, holding the deletion of six body clauses, two
# whole scenarios and one reverted scenario line. A human caught it; PR #358
# repaired it. This is that text.
# ============================================================================

T351 = "modified-block-currency-history-351"
R351 = "intakeFactory"
CAP351 = "ideation-dashboard"
REQ351 = "doxBench model catalog and provider boundary"
DELTA351 = ("openspec/changes/add-doxchat-model-intake/specs/"
            "ideation-dashboard/spec.md")

# The clauses `f68261f7` NAMES. Its message CLAIMS six body clauses and names
# these five; the sixth is never named, so these five are what is asserted.
CLAUSES_351 = (
    "SHALL remain exactly the three declared members",   # port-surface enumeration
    "MUST NOT be added as a fourth provider verb",
    "an `auto` entry that maps a turn to a model by declared role",
    "SHALL obtain its credential through the ratified broker lane",
    "thread file",
)


def test_the_351_block_omits_exactly_the_two_scenarios_canon_kept():
    """F-CLASS. The scenario arm on the real text, asserted on the NAMED titles.

    "some finding fired on that path" would pass over a build that reported the
    wrong titles — and the two it must name are the two the repair commit names:
    `The menu offers a routing rule` and `A fourth provider verb is proposed`.
    """
    hits = _of(_tree(T351), "titles")
    assert len(hits) == 1, [f.rule[:100] for f in hits]
    rule = hits[0].rule
    assert "The menu offers a routing rule" in rule
    assert "A fourth provider verb is proposed" in rule
    # the promoted spec it was read from is named — that is what a reader opens
    assert f"openspec/specs/{CAP351}/spec.md" in rule
    # ...and the block's OWN addition is not reported as a canon scenario lost
    assert "The intake affordance is submitted as a model" not in rule
    # ...nor are the five canon scenarios the block DID restate
    for kept in ("The browser loads model choices", "No model is configured",
                 "An unknown model id is submitted",
                 "A browser attempts a direct provider call",
                 "Hosted doxBench is opened"):
        assert kept not in rule, kept


def test_the_351_ledger_carries_every_clause_the_repair_commit_named():
    """U-CLASS for the clause text, F-CLASS for the arm.

    The repair commit CLAIMS six body clauses and NAMES five. Those five lie
    inside THREE of canon's sentences, because the ratified derivation splits a
    body paragraph into SENTENCES — so this asserts the clause TEXT found inside
    the reported units and never a row count (decision D3, research R3).

    The clause text is asserted U-class rather than on the rendered finding
    because the ledger truncates each unit at 140 characters and `thread file`
    sits past the cut (research R4).
    """
    missing = _units(T351, R351, CAP351, REQ351)
    blob = "\n".join(_texts(missing))
    for clause in CLAUSES_351:
        assert clause in blob, clause

    # F-class: exactly one ledger finding for this requirement — the ledger's
    # own promoted rule is "at most one finding per requirement, listing the
    # units", so here the count IS the obligation (data-model.md § 4).
    hits = _of(_for(_tree(T351), REQ351), "ledger")
    assert len(hits) == 1, [f.rule[:100] for f in hits]
    assert hits[0].severity == INFO
    assert hits[0].path == DELTA351
    # the hedge is in the finding, not only in the docs
    assert "CANNOT distinguish" in hits[0].rule


def test_the_351_reverted_scenario_line_is_reported():
    """§ 3.1's "one reverted scenario line".

    `f68261f7` records that "every loaded editor MUST remain usable" was
    narrowed to "the Outline and Document editors MUST remain usable". The
    narrowed line is a DIFFERENT unit, so canon's is uncarried — and the same
    defect appears on a WHEN line, where the block drifted canon's "hosted
    plane" to "hosted/read-only plane".
    """
    texts = _texts(_units(T351, R351, CAP351, REQ351))
    assert "**AND** every loaded editor MUST remain usable" in texts
    assert "**WHEN** doxBench runs on the hosted plane" in texts


def test_the_351_widened_bullet_is_reported_although_the_block_contains_it():
    """ROW A5(b) — § 3.4's mechanism END TO END, on the real instance.

    This is also § 6.4 of the packet: the single-bullet residue PR #358's manual
    `canon ⊆ intake ⊆ B` verification reported. Canon's bullet is a STRICT
    PREFIX of the block's replacement, so a containment rule yields zero here —
    on the very defect a human had to repair by hand.

    The containment relation is CHECKED in the test body, not claimed in the
    docstring: a fixture edit that broke the prefix relation would otherwise
    leave this test passing while testing nothing.
    """
    canon_bullet = ("**THEN** the selector MUST show exactly the available "
                    "catalog entries and their data-handling badges")
    root = _root(T351, R351)
    block = next(b for b in mbc.active_blocks(root)
                 if norm_title(b.title) == norm_title(REQ351))
    widened = [u.text for u in block.units
               if u.kind == mbc.SCENARIO_BULLET and canon_bullet in u.text]
    assert len(widened) == 1, widened          # the fixture's containment premise
    assert widened[0] != canon_bullet, "the premise is a STRICT prefix"
    assert widened[0].startswith(canon_bullet)

    # ...and the family reports canon's bullet anyway.
    assert canon_bullet in _texts(_units(T351, R351, CAP351, REQ351))


def test_the_351_findings_land_on_the_delta_path_at_the_right_severities():
    """F-CLASS. Non-empty FIRST: on an empty list every assertion below is
    vacuous, and an empty list is exactly what a broken discovery returns."""
    findings = _tree(T351)
    assert findings, "a vacuous pass is not a pass"
    assert {f.path for f in findings} == {DELTA351}
    assert {f.repo for f in findings} == {R351}
    assert {f.family for f in findings} == {mbc.FAMILY}
    assert {f.severity for f in _of(findings, "titles")} == {WARNING}
    assert {f.severity for f in _of(findings, "ledger")} == {INFO}
    assert not [f for f in findings if f.severity in ("error", "critical")]


# ============================================================================
# US1 · row A2 · packet § 3.2 — THE #329 ONE-OF-EIGHT CASE, RECONSTRUCTED
# ============================================================================

T329 = "modified-block-currency-history-329"
R329 = "driftFactory"
CAP329 = "doc-health"
REQ329 = "Deterministic check families"
DELTA329 = ("openspec/changes/add-release-inventory-drift-check/specs/"
            "doc-health/spec.md")

OMITTED_329 = (
    "Lifecycle conformance checks fire",
    "A register carries staged status",
    "Drift checks fire",
    "Catalog conformance checks fire",
    "Routing conformance checks fire",
    "Origin conformance checks fire",
    "Roster composition is checked across domains",
)


def test_the_329_block_omits_all_seven_titles_by_name():
    """F-CLASS, title by title. Seven titles, seven assertions — a build that
    reported the wrong seven would pass any count."""
    hits = _of(_tree(T329), "titles")
    assert len(hits) == 1, [f.rule[:100] for f in hits]
    rule = hits[0].rule
    for title in OMITTED_329:
        assert title in rule, title
    # the one the block DID restate is not named as missing
    assert "A run executes the check families" not in rule
    assert f"openspec/specs/{CAP329}/spec.md" in rule


def test_the_329_flat_file_level_count_buys_no_silence():
    """WHY COUNTING CANNOT SEE THIS CLASS — and the one place a count IS the
    assertion (data-model.md § 4).

    Canon states EIGHT scenarios for the requirement. The delta FILE contains
    EIGHT: one restated, plus seven brought by the change's own ADDED
    requirement `Release-inventory drift`. Count the file and nothing moved.
    The family fires anyway, because it accounts PER REQUIREMENT.
    """
    root = _root(T329, R329)
    basis = mbc.promoted(root, CAP329)[norm_title(REQ329)]
    delta_text = (root / DELTA329).read_text()

    assert len(basis.scenario_titles) == 8
    assert delta_text.count("#### Scenario:") == 8
    # ...and seven of canon's eight are gone from the MODIFIED block.
    assert _of(_tree(T329), "titles"), "the flat count must not buy silence"


def test_the_329_ledger_names_canon_s_body_sentences():
    """U-CLASS. Canon's enumeration sentence and its "Four of the seventeen"
    sentence are both uncarried, and bullets from more than one of the seven
    dropped scenarios are reported — so the ledger is reading the whole
    requirement, not just its first paragraph.

    The two-body-sentence SHAPE here coincides with the packet's own § 2.1 block
    (which also fails to carry two body sentences). That is a coincidence of
    form only; this fixture is NOT evidence about § 2.1.
    """
    missing = _units(T329, R329, CAP329, REQ329)
    bodies = [u.text for u in missing if u.kind == mbc.BODY]
    bullets = [u for u in missing if u.kind == mbc.SCENARIO_BULLET]

    assert any("seventeen check families" in b for b in bodies), bodies
    assert any("Four of the seventeen" in b for b in bodies), bodies
    # bullets from at least three distinct dropped scenarios
    assert len({u.scenario for u in bullets}) >= 3, {u.scenario for u in bullets}
    assert any("emit a drift finding identifying what diverged" in u.text
               for u in bullets)
    assert any("registers are a promoted organized-state home" in u.text
               for u in bullets)


# ---------------------------------- the provenance of both, checked against git


RECONSTRUCTIONS = (
    # (tree, repo, sha, delta_rel, canon_rel, requirement)
    (T351, R351, "bcfc26a0d2f182c652ed9054b82210ccbee8124a", DELTA351,
     f"openspec/specs/{CAP351}/spec.md", REQ351),
    (T329, R329, "d5f447e89cf619fd12113bcf03525468ece4470d", DELTA329,
     f"openspec/specs/{CAP329}/spec.md", REQ329),
)


def _requirement_section(text, title):
    """The `### Requirement: <title>` section, to the line before the next one."""
    out, inside = [], False
    for line in text.splitlines(keepends=True):
        if line.startswith("### Requirement:"):
            if inside:
                break
            inside = line.strip() == f"### Requirement: {title}"
        if inside:
            out.append(line)
    return "".join(out)


def _git(*args):
    return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True, text=True)


@pytest.mark.parametrize("tree,repo,sha,delta_rel,canon_rel,requirement",
                         RECONSTRUCTIONS,
                         ids=[r[0].rsplit("-", 1)[-1] for r in RECONSTRUCTIONS])
def test_the_reconstructed_fixtures_are_the_history_they_claim(
        tree, repo, sha, delta_rel, canon_rel, requirement):
    """A fixture that CLAIMS to be history is worth nothing unless the claim is
    checked. This re-derives both from git.

    THE TWO FAILURE MODES ARE TOLD APART BY ASKING THE REPOSITORY, exactly as
    `test_ideation_readiness.py` does: a COMPLETE checkout that cannot resolve
    the SHA — or resolves it and disagrees — is a DEFECT and fails naming the
    file; a TRUTHFULLY SHALLOW clone that cannot resolve it is a fact about the
    clone and skips. CI checks out with `fetch-depth: 0`, so the resolving path
    is the one that runs there.

    `git` is not among the hermeticity guard's refused binaries (it covers
    `nlm`, `gh` and the session `git push`), and two doc-health tests already
    shell out to it.
    """
    resolved = _git("rev-parse", "--verify", f"{sha}^{{commit}}")
    if resolved.returncode != 0:
        shallow = _git("rev-parse", "--is-shallow-repository")
        if shallow.stdout.strip() == "true":
            pytest.skip(f"shallow clone cannot resolve {sha[:12]} — a fact "
                        f"about this checkout, not about the fixture")
        pytest.fail(f"a COMPLETE checkout cannot resolve {sha[:12]}, which "
                    f"{tree}/README.md names as its source: "
                    f"{resolved.stderr.strip()}")

    root = _root(tree, repo)

    # the delta file is copied WHOLE (decision O4) — byte for byte
    shown = _git("show", f"{sha}:{delta_rel}")
    assert shown.returncode == 0, shown.stderr
    assert shown.stdout == (root / delta_rel).read_text(), (
        f"{tree}: the delta fixture is not {sha[:12]}'s text")

    # canon carries the REQUIREMENT verbatim inside synthetic scaffolding
    # (decision O3) — so the comparison is scoped to the section
    shown = _git("show", f"{sha}:{canon_rel}")
    assert shown.returncode == 0, shown.stderr
    expected = _requirement_section(shown.stdout, requirement)
    assert expected.strip(), f"{requirement!r} not found at {sha[:12]}"
    actual = _requirement_section((root / canon_rel).read_text(), requirement)
    assert actual.strip() == expected.strip(), (
        f"{tree}: the canon requirement is not {sha[:12]}'s text")
