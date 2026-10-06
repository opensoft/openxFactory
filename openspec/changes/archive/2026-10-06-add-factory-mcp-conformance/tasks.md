# Governance and realization handoff

Lane: mcp-family-contract

These are governance checkpoints. The single Speckit feature created at 2.1
will own executable implementation tasks; this file does not duplicate them.

## 1. Proposal and ratification

- [x] 1.1 Capture design and write proposal, design and scenario-complete delta; verify all artifacts exist and every requirement has scenarios.
- [x] 1.2 Validate the exact proposal and origin and record a consistency review; per-change checks pass and unrelated baseline findings are recorded in review/validation-2026-09-07.md.
- [x] 1.3 Brett Heap ratified this exact packet and ad-hoc origin on 2026-09-07; review/ratification-2026-09-07.md names the reviewed revision.

## 2. Speckit realization

- [x] 2.1 Created `specs/037-factory-mcp-conformance/` from the clean ratified design branch; spec and plan trace to this delta.
- [x] 2.2 Completed clarify, plan, six domain checklists, tasks and cross-artifact analysis in that feature; no critical findings. See the feature spec, plan and tasks for coverage.
- [x] 2.3 Local implementation and verification complete; see specs/037-factory-mcp-conformance/verification.md for deterministic evidence, required checks and existing baseline limitations. Review/merge/archive remain open.

## 3. Review and closure

- [x] 3.1 Review and land realization through the authorized repository process; verify exact merged revision and green checks, respecting sibling and shared-substrate claims.
  **Landed and green.** Verified 2026-10-06 by lane openxfactory-5
  (openXfactory-5) from the repository and its check runs, not from a handoff.
  - **Landing.** Pull request
    [#1243](https://github.com/opensoft/openxFactory/pull/1243) merged into
    `main` at 2026-10-06T03:37:58Z as
    `92010d3e67f2c556687e1c3583ed3ca1867f4b8b`, on Brett Heap's word *"land
    #1243 when green"* (2026-10-05). It landed by squash: `92010d3e` has the
    single parent `ba89e046`, and its tree `fd3b9f08` is the tree of the pull
    request's final head `6ab7126724bf7d5771d3929934ed0b28d29ea0aa`. The checks
    at that head therefore cover exactly the merged bytes.
  - **Green at the head.** Every context `main`'s ruleset requires passed at
    `6ab71267`: `signed-execution-chain-gate`, `lane-line`,
    `former-id-arrival-gate`, `openspec-cli-pin`, `wallet-validation`,
    `pytest-suite`, `release-tag-gate` and `openxdox-consumer-gate`. The
    `pytest-suite` run
    [37407361293](https://github.com/opensoft/openxFactory/actions/runs/37407361293)
    reads `selected=9831 passed=9825 skipped=6 failures=0 errors=0`. SonarCloud
    Code Analysis is not required; it failed on one S8707 finding (the CLI opens
    the declaration path its operator passes), which was dispositioned before
    the landing as accepted by design for an offline validator
    ([#1243 comment 6008804840](https://github.com/opensoft/openxFactory/pull/1243#issuecomment-6008804840)).
  - **Green on `main`.** `pytest-suite` ran on push at `92010d3e` itself, run
    [37409899722](https://github.com/opensoft/openxFactory/actions/runs/37409899722),
    success, with the same counts line. It passed again at `main` `51456835`,
    run
    [37480682619](https://github.com/opensoft/openxFactory/actions/runs/37480682619).
  - **The realization is whole on `main`.** The declared code surface is
    present: `contracts/factory-mcp/`, `scripts/validate-factory-mcp.py`,
    `tests/factory-mcp/` and `docs/factory-mcp-conformance.md`. The Speckit
    feature `specs/037-factory-mcp-conformance/tasks.md` has 16 of 16 boxes
    ticked. No commit after `92010d3e` touches the code surface, the feature
    or this packet.
  - **Claims respected.** Lane openXfactory-5 claimed the governing issue
    [#1242](https://github.com/opensoft/openxFactory/issues/1242) (comment
    5999969334), posted `LANDING` and `LANDED` on #1243 under lane-collision
    Rule 6 (comments 6008827123 and 6008830619), and released the claim
    (#1242 comment 6008836688).
  - **Correction to the addendum below.** The addendum was written before the
    landing and says the original commits are ancestors of the landing. The
    squash landing makes that true of the pull request's head and not of
    `main`: `d2baf6fd` and the ratified revision `8acd2ec4` are ancestors of
    `6ab71267`, which GitHub keeps at `refs/pull/1243/head`, and neither is an
    ancestor of `main`. The ratified delta is unchanged on `main`: the blob of
    `specs/factory-mcp-conformance/spec.md` is `a4865bd8` at both `8acd2ec4`
    and `92010d3e`.
- [x] 3.2 Archive only after merged green realization; verify promoted requirements and preserved provenance under the archive gate. Release cuts, hosted acceptance and consumer adoption remain separately governed.
  **Ticked before the run, because the archive wrapper refuses an open box**
  (`change has incomplete tasks` while any `- [ ]` line remains). The
  condition this item names is met: 3.1 records the merged, green realization.
  The archive is the governed wrapper's act,
  `TZ=UTC python3 scripts/proposal-support.py . archive add-factory-mcp-conformance --yes`,
  never a bare `openspec archive`. It is prepared on a DRAFT pull request that
  lands by merge commit, never squash, so the archive directory's date keeps
  matching its adding commit. It lands only on Brett Heap's archive word,
  which had not been given when this box was ticked. The run and its
  measurements are recorded under this item in the commit after the move.
  - **The word.** Brett Heap gave it on 2026-10-06, in session, verbatim
    *"archive add-factory-mcp-conformance when green"*. It is RULED in
    `opensoft/brett-wip` `lanes/log/openXfactory-5.md` at
    2026-10-06T17:25:24Z (commit `5f02a237`), against
    `openspec/changes/add-factory-mcp-conformance`. The RULED entry reads it
    as landing this archive's pull request, #1252, by merge commit under a
    Rule 6 window once its gates, checks and Copilot review are green, with
    the *Unavailable dependency* disclosure and the untouched relative link
    below both known. No GitHub comment carries the word; the register entry
    and this citation are its record.
  - **The run.** Performed in commit `7102cd48`, the commit that moves this
    directory:
    `TZ=UTC python3 scripts/proposal-support.py . archive add-factory-mcp-conformance --yes`,
    exit 0, 2026-10-06T16:21:19Z to 16:21:30Z. Its decisive lines:
    `ORIGIN RETAINED add-factory-mcp-conformance (declaration unchanged since
    the ratifying commit 92010d3e67f2)`; `Totals: 1 passed, 0 failed (1
    items)`; `Task status: ✓ Complete`; `factory-mcp-conformance: create`;
    `Applying changes to openspec/specs/factory-mcp-conformance/spec.md: + 8
    added`; `Totals: + 8, ~ 0, - 0, → 0`; `Change
    'add-factory-mcp-conformance' archived as
    '2026-10-06-add-factory-mcp-conformance'`; `NO SUPPORTING DOCS ...
    (origin retained, nothing to package)`. The CLI was the content-addressed
    `@fission-ai/openspec@1.12.0` pin, not the 1.13.1 on `PATH`. `--date` was
    not passed, so the directory takes the UTC day of the run, which is also
    the UTC day of its adding commit.
  - **Promoted requirements, verified by content.** The delta is all
    `## ADDED` over a new capability directory,
    `openspec/specs/factory-mcp-conformance/spec.md`. Its Purpose is the
    delta's own `## Purpose` text, and it holds eight requirements with
    twenty-two scenarios. Each requirement block was extracted by its
    `### Requirement:` heading from this archived delta and from canon, and
    hashed: all eight are byte-identical, and canon holds no requirement the
    delta lacks. Canon goes from 66 to 67 capability directories, and no other
    file under `openspec/specs/` changes.
  - **Provenance preserved.** The nine packet files move as pure renames
    (R100): proposal, design, delta, tasks, `.openspec.yaml`, and the four
    review records, including the ratification record that names the reviewed
    revision `8acd2ec4`. The origin block is unchanged since ratification on
    both histories: on `main` the ratifying commit is the squash `92010d3e`;
    on the original lineage it is `54bce013`; and the `.openspec.yaml` blob is
    `c1e5cd98` at `54bce013` and here. `8acd2ec4`, `54bce013` and `d2baf6fd`
    remain reachable through `refs/pull/1243/head`, a pull-request ref that
    deleting a branch does not remove.
  - **One link inside the packet now resolves one level short.**
    `proposal.md`'s relative link to
    `ideation/brainstorm/factory-mcp-overview.md` was written for the active
    path. Its bytes are kept as ratified, as two earlier archives kept the
    same link shape in three files. Repairing it is a bookkeeping edit of an
    archived record, which needs a ruling recorded first.
  - **Not done here, and separately governed.** No release is cut, nothing
    under `contracts/` changes, and no consumer pin advances. This archive
    settles none of the items still awaiting Brett Heap's rulings: an auth
    and transport block, the home of the family error vocabulary, shared
    transport, and enforcement of the *Unavailable dependency* scenario. The
    validator does not yet enforce that scenario, which canon now states.

## Addendum 2026-10-05: brought onto main

Lane openxfactory-5 (openXfactory-5) adopted this change from lane
`mcp-family-contract` on Brett Heap's word of 2026-10-05, verbatim *"confirm 1,
close 018, adopt the work, re-anchor codexFactory"*, under governing issue
opensoft/openxFactory#1242. It brought the change onto main in pull request
#1243 by MERGING `d2baf6fd`, so the original commits are ancestors of the
landing. The repairs below are non-normative: no requirement or scenario text
changed, and the ratified revision `8acd2ec4` still governs.

- The Speckit feature is renumbered 030 to 037 (`specs/037-factory-mcp-conformance/`),
  because main took 030 on 2026-09-08. Items 2.1 and 2.3 cite the new path.
- `AGENTS.md` keeps main's bytes. The SPECKIT active-plan pointer that main
  retired in `687b85e3` is not re-added.
- The test module is `tests/factory-mcp/test_factory_mcp_conformance.py`. Its old
  basename collided with `tests/corpus-adapter/test_conformance.py` and
  interrupted the required `pytest-suite` at collection.
- The sweep-ledger row is seeded (`--seed-ledger --moved-by '#1243'`).
- `review/ratification-2026-09-07.md` carries `Status: ratified` and a
  `Ratified:` citation, as doc-health `ratified-provenance` requires.
- The README OpenSpec Records row is added. New text names the codex
  repository `codeXfactory/codexFactory`.
- `review/codex-baseline-2026-09-07.md` is reduced to the revision, the three
  schema digests and the compatibility statement. Pull request #1243 lists the
  private-internals passages it removed, for the owner's disclosure decision.
- The validator now meets requirements already ratified, red first (tests
  `d8b2e0cb`, fix `59fbab7b`):
  - embedded `$id` resources (*Offline pinned reference integrity*, *Existing tools*);
  - union inventories through an optional `discriminator`, and coverage of every
    union member (*Lossless results and explicit failures*; design D1, "including
    union variants");
  - strict JSON Pointer indices;
  - stable codes and locations (*Malformed catalog*, *Deterministic validation*);
  - an https-only resource URI, a tool id token, tool schemas tied to `source`,
    and `contentSchema` and `dependencies` walked.

  The declaration schema gained one optional, closed field: `discriminator`.
- Not addressed: enforcing the *Unavailable dependency* scenario, and an
  auth/transport block. Both are normative and await Brett Heap's rulings.

Task 3.1 stays open until the landing, and 3.2 until the archive.
