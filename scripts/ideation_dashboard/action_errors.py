"""Lightweight action-route refusal catalog.

The hosted doxBench image intentionally omits NotebookLM's optional authoring
dependencies.  Route dispatch and fixed refusal responses must therefore stay
importable without loading ``notebook_action`` (and, transitively, PyYAML).

``notebook_action`` re-exports these names for compatibility with its callers;
the HTTP server imports this dependency-free module directly.
"""

from __future__ import annotations

ERR_INVALID_BODY = "invalid_request_body"
ERR_UNKNOWN_ACTION = "unknown_action"
ERR_UNKNOWN_TILE_KIND = "unknown_tile_kind"
ERR_INVALID_TILE_ID = "invalid_tile_id"
ERR_UNKNOWN_TILE = "unknown_tile"
ERR_NO_READABLE_DOCUMENTS = "no_readable_documents"
ERR_NLM_UNAVAILABLE = "nlm_unavailable"
ERR_NLM_FAILED = "nlm_failed"
ERR_SNAPSHOT_UNAVAILABLE = "snapshot_unavailable"
ERR_LOOPBACK_ONLY = "loopback_only"
ERR_ACTION_UNAVAILABLE = "action_unavailable"
ERR_ACTION_FAILED = "action_failed"

# code -> (HTTP status, fixed caller-safe message)
ERROR_CATALOG: dict[str, tuple[int, str]] = {
    ERR_INVALID_BODY: (400, "request body must be a JSON object"),
    ERR_UNKNOWN_ACTION: (404, "no such action route"),
    ERR_UNKNOWN_TILE_KIND: (400, "tile_kind must be one of: cluster, staged, proposal"),
    ERR_INVALID_TILE_ID: (400, "tile_id missing or malformed"),
    ERR_UNKNOWN_TILE: (404, "tile not found in the current snapshot"),
    ERR_NO_READABLE_DOCUMENTS: (422, "tile resolves to no readable documents"),
    ERR_NLM_UNAVAILABLE: (503, "nlm unavailable - notebook action skipped, not blocked"),
    ERR_NLM_FAILED: (503, "notebook projection failed (detail in the server log)"),
    ERR_SNAPSHOT_UNAVAILABLE: (503, "snapshot unavailable"),
    ERR_LOOPBACK_ONLY: (403, "notebook action is loopback-only"),
    ERR_ACTION_UNAVAILABLE: (503, "notebook action unavailable on this instance"),
    ERR_ACTION_FAILED: (503, "notebook action failed unexpectedly"),
}


def error_body(code: str) -> dict:
    """Return the fixed wire body for ``code``."""
    return {"error": code, "message": ERROR_CATALOG[code][1]}
