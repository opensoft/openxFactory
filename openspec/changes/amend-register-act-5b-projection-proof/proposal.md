---
code_surface: none — MEASURED, not assumed. The delta is requirement prose and the realization is two sentences of ONE operator runbook, and nothing mechanical reads either. Evidence, taken 2026-09-11 against openxFactory `main` `78d2c6f53d2591fefb695fd8be2d97801daeecf2`: (1) `grep -rn "governed-reissuance-runbook" scripts/ tests/ .github/ contracts/` returns NOTHING, exit 1 — no script, test, workflow or contract resolves, quotes or gates on the runbook this change amends; (2) the capability this delta writes, `review-authority-intake`, has NO promoted specification, so no validator, schema or fixture can be keyed to a requirement title or a scenario count that this packet moves; (3) no `governance/review-authority/` file, no `contracts/` file, no schema and no workflow is edited — not the register, not a grant, not a wallet, not a custody attestation, not `contracts/openxwallet-pin.yaml`, and not `.github/workflows/openxwallet-consumer-gate.yml`; (4) the ONE file this packet touches under `tests/` is `tests/sequenced_after/corpus-ledger.yaml`, a GENERATED REGISTRY gaining this change's own sweep row through the sanctioned `scripts/validate-sequenced-after.py . --seed-ledger`, which is derived from the packet's existence rather than authored, and is what the sweep gate reconciles against the corpus. Under `release-realization` an empty code surface archives ON LANDING plus its own task list rather than on merged-plus-green realization evidence — and the runbook edit is a TASK in that list (§3), so the archive is still gated on it.
target_release: implemented — the value `release-realization` names for a doc-only change: *"A proposal without the declarations is a doc-only change (`code_surface: none`, `target_release: implemented`) by default"* (`openspec/specs/release-realization/spec.md:24-30`). No contract bundle is cut, nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, no digest set moves, no release tag is owed, and no consumer's pin has to advance to receive this. The realization of a requirement amendment IS its promotion at archive, plus the two runbook sentences § 3 names.
sequenced_after: [add-wallet-carried-review-authority, register-gate-rules-council-seats]
---

# Proposal: amend-register-act-5b-projection-proof

Status: draft
Proposed: 2026-09-11, in lane `hermes-wallet-exercise` (window `codeXfactory-2`,
workstation Eagle), as the CITED CHANGE that Brett Heap's disposition of
2026-09-11T03:01:28Z queued by name.
Lane: hermes-wallet-exercise
Origin: The disposition entry
`openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`
§ `## Disposition — design § D4 step 5b`, landed on openxFactory `main` by PR
[#951](https://github.com/opensoft/openxFactory/pull/951) →
`1fb6d5cdc03e1df89a7c36b4bd308f07fc7c8b77` (2026-09-11T09:54:56Z), and its
codexFactory pointer landed by PR
[#389](https://github.com/codeXfactory/codexFactory/pull/389) →
`d26e8bf2582d07976dc6def9c9aaabb2eb4eaf60` (2026-09-11T09:58:37Z).
Family: the projection half of `add-wallet-carried-review-authority`'s S5
  register-act family, raised by the 2026-09-11 governed re-issuance of
  `gate_rules_council`'s holder and by no other event.

**NOTHING IS RATIFIED BY THIS PACKET AND IT ASSERTS NO APPROVAL.** It is
`Status: draft`, its `.openspec.yaml` carries the drafting provenance pair
(`proposed_by`/`proposed_on`) and no approval pair — the lawful unapproved
shape `add-drafted-proposal-origin` (issue #318) defined. **Seven decisions are
put for Brett Heap as multiple choice** (§ Open questions); each carries a
RECOMMENDED option with the one-line reason it is recommended, and **the
recommended option is the one the delta already ENCODES**, so a ruling that
takes every recommendation moves not one byte. Ruling otherwise on OQ-1, OQ-2,
OQ-4 or OQ-5 rewrites the requirement it names; ruling otherwise on OQ-3, OQ-6
or OQ-7 moves the packet rather than the wording.

## Why

**A ratified re-issuance procedure tells its walker to prove the register
projection by watching a convening get admitted, and no convening in this
estate reads the register projection.** The step was walked on 2026-09-11, the
walker STOPPED at it, and the stop is the finding.

The disposition entry that records it, verbatim from
`openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`
§ `## Disposition — design § D4 step 5b` (on `main` at `1fb6d5cd`):

> **THE FINDING.** codexFactory
> `openspec/changes/clarify-gate-rules-decline-position/design.md` § D4 step 5b
> — carried forward into `docs/governed-reissuance-runbook.md` and into §9.3 of
> this record — makes ***"verify one convening admits"*** the exit condition for
> the projection step, on the reading that an admitted `gate_rules_council`
> convening is itself proof that the register projection has been re-derived and
> carries the new grant. **That exit condition is UNREACHABLE AS BUILT.** §13.2
> establishes it against shipped code and this estate's own landed records: the
> convening admission path reads the **domain-content** projection, while the
> **register** projection is read only by `DatabaseSeatExerciseGate` inside
> `verdict_for_completion`, which this lane never reaches because legs 3 and 4 do
> not exist (ratified phase 6, ungated). An admitted convening proves the council
> content, the pin and the once-per-pin discipline; it proves nothing about grant
> state. Worse, dispatched at the wrong moment it returns a **green admission
> against a stale projection**, which the design's own wording would then read as
> clearance — the manufactured-clearance failure the governed-re-issuance
> discipline exists to refuse.

and the ruling this packet exists to discharge, same section:

> **THE RULING.** Brett Heap, multi-choice, **2026-09-11T03:01:28Z**:
> **disposition entry now, cited change later.** … **a narrow OpenSpec change
> amending `design.md` § D4 step 5b is QUEUED for after this ceremony closes.**

**THE CEREMONY HAS CLOSED.** The governed re-issuance ran end to end on
2026-09-10/11: T1 codexFactory PR #374 → `02e14c086d5ead77d0c390c33ba5df622f07a4df`
(2026-09-10T23:34:23Z); **T2** the register act, openxFactory PR #941 →
`f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0` (2026-09-11T02:29:10Z), revoking
`grant-grc-0001`, minting `grant-grc-0002` and repointing `row-grc-0001`; the
revocation-window check EMPTY under both candidate upper bounds; the projection
step proved by the substitute this packet is about; the hold lifted 04:10Z; and
one proof convening ADMITTED, run `34586762846`, `GRC-CONVENE-ba83adc8983b-34586762846`.
The walk record carries §§1–15 on `main` (last append PR #954 →
`f80ef2ecac9ef901ecee51a01d4c289862513da1`).

### The evidence the amendment is written on — the substitute, and what it proved

Recorded at the same record's §14.1 and reproduced here because the requirement
text is derived from it:

| | Value |
|---|---|
| Authority | Brett Heap, 2026-09-11T03:01:28Z, verbatim *"Operator word: hermes-wallet-exercise reads it"* |
| Executing lane | `hermes-wallet-exercise` — NAMED by the word, not self-selected |
| Wait condition | first refresher cycle after T2; Job `hermes-register-projection-refresher-29818320` created `2026-09-11T04:00:00Z`, `succeeded=1` (CronJob `lastSuccessfulTime` `2026-09-11T04:00:08Z`) |
| The read | `2026-09-11T04:03:38Z–04:03:40Z`, one invocation, every command a `kubectl get` with `-o jsonpath`/`-o custom-columns`; no `apply`, `patch`, `create`, `delete`, `edit`, `rollout` or side-effecting `exec` |
| What it read | ConfigMap `hermes-register-projection` → `hermes.opensoft.one/source-revision` = **`61cee60d85ec53a1107033fe0aea55ffe8987fa0`**; `projected-at` `2026-09-11T04:00:02Z`; `projection-digest` `sha256:10b1fb62…` |
| The comparison | `gh api repos/opensoft/openxFactory/compare/f0eea7ed…...61cee60d… --jq .status` → **`ahead`** — the published projection was derived from a revision of `main` that already carries T2 |
| Stated limit | proof **BY SOURCE REVISION**. The three row-level confirmations (`row-grc-0001` reading `grant_ref: grant-grc-0002`, the matching `expires_at`, and `projected_from.staleness_bound` still `P7D` verbatim) were **NOT** separately read, and §14.1 carries them as OWED |

**And the counter-example is in the same record.** The one proof convening that
was dispatched before the clean candidate, run `34561266626`, was refused
`council.self_review_refused` — *"not `review_authority.register_stale`, not
`review_authority.grant_revoked`"* (§14.3). The admitted one, run
`34586762846`, was refused nothing at all (§15.2). **Neither run's outcome moved
with the register**, which is the finding stated as a measurement instead of an
argument.

## A correction this packet owes the record, and makes in the open

**THE PHRASE THE DISPOSITION QUOTES IS NOT IN THE SENTENCE THE DISPOSITION
NAMES**, and the difference decides where the amendment goes. Measured
2026-09-11:

* codexFactory `openspec/changes/clarify-gate-rules-decline-position/design.md`
  § D4 **step 5b, as ratified**, reads in full: *"The register act alone does
  not un-park anything; the runtime resolves authority against an
  operator-established projection with a declared staleness bound. Step 5
  without 5b leaves the runtime refusing on a stale projection."* It names the
  artifact and the bound. **It states no exit test.** `grep -n "convening
  admits"` over that file returns exactly ONE line — line 463, inside the
  2026-09-11 annotation itself.
* The words ***"VERIFY ONE CONVENING ADMITS"*** are openxFactory
  `docs/governed-reissuance-runbook.md` **§5.2 step 3**, and the walk record's
  **§9.3 heading** repeats them. The runbook is what codexFactory `tasks.md` §3
  points its walker at by name.

So the defect is the RUNBOOK'S SENTENCE, reached from step 5b rather than
written in it. The disposition's attribution is a fair summary of the effect
and an imprecise one about the location, and this packet says so rather than
inheriting it: **nothing in codexFactory needs amending, and the sentence that
does is in this repository.**

## What changes

**FOUR ADDED requirements on `review-authority-intake`**, and two sentences of
one runbook at realization. In one line each:

1. **A re-issuance's projection step exits on an observed projection, never on
   an admitted convening** — the exit condition itself, and why an admission is
   silent rather than merely weak.
2. **The projection observation is a read-only act on a named operator's word,
   recorded with its values** — who may perform it, with what verbs, and what
   the record must carry.
3. **A projection observation follows a refresh that post-dates the register
   act, and the staleness bound does not stand in for one** — the precondition,
   stated as an EVENT and not as a clock, and the reason currency is not
   content.
4. **A projection observation states the limit of what it establishes** — the
   provenance-versus-content gap, recorded as owed rather than quietly covered.

At realization (§3 of `tasks.md`), `docs/governed-reissuance-runbook.md`:

* **§5.2 step 3** — the *"VERIFY ONE CONVENING ADMITS"* exit condition is
  replaced by the observed-projection test. The step keeps its true half (*"The
  park is not lifted by a green validator"*) and loses its false one (*"it is
  lifted when a real convening is admitted against the new grant"*).
* **§ "Contents" of the walk record** (the `step-5b` evidence bullet) — *"which
  convening was watched admitting"* becomes the observation's values and its
  stated limit.

**A THIRD SENTENCE IS MEASURED AND PUT AS OQ-4 RATHER THAN TAKEN QUIETLY.**
§5.2 step 2 says the bound *"is loose on purpose because nothing refreshes the
projection automatically."* That is no longer true: `hermes-register-projection-refresher`
runs `0 */2 * * *` and its cycle of 2026-09-11T04:00Z is the precondition the
2026-09-11 walk waited on. The correction rides with OQ-4 option A because it
is the same subject; it is NOT taken if OQ-4 is ruled otherwise.

## Why the delta is ADDED and not MODIFIED

`review-authority-intake` has **no promoted specification**: `openspec/specs/`
carries no directory of that name, because both changes that author the
capability — `add-wallet-carried-review-authority` (ratified 2026-08-23) and
`register-gate-rules-council-seats` (ratified 2026-09-06) — are ACTIVE and
neither has archived. There is no promoted requirement to modify, so the delta
is `## ADDED` and `sequenced_after:` declares both parents. **The consequence is
stated rather than discovered at the archive gate:** these four requirements
promote when THIS change archives, and if it archives before its parents the
capability's promoted file is created by a packet that is not its author. That
ordering is put as OQ-6.

## Why openxFactory and not codexFactory

1. **The sentence lives here.** Measured above: the exit condition is
   `docs/governed-reissuance-runbook.md` §5.2 step 3, an openxFactory document.
2. **The codexFactory home is being archived.** `clarify-gate-rules-decline-position`
   is pre-staged for archive as codexFactory draft PR #392 (`git mv` into
   `openspec/changes/archive/2026-09-11-…`), and its § D4 step 5b already
   carries the pointer annotation that says *"Nothing in this design is amended
   by that disposition."* Amending an archived change-local design would
   contradict canon's own rule that the durable record of a superseded step is
   the archived delta.
3. **The subject is domain-neutral.** The register, the projection, the
   staleness bound and *"a composition roll is a governed re-issuance"* are
   `review-authority-intake`'s, and the aggregation's working rule 1 puts
   neutral contracts here and forbids a domain repository from authoring them.
   Nothing in these four requirements names `gate_rules_council`, codexFactory,
   or any domain.

## Open questions — MULTIPLE CHOICE, for Brett Heap

**Each option is real, each RECOMMENDED option is what the delta already
encodes, and taking every recommendation moves no byte.**

**OQ-1 — What step 5b's exit condition becomes.**
- **A (RECOMMENDED)** — a DIRECT OBSERVATION of the published register
  projection's declared source revision, at or after the register act's landed
  commit. *Reason: it is the only check that reads the artifact the runtime
  actually resolves authority from, and it is exactly what was performed and
  proved on 2026-09-11.*
- **B** — build a reachable gate-side check: a required check that reads the
  register projection and reports its source revision. *Cost: nothing in the
  repository can see cluster state today; this is phase-6/runtime work and
  leaves 5b unexitable until it exists.*
- **C** — remove 5b's exit condition entirely and keep the projection as record
  evidence only. *Cost: turns a control into a note; §5.2's whole point is that
  the register act does not reach the runtime without the projection.*
- **D** — keep *"verify one convening admits"*, deferred until legs 3 and 4
  exist and a convening reaches verdict completion. *Cost: the step is
  unexitable for as long as phase 6 is ungated, and the wording that produced a
  manufactured-clearance risk stays in force meanwhile.*

**OQ-2 — How much the observation must read.**
- **A (RECOMMENDED)** — the declared source revision alone, with the unread
  row-level fields named as OWED with an owner. *Reason: it is what was actually
  proved, and requiring more would make the landed 2026-09-11 walk retroactively
  non-conformant.*
- **B** — source revision AND the three row-level confirmations
  (`grant_ref`, `expires_at`, `staleness_bound` verbatim), mandatory. *Cost:
  strictly stronger, but no walk has done it, so adopting it needs an explicit
  sentence that the 2026-09-11 precedent stands.*
- **C** — either, at the observer's discretion, recorded. *Cost: a discretionary
  bar is not a bar.*

**OQ-3 — Where the concrete field name lives.**
- **A (RECOMMENDED)** — the REQUIREMENT stays neutral (*"the published register
  projection's declared source revision"*); the RUNBOOK names the concrete
  artifact (ConfigMap `hermes-register-projection`, annotation
  `hermes.opensoft.one/source-revision`). *Reason: openxFactory owns neutral
  contracts and the deployment shape is hermes-install's to move.*
- **B** — name the concrete annotation in the requirement too. *Cost: a
  ratified requirement then moves whenever a deployment detail does.*
- **C** — neutral everywhere, concrete nowhere. *Cost: the walker is left to
  guess which field is "the declared source revision".*

**OQ-4 — Whether the refresher cycle is a stated precondition, and in what
terms.**
- **A (RECOMMENDED)** — state it as an EVENT: a refresh cycle that COMPLETED
  after the act landed, evidenced by the refresher's own success record; and
  correct §5.2 step 2's *"nothing refreshes the projection automatically"* in
  the same edit. *Reason: `0 */2` is a deploy detail that can change; the
  invariant is "a refresh that post-dates the act", and the stale sentence
  beside it would contradict the new one.*
- **B** — state it as a CLOCK: name the `0 */2` cadence and wait for the next
  tick. *Cost: pins a requirement to a CronJob schedule hermes-install owns.*
- **C** — say nothing about timing. *Cost: re-opens the exact failure of
  2026-09-11T02:5xZ, where the live projection was 45 minutes old, well inside
  `P7D`, and derived before the act.*

**OQ-5 — Who may perform the observation.**
- **A (RECOMMENDED)** — a named human operator's word that NAMES the executing
  lane; read-only verbs only; recorded with commands and values. *Reason: the
  read crosses from the governed tree into a running system, which is a
  governance fact and not tooling convenience.*
- **B** — any lane, under a standing ceremony word given once at the start.
  *Cost: the crossing stops being a named act, which is what made the
  2026-09-11 read auditable.*
- **C** — the operator personally, no lane. *Cost: correct and unavailable; it
  is the bottleneck the "named lane" shape exists to relieve.*

**OQ-6 — Delta class and archive ordering.**
- **A (RECOMMENDED)** — `## ADDED` on `review-authority-intake`, and this
  packet does NOT archive before `add-wallet-carried-review-authority`; the
  ordering is declared in `sequenced_after:` and named in `tasks.md` §5.
  *Reason: the capability's promoted file should be created by its author, not
  by an amendment to it.*
- **B** — `## ADDED` and archive whenever ready, accepting that this packet may
  create the promoted file. *Cost: a four-requirement file that reads as the
  whole capability until its parents land.*
- **C** — hold the packet entirely until a parent archives, then re-cut it as
  `## MODIFIED`. *Cost: the defective runbook sentence stays in force for as
  long as the parents do.*

**OQ-7 — Home capability.**
- **A (RECOMMENDED)** — openxFactory `review-authority-intake`. *Reason: it
  already owns the register, the staleness bound and "a composition roll is a
  governed re-issuance".*
- **B** — openxFactory `roles-authority-model`, which owns park/route/interrupt.
  *Cost: the park is the consequence; the register projection is the subject,
  and it is not in that capability.*
- **C** — codexFactory `domain-hermes-content`. *Cost: a domain repository would
  author a neutral contract, against working rule 1.*

## What this deliberately does not do

* **It does not amend codexFactory.** § D4 step 5b keeps its ratified text and
  its 2026-09-11 pointer annotation, and the archive of
  `clarify-gate-rules-decline-position` (draft PR #392) is untouched by this
  packet.
* **It does not rewrite the walk record.** `walk-2026-09-11-register-act.md` is
  `Status: record`; this change is cited back INTO it by name at archive, as a
  dated append if anything, and never as an edit.
* **It does not ratify the runbook.** `docs/governed-reissuance-runbook.md`
  keeps `Status: draft`; its own header rules why, and §3's edit does not move
  it.
* **It does not build the gate-side check of OQ-1 option B**, and it does not
  claim one is unnecessary — only that it does not exist today.
* **It does not touch the register, any grant, wallet, custody attestation,
  pin or workflow**, and it re-issues nothing.
* **It does not read the three owed row-level fields.** Naming them as owed is
  the requirement; reading them is the next operator's occasion.

## Impact

* **Affected capability:** `review-authority-intake` (openxFactory) — four
  ADDED requirements, twelve scenarios.
* **Affected documents at realization:** `docs/governed-reissuance-runbook.md`
  (two sentences; three if OQ-4 = A).
* **Affected procedures:** every future governed re-issuance walked from that
  runbook, and the archived 2026-09-11 walk only by citation.
* **Not affected:** the register and its files, the pinned reader, the consumer
  gate, the convening trigger, and every domain repository.
