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
    # sixteenth family (add-client-identity-roster; doc-health delta
    # "Deterministic check families"). The FIFTEENTH, "proposal-origin", is
    # absent from this list — a pre-existing omission that leaves that family
    # without a report section. It is recorded in this feature's research and
    # deliberately NOT fixed here: repairing another capability's registration
    # inside this change would put an unrelated family's report output on this
    # feature's evidence.
    "client-identity-composition",
    # eighteenth family (add-promotion-fidelity-check; doc-health delta
    # "Deterministic check families"). Registered here so the family gets
    # its own report section — the omission that left "proposal-origin"
    # sectionless above is a known defect, not a pattern to copy.
    "promotion-fidelity",
    # nineteenth family (add-release-inventory-drift-check; doc-health delta
    # "Deterministic check families").
    "release-inventory-drift",
    # twentieth family (add-duplicate-packet-check; doc-health delta
    # "Deterministic check families"). The eighteenth family's neighbour:
    # it asks whether ONE ruling was discharged by TWO archived packets,
    # which promotion fidelity reads as healthy either way.
    "duplicate-packet",
]


def recorded_rel(value: object) -> object:
    """A recorded repository-relative path, in the spelling this suite resolves.

    Governed records carry paths as machine-readable KEYS: a proposal packet's
    `origin.path`, and a support manifest's `origin_path`, `files[].path`,
    `files[].source_path` and `source_snapshot_path`. Every one of them was
    written by `str(PurePath)` at some point in this tooling's history, which
    on a Windows checkout spells them with backslashes. Read on any other
    machine each becomes a SINGLE component that resolves to nothing, and the
    two failure modes are both bad in their own way: `git ls-tree` matches no
    entry, so a sound record reports as unresolvable provenance (a false
    ERROR); and `Path(repo) / <that>` is not a directory, so a check
    SKIPS instead of running, which is worse — a check that silently does not
    run cannot be seen to have missed anything.

    So every reader here normalizes rather than assuming its own spelling. The
    writers were fixed first (PR #221 for the origin path, and its follow-up
    for the manifest's file paths), but fixing a writer cannot reach the
    records already on disk.

    THE SAME RULE as `proposal-support.py`'s `manifest_rel`, and deliberately a
    second copy: that mover is a hyphenated standalone script and cannot be
    imported. The two are pinned to each other by test, because two readers of
    one record that disagree about its alphabet would have one call a manifest
    sound while the other called it corrupt. Non-strings pass through
    untouched, so a malformed record still fails exactly as it did before.

    THE TRADEOFF: a POSIX path component may legally contain a backslash and
    would be split here. The staged-origin id grammar does not admit it, and
    for the file names inside a topic — which nothing constrains — the cost is
    a loud miss rather than a silent pass. An absurd case traded for a real one.
    """
    return value.replace("\\", "/") if isinstance(value, str) else value


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
    # `family -> [note line, ...]` for the families that RAN, rendered under
    # that family's own report heading (families.FAMILY_NOTES). A note says
    # something about the RUN a finding list cannot — today, which tree the
    # promotion-fidelity family measured.
    notes: dict = field(default_factory=dict)
