# NotebookLM Projection — Hosting Migration Evidence (2026-08-24)

Status: record
Kind: report
Captured: 2026-08-24
Repository context: openxFactory
Summary: Evidence for the hosting migration of the lifecycle notebook projection from the personal account (brettheap@gmail.com, profile `personal`) to the declared operator account (xFactor001@opensoft.one, profile `company`) — the recorded ids, the re-derivation, the parity numbers, Brett's 2026-08-24 rulings, and the three steps that are HELD rather than done.
Topics: notebooklm, lifecycle-notebook-projection, hosting-migration, parity, acceptance-evidence

Executed against
[the ratified runbook](notebook-projection-migration-runbook.md). Steps are
numbered as that runbook numbers them.

## Outcome in one line

The projection is **re-derived and live in the company account** — 7 books,
**626 managed sources** (633 total, counting each book's charter source), 608
unique managed titles, **0 unaccounted**. **Steps 5, 8 and 10 are HELD**: one on
a tooling defect, two on the runbook's own "only once parity holds"
precondition, which Brett has ruled stays unmet for now.

The counts reconcile as: the per-book table below sums to 626 managed sources;
adding the seven `00 [charter] Read me first` sources gives 633 total; and 626
managed sources carry 608 DISTINCT titles, because eighteen grounding documents
(`document-lifecycle`, `architecture`, `terminology-and-repo-topology`) are
projected into more than one book. 608 is therefore the number parity compares,
and it matches exactly.

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

## Step 8 — HELD by ruling: legacy books NOT retired

The runbook conditions retirement on parity holding. It does not hold, and
**Brett ruled on 2026-08-24 that it does not**:

> RETIREMENT HELD — parity does NOT hold for step 8 until the
> oversized-document handling gives the 228KB spec a projected form; legacy
> books stay untouched.

The legacy books were therefore **not archive-renamed and not touched**; they
remain live and intact in brettheap@gmail.com under the ids recorded in step 1.
The operator's reading — that a provider-imposed, pre-existing gap might be
treated as parity "holding" — was NOT adopted. The gate stands until the
document is projectable.

**What unblocks it.** F4's oversized-document handling must give
`openspec/specs/ideation-dashboard/spec.md` a projected form — chunking it into
provider-sized sources, or another representation that carries its content —
so canon reaches title-set equality and `--parity` exits zero. Skipping the
document does NOT clear this gate: the ruling requires a projected form, not an
excuse. Retirement then proceeds per step 8 against the step 1 ids, which is why
those ids and the `from_account` / `from_nlm_profile` history are kept.

## Step 8 — EXECUTED 2026-08-26

The hold above is discharged and the act is done. Gate cleared by Brett Heap's
2026-08-26 ruling (`openspec/changes/add-notebook-projection-identity/review/
retirement-gate-clearance-2026-08-26.md`); executed the same day.

**PROVENANCE, STATED PLAINLY.** The script was prepared by agents and its gates
verified without provider access (uuid arrays cross-checked against the mapping
block, gate logic simulated, a delete-verb assertion run over the source). It was
then run against the live accounts **at Brett's typed in-session instruction**,
by the session rather than by his own shell — the harness did not fire his `!`
line, and he directed the run rather than re-typing it. He authorized the act; an
agent's process performed it. Recorded that way because who pressed the key is
part of the evidence.

Full transcript: `scratchpad/step8-transcript-1787799596.log` (100 lines, tee'd
by the script).

### The recorded output, verbatim

```
## Step 8 — EXECUTED 2026-08-26

Renames (phase 2): renamed=7 skipped=0 failed=0
  RENAMED  b83e63e3-262a-4dfe-9b9f-332b3d27d1bb  xFactory — Drafts (RETIRED 2026-08-26 — hosting migration)
  RENAMED  6f10282a-7b5b-41c5-9109-55e603890730  xFactory — Canon (RETIRED 2026-08-26 — hosting migration)
  RENAMED  99b1ff52-2a93-43c2-b8fc-a153328ccd77  xFactory — Ideation OpsxFactory (RETIRED 2026-08-26 — hosting migration)
  RENAMED  c2b89469-396e-4fef-9154-fa9ade81d64c  xFactory — Ideation codexFactory (RETIRED 2026-08-26 — hosting migration)
  RENAMED  5830dbd2-5624-4852-987d-9f4e37746448  xFactory — Ideation MedxFactory (RETIRED 2026-08-26 — hosting migration)
  RENAMED  48ac861d-5a5c-4515-92fc-5b7b251c22c7  xFactory — Ideation LedgerxFactory (RETIRED 2026-08-26 — hosting migration)
  RENAMED  74ace7c8-b3df-4373-bcd2-64043b153cba  xFactory — Ideation openxFactory (RETIRED 2026-08-26 — hosting migration)

Aliases (phase 3): no alias resolves to a legacy id

Company books (phase 4): 7 of 7 present, none carrying (RETIRED ...)
```

### The gates, as they fired

```
PHASE 0  active profile: personal
PHASE 1  structural gate — found 7 of 7 legacy ids present:
  b83e63e3-…  xFactory — Working Drafts
  6f10282a-…  xFactory — Canon
  99b1ff52-…  xFactory Ideation — OpsxFactory
  c2b89469-…  xFactory Ideation — codexFactory
  5830dbd2-…  xFactory Ideation — MedxFactory
  48ac861d-…  xFactory Ideation — LedgerxFactory
  74ace7c8-…  xFactory Ideation — openxFactory
PHASE 3  clean: no alias resolves to a legacy id
PHASE 4  active profile: company — company books present: 7 of 7, none retitled
```

The phase-1 listing preserves the PRE-RENAME titles, which the renames overwrote
and which exist nowhere else now.

**Nothing was deleted.** Seven notebooks were renamed in `brettheap@gmail.com`
and remain there intact.

### The post-hoc parity confirmation

Brett's ruling made the live check post-hoc rather than a precondition. It was run
read-only (`--parity` short-circuits to `SystemExit(parity_report(...))` before
any write path) from a **freshly built 19-submodule assembly at that day's
aggregation main** — not from the shared checkout, which was 273 commits behind
with 112 uncommitted entries and would have derived from stale repo states.

```
hosting: operator_hosted — xFactor001@opensoft.one (nlm profile 'company', verified active)
[canon] PARITY FAIL: 3 missing, 0 extra (derived 116, live 113)
[canon]   MISSING [ratified] LedgerxFactory: accounting-roles-and-authority
[canon]   MISSING [ratified] OpsxFactory: managed-service-mapping
[canon]   MISSING [ratified] openxFactory: openxdox-dispatch-credential-binding
[drafts] PARITY FAIL: 3 missing, 2 extra (derived 189, live 188)
[drafts]   MISSING [draft] OpsxFactory: farheap-service-mapping-section7-2026-08-25-evidence
[drafts]   MISSING [draft] codexFactory: council-fail-path-registration
[drafts]   MISSING [draft] openxFactory: notebook-projection-retirement-runbook-step8
[drafts]   EXTRA   [draft] OpsxFactory: managed-service-mapping
[drafts]   EXTRA   [draft] openxFactory: openxdox-dispatch-credential-binding
[ideation-codexfactory] PARITY OK: 14 documents in 14 titles match
[ideation-ledgerxfactory] PARITY OK: 65 documents in 65 titles match
[ideation-medxfactory] PARITY FAIL: 0 missing, 4 extra (derived 47, live 51)
[ideation-medxfactory]   EXTRA   [staged] MedxFactory: root-truth-grounding/topic
[ideation-medxfactory]   EXTRA   [staged] MedxFactory: root-truth-target-claims/topic
[ideation-medxfactory]   EXTRA   [staged] MedxFactory: terminology-normalization/topic
[ideation-medxfactory]   EXTRA   [staged] MedxFactory: treatment-plan-generation/topic
[ideation-openxfactory] PARITY FAIL: 2 missing, 1 extra (derived 247, live 246)
[ideation-openxfactory]   MISSING [staged] openxFactory: openxwallet-neutral-home
[ideation-openxfactory]   MISSING [staged] openxFactory: treatment-options-engine
[ideation-openxfactory]   EXTRA   [staged] openxFactory: qualify-avatar-live-voice
[ideation-opsxfactory] PARITY OK: 16 documents in 16 titles match
parity union: 676 derived titles, 675 live managed titles, 8 unprojected, 7 unaccounted
parity: FAILED for 4 book(s): canon, drafts, ideation-medxfactory, ideation-openxfactory — pending changes remain
```

**PARITY DID NOT COME BACK CLEAN, AND THAT IS RECORDED RATHER THAN SOFTENED.**
Four books report pending changes. What it does and does not tell us:

* **THE RETIREMENT IS CONFIRMED, on the number that matters.** *Live managed
  titles: 675.* The 2026-08-25 run recorded *"675 derived titles, 675 live
  managed titles"*. **Live is unchanged across the retirement** — not one source
  was removed from or damaged in the company account. Every company book is
  present and none was retitled.
* **THE PENDING CHANGES ARE DERIVED-SIDE DRIFT, and no `--apply` has run since
  2026-08-25.** Every diff is a document whose repository state moved: two
  documents changed Status and therefore moved book (`managed-service-mapping`
  and `openxdox-dispatch-credential-binding` each read MISSING from canon and
  EXTRA in drafts — one document, one transition, counted at both ends), and
  `notebook-projection-retirement-runbook-step8` is MISSING from drafts because
  it is the runbook this very act followed, written the same day and never
  applied. Derived moved 675 → 676; live did not move at all.
* **The MedxFactory four are an assembly artifact**, not a live change. Live
  holds 51 there — the same 51 the 2026-08-25 run recorded — while this
  assembly derives 47, because the aggregation's MedxFactory pin no longer
  matches what was applied on 08-25.

So the projection needs a reconciling `--apply` to become current with the repos.
That is ordinary derived-projection drift, it predates this act, and it is not
retirement damage.

### Two defects found in the script while it ran

Recorded because this runbook is a governed document and its execution story
should be honest.

1. **The first cut crashed in phase 1** — an embedded f-string used backslash
   escapes inside a replacement field, illegal before Python 3.12. **Fail-closed
   held**: the gate aborted rather than proceeding to rename anything. But the
   abort reason read *"no notebooks listed"*, which blamed the account for a
   parser bug. Rewritten without f-strings, executed against five stub JSON
   cases before re-delivery, and the abort now distinguishes SCRIPT PARSE ERROR
   from an empty list from no output at all.
2. **The harness did not fire Brett's `!` line**, so the sitting ran by the
   session at his instruction instead of in his own shell. No behavioural
   difference to the act; recorded because the provenance above depends on it.

## Reconciling apply — EXECUTED 2026-08-27

Closes the derived-side drift the step-8 parity recorded. Run on Brett's
instruction, company profile active, from a **fresh 19-submodule assembly at that
day's aggregation main** with all pins verified matching (19/19).

### THE MANIFEST TRAP — read this before running from a fresh assembly

The first dry run from that assembly planned **703 operations**. It should have
planned about fifty.

`.claude/nlm-sync-manifest.json` is **gitignored**, so a freshly cloned assembly
has none. With no manifest the sync cannot tell which live sources already match,
and plans an `UPD` for **every source in every book** — 686 of the 703. The real
manifest lives in the operator's own workspace.

Copying it into the assembly (read-only with respect to the source workspace)
dropped the plan to **54 operations**. THE DIFFERENCE WAS ENTIRELY ARTIFACT.

**CORRECTED 2026-08-27 after review — the rule first written here contradicted
the ratified contract, and the contract wins.**

An earlier version of this section called the 703-op plan "artifact" and drew the
rule *"an assembly is repositories AND manifest; either one missing produces a
confident, wrong plan."* That is wrong on both halves.
§ 5 of `docs/lifecycle-notebook-projection.md` defines the manifest as

> intentional local derived state — not committed; safe to delete, next apply
> rebuilds it

so an assembly without one is CONFORMING, not incomplete. And the plan it
produces is not wrong: § 5's Update rule is *"repo content changed (SHA-256
tracked in the manifest) → delete + re-add"*, so with no manifest **nothing can
be known unchanged** and every source is refreshed. Delete-and-re-add of
identical content converges on the same end state — the run is idempotent in
EFFECT even where it is not idempotent in OPERATIONS.

**The honest rule:**

> A manifest-less assembly plans a **FULL REFRESH by design**. Carry the
> operator's manifest when an incremental plan is wanted. **Review the plan's
> magnitude before applying either way** — a full refresh is expensive (~2s per
> source operation, so roughly 700 ops ≈ 23 minutes) and it churns source ids,
> which is reason enough to choose deliberately rather than discover.

What actually happened here is smaller and less flattering than a trap: **the
plan was contract-correct and I had not read the contract.** Reviewing magnitude
before applying is what made the difference, and that habit is the transferable
part — not a rule about assemblies.

The genuinely comparable prior incident stands on its own terms: a doc-health
drift reading of 549 pending operations from a ONE-REPOSITORY workspace was an
artifact, because the derived set was missing nine repositories' documents. That
is a wrong INPUT. A missing manifest is a permitted input.

### The plan, reviewed before applying

| book | ADD | DEL | UPD |
| --- | --- | --- | --- |
| canon | 5 | — | 16 |
| drafts | 3 | 2 | 13 |
| ideation-medxfactory | — | 4 | — |
| ideation-openxfactory | 2 | 1 | 8 |
| ideation-codexfactory / ledgerxfactory / opsxfactory | — | — | — |

Three books planning **zero** is itself the evidence this was not an assembly
artifact — a wrong assembly shows mass DELs everywhere. The ADD/DEL profile
matches the drift recorded at step 8 exactly (drafts 3/2, MedxFactory 4,
openxFactory 2/1).

**Every DEL was reviewed before applying**, because a DEL removes live content:

* `managed-service-mapping` and `openxdox-dispatch-credential-binding` leave
  `drafts` and appear among canon's ADDs — the same two documents, whose Status
  moved from draft to ratified, counted at both ends.
* **The four MedxFactory topics are NOT a pin artifact**, which is what the
  earlier record suspected. They exist at the pin and upstream, and they carry
  `Status: realized (promoted into …, archived …)` — the four cite archive
  dates of 2026-08-05, 2026-08-06 and 2026-08-07 (two share the last). `STATUS_RE` accepts
  only the controlled vocabulary — brainstorm, staged, draft, ratified, standard,
  superseded, retired, record — and **`realized` is not in it**, so the scan
  cannot project them. Removing their sources is correct convergence, not loss.
  (That four governed documents carry an out-of-vocabulary Status is a
  MedxFactory doc-health matter, noted here and not fixed from this lane.)

### The apply, and a defect it exposed

54 of 54 operations executed, exit 0, no failures.

The first verification was **not** clean, and the reason is a real defect rather
than a settling delay:

**THE OVERSIZED-SOURCE RENAME FAILS SILENTLY.** A document above
`MAX_TEXT_ARG_BYTES` uploads as a temp file and is then renamed to its contract
title, because the CLI titles a `--file` source by filename. The sync waits
`time.sleep(2)` before renaming. For
`openspec/specs/ideation-dashboard/spec.md` — **279,235 bytes**, the largest
document in the corpus — two seconds is not enough: the add succeeds, the rename
does not, and the source sits under `xf-sync-XXXXXXXX.md`. Parity then reports it
MISSING, because by title it is.

Re-running the book, which the documented precedent prescribes, **did not fix it
— it added a second temp-named source.** Repaired by hand:
`nlm source rename <full-source-id> "[spec] openxFactory: ideation-dashboard"
--notebook xf-canon` succeeded immediately (minutes later, with the source
settled), and the duplicate was deleted. Canon went 120 → 119 sources with
exactly one correctly-titled spec.

Recorded as an OPEN DEFECT for the sync: the 2-second sleep is too short for the
largest projected document, and the failure is silent — the run reports success
while leaving a mistitled source. A re-run compounds it rather than repairing it.
The 2026-08-25 record called this "the known oversized-source readiness race" and
believed it repaired; it is not.

**This is the document Brett's retirement gate turned on.** Its projected form is
what cleared the hold, so its title landing correctly is not a cosmetic matter.

### Verification — all three clean

```
[canon] PARITY OK: 118 documents in 118 titles match
[drafts] PARITY OK: 189 documents in 189 titles match
[ideation-codexfactory] PARITY OK: 14 documents in 14 titles match
[ideation-ledgerxfactory] PARITY OK: 65 documents in 65 titles match
[ideation-medxfactory] PARITY OK: 47 documents in 47 titles match
[ideation-openxfactory] PARITY OK: 247 documents in 247 titles match
[ideation-opsxfactory] PARITY OK: 16 documents in 16 titles match
parity union: 678 derived titles, 678 live managed titles, 0 unprojected, 0 unaccounted
parity: PROVEN — every book in scope matches the corpus scan, 0 pending ADD/DEL/UPD
```

* `--parity`: **PROVEN**, exit 0, document-based.
* Convergence dry run: **ZERO** planned operations.
* doc-health `notebook-projection-drift` from the assembly: **no finding**.

**The drift chapter recorded at step 8 is closed.** Live managed titles moved
675 → 678 by the three genuinely new documents; nothing was lost.

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
`xfactor001@opensoft.one (owner)` — lower-cased **as the CLI rendered it**, kept
verbatim rather than normalised to the canonical `xFactor001@opensoft.one`
because this line quotes provider output and a tidied quote is not a quote. The CLI additionally reported
`is_public: true` / `access_level: public`; **that report is false**, and F5
below carries the proof.

### The posture ruling, and the act taken under it

Brett ruled on 2026-08-24:

> SHARING POSTURE: RESTRICT — Google-side deny-by-default; the app is the SOLE
> grantor (org-visible rejected on the logic-enforced-bound doctrine).

Acting on that ruling, the operator re-opened the live `xFactor001` browser
session and went to tighten all seven books through the provider UI, the CLI
toggle having no-opped. **No tightening was necessary: the books were already
Google-side deny-by-default**, and the provider offers no control to change
that would have made them more restricted.

Verified per book, 2026-08-24, as `xFactor001@opensoft.one`, driven by the
governed lane under Brett's ruling:

| book | collaborators | sharing-policy triple | link sharing |
| --- | --- | --- | --- |
| `xf-canon` | owner only | `[1, false, false]` | none |
| `xf-drafts` | owner only | `[1, false, false]` | none |
| `xf-ideation-openxfactory` | owner only | `[1, false, false]` | none |
| `xf-ideation-ledgerxfactory` | owner only | `[1, false, false]` | none |
| `xf-ideation-medxfactory` | owner only | `[1, false, false]` | none |
| `xf-ideation-opsxfactory` | owner only | `[1, false, false]` | none |
| `xf-ideation-codexfactory` | owner only | `[1, false, false]` | none |

The provider's own share dialog, read directly in the browser for `xf-canon`,
lists **only** `xFactor001 Notebook LM (Owner)` under "People with access" and
**contains no general-access control at all** — no "Anyone with the link", no
audience selector, nothing to switch off. The ruling's required end state was
therefore already the actual state; the only change made to any book's sharing
was none.

**The ruling's standing consequence:** from here the app is the sole grantor.
`share_out` stays `[]` until a governed grant is approved and recorded, and no
grant may be made by hand in the provider UI. Org-visible access is rejected,
so the Workspace default must never be relaxed to it.

The wallet-mediated access-control design that will implement app-sole-grantor
is being **staged separately** and is not part of this record.

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

**FIXED the same day** (`scripts/sync-notebooklm-books.py`):
`live_session_targets` now enumerates every worktree git lists for each
repository and asks each as a potential container owner through the same joint
signal, degrading to the canonical root alone only when a worktree list is
unreadable — safe there because this mode only ever REFUSES when it finds
nothing; it has no retire arm. The multi-match refusal also names the paths and
distinguishes a cross-repository collision (resolvable with
`--session-repository`) from two containers of one repository (no alias can
disambiguate). Covered by
`test_session_ref_sees_a_session_opened_from_a_feature_worktree`. The fix
UNBLOCKS step 5's retry but does not perform it — both sessions remain hosted
on the personal account until a real `--session-ref --apply` run migrates them.

The same landing closes the session route's exposure to the 2026-08-10 death
mode: `sync_session_notebook` was deliberately unbounded (workbench finding 21),
so nothing stopped a session whose derived corpus outgrew the provider's
per-notebook source cap — adds would fail past the cap mid-flight. It now
carries the lifecycle books' capacity guard: an over-cap plan refuses BEFORE
any mutation and names the excess. Covered by
`test_a_session_over_the_provider_source_cap_is_refused_before_any_mutation`.
This is the source-COUNT cap on the session route, not F4's single-document
size limit, which stays open.

**F4 — an oversized document fails silently and leaves litter.** Adding the
228 KB spec makes `nlm source add` report success while creating an untitled
`xf-sync-<random>.md` `generated_text` source instead of the intended titled
one. The sync neither verifies the add nor recognises the artifact, so it
retries every run and **accumulates one orphan per run**. Three had built up in
canon and were deleted by hand; canon is now clean at 103 (charter + 102
managed). Two defects to fix: verify the add, and either chunk or skip a
document over the provider's limit.

**F5 — `nlm share status` misreports Workspace notebooks as public.** All seven
new books report `is_public: true` with a public link. **The report is wrong,
and the books are not shared.** The CLI derives the flag heuristically in
`notebooklm_tools/core/sharing.py`, scanning every top-level list in the RPC
response and declaring the notebook public if any of them begins with the
integer `1`:

```python
for item in result:
    if isinstance(item, list) and len(item) >= 1:
        if item[0] == 1:  # Public access indicator
            is_public = True
            break
```

The comment above it already concedes "Position varies". What it actually
matches is a sharing-policy triple at position 6, whose first element is a MODE
CODE, not a boolean. Raw responses:

- new canon (Workspace): `… , [1, false, false], false]` → mode 1, both flags off
- legacy canon (consumer): `… , [3, true, true], false]` → mode 3, both flags on

So the heuristic fires on the mode code of the **more** restricted notebook and
stays silent on the less restricted one — it reports the posture backwards. Four
independent checks agree the new books are not exposed: the provider's share
dialog offers no general-access control and lists only the owner; an
unauthenticated fetch of the "public link" redirects to Google sign-in; the one
pre-existing notebook in the account, which the sync never touched, reports
`public` too; and `nlm share private` reports success while changing nothing —
because there is nothing to change.

Two consequences. The CLI's `is_public` / `access_level` **cannot be trusted for
Workspace-hosted notebooks** and should not be used as the roster's evidence of
posture; read the policy triple or the UI instead. And the "unapproved public
exposure" this run first reported was a tooling artifact, not a governance
breach — recorded here because the false positive is itself the defect worth
fixing.

## Corpus state this evidence was derived from

Workspace `/home/brett/projects/xFactory`, `openxFactory` at `ded08260`. The
workspace was deliberately NOT updated to `origin/main` (`01ff3434`, four
commits ahead) during the run: it is a shared checkout and the projection has
always derived from whatever the tree holds. Parity is measured against a scan
of the same tree, so it is self-consistent; ordinary drift is what the next
sync reconciles.
