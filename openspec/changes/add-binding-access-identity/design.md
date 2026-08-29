# Design: add-binding-access-identity

Status: draft

Three decisions in this packet are not obvious, and one of them is a trap that
the obvious design walks straight into. This records what the repository's own
evidence said when each was checked against it.

## 1. The obvious discriminator regresses the check it refines

Task 4.5 names one field: the record "carries no consumer or access-identity
field, and the validator compares no authorities". The obvious design follows
directly — add `access_identity`, and let `shared-secret-identity` pass a shared
`secret_ref` whenever the sharing bindings name different principals.

**That design is wrong, and the proof is a fixture already in the tree.**

`examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml` is
two bindings — `intent_dispatch` and `corpus_content_write` — sharing one
`secret_ref`. It exists because the serving tier must never hold key material
able to mint a content-write token. In the live estate those two bindings are
served by two DIFFERENT workload identities: the openXdox serving tier and the
content lane are separate systems with separate principals. So under the obvious
design, the moment that fixture's bindings each declare their (genuinely
distinct) access identity, **the negative fixture becomes conforming** — and the
refusal that `add-dispatch-credential-contract` shipped to keep dispatch and
content apart is silently retired by a change whose stated purpose was to make
an invariant MORE provable.

The custody change anticipated the general shape of this without naming the
mechanism: "relaxing the rule is a change to a check that exists to keep the
dispatch and content credentials apart"
(`openspec/changes/add-notebook-hosting-credential-custody/tasks.md:60-62`). Distinct access
identities alone IS that relaxation, wearing a governance field.

**What actually separates the two cases is intent, and intent has to be
declared.** Two consumers of one operated identity have ONE identity they both
authenticate as. Two credentials collapsed into one reference have no such
identity — there is nothing to declare, because the collapse is the defect.
Hence the second field, and hence a conjunction:

    shared secret_ref is licit  ⟺  every sharing binding declares the SAME
                                   operated_identity
                              AND  their access_identity values are all present
                                   and pairwise distinct

The dispatch/content fixture declares no `operated_identity` and keeps raising
the existing finding, byte-identically. That is why tasks §3.6 makes re-raising
it an explicit test rather than trusting the reasoning: **the claim that this
refines the check rather than regressing it is exactly the claim that needs an
executable probe.**

## 2. Why "declared" and not "inferred", and what the record cannot buy

A tempting alternative is to infer the two-consumer case from the estate — same
account name in the owner field, same provider, plausible topology. Every such
inference is a heuristic sitting where a refusal used to be, and a heuristic
that fails open on a credential-separation rule is worse than no rule.

The declaration is also the only version that is HONEST about its own reach. What
the record proves after this change is that two bindings CLAIM distinct
authorities. It cannot prove:

- that the two named principals exist,
- that they are actually distinct in the store,
- that their grants differ,
- or that either is scoped to only this secret.

Those are the store's facts. The requirement text says so in its own paragraph
rather than leaving a reader to assume the check reaches further than it does —
the same discipline the custody requirement used when it refused to let
per-system bindings read as per-system containment.

What the declaration DOES buy is worth the field: a claim now exists, it is
attributable to a named owner, and it is REFUSABLE when it contradicts itself.
Two bindings declaring one operated identity and one access identity are a
record asserting a separation and denying it in the same breath, and that is
newly a machine-detectable error rather than something only a careful reader
catches. That is precisely the "held by review rather than by the record"
condition the ratification flagged.

## 3. The requirement this packet may not touch, and what is owed instead

The natural home for "the schema owns two more optional fields" is the sentence
in `Canonical credential record shapes` that says what the schema owns. This
packet may not put it there.

`add-credential-escrow-checkout` holds a LIVE `## MODIFIED Requirements` block on
that exact requirement right now
(`openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md:5`),
carrying the sixth record kind and the optional `escrow:` block. The custody
change refused this collision deliberately and its ratification states the
discipline in terms: *"no requirement is MODIFIED here precisely so that two
active changes never hold two live deltas on one requirement text"*
(`openspec/changes/add-notebook-hosting-credential-custody/review/ratification-2026-08-23.md:46-48`).

The reason is mechanical, not stylistic. `MODIFIED` REPLACES a requirement
wholesale; it does not merge. Two live blocks on one requirement means the
second to archive silently deletes whatever the first added, `openspec validate
--strict` sees nothing (it checks a delta's shape, never what promotion will do),
and file-level scenario counts can net to zero. That is the class of issues #329
and #330, and it is the reason the `modified-block-currency` family exists.

So the sentence is OWED, not dropped, and the discharge is written down:
**whichever of the two packets archives SECOND carries the MODIFIED block, and
carries it scenario-complete against canon as it then stands** — including the
scenarios the first packet's promotion will have added. Tasks §2.3.

The alternative — this packet takes the block and the escrow packet drops it —
reverses a decision already ruled on a ratified packet, and is not the authoring
session's to take. It is OD-3, flagged for veto.

## 4. The release class, and why the cut is owed by the policy rather than by drift

Task 4.5 states the ritual is owed because this is a `contracts/schemas/` change.
That is right, but the FORCING MECHANISM is not the usual one, and it was
measured rather than assumed on 2026-08-29:

- `contracts/schemas/xfactory-credential-contracts.schema.yaml` IS a registered
  bundle contract — `contracts/manifest.yaml:2079`, `id: credential-contracts`,
  `type: schema`, with a `sha256` cross-repo consumers verify.
- It is NOT a member of the declared release digest inventory. The membership
  closure is built from `contracts/hermes-runtime/contract-index.yaml` entries
  marked `release_member`, and that catalog carries no credential entry.

So `release-inventory-drift` — the family that usually forces a cut when a schema
moves — will stay silent here. The cut is owed by
`docs/contract-versioning-policy.md` instead: a registered contract gaining
optional fields is its ADDITIVE (MINOR) class verbatim. Tasks §4.5 requires
re-verifying that membership AT the cut and naming in the CHANGELOG which of the
two reasons applied, because a forcing reason recorded from memory is how a
"working as designed" catch turns into a missed one.

**The compatibility argument, which is the one a reviewer should attack.** Three
facts, each checkable:

1. `required` is unchanged. A binding declaring neither field validates exactly
   as before.
2. `contract_schema_version` is unchanged; no field is removed, renamed or
   re-typed.
3. Every NEW refusal is reachable only through a field no earlier record could
   carry, because the field did not exist. A pre-extension repository's findings
   are its findings, unmoved.

Point 3 is the load-bearing one and the easiest to get wrong. It holds because
default-refuse is preserved in the right direction: silence still REFUSES a
shared reference. The extension only ever widens what may be RECORDED — it never
converts a previously-valid record into an invalid one.

## Risks

- **The regression risk, and it is the main one.** A validator rewrite that
  loosens a refusal can loosen it further than intended. Mitigated by keeping the
  EXISTING finding code and message for the undeclared case (so a pre-extension
  repository's output is byte-identical), and by tasks §3.6's explicit re-raise
  probe on the dispatch/content fixture.
- **Merge-order coupling with the escrow packet.** Both edit one schema file and
  both owe an additive minor. Neither proposal spends a number; §4.2 re-parses at
  the cut.
- **A field that becomes decoration.** Optional fields nothing requires can go
  unused, leaving the invariant exactly as review-held as before. This packet
  does not force adoption (OD-6) — the live bindings the custody change routed to
  the installs MAY adopt them. That is a deliberate limit, and it means this
  change makes the invariant PROVABLE rather than PROVEN. Whether a later change
  should require the declaration wherever an operated identity is shared is a
  real follow-up and is not smuggled in here.
- **`operated_identity` as free text** (OQ-2) can drift from the roster records
  that name the same subjects. Accepted at this cut on the same ground the escrow
  block took its shape from running prior art; binding it to a roster record is a
  follow-up with its own resolution question.
