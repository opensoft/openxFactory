---
code_surface: openxFactory — FIVE files move in substance, all in this pull request, and no other surface. (1) `contracts/openspec-cli-pin.yaml`: the `dispositions:` list LOSES two entries and gains none, going 5 -> 3. The two DELETIONS are the whole `repo: codexFactory` / `item: extend-merge-master-envelope-to-floor-bot-lanes` / `path: merge-master-approval/spec.md` entry and the whole `repo: codexFactory` / `item: relocate-review-authority-floor` / `path: merge-master-approval/spec.md` entry, together with the dated 2026-09-11 comment block that introduced them. Three prose passages move so the file stops describing a list it no longer has: a NEW dated 2026-10-09 paragraph in the header, the rollback note's count (five -> three), and the block above `dispositions:` (the two-class declaration keeps both classes, records that the canon-moved class is now empty, and the per-repository grouping goes from FOUR codexFactory entries to TWO). The dated 2026-09-11 header paragraph that recorded the two entries' arrival is LEFT AS ITS CHANGE WROTE IT. NO other field of the pin moves — not `version`, `integrity`, `shasum`, `tarball`, `lockfile`, `lockfile_integrity`, `lockfile_packages`, `rollback:`, `binary:`, `verify_pin:`, `consumer_entrypoint:`, `pinned_invocation:` or `resync_runbook:` — and NO surviving disposition entry is edited; in particular the `relocate-review-authority-floor` / `repository-gate-floor/spec.md` entry is byte-identical. (2) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: the count-pinning test moves 5 -> 3 and is renamed; the two triples leave `DISPOSITION_MEASUREMENT`, `DISPOSITION_CLASS` and `DISPOSITION_AUTHORITY_PREFIX`; `CANON_MOVED` and its `DISPOSITION_CLASS_CITATION` row STAY (`design.md` OQ-1). (3) `tests/doc-health/test_pin_shape_adapter.py`: the live-record count 5 -> 3. (4) `tests/pin_registrations/test_pin_registration_sweep.py`: the live packet-referent floor 4 -> 3, because the deleted entries carried the only two citations into `disposition-codexfactory-regular-pr-council-clearance-archive`. (5) `tests/sequenced_after/corpus-ledger.yaml` gains this change's own row, by `--seed-ledger`. `README.md` gains its OpenSpec Records entry. NOT THIS CHANGE'S SURFACE: `scripts/validate-openspec-cli-pin.py` does not move; no workflow moves; nothing under `openspec/specs/` is written; no ratified packet's documents are edited; codexFactory is not touched at all — its pin advance and both re-derivations are codexFactory acts in codexFactory's own pull request.
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin whose `contracts/manifest.yaml` row deliberately carries NO per-file `sha256` (the row's own comment names "a disposition RETIRED" as one of the three events the file legitimately moves on), and it appears in no `contracts/releases/*.digests.yaml` inventory, so no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own `openspec-cli-pin` and `pytest-suite` runs, green on openxFactory's tree, plus the codexFactory-tree measurements recorded in `evidence/codexfactory-sibling-currency-retirement-2026-10-09.md`.
sequenced_after: []
---

# Proposal: retire-codexfactory-sibling-currency-dispositions

Status: draft
Kind: proposal
Proposed: 2026-10-09, in lane `codexfactory-1` (display `codeXfactory-1`).
Origin: openxFactory
[#1286](https://github.com/opensoft/openxFactory/issues/1286), claimed by this
lane at
[comment 6086219075](https://github.com/opensoft/openxFactory/issues/1286#issuecomment-6086219075).
Coordination notice to the siblings' authoring lane on
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-6086181440),
the issue on which the two entries were ratified.

**THE WORD THIS PACKET IS DRAFTED UNDER, AND WHAT IT DOES NOT COVER.** Brett
Heap, first-hand in lane `codeXfactory-1`'s own session at
**2026-10-09T17:35:29Z**, chose ***"This lane drafts it (Recommended)"*** to the
question of who authors openxFactory's new change deleting the two codexFactory
sibling dispositions (gate G-1 of codeXfactory/codexFactory#549). Recorded on
[codeXfactory/codexFactory#549, comment 6086047985](https://github.com/codeXfactory/codexFactory/issues/549#issuecomment-6086047985).
That word authorizes THIS DRAFT. **It is not a ratification, not a landing word,
and not a ruling on any open question** (`design.md` § 7). This packet carries
`Status: draft`, the pull request is DRAFT, and both stay so until Brett's
own word.

In the same exchange he chose ***"Two-step: 93d13d6c now (Recommended)"***:
codexFactory's NEXT pin advance targets openxFactory `93d13d6c` without the
re-derivations, and the re-derivations ride a SECOND advance after this
deletion has landed. That is the sequence below.

## Why

`disposition-codexfactory-regular-pr-council-clearance-archive` (PR #1004,
landed at `5972c8f3`) added two `repo: codexFactory` entries to this pin, both on
`merge-master-approval/spec.md`. codexFactory PR #434 had archived
`add-regular-pr-council-clearance` and promoted a retitle of *Bounded autonomous
surface* into codexFactory's canon. Two still-ACTIVE codexFactory changes,
`extend-merge-master-envelope-to-floor-bot-lanes` and
`relocate-review-authority-floor`, hold their own `## MODIFIED` block for that
requirement, written against canon as it read before. Brett Heap ruled the
order, *"This change first"* (2026-09-11): each sibling re-derives its block
against the archived canon before its own archive, and each re-derivation
retires its entry here. The template's `tasks.md` 6.3 records that obligation
and performs none of it: *"Neither is drafted or begun here."*

**The entries cannot retire in the order their own `retires_when:` imagined.**
Each says the re-derivation happens, codexFactory's `--all` then REFUSES
`pin-disposition-stale`, and the entry is deleted afterwards. But codexFactory
does not read this file at openxFactory `main`. It reads it at the commit its own
`stack.yaml` declares (`xfactory.contract_ref`, `0992369a` at codexFactory
`main` `33b916c1`), and its `validate` checks openxFactory out there. So on
codexFactory's tree the re-derivation and the pin file can only change together,
in one codexFactory pull request, and every partial order is red. Measured on
2026-10-09 over codexFactory `main` `33b916c1`, through this repository's
pinned entrypoint (`evidence/codexfactory-sibling-currency-retirement-2026-10-09.md`):

| codexFactory tree | pin | result |
| --- | --- | --- |
| as on `main` | openxFactory `main`'s (5 entries) | exit **0**, 4 applied |
| as on `main` | this packet's (3 entries) | exit **1**, both findings UNDISPOSITIONED |
| both sibling blocks re-derived | openxFactory `main`'s | exit **2**, `REFUSE pin-disposition-stale` naming both entries |
| both sibling blocks re-derived | this packet's | exit **0**, 2 applied |

The fourth row is the end state, and it is reachable only if the deletion
exists on openxFactory first and codexFactory's advance to it carries both
re-derivations. So the deletion is published here first. On codexFactory's
tree, each entry and its finding then leave in the same commit, and the refusal
both entries predicted is not printed there on this sequence. **That is the
refusal's purpose met early, not bypassed**: the refusal exists to force a human
re-reading of an exception whose condition has gone, and this packet is that
re-reading, done before the condition goes and put to the convener for
ratification.

## What Changes

* **Two entries are DELETED, whole**: `extend-merge-master-envelope-to-floor-bot-lanes`
  and `relocate-review-authority-floor`, both `repo: codexFactory`, both
  `path: merge-master-approval/spec.md`, with every key (`level`, `finding`,
  `why`, `cited_to`, `ratified_by`, `retires_when`). Deletion is this file's only
  form for a retirement.
* **Their dated 2026-09-11 comment block is deleted with them.** It is a preface
  to the two entries and has nothing left to preface. The dated 2026-09-11
  paragraph in the HEADER, which records how the two arrived, is kept as its
  change wrote it, and a NEW dated 2026-10-09 paragraph follows it (`design.md`
  § 5).
* **The pin's present-tense prose is made true again**: the rollback note's
  count goes five -> three; the block above `dispositions:` keeps BOTH declared
  classes, says the canon-moved class now has no entry, and moves the
  per-repository grouping from four codexFactory entries to two.
* **`relocate-review-authority-floor`'s OTHER entry, on
  `repository-gate-floor/spec.md`, is untouched**, byte for byte. It is
  marker-blindness and retires on a different event, that change's archive.
* **Three test files move, deliberately** (`design.md` § 4):
  `tests/openspec_cli_pin/test_openspec_cli_pin.py` (count 5 -> 3, renamed;
  three per-entry maps lose two keys each; `CANON_MOVED` stays declared),
  `tests/doc-health/test_pin_shape_adapter.py` (the live-record count 5 -> 3),
  and `tests/pin_registrations/test_pin_registration_sweep.py` (the live
  packet-referent floor 4 -> 3).
* **No spec delta.** See *Capabilities*.

## Capabilities

**`neutral-product-pin` is applied, not extended.** The requirement *"A
dispositioned finding is cited, upgrade-coupled, and refused when stale"*
(`openspec/specs/neutral-product-pin/spec.md:639`) already states every property
this packet relies on: a disposition is scoped to one repository; an entry for
another repository is neither applied nor stale here; a finding no disposition
covers FAILS the run (the scenario *"A finding is reported that no disposition
covers"*); and an entry's remedy is an edit to the pin file. Removing an entry
whose finding still occurs on some tree is not a new rule. That scenario says
what then happens on that tree, and the sequence below keeps it off codexFactory
`main`. `.openspec.yaml` declares `skip_specs: true`, and `design.md` § 3
records the criterion.

## Impact

* **Why it is safe to land first, on BOTH trees.**
  * **openxFactory's own gate ignores `repo: codexFactory` entries.** The
    property is pinned against the real pin by
    `test_the_consumers_entries_are_out_of_scope_on_this_repositorys_own_tree`
    (`tests/openspec_cli_pin/test_openspec_cli_pin.py:946`), and it is
    measured on this branch with the gate's literal invocation (`tasks.md` 4.1).
  * **codexFactory reads its own declared pin.** Its `validate` checks
    openxFactory out at `stack.yaml` `xfactory.contract_ref` (the CLI pin's
    `contracts/manifest.yaml` row says *"CHECK OUT, NEVER COPY"*). Landing this
    packet moves no byte codexFactory reads until codexFactory itself advances.
* **THE COORDINATED SEQUENCE, AND ITS ONE HARD CONSTRAINT.**
  1. codexFactory #549's FIRST advance targets openxFactory `93d13d6c`
     (*"Two-step: 93d13d6c now"*). That pin still carries all five entries, which
     is the first row of the table above: exit 0. It does not depend on this
     packet in either direction.
  2. **This packet** is ratified on Brett Heap's word and lands under
     lane-collision Rule 6 on a separate landing word, producing commit **D** on
     openxFactory `main`.
  3. codexFactory #549's SECOND advance is ONE codexFactory pull request that
     advances the declared pin to an openxFactory commit at or after D (the
     newest one whose push workflows are all green when read) AND carries both
     sibling re-derivations, each under its own owner word (gate G-2 on #549).
     Its `validate` must read the fourth row of the table: exit 0, 2 applied.
  4. The aggregation's pin-syncs follow under its own rules.

  **The hard constraint: after D lands, codexFactory MUST NOT advance its
  declared openxFactory pin to D or later WITHOUT both re-derivations in the
  same pull request.** Without them it reads the second row: exit 1. This
  couples every codexFactory pin advance past D to the re-derivations. That
  cost is real and is put to the convener as `design.md` OQ-3.
* **Relation to the template's 6.3.** `disposition-codexfactory-regular-pr-council-clearance-archive`
  `tasks.md` 6.3 names the two re-derivations and says each retires its entry
  here. This packet performs the openxFactory half of that, the deletion, ahead
  of the codexFactory half, for the reason measured above. 6.3 stays OPEN: the
  re-derivations are codexFactory acts, not performed here. This packet does not
  edit that ratified packet. Whether its 6.3 gains a dated cross-reference, and
  when, is `design.md` OQ-2.
* **Still owed after this lands, named so nobody reads it as done:**
  * codexFactory #549's second advance, with both re-derivations and their owner
    words (G-2: extend- `tasks.md` 1.7 and its owner box 4.2a; a new dated
    amendment row in relocate-, which has no row for it today);
  * the template's 6.3 (above);
  * the watch on `Fission-AI/OpenSpec#1793`, which reaches the three surviving
    marker-blindness entries and is unchanged by this packet.
