# Staged: a governed derived RECOMMENDATION — a ranked member role, an evidence floor, and editorial weights

Status: staged
Kind: capability-proposal
Summary: `governed-derived-model` gains the three things a domain needs before
it can derive a RANKED SET OF OPTIONS with reasons attached — a third member
role, `role: recommendation`, whose outputs are ordered, cited and
non-authoritative; a declared `evidence_floor` dial with labelled, structurally
non-mixable relaxed modes; and an `editorial_weights` declaration for ranking
inputs that no truth store supplies. MedxFactory's treatment-options engine is
the forcing case, but none of the three gaps is medical.
Topics: governed-derived-model, derived-recommendation, ranked-options,
evidence-floor, evidence-grade, editorial-weights, omnigent-domain-overlay,
workflow-gate-contract
Repository context: openxFactory. This fragment holds ONLY the neutral half —
`governed-derived-model` (the derived-recommendation member role, the
evidence-floor dial, and the editorial-weights declaration), with
`omnigent-domain-overlay` and `workflow-gate-contract` supplying the
already-promoted refusal and gate surfaces this topic must not re-invent. The
realized half — the corpus backfill under `root-truth-grounding`, the new
mapping tables under `terminology-normalization`, and the engine itself under
`treatment-plan-generation` — is MedxFactory-owned and moved to that repository
2026-09-07 (see "Moved to MedxFactory" below). The neutral delta is the one
that needs designing; the Medx work is comparatively mechanical once it lands.
Staging ID: openxFactory:staging:treatment-options-engine
Captured: 2026-08-26
Source: Brett Heap, in session 2026-08-26, deciding to build rather than
explore — "we will build this". The six-step capability description that forced
this neutral delta is clinical and moved with the MedxFactory half.
Target capabilities: MODIFIED `governed-derived-model` (a derived-RECOMMENDATION
member role whose outputs are ranked, cited, and non-authoritative; a declared
evidence FLOOR per family with a labelled, non-mixable relaxation mode; and a
declaration for ranking weights that come from editorial judgement rather than
from the family's truth store). The MedxFactory-side targets —
`root-truth-grounding`, `terminology-normalization`, `treatment-plan-generation`
— were never fenced as `xspec:candidate` targets here, because they are
Medx-owned capabilities that do not resolve from an openxFactory document and
fencing them would emit tag-hygiene findings for a claim this repo cannot host;
they moved with the clinical half.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

Settled by Brett's 2026-08-26 decision, or by facts verified against the live
corpus the same day (the corpus verification moved with the clinical half). The
open questions do NOT reopen these. The numbering is the original's: claims 3,
4 and 7 are clinical and moved, and their numbers are left as gaps so the
claim-by-number cross-references in both halves keep resolving.

1. **We are building it.** This is a build decision, not an exploration. The
   six-step capability description is the capability description, not a menu —
   the six steps are clinical and moved with the MedxFactory half.
2. **A recommendation member PROPOSES; a named human DECIDES.** The output is a
   ranked list of options with cited reasons. Nothing about it selects, orders,
   executes, or repeats an external action. The Omnigent constitutional
   `execute_final_action: false` and `access_secrets: false` hold unchanged, and
   the domain's own decision gate stays human-reviewed. This is the governance
   boundary of the whole topic and it is not a dial.
5. **Floor-conforming first; a relaxed floor is a separate MODE, not a widened
   default.** Relaxed-mode results carry their evidence grade prominently and
   are structurally un-mixable with floor-conforming results. One list
   containing both, sorted together, is the failure this claim exists to
   prevent.
6. **Ranking weights the truth store does not supply are EDITORIAL POLICY,
   governed separately.** A truth store states facts but rarely grades them on
   a common scale. Severity numbers and combination weights are therefore
   judgement, versioned, human-reviewed, and VISIBLE in every output that used
   them — never buried in a scoring function.

## Moved to MedxFactory

Clinical corpus and engine content moved 2026-09-07 to MedxSoft/MedxFactory
`ideation/staging/treatment-plan-generation/treatment-options-engine-clinical.md`
(see that repo). What left, in the original's own section order: the
`Current state, verified against the live corpus (2026-08-26)` corpus recon;
claims 3, 4 and 7; `What changes → The MedxFactory half — corpus, tables,
engine`; `Build order`; the MedxFactory-side `Impact` code paths and the
clinical illustration of the recommendation-object bullet; idea notes 1–6;
conflicts 1 and 3–6, plus the clinical illustration of conflict 2; all ten
`Open questions` (Q1–Q10); the five MedxFactory `Related work` entries; and the
MEDX half of `Exit`. Claims 1, 2, 5 and 6, the recommendation-object impact
bullet and conflict 2 keep their neutral RULE here and their full clinical
illustration there.

## Why

<!-- xspec:candidate target=governed-derived-model -->
`governed-derived-model` promotes the shape of a derived object that must never
become truth: non-authoritative by construction, fully provenanced, read-only
against its truth store, zero action authority, and promoted to action only
through a named human. What it does not yet describe is the object that a
clinical, financial, or operational domain most wants to derive — a RANKED SET
OF OPTIONS with reasons attached. The promoted vocabulary has `role: model` and
`role: scenario`, and a scenario's outputs are `hypothesis_proposed | no_signal
| discarded` — an unordered verdict per hypothesis. A recommendation is ordered,
and the ordering is the product. Nothing in the promoted family says what a
ranking may rest on, whether the ranking's inputs must be visible, or what
happens when the ranking is produced from weights that no truth store contains.

Two further gaps show up the moment a domain tries. The first is the EVIDENCE
FLOOR. Every derived family rests on evidence of some grade, and a family that
can lower its floor deliberately — to hypothesise rather than to recommend — is
a normal and useful thing. What is not normal is lowering it silently, or
letting a floor-relaxed result be sorted into the same list as a
floor-conforming one. The promoted family has no dial for this, so a domain
that wants a hypothesis mode either invents one or leaves the distinction to
prose. The second is EDITORIAL WEIGHTS. A ranking almost always needs numbers
the truth store does not supply — a severity scale, a combination weight, a
tolerance for one class of harm over another. Those numbers are judgement.
Under the promoted "full provenance" requirement they have no home: they are
neither an evidence-traced fact nor a declared assumption about the subject.
They are policy, and policy wants a version, a reviewer, and visibility in the
output it shaped.

MedxFactory is the forcing case, but none of the three gaps is medical.
LedgerxFactory ranking remediation options, OpsxFactory ranking mitigations, and
AdxFactory ranking channel allocations all want the same object with the same
three properties, and all three would otherwise each invent it.
<!-- /xspec:candidate -->

## What changes

### The neutral half — a MODIFIED `governed-derived-model`

<!-- xspec:candidate target=governed-derived-model -->
A third member role, `role: recommendation`, joins `model` and `scenario`. A
conforming recommendation member emits an ORDERED set of candidate options; each
option carries the evidence references that admitted it and the references that
would have excluded it; the ordering criterion is declared rather than implicit;
and, like every other member of the family, the object is non-authoritative by
construction with a named human promoting authority. Its output-status
vocabulary keeps the promoted property that no value can represent an order,
launch, posting, or other external action — an option is proposed, or it is
withheld with a reason, and there is no third thing it can be.

A family declares an `evidence_floor` dial: the minimum evidence grade its
recommendation outputs may rest on, named in the domain's own grade vocabulary.
A family MAY additionally declare one or more RELAXED MODES, each naming the
floor it drops to and the reason it exists. A relaxed-mode output carries its
mode and its actual grade on the object itself, and the family declares that
relaxed and floor-conforming outputs are not merged into one ordering — the
non-mixability is structural, expressed in the object, not a rendering
convention a consumer may ignore.

A family whose ranking uses inputs that do not come from its declared truth
store declares them in an `editorial_weights` block naming a versioned,
human-reviewed policy artifact and the authority that reviews it. Every
recommendation output produced under such a family cites the weights version it
used and surfaces the weights that moved the ordering. This closes the gap the
promoted "full provenance" requirement leaves: a judgement number is neither
evidence nor an assumption about the subject, and calling it either would be a
lie the validator cannot catch.
<!-- /xspec:candidate -->

### The MedxFactory half — corpus, tables, engine

Clinical corpus and engine content moved 2026-09-07 to MedxSoft/MedxFactory
`ideation/staging/treatment-plan-generation/treatment-options-engine-clinical.md`
(see that repo). It was never fenced as candidate prose here: those
capabilities are Medx-owned and an openxFactory fragment cannot host their
delta text.

## Impact

<!-- xspec:candidate target=governed-derived-model -->
- Affected specs: `governed-derived-model` (MODIFIED — a third member role, an
  evidence-floor dial with declared relaxed modes, an editorial-weights
  declaration). MedxFactory realizes against `root-truth-grounding`,
  `terminology-normalization` and `treatment-plan-generation`; AdxFactory's
  `calibrated`-tier conformance and codexFactory's overlay both re-read the
  family, though an additive member role costs an existing conformant family
  nothing.
- Affected code: `openxFactory/scripts/validate-derived-models.py` grows the
  role and dial checks. The MedxFactory-side code impact moved with the
  clinical half.
- **The already-promoted refusal surfaces are load-bearing and unchanged.**
  `omnigent-domain-overlay`'s constitutional `execute_final_action: false` and
  `access_secrets: false` are what make a recommendation member safe to
  produce at all, and `workflow-gate-contract` is where the human decision
  lives. This topic ADDS a proposal object; it must not acquire an act.
- **A recommendation object is the first derived object a human reads and acts
  on directly.** A synthetic, internal family is one thing; a family whose
  ranked output a named human acts on is another. Everything in the promoted
  family that was theoretical protection becomes operative protection.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

Idea notes 1–6 are clinical and moved with the MedxFactory half.

- The neutral `role: recommendation` and the Medx engine could be sequenced
  either way, but doing the neutral one first is cheaper: the Medx family's
  conformance declaration then validates on the day it is written rather than
  being retrofitted against a role that changed shape underneath it. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

## Conflicts

- **Editorial weights versus a truth store's own no-invented-facts doctrine.**
  Where every record in a truth store cites a source, the family's whole point
  is that nothing enters without provenance. A weights table is a body of
  assertions with NO source record — it is judgement, and it will change the
  ordering of the options. The neutral `editorial_weights` declaration is
  the proposed reconciliation, but it is a reconciliation, not an absence of
  tension: the topic is introducing un-sourced numbers into a system built to
  refuse them. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- Conflicts 1 and 3–6 are clinical and moved with the MedxFactory half.

## Open questions

All ten open questions (Q1–Q10) are clinical and moved with the MedxFactory
half. Three of them gate this neutral change and are named in `Exit` below:
Q7, Q8 and Q9.

## Related work

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

- **`governed-derived-model` (promoted, openxFactory; DTN-014 `implemented`)** —
  the floor this topic modifies. MedxFactory conforms at tier `governed`,
  AdxFactory at `calibrated`.
- **`omnigent-domain-overlay` (promoted, openxFactory)** — constitutional
  `execute_final_action: false` / `access_secrets: false`, which is what makes
  claim 2 enforced rather than merely stated.
- **`workflow-gate-contract` (promoted, openxFactory)** — where the human
  decision is recorded; a recommendation output arrives at this gate, never
  past it.
- The five MedxFactory entries (`treatment-plan-generation`,
  `root-truth-grounding` / `root-truth-leaf-corpus`, `terminology-normalization`,
  `one-patient-integration-contracts`, `patient-consent-instrument`) moved with
  the clinical half.

## Exit

Two changes, sequenced, neutral first.

The NEUTRAL change modifies `governed-derived-model` with the recommendation
member role, the evidence-floor dial and its declared relaxed modes, and the
editorial-weights declaration, plus the validator support for all three. It can
be raised as soon as Q7, Q8 and Q9 carry dispositions — those three determine
whether the Medx family can be declared against the role at all, and a neutral
role designed without knowing that is a role that will need amending.

The MEDX change (or changes), and the disposition gate the open questions
carry, moved with the clinical half.
