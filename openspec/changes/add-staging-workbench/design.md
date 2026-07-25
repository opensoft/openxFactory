# Design: Staging Workbench (read-only foundation)

## Context

Brett's Track B ruling (2026-07-25, live against the running wheel):
**the staging area is where the real proposal gets developed**, and the
workbench is its read-only foundation. Track C — the AI chat layer that
makes the workbench generative — is a LATER change, and this one must not
be designed as if it already exists.

Brett's second ruling (2026-07-25, after PR #41 landed): **a gate must
hold the staging→proposal move until the topic's open questions are
closed and enough is done, and the staged topic's health must be clearly
indicated — a small health icon at the first click level, expanded at the
second.** This overrules the first draft's "completeness never gates"
bound and narrows D3: staged topics DO get an aggregate, because the
staged→proposal transition now needs a machine-checkable doneness bar
(D8–D10 below).

Three facts about the existing surfaces set the shape:

1. **The snapshot is the only data path.** The promoted capability's
   "Snapshot projection contract" is explicit: a view acquires data by
   delta declaring new snapshot fields and the generator populating them,
   and the renderer MUST NOT scan the repository. A completeness bar is
   therefore derived-model growth first and a view second.
2. **The wheel already has an extension point.** The expanded tile mounts
   its action row from ONE pure table (`WHEEL_ACTIONS[wheelKey]` with a
   `visible(item, env)` predicate) plus ONE mounter per verb; the
   read-only verbs (`read`, `lens`, `canvas`, `landed`) already ride it
   with no capability gate. The workbench action is one more row of the
   same kind — `add-wheel-action-verbs` design owns that extension point's
   description, so this change references it and re-specifies nothing.
3. **Document CONTENT already has a governed read path.** The viewer reads
   from the pinned checkout through the read-only `/source` pass-through,
   and the wheel's `landed` verb parses spec-delta text through the same
   route with an inline degraded message where the route is absent. The
   `outline` panel is the third consumer of that established path, not a
   new one.

## Goals / Non-Goals

**Goals**: make per-document maturity visible at a glance, deterministically
and testably; put one topic's documents, connections, and outline on one
scoped surface; grow the snapshot additively so no existing artifact is
invalidated; keep the whole surface read-only so Track C inherits a clean,
already-proven foundation.

**Non-Goals**: the AI chat layer (Track C) and every write it implies —
outline editing, fragment authoring, in-place document composition, any
workbench write path at all; tunable weights or thresholds (v1 constants);
aggregate completeness for clusters and possibles (the staged-topic health
aggregate of D8 is the ONE ruled exception); any re-scoring or
reinterpretation of the three-tier readiness panel; gating any verb other
than propose; new snapshot fields for the lens panel.

## Decisions

### D1 — v1 completeness is deterministic, with no LLM judgment
**Decision**: the score and all five signals are computed at snapshot
generation time from the pinned tree alone — no model call, no network, no
wall clock, no human input.

**Rationale**: two hard constraints and one precedent.

- *Testability.* A score that varies run to run cannot be unit-tested, and
  a rising-score scenario ("this document got more complete") cannot be
  asserted at all. Determinism makes the whole family fixture-testable.
- *Snapshot-time computability.* The snapshot MUST be byte-identical for an
  unchanged tree (the promoted spec's first scenario). A model-derived score
  in a document entry would break byte-identity outright, and stashing it
  outside the snapshot would violate the renderer's no-scan rule. So the
  signal must be a pure function of the tree or it cannot live in the
  snapshot at all.
- *Precedent.* The doc-health capability already draws exactly this line:
  "Every check in this pass MUST be deterministic — identical inputs produce
  identical findings, with no model calls; semantic analysis belongs to the
  agentic semantic sweep". Completeness sits on the deterministic side of
  that same line, and the judgment-shaped question ("is this topic ready?")
  already has an owner in the three-tier readiness panel.

**Consequence**: the five signals are deliberately structural proxies, not
an assessment of quality. A well-structured empty argument scores well; that
is honest about what the signal measures, and the human reading the bar is
the one who knows the difference. A semantic completeness assessment, if it
is ever wanted, belongs to a worker lane under its own contract — never
inside the deterministic generator.

### D2 — Weights are contract constants in v1
**Decision**: the score is a fixed-weight combination of the five
normalized signals at a fixed decimal precision, with the weights pinned as
contract constants.

**Rationale**: a per-run weight input would destroy reproducibility (the
same tree could yield different snapshots), and a committed weight config
would make every snapshot's scores a function of two inputs rather than
one — a much harder thing to reason about the first time the numbers look
wrong. Pinning them makes v1's scores comparable across every snapshot ever
generated. Fixed decimal precision is not cosmetic: it is what keeps the
rendered JSON byte-identical across platforms.

A tunable configuration is a plausible successor (Brett hinted the settings
panel could host weights) — see open question 1. Whatever shape it takes,
it must keep determinism: the weights would have to be part of the pinned
input, recorded in the snapshot beside the scores.

### D3 — Completeness is per DOCUMENT; the one aggregate is staged-topic health
**Decision**: only `documents[]` entries gain a `completeness` object.
Clusters and possibles get no aggregate score. Staged topics get exactly
one aggregate — the `health` object of D8 — and nothing else does.

**Rationale**: an aggregate would immediately be read as readiness, which
is a governed judgment with three named authorities and a recommendation
gate at min >= 8. Averaging deterministic document structure into a
tile-level number would create a second, unauthorized readiness signal that
looks authoritative and is not. That reasoning still bounds clusters and
possibles — cluster judgment already has an owner in the readiness panel.
Staged topics are the ruled exception: Brett's 2026-07-25 ruling makes the
staged→proposal transition conditional on structural doneness, and a gate
needs a defined, machine-checkable input. The aggregate is deliberately
named HEALTH, not readiness: it answers "is this topic's own material
structurally done" (open questions closed, documents past the threshold),
never "should this be proposed" — that judgment stays human, exercised by
clicking propose after the gate clears.

### D4 — The tab set is docs / lens / outline, and nothing else in v1
**Decision**: three panels.

- `docs` — the tile's document set with completeness bars. The set is
  derived strictly from snapshot edges, per tile kind (cluster edges;
  a possible's cited evidence, with claiming-cluster members shown
  separately-labelled as inherited; a staged topic's folder documents plus
  documents declaring it as a destination). The separation matters: cited
  evidence is a recorded pin, inherited membership is an inference from the
  cluster, and merging the two would silently upgrade an inference into
  evidence.
- `lens` — interconnectedness at tile scope, by RE-SCOPING the existing
  keyword-lens seed (`keyword_index`) and the existing edge/degree
  derivation. This is a filter over derivations the dashboard already
  computes, not a new analysis: no new snapshot field, no new score. The
  cluster wheel's existing `lens` verb jumps to the global lens with the
  cluster's topics checked; the workbench panel is that same derivation
  bounded to the tile so the human is not thrown out of their scope.
- `outline` — the topic's outline where one exists, read through `/source`
  read-only. For a staged topic that is the fragment's outline material
  (the feat-spec-shaped declaration of target capability, delta type,
  claims, open questions, exit path). Read-only in this change.

**Editing and chat arrive in Track C.** The `outline` panel is deliberately
a renderer, not an editor, and the workbench has no writing panel of any
kind. Track C is where the conversational layer lands — reading the scoped
tile, drafting with the human, and (under whatever gates that change
defines) proposing material back. Keeping the foundation read-only means
Track C is a purely additive change on a surface already proven live, and
it means this change carries no new write authority to review.

### D5 — Two senses of "workbench", deliberately kept apart
The promoted capability already has a "workbench": *workbench reference
sets* — user-assembled document SETS persisted as gitignored
`kind: ideation-workbench` manifests under `ideation/workbench/`, with
bounded actions (scratch notebook, readiness scoring, scoped doc-health,
draft-organize).

The staging workbench is a different thing: a scoped read-only VIEW over
one already-existing topic-bearing tile. It assembles no set, persists no
manifest, and writes nothing, so there is no contract collision — the
`ideation-workbench` schema is untouched by this change. Brett's label
("open workbench") is kept as the tile action's user-facing name because it
is what he calls it; the contract uses the full name *staging workbench*
wherever ambiguity is possible.

A later change could plausibly let the staging workbench SEED a reference
set (its `docs` panel is already a document set at a scope). That is a
write, so it is out of scope here by construction.

### D6 — The tile action carries no gate capability
**Decision**: `open workbench` is a read-only navigation verb with no
`visible` capability predicate — offered whether or not the loopback gate
is live, and therefore present on the deployed static image.

**Rationale**: the wheel already established this class (`read`, `lens`,
`canvas`, `landed` carry no gate because none of them writes). Gating a
read verb on a write capability would hide the workbench from every viewer
of the hosted dashboard, which is precisely the audience that most needs a
read-only surface. The panels degrade honestly where the `/source` route is
absent, exactly as the viewer and the `landed` flyout already do.

### D7 — Growth is additive, and the pre-growth snapshot must still render
The `completeness` object is optional. The nightly snapshot is regenerated,
so the field appears everywhere within one lane run — but a hosted image
serving yesterday's snapshot must not break. The `docs` panel therefore
treats missing completeness as "no bars", never as zero (a zero bar would
libel a finished document as a stub).

### D8 — Health is folder-scoped, blockers-first, tri-state
**Decision**: a staged topic's health derives exclusively from its FOLDER's
own corpus documents — `standing_open_items` (summed `open_markers` raw
counts), `doc_score_min` / `doc_score_mean`, a typed `blockers` list, and a
`status` derived from the blockers: `ready` (none), `stub` (no corpus
documents), `developing` (otherwise). The ready threshold
(`READY_MIN_SCORE`) is a v1 contract constant pinned beside the weights.

**Rationale**: documents that merely DECLARE the topic as a destination are
inbound context — their doneness is their own topic's business, and letting
an unfinished upstream note hold a finished fragment hostage would make the
gate capricious. Blockers-first keeps the aggregate honest: the status is a
summary of named, countable reasons, so a red icon is always explainable in
one hover and one refusal message. The three states match the tile's three
honest conditions — nothing there yet, being worked, worked to done — and
deriving status from blockers (rather than scoring status directly) means
the gate and the icon can never disagree about WHY.

### D9 — The gate evaluates live, through the same scoring module
**Decision**: the propose route recomputes the topic's health from the
pinned checkout at request time, importing the SAME Python scoring module
the generator uses; the snapshot's `health` object is display truth only.

**Rationale**: the snapshot is regenerated nightly, so it can trail the
checkout by a working day — and a gate that refuses (or worse, allows) on
yesterday's tree teaches people to distrust it. The generator and serve.py
are both Python, so one module serves both callers with zero duplication —
the same fixture-tested functions produce the icon and the refusal. The
guard sits in the route itself, the single choke point every surface
(tile action, CLI, direct request) already passes through, mirroring how
the missing-topic and duplicate refusals are enforced today.

### D10 — Health shows at the interaction levels Brett named
**Decision**: resting drum faces stay unadorned; the FOCUSED (first-click,
centred) staged tile face carries a compact tri-state indicator; the
EXPANDED (second-click) tile renders the full health block — status,
standing open items per document, score min/mean, blockers — verbatim from
the snapshot.

**Rationale**: this is Brett's stated shape ("small health icon in the
first click level and expanded in the second"), and it matches the wheel's
established progressive-disclosure model: focus answers "which topic",
expand answers "what would I do here". Rendering verbatim from the
snapshot keeps the renderer no-scan and makes any drift from the live gate
a visible, explainable staleness (D9's refusal message is authoritative),
never a silent client-side recomputation.

## Risks / Trade-offs

- **A structural proxy will be read as a quality verdict.** A polished stub
  can outscore a dense, unformatted, nearly-complete brainstorm. Mitigation:
  the signals are shown individually with their raw counts and the score is
  labelled as structural. Since the readiness gate now refuses on it (D8),
  a misleading score CAN cost a refused propose — but the refusal names the
  exact document and number, so the cost is closing a named gap or fixing a
  named miscount, never arguing with an opaque verdict.
- **The gate will be felt as friction.** The first refused propose on a
  topic Brett considers ready is the moment this design is judged.
  Mitigation: blockers are specific and actionable (this document, these
  standing markers, this score against this constant) — closing them IS the
  work the gate exists to force; and the threshold is calibrated with Brett
  on the real corpus at realization (task 6.5) before the gate ever refuses
  him.
- **Completeness could be mistaken for readiness.** Two scores in one
  dashboard invites conflation. Mitigation: D3 (no tile-level aggregate) and
  the explicit non-gating rule; the readiness panel keeps its own rendering
  and its own min >= 8 recommendation semantics.
- **Weight tuning pressure will arrive quickly.** The first time a
  document Brett considers finished shows a mid bar, the weights become the
  conversation. Mitigation: fixed constants make that conversation concrete
  (which signal is wrong, and by how much) rather than diffuse, and open
  question 1 already names the successor shape.
- **Generator cost.** Scoring reads every document's body, which the
  generator already loads for header parsing and topic extraction, so the
  added cost is per-document regex and counting work — but the marker and
  section scans are the first full-body passes in the generator. Mitigation:
  single-pass counting over already-loaded text; the nightly lane's runtime
  is watched at realization (task 5.1).
- **Track C temptation.** A read-only workbench with an outline panel will
  invite "just let me fix this line here". Mitigation: the read-only rule is
  a requirement with its own scenario, and the existing select-to-edit
  escape hatch already gives the human a legitimate editor path.

## Open Questions

1. **Weight tunability, and where it would live.** Brett hinted the
   settings panel (which already hosts the live wheel-diameter slider)
   could host completeness weights later. If it does, the tuning must not
   break determinism: candidate shapes are (a) view-only re-weighting in
   the renderer with the snapshot's constant-weight score untouched, or
   (b) a committed weight profile that the generator pins INTO the snapshot
   beside the scores, making the weights part of the reproducible input.
   Deferred to a successor change; v1 ships constants.
2. **Whether the `lens` panel's scope should be widenable in place** — one
   hop out from the tile's keywords to their co-occurring keywords, without
   leaving the workbench. The re-scoping derivation already supports it;
   the question is whether widening inside a scoped view confuses the scope
   or is exactly what a human working a topic wants.
3. **Whether the `docs` panel should offer the completeness signals as a
   sort/filter** (worst-first is the obvious working order) or stay in the
   snapshot's stable path order. Sorting is a pure renderer concern, so it
   can land either here at realization or later without contract impact.
4. **The `READY_MIN_SCORE` value.** A contract constant like the weights,
   so it needs a number before the gate can refuse. Recommendation: start
   at 0.60 and calibrate on the real corpus with Brett at realization
   (task 6.5) — the fragments he has actually taken to proposal (e.g.
   github-administration-plane, "all six open questions are resolved —
   ready to propose") are the ground truth for where ready sits.
5. **Whether the gate needs a human override.** V1 recommendation: NO —
   the honest response to a blocker is to close it (resolve the question,
   finish the document), and an override that skips that is the gate not
   existing. If a legitimate emergency shape emerges, the override must be
   a recorded gate action carrying a reason, never a silent bypass —
   a successor change.
