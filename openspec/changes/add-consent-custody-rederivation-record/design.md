# Design: add-consent-custody-rederivation-record

Status: draft
Lane: opsXfactory-1

Eight decisions, **C-1** through **C-8**, each with the alternative it rejects
and the measured reason. The F.1 ruling chose the repair FORM — a structured
block in this contract, ahead of a cut and a re-pin — and nothing below. Every
decision here is the authoring session's and is a veto point.

## Context

`contracts/schemas/consent-instrument.schema.yaml` is at
`contract_schema_version: 2`. Its `custody` object is closed to exactly
`{locator, sha256}` with `additionalProperties: false`, and the file says why in
its own words:

> CUSTODY IS A POINTER. The signed original is referenced by opaque locator +
> sha256 only (the document-cataloging custody pattern, ruling D9); there is no
> property its content could sit in, and the canonical validator rejects
> blob-shaped custody values regardless of schema outcome.

and, of the record object as a whole:

> CLOSED ON PURPOSE. … This family trades the additive-open posture for that
> rule; **growth takes a `contract_schema_version` bump.**

Ruling **D9** is `openspec/changes/archive/2026-08-06-add-consent-instrument/design.md`
§ *D9. Real-record placement — originals out; instance placement is domain
policy*: *"Neutrally mandatory: the SIGNED ORIGINAL never enters a product repo
(opaque locator + sha256 only — both instantiations already agree)."* The
promoted requirement is *The Signed Original Never Enters A Product Repo*.

The enforcing code is `scripts/validate-consent-instruments.py` `check_custody`,
which (a) refuses any key under `custody` outside `{locator, sha256}` as
`embedded-original-content`, (b) refuses a malformed digest as
`custody-sha256-malformed`, and (c) walks every string under `custody` with
`walk_strings` for base64 runs, `data:` URIs, PDF magic and multi-line bodies.
**Nothing anywhere re-derives a custody digest** — that absence is OpsxFactory
finding F.2, and it is why F.1 went thirteen days unseen and was then found by a
sweep looking for something else.

The precedent for the growth this packet proposes is on this same schema:
`add-client-identity-roster` took it from `contract_schema_version: 1` to `2` for
two ADDITIVE growths, and recorded in the file itself that the RECORD envelope's
`schema_version` stayed `const: 1` *"because changing it would invalidate every
instrument in the estate, which is the opposite of additive."*

## C-1. The record is a SIBLING of `custody`, never a member of it

**Decision:** a new top-level property on the record object,
`custody_rederivations`. `custody` is not touched: same two properties, same
`additionalProperties: false`, same comment.

**Rejected:** `custody.history[]` or `custody.rederivations[]`.

**Why, and it is D9's own argument rather than deference to it.** D9's closure
is not stylistic. It exists so that **no property exists in which the signed
original's content could sit** — that is the sentence, and `check_custody`
enforces it by refusing every unexpected key AND by walking every string beneath
`custody` for blob shapes. An array of objects inside `custody` would put eight
new string fields per entry under that walk, unbounded in count, in the one
place the contract has promised a reader that only a pointer and a digest live.
The sibling carries identical facts at identical rigor and leaves the promise
exactly as it was made. It also keeps the failure modes apart: a malformed
custody pointer and a malformed re-derivation chain are different defects with
different owners, and a reader who greps `custody:` still sees the pin and only
the pin.

**Cost of the veto:** admitting growth inside `custody` reopens D9 and obliges a
`## MODIFIED` to *The Signed Original Never Enters A Product Repo* that removes
the "nothing else" clause — a larger delta than this one, in the requirement
whose closure the whole family is built on.

## C-2. The name is `custody_rederivations`

**Decision:** `custody_rederivations`.

**Rejected:** `custody_history` (reads as a second custody object, which is
exactly the misreading C-1 exists to prevent, and invites future non-digest
facts into it); `custody_amendments` (collides with `amendments`, which is a
LIFECYCLE transition family under ruling D7 and must not acquire a second
meaning); `rederivations` (unanchored — the record already holds several
content addresses and an unqualified name would attract them).

**Measured against the schema's own naming.** The file's compound property names
are `status_history`, `delegation_clauses`, `dependent_refs`, `data_consent`,
`autonomy_position`, `instrument_class`, `instrument_id` — snake_case, and
every one names WHAT THE ENTRIES ARE rather than what they are about.
`custody_rederivations` follows that: each entry IS a re-derivation, qualified
by the pin family it belongs to. The `status_history` precedent is the closest
sibling shape in the file — an array of closed transition records standing
beside the scalar it explains, never inside it.

## C-3. Eight fields, all required, entry closed

**Decision:** each entry is `additionalProperties: false` with all of
`at`, `commit`, `previous_sha256`, `observed_sha256`, `diff_class`, `reason`,
`ruling_ref`, `recorded_by` required.

| Field | Shape | Why it cannot be optional |
| --- | --- | --- |
| `at` | `format: date-time` (RFC 3339) | when the divergence was RECORDED, which is not when it happened; the `amendments[].at` shape, reused verbatim |
| `commit` | `^[0-9a-f]{40}$` | the commit at which the target's bytes changed; without it no leg is re-derivable and the entry is a claim |
| `previous_sha256` | `^[0-9a-f]{64}$` | the digest this link starts from; the chain has no anchor without it |
| `observed_sha256` | `^[0-9a-f]{64}$` | the target's digest AT `commit`; the chain has no terminus without it |
| `diff_class` | closed enum | what kind of change moved the bytes — the fact a reviewer needs before deciding whether "content unchanged" is even claimable |
| `reason` | closed enum | which authorized act did it; the class the gate reports by |
| `ruling_ref` | non-empty string | the record that authorized ACCEPTING the divergence; an entry without one is an unauthorized re-pin wearing a record's clothes |
| `recorded_by` | non-empty string | who wrote it; an anonymous acceptance is not an acceptance |

**Rejected:** making `ruling_ref` and `recorded_by` optional "for convenience".
That is the whole defect in miniature: an entry that admits a divergence without
naming the authority for it is worse than no entry, because it verifies. This
estate refuses the uncited exception everywhere else it appears
(`doc-health`'s uncited-resolution rule; `health/dispositions.yaml`'s required
`cite`; the OpenSpec CLI pin's `pin-disposition-malformed`), and this is the
same shape.

**`ruling_ref` is a DECLARED POINTER, not a resolved one** — the posture
`dependent_refs.ref` already takes in this schema, and for the same reason: the
canonical validator opens no fragment and crosses no repository boundary.

## C-4. `diff_class` is closed at `header_only | content`

**Decision:** two members. `header_only` — the diff between `commit^` and
`commit` adds, removes or rewrites lifecycle-header lines and changes no other
byte. `content` — anything else.

**Rejected:** an open string (a free-text classification is the prose form
Brett declined, wearing an enum's name); a three-way split that separates
`whitespace_only` (no measured instance; a class with no instance is a guess);
`metadata_only` as a synonym (two spellings of one class is how a closed
vocabulary rots).

**Why it is closed, and why closure is the checkable part.** The estate's
measured instance is exactly `header_only`, 3 of 3: OpsxFactory `57fd9fd2`
prepended a `Status:` header and changed nothing else, and re-derivation at
`57fd9fd2^` returns the pin every time. The distinction earns its place because
**it is the one the reviewer of a future divergence actually needs**: a
`header_only` re-derivation says the instrument still points at the same
document, and a `content` one says a signed original's referent moved and the
consent may need re-execution rather than re-recording. An unknown member is a
SCHEMA refusal, so a novel class arrives as a contract question rather than as a
silently admitted string.

**The classification is itself re-derivable** and is stated in the requirement
as such: `diff_class` is a claim about two commits that a checker with the
repository in hand can measure. A `header_only` claim contradicted by the
measured diff is a finding of this family. It is NOT one of the digest legs that
admit or refuse currency — the digests decide that — but a record whose
classification is false is not a record this contract admits.

## C-5. `reason` is closed at three members

**Decision:** `lifecycle_header_edit`, `archive_move`, `other_ruled_edit`.

- `lifecycle_header_edit` — the measured instance; OpsxFactory
  `docs/packet-lifecycle-headers.md` permits it and 16 files took it at
  `57fd9fd2`.
- `archive_move` — the class the sweep expected and did NOT find, kept because
  a packet's move from `openspec/changes/<id>/` to
  `openspec/changes/archive/<date>-<id>/` is a routine act of this estate that
  can move a pinned target's bytes, and because naming it separately is what
  lets a future reader see that the measured 3 of 3 were NOT this.
- `other_ruled_edit` — the escape hatch, **and it is not a bare one**: every
  member requires `ruling_ref`, so the hatch carries the same authority
  obligation as a named member. This is `dependent_refs.kind`'s `other`-plus-
  `note` pattern from this same schema, transposed.

**Rejected:** an open string; a `content_correction` member (an actual content
correction to a signed original's referent is not a re-derivation at all — it is
grounds for re-execution, and admitting it as a `reason` would let this record
paper over the one case that must not be papered over).

## C-6. The chain rule, and the refusal posture

**Decision.** Custody is CURRENT for an instrument iff **either**

- **(direct)** `custody_rederivations` is absent or empty and the target named
  by `custody.locator` hashes at HEAD to `custody.sha256`; **or**
- **(chained)** with entries `e₁…eₙ` in declared order: `e₁.previous_sha256 ==
  custody.sha256`; `eᵢ.previous_sha256 == eᵢ₋₁.observed_sha256` for every
  `i > 1`; the target hashes at `eᵢ.commit^` to `eᵢ.previous_sha256` and at
  `eᵢ.commit` to `eᵢ.observed_sha256` for every `i`; and the target hashes at
  HEAD to `eₙ.observed_sha256`.

Anything else is **NOT CURRENT**, and a chain that cannot be re-derived is a
**REFUSAL, never an admission**.

**Why the `commit^` leg is not optional.** Without it the record would be
self-consistent arithmetic: any two digests can be written down in order. The
`commit^` leg is what forces the claim to touch the repository — it says *the
target really did hash to the previous value immediately before this commit* —
and it is the leg that makes `header_only` audit-able after the fact. Every leg
is re-derivable by anyone with the repository, and none is trusted on the
record's own word.

**Why refusal and not admission is the default.** An unreachable commit, a
shallow clone, a target absent at `commit^`, a rewritten history, a link
mismatch — every one of them means the checker CANNOT SEE the evidence. A
record that admits currency on unverifiable ground is worse than no record: it
converts "we cannot tell" into "verified", which is precisely the state F.1 was
already in for thirteen days without a record's help. **The record is an index
into evidence, never a substitute for it.**

**Rejected:** admitting a chain on internal consistency alone (an attacker or a
careless editor writes two digests and the pin verifies forever); a "grace"
mode that warns on an unre-derivable chain (a warning is an admission with a
softer voice — the whole point is that the gate refuses); comparing only HEAD to
the last `observed_sha256` and skipping the interior links (a chain whose middle
is fiction would pass, and the middle is where the ruling references live).

## C-7. The validator split — internal legs neutral, git legs at the consumer

**Decision.** `scripts/validate-consent-instruments.py` gains the INTERNAL legs:
first link equals the pin, each later link equals its predecessor's observed
digest, `at` is non-decreasing in declared order, no entry's digest is written
back into `custody.sha256`, closed enums, closed entry shape. It does **not**
gain the git re-derivation legs.

**Why.** The canonical validator is network-free and reads ONE repository —
the posture this schema already states for `dependent_refs.ref` (*"The validator
opens no fragment, confirms no entry's existence and crosses no repository
boundary"*). An instrument's `custody.locator` target lives in the CONSUMER's
repository; openxFactory holds no consent instruments at all. So the neutral
side owns the RULE and everything checkable from the record's own bytes, and the
re-derivation runs where the bytes are — OpsxFactory's F.2 gate, whose ruled
scope is *"every in-repo sha256 pointer to an in-repo target"*, with the
consent-custody family's rule being the one written here.

**Rejected:** a neutral re-derivation harness in openxFactory (it would need a
consumer checkout, a network, or a vendored copy of another repository's
history — all three refused by this validator family's posture); leaving the git
legs unspecified (an unspecified leg is implemented differently in every
consumer, and then the contract means five things).

**Named so it is not read as forgotten:** this split means openxFactory's own CI
cannot catch a broken consent pin. It has none to catch. The obligation lands on
the consumer's gate, and the requirement says so in as many words rather than
leaving a reader to infer that neutral validation is sufficient.

## C-8. Additive `contract_schema_version: 3`, not a new record kind

**Decision:** bump `contract_schema_version` 2 → 3; the record envelope's
`schema_version` stays `const: 1`; instruments without the array remain valid.

**Rejected:** a separate `xfactory_consent_custody_history` record kind
(splits one fact across two records with nothing binding them — the sidecar
form Brett declined, re-spelled as a contract); a major bundle version (nothing
is removed, narrowed or re-required; every existing instrument validates
unchanged under the new schema, which is the definition of additive here); a
breaking `schema_version` bump (would invalidate every instrument in the estate,
the reasoning the file already records for the 1 → 2 growth).

**The bundle version is NOT decided here.** `docs/contract-versioning-policy.md`
§ *Bundle Realization Order* allocates it at the cut, and § *Version Identity*
forbids a proposal reserving a minor before merge order is known. Measured at
authoring: `contracts/manifest.yaml:3` declares `contract-v3.4` and
`contracts/releases/` holds `contract-v3.4.digests.yaml`, so the next additive
minor is `contract-v3.5` **as things stand** — a measurement, not a claim.

## The consumer handoff, designed but not performed

Named here so the shape is reviewable, and scheduled in `tasks.md` § 6 as the
CONSUMER'S owed act, outside this change's archive gate.

1. openxFactory cuts the bundle (tasks § 5).
2. OpsxFactory advances `stack.yaml` `contract_ref` (today `724a2a4f…`) to the
   cut commit **in lockstep with the worker-enrollment-broker's
   runtime-shape validation** — the pin and the broker's declared shape move in
   one act or the `pin_gap_misdeclared` guard fails the advance closed.
3. OpsxFactory writes, per broken instrument, ONE `amendments` entry (the human
   half, per the F.1 ruling) AND ONE `custody_rederivations` entry (the machine
   half). The three entries are all `diff_class: header_only`,
   `reason: lifecycle_header_edit`, `commit: 57fd9fd2…`, with `ruling_ref`
   citing `docs/packet-lifecycle-headers.md` § *Editing an archived packet* and
   the F.1 ruling comment.
4. The fourth instrument, `opsx-farheap-node-inventory-reader-consent.yaml`,
   takes **nothing**. It is not broken, and a re-derivation entry on a current
   pin would be a false record of an event that did not occur.

## What this design does not settle

- **F.2's gate** — its finding classes, its refusal vocabulary, its per-family
  rules for the other content-address families (plan-acceptance desired-state
  refs, evidence digests, fence baselines, contract pins). OpsxFactory's, under
  its own ruling.
- **F.3** — when a file under `openspec/changes/archive/` may be edited at all,
  and what an editor owes every record that pins it. The F.3 ruling is *"both at
  once"*: an OpsxFactory change plus an openxFactory change amending the
  promoted `document-lifecycle` capability. **This packet is neither of them**
  and touches no `document-lifecycle` requirement.
- **Retroactive entries for divergences nobody measured.** The record admits a
  divergence its author can re-derive; it offers no way to bless one that
  predates the evidence.
