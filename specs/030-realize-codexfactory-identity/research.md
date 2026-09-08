# Phase 0 research: readings taken where the ratified packet is silent

**Feature**: `030-realize-codexfactory-repository-identity` | **Date**: 2026-09-08
**Head measured**: `e8021fed` (openxFactory `main` at branch point)
**Lane**: `provenance-autonomous-merge`

Every entry below is a reading this feature took because the ratified text does
not settle it. Each carries the source that constrains it. **Where the ratified
text does settle something, it is not restated here.**

---

## R-1 — The transfer has not happened, and the runbook puts this whole feature after it

**Decision**: author every rename now; land only what is true before the
transfer; hold the rest as draft pull requests naming the runbook step at which
each lands.

**Rationale**: `~/session-prompts/runbook-codexfactory-org-transfer.md` orders
the ceremony Phase 0 → Phase 10 and puts **step 10.2 — *"LANE. Realize the
change: the mapping row, the recorded sweep, the 123 renames across 60 files,
the origin-identity re-issuance, the freeze verification and the bundle cut"* —
LAST**, after the Phase 1 transfer. So the packet's own operational ordering
already answers "when do the renames land": after the move. This feature was
launched early on the convener's word, which creates a state the packet does not
describe — realization authorized, transfer unperformed. Measured, not assumed:
`gh api repos/codeXfactory/codexFactory` has no repository at this head, and
`gh api repos/opensoft/codexFactory` does.

GitHub redirects OLD→NEW after a transfer and never NEW→OLD before it, so a
reference respelled early has no grace period at all — the opposite of the
grace the packet's § Why discusses.

**Alternatives considered**:
- *Land all 124 renames now.* Rejected: reds `pytest-suite` and
  `merge-master-approval`, both required checks, on every openxFactory pull
  request; refuses today's real codexFactory clearing dispatches; and publishes
  citation URLs that 404.
- *Land nothing and only write the evidence.* Rejected: it spends the transfer
  window writing diffs instead of merging reviewed ones, which is the cost the
  ceremony's Phase 3 gates already make expensive.

---

## R-2 — The safe-now test, and why it admits only eight occurrences

**Decision**: an occurrence is SAFE NOW iff respelling it (1) states nothing
false about the present and (2) breaks no resolution that works today. Only
synthetic example and negative-fixture `repository:` values pass both.

**Rationale**: the packet's arbitration question (*does this string assert what
IS, or record what WAS READ?*) decides RENAME vs FROZEN. It does not decide
WHEN a rename lands, because the exemplar it follows
(`adopt-medxsoft-repository-identity`) was written **after** its transfer had
already happened on 2026-08-26. This feature needs a second question and states
it rather than deciding case by case.

The eight that pass: `contracts/omnigent/examples/` (6 files) and
`contracts/hermes-domain-overlay/examples/` (2 files). Their `repository:` is
illustrative data in an `.example.yaml` instantiation stub or in a negative
fixture whose only contract is *"produce exactly this finding and no other"* —
constitution principle IV holds these are never live configuration. Verified:
**none of the eight is a member of `contracts/releases/contract-v3.4.digests.yaml`**
(283 entries), so moving them alone triggers no `release-inventory-drift`
finding and no red `verify-commit`.

**Alternatives considered**:
- *Also land the regression denominator now.* Rejected: it carries the real
  engineering domain's canonical key with a real `commit` and `stack_digest`,
  and packet task 3.2 ties the resolver-key migration to *"the next bundle
  forward"*. It is also 1 of the 8 inventoried members (below).
- *Also land the prose documents now.* Rejected: `docs/architecture.md:25` and
  `README.md:316`/`:409` assert where engineering content lives **at present
  tense** — `"Engineering-domain implementation docs now belong in …"`. Made to
  read `codeXfactory/codexFactory` today, they state a falsehood about a
  repository that does not exist.

---

## R-3 — The eight inventoried members move in ONE slice

**Decision**: `domain-regression-inventory.yaml`, its three negative fixtures,
`contracts/hermes-runtime/README.md`, `docs/contract-versioning-policy.md`,
`docs/terminology-and-repo-topology.md` and `docs/xfactory-domain-factory-model.md`
land together, with `tests/hermes_runtime_contracts/test_domain_regression.py`,
in one gated slice — and the bundle cut follows it immediately on `main`.

**Rationale**: re-verified at this head against
`contracts/releases/contract-v3.4.digests.yaml`: all eight are present, and
**none of the other 52 renamed files is**, so `design.md` § 5's arithmetic holds
unchanged. None is in `scripts/doc_health/release_inventory.py`'s three-path
`EDITORIAL` set, so each moved blob is an `ERROR`-severity
`release-inventory-drift` finding and a red `verify-commit` until the cut
re-baselines the inventory. Splitting the eight puts a subset of that transient
on `main` with **no cut available to repair it**, because a cut needs all eight.

**Alternatives considered**: *move the four fixtures with the safe-now slice and
the four documents later.* Rejected for exactly the reason above; the transient
the packet predicts is bounded only if the eight are one slice.

---

## R-4 — The denominator's new sorted position, derived at this head

**Decision**: the codex entry moves from position **5 of 5** to position
**1 of 5** — FIRST.

**Rationale**: derived, not copied, as packet task 3.1 requires. The list at
this head is bytewise sorted by repository:

```text
1  opensoft/AdxFactory        (line 5)
2  opensoft/LedgerxFactory    (line 13)
3  opensoft/MedxFactory       (line 21)
4  opensoft/OpsxFactory       (line 29)
5  opensoft/codexFactory      (line 37)   <- moves
   opensoft/LegalxFactory     (line 46)   <- EXCLUSION row, a separate list, untouched
```

`c` is `0x63` and `o` is `0x6F`, so `codeXfactory/…` sorts before every
`opensoft/…` entry. `adopt-medxsoft-repository-identity` has **not** landed
(`MedxSoft/MedxFactory`, `M` = `0x4D`, would take first place), so the packet's
"SECOND if the exemplar has landed" branch does not fire and the entry goes
FIRST. `PINNED_TABLE` in `tests/hermes_runtime_contracts/test_domain_regression.py`
(line 53 onward) is reordered identically in the same commit; its
`sorted(..., key=lambda value: value.encode("utf-8"))` assertion and the
value-for-value `zip` against `entries` in document order are what make a split
commit red by construction.

---

## R-5 — `contracts/policies/repository-identity.yaml` does not exist: BLOCKER

**Decision**: prepare the mapping row's exact text as
[contracts/repository-identity-row.md](./contracts/repository-identity-row.md)
and do **not** create the file. Group 1 is blocked and the blocker is escalated
rather than worked around.

**Rationale**: measured — `git ls-tree origin/main -- contracts/policies/repository-identity.yaml`
returns nothing. Packet task 1.1 says in as many words *"Do not create the file
here"*, because `adopt-medxsoft-repository-identity` authors it at ITS task 1.1
and registers it in `contracts/manifest.yaml` at its task 1.3; *"authoring it
twice would produce two files claiming to be the mapping."* That change is
active on `main`, `Status: draft`, and **unrealized** — no Speckit feature under
`specs/` realizes it. Packet task 0.2's conditional fires only if the exemplar is
*"archived or withdrawn"*; it is neither, so the premise holds and the
instruction stands.

**Alternatives considered**:
- *Author the file here anyway.* Rejected: it is the one thing task 1.1
  forbids, and `contracts/manifest.yaml` registration belongs to the exemplar's
  task 1.3, so a file authored here would be an unregistered contract — a
  principle IV defect on top of a task violation.
- *Stack this feature's branch on an unmerged medxsoft realization branch.*
  Rejected: no such branch exists.

**Escalated**: recorded on codexFactory issue #279 and in this feature's
tasks.md; the convener's options are to realize the exemplar's group 1 first, or
to amend task 1.1.

---

## R-6 — The mapping row cannot carry `transferred_on` before the transfer

**Decision**: the row's text is prepared complete except `transferred_on`, which
is left as an explicit `<the transfer date>` placeholder in the prepared
fragment and filled from runbook step 1.2's verified output.

**Rationale**: `transferred_on` records a completed act. The exemplar's two rows
carry `transferred_on: 2026-08-26` because that transfer happened. A date
written before the act is a falsehood in a file whose whole purpose is that a
frozen former spelling stays machine-interpretable. This is the second, and
independent, reason group 1 is gated at runbook step 1.2 rather than merely
blocked on R-5.

---

## R-7 — Re-issuing the origin register early performs the revocation in reverse

**Decision**: group 5, plus the clearing corpus (3.8), the fixture register's
prose (3.11) and `tests/factory_identity/test_validator.py` (3.13), land in ONE
gated, human-only pull request.

**Rationale**: `scripts/validate-clearing-dispatch.py` compares a sealed
request's `origin.repository` against `governance/factory-identity/register.yaml`.
codexFactory's live dispatches today originate at `opensoft/codexFactory`.
Respelling the register today therefore refuses **today's real requests** — the
same revocation `design.md` § 4.3 warns the transfer will cause, applied in the
wrong direction and a day early. `tests/clearing/test_origin_signature.py`
(lines 200, 204, 205, 217, 356) asserts the live register by design, which is
why design § 3 and § 4.3 D-2 keep it in the same commit; that one-commit rule
also means the whole cluster shares one gate.

**Alternatives considered**: *split the unsigned clearing examples out and land
them now.* Rejected: they are checked against the register's identity and are
the corpus that proves the single-door attestation path; landing them ahead of
the register puts the example corpus and the live register in disagreement for
the length of the window.

---

## R-8 — `README.md` per line, as task 4.8 demands

**Decision**: nine occurrences, not eight; six renamed at the transfer, **three
frozen**. Recorded per line.

**Rationale**: the packet's line numbers (316, 409, 530, 531, 642, 644, 1172,
1184) have shifted — the README grew. Measured at this head, with the
records-and-assertions test applied per line:

| line | text | verdict |
| ---: | --- | --- |
| 316 | *"Engineering-domain implementation docs now belong in `opensoft/codexFactory`."* | RENAME — asserts what IS (present tense; gated) |
| 409 | the `## Domain Implementations` list entry | RENAME — asserts what IS (gated) |
| 629 | this packet's own OpenSpec Records entry: *"… `opensoft/codexFactory` as repository identity inside governed contract content. Measured at `origin/main` `64aad02e`: 281 occurrences across 150 files …"* | **FROZEN** — the former identity is the SUBJECT of the change and the sentence records a dated measurement. Respelling it would make the packet's record claim the change is about the identity it moves TO |
| 678, 679 | `[codexFactory #232](https://github.com/opensoft/codexFactory/issues/232)`, `[codexFactory #272](…/pull/272)` | RENAME — kept-current index citations; issue and pull-request NUMBERS carry through a transfer. Gated: the URL 404s until the move |
| 790, 792 | `[#232](…/issues/232)`, `[#203](…/issues/203)` | RENAME, same reasoning, gated |
| 1335 | *"… the first originating repository `opensoft/codexFactory` — plus the disjointness validator …"* inside **REALIZATION COMPLETE AT THIS PR** | **FROZEN** — narrates a completed dated act |
| 1347 | *"The realization for `opensoft/codexFactory` is therefore COMPLETE at this PR"* | **FROZEN** — same |

Task 4.8 named lines 1172/1184 as *"candidates for the freeze — decide against
the test, do not sweep, and record which way each went."* Both went to the
freeze, and a **third** joined them (line 629, this packet's own Records entry,
which did not exist when the packet was written).

**Consequence recorded**: the frozen set becomes **81 occurrences** where the
packet says 78 — the three README lines are frozen inside a file that is
otherwise renamed, so the file count does not move. Packet task 6.5's *"zero
remaining live occurrences outside the frozen and not-swept sets"* must be read
against 81, and this feature says so rather than letting a later reader find
three unexplained hits in `README.md`.

---

## R-9 — Task 3.8 says six clearing files; there are seven

**Decision**: seven files, eleven occurrences. Classified by rule, not by fresh
judgment.

**Rationale**: `contracts/clearing/examples/negative/` holds **five** negatives
carrying the string, not four:
`attestation-claiming-full-completeness-before-admission.yaml` (2),
`attestation-filing-a-dark-lane-as-a-widening.yaml` (2),
`attestation-with-one-estate-wide-expected-set.yaml` (1),
`deliberation-return-carrying-a-verdict.yaml` (1) and
`deliberation-return-that-does-not-match-its-shape.yaml` (1) — plus
`single-door-attestation.example.yaml` (3) and
`deliberation-return.example.yaml` (1). The fifth negative arrived with lane
`hermes-wallet-exercise`'s `admit-deliberation-clearing-operation` after
2026-09-07. Packet task 2.3 requires exactly this: classify a new occurrence by
the published rule. A clearing example is `contracts/**` outside
`signed-execution-chain/` → RENAME.

---

## R-10 — Task 5.4's respell is a no-op

**Decision**: run 5.4's validator half; record that its respell half has nothing
to respell.

**Rationale**: measured —
`governance/factory-identity/attestations/custody-attest-wal-origin-codexfactory-0001.yaml`
contains **no `opensoft/` owner segment at all**. Its seven mentions of
`codexfactory` are the BARE forms `wal-origin-codexfactory-0001`,
`grant-origin-codexfactory-0001`, `attest-custody-wal-origin-codexfactory-0001`
and the prose *"codexFactory's own hosted packaging environment"*. Packet task
6.4 is explicit that a transfer moves the OWNER SEGMENT only and that bare
member names are correct before and after — so the attestation is already
correct and editing it would violate 6.4.

---

## R-11 — `disposition-codexfactory-declared-renames` is not this feature's business

**Decision**: leave it failing; record what it is.

**Rationale**: the name collides and it is the one pre-existing
`openspec validate --all --strict` failure, so it had to be read rather than
assumed. It disposes of **OpenSpec CLI 1.12.0 scenario-currency findings** over
two declared, ratified SCENARIO RETITLES in codexFactory changes
(`add-regular-pr-council-clearance`, `amend-composition-selector-labelling`) by
adding two `dispositions:` entries to `contracts/openspec-cli-pin.yaml`. It has
**nothing to do with repository renames**, it is not the sweep-record mechanism
group 2 could use, and it fails `--strict` because it is a deltaless packet —
`Status: ratified`, realized on the openxFactory main line, awaiting archive.
The packet's own Impact section predicts the same: *"the one pre-existing failure
being `disposition-codexfactory-declared-renames`, … unrelated to this change and
not repaired by it."*

---

## R-12 — No CI job supplies `--domain-repo`, so the resolver-key migration edits no workflow

**Decision**: record the resolver-key migration as a consumer-visible note for
the bundle changelog; edit no workflow for it.

**Rationale**: measured — `git grep -- "domain-repo"` at this head returns only
`README.md` prose, `contracts/CHANGELOG.md`, `contracts/hermes-runtime/README.md`
(the flag's documentation), `contracts/intent-compliance/README.md`,
`contracts/omnigent/README.md` and `docs/contract-versioning-policy.md`. **No
workflow, no script and no test passes the flag with a repository key.** The
only in-test use is
`tests/hermes_runtime_contracts/test_domain_regression.py:410`,
`resolver("opensoft/codexFactory")`, against a `tmp_path` bare-mirror fixture
whose directory segments are the bare strings `"opensoft"` and
`"codexFactory.git"` — so the fixture's own path construction changes with the
key and nothing outside the test does.

---

## R-13 — `governance/factory-identity/` exists only in openxFactory

**Decision**: the human-only pull request is an **openxFactory** pull request.

**Rationale**: measured — `git ls-tree -d origin/main -- governance/factory-identity/`
on `opensoft/codexFactory` returns nothing; the tree exists only here, holding
`register.yaml`, one wallet, one grant and one custody attestation. This is
design § 4.3's own reason **D-2(a)**: *"The artifacts live in openxFactory's
governed tree, so there is no repository boundary to cross."* What is in
codexFactory is the FLOOR ENTRY naming the directory — the reason the pull
request is human-only — not the directory itself.

---

## R-14 — Group 7 and group 8.4 cannot complete in this feature

**Decision**: prepare group 7; record group 8.4 as owed; tick neither.

**Rationale**: two independent reasons, both structural.

- **Group 7 (the cut).** `docs/contract-versioning-policy.md` § Bundle
  Realization Order allocates the minor *after* rebasing onto the final
  integration point and re-checking availability, and constitution principle VI
  forbids reserving a number in advance. The final integration point is the
  merge of the gated slices, which **this lane does not perform**. The eight
  members' transient is therefore predicted and recorded, not observed on
  `main`.
- **Group 8.4 (`sync-notebooklm-books.py --apply`).** It writes to a live
  external service and the packet schedules it *"after the doc changes land"*.
  Running it against unmerged work would project drafts into the derived
  notebooks.

---

## R-15 — Which packet tasks this feature can tick, and which it cannot

**Decision**: tick nothing in the packet's `tasks.md` that requires a merge to
`main`; instead name, per task, the pull request that will tick it.

**Rationale**: the lane merges nothing. A tick is a claim that an act is done,
and for a rename the act completes at merge. The packet's group 0 already models
this discipline — box 0.3 ticks only because the ratification record *"is a diff
in this pull request, which is what lets this box be ticked under house
practice."* The same standard applied here leaves groups 1, 3, 4, 5 and 7
unticked, and group 2, 6 and 8 tickable only for the parts whose act is the
evidence itself and whose evidence is in an open pull request — so this feature
ticks **nothing** and records the mapping instead.
