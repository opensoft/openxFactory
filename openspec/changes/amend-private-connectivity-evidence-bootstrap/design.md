# Design: Source-only evidence bootstrap custody

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [amend-private-connectivity-evidence-bootstrap](proposal.md).

## Context

See [proposal](proposal.md). The accepted E scope covers four helper/test files, three shared-reader/regression files, one workflow and T010.json. The 043 [evidence contract](../../../specs/043-private-connectivity-production/contracts/task-evidence.md) requires authenticated original bootstrap outputs and a reviewed frozen manifest; it does not authorize additional export paths. T009 correctly declares its empty production pin population FUTURE. The frozen T010 file list cannot promote that population when the first real record arrives.

## Goals / Non-Goals

**Goals:** Provide exact durable source-only commissioning storage, avoid self-referential receipt hashes, preserve original command/source/output identities and separate scope ratification from actual custodian authentication. Make T010's first-record transition explicit.

**Non-Goals:** Approve unseen evidence, invent T001–T009 task receipts, select live protected custody, modify customer/provider state, relax pin reachability or numerical floors, enter Q1–Q5, or publish a contract/release.

## Decisions

### Exact additional records and T010 refinement

The proposed additional records are exactly:

| Path | Purpose |
| --- | --- |
| specs/043-private-connectivity-production/evidence/commissioning.json | Reviewed source-only control manifest, original bootstrap/CI exports and authenticated contained objects |
| openspec/changes/commission-private-connectivity-production-evidence/review/commissioning-authentication.md | Actual custodian review of source/output/command identities and human-decision provenance; draft until that review occurs |

No other export directory or file prefix is granted. The following is the complete proposed T010 files field:

- .github/workflows/pytest-suite.yml
- specs/043-private-connectivity-production/evidence/T010.json
- specs/043-private-connectivity-production/evidence/commissioning.json
- openspec/changes/commission-private-connectivity-production-evidence/review/commissioning-authentication.md
- scripts/doc_health/pin_class.py
- tests/doc-health/test_sentinel_vocabulary.py

The last two files already belong to the accepted E scope; this change assigns their measured first-record promotion to T010. T009 still implements and tests the initial registration before T010. The existing verifier/inventory helpers and their two test modules remain their own accepted T007/T008 implementation surfaces, with affected revalidation for the contained-object format. No owner, dependency, required case, task identity, verification command or live gate changes.

After actual ratification, update only the necessary working evidence contract/owner/commissioning handoff and T010 file list, recompute the complete review freeze and retain the prior identity. Before ratification, leave the current frozen implementation contract in force. Feature coordination documents, this packet, the README index and the sanctioned generated ledger remain governance/handoff surfaces.

### One source-only commissioning container

Use the reviewed manifest format with a closed contained-object table. The operator's independent trust anchor remains the complete coordinator commit, path and SHA-256. A contained-object reference carries only a closed opaque object identity; its authentication derives from that containing immutable manifest, not a caller-selected file, command, URL or verdict.

Required checks include unique object identities/JSON keys, existence, cycle refusal, exact task/case/scope/source/command identity, original immutable source/governance references, current human authority and actual required CI results. Contained objects admit only E bootstrap/source/CI material. Live or customer/provider evidence requires its later separately accepted custody and cannot be introduced by changing a contained object's class.

T001–T009 retain their original outputs and approvals as authenticated imports inside the container; no T001.json–T009.json files are created. The T010 receipt is a distinct file and may refer to authenticated source objects. The commissioning manifest may subsequently bind that receipt's immutable Git reference without changing the receipt or requiring the receipt to know its own containing commit/hash. Tested source, output-containing commits, receipt-containing commits and the final reviewed manifest are distinct identities.

Original command output and its source/exit/timing identities remain inspectable. Redacted exports record their original content digest and actual redaction method; normalization cannot remove provenance to avoid pin coverage. An importer must fail if original case/command/source/outcome evidence is unavailable. Human authentication is not inferred from a structurally valid export.

An alternative with many per-command JSON export files is rejected because it expands the accepted file surface and ownership/census obligations without improving the source-only custody boundary. A self-referential T010 receipt/manifest is rejected because its content hash cannot authenticate itself. Ignoring bootstrap provenance or moving pins to unswept extensions is rejected because it weakens the accepted evidence contract.

### First real pin population

Add only the exact commissioning JSON path beside the already closed production coordinator receipt/instance paths. Preserve local MUST_RESOLVE and explicit foreign ownership/reachability, unknown-path refusal and feature 040 registration. No prefix exclusion or ROLLING population is introduced.

T009's empty production members remain FUTURE until the actual commissioning/T010 records are committed. At T010, deliberately promote only members with actual committed sites, measure their standing site/member deltas from that tree, and update only the directly affected census assertion/comment. A foreign member with no actual foreign site remains FUTURE. Never mark absent data CURRENT, fabricate a witness, or guess the numeric delta.

Inventory generation and check remain distinct. Check is read-only; generation may change only an explicitly accepted new draft. Accepted observations are immutable. A later commissioning revision preserves the earlier reviewed container and its history in Git and is a newly reviewed control input, not a rewrite of the prior accepted observation.

### Two real owner decisions

First, Brett Heap reviews and ratifies this exact source/file/task refinement. That enables source implementation and preparation of the proposed exports. Second, the custodian reviews the actual original bootstrap/CI outputs, source/command bindings and human provenance, and records their authentication before the final manifest anchor is used for T010 acceptance.

The existing source-only C-08 policy remains: reviewed/redacted source exports in openXfactory Git, project-lifetime retention, existing repository access, exact commit/content identity, actual GitHub repository/run/job/output identity and Brett's review. Sensitive provider/customer data and future staging/production custody are excluded.

## Risks / Trade-offs

- A generated control file could be mistaken for owner approval → keep draft/accepted states distinct and require the actual authentication record and independently selected immutable anchor.
- A single container could conceal mixed sources → freeze each contained identity, class, task and command, retain original outputs and reject unresolved/cyclic references.
- The first record can move pin census and expose missing foreign checkouts → measure from actual committed data, retain foreign ownership proof and stop rather than suppress an uncovered path.
- Existing bootstrap logs may lack required provenance → report the missing evidence and rerun only genuinely repeatable source checks; preserve original human decisions and never manufacture historical execution.

## Migration Plan

Keep PR #1310 draft. Ratification precedes contract/scope edits and new record creation. Preserve the prior freeze, refine T010, implement and test the source-only container/inventory handling, then prepare the actual exports and obtain custodian authentication. Wire/verify the exact collected feature suites, commit actual source evidence, deliberately promote/measurably census its pins and run the required T010 check. Stop at missing evidence or approval; continue independently ready owner-proposal preparation.

On failure, retain failed/blocked evidence and the prior reviewed manifest; supersede with a reviewed corrected source input and rerun affected controls. Never disable a required check, overwrite accepted observations, advance a live gate or claim an archive as rollback.
