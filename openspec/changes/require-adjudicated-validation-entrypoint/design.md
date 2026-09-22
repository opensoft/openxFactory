# Design: require-adjudicated-validation-entrypoint

Status: ratified
Ratified by: require-adjudicated-validation-entrypoint — 2026-09-22, Brett Heap, "ratify #1140 and #1141" at head `c36ff08c` (record `review/ratification-2026-09-22.md`)
Kind: design

The ruling disposed of one box. These are the decisions this packet reaches in
turning that into a general rule — each with what vetoing it costs.

## D1 — The rule is about the ASSERTION, not only about the run

`neutral-product-pin` already obliges a consuming repository to INVOKE strict
validation only through the pin's `consumer_entrypoint:`. The obvious reading is
that a box instructing the raw command is already unlawful and no new requirement
is owed.

**That reading was tested and does not hold, for two reasons.**

1. **The existing requirement's subject is the BINARY, and its reason is PATH.**
   It says the entrypoint "SHALL resolve the CLI from the verified artifact
   rather than from `PATH`, so that whatever binary an engineer or a runner
   happens to have installed CANNOT determine a gate's verdict". A reader who
   obeys it completely may still believe the two commands reach the SAME verdict
   by different routes — one audited, one not. **They do not**, and the
   measurement is in `proposal.md`: exit 0 against exit 1 on one tree, same
   finding. The new fact is that the raw verdict is not a less-audited form of
   the repository's verdict but a DIFFERENT one.
2. **An assertion is not an invocation.** § 8.9's defect was not that somebody
   ran the wrong binary — nobody had to run anything for the box to be
   undischargeable. The defect was in what the box WROTE DOWN as its evidence.
   A rule reaching only runs cannot reach a record.

**Veto cost:** the packet. If the existing requirement is judged to cover this,
the honest act is to close this change rather than to weaken it — and then the
next box is written the same way with nothing to cite against it.

## D2 — `## ADDED` to `neutral-product-pin`, not `## MODIFIED` on the neighbour

The alternative was to MODIFY *A consuming repository runs OpenSpec validation
only through the pinned entrypoint* and fold the assertion rule into it.

**Rejected on two measured costs.** A `## MODIFIED` block must carry the whole
requirement, so it would put every one of that requirement's units and scenarios
into a currency relationship with canon for as long as this packet is active —
and this repository is currently carrying a live disposition for exactly that
class of drift. And the two rules have different subjects: one is about resolving
a binary, the other about what a record may claim. An ADDED requirement states
the second without re-opening the first.

**Veto cost:** one delta shape. The requirement text would survive a fold
substantially unchanged.

## D3 — The staleness property is carried as a SCENARIO, and deferred to by name

The property is already ratified in this same capability — *A dispositioned
finding is cited, upgrade-coupled, and refused when stale* — including the
whole-corpus staleness refusal and the narrowed-scan carve-out.

**So it is not re-legislated.** Restating it as a requirement would duplicate
canon inside one spec file, which is the defect the carriage rules exist to
catch. It appears here only as the ANSWER TO AN OBJECTION — that naming the
wrapper substitutes a suppressor for a check — and the scenario says in its own
last bullet that these are "the standing properties of *A dispositioned finding
is cited, upgrade-coupled, and refused when stale* rather than new tolerances".

**Veto cost:** one scenario, and an unanswered objection that this requirement
invites by its own subject.

## D4 — No checker is proposed, and that is a decision

The estate's precedent for gating a prose header is a `scripts/validate-*.py`
plus a corpus test in the required suite — `validate-code-surface.py` and
`validate-target-release.py` both. A sibling for this rule is imaginable.

**It is not proposed, because the measurement that would justify it has not been
taken.** Two things would have to be known first: how many live, non-archived
assertions the rule actually reaches, and whether a mechanical reader can tell an
ASSERTION of a green corpus from a CITATION of this very defect — this packet's
own `proposal.md` and delta both contain the raw command as quoted text, and so
would every future record about it. A checker that could not tell those apart
would red the packet that defines it.

**Veto cost:** none to the rule. A successor may take the measurement and propose
the gate; `tasks.md` § 5 names it as residue rather than sweeping it.

## D5 — The upstream fix is REGISTERED, never proposed

`tasks.md` and `proposal.md` both record what would retire the marker-blindness
class: an upstream CLI that reads the declared rename. They do not propose it.

**Three reasons, each measured.** The CLI is CONSUMED and never vendored, so
there is no fork in this estate to patch. Moving the pin is a ratified HUMAN-ONLY
act that must carry target-version evidence and re-derive every disposition in
the same change — so a bump proposed here, with no measurement of whether
`1.13.1` reads the marker, is precisely what those requirements refuse. And
retiring the class would not retire this requirement anyway: a second disposition
class is live in the pin file today, and any future disposition re-creates the
divergence.

**Veto cost:** a paragraph. The registration is honest bookkeeping, not a
commitment.

## D6 — What this packet does NOT do

- **It does not touch the disposition mechanism.** `contracts/openspec-cli-pin.yaml`
  is not edited, `reconcile()` is not edited, and no disposition row is added,
  altered or retired. The mechanism works; the requirement leans on it.
- **It does not edit § 8.9, or any ratified or archived text.** That box took its
  own packet's `[~]` contingency under `5778397686`. This requirement governs
  what is written next, and says so in its own body.
- **It ratifies nothing.** `tasks.md` § 1 is open.
