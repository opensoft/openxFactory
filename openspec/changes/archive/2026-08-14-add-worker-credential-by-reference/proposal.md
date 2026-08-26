# Proposal: add-worker-credential-by-reference

code_surface: xFactory aggregation (worker-lane fetch steps + runbook §11) + operator-executed provisioning (one KV-reader workload identity per install); openxFactory contract-only otherwise
target_release: implemented — code surface green on the xFactory aggregation main line (this change's declared code_surface, not openxFactory): task 2.3 wired the council-deliberation lane's vault fetch at `0af326a`; task 2.4's live evidence is the §11.4 smokes, operator-confirmed "token source VAULT with SMOKE OK," then a vault-write rotation consumed cleanly by the next run with zero host access; task 2.5 migrated the remaining two lanes and removed the host's service-scoped credential at `6758046`, with the final smoke run `31833019258` (GitHub Actions, `main`, council-deliberation-worker) recording "token source: vault (by reference; rotation is a vault write)" and SMOKE OK, leaving CPC-BRETT01 fully host-credential-free; task 3.1 ticks the archive-gate condition itself ("code surface green: vault fetch live on all three lanes, rotation scenario proven, host credential-free end state reached"). Corroborated by this change's own archive commit `b533a1f` and its README row. No contract bundle was cut — the credential-contracts requirement lands as a strict-validated contract addition within this repository, and the discharge named above is the operator-executed vault-fetch evidence the front matter's own archive-gate condition names. Authored as `implementation_pending — the contract lands now; the change archives on one worker lane fetching its model-provider credential from the vault per-job with green live evidence`, and that condition is what tasks 2.3–2.5 and the final smoke discharged. Left unrewritten by `archive-register-rulings` (PR #265, 2026-08-22) under a ruled freeze that register C3 read as covering this whole change; rewritten 2026-08-22 under Brett's follow-up in-session ruling that the freeze was scoped to the ratification-and-origin axis only, off this change's own tasks.md §2.3–§2.5 and §3.1 (register C1; see register C3 for the ratification half that stays open)

Status: ratified
Ratified: 2026-08-14 by Brett Heap — in-session, verbatim: "I ratify the contract — implement the realization"; realization proceeds directly from this change's tasks per the established lane pattern (Speckit reserved for feature-sized surfaces)

## Why

Between 2026-07-25 and 2026-08-13 three Omnigent worker lanes on the
opensoft CPC fleet were dark because ONE host-profile OAuth session expired
— and nothing noticed, because a host-resident credential fails silently
and its repair requires host administration. The repair itself took
multiple admin round-trips across two days and surfaced the decisive
mechanics (recorded in the codexFactory acceptance-record lineage and the
xFactory registration runbook):

- The Claude CLI's session file is REFRESHABLE STATE, rewritten in place by
  the CLI itself. It is the wrong class of secret to distribute: an
  ephemeral copy's successful refresh rotates tokens into a directory that
  is then discarded, silently staling the master.
- The right class is the LONG-LIVED, NON-ROTATING headless token
  (`setup-token` class), consumed via environment, with an ephemeral
  per-job config dir so no host state is ever read or written. The opensoft
  fleet already runs this shape at SERVICE scope — proven across the
  2026-08-14 acceptance campaign — but service-scope rotation still
  requires host administration and a service restart.
- Self-hosted runner jobs mint GitHub OIDC tokens exactly like hosted jobs,
  so a per-job federated fetch from a vault needs NO standing credential on
  the host: rotation becomes one vault write, effective next job, with the
  vault's access log as the per-fetch audit record.

Brett's two-case ruling (2026-08-11, recorded in the
`hermes-stack-topology-per-client` staging topic) fixes the ownership: a
client may license a domain factory WITHOUT OpsxFactory, so the pattern
cannot be an OpsxFactory capability. The CONTRACT is neutral (this change);
the vault OPERATOR is a per-install execution binding (`opsxfactory_executed`
when licensed, the client's own IT channel when not — the same fork the
client-infrastructure-liaison operating models already ratify); the lane
code is identical in both cases and consumes only bindings.

## What Changes

- `credential-contracts` gains the worker-credential distribution
  requirement: model-provider (and comparable worker-consumed) credentials
  are distributed BY REFERENCE — a vault-held secret of a non-rotating
  headless class, fetched per job by the runner's own federated workload
  identity into ephemeral job scope, with rotation-by-vault-write and
  audit-by-vault-log — and the vault operator is an execution binding,
  never contract content.
- The refreshable-session-file class is named non-conforming for
  distribution (storable nowhere but the host profile it belongs to, and
  preferably not there).
- Service-scoped materialization (the current opensoft shape) is named as
  the PERMITTED DEGRADED MODE where a per-install fetch identity does not
  yet exist: same secret class, same ephemeral job scope, but rotation
  requires host administration — a recorded gap, not a violation.

## Non-Goals

- No new record kinds or schema changes: the grant/binding record shapes
  already carry references; this requirement governs the distribution and
  consumption pattern.
- No mandate on WHICH vault product; the reference is an opaque URI plus a
  fetch-identity binding.
- No change to any lane's model-provider choice (subscription-primary
  stands) or to agent permission matrices (`access_secrets: false` is about
  agent-visible tooling; the job harness handling its own credential is the
  existing, unchanged posture).
- No notification surface for credential expiry (the non-rotating class
  makes expiry a scheduled, calendared event rather than a surprise).
