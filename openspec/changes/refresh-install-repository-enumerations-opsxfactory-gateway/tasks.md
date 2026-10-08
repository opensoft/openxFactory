# Tasks: refresh-install-repository-enumerations-opsxfactory-gateway

Status: draft
Kind: tasks
Lane: openxfactory-5 (openXfactory-5)

`code_surface: none`, `target_release: implemented`. Under `release-realization` this
packet therefore archives on LANDING plus this task list, not on merged-plus-green
realization evidence, and its one owed act is § 4.1, the `## Purpose` widening that
cannot ride in a delta. § 1 is the owner's acts, § 2 is what this packet itself
authored and measured, § 3 is what it does NOT do, and § 4 is the archive.

**WHAT IS TICKED AND WHAT IS NOT, STATED SO NO TICK IS READ AS MORE.** § 2 is ticked
because it is the evidence the packet is reviewable at all, and each box names the
command that produced it. § 1, § 3 and § 4 are UNTICKED by design. § 1 is Brett
Heap's, § 3's boxes are statements of what this packet does not do and are confirmed
at the archive, and § 4 is the archive act itself. No promoted specification byte
moves, no `## Purpose` is edited, no issue is closed and no repository is touched
anywhere in the estate by this packet: canon is written by the archive act, on a
separate word.

## 1. Ratification and landing (Brett Heap's acts, not this lane's)

- [ ] 1.1 Ratify this packet. Brett Heap's word on the pull request or on
      openxFactory#1259; the packet is `Status: draft` until then. His word of
      2026-10-08, *"Lane 5 indexes it now (Recommended)"* (logged RULED in
      `lanes/log/openXfactory-5.md` at 2026-10-08T18:36:12Z), commissioned the
      authoring and ratifies no text: it names no wording, no scope, and no answer
      to either open question.
- [ ] 1.2 The two open questions are put to him verbatim in the pull request body and
      stand or fall on their own:
      - **OQ-1** (`design.md` D4) — the gateway joins *"Contract breaks an adapter"*
        as the adapter family `Ops-gateway` (recommended: yes). Refusing it deletes
        `specs/canonical-contract-migration/spec.md` and nothing else moves.
      - **OQ-2** (`design.md` D3) — a routing scenario for the gateway in
        *"Install repository scope"* (recommended: no). Taking it adds ONE scenario to
        that block, worded in D3, and nothing else moves.
- [ ] 1.3 On ratification, flip `Status: draft` to `Status: ratified` in `proposal.md`,
      `design.md` and this file, add the `Ratified:` / `Ratified by:` line naming the
      word and its date, add `approved_by` and `approved_on` to `.openspec.yaml`
      BESIDE the drafting provenance (`kind`, `id` and `reason` unmoved, the
      addition-not-rewrite shape `add-drafted-proposal-origin` defined), write
      `review/ratification-<date>.md` as `Status: record`, and move the README row's
      status wording. **Ratification performs no realization**: no delta is promoted,
      no Purpose is widened, no box in § 3 or § 4 ticks on it, and #1259 stays open.
- [ ] 1.4 A land word, then an archive word. Each is a separate act on a separate word
      and neither is implied by § 1.1. #1259 closes at the archive (§ 4.2), by a word,
      and on no earlier pull request.

## 2. Authoring and validation (this lane's act, done before the pull request)

- [x] 2.1 Three spec deltas authored, BUILT from the promoted text programmatically by
      slicing each requirement block out of canon at `main` `e83259b4` and applying one
      exact single-occurrence substitution per unit, the builder refusing on any other
      count, rather than retyped, so no unit is dropped by transcription:
      `specs/repo-boundary-governance/spec.md` (3 MODIFIED: *Canonical workflow
      authority*, *Install repository scope*, *Copy-first migration*),
      `specs/shared-contract-ownership/spec.md` (1 MODIFIED: *Contract version
      pinning*), `specs/canonical-contract-migration/spec.md` (1 MODIFIED: *Contract
      provenance and compatibility*): **5 MODIFIED, 0 ADDED, 0 RENAMED, 0 REMOVED**.
      Measured with the family's own `derive_units` over canon's block and the delta's
      block: four blocks change exactly ONE scenario bullet (a two-line textual diff
      each, the old bullet and the new), and *Install repository scope* changes
      exactly ONE body sentence (the list sentence, its last line) and ADDS one
      paragraph of two sentences; every other unit of every block is carried. The
      requirement text inherited from canon carries no marker forward, a marker not
      being a carriage unit (`doc-health` *Currency of an active change's MODIFIED
      requirement blocks*).
- [x] 2.2 Every MODIFIED block carries ONE `**Removed from canon by
      refresh-install-repository-enumerations-opsxfactory-gateway (2026-10-08):**`
      marker naming the replaced sentence or bullet as a CommonMark code span (fenced
      with a longer backtick run where the unit itself contains backticks) and a reason
      beginning at the first ` — ` standing outside every span. Verified with
      `scripts/doc_health/modified_block_currency.py`'s own `parse_marker`: **FIVE
      markers, exactly ONE name each**, so the names the checker reads are the names
      the author intended and no marker names a unit its block does not replace.
- [x] 2.3 `.openspec.yaml` carries the ad-hoc origin declaration written by
      `python3 scripts/proposal-support.py . declare-adhoc` with DRAFTING provenance only
      (`proposed_by` and `proposed_on`, no `approved_by`, no `approved_on`), the lawful
      unapproved shape `add-drafted-proposal-origin` defined, plus a `related:` list.
      `python3 scripts/proposal-support.py . verify
      refresh-install-repository-enumerations-opsxfactory-gateway` passes.
- [x] 2.4 One row added at the head of README's *"OpenSpec Records"* active-changes block,
      in the block's own newest-first order. That block is substrate-claimed on
      openxFactory#630 (comment 6066626855) for this one row; nothing else in README is
      touched.
- [x] 2.5 One row seeded into `tests/sequenced_after/corpus-ledger.yaml` by
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`.
      Measured shape: `{state: active, class: co-modifier, declares:
      [refresh-install-repository-enumerations,
      amend-repo-boundary-governance-scope-first-line], depth: 2, prose: false}`.
      `co-modifier` because the ledger's corpus includes ARCHIVED changes that wrote the
      same keys, not because a live change collides (`design.md` D2). The diff is the
      check: **EXACTLY ONE ROW MOVED**, this change's own, and `--ledger-diff` reads
      consistent at the head the pull request body cites.
- [x] 2.6 Validation run and reported in the pull request body, every command with its
      result and the comparison against `main` in the same clone kind: the pinned
      `python3 scripts/validate-openspec-cli-pin.py --all --strict`;
      `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`;
      `python3 scripts/proposal-support.py . verify
      refresh-install-repository-enumerations-opsxfactory-gateway`; `python3
      scripts/doc-health.py --single-repo . --fail-on error`, compared finding for
      finding against `main`; the `tests/sequenced_after`, `tests/doc-health` and
      `tests/proposal-support` suites and the full `tests/` run CI's `pytest-suite`
      runs; `git diff --check`; and a scan of every commit message and the pull request
      body for a closing keyword.

## 3. What is NOT done by this packet, stated so no tick can claim it

Confirmed at the archive, each with the measurement that holds on the day.

- [ ] 3.1 **No promoted specification is edited by this packet's diff.**
      `openspec/specs/repo-boundary-governance/spec.md`,
      `openspec/specs/shared-contract-ownership/spec.md` and
      `openspec/specs/canonical-contract-migration/spec.md` are untouched; `git diff
      --stat` names no file under `openspec/specs/`. The archive commit is a different
      act and moves them (§ 4).
- [ ] 3.2 **No generator, checker, script, workflow or test is written.** `design.md` D7:
      the archived refresh refused to derive the enumerations (its D1) and to build a
      checker for the index rule (its D4), and D5 re-measures the fact those refusals
      rest on. A ledger row is a data row and not a test.
- [ ] 3.3 **No contract is added, changed or cut.** `contracts/manifest.yaml`,
      `contracts/README.md` and `contracts/CHANGELOG.md` are untouched, no digest
      inventory moves, no `contract_bundle_version` is allocated, and no annotated tag
      is owed.
- [ ] 3.4 **No repository is created, admitted, renamed, re-pinned or retired**, no
      submodule pointer moves in any repository, and nothing is edited in any other
      repository. `OpsxFactory-Gateway-Install`'s admission already happened
      (opensoft/xFactory#567); this packet only writes it into the index.
- [ ] 3.5 **No boundary requirement is authored for `OpsxFactory-Gateway-Install`**, and
      three sites are named and not edited, all UNCLAIMED candidates:
      `contracts/README.md` line 18 and `docs/repo-boundary-pilot-plan.md` line 100
      (an editorial release-inventory member and a dated pilot record, as the archived
      refresh found), and `scripts/estate-repository-inventory.yaml`, the estate's
      governed inventory, a data file read by validator code that carries no row for
      the repository. Adding that row is a code-surface edit under
      `release-realization`'s own capability and is not this packet's.
- [ ] 3.6 **Three requirements are not edited**: *"Submodule sequencing"* (its
      scenario already ends *"or a later install repository"*), *"Install repo scope
      links"* (per-repository README scenarios, not an index) and *"Install-repository
      enumerations are an index with a named authority"* (its nine-against-five count is
      a dated measurement; `design.md` D5 records today's ten-against-six).

## 4. Owed at the archive (the archive act, on a separate word)

`code_surface: none`, so per `release-realization` this change archives ON LANDING
rather than on merged-plus-green realization evidence. These boxes tick in the archive
commit itself and the archive lands by merge commit.

- [ ] 4.1 **THE `## Purpose` WIDENING, IN THE ARCHIVE COMMIT, IN A HUNK SEPARATE FROM
      THE PROMOTION, WITH THE SENTENCE QUOTED IN THE TICK AS WRITTEN.**
      `openspec/specs/repo-boundary-governance/spec.md`'s `## Purpose` names
      `openxFactory` and five install repositories, and a `## Purpose` in a delta is
      read only at capability creation, so this edit is made in the PROMOTED
      specification after the archive has written the deltas into canon. The proposed
      sentence, so the edit is reviewable BEFORE it is taken:

      > Defines how `openxFactory`, `Hermes-Install`, `Omnigent-Install`,
      > `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`, and
      > `OpsxFactory-Gateway-Install` assign canonical workflow policy ownership,
      > install repository scope, copy-first migration rules, and guarded
      > repo-boundary execution.

      The edit is a sixth name appended and canon's own `and` standing before the last
      name, the serial comma kept; every other word is canon's. Nothing else in the
      Purpose block is touched, and no `Removed from canon` marker is owed, a Purpose
      carrying no `SHALL`. The tick quotes the sentence and measures the edit token by
      token, as the archived refresh's § 4.1 did.
- [ ] 4.2 **Close openxFactory#1259** with the archive commit named, on Brett Heap's
      closing word, recording in the closing comment: which units widened (the five
      MODIFIED blocks and the `## Purpose`), the site that needed no edit (*"Submodule
      is proposed"*), the outcome of OQ-1 and of OQ-2, and that no boundary requirement
      was authored. The issue closes because the enumerations moved, not because a
      successor was named, and no closing keyword appears in this packet's pull request
      body or in any commit message before the archive.
- [ ] 4.3 Move the README *"OpenSpec Records"* row from the active block to the archived
      block, and re-seed the ledger row (`state: active` to `state: archived`,
      `moved_by: "#<archive PR>"`, `moved_on` the date its
      `archive/<YYYY-MM-DD>-refresh-install-repository-enumerations-opsxfactory-gateway`
      directory carries) with `python3 scripts/validate-sequenced-after.py . --seed-ledger
      --moved-by '#<archive PR>'`, `class:` and `declares:` unmoved. Re-run `--ledger-diff`
      clean at the head the archive record cites, and report the one row that moved.
- [ ] 4.4 Re-run the collision measurement of `design.md` D2 against the active corpus on
      the day of the archive, because it is a statement about the active corpus and the
      corpus moves: no other active ratified change may write any of the five requirement
      keys. If one does, STOP and rule the order under `release-realization`'s
      ordered-deltas rule before archiving.
