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
| [`conformance/`](conformance/) | corpus | The shared conformance corpus: `index.json` and one JSON vector per case under `vectors/<area>/`. Phase 1 lands the `foundation` area: the `definition` and `classification` boundaries. Phase 5 adds the `binding` area and the corpus-owned fixture `fixtures/repository-identity.json`. |
| [`producer-binding.schema.yaml`](producer-binding.schema.yaml) + [`producer-binding.template.yaml`](producer-binding.template.yaml) | `xfactory_council_producer_binding` | Phase 5. The producer workflow binding (data-model E10), judged by kind, and its instantiation stub, which is never accepted as live. No instance is published here (see [The producer binding](#the-producer-binding-phase-5)). |

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

## The producer binding (Phase 5)

A producer binding binds one producer principal's authority to the current
governed repository identity and to verified OIDC workflow claims (design D4;
FR-009). It names the issuer and audience the principal's token must carry, the
repository its job runs in (`caller_repository`, the token's `repository`
claim), the exact subject template that token's `sub` must equal, and the
reusable workflows it may run per operation, each with its revision rule. A
workflow reference is never a subject: `job_workflow_ref` and `sub` are
different claims, and permitted workflows are matched against the verified
`job_workflow_ref` only.

**Where an instance lives.** Brett Heap ruled OPEN-2 on 2026-10-08, "Consumer's
runtime config (Recommended)": the concrete instance is written into the
CONSUMER'S governed runtime configuration at the provisioning act (049 T031;
025 H3), and validated at the consumer's pin of this repository with

```sh
python3 scripts/validate-council-convening.py check <binding instance>
```

which runs E10 steps 1 to 6 against that pin's
`contracts/policies/repository-identity.yaml`, refuses the template stub as live,
and reports steps 7 to 14 as not checkable offline. This family ships only the
schema, the stub, the derivation from the identity map, and the corpus. The stub
is the commission job's binding and permits one operation. A seat's binding is
its own instance per seat (025 ruling (A)), and permits `seat_execution` only;
the stub's header spells out that entry.

**The order** (data-model E10). Steps 1 to 6 judge the instance alone:
`binding_malformed`, `binding_wildcard`, `issuer_mismatch` (the standard issuer
or GitHub's `/<enterprise-slug>` form), `repository_identity_unavailable` then
`repository_identity_former`, `subject_workflow_conflation`, and
`subject_template_mismatch`. Steps 7 to 14 judge the verified claims:
`claims_unverified`, `claims_expired`, `issuer_mismatch`, `audience_mismatch`,
`subject_template_mismatch`, `repository_identity_mismatch`,
`workflow_not_permitted`, and `workflow_revision_ungoverned`. At admission the
consumer runs steps 1 to 13 as E2 step A1, right after the record's shape check
and before retry identity (A3), so a token that fails binding never returns a
live snapshot; and step 14 as E2 step A4, after E2 step 5 has checked the
`governed` member it reads. The snapshot half of admission (E4) judges no
binding. A shared commission vector carries none, so a consumer runs it without
A1 and A4.

**The revision rule** is closed and fixed per operation (OPEN-3, "History +
unchanged rule file (Recommended)"): `equals_governed_revision` for
`commission`, and `on_governed_history_since_revision` for `seat_execution`
(follow-up 3, "At or after the frozen rev (Recommended)": a seat job's
`job_workflow_sha` on the governed first-parent history at or after the frozen
revision). Any other pairing is `binding_malformed`. The repository compared is
the one `job_workflow_ref` names, never the caller (follow-up 2,
"job_workflow_ref's repo (Recommended)"), so the estate's calling pattern, a
caller repository running the governed repository's reusable workflow, is
accepted, and a permitted workflow outside the governed repository fails closed.

**The identity map** is read through `load_transfers` in
`scripts/estate_inventory.py`, and through nothing else. That reader takes an
absent or unreadable map for an empty one, so this family first confirms that
the map exists, reads, parses under the same strict loader and is well formed,
and refuses `repository_identity_unavailable` otherwise, and when
`load_transfers` reports a malformed row. A former spelling, or a non-canonical
case variant (equal to a listed spelling ignoring ASCII case, not byte-equal), is
`repository_identity_former`; any spelling the map does not list, and a pending
row's former spelling, is current.

**The corpus never reads the live map** (round 7, R7-M1). Every vector whose
boundary reads the map carries it in its `repository_identity` oracle: the text
of the frozen fixture `conformance/fixtures/repository-identity.json` (one
complete transfer row and one pending row), or an `absent` or `unreadable`
state. The generator writes the fixture's text into those vectors and never
reads `contracts/policies/repository-identity.yaml`, so an edit to the live map,
which other changes make, moves no vector and fails no `generate --check`. A
vector that reads the map without the oracle is malformed
(`council-convening-vector-identity-map-missing`).

**One binding per principal.** An assignment's `holder.binding_ref` names a
binding by its `binding_id`. A per-seat principal is one binding per seat, told
apart by its subject template: GitHub's `repo:<owner>/<repo>:environment:<name>`
for a job that references a per-seat environment, or a documented subject
customization that carries it. The corpus carries such vectors.

**The subject grammar** is GitHub's ("OpenID Connect reference",
https://docs.github.com/en/actions/reference/security/oidc): elements are joined
by `:`, a `:` inside a value is written `%3A`, `context` is
`environment:<name>`, `pull_request` or `ref:<ref>`, and `repo` is
`<owner>/<repo>`, or `<owner>@<owner-id>/<repo>@<repo-id>` in GitHub's immutable
subject format. The template must carry a repository element (`repo`,
`repository` or `repository_id`) that names the binding's repository. The
closed set of subject claim keys is in the schema, with its sources; GitHub's
open `repo_property_*` family is not a member.

**The broker** refuses nothing at binding. A binding whose broker capability is
not verified parks activation, which E12 refuses as
`broker_capability_insufficient` (Phase 6; D4).

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
