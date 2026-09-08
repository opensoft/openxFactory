# Proposal Ratification: add-binding-consumer-identity

Status: ratified
Decision date: 2026-08-29
Ratifier: Brett Heap (repository owner) — in-session via question prompt
Ratified: 2026-08-29 by Brett Heap (repository owner) — in-session via question
prompt; record: this file.
Ratified baseline: this change as committed in the ratification commit carrying
this record (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/credential-contracts/spec.md` — 1 MODIFIED requirement and 3 ADDED, 36
scenarios), validated `--strict` and `--all --strict`.

## Decision

**RATIFY.** The requirement set stands as it is at this record's commit.

This change extends the published `xfactory_credential_binding_template` with an
additive optional `consumer:` block — a holder reference and a fetch identity —
so that the per-system authority `add-notebook-hosting-credential-custody`
ratified on 2026-08-23 becomes a fact of the record rather than an invariant held
by review. It is the successor that packet named five times and could not perform
itself, because extending `contracts/schemas/` carries the contract-release
ritual.

**This ratification authorizes realization; it does not perform it.** The change
carries a code surface and `target_release: the next additive minor`, so it
archives only on merged code with green realization evidence per
`release-realization`. **No contract byte moves with this ratification**, no
number is spent, and `contracts/` is untouched by the ratified diff.

## How this text was arrived at — the chain, in order

The ratified text is not the authored text, and the distance between them is the
point of the record.

1. **Three bot rounds on the authored packet.** Copilot twice (2 findings + 3
   previously-missed), Codex once (3 P1s). All taken. Four author self-catches
   landed alongside them.
2. **A §7.4 COUNCIL REVIEW, 2026-08-29**, convened outside the clearance pipeline
   by design — proposals are never-convenable through it on the unanimous ruling
   of 2026-08-28. Four seats sat: `lead-architect`, `lead-security`,
   `lead-quality`, `company-policy-lead`. **SPLIT 2–2 on the verdict word;
   UNANIMOUS 4/4 that the text as drafted was not ratifiable.** Fifteen blocking
   amendments. `split_vote: park_for_liaison` fired for the first time in that
   body's history.
3. **Brett's ruling of 2026-08-29 on the ballot: ACCEPT ALL BLOCKING
   AMENDMENTS**; one fix round on PR #497 dispatched to the packet's author; the
   ratification read after. Two procedural gaps written down in the same act —
   see "What this ratification does NOT cover".
4. **The fix round**, four commits: all fifteen blocking amendments carried, all
   sixteen non-blocking taken or refuted from the record with citations, and the
   convener's own finding corrected.
5. **Three further bot rounds on the fix round**, which found six more instances
   of the same defect class the council had convened over. All taken.
6. **This ratification.**

**Twenty-two findings taken across the whole arc; three refuted from the record
with citations.** The council record of authority is codexFactory
`hermes/domain/review-councils/records/2026-08-29-council-review-add-binding-consumer-identity.md`
— its §8 is the sole disposition — with the verbatim seat returns beside it at
`records/2026-08-29-seat-returns/` and the convening packet at
`convening-packets/2026-08-29-openxfactory-binding-consumer-identity.md`.

## What the council changed, and what survived

**The decisive repair, reached four ways** (LA-A1 · LS-A5 · LQ-A10 · CPL-A3).
The block's `required:` list landed at the introducing MINOR while the closure
correctly deferred to the MAJOR — so the packet phased one narrowing vector and
left others unphased, and **falsified a scenario that would have promoted into
canon**. Every seat that found it found it the same way: by BUILDING the
prescribed schema and driving a record through it. Two Copilot reviews, three
author self-catches and a Codex P1 round had all read the prescription instead.

**The repair is uniform phasing**: at the minor the schema constrains nothing
about the block; every constraining act lands together at the major behind one
deprecation window. Verified by construction, per CPL-C3, rather than by a second
prose read.

**What no seat refused was the change's purpose.** `lead-architect`: *"the
change's purpose is right, its measurements are honest, and its carriage is
lossless."* `lead-security`: *"I refuse the definition, not the change."* The
delta was measured loss-free by two seats independently and re-measured after
every edit that touched the MODIFIED block, per LQ-C2.

## Three questions the bench routed to the liaison, all ruled

Recorded separately from the ratification because each decides something the
council deliberately declined to decide.

1. **Decision 2 — ROUTE (i).** Phase the requiredness with the closure; keep the
   promise. Route (ii) — delete the promise and strike the scenario — is
   preserved in `design.md` §5 as a coherent design considered and ruled against.
2. **P-2 — SYNTHETIC IDENTIFIERS.** Parked by `lead-security` under its own
   escalation rule: may the packaged, digest-pinned, distributed corpus name the
   LIVE xFactory sync-lane and openXdox fetch identities? **It may not.** They
   stay in the consuming installs' own `credentials/` trees under the residency
   model. P-2 is DISCHARGED, not parked.
3. **P-3 — FILE THE SUCCESSOR NOW.** Filed as openxFactory **#502**, the
   estate-level MODIFIED-over-a-sibling's-ADDED governance gap: no governing
   requirement, no evaluating arm, no marker. **This change neither closes nor
   waits on it**, exactly as both raising seats required; it carries only its own
   local stopgap, a pre-archive assertion that canon holds the requirement title.
   A precision the packet owed itself and this record repeats: the seats cited
   EIGHT pairs; measured live that is FOUR, eight being the cumulative figure.

## The verification gap, in view at the read and accepted

**Brett ratified with this in view and chose to ratify rather than wait.**

Codex's last actual review was of `eb92cf90`, two heads before the ratified tip.
Its usage limit refused every request thereafter — six refusals across the
session. So the two commits that took its final four findings, and Copilot's
subsequent header finding, **were not re-read by the prescriber**. Copilot did
return CLEAN on the final head, which is real verification by a different reader
and is not the same thing.

This is recorded rather than rounded up because the packet's own quotable
sentence — the one `lead-quality` asked be carried as precedent — is exactly
about it:

> **A prescribed fix applied without a verifier is an unverified change, whatever
> its provenance.**

The mitigation actually relied on is not a bot: it is that **four independent
seats read this text end to end**, that every subsequent finding was reproduced
by execution before it was taken, and that the realization gate is still ahead —
merged code plus green evidence plus a contract cut, none of which this record
performs.

## Conscious-acceptance notes (Brett, at ratification)

1. **The block is DECLARED here and CONSTRAINED at the major.** Nothing narrows
   at this cut, and that is a measurement rather than a claim: six shapes a
   domain could already hold were built and driven against the prescribed minor
   schema, and all six validate. Seven breaking acts wait for one major behind
   one deprecation window and eight warning codes.
2. **The lift is real and it is fail-closed.** Two consumers of one deliberately
   shared credential become expressible — the shape the predecessor had to
   DECLINE — but only through six independent conditions over every pair, the
   sixth binding each reference to its own binding's map key. A security seat
   defeated the five-condition draft by execution on this capability's only red
   proof of serving-tier separation; condition six is what refuses it.
3. **The honest reach is honest in both directions now.** A declared consumer
   makes revocation of ACCESS readable; it does not un-share a bearer secret
   already fetched, and eviction still requires rotation reaching everyone. AND
   the record now publishes which principal reaches which secret — a disclosure
   the first three limits omitted, added as a fourth limit with its own scenario.
4. **The check is intra-document; the estate is not.** No per-repository
   validator can compare two consumers declared in two repositories. What this
   delivers there is readability at each site; the cross-repository sweep is an
   owed successor.
5. **`contracts/` is untouched by this change and a cut is owed at realization.**
   The minor is allocated then, by merge order — `add-credential-escrow-checkout`
   is already spending one on the same file and main is a third writer of that
   manifest.
6. **No live secret is created, moved, or read** by this change or its
   realization. The block names identifiers; it holds no material.

## What this ratification does NOT cover

- **It does not ratify the realization.** Tasks §1–§7 are authorized, not
  performed. The change stays ACTIVE until merged code, green evidence and the
  cut exist.
- **It does not settle the sitting's own charter.** Brett sanctioned
  convener-act seating for proposal reviews PENDING a charter amendment, and
  defined a 2–2 split on a proposal review as parking for the liaison. Both ride
  codexFactory issue #131 and are recorded at §8.3 and §8.4 of the council
  record — not here, because they govern the council rather than this packet.
- **It does not close #502**, and this change must not be delayed for it.
- **It does not decide the self-test count derivation**, which is filed as its
  own `credential-contracts` test-hygiene issue.

## Next

Realization per `tasks.md` §1–§6, which carries the contract-release ritual this
change's predecessor deliberately did not: the schema block, the warning channel
the validator does not have today, eight deprecation codes with a packaged probe
each, the fixture corpus including a `warning/` home that does not exist yet, the
`Deprecations Currently In Force` entry, and the cut. The ordering obligation at
§7.2 binds: this change SHALL NOT archive before
`add-notebook-hosting-credential-custody` does.
