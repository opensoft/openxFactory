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

from doc_health import ERROR, INFO, WARNING, Skip
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
#
# **THE SIXTH KEY, AND WHY THE OTHER FIVE NEEDED A GUARD** — added 2026-08-28
# with `add-unclassified-finding-class`'s fifth finding class. That class's
# finding QUOTES, verbatim, the rule text its map could not place, so a drift
# finding's text CONTAINS an arm's. The five probes above are unanchored
# substring tests, so every one of them would match a drift finding through its
# quotation and `test_every_finding_falls_into_exactly_one_class` would read two
# hits for one finding. `_arm` excludes the drift shape from each of them.
#
# **THIS IS A DECLARED COUPLING TO THE PRODUCTION MODULE.** `_DRIFT_OPENING`
# below is `modified_block_currency._DRIFT_RULE`'s opening phrase, spelled out
# here rather than imported for the same reason every other key is spelled out:
# a wording drifting in EITHER file must fail loudly instead of silently
# reclassifying. If that phrase changes, this line changes with it — and
# `test_the_drift_classifier_matches_the_module_s_own_opening` is what says so.
_DRIFT_OPENING = "this family's own class map has no pattern for "


def _arm(probe):
    return lambda r: not r.startswith(_DRIFT_OPENING) and probe(r)


CLASSIFIERS = {
    "titles": _arm(lambda r: "omits" in r and "scenarios" in r),
    "ledger": _arm(lambda r: "does not carry" in r and "body units" in r),
    "marker": _arm(lambda r: "carries a" in r and "marker by" in r),
    "ordering": _arm(lambda r: "the ordering of MODIFIED blocks" in r),
    "resolution": _arm(lambda r: "resolves to no promoted requirement" in r),
    "drift": lambda r: r.startswith(_DRIFT_OPENING),
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
    # F1's six + F2's seven + F5's one (`026-unplaced-finding-drift`) = 14 on
    # disk today. A FLOOR, never an equality: this must not fall due the next
    # time a feature adds a tree.
    assert len(ALL_TREES) >= 14, ALL_TREES
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

    # THE SIXTH KEY, EXERCISED. The map places everything over every tree above,
    # so `drift` matches nothing there and the partition would say nothing about
    # it. The class fires only under a drifted map — one entry removed from
    # `_CLASS_PATTERNS`, which is the live condition it reports — so the drift is
    # induced here, and the drift finding is required to match EXACTLY ONE key
    # despite carrying an arm's whole rule text inside it.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(mbc, "_CLASS_PATTERNS", tuple(
            entry for entry in mbc._CLASS_PATTERNS
            if entry[0] != mbc.CLASS_LEDGER))
        drifted = _tree("modified-block-currency-unplaced")
        drift = [f for f in drifted if mbc.classify(f) == mbc.CLASS_DRIFT]
        assert len(drift) == 1, [f.rule[:120] for f in drift]
        assert "does not carry" in drift[0].rule, (
            "the quotation is missing, so the exclusivity below is vacuous")
        hits = [k for k, fn in CLASSIFIERS.items() if fn(drift[0].rule)]
        assert hits == ["drift"], hits


def test_the_drift_classifier_matches_the_module_s_own_opening():
    """The declared coupling above, asserted rather than commented.

    `_DRIFT_OPENING` is typed out in this file on the same argument every other
    key is: comparing it with the module's own constant catches the wording
    drifting in EITHER file, where importing it would silently follow one of
    them."""
    assert mbc._DRIFT_RULE.startswith(_DRIFT_OPENING)
    assert mbc._CLASS_PATTERNS[-1][0] == mbc.CLASS_DRIFT


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
    # More than one class, and specifically the two the arms' own wording puts
    # in reach. Not pinned to an exact SET, because a fixture whose requirement
    # TITLE contains the word drags the ledger in too — which this feature's own
    # `name-order` tree does, making the naive key worse still rather than
    # better.
    assert len(hit_classes) > 1, hit_classes
    assert {"marker", "ordering"} <= hit_classes, hit_classes


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
    vacuous, and an empty list is exactly what a broken discovery returns.

    The titles severity FLIPPED to `error` 2026-08-31 (issue #357); it was
    `warning` through the advisory launch. The ledger arm is untouched by
    that flip (O8), so it is still the one class this fixture's `not
    critical` sweep excludes."""
    findings = _tree(T351)
    assert findings, "a vacuous pass is not a pass"
    assert {f.path for f in findings} == {DELTA351}
    assert {f.repo for f in findings} == {R351}
    assert {f.family for f in findings} == {mbc.FAMILY}
    assert {f.severity for f in _of(findings, "titles")} == {ERROR}
    assert mbc._LAUNCH_SEVERITY == ERROR
    assert {f.severity for f in _of(findings, "ledger")} == {INFO}
    assert not [f for f in findings if f.severity == "critical"]


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


# ============================================================================
# US3 · row A3 · packet § 3.3 — THE `Merged into` GUT
#
# THE ONE TRUE HOLE the audit found. The delta's rule — "A `Merged into` marker
# names titles only, so a bullet a merge makes redundant is a declared removal,
# not a permanent editorial row — but it has to be declared as a bullet, one at
# a time" — was asserted nowhere. F1's only end-to-end merge case has a
# one-bullet source that the block carries, so it is quiet in both arms.
# ============================================================================

TMERGE = "modified-block-currency-merge-gut"
RMERGE = "mergeFactory"
CAPMERGE = "merge-gut"
GUT = "A merge that guts its source"
DECLARED = "A merge that declares its redundant bullets"


def test_a_merge_marker_does_not_declare_the_bullets_it_makes_redundant():
    """The gut: a four-bullet scenario merged away, two of its bullets carried.

    The ledger reports EXACTLY the two the replacement does not carry, and says
    nothing about the two it does. A `Merged into` marker names TITLES.
    """
    hits = _of(_for(_tree(TMERGE), GUT), "ledger")
    assert len(hits) == 1, [f.rule[:100] for f in hits]
    rule = hits[0].rule
    assert "**AND** it MUST do the second thing" in rule
    assert "**AND** it MUST do the third thing" in rule
    # the bullet the replacement DOES carry is not reported...
    assert "it MUST do the first thing" not in rule
    # ...and neither is the untouched sibling scenario's bullet
    assert "it MUST survive" not in rule
    assert hits[0].severity == INFO


def test_the_scenario_arm_is_quiet_because_the_merge_marker_is_valid():
    """The other half of § 3.3: the marker is well formed and names an ABSENT
    title, so it declares what it says it declares — the scenario arm is quiet
    and no marker defect is emitted. Only the BULLETS survive as a finding."""
    findings = _for(_tree(TMERGE), GUT)
    assert findings, "a vacuous pass is not a pass"
    assert _of(findings, "titles") == []
    assert _of(findings, "marker") == []


def test_a_merge_companion_naming_its_redundant_bullets_silences_them():
    """§ 3.3's companion case. The same merge shape, PLUS a `Removed from canon`
    marker naming the two redundant bullets one at a time — which is the
    deliberation the class deserves. Nothing is reported.

    One of the two named bullets itself contains a backtick (it cites
    `openxFactory`), so its code span carries a LONGER FENCE — which makes this
    case carry § 3.7's fence rule end to end as well.
    """
    assert _for(_tree(TMERGE), DECLARED) == []


def test_the_merge_companion_is_quiet_because_of_its_marker_not_by_carriage():
    """SILENCE PROVES NOTHING UNLESS THE CAUSE IS REMOVED AND THE NOISE RETURNS.

    Rebuild the companion's block WITHOUT its `Removed from canon` marker
    paragraph and derive units from the result: the two bullets are then
    uncarried. So the quiet above is caused by the declaration, not by the
    block having carried them somewhere.
    """
    root = _root(TMERGE, RMERGE)
    basis = mbc.promoted(root, CAPMERGE)[norm_title(DECLARED)]
    block = next(b for b in mbc.active_blocks(root)
                 if norm_title(b.title) == norm_title(DECLARED))

    # with the marker: the two bullets are absent from the block AND suppressed
    kinds = (mbc.BODY, mbc.SCENARIO_BULLET)
    uncarried = mbc.carried([u for u in basis.units if u.kind in kinds],
                            [u for u in block.units if u.kind in kinds])
    assert len(uncarried) == 2, _texts(uncarried)   # absent, before suppression
    suppressed, defective = mbc.suppression(block.markers, basis.units,
                                            block.units)
    assert defective == [], defective
    assert all(u.pair() in suppressed for u in uncarried), _texts(uncarried)

    # without the marker: nothing suppresses them, and the arm would report both
    kept = [m for m in block.markers if m.form != "removed"]
    suppressed_without, _ = mbc.suppression(kept, basis.units, block.units)
    assert not any(u.pair() in suppressed_without for u in uncarried)


# ============================================================================
# US4 · row A5(a) · packet § 3.4 — CONTAINMENT AT EITHER END
#
# F1 widens at the END only, though its own SC-003 says "either end". The
# end-to-end half is fixture A's real instance (T014); these are the two
# synthetic directions.
# ============================================================================

CANON_UNIT = ("**THEN** the selector MUST show exactly the available catalog "
              "entries and their data-handling badges")


def test_a_block_unit_widened_before_canon_s_does_not_carry_it():
    """PREFIX widening — text added BEFORE canon's unit. F1's test adds text
    after it only, so a one-sided implementation would pass F1's suite."""
    canon = [mbc.Unit(mbc.SCENARIO_BULLET, CANON_UNIT, "S")]
    widened = [mbc.Unit(mbc.SCENARIO_BULLET,
                        "**THEN** where a provider lane resolves, " + CANON_UNIT,
                        "S")]
    assert CANON_UNIT in widened[0].text, "the containment premise"
    assert mbc.carried(canon, widened) == canon


def test_a_block_unit_widened_at_both_ends_does_not_carry_it():
    """BOTH ends at once, which is neither of the one-sided cases."""
    canon = [mbc.Unit(mbc.SCENARIO_BULLET, CANON_UNIT, "S")]
    widened = [mbc.Unit(mbc.SCENARIO_BULLET,
                        "**THEN** where a provider lane resolves, " + CANON_UNIT
                        + " and their provider lanes", "S")]
    assert CANON_UNIT in widened[0].text, "the containment premise"
    assert mbc.carried(canon, widened) == canon


# ============================================================================
# US4 · row A6 · packet § 3.5 — TOKENIZATION
# ============================================================================

TTOK = "modified-block-currency-tokens"
RTOK = "tokenFactory"
CAPTOK = "token-cases"
REQTOK = "Tokens with internal periods never end a sentence"


def test_no_unit_boundary_falls_inside_a_versioned_token():
    """`contract-v1.45` is the token shape F1's fixture lacks: its period sits
    BETWEEN DIGITS, which a naive `\\d\\.\\d` sentence guard waves through while
    a leading-dot or word-boundary rule catches `.openspec.yaml`.

    Run END TO END through the family, so a wiring regression cannot hide behind
    a green unit test. The three tokened sentences are restated VERBATIM by the
    block, so they must not be reported at all — and no reported unit may be a
    fragment of a backticked span.
    """
    findings = _tree(TTOK)
    assert findings, "a vacuous pass is not a pass"

    # ASSERTED POSITIVELY, on canon's own derivation. The first cut of this test
    # only checked that the tokens were ABSENT from the ledger — and the
    # mutation round killed it: strip the backticks from `contract-v1.45` in BOTH
    # documents and the sentence splits into two units on each side, which still
    # MATCH, so nothing is reported and the negative assertion still passed. A
    # negative cannot see a boundary that moved on both sides at once.
    root = _root(TTOK, RTOK)
    canon = mbc.promoted(root, CAPTOK)[norm_title(REQTOK)]
    for token, whole in (
        (".openspec.yaml",
         "The jump SHALL read `.openspec.yaml` for its repository name."),
        ("promotion_fidelity.py",
         "The disposition reader SHALL be the one `promotion_fidelity.py` "
         "already implements."),
        ("contract-v1.45",
         "A consumer SHALL pin `contract-v1.45` exactly rather than a movable "
         "tag."),
    ):
        # BODY units only: `.openspec.yaml` is cited in a scenario bullet too,
        # and this assertion is about the body's sentence split.
        holders = [u for u in canon.units
                   if u.kind == mbc.BODY and token in u.text]
        assert len(holders) == 1, (token, _texts(holders))
        assert holders[0].text == whole, (token, holders[0].text)

    # ...and the block restates all three verbatim, so none is reported.
    rule = _of(_for(findings, REQTOK), "ledger")[0].rule
    for token in ("contract-v1.45", ".openspec.yaml", "promotion_fidelity.py"):
        assert token not in rule, token
    # and no unit anywhere in the catalogue is a backtick fragment
    for f in findings:
        for chunk in f.rule.split("'"):
            assert chunk.count("`") % 2 == 0 or "``" in chunk, chunk[:80]


def test_each_tokenized_body_bullet_is_its_own_reported_unit():
    """§ 3.5's "each bullet SHALL be one unit with its list marker stripped".

    Canon carries a three-item bullet list and the block carries one, so EXACTLY
    TWO body units are reported — one unit carrying both dropped bullets, or
    three, is the defect under test, which is why the count is the assertion
    here (data-model.md § 4).
    """
    bodies = [u for u in _units(TTOK, RTOK, CAPTOK, REQTOK)
              if u.kind == mbc.BODY]
    bullets = [u.text for u in bodies if u.text.startswith("a reader MUST")]
    assert len(bullets) == 2, bullets
    assert "a reader MUST resolve the repository id before it reads the pin" in bullets
    assert "a reader MUST record which contract release it resolved" in bullets
    # the list marker is stripped
    assert not any(b.startswith(("-", "*", "+")) for b in bullets)


def test_a_note_edited_in_its_third_sentence_is_reported_once():
    """§ 3.5'S LAST CLAUSE, AND THE ONE F1 DOES NOT HAVE.

    Canon's dated bold note carries FOUR sentences. The block restates it with
    the THIRD sentence amended. The note is reported ONCE, as one undivided
    unit — no fragment of any other sentence of it appears separately.

    F1's block DROPS its two-sentence note, and dropped is the weaker case: an
    implementation that split a note into sentences would report a dropped note
    as N rows, but would report an EDITED note as 1 row out of N. Only the edit
    distinguishes "one undivided unit" from "sentence-wise comparison that
    happened to agree".
    """
    notes = [u for u in _units(TTOK, RTOK, CAPTOK, REQTOK)
             if u.text.startswith("**CORRECTED")]
    assert len(notes) == 1, _texts(notes)
    note = notes[0].text
    # it really is the whole four-sentence paragraph, not its first sentence
    assert note.count(" It carries four sentences.") == 1
    assert note.endswith("last.**")
    # and the sentences AROUND the edit are not reported on their own
    rule = _of(_for(_tree(TTOK), REQTOK), "ledger")[0].rule
    assert rule.count("CORRECTED 2026-08-27") == 1


def test_masking_governs_boundaries_and_not_equality():
    """A DISTINCT property from the mask's job, separated deliberately.

    The mask decides where units END. It says nothing about whether two units
    are EQUAL — so a sentence whose text is altered INSIDE its backticks is
    still ONE unit, and it is uncarried. Conflating the two is how a "RED stage
    2" ends up asserting that a test still passes.
    """
    canon = mbc.derive_units([
        "A consumer SHALL pin `contract-v1.45` exactly rather than a movable tag."
    ])[0]
    altered = mbc.derive_units([
        "A consumer SHALL pin `contract-v1.46` exactly rather than a movable tag."
    ])[0]
    assert len(canon) == 1 and len(altered) == 1        # boundaries: one each
    assert mbc.carried(canon, altered) == canon         # equality: not carried


# ============================================================================
# US4 · row A7 · packet § 3.6 — RE-WRAP QUIET, END TO END
# ============================================================================

TWRAP = "modified-block-currency-rewrap"
RWRAP = "rewrapFactory"


def test_a_rewrapped_scenario_complete_block_reports_nothing_through_the_family():
    """THE CASE LINE-LEVEL MATCHING FAILS, asserted through the family.

    F1 asserts this at `mbc.carried()` on units its test body synthesizes from
    canon, and its `-quiet` tree carries no MODIFIED block at all — so a wiring
    regression between `derive_units` and the arms leaves both F1 tests green.
    This block restates its requirement COMPLETELY while re-wrapping every
    paragraph, bullet and scenario line, one of them mid-sentence.
    """
    assert _tree(TWRAP) == []


def test_the_rewrap_tree_is_not_reported_skipped():
    """THE TWO SILENCES ARE DIFFERENT STATES. Canon's skip rule is "cannot run",
    not "found nothing" — and a tree that returned `Skip` would satisfy the
    `== []` above under a naive comparison. So the tree is shown to have RUN:
    it has an `openspec/changes/` directory and a MODIFIED block in it.
    """
    out = _tree(TWRAP)
    assert not isinstance(out, Skip)
    blocks = mbc.active_blocks(_root(TWRAP, RWRAP))
    assert len(blocks) == 1, blocks
    assert blocks[0].units, "the block was derived, not merely discovered"


# ============================================================================
# US4 · row A11 · packet § 3.7(d) — THE LONGER FENCE, END TO END
# ============================================================================

TFENCE = "modified-block-currency-fence"
RFENCE = "fenceFactory"
CAPFENCE = "fence-cases"
LONGER = "A longer fence names the whole unit"
SINGLE = "A single backtick names a fragment"
CLAUSE = ("An adapter that reaches a hosted provider SHALL obtain its "
          "credential through the `openxFactory` broker lane.")


def test_a_longer_fenced_named_unit_suppresses_the_whole_unit():
    """§ 3.7's fence clause END TO END. F1 pins it at `extract_code_spans`; no
    fixture exercised it through the family, and none showed it SUPPRESSING.

    The named unit cites `openxFactory`, so a single-backtick span would end at
    its first inner backtick and name a fragment. Fenced with a longer run, it
    names the unit, and the block that dropped that unit is quiet.
    """
    assert _for(_tree(TFENCE), LONGER) == []
    # ...and the premise: the clause really is absent from the block
    assert CLAUSE in _texts(_units(TFENCE, RFENCE, CAPFENCE, SINGLE))


def test_the_inner_backtick_does_not_truncate_the_named_unit():
    """THE PAIR THAT MAKES THE FENCE RULE FALSIFIABLE.

    A second requirement names the SAME clause with a SINGLE-backtick span,
    which under CommonMark ends at the clause's first inner backtick. The marker
    therefore names a FRAGMENT that matches no canon unit — so it suppresses
    nothing and the clause is reported.

    It is NOT reported as a marker defect: the delta reports a marker only when
    it names a unit the block STILL CARRIES, and a name matching no canon unit
    declares nothing and is silent. Without this sibling, a build that ignored
    fences entirely and matched the whole paragraph would pass the test above.
    """
    findings = _for(_tree(TFENCE), SINGLE)
    hits = _of(findings, "ledger")
    assert len(hits) == 1, [f.rule[:100] for f in hits]
    assert "broker lane" in hits[0].rule
    assert _of(findings, "marker") == []

    # the mechanism, directly: the single-backtick marker's names are a fragment
    root = _root(TFENCE, RFENCE)
    block = next(b for b in mbc.active_blocks(root)
                 if norm_title(b.title) == norm_title(SINGLE))
    assert len(block.markers) == 1, block.markers
    named = block.markers[0].names
    assert named and all(n != mbc.normalize(CLAUSE) for n in named), named
    assert any(n.endswith("through the") for n in named), named


# ============================================================================
# US4 · row A15 · packet § 3.10 — ORDERING BY DECLARATION, AGAINST NAME ORDER
# ============================================================================

TORDER = "modified-block-currency-name-order"
RORDER = "orderFactory"
DECLARER = "openspec/changes/add-zz-first/specs/name-order/spec.md"
EARLIER = "openspec/changes/add-aa-second/specs/name-order/spec.md"


def test_the_declaration_orders_the_pair_against_name_order():
    """§ 3.10'S LAST CLAUSE, WHICH F1 DOES NOT DISCHARGE AND SAYS SO.

    F1's `test_no_date_folder_or_created_field_decides_the_ordering` records in
    its own docstring that its fixture "sorts BEFORE ... by name and by any date
    a fixture could carry, AND THE DECLARATION POINTS THE SAME WAY", so the
    fixture cannot discriminate; it falls back to a structural grep whose
    forbidden patterns cover dates and `created:` but say nothing about ordering
    by FOLDER NAME or CHANGE-ID NAME — which the delta prohibits in the same
    breath as dates.

    Here `add-zz-first` DECLARES and is therefore the LATER writer, while
    sorting LAST by name. So:

    - its block is measured against `add-aa-second`'s OUTCOME, not canon, and
      the addition it fails to carry is reported against ITS path;
    - `add-aa-second`'s own block is measured against canon and is quiet.

    **Under name-ascending ordering the roles invert and this test fails.**
    """
    findings = _tree(TORDER)
    assert findings, "a vacuous pass is not a pass"

    # exactly one finding, and it lands on the DECLARER's path
    assert {f.path for f in findings} == {DECLARER}, [f.path for f in findings]
    hits = _of(findings, "ledger")
    assert len(hits) == 1, [f.rule[:100] for f in hits]

    # the basis SUBSTITUTION is visible in the finding: the spec it names is the
    # SIBLING'S DELTA, not the promoted spec
    assert EARLIER in hits[0].rule, hits[0].rule[:300]
    assert "openspec/specs/name-order/spec.md" not in hits[0].rule
    # ...and what it reports is the sibling's addition
    assert "The earlier writer adds this sentence" in hits[0].rule

    # the ordering arm itself is quiet: exactly one declaration between two
    # ratified writers IS the ordered case, so there is nothing to report
    assert _of(findings, "ordering") == []


def test_the_name_order_fixture_would_invert_under_name_ordering():
    """THE DISCRIMINATION, made explicit so a reader can see it is real.

    Sorted by change id, `add-aa-second` comes first — so a build that called
    the alphabetically-first change the earlier writer would make
    `add-aa-second` the declarer's counterpart and report against
    `add-aa-second`'s path instead. The fixture's ids disagree with its
    declaration deliberately; `README.md` says not to "tidy" them.
    """
    root = _root(TORDER, RORDER)
    changes = sorted(b.change for b in mbc.active_blocks(root))
    assert changes == ["add-aa-second", "add-zz-first"]
    # the DECLARER is the one that sorts LAST
    declared = mbc.declarations(root, mbc.active_blocks(root))
    assert ("add-zz-first", "add-aa-second") in declared, declared
    assert ("add-aa-second", "add-zz-first") not in declared, declared
    # and the finding is on the declarer, i.e. on the name-LAST change
    assert {f.path for f in _tree(TORDER)} == {DECLARER}


# ============================================================================
# US4 · row A10 · packet § 3.7(c) — THE FORM ANCHOR, ON THE REAL PACKET
# ============================================================================


def test_the_packets_own_marker_templates_are_not_marker_form():
    """ROW A10 CLAIMED THIS AND NOTHING ASSERTED IT.

    The audit's first pass said "the anchor is asserted against this packet's
    OWN delta prose, which promotes into canon". It was not: F1's
    `test_the_deltas_own_fenced_marker_examples_never_reach_the_parser` asserts
    over a fenced block written inside its own test body, and the packet sets
    its two templates out as `- ` BULLETS — ordinary carriage units that the
    fenced-block exemption never reaches.

    The delta's own argument for the strict anchor is precisely that these
    paragraphs promote into canon and "a looser test would read them as markers
    and exempt them from carriage — the check quietly declining to check the
    paragraphs that define it". This is the test that checks it, against the
    real file.

    **RE-AIMED BY THE ARCHIVE ACT (2026-08-27), NOT DELETED, AND THE RE-AIM IS
    THE CLAIM ARRIVING.** As written this read the packet's own ACTIVE delta at
    `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`.
    That packet archived, so the path is gone — and the two template bullets are
    now exactly where the paragraph above warned they were going: PROMOTED, in
    `openspec/specs/doc-health/spec.md`. So the subject moves one document over,
    and what it reads is now the promoted text rather than a prediction about it.
    The file read is now canon; nothing else about the test
    changed, and the count floor of two still fails on a file edit that moves
    them.
    """
    promoted = (REPO_ROOT / "openspec/specs/doc-health/spec.md").read_text()
    bullets = [line for line in promoted.splitlines()
               if re.match(r"^- ``?\*\*(Removed from canon by|Merged into)", line)]
    assert len(bullets) == 2, bullets     # a file edit that moves them fails here

    for bullet in bullets:
        body = re.sub(r"^- ", "", bullet)
        assert mbc.parse_marker(mbc.normalize(body)) is None, body
        # ...and it is not marker-form with the list marker left on either
        assert mbc.parse_marker(mbc.normalize(bullet)) is None, bullet


# ============================================================================
# US2 · rows A1–A18 — THE AUDIT, CHECKED RATHER THAN READ
# ============================================================================

AUDIT = (REPO_ROOT / "specs/020-modified-block-currency-fixtures"
         / "contracts/coverage-audit.md")
F1_TESTS = REPO_ROOT / "tests/doc-health/test_modified_block_currency.py"


def test_no_audit_row_cites_a_test_that_does_not_exist():
    """The audit's citations are a LIVE REFERENCE, not prose.

    Harvested from BACKTICKED SPANS ONLY. A bare `test_[a-z0-9_]+` scan over the
    whole file is permanently red: the audit's prose names the MODULE path, so
    the scan harvests `test_modified_block_currency` — a file, not a test
    function — and a reader would then be sent off to "fix the audit" for a
    defect in the harvester.

    The floor of thirty is a guard against the opposite failure: a regex that
    silently matches nothing passes every membership check ever written.
    """
    cited = set(re.findall(r"`(test_[a-z0-9_]+)`", AUDIT.read_text()))
    assert len(cited) > 30, f"only {len(cited)} names harvested — check the regex"

    # BOTH files: the rows cite F1's tests, and the closing ledger cites F2's
    # own — including the three tests that read this very audit.
    defined = set()
    for path in (F1_TESTS, Path(__file__)):
        defined |= set(re.findall(r"^def (test_[a-z0-9_]+)", path.read_text(),
                                  re.M))
    missing = sorted(cited - defined)
    assert not missing, f"audit cites tests that exist nowhere: {missing}"


def test_every_packet_section_three_item_has_an_audit_row():
    """SC-007. Fourteen items, none unaccounted for.

    Read off the `§ 3 item` column, which is the audit's own answer to "is every
    obligation accounted for". § 3.7 is split across five rows because it
    carries eleven distinct obligations, so items and rows are not one to one.
    """
    text = AUDIT.read_text()
    for item in ("3.1", "3.2", "3.3", "3.3a", "3.4", "3.5", "3.6",
                 "3.7(a)", "3.7(b)", "3.7(c)", "3.7(d)", "3.7(e–k)",
                 "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"):
            assert f"**{item}**" in text, item

    # every row carries exactly one verdict, and the tallies match the bodies
    # THE MAIN TABLE ONLY. A row is one of the eighteen iff it carries a BOLDED
    # verdict; the closing ledger repeats the row ids with unbolded verdicts in
    # a different column layout, and sweeping those in made this test count 28.
    rows = [ln for ln in text.splitlines()
            if re.match(r"^\| \*\*A\d+\*\*", ln)
            and re.search(r"\| \*\*(satisfied|partial|gapped)", ln)]
    assert len(rows) == 18, len(rows)
    verdicts = [re.findall(r"\| \*\*(satisfied, extended|satisfied|partial|gapped)\*\*", r)
                for r in rows]
    assert all(len(v) == 1 for v in verdicts), verdicts
    flat = [v[0] for v in verdicts]
    assert flat.count("satisfied") == 8, flat
    assert flat.count("satisfied, extended") == 1, flat
    assert flat.count("partial") == 6, flat
    assert flat.count("gapped") == 3, flat


def test_every_task_id_the_audit_cites_exists():
    """The review found the audit citing a WHOLE superseded task numbering after
    tasks were renumbered — `A1 T010–T014`, `A2 T015–T018` and so on. A citation
    nothing checks is a citation that rots at the first renumber."""
    tasks = (REPO_ROOT / "specs/020-modified-block-currency-fixtures"
             / "tasks.md").read_text()
    defined = set(re.findall(r"^- \[[ x]\] (T\d+[a-z]?)", tasks, re.M))
    cited = set()
    for span in re.findall(r"\*\*(T\d+[a-z]?(?:–T\d+[a-z]?)?)\*\*",
                           AUDIT.read_text()):
        cited |= {p for p in re.split(r"–", span)}
    assert cited, "no task ids harvested — check the regex"
    missing = sorted(cited - defined)
    assert not missing, f"audit cites task ids that do not exist: {missing}"


# ============================================================================
# US5 — PROVENANCE, DETERMINISM, AND THE ADVISORY BAND OVER THE CATALOGUE
# ============================================================================


def test_every_fixture_tree_this_feature_adds_carries_a_provenance_note():
    """A convention nothing checks is a convention that lasts one feature.

    LINE 3 is the machine-readable provenance line. The `SYNTHESIZED` match is
    CASE-SENSITIVE and WHOLE-WORD, and that is load-bearing: a reconstruction's
    note says "Not synthesized", and a case-insensitive substring test would
    read that as a synthesis claim — which the first cut of the templates would
    have caused, since it put the SHA on line 42 and "Not synthesized" on line 3.
    """
    reconstructed = {t for t, *_ in ((r[0],) for r in RECONSTRUCTIONS)}
    for tree in NEW_TREES:
        note = FIXTURES / tree / "README.md"
        assert note.is_file(), tree
        lines = note.read_text().splitlines()
        assert len(lines) >= 3, tree
        line3 = lines[2]

        sha = re.search(r"\b[0-9a-f]{40}\b", line3)
        synth = re.search(r"\bSYNTHESIZED\b", line3)
        assert bool(sha) ^ bool(synth), (tree, line3)
        if tree in reconstructed:
            assert sha, (tree, "a reconstruction must name its commit on line 3")
        else:
            assert synth, (tree, "a synthesis must say SYNTHESIZED on line 3")

        body = note.read_text()
        assert re.search(r"audit row \*\*A\d+\*\*", body), tree
        assert re.search(r"add-modified-block-currency-check`? § 3\.\d",
                         body), tree


def test_two_runs_agree_byte_for_byte_on_every_tree():
    """ROW A18'S EXTENSION. F1 pins one tree; this pins the catalogue.

    Non-empty FIRST: two empty lists are byte-identical, so a discovery
    regression returning nothing everywhere would pass this as written.
    """
    total = 0
    for tree in ALL_TREES:
        first, second = _tree(tree), _tree(tree)
        if isinstance(first, Skip):
            assert isinstance(second, Skip)
            assert (first.family, first.reason) == (second.family, second.reason)
            continue
        assert [f.__dict__ for f in first] == [f.__dict__ for f in second], tree
        total += len(first)
    assert total > 20, f"only {total} findings — determinism over nothing"


def test_no_new_tree_reports_an_unexpected_error_or_a_critical_finding():
    """F1's SC-009 said no `--fail-on` run reds on this family "on any tree" —
    true while the whole family launched advisory. FLIPPED 2026-08-31 (issue
    #357): the scenario-title arm is gate-bearing now, and two of these seven
    trees (`-history-351`, `-history-329`) reconstruct exactly the shape that
    arm exists to catch, so they NOW legitimately red a `--fail-on error` run
    — that is the flip working, not a regression this sweep should catch.

    What SC-009 still guarantees, and what O8 reserves, is that no OTHER class
    ever reaches `error` or `critical` on any of these seven trees. Split by
    arm rather than asserting one band over the whole collected list.

    Non-empty first: "no finding is `error`" is vacuously true of no findings.
    """
    collected = []
    for tree in NEW_TREES:
        out = _tree(tree)
        assert not isinstance(out, Skip), tree
        collected += out
    assert collected, "a vacuous pass is not a pass"
    titles = _of(collected, "titles")
    others = [f for f in collected if f not in titles]
    assert {f.severity for f in titles} <= {WARNING, ERROR}
    assert {f.severity for f in others} <= {WARNING, INFO}
    assert not [f for f in others if f.severity in ("error", "critical")]
    assert not [f for f in collected if f.severity == "critical"]


# ============================================================================
# THE SCOPE GUARD — F1's T059 shape
# ============================================================================


def test_this_feature_touches_no_production_module():
    """DECISION D1: F2 adds NO behaviour to the module.

    A signature-and-constant snapshot rather than a byte hash, so an unrelated
    comment edit does not red it. **If this test needs changing, a behaviour
    changed and FR-023 applies** — the fix is its own task with its own RED
    test, named as a defect in the PR, never folded into a fixture commit.

    `mbc.FAMILY not in FAMILY_NOTES` is deliberately NOT re-asserted here: F1's
    `test_the_family_publishes_no_basis_note` owns it, and a second copy is the
    duplication FR-002 forbids.

    **AMENDED AGAIN BY F5 (`026-unplaced-finding-drift`), 2026-08-28.**
    `add-unclassified-finding-class` adds a FIFTH finding class, so the severity
    tuple above gains `_DRIFT_SEVERITY` — the snapshot's job is to be COMPLETE
    over the module's severity constants, and a fourth constant it did not name
    would be a gap rather than a pass. **The public-callable list below is
    UNCHANGED and that is the assertion**, not an omission: the new class is a
    `FindingClass` INSTANCE and every one of F5's new names
    (`_DRIFT_SEVERITY`, `_DRIFT_ACTION`, `_DRIFT_RULE`, `_shape`,
    `_drift_findings`, `_report_order`) is private, so the emit adds no public
    callable. This amendment did NOT come from a red — a positive list does not
    notice a new private name, which is worth knowing about this guard's reach.

    **AMENDED BY F4 (`022-modified-block-currency-reporting`), 2026-08-27, AND
    THE GUARD WORKED.** F4 realizes packet § 5.1 — the family's report section
    must show its finding classes distinguishably — and that IS added
    behaviour, so this snapshot reddened on F4's first full run and was updated
    with the four names below rather than loosened: `FindingClass`, `classify`,
    `class_counts`, `class_summary`. Nothing this file asserts about F2's own
    fixtures changed, no severity moved, no rule text moved, and F2's claim that
    *F2* adds no behaviour is untouched. The update is recorded as F4's task T040
    and named in F4's PR body, which is exactly the handling the paragraph above
    asks for.

    **AMENDED BY THE § 7.2 FLIP, 2026-08-31 (issue #357), AND NAMED AS THE
    DEFECT IT IS: A DELIBERATE BEHAVIOUR CHANGE, RED ON PURPOSE.** The flip
    moves `_LAUNCH_SEVERITY` from `warning` to `error` — precisely the
    "behaviour changed" case this docstring's own rule anticipates — and
    touches nothing else this snapshot pins: `_RESOLUTION_SEVERITY`,
    `_LEDGER_SEVERITY` and `_DRIFT_SEVERITY` are unmoved (O8), and the public
    callable list below gained nothing.
    """
    assert (mbc.FAMILY, mbc._LAUNCH_SEVERITY, mbc._RESOLUTION_SEVERITY,
            mbc._LEDGER_SEVERITY, mbc._DRIFT_SEVERITY) == (
                "modified-block-currency", ERROR, WARNING, INFO, WARNING)
    assert mbc.DELTA_GLOB == "openspec/changes/*/specs/*/spec.md"
    assert mbc.CANON_TEMPLATE == "openspec/specs/{capability}/spec.md"
    assert (mbc.BODY, mbc.SCENARIO_TITLE, mbc.SCENARIO_BULLET) == (
        "body", "scenario-title", "scenario-bullet")

    public = sorted(n for n in vars(mbc)
                    if not n.startswith("_") and callable(getattr(mbc, n))
                    and getattr(getattr(mbc, n), "__module__", "")
                    == mbc.__name__)
    assert public == [
        "ActiveBlock", "FindingClass", "Marker", "PromotedRequirement", "Unit",
        "active_blocks", "carried", "class_counts", "class_summary", "classify",
        "declarations", "derive_units",
        "extract_code_spans", "fam_modified_block_currency", "fenced_regions",
        "is_dated_bold_note", "mask_code_spans", "normalize", "parse_marker",
        "parse_spec_requirements", "promoted", "resolve", "sibling_titles",
        "split_sentences", "suppression",
    ], public


def test_the_u_class_helper_reads_the_same_set_as_the_ledger_arm():
    """`_units` MUST mirror `_arm_ledger`'s kind filter, and this is what proves
    it — found by the mutation round, which dropped the filter and saw every
    U-class test stay green because each of them re-filters by kind afterwards.

    The arm states its own denominator and numerator in the finding it emits
    ("does not carry N of the M body units and scenario bullets"), so those two
    numbers are the arm's rule rather than an invented expectation. Unfiltered,
    `_units` returns the union of the ledger's set and the title arm's —
    measured at 24 of 36 on the #329 tree against the arm's 17 of 28.
    """
    for tree, repo, cap, req in (
        (T351, R351, CAP351, REQ351),
        (T329, R329, CAP329, REQ329),
        (TTOK, RTOK, CAPTOK, REQTOK),
    ):
        hits = _of(_for(_tree(tree), req), "ledger")
        assert len(hits) == 1, (tree, [f.rule[:80] for f in hits])
        stated = re.search(r"does not carry (\d+) of the (\d+) body units",
                           hits[0].rule)
        assert stated, hits[0].rule[:160]
        numerator, denominator = int(stated.group(1)), int(stated.group(2))

        assert len(_units(tree, repo, cap, req)) == numerator, tree

        root = _root(tree, repo)
        basis = mbc.promoted(root, cap)[norm_title(req)]
        kinds = (mbc.BODY, mbc.SCENARIO_BULLET)
        assert len([u for u in basis.units if u.kind in kinds]) == denominator, tree
