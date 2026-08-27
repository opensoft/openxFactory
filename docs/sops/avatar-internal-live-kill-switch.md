# SOP: Avatar Internal-Live Kill Switches

Status: draft
Kind: runbook
Repository context: openxFactory

- Operational status: active for the `internal_live` ring only
- Owner: openxFactory avatar platform maintainers
- Holder of both switches for this ring: **Brett Heap**
- Applies to: the `gpt-realtime-2.1` internal-live qualification ring
  (`qualify-avatar-live-voice`), its canary cohort, and the recorded
  revoke-versus-block policy at
  [`contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`](../../contracts/avatar-client/canary-cohort-and-rollback-policy.yaml)

## Provenance

RULED 2026-08-27 by Brett Heap, in session, as `qualify-avatar-live-voice`
§7.7. The ruling has three parts and this document is the second of them:

1. **The holder.** Brett Heap holds BOTH kill switches for the internal-live
   ring. A person, not a role — §7.4's page target and §7.7's switch holder
   were the same gap seen twice, and naming one human closes both.
2. **The mechanism.** A DOCUMENTED RUNBOOK ACT on the serving install —
   flipping the two server-side kill-switch flags. Not a web console: the
   console is an explicit kernel non-goal
   (`repo-boundary-governance` "Deferred aggregation and web-console
   integration"), so no operator surface was inherited and none is invented
   here. This document IS the operator surface.
3. **The rota.** DEFERRED to `avatar-pilot-hardening`. One named human is
   sufficient for a ring whose cohort is internal staff and one internally
   staffed domain sandbox; it is not sufficient for a pilot with real
   tenants, and the successor change owns that widening.

## What the two switches are

The kernel gives this ring exactly two server kill switches and no more —
`avatar-client-runtime` "Deterministic-first release gating and kill
switches": *"Two server kill switches SHALL exist — all new session creation,
and per model profile — each with optional revocation of active leases."*
Finer-grained scopes (media, tools, retention, drafts) are deferred with the
features they would govern, so an operator asking for one is asking for a
switch that does not exist.

| Switch | Scope | Effect when set |
| --- | --- | --- |
| `SWITCH-ALL-NEW` | ALL new session creation, every profile | The control API refuses every new session at preflight, whatever profile it names |
| `SWITCH-PROFILE` | One model profile — here `gpt-realtime-2.1` | The control API refuses new sessions on that profile only; other profiles are untouched |

### The two modes each switch carries

Revocation of active leases is OPTIONAL on each switch, and the option is not
the operator's mood — it is selected by the recorded policy. Both switches
therefore have exactly two modes:

- **`block_new`** — new work is refused immediately; IN-FLIGHT LEGS DRAIN to
  their natural terminal. Nothing mid-conversation is cut.
- **`revoke_active`** — new work is refused immediately AND affected active
  leases are revoked: media revoked, capture stopped, credential-free
  terminal, control channel healthy.

`revoke_active` reuses the landed consent-withdraw-mid-speech terminal path
exactly. No new terminal is invented for a kill-switch act, and none may be.

### Which mode, for which trigger

The selection rule is the recorded policy, not this runbook. Read it there;
it is reproduced here only so the operator does not have to hold two
documents open:

| Rollback class | Trigger mode | Switch act | Session outcome emitted |
| --- | --- | --- | --- |
| ROLLBACK-A — hard safety or integrity breach | automatic | `revoke_active` | `revoked` |
| ROLLBACK-B — latency, elevated error, or quota | automatic | `block_new` | `abandoned` (or `completed` if the leg reached its natural terminal first) |
| ROLLBACK-C — quality or cost judgment | OPERATOR — this runbook | operator-selected | whichever the selected scope binds, per the two rows above |

ROLLBACK-A and ROLLBACK-B fire from the §6.3.3 detection wiring. ROLLBACK-C
is the class this runbook exists for: it is a judgment call read off
telemetry, and the operator selects both the switch scope and whether active
leases are revoked. The operator ALSO holds the manual path for A and B —
automation that has not fired is not a reason to wait.

## The act

**What is contract-level, and stated here.** Each switch is server-side state
that the broker's control API reads at session preflight, and that the lease
authority reads when the selected scope requires revocation. Setting a switch
takes effect for NEW work immediately — the kernel's scenario "Emergency kill
switch is activated" requires the control API to "enforce the selected scope
immediately for new work and revoke affected active leases according to the
recorded policy".

**What is install-side, and deliberately NOT stated here.** The concrete flag
names, their storage, and the exact command that writes them belong to the
serving install, and the serving install DOES NOT YET EXIST — task 6.1.2, the
provisioning of the dedicated spend-capped internal-live provider project and
its broker deployment, is unticked. Writing a command here that nobody has
run would be a fabricated procedure, which is worse than an honest gap.

This split is not improvised: it is the same one §7.1's credential custody
ruling makes. The neutral half — the two scopes, the two modes, the selection
rule, the holder — lives in this repository. The concrete half lands in the
consuming install's own PR, and that PR is what turns the steps below from
shape into procedure.

### Procedure (shape — completed by the install PR)

1. **Decide the scope.** `SWITCH-PROFILE` unless the condition is not
   specific to `gpt-realtime-2.1`. `SWITCH-ALL-NEW` is the wider blast radius
   and stops sessions that were never part of this ring.
2. **Decide the mode** from the table above. If the trigger is a safety or
   integrity breach, it is `revoke_active` and it is not a judgment call.
3. **Set the flag** on the serving install. The install PR supplies the flag
   name and the write path; nothing in this repository writes it.
4. **Observe the effect, do not assume it.** New sessions refused; and for
   `revoke_active`, affected legs terminated with media revoked and capture
   stopped.
5. **Record the act** — who, when, which switch, which mode, the trigger, and
   the observed effect. A kill-switch act with no record cannot be told apart
   from an outage.
6. **Escalate** per the section below.
7. **Clearing a switch is a separate decision** with its own record. A switch
   cleared because the alert stopped is a switch cleared for the wrong
   reason: state why the condition is resolved.

### Rollback target — read before clearing anything

Rollback DISABLES VOICE and offers TEXT or HUMAN HANDOFF.
`gpt-realtime-2.1` is the FIRST qualified live profile, so **no model
fallback exists**. There is nothing to swap to, and an operator who believes
otherwise will wait for a hot-swap that cannot happen.

An abort ENDS THE MEDIA PLANE ONLY. The authority-owned workflow projection
and the policy-required structured records survive every abort — revoking a
leg ends media, never the logical session's governed record.

## Escalation and the alert path

**The page target for the usage meter is the same human who holds these
switches — Brett Heap.** That identity is the point, not a coincidence:
§7.4 ruled the alerting path on the condition that *the person who learns
about the spend is the person who can stop it*. An alert with no named
recipient and a kill switch with no named holder were recorded as one gap,
and the §7.7 ruling closes both ends of it.

The two alert channels, neither of which builds new infrastructure:

- The provider project's own native budget notifications on the dedicated
  internal-live project, at 50% and 80% of the ruled project cap.
- `gh issue create` from the metering job on the doc-health pattern — one
  issue per run, supersede-and-close the prior — on a per-tenant metered
  crossing of the ruled monthly budget, or on any cost-triggered session
  kill.

An untested alert path is indistinguishable from no alert path: at least one
alert must be observed DELIVERED end to end before the canary opens (§7.4;
wiring is task 6.1.4).

## Pre-canary obligation — RING-04

This runbook is the procedure that RING-04 rehearses, and RING-04 is a HARD
PREFLIGHT element of the four-element ring:

> Both server kill switches — all-new-session-creation and per-model-profile —
> exercised for real, each in BOTH block-new and revoke-active modes, BEFORE
> any canary traffic.

"Exercised for real" means exercised, not dry-run. A rollback path first
exercised when it is needed is not a rollback path — scenario ALV-003-S02
keeps the gate closed while it is unproven. RING-04 proves the SWITCH; it
does not prove the DETECTION, which is what the separate
`EXIT-ROLLBACK-B-REHEARSED` canary exit criterion is for.

## Limits of this document

- It covers the `internal_live` ring only. The pilot ring's data-handling
  review, real-tenant scale, and the operator rota belong to
  `avatar-pilot-hardening`.
- It names no vault, no provider project id, no flag value, and no
  credential. `credential-contracts` forbids a contract artifact hard-coding
  a vault operator, a vault product, or any secret value, and this
  repository is a contract artifact tree.
- It is not the exit contract. The binding exit contract is the kernel's
  four-element ring, recorded in
  [`internal-live-activation-checklist.yaml`](../../contracts/avatar-client/internal-live-activation-checklist.yaml).
