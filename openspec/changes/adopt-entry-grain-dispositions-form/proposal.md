---
code_surface: openxFactory — `scripts/doc_health/pin_shapes.py`, whose `_is_disposition_list` (`:217-223`), shape (c) `optional` entry (`:418-423`), and shared failure representation (`Failure`, `Verdict.render()`, `_first_failure`, `:465-536`) gain the ENTRY-GRAIN arm of an OPTIONAL member's present-and-malformed reading and the entry index/key it renders, plus that arm's tests under `tests/doc-health/` (hyphen: the tests directory is `tests/doc-health/`, the package under test is `scripts/doc_health/`) — `tests/doc-health/test_pin_shape_adapter.py`, which holds the adapter to the verifiers with its two-leg equivalence test, AND `tests/doc-health/test_tag_hygiene_pinned_targets.py`, whose family-level case asserts the rendered finding names the entry (`tasks.md` § 3). THAT IS THE WHOLE SURFACE AND NO FURTHER FILE IS ADMITTED. NO BYTE OF ANY NAMED FILE MOVES IN THIS PULL REQUEST: the filing carries the packet only — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, ONE `## MODIFIED` spec delta, one README "Active changes" bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml`. NOT THIS PACKET'S SURFACE, each for a stated reason: the five per-product pin verifiers, of which `scripts/validate-openspec-cli-pin.py` is READ AND MEASURED here (`pinned_dispositions`, `:787-857`) and NEVER edited — the adapter tracks those guards and does not author them; no pin record, no `contracts/` byte, no digest, no contract bundle; no schema member added and no `dispositions:` key added to any record; no capability created, renamed or deleted; nothing under `openspec/specs/` edited, this packet's delta being a change-packet delta that reaches canon only at the archive.
target_release: implemented
sequenced_after: [extend-prose-tagging-target-to-pinned-capabilities]
---

# Proposal: adopt-entry-grain-dispositions-form

Status: draft
Proposed: 2026-09-15, in lane `openxfactory-2` (display `openXfactory-2`),
session `c0d09b6d`, as the standing claim holder of openxFactory
[#1045](https://github.com/opensoft/openxFactory/issues/1045) (CLAIMED
2026-09-15T20:43:06Z, after the three reads Rule 1 requires, all three empty).
Origin: openxFactory #1045, a FINDING this lane filed on 2026-09-15 and did not
claim at filing, noted during the `extend-prose-tagging-target-to-pinned-capabilities`
arc (FILED #994 → RATIFIED #1019 → REALIZED #1040 → ARCHIVED #1042 →
`8944758c`) and RULED STANDS on that arc's own realization pull request, PR
#1040 round 8.

**THIS PACKET IS A PROPOSAL AND RATIFICATION IS BRETT HEAP'S WORD.** Nothing
here is ratified. It admits no text to canon, moves no byte of
`scripts/doc_health/pin_shapes.py` or of any test, edits no file under
`openspec/specs/`, and ticks no box in § 1 of `tasks.md`. The three lifecycle
documents carry `Status: draft` and `.openspec.yaml` carries DRAFTING
PROVENANCE ONLY — `kind: ad_hoc`, `proposed_by`, `proposed_on`, and NO
`approved_by`/`approved_on` — which is the lawful unapproved shape
`add-drafted-proposal-origin` defined; approval, when and if it comes, is a pure
ADDITION beside a fixed `kind` and `id`. The spec delta carries no lifecycle
header, as 308 of the 312 spec-delta files measured on `origin/main` do not.

## Why

**A RULING SAID THE ADAPTER STANDS, AND NAMED THE SUCCESSOR IT WAS NOT.** On PR
#1040 round 8, an automated review raised `scripts/doc_health/pin_shapes.py:223`
— `_is_disposition_list` accepts ANY list, while the full verifier's
`pinned_dispositions` refuses malformed ENTRIES. The lane RULED STANDS, for
reasons that are still good: the ratified design D-2 cites exactly
`scripts/validate-openspec-cli-pin.py:801-803` (absent-is-empty) and `:804-809`
(present-and-not-a-list refused) for this member; the two-leg equivalence test
holds the adapter to the CITED guards; and a record carrying
`dispositions: [{}]` resolves nothing anyway without a well-formed
`capabilities:` enumeration naming the capability. That ruling also named what
it was declining to do, verbatim: *"Extending the optional-member form to the
entry grain is a legitimate later delta against `neutral-product-pin`/this
capability, not this realization's — noted, not filed."* This packet is that
later delta, and it is the first: a corpus search for a successor returns only
issue #1045 itself.

**THE GAP IS MEASURED, IT IS ONE-DIRECTIONAL, AND IT IS EIGHT CASES.** Called
in memory with no file, no `git` and no network — `pinned_dispositions(pin)` is
a pure function of the record, evaluated as part of check 1 at
`scripts/validate-openspec-cli-pin.py:1966`, BEFORE `repository_identity`
(`:1973`) and before any fetch — the verifier's own guard REFUSES eight
entry-grain records that the adapter ACCEPTS today, and refuses NOTHING the
adapter refuses. The adapter is therefore NARROWER than the guard on the
entries and is nowhere WIDER. `design.md` D-1 carries the measurement, case by
case, with the refusal line each was raised from.

**WHY NARROWER IS THE DIRECTION THAT MATTERS.** Canon states the consequence
itself: *"a resolver that ACCEPTED what the shape's own GUARD REFUSES would, on
exactly those trees, admit a record the repository's own gate rejects at its
first shape check"*. The trees in question are the ones the adapter exists for —
a doc-health fixture tree, an aggregate run, a `--single-repo` run over an
arbitrary checkout, an added `contracts/evil-pin.yaml` — where no pin verifier
has run at all. On a landed tree the gap is invisible, because every record in
`contracts/` has already passed its full verifier as a required check; that is
why this is a FINDING and not a defect, and why the remedy is a change rather
than an edit.

**AND THREE OF THE FIVE ENTRY-GRAIN REFUSALS ARE RATIFIED CANON, WHICH MAKES
THE GAP SHARPER THAN THE ISSUE STATES IT FOR THOSE THREE.**
`neutral-product-pin`'s requirement *A dispositioned finding is cited,
upgrade-coupled, and refused when stale*
(`openspec/specs/neutral-product-pin/spec.md:577`) already obliges the
entry's identity keys, its citation and its authority (D-1): a disposition
*"SHALL carry a non-empty CITATION … and SHALL name the authority that granted
it"* (`:578`), *"SHALL identify ONE finding — the repository, the item, the
delta path, and the finding's own text"* (`:586-588`), and its scenario **A
disposition carries no citation** (`:633-636`) says that a disposition
recording *"no `cited_to:`, an empty one, or no granting authority"* makes the
pin *"REFUSED as malformed, before any artifact is fetched"*. So on those
three, the adapter today does not merely admit what one verifier's local
choice refuses — **it resolves a pinned target on a record a ratified
requirement of this estate says is refused as malformed.** The other two —
the entry's `why` member and its `level` value outside `BLOCKING_LEVELS` — are
named by no such ratified requirement and are that guard's OWN pure rule;
reaching them imposes no obligation BEYOND what the verifier already enforces
on every landed pin, never "none" and never "already ratified" for those two.
**Which is why no `neutral-product-pin` delta is carried:** issue #1045 offers
the act as one against `document-lifecycle` "and/or `neutral-product-pin`",
and measured, the second is not owed — its text is READ and CITED here and
NOT modified: the gap is the OFFLINE RESOLVER's reading, and the resolver is
`document-lifecycle`'s grammar.

**AND WHY IT IS NOT A WIDENING OF THE CONTRACT.** The adapter's boundary is
that it judges a record's SHAPE and never its FAITHFULNESS TO ITS SOURCE. Every
refusal this packet proposes to transcribe reads THE ENTRY ALONE, which is the
same thing the member-grain refusal it already carries reads. Reconciling a
disposition against a finding — the thing that needs the corpus — is the full
verifier's review concern and stays outside the contract, exactly where the
round-8 ruling put it.

## What Changes

ONE `## MODIFIED Requirements` block, over `document-lifecycle`'s *Prose tagging
marker hygiene*, restating the promoted requirement IN FULL and adding EXACTLY
ONE scenario: **A pin record's optional dispositions member carries a malformed
entry**. The scenario says that where a valid, complete published-artifact
record's OPTIONAL `dispositions:` sequence carries an entry that shape's own
PURE, SOURCE-FREE guard refuses, the pass MUST report an invalid pin naming the
member AND the entry, the target MUST NOT resolve, and an absent member, an
explicit `null` and an empty sequence MUST each still be read as EMPTY.

**NOT CHANGED, AND DELIBERATELY SO.** `dispositions:` stays OPTIONAL and stays
OUT of the shape-guard-required set; canon's own sentence *"`dispositions:` is
NOT in the set: it is read with an absent-is-empty default (`:801-803`)"* is
carried VERBATIM and is still true after this packet, because absent-is-empty is
a statement about the MEMBER and this delta is about an entry INSIDE a present
one. The nine-member shape-(c) table does not move. No other requirement of any
capability is modified, and `neutral-product-pin` is not modified at all: the
member is not one its ratified text names.

## Impact

- **Affected capability:** `document-lifecycle` (ONE requirement, ONE added
  scenario; every other promoted unit carried verbatim). `neutral-product-pin`
  is READ and CITED (`:577`, `:578`, `:586-588`, `:633-636`) and NOT modified:
  its text already names the identity keys, the citation and the authority
  (D-1) and is not wrong about any of them; the entry's `why` member and its
  `level` value outside `BLOCKING_LEVELS` are named by no such ratified text
  and are the verifier's own guard, so reaching them imposes no obligation
  BEYOND what that guard already enforces on every landed pin.
- **Affected code, at realization and not here:**
  `scripts/doc_health/pin_shapes.py`, `tests/doc-health/test_pin_shape_adapter.py`,
  and `tests/doc-health/test_tag_hygiene_pinned_targets.py`.
- **Affected records:** none. `contracts/openspec-cli-pin.yaml` is the ONLY
  record in this tree carrying `dispositions:` (measured, all six `*-pin.yaml`
  files), its six entries all pass the guard today, and they pass the proposed
  entry-grain form unchanged — the realization moves no record byte.
- **Behaviour on `origin/main`:** unchanged. No landed record is refused by this
  delta, because every landed record already satisfies the guard it transcribes.
