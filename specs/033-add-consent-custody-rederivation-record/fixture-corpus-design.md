# Fixture corpus design — 033-add-consent-custody-rederivation-record

**Status**: design only. Prepared 2026-09-09 while the consistency panel runs on
`489be604`. **NOTHING under `contracts/`, `scripts/` or `examples/` is touched
by this file** — it is the blueprint Phase D executes once the panel's verdict
is relayed.

## Measured starting corpus

`examples/consent-instrument/` holds **6** `*.example.yaml` (4 instruments, 1
class registry, 1 purpose model) and **7** `negative/*.yaml`. The validator's
own self-test note agrees: *"6 valid …, 7 negative …, 2 purpose probe(s)"*.

## Target corpus

| Bucket | Now | Added | After |
| --- | --- | --- | --- |
| `*.example.yaml` (positives) | 6 | **+3** | **9** (7 instruments, 1 registry, 1 purpose model) |
| `negative/*.yaml` | 7 | **+14** | **21** |
| `withheld/*.yaml` (NEW dir) | 0 | **+1** | **1** |
| purpose probes | 2 | 0 | 2 |

These are the counts T047, T048 and T049 must RE-MEASURE by listing the
directories — never copy from this table, which is a design intent and not a
measurement of what landed.

## Positives — three new files

| File | Task | Shape |
| --- | --- | --- |
| `consent-instrument-custody-chain-header-only.example.yaml` | T030 | TWO-entry unbroken chain, both entries `header_only` / `lifecycle_header_edit`, both locators equal to `custody.locator`, digests linking `pin → d1 → d2` |
| `consent-instrument-custody-archive-move.example.yaml` | T031 | ONE entry, `archive_move` / `path_only`. Locators DIFFER (live path → archive path); **both digests EQUAL**. This is the case a single-locator rule can never admit (design C-6a, `proposal.md` Example B) |
| `consent-instrument-custody-chain-two-entry.example.yaml` | T032 | The real repair's shape: e1 `archive_move`/`path_only` (locators differ, digests equal), e2 `lifecycle_header_edit`/`header_only` (both locators the archive path, digest moves). **CARRIES THE EQUAL-TIMESTAMP BOUNDARY**: `e1.at == e2.at`, admitted, because the requirement says the times *"do not decrease"* |

T033 adds no file: an EXISTING example is left byte-unchanged and re-validated,
proving the growth is additive for an instrument declaring no array.

**Every positive is a `xfactory_consent_instrument` in the packaged corpus's
existing domain**, so the packaged class registry and purpose model adjudicate
it without a new registry entry. Fixtures carry no credential, no tenant data
and no host-absolute path (Principle VII).

## Negatives — fourteen new files, one per named refusal

Named after the finding they provoke, matching the directory's existing
convention (`embedded-original-content.yaml`, `undeclared-lifecycle-skip.yaml`).

| # | File | Task | Code | Detail pin | Isolation: sound in everything except |
| --- | --- | --- | --- | --- | --- |
| 1 | `custody-chain-unanchored-digest.yaml` | T037 | `custody-chain-unanchored` | `previous_sha256` | the anchor's DIGEST half; locator anchors correctly |
| 2 | `custody-chain-unanchored-locator.yaml` | T037 | `custody-chain-unanchored` | `previous_locator` | the anchor's LOCATOR half; digest anchors correctly |
| 3 | `custody-chain-broken-link.yaml` | T034 | `custody-chain-broken-link` | — | the digest link; **locator pair sound** |
| 4 | `custody-chain-locator-gap.yaml` | T035 | `custody-chain-locator-gap` | — | the locator link; **digests link correctly** |
| 5 | `custody-chain-out-of-order.yaml` | T036 | `custody-chain-out-of-order` | — | the order; both digest and locator legs sound. `e2.at` strictly PRECEDES `e1.at` — equality is legal, so it must decrease |
| 6 | `custody-pin-rewritten.yaml` | T041 | `custody-pin-rewritten` | — | the pin. **MULTI-ENTRY**: `custody.sha256` advanced to `e1.observed_sha256` while `e2` still exists — FR-011's sharper *"while a LATER entry exists"* form |
| 7 | `custody-path-class-digests-differ.yaml` | T043 | `custody-path-class-digests-differ` | — | the class claim; chain otherwise anchors and links |
| 8 | `custody-diff-class-unknown.yaml` | T038 | `schema` | `custody_rederivations/0/diff_class` | the enum member |
| 9 | `custody-reason-unknown.yaml` | T038 | `schema` | `custody_rederivations/0/reason` | the enum member |
| 10 | `custody-entry-missing-ruling-ref.yaml` | T039 | `schema` | `'ruling_ref' is a required property` | the omission |
| 11 | `custody-entry-missing-recorded-by.yaml` | T039 | `schema` | `'recorded_by' is a required property` | the omission |
| 12 | `custody-entry-eleventh-property.yaml` | T040 | `schema` | `Additional properties are not allowed` | entry closure. An ELEVENTH property, since C-6a made TEN required — a "ninth" would not test closure |
| 13 | `custody-ruling-ref-blob.yaml` | T042 | `embedded-original-content` | `custody_rederivations[0].ruling_ref` | the blob shape; a 200+ char base64 run |
| 14 | `custody-recorded-by-blob.yaml` | T042 | `embedded-original-content` | `custody_rederivations[0].recorded_by` | the blob shape; a `data:` URI |

### The five `schema`-coded detail pins are MUTUALLY EXCLUSIVE, by construction

Rows 8–12 all fire `schema`, which is why the existing table's detail-pinning
rule applies (a code alone is too coarse: `schema` is satisfied by ANY schema
error). The chosen substrings cannot collide:

- rows 8 and 9 pin the jsonschema **instance path** (`…/diff_class`,
  `…/reason`), which appears in no other fixture's error text;
- rows 10 and 11 pin the **required-property message** naming a different field
  each;
- row 12 pins the **additionalProperties message**, which no other fixture
  provokes.

`self_test`'s check is `detail in line` over that fixture's own errors, so each
must appear in ITS fixture and the exclusivity guarantees none can satisfy
another's assertion. **Phase D verifies this by cross-checking each substring
against every other fixture's captured error text**, not by inspection.

## The third bucket — `examples/consent-instrument/withheld/`

| File | Task | Shape | Expected outcome |
| --- | --- | --- | --- |
| `custody-content-class-withheld.yaml` | T045 | Last entry declares `diff_class: content`; **every internal leg SOUND** — anchored to the pin in both halves, linked in both halves, non-decreasing `at`, closed enums, closed entry, pin unmoved | **`custody-content-class-withheld`** — not a pass, not an error |

### `EXPECTED_WITHHELD_OUTCOMES`, fail-closed both ways AND on the outcome

Mirrors `EXPECTED_NEGATIVE_FINDINGS`' discipline and adds the outcome check the
negatives already have as `negative-wrong-reason`:

| Failure mode | New self-test finding |
| --- | --- |
| fixture on disk, no table entry | `withheld-unregistered` |
| table entry, no fixture on disk | `withheld-missing` |
| fixture validates cleanly (no withholding) | `withheld-should-withhold` |
| fixture ERRORS instead of withholding | `withheld-wrong-outcome` |

**"The fixture exists" is not "the fixture withholds"** — that is the whole
reason the bucket needs its own outcome assertion.

## Exit-status expectations the corpus must satisfy

Brett Heap's ruling of 2026-09-09 — *"Exit 3 = needs a human decision
(Recommended)"* — plus the CONFIRMED precedence:

| Invocation | Exit |
| --- | --- |
| packaged self-test only (no path argument) | **0** — the withheld fixture is an EXPECTED withholding, exempt, exactly as a negative is an expected failure |
| a REAL instrument that withholds, nothing errors | **3** |
| a REAL instrument that withholds AND errors | **1** — errors dominate; a malformed record is not a decision for a human to take |
| findings, no withholding | **1** |
| harness/dependency failure | **2** |

## `examples/consent-instrument/README.md` growth (T047)

- **Layout tree**: complete over 9 positives, 21 negatives and the new
  `withheld/` directory, one annotated line each.
- **Schema → example map**: a **THIRD column** for the withheld bucket.
- **Named cases from the spec**: **nine new bullets** — one per REFUSAL code
  (the six that refuse, PLUS `embedded-original-content` under its newly
  extended reach), one positive chain-shapes bullet, one withheld bullet.
  `custody-content-class-withheld` is NOT counted among the seven; it has its
  own bullet, and counting it twice would leave a refusal unnamed.

## What this design does NOT settle

- **The identical-locators `path_only` gap.** A `path_only` entry whose two
  locators are EQUAL records an event that did not occur, and no fixture here
  provokes a refusal because **no refusal exists to provoke**. Ruled 2026-09-09:
  do not add the leg; record it as an OWED FINDING (T084, FR-048).
- **Any git-dependent leg.** Six of the ratified delta's 22 scenarios are the
  consumer's under § 7.1, and no fixture in this corpus can exercise them,
  because the neutral validator opens no repository.
