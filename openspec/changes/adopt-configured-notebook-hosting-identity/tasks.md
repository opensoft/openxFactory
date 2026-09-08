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
- [x] 0.3 Confirm the premises still hold at realization head, rather than
      trusting this packet's measurements: the five files still carry 40 lines
      (`git grep -cE` on the four addresses), none of them has become a member
      of the current `contracts/releases/contract-v*.digests.yaml` inventory,
      the Q1/Q3 docs pull request has LANDED (Group 6 edits the same document),
      and `openspec validate --all --strict` still reads one pre-existing
      failure and no more.

      - REALIZED 2026-09-08 (feature 031). Re-measured at realization head
        `e7c53012` rather than trusted: the four addresses sit on **40 lines
        across the same five files** (18 / 1 / 2 / 11 / 8 by `git grep -cIE`);
        none of the five is a member of
        `contracts/releases/contract-v3.4.digests.yaml`; the Q1/Q3 docs pull
        request **has landed** (PR #786, merged 2026-09-08T12:28:32Z, main
        `e8021fed`; PR #785 at 12:21:55Z); and `openspec validate --all
        --strict` reads **100 passed / 1 failed**, the one failure being
        `disposition-codexfactory-declared-renames` and no other. Recorded with
        the two suite baselines in
        `specs/031-configured-notebook-hosting-identity/research.md` § 0.3.
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

- [x] 2.1 Add ONE resolver, shared by both readers:
      `$XFACTORY_NOTEBOOK_HOSTING_DECLARATION` (absolute or workspace-relative),
      then `<workspace>/.xfactory/notebook-hosting.yaml`'s `declaration_path:`,
      then UNDECLARED. Standard library only — the sync deliberately carries no
      YAML dependency and this must not introduce one.

      - REALIZED 2026-09-08. `hosting_declaration_path(root)` in the sync and
        the same order in the validator. **TWO IMPLEMENTATIONS OF ONE ORDER,
        declared rather than quiet**: the sync could not share the validator's
        code because it must stay YAML-free and because it is HANDED its
        workspace root (walking outside it would let a real machine's
        configuration reach into a temporary tree), while the validator takes no
        root and discovers one. What is shared is the order, the variable name,
        the configuration path and the marker, and
        `TheResolutionOrderIsOneOrderTests` drives BOTH implementations through
        all three cases so a duplicated order cannot drift. Standard library
        only; no YAML dependency added.
- [x] 2.2 `scripts/sync-notebooklm-books.py`: `HOSTING_REL` becomes the
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

      - REALIZED 2026-09-08. `HOSTING_REL` became `EXAMPLE_REL`, naming the
        shipped fixture for prose and remedies only; the declaration's path is
        the resolver's output. `instance` joined `_HOSTING_SCALARS`.
        **A CONFIGURED PATH THAT IS NOT THERE READS AS UNDECLARED** — not an
        invention: OQ-A's own table states the case ("a checkout without the
        submodule initialized reads as UNDECLARED, which is correct, and is why
        that state must stay non-breaking") — and it now SAYS which of the two
        undeclared reasons applies, because silence would let an operator
        believe the record was read. A file that exists and cannot be parsed
        still fails closed. `enforce_hosting_profile()`'s five steps and every
        pre-existing refusal message are untouched.
- [x] 2.3 `scripts/validate-notebook-projection-hosting.py`: precedence becomes
      `argv[1]`, then the resolver, then `DEFAULT_REL` **as a fixture**. Add
      `--resolved` so the operator check of Group 5 is one scriptable command.
      Keep the not-found message's meaning: an install that has declared nothing
      is a transition state, not a passing one.

      - REALIZED 2026-09-08. Precedence is `argv[1]`, then the resolver, then
        `DEFAULT_REL` as a fixture; `--resolved` added. **`--resolved` ALSO
        REFUSES A RECORD MARKED AS AN EXAMPLE**, which this box did not ask for
        and § 3.4 requires: `--resolved` exists to be the LIVE record's
        conformance evidence, and a green line over a fixture would be evidence
        about a fixture. The not-found message keeps its meaning and now names
        which arm resolved the path.
- [x] 2.4 Add the four tests the resolver owes:
      env-var resolution; workspace-config resolution; absent configuration is
      UNDECLARED and the sync runs unbound exactly as it does today; a
      configured path resolving to the shipped example is REFUSED and the
      message names the file and the remedy.

      - REALIZED 2026-09-08. The four owed, plus six the design commits to:
        env-var resolution (absolute and workspace-relative), workspace-config
        resolution, env-over-config precedence (D-1), absent configuration is
        UNDECLARED and the run continues unbound, a configured path that does
        not exist is UNDECLARED, the shipped example is not the last resort, an
        empty environment value is unset, the example refusal fires and names
        the file and the remedy, the marker is read from the RECORD and not the
        path, and a record marked `live` (or unmarked) binds. **Twenty-four new
        tests** across the two modules (eleven in the sync's, thirteen in the
        validator's) plus three new subtests; none added skipped.
- [x] 2.5 Prove the resolver is behaviour-preserving BEFORE anything moves: with
      configuration pointing at the current committed path, every existing
      `tests/notebooklm/` test passes unchanged. This is the box that makes
      Group 5 safe.

      - REALIZED 2026-09-08, and PROVEN DIRECTLY rather than inferred. With
        configuration pointing at the still-committed record,
        `read_hosting_declaration()` returned the **byte-identical dict** the
        old constant produced, in all three spellings (workspace-relative env,
        absolute env, workspace config), and returned None with nothing
        configured — compared by equality against the pre-change module loaded
        from `origin/main`, values elided. The 126 existing tests then passed
        with every assertion structurally unchanged: only the shared
        `_declare_hosting()` helper (which now writes the configuration beside
        the record) and the fixture literals moved.
      - **AND THE PROOF FOUND A DEFECT WORTH THE BOX.** Three tests were
        passing by coincidence: `enforce_hosting_profile()` calls
        `profile_account()`, which reads the OPERATOR'S REAL
        `~/.notebooklm-mcp-cli` store, and on the authoring machine that
        store's recorded address EQUALLED the fixture literal. A synthetic
        literal turned the coincidence into a failure.
        `_HostingResolverCase` now isolates both the resolver's environment
        variable and that store, so a local run reproduces CI instead of
        reaching outside the harness.
- [x] 2.6 `.gitignore` the workspace configuration file, and state in its own
      header that it is per-machine and carries no secret — a path is not a
      credential, and nothing about this file should invite one.

      - REALIZED 2026-09-08. `.gitignore` covers `.xfactory/`, and the ignore
        entry's own comment states that the file carries a PATH and no secret,
        that the credential is held by the binding the record's `custody:`
        block names, and why the answer is per-machine (an operator's checkout,
        a public clone and a CI runner are three different answers, and the
        third is "nothing").
        **NOTE FOR THE OPERATOR:** the file sits at the WORKSPACE root, which
        for the aggregation layout is `opensoft/xFactory`, not this repository —
        so that repository's own `.gitignore` wants the same entry. Out of this
        feature's scope (it is a third repository) and named here rather than
        left to be discovered.
## 3. The public instance becomes synthetic

**Gated on 2.5 green AND Group 5 complete.**

- [x] 3.1 Rewrite `examples/notebook-projection-hosting.yaml` as a SYNTHETIC
      instance: `hosting.account`, `hosting.migration.from_account`, every
      `share_out[].hosting_account` and `[].user`, and the `denied[]` row go to
      `example.invalid` addresses (D-3); `hosting.domain` matches the synthetic
      account's domain, because the validator compares those two fields.

      - REALIZED 2026-09-08. Every identity-bearing value is
        `example.invalid` (D-3), and `hosting.domain` matches the synthetic
        account's domain because the validator and the sync both compare those
        two fields. `custody.binding_client` also went synthetic
        (`example-operator`): it names a real client in the live record and a
        synthetic instance should not point at one.
- [x] 3.2 Mark it in the record — `hosting.instance: example` (OQ-C) — at the
      two-space indent the sync's narrow reader parses, not in a comment. A
      comment is invisible to the reader that must refuse it.

      - REALIZED 2026-09-08. `hosting.instance: example`, first key under
        `hosting:` at the two-space indent the narrow reader parses. Verified by
        driving that reader over the shipped file: it reports
        `instance == 'example'` and `enforce_hosting_profile()` refuses.
- [x] 3.3 Keep the SHAPE byte-for-byte (D-4): same keys, same order, same
      comment structure, same roster arity. Rewrite the prose comments so they
      describe the SHAPE rather than Opensoft's history — the migration
      narrative, the 2026-08-27 rulings and the denial's reasoning belong to the
      live record, which now holds them.

      - REALIZED 2026-09-08. Same keys in the same order, same roster arity
        (7 grants, 1 denial), same comment structure — proven by a structural
        key-order comparison against the live record in its new home:
        `same keys in the same order: True`. The prose comments now describe the
        SHAPE; the migration narrative, the 2026-08-27 ruling and the denial's
        reasoning moved with the live record, which holds them.
- [x] 3.4 Take the actor names to role placeholders (OQ-D), keeping
      `share_out[].granted_by` equal to `approval.designated_actor` — the
      validator refuses them unequal, so this is one edit in two places.

      - REALIZED 2026-09-08. Two role placeholders, not one, because the roles
        differ: `The Install's Declaring Operator` for `hosting.declared_by`,
        and `The Designated Company-Policy Actor` for `approval.designated_actor`,
        `approval.declared_by`, all seven `granted_by` and the denial's
        `decided_by`. The validator's `granted_by == designated_actor` equality
        holds.
      - **DATE FIELDS WERE KEPT AS THEY WERE**, deliberately: this box and 3.1
        enumerate the identity-bearing values, and a date is not one. A
        synthetic actor granting a synthetic user on a real date asserts nothing
        about anybody, and the format is part of the shape a fixture proves.
- [x] 3.5 Prove it: `python3 scripts/validate-notebook-projection-hosting.py`
      exits 0 over the synthetic instance, and
      `test_the_committed_record_conforms` — re-aimed and renamed to say what it
      now asserts — passes.

      - REALIZED 2026-09-08. `python3
        scripts/validate-notebook-projection-hosting.py` -> **`0 error(s)`** over
        the synthetic instance, and `test_the_committed_record_conforms` is
        renamed `test_the_committed_example_conforms` with its assertion intact
        and its docstring stating what it now asserts and what replaced the rest.
- [x] 3.6 Leave `examples/lifecycle-notebook-workspaces.yaml` ALONE. Its two
      lines are comments and belong to the Q1 docs pull request; touching it
      here would make one file the subject of two lanes.

      - HELD 2026-09-08. `examples/lifecycle-notebook-workspaces.yaml` is
        untouched on this branch (`git diff --stat` names it nowhere).
## 4. The test fixtures

- [x] 4.1 `tests/notebooklm/test_nlm_auth.py`: `STORED` and `LEGACY` become
      synthetic. They are compared against each other and against captured
      values inside the harness, never against a live account, so the
      account-mismatch and carry-forward tests keep their exact meaning.

      - REALIZED 2026-09-08. `STORED` / `LEGACY` synthetic, with the reason
        beside them: both are compared against each other and against values
        captured inside the harness, never against a live account.
- [x] 4.2 `tests/notebooklm/test_sync_notebooklm_books.py`: `HOSTING_DECLARED`
      and `HOSTING_PENDING` fixture texts and the eleven assertions over them go
      synthetic. Keep the PENDING assertion that the run binds where the books
      actually live — it is the one that proves "a declaration is not a
      migration", and it works on any address.

      - REALIZED 2026-09-08. `HOSTING_DECLARED`, `HOSTING_PENDING`,
        `MigrationStateVocabularyTests.BASE` and every assertion over them.
        The PENDING assertion that the run binds where the books actually live
        is kept and now names the synthetic previous host. The
        unreadable-shape fixtures' made-up local part on a real domain also
        moved to `example.invalid`, so this file carries ONE synthetic
        convention rather than two.
- [x] 4.3 `tests/notebooklm/test_validate_hosting.py`: `BASE`, `ENTRY` and the
      eight assertions over them go synthetic. Keep every negative mutation
      firing for its stated reason — service account, consumer account, domain
      mismatch, roster-key collision, `granted_by` disagreement.

      - REALIZED 2026-09-08. `BASE`, `ENTRY`, `FIELDS` and the assertions over
        them; the roster users' `@example.com` moved to `@example.invalid` for
        the same one-convention reason (D-3 rejected `example.com` as a real
        registered domain). Every negative mutation still fires for its stated
        reason — service account, consumer account, domain mismatch,
        roster-key collision, `granted_by` disagreement — and the suite proves
        it: 58 tests in that module, up from 45.
      - **ACTOR NAMES IN THE TESTS WERE LEFT ALONE**, and that is a scope
        judgement rather than an omission. OQ-D rules role placeholders for THE
        SYNTHETIC INSTANCE; `Brett Heap` is not in the sheet's four-address set,
        and the packet's own § *What this deliberately does not change* forbids
        widening scope quietly. If the actor should go synthetic in the fixtures
        too, that is one further edit and a word.
- [x] 4.4 Re-run the whole suite and check the `pytest-suite` pins: SKIPPED must
      not move (no test is added skipped), SELECTED and PASSED may only rise,
      and the floors are raised deliberately with the four new tests as the
      reason.

      - REALIZED 2026-09-08. `tests/notebooklm` 251 passed / 40 subtests (was
        250 pre-change over 227 tests); the targeted suite
        `tests/notebooklm tests/doc-health tests/sequenced_after` **2021 passed,
        37 subtests** against a **1997 passed** baseline. **NO TEST IS ADDED
        SKIPPED, SO NO PIN MOVES AND `.github/workflows/pytest-suite.yml` IS
        NOT TOUCHED** — and the floors are deliberately NOT raised, which is
        the one place this box could be read as asking for something the
        workflow forbids: its own comment says "(MIN_SELECTED and MIN_PASSED are
        FLOORS and need no edit: the new module only raises the actuals, which
        widens the printed margin)", and it pins its numbers to a CI run because
        a developer worktree measures a different SKIPPED. Raising a floor to a
        locally measured number is exactly what that file refuses.
- [x] 4.5 Sweep for a missed literal:
      `git grep -nE "<the four addresses>" -- tests/ examples/ scripts/ openspec/specs/`
      returns nothing. File the output as the realization evidence.

      - REALIZED 2026-09-08. `git grep -nE '<the four addresses>' -- tests/
        examples/ scripts/ openspec/specs/` returns **exactly ONE line**:
        `openspec/specs/lifecycle-notebook-projection/spec.md:459`. Over the
        WHOLE tree it returns the same one line and nothing else — 39 of the 40
        are gone. That last line is the promoted spec's identity bullet, which
        task 1.1 reserves for the archive act and forbids editing by hand, so
        the sweep is empty in every file this feature is permitted to touch.
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

- [x] 6.1 `docs/lifecycle-notebook-projection.md` § *The declaration* and § *The
      approval lane*: describe the two-file model — the synthetic instance here,
      the live record resolved from configuration, the resolution order, and the
      operator check that replaces the CI one. **Sequenced after the Q1 docs
      pull request** (it redacts three address lines in this same file; 0.3
      checks that it landed).

      - REALIZED 2026-09-08. § *The declaration* now opens on the two-file
        model, states why two files rather than one redacted file, carries the
        resolution order as a block with its three deliberate properties, and
        names the three things that replace the lost CI check including the
        `--resolved` operator command. § *The approval lane* stops naming a
        person and a file that is now a fixture: the actor is named in an
        install's own live declaration, and the committed example's actor is a
        role placeholder by OQ-D. § 1's pointer at the top of the document moved
        with them.
- [x] 6.2 `docs/notebook-projection-migration-runbook.md` and
      `docs/notebooklm-sync-open-item.md`: update the four path references that
      now resolve differently. Prose redaction in those files is Q1's, not this
      change's — touch only the structural claims.

      - REALIZED 2026-09-08. `docs/notebook-projection-migration-runbook.md`
        (step 1a's custody pointer, step 3's flip, step 9's roster write) and
        `docs/notebooklm-sync-open-item.md` (§ Account, and the realization
        note) now say the declaration is resolved from configuration. Step 3
        gained the `--resolved` proof line. Prose redaction in those files was
        Q1's and had already landed.
      - **`docs/notebook-projection-migration-evidence-2026-08-24.md` WAS LEFT
        ALONE.** Its reference is a dated record of where the declaration was on
        2026-08-24, which was true then; rewriting a dated evidence record to
        describe a later structure would falsify it. This box names the runbook
        and the open item, and those are what moved.
- [ ] 6.3 `README.md`: move this change's OpenSpec Records entry from proposal
      to realized/archived state at the archive act, and add the doc index line
      if a section title moved.
- [ ] 6.4 File the realization evidence: the sweep output from 4.5, the resolver
      test names, the `--resolved` green line from 5.2 (values elided), and the
      pytest pin deltas.

      - PARTLY FILED 2026-09-08 and DELIBERATELY NOT TICKED. Everything this
        feature can supply is in
        `specs/031-configured-notebook-hosting-identity/evidence/realization-2026-09-08.md`:
        the 4.5 sweep output, the twenty-three resolver test names, the 2.5
        equality proof, the two validator green lines, the pytest and doc-health
        deltas, and the pin non-movement with its reason. **The one item it
        cannot carry is the `--resolved` green line, which is 5.2's and is the
        operator's to produce** — so the box stays open rather than being
        ticked on four fifths of its content.
- [ ] 6.5 Re-run the sweep ledger at the realization head
      (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<PR>'`) and confirm the diff is this change's own row.

      - RUN READ-ONLY 2026-09-08, NOT TICKED. `python3
        scripts/validate-sequenced-after.py .` at the realization head ->
        **`sequenced_after validation passed (41 active changes, 7 declaring the
        field)`**, so this change's row is intact and no partner row moved. The
        box asks for the `--seed-ledger --moved-by '#<PR>'` form, which WRITES
        the ledger against a pull-request number — that is a landing act with a
        number this branch does not yet have, so it belongs to the merge or the
        archive and not here.
- [ ] 6.6 Archive only when `release-realization`'s gate is satisfiable: the
      code surface merged on openxFactory main and green — the pytest suite with
      the new fixtures, the validator over the synthetic instance, and the
      operator's `--resolved` line for the live record. A doc-only archive is
      not available to this change; its surface is not `none`.
