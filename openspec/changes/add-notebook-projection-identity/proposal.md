---
code_surface: openxFactory (`scripts/sync-notebooklm-books.py` — the declared-field read, `nlm` profile selection at every CLI invocation, a bulk session-migration mode, an explicit workspace-record replacement step, and a parity/report mode; a share-out roster artifact and its validation; `docs/lifecycle-notebook-projection.md` — section 1's "one shared account" framing and section 6's operator runbook, both written assuming one human's browser session; the install/tenant intake surface that carries the declared field). The GOVERNED SHARE-APPROVAL ACT itself is a human act in Google's own UI, not code — this change gives it a record, not an automation.
target_release: implementation_pending — the requirements land now; the change archives only on merged code with green realization evidence, because its load-bearing claims are executable ones (the sync runs under the declared account; the migration re-derives, proves parity and records the retirement). The evidence gate is Opensoft's own cutover onto `xFactor001@opensoft.one`, parity proven against the corpus scan, and the personal-hosted books retired by recorded act.
---

# Proposal: add-notebook-projection-identity

Status: draft
Proposed: 2026-08-23, the day the staged topic's last precondition was met.
All five of its questions carry dispositions (merged as PR #272), and Brett
Heap confirmed the hosting account — `xFactor001@opensoft.one` — and
authorized raising this change. Ratification is a separate act, still PENDING.

THE REALIZATION RUNS POST-RATIFICATION. No sync-script, roster, doc or intake
edit lands with this proposal itself; its own diff is spec text plus these
records.

## Why

The entire governed NotebookLM projection — every per-repo `xFactory Ideation
— <RepoName>` book, `xf-drafts`, `xf-canon`, and every live `xf-session-*`
notebook — is created by `scripts/sync-notebooklm-books.py` under the `nlm`
CLI's DEFAULT profile, which resolves to one person's personal consumer Gmail
(`brettheap@gmail.com`). Nothing declares that. It is an incidental fact of
whoever ran `nlm login` first.

This was proven live on 2026-08-15. Brett, browsing as his own Workspace
identity (`brett.heap@farheap.com`, managed by tech-corps.com), hit "request
access" on a dashboard "open notebook" link — and the request landed in the
personal Gmail's inbox, where it sat unmanaged. The governed corpus of a
governed product was gated behind one individual's mail.

`docs/lifecycle-notebook-projection.md` already names the disease in its own
words — "the quota is one shared account" — but only as a capacity-planning
fact (the capacity guard, the per-session quota note). The promoted spec goes
further and RATIFIES the premise: "The account is shared between workspaces."
Neither has ever modeled WHICH account, or treated that choice as something an
install declares.

The failure modes are the ones this family has already retired once, in the
personal PAT removed from openXdox dispatch. The projection dies with one
person's account. It misattributes every book's real owner. It gates access
through an inbox instead of a policy. It concentrates the platform's
account-level quota on one individual rather than on the tenant that actually
owns the corpus. And there is no offboarding story at all: the account belongs
to a person, and people leave.

## What Changes

**The hosting identity becomes a declared, two-case intake fact.** An xFactory
install declares which Google identity hosts its NotebookLM projection. Case A,
operator-hosted: a company-owned Google Workspace USER account in the operating
party's own domain, which runs the sync and shares out to individual users.
Case B, self-hosted/personal: an individual installer keeps the books under
their own personal Google account, with no company account implied and no
governance obligation attached. Case B is legitimate, not a degraded Case A —
a person who installs the system for themselves genuinely wants their own
books.

**The account must be a Google USER account, and the reason is a platform
constraint, not a preference.** NotebookLM has no API and a GCP service account
cannot drive its consumer web UI, so no service-principal identity can host a
projection. A Workspace user is exactly the shape that works, and it brings
what a consumer Gmail cannot: admin-console policy, org-owned retention,
offboarding, and no personal-recovery path back to one individual.

**Opensoft's own install declares Case A on `xFactor001@opensoft.one`** — a
Google Workspace user in `opensoft.one`, confirmed by Brett Heap on 2026-08-23.

**The sync runs under the declared account.** `scripts/sync-notebooklm-books.py`
selects the `nlm` CLI profile bound to the declared identity instead of always
taking the tool's default. The CLI is already profile-aware
(`~/.notebooklm-mcp-cli/`), so this selects between an existing mechanism
rather than building new plumbing — but the script passes NO profile today
(`subprocess.run(["nlm", *args])`, no flag, no environment), so this is real
code.

**Access is shared out FROM the hosting account, and every share act is
recorded.** Individual users never authenticate independently against a shared
login. A share request lands in the hosting account's own UI; a designated
company-policy actor approves or denies it there; and the approval act WRITES
the share-out roster. The roster is the record — one artifact, not an audit
trail beside a list. An entry carries the account, the person, the book, the
role, the grant time and the granting actor, and references an
identity-brokering persona wherever one resolves. Its UNIQUENESS is keyed on
the stable `(hosting_account, user, book_or_alias)` triple, with the decision
fields held as attributes, so re-approving or re-roling a person UPDATES their
one live entry rather than adding a second — the grantee is in the key, which
is the whole structural difference from the client-identity roster.

**The custody rule generalizes an existing requirement rather than inventing
one.** `credential-contracts` already promotes "The credential vault operator
is an execution binding, never contract content", with an
operations-factory-operated scenario and a client-operated scenario. That IS
the two-case fork. This change widens it from vault-operator custody to
operated-identity custody, so the hosting account falls under the rule the
family already ratified. No new record kind: that spec already carries
requirements bound to no record kind, and its schema is open where the mapping
would land (one `additionalProperties: false` closure, against eleven in the
client-identity-roster schema — parsed objects; a raw grep says fourteen there
because three matches are the schema's own header prose, see design.md).

**Opensoft's own books migrate, and the old ones are retired by recorded act.**
The projection is derived, never curated, so re-creating the lifecycle books
under the declared account is a re-derivation rather than a data migration.
Parity is proven against the corpus scan — not against the legacy books, which
are the artifact whose fidelity is in question — and only then are the
personal-hosted books retired the way 2026-08-10 retired the shared Ideation
book: archive-rename, delete the alias, retire the workspace record.

### The five dispositions this change encodes

All five are dispositioned on the staged fragment; the two marked BRETT are his
rulings, the rest are adjudications on executed evidence.

1. **Q1 — contract home (resolved).** `lifecycle-notebook-projection` carries
   the mechanism; `credential-contracts` carries the custody rule as a
   generalization of the requirement it already promotes. Neither
   client-infrastructure capability is the home (both are client-tenant scoped),
   and no new capability is proposed. This closed the one-vs-two-changes fork to
   ONE COMBINED change — one mechanism, one custody rule, one code surface.
2. **Q2 — account type (RULED BY BRETT HEAP).** A dedicated Google Workspace
   USER account in the operating tenant's own domain, never a consumer Gmail.
   Confirmed the same day as `xFactor001@opensoft.one`, with the change
   authorized to raise on it.
3. **Q3 — does the share-out roster reuse `client-identity-roster`? (resolved
   on an EXECUTED mapping).** No, and the reason is structural. Run against the
   realized schema and validator, the honest variant produces 11 errors; the
   force-fit variant with eight marked lies passes with ONE grantee and FAILS
   with two on `duplicate-identity-key`, because the grantee is not in the
   uniqueness tuple. That roster models one principal / many scopes; a share-out
   list is the transposed shape, one scope / many principals. A distinct small
   roster it is.
4. **Q4 — the monitor/approve lane (resolved).** A governed MANUAL lane —
   NotebookLM exposes no share or admin API, re-verified — with the unification
   the capture missed: the approval act's record IS the roster entry.
5. **Q5 — migration sequencing (resolved).** The `split-ideation-book-per-repo`
   retirement runbook, step for step, with parity reconciled against the corpus
   scan and retirement by recorded manual act.

## Impact

- **Affected specs.** `lifecycle-notebook-projection` — 2 MODIFIED
  requirements (the ratified shared-account premise; projection implementation
  ownership, which now includes running under the declared account) and 3
  ADDED (the declared hosting identity, share-out from the account with its
  roster, and the migration/retirement obligation). `credential-contracts` — 1
  MODIFIED requirement (vault-operator custody generalized to operated-identity
  custody).
- **Affected code, at realization.** `scripts/sync-notebooklm-books.py`
  (declared-field read; profile selection; bulk session migration; explicit
  workspace-record replacement; parity/report mode);
  `docs/lifecycle-notebook-projection.md` (section 1's shared-account framing,
  section 6's operator runbook); the share-out roster artifact and its
  validation; and whatever install/tenant intake surface carries the declared
  field.
- **Two realization gaps found in review, carried as scope.** A plain `--apply`
  never creates live `xf-session-*` notebooks — `--session-ref` handles one
  named session and returns before the lifecycle loop, `--session-sweep` only
  retires — so the migration needs a bulk session mode or per-session runs. And
  `ensure_workspace_record()` derives its record id from `spec.key`, unchanged
  in the new account; finding that id with a different `provider_notebook_id`
  it returns WITHOUT registering the replacement, so retiring the old record
  would leave the company-hosted book unregistered. The 2026-08-10 precedent
  escaped this because its successors carried new record ids.
- **No client-tenant act, credential, or account is created or granted by this
  change.** The Opensoft account already exists; nothing in a paying client's
  estate is touched.
- **Nothing changes for an install that declares nothing.** The undeclared case
  keeps today's behavior — the CLI's default profile — stated honestly as a
  fallback rather than left unmodeled.
- **Out of scope, deliberately.** Any automated approval flow (the platform has
  no surface for one), any Drive-level or org-wide sharing policy, and the
  `xf-wb-*` cross-checkout deletion bug already recorded as its own change in
  `docs/notebooklm-sync-open-item.md`.
