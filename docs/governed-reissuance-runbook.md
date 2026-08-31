# Governed Re-Issuance — a provider alias roll or composition bump (operator runbook)

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `openspec/changes/add-wallet-carried-review-authority/tasks.md` task
  7.6, written against
  [`rulings-2026-08-29.md`](../openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md)
  R8 (the re-issuance record's five fields) and R9 (in-flight behavior)

**Why this document is `draft` and not `ratified`.** Task 7.6's own text rules
it: *"neither ruling is enforced until the change carrying R6–R12 is ratified,
so this task stays OPEN"*
([`tasks.md`](../openspec/changes/add-wallet-carried-review-authority/tasks.md),
task 7.6). This runbook is written against a settled target, and following it
produces a real, checkable act — but no gate in this estate today refuses a
re-issuance that skips it. **Writing the runbook does not ratify R6–R12, and
walking it does not exercise an enforced control.** That sentence belongs on
every walk record this runbook produces.

---

## Before you start

**A composition bump is a revocation event, not a config edit.** A reviewing
holder's identity IS its declared composition, and the ratified rule is
unforgiving on purpose:

> *"openXwallet SHALL treat any change in an agent's declared composition as
> the end of that agent's certified identity: its outstanding grants are
> revoked at once through the core's revocation-propagation rule, with no
> tolerance band and no grace period, and resuming requires re-issuance
> against the changed composition."*
> — `openspec/specs/openxwallet-agent-profile/spec.md`, requirement *A
> composition change revokes the agent's grants immediately*, in
> **`opensoft/openXwallet`** at the commit
> [`contracts/openxwallet-pin.yaml`](../contracts/openxwallet-pin.yaml) pins.

The same family adds, ratified 2026-08-28 in
`openspec/changes/add-composition-drift-cascade/` (openXwallet PR #3, an
ancestor of the pinned commit):

> *"Resuming authority SHALL require an EXPLICIT, HUMAN-RATIFIED issuance act
> against the changed composition. No automatic reissue, and no standing
> reissue policy that acts on its own, may restore authority."*

and

> *"A declared model component SHALL name an EXACT version. A model family, an
> alias, or any other moving reference is not a pin and is a validation
> failure, because a reference that resolves differently over time defeats the
> hash it is declared into."*

**Read that second quotation twice before you start.** It is why an
alias-to-exact flip is not a tidy-up: the alias was never a pin, so pinning it
is itself the composition bump this runbook is walked against.

You need:

* write access to the repository that OWNS the declaration being bumped (for
  the merge-readiness council that is `opensoft/codexFactory`, not this
  repository);
* the **ratifying human** available, because step 5 cannot be delegated —
  `governance/review-authority/register.yaml` is a *"PERMANENTLY HUMAN-ONLY
  SURFACE (ratified requirement, explicit here by name): no council verdict may
  ever produce an autonomous approval of a change to THIS file"*;
* the ability to **re-derive the Hermes register projection** (step 5b), because
  the register act does not reach the runtime without it;
* the superseded grant's own file open, so you are quoting it rather than
  remembering it.

**What this runbook does NOT establish: the provider plane.** R5 requires the
plane to be EVIDENCED by read-back and never inferred, and that evidence is the
Operator's Packet 2 identity record — a different artifact, a different act.
Reading a Claude Code transport as evidence of a direct-Anthropic plane is the
exact error R5 forbids. Carry the Gate-Rules Council's own sentence onto every
walk record: *"This Council does not evidence the plane and must not appear
to."*

---

## 0. Scope and trigger

### 0.1 What triggers this runbook

Any change to a **declared component** of a reviewing holder's composition. For
the merge-readiness council the declared set is **six components**, enumerated
in codexFactory `hermes/domain/review-councils/merge-readiness.yaml` under
`council.composition_source_map.components`:

**Every path in this table is a `codexFactory` path**, spelled with its
repository because this runbook lives in `openxFactory` and an unqualified
`agent-mixes.yaml` resolves to nothing here:

| Component | Binding | Declared source |
|---|---|---|
| `model_version` | content | `codexFactory:hermes/domain/agent-mixes.yaml#…model_assignments` |
| `prompt_contract` | content | `codexFactory:hermes/domain/agent-mixes.yaml#…prompt_contract` |
| `tool_manifest` | content | `codexFactory:hermes/domain/agent-mixes.yaml#…tool_manifest` |
| `policy_version` | content | `codexFactory:hermes/domain/review-councils/merge-readiness.yaml#council.policy_version` |
| `parameters` | content | `codexFactory:hermes/domain/agent-mixes.yaml#…parameters` |
| `retrieval_corpus` | reference | `codexFactory:hermes/domain/agent-mixes.yaml#…retrieval_corpus` |

A **provider alias roll** touches `model_version` and nothing else. An
alias-to-exact flip touches `model_version` and nothing else. Both are in
scope; both are one bump.

**Any single component is sufficient.** The ratified scenario is *"declared
change is not a percentage"* — *"WHEN any single component of the declared set
changes, THEN the change alone is sufficient to revoke, AND no threshold,
score, or tolerance band is consulted."* Do not look for a second component to
justify the act.

### 0.2 What is NOT a declared component, and why that matters here

Two things execute inside a seat and are declared nowhere:

* **The runtime.** The composition enumerates six components and the runtime is
  not one of them, although the soak's own semantics treat a runtime change as
  invalidating (`codexFactory:scripts/merge_master/codexfactory-routine-code-clearance.yaml`,
  `soak_gate`'s preamble: *"a mid-soak runtime reseed or image change invalidates the rows
  taken before it"*). A reseed is therefore a **soak-invalidating** event that
  is **not** a composition bump — recover it through §6, not through this
  runbook's steps 1–5.
* **The CLI's internal helper model.** `claude-haiku-4-5-20251001` executed in
  **33 of 33** measured judgments of the 2026-08-22 corpus, is declared in no
  composition file, is pinned by no flip, and carries the earliest published
  retirement floor in the surveyed register (**2026-10-15**). Whether it becomes
  a seventh component or lives under `Parameters` belongs to the R6–R12 change
  (`codexFactory:hermes/domain/review-councils/records/2026-08-29-gate-rules-s5-seat-model-selection.md`
  §6.1 P-1), **not to a walk of this runbook**.

**Consequence, and state it on every record this runbook produces:** completing
this runbook does NOT make a composition fully pinned. Repair R-IV of the
2026-08-29 sitting exists to stop exactly that claim.

### 0.3 Who holds which act

Six roles, and the runbook never collapses them
([`rulings-2026-08-29.md`](../openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md),
"Decision-owner honesty note"; R11's `propose → approve → attest → register →
activate → revoke`):

| Act | Holder | Where it is performed |
|---|---|---|
| select a seat's model on duty-specific soak evidence | the Gate-Rules **Council** | a codexFactory selection record |
| accept or reject that output on record | the **convener** | the same record's operator slots |
| apply it to the enrolled roster | the roster-change **Lead**, via `roster_change: lead_accepted_recorded` | a codexFactory **roster-change** record |
| evidence exact provider identity and the plane | the **Operator** | the Packet 2 identity record |
| **register** — issue or re-issue | a named **human ratifier** | `governance/review-authority/` in THIS repository |
| revoke | **no RATIFIER** — the cascade is fail-closed and *"a fail-closed cascade must not wait on a human"* (R11) — but see the note below: today an operator still performs the WRITE | `governance/review-authority/grants/` in THIS repository |

**REGISTER is the only human-ratified act in that list, and RE-ISSUE always
requires one** (R11). If you find yourself about to perform two of these roles
in one motion, stop and disclose it on the record instead — the 2026-08-22
precedent did exactly that when one human held two capacities.

> **REVOCATION NEEDS NO RATIFIER, BUT IT IS NOT AUTOMATIC HERE, AND THE
> DIFFERENCE MATTERS.** R11's point is that revocation must not *wait on* a
> human decision. It is not a claim that something in this estate performs it.
> **Nothing today writes `state: revoked` into a grant file.** The register is a
> file on a permanently human-only surface; there is no daemon, no reconciler
> and no hook that walks a composition change into
> `governance/review-authority/grants/`. Until the drift-cascade change's
> declared realization surface exists, **the write is an operator act**, and the
> only thing that is genuinely automatic is the REFUSAL: the reader fails the
> required gate when a row's grant does not back it, and the runtime refuses at
> exercise. Treat step 5 as a hand-performed act with a machine-enforced
> refusal behind it, and never as a cascade that ran while you were not
> looking.

---

## 1. Step 1 — establish the superseded state

Record what is being ended, before anything is edited. A re-issuance whose
superseded half is reconstructed afterwards is a story, not a record.

Capture, verbatim:

1. **The declaration as it stands.** Every component of §0.1's table at its
   current value, quoted from the file, with the file's commit sha. For a
   `model_version` bump that means each seat's `selector`, `selector_kind` and
   `pin_status` as currently written.
2. **The active grant.** From this repository:
   `governance/review-authority/grants/grant-mrc-0001.yaml` — `grant_id`,
   `audience.wallet_ref`, `audience.holder_ref`, `scope`, `issued_at`,
   `issued_by`, `expires_at`, `state`.
3. **The backing register row.** `governance/review-authority/register.yaml`,
   `rows[row_id: row-mrc-0001]` — all nine fields. The reader enforces exact
   set-equality over them, so quote them as a set, not as a summary.
4. **The composition hash before the bump — and its honest status.**

> **THE CANONICAL HASH DOES NOT EXIST YET, AND THIS RUNBOOK MUST NOT PRETEND IT
> DOES.** R6 (the plane sits INSIDE the digest) and R7 (JSON Canonicalization
> Scheme, RFC 8785, `sha256:<lowercase-hex>`, recorded with the profile name
> and version) are **ratification targets**: *"none of them is implementable
> until the change that carries them is authored and ratified."* Until then,
> record the composition's identity as the **git blob shas of the declaring
> files at the named commit**, label it exactly that, and carry the canonical
> digest field as **PENDING R6/R7**. A locally-invented digest recorded in the
> hash's place is worse than an empty field, because a later reader cannot tell
> the two apart.

---

## 2. Step 2 — the bump, as ONE change

**The edit and every assertion bound to it move in one commit set.** This is not
tidiness; it is a measured property of this estate. In the 2026-08-31
alias-to-exact flip the domain roster edit and the tenant declaration were *"red
in either order alone … One change, both edits"* (2026-08-29 sitting record
§8.5), and a complete four-seat flip was still red where the test literals had
not moved with it.

The rule generalizes: **before you edit, enumerate every place the old value is
asserted**, then move them together.

1. Grep the owning repository for the old value — configuration, workflow YAML,
   tenant declarations, test literals, mutation-test heredocs, run-log strings.
2. Confirm each hit is a **value** and not a **key**. A component's key set is
   an invariant that mutation tests defend; a bump changes values only. If a key
   must move, you are not walking this runbook — you are authoring a
   composition-schema change.
3. Make the edits. Run the owning repository's full gate suite, not a subset.
4. Prove the coupling rather than asserting it: show that the set is green
   whole and red partial. Naming the tests that go red under a partial edit is
   the evidence; "they must move together" is not.

**Where the tenant is involved**, a tenant declaration is amended as a **fresh
dated entry preserving what it supersedes**, never as a silent rewrite — the
superseded declaration stays legible beside its successor with its own date,
authority and record pointer.

---

## 3. Step 3 — the in-flight behavior (R9), verbatim

Everything already in flight when step 2 merges is governed by this, and it is
quoted rather than paraphrased because paraphrase is where grandfathering gets
reinvented:

> **R9 — In-flight: a revoked holder PARKS the convening with a named refusal.**
> No grandfathering. An earlier admission stamp is not honored by an exercise
> that detects a composition mismatch. A parked convening resumes only under a
> new human-ratified issuance act — never by the runtime, never by elapsed time.
> — [`rulings-2026-08-29.md`](../openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md) R9

Operationally, between step 2 and step 5:

* **Expect every convening against the bumped holder to park.** Under
  `missing_required_seat: refused` a fleet-wide revocation parks every in-flight
  convening — which is the cost this pin exists to make *scheduled* rather than
  *unannounced*, and the reason step 5 is scheduled with step 2 rather than
  discovered after it.
* **Do not clear a park by re-running it.** A park is the control working. The
  only exit is step 5 **and step 5b together** — the register act alone leaves
  the runtime refusing on a stale projection (§5.2).
* **Do not honor an earlier admission stamp.** An exercise that detects a
  composition mismatch refuses regardless of when the candidate was admitted.
* **Name the refusal.** A park whose reason does not name the composition event
  that caused it is indistinguishable from an outage, and the ratified scenario
  *"declaring the change is not performing it"* makes an unnamed revocation a
  validation failure in its own right.

**Honest limit.** R9 is ruled DIRECTION. The runtime's enforcement of it — the
rehearsed revoked-holder park of task 7.7 — is tracked separately, and this
runbook's step 3 is a description of the target, not a report of a control you
just exercised. Say which of the two your walk record is describing.

---

## 4. Step 4 — the re-issuance record (R8): five fields, a MINIMUM

> **R8 — Re-issuance record grammar: the five fields are the MINIMUM.** A
> re-issuance act records the superseding grant reference, the superseded grant
> reference, the composition hash issued against, the ratifying human, and the
> effective time. … this ruling adopts them as a floor a carrying change may
> extend, and NOT as a ceiling. It does not make them an already-required record
> format before that change is ratified.
> — [`rulings-2026-08-29.md`](../openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md) R8

Write the five, each on its own line, each either a real value or an explicit
PENDING that names what it waits on:

| Field | What goes in it | If it cannot be filled yet |
|---|---|---|
| **superseding grant reference** | the `grant_id` issued by step 5 | `PENDING — the register act (step 5) has not been performed`; it does not exist before that act and inventing an id is a forgery |
| **superseded grant reference** | the `grant_id` captured at step 1 | never pending — if you cannot name it, you have not established what you are ending |
| **composition hash issued against** | the canonical digest under R6/R7 | `PENDING R6/R7 — recorded instead as the declaring files' blob shas at <commit>`, per step 1's warning |
| **ratifying human** | the named human who performs step 5 | never pending — an unnamed ratifier is not a ratification |
| **effective time** | the instant the superseding grant takes effect | never pending — record the intended instant and correct it at step 5 if it moves |

**A MINIMUM, not a ceiling — so add what your act actually carries.** For a
Council-selected model bump that means at least: the selection record, the
roster-change record and the Lead's acceptance; the identity assertion linking
any alias the prior record ruled to the exact identifier now pinned; and every
condition still outstanding on the selection. **Omitting one of the five is a
defective record. Adding a sixth is the ruling working as intended.**

---

## 5. Step 5 — the register act (POINTER ONLY)

**This runbook does not perform step 5, and walking it does not.** The register
act is sequencing step 5 of
[`rulings-2026-08-29.md`](../openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md)'s
"Sequencing" list — *"The human-ratified register act issues against the
resulting composition"* — and it is:

* **human-only, by ratified requirement.** `register.yaml` says so on its own
  face, by name, and a council whose commission is recorded there is never
  eligible to clear a candidate that edits it;
* **explicit, never standing.** *"No automatic reissue, and no standing reissue
  policy that acts on its own, may restore authority: the act is performed
  afresh each time, by a named human, against the composition then declared";*
* **shape-constrained.** `row-mrc-0001` carries nine fields
  (`row_id`, `holder_ref`, `wallet_ref`, `target_repo`, `act`,
  `authority_tier`, `grant_ref`, `expires_at`, `state`) and the reader enforces
  **exact set-equality** over them, plus an enumerated top level. There is no
  model field on a row and adding one would be refused. A re-issuance does not
  smuggle the composition onto the row.

### 5.1 The atomic acts, in order — and a grant is REPLACED, never revived

**Do not "un-revoke" the superseded grant, and do not edit it back to
`active`.** The ratified core rule is terminal:

> *"A revoked grant SHALL NEVER return to the active state. Authority resumes
> only as a NEW grant, which records the grant it supersedes and the holder
> composition or standing it was issued against. A revocation is therefore a
> terminal fact about that grant rather than a suspension of it."*
> — `openxwallet` core, `add-composition-drift-cascade` (ratified 2026-08-28,
> ancestor of the pinned commit)

So step 5 is **three writes and one non-write**, and they land in ONE change:

1. **REVOKE the superseded grant, in place.** In its own file, set
   `state: revoked` and add the `revocation` block the schema requires —
   `revoked_at` (the instant) and `reason` (naming the **composition event**,
   because a revocation whose reason does not name what caused it is
   indistinguishable from an outage). Reason class is **DRIFT**, and DRIFT
   propagates exactly as CAUSE — *"no derived authority survives on the strength
   of its parent's reason."*
2. **MINT a NEW grant file** — a new `grant_id`, `state: active`, `issued_at`
   the effective instant, `issued_by` the named ratifying human, `expires_at`
   chosen afresh, and the scope carried forward deliberately rather than copied
   without looking.
3. **REPOINT the row.** `grant_ref` → the new `grant_id`; `expires_at` → the new
   grant's, **character-for-character**. **The row's own `state` stays
   `active`** — the row is the authority's continuing existence, not the
   grant's.
4. **DO NOT add a row.** The single-row cap is retained and bounds AUTHORITY
   ROWS; a second row for the same holder and target is refused.

**Why all of it is one change, mechanically.** The reader checks that a row's
`grant_ref` names a grant whose `state` is `active` and whose `expires_at`
equals the row's. Revoke the old grant and stop, and the required gate fails
`register-grant-mismatch: grant state 'revoked'`. Mint the new grant and forget
the repoint, and the row still backs a revoked grant. **There is no order of
these writes that is green halfway**, which is the point: the window in which a
revoked holder looks authorized cannot be entered from this runbook.

**HONEST LIMIT — the "records the grant it supersedes" half has NO FIELD YET.**
The pinned grant schema is `additionalProperties: false` and carries no
`supersedes` key; `parent_grant_ref` means *derived from*, which is a different
relation and must not be borrowed for this one. The drift-cascade change that
ruled the requirement declares its realization surface and does not perform it.
**Until that surface lands, the supersession is recorded in the re-issuance
record of step 4 and nowhere else** — say so there, rather than inventing a
field the validator would refuse.

When steps 1–3 are done, return to step 4 and fill the **superseding grant
reference** and the **effective time**. **The re-issuance record is not complete
until that return trip has happened.**

### 5.2 Step 5b — the projection, or the park does not open

**Landing the register act does not un-park anything by itself, and stopping
here is the commonest way to think this runbook is finished when it is not.**
The runtime does not read `register.yaml`; it reads an operator-established
**projection** of it:

> *"The operator's Hermes register projection
> (`hermes_review_authority_register_projection`, schema_version 2) takes each
> seat row from here plus the authorizing row, the wallet's custody model and
> the grant's constraints — nothing invented — and `revocation_staleness_bound`
> above travels into it verbatim as `projected_from.staleness_bound`. **Until
> the projection is re-derived, the runtime still refuses with
> `review_authority.root_key_mismatch`**; that step is an operator act and it
> must not carry a fact this file does not."*
> — [`governance/review-authority/register.yaml`](../governance/review-authority/register.yaml)

So:

1. **Re-derive the projection** from the amended register. Nothing is invented
   in it: every field comes from the register rows, the authorizing row, the
   wallet's custody model and the grant's constraints.
2. **Carry `revocation_staleness_bound` VERBATIM** into
   `projected_from.staleness_bound`. It is declared on the human-only surface
   **beside the rows it bounds** precisely so a deploy setting cannot loosen it,
   and the runtime holds a ceiling of its own and honours whichever is tighter —
   *"an artifact must never be able to widen its own trust window."* Today the
   bound is **`P7D`**, and it is loose on purpose because nothing refreshes the
   projection automatically; do not tighten it here as a tidy-up.
3. **VERIFY ONE CONVENING ADMITS.** The park is not lifted by a green validator
   — it is lifted when a real convening is admitted against the new grant. Until
   you have seen that, you have evidence that the *files* are consistent and no
   evidence that the *lane* recovered. Record which convening you watched.

**A projection older than the bound REFUSES, never proceeds on the stale copy.**
A re-issuance that lands the register act and skips 5b leaves every convening
parked with a refusal that names a key mismatch rather than the composition
change — the correct outcome reached by a confusing route, and the operator
reading it will look in the wrong place.

---

## 6. Step 6 — provider-roll recovery

For when the provider moves under you rather than you moving first.

### 6.1 The watch, and its honest status

Every pinned identifier carries a retirement or deprecation horizon, and **each
one needs a NAMED HUMAN OWNER** (LQ-C5 and CSC-C3, 2026-08-29 §8.8), for the
reason the sitting recorded in terms:

> *"nothing in the estate reads a retirement date, so every one of these is
> today a promise rather than a control."*

Maintain the watch as a table of `pinned identifier → horizon → named owner`,
and re-state that sentence beside it. A watch table that reads as a control is
worse than no table.

The watch additionally carries the **runtime/reseed** horizon — including the
CLI helper's **2026-10-15** floor (§0.2) — as a runtime item, **not** as a fifth
pinned composition identifier. That scope correction is CSC-C3's own.

### 6.2 When an identifier is retired or re-pointed

1. **Detect it as a mismatch, not as a failure.** The served-model read-back is
   what makes this visible: the served identifier is carried into the run
   artifact beside the declared one, and an exact declaration absent from the
   served map refuses. **An alias-declared seat cannot be verified this way** —
   its read-back is carried and marked unverifiable-by-construction, which is
   precisely the argument for exact pins.
2. **Treat it as a bump, in this runbook's order.** A provider re-point changes
   what `model_version` denotes, so it is §0.1's trigger even though no file was
   edited by you. Run steps 1 → 2 → 3 → 4 → 5.
3. **Expect the parks, and budget for them.** Refusals recommission, and the
   convening budget binds at commission (`max_convenings_per_rolling_24h: 12`,
   `enforced_at: convening_commission`, `uncountable_is: exhausted`). A
   re-commission storm during a roll can exhaust the budget and park the surface
   for reasons unrelated to the roll. **Record budget consumption alongside the
   roll** (LQ-C2) so the two causes stay distinguishable.
4. **A runtime reseed is a different animal.** It invalidates soak rows without
   being a composition bump (§0.2). Order matters: reseed first, then re-pin, or
   the rows taken between the two measure a system that no longer exists.

### 6.3 When a roll is forced and the ratifier is unavailable

There is no automatic path, by ratified rule, and the runbook offers none. The
holder stays revoked and its convenings stay parked until a named human performs
step 5. **Naming that as the cost is the point of pinning: a scheduled
re-issuance instead of an unannounced outage.**

---

## 7. Record the act

A walk of this runbook is a **dated act** and is recorded separately from this
standing document.

**Where.** Beside the change that commissioned it, as a dated artifact —
`openspec/changes/<change>/walk-<YYYY-MM-DD>-<subject>.md` — the pattern the S5
change already uses for its dated rulings, and the archived
`d10-acceptance-runbook.md` precedent for an in-change-dir operator artifact.

**Contents:**

* each step above with **what it produced**, not with a tick;
* the step-1 superseded state, quoted;
* the step-2 bump's identity — the merge commit of the change that performed it,
  and the tests that prove the commit set is green whole and red partial;
* the step-4 five-field record, with each PENDING naming what it waits on, and
  the supersession recorded **in prose** because no grant field carries it yet
  (§5.1);
* the step-5 acts — the revoked grant's id and revocation reason, the new
  grant's id, and the row's repointed `grant_ref`/`expires_at` — and the
  **step-5b** evidence: that the projection was re-derived, that the staleness
  bound travelled verbatim, and **which convening was watched admitting**;
* the honest limits restated, in terms: **R8 and R9 are not enforced until the
  change carrying R6–R12 is ratified**, so the walk demonstrates the runbook
  against a real bump and does not exercise an enforced control; **this walk
  does not evidence the plane**; and **no fully-pinned-composition claim is
  made** while the helper of §0.2 remains undeclared.

**What a walk does NOT do:** it ticks no task by itself. Task 7.6 stays OPEN by
its own text until R6–R12 is ratified, and any ledger movement is a separate,
argued act in the change's own `tasks.md`.

---

## What this runbook deliberately does not do

* **It does not perform the register act, or the projection re-derivation.**
  Steps 5 and 5b are pointers. The act is a named human's, on a permanently
  human-only surface, and the projection that makes it reach the runtime is the
  operator's.
* **It does not evidence the provider plane.** That is R5 and the Operator's
  Packet 2 identity record. Nothing here may be cited as plane evidence.
* **It does not define the canonical composition hash.** R6 and R7 are
  ratification targets carried by a change that is not yet authored; step 1
  records a substitute and labels it as one.
* **It does not enforce anything.** No gate in this estate refuses a
  re-issuance that skips this document. It is a written target, and it says so
  in its own header.
* **It does not claim a fully pinned composition.** The runtime and the CLI's
  helper model are undeclared, and §0.2 keeps that visible on purpose.
* **It does not select a model, accept a roster change, or ratify anything.**
  Those are four different holders' acts (§0.3), and a runbook that let one
  person walk all of them would have re-created the ritual this work exists to
  end.
