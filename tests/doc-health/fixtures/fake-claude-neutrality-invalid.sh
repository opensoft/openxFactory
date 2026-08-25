#!/bin/sh
# Fake neutrality-scout worker returning CONTRACT-VIOLATING output: a
# suggested_decision outside promote|split. neutrality_dispatch
# .enforce_contract rejects the WHOLE artifact (task 1.3 "reject malformed,
# never partially apply"), so the merge records rejected=1 and drafts
# nothing -- the sibling of fake-claude-organizer-invalid.sh.
REPO="${REPO:-MedxFactory}"
DOC_PATH="${DOC_PATH:-schemas/generic-envelope.schema.yaml}"

cat <<JSON
{"candidates": [{"repository": "$REPO", "path": "$DOC_PATH", "what_it_is": "A generic queue-item envelope schema.", "neutrality_evidence": ["Generic queue fields only"], "counter_evidence": [], "domain_local_exclusions": [], "suggested_decision": "relocate", "confidence": 0.9}]}
JSON
