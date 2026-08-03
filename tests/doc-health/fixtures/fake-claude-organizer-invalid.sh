#!/bin/sh
# Fake ideation-organizer worker returning CONTRACT-VIOLATING output: a
# non-numeric confidence. organizer.enforce_contract rejects the WHOLE artifact
# (spec "Whole-artifact rejection"), so the merge records rejected=1 and
# persists nothing -- the sibling of fake-claude-cataloger-invalid.sh.
REPO="${REPO:-openxFactory}"
DOC_PATH="${DOC_PATH:-ideation/brainstorm/inbox/XFI-2026-014/idea.md}"
SECTION="${SECTION:-problem-statement}"
PASSAGE="${PASSAGE:-Could be neutral doc-health or OpsxFactory monitoring; awaiting triage.}"

cat <<JSON
{"recommendations": [{"claim_candidate_id": "candidate-01", "source_ref": {"repository": "$REPO", "path": "$DOC_PATH", "section": "$SECTION", "passage": "$PASSAGE"}, "summary": "x", "recommended_scope": "unclassified", "alternatives": [], "domain_local_exclusions": [], "ambiguity": ["Owner unknown"], "rationale": "r", "confidence": "high"}]}
JSON
