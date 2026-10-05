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

- [ ] 3.1 Review and land realization through the authorized repository process; verify exact merged revision and green checks, respecting sibling and shared-substrate claims.
- [ ] 3.2 Archive only after merged green realization; verify promoted requirements and preserved provenance under the archive gate. Release cuts, hosted acceptance and consumer adoption remain separately governed.

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
