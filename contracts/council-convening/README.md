# council-convening Contract Family

Status: ratified
Ratified by: renew-resolved-council-protocol (ratified 2026-10-03 by Brett Heap,
*"ratify all three as disclosed"*; record
[`openspec/changes/renew-resolved-council-protocol/review/ratification-2026-10-03.md`](../../openspec/changes/renew-resolved-council-protocol/review/ratification-2026-10-03.md);
packet #1267 merged as `80f47483` on 2026-10-08)
Kind: reference

The neutral provider contract for **the resolved council protocol**. It covers
what the producer of a council convening and its consumer must agree on, and
what neither may invent: the commission record and its resolved, ordered roster;
the frozen snapshot and its per-seat assignments; key registration and signed
seat returns; the producer's workflow binding; and the versioned migration from
the legacy protocol. It is realized by Speckit feature
[`035-renew-resolved-council-protocol`](../../specs/035-renew-resolved-council-protocol/spec.md),
one reviewed pull request per phase.

## DORMANT, UNREGISTERED AND PENDING REALIZATION

**Nothing in this family is published, and nothing in it selects or activates
anything.**

- No file here has a row in [`contracts/manifest.yaml`](../manifest.yaml), and no
  `contract-v*` release includes it. A shape becomes normative only when it lands
  in its phase and a release publishes it: the additive and deprecating minor
  (feature Phase 7) for the replacement, and the removal major (Phase 8) for the
  end of legacy acceptance. The successors may build **dormant** code against a
  reviewed `main` commit after any of Phases 1 to 6, as design D5 allows. They
  activate only against the published releases.
- The replacement protocol `xfc-resolved-council-1` is `available`: selectable
  for rehearsal only. It is not `admission_eligible`, and no record of this
  family can make it active before the removal major and the owner's matched
  activation (FR-011, FR-012).
- The CI gate [`council-convening-gate`](../../.github/workflows/council-convening-gate.yml)
  REPORTS and does not GATE. Making it a required check is an owner act on a
  ruleset.

## What is here at Phase 1

| file | kind | what it is |
|---|---|---|
| [`shared-definitions.schema.yaml`](shared-definitions.schema.yaml) | definitions only | Every grammar the family's records share: identifiers, the candidate, digests by `$ref` to `xfc-jcs-sha256-1`, keys, signatures, decimal strings, and the closed `principal_kind`, `refusal_code` and `finding_code` enumerations. |
| [`protocol-registry.schema.yaml`](protocol-registry.schema.yaml) + [`protocol.registry.yaml`](protocol.registry.yaml) | `xfactory_council_protocol_registry` | The CLOSED protocol registry, schema plus its one instance: the replacement `xfc-resolved-council-1` (`available`) and the legacy `xfactory-council-seat-return/v1` (`in_use`, identification only). Every tag field is `null` until a cut writes it. |
| [`convening-snapshot.schema.yaml`](convening-snapshot.schema.yaml) + [`seat-assignment.schema.yaml`](seat-assignment.schema.yaml) | `xfactory_council_convening_snapshot`, `xfactory_council_seat_assignment` | Phase 3. The frozen snapshot the consumer issues at admission, holding the admitted commission record and one assignment per required seat in roster order (data-model E4). The public assignment a seat job receives (E5), with a lifetime above 0 and at most the contract ceiling of 21600 seconds (`$defs/lifetime_ceiling_seconds`, Brett Heap's OPEN-1 ruling). Their vectors are the corpus's `assignment` area. |
| [`conformance/`](conformance/) | corpus | The shared conformance corpus: `index.json` and one JSON vector per case under `vectors/<area>/`. Phase 1 lands the `foundation` area: the `definition` and `classification` boundaries. |

The canonical validator is
[`scripts/validate-council-convening.py`](../../scripts/validate-council-convening.py),
a thin CLI over the reference implementation in
[`scripts/council_convening/`](../../scripts/council_convening/). Its tests are
`tests/council_convening/`. Two digest subjects, `council_convening` and
`council_seat_return_payload`, are added to the ONE construction's closed
enumeration in
[`signed-execution-chain/digest-construction.schema.yaml`](../signed-execution-chain/digest-construction.schema.yaml).
That widens SUBJECTS; it adds no second construction.

Later phases add the commission record and its predicate registry (Phase 2),
the snapshot and assignments (Phase 3), the challenge, registration, return and
signing contexts (Phase 4), the producer binding (Phase 5), and the protocol
selection, activation evidence and runbook (Phase 6).

## Classification comes first, and a legacy record is never passed

Every boundary over a protocol-carrying record begins with classification
against the closed registry (data-model E1):

1. a record whose `protocol` is `xfc-resolved-council-1` is a replacement record,
   whatever else it carries;
2. a record whose `protocol` is `xfactory-council-seat-return/v1` is a legacy
   record, and any other `protocol` value is `protocol_unknown`;
3. a record with no `protocol` is legacy when one of the registry's recognition
   rules matches, and `protocol_unknown` otherwise.

What follows depends on the side's **selected** protocol, never on payload shape
alone. A legacy record under a replacement selection is refused,
`legacy_protocol_refused`. A replacement record under a legacy selection is
refused, `protocol_not_selected`. A legacy record under a legacy selection, or
offline, is **routed** to the legacy verifier: this family gives it no verdict,
and the validator's `check` exits 3, which is never a pass. The legacy verifier
(Hermes 015 and its golden vectors) remains the only verifier of legacy bytes.

## Ownership: what stays the successors'

The provider owns the shapes, the closed registries, the evaluation orders, the
validator and the corpus. The successors own everything that runs:

| Item | Owner |
|---|---|
| Domain rule-file adapters | the producer (codexFactory 049), and the consumer (Hermes 025) through its allowlisted governed-repository adapter |
| HTTP routes, request and response envelopes, status codes and error bodies | the consumer (025) |
| Persistence, transactions and uniqueness | the consumer (025) |
| Trusted collection and pre-submit rechecks | the producer (049) |
| Per-seat job isolation and key minting | the producer (049) |
| The concrete producer-binding instance in the consumer's runtime configuration | the operator, at the provisioning act |
| Broker enforcement | owner-provisioned |

Each side refuses with this family's vocabulary, through a total mapping from its
internal names that it records in its own evidence. The one exemption is the
consumer's council-and-mix guard and its touched-object and base-branch guards,
which keep the consumer's own codes and are proven by its own tests.

## Out of scope

None of the following belongs to this family or its feature (research R20):

- producer or consumer implementation;
- HTTP routes, envelopes, status codes and error bodies (025);
- persistence and transactions (025);
- the domain rule-file adapters (each side);
- broker provisioning and credentials;
- deployment;
- successor pin advances;
- activation;
- any spec delta;
- the archive of the governing change.

Local tests are never reported as publication, deployment or activation.

## The adapter residual risk, and why it fails closed

Each side derives the neutral rule projection from the domain's rule files
through its own adapter, and the neutral corpus cannot test a domain file. So the
two adapters could map the same domain file differently (research R6). Such a
disagreement **fails closed**: the consumer's projection differs from the one the
record carries, and admission refuses `rule_projection_mismatch`. The producer's
own tests over real council documents, and the owner's matched rehearsal, are
where such a disagreement is caught before activation.

## Wallet trust

Wallet trust controls outside worker registration are unchanged (FR-010). This
family adds no wallet, grant, custody or trust-anchor rule, and edits nothing
under `governance/review-authority/` or `openXwallet/`.

## Brett Heap's rulings this family encodes

He ruled each on 2026-10-08, first-hand, choosing the recommended option. The
record is opensoft/brett-wip `lanes/log/codeXfactory-2.md`, RULED lines at
19:24:21Z (OPEN-1 to OPEN-4), 19:24:59Z (OPEN-5) and 23:03:35Z (the three
follow-ups). The labels are verbatim.

| Ruling | Label | What it fixes |
|---|---|---|
| OPEN-1 | "600 s challenge, 6 h assignment (Recommended)" | The contract ceilings: a challenge lives at most 600 seconds and an assignment at most 21600 seconds (Phases 3 and 4). |
| OPEN-2 | "Consumer's runtime config (Recommended)" | The concrete producer-binding instance lives in the consumer's governed runtime configuration; this family ships only its schema, a `.template.yaml` stub, the derivation and the corpus (Phase 5). |
| OPEN-3 | "History + unchanged rule file (Recommended)" | Revision currency: a revision on the governed first-parent history whose sources equal the governed tip's at admission, otherwise `rule_superseded` (Phases 2 and 5). |
| OPEN-3 follow-up 1 | "Every governed source (Recommended)" | The currency test covers every governed source a convening cites, not only the rule file. |
| OPEN-3 follow-up 2 | "job_workflow_ref's repo (Recommended)" | The ruling's "producer repository" is the repository named in `job_workflow_ref`; a permitted workflow outside the governed repository is refused. |
| OPEN-3 follow-up 3 | "At or after the frozen rev (Recommended)" | A seat job's workflow commit must be on the governed history at or after the frozen revision. |
| OPEN-4 | "Join behind a version floor (Recommended)" | The family joins the release inventory behind `COUNCIL_CONVENING_RELEASE_FLOOR`, set at the Phase 7 cut. |
| OPEN-5 | "Keep the existing names (Recommended)" | The predicate registry keeps `changed_paths_intersect` and `rule_touches_security_posture`, with no mapping layer (Phase 2). |

## Owner acts, named and not performed

No task of this family performs any of these. Each is the owner's, and each is
recorded with dated evidence when it happens:

- landing each phase's pull request (Brett Heap's word);
- making `council-convening-gate` a required check (a ruleset act);
- allocating and publishing each release, and the annotated tags;
- the successors' pin advances;
- broker and credential provisioning, including writing the binding instance into
  the consumer's runtime configuration;
- deployment;
- the commissioning pause, the matched activation and the paired rollback;
- the archive of `renew-resolved-council-protocol`.
