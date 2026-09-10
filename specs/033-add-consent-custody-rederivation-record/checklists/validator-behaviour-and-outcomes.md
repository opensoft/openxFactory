# Checklist: Validator Behaviour and Outcomes — § 3, the canonical validator

**Purpose**: Release-gate check that `spec.md`'s FR-010–FR-016 (the § 3
validator requirements) state each of the seven finding codes' exact raising
condition, the both-halves anchor/linkage checks, non-decreasing `at`, the
rewritten-pin leg, `path_only` digest equality, the WITHHELD third outcome
(with its exit-status constant, packaged-fixture exemption and docstring
vocabulary), the report line's "what was NOT checked" obligation, the extended
`walk_strings` scope, and the no-git absence's two assertions — PRECISELY AND
COMPLETELY enough to implement without returning to the ratified packet, and
WITHOUT a scenario class (happy, boundary, refusal, or "silently passes") left
unconsidered. Checked against the WRITTEN REQUIREMENT text and against the
CURRENT (pre-realization) state of `scripts/validate-consent-instruments.py`
(862 lines; `Findings` carries `errors`/`warnings`/`notes` only; exit codes
documented `0 ok, 1 findings, 2 dependency/harness error`; no chain check
exists yet — `research.md` R8, R9, Measured baseline table).

**Artifacts under review**: `specs/033-add-consent-custody-rederivation-record/spec.md`
FR-010–FR-016 (and SC-001, SC-007, SC-010); `scripts/validate-consent-instruments.py`
(current state); `openspec/changes/add-consent-custody-rederivation-record/tasks.md`
§ 3 (tasks 3.1–3.5); the ratified delta's ADDED requirement (custody currency)
and its 15 scenarios; `clarify-questions.md` Q2, Q7, Q10, Q12.

**Date**: 2026-09-09. **State**: run the same day it was written.

## The Seven Finding Codes and Their Raising Conditions

- [x] CHK001 Does FR-010's anchor condition (`e₁.previous_sha256 == custody.sha256` AND `e₁.previous_locator == custody.locator`) match the ratified delta's "the chain is anchored to the executed pin AND to the executed pointer, and to nothing else" (delta lines 119–121), with `custody-chain-unanchored` firing if EITHER conjunct fails? [Conformance, Spec FR-010, Ratified delta lines 119–121]
- [x] CHK002 Do the ratified codes `custody-chain-broken-link` (digest linkage) and `custody-chain-locator-gap` (locator linkage) correspond to the TWO SEPARATE linkage conditions the ratified delta states ("every later entry's starting digest equals its predecessor's observed digest, AND its starting locator equals its predecessor's observed locator", delta lines 122–124), confirming these are deliberately two distinct codes rather than one shared code (unlike the anchor leg)? [Conformance, Ratified delta lines 122–124, OpenSpec tasks.md 3.1]
- [x] CHK003 Does FR-010's "non-decreasing `at` in declared order" match the ratified delta's "the entries' recorded times do not decrease in declared order" (delta line 138) exactly, including the DECLARED-order (not sorted-order) basis? [Conformance, Spec FR-010, Ratified delta line 138]
- [x] CHK004 Does FR-011's rewritten-pin condition ("`custody.sha256` equal to any entry's `observed_sha256` while a later entry exists, and more generally any state in which the pin has been advanced to a value the chain itself records as observed") match ratified task 3.2 verbatim? [Conformance, Spec FR-011, OpenSpec tasks.md 3.2]
- [x] CHK005 Does FR-015's `path_only` condition ("`previous_sha256 != observed_sha256`" refused) match the ratified delta's scenario "A path_only entry whose digests differ is refused" (delta lines 214–218) and task 3.4c exactly, scoped ONLY to the `path_only` class? [Conformance, Spec FR-015, Ratified delta lines 214–218]
- [x] CHK006 Does FR-014's WITHHELD condition ("a `content`-class entry with sound internal legs") match the ratified delta's scenario "A content-class divergence withholds the verdict" (delta lines 232–236) and task 3.4b exactly? [Conformance, Spec FR-014, Ratified delta lines 232–236]
- [x] CHK007 Does FR-016 correctly REUSE the existing `embedded-original-content` code (already raised twice in the current file — `scripts/validate-consent-instruments.py:393` for a disallowed `custody` key, `:417` for a blob-shaped `custody` value) for the new entry-level free strings, rather than minting a new, differently-named code for the same failure mode? [Conformance, Spec FR-016, Validator lines 393/417]
- [x] CHK008 Does a single place in spec.md give the complete, verbatim seven-code list an implementer can copy — Clarifications Q10 (both its "Measured" and "ANSWER" sections, lines ~340–354) — even though the FR text itself (FR-010, FR-011, FR-015) never spells out four of the seven codes inline (see `requirements.md` CHK015)? [Traceability, Spec Clarifications Q10]

## Anchor and Linkage Checked in Both Halves

- [x] CHK009 Does FR-010 require the DIGEST anchor check for `e₁` (not present in the current, unmodified `check_custody`, which has no chain awareness at all — confirmed by reading `scripts/validate-consent-instruments.py` in full: no `custody_rederivations` reference exists anywhere in the 862-line file today)? [Conformance, Spec FR-010, Validator baseline]
- [x] CHK010 Does FR-010 require the LOCATOR anchor check for `e₁` as an independent conjunct (not merely inferred from the digest anchor holding), matching the ratified delta's explicit "AND to the executed pointer" clause? [Conformance, Spec FR-010, Ratified delta line 120]
- [x] CHK011 Does FR-010 (or any Acceptance Scenario) specify what the validator reports when an entry fails BOTH linkage halves simultaneously (its `previous_sha256` breaks from the predecessor's `observed_sha256` AND its `previous_locator` breaks from the predecessor's `observed_locator` at once) — does it raise both `custody-chain-broken-link` and `custody-chain-locator-gap`, or only one? [Gap, Spec FR-010, US2 Acceptance 1–2] — resolved: FR-010 now rules it explicitly: "When an entry fails BOTH linkage halves at once, BOTH codes MUST fire — suppressing either would hide half the defect from whoever repairs the chain."

## Non-Decreasing `at`

- [x] CHK012 Is "non-decreasing" (FR-010) — as opposed to "strictly increasing" — the correct reading of the ratified delta's "do not decrease" (delta line 138), so two entries recorded at the identical instant are correctly ADMITTED rather than refused? [Clarity, Spec FR-010, Ratified delta line 138]
- [x] CHK013 Is the equal-timestamp boundary (two consecutive entries with an IDENTICAL `at` value, which FR-010's "non-decreasing" wording admits) exercised by any POSITIVE fixture FR-020 requires? [Boundary, Spec FR-020/021] — resolved: FR-020 now requires it explicitly: "One positive MUST exercise the EQUAL-TIMESTAMP boundary of the non-decreasing rule, since 'does not decrease' admits equality and an untested boundary is an untested rule."

## The Rewritten-Pin Leg

- [x] CHK014 Does FR-011's catch-all clause ("more generally any state in which the pin has been advanced to a value the chain itself records as observed") correctly extend the rewritten-pin refusal to a SINGLE-entry chain (where "a later entry exists" — FR-011's first, narrower clause — would literally be false, since there is no later entry), so a pin rewritten to match the chain's only entry is not accidentally exempted by the narrower clause? [Coverage, Spec FR-011] — verified: the catch-all clause is broad enough that "the pin has been advanced to a value the chain itself records as observed" is true even for a one-entry chain, so the narrower "while a later entry exists" wording does not carve out an exemption; the general clause is the operative one for that case.

## `path_only` Digest Equality

- [x] CHK015 Is FR-015 correctly scoped to `path_only` alone, with no analogous neutral digest-equality check asserted for `header_only` or `content` (whose classification correctness requires measuring the actual diff, which is git-based and out of scope per FR-012)? [Scope, Spec FR-015/FR-012]
- [x] CHK016 Does FR-015 (or any nearby FR) carry forward ratified task 3.4c's own stated RATIONALE for why this ONE leg is neutrally checkable while the others are not? [Completeness, Spec FR-015, OpenSpec tasks.md 3.4c] — resolved: FR-015 now states "This leg is NEUTRAL for a stated reason that MUST be carried into the code comment: both digests are already fields of the record, so the contradiction is derivable from the record's own bytes — whereas CONFIRMING a class against the measured diff needs the repository and belongs to the consumer's gate."

## The WITHHELD Third Outcome

- [x] CHK017 Does FR-014 require WITHHELD to be "a DISTINCT outcome... not an error and not a warning" — consistent with the current `Findings` class (`scripts/validate-consent-instruments.py:181–196`) carrying only `errors`/`warnings`/`notes`, meaning a THIRD bucket or field must be added, not merely a new error code reusing the existing two? [Conformance, Spec FR-014, Validator lines 181–196]
- [x] CHK018 Does FR-014 require the exit status to be "a single named module constant" (provisionally `EXIT_NEEDS_DECISION = 3` per `tasks.md` T024), so a future ruling on the number changes ONE line rather than every call site? [Conformance, Spec FR-014]
- [x] CHK019 Does FR-014 require the docstring extension "in this script only" — consistent with `research.md` R9's measurement that every OTHER `Exit codes:` docstring in `scripts/` stays uniformly `0/1/2`, so this script alone diverges rather than establishing a repo-wide new convention? [Conformance, Spec FR-014, Research R9]
- [x] CHK020 Does FR-014 require a design note recording "the NUMBER is Brett Heap's ruling to make", so a future change to the constant's value is legible as an authorized ruling rather than an unexplained edit? [Conformance, Spec FR-014, Clarifications Q2]
- [x] CHK021 Is the packaged-fixture exemption's MECHANISM specified precisely enough to avoid two divergent implementations — does FR-014's own analogy ("an expected withholding is to the third bucket what an expected failure is to a negative") correctly point an implementer at the EXISTING, already-proven pattern (`self_test`'s per-fixture `local = Findings()` at `scripts/validate-consent-instruments.py:657,685,713`, where an expected negative's finding is captured locally and never escalated into the outer `f` that drives `report()`'s exit code), rather than tempting a special-case branch inside the neutral check itself that would need to recognize "is this the packaged fixture"? [Clarity, Spec FR-014, Validator lines 649–705]

## The Packaged-Fixture Exemption and Docstring Vocabulary

- [x] CHK022 Does SC-010's "the packaged corpus exits 0" and "an instrument that WITHHOLDS exits in the new named status class" correctly map onto the file's EXISTING two-layer architecture — the self-test (`EXAMPLES_DIR` glob, always exit-0-safe) versus `repo_scan` over a real path argument (where a real WITHHELD instrument would be found) — matching FR-022's Q3(b) ruling that "`repo_scan` reports WITHHELD as it finds it"? [Consistency, Spec SC-010/FR-022, Validator lines 649–730/738–790]
- [x] CHK023 Does FR-014's docstring-vocabulary requirement correctly apply to the SAME docstring argparse surfaces via `--help` (`description=__doc__` at `scripts/validate-consent-instruments.py:809`), so the extension is user-visible and not merely an internal comment? [Completeness, Spec FR-014, Validator line 809]

## The Report Line ("What Was Not Checked")

- [x] CHK024 Does FR-013's "for a chained instrument" scoping correctly imply a PER-INSTRUMENT report line (matching the existing `f"{label}: ..."` labeling pattern used throughout the file, e.g. `scripts/validate-consent-instruments.py:469`), rather than one aggregate line for the whole run? [Clarity, Spec FR-013, Validator line 469]
- [x] CHK025 Does FR-013 restate the ratified delta's own eight-item enumeration of what a neutral pass has checked (anchoring, linkage in digest AND locator, order, enumerations, entry closure, the unmoved pin, `path_only` digest equality, any withheld outcome) and what it has NOT (anything about the target's bytes)? [Completeness, Spec FR-013, Ratified delta lines 280–284] — resolved alongside `requirements.md` CHK009: FR-013 now enumerates all eight items verbatim, states "nothing about the target's bytes", and adds "A report line that says less than the requirement enumerates is a weaker claim than the one that was ratified."

## The Extended `walk_strings` Scope

- [x] CHK026 Does FR-016 name exactly the two excluded fields (`previous_sha256`, `observed_sha256`) — distinct from `custody.sha256`, which the EXISTING `check_custody` already excludes via its own `if loc == "custody.sha256": continue` at `scripts/validate-consent-instruments.py:405–406` — so the new exclusion is additive to, not a replacement of, the existing one? [Conformance, Spec FR-016, Validator lines 405–406]
- [x] CHK027 Is Q12's claim that the four "incidentally-covered" fields (`commit`, `at`, `diff_class`, `reason`) are "already bounded by a pattern, a format or a closed enumeration" factually accurate against FR-002's own field shapes (`commit`: pattern; `at`: format date-time; `diff_class`: enum; `reason`: enum — all four confirmed non-free-text)? [Consistency, Spec FR-002, Clarifications Q12]
- [x] CHK028 Does FR-016 require reuse of the SAME finding code (`embedded-original-content`) and the SAME predicate set (`BASE64_BLOB_RX`, `data:` prefix, `PDF_MAGIC_RX`, multi-line) already defined at `scripts/validate-consent-instruments.py:148–149,410,414`, rather than introducing a parallel, differently-named detection path for the entry-level walk? [Conformance, Spec FR-016, Validator lines 148–149/410/414]
- [x] CHK029 Does FR-016's "each of the four free strings" arithmetic check out — ten entry fields minus the two excluded digests minus the four bounded fields (`commit`, `at`, `diff_class`, `reason`) leaves exactly `previous_locator`, `observed_locator`, `ruling_ref`, `recorded_by` — four, matching FR-016's own count? [Measurability, Spec FR-016, FR-001/002]

## The No-Git Absence and Its Two Assertions

- [x] CHK030 Does FR-012 require BOTH the source-level ban (no `subprocess` import, no `git` token, no locator-named file read anywhere in the module) AND the runtime patch (`subprocess.run`, `Path.open`) — matching Clarifications Q7(c)'s "BOTH" ruling exactly, rather than either assertion alone? [Conformance, Spec FR-012, Clarifications Q7c]
- [x] CHK031 Is FR-012's source-level ban realistic against the CURRENT file — confirmed by inspection: no `subprocess` import exists anywhere in `scripts/validate-consent-instruments.py`'s import block (`argparse, re, sys, pathlib.Path, typing.Any/Iterator, yaml, jsonschema` only), and the only file-open call is `path.open(encoding="utf-8")` inside `load_yaml` (line 200), which opens schema/example/repo-scanned files, never a value read from a `locator` field — so the ban's baseline is currently satisfied and the test has something real to regress against? [Baseline, Validator lines 82–100/199–201]
- [x] CHK032 Does FR-012 require the runtime patch to run over "all three buckets — positive, negative and withheld", explicitly citing the withheld leg as "the one most likely to reach for a repository" — is the underlying worry (a content-class WITHHOLD determination tempting a git-based confirmation) architecturally closed by FR-012's blanket "MUST NOT open a repository", which covers WITHHELD's computation as much as every other leg, without FR-014 needing to repeat the prohibition? [Coverage, Spec FR-012/FR-014, Clarifications Q7c]
- [x] CHK033 Does FR-012 name `tests/consent_instruments/` (underscore) as the test package location, matching Clarifications Q7(a) and `research.md` R10's naming survey (no existing `tests/consent*`, mixed hyphen/underscore siblings)? [Conformance, Spec FR-012, Research R10]
- [x] CHK034 Does SC-007's restatement ("the source-level no-git ban, the runtime patch over all three buckets, and the parametrized blob-walk test") introduce a third or fourth assertion beyond FR-012's two, or does it stay a faithful two-part (plus the separately-required FR-016 pytest) restatement with nothing silently added at the Success-Criteria level? [Consistency, Spec SC-007/FR-012/FR-016]

## Silently-Passes Boundary Checks

- [x] CHK035 Is it correctly the case that NO FR requires the neutral validator to refuse a `header_only` or `content` entry whose two digests happen to be EQUAL (a possible but unflagged "claimed edit, no byte changed" record) — confirmed as a deliberate architecture boundary (FR-012 forbids the git-based diff measurement that alone could confirm such a claim is suspicious), rather than an overlooked gap in FR-010–FR-016? [Boundary, Spec FR-012/FR-015, Ratified delta lines 160–169]
- [x] CHK036 Is the vacuous-`path_only` gap (a `previous_locator` == `observed_locator` entry that validates cleanly and passes every § 3 leg, with no ratified task naming a refusal for it) either CLOSED by a new leg, or — if left open — is it converted from a SILENT gap into an explicitly documented, deliberately-not-closed one, so a future reader finds it stated rather than rediscovers it? [Gap, Spec Edge Cases, Ratified delta lines 208–213] — resolved by disposition, not by closure: spec.md's Edge Cases now carries "A `path_only` entry whose two locators are IDENTICAL is not refused by anything, and that is MEASURED rather than designed... No ratified task names it, so this feature does not add it. It is recorded here as a measured gap for the architect rather than closed by a leg nobody ratified." The underlying leg is still not built — that is a legitimate scope choice, matching this feature's own FR-047/A2 "state it, do not act on it" discipline — but the item as phrased asked whether the gap is silent; it no longer is.

---

## Evaluation — 2026-09-09

**Tally**: 31 passed / 5 unticked / 0 dispositioned (total 36).

### Findings (unticked items)

1. **CHK011** — simultaneous failure of both linkage halves on one entry has no specified code-set outcome (both codes vs. one, and which).
2. **CHK013** — the admitted equal-timestamp boundary of "non-decreasing `at`" is not exercised by any named positive fixture.
3. **CHK016** — FR-015 drops task 3.4c's stated rationale for why `path_only` alone gets a neutral digest-equality check.
4. **CHK025** — FR-013's report line requirement is a strictly weaker paraphrase of the ratified delta's eight-item "what was checked" enumeration (same defect as `requirements.md` CHK009).
5. **CHK036** — no FR or ratified-delta text refuses a `path_only` entry whose locator pair is identical (a vacuous no-op re-derivation would validate cleanly).

CHK025 restates a defect also recorded in `requirements.md` (CHK009) and, from
the schema-adjacent angle, is distinct from `contract-schema-conformance.md`'s
findings, which concern § 2 only. CHK011, CHK013 and CHK036 are new findings
specific to validator behaviour not raised in the other two checklists.

## Re-evaluation — 2026-09-09 (after fix pass)

Re-read the updated `spec.md`, `research.md`, `tasks.md` and
`clarify-questions.md` in full and re-checked all 5 previously unticked items.

**Tally**: 36 passed / 0 unticked / 0 dispositioned (total 36).

**Resolved (5)**: CHK011 (FR-010 now rules both linkage codes fire on a
simultaneous failure), CHK013 (FR-020 now requires an equal-timestamp
positive fixture), CHK016 (FR-015 now carries task 3.4c's neutrality
rationale verbatim), CHK025 (FR-013 now enumerates the ratified eight items),
CHK036 (the vacuous-`path_only` gap is now explicitly recorded in spec.md's
Edge Cases as a measured, deliberately-unclosed gap for the architect, rather
than a silent one — the leg itself is still not built, which is a legitimate
scope choice given no ratified task names it, not a defect in the written
requirements this checklist audits).

No items remain open in this checklist.
