"""The auto-detection wiring the recorded rollback policy presupposes (task 6.3.3).

The policy names §6.3.3 as its `detection_wiring_owner` for ROLLBACK-A and
ROLLBACK-B alike. This module is that owner. It holds TWO trips and nothing
else; the ACT each trip fires is ``rollback.decide`` plus the runtime's
existing kill switch, and no terminal or switch is invented here.

TRIP 1 — LATENCY, firing ROLLBACK-B (auto-block-new, in-flight legs drain).
Evaluates incoming AVC-10 samples against ALV-SLO-001. Three refusals, all of
which mean "does not trip", stack on top of each other:

* **Not a gated cell.** Only `p50` and `p95`, only
  `first_playable_after_authorized_ms` and `sideband_ready_after_request_ms`,
  only `windows_desktop` and `web_canvas`, only `network_class: nominal`. The
  recorded-not-gated tier is evaluated and recorded, never gated — a
  comparison that CLAIMS the gated tier from one of those cells is refused,
  and the refusal attaches to the claim, not to the cell.
* **Under the declared minimum.** `latency-sample-minimum.yaml` declares
  `n_min: 100` per cell, BEFORE any measuring run, and `under_minimum.effect:
  recorded_not_gated`. AN UNDER-SAMPLED CELL NEVER TRIPS. At n=30 a p95
  estimate is a maximum wearing a percentile's name, and auto-blocking a ring
  on one would be auto-blocking on noise.
* **Incomplete or malformed comparison.** A cell with only one of the two
  reference classifications has nothing to compare; a sample with a
  non-integer, negative or absent `value_ms` is not a measurement. Both are
  refused as evidence rather than evaluated, exactly as the SLO's own
  `comparison_cell` note refuses a comparison whose sides do not match.

MATERIALITY is ALV-SLO-001's ruled rule, unchanged: a governed-adapter
percentile is a material regression when it exceeds the same-cell
direct-provider reference by more than 15 percent relative OR more than 150
milliseconds absolute, WHICHEVER IS GREATER — adapter > reference +
max(0.15 x reference, 150).

TRIP 2 — SAFETY EVALUATION, firing ROLLBACK-A (auto-abort WITH active-lease
revocation through the landed consent-withdraw terminal path).
§6.2.1's synthetic evaluation corpus DOES NOT EXIST YET — that task is
unticked — so what this module defines is the INPUT SEAM the corpus will feed:
:class:`SafetyEvalSignal`, whose `trigger` must be one of ROLLBACK-A's eight
ruled triggers. The seam is wired FAIL-CLOSED IN THE DETECTOR'S DIRECTION: an
absent signal, a malformed signal, a foreign object, or an unrecognised
trigger NEVER trips. That is the safe direction for an automatic abort — a
detector that fired on garbage would revoke live leases on a parse error,
which is precisely the harm ROLLBACK-B's `revoke_active_leases: false` was
ruled to avoid on a merely performance-shaped condition.

An absent signal is not evidence of safety, and this module does not claim it
is. It reports :attr:`SafetyVerdict.REFUSED_ABSENT`, which is a distinct value
from :attr:`SafetyVerdict.NO_TRIP_PASSED`, so a ring operator can tell "the
evaluation ran and passed" from "no evaluation arrived" — and the second is a
gate condition for the canary, not a green light.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional

from .rollback import CLASS_TRIGGERS, RollbackClass


# --------------------------------------------------------------------------- #
# ALV-SLO-001 and latency-sample-minimum.yaml — the pinned values
# --------------------------------------------------------------------------- #
RELATIVE_THRESHOLD_PCT = 15
ABSOLUTE_THRESHOLD_MS = 150

GATED_PERCENTILES = ("p50", "p95")
GATED_INTERVALS = frozenset(
    {"first_playable_after_authorized_ms", "sideband_ready_after_request_ms"}
)
GATED_PLATFORMS = frozenset({"windows_desktop", "web_canvas"})
GATED_NETWORK_CLASS = "nominal"

REFERENCE_CLASSIFICATION = "direct_provider_reference"
ADAPTER_CLASSIFICATION = "governed_adapter"

#: Declared 2026-08-27, BEFORE any measuring run (§7.5, feeding §5.2).
DECLARED_SAMPLE_MINIMUM = 100

#: The task that owns the safety-evaluation corpus this trip's seam consumes.
#: It is UNBUILT, and the seam says so rather than implying a corpus exists.
SAFETY_CORPUS_OWNER = "qualify-avatar-live-voice 6.2.1"

#: ROLLBACK-A's eight ruled triggers, READ FROM `rollback.CLASS_TRIGGERS`
#: rather than restated, so the detector and the act cannot drift apart.
SAFETY_TRIGGERS = CLASS_TRIGGERS[RollbackClass.A]


# --------------------------------------------------------------------------- #
# Trip 1 — latency
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class LatencySample:
    """One AVC-10 voice-latency sample — THE LATENCY TRIP'S INPUT SEAM.

    `region` participates in the SLO's `comparison_cell.must_match` and is
    carried even though the declared sampling cells do not axis on it, so a
    comparison across two regions is refused rather than silently pooled.
    """

    platform: str
    network_class: str
    region: Optional[str]
    reference_classification: str
    interval: str
    value_ms: int


class CellVerdict(Enum):
    GATED_PASS = "gated_pass"
    GATED_MATERIAL_REGRESSION = "gated_material_regression"
    RECORDED_NOT_GATED_UNDER_MINIMUM = "recorded_not_gated_under_minimum"
    REFUSED_NOT_A_GATED_CELL = "refused_not_a_gated_cell"
    REFUSED_INCOMPLETE_COMPARISON = "refused_incomplete_comparison"


#: The verdicts that are allowed to trip ROLLBACK-B. Exactly one value.
TRIPPING_VERDICTS = frozenset({CellVerdict.GATED_MATERIAL_REGRESSION})


@dataclass(frozen=True)
class CellComparison:
    platform: str
    network_class: str
    region: Optional[str]
    interval: str
    percentile: str
    reference_n: int
    adapter_n: int
    reference_ms: Optional[int]
    adapter_ms: Optional[int]
    threshold_ms: Optional[int]
    verdict: CellVerdict

    @property
    def trips(self) -> bool:
        return self.verdict in TRIPPING_VERDICTS

    def evidence_line(self) -> str:
        return (
            f"{self.platform}/{self.network_class}/{self.interval}/{self.percentile} "
            f"ref_n={self.reference_n} adapter_n={self.adapter_n} "
            f"ref={self.reference_ms} adapter={self.adapter_ms} "
            f"threshold={self.threshold_ms} -> {self.verdict.value}"
        )


@dataclass(frozen=True)
class LatencyEvaluation:
    comparisons: tuple[CellComparison, ...]
    malformed_samples: int
    declared_minimum: int

    @property
    def trips(self) -> tuple[CellComparison, ...]:
        return tuple(c for c in self.comparisons if c.trips)

    @property
    def tripped(self) -> bool:
        return bool(self.trips)


def _sample_is_wellformed(sample: object) -> bool:
    for attr in ("platform", "network_class", "reference_classification", "interval"):
        value = getattr(sample, attr, None)
        if not isinstance(value, str) or not value:
            return False
    region = getattr(sample, "region", "")
    if region is not None and not isinstance(region, str):
        return False
    value_ms = getattr(sample, "value_ms", None)
    if isinstance(value_ms, bool) or not isinstance(value_ms, int) or value_ms < 0:
        return False
    return True


def _percentile_ms(sorted_values: list[int], percentile: str) -> Optional[int]:
    """Nearest-rank percentile — deterministic, no interpolation.

    Nearest rank is chosen over an interpolating estimator because the whole
    suite is a determinism proof: an interpolated p95 depends on the estimator
    a reader happens to use, and two readers disagreeing about whether a gate
    tripped is worse than a slightly coarser estimate at n>=100.
    """
    n = len(sorted_values)
    if n == 0:
        return None
    pct = {"p50": 50, "p95": 95, "p99": 99}.get(percentile)
    if pct is None:
        return None
    rank = -((-pct * n) // 100)  # ceil(pct * n / 100)
    rank = min(max(rank, 1), n)
    return sorted_values[rank - 1]


def materiality_threshold_ms(reference_ms: int) -> int:
    """reference + max(15% of reference, 150 ms) — the ruled `greater_of` rule."""
    relative = (reference_ms * RELATIVE_THRESHOLD_PCT) // 100
    return reference_ms + max(relative, ABSOLUTE_THRESHOLD_MS)


def _is_gated_cell(platform: str, network_class: str, interval: str) -> bool:
    return (
        platform in GATED_PLATFORMS
        and network_class == GATED_NETWORK_CLASS
        and interval in GATED_INTERVALS
    )


def evaluate_latency(
    samples: Iterable[object], *, minimum: int = DECLARED_SAMPLE_MINIMUM
) -> LatencyEvaluation:
    """Evaluate AVC-10 samples against ALV-SLO-001. NEVER raises.

    A detector that raises on bad input is a detector that stops detecting, so
    every malformed sample is counted and dropped and the run continues on the
    samples that are measurements.
    """
    buckets: dict[tuple, dict[str, list[int]]] = {}
    malformed = 0
    for sample in samples:
        if not _sample_is_wellformed(sample):
            malformed += 1
            continue
        classification = sample.reference_classification
        if classification not in (REFERENCE_CLASSIFICATION, ADAPTER_CLASSIFICATION):
            malformed += 1
            continue
        key = (sample.platform, sample.network_class, sample.region, sample.interval)
        sides = buckets.setdefault(key, {REFERENCE_CLASSIFICATION: [], ADAPTER_CLASSIFICATION: []})
        sides[classification].append(sample.value_ms)

    comparisons: list[CellComparison] = []
    for key in sorted(buckets, key=lambda k: tuple("" if p is None else str(p) for p in k)):
        platform, network_class, region, interval = key
        sides = buckets[key]
        reference = sorted(sides[REFERENCE_CLASSIFICATION])
        adapter = sorted(sides[ADAPTER_CLASSIFICATION])
        for percentile in GATED_PERCENTILES:
            comparisons.append(
                _compare_cell(
                    platform, network_class, region, interval, percentile,
                    reference, adapter, minimum,
                )
            )
    return LatencyEvaluation(
        comparisons=tuple(comparisons),
        malformed_samples=malformed,
        declared_minimum=minimum,
    )


def _compare_cell(
    platform: str,
    network_class: str,
    region: Optional[str],
    interval: str,
    percentile: str,
    reference: list[int],
    adapter: list[int],
    minimum: int,
) -> CellComparison:
    reference_n, adapter_n = len(reference), len(adapter)
    base = dict(
        platform=platform,
        network_class=network_class,
        region=region,
        interval=interval,
        percentile=percentile,
        reference_n=reference_n,
        adapter_n=adapter_n,
    )
    if not _is_gated_cell(platform, network_class, interval):
        # Recorded, not gated. The refusal attaches to a claim of the gated
        # tier, not to the cell, so the numbers are still computed and carried.
        return CellComparison(
            reference_ms=_percentile_ms(reference, percentile),
            adapter_ms=_percentile_ms(adapter, percentile),
            threshold_ms=None,
            verdict=CellVerdict.REFUSED_NOT_A_GATED_CELL,
            **base,
        )
    if reference_n == 0 or adapter_n == 0:
        return CellComparison(
            reference_ms=_percentile_ms(reference, percentile),
            adapter_ms=_percentile_ms(adapter, percentile),
            threshold_ms=None,
            verdict=CellVerdict.REFUSED_INCOMPLETE_COMPARISON,
            **base,
        )
    if reference_n < minimum or adapter_n < minimum:
        # Insufficient n refuses the CLAIM, not the cell: recorded, not gated.
        return CellComparison(
            reference_ms=_percentile_ms(reference, percentile),
            adapter_ms=_percentile_ms(adapter, percentile),
            threshold_ms=None,
            verdict=CellVerdict.RECORDED_NOT_GATED_UNDER_MINIMUM,
            **base,
        )
    reference_ms = _percentile_ms(reference, percentile)
    adapter_ms = _percentile_ms(adapter, percentile)
    if reference_ms is None or adapter_ms is None:
        return CellComparison(
            reference_ms=reference_ms,
            adapter_ms=adapter_ms,
            threshold_ms=None,
            verdict=CellVerdict.REFUSED_INCOMPLETE_COMPARISON,
            **base,
        )
    threshold = materiality_threshold_ms(reference_ms)
    verdict = (
        CellVerdict.GATED_MATERIAL_REGRESSION
        if adapter_ms > threshold
        else CellVerdict.GATED_PASS
    )
    return CellComparison(
        reference_ms=reference_ms,
        adapter_ms=adapter_ms,
        threshold_ms=threshold,
        verdict=verdict,
        **base,
    )


# --------------------------------------------------------------------------- #
# Trip 2 — safety evaluation
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class SafetyEvalSignal:
    """THE SAFETY TRIP'S INPUT SEAM — the shape a §6.2.1 run will feed.

    `corpus_ref` names the synthetic corpus the verdict came from. It is
    required and must be non-empty: a safety verdict with no corpus behind it
    cannot be re-run by anyone reading the record, and an unreproducible
    verdict must not revoke live leases.
    """

    run_id: str
    corpus_ref: str
    scenario_class: str
    trigger: str
    verdict: str  # "pass" | "fail"
    finding: str = ""


PASS_VERDICT = "pass"
FAIL_VERDICT = "fail"


class SafetyVerdict(Enum):
    TRIPPED = "tripped"
    #: The evaluation ran and passed. Distinct from REFUSED_ABSENT on purpose.
    NO_TRIP_PASSED = "no_trip_passed"
    #: No signal arrived. NOT evidence of safety — a canary gate condition.
    REFUSED_ABSENT = "refused_absent"
    #: A signal arrived that is not a usable evaluation result.
    REFUSED_MALFORMED = "refused_malformed"
    #: A well-formed signal naming a trigger ROLLBACK-A does not recognise.
    REFUSED_UNKNOWN_TRIGGER = "refused_unknown_trigger"


#: The one verdict allowed to fire an automatic abort with lease revocation.
SAFETY_TRIPPING_VERDICTS = frozenset({SafetyVerdict.TRIPPED})


@dataclass(frozen=True)
class SafetyDecision:
    verdict: SafetyVerdict
    trigger: Optional[str]
    run_id: Optional[str]
    corpus_ref: Optional[str]
    detail: str

    @property
    def trips(self) -> bool:
        return self.verdict in SAFETY_TRIPPING_VERDICTS


def evaluate_safety_signal(signal: object) -> SafetyDecision:
    """Read a safety-evaluation signal. NEVER raises, and fails closed.

    "Fails closed" for an ABORT detector means it does not fire: absent,
    malformed, foreign, or unknown-trigger input yields a non-tripping verdict
    that says which of those it was. Revoking active leases on a parse error
    would spend the safety mechanism on a data problem.
    """
    if signal is None:
        return SafetyDecision(
            SafetyVerdict.REFUSED_ABSENT, None, None, None,
            "no safety-evaluation signal arrived; absence is not a pass",
        )
    run_id = getattr(signal, "run_id", None)
    corpus_ref = getattr(signal, "corpus_ref", None)
    scenario_class = getattr(signal, "scenario_class", None)
    trigger = getattr(signal, "trigger", None)
    verdict = getattr(signal, "verdict", None)
    for name, value in (
        ("run_id", run_id),
        ("corpus_ref", corpus_ref),
        ("scenario_class", scenario_class),
        ("trigger", trigger),
        ("verdict", verdict),
    ):
        if not isinstance(value, str) or not value.strip():
            return SafetyDecision(
                SafetyVerdict.REFUSED_MALFORMED,
                trigger if isinstance(trigger, str) else None,
                run_id if isinstance(run_id, str) else None,
                corpus_ref if isinstance(corpus_ref, str) else None,
                f"safety signal field {name!r} missing or not a non-empty string",
            )
    if verdict not in (PASS_VERDICT, FAIL_VERDICT):
        return SafetyDecision(
            SafetyVerdict.REFUSED_MALFORMED, trigger, run_id, corpus_ref,
            f"verdict must be {PASS_VERDICT!r} or {FAIL_VERDICT!r}, got {verdict!r}",
        )
    if trigger not in SAFETY_TRIGGERS:
        return SafetyDecision(
            SafetyVerdict.REFUSED_UNKNOWN_TRIGGER, trigger, run_id, corpus_ref,
            f"{trigger!r} is not one of ROLLBACK-A's recorded triggers",
        )
    if verdict == PASS_VERDICT:
        return SafetyDecision(
            SafetyVerdict.NO_TRIP_PASSED, trigger, run_id, corpus_ref,
            "safety evaluation passed",
        )
    return SafetyDecision(
        SafetyVerdict.TRIPPED, trigger, run_id, corpus_ref,
        f"safety evaluation failed on {trigger}",
    )
