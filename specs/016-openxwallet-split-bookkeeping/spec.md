# Feature Specification: split-openxwallet-repo §1 bookkeeping

**Feature Branch**: `016-openxwallet-split-bookkeeping`

**Created**: 2026-08-26

**Status**: Draft

**Input**: User description: "Split-openxwallet-repo §1 bookkeeping: Amendment 2 to docs/openxdox-naming.md, the xFactory working-rule-#1 amendment, and the packet's own task ledger — realizes tasks.md group 1 of the ratified change (PR #391, main 5ef6d8d2)"

## Context

The OpenSpec change `split-openxwallet-repo` was ratified as proposed by Brett
Heap on 2026-08-26 and merged to openxFactory `main` at `5ef6d8d2`
(PR opensoft/openxFactory#391). Its `tasks.md` §1 is **the change's own diff** —
the doctrine edits and bookkeeping that belong to the ratification itself, as
distinct from §2–§12, which are named successors carrying their own
`code_surface` and their own realization evidence.

Most of §1 landed with the packet. Three items did not, and they are this
feature's entire scope: task 1.10 (the doc-health no-new-findings measurement,
run but unticked), task 1.11 (Amendment 2 to `docs/openxdox-naming.md`, in two
edits), and task 1.12 (the xFactory aggregation repo's working-rule #1
amendment, which lives in a different repository). A fourth item, task 1.1,
carries a stale trailing `Status: draft.` that the ratification falsified.

The house rule is that **OpenSpec ratifies and Speckit builds**: this feature is
the build vehicle for §1's remainder, not a second ratification of it. Every
text this feature writes is already quoted verbatim in the ratified
`proposal.md`, so the work is transcription plus evidence, and any deviation
from the quoted text is a defect rather than an improvement.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The naming record stops contradicting the ratified ruling (Priority: P1)

`docs/openxdox-naming.md` is a `ratified` record that lists `openxWallet` among
the lowercase family exceptions. R1 of the ratified change moved the product to
the house `openX<type>` capital-X form as `openXwallet`. Until the record is
amended, canon contradicts a ratified ruling, and the brand about to be created
at `opensoft/openXwallet` would be created under a spelling its own naming
record calls an exception.

A governance reader opens the naming record and reads, in one place, that
`openXwallet` is now on the house form, that the wire label deliberately stays
lowercase, and that `openXwallet-Install` is a registered name with no
repository behind it.

**Why this priority**: it is the only §1 item that resolves a live
contradiction inside a `ratified` document. It also gates nothing else, so it
can land alone and still deliver the whole value.

**Independent Test**: read `docs/openxdox-naming.md` end to end. Amendment 2
exists, is dated 2026-08-26, sits after Amendment 1, matches Amendment 1's
shape, and the inline pointer earlier in the record reads as grammatical English
naming one exception. Doc-health emits no new status or tag finding against the
file.

**Acceptance Scenarios**:

1. **Given** the ratified naming record with Amendment 1 as the last section,
   **When** Amendment 2 is appended, **Then** the new section's heading, body
   and closing "amended rather than rewritten" paragraph are byte-identical to
   the text quoted in `proposal.md` § "What this change RATIFIES" item 4.
2. **Given** the inline pointer whose sentence names TWO exceptions,
   **When** `openXwallet` leaves that list, **Then** the sentence reads
   "the lowercase `openxFactory` spelling is the family exception, not the rule;
   `openXwallet` left this list in Amendment 2" — singular noun, singular verb.
3. **Given** the record's `Status: ratified` header with exactly one
   `Ratified by:` citation line, **When** Amendment 2 lands, **Then** the
   lifecycle header is unchanged and still carries exactly one citation line.
4. **Given** the earlier record text that was true when written,
   **When** Amendment 2 lands, **Then** no prior sentence is rewritten or
   deleted — the record is amended, never rewritten.

---

### User Story 2 - The aggregation working rule stops being false as written (Priority: P1)

xFactory `CLAUDE.md` working rule #1 says domain-neutral contracts live **ONLY**
in `openxFactory`. The ratified change authorizes a neutral product repository
that openxFactory pins, which makes the rule false the moment the shed lands.
Every agent session in the workspace reads that file for orientation, so a stale
absolute there misdirects work in nine submodules.

An agent starting a session in the aggregation repo reads a working rule that
permits the neutral product repository, still forbids domain repos from
authoring neutral contracts, and still requires every consumer to pin.

**Why this priority**: it is a cross-repository edit with its own review gate,
and it is the item most likely to be forgotten once the wave moves to §2. It is
independent of User Story 1.

**Independent Test**: on the aggregation repo's proposed branch, read
`CLAUDE.md` § "Working rules" item 1. It matches the replacement text quoted in
`proposal.md` item 5 verbatim, and no other line of the file changed.

**Acceptance Scenarios**:

1. **Given** working rule #1's current text, **When** the amendment lands,
   **Then** item 1 reads exactly the replacement text quoted in the proposal,
   including "domain repos never author neutral contracts".
2. **Given** the aggregation repo is a shared checkout with nine submodules,
   **When** the amendment is prepared, **Then** it is authored in a dedicated
   worktree on its own branch and committed with an explicit pathspec naming
   only `CLAUDE.md`.
3. **Given** the amendment is a governance edit to another repository,
   **When** it is delivered, **Then** it arrives as an open pull request citing
   §1 of the ratified change and is **not** merged by this feature.
4. **Given** rules #2 through the end of the file, **When** the amendment
   lands, **Then** they are byte-identical to before.

---

### User Story 3 - §1's ledger tells the truth about itself (Priority: P2)

`tasks.md` §1 is the record of what the ratification did. Task 1.1 still ends
"`Status: draft`." — true when written, falsified by the ratification recorded
two tasks below it. Task 1.10's measurement was performed but its box is
unticked, so a reader cannot tell whether it passed, failed, or was skipped.

A reviewer reads §1 and can tell, per task, whether it is done and what evidence
says so.

**Why this priority**: it is bookkeeping over the other two stories' outcomes,
so it settles last. It carries real value — an unticked box that was actually
verified is indistinguishable from work never done — but it cannot be completed
before the stories it records.

**Independent Test**: read `tasks.md` §1. Every box is ticked, each newly ticked
box carries a trailing evidence note naming a file and a commit or PR, and 1.1's
trailing status clause describes the ratified state.

**Acceptance Scenarios**:

1. **Given** task 1.1's stale trailing "`Status: draft`.", **When** the ledger
   is corrected, **Then** the clause describes the header's ratified state and
   R1–R8 are not renumbered and the LOCKED block is untouched.
2. **Given** task 1.10's performed-but-unticked measurement, **When** it is
   ticked, **Then** the evidence note records the comparison actually made —
   the pre-packet tree, the post-packet tree, the finding counts for each, and
   any new finding by name and class.
3. **Given** a §1 task this feature completes, **When** it is ticked,
   **Then** a trailing evidence note names the file changed and the commit or
   pull request that carries it.
4. **Given** §2–§12's boxes, **When** §1 is completed, **Then** not one of
   them is ticked — each successor archives on its own evidence.

---

### Edge Cases

- **The mechanical substitution trap.** Deleting `` / `openxWallet` `` from the
  inline pointer leaves "the lowercase `openxFactory` spellings are the family
  exceptions" — plural agreement with a singular subject, inside a `ratified`
  record. The pointer must be rewritten as a sentence, not patched as a token.
- **A second citation line.** `document-lifecycle.md` § Status Claim Rules makes
  a bare or doubled ratification citation a violation: a `ratified` header names
  its ratification on exactly ONE line. Amendment 2 therefore adds no
  `Amended:`, `Ratified:` or second `Ratified by:` line to the header —
  Amendment 1's precedent, which changed no header line at all.
- **Case-sensitive spelling drift.** `openXwallet` (capital X, lowercase w) is
  the brand; `openxwallet` is the wire label; `openxWallet` is the retired
  spelling. All three appear legitimately in the record. A global
  case-insensitive replace corrupts capability ids, the `xfactory_wallet_*` kind
  prefix, paths and finding codes.
- **The pre-existing doc-health finding.** The packet's landing produced exactly
  one new finding, on the staged topic that cites the proposal. Its remedy is a
  lifecycle act on the staged topic, which is outside §1. Task 1.10 must be
  ticked with an evidence note that names it rather than a bare claim of green.
- **Aggregation-repo drift mid-edit.** The shared aggregation checkout may have
  other sessions' uncommitted work. The amendment must never sweep it.
- **Working rule #1 is contradicted until P4 lands.** The amendment makes the
  rule permissive before the shed exists. The ratified proposal states this
  deliberately; this feature must not "fix" it by deferring the edit.

## Requirements *(mandatory)*

### Functional Requirements

#### The naming record (task 1.11)

- **FR-001**: `docs/openxdox-naming.md` MUST gain a new final section headed
  `## Amendment 2 — openXwallet leaves the exception list (2026-08-26)`,
  appended after Amendment 1, whose body is the text quoted verbatim in
  `openspec/changes/split-openxwallet-repo/proposal.md` § "What this change
  RATIFIES" item 4.
- **FR-002**: Amendment 2 MUST record all three facts the quoted text carries:
  that `openxWallet` becomes `openXwallet` on the house `openX<type>` form by
  R1 of `split-openxwallet-repo` (Brett's ruling, 2026-08-26); that the wire
  label stays lowercase `openxwallet` by this record's own brand-versus-label
  rule; and that `openXwallet-Install` is registered as a NAME with no
  repository created, per the design's Q4 disposition.
- **FR-003**: Amendment 2 MUST close with the "amended rather than rewritten"
  paragraph, following Amendment 1's shape, so the record states why the earlier
  text stands rather than silently coexisting with it.
- **FR-004**: The inline pointer in § Decision MUST read
  "(the lowercase `openxFactory` spelling is the family exception, not the rule;
  `openXwallet` left this list in Amendment 2)" — the proposal's verbatim
  replacement, grammatical with one exception named.
- **FR-005**: No other sentence of `docs/openxdox-naming.md` MUST change, and
  its lifecycle header MUST remain byte-identical, carrying exactly one
  ratification citation line.

#### The aggregation working rule (task 1.12)

- **FR-006**: xFactory `CLAUDE.md` § "Working rules" item 1 MUST be replaced
  with the text quoted verbatim in `proposal.md` item 5: neutral contracts live
  in `openxFactory` or in a neutral `open*` product repository that
  `openxFactory` pins by commit and digest; domain repos never author neutral
  contracts; every consumer pins the openxFactory version it consumes in its
  `stack.yaml`.
- **FR-007**: The amendment MUST be authored in a dedicated aggregation-repo
  worktree on its own branch, never in the shared root checkout, and committed
  with an explicit pathspec naming only `CLAUDE.md`.
- **FR-008**: The amendment MUST be delivered as an open pull request against
  `opensoft/xFactory` `main`, whose body cites §1 of the ratified openxFactory
  change and PR #391, and MUST NOT be merged by this feature.
- **FR-009**: No file in the aggregation repo other than `CLAUDE.md` MUST be
  modified, and no other line of `CLAUDE.md` MUST change.

#### The task ledger (tasks 1.1, 1.10, and this feature's ticks)

- **FR-010**: Task 1.1's trailing "`Status: draft`." MUST be replaced with a
  clause describing the proposal header's actual ratified state, without
  renumbering R1–R8 and without editing the LOCKED constraint block.
- **FR-011**: Task 1.10 MUST be ticked with an evidence note recording the
  measurement actually performed: the two trees compared, the finding counts
  from each, and any finding present in the later run and absent from the
  earlier one, named with its family, path and class.
- **FR-012**: Every §1 task this feature completes MUST be ticked with a
  trailing evidence note naming the changed file and the commit or pull request
  carrying it, in the shape §1's already-ticked tasks use.
- **FR-013**: No box in `tasks.md` §2–§12 MUST be ticked, and no successor's
  text MUST change.
- **FR-014**: `README.md`'s `## OpenSpec Records` block MUST be edited only if a
  §1 task requires it; the change is already listed there by task 1.9, so the
  expected outcome is no edit.

#### Validation

- **FR-015**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` MUST pass
  with zero failures before the openxFactory commit.
- **FR-016**: `python3 scripts/doc-health.py --single-repo .` MUST report no new
  finding attributable to this feature's edits, compared against the same
  command on the feature branch's base commit.
- **FR-017**: Both pull requests MUST be left open for human review; this
  feature merges nothing.

### Key Entities

- **`docs/openxdox-naming.md`**: the `ratified` capability naming record.
  Amendment 1 (2026-08-14, the public host) is the precedent for shape: a dated
  `## Amendment N — <subject> (<date>)` section appended at the end, closing
  with a paragraph explaining that the record is amended rather than rewritten,
  and changing no header line.
- **`openspec/changes/split-openxwallet-repo/proposal.md`**: the ratified
  source of every text this feature writes. It quotes Amendment 2 and the
  working-rule replacement in full precisely so the diff is checkable against
  text rather than intent.
- **`openspec/changes/split-openxwallet-repo/tasks.md` §1**: the change's own
  work ledger. §2–§12 are named successors and out of scope.
- **xFactory `CLAUDE.md`**: the aggregation repo's orientation file, read by
  every session across nine submodules. Working rule #1 is the only target.
- **The two spellings**: `openXwallet` is the brand; `openxwallet` is the wire
  label, deliberately unreconciled. Both are correct in their own places.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader of `docs/openxdox-naming.md` can determine
  `openXwallet`'s current spelling, its wire label, and `openXwallet-Install`'s
  registered-name-only standing from that one file, with no reference to the
  change packet.
- **SC-002**: Amendment 2's body and the replaced inline pointer are
  byte-identical to the corresponding quoted text in the ratified proposal —
  a mechanical diff, zero discrepancies.
- **SC-003**: Every sentence of `docs/openxdox-naming.md` that predates
  Amendment 2 survives unchanged, and the file's lifecycle header is unchanged.
- **SC-004**: xFactory working rule #1 permits the neutral product repository
  while still forbidding domain repos from authoring neutral contracts, and the
  aggregation diff touches exactly one file and exactly that rule.
- **SC-005**: Every box in `tasks.md` §1 is ticked, and every box in §2–§12 is
  untouched.
- **SC-006**: Each box this feature ticks carries a trailing evidence note a
  reviewer can resolve to a file and a commit or PR without asking the author.
- **SC-007**: `openspec validate --all --strict` reports zero failures, and the
  doc-health finding counts on the feature branch equal those on its base
  commit for every family this feature's files belong to.
- **SC-008**: Both pull requests are open and unmerged when the feature reports
  complete.

## Assumptions

- The ratified `proposal.md` at `5ef6d8d2` is the authoritative source for every
  text this feature writes. Where this feature's judgment differs from the
  quoted text, the quoted text wins; no clarification round can change that,
  because the text is ratified.
- Amendment 1 is the shape precedent, and its precedent includes what it did
  **not** do: it added no header line. Amendment 2 follows both halves.
- The design's Q4 disposition ("the NAME is registered in Amendment 2 and no
  repository is created") is settled and travels into the record as written;
  whether Hermes is the eventual issuer host is out of scope.
- Task 1.10's phrase "the tree before the packet's completion" resolves to the
  first parent of the merge commit `5ef6d8d2` — openxFactory `main` immediately
  before PR #391 landed.
- 1.10's scope is "this change directory or the README entry". A new finding
  whose path lies outside both is reported in the evidence note rather than
  silently absorbed or silently remedied, because remedying it would be a
  lifecycle act on a staged topic that §1 does not authorize.
- The aggregation repo needs no initialized submodules for a `CLAUDE.md`-only
  edit, so the worktree is created without them.
- Neither pull request is merged here: both are governance edits, and the merge
  gate is human.
- §1 carries no code surface. There is nothing to unit-test; the evidence is
  validator output and a checkable diff against ratified text.
