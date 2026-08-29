# Intent Compliance Contract

Status: ratified
Ratified by: `add-standing-policy-compliance-contract` on 2026-08-26.
Registered in the additive `contract-v2.3` bundle; merge and annotated-tag
publication evidence remains pending realization.

This family defines neutral evidence for evaluating governed intent against
standing policy at approval, immediately before dispatch, and at post-build
admission. Domain repositories own concrete policy classes, detectors, prompts,
scope resolvers, registry instances, and runtime integration. They do not own or
copy these record shapes.

## Records

- `veto-class-vocabulary.schema.yaml` binds domain-owned veto classes to exact
  policy and ratification blobs plus issuer and revoker authority roles.
- `policy-allowance.schema.yaml` records one immutable, scoped approval.
- `policy-allowance-revocation.schema.yaml` appends an authenticated revocation
  without rewriting approval facts.
- `policy-allowance-registry.schema.yaml` records an append-only current-state
  revision whose allowance identifiers are never repointed.
- `compliance-decision.schema.yaml` records the closed outcome, all layer
  findings, current authority resolution, optional bounded classifier evidence,
  deterministic evidence, and static dispatch-authorization evidence
  conditioned on the evaluated registry head.

Each schema has a sibling `.template.yaml`. Executable positive and
requirement-indexed negative records live under `examples/`.

## Canonical digests

Content-addressed records use the integer-only RFC 8785 JSON Canonicalization
Scheme subset: floats and non-finite numbers are forbidden, integers are bounded
to the interoperable JSON range, and object names use RFC 8785 UTF-16 ordering.
The record's own digest member is omitted while computing that digest:
`vocabulary_digest`, `approval_digest`, `revocation_digest`, or
`revision_digest`. The same omission rule applies to nested `scope_digest`,
scope-verdict `verdict_digest`, and classifier `result_digest`. Policy and
ratification source digests are SHA-256 over exact Git blob bytes at the
declared immutable revision.

## Closed evaluation rules

Composition precedence is `block > needs_human_review > allow`. Deterministic
evaluation is permanent and cannot be erased by classifier or Hermes findings.
One deterministic finding with `disposition: block` is sufficient for a pure
veto: the decision is `block` even when `allowance_references` and `resolutions`
are both empty. Allowance evidence is required to satisfy a deterministic
finding, but can never neutralize a deterministic block. Classifier and Hermes
findings are supplementary layers and cannot downgrade that block.
Classifier escalation is optional, single-invocation, single-turn, hard-capped,
and fail-closed. A claimed allowance is only a `(registry_id, allowance_id)`
reference; copied allowance payloads are forbidden. Approval, dispatch, and
admission retain identical content, policy, vocabulary, registry identity, and
lexicographically ordered allowance-reference sets while later gates resolve
the current registry revision again.

Static dispatch-authorization evidence binds the decision, content, registry
head, evaluator, and evidence-validity timestamp. It is not a credential and
does not prove issuance, replay protection, atomic consumption, or worker
invocation. Those operational guarantees belong to the consuming domain runtime
and require domain-owned conformance evidence.

Every issuer, revoker and cited policy approval carries an `authority_source`
reference to an immutable blob whose revision is an ancestor of a caller-supplied
trusted commit. The validator hashes the exact bytes at the declared path and
revision, then parses one closed authority document bounded to 64 authorization
entries and 64 approval ids per entry. The source authorizes only the exact
`(principal_id, authority_role)` tuple it contains and, for policy approval, the
exact cited `approval_id`; substituting any member fails the binding. The
validator loads the complete authoritative vocabulary, allowance, revocation,
and registry family from that exact Git tree; neither the candidate worktree,
local-only objects, nor remote configuration establishes trust. The source blob
is not self-authenticating authority: trust still comes from the out-of-band
repository and commit, while registry admission authorizes an allowance or
revocation record.

Registry outcomes are one closed tagged state. `status: resolved` carries the
uniquely derived `registry_id`, `revision_id`, and `revision_digest`;
`status: unresolved` carries the registry id and exactly one reason,
`registry_not_found` or `registry_head_ambiguous`, with no invented revision
identity. The decision's registry object and `deterministic_evidence.registry`
must exactly match the derived tag, and every unresolved allowance resolution
must repeat its reason. Unresolved state yields `needs_human_review`, never
`allow`. Registry admission makes referenced records authoritative; copied
allowance payloads remain forbidden.

Static decision corpora may contain any completed prefix of `approval`,
`dispatch`, and `admission` for a `governed_binding_id`; when multiple gates are
present, they are unique, strictly chronological, and retain identical governed
bindings. Correlation references are telemetry only and never join gates.
Redacted detail is a bounded list of closed identifier codes rather than
free-form text.

## Validation and consumption

Run from a pinned openxFactory checkout:

```bash
python3 scripts/validate-intent-compliance.py
python3 scripts/validate-intent-compliance.py --strict \
  --trusted-repository ../domain-repository \
  --trusted-repository-id example/domain-factory \
  --trusted-commit 0123456789abcdef0123456789abcdef01234567 \
  ../candidate-records
```

The first command validates schemas, a positive baseline, every single-mutation
negative fixture, and requirement coverage. YAML aliases, duplicate keys,
floats, excessive depth/document count,
oversized files, and unbounded discovery are rejected before semantic use.
The second discovers candidate decisions, loads all authoritative records from
the exact trusted commit, resolves every source blob against that snapshot, and
fails when no governed records exist. Trusted checkout, canonical repository ID,
and commit arguments are mandatory and out-of-band for target validation.
Exit codes are `0` for conformance, `1` for contract findings, and `2` for a
validator/schema/dependency harness failure.

Consumers pin `opensoft/openxFactory` by release tag or exact commit and invoke
the validator from that checkout. Runtime instances reside in the consuming
domain repository. Generated adapters may live there, but schemas and validator
copies are non-canonical and must not replace the pinned family.
