#!/bin/sh
# Fake document-cataloger worker (T001): prints a valid, contract-conforming
# recommendation artifact to stdout, ignoring stdin -- mirrors the shape a
# real `claude` binary invocation would return for one dispatched shard,
# standing in for the model-invocation boundary in hermetic tests
# (tests/doc-health/test_catalog_dispatch.py), the same role
# semantic.py's real_invoke seam plays for the sibling sweep worker.
#
# The target document is configurable via environment variables so a test
# can point this at a REAL selected document (matched by repo + path):
# REPO, DOC_PATH, PASSAGE.
#
# Prompt contract v3: the worker returns the grounding PASSAGE verbatim, not
# a hash (a tool-less `claude -p --tools "" --max-turns 1` child cannot
# compute SHA-256); orchestration computes the persisted passage_sha256. The
# worker no longer echoes `content_hash` either -- enforce_contract matches
# each entry to its shard selection by (repo, path) and persists the shard's
# own authoritative content_hash, so echoing one added no integrity and only
# invited transcription drift (live run 29349336374 dropped a single hex
# character from one of 25 entries under v2, voiding the whole artifact).
REPO="${REPO:-alpha}"
DOC_PATH="${DOC_PATH:-docs/a.md}"
PASSAGE="${PASSAGE:-The Overview section states this document governs the widget domain.}"

cat <<JSON
{"entries": [{"repo": "$REPO", "path": "$DOC_PATH", "facet_assignments": [{"facet": "factory_scope", "values": ["domain"], "confidence": 0.9, "section": "## Overview", "passage": "$PASSAGE", "evidence_refs": [], "proposed_values": []}]}]}
JSON
