# Architect rulings at completion — mirror

Status: record
Lane: opsXfactory-1

**This is the Speckit-tree MIRROR of the block appended to**
`openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md`
(architect ruling 032-Q4: the evidence lives in BOTH trees). The packet-side
file is the one the change archives on; this copy is byte-equivalent in
substance so a reader of the feature tree needs no cross-repository hop.

## Architect rulings at completion — 2026-09-09T18:28Z

The orchestrator reported three items to the architect seat (lane
`opsXfactory-1`, the main session) at the end of realization. Two were DECLARED
DEVIATIONS put up for ruling rather than taken silently; both are **ACCEPTED**,
and the third is confirmed as recorded rather than acted on. Recorded here so
the acceptances are part of the packet's evidence and not only of a session.

**1. Phases C, D and E ride ONE commit (`f420cd50`) — ACCEPTED.** The reason is
the invariant, not convenience: **box 3.3 asks for a TEST that pins an absence**
(*"A test pins that absence so a helpful later edit fails on the developer's
machine first"*), so `tests/consent_instruments/` IS box 3.3's evidence and its
tick cannot precede it. Splitting the phases across commits would have broken
tick-rides-its-evidence (FR-041, architect ruling 032-Q5). **The invariant
outranks the phase boundary**, and the phase boundary is a `plan.md` sequencing
aid that `tasks.md` never states as a commit rule — `tasks.md` prescribes "one
commit" only for § 2 and for the § 5 candidate. Each phase still filed its own
raw transcript (FR-042b).

**2. The cut-coupled `contracts/README.md` consent-row amendment — ACCEPTED.**
The row now reads *amended at `contract-v1.33` (1 → 2) and again at
`contract-v3.5` (2 → 3, additive)*. **No ratified task names this edit**; it is
DERIVED from T061a's measurement and declared as such. `git show --stat 807a4f47`
— the `contract-v3.4` cut — moved SIX files, `contracts/README.md` among them,
and its two lines there were REGISTRATION-STATE rows for the family that cut
published. This cut's registration state also moves, so the same slot takes the
same kind of note. **It is admitted in the same class as the cut-coupled tests
(panel F1): a declared, attributed, measured cut-coupled act — not invented
scope.**

**3. The carried findings stay RECORDED, NOT ARMED — confirmed.** The task 3.2
paraphrase defect (the delta governs; the leg is anchor-relative; no ratified
text was altered), the identical-locators `path_only` gap (owed to F.2 or a
successor; **no refusal leg added here**), and clarify A2's REPORT → REFUSAL
conversion (which needs F.2's gate, and that gate is OpsxFactory's) all stay as
written. Nothing is built, scheduled or armed by this realization.

### The full-suite baseline, stated once and plainly

`python3 -m pytest tests/ -q -m "not postgres"` at the candidate `d54d89ca`:
**1 failed, 10662 passed, 36 skipped, 338 deselected**, rc=1. Re-run at the
Phase H head: identical counts.

- The single failure is
  `tests/ideation-dashboard/test_snapshot.py::test_find_validator_locates_pinned_checkout`.
  It resolves a **pinned checkout that exists only in an aggregation workspace
  layout**, which a linked worktree is not.
- It is **PROVEN PRE-EXISTING by a baseline, not by assertion**: the same node id
  fails identically in a SEPARATE CLONE at pristine `main` **`e86eca35`**,
  carrying none of this branch's bytes.
- The second failure seen in the Phase E run — a **30-second subprocess-ceiling
  flake** on a loaded workstation
  (`test_release_mode_field_is_preserved_on_the_real_repository`) — **PASSED on
  re-run**, which is why it was baselined rather than chased.
- **ZERO failures name a consent surface**: none under
  `tests/consent_instruments/`, none touching `examples/consent-instrument/`,
  `scripts/validate-consent-instruments.py`,
  `contracts/schemas/consent-instrument.schema.yaml` or `contracts/manifest.yaml`.
- **THE `openXwallet` GITLINK MUST BE INITIALIZED, AS CI DOES IT.** Without
  `git submodule update --init openXwallet` this gate reports **96 failed and 50
  errors** that are entirely the submodule's absence —
  `tests/clearing/conftest.py` REFUSES rather than degrading to a skip, and
  `tests/trust-anchor/`, `tests/openxwallet_pin/` and
  `tests/signed_execution_chain/` read the same gitlink. CI initializes it in a
  dedicated App-token step before the suite because openXwallet is a second,
  private org repository. Anyone re-running this gate must do the same, or read
  146 findings that say nothing about the code.
