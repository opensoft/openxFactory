"""Doc-health checker suite: the in-repo implementation of the promoted
openxFactory `doc-health` contract (adopted from codexFactory by
`adopt-neutral-tooling-home`).

The contract (check families, severities, thresholds, report schema) is
owned by docs/doc-health.md and the `doc-health` spec; this package
implements it in the same repository. Changes to WHAT the checks are
happen through the contract; this package follows.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CRITICAL = "critical"
ERROR = "error"
AUTO_FIXABLE = "auto-fixable"
CONTESTED = "contested"
WARNING = "warning"
INFO = "info"
SEVERITY_RANK = {CRITICAL: 0, ERROR: 1, WARNING: 2, INFO: 3}

TAXONOMY = {
    "brainstorm", "staged", "draft", "ratified",
    "standard", "superseded", "retired", "record",
}

# Contract defaults (openxFactory doc-health "Aging Threshold Defaults").
# A run overriding any of these must state the deviation in its report.
DEFAULT_THRESHOLDS = {
    "staged_warning_days": 30,
    "staged_error_days": 90,
    "candidate_warning_days": 30,
    "candidate_error_days": 90,
    "supersedes_warning_days": 14,
    "supersedes_error_days": 45,
    "draft_warning_days": 60,
    # add-document-cataloging: pending-classification facet aging,
    # measured from state_since (research D8 / data-model.md facet
    # state machine).
    "document_catalog_pending_warning_days": 30,
    "document_catalog_pending_error_days": 90,
    # add-cross-factory-ideation-routing: routing-record aging measured
    # from the latest transition (doc-health delta "Aging threshold
    # defaults"). intake/triaging/incomplete-split records age; routed,
    # rejected, and explicitly deferred records do not.
    "routing_warning_days": 30,
    "routing_error_days": 90,
}

# Contract family ids, in the contract's table order.
FAMILY_IDS = [
    "status-validity",
    "standard-backing",
    "ratified-provenance",
    "succession-integrity",
    "location-conformance",
    "record-immutability",
    "staged-candidate-aging",
    "register-lifecycle-consistency",
    "tag-hygiene",
    "submodule-pin-drift",
    "contract-copy-drift",
    "notebook-projection-drift",
    # thirteenth family (add-document-cataloging, FR-006).
    "document-catalog",
    # fourteenth family (add-cross-factory-ideation-routing; doc-health
    # delta "Deterministic check families").
    "ideation-routing",
]


@dataclass(frozen=True)
class Finding:
    severity: str
    family: str
    repo: str
    path: str
    rule: str
    action: str
    resolution: str = "auto-fixable"
    disposer: str | None = None  # semantic findings name their disposition authority

    def sort_key(self):
        return (SEVERITY_RANK[self.severity], self.family, self.repo,
                self.path, self.rule)

    def match_key(self):
        """Regression-rule identity: contract matches by family + path."""
        return (self.family, self.repo, self.path)


@dataclass
class Skip:
    family: str
    reason: str


@dataclass
class RunResult:
    findings: list = field(default_factory=list)
    skips: list = field(default_factory=list)
    preflight: list = field(default_factory=list)  # (repo, entry, ok, detail)
