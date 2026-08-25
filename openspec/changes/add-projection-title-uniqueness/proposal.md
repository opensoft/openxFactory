---
code_surface: openxFactory (`scripts/sync-notebooklm-books.py` — the title derivation inside `scan()`, which is today one conditional expression special-casing `README`; a repository-scoped uniqueness pass over the scan's desired set; and `parity_report()`, whose per-book comparison is a title-SET equality that cannot see a collapse. `docs/lifecycle-notebook-projection.md` § 2 — the "ambiguous stems" rule the derivation implements, plus an `Amended by:` line. `tests/notebooklm/test_sync_notebooklm_books.py` — a collision fixture over the three real shapes this corpus contains, an injectivity assertion over the whole derived set, a stability assertion against status change, and the parity-blindness regression. NO change to book identity, the `[status]` prefix vocabulary, charter text, chat framing, the grounding set, the corpus scan scope, the capacity guard's arithmetic, the session namespace, or any hybrid surface.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main PLUS one piece of evidence the code alone cannot give: an APPLIED sync that migrates the live books, because the defect is a discrepancy between a manifest and a provider and only the provider can say it closed. Concretely — `python3 -m pytest tests/notebooklm tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a post-apply provider read showing the seven books at 700 sources with `--parity` clean under the amended document-level rule. The change ships ACTIVE and archives only after that read.
Status: ratified
Ratified: 2026-08-25 by Brett Heap — in-session, multiple-choice ruling round over OQ-1 through OQ-4; every ruling adopts the recommendation, OQ-1's adoption folds in the OQ-4 scope sub-question (repository scope, closing the three latent pairs as a side effect), and OQ-3's adoption defers execution to realization rather than to this ruling. The round is recorded question by question in the Open Questions section of openspec/changes/add-projection-title-uniqueness/proposal.md, which is this file. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and it clears that spelling's three-way floor on all three axes rather than on the one it needs: approver (`by Brett Heap`), date (`2026-08-25`), and a resolvable record path.
Proposed: 2026-08-25
Origin: The lifecycle-notebook sync report of 2026-08-25, which recorded four MedxFactory staging topics synced into a book holding one source for them. Raised in-session the same day; no staged topic preceded it.
---

# Proposal: add-projection-title-uniqueness

## Why

**The projection can lose a document without anything reporting it.**

A lifecycle book's sources are titled `[<status>] <repo>: <file stem>`. The
title is not decoration — it is the projection's IDENTITY KEY. `scan()` builds
a desired map keyed by repository-relative PATH, and `sync_book()` reconciles
that map against the live book BY TITLE. Three lines decide the outcome:

- `wanted_titles = set(desired.values())` — the desired map's N path keys
  become a set of titles, and duplicates vanish there.
- the deletion pass keeps `sids[0]` for a wanted title and deletes every other
  copy, so a book is actively held at one source per title.
- the add pass writes `mf[rel]` for EVERY path key, so the manifest records
  all N documents as synced.

So when two documents of one repository share a file stem, the book ends up
holding one source and the manifest ends up claiming several. The document
that lost is not reported missing anywhere. It is not in the book, and every
artifact that would notice says it is.

**The governing rule anticipated exactly one instance of this and stopped
there.** `docs/lifecycle-notebook-projection.md` § 2 says, in full:

> Title rule for ambiguous stems: when the file stem is `README` (or otherwise
> non-unique within a repo), the title uses `<parent-dir>/<stem>` — e.g.
> `[ratified] AdxFactory: ideation/README`.

The parenthesis — "or otherwise non-unique within a repo" — states the general
rule. The implementation implements the example instead:

```python
stem = f"{f.parent.name}/{f.stem}" if f.stem.lower() == "readme" else f.stem
```

Everything that is not literally named `README` falls through to its bare stem.

**`--parity` is structurally blind to the class.** The parity mode is the one
surface built to prove a book against the corpus scan, and it compares
`set(items.values())` against the set of live titles. A collapse leaves both
sets equal, so parity reports OK on a book that is missing documents. A check
that compares titles cannot find a document that never got a title of its own.

## What was measured

Everything below was measured on 2026-08-25 against a scratch assembly of the
ten repositories at the live mains the books currently mirror, using the
sync's own `scan()`. No apply-mode run, no provider mutation; the live counts
come from a read-only notebook listing.

**Corpus-wide collision census — three collisions, five documents displaced.**

| book | derived title | documents | absent |
| --- | --- | --- | --- |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | 4 | 3 |
| `drafts` | `[draft] openxFactory: requirements` | 2 | 1 |
| `ideation-opsxfactory` | `[staged] OpsxFactory: exchange-execution-bringup` | 2 | 1 |

The MedxFactory four are `ideation/staging/{root-truth-grounding,
root-truth-target-claims, terminology-normalization,
treatment-plan-generation}/topic.md` — four separate staged topics, one source.
The drafts pair is `specs/005-customer-subject-runtime/checklists/
requirements.md` and `specs/007-client-identity-roster/checklists/
requirements.md`. The OpsxFactory pair is a brainstorm-located document that
carries `Status: staged` and the organized staging fragment it points at —
two genuinely distinct documents that both landed on the same stem.

**The provider agrees to the source.** Derived: 693 book slots, 688 distinct
titles, plus seven charters. Live, read from the provider the same day:

| book | live sources | corpus scan wants |
| --- | --- | --- |
| `xFactory — Canon` | 114 | 114 |
| `xFactory — Working Drafts` | 188 | **189** |
| `xFactory Ideation — openxFactory` | 247 | 247 |
| `xFactory Ideation — LedgerxFactory` | 66 | 66 |
| `xFactory Ideation — MedxFactory` | 49 | **52** |
| `xFactory Ideation — OpsxFactory` | 16 | **17** |
| `xFactory Ideation — codexFactory` | 15 | 15 |
| total | **695** | **700** |

Five sources short, in exactly the three books the census names. The manifest
carries the other side of the same discrepancy: 51 rows for MedxFactory's book
against 48 distinct titles, 227 rows in drafts against 226, 18 in OpsxFactory
against 17.

**The current README rule is not itself injective.** `openxFactory` projects
`contracts/memory-gateway/README.md` and `examples/memory-gateway/README.md`;
both derive `memory-gateway/README`. They do not collide TODAY only because
their statuses differ, which puts different prefixes on their titles and sends
them to different books. Two more same-repository stem pairs are in the same
position — `company-provisioning` in LedgerxFactory and
`codexfactory-domain-hermes-content` in openxFactory. A status change on any
one of those three pairs turns it into a live collapse with no code change at
all. These are latent instances of the same defect, and a rule that only fires
on observed collisions leaves them latent.

## What this changes

The capability gains the guarantee its implementation was assumed to have:
**one projected document, one source.** The delta states it as an INJECTIVITY
obligation on the title derivation rather than as a filename special case, so
the next repeated stem is handled by the rule instead of by a second
exception. It also amends parity to prove membership at the DOCUMENT level,
because the mode that exists to catch this could not.

The recommended derivation — **candidate (a), measured against three
alternatives in `design.md`** — is: a title carries the SHORTEST
repository-relative path suffix that distinguishes the document from every
other projected document of the same repository, with `README` keeping today's
parent-directory floor. Bare stems stay bare where they are already unique.

## What this deliberately does not change

- **The capacity guard needs no delta, and that is a measured claim.** The
  guard computes projected occupancy as `len(desired) + 1 + unmanaged` —
  DOCUMENTS, not titles. It has been counting the collapsed documents all
  along, so the guard's arithmetic does not move by one anywhere; only actual
  occupancy rises to meet the number the guard already used. Per book, before
  and after: canon 114/114, drafts 189/189, openxFactory 247/247,
  LedgerxFactory 66/66, MedxFactory 52/52, OpsxFactory 17/17, codexFactory
  15/15. The largest book stays at 247 of the 300 cap, headroom 53 — clear of
  the thirty-source warn threshold, which no candidate approaches.
- **No prefix, book, charter, framing, grounding or scan-scope change.** The
  `[status] repo:` shape is untouched; only what follows the colon can grow a
  path qualifier.
- **The `[spec]` and `[grounding]` title families are out of scope.** Both are
  already keyed by something other than a file stem (`[spec]` by the
  capability directory name, `[grounding]` by a fixed three-document set) and
  neither collides. Measurement confirmed it: including them in the uniqueness
  scope over-qualified one drafts title for no reason, and excluding them is
  the correct scope, not a convenience.

## Orchestrator Decisions

The in-session instruction authorized RAISING a proposal against the measured
defect. The four decisions below were taken by the authoring session under
measurement, are NOT covered by that authorization, and are flagged here for
veto. Reverting any one of them is an edit to this change, not a new one.

**The veto window closed 2026-08-25 with the ratification round below: none
of the four decisions was reverted, so all four stand as written.** Decision 1
(candidate (a)) and Decision 2 (repository scope) are the two decisions the
Open Questions round actually put to a choice — OQ-1 ruled Decision 1, and its
fold-in of OQ-4 ruled Decision 2 — and both were confirmed rather than
reverted. Decisions 3 and 4 were not raised as questions and drew no veto in
the round; per this section's own rule, reverting either now would be an edit
to this change, not a fact about the round that already ran.

1. **The rule candidate is (a), collision-triggered minimal suffix.** Chosen on
   churn: 14 renamed titles against 611 for the always-fully-qualified
   alternative. The cost is named rather than hidden — see § Open Questions Q1
   and `design.md` § 4.
2. **The uniqueness scope is the whole REPOSITORY, not the book and not
   (book, status).** It costs 14 renames against 8 for the tightest correct
   scope, and buys immunity to status change: under repository scope no
   document is ever retitled because a sibling's `Status:` header moved. The
   three latent pairs above are pre-empted by exactly this choice.
3. **The delta MODIFIES `Authority framing` rather than adding a new
   requirement.** That requirement is where the promoted spec already states
   what a source title is; a second requirement about titles would leave two
   places to read and one to forget. The cost is a full restatement, which the
   promotion-fidelity family now enforces.
4. **`--parity` is amended in the same delta.** The blindness is not a
   separate defect: a rule that guarantees injectivity and a check that cannot
   observe injectivity would ship the same silence in a new place.

## Open Questions

**Q1 — the rule candidate.** Measured, four ways, in `design.md` § 4. (a)
collision-triggered minimal suffix: 14 renames, 28 book operations, zero
collisions left. (b1) always `<parent>/<stem>`: 572 renames — and it STILL
LEAVES A COLLISION, because both checklist documents sit in a directory named
`checklists`; it is eliminated on correctness, not on cost. (b2) always the
full repository-relative path: 611 renames, 1222 book operations, correct by
construction and stable forever, longest title 130 characters against 110
today. (c) a declared list of structural stems always qualified: 14 renames
and it too leaves a collision, because `exchange-execution-bringup` is not a
structural name any list would have contained — a fixed enumeration is
provably insufficient on this corpus. So the real fork is (a) versus (b2):
28 operations and titles that depend on collision state, or 1222 operations
and titles that never do. **Recommendation: (a).** Its known cost is that
adding a colliding document later RENAMES the incumbent — one extra
delete-plus-add on a book, at the moment a second `topic.md`-shaped file
appears. `design.md` § 5 records a variant (a′) that removes even that, by
pinning a document's qualification level in the manifest so it can rise but
never fall; it is not proposed here because it puts identity state in a file
that is today a pure cache.

**RULED (2026-08-25, Brett, in-session multiple choice): recommendation
adopted — (a), collision-triggered minimal suffix, at REPOSITORY scope.** 14
renames, 28 book operations, zero collisions; the repository-scope choice
closes the three latent pairs (`memory-gateway/README` twice,
`company-provisioning`, `codexfactory-domain-hermes-content`) as a side
effect. This ruling folds in Q4's scope sub-question below — the two are one
choice, not two — so Q4 records the fold rather than a second, independent
decision.

**Q2 — does the migration ride the realization's own sync slice?** The rule
change makes 14 titles wrong in the live books at the instant it merges, and
`notebook-projection-drift` will report 28 pending operations until an
apply-mode sync runs. Either the realization commit is followed immediately by
an operator-run apply (one slice, books correct on merge, and the archive
evidence is available at once), or the apply is a separate scheduled act (the
books sit visibly drifted in between, and the archive gate waits). The
proposal assumes ONE SLICE and § 4 of `tasks.md` is written that way; splitting
it is a task edit.

**RULED (2026-08-25, Brett, in-session multiple choice): recommendation
adopted — the migration rides the realization's own sync slice.** One slice:
the realization commit is followed immediately by an operator-run apply, so
the books are correct on merge and the archive evidence exists at once.
`tasks.md` § 4 is already written this way and needs no edit; no drift window
is opened.

**Q3 — should the un-collapsed documents' arrival be announced?** Three
MedxFactory staging topics, one draft checklist and one OpsxFactory staging
fragment have never been in a book. Anyone who has queried those books has
been answered from a corpus missing them. This proposal does not claim that is
worth a record beyond this text; if it is, the place is
`docs/archive-record-discrepancies.md`, which already carries this shape of
finding.

**RULED (2026-08-25, Brett, in-session multiple choice): a record is
owed.** The five never-projected documents — the three MedxFactory staging
topics, the openxFactory draft checklist, the OpsxFactory staging fragment —
get a dated, append-only entry in `docs/archive-record-discrepancies.md`, in
the shape that document already carries for this class of finding. The entry
is written at realization (`tasks.md` § 4), not now: this proposal has not
been realized yet, and the record documents what the migration did, not what
it will do.

**Q4 — the three latent pairs.** Decision 2 pre-empts them silently, by
qualifying `memory-gateway/README` (twice), `company-provisioning` and
`codexfactory-domain-hermes-content` before they can collide. That is four of
the 14 renames. If the tightest scope is preferred instead, those four renames
disappear and the three pairs stay one status change away from a collapse.

**RULED (2026-08-25, Brett, in-session multiple choice): folded into Q1
above — no independent ruling.** Repository scope was ruled as part of Q1's
candidate choice, which pre-empts the three latent pairs named here. The
tightest correct scope — 8 renames, leaving the pairs latent — was not taken.

## Impact

- Affected capability: `lifecycle-notebook-projection` (one MODIFIED
  requirement).
- Affected code: `scripts/sync-notebooklm-books.py`,
  `docs/lifecycle-notebook-projection.md` § 2,
  `tests/notebooklm/test_sync_notebooklm_books.py`.
- Affected artifacts: the seven live lifecycle books gain five sources and 14
  titles are renamed; `.claude/nlm-sync-manifest.json` re-keys those 14 rows on
  the next apply.
- Risk: the migration is 28 provider operations on books that hold 695
  sources. It is delete-plus-add on titles, not a re-derivation of content, and
  it is bounded and enumerable in advance — the full rename list is in
  `design.md` § 6.
