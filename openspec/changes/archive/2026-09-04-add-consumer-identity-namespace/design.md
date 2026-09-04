# Design: add-consumer-identity-namespace

Status: ratified
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session, verbatim
"implement your recommendations on all these". Record:
`review/ratification-2026-09-03.md`.

The proposal states WHAT changes. This states the choices that had more than one
defensible answer, and the answer that was taken.

## 1. The naming question, which two ratified acts had already narrowed

Three candidate spellings existed and two were spent before this packet opened.

**`tenant` / `tenant_ref` are NOT available.**
`adopt-subject-tenant-domain-vocabulary` (ratified 2026-07-23) reserves `tenant`
for the TENANT-OPERATOR LAYER of the canonical Subject / Tenant / Domain
layering, and the mapping is machine-readable at
`contracts/policies/layer-vocabulary.yaml`. A credential binding's issuing
directory is not the tenant-operator organization — a single tenant operator may
run several directories, and one directory may serve several — so reusing the
word would give a ratified term a SECOND SENSE inside one contract family. That
is how a vocabulary stops being one, and this estate has already paid for it
once: the legacy `customer|client|domain` keys survive as FROZEN MACHINE
IDENTIFIERS precisely because renaming them ad hoc was refused.

**`realm` is Keycloak's word**, taken up by `add-identity-brokering` for that
product's instance of the idea. The credential schema is provider-neutral and
carries Azure, AWS and HashiCorp shapes in its own examples; naming a
provider-neutral member after one product's concept would mislead every consumer
that does not run that product.

**`identity_namespace` collides with nothing** — verified by search over
`contracts/`, `scripts/`, `docs/` and `examples/` before it was chosen — and it
follows a compound idiom this repository's contracts already write:
`policy_namespace` in `contracts/hermes-runtime/`, `diagnostic_namespace` in
`contracts/schemas/xfactory-domain-stack.schema.yaml`. The vocabulary is REUSED
in shape, not re-coined.

## 2. The grammar: reused rather than invented

`identity_namespace` carries identity-brokering's identifier pattern — the same
one `holder_ref`, `fetch_identity` and `requirement_ref.requirement_id` carry —
and the reason is a measurement rather than a preference. The shapes a real
namespace takes were listed and driven against the pattern before it was chosen:
an Entra tenant domain (`contoso.onmicrosoft.com`), a directory GUID
(`72f988bf-86f1-41af-91ab-2d7cd011db47`), an AWS account id (`123456789012`), a
Vault namespace path (`admin/eng`), a Keycloak realm name (`xfactory`). All five
match `^[A-Za-z0-9][A-Za-z0-9._:/-]*$` within the 200-character bound. A second
pattern would have bought nothing and would have been a second thing to keep in
step with the projection.

**A CONSEQUENCE OF REUSING IT, TAKEN DELIBERATELY**: the pattern admits `ghp_…`,
`AKIA…` and base64-shaped values, exactly as it does for the two members beside
it. That is why the member joins the `baked-secret` screen in the same commit —
see § 5.

## 3. The comparison, and why it is ONE predicate

Canon states the comparison in ONE sentence — the lift's third condition, which
this packet rescopes from *"their fetch identities DIFFER"* to *"their fetch
AUTHORITIES DIFFER"* — and RAISES the named `shared-authority-identity` finding
on the same comparison. Two callers, one sentence.

The first draft of this realization rescoped the FINDING and left the LIFT
comparing bare strings, and the defect that produced was found by EXECUTION
rather than by reading: a pair sharing a `secret_ref`, declaring one fetch
identity in two different namespaces, escaped the named fault (correctly) and
was then refused by `shared-secret-identity` (incorrectly), because the lift's
third condition still saw one identity. **A reader would have been told about
two credentials collapsing into one and would have split the secret, leaving the
namespaces untouched** — the wrong repair, under the wrong finding, which is
exactly what *"a refusal shall name the fault it found, and name it once"*
exists to prevent.

The repair is `_same_fetch_authority`, called from both sites. The packet's own
inherited lesson applies to it: a prescription that has to be BUILT to find its
defect is a prescription that should have shipped with the build.

## 4. Why the fallback REPORTS

Three shapes reach the fallback: no namespace on either side (every record that
exists today), a namespace on ONE side, and a namespace that does not match the
grammar. All three compare the bare fetch identity and all three REPORT.

**The one-sided case is the one that decides the design.** If absence CLEARED,
an estate holding a genuine authority collapse could silence the refusal by
deleting a member from one of the two bindings — without writing a single false
statement, and while leaving the true one on the other binding. A rule that can
be turned off by omission is not a rule, and it would be a strictly worse
instrument than the over-report the member exists to end: the over-report is
visible, and the silence is not.

**The ungrammatical case follows from the same reasoning and not from tidiness.**
Clearing a finding on a value nothing could read is the FAIL-OPEN shape this
family has already had to repair once, in a drift check that treated what it
could not read as satisfied. So an unreadable namespace is treated exactly as an
absent one by the comparison — and is warned in its own right beside it, so the
record says what happened.

**AND THE MESSAGE CARRIES IT.** Where the comparison READ a namespace on both
sides, the finding names it (*"authenticating as 'runtime_identity' in
identity_namespace 'directory-tenant-a'"*), because *"authenticating as
'runtime_identity'"* is ambiguous in precisely the way this member exists to end.
Where exactly one side declared one, the message says the comparison FELL BACK
and names the remedy that keeps the record TRUE — declare the namespace on BOTH
bindings, never delete it from the one that has it.

## 5. The third free string, and why it is screened now

`add-binding-consumer-identity` § 2.6 extended `_looks_like_raw_secret` from
`secret_ref` alone to `consumer.holder_ref` and `consumer.fetch_identity`, IN
THE RELEASE THAT DECLARED THEM, with one registered negative per field. The
reasoning was that a new free-string sink on the one record kind whose invariant
is *"never bake a secret"* is a GAP rather than a permission.

That reasoning reaches a third member identically, and the alternative was
considered: defer the screen to the major on the ground that a raw secret in a
namespace validates on the current major, so refusing it now is a narrowing.
**REJECTED.** It is the same act § 2.6 took, at the same point in a member's
life, and taking it a release later would leave a sink unscreened for exactly
the window in which nobody is looking at it — reopening the gap § 2.6 closed,
one member on. The narrowing is real, it is NAMED in `target_release:` rather
than hidden, and it refuses only a record that bakes a credential into a
contract.

The § 2.6 limit is carried unchanged rather than re-claimed: `_B64ISH` requires
forty characters, so a 38-character alphanumeric secret passes this screen. The
screen catches SHAPES it recognises; it is not a secret detector.

## 5b. What the member does NOT do to the stub exemption

`_declares_stub` grants the exemption to a block that declares the const-true
token AND NO IDENTIFIERS. `identity_namespace` is deliberately NOT added to that
test, and the decision is stated rather than left to be read off the code: a
namespace names a DIRECTORY, and naming a directory names no principal. A
template written before any install exists may legitimately already know which
tenant will issue its identity, and withdrawing the exemption from it would warn
every such scaffold for the whole minor while teaching nothing.

The other half is unchanged and still holds: a block carrying a LIVE identifier
beside the token loses the exemption, exactly as PR #516's Codex round required.

## 6. #553 — the ambiguity is per-document, and canon now says so

**This section is #553's and touches nothing of #511's.** It is here because the
two rulings ride in one MODIFIED block, and a reader must be able to see which
edits belong to which act.

**The gap, inherited rather than introduced.** Canon's scenario *"The requirement
reference resolves to more than one record"* — promoted 2026-08-31 when
`add-binding-consumer-identity` archived — reads *"matches requirement records in
more than one document, or more than one record in a document"*. The shipped
resolver cannot see the first arm: `resolve_requirement`
(`scripts/validate-credential-contracts.py`) matches
`[r for r in index.get(doc_ref, []) if r.get("id") == rid]` against the ONE
document the reference names, over an index keyed BY DOCUMENT PATH. A `dup_lane`
declared once in `a.requirements.yaml` and once in `b.requirements.yaml`
resolves `ok` from a reference naming either.

**Codex raised it** on PR #542, round 3, 2026-08-31 23:54 UTC, against the tip
that was ratified. **Brett ruled it 2026-09-01** — SCOPE TO PER-DOCUMENT, the
cross-document arm filed as issue #553 — and ruled #553 itself on 2026-09-03:
**AMEND THE PROMOTED SCENARIO, DO NOT BROADEN THE RESOLVER.**

**Two edits, and the count is the point.** (1) The scenario's WHEN becomes
*"matches more than one requirement record in the requirements document the
reference names"* — the cross-document arm dropped. (2) The six-conditions
sentence's *"resolving, in the repository under validation, to EXACTLY ONE
requirement"* becomes *"resolving, IN THE ONE REQUIREMENTS DOCUMENT THAT
REFERENCE NAMES, to EXACTLY ONE requirement"*. Every other scenario title and
every other body sentence of that requirement is byte-identical or carries only
#511's edits.

**What is NOT touched, cited rather than edited.** `resolve_requirement`, its
`ambiguous` status, and `add-requirement-ref-resolution-integrity`'s `tasks.md`
§ 3.4 freeze — *"`resolve_requirement` is CALLED, not edited: same statuses,
same index, same grammar, same never-open-a-path rule"* — all stand exactly as
they are. That packet is ACTIVE and RATIFIED, and this packet does not write
inside it. Its § 9.4 obligation, which forbids leaving the contradiction
standing, is DISCHARGED by the AMEND branch § 9.4 itself names.

**And the rule that survives is stated, so the amendment is not read as a
tightening.** Requirement ids are NAMESPACED BY THEIR DOCUMENT. Repository-wide
uniqueness of a requirement id is NOT a rule, was never one, and is not made one
here: two requirements documents may legitimately each declare a short id of
their own. What canon now says is what the resolver does — a reference is
resolved WITHIN THE DOCUMENT IT NAMES, and ambiguity is ambiguity there.

## 7. Delta placement, and the collision that decided it

Both requirements this packet writes are PROMOTED CANON in
`openspec/specs/credential-contracts/spec.md`, added by
`add-binding-consumer-identity` and promoted at its archive. So:

- **The blocks are `## MODIFIED Requirements` and carry no `Modified over`
  marker.** `govern-sibling-added-modified-deltas` reserves that form for a
  block whose requirement exists only as an ACTIVE sibling's `ADDED` or
  `RENAMED` `TO:` title. Naming an archived basis would be the misdeclared state
  that packet's own arm reports.
- **Both blocks are copied VERBATIM from canon at `origin/main` and then
  edited**, and the copy was verified programmatically before a byte was
  changed. `modified-block-currency` runs at `error` on this family.
- **Two ACTIVE changes hold `credential-contracts` deltas and NEITHER holds
  either requirement**: `add-credential-escrow-checkout` MODIFIES *"Canonical
  credential record shapes"*, and `add-requirement-ref-resolution-integrity`
  holds two ADDED requirements. Checked at authoring time against the branch's
  merge-base and again before the PR.
- **A third writer wanted one of them, and that is why this packet is a fold.**
  The lane holding #553 stopped before authoring for exactly this reason. Two
  live MODIFIED blocks on one requirement are not a merge conflict — they are a
  SILENT REVERT at archive, invisible in both reviews, because whichever
  archives second is the whole text canon keeps.

## 8. The contracts-and-release decision

The member changes the SCHEMA FILE's bytes, so two things follow and no more.
The `contracts/manifest.yaml` row's `sha256` is recomputed in the same commit —
forced by `test_manifest_row_digest.py`, which reds at the commit rather than at
a consumer that pinned a digest for bytes nobody shipped — and its
`consumption_rule` gains the member's paragraph, because that field is what a
cross-repository consumer reads to learn what it is pinning.

**THE CUT IS NOT PART OF THIS CHANGE**, by the ruling's own words, and the
version-headed `contracts/CHANGELOG.md` entry goes with it rather than here.
That is this repository's ritual and not a deferral of convenience, and this
packet watched the ritual run under it: PR #616 was the `contract-v3.1` cut and
wrote the CHANGELOG, the manifest,
`contracts/releases/contract-v3.1.digests.yaml` and the policy doc together —
it MERGED while this packet was in review, and its `contract-v3.1` was then
found DEFECTIVE and SUPERSEDED by `contract-v3.2` (PR #624) before this packet
landed — two bundle moves under one unchanged packet, which is precisely why no
number was written here. A
version heading written here with no tag and no inventory would be a HALF CUT,
and it would spend a number another packet is holding. § 5 of `tasks.md`
prescribes the entry verbatim so the cut has nothing to invent.

## 9. What this change is not

- It is not a claim that the declared namespace matches the provider's directory.
  Where they disagree the directory governs, and detecting that is live-estate
  reconciliation.
- It is not a cross-repository comparison. One validator reads one repository,
  and the residency model puts two consumers' bindings in two trees.
- It is not a requiredness. The member is optional at BOTH releases, and making
  it required would be a narrowing nothing warned about.
- It is not a weakening of `shared-authority-identity`. The finding fires on
  every shape it fires on today except one: two grammatical, declared, DIFFERENT
  namespaces — which was never the fault it names.
