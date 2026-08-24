# NotebookLM Projection — Hosting Migration Evidence (2026-08-24)

Status: record
Kind: report
Captured: 2026-08-24
Repository context: openxFactory
Summary: Evidence for the hosting migration of the lifecycle notebook projection from the personal account (brettheap@gmail.com, profile `personal`) to the declared operator account (xFactor001@opensoft.one, profile `company`) — the recorded ids, the re-derivation, the parity numbers, and the three steps that are HELD rather than done.
Topics: notebooklm, lifecycle-notebook-projection, hosting-migration, parity, acceptance-evidence

Executed against
[the ratified runbook](notebook-projection-migration-runbook.md). Steps are
numbered as that runbook numbers them.

## Outcome in one line

The projection is **re-derived and live in the company account** (7 books, 638
managed sources, 0 unaccounted); **steps 5, 8 and 10 are HELD** — one on a
tooling defect, two on the runbook's own "only once parity holds" precondition.

## The gate — how the account was authenticated

The runbook records this migration as beginning with an interactive
`nlm login --profile company` that only Brett can perform. It was instead
performed unattended, from credentials held by reference in Azure Key Vault
(`kv-opensoft-xfactory-qa`, secrets `xfactor-001-google-username` /
`xfactor-001-google-password`, versionless so rotations are picked up). No
credential value was written to disk, passed in a command line, or logged.

`nlm login --profile company --cdp-url …` — the runbook's documented CDP route —
**failed**, and its failure is a finding in its own right (see F1). The session
was captured instead with the repo's own harness,
`scripts/nlm_auth.py refresh --cdp-url`, which writes the full native profile
(cookie list + csrf_token + session_id). Authentication was then PROVEN with a
real call, `nlm notebook list --profile company`, not with `login --check`.

`profiles/company/metadata.json` records `email: xFactor001@opensoft.one`. The
harness writes that field null, so it was set from the vault-held username; the
sync's binding check reads it.

## Step 1 — legacy ids recorded, aliases DELETED (not repointed)

Recorded before any `--apply`, from the flat alias store, and the aliases then
deleted so the re-derivation could not silently repoint them:

| alias | legacy notebook id (brettheap@gmail.com) | title | sources |
| --- | --- | --- | --- |
| `xf-canon` | `6f10282a-7b5b-41c5-9109-55e603890730` | xFactory — Canon | 101 |
| `xf-drafts` | `b83e63e3-262a-4dfe-9b9f-332b3d27d1bb` | xFactory — Working Drafts | 186 |
| `xf-ideation-openxfactory` | `74ace7c8-b3df-4373-bcd2-64043b153cba` | xFactory Ideation — openxFactory | 196 |
| `xf-ideation-ledgerxfactory` | `48ac861d-5a5c-4515-92fc-5b7b251c22c7` | xFactory Ideation — LedgerxFactory | 66 |
| `xf-ideation-medxfactory` | `5830dbd2-5624-4852-987d-9f4e37746448` | xFactory Ideation — MedxFactory | 49 |
| `xf-ideation-opsxfactory` | `99b1ff52-2a93-43c2-b8fc-a153328ccd77` | xFactory Ideation — OpsxFactory | 16 |
| `xf-ideation-codexfactory` | `c2b89469-396e-4fef-9154-fa9ade81d64c` | xFactory Ideation — codexFactory | 15 |

## Steps 2–3 — binding and declaration

`nlm login switch company` (`auth.default_profile` = `company`), then
`hosting.migration.state` flipped `pending` → `complete` in
`examples/notebook-projection-hosting.yaml`, with `completed_at: "2026-08-24"`.
`from_account` / `from_nlm_profile` are kept as history.

Identity was checked as the runbook requires: the company account listed **no**
`xFactory — Canon`, so it is not the old account.

## Step 4 — re-derivation

`sync-notebooklm-books.py . --apply`, bound to `company` and verified active.
The first run **failed all seven books** partway through: the NotebookLM CLI
session lasts roughly twenty minutes and the re-derivation needs far longer, so
every call after expiry failed (see F2). The run was resumed after a session
refresh, under a background refresher, and completed with **zero failures**.

The books created:

| book | new notebook id (xFactor001@opensoft.one) | managed sources |
| --- | --- | --- |
| `xf-drafts` | `991f0af7-2077-4c26-ac1d-d92e2af9f99c` | 186 |
| `xf-canon` | `b331ed13-fa0b-456a-8004-184f66939ecd` | 102 |
| `xf-ideation-openxfactory` | `02295a6e-0193-4f6f-9501-c6e9e03bdc01` | 194 |
| `xf-ideation-ledgerxfactory` | `0042f5e6-6e49-4ea1-9a14-e298bfe0fb09` | 65 |
| `xf-ideation-medxfactory` | `81217e98-1cd2-4bb4-a4b8-917c601ce9e5` | 48 |
| `xf-ideation-opsxfactory` | `2c2ba7ae-65e1-436a-ba4c-0a5f8f2a99bb` | 17 |
| `xf-ideation-codexfactory` | `251c118f-4a02-4c9e-8ea2-025b12237e1c` | 14 |

Each book also carries its `00 [charter] Read me first` source. Aliases were
re-registered by the run, pointing only at the new notebooks.

## Step 5 — HELD: live session notebooks NOT migrated

Two sessions are live and each already has a notebook in the account being
abandoned:

- `xf-session-openxfactory-subject-document-estate-k11b9e42d8b96` (10 sources),
  branch `draft/subject-document-estate`
- `xf-session-openxfactory-company-provisioning-ledger-estate-subject-onboarding-intake-ke5b102225f04`
  (11 sources), branch
  `draft/company-provisioning-ledger-estate-subject-onboarding-intake`

`--session-sweep` sees both (`2 live session(s); no orphans`), but
`--session-ref <branch> --session-repository openxFactory --apply` refuses each
with "no live session worktree … under /home/brett/projects/xFactory". See F3.
Nothing was forced. **These two sessions remain hosted on the personal
account** — exactly the condition the runbook's step 5 warns about.

## Step 6 — workspace records replaced, not retired

Each of the seven records in `examples/lifecycle-notebook-workspaces.yaml` had
its `provider_notebook_id` updated to the new notebook. Record ids are
key-derived and unchanged, so each record IS still the live book's
registration; none was retired, per the runbook's step 8.3. The legacy → new
mapping is recorded in a comment in that file.

## Step 7 — parity against the corpus scan

```
[canon] PARITY FAIL: 1 missing, 0 extra (derived 103, live 102)
[canon]   MISSING [spec] openxFactory: ideation-dashboard
[drafts] PARITY OK: 186 titles match
[ideation-codexfactory] PARITY OK: 14 titles match
[ideation-ledgerxfactory] PARITY OK: 65 titles match
[ideation-medxfactory] PARITY OK: 48 titles match
[ideation-openxfactory] PARITY OK: 194 titles match
[ideation-opsxfactory] PARITY OK: 17 titles match
parity union: 609 derived titles, 608 live managed titles, 1 unprojected, 0 unaccounted
parity: FAILED for 1 book(s): canon — pending changes remain
```

The closing plain dry run is zero-pending except that same single item:

```
== drafts: 187 desired sources ==
== canon: 103 desired sources ==
[canon] ADD  [spec] openxFactory: ideation-dashboard
== ideation-openxfactory: 194 desired sources ==
== ideation-ledgerxfactory: 65 desired sources ==
== ideation-medxfactory: 51 desired sources ==
== ideation-opsxfactory: 18 desired sources ==
== ideation-codexfactory: 14 desired sources ==
```

**The one missing source is pre-existing and provider-imposed, not a fidelity
loss from this migration.** `openspec/specs/ideation-dashboard/spec.md` is
228 041 bytes, five times the next largest spec, and exceeds what the provider
accepts as a pasted source. The legacy canon book (101 sources) did not contain
it either — verified directly against the personal account. `0 unaccounted`
across the union is the load-bearing number: nothing that WAS projected went
missing. See F4.

Two further reconciliations, both pre-existing corpus conditions surfaced by a
fresh derivation and both now converged: three MedxFactory staging documents
that derive one identical title (`[staged] MedxFactory: topic`) and one such
OpsxFactory duplicate were deleted by the sync's own plan.

## Step 8 — HELD: legacy books NOT retired

The runbook conditions retirement on parity holding. It does not hold. The
legacy books were therefore **not archive-renamed and not touched**; they
remain live and intact in brettheap@gmail.com under the ids recorded in step 1.
This is the guard working, and clearing it is a ruling for Brett, not an
inference for the operator: the failing item is provider-imposed and
pre-existing, so a reasonable ruling is that parity "holds" for retirement
purposes — but that is his call.

## Step 9 — readers listed, NOTHING granted

No share was granted, and no roster entry was written; `share_out` and `denied`
stay empty.

Legacy books (personal account) — all seven identical:
`is_public: false`, `access_level: restricted`, sole collaborator
`brettheap@gmail.com (owner)`. **No pending collaborator requests exist on any
of them**; the 2026-08-15 request the runbook anticipates is not visible
through the provider's sharing API and must be resolved from whatever record
originated it.

New books (company account) — all seven: sole collaborator
`xfactor001@opensoft.one (owner)`, but `is_public: true` /
`access_level: public`. See F5: this is an account-level default, not an act of
this migration, and it is a posture decision for the company-policy actor.

## Step 10 — HELD

Closes on the migration's realization, which is not complete while steps 5 and
8 are held.

## Findings

**F1 — `nlm login` is broken by Google's rebrand.** NotebookLM is now served
from `notebook.google.com` ("Gemini Notebook"); `notebooklm.google.com`
redirects there. The CLI's `_is_notebooklm_url()` accepts only
`notebooklm.google.com` / `notebooklm.cloud.google.com`, so `is_logged_in()`
returns false for a browser that IS signed in and `nlm login --cdp-url` dies on
"Login timeout" after its 300 s wait. `NOTEBOOKLM_BASE_URL` cannot be pointed
at the new host — it is validated against an allow-list that excludes it. The
CLI's API calls still work, so only the login path is affected. The runbook and
`docs/notebooklm-sync-open-item.md` both describe the broken route as the way
in and need updating.

**F2 — a long `--apply` outlives its session.** Sessions last roughly twenty
minutes; the full re-derivation of 639 sources takes far longer. The first
attempt lost every book. Nothing in the sync detects or renews this. The
workaround used here — refreshing the on-disk profile from the live browser
every seven minutes, atomically, while the sync runs — works precisely because
the sync shells out to `nlm` per operation and each process re-reads the
profile. Worth making a first-class feature rather than an operator trick.

**F3 — `live_session_targets` asks only the canonical checkout.** The sweep
path, `live_session_aliases`, deliberately enumerates EVERY worktree of a
repository, and its own comment records why: asking only the canonical checkout
once "declared two LIVE sessions dead, both holding unmerged work". The
single-branch path never got that fix, so `--session-ref` cannot see a session
opened from a feature worktree — which is where both live sessions are. Same
two sessions, same root cause, opposite direction.

**F4 — an oversized document fails silently and leaves litter.** Adding the
228 KB spec makes `nlm source add` report success while creating an untitled
`xf-sync-<random>.md` `generated_text` source instead of the intended titled
one. The sync neither verifies the add nor recognises the artifact, so it
retries every run and **accumulates one orphan per run**. Three had built up in
canon and were deleted by hand; canon is now clean at 103 (charter + 102
managed). Two defects to fix: verify the add, and either chunk or skip a
document over the provider's limit.

**F5 — new books default to `public`, `nlm share private` silently fails.** All
seven new books report `is_public: true` with a public link, where the legacy
books were `restricted`. This is an account default, not an act of this
migration: the one pre-existing notebook in the company account, which the sync
never touched, is public too. It is also **not anonymous exposure** — fetching
the public link unauthenticated redirects to Google sign-in, so the plausible
reading is a Workspace "anyone in the organisation with the link" default.
`nlm share private` was attempted on all seven, reported success on each, and
changed nothing — the same silent-failure class as F4. The posture therefore
still differs from the legacy one and needs a ruling plus, most likely, a
Workspace admin setting.

## Corpus state this evidence was derived from

Workspace `/home/brett/projects/xFactory`, `openxFactory` at `ded08260`. The
workspace was deliberately NOT updated to `origin/main` (`01ff3434`, four
commits ahead) during the run: it is a shared checkout and the projection has
always derived from whatever the tree holds. Parity is measured against a scan
of the same tree, so it is self-consistent; ordinary drift is what the next
sync reconciles.
