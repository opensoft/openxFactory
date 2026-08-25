#!/bin/sh
# Fake neutrality-scout worker: prints a valid, contract-conforming
# candidates artifact to stdout, ignoring stdin -- mirrors the shape a real
# `claude` invocation would return for one dispatched batch, standing in for
# the model-invocation boundary in hermetic tests (test_neutrality_dispatch
# .py), the same role fake-claude-organizer.sh plays for the organizer lane.
#
# The judged subject is configurable via environment variables so a test can
# point this at a REAL dispatched subject (matched by repository + path):
# REPO, DOC_PATH, DECISION.
#
# Per the prompt contract the scout returns ONLY subjects it judges
# neutral-worth; dispatched subjects it omits were judged domain-appropriate.
REPO="${REPO:-MedxFactory}"
DOC_PATH="${DOC_PATH:-schemas/generic-envelope.schema.yaml}"
DECISION="${DECISION:-promote}"

cat <<JSON
{"candidates": [{"repository": "$REPO", "path": "$DOC_PATH", "what_it_is": "A generic queue-item envelope schema with no domain vocabulary. It declares ids, digests, retry budgets, and labels any factory needs.", "neutrality_evidence": ["The schema body defines only generic queue fields (item_id, queue_name, body_digest, retry_budget) with no domain nouns", "Zero domain vocabulary anywhere in the file content"], "counter_evidence": ["The retry budget ceiling of five may encode one team's operational preference"], "domain_local_exclusions": ["any deployment-specific queue naming convention"], "suggested_decision": "$DECISION", "suggested_artifact": "contracts/schemas/xfactory-queue-item-envelope.schema.yaml", "confidence": 0.86}]}
JSON
