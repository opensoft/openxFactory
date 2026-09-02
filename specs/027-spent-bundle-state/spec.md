# Feature Specification: the third state — a SPENT bundle

**Feature Branch**: `027-spent-bundle-state`

**Created**: 2026-09-02

**Status**: Draft

**Realizes**: `openspec/changes/declare-spent-bundle-state` (ratified
2026-09-02 by Brett Heap, in session, in TWO ACTS over OD-3 and OD-4; record
`openspec/changes/declare-spent-bundle-state/review/ratification-2026-09-02.md`;
merged as PR #578, squash `f4fddf7c`, which is this branch's base). ONE
`## MODIFIED Requirements` block over the promoted canon requirement
`Release-tag publication` in the `doc-health` capability. That packet's
`tasks.md` § 2 (2.1–2.9) is this feature's plan at task grain; § 3 and § 5 are
NOT this feature's and are not touched.

**Input**: Speckit realization of `declare-spent-bundle-state`: a SPENT state
for the `release-tag-publication` doc-health family, entered ONLY by an
explicit reserved declaration read from `contracts/CHANGELOG.md` at the
published tip; three outcomes (ACCEPTED `info`, PROVISIONAL `warning`, REFUSED
`error`); every finding on the spent bundle's own release inventory except one;
and the `contract-v2.6` declaration that makes `main` green.

## Why this exists (one paragraph, from the ratified packet)

`scripts/doc_health/release_tag_publication.py` has exactly two answers for a
bundle — *published*, or *owes a tag*. `contract-v2.6` is a third: DECLARED at
`bbbbeda9`, NEVER VERIFIABLE there (five `HGR-RELEASE-DIGEST-MISMATCH`
findings, because the cut branch was never rebased onto the final integration
point), and NEVER PUBLISHABLE (the targeting rule requires a first-parent
commit on published `main` that declares the bundle AND at which
`verify-commit` passes; exactly one commit declares it and `verify-commit`
fails there — and a completion commit could not have cured the second defect,
an ADDITIVE change class over a tree that refuses three shapes `contract-v2.5`
accepted). The finding the family raises is TRUE and its prescribed action —
retro-publication — is unperformable by anyone, which is how a report loses the
readers the rest of it needs. Brett Heap ruled the supersession on 2026-09-02
("Supersede: v3.0 is the completion"); the cut declined to relax the check
inside a release and filed issue #575 instead.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — a reader of the report meets an answerable finding (Priority: P1)

A maintainer reading the nightly doc-health report finds
`contracts/releases/contract-v2.6.digests.yaml` reported at `info`, saying that
the bundle is SPENT, which bundle superseded it, where the record is, who ruled
it and on what measurement — rather than an `error` telling them to publish a
tag that cannot exist.

**Why this priority**: it is the whole of the packet's Why, and it is the state
Brett ruled explicitly (OD-3: *"the reader who finds
`contracts/releases/contract-v2.6.digests.yaml` with no matching tag is owed
the answer where they are looking"*).

**Independent test**: over a fixture repository holding a cut-and-untagged
bundle, a later cut, a published tag on the later cut, and the reserved
declaration inside the later cut's changelog entry, `check_repo` returns
exactly one finding and it is that `info`.

**Acceptance**: FR-001, FR-002, FR-006, FR-007, FR-013.

### User Story 2 — a bundle cannot be walked away from (Priority: P1)

An operator who wants an inconvenient untagged bundle to stop being reported
finds that there is exactly one way to do it: publish the tag of a LATER
bundle that supersedes it. Every other route — silence, an absent record, a
missing element, a self-declaration, a duplicate, an earlier successor, a
successor that was never cut, a declaration about the bundle the manifest still
declares — leaves the `error` standing, and adds one of its own.

**Why this priority**: this is the guard, and it is what makes the state safe
to have at all (OD-4 as ruled, narrowed by OD-9 on a Codex P1). A state that
could be entered by writing a sentence would be the check being switched off
with a citation attached.

**Independent test**: seven fixture repositories, one per refusal, each
asserting BOTH the refusal `error` AND that the superseded
`error` still stands beside it.

**Acceptance**: FR-003, FR-004, FR-005, FR-008, FR-009, FR-010, FR-011.

### User Story 3 — the state's disappearance is itself reported (Priority: P2)

A later session that deletes the declaration, or the inventory, to quiet the
report finds that the `info`'s disappearance raises an `uncited-resolution`
ERROR against the exact bundle whose record went missing — and that two spent
bundles carry two identities, so one removal cannot hide behind the other's
surviving finding.

**Why this priority**: it is OD-5 as amended on Codex's P1, and OQ-3 asks
whether the mechanism it relies on actually behaves this way for an `info`. The
packet requires it PROVED rather than inherited.

**Independent test**: render a report from the accepted `info`, read it back
with `report.parse_previous`, and assert `report.uncited_resolutions` raises
exactly one error on that bundle's inventory path; then the two-bundle version
of the same, withdrawing one declaration.

**Acceptance**: FR-007, FR-012.

### User Story 4 — nothing else moves (Priority: P2)

A reviewer checking what this feature relaxed finds: the threshold still five,
the floor still `contract-v1.7`, MISPLACED and LIGHTWEIGHT untouched and
explicitly beyond the state's reach, the declared bundle's distance grading
untouched, the five bundles under § *Untagged Bundles After Enforcement Began*
not retrofitted, no new family, and `family-enumeration` silent.

**Why this priority**: the packet's Non-goals, and the difference between a
third state and a relaxation.

**Independent test**: the file's pre-existing 19 tests pass unchanged in
substance; a no-retrofit fixture holding a below-floor bundle and a published
bundle, each named by a declaration, returns `[]`.

**Acceptance**: FR-014, FR-015.

### Edge cases

* A declaration whose SUBJECT is a bundle this repository never cut — a typo —
  disposes nothing and must not be read as disposing anything else.
* A line that begins with the reserved opener and completes nothing.
* A CAUSE containing the element separator.
* `contracts/CHANGELOG.md` unreadable at the published tip: the read failed,
  which is not the same fact as no declaration (#338, one document over).
* Two declarations naming one bundle.

## Requirements *(mandatory)*

### Functional requirements

- **FR-001** The family MUST read SPENT declarations from
  `contracts/CHANGELOG.md` AT THE PUBLISHED TIP and from nowhere else — never
  from `health/dispositions.yaml`, never from the working tree, never from
  silence.
- **FR-002** The declaration MUST take one reserved single-line form, whose
  opener `**SPENT BUNDLE:**` is RESERVED: no other line in that file may begin
  with it, and a line that does and does not complete the form is a MALFORMED
  declaration rather than prose.
- **FR-003** Four elements MUST be checked for presence and non-emptiness: the
  superseding bundle, the cause, the ruling (author AND date) and the
  measurement of record. A declaration omitting any MUST be an `error` NAMING
  which, and MUST NOT be reported in the absent-tag words.
- **FR-004** A declaration MUST be accepted only where the `## contract-vX.Y`
  entry containing it is the entry of the bundle it names as superseding; and a
  bundle MUST NOT be able to declare ITSELF spent.
- **FR-005** The superseding bundle MUST be CUT, MUST be PUBLISHED (an
  annotated tag peeling to a commit that declares it) and MUST be STRICTLY
  LATER in `(major, minor)`. Where it was never cut, or is not later, the
  declaration MUST be an `error` accepting nothing.
- **FR-006** An ACCEPTED declaration MUST emit exactly one `info` naming the
  spent bundle, the superseding bundle and where the record is; and MUST NOT be
  recorded as the tag obligation having been MET.
- **FR-007** Every finding of this state MUST land on
  `contracts/releases/<bundle>.digests.yaml`, and the accepted `info` MUST be
  classed `contested` — with ONE exception (FR-011).
- **FR-008** A PROVISIONAL declaration — well formed, its LATER successor cut
  but not published — MUST emit one `warning` and MUST SUPPRESS the
  superseded-and-never-published `error` for that bundle: ONE finding, not two.
- **FR-009** The family MUST NOT suppress the SUCCESSOR's own finding, which is
  raised on the successor's own account and is what bounds the provisional band.
- **FR-010** A REFUSED declaration MUST leave the superseded
  `error` standing beside it, so that a bad declaration removes nothing; and
  more than one declaration naming one bundle MUST accept NONE of them.
- **FR-011** A declaration whose SUBJECT this repository never cut MUST be a
  `warning` on `contracts/CHANGELOG.md` — the one finding of this state with no
  per-bundle inventory to land on — and MUST NOT be read as disposing any other
  bundle.
- **FR-012** A declaration naming the bundle `contracts/manifest.yaml` declares
  at the published tip MUST be an `error`, and that bundle MUST continue to be
  graded by distance exactly as today.
- **FR-013** The changelog read MUST join the manifest read at the SAME commit
  under the SAME guard: `blobs_at` answering nothing is a SKIP naming that read,
  never "no declaration".
- **FR-014** The SPENT state MUST reach the ABSENT-tag arm and nothing else:
  no MISPLACED tag, no LIGHTWEIGHT ref, no distance-graded finding on the
  currently declared bundle is quieted by it.
- **FR-015** The state MUST NOT be read backwards onto the five bundles the
  versioning policy records under § *Untagged Bundles After Enforcement Began*,
  nor onto any bundle below the `contract-v1.7` floor.
- **FR-016** `contracts/CHANGELOG.md` MUST carry ONE reserved declaration for
  `contract-v2.6`, inside the EXISTING `contract-v2.6` disposition subsection of
  the `contract-v3.0` entry, and `main` MUST go green BECAUSE of it — proved by
  removing it and seeing the `error` return.

### Key entities

* **SpentDeclaration** — one reserved line as READ, never as judged: subject,
  containing entry, superseding bundle, cause, author, date, measurement, line
  number, the elements it is missing, a non-element defect, and how many
  declarations named the same subject.
* **The three outcomes** — ACCEPTED / PROVISIONAL / REFUSED, which is a
  three-way and not a two-way: a two-way reading makes the ruled `warning` band
  unreachable (Codex round-3 P1).
* **The finding identity** — `(family, repo, path)`, which is why the path is
  `contracts/releases/<bundle>.digests.yaml` and not the manifest or the
  changelog.

## Success criteria *(mandatory)*

- **SC-001** `python3 -m pytest tests/doc-health` reports the SAME failure set
  as `main` — exactly one, `test_this_repository_reads_zero_and_the_probe_can_fire`,
  which reads the LIVE remote `main` and cannot see this branch's declaration.
  It goes green at the squash, and that is proved locally against a simulated
  post-merge origin rather than asserted.
- **SC-002** All 13 new scenarios of the amended requirement are tested, each
  with the positive control the file's convention requires.
- **SC-003** The red-first proof holds over the real repository: with the
  declaration at the published tip, one `info`; with it removed, the `error`.
- **SC-004** `--single-repo` doc-health moves by exactly one row against
  `f4fddf7c`: a `release-inventory-drift` `info` on `contracts/CHANGELOG.md`
  labelled *editorial member — expected between cuts*. `family-enumeration`
  silent.
- **SC-005** `openspec validate --all --strict`, `proposal-support verify`,
  `validate-sequenced-after.py` and `tests/sequenced_after` all pass, and no
  sequenced-after pin moves.

## Out of scope

* `docs/contract-versioning-policy.md`'s obligation-side paragraph — OpenSpec
  tasks § 3.1, ROUTED TO THE NEXT CUT by the owner's ruling of 2026-09-02 (see
  plan.md § Routing).
* Publishing or fabricating a tag for `contract-v2.6`; editing the manifest,
  the `contract-v2.6` entry or its inventory; touching
  `health/dispositions.yaml`; fixing #338; archiving the packet (§ 5, after
  merge).
