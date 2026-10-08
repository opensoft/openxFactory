# Proposal Ratification: realize-doc-health-direction-arc

Status: ratified
Kind: report
Decision date: 2026-10-06
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-10-06 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-4` (display `openXfactory-4-openDox_extraction`), by interactive
multi-choice, verbatim: *"Ratify it (Recommended)"*, given at about **18:59Z**
and recorded at `opensoft/openxFactory`
[#656](https://github.com/opensoft/openxFactory/issues/656) comment
[`6023375303`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-6023375303)
(created 2026-10-06T19:00:45Z).
Ratified baseline: the change as landed on `main` at **`fc4fa0ff`** (#1253,
T070b, merged 2026-10-06T18:56:42Z), after #1247 → `51456835` filed it.

## Decision

**RATIFY.** The change stands as it is at `fc4fa0ff`: `proposal.md`, `design.md`
(§ 11's D1–D7 included), `tasks.md` and `.openspec.yaml`, with `skip_specs: true`,
so there is no spec delta to ratify.

**This ratification authorizes realization; it does not perform it.** The ruling
record says what it authorizes: T072 starts now in openDox-code, and is
opportunistic under ARC-6, and T074 and T075 follow in plan order. Nothing is
promoted by it. The change declares no spec delta, and `code_surface:` is not
`none`, so under `release-realization` it archives only on merged, green
realization evidence (tasks 7.1–7.4).

**No code byte, pin, gitlink, contract bundle or release tag moves with this
record.**

## 1. The word, and exactly what it decided

> Ratify it (Recommended)

The ruling record in comment `6023375303` describes the question Brett Heap was
asked. It named the change and what it holds:

- the OpenSpec change `realize-doc-health-direction-arc`, on `main` as a draft;
- #1247 (T070, `51456835`) authored it, and #1253 (T070b, `fc4fa0ff`) folded in
  Copilot's four items, with Copilot recommending approval at #1253's final head;
- it writes up Brett's ARC-Q1–ARC-Q4 (a) (`6003918488`);
- the work it describes: openDox-code re-authors the generic `lines` slice
  (T072); openXdox-code declares four seams, moves its eight modules off
  openxFactory's `doc_health` and respells 7 tests (T074); openxFactory's host
  registers the seams (T075);
- the change itself contains no code;
- it stays active until that work is merged and green, and it holds up neither
  release 2 nor #1144's archive (ARC-Q3 (a)).

The option text read: *"I post your word on #656 and land the ratification record
(Status: ratified, Ratified by) under a Rule 6 window. T072 can start right away;
T074 and T075 then follow in order."*

The ruling record states what was done on the word:

1. **The `#656` half of T071** is that comment.
2. **This record** goes in one openxFactory PR under a Rule 6 window, in the form
   of #1144's own record (`cd494e4c`, #1151): the three lifecycle documents'
   `Status: ratified` and citation lines, the `.openspec.yaml` approval pair, and
   the README *Active changes* bullet.
3. **T072 starts now** in openDox-code. It is opportunistic (ARC-6): it rides
   T061's pin only if it has already landed.
4. **T074 and T075 follow in plan order.** T074 comes after T071, T072's pin,
   T021 and T073; T075 comes after T074 and T064.

## 2. The ratification read: D1–D7 stand as recommended

`tasks.md` 1.2 provides: *"The word rules `design.md` § 11's D1–D7 as recommended
unless it says otherwise; a different answer is encoded before 2.1 starts."* The
word does not say otherwise, so the seven decisions stand as recommended and
nothing is encoded before 2.1 starts:

| decision | stands as recommended |
| --- | --- |
| D1 | No openXdox-spec delta; `skip_specs: true` (§ 5) |
| D2 | Every seam is read at USE, never at import (§ 4.2) |
| D3 | An unregistered seam refuses by name (§ 4.2) |
| D4 | (a): a lone checkout's governed columns are keyed on the governed seams (§ 10) |
| D5 | The surfaces check over this change's own landings (§ 8) |
| D6 | The staged topic stays staged until T077, as this change's `staged` origin |
| D7 | The host fills openXdox's four seams as their own all-or-none group (§ 4.3) |

**What this read does not claim.** The ruling record describes the question
without itemizing D1–D7, and this record does not claim that Brett Heap was shown
them one by one. It applies 1.2's own rule, which the packet states and which the
word ratifies.

## 3. What the word authorizes, and what it does not

- **It authorizes** the realization the change describes, in plan 038's order.
  The ruling record names T072, T074 and T075. T076 (F9.2's re-run) and T077 (the
  archive) follow them in the plan's own order, T070 → T071 → T072 → T074 →
  T075 → T076 → T077, each under its own task's gates.
- **It performs nothing.** No realization, no archive, no promotion and no pin
  move happens by the word or by this record.
- **It moves no declaration.** `code_surface:`, `target_release: implemented` and
  `sequenced_after: []` stand as landed. The sweep-ledger row for the change
  (`state: active`, `moved_by: "#1247"`) does not move.
- **It gates nothing.** Not release 2's close, not T061's 0.2.0 bump (ARC-6) and
  not #1144's archive (ARC-Q3 (a)).

## 4. The change did not move between its landing and the word

`fc4fa0ff` merged at 18:56:42Z, and the word was given at about 18:59Z. The
change directory's tree at `fc4fa0ff` is `02d362f6ebcaf49e18aa107f7ce2b3a409ca2275`.
It is the same tree as at #1253's final head `e4f3f1db`, and as on `main`'s head
`a936e531`, the base of this record's commits. The last commit on `main` that
touches the directory is `fc4fa0ff`. The commits after it touched no byte of it:
#1252 → `c44c1610` (the archive of `add-factory-mcp-conformance`, 18:58:06Z),
#1254 → `a2dc658d`, #1138 → `9171d14a`, #1251 → `1837ea75`, #1250 → `3cec62fd`,
#1256 → `8c1eeae1`, #1255 → `0992369a`, #1257 → `c70bdbd9`, #1260 → `f335c077`,
#1258 → `16779816` (the archive of `add-worker-input-budget`), #1266 →
`a38585e9` and #1264 → `a936e531`.

The changes this record makes are the first after the landing, and **none of them
is requirement or scenario text**: the change has no spec delta.

- **`proposal.md`:**
  - `Status: ratified` with a `Ratified:` citation.
  - A qualifier above the filing's "DRAFT. FILING IS NOT RATIFYING" paragraph,
    which is kept verbatim as the filing's record.
  - A `## Ratification record` section.
  - A read-at-ratification note after the D1–D7 list.
- **`design.md` and `tasks.md`:** `Status: ratified` with a `Ratified by:`
  citation. `design.md` § 11 gains the same read-at-ratification note. `tasks.md`
  1.1 (the filing) and 1.2 (this act) are ticked, and 1.2 carries a marked note.
- **`.openspec.yaml`:** the approval pair `approved_by` / `approved_on` is ADDED
  after `proposed_on`, never substituted. `kind`, `id`, `path`, `reason`,
  `proposed_by` and `proposed_on` do not move.
- **This record.**
- **`README.md`:** the *Active changes* entry's status.

The citation split is the one #1144's record carried (`cd494e4c`): `Ratified:` on
`proposal.md`, and `Ratified by:` on `design.md` and `tasks.md`.

**The one divergence from the text as filed.** `tasks.md` 1.2 says this record
carries `Status: record`. It carries `Status: ratified` with a `Ratified:`
citation, as #1144's record did. `document-lifecycle` sanctions both spellings.
The option put to Brett Heap read "(Status: ratified, Ratified by)", and a
`Status: record` file trips `record-immutability` on any later edit. The holder
confirmed the form on `#656` (comment `6023619783`). 1.2 keeps its as-filed
wording and carries a marked note saying so, as #1151 did for its own 1.8.

## 5. What stood between the proposal and the word

- #1247 filed the change. Copilot's review `5427373153` at its head `2a79d329`
  named four items.
- #1253 folded the four in BEFORE the word, at the holder's ruling. At its first
  head `02e3d706`, Copilot's review `5432328728` recommended changes on two
  findings about item 4's protected-suite selector, both fixed in `15137889`. At
  its final head `e4f3f1db`, Copilot's review `5432608039` read "Approval
  recommended" with Findings: None, and both earlier threads were resolved.
- At `e4f3f1db` there are 18 check runs: 17 completed successfully, and Sourcery
  review was skipped.

This record freezes only the state the word was given over.

## 6. What was measured at this record's commit

The measurement was taken on the tree this record lands in: `main` at `a936e531`
plus this record's changes.

| gate | result |
| --- | --- |
| `OPENSPEC_TELEMETRY=0 openspec validate realize-doc-health-direction-arc --strict` (the pinned 1.12.0) | valid |
| `scripts/validate-openspec-cli-pin.py --all --strict` | exit 0, 0 UNDISPOSITIONED failures; 114 passed, 1 failed (115 items), the one being the accepted exception that `main` alone also reports |
| `scripts/validate-code-surface.py .` and `scripts/validate-target-release.py .` | passed |
| `scripts/validate-sequenced-after.py .` and `--ledger-diff` | passed; ledger consistent with the corpus (234 rows), and this change's row does not move |
| `scripts/proposal-support.py . verify realize-doc-health-direction-arc` | ok |
| `scripts/doc-health.py --single-repo .` | 31 critical, 26 error, 69 warning, 20 info; the report is byte-identical to `main` alone, run in the same clone kind with the submodules initialised in both, and 0 findings name this change |
| doc-health, the families `tasks.md` 1.2 names, on this tree | `proposal-origin` 0 findings and `status-validity` 0 findings; `record-immutability` (4 critical) and `ratified-provenance` (27 critical) name nothing of this change, and they are `main`'s own because the whole report is byte-identical to `main`'s. Negative control: dropping `proposal.md`'s `Ratified:` line takes `ratified-provenance` to 28 critical and names `proposal.md` |
| `pytest tests/ -m "not postgres" -k "ledger or records or sequenced or openspec"` | 615 passed, 3 skipped |
| `pytest` over `tests/sequenced_after`, `code_surface`, `target_release`, `proposal-support`, `scope_globs` and `packet_reference` | 866 passed, 311 subtests passed |
| `pytest tests/doc-health` | 2157 passed |

The running measurement lives in the pull request that carries this record.
