# Design — declare-client-standing-policy-contract

Short by intent. The CONTRACT SHAPE is not open here: it was ratified
2026-08-22 by Brett Heap on hermes-install `add-client-overlay-standing-policy`
(four sub-rulings — the shape as built; `policy_position` not
`policy_override`; a declared-but-empty `{}` REFUSES; no `relation_to_*`
field), and this change DECLARES that shape in the contract openxFactory owns.
What is genuinely decided here is openxFactory-side and mechanical: where the
declaration lives, where the rules that JSON Schema cannot express live, how
wide the prohibited-content scan reaches, and whose message text wins where two
implementations phrase the same refusal differently. Every claim below was read
against the checked-out sources at authoring time; file and symbol names are
given so a reviewer can re-verify without trusting this document.

## 1. D1 — Declared INLINE, not as a fourth sibling schema file

Issue #254 raises the alternative in as many words: *"Likely also worth a new
`contracts/client-content/client-policies.schema.yaml` sibling … if this repo
wants the same per-kind schema decomposition the other three blocks already
have."*

**Position: inline.** The three siblings decompose per KIND, and these entries
have no kind.

- `client-policy-overrides.schema.yaml`, `client-memory-boundaries.schema.yaml`
  and `client-integration-boundaries.schema.yaml` each govern a
  self-identifying SUB-DOCUMENT: each declares `required: [schema_version,
  kind, …]` with a single-value `kind` enum, and
  `validate-client-content.py::validate_structure` dispatches on that inner
  `kind` — the overlay branch literally recurses
  (`findings.extend(validate_structure(po))`) into the sub-document, which
  works only because the sub-document announces what it is.
- `client.policy_namespace` is a scalar and `client.policies` is a bare mapping
  of policy id to policy body. Neither carries a `kind`, and giving them one to
  earn a file would invent a document boundary the ratified runtime does not
  have: hermes-install reads `client["policies"]` directly.
- **The mirror already answered this.** `subject.policies` is declared inline
  in `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`, not
  in a `subject-policies.schema.yaml`. This change is a faithful mirror one
  layer up; diverging on file layout would make the two families describe the
  same construct in two shapes for no gain.
- **A sibling file also costs a manifest row and a digest** for a schema no
  dispatcher reaches — a released surface with no reader.

**Consequence, recorded:** `contracts/manifest.yaml` gains NO row. The existing
`client-overlay` row's `sha256` is RECOMPUTED, because the schema file's bytes
changed and `scripts/validate-manifest-digests.py` fails closed on a stale
digest.

## 2. D2 — The conditional requirement lives in the validator

`client.policy_namespace` is required WHEN AND ONLY WHEN `policies` is present.
JSON Schema expresses that with `if`/`then`/`dependentRequired` — and **no
schema in this repository's contract families uses one**. The family's stated
idiom is the opposite: every `client-content/*.schema.yaml` header says
*"Structural shape; the stricter-only comparability rules live in the canonical
validator (`scripts/validate-client-content.py`) and are never re-implemented
by consumers"*, and the subject family says the same in its own header, listing
four numbered rules it leaves to `validate-hermes-domain-overlay.py`.

So the schema states the SHAPE (`policy_namespace` is a non-empty string when
present; `policies` is a non-empty mapping of well-formed entries) and the
validator states the RULE. The schema comment enumerates the five rules it
cannot express so a reader of the schema alone is never misled into thinking
the shape is the contract.

**The converse is deliberately not an error.** A `policy_namespace` declared
with no `policies` is inert, and refusing it would be a new refusal class this
contract never declared — and one hermes-install does not implement, so canon
would refuse what the runtime accepts.

## 3. D3 — The empty-map refusal, mirrored rather than re-decided

Ruling (c) of 2026-08-22 stands as ratified: `client.policies: {}` REFUSES.
openxFactory implements it identically rather than treating an empty map as
absent, for the reason the ruling was granted on — readiness clears
`materialized_policy:<layer>` on ROW PRESENCE, so an empty row reports a veto
seat armed with nothing behind it.

Two mechanical consequences worth stating because they are easy to get wrong:

1. **The block is entered on `"policies" in client`, not on truthiness.** A
   truthiness test would make `{}` unreachable — the exact behaviour the ruling
   forbids.
2. **A bare `policies:` parses to `None`** and is the same declaration of
   emptiness, so it takes the same finding; a block of some OTHER type is a
   different mistake and takes its own. `policies` reads plural, so a list is
   the mistake an author is most likely to make, and the empty-block message
   ("omit the block entirely to carry none") would send that author to DELETE
   the block rather than reshape it. hermes-install split these two findings in
   an adversarial-review follow-up on its own branch; canon adopts the split
   rather than re-deriving the same defect.

## 4. D4 — The prohibited-content scan is SUBTREE-SCOPED, and the asymmetry is the decision

`validate-hermes-domain-overlay.py::_prohibited_subject_content` walks the
WHOLE subject document. This validator walks only `client.policies`, matching
hermes-install's `_prohibited_policy_content(..., seat="tenant",
path="client.policies")`. **Position: preserve the asymmetry, and say why in
the code.**

- **The subject kind was NEW when its walk was written.** A whole-document rule
  cost no existing document its verdict, because no conforming document existed
  yet. `hermes_client_overlay` has been released since `contract-v1.17` and is
  live-seeded; a whole-document walk would change the verdict of overlays that
  use none of the new block. That is a breaking change wearing an additive
  change's clothes, and the frozen `client.required` would be the only thing
  left that was actually additive.
- **It would invert the divergence direction the sequencing ruling was granted
  on.** That ruling accepted a window in which *"hermes-install is stricter
  than canon, never the reverse"*. A wider canonical scan makes canon refuse
  what the shipped runtime accepts — the reverse — and turns a bounded window
  into a genuine conflict.
- **The narrower scan is not a coverage gap for the new block.** Everything the
  new block can carry is inside the subtree, and the walk is recursive within
  it (`_walk_entries`), so key material one level deeper than a policy entry
  still refuses — proven by the packaged
  `client-policy-credential-value.yaml` negative, whose secret sits at
  `client.policies.standing-policy.escalation.token`.
- **Widening it later stays available** as its own change, with its own
  evidence about what it would newly refuse. Nothing here forecloses it.

## 5. D5 — Message text: hermes-install's wording, this file's conventions

Two implementations phrase the same refusal, and the parity suite hermes-install
plans compares an `# expected_failure:` header as a SUBSTRING of the runtime's
message (`assert reason in runtime_reason`). Alignment therefore means: each
fixture header must be a substring of BOTH messages. The rule applied here is
**adopt hermes-install's wording verbatim wherever it is layer-neutral, and let
this file's conventions win where they conflict** — flagged, not silent:

| Where | Choice |
|---|---|
| The six address findings and the two prohibited-content findings | hermes-install's text, verbatim, with `client.policies.<key>` paths and the seat word `tenant` (which is also what the subject validator's own text becomes one layer up) |
| `missing or empty client.policy_namespace` | hermes-install's text MINUS its trailing *"and the seed binds that declaration to the layer"*. Canon describes a document, not a seeding act; the retained text is a strict PREFIX of the runtime's, so every substring check still passes |
| Credential findings | Appended to the one flat `findings` list. hermes-install raises them separately under `RemediationCategory.SECRET_MATERIAL_PRESENT`; this validator has no remediation vocabulary and inventing one for a single rule would be a larger change than the rule |
| Constant naming | `PROHIBITED_DOMAIN_BLOCKS` — hermes-install's `_PROHIBITED_DOMAIN_BLOCKS` semantics (the list names the DOMAIN layer's slice, not the seat being checked, and now governs two seats), with the leading underscore dropped because module constants in this file carry no sigil (`ALLOWLIST_KEYS`, `DENYLIST_KEYS`, `CEILING_PARENT`). The subject validator's `PROHIBITED_SUBJECT_BLOCKS` is NOT renamed here: it is a released contract's canonical implementation and belongs to its own change |

**PORTED, NOT IMPORTED.** The three shared constants
(`PROHIBITED_DOMAIN_BLOCKS`, `CREDENTIAL_VALUE_KEYS`, `RAW_SECRET_MARKERS`) are
duplicated from `validate-hermes-domain-overlay.py` with a provenance comment.
Verified first: **no canonical validator in `scripts/` imports another** — the
only cross-module imports are into the shared
`scripts/hermes_runtime_validation` package (`validate-contract-release.py`,
`validate-hermes-runtime-contracts.py`), into a test-side scanner
(`validate-avatar-runtime.py`), and into the `xfactory` package
(`validate-memory-gateway.py`). Importing one canonical script into another
would let an edit to the subject family silently re-decide a tenant verdict.

## 6. The self-test trap this change had to fix first

`self_test()` loaded exactly two filenames: the baseline and
`hermes-client-overlay.example.yaml`. A second positive would have been
packaged, digested, published — and never validated. It now discovers positives
(`EXAMPLES.glob("*.example.yaml")` minus the baseline comparand, which keeps its
role as the `client_policy_baseline` every positive is checked against) and
fails closed if none are found. Same trap class as the parity-suite `continue`
that `add-subject-overlay-contract` design §8 named, one directory over.

## 7. The enforceable slice, and where openxFactory stops

A conforming client overlay that declares the block contributes one additional
content-kind payload beyond the tenant slice it already contributed:

```yaml
policy_position:                  # keyed by policy id
  <policy-id>:
    policy_namespace: …           # restated in the payload, deliberately
    policy_id: <policy-id>
    …the tenant-owned policy body…
```

`policy_position` is REUSED, not invented — the same ratified content kind the
Domain and Subject seats already materialize, so a lens resolving
`<namespace>/<policy-id>` reads the same KIND of row whichever layer it is
reading. Extraction, transaction shape, provenance columns and the refusal
vocabulary stay hermes-install's, exactly as the subject contract drew the line:
*what a conforming document contributes* is ours, *how the rows get written* is
theirs.

## 8. Risks and rollback

- **Risk: canon and the runtime drift apart later.** The ported constants and
  the duplicated rule bodies are two implementations of one meaning. Mitigated
  by the release gate: this change does not archive until hermes-install has
  re-pinned AND admitted `hermes_client_overlay` to `PARITY_KINDS`, which is
  the mechanism that makes a future drift fail a suite instead of passing
  quietly. Until then the packaged negatives are the standing proof, and each
  header was checked to be a substring of the runtime's own message text.
- **Risk: an existing client overlay newly fails.** Structurally excluded —
  every new rule is reached only from `if "policies" in client`, and no
  committed overlay in any repository declares that block
  (`config/clients/opensoft/overlay.yaml` is untouched by the change that
  introduced the capability).
- **Risk: the additive digest change forces a re-pin.** It does not.
  `client.required` is byte-frozen and the two properties are optional, so a
  consumer that ignores the block reads the new schema exactly as it read the
  `contract-v1.17` copy. Only a consumer that USES the block needs the new tag.
- **Rollback:** revert the two schema properties and the validator's
  standing-policy section; the `hermes_client_overlay` branch returns to three
  checks, the fixtures are removed with it, and the manifest digest reverts to
  `f67a3412…`. No other kind, validator, or released digest is involved.

## 9. Open questions

- **OQ-A — should the subject validator's `PROHIBITED_SUBJECT_BLOCKS` be
  renamed to match?** The name describes the wrong document (the blocks are the
  DOMAIN layer's) and two seats now share the list. Not done here: renaming a
  constant inside a released contract's canonical implementation is that
  contract's change to make, and doing it from a tenant-side change would put
  the edit where no reviewer of the subject contract would look for it.
- **OQ-B — a tenant content SET.** Symmetric with the subject path's own open
  question and with hermes-install's OQ-4: tenant policies ride INLINE because
  no loader sweeps a `config/clients/<ref>/policies/` directory, so such a
  directory would be unloaded content that drifts. A
  `hermes_client_content_manifest` is named as future work, not smuggled in.
- **OQ-C — the parity fixture root.** Admitting `hermes_client_overlay` to
  `PARITY_KINDS` needs `_fixture_dir()` to resolve per kind: the client corpus
  is `contracts/client-content/examples`, the suite currently hardcodes
  `contracts/hermes-domain-overlay/examples`. Recorded so the admission is
  scoped honestly; owned by hermes-install.
