# Design: amend-neutral-product-pin-source-tree-digest

Status: draft
Kind: design

The ruling fixes the OUTCOME and its GROUND. It does not fix the sentences, and
these are the decisions this packet reaches beyond the ruled word — each stated
with what vetoing it costs, so a reader can strike one without re-deriving the
packet.

## D1 — Amend the clause, rather than record an exception beside it

**RULED, not designed.** `#656` comment `5777949892`, 2026-09-22T14:04:00Z,
Brett Heap, by multi-choice: **"(b) — AMEND THE CLAUSE."** The alternative (a)
was to leave the ratified text standing and carry the pin shape as a declared
exception. The ruling's own reason is recorded with it: *"It leaves ONE rule in
the corpus rather than a rule and an exception, and its reasoning is already
written in the requirement three paragraphs down."*

**Veto cost:** the whole packet. This is the commission.

## D2 — An enumeration stays LAWFUL and stays OWED where no whole-tree digest is recorded

The amendment ADMITS a second discharge; it does not replace the first. Two pins
in this repository carry per-file lists — `contracts/openxwallet-pin.yaml` (eight
`files:` digests and a `pinned_by_commit_only:` list) and the openRepoShape pin —
and both stay conformant, unedited, on the clause's original words.

**Why it is written rather than left implied.** An amendment that said only "a
whole-tree digest discharges the obligation" would leave open whether a pin with
NEITHER form had discharged it, since the sentence granting the equivalence would
be the newest one and could be read as the operative one. The paragraph therefore
closes that reading in its last sentence: *a pin that records NEITHER a per-file
list NOR a whole-tree digest over the commit's tree has discharged nothing.*

**Veto cost:** one sentence, and a hole where a pin carrying no digest of any
kind could claim the equivalence.

## D3 — The boundary goes in the NORMATIVE text, not only in the proposal

The ruling says what to admit. It does not say where the admission stops, and an
equivalence granted without a stated boundary is the shape every over-broad
exception has. Two boundary statements are therefore in the requirement itself:

1. **WHICH FORM, never WHETHER.** The equivalence is about which form the digest
   obligation takes and never about whether digests are owed, so it authorizes
   skipping no digest anywhere.
2. **THE RUNTIME-DEPLOYMENT CLAUSE IS UNTOUCHED.** That clause — carried here
   verbatim from `split-opendox-two-layer-product` — forbids reading a
   deployment declaration as permission to skip the digests. The amendment says
   in as many words that it is *"untouched by it and narrowed by it in no
   respect"*, and scenario *The equivalence is cited as permission to skip a
   digest* refuses the misreading directly.

**This is the one place the packet could have done harm, and the first draft
did.** The runtime clause's own sentence names "commit and per-file `sha256`" as
the trusted referent. That phrase is carried WITHOUT EDIT: correcting it to name
the admitted second form would be a normative change to a clause the ruling did
not reach, in a packet commissioned to amend a different clause.

**THIS CLAUSE TOOK TWO REVIEW ROUNDS AND THE SECOND OVERTURNED THE FIRST. Both
are recorded, because the discarded reading is the instructive one.**

*Round 1 (Copilot `r4073177274`).* The first draft granted the equivalence to any
source-tree pin and separately asserted the runtime clause was "untouched", with
nothing reconciling the two. That was a real defect: an assertion is not a scope.
The round-1 repair EXCLUDED runtime-clause-governed pins from the equivalence.

*Round 2 (Copilot `r4073495698`) — and the exclusion was wrong.* Measured:
`contracts/opendox-pin.yaml`:190 carries a real `migration:` block
(`range: "0001..0002"`, `reversible: false`, a named runbook) **and** a whole-tree
`digests.tree_sha256` with no per-file list. So the runtime clause GOVERNS that
pin, and an exclusion would have made **the very pin this amendment was ruled
for** non-conformant — the exact opposite of RULED `5768144952`, which settled
that this is the shape it keeps. A reading that breaks the pin the ruling was
about is refused by that fact alone.

**The resolution, which is the reading that was available all along.** The two
clauses govern DIFFERENT obligations. The runtime clause governs what a bump must
DECLARE — the migration range, the reversibility, the runbook — and this
equivalence governs which FORM the completeness obligation takes. So the
equivalence reaches a source-tree pin whether or not its product is a runtime,
and every obligation that clause imposes stays owed in full, its prohibition on
reading a deployment declaration as permission to skip the digests preserved
exactly. Where it names "commit and per-file `sha256`" it names the referent a
FILE-READ pin carries; a whole-tree pin's referent is its commit and its tree
digest, **which is not less verified and not less trusted**. That is a reading of
the clause under the amended definition of "the digests", not a weakening of it:
nothing it forbids becomes permitted, and nothing it requires becomes optional.

**What "do not touch the runtime clause" meant, stated so the next reader does
not repeat round 1.** It meant do not weaken the deployment obligation. It did
NOT mean carve runtime products out of the equivalence — and conflating those two
is what produced a repair that broke a live pin.

**Veto cost:** two sentences and one scenario, and an equivalence whose edges a
later reader has to infer.

## D4 — The block is written over the basis's OUTCOME

`split-opendox-two-layer-product` holds an active `## MODIFIED` block on this
same requirement, ratified 2026-09-05, contributing the runtime-deployment
clause, its own per-requirement record and two scenarios.

**Considered and rejected: write over canon as promoted.** That block would carry
five scenarios. The moment the basis archived, canon would hold seven and this
block would omit two — the exact finding class `contracts/openspec-cli-pin.yaml`
records as *"canon moved under an un-re-derived delta"*, which costs a disposition
row, a citation and a human reading. Writing over the outcome makes the block
correct in both orders: while the basis is active the declaration is the record
of why, and after it archives the block simply matches canon.

**The form is the basis's own**, one link up this chain: `split-opendox` wrote
its block over `add-openspec-cli-pin`'s outcome and recorded it in a dated
per-requirement paragraph, explicitly NOT the reserved pairing marker (whose form
is reserved for a basis that ADDS an unpromoted requirement). This packet
follows it exactly, and adds the `sequenced_after:` declaration the substrate
now provides.

**Veto cost:** a re-derivation of the block against canon plus a disposition row
when the basis archives.

## D5 — `code_surface: none`, and the measurement is the argument

Not asserted from the shape of the change but measured, and the measurement is in
the front matter with its commands. The short form: **no code in this repository
enforces the per-file obligation on a source-tree pin**, so there is nothing for
an amendment admitting a second form to move. The two pin verifiers never read
either key; the two that do read `pinned_by_commit_only:` read it with an
absent-is-empty default; the 105 tests over the two pin packages build their
fixtures in exactly the shape this amendment admits and pass unchanged.

**The consequence is procedural and worth stating:** an empty code surface
archives on landing plus the task list, not on merged-plus-green realization
evidence. There is no realization pull request to wait for.

**Veto cost:** if the measurement were wrong, the packet would owe a realization
gate. It is re-runnable from the front matter's own commands.

## D6 — What this packet does NOT do

- **It edits no pin file.** What `contracts/opendox-pin.yaml` and
  `contracts/openxdox-pin.yaml` carry was settled and executed by `5768144952`;
  this packet settles only the normative text. The openXdox-side header
  amendment registered by that ruling is a different repository's act and is
  named as residue in `tasks.md` § 5.1.
- **It answers one of three pre-stage findings, and says so.** `#1139` review
  `5273796676` registered three; `5777949892` answers the `neutral-product-pin`
  per-file one. `corpus-adapter-seam` and `domain-mapping-declaration` stay as
  ratified, registered for a successor.
- **It ratifies nothing.** `tasks.md` § 1 is open.
