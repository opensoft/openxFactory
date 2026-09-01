"""The lifecycle scan set: membership, the four readers, and the invariance.

`govern-openspec-corpus-membership` (ratified 2026-08-23) declares a SECOND
document set beside the governed corpus — each OpenSpec change packet's
`proposal.md` and its `review/` records — and rules that exactly four
families read it while every corpus measurement stays where it was.

Three claims are under test here, and they fail in different directions:

1. **Membership** is the resolved path list, asserted as a list and never as
   a count (§3.1). A count passes for the wrong set: the fixture packet holds
   eight documents, two of which belong, and several wrong globs return two.
2. **Exactly four readers** (§3.2/§3.3), driven from `FAMILIES` itself so a
   family added later is covered by construction rather than by memory. A new
   family that is in neither list fails the classification test loudly.
3. **Invariance** (§3.4), the load-bearing one: the per-stage census, the word
   totals, the canon-share headline, the shared inventory and the catalog
   snapshot are compared as RENDERED BYTES between a run with the scan set and
   a run without it. Summed integers can agree while the render disagrees, and
   the ruling's whole case against full membership was that the headline must
   not move.

The two historical defects (§3.5) are frozen as fixtures rather than described
in prose: `fixtures/lifecycle-historical/` holds the real pre-fix records from
blobs `02a71d6` (phase-b) and `280fc8b` (roster-device). Both were replayed
against the live blobs while this module was written, and the fixtures produce
the same findings the blobs do.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from conftest import FIXTURES, FakeGit

from doc_health import CRITICAL, DEFAULT_THRESHOLDS, ERROR, Skip
from doc_health import catalog, corpus, families, inventory, report, semantic
from doc_health.families import FAMILIES
from doc_health.runner import Context, run_suite

AS_OF = date(2026, 8, 23)
HEAD = "0" * 40

# The four families the capability declares as readers of the scan set, and
# the rest, which read the governed corpus alone. Written out rather than
# derived so that a family added to `FAMILIES` lands in neither list and
# `test_every_family_is_classified_as_reader_or_non_reader` fails — which is
# what makes §2.3's "one-line opt-in" safe rather than merely cheap.
#
# MEASURED DISCREPANCY, recorded and then FIXED. The doc-health capability's
# "Deterministic check families" requirement said SIXTEEN while `FAMILIES`
# holds SEVENTEEN: `staged-topic-template` was registered on 2026-08-15 by
# `add-staged-topic-outline-template` and the count sentence was never updated
# with it. The first cut of this change recorded that as a pre-existing defect
# and left it for its own ruling — wrongly, because this change's spec delta
# MODIFIES that requirement and would have re-ratified the stale count under
# its own authorship. The delta now reads "seventeen", enumerates
# `staged-topic template`, and says "the other thirteen families".
#
# The list below is unchanged by that correction and always was: it is driven
# from `FAMILIES`, so it reports the corpus rather than the sentence, and the
# `len(FAMILIES) - 4 == 13` assertion is the one that would have caught the
# sentence drifting again.
READERS = {
    "status-validity",
    "standard-backing",
    "ratified-provenance",
    "succession-integrity",
}
NON_READERS = {
    # add-release-tag-publication-check. It reads a MANIFEST FIELD and a set of
    # PUBLISHED GIT REFS — neither of them a governed-corpus document and
    # neither carrying a lifecycle header — so it takes neither document list,
    # exactly as the promoted requirement says of it.
    "release-tag-publication",
    "staged-topic-template",
    "location-conformance",
    "record-immutability",
    "staged-candidate-aging",
    "register-lifecycle-consistency",
    "tag-hygiene",
    "submodule-pin-drift",
    "contract-copy-drift",
    "notebook-projection-drift",
    "document-catalog",
    "ideation-routing",
    "proposal-origin",
    "client-identity-composition",
    # add-promotion-fidelity-check. It reads archived spec DELTAS and
    # promoted SPECS — bodies, not headers — so it never wants the
    # lifecycle scan set. It does read ONE header, an archived proposal's
    # `Status:`, and it reads it through `corpus.parse_status` on the file
    # directly rather than through `_lifecycle_scope`, because it needs the
    # status of a NAMED packet rather than a sweep over a document list.
    "promotion-fidelity",
    # add-duplicate-packet-check. The eighteenth family's neighbour, and a
    # non-reader for the same reason twice over: it compares archived delta
    # BODIES to each other, and the two headers it does read — an archived
    # proposal's `Status:` and its prose naming a lineage — belong to NAMED
    # packets, not to a swept document list. It reads the status through the
    # eighteenth family's own `declares_pre_ratification`, so there is one
    # reader of that header between them rather than two.
    "duplicate-packet",
    # add-release-inventory-drift-check. It reads CONTRACT ARTIFACT BYTES — a
    # release digest inventory and the blobs it names, at a commit — so it
    # takes neither the governed corpus nor the lifecycle scan set, and reads
    # no lifecycle header at all. Its document list is the inventory's own
    # member set, which is fixed by the release rather than by any scan.
    "release-inventory-drift",
    # add-family-enumeration-check. Its two inputs are a PROMOTED SPEC and a
    # PYTHON DICT — `doc-health`'s own "Deterministic check families"
    # requirement plus `families.FAMILIES` — so neither the governed corpus
    # nor the lifecycle scan set is its document list, and it reads no
    # lifecycle header at all. It also reads ACTIVE change deltas, and by
    # named path rather than by any sweep.
    "family-enumeration",
    # add-modified-block-currency-check. Its two inputs are an ACTIVE CHANGE
    # DELTA and the PROMOTED SPEC it has not yet replaced — bodies rather than
    # headers, and neither of them a lifecycle-scan-set document. It moves no
    # census, word count, canon-share figure, inventory entry or catalog record
    # either, which is what its own owning requirement now states in canon.
    "modified-block-currency",
}


# The four byte-exact-evidence PROBES. Each one MATCHES a ruled glob — three
# are literally named `proposal.md`, the fourth sits in a `review/` directory
# — and each is kept out of the scan set by `EVIDENCE_PARTS` and by nothing
# else. Each also carries a live defect (an uncited `ratified` header, a
# free-form status), so a build that drops the filter does not merely grow the
# membership list, it REPORTS a frozen record: the false finding the
# capability's "byte-exact evidence" scenario forbids.
#
# The bare `source-snapshots/` probe exists because the first draft of this
# fixture made that segment UNPINNED and the segment-by-segment assertion
# below caught it: in today's corpus every `source-snapshots/` directory is
# nested under `supporting-docs/`, so the outer segment excluded them all and
# dropping `source-snapshots` from the rule changed nothing observable. That
# is the platform-inert class again — a clause of the rule no test could see.
EVIDENCE_PROBES = (
    "openspec/changes/alpha-uncited-ratified/supporting-docs/"
    "source-snapshots/proposal.md",
    "openspec/changes/alpha-uncited-ratified/source-snapshots/proposal.md",
    "openspec/changes/alpha-uncited-ratified/evidence/proposal.md",
    "openspec/changes/alpha-uncited-ratified/supporting-docs/review/"
    "frozen-review-2026-01-02.md",
)


# The capture blob `record-immutability` compares against for the `record`
# bait document: it differs from the fixture text, so that family WOULD fire
# on the bait if it ever read the scan set. Without a differing blob the
# mutation "add record-immutability to the reader list" changes nothing
# observable and survives.
RECORD_BAIT = "openspec/changes/theta-record-bait/proposal.md"
RECORD_BAIT_BLOB = (
    "# Proposal: theta-record-bait\n\nStatus: record\n\n"
    "The captured text, which the fixture on disk no longer matches.\n")


def _ctx(fixture: str, *, lifecycle: bool = True, catalog_root=None) -> Context:
    """A context over a fixture corpus, built by `build_context`'s own loop.

    `lifecycle=False` is the empty-scan-set arm of the invariance test: the
    SAME corpus, the same everything, with `lifecycle_docs` left empty.
    """
    base = FIXTURES / fixture
    repo_paths = {p.name: p for p in sorted(base.iterdir()) if p.is_dir()}
    docs, lifecycle_docs, capabilities, change_ids = [], [], {}, {}
    for name, path in repo_paths.items():
        docs.extend(corpus.load_docs(name, path))
        if lifecycle:
            lifecycle_docs.extend(corpus.load_lifecycle_docs(name, path))
        capabilities[name] = corpus.spec_capabilities(path)
        change_ids[name] = corpus.change_ids(path)
    git = FakeGit(heads={n: HEAD for n in repo_paths},
                  captures={(n, RECORD_BAIT): RECORD_BAIT_BLOB
                            for n in repo_paths})
    return Context(
        repo_paths=repo_paths, docs=docs, lifecycle_docs=lifecycle_docs,
        capabilities=capabilities, change_ids=change_ids, git=git,
        thresholds=dict(DEFAULT_THRESHOLDS), as_of=AS_OF, agg_root=None,
        catalog_root=catalog_root)


def _fired(ctx, family: str):
    out = FAMILIES[family](ctx)
    return [] if isinstance(out, Skip) else out


def _keys(findings):
    return sorted((f.severity, f.path, f.rule) for f in findings)


# --------------------------------------------------------------- membership


def test_scan_set_is_the_resolved_path_list():
    """§3.1. The claim is the PATH LIST, asserted whole.

    Everything in the fixture packet is here: the proposal and the review
    record because they make a standing claim, and `tasks.md`, `design.md`,
    the spec delta, `supporting-docs/`, `supporting-docs/source-snapshots/`
    and `evidence/` because they do not. The archived packet is here too, one
    directory deeper than an active one, which is the case a glob rooted at
    `openspec/changes/*/` would silently drop.
    """
    repo = FIXTURES / "lifecycle-scan" / "openxFactory"
    got = [p.as_posix() for p in corpus.iter_lifecycle_paths(repo)]
    assert got == [
        "openspec/changes/alpha-uncited-ratified/proposal.md",
        "openspec/changes/alpha-uncited-ratified/review/finding-2026-01-04.md",
        "openspec/changes/alpha-uncited-ratified/review/ratification-2026-01-03.md",
        "openspec/changes/archive/2026-01-01-zeta-archived/proposal.md",
        "openspec/changes/beta-out-of-window/proposal.md",
        "openspec/changes/delta-unbacked-standard/proposal.md",
        "openspec/changes/epsilon-superseded/proposal.md",
        "openspec/changes/eta-non-reader-bait/proposal.md",
        "openspec/changes/gamma-free-form-status/proposal.md",
        "openspec/changes/theta-record-bait/proposal.md",
    ]

    # Stated as exclusions too, because the list above reads as an inclusion
    # list and the ruling's boundary is what it leaves OUT. Each of these
    # exists in the fixture packet and none may appear. The last three are
    # the EVIDENCE PROBES: each matches a ruled glob and is kept out by
    # `EVIDENCE_PARTS` alone — see
    # `test_byte_exact_evidence_is_excluded_from_membership`.
    excluded = [
        "openspec/changes/alpha-uncited-ratified/tasks.md",
        "openspec/changes/alpha-uncited-ratified/design.md",
        "openspec/changes/alpha-uncited-ratified/specs/widget/spec.md",
        "openspec/changes/alpha-uncited-ratified/supporting-docs/fragment.md",
        "openspec/changes/alpha-uncited-ratified/supporting-docs/"
        "source-snapshots/fragment.md",
        "openspec/changes/alpha-uncited-ratified/evidence/run-record.md",
        *EVIDENCE_PROBES,
    ]
    for rel in excluded:
        assert (repo / rel).is_file(), f"fixture lost {rel}"
        assert rel not in got


def test_byte_exact_evidence_is_excluded_from_membership():
    """The capability's byte-exact-evidence scenario is a MUST NOT on
    MEMBERSHIP, so it is enforced at the point membership is decided.

    The first cut of this change disclosed the gap and left it open on the
    measurement that no corpus file occupied it. That reads a MUST as an
    observation about today's file names. It is closed now by
    `corpus.EVIDENCE_PARTS`, applied by `iter_lifecycle_paths` AFTER the
    ruled globs resolve — the globs themselves are untouched, because OQ-2
    ruled them and narrowing a ruled glob in code would be re-ruling it.

    Three things are asserted, and they fail in different directions:

    1. Each probe really does MATCH a ruled glob, computed rather than
       claimed. Without this the test would pass over a build with no filter
       at all if the probes happened not to match — which is precisely how
       the reviewer's `location-conformance` mutation survived.
    2. Each probe is absent from the resolved set.
    3. Every excluded segment is load-bearing INDIVIDUALLY: dropping any one
       member of `EVIDENCE_PARTS` re-admits at least one probe.
    """
    repo = FIXTURES / "lifecycle-scan" / "openxFactory"

    matched = {p.relative_to(repo).as_posix()
               for pattern in corpus.LIFECYCLE_SCAN
               for p in repo.glob(pattern) if p.is_file()}
    resolved = {p.as_posix() for p in corpus.iter_lifecycle_paths(repo)}

    for probe in EVIDENCE_PROBES:
        assert (repo / probe).is_file(), f"fixture lost {probe}"
        assert probe in matched, (
            f"{probe} no longer matches a ruled glob, so it cannot pin the "
            "evidence filter — the probe is inert, not the filter")
        assert probe not in resolved

    # The filter is EXACTLY the set difference: nothing else was dropped.
    assert matched - resolved == set(EVIDENCE_PROBES)

    # Each segment individually kills. `frozenset` minus one member, applied
    # by the same predicate, must re-admit something.
    for segment in sorted(corpus.EVIDENCE_PARTS):
        weakened = corpus.EVIDENCE_PARTS - {segment}
        readmitted = {
            p for p in matched
            if not any(part in weakened for part in Path(p).parts)}
        assert readmitted - resolved, (
            f"dropping {segment!r} from EVIDENCE_PARTS re-admits nothing, so "
            "that segment is unpinned")


def test_the_evidence_probes_would_fire_if_admitted():
    """The membership test above is a path assertion; this is the behavioural
    half, and it is what makes the mutation kill real rather than cosmetic.

    Each probe is run through the four families AS IF it had been admitted —
    a `Context` whose `lifecycle_docs` is the probe list — and each must be
    reported. A probe nothing reports proves nothing about the filter.
    """
    repo = FIXTURES / "lifecycle-scan" / "openxFactory"
    probes = [corpus.Doc(
        repo.name, rel, (repo / rel).read_text(encoding="utf-8"),
        corpus.parse_status((repo / rel).read_text(encoding="utf-8")),
        corpus.parse_kind((repo / rel).read_text(encoding="utf-8")))
        for rel in EVIDENCE_PROBES]

    admitted = Context(
        repo_paths={repo.name: repo}, docs=[], lifecycle_docs=probes,
        capabilities={repo.name: corpus.spec_capabilities(repo)},
        change_ids={repo.name: corpus.change_ids(repo)},
        git=FakeGit(heads={repo.name: HEAD}),
        thresholds=dict(DEFAULT_THRESHOLDS), as_of=AS_OF, agg_root=None)

    reported = {f.path for family in sorted(READERS)
                for f in _fired(admitted, family)}
    assert reported == set(EVIDENCE_PROBES), (
        "a probe the four families would not report cannot pin the filter: "
        f"unreported {sorted(set(EVIDENCE_PROBES) - reported)}")

    # ...and on the REAL set they are reported by nobody, because they are
    # not in it.
    live = _ctx("lifecycle-scan")
    live_reported = {f.path for family in sorted(READERS)
                     for f in _fired(live, family)}
    assert not live_reported & set(EVIDENCE_PROBES)


def test_a_non_ratification_review_record_needs_a_status_and_no_citation():
    """The WIDENED `review/` rule (Brett, 2026-08-23), stated as the two
    obligations it actually creates rather than as one.

    Every `review/` record under a packet is a governance document, whatever
    its subject — so `finding-2026-01-04.md` is IN the set (asserted on the
    membership list above, and again here). The taxonomy obligation reaches
    it: it carries `Status: record`, a conforming value. The
    ratification-citation obligation does NOT reach it, because that rule
    binds a `ratified` status and this document claims none — so
    `ratified-provenance` must be silent about it, and demanding a citation
    would be demanding provenance for a claim the document does not make.
    """
    ctx = _ctx("lifecycle-scan")
    rel = "openspec/changes/alpha-uncited-ratified/review/finding-2026-01-04.md"
    doc = next(d for d in ctx.lifecycle_docs if d.path == rel)
    assert doc.status == "record"

    for family in sorted(READERS):
        assert not [f for f in _fired(ctx, family) if f.path == rel], \
            f"{family} fired on a conforming non-ratification review record"

    # The other half of the widened rule, so this test is not merely
    # asserting that a conforming document conforms: a review record with NO
    # taxonomy status IS reported, subject notwithstanding.
    bare = corpus.Doc(doc.repo, "openspec/changes/alpha-uncited-ratified/"
                      "review/finding-no-header.md",
                      "# A review finding with no header\n", None, None)
    widened = Context(
        repo_paths=ctx.repo_paths, docs=[], lifecycle_docs=[bare],
        capabilities=ctx.capabilities, change_ids=ctx.change_ids, git=ctx.git,
        thresholds=ctx.thresholds, as_of=AS_OF, agg_root=None)
    assert _keys(_fired(widened, "status-validity")) == [
        (ERROR, bare.path, "missing status header")]
    assert not _fired(widened, "ratified-provenance")


def test_scan_set_declares_exactly_the_two_ruled_patterns():
    """§3.6's structural pin, and the reason it is structural.

    The platform-inert mutation class: a boundary mutation that leaves
    observable values unchanged on this platform proves nothing. Bare
    `("openspec",)` returns no files at all on POSIX and so is caught by the
    counts, but a pattern set widened to `openspec/changes/**/*.md` would
    change the resolved list on this corpus and could be narrowed back by a
    reviewer to something that happens to agree. The DECLARED tuple is the
    ruled contract (OQ-2), so it is asserted as the tuple.
    """
    assert corpus.LIFECYCLE_SCAN == (
        "openspec/changes/**/proposal.md",
        "openspec/changes/**/review/*.md",
    )
    assert isinstance(corpus.LIFECYCLE_SCAN, tuple)


def test_build_context_populates_the_scan_set():
    """The WIRING, exercised through `runner.build_context` itself.

    Every other test in this module constructs its own `Context`, so all of
    them would pass over a build where `build_context` never populated
    `lifecycle_docs` at all — the families would be ready to read a set the
    runner never assembles, and the real run would find nothing. This test is
    the one that fails on that mutation.

    It also asserts the boundary at the point of construction: the two sets
    are disjoint, and the scan set is NOT in `ctx.docs`.
    """
    from types import SimpleNamespace

    from doc_health import runner

    repo = FIXTURES / "lifecycle-scan" / "openxFactory"
    ctx = runner.build_context(SimpleNamespace(
        single_repo=str(repo), repo_root=None, config=None, family=None,
        as_of=AS_OF.isoformat(), routing_strict=False))
    assert [d.path for d in ctx.lifecycle_docs] == \
        [p.as_posix() for p in corpus.iter_lifecycle_paths(repo)]
    assert ctx.lifecycle_docs
    assert not ({d.path for d in ctx.lifecycle_docs}
                & {d.path for d in ctx.docs})
    assert all(d.repo == repo.name for d in ctx.lifecycle_docs)


def test_lifecycle_docs_are_built_by_the_one_header_reader():
    """`load_lifecycle_docs` reuses `parse_status`/`parse_kind`, never a
    second reader (`align-status-reader-to-real-lines`). Asserted by result:
    every scan-set Doc's status equals what `parse_status` returns for its
    own text, and the free-form fixture's raw value survives unnormalized.
    """
    ctx = _ctx("lifecycle-scan")
    assert ctx.lifecycle_docs
    for doc in ctx.lifecycle_docs:
        assert doc.status == corpus.parse_status(doc.text)
        assert doc.kind == corpus.parse_kind(doc.text)
    gamma = next(d for d in ctx.lifecycle_docs if "gamma" in d.path)
    assert gamma.status == "ratified — Test Owner, 2026-01-05, in-session ruling"


# ------------------------------------------------- the four families fire


def test_ratified_provenance_fires_on_an_uncited_scan_set_proposal():
    """§3.2, rule one: uncited `ratified`."""
    got = _fired(_ctx("lifecycle-scan"), "ratified-provenance")
    assert _keys(got) == [(
        CRITICAL, "openspec/changes/alpha-uncited-ratified/proposal.md",
        "ratified header carries no citation in either sanctioned spelling")]


def test_status_validity_fires_on_out_of_window_and_free_form_scan_set_headers():
    """§3.2, rules two and three: a `Status:` past the header window reads as
    absent, and a value the taxonomy does not contain is free-form.
    """
    got = _fired(_ctx("lifecycle-scan"), "status-validity")
    assert _keys(got) == [
        (ERROR, "openspec/changes/beta-out-of-window/proposal.md",
         "missing status header"),
        (ERROR, "openspec/changes/gamma-free-form-status/proposal.md",
         "free-form status 'ratified — Test Owner, 2026-01-05, "
         "in-session ruling'"),
    ]


def test_standard_backing_fires_on_an_unbacked_scan_set_standard():
    """§3.2, rule four: an unbacked `standard` claim."""
    got = _fired(_ctx("lifecycle-scan"), "standard-backing")
    assert _keys(got) == [(
        CRITICAL, "openspec/changes/delta-unbacked-standard/proposal.md",
        "standard claim without resolvable backing")]


def test_succession_integrity_fires_on_a_scan_set_superseded_document():
    """§3.2, rule five: `superseded` with no resolvable successor."""
    got = _fired(_ctx("lifecycle-scan"), "succession-integrity")
    assert _keys(got) == [(
        ERROR, "openspec/changes/epsilon-superseded/proposal.md",
        "superseded without resolvable successor")]


def test_a_conforming_scan_set_document_fires_nothing():
    """The review record and the archived packet both satisfy every rule, so
    the four families report them not at all. Without this, every test above
    would also pass for a family that fires on everything in the set.
    """
    ctx = _ctx("lifecycle-scan")
    quiet = {
        "openspec/changes/alpha-uncited-ratified/review/"
        "ratification-2026-01-03.md",
        "openspec/changes/archive/2026-01-01-zeta-archived/proposal.md",
    }
    for family in sorted(READERS):
        for finding in _fired(ctx, family):
            assert finding.path not in quiet, f"{family} fired on {finding.path}"


# --------------------------------------------------- the boundary holds


def test_every_family_is_classified_as_reader_or_non_reader():
    """§3.3's loud failure. A family added to `FAMILIES` and to neither list
    fails HERE, with its name, rather than silently acquiring or losing the
    wider scope — the capability's "an automated check MUST hold that
    boundary" scenario.
    """
    assert READERS | NON_READERS == set(FAMILIES), (
        "a family is in neither the reader nor the non-reader list: "
        f"{sorted(set(FAMILIES) - (READERS | NON_READERS))}; "
        "or a listed family no longer exists: "
        f"{sorted((READERS | NON_READERS) - set(FAMILIES))}")
    assert not READERS & NON_READERS
    # Four readers, as ruled (OQ-3). Thirteen non-readers, as MEASURED — see
    # the note on NON_READERS. The promoted requirement's "sixteen families"
    # predated `staged-topic-template`, so the original "the other twelve"
    # was arithmetic from a stale total, not a claim about a thirteenth
    # family having the wider scope; this change's MODIFIED block now says
    # seventeen and thirteen. Which four read the set is what the ruling
    # settles, and that half is asserted exactly.
    assert READERS == {"status-validity", "standard-backing",
                       "ratified-provenance", "succession-integrity"}
    assert len(NON_READERS) == len(FAMILIES) - 4 == 19
    assert "staged-topic-template" in NON_READERS
    assert "promotion-fidelity" in NON_READERS
    assert "duplicate-packet" in NON_READERS
    assert "family-enumeration" in NON_READERS
    assert "modified-block-currency" in NON_READERS


def test_the_reader_list_is_structural_not_incidental():
    """§3.6's second structural pin, and it was added because a mutation
    SURVIVED without it.

    Adding `location-conformance` to the reader list changed nothing
    observable on the first cut of this fixture — no scan-set document
    happened to violate a location rule — so the behavioural test below
    passed over a build with FIVE readers. That is the platform-inert class
    wearing a different hat: a mutation whose effect the fixture cannot see
    proves nothing about the boundary.

    Two answers, both kept. The fixture gained bait documents that the
    non-readers WOULD report (see `test_the_non_reader_bait_is_live`), and
    this test asserts the boundary structurally: `_lifecycle_scope` appears
    in the source of exactly the four declared readers and nowhere else in
    the package. A fifth reader is then a one-line opt-in that fails HERE,
    by name, whatever the fixture happens to contain.
    """
    import inspect

    for name, fn in sorted(FAMILIES.items()):
        uses = "_lifecycle_scope(" in inspect.getsource(fn)
        assert uses == (name in READERS), (
            f"{name} {'reads' if uses else 'does not read'} the lifecycle "
            f"scan set, and the declared reader list says otherwise")

    # ...and no other module in the package CALLS the accessor, so the four
    # call sites above are the complete inventory. Matched on the call shape
    # `_lifecycle_scope(` rather than the bare name, because the name also
    # appears in prose that documents the boundary (runner.py's Context
    # field) and a test that forbids describing the rule is a bad test.
    package = Path(families.__file__).parent
    others = sorted(
        p.name for p in package.glob("*.py")
        if p.name != "families.py"
        and "_lifecycle_scope(" in p.read_text(encoding="utf-8"))
    assert others == [], f"{others} call families._lifecycle_scope"
    assert families.__file__.endswith("families.py")
    source = Path(families.__file__).read_text(encoding="utf-8")
    assert source.count("for doc in _lifecycle_scope(ctx):") == 4


def test_the_non_reader_bait_is_live():
    """The bait documents are only useful if they would REALLY fire.

    Asserted by running the two families over the scan set directly, as a
    scan-set-only corpus. If a later edit makes the bait inert — a taxonomy
    change, a marker-grammar change — this fails here rather than silently
    weakening the boundary test below.
    """
    scan_only = _ctx("lifecycle-scan")
    as_corpus = Context(
        repo_paths=scan_only.repo_paths, docs=scan_only.lifecycle_docs,
        lifecycle_docs=[], capabilities=scan_only.capabilities,
        change_ids=scan_only.change_ids, git=scan_only.git,
        thresholds=scan_only.thresholds, as_of=AS_OF, agg_root=None)
    bait = {
        "location-conformance":
            "openspec/changes/eta-non-reader-bait/proposal.md",
        "tag-hygiene":
            "openspec/changes/eta-non-reader-bait/proposal.md",
        "record-immutability":
            "openspec/changes/theta-record-bait/proposal.md",
    }
    for family, path in sorted(bait.items()):
        assert [f for f in _fired(as_corpus, family) if f.path == path], \
            f"{family} would not fire on its bait, so it cannot pin anything"


def test_only_the_four_declared_families_read_the_scan_set(tmp_path):
    """§3.3. Driven from `FAMILIES`, both directions asserted.

    The twelve non-readers must return the IDENTICAL findings whether the scan
    set is present or empty — a stronger claim than "no finding names a
    scan-set path", because a family could otherwise let a scan-set document
    change a finding it reports against some other path. The four readers must
    differ, or the test is passing for a build where nothing was wired at all.
    """
    full = _ctx("lifecycle-scan", catalog_root=tmp_path)
    empty = _ctx("lifecycle-scan", lifecycle=False, catalog_root=tmp_path)
    scan_paths = {d.path for d in full.lifecycle_docs}
    assert scan_paths

    for family in sorted(NON_READERS):
        with_set = _keys(_fired(full, family))
        without = _keys(_fired(empty, family))
        assert with_set == without, f"{family} moved with the scan set"
        assert not [k for k in with_set if k[1] in scan_paths], \
            f"{family} reported a scan-set document"

    for family in sorted(READERS):
        with_set = _keys(_fired(full, family))
        without = _keys(_fired(empty, family))
        assert with_set != without, f"{family} did not read the scan set"
        assert [k for k in with_set if k[1] in scan_paths], \
            f"{family} reported no scan-set document"


def test_the_scan_set_moves_no_corpus_measurement(tmp_path):
    """§3.4, the load-bearing test, compared as RENDERED BYTES.

    The per-stage census, the governance and canon word totals, the
    canon-share headline, the shared inventory and the catalog snapshot are
    each rendered twice — once over a corpus with a non-empty scan set, once
    with an empty one — and compared byte for byte. Summed integers are not
    enough: two different corpora can sum alike, and the ruled option's whole
    case against full membership was a 12.2-point fall in the headline.

    The last assertion is the one that keeps this test honest: the two REPORTS
    must differ. If they did not, every comparison above would be passing over
    a build where the scan set was never read.
    """
    full = _ctx("lifecycle-scan", catalog_root=tmp_path)
    empty = _ctx("lifecycle-scan", lifecycle=False, catalog_root=tmp_path)

    # The governed corpus itself is the same list of the same documents.
    assert [(d.repo, d.path, d.status) for d in full.docs] == \
           [(d.repo, d.path, d.status) for d in empty.docs]
    scan_paths = {d.path for d in full.lifecycle_docs}
    assert scan_paths and not scan_paths & {d.path for d in full.docs}

    # SECOND, INDEPENDENT PIN on the two runner mutations, in a different test
    # from `test_build_context_populates_the_scan_set` and reached by a
    # different route. That test was the ONLY killer for both "build_context
    # never populates lifecycle_docs" and "build_context extends `docs` with
    # the scan set" — a single killer means a single test edit hides both.
    # This arm goes through `build_context` itself and states the governed
    # corpus POSITIVELY: `ctx.docs` is exactly `iter_doc_paths`, no more and
    # no less, so a build that folded the scan set into `docs` fails here even
    # if every disjointness assertion elsewhere were deleted.
    from types import SimpleNamespace

    from doc_health import runner

    repo = FIXTURES / "lifecycle-scan" / "openxFactory"
    built = runner.build_context(SimpleNamespace(
        single_repo=str(repo), repo_root=None, config=None, family=None,
        as_of=AS_OF.isoformat(), routing_strict=False))
    assert [d.path for d in built.docs] == \
        [p.as_posix() for p in corpus.iter_doc_paths(repo)]
    assert [d.path for d in built.lifecycle_docs] == \
        [p.as_posix() for p in corpus.iter_lifecycle_paths(repo)]
    assert built.lifecycle_docs

    def sections(ctx):
        spec_words = sum(
            len(p.read_text(encoding="utf-8").split())
            for _, path in sorted(ctx.repo_paths.items())
            for p in corpus.promoted_spec_paths(path))
        result = run_suite(ctx, None, set())
        text = report.render(ctx.as_of, result.findings, result.skips, [],
                             ctx.docs, spec_words, [], [])
        blocks = {}
        current = None
        for line in text.splitlines(keepends=True):
            if line.startswith("## "):
                current = line.strip()
                blocks[current] = ""
            if current:
                blocks[current] += line
        return text, blocks

    full_text, full_blocks = sections(full)
    empty_text, empty_blocks = sections(empty)

    # The canon-share headline sentence, byte for byte.
    def canon_line(text):
        return next(l for l in text.splitlines()
                    if l.startswith("Canon share by words:"))
    assert canon_line(full_text) == canon_line(empty_text)

    # The whole per-stage census section, byte for byte — every stage row,
    # every document count, every word total, and the promoted-spec row.
    assert full_blocks["## Per-Stage Counts"] == \
        empty_blocks["## Per-Stage Counts"]
    assert "| ratified |" in full_blocks["## Per-Stage Counts"]

    # The shared inventory, in both shapes the suite emits, as rendered JSON.
    for build in (
        lambda c: semantic.build_inventory(c.docs),
        lambda c: inventory.build_inventory(c.docs, c.repo_paths, git=c.git),
    ):
        assert json.dumps(build(full), indent=1, sort_keys=True) == \
            json.dumps(build(empty), indent=1, sort_keys=True)

    # The catalog snapshot, through the catalog's own byte-stable renderer.
    def snapshot(ctx):
        inv = inventory.build_inventory(ctx.docs, ctx.repo_paths, git=ctx.git)
        return catalog.render({"entries": catalog.mechanical_entries(inv)})
    assert snapshot(full) == snapshot(empty)

    # ...and the reports themselves are NOT identical, or nothing was read.
    assert full_text != empty_text
    assert "alpha-uncited-ratified/proposal.md" in full_text
    assert "alpha-uncited-ratified/proposal.md" not in empty_text


# ------------------------------------------- the two historical defects


def test_phase_b_uncited_ratified_header_fires_ratified_provenance():
    """§3.5, defect one — `add-doxbench-editing-phase-b` at blob `02a71d6`.

    The fixture freezes the fifteen-real-line header window of the real
    pre-fix record. The whole point of the campaign: a `ratified` proposal
    whose header carries no citation was invisible to doc-health because
    `openspec/` was not a governed root, and `sanction-ratified-record-spelling`
    had to park it as out of scope.
    """
    ctx = _ctx("lifecycle-historical")
    path = ("openspec/changes/archive/2026-08-22-add-doxbench-editing-"
            "phase-b/proposal.md")
    assert (CRITICAL, path,
            "ratified header carries no citation in either sanctioned "
            "spelling") in _keys(_fired(ctx, "ratified-provenance"))
    assert not [f for f in _fired(ctx, "status-validity") if f.path == path]


def test_roster_device_out_of_window_header_fires_status_validity_only():
    """§3.5, defect two — `add-roster-device-admission-surface` at blob
    `280fc8b`, frozen byte-exactly because the defect IS the line number.

    Its `Status: ratified` sits at real line 41, past
    `corpus.STATUS_SCAN_LINES`, so the header reads as ABSENT. Two things
    follow, and the second is the one a reader gets wrong: `status-validity`
    reports a missing header, and `ratified-provenance` reports NOTHING —
    a document whose status does not parse is not a `ratified` document to
    that family, so the citation rule can never be what catches this.
    """
    ctx = _ctx("lifecycle-historical")
    path = ("openspec/changes/archive/2026-08-22-add-roster-device-"
            "admission-surface/proposal.md")
    doc = next(d for d in ctx.lifecycle_docs if d.path == path)
    assert doc.status is None
    assert [b for b, _ in corpus.split_keepends(doc.text)][40] == \
        "Status: ratified"

    assert (ERROR, path, "missing status header") in \
        _keys(_fired(ctx, "status-validity"))
    assert not [f for f in _fired(ctx, "ratified-provenance")
                if f.path == path]


def test_the_frozen_fixtures_are_the_real_records():
    """The fixtures are evidence, so their provenance is asserted rather than
    described. Both name the blob they were taken from, and roster-device —
    frozen whole, because a truncation would move the line under test — still
    carries the realization banner that pushed its header out of the window.
    """
    base = (FIXTURES / "lifecycle-historical" / "openxFactory" / "openspec"
            / "changes" / "archive")
    phase_b = (base / "2026-08-22-add-doxbench-editing-phase-b"
               / "proposal.md").read_text(encoding="utf-8")
    roster = (base / "2026-08-22-add-roster-device-admission-surface"
              / "proposal.md").read_text(encoding="utf-8")
    assert "02a71d6" in phase_b
    assert "# Proposal: add-doxbench-editing-phase-b" in phase_b
    assert "REALIZED AND ARCHIVED 2026-08-22" in roster
    assert len(corpus.split_keepends(roster)) == 130
