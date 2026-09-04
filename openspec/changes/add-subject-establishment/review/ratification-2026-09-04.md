# Proposal Ratification: add-subject-establishment

Status: ratified
Decision date: 2026-09-04
Ratifier: Brett Heap (openxFactory repository owner) — in session, recorded on
PR #491
Ratified: 2026-09-04 by Brett Heap (repository owner) — in session, verbatim:
"accept all, recommendations stand" — a RULING ROUND over the six §
Orchestrator decisions (OD-1 … OD-6) and the six § Open Questions (OQ1 … OQ6)
this proposal declined to decide by itself, then the ratification of the
packet on that basis; record: this file.
Ratified baseline: this change as committed in the ratification commit
carrying this record — `proposal.md`, `tasks.md`, `.openspec.yaml`, this
record, the eleven-requirement spec delta
`specs/subject-establishment/spec.md`, `design.md`, and the promotion
bookkeeping this packet's own PR already carried and does not repeat here:
`README.md`, `ideation/README.md`, `ideation/staging/INDEX.md`,
`docs/domain-neutralization-candidate-register.md`,
`supporting-docs/manifest.yaml`,
`supporting-docs/subject-establishment.md`,
`supporting-docs/source-snapshots/subject-establishment.md`,
`tests/sequenced_after/corpus-ledger.yaml` and
`tests/doc-health/test_sentinel_vocabulary.py`. No file outside
`openspec/changes/add-subject-establishment/` moves in the ratifying commit
itself. **NOTHING IN THE PACKET'S SPEC DELTA CHANGES BETWEEN THE TIP THE
RULING WAS GIVEN OVER AND THIS COMMIT.** The ruling was given over head
`52233363` (six required checks green, all eight Copilot review threads
resolved, no Codex review on record), and the ratifying commit adds only this
record and the front-matter / task-list bookkeeping that states the ruling —
no requirement, no scenario and no line of `specs/subject-establishment/spec.md`
moves.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § Archive gate's realization gates:
`OPENSPEC_TELEMETRY=0 openspec validate add-subject-establishment --strict`
VALID, and `--all --strict` **90 passed / 0 failed**;
`python3 scripts/proposal-support.py . verify add-subject-establishment` ok;
`pytest tests/sequenced_after` **158 passed**;
`python3 scripts/validate-sequenced-after.py . --ledger-diff` — **per-change
sweep ledger consistent with the corpus (163 rows)**; and
`pytest tests/doc-health -q -p no:cacheprovider` **1532 passed, 0 failed**.
CI at `52233363`: `lane-line`, `merge-master-approval`,
`openreposhape-pin-gate`, `openxwallet-consumer-gate`, `pytest-suite` and
`signed-execution-chain-gate` — all six **SUCCESS**.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, the ELEVEN ADDED
requirements and 37 scenarios of the new neutral capability
`subject-establishment` — no MODIFIED block anywhere, no promoted requirement
in any other capability moves a word — and every one of the six orchestrator
decisions and six open questions this packet flagged rather than decided for
itself.

**Ratification authorizes promotion of the spec delta and performs no further
realization.** `tasks.md` § Open — the named successor
`add-subject-establishment-contracts` (the two artifact kinds' schemas, the
validator, packaged fixtures, and OQ1's system-of-record measurement pass),
the LedgerxFactory back-citation follow-up, the codexFactory and OpsxFactory
instantiations, DTN-015's harvest re-expression, and the MedxFactory
consumer — is NOT built by this act. No schema lands in the ratifying commit,
no validator is written, and no domain repository is touched.

## The chain of authority, as SEPARATE ACTS

Recorded as a chain because no single act in it authorizes what the next one
does, and reading any of them as covering the others is the failure this
estate records against itself most often.

1. **The ORIGIN.** Brett named the generalization on 2026-07-28 while the
   Ledgerx work was in front of him: *"this concept of intake is also a
   general startup … some of this neutral concept should be elevated to
   openXfactory."* That act named the idea. It did not file a topic and did
   not rule anything below it.
2. **The FILING ruling, 2026-08-28, verbatim: "Progress both."** Brett's
   selection over the orchestrating session's triage survey of the ageing
   staging topics, admitting `subject-establishment` (alongside the sibling
   escrow topic) into the proposal queue on the topic's own declared exit
   path — both of whose gates were independently verified clear
   (`.openspec.yaml` § origin.reason; `tasks.md` A.2). **This ruling covers
   the decision to FILE and nothing else.** It ratified no capability name,
   no requirement text, no scope boundary and no decision to carry no schema
   surface — `.openspec.yaml`'s `approved_by` field says so in terms, and
   every one of the six orchestrator decisions and six open questions below
   was authored afterward, by the authoring session, and flagged there for
   veto.
3. **THE RULING ROUND, 2026-09-04, verbatim: "accept all, recommendations
   stand."** Brett Heap, repository owner, in session, recorded on PR #491.
   This is the act that disposes of OD-1 … OD-6 and OQ1 … OQ6 — § *The six
   orchestrator decisions, ruled* and § *The six open questions, ruled*
   below.
4. **THIS RATIFICATION**, on that basis, over the baseline named above.

**Act 2 does not authorize act 3, and act 3 authorizes no code.** Each is
written down where it happened.

## The six orchestrator decisions, ruled

All six were RULED VERBATIM as: **"accept all, recommendations stand"** —
every decision ACCEPTED AS PROPOSED, and nothing amended.

| | Decision | Disposition |
|---|---|---|
| **OD-1** | no schema surface here; the contracts are the named successor `add-subject-establishment-contracts` | **RULED: ACCEPTED AS PROPOSED** |
| **OD-2** | ONE capability carrying two authority classes, not two capabilities | **RULED: ACCEPTED AS PROPOSED** |
| **OD-3** | the capability is named `subject-establishment` | **RULED: ACCEPTED AS PROPOSED** |
| **OD-4** | the cross-factory handoff is consumed from `deployment-handoff-boundary` with no MODIFIED block there | **RULED: ACCEPTED AS PROPOSED** |
| **OD-5** | layer ownership is stated; the STORE is not | **RULED: ACCEPTED AS PROPOSED** |
| **OD-6** | the archive gate is merge plus green plus the ruling round, stricter than `code_surface: none` alone | **RULED: ACCEPTED AS PROPOSED, AND NOW SATISFIED** |

**OD-1, the one decision carrying a live counter-precedent, recorded rather
than smoothed over.** `proposal.md`'s front matter and § Orchestrator
decisions put the counter-precedent to the owner in the same breath as the
decision: the IDENTICAL call — carry no schema surface — was VETOED by Brett
on 2026-08-28 over PR #479, in the sibling packet `add-credential-escrow-checkout`
(its OD-2), on the reasoning that content he had ALREADY ruled the shape of
should not wait for a successor. That reasoning was disclosed as NOT
transferring cleanly here — no ruling has fixed either artifact kind's fields
in this packet, and the second consumer's mapping is not yet authored
anywhere — and the owner, informed of the earlier veto, ACCEPTED OD-1 anyway.
The schemas remain the named successor `add-subject-establishment-contracts`,
to be authored against a domain instantiation rather than ahead of one, and
`tasks.md` § Archive gate G.2 (a gate that would have grown had OD-1 been
vetoed) does not fire.

**OD-6, the decision that governs this record's own existence.** The standing
rule archives a `code_surface: none` proposal on landing. This packet declined
that rule for itself, on the argument that a promoted capability carrying six
unruled decisions and six open questions is canon with invisible holes in it.
The ruling ACCEPTS that stricter gate, and this ratification — together with
the green merge of PR #491 — is what SATISFIES it: `tasks.md` § Archive gate
G.1 is ticked by this record, not bypassed by it.

## The six open questions, ruled

All six carried a recommendation and no decision in `proposal.md`. The
2026-09-04 ruling disposes of every one as **"RULED: recommendation stands"**
— the recommendation is what is now in force, restated here in one line each
so a later reader is not sent back to `proposal.md` to learn what was ruled.

**OQ1 — RULED: recommendation stands.** Do NOT mint a neutral "system of
record" record kind in this packet; requirement 4 names it as an unshaped
target, and the measurement pass against `client-infrastructure-request`'s
execution-binding vocabulary and `client-identity-roster` travels with the
successor that authors the schema (`tasks.md` O.2).

**OQ2 — RULED: recommendation stands.** The escalation ladder
(`roles-authority-model`) owns the REVIEW ROUTING that requirement 6
expresses; requirement 5's archetype harvest states its invariants (new
version, no retroactive invalidation) and names no mechanism, and is
re-expressed through DTN-015's correction→promotion loop as a follow-up once
DTN-015 leaves `seed` (`tasks.md` O.6) — a refinement, not a contradiction of
what was ruled.

**OQ3 — RULED: recommendation stands.** The DESIGNER owns the conformance
verdict because it owns the intent the read-back diff is taken against; the
APPLIER owns the applied-state fact because it alone holds authority in the
target system; a disagreement is a finding against the realization MAPPING,
resolved the way requirement 10 resolves a lift/mapping disagreement, and is
never a negotiation between the two parties.

**OQ4 — RULED: recommendation stands.** YES, a factory's own governed store
MAY be the system of record, but the realization stays REQUIRED against it —
never optional — because making realization optional would let a domain skip
the design/realization split by declaring itself system-of-record-free.

**OQ5 — RULED: recommendation stands.** Left to `consent-instrument`
(DTN-016, `adopted`): requirement 2 grades a fact's EVIDENCE, a consent
instrument answers whether the estate was PERMITTED to hold it, and folding
the second question into requirement 2 would put a consent obligation in a
capability with no consent vocabulary. MedxFactory's new-patient
instantiation is left as the place to prove the composition.

**OQ6 — RULED: recommendation stands.** OpsxFactory is named in the register
and in `proposal.md` § Impact as a third consumer in its own right (its own
new-managed-estate motion, distinct from its role as codex's applier), but
promotion does NOT wait on an Opsx mapping being authored — two structurally
different platforms (MSBC and GitHub) already exercise the design/realization
split, which is the claim under test.

## The review record — Copilot rounds 1–3 taken, Codex NON-REVIEW throughout

**Copilot, authoring pass, 2026-08-29** — an initial non-actionable "Pull
request overview" summary at `02:42:47Z`, followed by a findings pass at
`03:05:37Z`: *"Copilot reviewed 12 out of 13 changed files … generated 3
comments"* (one suppressed). All three were taken before the bring-forward,
recorded in the commit that later carried them forward as *"Copilot's three
findings taken"* (`d688c244`).

**Codex, invoked twice on PR #491, NON-REVIEW both times.** `@codex review`
was posted at `2026-09-04T01:03:31Z` on head `d688c244`; the
`chatgpt-codex-connector` bot replied at `01:03:41Z`: *"You have reached your
Codex usage limits for code reviews."* Invoked again implicitly on the round-2
push; the bot replied again at `01:40:14Z` with the same usage-limit refusal.
**Codex produced zero findings and zero verdicts on this PR** — a usage-limit
reply is a NON-REVIEW, not a clean bill, and is recorded as such rather than
read as silence-equals-approval.

**Copilot round 1 (post-bring-forward), `2026-09-04T01:04:26Z`** — 🟡
*Changes recommended*: newly-edited measurement/log prose internally
inconsistent with the updated pin-site/member counts. Taken in
`f2c79272` ("Copilot round 2" in the commit's own numbering, which counts the
pre-bring-forward pass as round 1).

**Copilot round 2, `2026-09-04T01:28:26Z` and `01:38:48Z`** — 🟡 *Changes
recommended* (two review posts, one finding-set): a pinned test failure
message inconsistent with the updated assertion, and `tasks.md`'s
introduction naming `contract-v2.1` as the current contract bundle three
merges after it stopped being. Taken in `ac6e13d2` ("Copilot round 3" in the
commit's own numbering).

**Copilot's final pass, `2026-09-04T02:01:09Z`** — 🔵 *Needs a closer look*,
zero actionable findings: it notes the packet *"explicitly depends on
additional human governance review (OD/OQ ruling round) beyond automated
validation"* — which is exactly what this record performs. No fix is owed
against it.

**All eight review threads on PR #491 are RESOLVED** (verified via the
GraphQL review-thread listing at ratification time — `isResolved: true` on
every one, most `isOutdated: true` from the two catch-up merges). No
unaddressed Copilot thread remains.

**Sourcery** posted its standard upsell-stub comment on 2026-08-29 (*"Your
private repo does not have access to Sourcery"*) and reviewed nothing.

## What ratification does NOT authorize

Stated as a list because a ratification record that leaves this implicit is
how a realization acquires scope nobody granted it.

1. **No schema, no validator, no fixtures land here (OD-1).**
   `contracts/schemas/xfactory-subject-design.schema.yaml`,
   `contracts/schemas/xfactory-platform-realization.schema.yaml` and
   `scripts/validate-subject-establishment.py` are the named successor
   `add-subject-establishment-contracts`, to be authored against a real
   domain instantiation and not ahead of one — the ruling accepted this
   knowing the #479 counter-precedent went the other way, and did not revisit
   that distinction.
2. **No code lands here.** `code_surface: none` stands as measured; nothing
   under `contracts/` or `scripts/` moves in this commit, and no domain
   repository is touched.
3. **No delta on `deployment-handoff-boundary`, `roles-authority-model` or
   `governed-derived-model`.** All three are CONSUMED, cited and unmodified,
   per OD-2 and OD-4 as ruled.
4. **No contract bundle is spent.** `target_release` stays `none`, re-measured
   against `contract-v3.2` at the ratification commit and unchanged from
   authoring: no path this change writes appears among the declared bundle's
   digest entries.
5. **OQ1 … OQ6 are RULED, not left open, but their MEASUREMENT PASSES are not
   performed here.** OQ1's system-of-record vocabulary measurement, OQ2's
   DTN-015 re-expression, OQ5's consent-instrument composition proof, and
   OQ6's Opsx mapping are the successor's and the consuming domains', not
   this commit's.
6. **The archive gate is satisfied, not bypassed.** OD-6, as ruled, made the
   gate merge-plus-green-plus-this-ruling-round; this record IS that round,
   and `tasks.md` § G.1 is ticked on that basis, on the merge of PR #491 by
   the orchestrator. **This record does not merge PR #491 and does not
   archive the change** — merge is the orchestrator's act, and the archive
   follows the same convention every other `code_surface: none` promotion in
   this estate has used: merge, green, then the archive-support transition.
7. **Nothing outside `openspec/changes/add-subject-establishment/` moves in
   the ratifying commit.** The promotion bookkeeping this packet's own PR
   already carries (`README.md`, `ideation/README.md`,
   `ideation/staging/INDEX.md`, the DTN-017 register row, the two test-file
   changes) is UNCHANGED by this record and is not re-touched or re-derived
   here.
