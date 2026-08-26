"""Cluster-canvas draft authoring (D12; change 3.9; US5 T021).

The canvas's two write actions — option-set CHOOSE-ONE and the COMPOSER — never
touch the possibles register. They assemble a possibles-register SECTION draft
(the `possibles_register:` container the pinned validator recognises) and write
it, through the interactivity boundary's `OutputBoundary`, to a run-local drafts
directory under the gitignored `ideation/workbench/` allowlist. A human reviews
and commits the draft into the register; machinery enters NOTHING. AI
suggest/derive trays are explicitly out of scope (follow-on deltas).

Every drafted entry/transition is SCHEMA-VALID against
`ideation-possibles-register.schema.yaml#/$defs/register_entry` so a human can
apply it verbatim (tested in test_canvas.py via the pinned validator):

  CHOOSE-ONE  the chosen option proceeds; each SIBLING is drafted
              `state: superseded` with the required `reason` and `citation`
              (the chosen member's id — the schema's "citation names what
              displaced it"). latent -> superseded and picked -> superseded are
              the legal moves the register state machine accepts.
  COMPOSER    a new `state: latent` possible carrying `provenance` and any
              attached evidence pins — the durable backlog statement a "member
              unclaimed by any possible" gap prompt asks the human to name.

The register `register_entry` requires `provenance`, which the snapshot's read
projection drops. The draft reconstructs it from what the snapshot DOES carry:
a possible's first evidence pin (document + section), else its claiming
cluster's first member document with the `Possible feats` section. This is why
the draft is faithful and applyable — the human commits it as-is.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Where committed drafts land — MUST match canvas-model.js `DRAFTS_DIR`. Under
# the gitignored `ideation/workbench/` prefix, so a draft is never tracked and
# never the register itself.
DRAFTS_DIR = "ideation/workbench/drafts/"

# The register-section container key the validator auto-detects (see
# validate-ideation-dashboard-contracts.py REGISTER_CONTAINER_KEY).
CONTAINER_KEY = "possibles_register"

# Field order for a human-readable, register-shaped entry.
_ENTRY_ORDER = (
    "id", "title", "claim", "state", "reason", "citation",
    "provenance", "claiming_clusters", "pick", "option_set", "supporting_evidence",
)


def supersede_reason(chosen_id: str) -> str:
    """The one wording shared with canvas-model.js `supersedeReason` (locked by a
    cross-check in test_canvas.py)."""
    return f"Option-set sibling {chosen_id} was chosen at the cluster canvas."


# --------------------------- snapshot lookups ---------------------------

def _possibles(snapshot: dict) -> list[dict]:
    return [p for p in snapshot.get("possibles") or [] if isinstance(p, dict)]


def _cluster(snapshot: dict, cluster_id: str) -> dict | None:
    for c in snapshot.get("clusters") or []:
        if isinstance(c, dict) and c.get("id") == cluster_id:
            return c
    return None


def _first_member_document(snapshot: dict, cluster_id: str) -> str | None:
    cluster = _cluster(snapshot, cluster_id)
    if not cluster:
        return None
    for edge in cluster.get("document_edges") or []:
        if isinstance(edge, dict) and edge.get("document"):
            return edge["document"]
    return None


def _cluster_pins(snapshot: dict, cluster_id: str) -> dict[str, dict]:
    """Evidence pins available on this cluster's evidence board, keyed by
    document (first pin wins) — the pins the composer may attach."""
    pins: dict[str, dict] = {}
    for p in _possibles(snapshot):
        if cluster_id not in (p.get("claiming_clusters") or []):
            continue
        for pin in p.get("supporting_evidence") or []:
            doc = pin.get("document") if isinstance(pin, dict) else None
            if doc and doc not in pins:
                pins[doc] = pin
    return pins


def _derive_provenance(snapshot: dict, possible: dict) -> dict[str, str] | None:
    """Register `provenance` (document + section) for a possible: its first
    evidence pin, else its claiming cluster's first member document."""
    for pin in possible.get("supporting_evidence") or []:
        if isinstance(pin, dict) and pin.get("document"):
            return {"document": pin["document"], "section": pin.get("section") or "Possible feats"}
    for cid in possible.get("claiming_clusters") or []:
        doc = _first_member_document(snapshot, cid)
        if doc:
            return {"document": doc, "section": "Possible feats"}
    return None


def _ordered(entry: dict) -> dict:
    """Re-key an entry into the human-readable register field order (drops keys
    that are absent/None)."""
    out: dict[str, Any] = {}
    for key in _ENTRY_ORDER:
        if key in entry and entry[key] is not None:
            out[key] = entry[key]
    return out


# --------------------------- draft builders ---------------------------

def build_supersede_draft(snapshot: dict, option_set_id: str, chosen_id: str) -> dict:
    """The choose-one draft: a register section of the SIBLING supersessions
    (never the chosen member — proceeding to `picked` is the organize gate, a
    separate human action). Raises ValueError on an unknown option set / chosen
    id / a sibling with no derivable provenance."""
    members = [p for p in _possibles(snapshot)
               if (p.get("option_set") or {}).get("id") == option_set_id]
    if not members:
        raise ValueError(f"no possibles in option set {option_set_id!r}")
    member_ids = {p["id"] for p in members if p.get("id")}
    if chosen_id not in member_ids:
        raise ValueError(f"chosen {chosen_id!r} is not a member of option set {option_set_id!r}")

    entries: list[dict] = []
    for p in members:
        if p.get("id") == chosen_id:
            continue
        provenance = _derive_provenance(snapshot, p)
        if provenance is None:
            raise ValueError(f"cannot derive provenance for sibling {p.get('id')!r}")
        entry = {
            "id": p.get("id"),
            "title": p.get("title") or p.get("id"),
            "claim": p.get("claim") or p.get("title") or p.get("id"),
            "state": "superseded",
            "reason": supersede_reason(chosen_id),
            "citation": chosen_id,
            "provenance": provenance,
            "claiming_clusters": p.get("claiming_clusters"),
            "option_set": p.get("option_set"),
            "supporting_evidence": p.get("supporting_evidence"),
        }
        entries.append(_ordered(entry))
    return {CONTAINER_KEY: entries}


def build_composer_draft(
    snapshot: dict, cluster_id: str, *,
    id: str, title: str, claim: str, evidence_documents: tuple[str, ...] | list[str] = (),
) -> dict:
    """The composer draft: one new `latent` possible for `cluster_id`, with
    provenance and any attached evidence pins resolved from the cluster's
    evidence board. Raises ValueError when required fields are missing or no
    provenance is derivable."""
    if not (id and id.strip()):
        raise ValueError("composer draft requires a non-empty id")
    if not (title and title.strip()):
        raise ValueError("composer draft requires a non-empty title")
    if not (claim and claim.strip()):
        raise ValueError("composer draft requires a non-empty claim")

    board = _cluster_pins(snapshot, cluster_id)
    pins = [board[doc] for doc in evidence_documents if doc in board]

    if pins:
        provenance = {"document": pins[0]["document"],
                      "section": pins[0].get("section") or "Possible feats"}
    else:
        doc = _first_member_document(snapshot, cluster_id)
        if doc is None:
            raise ValueError(f"cannot derive provenance for cluster {cluster_id!r}")
        provenance = {"document": doc, "section": "Possible feats"}

    entry = {
        "id": id.strip(),
        "title": title.strip(),
        "claim": claim.strip(),
        "state": "latent",
        "provenance": provenance,
        "claiming_clusters": [cluster_id],
        "supporting_evidence": pins or None,
    }
    return {CONTAINER_KEY: [_ordered(entry)]}


# --------------------------- draft paths + write ---------------------------

def supersede_draft_path(option_set_id: str, chosen_id: str) -> str:
    return f"{DRAFTS_DIR}supersede-{option_set_id}-{chosen_id}.register.yaml"


def composer_draft_path(possible_id: str) -> str:
    return f"{DRAFTS_DIR}possible-{possible_id}.register.yaml"


def render_draft(draft: dict) -> str:
    """Serialize a draft register section to YAML (block style, field order
    preserved, a leading provenance comment banner)."""
    body = yaml.safe_dump(draft, sort_keys=False, default_flow_style=False, allow_unicode=True)
    header = ("# Cluster-canvas draft (D12) — a possibles-register section for HUMAN COMMIT.\n"
              "# Machinery wrote this under a declared output path; nothing entered the\n"
              "# register. Review, then apply it verbatim into the cross-reference index.\n")
    return header + body


def write_draft(boundary, rel_path: str, draft: dict) -> Path:
    """Write a draft through the interactivity boundary (declared output-path
    allowlist). Never writes the register; the boundary refuses anything outside
    its allowlist."""
    return boundary.write_output(rel_path, render_draft(draft))
