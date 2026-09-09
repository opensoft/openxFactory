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

## § 4 gate results

All runs at head `645e88ec41c271b002376017e810540f5e1912b1` unless a later
final-head section supersedes them. `PIN` is `<scratchpad>/cli-pin-prefix`.

### 4.1 — the pinned OpenSpec CLI (FR-024, SC-002)

**Pinned CLI**: `@fission-ai/openspec@1.12.0`, resolved from the pinned artifact
at content address `c844543999f673cdd72445879b86a4abea4c07ef`, integrity
`sha512-oFE2Lj7WVSc87nSi…` **verified** by the entrypoint on every run. PATH's
`openspec` is 1.2.0 and was never used for any recorded result.

```bash
OPENSPEC_TELEMETRY=0 PATH="$PIN/bin:$PATH" \
  python3 scripts/validate-openspec-cli-pin.py --change govern-archived-record-edits --strict
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
