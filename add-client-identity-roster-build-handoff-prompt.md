# Handoff Prompt: openxFactory — build `add-client-identity-roster` via Speckit feature `007-client-identity-roster`

Prepared: 2026-08-14 by **team-003** (end of a long session; nothing in
flight; no live provider act pending; no client-tenant act authorized by this
work). Revised the same session to route the build through **Speckit** rather
than direct realization — see "Route" below.
Repo: **openxFactory**. OpenSpec change ratified on branch
`change/add-client-identity-roster` (tip `f604626`), PR
**opensoft/openxFactory#173**. `origin/main` at `363f0e8`.
Untracked session artifact — **do not commit this file** (see
`/home/brett/projects/xFactory/HANDOFFS.md`).

## Route: this is a Speckit build, and THIS FILE IS THE SPECIFY SEED

The OpenSpec half is **done and ratified**. Per
`~/.agents/protocols/openspec-speckit-workflow.md`, a change carrying a code
surface hands off to **exactly one** Speckit feature, and the OpenSpec change
archives only after that Speckit work and its PR have landed.

- Feature to create: **`007-client-identity-roster`** (openxFactory has
  `001`–`006` today).
- Precedent to follow: **`specs/006-openxwallet-contracts`** — a neutral
  *contract* feature (schema + validator + contracts), the same shape as this
  one. Read it before starting; it shows how contract realization is
  structured as a Speckit feature in this repo.
- **Do NOT build straight from the OpenSpec `tasks.md`.** Sections 2–5 there
  are the governed *handoff sketch*. Speckit owns the executable task list and
  regenerates it — the protocol explicitly forbids duplicating task lists
  between the two systems. (Same pattern as OpsxFactory's
  `add-request-intake-boundary`, whose OpenSpec tasks were the sketch and
  whose Speckit run produced 37 of its own.)
- Seed `/speckit.specify` from the ratified OpenSpec packet **plus this file**.

### Entry precondition NOT met — clear it before `/speckit.specify`

The protocol requires specify to run from the root checkout on the repo base
branch. As of this handoff:

- openxFactory's root checkout is on **`change/cred-by-ref`** (another lane's
  work, plus this untracked handoff), and
- **`main` is held by another lane's worktree**
  (`openxFactory-worktrees/change-add-wheel-action-verbs`).

Do **not** commit or move another session's work to clear this. Two clean
paths: (a) run specify from a **plain clone** of openxFactory — also what the
submodule-worktree hazard memory recommends over a worktree for commits; or
(b) wait for those lanes to release `main`. Verify with `git status -sb` and
`git branch --show-current` from the same shell before running specify.

## Implementation arrangement (this project's protocol)

Architect seat answers `/speckit.clarify` itself — only genuine scope
*changes* escalate to Brett. An Opus orchestrator runs the execution
(speckit-implement, teammate spawning) with cheaper lanes for mechanical work.
Clarify rounds run at the slightest ambiguity, iteratively. `/speckit-checklist`
runs **no-arg = deep and wide** (max coverage). `/speckit-analyze` loops —
fix ALL findings, re-analyze — until zero. Ultracode/Workflow fan-outs at
**gates only**, never during implement. Every batch of architect rulings gets a
**cross-model adversarial review before dispatch** (write the rulings to a
decision-log file first; subagents cannot read the session transcript).

That review protocol already earned its cost twice on this very change — see
"Two flaws" below.

## Read first (in this order)

1. `/home/brett/projects/xFactory/CLAUDE.md` — shared-tree discipline. Other
   sessions have uncommitted work in these repos right now: stage **explicit
   pathspecs**, never `git add -A`, inspect `git diff --cached --stat` before
   committing. Pushes race — `pull --rebase` and retry.
2. `openspec/changes/add-client-identity-roster/` — the ratified packet:
   `proposal.md`, `design.md` (rejected alternatives — read before changing any
   decision), `specs/` (three deltas), `clarify-questions.md` (five binding
   answers), `tasks.md` (the sketch, not your task list),
   `review/decision-review-2026-08-14.md`.
3. `specs/006-openxwallet-contracts/` — the structural precedent.
4. `openspec/specs/credential-contracts/spec.md` and
   `openspec/specs/consent-instrument/spec.md` — this sits beneath them, and
   you are MODIFYING one.

## The five ratified answers that bind the build (do not relitigate)

1. **Residency class-independent** — client-resident single-tenant default for
   every authority class; `vendor_tenant_multi` only via the governed model
   with full obligations.
2. **Blocking scope: all three** — intra-repo entry conformance BLOCKS the
   owning domain's gate; cross-domain composition REPORTS via doc-health; an
   open drift finding REFUSES grant issuance.
3. **Enrollment as drafted** — permissive axis, `planned` entries allowed, cost
   accepted. If cost bites, the lever is the multi-tenant model with
   obligations, never a quiet relaxation of the axis.
4. **Contract + both wirings** — the change archives only when the contract
   records AND the consent-instrument cascade AND the doc-health family are all
   landed and green. Contract-only is not an acceptable stopping point.
5. **First-release `admission_surface` vocabulary = `business_central` and
   `exchange` ONLY** — the two client-tenant Entra-homed surfaces with
   PROMOTED capabilities. Not endpoint/Intune, Windows 365 or Entra-directory
   (ratified changes, unpromoted capabilities, live targeting unauthorized →
   no live identity to roster); not `github` (promoted but non-Entra, routed by
   `client-infrastructure-liaison` — named successor).

## Two flaws the cross-model review killed — do not reintroduce them

The first draft was rewritten because it (a) keyed uniqueness on
(workload, class), which **forbade a per-environment identity** and thereby
mandated the structural→logical degradation this change exists to expose, and
**invalidated a ratified class** (`microsoft_managed_node_inventory_reader`
deliberately spans Entra+Intune+Windows 365 because the provider offers
nothing narrower); and (b) admitted a `destructive` class, inverting the
ratified position (`opsx_provider_identity: prohibited`,
`max_grant_minutes: 0` — the family holds **no** destructive identity).

Uniqueness is now **(domain, admission surface, authority class, blast-radius
unit, duty)**; classes are **`observe|mutate`** only. **Acceptance test for
your own work: if any schema, validator or fixture you write makes a per-unit
or duty-separated identity a finding, you have regressed it.**

## What the build must produce (the sketch — Speckit will decompose it)

**Contract records.** `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
(note the `xfactory-` family prefix; field list in OpenSpec tasks 2.1 — do not
drop `granted_permissions[]`, which is what makes the axis falsifiable, or
`admission[]`, which is a LIST). Closed `admission_surface` vocabulary per
answer 5. Packaged `examples/` covering the **BC two-admission-act worked
case** (per-environment application user = provider-enforced, Sandbox1; plus
the admin-center Entra-app authorization = tenant-wide, no selector → declared
excess + gate obligation + enforcement test), a provider-forced multi-surface
reader, a duty-separated pair, and one `planned` entry.
`scripts/validate-client-identity-roster.py` (canonical, deterministic,
network-free — follow sibling `scripts/validate-*.py`) with fixtures: one
positive, one negative per rule. A **declared placement** for domain
fragments — required, because `scripts/validate-credential-contracts.py`
SKIPS unknown kinds as "out of scope", so a misplaced instance is silently
unvalidated. `contracts/manifest.yaml` row (copy the last entry's shape:
path, source_path, type, schema_version, **sha256**, compatibility,
adapter_owner, consumption_rule), `contracts/CHANGELOG.md` entry, and the
bundle bump — manifest is at **`contract-v1.31`**, so register at
**`contract-v1.32`**.

**The two wirings + the refusal.** Register the canonical validator in the
**`domain-conformance-checks`** pack so intra-repo conformance is BLOCKING.
Add the **doc-health sixteenth family**, CROSS-DOMAIN ONLY (assemble per-client
fragments from pinned repos; report shared identity material and undeclared
cross-domain reach; do NOT duplicate intra-repo rules) — the spec delta changes
the count word from "fifteen" to "sixteen", and the family list in
`scripts/doc_health/` must agree with the promoted spec or **doc-health
self-gates against you**. Wire the **grant-issuance refusal** so an open drift
finding becomes an `issuance_preconditions` failure — the mechanism exists on
`deployment_operator` / `aks_workload_administration` in OpsxFactory's
`credentials/requirements.yaml`; follow it, do not invent a second. Realize the
**consent-instrument cascade** so governed identities join the
dependent-reference list and cascade evidence covers identity
removal/retirement AND withdrawal of provider-side admission (check whether
`scripts/validate-consent-instruments.py` must learn the new dependent kind).

**Domain follow-ups (NOT archive blockers, executed in the domain repos).**
OpsxFactory publishes its fragment including three findings this investigation
surfaced: the `opsx-farheap-bc-observer` name/purpose mismatch (it achieves
more than observation), an inert Microsoft Graph delegated `User.Read` scope
its identity record omits, and the tenant-wide admin-center excess with its
gate obligation. LedgerxFactory publishes its `ledgerx-farheap-bc-*` fragment.

**Carried open decision — Brett's, not the builder's:** answer 1 makes
LedgerxFactory's ratified multi-tenant Reader/Poster pair non-conformant as
designed; it must either declare `vendor_tenant_multi` with full obligations
(including a **consent amendment per affected client**) or move
client-resident. Do not resolve unilaterally — it touches live client consent
instruments.

## Arm the usage guard in your clone (one command)

A `UserPromptSubmit` guard injects a warning when the 5-hour window, the Fable
weekly bucket, or context crosses a threshold — the model cannot otherwise see
any of them. It is registered for every profile by the launcher, but **gated
per project**, so in the plain clone you create for `/speckit.specify`:

```bash
touch .claude/usage-guard.on                     # arm this lane
git rev-parse --git-dir                          # then add the flag to
# ...   echo '.claude/usage-guard.on' >> "<that>/info/exclude"    (keeps it untracked)
```

The flag is found by walking UP from the session's cwd, so arming the clone
root covers every subdirectory session in it. Speckit worktrees are the
exception: they live in a SIBLING container (`<repo>-worktrees/...`), which is
not inside the repo, so each worktree needs its own `touch
.claude/usage-guard.on`.

The shared checkout at `projects/xFactory/openxFactory` is already armed. At
>=95% of the 5-hour window or the Fable weekly bucket the guard tells you to
stop at a breakpoint and refresh this handoff — follow it; that is the global
CLAUDE.md rule, not a suggestion.

## Mechanics and landmines

- Run `openspec` from the **openxFactory root**, not the workspace root.
  Validate with `OPENSPEC_TELEMETRY=0 openspec validate
  add-client-identity-roster --strict` and `--all --strict` (58 items today,
  all passing).
- **Parser gotcha that bit this session:** strict validation reads only a
  requirement's **FIRST LINE** for SHALL/MUST. Two requirements failed until
  reworded with SHALL on line one.
- Worktrees on this submodule behaved fine this session (`git status
  --porcelain` = 0 immediately after `worktree add`), but a memory warns they
  can misreport deletions — verify porcelain is clean right after creating one;
  if it shows mass deletions, abandon it and use a plain clone.
- The BC evidence chain (v3–v7) motivating this contract is **NOT on
  OpsxFactory main** — it lives on branch
  `evidence/bc-general-verify-probe-20260810` (OpsxFactory PR **#19**, open).
- Follow-on Speckit commands run **from the generated worktree**, not the root
  checkout.

## Do not

- Perform any client-tenant act, mint any credential, or run any live provider
  call. This change authorizes none; the BC investigation's live probes are
  finished.
- Touch OpsxFactory's `007-request-intake-boundary` lane (PR #16) — another
  session owns it. (Note the coincidence: that is OpsxFactory's feature 007;
  this is openxFactory's. Different repos.)
- Commit another lane's work to clear the specify precondition.
- Commit this handoff file.

## Exit criteria

Speckit side: analyze clean, checklists resolved, implementation green —
`openspec validate --all --strict`; canonical validator green over fixtures;
doc-health family green; both MODIFIED capabilities' suites unaffected;
manifest/CHANGELOG/bundle landed. Then the feature PR lands, and only after
that does the OpenSpec change archive per `release-realization` (OpenSpec tasks
5.3). Domain fragments are follow-ups, not blockers.
