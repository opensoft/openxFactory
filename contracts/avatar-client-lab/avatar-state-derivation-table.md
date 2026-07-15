<!--
Status: ratified
Ratified by: adopt-avatar-client-lab-candidates (tasks 4.1-4.3)
Kind: neutral acceptance artifact (avatar-client-lab) — landed at
  contracts/avatar-client-lab/avatar-state-derivation-table.md
  (+ machine-readable companion avatar-state-derivation-table.yaml).
Provenance: adopted from codexFactory branch 002-avatar-client-lab @ 3a8fbd5
  (7/7 panel-confirmed; evidence in
  specs/002-avatar-client-lab/upstream-drafts/p1-derivation-table/ — README.md +
  escalation-memo.md, and the feature's upstream-drafts/STATUS.md). The body below
  is byte-faithful to that source EXCEPT: this D6 header swap; §8 "open questions"
  replaced by §8 "Ratifications" (the six OQ dispositions with citations and the
  product-owner sign-off, Brett 2026-07-15); the OQ-5 mapping change
  (governed_action_pending ⇒ listening, not thinking); and the OQ-6 scoping
  amendment (blocked is the lawful INV-2 fail-closed target). Those resolutions are
  applied consistently in this file and its .yaml companion.
Evidencing purpose: the neutral acceptance artifact FR-012/SC-002 gate (ix)(a) and
  gate (vi) name as "the avatar-state derivation table (plan P1)" — maps the four
  authoritative runtime axes (the ten closed media.states + AVC-12
  control_health/session_outcome) to the six avatar states. deriveAvatarState
  implements it faithfully; gate (vi) tests against it. Machine-checked fail-closed
  by scripts/validate-avatar-client.py::check_avatar_state_derivation_table.
-->

# Avatar-State Derivation Table (neutral, openxFactory-owned)

**Status:** ratified — landed by `adopt-avatar-client-lab-candidates` (tasks 4.1-4.3;
product-owner sign-off Brett 2026-07-15, recorded in §8 Ratifications).
**Owning task:** `adopt-avatar-client-lab-candidates` — the new owning openxFactory
task the P1 escalation required (the source folder's `escalation-memo.md` was the
escalation instrument).
**Supersedes the interim posture:** the spec's normative derivation invariants
governed in the interim (spec Clarifications Q2/Q3, data-model §6). This landed
table REPLACES that interim posture with the exact named combinations below.

## 1. Purpose and scope

`avatar-client-runtime` owns four **authoritative runtime axes**, consumed
read-only and never authored by the client (`docs/avatar-first-ui-standard.md`
§15):

1. **session lifecycle** — broker-owned;
2. **control health** — lease-derived (`control_health ∈ {healthy, degraded, lost}`);
3. **media state** — trusted-adapter observation constrained by authority (the
   ten closed `media.states`); and
4. **workflow projection** — Hermes/workflow-authority-owned.

This table is the single neutral, openxFactory-owned acceptance artifact that
maps those axes (with the AVC-12 `session_outcome` terminal) onto the **six**
avatar presentation states of the replaceable renderer seam (FR-019):

```
listening · thinking · speaking · interrupted · blocked · handoff
```

The app-land selector `deriveAvatarState(NormalizedViewState) -> AvatarPresentationState`
implements this table faithfully (session-core.md); CI **gate (vi)**
(authority-derivation) tests the selector against it; and the
`control_health`/`session_outcome`-combination half of **gate (ix)(a)**
(state-reachability, FR-012/SC-002) is decided by the exact combinations this
table names.

**Non-negotiable framing (settled law):**

- The renderer receives **only** a presentation state derived from authority —
  **no kernel state** — owns no clock, and cannot affect authority (FR-020).
- Presentation state MUST NOT be used to author, imply, or fabricate an
  authoritative transition (standard §15). This table is a projection **out of**
  the authority axes; it never feeds back into them.
- A fixture evidences a denominator `media.state` ONLY through **kernel** fields
  (the AVC-12 snapshot `media_state` populated to a closed ten-enum value,
  `control_health`, `session_outcome`) — never the app-land presentation
  `media_state`, never derived in-app (spec L4; data-model §4). **This rule
  scopes gate (ix)(a) state-reachability EVIDENCING only. It is distinct from
  `deriveAvatarState`'s own DERIVATION input, which IS the reduced
  `NormalizedViewState.media_state` app-land presentation projection
  (data-model §4/§6; session-core.md) — see R5 (§4) — because R1–R4 already
  intercept every control-health, handoff, terminal, and interruption value
  before R5 ever reads `media_state`, so R5 only ever observes the ten
  closed-state subset of that superset field.**

## 2. The input axes (exact enumerations)

### 2.1 `media.state` — the ten closed states (denominator; FR-012)

From the pinned, content-addressed `avatar-first-ui-profile.schema.yaml`
(`media.states` enum — the authoritative FR-012/SC-002 denominator):

```
permission · capture_authorized · capture_pending · capture_active ·
listening · speaking · control_degraded · control_lost ·
governed_action_pending · retention_active
```

Kernel **normalization** (AVC-12 `control_health` → denominator `media.state`):
`lost ⇒ control_lost`, `degraded ⇒ control_degraded` (data-model §4; plan
gate (ix)(a)). The two **control** `media.states` are therefore evidenced through
the `control_health` axis, not through a `media_state`-carrying fixture. The
landed UI seeds carry the control condition **already-flavored** in that field —
`control-lost-failure.yaml`'s snapshot is `control_health: control_lost` (plan
P12; data-model §4) — which is the denominator value itself, so it *normalizes to
itself*, whereas the AVC-12 conformance cases carry the enum value `lost` (which
normalizes to `control_lost`). This reachability flavoring is the **inverse** of
the derivation canonicalization in §2.2 (they serve different purposes).

> **Presentation superset (NOT denominator).** The landed UI seeds also emit the
> app-land presentation values `idle` (P4 denial), `blocked` (P5 control-loss),
> and `revoked` (P6 revocation). These are presentation projections in the
> observed superset (data-model §4), **not** members of the ten-state
> denominator, and per locked decision 6 the seeds are not rewritten. This table
> reads them only as evidence of the underlying kernel condition
> (`session_outcome`, `control_health`).

### 2.2 `control_health` — AVC-12 (`avc-12-state-snapshot.schema.yaml`)

Canonical closed enum: `healthy · degraded · lost`.

**Control-axis canonicalization (before precedence; normative — data-model §4,
settled law L4).** A fixture may present the control condition in **either**
surface encoding: the canonical enum (`lost` / `degraded`, the AVC-12 conformance
cases) **or** the already-flavored denominator-`media.state` form
(`control_lost` / `control_degraded`, the landed UI seeds — e.g.
`control-lost-failure.yaml`'s snapshot `control_health: control_lost`; §2.1, plan
P12). Before the §4 precedence runs, `deriveAvatarState` **canonicalizes** the
control axis (the inverse of §2.1's reachability flavoring):

```
control_lost ⇒ lost · control_degraded ⇒ degraded   (already-flavored ⇒ canonical)
healthy · degraded · lost                            (pass through unchanged)
```

After canonicalization the control axis is always exactly one of
`{healthy, degraded, lost}`. Two consequences are load-bearing for §4: the
already-flavored control values are **recognized** — NEVER an R0 unknown-enum
trigger — and R1's `control_health ∈ {degraded, lost}` matches **both** encodings
(so the P5 seed's `control_lost ⇒ lost` resolves via R1, not R0 — §6). This holds
whether a consumer reads the kernel snapshot `control_health` (which may be
already-flavored) or the reduced `view_state.control_state` (which the reducer
already emits canonical — `control-lost-failure.yaml`'s `control_state: lost`):
both routes land on R1.

### 2.3 `session_outcome` — AVC-12 (`shared-definitions.schema.yaml` / `session-outcomes.registry.yaml`)

Closed enum: `granted · denied · completed · abandoned · expired · revoked ·
session_limit_reached`. Plus **absent/unset** (no terminal reached yet).
`granted` and absent are **non-terminal**; the other six are **terminal**.

### 2.4 `session_lifecycle` — broker-owned (open string; AVC-12 `session_lifecycle`)

Neutral interaction-state vocabulary (`docs/avatar-first-ui-standard.md` §9).
The values this table consumes are the **handoff** signals
(`handoff_requested`, `handoff_active`) and the **processing** signals
(`tool_request_pending`, `workflow_waiting`,
`comprehension_or_confirmation_check`). The exact binding to the runtime's
session-lifecycle transition registry is ratified in §8 Ratifications (OQ-1).

## 3. Normative derivation invariants (embedded — settled law, binding)

These are the spec's derivation invariants (spec Clarifications Q2/Q3, FR-020,
data-model §6, session-core.md). INV-1, INV-3, and INV-4 are reproduced
verbatim as the constraints this table MUST satisfy. INV-2's *trigger*
condition is likewise verbatim; its *target avatar state* (`blocked`) is
ratified by the OQ-6 scoping amendment (§8 Ratifications). The rules in §4 are
the total, gap-free realization of these constraints:

- **INV-1.** `control_lost` / `control_degraded` ⇒ `blocked` — **never**
  `speaking`.
- **INV-2 (fail-closed target ratified — OQ-6 scoping amendment; §8).**
  Unknown enum / unknown producer / forbidden key ⇒ fail-closed safe state —
  this trigger condition is verbatim from spec Clarifications Q2/Q3, FR-009,
  data-model §6, and session-core.md. Those sources name the trigger but not the
  avatar presentation the safe state renders as. The OQ-6 ratification (§8) makes
  `blocked` (R0, R6) the lawful target by an explicit amendment: **`blocked`
  derives ONLY from `control_lost` / `control_degraded` (INV-1) OR the INV-2
  fail-closed condition** — grounded in FR-018(b), which groups a fail-closed
  local failure together with control/policy-channel loss on the same labeled
  safe/unavailable surface. This is a ratified mapping, no longer a bare
  candidate choice; see §8 Ratifications (OQ-6).
- **INV-3.** `handoff` ⇒ `handoff`.
- **INV-4 (P6 revocation-terminal nuance).** Consent-withdraw-mid-speech (P6 seed
  `consent-withdraw-mid-speech.yaml`: `control_state: healthy` /
  `media_state: revoked`) is a **clean authored revocation terminal** — the
  avatar LEAVES `speaking` to a **non-speaking, non-`blocked`** state. `blocked`
  derives **ONLY** from `control_lost` / `control_degraded` (INV-1), never from a
  healthy-control terminal.

**Landed-seed corollary (binding, plan P11).** The five landed deterministic
seeds reach only the avatar states `{listening, thinking, speaking, blocked}`
and NEVER produce an `interrupted` or `handoff` avatar-state transition.
Therefore the P6 revocation terminal of INV-4 resolves to **`listening`** (the
only `{listening, thinking, speaking, blocked}` member that is non-speaking,
non-blocked, and carries no processing). `interrupted` and `handoff` are reached
ONLY by not-yet-landed fixtures (P11).

## 4. Derivation procedure (normative core — precedence-ordered, total)

`deriveAvatarState` evaluates the rules **top to bottom; the first match wins**.
Precedence ordering is what makes the mapping **total and contradiction-free**:
every possible `(session_lifecycle × control_health × media.state ×
workflow_projection × session_outcome)` tuple resolves to **exactly one** of the
six states, and the ordering encodes INV-1…INV-4 directly.

| # | Rule | Trigger (first match wins) | Output | Basis |
|---|------|----------------------------|--------|-------|
| **R0** | Fail-closed / indeterminate | ANY consumed axis carries a **present-but-unknown/unparseable** enum (`media.state` present and `∉` ten, `control_health ∉ {healthy,degraded,lost}` **after control-axis canonicalization (§2.2)** — the already-flavored `control_lost` / `control_degraded` canonicalize to `lost` / `degraded` and are recognized, so they are NOT R0 triggers, `session_outcome ∉` seven) — an **absent/unset** kernel `media.state` is NOT itself an R0 trigger; a terminal-only snapshot that carries no kernel `media.state` field falls through to R1–R6 on the other axes; OR an unauthorized producer / forbidden key drove the reducer to its fail-closed safe view-state; OR an axis **inconsistency** (`media.state ∈ {control_lost,control_degraded}` while `control_health = healthy`) | `blocked` (ratified — INV-2 fail-closed amendment; §8 OQ-6) | INV-2; lawful via the OQ-6 scoping amendment (FR-018(b)) |
| **R1** | Control-health safety trip | `control_health ∈ {degraded, lost}` (after §2.2 canonicalization — equivalently the already-flavored `control_lost` / `control_degraded`) OR `media.state ∈ {control_degraded, control_lost}` | `blocked` (never `speaking`) | INV-1; P5 `control-lost-failure.yaml` |
| **R2** | Handoff | (`control_health = healthy`) AND [`session_lifecycle ∈ {handoff_requested, handoff_active}` OR `workflow_projection` designates a handoff scope] | `handoff` (shows scope, carries no token) | INV-3; P11 `avatar-handoff-escalation` (landed; §8 OQ-1) |
| **R3** | Authored terminal / clean revocation | (`control_health = healthy`, not R2) AND `session_outcome ∈ {denied, revoked, abandoned, expired, completed, session_limit_reached}` — the **kernel** AVC-12 snapshot field only; never the app-land presentation `media_state` (§1 non-negotiable framing; L4) | `listening` (leaves any speaking turn; non-speaking, non-`blocked`) | INV-4; P4 `governed-action-denial.yaml`, P6 `consent-withdraw-mid-speech.yaml` |
| **R4** | Interruption of an active turn | (`control_health = healthy`, no terminal, not R2) AND an authoritative interruption of the CURRENT turn while `media.state = speaking` — an explicit stop/cancel (`response.cancel` / `output_audio_buffer.clear`) or a superseding new user turn — with the session remaining live (non-terminal) | `interrupted` | FR-019; P11 `avatar-interrupted-barge-in` (landed; §8 OQ-2) |
| **R5** | Live media-state presentation | (`control_health = healthy`, no terminal, not R2/R4) — map `viewState.media_state`, the **app-land presentation projection** `deriveAvatarState` actually consumes (data-model §4/session-core.md; distinct from the gate (ix)(a) kernel-evidencing rule scoped in §1) — by this point R1–R4 have already intercepted every control-health/handoff/terminal/interruption value, so only the ten closed-state values remain observable here (exhaustive, §4.1) | per §4.1 | six-state arc (P3), offline-acceptance (M0) |
| **R6** | Default catch-all (fail-closed) | none of the above matched | `blocked` (ratified — INV-2 fail-closed amendment; §8 OQ-6) | INV-2; lawful via the OQ-6 scoping amendment (FR-018(b); totality guard; unreachable given R0 + R5 exhaustiveness) |

> **R0 / R6 output is RATIFIED (OQ-6 scoping amendment; §8 Ratifications).** The
> `blocked` shown for R0 and R6 is ratified as the INV-2 fail-closed target by an
> explicit amendment (product-owner sign-off, Brett 2026-07-15): **`blocked`
> derives ONLY from `control_lost` / `control_degraded` (INV-1) OR the INV-2
> fail-closed condition** (unknown enum / unknown producer / forbidden key /
> the R0 axis inconsistency). The amendment is grounded in FR-018(b): a
> fail-closed local failure and control/policy-channel loss render the same
> labeled safe/unavailable surface, so the two lawful `blocked` sources share one
> surface. No landed seed exercises R0 or R6 (see §6); the amendment governs the
> mapping in their absence.

### 4.1 R5 media-state map (control healthy; no terminal, handoff, or interruption)

| observed `viewState.media_state` (app-land presentation projection — §1 scoping; NOT the gate (ix)(a) kernel-evidencing field) | avatar state | note |
|---|---|---|
| `speaking` | `speaking` | avatar emitting spoken / transcript output (six-state arc P3) |
| `governed_action_pending` | `listening` (**OQ-5 ratified**) | a governed action is pending approval — a non-speaking awaiting posture mapped like every other awaiting baseline; the action card + status strip (AFU-004 family) surface the governed-action pendency, so `thinking` is not used (it would falsely signal model activity during a governance wait) |
| `permission` | `listening` | pre-capture / disclosure / mic-permission stage — attentive baseline |
| `capture_pending` | `listening` | capture being set up; a held provider answer is **not** active media (§17) — baseline |
| `capture_authorized` | `listening` | capture authorized, not yet speaking (M0 `offline-acceptance.yaml`; the "`listening` (capture_authorized) baseline" label is the sibling `six-state-transition-arc.yaml` / task 4.3's characterization of M0, not M0's own comment) |
| `capture_active` | `listening` | mic actively capturing user input — prototypical `listening` |
| `listening` | `listening` | identity |
| `retention_active` | `listening` | structured-record retention is a background authority flag; the sole-observed baseline is `listening` (typically concurrent with another live state, which — if present as the observed `media.state` — takes that state's mapping) |
| `control_degraded` | (handled at R1) | ⇒ `blocked` |
| `control_lost` | (handled at R1) | ⇒ `blocked` |

> **OQ-5 (ratified — replacement; §8 Ratifications).** `governed_action_pending`
> maps to `listening`, NOT `thinking`. Every other non-speaking awaiting/attentive
> `media.state` above (`permission`, `capture_pending`, `capture_authorized`,
> `capture_active`, `listening`, `retention_active`) maps to `listening`, and no
> released source (standard §17/§18, the UI-profile schema, or the runtime spec)
> grounds routing `governed_action_pending` to `thinking` instead. The
> governed-action pendency is authoritatively surfaced by the action card + status
> strip (AFU-004 family); `thinking` would falsely signal model activity during a
> governance wait. This is a documented ratification replacement of the
> candidate's provisional `thinking` (product-owner sign-off, Brett 2026-07-15);
> see §8 Ratifications (OQ-5).

**R5 processing overlay (`thinking`).** Independently of the `media.state`
baseline above, when `control_health = healthy`, no terminal, not R2/R4, and a
command is in flight — `session_lifecycle ∈ {tool_request_pending,
workflow_waiting, comprehension_or_confirmation_check}` OR a `command_accepted`
event whose `workflow_result` is still pending — the avatar state is `thinking`
(six-state arc: `command_accepted ⇒ thinking`). This overlay takes precedence
over the `capture_*` / `listening` / `permission` / `retention_active` baselines
but NOT over `speaking` (a streamed response in flight presents as `speaking`).

## 5. Enumerated combination matrix (every cell, no gaps)

### 5.1 `control_health ∈ {degraded, lost}` — R1 dominates

For **every** `media.state`, **every** `session_outcome`, and **every**
`session_lifecycle`: the derived avatar state is **`blocked`**. (INV-1; R1
outranks R2/R3/R4/R5.) A fresh authoritative transition — a handoff, a new
speaking turn — cannot be admitted once control is degraded/lost, because the
producer-authority guard drops post-loss authoritative events (session-core.md;
avatar-client-runtime "Leased control channel"). Twenty cells (10 × 2), all
`blocked`.

### 5.2 `control_health = healthy`

Base cell = R5 (no terminal, no handoff, no interruption, no command in flight).
Override columns apply the higher-precedence rules; **read left-to-right, first
non-empty override wins over the base**.

| `media.state` | base (R5) | R2: `session_lifecycle` handoff | R3: terminal `session_outcome` | R4: interruption of active turn | R5 overlay: command in flight |
|---|---|---|---|---|---|
| `permission` | `listening` | `handoff` | `listening` | — (no active turn) | `thinking` |
| `capture_pending` | `listening` | `handoff` | `listening` | — | `thinking` |
| `capture_authorized` | `listening` | `handoff` | `listening` | — | `thinking` |
| `capture_active` | `listening` | `handoff` | `listening` | — | `thinking` |
| `listening` | `listening` | `handoff` | `listening` | — | `thinking` |
| `speaking` | `speaking` | `handoff` | `listening` (leaves speaking) | `interrupted` | `thinking` (n/a while streaming) |
| `governed_action_pending` | `listening` (OQ-5 ratified) | `handoff` | `listening` | — (not a speaking turn) | `thinking` |
| `retention_active` | `listening` | `handoff` | `listening` | — | `thinking` |
| `control_degraded` | `blocked` (R1) | `blocked` | `blocked` | `blocked` | `blocked` |
| `control_lost` | `blocked` (R1) | `blocked` | `blocked` | `blocked` | `blocked` |

- **`—`** in R4 = no active speaking turn to interrupt, so R4 cannot fire; the
  cell falls to its base / next-applicable rule.
- The R3 column covers all six terminal `session_outcome` values identically
  (`denied · revoked · abandoned · expired · completed · session_limit_reached`)
  ⇒ `listening`. The governed **outcome** (denial / cancellation label + cue) is
  rendered in the governed-action card `outcome_slots` / `fallback_slots`
  (FR-018, data-model §9) — a concern **separate** from the avatar state.
- `session_outcome ∈ {granted, absent}` is non-terminal and does not trigger R3;
  such cells resolve at R5 (base or overlay).

## 6. Landed-seed cross-check (verification; must reproduce every seed)

Each of the five landed deterministic seeds MUST derive the avatar state this
table produces. This is a `deriveAvatarState`-**correctness** check: it reads
each seed's `expected.view_state` (deriveAvatarState's actual input, §1) and
confirms the table's rules reduce it to the seed's own stated avatar state. It
is NOT a kernel-evidence check — `media.state` reachability-evidencing (gate
(ix)(a)) is P12-gapped for all eight non-control denominator states (§7), and
two of the five seeds below (M0, P3) carry no kernel `media_state` field in
their canonical AVC-12 snapshot at all. This is the field-by-field
verification anchor:

| Seed (P-row) | kernel condition | table rule | derived avatar state | seed's own statement |
|---|---|---|---|---|
| `offline-acceptance.yaml` (M0) | healthy; `media_state: capture_authorized` is `expected.view_state`'s presentation projection — the canonical AVC-12 snapshot carries no kernel `media_state` field. This IS `deriveAvatarState`'s actual R5 input (§1 scoping), but it does NOT kernel-evidence a denominator state (P12 gap, §7); no terminal | R5 base | `listening` | own comment: "offline-acceptance fixture (SC-006)" (the "`listening` (capture_authorized) baseline" phrasing is the sibling `six-state-transition-arc.yaml` / task 4.3's, not M0's own) |
| `six-state-transition-arc.yaml` (P3) | healthy; `command_accepted` then streamed `transcript_segment`; ends `media_state: speaking`, likewise `expected.view_state`'s presentation projection (the canonical snapshot carries no kernel `media_state` field) — R5's actual input (§1 scoping), not a kernel-evidenced denominator state (P12 gap, §7) | R5 overlay → then R5 `speaking` | `thinking` → `speaking` | listening→thinking→speaking arc |
| `governed-action-denial.yaml` (P4) | healthy, kernel `session_outcome: denied` (the snapshot carries no kernel `media_state` field; `media_state: idle` is `expected.view_state`'s presentation projection, not consumed by R3) | R3 | `listening` (never `speaking`) | "avatar NEVER entering `speaking`" |
| `control-lost-failure.yaml` (P5) | snapshot `control_health: control_lost` (already-flavored; §2.2 canonicalizes ⇒ `lost`, so it is recognized and matches R1 — NOT the R0 unknown-guard); its reduced `view_state.control_state` is already the canonical `lost` | R1 | `blocked` | "derives `blocked`, never `speaking`" |
| `consent-withdraw-mid-speech.yaml` (P6) | healthy, kernel `session_outcome: revoked` (the snapshot carries no kernel `media_state` field; `media_state: revoked` is `expected.view_state`'s presentation projection, not consumed by R3) | R3 (INV-4) | `listening` (leaves `speaking`; non-`blocked`) | "avatar LEAVES `speaking` … a clean authored revocation terminal, not a `blocked` safety trip" |

All five land in `{listening, thinking, speaking, blocked}` (plan P11 corollary
§3). No seed produces `interrupted` or `handoff`. ✓ No contradiction with the P6
revocation-terminal nuance. ✓

## 7. State-reachability denominator — the combinations this table "names"

FR-012/SC-002 gate (ix)(a) denominator = the **ten closed `media.states`** plus
"the AVC-12 `control_health`/`session_outcome` combinations named by the
derivation table." The combinations this table names (i.e. the axis values that
change the derived output for a given `media.state`) are exactly:

1. `control_health = lost` ⇒ evidences denominator `control_lost` (kernel
   `control_health`; landed today via `control-lost-failure.yaml`, P5).
2. `control_health = degraded` ⇒ evidences denominator `control_degraded`
   (kernel `control_health`; **no landed fixture — open tracked gap P13**).
3. the eight non-control `media.states` ⇒ evidenced by a kernel
   `media_state`-carrying fixture (**P12 — not yet landed**), never the
   presentation `media_state`.
4. terminal `session_outcome ∈ {denied, revoked, abandoned, expired, completed,
   session_limit_reached}` ⇒ enters the denominator **only** through R3 (it does
   NOT add new denominator `media.states`; it maps to the `listening` baseline).
   Consistent with FR-012's rule that `session_outcome` "is not an independent
   state-reachability denominator; it enters the denominator only through the
   exact combinations P1's table names."

`session_outcome ∈ {granted}` and absent are non-terminal and name no additional
combination.

## 8. Ratifications (candidate open questions OQ-1..OQ-6, resolved on landing)

The candidate's §8 enumerated six open questions (OQ-1..OQ-6). Each is ratified
below under the new owning task `adopt-avatar-client-lab-candidates` (task 4.1),
against its cited source, with the default posture of design D4: the normative
invariants win; any unsourced mapping is ratified with a citation or replaced.

**Product-owner sign-off: Brett, 2026-07-15.**

- **OQ-1 — RATIFIED WITH BINDING (handoff signal binding).** R2's handoff
  trigger binds to the runtime's session-lifecycle **transition registry** — the
  "transition registry declaring allowed predecessors, terminal states, and
  authority sources" named in the `avatar-client-runtime` capability spec's
  requirement *"Leased control channel and deterministic recovery."* Standard §9's
  `handoff_requested` / `handoff_active` names are kept as **neutral projections**
  of those transitions, signaled via `lifecycle_transition` events on the
  broker-owned `session_lifecycle` axis. Proof path: the landed
  `avatar-handoff-escalation` deterministic seed
  (`examples/avatar-first-ui/fixtures/deterministic/avatar-handoff-escalation.yaml`).
- **OQ-2 — RATIFIED WITH BINDING (interrupted signal binding).** R4's
  `interrupted` trigger binds to an authoritative control-channel stop/cancel —
  the runtime's `response.cancel` / `output_audio_buffer.clear` allowlist — or a
  superseding authoritative turn. Proof path: the landed
  `avatar-interrupted-barge-in` deterministic seed
  (`examples/avatar-first-ui/fixtures/deterministic/avatar-interrupted-barge-in.yaml`).
- **OQ-3 — RATIFIED AS-IS (terminal → `listening`).** Clean terminals map to
  `listening` (R3). This is forced by the closed six-state vocabulary (FR-019),
  which has no dedicated "session ended / idle" state, and by the plan-P11
  corollary (landed seeds reach only `{listening, thinking, speaking, blocked}`).
  **Revisit note:** a seventh presentation state (e.g. `ended`) would be a kernel
  vocabulary change — out of scope for this table; R3's target is the natural
  place to revisit if such a state is ever added.
- **OQ-4 — CONFIRMED (machine-readable form + gate wiring).** The companion
  `avatar-state-derivation-table.yaml` (landed alongside this file) is the
  content-addressed vendored source that gate (vi) tests `deriveAvatarState`
  against, mirroring the P2 client-acceptance-map / capability-scenario-register
  pattern. Manifest registration in `contracts/manifest.yaml` happens at this
  change's section-5 release cut (`contract-v1.12`), not here.
- **OQ-5 — REPLACED (`governed_action_pending` maps to `listening`, not
  `thinking`; D4 unsourced-mapping rule).** The candidate's provisional
  `governed_action_pending ⇒ thinking` is replaced with
  `governed_action_pending ⇒ listening`, applied in both the `.md` prose/tables
  (§4.1, §5.2) and the `.yaml` `media_state_map`. Rationale: no released source
  (standard §17/§18, the UI-profile schema, or the runtime spec) grounds
  `thinking`; every analogous non-speaking awaiting state maps to `listening`;
  governed-action pendency is authoritatively surfaced by the action card +
  status strip (the AFU-004 family), and `thinking` would falsely signal model
  activity during a governance wait. This is a documented ratification
  replacement per D4/D6, recorded here in the provenance/ratification section —
  not a silent edit.
- **OQ-6 — RATIFIED WITH SCOPING AMENDMENT (unknown-enum / fail-closed target).**
  The fail-closed target for INV-2 (unknown enum / unknown producer / forbidden
  key / the R0 axis inconsistency) is `blocked`. It is made lawful by an explicit
  amendment recorded in this table's prose (§3 INV-2, §4 R0/R6): **`blocked`
  derives ONLY from `control_lost` / `control_degraded` (INV-1) OR the INV-2
  fail-closed condition.** The amendment cites FR-018(b), which groups a local
  fail-closed failure together with control/policy-channel loss on the same
  labeled safe/unavailable surface.

## 9. Provenance

Authored as a **candidate** by flutterBench Bench B (parallel drafts lane) for
feature `002-avatar-client-lab`, from the released sources only, then reviewed,
ratified (§8), and landed here by the new owning openxFactory task
`adopt-avatar-client-lab-candidates` (tasks 4.1-4.3). The candidate source —
including the escalation instrument and the sources-consulted / verification
evidence — lives in codexFactory at
`specs/002-avatar-client-lab/upstream-drafts/p1-derivation-table/`
(`README.md` + `escalation-memo.md`) on branch `002-avatar-client-lab` @
`3a8fbd5`. This landed artifact is the neutral, openxFactory-owned source that
`deriveAvatarState` implements and gate (vi) tests against; the codexFactory lab
vendors + pins it at realization.
