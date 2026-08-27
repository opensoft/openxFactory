# Retirement Gate Clearance: add-notebook-projection-identity, step 8

Status: record
Kind: decision record
Decision date: 2026-08-26
Ruler: Brett Heap (repository owner) — in-session
Ruled: 2026-08-26 by Brett Heap (repository owner) — the retirement gate is
CLEARED ON REPO EVIDENCE; the live provider check becomes post-hoc confirmation
rather than a precondition
Applies to: runbook step 8 (`docs/notebook-projection-migration-runbook.md`),
tasks 4.6 and — through it — 4.7, 5.1, 6.1, 6.2
Supersedes: the 2026-08-24 hold recorded in
`docs/notebook-projection-migration-evidence-2026-08-24.md` § "Step 8 — HELD by
ruling"

## 1. The hold, in its own words

Brett ruled on 2026-08-24:

> RETIREMENT HELD — parity does NOT hold for step 8 until the oversized-document
> handling gives the 228KB spec a projected form; legacy books stay untouched.

(The quotation stands verbatim. For a reader checking the figure: that document,
`openspec/specs/ideation-dashboard/spec.md`, measures **270,834 bytes** today —
it has grown since the ruling. Nothing turns on the number; the note is here so a
checker finding 264 KiB does not think the wrong file is meant.)

The evidence record stated the unblock condition precisely, and its last sentence
is the one that governs this clearance:

> F4's oversized-document handling must give
> `openspec/specs/ideation-dashboard/spec.md` a projected form — chunking it into
> provider-sized sources, or another representation that carries its content — so
> canon reaches title-set equality and `--parity` exits zero. **Skipping the
> document does NOT clear this gate: the ruling requires a projected form, not an
> excuse.**

So the question this record answers is narrow and factual: **does that document
now have a projected form?** Not "is the gap tolerable", which the ruling already
refused.

## 2. The evidence chain

Four independent facts, each verifiable from the repository without provider
access. They were assembled by a read-only scout on 2026-08-26 and are recorded
here in the order they were checked.

### 2.1 The F4 handling exists in code

`scripts/sync-notebooklm-books.py` carries `MAX_TEXT_ARG_BYTES = 100_000` and an
oversized path in `add_text_source()`: content above that ceiling is written to a
temp file, added with `--file`, and then **renamed to its contract title** (the
CLI titles a `--file` source by filename and ignores `--title`).

The constant's own comment names this exact document as the case that forced it:

> A single argv string on Linux caps at MAX_ARG_STRLEN (131072 bytes), so a
> governance doc that large cannot ride `--text` — proven live 2026-08-10 by the
> promoted ideation-dashboard spec (Errno 7 killed the canon book).

This is the "another representation that carries its content" the ruling
permitted: the whole document, uploaded by a route that does not run into the
argv ceiling. It is not chunking and it is not skipping.

### 2.2 The manifest records the document as a live canon source

`.claude/nlm-sync-manifest.json` in the workspace root — written by the
2026-08-25 apply, mtime 10:46 — carries a row under `canon` keyed
`openxFactory/openspec/specs/ideation-dashboard/spec.md`, with a content hash and
a `[spec] …` title.

A manifest row is the sync's own record that the source exists in that book. It
is not proof of the provider's state, which is why it is one fact of four rather
than the answer on its own.

### 2.3 Canon reached title-set equality

The 2026-08-24 evidence recorded canon failing exactly this way:

```
[canon] PARITY FAIL: 1 missing, 0 extra (derived 103, live 102)
```

The 2026-08-25 run reports canon at **113 documents in 113 titles**, and the
union at **675 derived / 675 live managed, 0 unprojected, 0 unaccounted** —
`parity: PROVEN`, exit 0. Canon's live count rose from 102 to 113 and its parity
failure is gone. The single missing document was the condition of the hold.

### 2.4 A convergence dry run plans zero operations

`notebook-projection-drift` over the applied state plans **zero** ADD/DEL/UPD.
A missing source would plan an ADD.

### 2.5 A WARNING FOR WHOEVER CHECKS THIS NEXT — the drift number needs a full assembly

Verifying § 2.4 from an isolated clone produces an alarming and meaningless
number, and the mechanism is worth recording so the next reader does not have to
rediscover it — or worse, believe it.

A doc-health run taken from a scratch workspace containing **only `openxFactory`**
reported `notebook-projection-drift: 549 pending operations`. There is no drift.
The reasoning, corrected at review after a first, imprecise reading:

* The family does not simply skip on a small workspace. `_real_notebook_dryrun`
  returns `None` — and the family emits `Skip` — only when `agg_root is None` or
  the sync script is not found under it. A scratch parent holding one repository
  still resolves both, so the dry run **ran**.
* What ran was therefore an **AGGREGATION run over a PARTIAL assembly**. The sync
  derived the projected set from the one repository present (~246 documents, the
  openxFactory book's own count) and compared it against **675 live managed
  sources** spanning ten repositories.
* Everything the missing nine repositories contribute is live-but-underived, so
  the plan fills with **DELs**. The count is a measure of how much of the
  workspace was absent, not of how far the projection has drifted.

**So: the authoritative drift number comes only from a complete workspace
assembly** — the nightly, or an operator's own full checkout. A number obtained
any other way should be discarded rather than reported, and a run whose
`agg_root` is genuinely absent will say `Skip` rather than mislead.

## 3. THE INSTRUMENT THAT MEASURED 2026-08-24 WAS BLIND — said plainly

This record would be dishonest if it presented § 2.3 as simply "parity improved".
The parity mode that produced the 2026-08-24 numbers **could not have detected
this class of gap at all**, and that was established after the hold, by a
different change.

`add-projection-title-uniqueness` (archived 2026-08-25, PR #353, merged commits
`79bec8a7` and `839e0d8e`) found that a source title is the projection's identity
key, that `parity_report()` compared a set of derived TITLES against a set of live
TITLES, and therefore:

> Parity reports OK on a book that is missing documents.

Its measured consequence, in its own design § 2: **three collisions, eight
documents, five displaced** — and the books were, in that change's own words,

> Five sources short, in exactly the three books the census names.

(An earlier draft of this record set a paraphrase of that finding in quotation
marks. The sentence above is the supported verbatim, from that change's
`proposal.md`; the paraphrase said the same thing and was not a quotation.)

One of those books is named in its own table: `ideation-medxfactory`, four
documents collapsed to three titles. The 2026-08-24 evidence in this repository
records `[ideation-medxfactory] PARITY OK: 48 titles match`.

**So the 608/608 figure in the migration evidence was not a lie and was not
sound.** It was a true statement about titles produced by an instrument that could
not see documents. The 2026-08-25 run is a different measurement: it proves
membership over DOCUMENTS, which is why each line reads *N documents in N titles*
and why the equality of those two numbers is the injectivity made visible.

This matters for the gate in both directions, and both are recorded:

* It **weakens** the 2026-08-24 evidence, including its 608/608 parity claim.
* It **strengthens** this clearance, because the run being relied on here is the
  one taken under the amended rule, after the defect was fixed — which is exactly
  the ordering `add-projection-title-uniqueness` task 4.4 insisted on: *"A parity
  pass taken BEFORE § 2.3 lands proves nothing about this defect — that is the
  whole finding — so the run that counts is the one after."*

## 4. The ruling

**Brett Heap, 2026-08-26: the retirement gate is CLEARED on the repository
evidence chain above. The live provider check is post-hoc confirmation, not a
precondition.**

The 2026-08-24 hold is discharged on its own stated terms — the document has a
projected form — and not by the reading the hold explicitly refused (treating a
provider-imposed gap as parity "holding").

### What this clearance does NOT assert

Recorded so the limit travels with the permission:

* It does not assert the provider's current state. The definitive read is
  `--parity` under the company profile, which needs the operator session. That
  read is now confirmation of an executed decision rather than a gate on it.
* It does not retire anything. Step 8 is an ACT, and it is an act on the legacy
  account's own notebooks — see § 5.
* It does not clear steps 5 or 10 by itself. Step 5 (live session notebooks)
  is separately held; step 10 closes on the realization, which needs step 8 done.

## 5. Step 8 is READY — AWAITING OPERATOR EXECUTION

Step 8 archive-renames seven notebooks **in `brettheap@gmail.com`**. Nothing in
this repository can perform it: it requires an authenticated `nlm` session bound
to the legacy account, and profile selection is process-global user state the
sync deliberately refuses to switch.

It is therefore prepared rather than performed. The exact commands, expected
outputs, and abort conditions are in:

**`docs/notebook-projection-retirement-runbook-step8.md`**

written to be run in one sitting, with the seven legacy ids resolved from the
legacy→company mapping recorded at the head of
the mapping block at the head of
`examples/lifecycle-notebook-workspaces.yaml` headed
`# Legacy (still live, pending retirement) -> new (live, registered) ids:`.

(Cited by header rather than line number: an earlier draft said "lines 21–28",
and the gate-clearance note this record itself added shifted the block to line 38.
A line citation into a file the same change edits rots by construction.)

That mapping is their ONLY source in this repository — the workspace records'
`provider_notebook_id` fields carry only the company ids. An earlier draft of
this record claimed the legacy ids came from those fields; the seven values were
right and the provenance sentence was wrong, corrected here rather than quietly.

**The wrong-profile hazard is smaller than this record first implied**, and the
runbook now says so: the renames address notebooks by uuid, the seven legacy
uuids exist only in the legacy account, so running them on the company profile
ERRORS rather than retitling the live books. The profile check remains as a
courtesy, not as the thing standing between the operator and a silent
corruption — which was underselling a guard that is structural.

## 6. The remaining chain, mapped

Where each downstream item stands once step 8 executes:

| Item | State | Unblocked by |
| --- | --- | --- |
| 4.4 re-derive | **TICKED HERE** — ran 2026-08-24, evidence in PR #289; the tick was owed since then | — |
| 4.5 prove parity | **TICKED HERE**, against the 2026-08-25 amended-rule run, with the blind-instrument caveat recorded | — |
| 4.6 retire legacy books | **READY — awaiting operator** | this ruling + the step-8 runbook |
| 4.7 share out | Awaiting **task 2.4** (the designated company-policy actor is still unnamed) — an operator decision, independent of step 8 | 2.4, then the governed lane |
| 5.1 close the open item | Closes on the realization, which needs 4.6 done | 4.6 |
| 6.1 / 6.2 archive bookkeeping | Ride the archive | 5.1, then archive-on-evidence |
| Step 5 (session notebooks) | Separately HELD — see the 2026-08-24 evidence; **not** cleared by this ruling | its own disposition |
| `add-notebook-hosting-credential-custody` | Independent; § 1–§ 3 in flight | — |
| `notebook-access-wallet-governance` (#294) | Staged, and its INDEX row sequences it **behind these held steps** | 4.6 clearing |

## 7. CORRECTED AFTER EXECUTION (2026-08-26) — the chain is longer than § 6 said

Step 8 executed the same day. Two corrections to the map above, both making the
archive FURTHER away rather than nearer, which is why they are recorded:

* **4.6 is DONE** — renamed=7, skipped=0, failed=0; aliases clean; the seven
  company books present and un-retitled. Evidence in
  `docs/notebook-projection-migration-evidence-2026-08-24.md`.
* **5.1 IS NOT MET, and § 6 was wrong to imply step 8 would close it.** That open
  item records the AUTHENTICATION blocker; its own strategic direction is
  unattended re-authentication — the *"log in whenever it wants"* property. The
  account moved and the property does not exist: the sign-in is interactive,
  `nlm login` is broken by the notebook.google.com rebrand, and the ratified
  custody text says custody does not deliver automation. It closes on that
  capability, not on this act.
* **The post-hoc parity did not come back clean**, and the retirement is
  confirmed anyway on the number that matters: live managed titles are **675**,
  exactly what 2026-08-25 recorded. The four books reporting pending changes are
  derived-side drift since that apply — including this very runbook, written the
  same day and not yet projected.

So the archive now waits on THREE things, not two: **4.7** (blocked on task 2.4's
unnamed company-policy actor), **5.1** (blocked on unattended auth, a named
successor), and a reconciling `--apply` to clear the derived drift.

**Archive-on-evidence for this change is reachable once 4.6 and 4.7 execute and
5.1 closes** — 4.7 being the one that still carries an unnamed actor, so it, not
step 8, is now the long pole.
