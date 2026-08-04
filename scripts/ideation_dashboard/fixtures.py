"""R4 worked-example possibles backfill loader (plan "fixtures.py"; change
task 3.1).

The consolidated possibles register (read through `register.py`) is the R4
backfill: it carries entries for the four worked examples ONLY — doc-health,
avatar, ideation-governance, and the DTN register. This module is the generator's
no-fabrication gate over that register: it identifies which corpus documents
actually declare a `Possible feats:` section (the worked examples) and projects
register entries into snapshot `possible`s for those documents ONLY. A legacy
document without a `Possible feats:` section carries no possibles, and no register
history is fabricated for it (FR-004; spec scenario "The worked-example fixtures
load without fabricated history").

The projection is one-for-one and field-for-field with the register `register_entry`
shape, minus the register-only `provenance` (the snapshot's `possible` does not
yet carry it) and with evidence `document` refs mapped to document ids. The
snapshot field set and their order are fixed by `POSSIBLE_FIELDS`.
"""

from __future__ import annotations

import re
from typing import Any

# A `Possible feats:` section header at any markdown depth (`## Possible feats`).
_POSSIBLE_FEATS_RE = re.compile(r"(?m)^#{1,6}\s+Possible feats\b")

# The snapshot `possible` fields projected one-for-one from a register entry.
# `provenance` (register-only) is intentionally absent — the snapshot's `possible`
# does not yet carry it (the schemas note it MAY be projected additively later).
POSSIBLE_FIELDS = (
    "id", "title", "claim", "state", "reason", "citation",
    "claiming_clusters", "pick", "option_set", "supporting_evidence",
    # AI-derivation intake (add-possibles-derivation-lane; contract-v1.14):
    # projected ADDITIVELY so the WHEEL's distinct-class rule can tell an
    # UNDISPOSED derived possible (non-`indexed` edge class) from indexed
    # register data. The kernel and snapshot schemas are open/additive.
    "origin", "derivation",
)


def declares_possible_feats(text: str) -> bool:
    """True when a document declares a `Possible feats:` section — the marker of
    a worked example that may carry possibles."""
    return bool(_POSSIBLE_FEATS_RE.search(text))


def worked_example_doc_ids(docs) -> set[str]:
    """Doc ids (repo-relative paths) that declare a `Possible feats:` section —
    the ONLY documents a possible may attach to. `docs` are doc_health `Doc`s
    (each carrying `.path` and `.text`)."""
    return {d.path for d in docs if declares_possible_feats(d.text)}


def project_possibles(
    entries: list[dict[str, Any]],
    *,
    worked_example_docs: set[str],
    path_to_doc_id: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Project consolidated register entries into snapshot `possible`s (sorted by
    id). Drops the register-only `provenance`, maps evidence `document` paths to
    document ids, and — the no-fabrication guard — skips any entry whose
    provenance document is not a worked example that actually declares a
    `Possible feats:` section, so legacy docs never acquire invented possibles."""
    path_to_doc_id = path_to_doc_id or {}
    out: list[dict[str, Any]] = []
    for entry in entries:
        provenance = entry.get("provenance") or {}
        source = provenance.get("document")
        if source is not None and source not in worked_example_docs \
                and entry.get("origin") != "ai-derived":
            # The no-fabrication gate guards `Possible feats:` INGESTIONS —
            # an ai-derived entry is not one: its provenance cites the primary
            # source member + the deriving cluster context, its legitimacy is
            # the derivation contract (worker-run identity + pending_review +
            # cluster edge + evidence pin, validator-enforced), and dropping
            # it here would silently hide every lane-merged possible from the
            # dashboard.
            continue
        projected: dict[str, Any] = {}
        for key in POSSIBLE_FIELDS:
            if key in entry and entry[key] is not None:
                if key == "supporting_evidence":
                    projected[key] = [_project_evidence(pin, path_to_doc_id)
                                      for pin in entry[key]]
                else:
                    projected[key] = entry[key]
        out.append(projected)
    out.sort(key=lambda p: p["id"])
    return out


def _project_evidence(pin: dict[str, Any], path_to_doc_id: dict[str, str]) -> dict[str, Any]:
    """Map an evidence pin's `document` (a repo-relative path in the register) to
    the projected document id (identity while document id == repo-relative path)."""
    projected = dict(pin)
    document = projected.get("document")
    if document in path_to_doc_id:
        projected["document"] = path_to_doc_id[document]
    return projected
