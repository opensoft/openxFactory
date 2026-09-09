"""Keyword-lens recipe evaluation + persistence (D13; change 3.10; US6 T024).

The lens is the set-builder that lets a human name an intensional cluster the
machine clustering missed — a keyword query (checked + pinned) over the
DECLARED controlled vocabulary (`documents[].topics`), persisted as a
re-runnable workbench recipe. This module is the Python half, sitting next to
the workbench engine (`workbench.py` owns manifest persistence + the W1 guard);
the browser half is `web/views/lens-model.js` (bullseye geometry) — the two
share ONLY the semantics below, verified by the JS/Python cross-checks in
test_lens.py.

RECIPE SEMANTICS (the same rules lens-model.js implements):

  check = stratify   a checked keyword contributes to a document's MATCH COUNT
                     (how many checked keywords it carries). The bullseye shows
                     every document matching >= 1 checked keyword, stratified by
                     match count; innermost ring = matches ALL checked.
  pin = require      a pinned keyword HARD-FILTERS: a document lacking it is off
                     the bullseye entirely (never a near-miss ring). W1: pinned
                     MUST be a subset of checked (validator rule + set_recipe).

  matched (recipe membership)  the documents matching ALL checked keywords (the
                     innermost ring) — the recipe's intensional definition,
                     auto-included as `recipe-match` members. Outer-ring docs
                     are near-misses a human may pull in as a `manual-include`
                     OVERRIDE (with a recorded reason); a center doc a human
                     removes becomes an `excluded` OVERRIDE (with a reason).
                     Overrides are evidence, never a silent set edit — the
                     workbench engine refuses either without a reason.

  re-run             recipe evaluation is PURE given (snapshot, recipe): as the
                     corpus grows, `new_candidates` = newly-matched docs NOT
                     already recorded as members or excluded (so the validator's
                     "new_candidates disjoint from members ∪ excluded" rule holds
                     and recorded OVERRIDES are never touched — spec scenario 4).

  add-as-cluster     creates the recipe-seeded workbench manifest through the
                     engine + boundary AND submits the human-seen cluster
                     proposal into the cross-reference recommendation queue
                     (change 3.5 / T028), recording the HONEST `add-as-cluster`
                     action referencing the queue entry. The pending_review
                     intake contract is now REALIZED (2026-07-14,
                     add-ideation-cross-reference-readiness), so the submission
                     path (`human_seen.py`) builds the intake, refuses one
                     lacking the full evidence contract before persistence, and
                     writes the `pending_review` entry into the gitignored queue
                     validated by the pinned cross-reference validator — never
                     rewriting the generated index. The Python half of this verb
                     now lives in `lens_submission.py` (pre-carve split S-2):
                     submitting into openxFactory's cross-reference queue is
                     adapter-column work, so this module states the semantics and
                     no longer imports `human_seen`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from . import workbench as wb
from .workbench import (
    SEED_RECIPE, VIA_MANUAL_INCLUDE, VIA_RECIPE_MATCH,
    Workbench, WorkbenchError, _utcnow,
)

# `lens_submission.add_as_cluster` SUBMITS the human-seen cluster proposal into
# the cross-reference recommendation queue (change 3.5 / T028). The T028 blocker
# cleared 2026-07-14 when add-ideation-cross-reference-readiness realized the
# pending_review intake contract in ideation-cross-reference.schema.yaml; the
# submission path lives in human_seen.py (build -> refuse-if-incomplete -> write
# -> validate against the pinned cross-reference validator). THE VERB LEFT THIS
# MODULE with pre-carve split S-2; the NOTE stayed, because it is surfaced BOTH
# on-screen (the browser PLAN — byte-identical to lens-model.js's
# PENDING_PROPOSAL_NOTE) and as the lens_submission.add_as_cluster result note,
# and that byte-identity cross-check is between this module and its OWN browser
# half.
PENDING_PROPOSAL_NOTE = (
    "Workbench reference set created (recipe-seeded, through the engine + "
    "boundary) and the human-seen cluster proposal submitted to the "
    "cross-reference queue with a pending_review disposition — a disposing "
    "authority reviews it; it never bypasses review, and on acceptance it "
    "becomes a topic cluster."
)


# --------------------------------------------------------------------------
# pure recipe evaluation (snapshot, recipe) -> membership + bullseye rows
# --------------------------------------------------------------------------

@dataclass
class RecipeEvaluation:
    """The deterministic result of evaluating a recipe against a snapshot.

    `matched`  documents matching ALL checked keywords (recipe membership, the
               innermost ring) — what `new_candidates` derives from.
    `universe` documents on the bullseye (>= 1 checked keyword, passing the pin
               filter) — the flat matrix / bullseye membership.
    `rows`     one entry per universe doc, in snapshot document order:
               {document, matched_subset (checked order), match_count}.
    """
    checked: list[str]
    pinned: list[str]
    matched: list[str] = field(default_factory=list)
    universe: list[str] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)


def _doc_topics(snapshot: Mapping) -> list[tuple[str, set[str]]]:
    """(document id, declared-topic set) in snapshot document order (sorted by
    path in the generator) — declared only; inferred tags arrive with document-
    cataloging and are OUT of v1."""
    out: list[tuple[str, set[str]]] = []
    for d in snapshot.get("documents") or []:
        if isinstance(d, dict) and d.get("id"):
            out.append((d["id"], set(d.get("topics") or [])))
    return out


def evaluate_recipe(snapshot: Mapping, checked: Sequence[str],
                    pinned: Sequence[str] = ()) -> RecipeEvaluation:
    """Evaluate a keyword recipe against a snapshot. PURE: depends only on the
    snapshot's `documents[].topics` and the checked/pinned sets. Enforces W1
    (pinned ⊆ checked) up front so an ill-formed query fails loud, matching
    `Workbench.set_recipe`."""
    checked = list(checked)
    pinned = list(pinned)
    stray = set(pinned) - set(checked)
    if stray:
        raise WorkbenchError(
            f"recipe pinned keyword(s) {sorted(stray)} are not in checked "
            "(validator rule W1: pinned MUST be a subset of checked)")

    ev = RecipeEvaluation(checked=checked, pinned=pinned)
    pin_set = set(pinned)
    n_checked = len(checked)
    for doc_id, topics in _doc_topics(snapshot):
        if not pin_set <= topics:          # pin = require: hard filter
            continue
        matched_subset = [k for k in checked if k in topics]  # preserve checked order
        match_count = len(matched_subset)
        if match_count == 0:               # matches no checked keyword: off the bullseye
            continue
        ev.universe.append(doc_id)
        ev.rows.append({
            "document": doc_id,
            "matched_subset": matched_subset,
            "match_count": match_count,
        })
        if n_checked and match_count == n_checked:  # innermost ring = recipe membership
            ev.matched.append(doc_id)
    return ev


# --------------------------------------------------------------------------
# recipe re-run (grows new_candidates without touching overrides)
# --------------------------------------------------------------------------

def recipe_of(w: Workbench) -> tuple[list[str], list[str]]:
    recipe = w.data.get("recipe") or {}
    return list(recipe.get("checked") or []), list(recipe.get("pinned") or [])


def rerun_recipe(snapshot: Mapping, w: Workbench, *, now: str | None = None) -> list[str]:
    """Re-evaluate the manifest's recipe against a (possibly grown) snapshot and
    record `new_candidates` — documents that now match ALL checked keywords but
    are NEITHER already a member NOR excluded. Recorded overrides (`members` /
    `excluded`) are LEFT UNTOUCHED (spec scenario 4); the result is disjoint from
    members ∪ excluded by construction (validator rule). Updates `recipe.last_run`
    to the snapshot's source revision. Returns the new_candidates list."""
    checked, pinned = recipe_of(w)
    if not checked:
        raise WorkbenchError("manifest has no recipe to re-run (no checked keywords)")
    ev = evaluate_recipe(snapshot, checked, pinned)
    members = set(w.member_documents())
    excluded = {e.get("document") for e in (w.data.get("excluded") or []) if isinstance(e, dict)}
    new_candidates = [d for d in ev.matched if d not in members and d not in excluded]

    stamp = now or _utcnow()
    recipe = w.data.setdefault("recipe", {})
    recipe["checked"] = checked
    if pinned:
        recipe["pinned"] = pinned
    source_revision = (snapshot.get("generation") or {}).get("source_revision") or "unknown"
    recipe["last_run"] = {"source_revision": source_revision, "at": stamp}
    recipe["new_candidates"] = new_candidates
    w._touch(stamp)
    return new_candidates


# --------------------------------------------------------------------------
# recipe-seeded workbench manifest ("save recipe" / "add as cluster")
# --------------------------------------------------------------------------

def build_workbench_from_recipe(
    repository: str, name: str, checked: Sequence[str], pinned: Sequence[str],
    snapshot: Mapping, *,
    includes: Mapping[str, str] | None = None,
    excludes: Mapping[str, str] | None = None,
    now: str | None = None,
) -> Workbench:
    """Assemble a recipe-seeded `ideation-workbench` manifest from a keyword
    query and the current snapshot, THROUGH the engine's override discipline:

      * every doc matching all checked keywords becomes a `recipe-match` member;
      * `includes` are `manual-include` OVERRIDES on non-matching docs — each
        REQUIRES a recorded reason (the engine refuses a bare include);
      * `excludes` are `excluded` OVERRIDES on matching docs the human removed —
        each REQUIRES a recorded reason (the engine refuses a bare exclude) and
        drops the doc from members;
      * `recipe.last_run` is stamped so the set is immediately re-runnable.

    Returns the in-memory Workbench; the caller persists it via `save`/
    `add_as_cluster` through an OutputBoundary. Never writes anything itself."""
    now = now or _utcnow()
    recipe: dict = {"checked": list(checked)}
    if pinned:
        recipe["pinned"] = list(pinned)
    w = Workbench.create(repository, name, seed=SEED_RECIPE, recipe=recipe, now=now)

    ev = evaluate_recipe(snapshot, checked, pinned)
    for doc in ev.matched:
        w.add_member(doc, VIA_RECIPE_MATCH, now=now)
    for doc, reason in (includes or {}).items():
        w.add_member(doc, VIA_MANUAL_INCLUDE, reason=reason, now=now)
    for doc, reason in (excludes or {}).items():
        w.exclude(doc, reason, now=now)  # engine refuses a bare exclude; drops from members

    source_revision = (snapshot.get("generation") or {}).get("source_revision") or "unknown"
    w.data["recipe"]["last_run"] = {"source_revision": source_revision, "at": now}
    return w
