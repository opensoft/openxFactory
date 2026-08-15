# Staged: who hosts the NotebookLM projection — company account, declared at install

Status: staged
Kind: capability-proposal
Summary: The governed NotebookLM projection (per-repo Ideation books,
`xf-drafts`, `xf-canon`, session books) is created today under one person's
personal consumer Gmail — verified live 2026-08-15 when Brett's own Workspace
identity hit a "request access" wall on a dashboard notebook link. Brett rules
the normal case should be a company service account, declared as part of an
xFactory install's own intake, with personal hosting kept legitimate as the
other declared case (the exact two-case shape already ratified for the
openXdox dispatch credential); a company-policy Hermes governance job then
monitors that account and approves proper share requests instead of the
access-request loop sitting unmanaged in one person's inbox.
Topics: notebooklm, lifecycle-notebook-projection, identity, credential-custody,
tenant-intake, two-case-hosting, share-out-roster, company-policy-hermes
Repository context: openxFactory owns both candidate target capabilities —
`lifecycle-notebook-projection` (the projection mechanism itself: books,
sync, aliases, the operator runbook) and `credential-contracts` (the
account-custody rule this topic's two-case model would extend) — and is
where `scripts/sync-notebooklm-books.py` already lives. Whichever repo or
install stands up its own xFactory instance is the party that would declare
its hosting account at intake time; today that is Opensoft's own tenant
(`opensoft-company-policy`), the only live install.
Staging ID: openxFactory:staging:notebook-projection-identity
Captured: 2026-08-15
Source: Brett Heap's live-session ruling 2026-08-15, made immediately after
he (browsing as his Workspace identity `brett.heap@farheap.com`, managed by
tech-corps.com) hit "request access" on a dashboard "open notebook" link —
the request landed in the personal Gmail (`brettheap@gmail.com`) that
`scripts/sync-notebooklm-books.py` has always run under, by default CLI
profile, with no declared account of its own.
Target capabilities: MODIFIED `lifecycle-notebook-projection` (declared
hosting-account field for the projection; sync runs under the declared
account; share-out roster from that account) and MODIFIED
`credential-contracts` (the two-case account-custody rule: company service
account as the normal case, personal hosting as the other legitimate case)

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

The following are settled by Brett's 2026-08-15 direction and are NOT
reopened by the open questions below — they are the fixed baseline the
questions iterate against:

1. The notebook projection SHOULD be hosted in a **company service
   account** — the normal case, not an individual's personal account.
2. The hosting account (**"the Google NotebookLM location"**) becomes
   **part of the intake for setting up that xFactory** — a declared
   install-time decision in the tenant setup flow, not an incidental fact
   of whoever happened to run `nlm login` first.
3. **Personal hosting stays legitimate.** A person (not a company) who
   gets and installs the system may genuinely want the books in their own
   personal Gmail. This is a declared **two-case** choice, not a rule with
   corporate as the only legitimate branch.
4. Normal process: stand up a **company xFactory user account** (Google),
   and the system **shares out to users from there** — individual users
   never each authenticate independently against a shared personal login.
5. **Company-policy Hermes** (the tenant layer) gains a governance job:
   **monitor this account and approve proper share requests** — the
   access-request loop Brett just hit manually becomes a governed policy
   lane, not an ungoverned side channel sitting in one person's inbox.
6. **This is the same shape as an already-ratified precedent.** The
   operator-hosted-vs-self-hosted fork this topic proposes for NotebookLM
   identity is the exact fork already ratified for the openXdox dispatch
   credential — Case A operator-hosted (the operator owns and operates the
   credential/account, applied through intake) vs Case B self-hosted (the
   licensee's own channel operates it, no Opensoft identity performing the
   privileged act) — see
   [`docs/openxdox-dispatch-credential-binding.md`](../../../docs/openxdox-dispatch-credential-binding.md).
   This topic asks the family to recognize that fork as a general
   identity-hosting principle, not a credential-specific one-off.

## Why

<!-- xspec:candidate target=lifecycle-notebook-projection -->
The entire governed NotebookLM projection — every per-repo `xFactory
Ideation — <RepoName>` book, `xf-drafts`, `xf-canon`, and every live session
book — is created by `scripts/sync-notebooklm-books.py` under the `nlm`
CLI's default profile, which resolves to one person's personal consumer
Gmail (`brettheap@gmail.com`). This was proven live 2026-08-15: Brett,
browsing as his Workspace identity (`brett.heap@farheap.com`, managed by
tech-corps.com), hit "request access" on a dashboard "open notebook" link,
and the request sits unmanaged in the personal Gmail's inbox/share dialog.
`docs/lifecycle-notebook-projection.md` already names the underlying
disease in its own words — "the quota is one shared account" — but only as
a capacity-planning fact (section 5's capacity guard, section 9's
per-session quota note); it has never modeled WHICH account, or treated
that choice as something an install declares. This is the identical shape
of the personal PAT just retired from openXdox dispatch: the projection
dies with one person's account, misattributes every book's real owner,
gates access through one person's inbox instead of a policy, and
concentrates the platform's source-count quota on one individual rather
than the tenant that actually owns the corpus.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=lifecycle-notebook-projection -->
An xFactory install's intake gains a declared field: which Google identity
hosts that install's NotebookLM projection — a company xFactory service/user
account (the normal case) or a personal account (the legitimate
individual-installer case). `scripts/sync-notebooklm-books.py` runs under
whichever account is declared, selecting the matching `nlm` CLI profile
(the CLI is already profile-aware via `~/.notebooklm-mcp-cli/`, so per-install
profiles are additive, not new plumbing) rather than always the tool's
default profile. Once a company account is declared, the three lifecycle
books, their aliases, and every session notebook are created under it, and
other users reach them only through an explicit share-out FROM that
account — never by each independently authenticating against one person's
login.
<!-- /xspec:candidate -->

<!-- xspec:candidate target=credential-contracts -->
The choice of hosting identity is governed by the same two-case model
already ratified for the openXdox dispatch credential (Claim 6): Case A,
operator-hosted — the operating party owns a company Google/Workspace
account and runs the sync under it, sharing out to individual users from
there; Case B, self-hosted/personal — an individual installer keeps the
books under their own personal Gmail, with no company account implied and
no governance obligation attached. For Case A, company-policy Hermes (the
tenant layer) gains a governance job: monitor the hosting account's pending
share requests and approve the legitimate ones, turning the manual
"request access" dialog Brett hit into a recorded, governed policy act
rather than an unmanaged inbox item.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=lifecycle-notebook-projection -->
- Affected specs: `lifecycle-notebook-projection` (MODIFIED — a declared
  hosting-account field, `nlm` profile selection at sync time, and a
  share-out-from-the-account rule); `credential-contracts` (MODIFIED — the
  two-case account-custody rule, paralleling the dispatch-credential
  binding shape already ratified there in spirit via
  `docs/openxdox-dispatch-credential-binding.md`).
- Affected code: `scripts/sync-notebooklm-books.py` (profile/account
  selection), `docs/lifecycle-notebook-projection.md` (section 1's "one
  shared account" framing and section 6's operator runbook, both written
  assuming a single human's browser session), and whatever install/tenant
  intake flow ends up carrying the declared field (see Open question 1 —
  no such flow is named yet).
- **Honest gap:** neither `client-infrastructure-request` nor
  `client-infrastructure-liaison` was used as a target here, though both
  were checked. Both govern a **paying client's own tenant**
  infrastructure (Business Central, Entra, Exchange, and the like) under a
  liaison/execution-binding model — a different bounded context from an
  operator's own internal governance tooling account. Forcing this
  delta's target= onto either would misrepresent what they own; this
  topic uses `lifecycle-notebook-projection` and `credential-contracts`
  instead, both of which resolve and both of which are the real owners of
  the mechanism and the custody rule respectively.
- The company-policy-Hermes monitor/approve lane (Claim 5) has no clean
  existing mechanical home either — `workflow-gate-contract` and
  `roles-authority-model` were checked and neither models "approve a
  pending third-party share-access request" as a requirement shape today.
  Flagged honestly in Open question 4 rather than force-fit onto either.
- No client-tenant act, credential, or account is created or granted by
  staging this topic. No existing book, alias, or sync behavior changes
  until a company account actually exists and is declared somewhere.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

- Migrating the existing three books (plus every live session book) off
  `brettheap@gmail.com` should be cheap: NotebookLM has no ownership-transfer
  mechanism, but the books are explicitly **derived** artifacts — membership
  is "always derived from `Status:` headers — never hand-curated"
  (`docs/lifecycle-notebook-projection.md` section 1) — so re-creating them
  under the company account and re-running the sync is a re-derivation, not
  a migration in the data-loss sense. Aliases already re-register
  idempotently per run (per this repo's own CLAUDE.md orientation), so the
  alias layer needs no special handling either. — Added-by: Claude Opus 4.8
  (session, Brett's direction) · 2026-08-15
- A per-install hosting account also shards the platform's quota
  ceilings, not just governs identity. The 300-source-per-notebook cap
  that forced `split-ideation-book-per-repo` (2026-08-10) is a per-notebook
  limit, but the underlying Google-account-level quota (API calls, storage,
  concurrent notebooks) is presumably per-ACCOUNT — one shared personal
  account concentrates that ceiling across every install this workspace
  ever serves, while per-install company accounts would shard it the same
  way per-repo books already shard the per-notebook source cap. — Added-by:
  Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
- The `nlm` CLI is already profile-aware (credentials land under
  `~/.notebooklm-mcp-cli/`, shared with containers that mount the same
  home, per the section 6 runbook) — per-install profiles are therefore an
  existing mechanism this topic would select between, not new plumbing to
  build. — Added-by: Claude Opus 4.8 (session, Brett's direction) ·
  2026-08-15
- The company-policy-Hermes monitor/approve lane may be constrained by a
  real platform limitation: NotebookLM has no documented admin or
  share-management API today (`docs/lifecycle-notebook-projection.md`'s
  "Known Limitations" section describes only source-count limits, ~20-minute
  session expiry, and title-based matching — no share/access-request
  surface). The mechanism may have to be a periodic CLI check or a human
  relay rather than an event-driven approval flow, and that should be said
  honestly rather than assumed away. — Added-by: Claude Opus 4.8 (session,
  Brett's direction) · 2026-08-15

## Conflicts

- `docs/lifecycle-notebook-projection.md` documents and structurally
  depends on the one-shared-account model throughout: section 1's "the
  quota is one shared account, consumed by the three books, every live
  `xf-wb-*` reference set, and every live `xf-session-*`" framing, and
  section 6's operator runbook ("Authenticate (host shell with a browser;
  ~20 min session lifetime)... Credentials land in `~/.notebooklm-mcp-cli/`,
  shared with containers that mount the same home"), both written assuming
  exactly one human's interactive login. This topic contradicts that model
  by design — ratifying it requires amending those sections' account-identity
  assumptions, not adding a second model beside them. — Added-by: Claude
  Opus 4.8 (session, Brett's direction) · 2026-08-15
- The section 6 auth runbook's browser-login flow assumes a human sitting
  at a keyboard; a company SERVICE/user account changes that story (Google
  Workspace accounts commonly authenticate via domain-wide delegation, a
  dedicated admin's browser session performed on the account's behalf, or
  a service-account key — none of which is today's `nlm login` flow) and
  this topic does not resolve which mechanism a declared company account
  would actually use to authenticate the sync. — Added-by: Claude Opus 4.8
  (session, Brett's direction) · 2026-08-15
- The template mandates live `xspec:candidate` markers in every staged
  primary fragment's Why/What changes/Impact sections (per
  `staged-topic-outline-template`'s Claim 7), yet
  `docs/document-lifecycle.md`'s prose-tagging-markers material has
  historically described staged docs as needing no inline markers at all.
  This topic is (per direction) the template's first fresh conformer
  carrying LIVE markers rather than illustrative/fenced ones; verification
  against the actual `doc_health/families.py` `fam_tag_hygiene` checker
  found NO rejection — only `Status: record` documents are excluded from
  candidate blocks, and staged documents validate normally provided
  `target=` resolves to a real capability under `openspec/specs/`. No
  checker-vs-template conflict was actually found in practice, but the
  template-vs-prior-convention TENSION itself (mandating markers where the
  lifecycle doc's own prose once said none were needed) is recorded here
  for the template's own ratification to settle. — Added-by: Claude Opus
  4.8 (session, Brett's direction) · 2026-08-15

## Open questions

### Q1. Which capability owns the declared-hosting-location delta?

Context: `lifecycle-notebook-projection` already owns the sync mechanism
itself (books, aliases, the operator runbook) but has never modeled WHICH
account runs it as a declared fact. `client-infrastructure-request` and
`client-infrastructure-liaison` were checked as candidates and both govern
a PAYING CLIENT's own tenant infrastructure (Business Central, Entra,
Exchange) under a liaison/execution-binding model — a different bounded
context from an operator's own internal governance tooling account.
`credential-contracts` already owns the shape of the two-case
operator-hosted-vs-self-hosted binding the openXdox dispatch credential
uses, but that precedent is a runbook doc
(`docs/openxdox-dispatch-credential-binding.md`), not a spec requirement —
the two-case principle itself may not be formally owned by
`credential-contracts` today so much as documented beside it.
Recommended answer: `lifecycle-notebook-projection` carries the declared
hosting-account field and the share-out-from-the-account rule (Claim 2 and
4); `credential-contracts` carries the two-case account-custody rule
itself (Claim 6), extending the same principle it already houses in
runbook form for openXdox dispatch. Neither `client-infrastructure-request`
nor `client-infrastructure-liaison` is the right home — both are scoped to
a client's own tenant, not the operator's tooling identity — and no new
capability is proposed unless the eventual draft proves these two too
narrow.
Explanation: this keeps the account-identity mechanism where the
projection itself already lives, and keeps the custody PRINCIPLE where the
family's other two-case precedent already lives, rather than stretching a
client-tenant-scoped capability to cover an operator-internal concern it
was never written for. The honest risk is that `credential-contracts`'
five record kinds (requirements, grant template, binding template, broker
contract, audit policy) are all CREDENTIAL-shaped, and a Google-account
identity choice may not map cleanly onto any of the five without an
extension — that mapping is exactly what a future draft would need to
prove or disprove.
Disposition status: open
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15

### Q2. Company account type — Workspace user vs. consumer Gmail for the company case?

Context: "company xFactory user account (Google)" (Claim 4) does not by
itself specify whether that account must be a Google Workspace account in
the company's own verified domain, or could be an ordinary consumer Gmail
merely designated "the company one" by convention.
Recommended answer: a Google Workspace user account in the operating
party's own domain — not a consumer Gmail, even one informally designated
as the company account.
Explanation: a Workspace account brings admin-console policy (2FA
enforcement, session controls, offboarding when the operator changes),
org-owned retention and audit, and — critically — no personal-recovery
path back to one individual the way a consumer Gmail always retains one.
A consumer Gmail labeled "company" inherits every personal-account failure
mode this topic exists to retire (single recovery email/phone, no admin
console, no enforced org policy); it would be Case A's account type
wearing Case B's actual risk profile.
Disposition status: open
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15

### Q3. Does the share-out roster consume the in-flight `add-client-identity-roster` proposal?

Context: `add-client-identity-roster` (ratified 2026-08-14,
`openspec/changes/add-client-identity-roster/`) governs identities standing
in a PAYING CLIENT's tenant — app registrations and service principals on
a declared admission surface (Business Central, Exchange, and so on), keyed
on `(domain, surface, class, blast-radius unit, duty)`, with verified
provider-side admission as a first-class fact. The share-out roster this
topic needs is a different shape on its face: a list of HUMAN users an
internal Google account has shared specific notebooks with, not
provider-admitted service principals in a client's estate.
Recommended answer: lean toward NOT inventing a second, structurally
similar contract without first checking whether
`client-identity-roster`'s shape can carry it — but this is unproven, not
settled. That roster's uniqueness key and its verified-admission-act
machinery are built for provider-side app registrations, not a human-invite
list; if a real drafting pass shows the key genuinely cannot represent
"user X has view access to book Y, granted by whom, when," the honest
fallback is a distinct, small roster (keyed roughly on
`(account, user, book_or_alias, role, granted_at)`) rather than stretching
`client-identity-roster` to fit a case its admission-surface model was
never designed for.
Explanation: the family's own stated discipline (this same
`add-client-identity-roster` proposal, "no second roster competing for the
same ground") argues against inventing parallel machinery reflexively —
but that discipline applies to genuinely overlapping ground, and a
human-user Google Docs sharing list may simply not be the same ground as
client-tenant service-principal admission. This question should be settled
by attempting the mapping, not by assumption either way.
Disposition status: open
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15

### Q4. What does the company-policy-Hermes monitor/approve lane look like mechanically, given no NotebookLM share API?

Context: `docs/lifecycle-notebook-projection.md`'s own "Known Limitations"
section names source-count limits, ~20-minute session expiry, and
title-based matching — nothing resembling a programmatic share-request or
admin-management surface. The "request access" flow Brett hit today is an
ordinary Google Drive/Docs-style browser dialog landing in the account
owner's inbox, not an API event.
Recommended answer: start with a governed MANUAL lane — a request lands in
the account's inbox or pending-share list; a designated company-policy
actor reviews it and approves or denies it inside the Google account's own
UI; that act is then RECORDED (who approved, for what book, when) as an
audit entry the tenant layer owns. Automate the detection/relay step
(periodic `nlm`-CLI polling, or another mechanism) only if and when a real
API-shaped surface exists — do not design against a capability the
platform does not currently offer.
Explanation: this mirrors the `client-identity-roster` proposal's own
"report-only... no automated remediation" discipline for a case where the
acting party has no privileged API to automate against — a governed manual
act, evidenced and recorded, is strictly better than either an ungoverned
manual act (today's status quo) or a fictional automated one the platform
cannot actually support.
Disposition status: open
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15

### Q5. What is the migration sequencing for opensoft's current, personally-hosted books?

Context: today's three live lifecycle books plus every live session book
sit under `brettheap@gmail.com`. Idea note 1 establishes that re-creating
them under a company account is cheap (they are derived, not migrated,
data), but a live cutover still needs a moment where old and new
coexist without doubling sync targets, losing in-progress chat history, or
leaving both "live" indefinitely with no declared retirement.
Recommended answer: re-create the books under the company account the
next time `sync-notebooklm-books.py --apply` runs after that account
exists and is declared somewhere the sync can read; verify parity (source
counts, titles, registered aliases) against the personal-hosted originals;
then explicitly retire the personal-hosted books (not merely stop touching
them) once parity is confirmed.
Explanation: an explicit retirement step matters because this repo already
has one precedent for what happens when a book's lifecycle is left
implicit — the shared Ideation book silently hit its 300-source cap before
anyone declared it "old" and split it (the incident behind
`split-ideation-book-per-repo`). A declared retirement avoids repeating
that pattern for the personal-hosted books once the company-hosted ones
are proven equivalent.
Disposition status: open
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15

## Exit

Iterate this fragment in doxBench until all five open questions above
carry a disposition other than `open`. The likely landing is one or two
OpenSpec changes — a `lifecycle-notebook-projection` delta for the
declared-hosting-account mechanism and share-out rule, and a
`credential-contracts` delta for the two-case custody principle, either as
one combined change or sequenced separately depending on Q1's resolution —
raised only once a real company account exists to prove the declared-field
and re-creation path against.
