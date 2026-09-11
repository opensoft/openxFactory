"""The add-as-cluster VERB: the lens set-builder's one reach into openxFactory's
cross-reference queue (pre-carve split S-2, `split-opendox-two-layer-product`
§ 3.1).

COLUMN: `openxFactory`'s OWN ENGINEERING ADAPTER (design D3's third column,
RULING DQ-1) — the same column as `human_seen.py`, which this module is the
lens-side caller of. `lens.py` is openDox (D3: "the keyword-query half of `lens`
… PULL UP"), and `add_as_cluster` was the one thing in it that was not: it
submits a human-seen cluster proposal into `openxFactory`'s cross-reference
recommendation queue, which a student or a lab assistant using openDox has no
notion of.

WHY A MODULE AND NOT AN EDIT CLASS. The § 3.1 carve manifest files every path
with ONE disposition and one destination; a file whose halves belong to two
columns cannot be filed, and an import rewrite cannot invent a module. Lifting
`AddAsClusterResult` and `add_as_cluster` out UNCHANGED, byte for byte, is what
makes `lens.py` a pure per-file move later. The scout memo (§ 4, S-2) measured
this as the single `oD -> openxFactory` import edge in the whole package.

NO RE-EXPORT BACK INTO `lens.py`, deliberately. The obvious kindness — leaving
`from .lens_submission import add_as_cluster` behind so every caller keeps
working — would re-import `human_seen` into `lens.py` transitively and put the
edge straight back. The point of the split IS the removed edge, so the two
in-tree callers are repointed instead: `gate_routes.execute_lens_add_as_cluster`
and `tests/ideation-dashboard/test_lens.py`. `lens.py` no longer imports
`human_seen` in any form, and `test_lens_column_split.py` keeps it that way.

WHAT STAYED BEHIND, AND WHY. `PENDING_PROPOSAL_NOTE` is still `lens.py`'s,
imported back here: it carries a byte-identity contract with the browser half
(`web/views/lens-model.js`'s constant of the same name, asserted by
`test_js_and_python_persistence_constants_agree`), and both are the openDox
lens. Splitting the pair across the column boundary would have moved a
cross-checked constant away from the thing it is cross-checked against. That
import, and the four names read from `workbench.py`, are this module's two
`stays -> openDox` reaches; they are recorded for the manifest author rather
than solved here, and § 7 OQ-B is RULED as of 2026-09-09 (Brett Heap, `#656`,
"rule all OQs as recommended"): these two reaches are the ones the ruling
leaves IN-TREE, because `add_as_cluster` is adapter->core by construction and
the carve reaches it THROUGH openXdox as an `import rewrites` edit. The sibling
reaches that same ruling re-plumbs BEFORE the carve are elsewhere --
`human_seen.py`'s `workbench.slug` (B-1, PR #843: `slug` into the neutral
`scripts/path_slug.py`, which is where `human_seen` reads it once that lands)
and the four `serve_wire` names `serve_openxfactory_lanes.py` reads (B-2).

NO BEHAVIOUR CHANGE: same names, same signatures, same order of operations,
same refusals.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py
    sys.path.insert(0, str(_SCRIPTS_DIR))

# § 5.2 SHED REACH (RULED (a) / RULED Q7, `#656`): `lens` and `workbench` left
# openxFactory at the carve and are read from the PINNED openDox leg through
# the ONE resolver. See `scripts/carved_reach.py`.
from carved_reach import install as _install_carved_reach  # noqa: E402

_install_carved_reach()

from . import human_seen  # noqa: E402
from .human_seen import HumanSeenSubmission, SubmissionRefused  # noqa: F401 (re-export)
from opendox.lens import PENDING_PROPOSAL_NOTE
from opendox.workbench import ACTION_ADD_AS_CLUSTER, OutputBoundary, Workbench, save


@dataclass
class AddAsClusterResult:
    """Outcome of `add_as_cluster`: the recipe-seeded manifest path PLUS the
    human-seen submission written into the cross-reference queue."""
    manifest_path: Path
    queue_path: Path
    queue_relpath: str
    cluster_id: str
    intake: dict
    note: str = PENDING_PROPOSAL_NOTE


def add_as_cluster(
    w: Workbench, boundary: OutputBoundary, snapshot: Mapping,
    submission: HumanSeenSubmission, *,
    relpath: str | None = None, now: str | None = None,
    validate: bool = False, validator: Path | None = None,
    xref_validator: Path | None = None, repo=None,
) -> AddAsClusterResult:
    """Create the recipe-seeded workbench reference set on disk AND submit the
    human-seen cluster proposal into the cross-reference recommendation queue
    (change 3.5 / T028; the pending_review intake contract realized 2026-07-14).

    Order (nothing is persisted until the evidence is complete):

      1. REFUSE an evidence-incomplete submission before ANY write (spec scenario
         "A submission lacks evidence" — `human_seen.require_complete_evidence`).
      2. Build the human-seen intake from the set's members + the submission's
         organizer evidence, write the `pending_review` entry into the gitignored
         cross-reference queue THROUGH the boundary, and (`validate=True`)
         re-check it with the pinned cross-reference validator (`xref_validator`).
      3. Record the honest `add-as-cluster` action referencing that queue entry.
      4. Save the recipe-seeded manifest through the boundary LAST, so the
         PERSISTED manifest carries the action_history entry (`validate=True`
         re-checks it with the pinned dashboard validator, `validator`).

    The manifest is saved AFTER the action is recorded: recording appends the
    `add-as-cluster` entry to the in-memory workbench, so saving last is what puts
    it in the file at `manifest_path` (previously the action was appended after
    save, leaving the written manifest without it).

    Returns the manifest + queue paths and the intake index. The proposal NEVER
    bypasses review — a disposing authority folds it into the index on acceptance
    (retaining its `origin: human-seen` provenance)."""
    human_seen.require_complete_evidence(submission)            # step 1: refuse first
    result = human_seen.submit_from_workbench(                  # step 2: write queue entry
        w, snapshot, submission, boundary, now=now,
        validate=validate, validator=xref_validator, repo=repo)
    w.record_action(ACTION_ADD_AS_CLUSTER, reference=result.relpath, now=now)  # step 3
    manifest_path = save(w, boundary, relpath=relpath, validate=validate,       # step 4: persist WITH the action
                         validator=validator)
    return AddAsClusterResult(
        manifest_path=manifest_path, queue_path=result.path,
        queue_relpath=result.relpath, cluster_id=result.cluster_id,
        intake=result.index, note=PENDING_PROPOSAL_NOTE)
