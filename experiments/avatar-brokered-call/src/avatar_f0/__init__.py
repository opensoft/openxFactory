"""Avatar F0 brokered-call feasibility harness.

Disposable, tenant-data-free lab experiment (openxFactory change
``qualify-avatar-brokered-call-feasibility``). NOT for live/production use; a PASS
never qualifies a provider profile. See specs/002-avc-f0-feasibility/spec.md.
"""

__version__ = "0.1.0"
PROTOCOL_VERSION = "1"
CHANGE_ID = "qualify-avatar-brokered-call-feasibility"
INTERFACE_BASELINE = "avatar-client-parallel-v1"

# Terminal status vocabulary (fail-closed; closed set).
PASS = "PASS"
FAIL = "FAIL"
INCONCLUSIVE = "INCONCLUSIVE"
STATUSES = (PASS, FAIL, INCONCLUSIVE)

# The six authoritative trial groups and their planned counts (FR-006).
GROUP_PLANNED = {
    "F0-A": 20,  # baseline
    "F0-B": 10,  # delayed sideband
    "F0-C": 10,  # sideband failure (hosts the readiness-timeout path)
    "F0-D": 10,  # revocation
    "F0-E": 10,  # exact retry
    "F0-F": 10,  # changed retry
}
TOTAL_TRIALS = 70
