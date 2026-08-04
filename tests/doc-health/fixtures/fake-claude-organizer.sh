#!/bin/sh
# Fake ideation-organizer worker: prints a valid, contract-conforming
# recommendation artifact to stdout, ignoring stdin -- mirrors the shape a real
# `claude` invocation would return for one dispatched idea, standing in for the
# model-invocation boundary in hermetic tests (test_organizer_dispatch.py), the
# same role fake-claude-cataloger.sh plays for the sibling cataloger worker.
#
# The target source is configurable via environment variables so a test can
# point this at a REAL selected source (matched by repository + path):
# REPO, DOC_PATH, SECTION, PASSAGE.
#
# Per the organizer prompt contract the worker returns the grounding PASSAGE
# verbatim (a tool-less `claude -p --tools "" --max-turns 1` child cannot
# compute SHA-256) and NO revision -- orchestration derives passage_sha256 and
# supplies the committed revision. The disposition is omitted; orchestration
# forces `pending_review`.
REPO="${REPO:-openxFactory}"
DOC_PATH="${DOC_PATH:-ideation/brainstorm/inbox/XFI-2026-014/idea.md}"
SECTION="${SECTION:-problem-statement}"
PASSAGE="${PASSAGE:-Could be neutral doc-health or OpsxFactory monitoring; awaiting triage.}"

cat <<JSON
{"recommendations": [{"claim_candidate_id": "candidate-01", "source_ref": {"repository": "$REPO", "path": "$DOC_PATH", "section": "$SECTION", "passage": "$PASSAGE"}, "summary": "Cross-repo document-freshness signal", "recommended_scope": "unclassified", "proposed_owner": null, "proposed_target": null, "alternatives": [], "domain_local_exclusions": [], "dependencies": [], "ambiguity": ["Owner unknown; needs triage."], "rationale": "Captured before ownership is known.", "confidence": 0.72}]}
JSON
