---
code_surface: codexFactory (snapshot generator per-document completeness scoring + staged-topic health aggregation, the propose route's readiness guard in serve.py, the staging-workbench view and its docs/lens/outline panels, the wheel's WHEEL_ACTIONS / ACTION_MOUNTERS workbench row, the staged tile's focused health indicator + expanded health block), openxFactory (additive `ideation-dashboard-snapshot` document `completeness` and staged-topic `health` growth)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-staging-workbench

## Why

The dashboard can now move a topic through every gate — dispose, propose,
promote-to-staging, derive-possibles, research-brief, demote, ratify,
kickoff — but it gives a human nowhere to WORK a topic. The staging area is
where the real proposal gets developed (Brett, 2026-07-25), and today that
development happens entirely outside the dashboard: the wheel shows a
staged tile as six words on a 196x132 drum face, the explorer lists its
folder, and the viewer opens one document at a time. Nothing puts a
topic's documents, its connections, and its outline on one surface at one
scope.

Two gaps make that surface impossible to assemble today.

FIRST, nothing says how far a document has come. Every maturity signal the
corpus carries is either a DEFECT signal (doc-health findings — something
is wrong) or a JUDGMENT signal (the three-tier readiness panel — reviewers
scoring a whole cluster 1-10, gating a recommendation flag). Neither
answers the question a human asks while working a topic: which of these
eleven documents is a stub and which is nearly done? That is a
structural question about one document, and it is answerable
deterministically from the tree — sections present, body length, open
markers still standing, declared topics that resolve to the vocabulary,
edges into the rest of the corpus.

SECOND, the snapshot is the dashboard's only data path, and it carries no
such field. The promoted capability already fixes the remedy: "a view
acquires data by delta declaring new snapshot fields and the generator
populating them" — the renderer MUST NOT scan the repository. So the
workbench cannot exist until the snapshot grows.

This change lands the read-only foundation: the derived-model growth that
makes completeness visible, the scoped view that reads it, and the tile
action that opens it. The AI chat layer that will make the workbench
generative is Track C — deliberately a LATER change (see out of scope).

## What Changes

- ADD a deterministic per-document completeness signal to the snapshot's
  derived model. The generator computes it at generation time and emits an
  additive `completeness` object on each `documents[]` entry: a `score`
  plus five named signals — `structure` (the document's expected
  structural elements present), `length` (body size against a fixed
  saturation threshold), `open_markers` (an INVERSE signal over
  open-question / TODO markers), `keyword_coverage` (declared `Topics:`
  subjects that resolve to the snapshot's keyword vocabulary), and
  `link_degree` (the document's snapshot edge degree). No model call, no
  judgment: the whole computation is a function of the pinned tree, so the
  same tree yields the same scores and a byte-identical snapshot.
- FIX the weights as contract constants in v1. The score is a fixed-weight
  combination of the five normalized signals at a fixed decimal precision;
  a tunable weight configuration is a possible successor, not part of this
  change (design D2, open question 1).
- BOUND the per-document score to judgment-free surfaces, with ONE
  sanctioned gate consumer. Completeness is not an input to the readiness
  recommendation gate and produces no doc-health finding; the
  staged-to-proposal readiness gate below is the only verb that may refuse
  on it, and only through the staged-topic health aggregate. (Brett's
  2026-07-25 ruling — a gate must hold the staging→proposal move until
  open questions are closed and enough is done — supersedes this change's
  earlier informational-only posture.)
- ADD a per-staged-topic health aggregate to the snapshot's derived model:
  an additive `health` object on each `staged_topics[]` entry, computed
  from the topic FOLDER's own corpus documents — standing open items
  (summed `open_markers` raw counts), doc score min/mean, a typed
  `blockers` list, and a derived tri-state `status`
  (`ready` / `developing` / `stub`). The ready threshold
  (`READY_MIN_SCORE`) is a contract constant in v1, pinned beside the
  completeness weights. Deterministic and additive, exactly like the
  per-document signal.
- ADD the staged-to-proposal readiness gate: the `propose` action refuses
  a topic whose health is not `ready`, evaluated LIVE against the pinned
  checkout with the same scoring module the generator uses (never the
  possibly-stale snapshot), citing the blockers concretely and persisting
  nothing. Enforced at the route, so tile, CLI, and direct requests are
  gated identically; the existing missing-topic and duplicate refusals
  stand unchanged.
- ADD two-level tile health display on the staged wheel: a compact health
  indicator on the FOCUSED (first-click) tile face, and the full health
  block — status, standing open items per document, score min/mean,
  blockers — on the EXPANDED (second-click) tile, rendered verbatim from
  the snapshot. Resting drum faces stay unadorned.
- EXTEND (additive, no `contract_schema_version` bump)
  `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`: the
  `document` `$def` grows an optional `completeness` object. Additive by
  the schema's own stated posture (consumers ignore unknown properties, no
  object sets `additionalProperties: false`), so every existing snapshot
  stays valid and a renderer reading a pre-growth snapshot degrades to "no
  bars" rather than failing.
- ADD the staging workbench: a full-screen view scoped to exactly ONE
  topic-bearing tile — a cluster, a possible, or a staged topic — with
  three tabbed panels. `docs` lists the tile's document set from the
  snapshot's own edges, each row carrying its completeness bar and the
  named signals behind it. `lens` renders interconnectedness scoped to
  that tile's keywords and documents by RE-SCOPING the existing
  keyword-lens and degree derivation — no new analysis, no new snapshot
  field. `outline` renders the topic's outline when one exists (for a
  staged topic, the fragment's outline material) through the same
  read-only `/source` pass-through the viewer and the wheel's `landed`
  verb already use.
- HOLD the workbench read-only. It writes NOTHING in this change: no
  document, no register entry, no `ideation-workbench` manifest, no gate
  artifact. Outline EDITING is out of scope here.
- ADD the `open workbench` tile action on the clusters, possibles, and
  staged wheels through the wheel's established action-row extension point
  (`WHEEL_ACTIONS` / `actionsFor` plus one `ACTION_MOUNTERS` entry,
  described in `add-wheel-action-verbs` design and not re-specified here).
  Because it writes nothing it carries NO gate capability requirement,
  exactly like the existing read-only `read` / `lens` / `canvas` /
  `landed` verbs, and it is therefore offered on the deployed static image
  too, where content-dependent panels degrade inline.

## Impact

- Affected specs: `ideation-dashboard` (six ADDED requirements: the
  completeness signal, the staged-topic health signal, the workbench view,
  the workbench tile action, the staged-to-proposal readiness gate, the
  staged tile health display). No MODIFIED requirement: the "Snapshot
  projection contract" requirement already prescribes additive field
  growth by delta as the way a view acquires data, and the "Interactivity
  boundary" requirement already bounds a read-only surface — this change
  adds within both rather than restating either. The readiness gate ADDS a
  refusal condition beside `add-propose-verb`'s staged-topic proposal
  commissioning requirement without modifying it (that change's own
  refusals stand); archive `add-propose-verb` first, then this.
- Affected schemas: `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`
  (additive `document.completeness` and `staged_topic.health`; no
  `schema_version` bump, no existing snapshot invalidated). No change to
  `ideation-workbench.schema.yaml` — see design D5 on the two senses of
  "workbench".
- Affected code (codexFactory, Speckit-side): `generator.py`
  (`_document_entry` gains the scoring call; one new deterministic scoring
  module with the fixed weights, the health aggregation, and the
  `READY_MIN_SCORE` constant), `serve.py` (the propose route gains the
  readiness guard, importing that same scoring module), `snapshot.py`
  callers unchanged (validation stays schema-driven), the new workbench
  view plus its pure model module, `views/wheel-model.js`
  (`WHEEL_ACTIONS` rows for `clusters` / `possibles` / `staged`; staged
  tile health chrome model) and `views/wheel.js` (`ACTION_MOUNTERS` entry;
  focused-tile indicator + expanded health block), `app.js` nav wiring,
  tests.
- NOT in scope — **Track C, a later change**: the AI chat layer over the
  workbench (a conversational partner that reads the scoped tile and
  drafts material with the human) and everything it implies — outline
  EDITING, writing staging fragments from the workbench, composing or
  revising documents in place, and any workbench write path at all. This
  change is deliberately the read-only foundation Track C will be built
  on; nothing here may be designed as if the chat layer already exists.
- NOT in scope: a tunable weight or threshold configuration (v1 weights
  and `READY_MIN_SCORE` are contract constants); any aggregate for
  clusters or possibles (design D3 — the staged-topic health aggregate is
  the ONE sanctioned aggregate, per Brett's 2026-07-25 ruling); any
  re-scoring of the cross-reference readiness tiers; a gate on any verb
  other than propose; new snapshot fields for the lens panel.
- Compatibility: additive snapshot growth only, no field removed or
  retyped; a pre-growth snapshot renders with no completeness bars; the new
  tile action adds no capability, no route, and no write authority, so the
  hosted plane needs no contract change.
