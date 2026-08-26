#!/bin/sh
# Fake document-cataloger worker (T001): prints a CONTRACT-VIOLATING
# recommendation artifact (an invented facet name outside the contract's
# six controlled facets) to stdout, ignoring stdin -- exercises
# cataloger.enforce_contract's whole-artifact rejection path (FR-009: a
# single defect voids the entire artifact). Same env-var target
# configuration as fake-claude-cataloger.sh (REPO, DOC_PATH, PASSAGE), so a
# test can still land the artifact against a real dispatched shard/document
# (matched by repo + path) before the facet-name defect itself triggers
# rejection. Prompt contract v3: no worker-echoed content_hash.
REPO="${REPO:-alpha}"
DOC_PATH="${DOC_PATH:-docs/a.md}"
PASSAGE="${PASSAGE:-The Overview section states this document governs the widget domain.}"

cat <<JSON
{"entries": [{"repo": "$REPO", "path": "$DOC_PATH", "facet_assignments": [{"facet": "not_a_real_facet", "values": ["domain"], "confidence": 0.9, "section": "## Overview", "passage": "$PASSAGE", "evidence_refs": [], "proposed_values": []}]}]}
JSON
