# Tasks: adopt-configured-notebook-hosting-identity

**NOTHING IN THIS FILE IS PERFORMED BY THE PROPOSAL.** Every spec edit,
resolver, synthetic literal, fixture change and move below is implementation
work for a later Speckit feature, after ratification. The proposal declares the
disposition; the tasks execute it. This packet's landing ticks nothing except
0.1.

**AND NOTHING IN THIS FILE MOVES THE LIVE RECORD.** Group 5 is an OPERATOR
ceremony in a PRIVATE repository, performed by Brett Heap on his own word. It is
named here because the ordering depends on it — not owned here.

**ORDER IS LOAD-BEARING IN ONE PLACE.** Group 2 (the resolver) must land and be
green BEFORE Group 5 (the move), and Group 5 before Group 3 (the public instance
goes synthetic). Any other order leaves an install unable to sync between two
commits, or publishes a synthetic declaration as if it were live. `design.md`
§ 3.3 states it once and this file follows it.

## 0. Ratification gate

- [x] 0.1 (2026-09-08) **Authorization to author is recorded, and it is not a
      ratification.** Brett Heap (convener), Q2 option [A] on
      `~/session-prompts/redaction-outside-ideation-decision-2026-09-07.md`,
      2026-09-08T03:36Z, through the interactive multi-choice walkthrough:
      "one small governed change (proposal -> your ratification -> Speckit
      realization)". The ruling settled the FORM and explicitly left the live
      record's home to the realization; it settled nothing else. Recorded in
      `.openspec.yaml` `origin.approved_by` / `approved_on`.
- [x] 0.2 (2026-09-08) **Ratified.** Brett Heap (convener)'s word on the
      delta, the resolver shape and the five open questions — verbatim
      **"Ratify 783 and merge"**, given through the interactive multi-choice
      walkthrough, ~12:20Z-12:35Z UTC, against head
      `fd7a74fe3f9d6257bbdeb5b950c040d50a8038fb`. **OQ-A, OQ-B, OQ-C, OQ-D and
      OQ-E are all RULED**, each matching this packet's own recommendation —
      see the record. Recorded as `review/ratification-2026-09-08.md` in this
      change directory, a diff in the pull request that carries it, which is
      what lets this box be ticked under house practice. **No box in Groups
      1-9 is ticked by this act.**
- [ ] 0.3 Confirm the premises still hold at realization head, rather than
      trusting this packet's measurements: the five files still carry 40 lines
      (`git grep -cE` on the four addresses), none of them has become a member
      of the current `contracts/releases/contract-v*.digests.yaml` inventory,
      the Q1/Q3 docs pull request has LANDED (Group 6 edits the same document),
      and `openspec validate --all --strict` still reads one pre-existing
      failure and no more.

## 1. The promoted requirement

- [ ] 1.1 Apply the delta to canon **by the archive act, never by hand** — the
      `## MODIFIED Requirements` block in
      `specs/lifecycle-notebook-projection/spec.md` replaces
      *The projection's hosting identity is declared at install* wholesale, so
      the block IS the post-archive text. Re-read it against canon immediately
      before archiving: `modified-block-currency` exists because a block written
      weeks earlier holds a silent deletion when canon moves under it.
- [ ] 1.2 Re-verify, at that moment, that the block still carries all four
      promoted body paragraphs byte-identically and all five promoted scenario
      titles, and that the ONLY promoted unit it does not carry is the one
      identity bullet. Expect exactly ONE `info` carriage-ledger finding and
      ZERO scenario-title findings; anything else means canon moved and the
      block owes a re-read, not a re-run.
- [ ] 1.3 Do NOT add a `Removed from canon by` marker. It names the retired unit
      as a code span carrying that unit's exact text — the address — so using it
      would reprint in the delta the value the delta removes. The delta's header
      paragraph is the declaration instead. (`design.md` § 4.)

## 2. The configured-path resolver

- [ ] 2.1 Add ONE resolver, shared by both readers:
      `$XFACTORY_NOTEBOOK_HOSTING_DECLARATION` (absolute or workspace-relative),
      then `<workspace>/.xfactory/notebook-hosting.yaml`'s `declaration_path:`,
      then UNDECLARED. Standard library only — the sync deliberately carries no
      YAML dependency and this must not introduce one.
- [ ] 2.2 `scripts/sync-notebooklm-books.py`: `HOSTING_REL` becomes the
      resolver's output rather than a constant. `read_hosting_declaration()`
      keeps its narrow scalar parse UNCHANGED in SHAPE and gains exactly two
      things: `instance` joins `_HOSTING_SCALARS` (without which the reader
      cannot see the marker at all — it reads only the keys in that tuple at
      `indent == 2`), and one branch says a record marked as an example is not
      a declaration.
      `_refuse_unusable_declaration()` gains the matching refusal, worded like
      its siblings (what was found, why it is refused, the exact remedy).
      `enforce_hosting_profile()`'s five steps and every refusal message are
      untouched.
- [ ] 2.3 `scripts/validate-notebook-projection-hosting.py`: precedence becomes
      `argv[1]`, then the resolver, then `DEFAULT_REL` **as a fixture**. Add
      `--resolved` so the operator check of Group 5 is one scriptable command.
      Keep the not-found message's meaning: an install that has declared nothing
      is a transition state, not a passing one.
- [ ] 2.4 Add the four tests the resolver owes:
      env-var resolution; workspace-config resolution; absent configuration is
      UNDECLARED and the sync runs unbound exactly as it does today; a
      configured path resolving to the shipped example is REFUSED and the
      message names the file and the remedy.
- [ ] 2.5 Prove the resolver is behaviour-preserving BEFORE anything moves: with
      configuration pointing at the current committed path, every existing
      `tests/notebooklm/` test passes unchanged. This is the box that makes
      Group 5 safe.
- [ ] 2.6 `.gitignore` the workspace configuration file, and state in its own
      header that it is per-machine and carries no secret — a path is not a
      credential, and nothing about this file should invite one.

## 3. The public instance becomes synthetic

**Gated on 2.5 green AND Group 5 complete.**

- [ ] 3.1 Rewrite `examples/notebook-projection-hosting.yaml` as a SYNTHETIC
      instance: `hosting.account`, `hosting.migration.from_account`, every
      `share_out[].hosting_account` and `[].user`, and the `denied[]` row go to
      `example.invalid` addresses (D-3); `hosting.domain` matches the synthetic
      account's domain, because the validator compares those two fields.
- [ ] 3.2 Mark it in the record — `hosting.instance: example` (OQ-C) — at the
      two-space indent the sync's narrow reader parses, not in a comment. A
      comment is invisible to the reader that must refuse it.
- [ ] 3.3 Keep the SHAPE byte-for-byte (D-4): same keys, same order, same
      comment structure, same roster arity. Rewrite the prose comments so they
      describe the SHAPE rather than Opensoft's history — the migration
      narrative, the 2026-08-27 rulings and the denial's reasoning belong to the
      live record, which now holds them.
- [ ] 3.4 Take the actor names to role placeholders (OQ-D), keeping
      `share_out[].granted_by` equal to `approval.designated_actor` — the
      validator refuses them unequal, so this is one edit in two places.
- [ ] 3.5 Prove it: `python3 scripts/validate-notebook-projection-hosting.py`
      exits 0 over the synthetic instance, and
      `test_the_committed_record_conforms` — re-aimed and renamed to say what it
      now asserts — passes.
- [ ] 3.6 Leave `examples/lifecycle-notebook-workspaces.yaml` ALONE. Its two
      lines are comments and belong to the Q1 docs pull request; touching it
      here would make one file the subject of two lanes.

## 4. The test fixtures

- [ ] 4.1 `tests/notebooklm/test_nlm_auth.py`: `STORED` and `LEGACY` become
      synthetic. They are compared against each other and against captured
      values inside the harness, never against a live account, so the
      account-mismatch and carry-forward tests keep their exact meaning.
- [ ] 4.2 `tests/notebooklm/test_sync_notebooklm_books.py`: `HOSTING_DECLARED`
      and `HOSTING_PENDING` fixture texts and the eleven assertions over them go
      synthetic. Keep the PENDING assertion that the run binds where the books
      actually live — it is the one that proves "a declaration is not a
      migration", and it works on any address.
- [ ] 4.3 `tests/notebooklm/test_validate_hosting.py`: `BASE`, `ENTRY` and the
      eight assertions over them go synthetic. Keep every negative mutation
      firing for its stated reason — service account, consumer account, domain
      mismatch, roster-key collision, `granted_by` disagreement.
- [ ] 4.4 Re-run the whole suite and check the `pytest-suite` pins: SKIPPED must
      not move (no test is added skipped), SELECTED and PASSED may only rise,
      and the floors are raised deliberately with the four new tests as the
      reason.
- [ ] 4.5 Sweep for a missed literal:
      `git grep -nE "<the four addresses>" -- tests/ examples/ scripts/ openspec/specs/`
      returns nothing. File the output as the realization evidence.

## 5. [OPERATOR — BRETT] The live record's move

**This group is Brett Heap's. It happens in a PRIVATE repository, on his own
word, and no agent performs it.** Gated on OQ-A being answered and on 2.5 green.

- [ ] 5.1 Copy the live record — `hosting:` block, `custody:` reference,
      `approval:` block, all seven `share_out` rows and the `denied` row —
      **VERBATIM** into the home OQ-A settles (recommended:
      `installs/hermes-install` `config/clients/opensoft/notebook-projection-hosting.yaml`).
      It is a record of eight governed acts (OQ-E); it moves, it is not
      re-authored.
- [ ] 5.2 Write the workspace configuration naming that path, and prove the
      binding: `python3 scripts/validate-notebook-projection-hosting.py
      --resolved` exits 0, and a `sync-notebooklm-books.py` dry run prints the
      `hosting: operator_hosted — … (nlm profile …, verified active)` line
      against the resolved record.
- [ ] 5.3 Record the move where the receiving repository records governed
      config: a one-line note in its own change or commit body citing this
      change id and this ruling. The public tree learns only that a record
      exists and where — never the values.
- [ ] 5.4 Confirm the public flip's gate: after 5.2 and Group 3, no line of the
      public tree carries a live identity for this projection. **The flip is
      gated on THIS box, not on this packet's merge.**

## 6. Documents, records and the archive gate

- [ ] 6.1 `docs/lifecycle-notebook-projection.md` § *The declaration* and § *The
      approval lane*: describe the two-file model — the synthetic instance here,
      the live record resolved from configuration, the resolution order, and the
      operator check that replaces the CI one. **Sequenced after the Q1 docs
      pull request** (it redacts three address lines in this same file; 0.3
      checks that it landed).
- [ ] 6.2 `docs/notebook-projection-migration-runbook.md` and
      `docs/notebooklm-sync-open-item.md`: update the four path references that
      now resolve differently. Prose redaction in those files is Q1's, not this
      change's — touch only the structural claims.
- [ ] 6.3 `README.md`: move this change's OpenSpec Records entry from proposal
      to realized/archived state at the archive act, and add the doc index line
      if a section title moved.
- [ ] 6.4 File the realization evidence: the sweep output from 4.5, the resolver
      test names, the `--resolved` green line from 5.2 (values elided), and the
      pytest pin deltas.
- [ ] 6.5 Re-run the sweep ledger at the realization head
      (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<PR>'`) and confirm the diff is this change's own row.
- [ ] 6.6 Archive only when `release-realization`'s gate is satisfiable: the
      code surface merged on openxFactory main and green — the pytest suite with
      the new fixtures, the validator over the synthetic instance, and the
      operator's `--resolved` line for the live record. A doc-only archive is
      not available to this change; its surface is not `none`.
