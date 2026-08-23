# Design: add-notebook-projection-identity

Status: draft

The five decisions this change encodes were dispositioned on the staged topic
`notebook-projection-identity` on 2026-08-23 and merged as PR #272. This
document carries the EVIDENCE behind them — what was executed, what was
verified, what was found wrong — so the ratification read can check the
reasoning rather than re-derive it.

## Ruling 1 — The share-out roster is its own contract, and the mapping proves it

The staged question named its own settling method: attempt the mapping against
`client-identity-roster`, do not assume either way. The mapping was RUN against
the realized schema
(`contracts/schemas/xfactory-client-identity-roster.schema.yaml`, published
through `contract-v1.40`) and its real validator
(`scripts/validate-client-identity-roster.py`), in two variants.

**Honest variant — the share-out facts stated truthfully: 11 validator errors.**

- `identity_kind` is CLOSED to one member, `entra_app_registration`. A human
  Google account is not one.
- `admission_surface` is CLOSED to `business_central`, `exchange`, `device` and
  `directory`. NotebookLM is none of them — and the schema does not merely omit
  it, it ROUTES it away: "non-Entra providers... are a NAMED SUCCESSOR routed by
  `client-infrastructure-liaison`. An identity on a surface outside this
  vocabulary is OUT of roster scope."
- `residency_model` is CLOSED to `client_tenant_single` / `vendor_tenant_multi`.
- `consent_ref` must RESOLVE intra-repo against a consent-instrument record;
  there is no consent instrument for a colleague being shown a notebook.
- `granted_by`, `granted_at` and the hosting account have nowhere to live under
  the schema's eleven `additionalProperties: false` closures.

A NOTE ON THAT COUNT, because two review passes have now disagreed about it in
opposite directions. Eleven is the count of OBJECTS whose `additionalProperties`
is literally `false`, obtained by parsing the schema. A raw
`grep -c "additionalProperties: false"` returns FOURTEEN, because three of its
matches are backtick-quoted prose inside the schema's own header block scalar
(lines 37, 40 and 43), which explains the closure convention rather than
applying it. Eleven is the number that means anything here; fourteen counts the
schema talking about itself.

**Force-fit variant — eight fields knowingly falsified, each marked: passes with
ONE grantee, FAILS with two.** With two people sharing one book the validator
raises `duplicate-identity-key`. The reason is the load-bearing one: THE GRANTEE
IS NOT IN THE UNIQUENESS TUPLE. `identity_key` is `(domain,
admission_surface, authority_class_intended, blast_radius_unit, duty)`, so two
grantees on one book collide by construction.

**The failure is structural, not a vocabulary gap.** The client-identity roster
models ONE PRINCIPAL against MANY SCOPES. A share-out list is the transposed
shape: ONE SCOPE against MANY PRINCIPALS. Widening enums cannot fix a transposed
key, and the family's "no second roster competing for the same ground"
discipline does not apply, because this is not the same ground.

Hence a distinct, small roster keyed on `(hosting_account, user, book_or_alias,
role, granted_at, granted_by)`.

**Two facts from the identity-brokering family bear on it**, both post-dating
the capture (`add-identity-brokering`, active; contracts on main, capability not
yet promoted). It models the HUMAN-persona half of this ground, so roster
entries should reference a persona wherever one resolves. And its
`surface-adoption.schema.yaml` requires `human_accounts_held_by_surface` as a
const `false`, reasoning that "an account that resolves nowhere is an identity
the governed layer cannot name" — so an account sharing to arbitrary
unresolvable Google accounts is a shape the governed layer already refuses. That
REINFORCES the company-account-plus-explicit-roster direction rather than merely
coexisting with it.

## Ruling 2 — The custody rule generalizes an existing requirement; the capture's reason for doubting that was wrong

The staged capture recorded that the two-case operator-hosted-vs-self-hosted
precedent "is a runbook doc, not a spec requirement", and that the principle
"may not be formally owned by `credential-contracts` today so much as documented
beside it". **Both claims were wrong**, and were corrected in place on the
fragment with a dated note rather than silently rewritten.

`openspec/specs/credential-contracts/spec.md` carries the requirement "The
credential vault operator is an execution binding, never contract content"
(lines 133-145), with an operations-factory-operated scenario and a
client-operated scenario. That IS the two-case fork, promoted.
`docs/openxdox-dispatch-credential-binding.md` is its downstream realization
doc.

Two consequences follow, and both are why this change is shaped as it is:

- The custody delta GENERALIZES rather than adds beside. Vault-operator custody
  widens to operated-identity custody, with the vault named as its first
  instance so nothing about the existing lane changes.
- **No new record kind is needed** — which retires the capture's stated risk
  that all five of `credential-contracts`' record kinds are credential-shaped.
  That spec already carries requirements bound to no record kind, and its schema
  is open where a mapping would land: ONE `additionalProperties: false` closure
  in `xfactory-credential-contracts.schema.yaml`, against ELEVEN in the roster
  schema (parsed objects, per the note in Ruling 1 — not the raw grep's
  fourteen).

**An open naming question for the ratification read.** The MODIFIED requirement
keeps its vault-specific HEADER while its body now states the general rule.
Renaming it would be a REMOVE plus an ADD — a heavier act than the disposition
asked for, and one that discards the requirement's identity. The alternative is
to accept a header that under-describes its body until some later change renames
it. This is flagged rather than decided: the ratifier may prefer the rename.

## Ruling 3 — The approval lane is manual, and its record IS the roster

NotebookLM exposes no share or admin API. Re-verified at disposition time:
nothing in this repository and nothing in the platform models third-party
share-request approval. The "request access" flow is an ordinary browser dialog
landing in the account owner's mail, not an API event.

So the lane is a governed MANUAL act — a request lands in the hosting account's
UI, a designated company-policy actor decides it there, and the act is recorded.
This mirrors the client-identity-roster's own "report-only, no automated
remediation" discipline for a case where the acting party has no privileged API:
a governed manual act, evidenced, beats both an ungoverned manual act (today)
and a fictional automated one.

**The unification the capture missed:** the approval act's record IS the
share-out roster entry. Approving writes or updates the roster; denial is
recorded in the same lane. One artifact, not an audit trail beside a list. This
also answers the capture's honest gap that the monitor/approve lane had no
mechanical home — neither `workflow-gate-contract` nor `roles-authority-model`
had to be stretched, because the roster is the home.

## Ruling 4 — Migration follows the 2026-08-10 runbook, and review found two gaps in it

The `split-ideation-book-per-repo` retirement is the template: re-derive under
the declared account, prove parity, then retire by recorded act
(archive-rename, DELETE the alias rather than repoint it, retire the workspace
record in place). Parity is proven against THE CORPUS SCAN, not against the
legacy books — those are the artifact whose fidelity is in question — plus a
final zero-pending dry run.

**Two gaps in applying that runbook here, found in the PR #272 review round
(Codex, P2 each) and verified against the script.** Neither changes the runbook;
both bound what "one run" covers, and both are carried into tasks §4:

1. **A plain `--apply` never creates live session notebooks.** `--session-ref`
   handles exactly one named session and returns before the lifecycle loop —
   the script says so itself: "A SESSION run is only ever about one session's
   notebook: it never syncs a lifecycle book" — and `--session-sweep`
   reconciles and retires but never creates. Every live `xf-session-*` notebook
   therefore needs its own run, or a bulk mode, before the old account is
   retired.
2. **`ensure_workspace_record()` refuses to register the replacement.** It
   derives `record_id` from `spec.key`, unchanged in the new account; finding
   that id present with a different `provider_notebook_id` it prints "reconcile
   by hand" and RETURNS without registering. Retiring the old record on top of
   that leaves the company-hosted book with no active
   `external_source_workspace` record. The 2026-08-10 precedent escaped this
   because its successors were new per-repo keys with new record ids.

## Ruling 5 — The hosting identity must be a Google user account, and Opensoft's is `xFactor001@opensoft.one`

Brett Heap ruled the account type in session: a dedicated Google Workspace USER
account in the operating tenant's own domain, never a consumer Gmail. A
platform fact the capture predates reinforces rather than merely permits it — a
GCP service account CANNOT drive NotebookLM (no API; consumer web UI only), so
the hosting identity MUST be a Google user account, which is exactly what a
Workspace user is. That also settles the staged fragment's loose "company
service account" wording, which Claim 4 had already spelled out correctly as a
"company xFactory user account (Google)".

Brett confirmed the account the same day: **`xFactor001@opensoft.one`**, a
Workspace user in `opensoft.one`, and authorized raising this change on it. The
earlier `xfactory-books@opensoft.one` was a working name and was never created.

## Rejected alternatives

- **Stretching `client-identity-roster` to carry the share-out list.** Rejected
  on executed evidence, not taste — see Ruling 1. The duplicate-key failure is
  the specific proof: the grantee is not in the uniqueness tuple.
- **`client-infrastructure-request` / `client-infrastructure-liaison` as the
  contract home.** Both govern a PAYING CLIENT's own tenant infrastructure under
  a liaison/execution-binding model. This is the operator's own internal
  governance tooling account — a different bounded context. Forcing either
  would misrepresent what those capabilities own. (The roster schema makes the
  same distinction from its side, routing non-Entra surfaces to the liaison.)
- **A new capability for hosting identity.** Unnecessary: the mechanism belongs
  where the projection already lives, and the custody principle where the
  family's two-case precedent already lives.
- **Two sequenced changes instead of one.** Rejected by Q1's resolution: one
  mechanism, one custody rule and one code surface land together, and splitting
  them would ratify a declared field with no custody rule or a custody rule with
  nothing declaring anything.
- **Designing an automated approval flow now.** Rejected on the platform
  constraint — there is no surface to automate against, and designing one would
  be fiction.

## Honest limitations

- **Authentication of a Workspace account to the `nlm` CLI is not solved by
  this change.** The section 6 runbook's browser-login flow assumes a human at a
  keyboard with a ~20-minute session; a company account changes that story and
  this change does not resolve which mechanism it will use. The open operational
  item `docs/notebooklm-sync-open-item.md` tracks that blocker and closes on this
  change's realization, not on its ratification.
- **The share-out roster's artifact form is not fixed here.** Whether it is a
  contract-family schema under `contracts/` with a validator, or a lighter
  governed record, is a realization decision (tasks §2) — the requirement fixes
  its KEY and its role as the approval record, which is what the disposition
  settled.
- **No parity/report mode exists yet.** 2026-08-10's parity was hand-assembled
  from `nlm source list` output. The migration requirement asks for parity to be
  PROVEN, so the mode is worth building rather than repeating by hand.

## Realization mode

The code surface is modest — profile selection, a declared-field read, a bulk
session mode, a record-replacement step, a parity mode, the roster artifact, and
doc amendments — with no new service and no cross-repo runtime. The
`add-roster-device-admission-surface` precedent (archived 2026-08-22) is the
likely route: ratification authorizes the realization tasks, which then land
directly rather than through a successor change. The ratification read decides;
`target_release: implementation_pending` holds either way, because the change
archives only on merged code with green evidence — Opensoft's own cutover onto
`xFactor001@opensoft.one`, parity proven against the corpus scan, and the
personal-hosted books retired by recorded act.
