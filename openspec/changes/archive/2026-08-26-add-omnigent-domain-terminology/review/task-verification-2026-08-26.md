# Task verification: `add-omnigent-domain-terminology`

Status: record
Date: 2026-08-26
Ruling: Brett Heap, in-session 2026-08-26 — claim the change and run the
archive gate now: verification sweep, final ticks, then archive.
Verifier: Claude Opus 5 (agent), read-only against fresh clones.

## Method, and why it is stated first

Every ticked box in `tasks.md` was re-checked against the **artifacts at live
main**, not against the tick's own prose. Claimed file paths were opened,
claimed registry entries were parsed rather than grepped, claimed counts were
recounted, claimed commits were resolved and tested for ancestry, and claimed
digests were recomputed. The house rule this sweep serves is that a false tick
is worse than an open task, so a claim that could not be reproduced is
recorded as NOT VERIFIED rather than passed over.

Six fresh clones were used, all under a scratchpad, none of them a working
checkout: `opensoft/openxFactory` at `84375a55`, plus read-only clones of
`OpsxFactory` (`f1065cc`), `codexFactory` (`94d65b8`), `MedxFactory`
(`933cf15`), `LedgerxFactory` (`e0d1abe`) and `AdxFactory` (`1fc5a2f`). No
file in any existing checkout was read or written.

## Verdict table

| Task | Claim in one line | Verdict | Evidence |
|---|---|---|---|
| 1.1 | Direction 2026-08-09; annotate, never rename | VERIFIED | Direction quoted verbatim in `proposal.md` Why; the rename analysis is the proposal's own third paragraph |
| 1.2 | Ratified 2026-08-26, front matter moves with a record-citing line | VERIFIED | `proposal.md` front matter: `Status: ratified` + `Ratified: 2026-08-26 by Brett Heap`, citing `sanction-ratified-record-spelling` for the spelling |
| 2.1 | Optional `terminology` block + `label_map` $def | VERIFIED | `contracts/omnigent/omnigent-domain-overlay.schema.yaml:84` block; `label_map` at `:270`; `job_types`/`stop_conditions`/`routing` `$ref` it at `:148,150,152` |
| 2.2 | Validator semantic checks | VERIFIED | `scripts/validate-omnigent-contracts.py`: orphan key `:199`, duplicate label `:210`, unregistered body `:226`, `no_clean_equivalent` without note `:237`; registry loaded at `:93` |
| 2.2b | `standards_alignment` is a map keyed by body id, at most one per body | VERIFIED | Schema `:113`; all five shipped overlays parse as body-keyed maps with no duplicate body per worker |
| 2.2c | `standards-bodies.yaml` registry with load-bearing `names` | VERIFIED | 44 bodies parse; every entry carries `names`; the sourcing caveat is in the file header |
| 2.3 | Positive example demonstrates both crosswalk shapes | VERIFIED | `omnigent-domain-overlay.example.yaml` — `scope_framer` mapped under `apqc_pcf` AND `sfia` (multi-body), `change_author` `no_clean_equivalent` with note |
| 2.4 | Three negative fixtures with `# expect:` markers, family green | VERIFIED | All three files present; validator run exit 0, each rejected for the expected reason (`terminology`, `standards-bodies.yaml`, `no_clean_equivalent`) |
| 3.0 | Standing per-domain term/version verification | **TICKED THIS SWEEP** | See §"3.0 discharge" |
| 3.0a | Thirteen O*NET codes re-read; version moved 30.3 -> 31.0; ledgerx flagged not corrected | VERIFIED | `onet_it_occupations` carries 6 codes, `onet_engineering_occupations` 7 — thirteen exactly; both read `O*NET Database 31.0, released August 2026 (verified 2026-08-26)` |
| 3.1 | opsx: 9/5/8/6 covered, 6 mapped + 3 unmapped, `onet_it_occupations` alone | VERIFIED | Recounted from the overlay: terminology 9 workers / 5 job_types / 8 stop_conditions / 6 routing; unmapped set is exactly `blast_radius_reviewer`, `change_documentation_agent`, `admission_packet_agent`; one body |
| 3.2 | ledgerx: PCF returns as a third body; 28 crosswalks over 14 workers; PCF 6/3/5 | VERIFIED | 14 + 9 + 5 = 28 recounted; PCF mapped set and unmapped set match the read-back name for name; 5 omitted; APQC paragraph rides the header with ® marks; O*NET pin and by-version attribution moved together |
| 3.3 | adx: 10 workers, three bodies, O*NET 10 (5/5), PCF 10 (6/4), IAB 3 | VERIFIED | All four counts recounted exactly; `job_types`/`stop_conditions`/`routing` label sets unchanged by the population diff |
| 3.4 | codex: 11/12/6/6 covered, 8 mapped + 3 unmapped, `onet_engineering_occupations` alone | VERIFIED | Recounted; unmapped set is exactly `pr_admission_agent`, `merge_readiness_agent`, `scrum_master_worker`; one body |
| 3.5 | Medx population | **TICKED THIS SWEEP** | See §"3.5 discharge" |
| 3b.1 | 17 bodies, all Anglo-American, no jurisdiction field | VERIFIED | Registry at `df16f213` parses to exactly 17 bodies |
| 3b.2 | China report returned, 13 registry-shaped entries | VERIFIED | `LedgerxFactory .../supporting-docs/china-accounting-bodies-research-report.md` present, `Status: record` |
| 3b.3 | APQC version-sensitivity recorded so it cannot recur silently | VERIFIED | `apqc_pcf` entry carries the version pin and the rule; opsx overlay asserts no APQC mapping |
| 3b.4 | Registry now 30 bodies; `jurisdiction` on every body | VERIFIED | Registry at `8572d593` parses to exactly 30; every one of the 44 entries today carries `jurisdiction` |
| 3b.5a | 30 -> 41; `aicpa` split; SOX 404 rejected on the record | VERIFIED | Registry at `db4de64d` parses to exactly 41; `aicpa_professional_standards` + `aicpa_foundational_competencies` + `cgma_competency_framework` all present; the SOX rejection is recorded in the file |
| 3b.5b | APQC hierarchy removed from ledgerx and adx | VERIFIED | Both overlays preserve the removal note in place, marked superseded by the 2026-08-26 correction below it |
| 3b.5c | O*NET adopted in the accounting overlay, 14/14, 3 unmapped | VERIFIED | 14 crosswalks; unmapped are `document_fact_reader`, `ledger_platform_specialist`, `posting_admission_agent` |
| 3b.5d | Discharged — APQC published the grant on page 2 | VERIFIED | `apqc_pcf` carries `reuse_licence`, `yes_with_conditions`, the mandatory paragraph verbatim, and the browser-reading provenance for 8.0 |
| 3b.5e | Briefs written; folder ruled to `research/` | VERIFIED | Three prompts in `research/`; the adx brief is in AdxFactory as the task says |
| 3b.5f | Last brief run; nothing adopted; registry untouched | **VERIFIED, WITH A DEFECT REPAIRED** | See §"3b.5f" |
| 3b.5g | opsx brief run; ITIL/SFIA/COBIT fail; NIST CSF registered but no function mapping | VERIFIED | Report present (117 lines); `nist_csf` registered public-domain; opsx overlay ships no NIST mapping |
| 3b.5h | codex brief run; SWEBOK/SFIA/12207 fail; Scrum declined | VERIFIED | Report present (76 lines); codex overlay ships one body |
| 3b.5i | medx brief run; register nothing; refusal recorded in data | VERIFIED | Report present (69 lines); registry unchanged across `761b3707` (43 before, 43 after); overlay records 11 refusals |
| 3b.5j | All five domains verified; narrowed twice | VERIFIED | Narrowings are recorded in 3b.5k (9 -> 8) and 3b.5l (8/9 -> 8/10) |
| 3b.5k | APQC verdict corrected; bar came off the wrong document | VERIFIED | Registry entry carries both provenances; 3b.5b preserved rather than rewritten |
| 3b.5l | IAB reuse test run; CC BY 3.0; steward corrected; id kept | VERIFIED | `iab` entry carries the corrected steward, the verbatim grant, `licence_page`, CC BY §4 conditions, and all five gaps (a)–(e); registry stays 44 — the id was not split |
| 4.1 | Opsx consumer follow-up | **TICKED THIS SWEEP** | See §"4.1 discharge" |
| 5.1 / 5.2 / 5.3 | Explicitly out of scope | UNTICKED BY PRECEDENT | See §"Section 5" |

**Ticks that could not be verified: none.** Every previously ticked box
reproduced against the artifacts. Four MINOR findings are recorded below;
none of them falsifies a tick.

## 3.0 discharge — the standing per-domain obligation

3.0 asks for the chosen bodies' **current terms and versions** verified
against each body's own publication before a crosswalk is committed. Ticked
2026-08-26 on this evidence:

| Domain | Bodies committed | Verification evidence | Result |
|---|---|---|---|
| opsx | `onet_it_occupations` | 3.0a + OpsxFactory `2d3e5ad` (on main) | 6/6 codes verbatim; version corrected 30.3 -> 31.0 |
| codex | `onet_engineering_occupations` | 3.0a + codexFactory `d5f5f3c` (on main) | 7/7 codes verbatim; same version correction |
| ledgerx | `onet_accounting_occupations`, `apqc_pcf`, `coso_icif` | 3.2 / PR #24 | O*NET pin + by-version attribution moved together; PCF pinned 8.0, licence page read; COSO unchanged |
| adx | `onet_marketing_occupations`, `apqc_pcf`, `iab` | 3.3 / PR #4 + PR #5 | O*NET codes read 2026-08-26 at 31.0, two title gaps re-tested rather than inherited; IAB versions read |
| medx | **none, by choice** | 3b.5i / MedxFactory `5d16ccc5` | Vacuous: an obligation over chosen bodies is discharged by choosing none |

Three residuals are carried into the tick note rather than hidden by it,
because this tick states what the verification RETURNED and two bodies came
back "unreachable, recorded as a gap" rather than "confirmed":

1. **PCF 8.0's numbering was not re-read** (ledgerx and adx). Element names,
   decimal numbers and five-digit IDs were text-extracted from the primary 7.4
   PDF because apqc.org answers HTTP 403 to automation and no 8.0 mirror is
   public. Both overlays state this in their own headers. 3b.3's failure mode
   is held at arm's length, not eliminated.
2. **Two of three IAB version dates are contested** between the steward's own
   surfaces; the registry records both readings and resolves neither.
3. **Task-level verification is OUTSTANDING and unclaimed** in all four
   crosswalking domains. Every mapping is occupation-level; only 11-3021.00
   and 27-3042.00 ever had task statements read verbatim, and no overlay
   asserts a task-statement match. 3.0 asked for terms and versions and got
   them; task statements are a further claim the family does not make.

## 3.5 discharge — Medx

`terminology` landed at MedxFactory `5d16ccc5` (on main, 2026-08-09), commit
subject "Add medx terminology: display labels only, and the provider-mapping
refusal in data". Recounted at main: 11 workers, 6 job_types, 9
stop_conditions, 7 routing classes — full coverage of every declared id —
with all eleven worker classes recording `no_clean_equivalent` against
`nucc_taxonomy`, each with a note. Zero mapped, by design.

That IS the population, per 3b.5i, and the box is ticked on that finding
rather than by re-arguing it. The refusal is written against the PROVIDER
taxonomy specifically because that is the mapping a contributor would reach
for and it is the dangerous one.

## 4.1 discharge — the named consumer

OpsxFactory PR #115, merged to main 2026-08-26 as `f1065cc`; change packet
`openspec/changes/render-domain-labels-in-refusals/` in that repo. Verified at
OpsxFactory main artifact by artifact:

- `workflows/business-central-administration.yaml` carries
  `workflow.adjudication` with the three flags true and the four-entry fixed
  `order` of `id` + `display_label` pairs.
- `scripts/business_central_administration.py` carries
  `ADJUDICATION_CHECK_LABELS`, `adjudication_check_label()` and
  `_adjudication_refusal()`, which composes "adjudication refused at the
  `<label>` check: `<detail>`" and attaches `check_id` to the raised error.
  An undeclared id raises rather than falling back to the id.
- All five adjudication negative fixtures assert the RENDERED LABEL.
- `test_refusal_renders_the_domain_label_and_never_the_check_id` asserts the
  id is ABSENT per check (`assertNotIn`), not merely demoted.
- `ADJUDICATION_ORDER` is byte-identical before and after — 5.1 held on the
  consumer surface too.

## 3b.5f — the one defect this sweep found in a ticked box

3b.5f was ticked CLOSED on 2026-08-26 after the ledgerx UN/CEFACT + BIAN
round ran. Its substantive claims all VERIFY: the report exists at
`research/ledgerx-international-process-bodies-research-report.md` (338
lines, `Status: record`), UN/CEFACT's five OWL finance classes and BIAN's 259
Apache-2.0 Service Domain specifications are both in it, fourteen of fourteen
workers record no counterpart against each body, and
`contracts/policies/standards-bodies.yaml` is genuinely untouched by that act.

**But the box contained two statements that were false when read as current
state**, both artifacts of the prepend-a-closing-note edit at `64e0badc`:

1. A **broken antecedent**. When ledgerx was appended to the five-brief list,
   the sentence after it — "Its findings landed in two places and neither is a
   report file: the crosswalks themselves went into AdxFactory
   `02d022cefb34`" — kept its wording. It was written about the ADX round;
   after the edit it read as though the LEDGERX round produced no report,
   contradicting the same task's own citation of that report.
2. A **stale tail**: "WHAT THIS TASK STILL OWES: the ledgerx UN/CEFACT + BIAN
   round, and only that. Its brief is written and has NEVER been run", plus
   the paragraph after it. That is the pre-run text, left unlabelled beneath a
   closing note that says the opposite.

**Repaired on this branch, not deleted.** The antecedent is corrected in place
with a note saying what was wrong and why; the stale tail is marked
SUPERSEDED under the append discipline the way 3.2 and 3.3 mark their own
original text, so the CLOSED note stays checkable against what was still owed
when it was written. This is exactly the class of defect the sweep exists to
catch: a ticked box asserting, in its own words, that its work had never been
done.

## Section 5 — treated by precedent

All three boxes stay UNTICKED, with a closing note. Precedent read rather than
assumed: `add-roster-device-admission-surface` archived with its out-of-scope
box unticked ("an unticked box here means 'owned elsewhere', and ticking it
would claim work this repository never did"), following
`refine-demote-round-trip-mechanics` §8 by ruling;
`sanction-ratified-record-spelling` §5.1 ticked its box only because a
separate decision was later taken and could be named. Neither pattern fits a
prohibition.

**5.1 and 5.2 were measured, not asserted.** Every population commit was
diffed on the identity surface — worker ids, archetypes, permissions,
credential requirements, rung ceilings, routing:

| Repo | Commit | Identity surface |
|---|---|---|
| LedgerxFactory | `ded4a0128f9e` | identical |
| AdxFactory | `02d022cefb34` | identical |
| AdxFactory | `1fc5a2f` (IAB promotion) | identical |
| OpsxFactory | `1b118c9` | identical |
| codexFactory | `54ccc9b` | identical |
| MedxFactory | `5d16ccc5` | identical |

Six of six. 5.2 also survived a swap that could have broken it: 3.1 records
the unmapped set MOVING when the body changed, which is a crosswalk behaving
descriptively rather than as an identity.

5.3's choosing did happen, five times, in each domain's own repo — which is
what "out of scope here" reserved. Recorded on the box.

## Overlay-manifest digest integrity

Every domain's `omnigent/overlay-manifest.yaml` was checked by recomputing
`sha256sum omnigent/domain-overlay.yaml` at that repo's main:

| Repo | Declared digest | Recomputed | Match |
|---|---|---|---|
| OpsxFactory | `f477c1ba…4805e` | `f477c1ba…4805e` | yes |
| codexFactory | `bd31dfac…679f2` | `bd31dfac…679f2` | yes |
| MedxFactory | `5823fa73…62fab` | `5823fa73…62fab` | yes |
| LedgerxFactory | `49c54a6b…51649` | `49c54a6b…51649` | yes |
| AdxFactory | `e1da57e9…c09df` | `e1da57e9…c09df` | yes |

Five of five. No overlay is shipping content its manifest does not pin.

## Registry arithmetic, recounted from git rather than trusted

| Commit | Task claiming it | Bodies |
|---|---|---|
| `df16f213` | 3b.1 ("all 17 registered bodies") | 17 |
| `8572d593` | 3b.4 ("registry now holds 30") | 30 |
| `db4de64d` | 3b.5a ("30 -> 41") | 41 |
| `109a120d` | 3b.5g (NIST CSF registered) | 42 |
| `a35dc517` | 3b.5h | 43 |
| `761b3707` | 3b.5i ("no crosswalk body registered") | 43 — unchanged, as claimed |
| `d7e4965b` | 3.3 prerequisite (`onet_marketing_occupations`) | 44 |
| `4044bd9f` | 3b.5l (`iab` corrected, id kept not split) | 44 — unchanged, as claimed |

Every claimed count is exact.

## MINOR findings — recorded, none blocking

1. **Two branch shas cited in ticks are stale-by-rebase.** 3.2 cites
   LedgerxFactory `ded4a0128f9e` and 3.3 cites AdxFactory `02d022cefb34`,
   both "unmerged as of this tick". Both PRs were merged with a rebase merge,
   so main carries `e0d1abeb` and `6543a14a` instead. Verified equivalent:
   **identical tree and identical parent** in both cases — only the commit
   object differs. The content claim is true; the sha citation no longer
   resolves on main. Recorded here rather than rewritten into the ticks,
   because the ticks are honest about the state at the moment they were
   written and this record is where the merge evidence belongs.
2. **`onet_marketing_occupations` carries seven codes, not the "six" 3.3's
   prerequisite note claims** — 11-2021.00, 13-1161.01, 13-1041.00,
   13-1041.07, 15-2051.00, 15-2051.01, 27-1011.00 (five parents, two detailed
   sub-occupations). Counting parents only gives five; counting all gives
   seven. Neither is six. No shipped mapping is affected: every code the adx
   overlay uses is on the entry.
3. **`nist_csf`'s `scope` names five CSF Functions** ("Identify / Protect /
   Detect / Respond / Recover") while 3b.5g records that the Function names
   could not be enumerated from a primary source. The two are reconcilable —
   the scope line is inherited 2026-08-09 seed text under the registry's own
   sourcing caveat, and 3b.5g's operative claim (no function-level mapping was
   authorised, and none shipped) is TRUE, verified in the opsx overlay. But
   CSF 2.0 has **six** Functions; Govern was added in 2.0, and the seed line
   predates the version pin sitting beside it. Unverified seed text, flagged.
4. **Four domain overlays cite this change by active path.** opsx and codex
   cite `research/...` AND pin a commit sha (`bf266c9486af`), so they survive
   the archive move. MedxFactory cites
   `.../add-omnigent-domain-terminology/supporting-docs/medx-clinical-bodies-research-report.md`,
   a path that has been wrong since the 2026-08-22 folder ruling moved these
   reports to `research/`; ledgerx and adx cite `.../tasks.md` unpinned. All
   three move again under `archive/` on this archive. Each is that domain's own
   act in its own repo; named rather than silently repaired across four
   repositories this change does not own.

## Archive gate

The proposal declares:

```
code_surface: openxFactory (contracts/omnigent/ schema + example + negative
              fixtures; scripts/validate-omnigent-contracts.py semantic checks)
target_release: implemented
```

So the **realization archive gate applies** — this is not a `code_surface:
none` doc-only change that archives on landing. The gate requires the code
merged on the implemented target through the owning domain's engineering
gates, and, the surface being runnable, a green run of it.

**MERGED ON THE IMPLEMENTED TARGET — yes.** Every code-surface commit is an
ancestor of `openxFactory` `origin/main`, each landed through a reviewed PR:
`df16f213` (schema, validator, example, fixtures, registry), `2c06ced4`
(legacy-vocabulary lint exemption for terminology keys), and the registry
sequence `ff059224`, `8572d593`, `db4de64d`, `109a120d`, `a35dc517`,
`761b3707`, `65b3348d`, `d7e4965b`, `062cb489`, `583eb247`, `4044bd9f`.

**GREEN RUN OF THE RUNNABLE SURFACE — yes.**
`python3 scripts/validate-omnigent-contracts.py` was run in this fresh clone
at main and exited 0: the positive examples validate, and all three
terminology negative fixtures are rejected for their declared reasons
(`terminology` orphan key, unresolved `standards-bodies.yaml` id,
`no_clean_equivalent` without a note) alongside the twelve pre-existing
fixtures. `openspec validate --all --strict` is green at 79/79.

**On CI, stated plainly rather than claimed as the evidence.** openxFactory's
`pytest-suite` runs on `main` are largely `cancelled` right now — the workflow
uses a concurrency group and main is advancing faster than a run completes;
PR #383's "fail" is that same cancellation ("Canceling since a higher priority
waiting request for pytest-suite-refs/heads/main exists") at 16% with zero
test failures, not a red merge. The last uncancelled main run is **green at
`583eb247`**, itself a code-surface commit of this change. The direct run of
the runnable surface above is the realization evidence; CI is recorded as
corroboration with its concurrency artifact named.

**No managed-subject deployment** is involved, so the correlation-identifier
clause does not apply. **Origin retention**: `.openspec.yaml` carries its
`ad_hoc` origin unchanged from creation — id, reason, `approved_by` (Brett,
2026-08-25, "admit the three remaining packets"), `approved_on`. **Proposal
support gate**: this change has no `supporting-docs/` folder; its research
lives in `research/` by the 2026-08-22 ruling recorded at 3b.5e, so the
support-bundle clause has nothing to bundle.

**GATE MET.** The change archives.

## Requirement-map diff (thin-delta check)

The delta carries **`## ADDED Requirements` only** — no `MODIFIED`, no
`REMOVED` — so the thin-delta hazard (a MODIFIED delta replacing a promoted
requirement block wholesale and silently dropping scenarios) has no surface
here. Verified by structure, then by content:

| Capability | Requirements before | Requirements after | Scenarios before | Scenarios after |
|---|---|---|---|---|
| `omnigent-domain-overlay` | 8 | 11 | 21 | 29 |

The three added requirements and their scenario counts:

- Domain-expert display terminology for declared vocabulary — 3 scenarios
- Human-facing surfaces render domain terminology — 2 scenarios
- Standards alignment is a descriptive crosswalk, never an identity or a
  claim — 3 scenarios

All eight pre-existing requirements were body-hashed before the archive and
re-hashed after: **8/8 unchanged, byte for byte**, and their 21 scenarios are
carried forward intact. No promoted requirement was restated, reworded or
re-scoped by this promotion; the archetype vocabulary, permission matrix,
credential tiers and authority-conservation rules are untouched, which is what
the proposal's Impact section promised.
