"""Neutral v2 Hermes job lifecycle semantics (T066/T070/T071).

Pure, deterministic checks for scoped v2 job envelopes, runs, and events. The
functions consume plain mappings and never touch ambient clock, network, or
mutable state, so the same contract bytes have the same meaning in the portable
validator and the PostgreSQL conformance lane. Structural validation remains the
responsibility of the offline schema registry; this module enforces scope
sharing, job/run/event correlation, monotonic event sequencing, terminal-layer
new-job denial, retained retired-layer evidence access, and neutral-core
exclusion of single-domain vocabulary.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping

from scripts.hermes_runtime_validation.semantics.topology import LAYER_TRANSITIONS

ENVELOPE_KIND = "openxfactory-hermes-runtime-job-envelope-v2"
RUN_KIND = "openxfactory-hermes-runtime-job-run-v2"
EVENT_KIND = "openxfactory-hermes-runtime-job-event-v2"
RECORD_KINDS = frozenset({ENVELOPE_KIND, RUN_KIND, EVENT_KIND})

# Single-domain vocabulary that MUST NOT appear in a neutral job property name.
# Overlays carry these nouns in descriptive `extensions` only.
FORBIDDEN_DOMAIN_TOKENS = frozenset(
    {"project", "repository", "feature", "patient", "company"}
)

VALID_LAYER_STATES = frozenset(LAYER_TRANSITIONS)
TERMINAL_LAYER_STATES = frozenset({"suspended", "retired"})

SUPPORTED_OPERATIONS = frozenset(
    {"admit_new_job", "validate_job_correlation", "evaluate_retired_layer_evidence"}
)

EVIDENCE_FIELDS = ("event_refs", "artifact_refs", "approval_refs", "trace_refs")


def _finding(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _sorted(findings: list[Mapping[str, object]]) -> list[dict[str, str]]:
    return sorted(
        (dict(item) for item in findings),
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )


def _tokens(value: str) -> set[str]:
    return set(value.replace("-", "_").lower().split("_"))


def _scope_tuple(scope: object) -> tuple[str, str, str, str] | None:
    """Return the exact layer scope tuple, or None when it is not a layer scope."""

    if not isinstance(scope, Mapping) or scope.get("scope_kind") != "layer":
        return None
    values: list[str] = []
    for key in ("installation_id", "stack_id", "layer_id"):
        value = scope.get(key)
        if not isinstance(value, str) or not value:
            return None
        values.append(value)
    return ("layer", values[0], values[1], values[2])


def _domain_noun_findings(node: object, path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if isinstance(node, Mapping):
        for key, value in node.items():
            key_path = f"{path}.{key}" if path else str(key)
            if key == "extensions":
                # Namespaced descriptive overlay data may carry domain nouns.
                continue
            if _tokens(str(key)) & FORBIDDEN_DOMAIN_TOKENS:
                findings.append(
                    _finding(
                        "HGR-JOB-DOMAIN-NOUN",
                        key_path,
                        f"neutral job record must not encode domain noun {key!r}",
                    )
                )
            findings.extend(_domain_noun_findings(value, key_path))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            findings.extend(_domain_noun_findings(item, f"{path}[{index}]"))
    return findings


def _validate_single_record(record: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if _scope_tuple(record.get("owning_scope")) is None:
        findings.append(
            _finding(
                "HGR-JOB-SCOPE-MISSING",
                "owning_scope",
                "governed job record must carry a closed layer scope with exact "
                "installation, stack, and layer identity",
            )
        )
    findings.extend(_domain_noun_findings(record, ""))
    return findings


def _resource_scope(resource: object) -> tuple[str, str, str] | None:
    """Return the exact (installation, stack, layer) scope of a resource reference.

    Cross-layer source/target coordinates are only meaningful at full scope: a
    layer_id is unique only within a stack, so comparing layer_id alone would let
    a foreign installation or stack that reuses the string pass as in-scope.
    """

    if not isinstance(resource, Mapping):
        return None
    values: list[str] = []
    for key in ("installation_id", "stack_id", "layer_id"):
        value = resource.get(key)
        if not isinstance(value, str) or not value:
            return None
        values.append(value)
    return (values[0], values[1], values[2])


def _validate_cross_layer(
    job: Mapping[str, object], job_scope: tuple[str, str, str, str] | None
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    requirements = job.get("cross_layer_requirements", [])
    if not isinstance(requirements, list):
        return findings
    job_layer_scope = job_scope[1:] if job_scope is not None else None
    for index, requirement in enumerate(requirements):
        path = f"cross_layer_requirements[{index}]"
        if not isinstance(requirement, Mapping):
            findings.append(
                _finding(
                    "HGR-JOB-CROSS-LAYER",
                    path,
                    "cross-layer requirement must be a closed mapping",
                )
            )
            continue
        source = requirement.get("source_resource")
        target = requirement.get("target_resource")
        binding = requirement.get("binding_ref")
        source_scope = _resource_scope(source)
        target_scope = _resource_scope(target)
        valid = (
            job_layer_scope is not None
            # source must be the job's exact owning layer (installation, stack,
            # layer), not merely a matching layer_id in some other installation.
            and source_scope == job_layer_scope
            # target must share the job's installation and stack but be a
            # distinct layer -- an actual cross-layer edge within one stack.
            and target_scope is not None
            and target_scope[0] == job_layer_scope[0]
            and target_scope[1] == job_layer_scope[1]
            and target_scope[2] != job_layer_scope[2]
            and isinstance(binding, Mapping)
            and isinstance(binding.get("binding_id"), str)
            and bool(binding.get("binding_id"))
        )
        if not valid:
            findings.append(
                _finding(
                    "HGR-JOB-CROSS-LAYER",
                    path,
                    "cross-layer requirement must bind an in-scope source at the "
                    "job's exact installation, stack, and layer, a distinct target "
                    "layer within that same installation and stack, and an exact "
                    "binding reference",
                )
            )
    return findings


def _mappings(value: object) -> list[Mapping[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _validate_admission(payload: Mapping[str, object]) -> list[dict[str, str]]:
    job = payload.get("job")
    job = job if isinstance(job, Mapping) else {}
    job_scope = _scope_tuple(job.get("owning_scope"))
    if job_scope is None:
        return [
            _finding(
                "HGR-JOB-SCOPE-MISSING",
                "job.owning_scope",
                "new governed job must carry a closed layer scope before admission",
            )
        ]
    lifecycle = _mappings(payload.get("layer_lifecycle", []))
    match: Mapping[str, object] | None = None
    for entry in lifecycle:
        entry_scope = (
            str(entry.get("installation_id", "")),
            str(entry.get("stack_id", "")),
            str(entry.get("layer_id", "")),
        )
        if entry_scope == (job_scope[1], job_scope[2], job_scope[3]):
            match = entry
            break
    if match is None:
        return [
            _finding(
                "HGR-JOB-LAYER-UNKNOWN",
                "layer_lifecycle",
                "new governed job requires one exact registered layer lifecycle entry",
            )
        ]
    state = str(match.get("state", ""))
    if state not in VALID_LAYER_STATES:
        return [
            _finding(
                "HGR-JOB-LAYER-STATE",
                "layer_lifecycle",
                f"layer lifecycle state {state!r} is not a known state",
            )
        ]
    if state in TERMINAL_LAYER_STATES:
        return [
            _finding(
                "HGR-JOB-LAYER-TERMINAL",
                "layer_lifecycle",
                f"layer state {state!r} does not admit new governed jobs",
            )
        ]
    return _validate_single_record(job)


def _validate_correlation(payload: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    job = payload.get("job")
    job = job if isinstance(job, Mapping) else {}
    job_scope = _scope_tuple(job.get("owning_scope"))
    job_id = job.get("job_id")

    findings.extend(_validate_cross_layer(job, job_scope))

    known_run_ids: set[str] = set()
    for index, run in enumerate(_mappings(payload.get("runs", []))):
        run_id = run.get("run_id")
        if isinstance(run_id, str):
            known_run_ids.add(run_id)
        if _scope_tuple(run.get("owning_scope")) != job_scope:
            findings.append(
                _finding(
                    "HGR-JOB-SCOPE-MISMATCH",
                    f"runs[{index}].owning_scope",
                    "run scope must exactly match its owning job scope",
                )
            )
        if run.get("job_id") != job_id:
            findings.append(
                _finding(
                    "HGR-JOB-CORRELATION",
                    f"runs[{index}].job_id",
                    "run must correlate to the exact owning job",
                )
            )

    events_by_run: dict[str, list[tuple[int, Mapping[str, object]]]] = defaultdict(list)
    for index, event in enumerate(_mappings(payload.get("events", []))):
        if _scope_tuple(event.get("owning_scope")) != job_scope:
            findings.append(
                _finding(
                    "HGR-JOB-SCOPE-MISMATCH",
                    f"events[{index}].owning_scope",
                    "event scope must exactly match its job and run scope",
                )
            )
        if event.get("job_id") != job_id or event.get("run_id") not in known_run_ids:
            findings.append(
                _finding(
                    "HGR-JOB-CORRELATION",
                    f"events[{index}]",
                    "event must correlate to the exact job and a known run",
                )
            )
        events_by_run[str(event.get("run_id"))].append((index, event))

    for _run_id, entries in events_by_run.items():
        previous: int | None = None
        for index, event in entries:
            sequence = event.get("sequence")
            if (
                not isinstance(sequence, int)
                or isinstance(sequence, bool)
                or sequence < 0
            ):
                findings.append(
                    _finding(
                        "HGR-JOB-SEQUENCE",
                        f"events[{index}].sequence",
                        "event sequence must be a non-negative integer",
                    )
                )
                continue
            if previous is not None and sequence <= previous:
                findings.append(
                    _finding(
                        "HGR-JOB-SEQUENCE",
                        f"events[{index}].sequence",
                        "event sequence must strictly increase per run",
                    )
                )
            previous = sequence
    return findings


def _validate_retired_evidence(payload: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    run = payload.get("run")
    run = run if isinstance(run, Mapping) else {}
    available = _mappings(payload.get("available_evidence", []))
    required_refs: list[Mapping[str, object]] = []
    for field in EVIDENCE_FIELDS:
        for ref in _mappings(run.get(field, [])):
            required_refs.append(ref)
    summary = run.get("summary_ref")
    if isinstance(summary, Mapping):
        required_refs.append(summary)
    for ref in required_refs:
        if ref not in available:
            findings.append(
                _finding(
                    "HGR-JOB-EVIDENCE-DROPPED",
                    "available_evidence",
                    "retired-layer evidence "
                    f"{ref.get('resource_type')}:{ref.get('resource_id')} "
                    "must remain accessible",
                )
            )
    return findings


def validate_jobs_document(
    document: Mapping[str, object], *, evaluation_time: str
) -> list[dict[str, str]]:
    """Validate one jobs semantic document deterministically.

    Dispatches on the instance ``operation`` (admission, correlation, retired
    evidence) or, for a bare record, its v2 ``kind``. Unknown operations and
    documents fail closed. ``evaluation_time`` is accepted for API parity with
    the other semantic entrypoints; jobs semantics are time-independent.
    """

    del evaluation_time  # jobs semantics are pure and time-independent
    if not isinstance(document, Mapping):
        return [
            _finding(
                "HGR-JOB-OPERATION-UNKNOWN",
                "$",
                "jobs document must be a closed mapping",
            )
        ]
    operation = document.get("operation")
    if operation is not None:
        payload = document.get("input", {})
        payload = payload if isinstance(payload, Mapping) else {}
        if operation == "admit_new_job":
            return _sorted(_validate_admission(payload))
        if operation == "validate_job_correlation":
            return _sorted(_validate_correlation(payload))
        if operation == "evaluate_retired_layer_evidence":
            return _sorted(_validate_retired_evidence(payload))
        return [
            _finding(
                "HGR-JOB-OPERATION-UNKNOWN",
                "operation",
                f"unknown jobs operation {operation!r}",
            )
        ]
    if document.get("kind") in RECORD_KINDS:
        return _sorted(_validate_single_record(document))
    return [
        _finding(
            "HGR-JOB-OPERATION-UNKNOWN",
            "kind",
            "document is neither a known jobs operation nor a v2 job record",
        )
    ]
