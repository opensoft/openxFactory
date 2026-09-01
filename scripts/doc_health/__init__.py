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

# `projection` is the NINTH standing (declare-generated-projection-status,
# 2026-08-28). It is not a synonym for "generated": a `record` is generated
# too, and stays a record. The distinguishing property is RE-DERIVATION over
# the same path — a projection is rewritten in place from a declared source of
# truth, so it has no captured state to be immutable against, while a dated
# one-shot capture does and keeps `record`.
TAXONOMY = {
    "brainstorm", "staged", "draft", "ratified",
    "standard", "superseded", "retired", "record",
    "projection",
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
# EVERY registered family appears here, and a test pins
# `set(FAMILY_IDS) == set(FAMILIES)` so the drift class cannot come back.
# `families.FAMILIES` remains the sole AUTHORITY for which families exist —
# this list is its complete projection onto the report, not a second
# definition of the set. ORDER here is presentational and deliberately NOT
# pinned to FAMILIES' order: it is the order "## Findings By Family" renders
# sections in (`report.render`), so it is a layout choice, while membership is
# not. RULED 2026-08-25 (Brett, "fix the FAMILY_IDS drift") after two
# registered families — `staged-topic-template` and `proposal-origin` — were
# found reporting 61 findings between them, three of them ERRORS, that counted
# in the headline and the ranked plan while rendering under no section at all.
FAMILY_IDS = [
    "status-validity",
    # second family (add-staged-topic-outline-template). ADDED 2026-08-25 by
    # the FAMILY_IDS drift fix: it had been registered in FAMILIES since
    # 2026-08-15 and never listed here, so its 28 findings had no section.
    "staged-topic-template",
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
    # fifteenth family (add-proposal-origin-contract). ADDED 2026-08-25 by the
    # FAMILY_IDS drift fix. Its absence was recorded here three times as a
    # known omission deferred on the "not in this change's evidence" rule —
    # correctly each time, and the deferral outlived its reason: the family was
    # reporting 33 findings, three of them ERRORS, under no section.
    "proposal-origin",
    # sixteenth family (add-client-identity-roster; doc-health delta
    # "Deterministic check families").
    "client-identity-composition",
    # eighteenth family (add-promotion-fidelity-check; doc-health delta
    # "Deterministic check families"). Registered here so the family gets
    # its own report section — the omission that once left "proposal-origin"
    # sectionless above was a known defect, not a pattern to copy, and is
    # fixed as of 2026-08-25.
    "promotion-fidelity",
    # nineteenth family (add-release-inventory-drift-check; doc-health delta
    # "Deterministic check families").
    "release-inventory-drift",
    # twentieth family (add-duplicate-packet-check; doc-health delta
    # "Deterministic check families"). The eighteenth family's neighbour:
    # it asks whether ONE ruling was discharged by TWO archived packets,
    # which promotion fidelity reads as healthy either way.
    "duplicate-packet",
    # twenty-first family (add-family-enumeration-check; doc-health delta
    # "Deterministic check families"). It derives that requirement's own
    # enumeration and counts from `families.FAMILIES` instead of trusting the
    # hand-restatement every new family has to write.
    "family-enumeration",
    # twenty-second family (add-modified-block-currency-check; doc-health delta
    # "Deterministic check families"). The eighteenth family's other neighbour,
    # reading the OTHER direction: promotion fidelity compares an ARCHIVED delta
    # to canon, this compares an ACTIVE delta to the canon it has not yet
    # replaced — while the change can still be edited, which is the only moment
    # the remedy is one line.
    "modified-block-currency",
    # twenty-third family (add-release-tag-publication-check; doc-health delta
    # "Deterministic check families"). The release surface's other half:
    # release-inventory drift asks whether the DECLARED bundle still describes
    # the bytes, this asks whether that bundle was ever PUBLISHED — an
    # obligation `docs/contract-versioning-policy.md` states absolutely and
    # nothing checked, which is how two bundles reached consumers untagged.
    "release-tag-publication",
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
    #
    # TWO KINDS OF LINE RENDER IN THAT POSITION, and only the first travels in
    # this field. `FAMILY_NOTES` is `(ctx) -> lines` and is collected here beside
    # the family call. `families.FAMILY_SUMMARIES` is `(that family's findings)
    # -> lines` — the per-class tally `add-modified-block-currency-check` § 5.1
    # asks for — and is consulted by `report.render` itself, where the findings
    # it counts are already in hand. Kept apart because they answer different
    # questions (the run vs the findings) and because they differ on a skip: a
    # skipped family still has a basis to state and has no tally to state.
    notes: dict = field(default_factory=dict)
