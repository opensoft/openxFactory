# Staged: a treatment-options engine — indicated, minus contraindicated, minus interacting, weighted by adverse reactions

Status: staged
Kind: capability-proposal
Summary: For one patient and one charted condition, produce a shortlist of drug
options by running a cited filter chain over the Medx root-truth corpus: start
from everything INDICATED for the condition, subtract what is CONTRAINDICATED
for this patient, subtract or flag what INTERACTS with the patient's current
medications, and weigh what remains by ADVERSE REACTION profile. A REBALANCE
mode searches for a whole combination rather than one drug — fewer negative
interactions, more positive ones, a better reaction profile — and reruns when a
charted observation says the patient is not responding. An OFF-LABEL mode runs
the same chain with the evidence floor lowered and mechanism-of-action
similarity admitted as a candidate generator. Every line of every output cites a
record; the engine proposes and a clinician decides.
Topics: treatment-options, root-truth-corpus, governed-derived-model,
med-rt, rxclass, drug-interactions, adverse-reactions, mechanism-of-action,
off-label, evidence-grade, terminology-normalization, treatment-plan-generation
Repository context: SPLIT, deliberately. openxFactory owns the neutral half —
`governed-derived-model` (the derived-recommendation member role, the
evidence-floor dial, and the editorial-weights declaration), with
`omnigent-domain-overlay` and `workflow-gate-contract` supplying the
already-promoted refusal and gate surfaces this topic must not re-invent.
MedxFactory owns the realized half — the corpus backfill under
`root-truth-grounding`, the new mapping tables under
`terminology-normalization`, and the engine itself under
`treatment-plan-generation`. This fragment is staged in openxFactory because
the neutral delta is the one that needs designing; the Medx work is
comparatively mechanical once it lands.
Staging ID: openxFactory:staging:treatment-options-engine
Captured: 2026-08-26
Source: Brett Heap, in session 2026-08-26, deciding to build rather than
explore — "we will build this". The capability was described in six steps:
(1) list all drugs indicated for the condition, (2) remove those
contraindicated for this patient, (3) check interactions against the patient's
current medications, (4) weigh adverse reactions, (5) rebalance — search for a
combination with fewer negative and more positive interactions and a better
reaction profile, trial the patient on it for some weeks, and rerun if the
chart says they are not responding, (6) off-label mode — the same engine with
the evidence-grade gate lowered and mechanism-of-action similarity admitted as
a candidate generator.
Target capabilities: MODIFIED `governed-derived-model` (a derived-RECOMMENDATION
member role whose outputs are ranked, cited, and non-authoritative; a declared
evidence FLOOR per family with a labelled, non-mixable relaxation mode; and a
declaration for ranking weights that come from editorial judgement rather than
from the family's truth store). The MedxFactory-side targets —
`root-truth-grounding`, `terminology-normalization`, `treatment-plan-generation`
— are named throughout but NOT fenced as `xspec:candidate` targets, because
they are Medx-owned capabilities that do not resolve from an openxFactory
document and fencing them would emit tag-hygiene findings for a claim this repo
cannot host.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

Settled by Brett's 2026-08-26 decision, or by facts verified against the live
corpus the same day (see the next section for the verification). The open
questions below do NOT reopen these.

1. **We are building it.** This is a build decision, not an exploration. The
   six steps above are the capability description, not a menu.
2. **The engine PROPOSES; a clinician DECIDES.** The output is a ranked list of
   options with cited reasons. Nothing about it selects, orders, prescribes, or
   cycles a regimen. The Omnigent constitutional `execute_final_action: false`
   and `access_secrets: false` hold unchanged, and the treatment-plan gate stays
   human-reviewed. This is the governance boundary of the whole topic and it is
   not a dial.
3. **The rebalance trigger is a chart OBSERVATION, never a timer and never an
   automatic rerun.** "The patient is not responding" is a charted clinical
   fact that a human enters; the engine reruns because that fact appeared, not
   because weeks elapsed. A rebalance that fires on its own would be the system
   cycling regimens, which claim 2 forbids.
4. **Every line of every output cites a root-truth record.** The filter chain is
   an argument, and each step of the argument names the accepted record that
   licenses it. A step with nothing to cite does not run silently — it is
   surfaced as a gap.
5. **On-label first; off-label is a separate MODE, not a widened default.**
   Off-label results carry their evidence grade prominently and are structurally
   un-mixable with on-label results. One list containing both, sorted together,
   is the failure this claim exists to prevent.
6. **The interaction-severity weights are EDITORIAL POLICY, governed
   separately.** Labels state interactions but do not grade them on any common
   scale, and almost never state positive ones. Severity numbers and combination
   weights are therefore our judgement, versioned, human-reviewed, and VISIBLE
   in every output that used them — never buried in a scoring function.
7. **The backfill fetches nothing new.** Adverse-reaction (SPL §6) and
   mechanism-of-action (SPL §12.1) extraction runs over the custody XMLs already
   pinned by digest under `var/root-truth-sources/`. Same recipe, same sources,
   same review gate — new sections of documents we already hold.

## Current state, verified against the live corpus (2026-08-26)

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

Measured in `/home/brett/projects/MedxFactory-worktrees/corpus-main` on
2026-08-26. Several of these correct the shape the capability was described
with, and the corrections change what the deltas have to be.

- **6,506 records over 1,302 distinct `medication_*` concepts**, with 1,298
  custody SPL XMLs (261 MB) under `var/root-truth-sources/`. Against the
  prescribable RxNorm ingredient set (5,803 `medication_*` rows), the corpus
  covers about 22% of ingredients.
- **The claim-type enum is CLOSED AT TEN**, in
  `scripts/root_truth/validate_root_truth.py:24-25`: `indication`, `dosing`,
  `contraindication`, `interaction`, `monitoring`, `target`,
  `biomarker_association`, `efficacy`, `adverse_effect`,
  `diagnostic_criterion`. **`adverse_effect` ALREADY EXISTS** (3 records), so
  the adverse-reaction work is a BACKFILL under an existing member, not a new
  claim type. `mechanism_of_action` does NOT exist; the nearest member is
  `target` (1 record), and whether MoA is `target` or an eleventh member is
  Q7 below — an eleventh member breaks a deliberately closed enum.
- **Claim-type distribution is five fat types and five thin ones**: monitoring
  1,301 / indication 1,300 / interaction 1,299 / dosing 1,299 /
  contraindication 1,298, then adverse_effect 3, efficacy 2,
  biomarker_association 2, target 1, diagnostic_criterion 1. One record per
  claim type per drug family, essentially.
- **The drug-to-condition edge does not exist.** Of 6,510 grounded pairs,
  6,505 are `medication_*` and exactly FIVE are `condition_*` (0.08%).
  Indications are one prose blob per family — `RT-SIMVASTATIN-IND-0001` carries
  six distinct indication limbs in a single `claim` string. "List all drugs
  indicated for condition X" is therefore **not answerable from the corpus at
  all** today; it is not slow or partial, it is absent. This is gap 1 and it is
  the load-bearing one.
- **The condition namespace already has TWO id conventions**, and they
  collide. The generated ICD-10 table (`icd10cm-fy2026.json`, 98,184 rows)
  emits `condition_a00_0`-style ids keyed off the code; the curated
  `examples/terminology/tables/conditions.yaml` emits readable slugs like
  `condition_essential_hypertension`; and the generated manifest states that
  curated keys are SKIPPED at generation time, so curated wins. The five
  condition pairs in the corpus contain both conventions
  (`condition_c74_0` and `condition_essential_hypertension`). A structured
  `indicated_for: [condition_*]` field must decide which convention it writes
  before it writes a single row (Q4).
- **The evidence-grade vocabulary is already multi-valued**, contrary to the
  "everything is `regulatory_label`" shorthand: 6,499 `regulatory_label`,
  3 `retrospective_cohort_study`, 2 `clinical_practice_guideline`,
  2 `public_health_guidance`. The off-label mode's floor-lowering therefore
  has grades to lower TO — the vocabulary exists, it is just barely populated.
- **There is no drug-class field anywhere** in the record schema, the templates,
  or the terminology tables.
- **`medx.domain.policy.plan_authoring_models` is at version `1`**, pinning
  `claude-fable-5` for `generation`, `critique`, and — additively, per
  `add-root-truth-interim-corpus` — `claim_extraction`. Its own position
  `policy-revision-is-governed` says the admissible set changes "only through an
  OpenSpec change; no runtime, session, or operator override widens the pins".
  So re-pinning extraction to a cheaper tier for the backfill is a **policy
  version bump through OpenSpec**, not a runtime switch. Recommended anyway on
  cost — see the build order.
- **`treatment-plan-generation` is already promoted in MedxFactory** with nine
  requirements, including "Charted diagnoses are the only plan entry points",
  "Every clinical claim cites patient evidence from the pinned run", "Every
  rationale statement declares its knowledge basis", "Generation runs as a
  governed job on the closed worker plane", "Consent is checked at job start
  with a distinct purpose", and "Admissible authoring models are pinned by
  policy". **The engine is not greenfield** — most of its governance envelope
  already exists (Q8).
- **MedxFactory's `governed-derived-model` conformance declares exactly ONE
  family**, `dream_simulation`, at tier `governed`, with dials
  `identity: synthetic`, `scope: domain`, `truth_store: patient_truth_model`,
  `promoting_authority: clinician_of_record`, `person_modeling:
  synthetic_only`. A treatment-options family is a SECOND family whose dials
  differ on the two that matter most: it is `scope: subject` and it models a
  real, identified patient (Q9).

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

Not fenced as candidate prose: these capabilities are Medx-owned and an
openxFactory fragment cannot host their delta text.

**Structured indication and contraindication concepts.** Records grow derived,
reviewable `indicated_for: [condition_*]` and `contraindicated_in:` fields
alongside the prose `claim` they are derived FROM — the prose stays
authoritative and the structure stays a derivation of it. Two generators, in
this order: NLM MED-RT relationships served through the RxClass API
(`may_treat`, `may_prevent`, `CI_with`, `has_MoA`, `has_PE`), which is
deterministic and involves no model at all; then a model pass mapping residual
label prose onto condition concepts only where MED-RT is thin. Both land at
`review_status: proposed` and become citable only through the existing human
review gate.

**Adverse-reaction backfill under the EXISTING `adverse_effect` claim type**,
extracted from SPL §6 over the already-pinned custody XMLs. No enum change, no
new fetching, no new license question — the recipe that produced 6,499 records
run over a section we already hold.

**Mechanism-of-action claims** from SPL §12.1, plus the structured MED-RT
`has_MoA` / `has_PE` edges. This is the layer that makes off-label mode
possible: without a mechanism, "similar drug" has no meaning that cites
anything. Whether these are `claim_type: target` or an eleventh enum member is
Q7 and must be answered before extraction starts, because it determines every
record id.

**A drug-class terminology table** — FDA Established Pharmacologic Class from
the SPL itself, and WHO ATC through RxClass — generated the way the ICD-10 and
RxNorm tables are generated, with a pin-registry entry, a source digest, and a
license commit rule (Q10).

**The treatment-options derived model**: the filter chain, realized as a
governed derived family whose output is a recommendation member, running on the
closed worker plane under the consent and gate obligations
`treatment-plan-generation` already promotes. On-label only in its first form.

**The interaction-severity table**, and only then rebalance. Rebalance is a
search over combinations, and a search needs a scoring function; a scoring
function needs the severity scale; and the severity scale is the editorial
policy artifact the neutral half just gave a home to. Building rebalance before
the table would mean hard-coding judgement into a search.

**Off-label mode** last, behind the declared floor relaxation, with
mechanism-of-action similarity as the candidate generator and the grade on
every result.

## Build order

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

The order is Brett's, with one governance note attached to step 1.

1. **Backfill §6 and §12.1 over existing sources.** Same recipe, same custody
   digests, same review gate. NOTE: the extractor model is pinned by
   `medx.domain.policy.plan_authoring_models` v1 at `claude-fable-5`, and that
   policy's own position says the admissible set moves only through an OpenSpec
   change. Re-pinning EXTRACTION to a lower tier is therefore a policy VERSION
   BUMP, not a configuration change — recommended on cost, since the backfill is
   ~2,600 extractions of structured label sections, but it must go through the
   change flow and the version bump must be visible in every record it produces.
2. **The MED-RT class / indication / MoA table**, scripted, deterministic, no
   model in the loop.
3. **The derived treatment-options model, on-label only.**
4. **The interaction-severity table, then rebalance.**
5. **Off-label mode.**

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
  role and dial checks; `MedxFactory/models/derived-model-conformance.yaml`
  gains a second family; `MedxFactory/scripts/root_truth/` and
  `scripts/terminology/` grow the backfill and the new tables.
- **The already-promoted refusal surfaces are load-bearing and unchanged.**
  `omnigent-domain-overlay`'s constitutional `execute_final_action: false` and
  `access_secrets: false` are what make a recommendation member safe to
  produce at all, and `workflow-gate-contract` is where the human decision
  lives. This topic ADDS a proposal object; it must not acquire an act.
- **A recommendation object is the first derived object a clinician reads and
  acts on directly.** The dream/simulation family is synthetic and internal;
  this one is about a real patient, in front of a prescriber. Everything in the
  promoted family that was theoretical protection becomes operative protection.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

- The filter chain reads like set arithmetic — indicated MINUS contraindicated
  MINUS interacting, weighted — but the interesting engineering is in the
  MINUS. A drug excluded for this patient is more clinically informative than a
  drug that was never a candidate, and a chain that silently drops exclusions
  throws away the reasoning a clinician most wants to see. The output probably
  wants an EXCLUDED list with reasons beside the shortlist, not just the
  shortlist. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- Rebalance is a combinatorial search and the search space is not small: even a
  five-drug regimen drawn from a 40-candidate pool is ~658k combinations before
  any pruning. The corpus is the pruner — most pairs have no interaction record
  at all, and absence of a record is not absence of an interaction. How the
  search treats UNKNOWN pairs is probably the hardest unasked question in this
  topic; treating unknown as safe is optimistic, treating it as unsafe prunes
  almost everything. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- Mechanism-of-action similarity as a candidate generator has a well-known
  failure mode: same mechanism, wildly different clinical behaviour. It is a
  GENERATOR, not evidence, and the off-label output should say so in exactly
  those words — "this was suggested because it shares a mechanism" is an honest
  sentence and "this is indicated" is not. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-08-26
- The 22% ingredient coverage number cuts both ways. It is enough to build and
  demonstrate the engine on common conditions, and nowhere near enough for the
  engine's silence about a drug to mean anything. Any output has to distinguish
  "not recommended" from "not in the corpus", and the coverage registry
  (`examples/root-truth/coverage-registry.json`) already exists to answer the
  second. — Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- SPL §6 adverse-reaction sections often carry INCIDENCE TABLES — percentages by
  arm — which is a genuinely different kind of content from the prose claims the
  corpus holds today. Extracting a table into a prose `claim` string would
  destroy the only thing that makes it weightable. Either §6 extraction produces
  structured incidence rows or adverse-reaction weighting stays qualitative
  (Q5). — Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- "Positive interaction" is doing a lot of work in the goal statement and may
  name two different things: pharmacokinetic boosting (ritonavir, carbidopa —
  which labels DO state, because it is why the combination product exists) and
  clinical synergy across a regimen (which labels essentially never state). The
  first is already in the corpus under `interaction`; the second is not, and
  probably cannot be at `regulatory_label` grade. — Added-by: Claude Opus 5
  (session, Brett's direction) · 2026-08-26
- The neutral `role: recommendation` and the Medx engine could be sequenced
  either way, but doing the neutral one first is cheaper: the Medx family's
  conformance declaration then validates on the day it is written rather than
  being retrofitted against a role that changed shape underneath it. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

## Conflicts

- **The claim-type enum is deliberately CLOSED at ten, and the MoA work wants
  an eleventh.** `validate_root_truth.py` enforces closure and the template
  comment names the count. Adding `mechanism_of_action` is a contract act
  against a design decision that was made on purpose. Reusing `target` avoids
  the act but conflates a molecular target with a mechanism, which are not the
  same claim. Unresolved; Q7 recommends a direction without settling it. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- **Editorial weights versus the corpus's own no-invented-facts doctrine.**
  Every root-truth record cites a source digest, and the family's whole point is
  that nothing enters without provenance. A severity table is a body of
  assertions with NO source record — it is our judgement, and it will change the
  ordering of clinical options. The neutral `editorial_weights` declaration is
  the proposed reconciliation, but it is a reconciliation, not an absence of
  tension: the topic is introducing un-sourced numbers into a system built to
  refuse them. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- **`treatment-plan-generation` promotes "Charted diagnoses are the only plan
  entry points", and off-label mode's candidate generator is mechanism
  similarity.** These do not obviously contradict — off-label still STARTS from
  a charted diagnosis — but the generator reaches drugs that no charted
  diagnosis indicates, and the promoted requirement was written to stop exactly
  that kind of reach. Whether the requirement bounds the ENTRY POINT or the
  whole candidate set has to be read carefully before off-label mode is built. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- **MedxFactory's derived-model conformance declares `person_modeling:
  synthetic_only`.** Its single family is synthetic by construction. A
  treatment-options family for a real patient cannot be declared under that
  dial, and the promoted spec requires `identified_persons_under_policy` to
  reference an authorizing domain policy that does not yet exist. The
  declaration file is currently INCONSISTENT with what this topic will need. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- **Two condition-id conventions coexist in the terminology layer**, curated
  slugs and generated ICD-10 codes, with curated silently winning at generation
  time. Writing `indicated_for` against either one makes the other wrong, and
  the five condition pairs already in the corpus use both. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-08-26
- **"Rebalance reruns" reads like a loop, and claim 2 forbids a loop.** Brett's
  own step 5 settles the trigger as a chart observation, so the conflict is with
  the phrasing rather than the design — but the phrasing is what an implementer
  will read, and a scheduler that polls the chart for non-response would satisfy
  the words while violating the claim. Recorded so the eventual proposal states
  the trigger as an event a human authored. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-08-26

## Open questions

### Q1. Which reference grades drug interactions, and can we cite it?

Context: SPL labels state interactions but do not grade them on any common
scale — 1,299 `interaction` records exist and none carries a severity. The
well-known graded references (Lexicomp, Micromedex, Stockley's) are commercial
and licensed; DrugBank's interaction set has a licence that varies by use;
ONCHigh and the CredibleMeds QT list are narrow but freely usable and
authoritative within their scope.
Recommended answer: do not adopt a commercial scale. Define our OWN small
ordinal scale (contraindicated / major / moderate / minor / unknown) as the
editorial policy artifact, seed it from the freely usable narrow lists where
they apply, and record for every graded pair which source or judgement set the
grade, so a later licence acquisition can replace judgement with citation
pair-by-pair rather than wholesale.
Explanation: the licence question is the binding constraint, not the
pharmacology. A scale we define is one we can publish, version, review, and show
in the output — all things claim 6 requires — whereas a licensed scale we
cannot redistribute makes the "weights visible in every output" obligation
unsatisfiable. Starting from freely usable narrow lists means the highest-stakes
pairs (QT prolongation, contraindicated combinations) are cited rather than
judged from day one.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q2. How does patient state — conditions, current medications, labs, allergies — enter the engine?

Context: `one-patient-integration-contracts` is promoted in MedxFactory and
already owns exactly this: identity bindings as explicit contract objects,
intake and source-assertion contracts that preserve provenance, snapshot and
projection contracts that preserve source-aware meaning, a synthetic layered
deterministic golden patient, and portable acceptance-gate evidence shapes. Its
last requirement is "Contract conformance grants no clinical authority".
`treatment-plan-generation` separately requires that every clinical claim cite
patient evidence from a PINNED RUN.
Recommended answer: yes — patient state enters through the
`one-patient-integration-contracts` snapshot, pinned per run, with no second
path. The engine reads a snapshot and cites it; it never queries a live chart
mid-run.
Explanation: the pinned-run requirement already exists and exists for this
reason — a recommendation whose inputs moved underneath it cannot be reviewed,
because the reviewer cannot reconstruct what the engine saw. Reusing the
contract also inherits the golden patient as a fixture, which is what makes the
engine testable without touching a real record. The open part is narrower than
the question sounds: whether the snapshot's current SHAPE carries everything the
chain needs, in particular allergies and the active medication list with
enough fidelity to key interactions.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q3. Where does evidence for POSITIVE interactions come from?

Context: labels state negative interactions and essentially never state
synergy. The rebalance objective explicitly wants "more positive interactions",
so the objective function has a term with almost no corpus behind it. Guidelines
and literature do carry synergy claims, at
`clinical_practice_guideline` / `retrospective_cohort_study` grade — grades the
corpus already admits, with 5 records between them.
Recommended answer: split the term. Pharmacokinetic boosting IS in the labels
(it is why fixed-dose combinations exist) and can be extracted at
`regulatory_label` grade from the existing `interaction` records. Clinical
synergy is a guideline-grade claim, and rebalance should treat it as a
SEPARATE, lower-graded, separately displayed contribution rather than folding it
into one score with label-grade evidence.
Explanation: collapsing two evidence grades into one number is the same defect
claim 5 forbids for on-label versus off-label, one level down. A clinician
reading "this combination scores well on positive interactions" needs to know
whether that rests on a label statement or a cohort study, and a single blended
score destroys the distinction irrecoverably.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q4. ICD-10 or SNOMED CT for the condition concepts `indicated_for` points at?

Context: the generated ICD-10-CM table exists (98,184 rows, FY2026,
`condition_<code>` ids); no SNOMED table exists; SNOMED CT requires an
affiliate licence in most jurisdictions and `terminology-normalization` promotes
that "License commit rules are enforced structurally". Separately, the curated
`conditions.yaml` uses readable slugs and takes precedence over generated keys,
so the condition namespace already holds two conventions.
Recommended answer: ICD-10-CM now, through the generated table's
`condition_<code>` convention, and retire the curated readable slugs into
aliases rather than letting both conventions write. Design `indicated_for` to
carry the code SYSTEM alongside the concept so a later SNOMED table is an
additive mapping rather than a migration.
Explanation: the licence rule makes SNOMED a gated decision and ICD-10 an
available one, and MED-RT's own indication edges resolve to ICD-10 and MeSH
more readily than to SNOMED. The real cost of choosing is not the vocabulary
but the id convention: two conventions in one namespace will produce silent
misses in the filter chain, where a miss looks exactly like "no drug is
indicated for this".
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q5. Does adverse-reaction weighting need incidence data, or is qualitative enough?

Context: SPL §6 carries both prose and incidence TABLES (percentages by arm).
The corpus's record shape is one prose `claim` string per record, which cannot
hold a table without destroying it. Weighing "weigh adverse reactions" against
one another without incidence means weighing severity only.
Recommended answer: extract incidence where §6 presents it as a table, as
structured rows on the `adverse_effect` record, and let the weighting use
incidence where present and severity-only where absent — with the output saying
which it used for each drug.
Explanation: severity without incidence ranks a 30%-incidence nuisance the same
as a 0.01% catastrophe, which is not a defensible ordering and is precisely the
kind of hidden judgement claim 6 exists to expose. The cost is a record-shape
change for one claim type; the alternative is a weighting nobody can justify to
a clinician. Note this makes the §6 backfill materially more expensive than the
§12.1 one, which affects the step-1 model-tier decision.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q6. What consent and liability gates does off-label mode need in Hermes?

Context: `treatment-plan-generation` already requires consent checked at job
start with a DISTINCT PURPOSE, and `patient-consent-instrument` is a promoted
Medx capability. Off-label prescribing is legal and routine in clinical
practice, but off-label RECOMMENDATION BY A SYSTEM is a different posture, and
the consent purpose "generate a treatment plan" does not obviously cover
"generate off-label hypotheses".
Recommended answer: off-label mode runs under its own consent purpose, distinct
from on-label generation, and its outputs carry a standing disclosure naming the
mode and the evidence floor. Do not attempt to encode liability — record the
mode, the floor, the generator, and the human who requested it, and let the
liability question be answered by the record rather than by the system.
Explanation: the distinct-purpose machinery already exists and is the cheapest
correct answer; inventing a liability model inside the engine would be the
engine making a legal judgement, which is a worse version of claim 2's failure.
The disclosure obligation is the part that must be structural, because a mode
label that a rendering layer can drop is not a disclosure.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q7. Is mechanism-of-action the existing `target` claim type, or an eleventh enum member?

Context: the claim-type enum is closed at ten by explicit design
(`validate_root_truth.py:24-25`, and the template comment names the count).
`target` exists with one record; `mechanism_of_action` does not exist. MED-RT
distinguishes `has_MoA` from `has_PE` (physiologic effect) and from the target
itself, so the source vocabulary makes three distinctions where our enum offers
one.
Recommended answer: add `mechanism_of_action` as an eleventh member, and leave
`target` alone. Do not overload `target`.
Explanation: a molecular target and a mechanism are different claims — "binds
EGFR" and "inhibits tyrosine kinase signalling downstream of EGFR" are not the
same sentence and do not license the same inference. Off-label similarity
reasoning runs on MECHANISM, so conflating the two would make the off-label
generator's evidence unciteable at the level it actually reasons at. The enum is
closed to stop drift, not to stop growth; growing it once, deliberately, through
a change, is what a closed enum is FOR. This must be settled before extraction
starts, because it determines every record id the backfill mints.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q8. Is the engine a new MedxFactory capability, or a MODIFIED `treatment-plan-generation`?

Context: `treatment-plan-generation` is already promoted with nine
requirements covering the entry point, the citation obligation, the knowledge-
basis declaration, the closed worker plane, consent, the model pin, and the
plan-G1 fixture-replay gate with zero EMR writes. The options engine needs all
nine, unchanged. What it adds is the filter chain, the ranking, the rebalance
mode, and the off-label mode.
Recommended answer: MODIFIED `treatment-plan-generation`, not a new capability
— with the ranked-options object declared as a conforming
`governed-derived-model` recommendation member.
Explanation: a new capability would either restate nine requirements or leave
them unstated, and both are worse than an additive delta. The options engine is
recognisably the same governed job producing a richer artifact, and the
plan-G1 gate is already the right demonstration shape for it. The counterargument
worth hearing is that rebalance and off-label are big enough to deserve their own
capability boundary; if so, they should be SEPARATE later capabilities rather
than a reason to fork the on-label engine out of the existing one.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q9. Which domain policy authorizes `person_modeling: identified_persons_under_policy` for the new family?

Context: `governed-derived-model` promotes that a family declaring
`identified_persons_under_policy` SHALL reference a domain policy that
authorizes it, and that validation FAILS if the referenced policy document does
not exist. MedxFactory's declaration today has one family at `synthetic_only`,
so no such policy has ever been needed. The nearest existing artifacts are
`patient-consent-instrument` and `medx.domain.policy.plan_authoring_models`,
neither of which is about person modeling.
Recommended answer: write a new Medx domain policy position for it — a
`patient_derived_modeling` category under `hermes/domain/policies/` — rather
than stretching the consent instrument to cover it. Declare the second family
as `scope: subject` with the isolation boundary named per-patient.
Explanation: the consent instrument governs what a patient permits; the person-
modeling dial governs what the FACTORY permits itself to derive about an
identified person. They answer different questions and a policy that conflates
them will be cited for the wrong one. This is small work but it is a hard
validation blocker — the family cannot be declared at all until the policy file
exists.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q10. Do the RxClass / MED-RT and ATC sources clear the terminology pin registry's licence commit rule?

Context: `terminology-normalization` promotes that a pin registry declares every
code system and its commit rule, and that "License commit rules are enforced
structurally" — the ICD-10 and RxNorm raw archives are gitignored INPUTS under
`var/terminology-releases/`, digest-pinned in the generated manifest, with only
the derived tables committed. MED-RT is NLM-produced and openly available;
RxClass is an NLM API; WHO ATC is copyrighted by the WHO Collaborating Centre
and its redistribution terms are NOT the same as RxNorm's, even though RxClass
serves ATC classes.
Recommended answer: MED-RT and the RxClass-served MED-RT relationships commit
as derived tables under the existing pattern. Treat ATC as a SEPARATE pin with
its own commit rule, and do not assume RxClass serving it makes it
redistributable; if the rule cannot be cleared, ship FDA EPC alone, which comes
from the SPL we already hold in custody.
Explanation: the promoted requirement makes this a structural gate rather than a
judgement call, so getting it wrong blocks a validate rather than producing a
finding. EPC-alone is a genuinely acceptable fallback — it is label-derived, it
is the class vocabulary the labels themselves use, and it needs no new source at
all.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

## Related work

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

- **`governed-derived-model` (promoted, openxFactory; DTN-014 `implemented`)** —
  the floor this topic modifies. MedxFactory conforms at tier `governed`,
  AdxFactory at `calibrated`.
- **`treatment-plan-generation` (promoted, MedxFactory)** — nine requirements
  the engine inherits rather than restates; Q8 asks whether it IS the home.
- **`root-truth-grounding` and `root-truth-leaf-corpus` (promoted,
  MedxFactory)** — the record contract, the acceptance gate, the coverage
  registry, and the custody-digest discipline the backfill runs under.
- **`terminology-normalization` (promoted, MedxFactory)** — the pin registry and
  licence commit rule that the drug-class and indication tables must satisfy.
- **`one-patient-integration-contracts` (promoted, MedxFactory)** — the pinned
  patient snapshot Q2 recommends as the single input path.
- **`patient-consent-instrument` (promoted, MedxFactory)** — the distinct-purpose
  consent machinery off-label mode reuses in Q6.
- **`omnigent-domain-overlay` (promoted, openxFactory)** — constitutional
  `execute_final_action: false` / `access_secrets: false`, which is what makes
  claim 2 enforced rather than merely stated.
- **`workflow-gate-contract` (promoted, openxFactory)** — where the clinician's
  decision is recorded; the engine's output arrives at this gate, never past it.

## Exit

Two changes, sequenced, neutral first.

The NEUTRAL change modifies `governed-derived-model` with the recommendation
member role, the evidence-floor dial and its declared relaxed modes, and the
editorial-weights declaration, plus the validator support for all three. It can
be raised as soon as Q7, Q8 and Q9 carry dispositions — those three determine
whether the Medx family can be declared against the role at all, and a neutral
role designed without knowing that is a role that will need amending.

The MEDX change (or changes) covers the corpus backfill, the new terminology
tables, and the engine. It cannot be raised until Q10 clears, because the licence
commit rule is a structural validation gate rather than a design preference, and
until the step-1 model-tier decision has either bumped
`medx.domain.policy.plan_authoring_models` or explicitly declined to.

Crossing the gate requires every open question above to carry a disposition
other than `open`, with Q1's severity-scale decision made BEFORE any rebalance
work begins rather than alongside it — a search built on a provisional scale
encodes the provisional judgement into the search.
