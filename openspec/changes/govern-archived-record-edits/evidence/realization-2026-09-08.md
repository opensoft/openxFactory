# Realization evidence — govern-archived-record-edits (openxFactory half)

**Branch**: `032-govern-archived-record-edits`
**Lane**: `opsXfactory-1`
**Head this file was opened at**: `645e88ec41c271b002376017e810540f5e1912b1`
**Base**: `main` `68712924732849fd146c3a1969b79879b44fae7c`
**Realization date**: 2026-09-08 (the date this branch's acts are dated to, and
the date this file's name carries). Gate runs are stamped with their own UTC
time; the § 4 runs below were taken either side of the 2026-09-09T00:00Z
rollover and each says which, because an aging finding's day count moves with
the clock and a comparison that hid that would be a false comparison.

## What this file is NOT

- **Not a ruling.** Nothing here authorizes anything. The ruling that authorized
  this packet is Brett Heap's, recorded at `review/ratification-2026-09-08.md`.
- **Not a ratification.** The packet was ratified on 2026-09-08; this file
  records the realization that followed it.
- **Not a promotion.** The delta reaches promoted canon at the ARCHIVE ACT,
  which is a separate, later act and is the lane's.

## What this file is

**LOCAL evidence at a named head, not CI.** Every result below was produced by a
command run in a dedicated clone at the head it names. CI on the lane's pull
request is a SEPARATE confirmation that this realization neither performs nor
claims.

**A record of edits to an ACTIVE packet.** This packet is not under
`openspec/changes/archive/`, so the ratified requirement *An archived record is
edited only as a bookkeeping correction under a recorded ruling* does not bind
these edits. The discipline is followed anyway — dated notes, superseded
sentences quoted and named, nothing deleted — because the packet's credibility
rests on it. After the archive act the same edits WOULD take the archived-record
route, which is why realization happens before the archive rather than after.

**Two evidence homes, different jobs.** THIS file is AUTHORITATIVE: it is what
the archive act reads. The files under
`specs/032-govern-archived-record-edits/evidence/` are the RAW CAPTURES it cites
by path. Where the two disagree the capture is right and this file is corrected
forward.

**One sanitization, declared.** Two captures carried host-absolute paths in the
pinned CLI's own banner. Per the estate rule against writing host-absolute paths
into committed files, `<pinned-cli-cache>` and `<scratchpad>` were substituted in
`gate-4.1-change-strict.txt` (2 + 1 occurrences) and `gate-4.1-all-strict.txt`
(2 + 1). Nothing else was altered: return codes, counts, summary lines and the
integrity digest are as produced.

## Heads every cross-repository claim below was measured at

| Repository | Ref | Sha |
| --- | --- | --- |
| openxFactory | branch head | `645e88ec41c271b002376017e810540f5e1912b1` |
| openxFactory | `main` (branch base) | `68712924732849fd146c3a1969b79879b44fae7c` |
| openxFactory | `origin/main` at check time | `6cc062887709c2bf537c7123a40a3cde654acd36` |
| OpsxFactory | `origin/main` at check time | `bbbef015cd394e2de31586b9718356586c413884` |

`origin/main` moved from `68712924` to `6cc06288` while this branch was open. NO
forward merge was taken — no task called for one — so `68712924` remains the
comparand for the path-set check and the doc-health baseline, and that is stated
rather than left to inference.

## Measurement 1 — the pinned-target check (task 4 note, FR-008)

**No IN-REPO `sha256` pin names `docs/document-lifecycle.md`, measured at base
`68712924`.** "In-repo" is load-bearing: task 1.2a's ratified scope is in-repo
pointers to in-repo targets, and a broader claim would overstate what was
measured. Re-taken at the final head below.

Method, named rather than only its conclusion:

```bash
grep -rn 'sha256' --include='*.yaml' --include='*.yml' --include='*.json' . \
  | grep -i 'document-lifecycle'                      # no output
grep -rln 'docs/document-lifecycle.md' --include='*.yaml' --include='*.yml' \
  --include='*.json' .                                # 5 files, each resolved below
python3 -c "yaml.safe_load(contracts/manifest.yaml) -> walk all string values"
                                                      # 0 docs/-prefixed path values
```

`contracts/manifest.yaml` was PARSED as YAML rather than grepped: a grep over a
folded scalar reports prose that is not a path value.

The five files that name the path were each resolved rather than dismissed:

| File | Why it is not a pin |
| --- | --- |
| `contracts/schemas/ideation-dashboard-snapshot.schema.yaml` | A COMMENT naming the document as the source of the `Status:` vocabulary. No digest anywhere near it. |
| `examples/document-cataloging/document-catalog-pending-transitions.example.yaml` | Catalog-snapshot FIXTURE. It does pair the path with `content_hash: 11cdac06…`; that value already matched neither the file at base `68712924` (`10f8404a…`) nor at this head, so nothing was verifying it before this branch either. |
| `examples/document-cataloging/document-catalog-reference-invalidation.example.yaml` | Same fixture family; its `{repo, path}` evidence refs carry no digest. |
| `examples/document-cataloging/negative/snapshot-evidence-ref-extra-property.yaml` | A deliberately INVALID negative fixture. |
| `openspec/changes/archive/2026-08-22-sanction-ratified-record-spelling/.openspec.yaml` | Narrative prose naming the document. No digest. |

**The fixture criterion is met and PROVEN, not asserted** (FR-008b): no gate
reads these as pins and nothing verifies them.
`scripts/validate-document-catalog.py` schema-validates the examples' SHAPE and
never hashes a file on disk; doc-health's catalog families read
`ctx.catalog_root` — `health/document-catalog/` — and that tree DOES NOT EXIST in
this repository, so there is no live catalog entry naming this document at all.
`examples/document-cataloging/README.md` states the same in its own words:
"static reference material, not runtime state".

**FR-008c's contingency did NOT fire.** No pin was found naming a file this
branch edits, and no candidate pin was left unresolved.

**Two facts kept apart** (FR-008b): "no in-repo pin names this file" is a
statement about POINTERS. "This family has declared no re-derivation rule" is a
statement about OBLIGATIONS. Only the first is measured here; nothing is asserted
about the second. The measurement is IN-REPO by ruling and says nothing about
pins held in a consuming repository (FR-035).

## Measurement 2 — MODIFIED-block currency (task 4.2 — RUN AND RECORDED, BOX LEFT OPEN)

Requirement compared: *Proposal packets carry the lifecycle header*, canon at
`openspec/specs/document-lifecycle/spec.md` against the delta at
`openspec/changes/govern-archived-record-edits/specs/document-lifecycle/spec.md`.

| Measure | Value |
| --- | --- |
| canon characters | **5,815** |
| delta characters (quickstart script's own bound) | **7,209** |
| delta characters (bounded at `## ADDED Requirements`) | **7,186** |
| **canon lines removed** | **0** |
| delta lines added | 17 |

**The two delta numbers are reconciled rather than one of them reported.**
`quickstart.md` § 5 states 7,186 beside a script whose terminator is
`\n### Requirement:`; because the next `### Requirement:` heading falls under
`## ADDED Requirements`, that script actually returns 7,209. The difference is
exactly 23 characters = `len("\n## ADDED Requirements\n")`. The discrepancy is in
this feature's own quickstart expectation, not in the ratified bytes, and the
load-bearing result is identical under both bounds: **0 canon lines removed** —
the MODIFIED block carries canon forward whole and inserts only.

**Box 4.2 is deliberately LEFT UNTICKED.** The rule demands currency
CONTINUOUSLY until archive; a realization tick would retire the clearance signal
the `modified-block-currency` family exists to keep live. The archive act re-runs
this.

## Measurement 3 — the cross-citations against the landed twin (FR-007a, SC-010)

Performed in a READ-ONLY clone of OpsxFactory (`<scratchpad>/opsx-citation-archive`,
`git fetch origin main` taken first). Nothing in OpsxFactory was written.

**The twin LANDED**: `bbbef015cd394e2de31586b9718356586c413884` — "Merge pull
request #279 from opensoft/change/govern-archived-record-edits",
2026-09-08T11:28:23-04:00 = **2026-09-08T15:28:23Z**.
`git merge-base --is-ancestor bbbef015… origin/main` succeeds; it is that
repository's `main` tip at the check.

**This packet's citations of the twin, on OpsxFactory `main` `bbbef015…`:**

| Citation | Resolves |
| --- | --- |
| `OpsxFactory:change:govern-archived-record-edits` (the twin) | YES — `openspec/changes/govern-archived-record-edits/` present and ACTIVE, six files, delta at `specs/openspec-archive-citation-integrity/spec.md` |
| `docs/packet-lifecycle-headers.md` (the local convention) | YES — present |
| `OpsxFactory:change:add-pre-archive-citation-gate` | YES — at `openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/` |
| `OpsxFactory:change:add-content-address-integrity-gate` | YES, as PROPOSED — branch `change/add-content-address-integrity-gate` at `cbbe5b48`; absent from `main`, which is what the packet itself asserts |
| `models/content-address-families.yaml` ABSENT from `main` and from the proposing branch | HOLDS — absent, as claimed |
| OpsxFactory commit `57fd9fd2` | YES — 2026-08-24, "Discharge all 55 lifecycle-header defects in the OpenSpec scan set" |
| OpsxFactory commit `40aaa93b` (PR #248) | YES — 2026-09-06 |

**The archive-path pair resolved as the packet built it to.** `.openspec.yaml`
§ Register and `proposal.md` name BOTH the live path
`openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`
and the archive path
`openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`,
saying explicitly that the first was the fact at authoring and the second becomes
the fact on merge. MEASURED NOW: the archive path IS PRESENT and the live path IS
GONE — the archive landed. The citation therefore RESOLVES; what is stale is only
the packet's tense ("still OPEN at this writing"), a dated claim that was true
when written. NO EDIT IS MADE FOR IT: `.openspec.yaml` is frozen (FR-009a) and
`proposal.md` takes only the one additive note FR-010 authorizes, whose subject
is the enumeration. This is recorded here instead.

**The twin's citations of this packet, on openxFactory `main` `6cc06288`:**

| Citation | Resolves |
| --- | --- |
| openxFactory's `govern-archived-record-edits` | YES — `openspec/changes/govern-archived-record-edits/` present |
| PR #788 merged as openxFactory `main` `3504287a2536b047e5ff4f9f8345b5ae735ba7ab` | YES — resolves and IS an ancestor of `origin/main` |
| `openspec/changes/govern-archived-record-edits/review/ratification-2026-09-08.md` | YES — present |
| the promoted `document-lifecycle` capability | YES — `openspec/specs/document-lifecycle/spec.md` present |
| openxFactory's `prepare-openspec-1.12-readiness` | YES — active change present |
| openxFactory's `add-consent-custody-rederivation-record` | YES — active change present |

**EVERY CROSS-CITATION RESOLVES IN BOTH DIRECTIONS.** None failed, so FR-025's
stop was not triggered on this ground. Task 3.1's act is DONE and its box is
ticked on THIS PERFORMED CHECK, not on the merge alone.

**Dated third-party measurement for task 3.3** (FR-032): openxFactory's
`add-consent-custody-rederivation-record` merged `543d47a9` (PR #774,
2026-09-07); its `tasks.md` at `origin/main` `6cc06288` carries **46 unticked
boxes and 0 ticked**, counted 2026-09-09 UTC.

## § 4 gate results — INTERIM, at head `645e88ec`

**THESE ARE THE INTERIM RESULTS.** They were taken at head `645e88ec`, which
carries the `docs/document-lifecycle.md` adoption but NOT the `tasks.md`,
`proposal.md` or `README.md` edits that followed. They are SUPERSEDED BY THE
FINAL-HEAD SECTION AT THE END OF THIS FILE and are kept rather than deleted, so
a reader can see what was measured when. Every result below was reproduced at
the final head; none was replaced by a different value. `PIN` is
`<scratchpad>/cli-pin-prefix`.

### 4.1 — the pinned OpenSpec CLI (FR-024, SC-002)

**Pinned CLI**: `@fission-ai/openspec@1.12.0`, resolved from the pinned artifact
at content address `c844543999f673cdd72445879b86a4abea4c07ef`, integrity
`sha512-oFE2Lj7WVSc87nSi…` **verified** by the entrypoint on every run. PATH's
`openspec` is 1.2.0 and was never used for any recorded result.

```bash
OPENSPEC_TELEMETRY=0 PATH="$PIN/bin:$PATH" \
  python3 scripts/validate-openspec-cli-pin.py --change
  govern-archived-record-edits --strict
```

- **rc 0.** `Totals: 1 passed, 0 failed (1 items)`
- `OK openspec-cli-pin: … verified against its content address and every target validated --strict clean`
- capture: `specs/032-govern-archived-record-edits/evidence/gate-4.1-change-strict.txt`

```bash
OPENSPEC_TELEMETRY=0 PATH="$PIN/bin:$PATH" \
  python3 scripts/validate-openspec-cli-pin.py --all --strict
```

- **rc 0.** `Totals: 99 passed, 2 failed (101 items)`
- `every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.`
- capture: `specs/032-govern-archived-record-edits/evidence/gate-4.1-all-strict.txt`

**SC-002's comparison, taken in BOTH directions.** The ratification record's
baseline is 99 passed / 2 failed / 0 undispositioned. Measured here: **99 passed
/ 2 failed / 0 undispositioned.** The count moved in NEITHER direction — not up,
which would be a new undispositioned finding this branch cannot clear (
`contracts/**` holds the dispositions and is frozen), and not down, which would
be a difference too rather than a bonus. The two accepted exceptions are
`add-chain-attestation / signed-execution-chain` and
`add-composed-view-authoring / ideation-dashboard`, both dispositioned in
`contracts/openspec-cli-pin.yaml` and both accepted by Brett Heap, 2026-09-05.
They are PRE-EXISTING (FR-037): they sit in files this branch does not touch and
predate it.

### 4.3 — the corpus validators (SC-004)

Capture: `specs/032-govern-archived-record-edits/evidence/gate-4.3-validators.txt`

| Command | rc | Summary line |
| --- | --- | --- |
| `python3 scripts/validate-sequenced-after.py .` | **0** | `sequenced_after validation passed (41 active changes, 8 declaring the field).` |
| `python3 scripts/validate-sequenced-after.py . --ledger-diff` | **0** | `per-change sweep ledger consistent with the corpus (185 rows).` |
| `python3 scripts/validate-scope-globs.py .` | **0** | `scope_globs validation passed (all active changes conform).` |
| `python3 scripts/validate-manifest-digests.py .` | **0** | `OK contracts/manifest.yaml: 188 per-file digest(s) verify` |

### 4.4 — doc-health, finding set diffed against `main` (SC-003, FR-028, FR-029)

**Baseline authority**: `main` **`68712924`**, the commit this branch was cut
from and has not merged past.

**The identity trap was handled by construction.** doc-health stamps the
checkout's DIRECTORY BASENAME into `repo=<basename>` on every finding line, into
the `Repo-Identity:` header and into the "scope limited to single repo" line, and
`--previous-report` REFUSES a mismatched pair by design. Both baseline checkouts
therefore carry the SAME basename as the branch checkout — `oxf-realize-f3` —
at `<scratchpad>/dh-base/oxf-realize-f3` and `<scratchpad>/dh-proof/oxf-realize-f3`.
`--previous-report` was not used.

**The recipe was PROVEN main-vs-main before it was trusted**: two runs over the
SAME commit `68712924` from the two identically-named directories, `diff` → **ZERO
differences**. Only then was a branch-vs-main diff treated as evidence.

**A SUPERSEDED INTERIM RESULT, STRUCK AND KEPT** (FR-021). The first branch
comparison was taken across the **2026-09-09T00:00Z rollover**: the baseline ran
on 2026-09-08 and the branch run on 2026-09-09. Every `staged-candidate-aging`
and `ideation-routing` finding embeds a DAY COUNT in its message, so all of them
moved by one day, and two topics crossed the 30-day threshold and appeared as new
warnings (`manager-review-approval-scope-kind`, `session-notebook-reconciliation`),
taking the headline from 55 to 57 warnings. NONE of that came from this branch's
diff. That run is superseded by the pinned-clock comparison below and is kept at
`specs/032-govern-archived-record-edits/evidence/doc-health-diff-INTERIM-superseded-clock-rollover.txt`
rather than deleted.

**The comparison of record** pins the aging clock on BOTH sides with
`--as-of 2026-09-09`, and the main-vs-main proof was RE-TAKEN at that same
`--as-of` (`diff` → ZERO differences) before the branch was compared:

```bash
python3 scripts/doc-health.py --single-repo <baseline-checkout> --as-of 2026-09-09 \
        --fail-on error --report-out <A>
python3 scripts/doc-health.py --single-repo . --as-of 2026-09-09 \
        --fail-on error --report-out <branch>
diff <A> <branch>
```

- **FINDING SET: IDENTICAL.** `diff` of the `- severity=…` finding lines returns
  **zero differences** (rc 0). Headline both sides: **10 critical, 9 error, 55
  warning, 16 info.**
- The full-report diff is not empty, and the two differing lines are named rather
  than smoothed away. **Neither is a finding**; both are counts that moved only
  because the document GREW by 199 words:
  - `Canon share by words: 38.9% (345150 → 345349 canon words / 886876 → 887075 governance words)` — the percentage is unchanged at 38.9%.
  - `| standard | 6 | 16115 |` → `| standard | 6 | 16314 |` — the same 199 words, and the document COUNT is unchanged at 6.
- Both runs exit **rc 1** on PRE-EXISTING error-level findings (10 critical, 9
  error) that are present identically on `main` and are not attributed to this
  branch (FR-037). Most live in files FR-009a freezes.
- captures: `doc-health-main-68712924-asof-2026-09-09-A.md`,
  `doc-health-main-68712924-asof-2026-09-09-B.md` (the proof twin),
  `doc-health-branch-645e88ec-asof-2026-09-09.md`,
  `doc-health-diff-main-vs-branch.txt`, all under
  `specs/032-govern-archived-record-edits/evidence/`.

### 4.5 — the test suite (SC-005)

```bash
python3 -m pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q
```

- **rc 0** — captured as a return code, not inferred from a pipeline
- `330 passed, 2 subtests passed in 26.32s`
- capture: `specs/032-govern-archived-record-edits/evidence/gate-4.5-pytest.txt`

## The note classes, and they sum to 28

Every box in this packet's `tasks.md` carries exactly ONE of the three classes,
audited mechanically rather than counted by eye:

| Class | Count | Boxes |
| --- | --- | --- |
| **ticked-with-evidence** | **19** | 0.1, 1.1, 1.2, 1.2a, 1.2b, 1.2c, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 3.1, 3.4, 4.1, 4.3, 4.4, 4.5, 5.1 |
| **NOT-OWED** | **8** | 3.2, 3.3, 3.5 (other repositories or another packet), 5.2, 5.3 (the lane's landing acts), 6.1, 6.2, 6.3 (the archive act) |
| **RUN-RECORDED-LEFT-OPEN** | **1** | 4.2 |
| | **28** | |

**19 + 8 + 1 = 28**, which is the packet's full box count. The audit also
confirmed: no box carries two classes or none; every note carries its UTC date;
the tick state matches the class on every box (nothing ticked without the
ticked-with-evidence class, nothing carrying that class left unticked); and all
FIVE § 4 notes CITE this file rather than restating a result.

**Every NOT-OWED note says WHICH KIND it is.** All eight are NOT-OWED-YET —
falling due to another repository, another packet, or the lane — rather than
permanently another's; each names the owner and, where it is measurable, the
state that owner is in at a named head and date.

**The class is not the note.** Each of the 28 also carries the act performed, the
UTC date, and a pointer to its evidence.

## No invented quotation

Every block quotation this realization wrote into `tasks.md` was checked
mechanically against the file's pre-edit bytes: **7 block quotes and 4 inline
quotations, all 11 present verbatim** (whitespace-normalised comparison against
`HEAD:openspec/changes/govern-archived-record-edits/tasks.md`). **NO WORD IS
ATTRIBUTED TO BRETT HEAP ANYWHERE.** The § 1 notes cite the ratification by
review id `5141756427`, its APPROVED state, its `2026-09-08T12:38:36Z` timestamp
and the record path, and say in terms that the approval body is EMPTY so no
verbatim word exists. Restating what a record states is citation; putting a
sentence in his mouth would be invention, and none is made.

## The approval state, re-measured — BOTH REVIEWS NOW READ DISMISSED

**A READER WHO SEES "APPROVED" AND STOPS THERE WOULD BE MISLED, SO THE TWO
FACTS ARE STATED IN ONE CLAUSE EVERYWHERE THIS REALIZATION CITES THE APPROVAL.**
Measured 2026-09-09 UTC, read-only, `gh api
repos/opensoft/openxFactory/pulls/788/reviews` plus the issue timeline for the
dismissal events:

| Review | By | State now | Submitted | Commit | Body | Dismissed |
| --- | --- | --- | --- | --- | --- | --- |
| `5141756427` | `brettheap` (MEMBER) | **DISMISSED** (`state_was: approved`) | `2026-09-08T12:38:36Z` | `d0f8cccf` | EMPTY | `2026-09-08T12:53:23Z`, no message |
| `5142530432` | `brettheap` (MEMBER) | **DISMISSED** (`state_was: approved`) | `2026-09-08T13:45:56Z` | `158a4d3b` | EMPTY | `2026-09-08T13:53:22Z`, no message |
| `5138391380` | `sourcery-ai[bot]` | COMMENTED | `2026-09-08T06:58:14Z` | `97d1e7fa` | 248 bytes | — |

**THERE ARE TWO APPROVING REVIEWS, NOT ONE**, and both were dismissed by GitHub
on the pushes that followed them. No dismissal message on either, with
`state_was: approved` on both timeline events — the signature of automatic
stale-approval dismissal under branch protection, not a withdrawal. **THE
RATIFICATION STANDS** on `review/ratification-2026-09-08.md`, which is the
durable record, and NOT on a currently-APPROVED review; every note this
realization writes says so in the same clause as the citation.

**THE RATIFIED TEXT IS NOT EDITED FOR THIS.** `proposal.md`'s front matter, the
ratification record itself, and the ratified README row sentences all say
"APPROVED" without the dismissal, and all three are FROZEN. The clause lives in
the realization's own notes and in this file. Nine notes in the packet's
`tasks.md` carry it.

**ONE DIVERGENCE, NAMED RATHER THAN RESOLVED.** The record gives the ratified
baseline as `8cc76e1b`; the API reports `d0f8cccf` as review `5141756427`'s
commit. The record's own § on the two clocks already measures the packet's bytes
as IDENTICAL at both heads, so nothing turns on it and this realization resolves
nothing — it records both readings, because the failure this packet exists to
refuse is a claim whose basis nobody can re-derive.

## The active-proposal census — what the corpus actually does

**19 TICKED / 9 OPEN IS THE NORM HERE, NOT AN INNOVATION**, and it is counted
rather than asserted. Across the **40 active openxFactory changes carrying a
`tasks.md`** at this head:

- **38 of 40 carry at least one ticked box** while still active and unarchived.
- Only **TWO** are wholly unticked: `adopt-medxsoft-repository-identity` (0/30)
  and `add-consent-custody-rederivation-record` (0/46) — the second being the
  very packet this one cites at task 3.3, which is why it was the comparison the
  ratified text reached for.
- **RE-TAKEN after the forward merge**, at `main` `6da94302`: **43** active
  changes with a `tasks.md`, **40** carrying at least one ticked box, **3**
  wholly unticked — main's two new proposals arrive unticked, as new proposals
  do. The proportion is unchanged and so is the conclusion.
- Ratios span 50/6 (`prepare-openspec-1.12-readiness`) to 0/46; this packet's
  19/9 sits in the middle of the distribution.

An active packet with every box open is the OUTLIER in this corpus. That is the
measured basis for ticking a ratified-but-unarchived packet, and it is recorded
here so the archive act does not have to take it on trust.

## The `untick` re-derivation over the packet

**RUN AFTER THE CONTENT WAS FINAL, AND IT CAUGHT TWO THINGS READING DID NOT.**
`grep -rn -i untick` over the packet's `tasks.md`, `proposal.md`, `design.md`,
`.openspec.yaml`, `review/` and `specs/` (the evidence file is excluded, since
recording the sweep would otherwise perturb it) returns **27 hits**, every one
classified:

- **Ratified assertions now AMENDED, with a block quote beside them** —
  `tasks.md` 7, 80-81, 86, 138, 142, and **686** (the § 6.1 "what the archive act
  reads is the UNTICKED BOX 3.4"); `proposal.md` 17 and 99.
- **This realization's own block quotes of those** — `tasks.md` 17, 95, 154, 158;
  `proposal.md` 57, 63.
- **This realization's own prose** — `tasks.md` 103, 648, 650; `proposal.md` 52.
- **True statements about OTHER packets, measured and dated** — `tasks.md` 124
  and 505, `proposal.md` 152 and 282, `design.md` 231,
  `specs/document-lifecycle/spec.md` 266 (all the consent packet's 46/0, verified
  2026-09-09 at `main` `6cc06288`).

**THE SWEEP EARNED ITS PLACE: `tasks.md:686` was found by it, not by reading.**
§ 6.1's ratified "what the archive act reads is the UNTICKED BOX 3.4" is
falsified by 3.4's tick, and the note there addressed it in prose without
block-quoting it. It now carries the quote, in the same form as every other
amendment.

**AND ONE FINDING THIS REALIZATION DELIBERATELY DOES NOT FIX, because it cannot:**
`.openspec.yaml:47-50` asserts *"NOTHING IS REALIZED BY THIS PACKET. No archived
byte is edited, no pin is re-derived, no checker is written, no convention is
amended, and every box in `tasks.md` is unticked."* Two of those clauses are now
false — something IS realized, and the boxes are not all unticked. **`.openspec.yaml`
is FROZEN** by the ratified scope (`spec.md` FR-009a lists it, and the packet's
own § *What This Change Does NOT Do* keeps it), so amending it is not this
realization's act. It is RECORDED here instead, by file and line, so the archive
act sees a known-stale ratified assertion rather than discovering one. The same
is true of `review/ratification-2026-09-08.md:115` ("stays unticked on `main`"),
which is a record of what was true when it was captured and is correct as a
record.

## Gates that could not be run

**NONE.** Every § 4 gate RAN. No gate was skipped for a missing dependency or an
unavailable checkout, so FR-025's "could not run" class is empty here — a
distinct fact from a gate that ran and FAILED, and stated so it is not confused
with one.

## Failures

**NO § 4 GATE FAILED.** Every return code above is the code the command produced.
The two rc 1 values under 4.4 are doc-health reporting PRE-EXISTING findings that
are byte-identical on `main`; they are not this branch's and no tick rests on
their absence.

---

## FINAL-HEAD RESULTS — head `539edd282dd3e16c0cba6c0e5395d3b2882a618f`

**THIS SECTION IS THE ONE THE ARCHIVE ACT READS.** The interim section above was
taken at `645e88ec`; the commits after it — the task record, the `proposal.md`
realization note and the `README.md` row sentence — all touch paths the pinned
CLI and doc-health scan, so the whole § 4 set was re-run here. **Every gate was
re-run; NONE was carried forward.** No superseded result was deleted; the interim
section is struck by name above.

**NO FORWARD MERGE WAS TAKEN.** `origin/main` moved to `6cc06288` while this
branch was open and no task called for merging it, so these results are not
stale on that ground. A forward merge taken after this run would make this run
stale and the set would have to be re-run at the new head.

### Preconditions, re-taken at this head

- **Ancestry / packet currency (T002's check).**
  `git merge-base --is-ancestor 3504287a HEAD` still succeeds.
  `git log --oneline 3504287a..main` over the packet, `openspec/specs/document-lifecycle`
  and `docs/document-lifecycle.md` is still **EMPTY** — the ratified bytes, promoted
  canon and the § 3.4 target have not moved on `main`. The same log against `HEAD`
  now lists exactly this branch's four content commits (`645e88ec`, `31704f0a`,
  `0e7a67f3`, `1b9b66c7`) and nothing else, which is the expected difference and
  not a movement of canon.
- **Pinned target, re-taken (FR-008a).** Still **no IN-REPO `sha256` pin names
  `docs/document-lifecycle.md`** — the grep returns nothing and
  `health/document-catalog/` still does not exist. A pin arriving with a forward
  merge would be a pin; none arrived, because no merge was taken. The finding is
  recorded beside the earlier one rather than over it: both readings agree.

### The gates at the final head

| Gate | Command | rc | Result |
| --- | --- | --- | --- |
| 4.1a | `validate-openspec-cli-pin.py --change govern-archived-record-edits --strict` | **0** | `Totals: 1 passed, 0 failed (1 items)` |
| 4.1b | `validate-openspec-cli-pin.py --all --strict` | **0** | `Totals: 99 passed, 2 failed (101 items)`, **0 UNDISPOSITIONED** |
| 4.3a | `validate-sequenced-after.py .` | **0** | `sequenced_after validation passed (41 active changes, 8 declaring the field).` |
| 4.3b | `validate-sequenced-after.py . --ledger-diff` | **0** | `per-change sweep ledger consistent with the corpus (185 rows).` |
| 4.3c | `validate-scope-globs.py .` | **0** | `scope_globs validation passed (all active changes conform).` |
| 4.3d | `validate-manifest-digests.py .` | **0** | `OK contracts/manifest.yaml: 188 per-file digest(s) verify` |
| 4.4 | `doc-health.py --single-repo . --as-of 2026-09-09 --fail-on error` | 1 (pre-existing) | **finding set IDENTICAL to `main`'s** |
| 4.5 | `pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q` | **0** | `330 passed, 2 subtests passed` |

Both 4.1 runs go through `scripts/validate-openspec-cli-pin.py` with
`@fission-ai/openspec@1.12.0` on `PATH`, verified against content address
`c844543999f673cdd72445879b86a4abea4c07ef` on every run; PATH's 1.2.0 was never
used. **SC-002 at the final head: 99 / 2 / 0 — the ratified baseline exactly,
moved in NEITHER direction.**

Captures: `final-gate-4.1-change-strict.txt`, `final-gate-4.1-all-strict.txt`,
`final-gate-4.3-validators.txt`, `final-gate-4.5-pytest.txt`,
`final-doc-health-branch-be643e55.md`, `final-doc-health-diff-main-vs-branch.txt`,
`final-modified-block-currency.txt`, all under
`specs/032-govern-archived-record-edits/evidence/`.

### 4.4 at the final head, in full

Baseline unchanged: `main` `68712924`, same identically-named checkout, same
`--as-of 2026-09-09` on both sides, `--previous-report` never used.

- **Finding-line diff: ZERO differences.** Headline identical both sides: **10
  critical, 9 error, 55 warning, 16 info.**
- The full-report diff has the SAME TWO non-finding lines as the interim run and
  no others — canon/governance word totals +199 (share unchanged at 38.9%) and
  the `standard` stage word count +199 (document count unchanged at 6). The
  `tasks.md`, `proposal.md` and `README.md` commits added no finding: `README.md`
  is outside doc-health's governed roots, `tasks.md` is a packet working file the
  rules do not reach, and `proposal.md` IS in the lifecycle scan set and still
  parses `Status: ratified` — checked directly against the repository's own
  `corpus.parse_status`, which returns `ratified` for the file both before and
  after the realization note.
- **IDEMPOTENCE (FR-024a), demonstrated rather than assumed**: the baseline was
  re-run a third time at the same head and the same `--as-of`, and the report was
  **byte-identical** to the stored baseline. No result here was obtained by
  re-running until green.

### 4.2 at the final head — re-taken, still NOT ticked

canon **5,815** characters; delta **7,209** (script bound) / **7,186** (bounded
at `## ADDED Requirements`); **0 canon lines removed** under both bounds. Canon
did not move under the block, and no forward merge was taken that could have
moved it. **The box remains deliberately OPEN for the archive act.**

### Failures at the final head

**NONE.** No § 4 gate failed at this head, so no tick rests on a failed gate and
nothing in `tasks.md` is struck on that ground. Had one failed, the tick it
supported would have been struck by a dated line naming the failing head rather
than removed. The two rc 1 values are doc-health reporting pre-existing findings
identical on `main`.

### Standing note on a later veto

Any of the five rulings open to veto, exercised after this run, RE-OPENS it for
the paths that ruling touches: the reversal is a forward-only act and the gate
set is re-run at the head that carries it. Two of the five are already isolated
for exactly that — the `proposal.md` note is commit `1b9b66c7` alone and the
`README.md` row sentence is commit `539edd28` alone, so each reverts as one
named act without disturbing anything else.

---

## RE-RUN AT THE TRUE FINAL HEAD — `be643e55b5006b60aa6f488c4ed2f6b3b8de67ca`

**WHY THERE IS A SECOND FINAL HEAD, STATED RATHER THAN GLOSSED.** After the
`539edd28` run, one more commit landed on `tasks.md`: `be643e55`, a PURE
WHITESPACE re-wrap of the realization notes to the file's own 80-column style
(the attribution phrase was interpolated without re-wrapping, leaving 32 lines
at ~170 characters). `tasks.md` sits inside the change directory the pinned CLI
scans, so carrying `539edd28`'s results forward would have been reporting a
result for a head that no longer exists. **THE WHOLE § 4 SET WAS RE-RUN.**

**EVERY RESULT REPRODUCED IDENTICALLY at `be643e55`:**

| Gate | rc | Result |
| --- | --- | --- |
| 4.1a `--change … --strict` | **0** | `Totals: 1 passed, 0 failed (1 items)` |
| 4.1b `--all --strict` | **0** | `Totals: 99 passed, 2 failed (101 items)`, **0 UNDISPOSITIONED** |
| 4.3 (all four validators) | **0** | 4 of 4 at rc 0 |
| 4.4 doc-health | 1 (pre-existing) | **finding set IDENTICAL to `main`'s** |
| 4.5 pytest | **0** | `330 passed, 2 subtests passed` |

No value moved in any direction. SC-002 is 99 / 2 / 0 here too — the ratified
baseline exactly.

**A SANITIZATION THAT WAS UNDONE AND HAD TO BE RE-APPLIED — DECLARED, NOT
QUIETLY FIXED.** The two `final-gate-4.1-*` captures were sanitized of
host-absolute paths after the `539edd28` run, and the `be643e55` RE-RUN THEN
OVERWROTE THEM with fresh raw output, which was committed unsanitized in
`5dccfad1`. Two host-absolute paths per file therefore sat in the repository
between `5dccfad1` and the merged-head commit, against the estate rule that
committed files carry no host-absolute path. Re-sanitized here, forward-only.
The lesson is the same one this packet is about: an automated step that rewrites
a file after a manual correction silently undoes it, and only re-checking the
invariant at the end catches it. The invariant is now re-checked over BOTH
evidence directories at the final commit.

**ONE HONEST NOTE ABOUT THE CAPTURE FILES.** The `final-gate-*` captures were
OVERWRITTEN in place by this re-run rather than written alongside the
`539edd28` ones, so those files now hold `be643e55`'s output. Nothing is lost:
`539edd28`'s values are recorded in the FINAL-HEAD RESULTS table above, which is
preserved unchanged, and the two runs agree line for line on every recorded
figure. The doc-health capture was RENAMED from
`final-doc-health-branch-539edd28.md` to `final-doc-health-branch-be643e55.md`
so no file carries a head it does not hold. This paragraph exists because an
overwritten capture that nobody declares is exactly the failure mode this
packet's own motivating commit demonstrates.

**WHAT LANDS AFTER THIS RUN, AND WHY IT CANNOT MOVE A GATE.** One commit
follows: the feature's `specs/032-govern-archived-record-edits/` tree and this
`evidence/` file. Neither is gate-scanned — root `specs/` is outside
doc-health's `GOVERNED_ROOTS` and outside the pinned CLI's change scan, and
`evidence/` is excluded from the lifecycle scan set by `EVIDENCE_PARTS` and is
not part of the spec delta. The claim was CHECKED rather than asserted: the full
gate set was run once more after that commit and every result was unchanged.

**STILL NO FORWARD MERGE.** `origin/main` remains at `6cc06288` as far as this
branch is concerned; nothing was merged in, so no gate result here is stale on
that ground.

---

## THE FORWARD MERGE, AND THE GATE SET RE-RUN ON THE MERGED HEAD

**MERGED HEAD: `a83f2eb19b1b5c079254f7c35d6e79dbb20dcfb9`** (merge parents
`1a4864d1` and `6da94302`). `origin/main` moved from `68712924` to `6da94302`
while this branch was open — 19 commits — and FR-011 makes the earlier run stale
the moment the merge lands, so **the whole § 4 set was re-run here**. The merge
is `--no-ff` and carries the three trailers; it is the ONE commit FR-014 exempts
from the authored-commit trailer audit, and it is named as such rather than
counted as a violation.

**MAIN MOVED THE GATES THEMSELVES**, which is the strongest reason nothing was
carried forward: `scripts/proposal-support.py`, `scripts/sequenced_after.py` and
`scripts/validate-sequenced-after.py` all changed substantially, and
`validate-sequenced-after.py` gained a new arm — `archive-date agreement passed
(no archived row's moved_on predates its directory)` — that did not exist when
the earlier results were taken.

### The three shared files, resolved at the UNION by row-id set

| File | ours | main | merged | union | verdict |
| --- | --- | --- | --- | --- | --- |
| `README.md` Records rows | 187 | 189 | **189** | **189** | **merged == union** |
| `tests/sequenced_after/corpus-ledger.yaml` rows | 183 | 185 | **185** | **185** | **merged == union** |

Both merged automatically. Main contributed both new ids in each
(`amend-mirror-floor-regeneration-merge-authority`,
`refresh-install-repository-enumerations`) and re-classed
`mirror-floor-regeneration-automation`; this branch contributed NO row to either
file, so the union is main's set and nothing of this branch's was dropped. The
realization amendment at the END of our Records row survives intact.
`docs/document-lifecycle.md` also merged cleanly — main's addition is in
§ *Gates In Practice* near line 412, the adopted bullet is at line 138, and they
do not touch; the byte-exact note form is present and unchanged after the merge.

**THIRTEEN README LINE CITATIONS WERE RE-DERIVED**, because the merge shifted
them: the row start `515 → 659`, the first assertion `527 → 671`, the second
`545-548 → 689-692`. Every pointer in `tasks.md`, `spec.md`, `research.md` and
this file was updated and re-checked to resolve; a line pointer that silently
goes stale is the same defect class as a stale digest.

### Results on the merged head — every gate re-run, none carried forward

| Gate | rc | Result |
| --- | --- | --- |
| 4.1a `--change … --strict` | **0** | `Totals: 1 passed, 0 failed (1 items)` |
| 4.1b `--all --strict` | **0** | `Totals: 101 passed, 2 failed (103 items)`, **0 UNDISPOSITIONED** |
| 4.3a `validate-sequenced-after.py .` | **0** | `sequenced_after validation passed (43 active changes, 10 declaring the field).` + `archive-date agreement passed (no archived row's moved_on predates its directory).` |
| 4.3b `--ledger-diff` | **0** | `per-change sweep ledger consistent with the corpus (187 rows).` |
| 4.3c `validate-scope-globs.py .` | **0** | `scope_globs validation passed (all active changes conform).` |
| 4.3d `validate-manifest-digests.py .` | **0** | `OK contracts/manifest.yaml: 189 per-file digest(s) verify` |
| 4.4 doc-health | 1 (pre-existing) | **finding set IDENTICAL to `main` `6da94302`'s** |
| 4.5 pytest | **0** | `375 passed, 2 subtests passed` |

**SC-002 ON THE MERGED HEAD, AND THE COMPARISON IS ON THE RIGHT NUMBER.** The
item TOTAL rose 101 → 103 and the passed count 99 → 101 because MAIN ADDED TWO
ACTIVE CHANGES, not because anything of this branch's moved. The number SC-002
compares — the **dispositioned-exception count** — is **2**, exactly the ratified
baseline, and **UNDISPOSITIONED is 0**. Neither moved in either direction. The
two exceptions are the same pre-existing pair, in files this branch does not
touch. Test count 330 → 375 for the same reason: main added tests.

### 4.4 on the merged head, in full

**BASELINE RE-TAKEN AT THE COMMIT THE BRANCH MERGED FROM** (FR-029): `main`
**`6da94302`**, not the old `68712924`. Both baseline checkouts were moved to that
commit, both still named `oxf-realize-f3`, and **the recipe was RE-PROVEN
main-vs-main at the new baseline before it was trusted** — two runs over
`6da94302` from the two identically-named directories, `diff` → **ZERO
differences**. `--as-of 2026-09-09` pinned on both sides. `--previous-report`
never used.

- **Finding-line diff: ZERO differences.** Headline identical both sides: **10
  critical, 9 error, 57 warning, 16 info** (57 rather than 55 because the aging
  clock advanced on `main` too — it is identical on both sides, so it is not a
  difference this branch made).
- The full-report diff has the SAME TWO non-finding lines and no others: canon
  and governance word totals +199 (share unchanged at 39.1%) and the `standard`
  stage word count +199 (document count unchanged at 6). That is the adopted
  bullet, and it is not a finding.

### 4.2 and the pinned target, re-taken on the merged head

- **4.2**: canon **5,815**; delta **7,209** / **7,186**; **0 canon lines
  removed** under both bounds. Canon did not move under the block in the merge.
  **The box stays OPEN.**
- **Pinned target**: still **no IN-REPO `sha256` pin** names
  `docs/document-lifecycle.md`, and `health/document-catalog/` still does not
  exist. The merge brought no pin with it — which is exactly why FR-008a makes
  this a re-take rather than a citation.

### The `untick` sweep, re-run on the merged head

**29 hits, up from 27, and both new ones are this realization's own** — the § 6.1
block quote and the sentence naming the sweep that found it. No new
un-superseded assertion arrived with the merge, which is what the re-run is for.
The `.openspec.yaml:47-50` finding is unchanged and still deliberately unfixed,
that file being frozen. The sibling packet's **46 unticked / 0 ticked** was
re-measured at `6da94302` and still holds.

### Trailer audit on the merged head

**15 commits in `origin/main..HEAD`: 1 merge (exempt) + 14 authored, and 14 of
14 carry all three trailers.** SC-007 re-checked against the NEW merge base
`6da94302`: still only the six allowed paths, and nothing under any `archive/`
path, `scripts/`, `.github/`, `contracts/` or `tests/`.
