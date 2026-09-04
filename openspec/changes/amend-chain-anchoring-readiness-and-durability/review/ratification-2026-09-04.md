# Proposal Ratification: amend-chain-anchoring-readiness-and-durability

Status: ratified
Decision date: 2026-09-04
Ratifier: Brett Heap (openxFactory repository owner) — in session, recorded on
PR #548
Ratified: 2026-09-04 by Brett Heap (repository owner) — in session, verbatim:
"ratify 2 and 3" — a ruling over the TWO requirements this packet still
carries, given after a SEPARATE earlier ruling had withdrawn the third; record:
this file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `tasks.md`, `design.md`, `.openspec.yaml`, this
record, and the spec delta `specs/chain-anchoring/spec.md` carrying TWO
`## ADDED Requirements` and 34 scenarios (20 on requirement 2, 14 on
requirement 3), with no `## MODIFIED Requirements` block anywhere and no
promoted requirement in any other capability moving a word. The promotion
bookkeeping this packet's own PR already carried is unchanged here and not
repeated: the `README.md` OpenSpec Records row and this change's one
`tests/sequenced_after/corpus-ledger.yaml` row.
**NOTHING IN THE PACKET'S SPEC DELTA CHANGES BETWEEN THE TIP THE RULING WAS
GIVEN OVER AND THIS COMMIT**, and that is stated first rather than left to a
diff. The ruling was given over head `2677cef9` — all seven required checks
green, all 22 review threads resolved, Copilot's final verdict on that exact
head 🟢 *Approval recommended*. The ratifying commit merges `origin/main` at
`bbc21e41` (the merge is a catch-up, never a rebase) and adds this record plus
the front-matter and task-list bookkeeping that STATES the ruling. Verified
mechanically rather than asserted: `git diff 2677cef9 <merge> --
openspec/changes/amend-chain-anchoring-readiness-and-durability/` is EMPTY — no
requirement, no scenario and no line of `specs/chain-anchoring/spec.md` moves in
the catch-up merge.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § 2's realization gates or § 3's release gates:
`OPENSPEC_TELEMETRY=0 openspec validate
amend-chain-anchoring-readiness-and-durability --strict` VALID, and
`--all --strict` **90 passed / 0 failed**;
`python3 scripts/proposal-support.py . verify
amend-chain-anchoring-readiness-and-durability` ok;
`pytest tests/sequenced_after -q` **162 passed**;
`python3 scripts/validate-sequenced-after.py . --ledger-diff` — **per-change
sweep ledger consistent with the corpus (164 rows)**; and
`pytest tests/doc-health -q -p no:cacheprovider` **1542 passed, 0 failed**.
CI at `2677cef9`: `clearing-dispatch-gate`, `lane-line`,
`merge-master-approval`, `openreposhape-pin`, `pytest-suite`,
`signed-execution-chain-gate` and `wallet-validation` — all seven **SUCCESS**.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, the TWO ADDED
requirements and 34 scenarios this amendment adds to the ratified
`chain-anchoring` capability — *Fixed UTC durability batches account for every
accepted event exactly once* and *Witness submission and confirmation remain
distinct evidence states* — **as written**, unamended.

**A THIRD REQUIREMENT WAS WITHDRAWN BEFORE THIS RULING AND IS NOT DISPOSED OF
BY IT.** *Realization waits for the released chain and an operational PKI plane*
was REMOVED from the delta by a SEPARATE, EARLIER ruling of the same owner on
the same day. It is **not ratified and not refused** — § *Dispositions* says so
in terms, because a reader who finds two requirements where the proposal's
history shows three is owed the reason, and "the owner rejected it" is not that
reason.

**Ratification authorizes promotion of the spec delta and performs no
realization.** The obligations these two requirements create fall on schemas
that ALREADY LANDED, at PR #629, ahead of and without this amendment; the pass
that discharges them is a **separate, named successor** and is not built by this
act — § *The realization cost, stated as an obligation*, which is the one part
of this record that binds future work rather than describing past work.

## The chain of authority, as SEPARATE ACTS

Recorded as a chain because no single act in it authorizes what the next one
does, and reading any of them as covering the others is the failure this estate
records against itself most often. **Four acts here, and the middle two are the
ones most likely to be collapsed into one.**

1. **The FILING, 2026-08-31, verbatim: "proceed."** Brett Heap, in session,
   over the reconciliation of the two competing tranche-three anchoring packets
   after the Opus/Fable review, the GLM review, the Terra opinion and the
   partial Kimi integration review. That act selected the already-ratified
   `add-chain-anchoring` as the SURVIVOR, authorized closing PR **#521** without
   merge, and directed that the superseded draft's unique semantic improvements
   be preserved in governed follow-up work rather than lost or re-imported under
   a second capability identity. **This packet is that follow-up work, and it
   carries #521's content forward** — which is precisely why the filing approval
   cannot be read as ratifying it: `.openspec.yaml`'s `origin.approved_by` says
   so in its own words, *"This origin approval authorizes filing the draft and
   does not ratify its content."* It ratified no requirement text, no scenario,
   and no scope boundary.
2. **The ADOPTION ruling, 2026-09-03, verbatim: "adopt the chain-anchoring
   branch after v3.1 lands."** Given in session and claimed on this PR by lane
   `openxfactory-1d` on 2026-09-04T00:41Z, because PR #548 was the only open
   `chain-anchoring` object and an ownerless branch cannot carry a claim. That
   ruling produced **PR #629** — `add-chain-anchoring`'s realization: twelve
   schemas, a refusing canonical validator, squash `11feff75`, merged
   2026-09-03T23:55:32-04:00. **It is an act on the BASIS packet, not on this
   one.** It authorized adopting and landing a realization; it ruled nothing
   about this amendment's requirements, and this record does not read it as
   having done so.
3. **The WITHDRAWAL ruling, 2026-09-04 ~02:3xZ, verbatim: "bring 548 forward
   after 629 lands, drop requirement 1."** Brett Heap, repository owner, in
   session, recorded on PR #548 (comment `5534659121`). **This is the act that
   removed requirement 1, and it is the act that this ratification most needs
   kept separate from itself**, because the two are one sentence apart in the
   day's history and mean opposite things about the same text. Its reason is on
   the record rather than inferred: requirement 1 gated `chain-anchoring`
   **schema and validator AUTHORING** on an operational PKI plane that does not
   exist — and the owner had already ruled that authoring DONE, at #629, which
   landed without any such gate and without the shared Speckit feature
   requirement 1 also mandated. **Ratifying requirement 1 after that would have
   retroactively declared the landed realization illegitimate.** The requirement
   conflated two gates the schemas themselves keep apart — contract
   REALIZATION (authoring schema and validator text) versus runtime
   COMMISSIONING (naming a live signed-log instance) — and only the latter
   plausibly needs a live PKI plane; #629's own OPEN item 2 already tracks the
   still-unmet `[OPERATOR]` conditions for that, separately and where they
   belong.
4. **THE RATIFICATION, 2026-09-04 ~05:10Z, verbatim: "ratify 2 and 3."** Brett
   Heap, repository owner, in session, recorded on PR #548 (comment
   `5536095884`). Given over head `2677cef9`, on the delta as it stood AFTER the
   withdrawal — two requirements, 34 scenarios — and accepting both **as
   written**, with no amendment sought and none made. The same ruling queued the
   realization cost ahead of the next contract cut; that clause is carried in
   § *The realization cost* below, not folded into the ratification itself.
5. **THIS RECORD**, on that basis, over the baseline named above.

**Act 1 does not authorize act 3, act 3 does not authorize act 4, and act 4
authorizes no code.** Each is written down where it happened.

## Dispositions

| | Requirement | Scenarios | Disposition |
|---|---|---|---|
| **1** | *Realization waits for the released chain and an operational PKI plane* | 6 | **REMOVED — WITHDRAWN on the owner's ruling of 2026-09-04. NOT ratified, NOT refused.** |
| **2** | *Fixed UTC durability batches account for every accepted event exactly once* | 20 | **RATIFIED AS WRITTEN** on head `2677cef9` |
| **3** | *Witness submission and confirmation remain distinct evidence states* | 14 | **RATIFIED AS WRITTEN** on head `2677cef9` |

**Requirement 1 — WITHDRAWN, and the distinction is load-bearing.** A
withdrawal is not a refusal, and this record refuses to write it as one. The
owner did not find the requirement wrong on its merits; he found it OVERTAKEN —
a gate on authoring, ruled after the authoring it gated had already been ruled
done and landed. Nothing here decides whether an operational PKI plane is owed
before a `chain-anchoring` RUNTIME is commissioned; that question is live,
belongs to commissioning rather than to contract realization, and is tracked at
#629's OPEN item 2 under the `[OPERATOR]` conditions. **A later packet may raise
the commissioning gate on its own merits without contradicting this act.** The
withdrawn text is not erased from the project's history: it remains readable in
full at this branch's pre-removal commit `adccf578` and earlier, and the removal
is recorded in `proposal.md` § *Requirement 1 removed — owner's ruling
2026-09-04* and in `design.md` § *Context* (where decision D2 is retained as the
historical record of a decision this amendment no longer makes). **The removal
was surgical, and that was verified mechanically rather than trusted**: the
delta went from 3 requirements / 40 scenarios to 2 / 34, and the text of
requirements 2 and 3 is **BYTE-IDENTICAL** from `adccf578` to the ratified head
— so the two requirements the owner ratified are exactly the two that stood
before the third was withdrawn, not a rewrite occasioned by it.

**Requirement 2 — RATIFIED AS WRITTEN.** The durability profile is now canon:
consecutive non-overlapping UTC windows from `00:00:00Z` inclusive to the next
exclusive; ONE atomic log-admission transaction that validates, dedupes, records
trusted acceptance time, selects the window from that acceptance time and
assigns a monotonic leaf sequence, with owner source time descriptive only and
forbidden from selecting or reopening a window; a close that serializes after
every admission before the boundary and records BOTH a
`close_sequence_watermark` and a resolving signed-log checkpoint, so a manifest
cannot lower its own denominator to match a retained prefix; a signed
append-only eligibility registry snapshotted once per window, with zero-or-
multiple matches REFUSED and mid-window activations deferred to the next window;
anchoring control leaves excluded from the event count so a batch cannot include
itself; one released digest-bound `daily-Merkle` construction profile that makes
every root independently reproducible; and a six-node proof chain from event
leaves through `daily_batch_root`, canonical manifest bytes, `material_digest`,
the configuration-bound `anchored_digest`, the identity aggregation path, and
per-witness commitment paths that must all begin at the SAME
`aggregation_root == anchored_digest`. Empty windows still emit a signed,
linked, count-zero checkpoint, and continuity binds the preceding daily item's
`anchored_digest` — not its `daily_batch_root` — so consecutive empty days
sharing one deterministic empty root cannot be silently dropped. **The ratified
witness configuration, its ordering and its no-selectivity rule are consumed
unchanged and are not reopened by a word of this.**

**Requirement 3 — RATIFIED AS WRITTEN.** Interface acceptance is now
contractually distinct from independently verified confirmation, per witness and
per network. Kaspa *submitted* means the serialized commitment transaction was
accepted for processing by the declared interface and MUST NOT mean Kaspa
confirmed; OpenTimestamps *submitted* means a detached proof over the same
configuration-bound `aggregation_root == anchored_digest` was accepted and
retained — a proof over a raw `daily_batch_root` is REFUSED — and MUST NOT mean
Bitcoin confirmed; a long-horizon durability claim SHALL cite Bitcoin-confirmed
evidence and never an unupgraded timestamp or Kaspa alone. What separates the
two states is not an implementer's threshold and not a number this specification
invents: it is an **append-only signed confirmation-profile registry** of
immutable versioned operator-approved profiles, each binding network, id,
version, canonical content digest, approval record, predecessor, activation log
sequence and checkpoint, effective interval and closed standing
(`active | retired | compromised`), snapshotted once per witness per UTC window,
with rollback, mid-window activation, content substitution and
digest-mismatch all REFUSED. Historical receipts keep immutable as-of evidence
while current verification also reports current standing, so a retired or
compromised profile stops minting new claims without rewriting old ones. The
existing receipt/state split is preserved exactly: submitted and in-flight state
live in the anchor-state record, the receipt gains a per-chain entry only when
that entry's proof material is captured whole, and a later upgrade APPENDS
against the same anchored digest rather than re-anchoring the item.

## The realization cost, stated as an obligation

**This is the one section of this record that binds work not yet done, and it is
stated as an obligation rather than as a note, because the window in which it
can be discharged cheaply is already open and will close at the next contract
cut.**

`add-chain-anchoring` REALIZED before this amendment ratified. PR #629 (squash
`11feff75`) authored twelve `contracts/chain-anchoring/` schemas and the
canonical reader `scripts/validate-chain-anchoring.py` **against the basis
alone**, and #629's own body disclosed the gap rather than leaving it to be
found: *"If #548 lands, this realization needs a follow-on pass."* Re-measured
independently on this branch's merged head at ratification time, over every
landed schema and the reader:

* `grep -rniE "confirmation|profile" contracts/chain-anchoring/*.schema.yaml
  scripts/validate-chain-anchoring.py` returns **ZERO matches**. Neither
  requirement 3's confirmation-profile registry nor any binding to one exists
  anywhere in the realized family.
* `contracts/chain-anchoring/anchor-state.schema.yaml`'s `witness_status_row`
  carries the **closed, three-member** `status` enum
  `[in_flight, landed, terminally_failed]` under `additionalProperties: false`.
  That distinguishes in-flight from landed. It is **not** requirement 3's
  interface-submitted-versus-independently-verified-confirmed distinction, and
  it binds no confirmation-profile id, version, content digest, activation
  checkpoint or standing anywhere in the mint-time configuration block.
* None of requirement 2's fixed-UTC durability batch, eligibility registry or
  daily-Merkle construction machinery is realized. #629's OPEN items name only
  the basis's own unclosed operator conditions, not this amendment's profile.

**THE SUCCESSOR REALIZATION, AND ITS DEADLINE.** A follow-on realization pass —
a **new, separate PR**, sequenced after this ratification — MUST land before the
`contracts/chain-anchoring/` schemas ship in a TAGGED contract bundle. It owes:

1. a **confirmation-profile registry contract** (a new neutral contract, or an
   extension of an existing one) carrying the append-only registry shape
   requirement 3 ratifies, plus the profile id / version / content-digest /
   activation-checkpoint / standing binding added to the receipt's mint-time
   configuration block;
2. the **widen-or-replace of `anchor-state.schema.yaml`'s closed per-witness
   `status` enum**, separating `submitted` from `confirmed` per network;
3. requirement 2's fixed-UTC durability batch, eligibility-registry and
   daily-Merkle construction machinery, added on top of the realized
   receipt/anchor-state pair — additive schema and validator work, but
   unstarted.

**WHY THE DEADLINE IS REAL, AND MEASURED RATHER THAN ASSERTED.** Item 2 is a
**breaking** change to a closed enum's member set: every existing `landed` value
would have to be re-evaluated against the new submitted/confirmed split. Against
an UNPUBLISHED schema that costs nothing; against a PUBLISHED one it is a
compatibility break, and a released receipt is never silently reinterpreted. The
window is open **right now**, and only just:

* `contracts/manifest.yaml` declares `contract-v3.3` and carries **54**
  `chain-anchoring` references — #629 registered the family in the manifest.
* `contracts/releases/contract-v3.3.digests.yaml` carries **ZERO**
  `chain-anchoring` entries. The schemas are REGISTERED but have NOT SHIPPED in
  any tagged bundle.
* The arithmetic that makes that so, stated because it is a twenty-minute
  margin and not a comfortable one: the `contract-v3.3` tag was cut at
  `16b85614`, **2026-09-03T23:35:19-04:00**; #629 merged at `11feff75`,
  **2026-09-03T23:55:32-04:00**. **`contract-v3.3` PREDATES #629 by twenty
  minutes**, which is the only reason the enum is still unpublished and the only
  reason this obligation is cheap.

`tasks.md` § 2.4 remains live for exactly this: the successor VERIFIES,
immediately before it changes any schema, that no bundle cut the family in
between — and if one has, it STOPS and governs the compatibility and version
class before touching the enum, rather than discovering the break at a consumer.

## What ratification does NOT authorize

Stated as a list because a ratification record that leaves this implicit is how
a realization acquires scope nobody granted it.

1. **No code lands here.** Not one line of any
   `contracts/chain-anchoring/*.schema.yaml`, not one line of
   `scripts/validate-chain-anchoring.py`, not one test, not one fixture. The
   realization is the NEXT PR.
2. **No schema is edited here** — and specifically, `anchor-state.schema.yaml`'s
   `status` enum is **untouched** by this commit. The widen/replace is named
   above as an obligation, and naming an obligation is not discharging it.
3. **No confirmation-profile registry is authored, approved or published**, and
   no `daily-Merkle` construction profile is released. `tasks.md` § 1.3 and
   § 1.4 stay OPEN by design: those are operator approval acts, not authoring
   acts, and this ratification performs neither.
4. **No contract bundle is cut and no tag is published.** `contract-v3.3` stands
   as the declared bundle, unspent by this change; the next additive minor is
   allocated by merge order **at realization**, never reserved by a proposal —
   the standing rule this estate has kept since the `contract-v1.28` renumber
   sweep. `tasks.md` § 3.3 is the cut and it is not fired here.
5. **No runtime is commissioned.** No signed-log instance identity, signer
   chain, custody owner, reachable interface or current checkpoint is claimed by
   this act, and none is implied by it. `tasks.md` § 2.5 states the
   realization-versus-commissioning split and this record does not close it.
6. **Requirement 1 is not decided on its merits.** It is WITHDRAWN, not refused.
   Nothing here rules that an operational PKI plane is unnecessary for runtime
   commissioning; #629's OPEN item 2 and its `[OPERATOR]` conditions remain the
   place that question lives.
7. **The ratified `add-chain-anchoring` capability is not reopened.** Its witness
   configuration, ordering, no-selectivity rule, receipt/state split, timing
   model, privacy boundary and claim-not-factory failure semantics are CONSUMED
   and unmodified — there is no `## MODIFIED Requirements` block in this delta,
   and none is created by this act.
8. **This change does not archive, and the archives it names are not
   reordered.** `tasks.md` § 3.2 stands: `add-chain-anchoring` archives FIRST to
   create canonical `chain-anchoring`, this amendment SECOND, with all eleven
   promoted requirements verified byte-for-byte against their two deltas — nine
   from the basis plus this amendment's two. **The basis has not archived yet**
   (its realization merged; its archive is a separate act), so neither archive
   is performed or authorized here.
9. **This record does not merge PR #548.** Merge is the orchestrator's act, on
   the owner's ruling.

## The review record — fourteen Copilot rounds, five substantive Codex rounds, and a Codex NON-REVIEW across the bring-forward

**22 review threads, ALL RESOLVED, ZERO UNRESOLVED** at ratification time —
verified through the GraphQL review-thread listing rather than by eye
(`totalCount 22`, `isResolved: true` on every node). Twelve are Copilot's, ten
are Codex's.

**CODEX REVIEWED THIS PACKET SUBSTANTIVELY, AND THAT IS RECORDED RATHER THAN
FLATTENED INTO THE USUAL USAGE-LIMIT NOTE.** Across five rounds on five named
heads, Codex produced **ten findings — two P2 and eight P1** — and every one was
taken into the requirement text rather than deferred. They are the reason
requirements 2 and 3 read as they do, and a reader who takes them for authoring
polish will misjudge the delta:

| Round | Head | Findings |
|---|---|---|
| 1 · `2026-08-31T23:37:57Z` | `9231654e` | **P2** declare the proposal's origin; **P2** require a deterministic Kaspa `submitted` state |
| 2 · `2026-09-02T08:37:23Z` | `b5879f17` | **P1** bind eligibility-registry CONTENTS (not just the version label) into the manifest; **P1** select ONE confirmation profile per daily item |
| 3 · `2026-09-02T09:03:58Z` | `3dfbad6d` | **P1** commit to the previous daily ITEM rather than its event root — consecutive empty days share one deterministic root; **P1** define or commit the daily Merkle construction, or two conforming implementations produce different roots |
| 4 · `2026-09-02T09:50:58Z` | `f08fd768` | **P1** bind the close watermark into each daily manifest — otherwise a minter omits the final admissions and lowers its own `last sequence` and `event count` to match; **P1** define deterministic eligibility-VERSION selection |
| 5 · `2026-09-02T10:23:15Z` | `adccf578` | **P1** model registry retirement as an append-only TRANSITION rather than an edit to a published entry; **P1** refuse ambiguous confirmation-profile snapshots |

Each of those P1s is a hole through which a conforming implementation could have
produced an unverifiable or non-reproducible batch, and each is now closed by
named normative text and its own scenario — the close watermark and resolving
checkpoint, the content-digest binding, the `previous_daily_anchored_digest`
continuity link, the released `daily-Merkle` profile, the unique-active-entry
selection rule, and the append-only activation/retirement transition.

**Codex was a NON-REVIEW across the bring-forward, and a usage-limit reply is
recorded as a non-review rather than read as approval.** `@codex review` was
posted **13** times on this PR over its life; the `chatgpt-codex-connector` bot
replied **8** times with *"You have reached your Codex usage limits for code
reviews."* Critically, **both invocations after the requirement-1 drop** —
`2026-09-04T04:13:29Z` on head `614b849b` and `2026-09-04T04:47:39Z` on head
`2677cef9` — were usage-limit refusals. **Codex has therefore produced zero
findings and zero verdicts on the ratified head**, and that is stated plainly:
the substantive Codex record above is against the THREE-requirement delta, and
no Codex verdict exists on the two-requirement delta the owner ratified. Silence
here is a quota, not a clean bill.

**Copilot — fourteen review posts, ending 🟢 on the ratified head.** The
findings pass at authoring (`9231654e`) raised the missing `origin:` declaration
and a grammar fix; `8bccd96c` raised two document-shape findings (`tasks.md`
missing its `# Tasks …` title, `spec.md` missing its `# … Specification` title),
both taken. `1200e7e5`, `8eb604ff` and `a6cc5261` generated no new comments,
`a6cc5261` being the first 🟢 *Approval recommended*. `b5879f17`, `89a75dfa`,
`3c0ada4e`, `c2a8ebd1` and `adccf578` raised wording and consistency findings —
an ungrammatical canary clause, a duplicated movement-log bullet in the sweep
pin's docstring, a dangling-comma sentence break in the durability bullet — all
taken. `3dfbad6d` returned 🔵 *Needs a closer look*, its stated reason being that
the packet *"introduces substantial new normative contract/spec requirements and
governance-critical semantics that merit final human review"* — which is what
this record performs.

**THE ROUND THAT MATTERS MOST IS THE BRING-FORWARD ROUND, because it caught the
withdrawal being half-done.** Copilot on `614b849b`, `2026-09-04T04:16:15Z` — 🟡
*Changes recommended*, **five findings, all taken** — showed that dropping
requirement 1 from the delta had left five artifacts still describing it as live:
`README.md`'s Active-changes entry still opened *"Three semantic gaps survive…"*
and still listed the PKI prerequisite and the mandatory shared-Speckit-feature
linkage in the same entry that announced the drop; `design.md` § Context still
framed the amendment as preserving three obligations; its Goals list still
carried making the PKI dependency normative; decision D2 still read as an active
decision rather than a historical one; and `tasks.md` § 1.1 still said *"three
additive requirements"* directly above a note saying there were two. **A
governance packet that contradicts its own withdrawal is worse than one that
never withdrew** — a later reader cannot tell which half is current — and the
repair commit `2677cef9` is what makes this record's baseline coherent.

**Copilot's final verdict on the ratified head `2677cef9`,
`2026-09-04T04:47:30Z` — 🟢 *Approval recommended*, zero new comments**: *"The
changes are consistent, self-contained documentation/spec additions that
correctly integrate into the README index."* No fix is owed against it, and no
Copilot thread is unaddressed.

**Sourcery is an upsell stub on this repository** — it posted its standard
*"Your private repo does not have access to Sourcery"* comment on 2026-08-31 and
reviewed nothing.

## One inherited red, cleared before ratification and recorded because it shaped the PR's history

This PR spent time on two failures that were never its own, and both are closed.
It sat **CONFLICTING with `main`** on 2026-09-01, during which its required
checks were not merely slow but **never queued** — GitHub cannot compute a merge
ref for a conflicted PR, so every `on: pull_request` workflow needing one simply
never starts, while `merge-master-approval` keeps reporting green because it does
not need one. And on `a6cc5261` its `pytest-suite` was red on
`tests/sequenced_after/test_sweep.py::test_the_live_sweep_reproduces_the_AUTHORING_measurement`
(expected `active_co_modified == 19`, observed `18`), which reproduced unchanged
on clean `main` with this PR absent and was already open upstream as **#568**.
Both are historical: `main` has since replaced that hand-written pin mechanism
entirely with the ledger-based system (`add-per-change-sweep-ledger`,
`corpus-ledger.yaml`), this branch took `main`'s side whole at the 2026-09-04
catch-up merge and satisfied its ledger obligation with the tool rather than by
hand, and **all seven required checks are green on the ratified head**. Recorded
because the bring-forward's merge resolutions are only legible against it.
