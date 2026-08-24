# Define Human Escalation Contract

code_surface: none
target_release: implemented
Status: ratified
Ratified: 2026-07-12 — record: this change's own tasks.md 1.1, which closes its one open question "resolved by 2026-07-12 ratification: drafted position stands"; the archive act followed the same day in `5d95fdf`, "Realize and archive define-human-escalation-contract", whose body records "Spec delta (7 requirements) merged into the promoted roles-authority-model capability; archived on landing per code_surface: none". The DATE ONLY is recorded: the task line names no ratifier in prose, so none is claimed. Corroborated by `docs/roles-and-authority.md`'s own header, verified against the live file — "Ratified by: define-human-escalation-contract; amended by add-github-app-identity-tiers". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The authority model tells agents to "request human review" without ever
defining when: Merge Master handles "medium/high-risk actions" and "human
review is required for risky reviews," but *risky* is undefined, the
escalation-boundaries list circularly includes "human-review requirements"
as a trigger, and the engineering escalation table consults an `HR` role
that has been dangling since the original canonical roles doc (#10). Every
undefined trigger decays into one of two failure modes: agents never
interrupt (a governance hole) or agents over-interrupt (the human becomes
the factory's bottleneck and alarm fatigue erases the signal). Human
attention is the scarcest resource in the factory; the contract must set
the interrupt bar explicitly — and set it very high.

## What Changes

- Define the **human-attention escalation ladder** in the neutral authority
  model — every situation needing a decision must be resolved at the first
  rung that can hold it:
  1. **Route** — decidable within some agent authority per the escalation
     tables. Never reaches a human.
  2. **Park** — requires human authority but can safely wait: the workflow
     enters `blocked`, and a decision-ready packet queues at the gate that
     human already owns (ratify gate, admission gate, grant approval).
     The human decides on their own schedule. **This is the default and
     near-universal human path.**
  3. **Interrupt** — claims human attention now. Legal only on containment
     failure: the situation actively deteriorates while parked AND no agent
     can contain it within its declared permissions.
- Enumerate the **exhaustive interrupt classes** (everything else parks):
  suspected live secret or credential exposure no agent can revoke;
  evidence of active unauthorized access to governed systems; an
  irreversible external action already in flight that must be halted and
  no agent holds the halt authority.
- Name the explicit **non-interrupt list**: failed checks, merge conflicts,
  authority deadlocks, contested findings, medium/high-risk merge
  decisions, deadline pressure, and ambiguity of any routed class — all
  park, none interrupt.
- Define the **low-risk enforcement envelope** that bounds Merge Master's
  autonomous approvals (all required checks pass, policy-required governed
  review verdict is ADMIT with no undispositioned conditions, ordinary
  revert suffices as rollback, within approved scope, no open security
  findings) — anything outside it parks at the merge gate; it never
  interrupts.
- Define **parked-decision delivery rules** that keep the human's visit
  cheap: a one-screen decision-ready packet (situation, at most three
  options with one recommendation, evidence references, consequence per
  option and of deciding nothing), deduplication by root cause, and
  fail-closed silence semantics — no answer means it stays blocked;
  timeouts never escalate autonomy.
- Require every interrupt to **cite its trigger class** in the audit
  record; an uncited interrupt is itself a policy violation.
- Require **structural parking**: where the domain's external enforcement
  system supports required human review (for engineering: GitHub branch
  protection/rulesets, CODEOWNERS path scoping, environment required
  reviewers), the parked human gates are encoded there as rules — the
  merge or deploy action is physically held until the human act, parking
  survives agent misbehavior, and the enforcement configuration becomes
  the machine-readable declaration of where a human gate exists.
- Update `docs/roles-and-authority.md` (Merge Master text and escalation
  boundaries) to reference the ladder instead of undefined "risky"/"human
  review" language.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `roles-authority-model`: adds the human-escalation contract — the ladder,
  the exhaustive interrupt classes, the non-interrupt list, the low-risk
  envelope, parked-decision delivery, and the domain-instantiation
  obligation (delta is purely ADDED requirements; existing ownership
  requirements are untouched).

## Impact

- `docs/roles-and-authority.md` — gains the human-escalation contract
  section; Merge Master and escalation-boundaries wording updated to
  reference it.
- Domain follow-through (not in this change's tree): codexFactory rewords
  `docs/engineering-roles-and-authority.md:43` to replace the dangling
  `HR` reference with a reference to this contract, and maps the interrupt
  classes to engineering examples; its `omnigent/domain-overlay.yaml`
  routing and stop conditions already conform (they route to agent
  authorities and block rather than interrupt).
- Consistent with the codexFactory `realize-credential-contracts` proposal:
  deploy/production grant approvals are parked decisions at the grant
  gate, not interrupts.
- No code surface; a future doc-health family auditing interrupt-class
  citations is noted as a candidate, not part of this change.
