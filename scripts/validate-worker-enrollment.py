#!/usr/bin/env python3
"""Validate the worker-enrollment contract family (add-worker-enrollment-broker).

The openxFactory-owned canonical validator for the seven kinds
`worker_enrollment_request`, `worker_lease`, `worker_enrollment_grant`,
`worker_lease_renewal`, `worker_enrollment_policy`,
`worker_enrollment_audit_record`, and `worker_removal_grant`
(`contracts/worker-enrollment/*.schema.yaml`).
Run from the pinned openxFactory checkout, never copied into the broker service,
the host app, or a domain repo:

    python3 scripts/validate-worker-enrollment.py [REPO_PATH] [--strict]

Two layers run:

1. Packaged reference examples (`contracts/worker-enrollment/examples/`): every
   `*.example.yaml` must pass schema conformance AND every cross-shape rule;
   every file under `negative/` must FAIL for its INTENDED reason, declared in
   its own `# expected_failure:` header and optionally pinned further by an
   `# expected_failure_detail:` substring — because a finding CODE alone is too
   coarse an anchor for some rules (`schema` is satisfied by any schema error at
   all), so a fixture could keep passing its self-test while no longer testing
   the invariant it is named for. The self-test fails closed if a positive
   example fails or a negative stops failing for its reason (spec R10).
2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose `kind` is one of
   the seven family kinds is validated. Other kinds are skipped and counted; the
   packaged `examples/` tree is excluded, because the negatives there are
   deliberately invalid and layer 1 already asserts exactly how.

The rules the shapes cannot express (change task 1.9; rule (i), and rules (a), (b)
and (e) reaching `worker_removal_grant`, came with task 2.5's contract delta):

  (a) NO TOKEN OR SECRET ANYWHERE. No token/secret/key-shaped property may appear
      in any record or lease at any depth, and no value may carry a secret shape.
      Property names are matched against a token-name vocabulary; values are
      scanned against the shared `contracts/avatar-client/redaction/` denylist
      (bounded `SENTINEL_` forms exempt, the same reuse
      `scripts/validate-client-infrastructure.py` makes) plus a
      remove/registration-token entropy heuristic. The denylist is applied BY CLASS:
      `class: credential` (and the credential-shaped `jwt_token`) are errors,
      while the identifier-class patterns are advisory — an Intune device GUID
      really is a fleet `host_id` and an engineer UPN really is a subject `ref`,
      both legal by shape, so treating every denylist entry as a secret failed
      the family's own realistic records. CHUNKING is checked too: a token split
      across separators, across the items of an array, or across the entries of a
      bounded flag map defeats a per-value run test, so values are re-tested with
      separators removed and containers are re-tested concatenated. The ONLY
      exemptions are the two DECLARATION blocks — an enrollment grant's
      `registration_token` and a removal grant's `remove_token` — and a
      `.value` present inside either in a stored artifact is itself a finding,
      since that value is wire-only by contract (spec R2, R3, R9).
  (b) TEMP LEASES ARE SEGREGATED, AND SO ARE TEMP REMOVAL GRANTS. A temp-estate
      lease never names a standing execution-lane runner group, and neither does a
      temp-estate `worker_removal_grant` — whose `binding.runner_group` is the BLAST
      RADIUS of a remove token, so a standing group there is authority to deregister
      FLEET workers. The removal grant names the field exactly as the lease does so
      this rule needs no special case. With an enrollment policy in scope the check
      reads `standing_execution_lane_runner_groups` and `estates.temp.runner_group`
      from it. With NO policy in scope — the normal case for the host app and the
      broker checkouts, since the policy instance lives in the managed-platform
      repo — the fallback is an ALLOW-list on the group name (it must read as a
      temp/volunteer group), never a deny-list of today's standing group names,
      and the fallback always says so in a note (spec R8).
  (c) THE ESTATE PACKAGE SPLIT HOLDS. A fleet grant carries version + sha256 +
      self-update disabled; a temp grant carries no pin at all. With a policy in
      scope the fleet pin must MATCH the policy's declared package, not merely be
      present (spec R7).
  (d) EVERY RENEWAL RESPONSE CARRIES THE FLOOR — approvals included, because the
      renewal response is the only channel that reaches unmanaged hardware — and
      the floor must be MEANINGFUL: a zero floor is a finding wherever it appears
      (on a response or on a lease's `floor_in_force`), and a `source: policy`
      floor is checked against the declared per-estate floors of the policy it
      cites whenever that policy is in scope — presence alone let a broker
      regression zero or stale the control silently (spec R4, R5).
  (e) ESTATE, SUBJECT, HOST MANAGEMENT AND TRUST TIER AGREE. Relabelling one enum
      turned a volunteered laptop into a managed-fleet worker in the standing
      execution lane, with an audit record corroborating it. The schemas now
      couple the four fields; this rule is the second layer, and it also names
      the coupling for the estate the rule (b) segregation check keys off. It runs
      on all THREE shapes that carry the four facts — the lease, the audit record,
      and the removal grant (spec R1, R8).
  (f) THE RENEWAL EXCHANGE IS AUTHENTICATED, AND A DEVICE-CODE RENEWAL HOLDS NO
      STANDING SECRET. R1 extends the device-code identity to renewals and
      forbids escrow on the machine; a persisted refresh credential beside the
      lease is that escrow (spec R1).
  (g) LEASE EXPIRY MATCHES CADENCE, AND THE REGISTRATION TOKEN IS SHORT-LIVED.
      `expires_at` must be `issued_at` + `cadence.ttl` within the declared clock
      skew, and a grant's token lifetime must be positive and within both its own
      declaration and the policy ceiling — the bounds R2, R4 and R6 compute with
      (spec R2, R4, R6).
  (h) A STANDING EXECUTION LANE ACCEPTS NO VOLUNTEERED HARDWARE. The policy's
      lane declarations and its tier projections must agree with its own
      standing-group list (spec R8 scenario 3).
  (i) THE REMOVE TOKEN IS SHORT-LIVED TOO. `worker_removal_grant` (task 2.5's
      contract delta) declares the enrollment grant's transient discipline for a
      token of the SAME administration-tier authority pointed the other way, so it
      gets the same clock check: the `issued_at` -> `expires_at` span must be
      positive, within the grant's own declared `lifetime`, and within the
      contract's fifteen-minute ceiling. The registration token's hole — a 73-year
      "single-use" token that validated cleanly — was a real finding, and it would
      have reappeared verbatim on a shape whose bound nothing checked (spec R3).

Two consistency checks are reported as WARNINGS rather than errors (they are
cross-field readings, not contract rules): a renewal response that reports an
observed app version below its own floor while requiring no action, and a
`last_known` floor served on a response that is not a `policy_unavailable`
refusal. Identifier-class denylist matches outside reference fields warn too.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "worker-enrollment"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
REDACTION_DIR = ROOT / "contracts" / "avatar-client" / "redaction"

SCHEMA_FILENAMES = [
    "worker-enrollment-request.schema.yaml",
    "worker-lease.schema.yaml",
    "worker-enrollment-grant.schema.yaml",
    "worker-lease-renewal.schema.yaml",
    "worker-enrollment-policy.schema.yaml",
    "worker-enrollment-audit-record.schema.yaml",
    "worker-removal-grant.schema.yaml",
]

KIND_TO_SCHEMA = {
    "worker_enrollment_request": "worker-enrollment-request.schema.yaml",
    "worker_lease": "worker-lease.schema.yaml",
    "worker_enrollment_grant": "worker-enrollment-grant.schema.yaml",
    "worker_lease_renewal": "worker-lease-renewal.schema.yaml",
    "worker_enrollment_policy": "worker-enrollment-policy.schema.yaml",
    "worker_enrollment_audit_record": "worker-enrollment-audit-record.schema.yaml",
    "worker_removal_grant": "worker-removal-grant.schema.yaml",
}

# date/date-time enforced, not merely annotated.
FORMAT_CHECKER = FormatChecker()

# Rule (a), property side: names a token/secret/key could plausibly hide behind.
TOKEN_KEY_RX = re.compile(
    r"(?:^|_)(?:token|tokens|secret|secrets|password|passwd|pwd|credential|"
    r"credentials|apikey|api_key|key|keys|privatekey|pat|bearer|assertion|"
    r"signature|sas)(?:$|_)",
    re.IGNORECASE,
)
# The only legitimate token-shaped property NAMES in the family, all four of them
# DECLARATIONS ABOUT tokens and secrets rather than places one could sit: a
# grant's transient registration-token block, a removal grant's transient
# remove-token block (each block's `value` is checked separately), the policy's
# lifetime ceiling for the registration token, and a renewal's assertion that no
# standing secret was escrowed on the host. Each is an exact (kind, path) pair, so
# the exemption cannot widen to a sibling — a `registration_token` on a REMOVAL
# grant is a finding precisely because the pair is not in this set.
TOKEN_KEY_EXEMPT = {
    ("worker_enrollment_grant", "registration_token"),
    ("worker_enrollment_policy", "registration_token"),
    ("worker_removal_grant", "remove_token"),
    ("worker_lease_renewal", "request.authentication.standing_secret_on_host"),
}
# The transient-token DECLARATION block each issuance shape carries. Its `value` is
# `writeOnly` by contract — wire-only — so its presence in a stored, committed, or
# scanned artifact is a finding whatever the block is called (spec R2, R3).
TRANSIENT_TOKEN_PROPERTY = {
    "worker_enrollment_grant": "registration_token",
    "worker_removal_grant": "remove_token",
}

# Rule (a), value side: runs of the token alphabet. `/` and `.` and `:` are
# deliberately NOT run characters, so URLs and paths split into short segments
# instead of reading as one long opaque blob — the de-chunking pass below is what
# stops that leniency from being a smuggling channel.
RUN_RX = re.compile(r"[A-Za-z0-9+=_-]{28,}")
# Separators stripped before re-testing a value or a concatenation.
SEPARATORS = str.maketrans("", "", "._:/-")

# Denylist classes that are genuinely secrets. Identifier-class patterns are
# advisory: the family's `identifier` $def explicitly permits `@` (an engineer
# UPN) and a fleet `host_id` really is the Intune device GUID.
SECRET_CLASSES = {"credential", "sdp", "transcript", "raw_payload", "media"}
CREDENTIAL_SHAPED_IDENTIFIERS = {"jwt_token"}
# Keys whose value is a REFERENCE by contract; an identifier-class match there is
# the shape working as designed, not a leak.
REFERENCE_KEY_RX = re.compile(
    r"^(?:.*_)?(?:id|ids|ref|refs|name|owner|host|subject)$", re.IGNORECASE)

# Rule (b) fallback when no enrollment policy is in scope: an ALLOW-list, because
# a deny-list of today's standing group names silently retires itself the first
# time a group is added or renamed (`Default` and `xfactory-omnigent-workers` are
# both real standing lanes and neither reads as one).
TEMP_GROUP_RX = re.compile(r"temp|volunteer", re.IGNORECASE)
STANDING_GROUP_RX = re.compile(r"execution[ ._-]?lane|standing", re.IGNORECASE)

VERSION_RX = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")
DURATION_RX = re.compile(
    r"^(?P<sign>-?)PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?$")
# A long lowercase-hex blob is a digest where a digest belongs and an opaque
# secret anywhere else (the value heuristic deliberately ignores digests).
HEX_BLOB_RX = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{32,}(?![0-9a-fA-F])")
DIGEST_KEYS = {"sha256", "digest", "checksum", "fingerprint", "hash"}

# The contract pattern caps a declared token lifetime at 15 minutes; with no
# policy in scope that ceiling is what "short-lived" means for a registration
# token, and it is ALWAYS what it means for a remove token (spec R2, R3).
TOKEN_LIFETIME_CEILING_S = 15 * 60
NAME_SEGMENT_RX = re.compile(r"([A-Za-z0-9_]+)(?:\[\d+\])*$")


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline registry over all six schemas so the grant's cross-file `$ref`
    into `worker-lease.schema.yaml` resolves (the same approach
    scripts/validate-ideation-dashboard-contracts.py takes). Each schema is
    registered under BOTH its absolute `$id` and its filename, so the bundle
    resolves identically here and in a consumer's stock validator."""
    resources = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(CONTRACT_DIR / name)
        docs[name] = doc
        resource = Resource.from_contents(doc, default_specification=DRAFT202012)
        resources.append((name, resource))
        if doc.get("$id"):
            resources.append((doc["$id"], resource))
    return Registry().with_resources(resources), docs


def validator_for(kind: str, registry: Registry, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(
        docs[KIND_TO_SCHEMA[kind]], registry=registry, format_checker=FORMAT_CHECKER)


# --------------------------- shared parsing helpers ---------------------------

def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def parse_duration(value: Any) -> int | None:
    """ISO-8601 PT duration -> seconds (the only forms this family declares)."""
    if not isinstance(value, str):
        return None
    m = DURATION_RX.match(value)
    if not m:
        return None
    total = (int(m.group("h") or 0) * 3600 + int(m.group("m") or 0) * 60
             + int(m.group("s") or 0))
    return -total if m.group("sign") else total


def parse_version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    m = VERSION_RX.match(value)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


# --------------------------- secret-shape heuristics ---------------------------

@dataclass
class SecretScan:
    """Reuse the shared avatar-client redaction denylist + bounded sentinels
    rather than re-declaring secret patterns here (the reuse
    scripts/validate-client-infrastructure.py already makes)."""
    patterns: list[tuple[str, str, re.Pattern[str]]] = field(default_factory=list)
    allowed: set[str] = field(default_factory=set)


def load_secret_scan() -> SecretScan:
    scan = SecretScan()
    denylist = REDACTION_DIR / "denylist-patterns.yaml"
    sentinels = REDACTION_DIR / "sentinels.yaml"
    if denylist.is_file():
        for entry in (load_yaml(denylist) or {}).get("patterns") or []:
            scan.patterns.append(
                (entry["id"], entry.get("class", "unclassified"), re.compile(entry["regex"])))
    if sentinels.is_file():
        for entry in (load_yaml(sentinels) or {}).get("sentinels") or []:
            if entry.get("bounded_form"):
                scan.allowed.add(entry["bounded_form"])
    return scan


def token_shaped(value: str) -> str | None:
    """A registration/remove token is a long single run of the token alphabet
    carrying both digits and upper case (GitHub runner tokens are base32). Long
    lowercase-hex runs — sha256 digests — are deliberately NOT token-shaped."""
    for run in RUN_RX.findall(value):
        if any(c.isdigit() for c in run) and any(c.isupper() for c in run):
            return run
    return None


def chunked_token(value: str) -> str | None:
    """The same test with separators removed, per whitespace-delimited word: a
    token written `AABF...TS6.FCWO...HJ.TP7Q` passes a run test and reassembles
    with one `replace`, which is exactly how the negative fixture the family
    declares impossible-by-shape was reproduced."""
    for word in value.split():
        stripped = word.translate(SEPARATORS)
        if stripped != word:
            run = token_shaped(stripped)
            if run is not None:
                return run
    return None


def concatenated_token(values: list[str]) -> str | None:
    """Siblings joined: an array of key lines, or a bounded flag map whose
    entries each stay under the per-value run floor."""
    if len(values) < 2:
        return None
    joined = "".join(values).translate(SEPARATORS)
    return token_shaped(joined)


def key_of(loc: str) -> str:
    m = NAME_SEGMENT_RX.search(loc)
    return m.group(1) if m else loc


def walk(node: Any, path: str = "") -> Iterator[tuple[str, str | None, Any]]:
    """Yield (path, key, value) for every node, so both property NAMES and
    string VALUES can be judged."""
    if isinstance(node, dict):
        for k, v in node.items():
            here = f"{path}.{k}" if path else str(k)
            yield here, str(k), v
            yield from walk(v, here)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            here = f"{path}[{i}]"
            yield here, None, v
            yield from walk(v, here)


# --------------------------- rule (a): no token or secret ---------------------------

def _scan_value(f: Findings, label: str, loc: str, value: str, scan: SecretScan) -> None:
    if value in scan.allowed:
        return
    for pid, cls, rx in scan.patterns:
        if not rx.search(value):
            continue
        if cls in SECRET_CLASSES or pid in CREDENTIAL_SHAPED_IDENTIFIERS:
            f.error("embedded-secret",
                    f"{label}: {loc}: value matches secret pattern {pid!r} "
                    f"(class {cls}) — references only; bounded SENTINEL_ forms in "
                    f"fixtures")
            return
        if REFERENCE_KEY_RX.match(key_of(loc)):
            # A device GUID host_id and an engineer UPN ref are the contract's
            # own shapes; flagging them made the first real record fail CI.
            continue
        f.warn("identifier-in-record",
               f"{label}: {loc}: value matches identifier pattern {pid!r} outside "
               f"a reference field — this family carries references, not "
               f"high-cardinality identifiers in prose")
        return
    run = token_shaped(value) or chunked_token(value)
    if run is not None:
        f.error("embedded-secret",
                f"{label}: {loc}: value carries a registration- or remove-token shape "
                f"({len(run)}-character mixed-case token alphabet run, separators "
                f"removed) — token values live in no stored artifact (spec R2, R3)")


def _scan_containers(f: Findings, label: str, doc: dict, scan: SecretScan) -> None:
    """Chunking across SIBLINGS. Applied where a token could plausibly be split
    and the values are bounded by shape rather than by meaning: any array of
    strings, any `profiles` flag map, and every map inside a grant's
    broker-served `host_manifest.inline` — the one artifact the temp estate has
    no other delivery plane for."""
    for loc, _key, value in [("", None, doc), *walk(doc)]:
        inline = loc.startswith("host_manifest.inline")
        if isinstance(value, list):
            strings = [v for v in value if isinstance(v, str)]
            run = concatenated_token(strings) if len(strings) == len(value) else None
        elif isinstance(value, dict) and (key_of(loc) == "profiles" or inline):
            strings = [v for v in value.values() if isinstance(v, str)
                       and parse_dt(v) is None and parse_duration(v) is None]
            run = concatenated_token(strings)
        else:
            continue
        if run is not None:
            f.error("embedded-secret",
                    f"{label}: {loc or '<root>'}: the concatenation of this "
                    f"container's values carries a registration-token shape "
                    f"({len(run)} characters) — a token chunked across siblings is "
                    f"still a token in a stored artifact (spec R2, R9)")
        if inline:
            for k, v in (value.items() if isinstance(value, dict) else []):
                if isinstance(v, str) and k not in DIGEST_KEYS and HEX_BLOB_RX.search(v):
                    f.error("embedded-secret",
                            f"{label}: {loc}.{k}: opaque hex blob in a broker-served "
                            f"host manifest under a non-digest key — the temp estate's "
                            f"only delivery channel carries configuration, never "
                            f"material (spec R2)")


def check_no_token(f: Findings, label: str, kind: str, doc: dict, scan: SecretScan) -> None:
    for loc, key, value in walk(doc):
        if key is not None and TOKEN_KEY_RX.search(key) and (kind, loc) not in TOKEN_KEY_EXEMPT:
            f.error("token-in-record",
                    f"{label}: {loc}: token/secret-shaped property in a "
                    f"{kind} — no record or lease in this family has one, at any "
                    f"depth (spec R2, R9)")
        if isinstance(value, str):
            _scan_value(f, label, loc, value, scan)
    _scan_containers(f, label, doc, scan)
    prop = TRANSIENT_TOKEN_PROPERTY.get(kind)
    if prop:
        token = doc.get(prop)
        if isinstance(token, dict) and "value" in token:
            f.error("token-in-record",
                    f"{label}: {prop}.value: the transient token value is "
                    f"wire-only — no stored, committed, or scanned artifact may carry "
                    f"it (spec R2, R3)")


# --------------------------- rule (e): estate coherence ---------------------------

TEMP_SIGNALS = "estate temp / volunteered_hardware tier / engineer subject / unmanaged host"


def _estate_signals(doc: dict) -> tuple[str | None, list[str]]:
    """The four facts the estate is made of, read off a lease or an audit record."""
    estate = doc.get("estate")
    temp = []
    if doc.get("trust_tier") == "volunteered_hardware":
        temp.append("trust_tier=volunteered_hardware")
    subject = doc.get("subject") or {}
    if isinstance(subject, dict):
        if subject.get("class") == "engineer":
            temp.append("subject.class=engineer")
        if subject.get("authentication_mode") == "device_code":
            temp.append("subject.authentication_mode=device_code")
    host = doc.get("host") or {}
    if isinstance(host, dict) and host.get("managed") is False:
        temp.append("host.managed=false")
    return estate, temp


def check_estate_coherence(f: Findings, label: str, kind: str, doc: dict) -> None:
    """Rule (e). The schemas couple these fields now; this is the second layer,
    and it is the layer that explains the finding — because the whole bypass was
    that rule (b) keys off `estate`, so one relabelled enum turned a volunteered
    workstation into a managed-fleet worker in a standing lane with an audit
    record agreeing."""
    estate, temp = _estate_signals(doc)
    if estate == "fleet" and temp:
        f.error("estate-coherence",
                f"{label}: estate 'fleet' contradicts {', '.join(temp)} — the four "
                f"facts ({TEMP_SIGNALS}) are ONE fact, and the temp segregation "
                f"rule keys off the estate, so a mislabelled estate would carry "
                f"volunteered hardware into a standing lane (spec R1, R8)")
    if estate == "temp":
        if doc.get("trust_tier") not in (None, "volunteered_hardware"):
            f.error("estate-coherence",
                    f"{label}: estate 'temp' with trust_tier "
                    f"{doc.get('trust_tier')!r} — a volunteered workstation is "
                    f"volunteered hardware on the record (spec R8)")
        host = doc.get("host") or {}
        if isinstance(host, dict) and host.get("managed") is True:
            f.error("estate-coherence",
                    f"{label}: estate 'temp' with host.managed true — the temp "
                    f"estate is the unmanaged one (spec R1)")


# --------------------------- rule (b): temp segregation ---------------------------

def _is_temp_scoped(record: dict) -> bool:
    """Any temp-shaped fact puts the record in scope, not just the estate label:
    the segregation check must not be disarmable by relabelling one enum."""
    estate, temp = _estate_signals(record)
    return estate == "temp" or bool(temp)


def check_temp_segregation(f: Findings, label: str, record: dict, policy: dict | None) -> None:
    """Rule (b), over any record whose `binding.runner_group` is a GRANT of scope:
    a `worker_lease` (the group the worker executes in) and a `worker_removal_grant`
    (the group the remove token may deregister within). The removal grant names the
    field exactly as the lease does so that this rule reads both without a special
    case — and a remove token scoped to a standing execution lane is the larger
    hazard of the two, because it removes FLEET workers rather than adding a
    volunteered one."""
    if not isinstance(record, dict) or not _is_temp_scoped(record):
        return
    group = (record.get("binding") or {}).get("runner_group")
    if not isinstance(group, str):
        return  # shape failure; the schema layer reports it
    if policy is not None:
        standing = set(((policy.get("standing_execution_lane_runner_groups")) or []))
        temp_group = (((policy.get("estates") or {}).get("temp")) or {}).get("runner_group")
        if group in standing:
            f.error("temp-lease-in-standing-group",
                    f"{label}: binding.runner_group {group!r} is a standing "
                    f"execution-lane group declared by policy "
                    f"{policy.get('policy_version')!r} — a temp-estate lease BINDS, "
                    f"and a temp-estate removal grant SCOPES ITS REMOVE TOKEN TO, the "
                    f"dedicated temp group and never a standing one (spec R8)")
        elif isinstance(temp_group, str) and group != temp_group:
            f.error("temp-lease-in-standing-group",
                    f"{label}: binding.runner_group {group!r} is not the dedicated "
                    f"temp runner group {temp_group!r} declared by policy "
                    f"{policy.get('policy_version')!r} (spec R8)")
        return
    f.note("no worker_enrollment_policy in scope: rule (b) runs its NAMING "
           "FALLBACK (a temp lease must bind a group that reads as a temp or "
           "volunteer group). The policy instance lives in the managed-platform "
           "repo, so this is the normal case in a broker or host-app checkout — "
           "scan the policy alongside the leases to check declared facts instead")
    if not TEMP_GROUP_RX.search(group):
        f.error("temp-lease-in-standing-group",
                f"{label}: binding.runner_group {group!r} does not read as the "
                f"dedicated temp/volunteer group and no enrollment policy is in "
                f"scope to declare which groups are standing lanes — the fallback "
                f"is fail-closed on purpose, because a deny-list of today's "
                f"standing group names ('Default', 'xfactory-omnigent-workers') "
                f"catches neither (spec R8)")


# --------------------------- rule (c): estate package split ---------------------------

PIN_FIELDS = ("version", "sha256")


def check_package_split(f: Findings, label: str, grant: dict, policy: dict | None) -> None:
    lease = grant.get("lease")
    estate = lease.get("estate") if isinstance(lease, dict) else None
    pkg = grant.get("runner_package")
    if not isinstance(pkg, dict) or estate not in ("fleet", "temp"):
        return  # shape failure; the schema layer reports it
    if estate == "fleet":
        missing = [k for k in PIN_FIELDS if not pkg.get(k)]
        if pkg.get("mode") != "pinned":
            missing.append(f"mode=pinned (got {pkg.get('mode')!r})")
        if pkg.get("self_update") != "disabled":
            missing.append(f"self_update=disabled (got {pkg.get('self_update')!r})")
        if missing:
            f.error("fleet-grant-without-package-pin",
                    f"{label}: runner_package is missing {', '.join(missing)} — a "
                    f"fleet grant is hard-pinned with runner self-update disabled, "
                    f"and bumps ride manifest rollouts (spec R7)")
            return
        declared = (((policy or {}).get("estates") or {}).get("fleet") or {}).get("runner_package")
        if isinstance(declared, dict):
            drift = [f"{k}: grant {pkg.get(k)!r} vs policy {declared.get(k)!r}"
                     for k in ("version", "sha256", "platform")
                     if declared.get(k) and pkg.get(k) != declared.get(k)]
            if drift:
                f.error("fleet-grant-pin-contradicts-policy",
                        f"{label}: runner_package contradicts the package declared "
                        f"by policy {(policy or {}).get('policy_version')!r} "
                        f"({'; '.join(drift)}) — the pin's purpose is a known, "
                        f"digest-verified artifact, which presence alone does not "
                        f"establish (spec R7)")
    else:
        carried = [k for k in PIN_FIELDS if pkg.get(k)]
        if pkg.get("mode") == "pinned":
            carried.append("mode=pinned")
        if pkg.get("self_update") == "disabled":
            carried.append("self_update=disabled")
        if carried:
            f.error("temp-grant-carries-package-pin",
                    f"{label}: runner_package carries {', '.join(carried)} — a temp "
                    f"grant carries NO pin: the runner self-updates and the "
                    f"fail-closed control is the app-version floor (spec R7)")


# --------------------------- rules (g)/(i): token lifetime + lease cadence ---------------------------

def _check_token_span(
    f: Findings, label: str, token: dict, issued: datetime | None, ceiling: int,
    code: str, prop: str, issued_prop: str, spec: str,
) -> None:
    """The clock half of "short-lived" (spec R2, R3), shared by the two transient
    tokens this family issues. Kept as ONE function on purpose: the registration
    token's 73-year hole was found by a review, and a remove token that carried its
    own copy of this check would be free to drift out of step with the shape whose
    discipline it claims to mirror."""
    expires = parse_dt(token.get("expires_at"))
    declared = parse_duration(token.get("lifetime"))
    if issued is None or expires is None:
        return  # shape failure; the schema layer reports it
    actual = (expires - issued).total_seconds()
    if actual <= 0:
        f.error(code,
                f"{label}: {prop}.expires_at is at or before {issued_prop} — the "
                f"response ships an already-expired single-use token ({spec})")
        return
    if actual > ceiling:
        f.error(code,
                f"{label}: {prop} lives {int(actual)}s from {issued_prop}, past the "
                f"{ceiling}s ceiling — 'short-lived' is a bound this family declares, "
                f"not an adjective ({spec})")
    if declared is not None and actual > declared:
        f.error(code,
                f"{label}: {prop}.expires_at is {int(actual)}s after {issued_prop} "
                f"but the declared lifetime is {declared}s ({spec})")


def check_token_lifetime(f: Findings, label: str, grant: dict, policy: dict | None) -> None:
    """Rule (g), registration half: the policy declares the ESTATE ceiling, so it
    overrides the contract's pattern cap when a policy is in scope."""
    token = grant.get("registration_token")
    if not isinstance(token, dict):
        return  # shape failure; the schema layer reports it
    ceiling = parse_duration(
        (((policy or {}).get("registration_token")) or {}).get("max_lifetime")) \
        or TOKEN_LIFETIME_CEILING_S
    _check_token_span(
        f, label, token, parse_dt(grant.get("granted_at")), ceiling,
        "registration-token-not-short-lived", "registration_token", "granted_at",
        "spec R2 scenario 3")


def check_remove_token_lifetime(f: Findings, label: str, removal: dict) -> None:
    """Rule (i). The remove token's ceiling is the CONTRACT's fifteen-minute bound —
    the `short_lifetime` pattern both issuance shapes share. The policy's
    `registration_token.max_lifetime` is deliberately NOT read here: it is the
    estate's ceiling on ENROLLMENT tokens, and silently reusing it would let a
    policy edit widen an authority it never mentions."""
    token = removal.get("remove_token")
    if not isinstance(token, dict):
        return  # shape failure; the schema layer reports it
    _check_token_span(
        f, label, token, parse_dt(removal.get("issued_at")),
        TOKEN_LIFETIME_CEILING_S, "remove-token-not-short-lived", "remove_token",
        "issued_at", "spec R3 scenario 2")


def check_lease_floor(f: Findings, label: str, lease: dict) -> None:
    floor = (lease.get("floor_in_force") or {}).get("min_app_version")
    if parse_version(floor) == (0, 0, 0):
        f.error("floor-not-meaningful",
                f"{label}: floor_in_force.min_app_version is {floor!r} — the lease's "
                f"record of the floor it was told is the host-legible half of the "
                f"only control that reaches unmanaged hardware (spec R4, R5)")


def check_lease_cadence(f: Findings, label: str, lease: dict) -> None:
    issued = parse_dt(lease.get("issued_at"))
    expires = parse_dt(lease.get("expires_at"))
    cadence = lease.get("cadence") or {}
    ttl = parse_duration(cadence.get("ttl")) if isinstance(cadence, dict) else None
    skew = parse_duration(cadence.get("clock_skew_tolerance")) if isinstance(cadence, dict) else 0
    if issued is None or expires is None or ttl is None:
        return  # shape failure; the schema layer reports it
    actual = (expires - issued).total_seconds()
    if abs(actual - ttl) > max(skew or 0, 0):
        f.error("lease-expiry-inconsistent-with-ttl",
                f"{label}: expires_at is {int(actual)}s after issued_at but "
                f"cadence.ttl is {ttl}s — R4's 'TTL plus the declared grace window' "
                f"and R6's 'cadence plus grace' bound are computed from these two "
                f"fields, so they must not drift apart (spec R4, R6)")


# --------------------------- rule (d)/(f): the renewal exchange ---------------------------

def check_renewal(f: Findings, label: str, renewal: dict, policy: dict | None) -> None:
    request = renewal.get("request") or {}
    auth = request.get("authentication") if isinstance(request, dict) else None
    if isinstance(auth, dict):
        # Rule (f): R1 extends the device-code identity to renewals and forbids
        # escrow on the machine. A persisted refresh credential IS that escrow.
        if auth.get("mode") == "device_code" and auth.get("standing_secret_on_host") != "none":
            f.error("renewal-escrows-standing-secret",
                    f"{label}: request.authentication declares "
                    f"standing_secret_on_host "
                    f"{auth.get('standing_secret_on_host')!r} under device_code — a "
                    f"volunteer workstation holds NO standing secret at any point, "
                    f"so a refresh credential persisted beside the lease is a "
                    f"contract violation rather than an implementation choice "
                    f"(spec R1)")
    response = renewal.get("response")
    if not isinstance(response, dict):
        return
    floor = response.get("floor")
    min_version = floor.get("min_app_version") if isinstance(floor, dict) else None
    if not min_version:
        f.error("renewal-response-missing-floor",
                f"{label}: response carries no floor.min_app_version — the floor "
                f"travels on EVERY renewal response, approvals included, because it "
                f"is the only control that reaches unmanaged hardware (spec R4)")
        return
    source = floor.get("source")
    refusal = response.get("refusal_reason")
    if parse_version(min_version) == (0, 0, 0):
        f.error("floor-not-meaningful",
                f"{label}: response.floor.min_app_version is {min_version!r} — a "
                f"zero floor denies nothing, and the floor is the ONLY fail-closed "
                f"control that reaches unmanaged hardware, so a zeroed or defaulted "
                f"one is the control switched off rather than a permissive setting "
                f"(spec R4, R5)")
    # Only the policy the response CITES can adjudicate its floor: a response
    # carrying a raised floor at worker-enrollment-v2 is not contradicted by the
    # v1 instance that happens to be in the scan.
    cites_policy = policy is not None and \
        response.get("policy_version") == policy.get("policy_version")
    if source == "policy" and cites_policy:
        declared = {est.get("min_app_version")
                    for est in ((policy.get("estates") or {}).values())
                    if isinstance(est, dict)}
        declared.discard(None)
        if declared and min_version not in declared:
            f.error("renewal-floor-contradicts-policy",
                    f"{label}: response.floor.min_app_version {min_version!r} "
                    f"matches no per-estate floor declared by policy "
                    f"{policy.get('policy_version')!r} ({sorted(declared)}) — a "
                    f"floor whose presence is checked but whose value is not is a "
                    f"control a regression can zero out silently (spec R4)")
    elif source == "last_known" and refusal != "policy_unavailable":
        f.warn("floor-provenance",
               f"{label}: response serves a last_known floor on a response that is "
               f"not a policy_unavailable refusal — the floor reaching unmanaged "
               f"hardware should be the one the policy declares (spec R4)")
    observed = parse_version(((request or {}).get("observed") or {}).get("app_version"))
    wanted = parse_version(min_version)
    if observed and wanted and observed < wanted and response.get("required_action") == "none":
        f.warn("floor-consistency",
               f"{label}: observed app version is below the response floor "
               f"{min_version} yet required_action is 'none' — a below-floor worker "
               f"fails closed (spec R5)")


# --------------------------- rule (h): lane declarations ---------------------------

def check_policy_lanes(f: Findings, label: str, policy: dict) -> None:
    standing = set(policy.get("standing_execution_lane_runner_groups") or [])
    for i, lane in enumerate(policy.get("execution_lanes") or []):
        if not isinstance(lane, dict):
            continue
        if lane.get("runner_group") in standing and \
                "volunteered_hardware" in (lane.get("accepts_trust_tiers") or []):
            f.error("standing-lane-accepts-volunteered-hardware",
                    f"{label}: execution_lanes[{i}] {lane.get('lane_ref')!r} is bound "
                    f"to standing execution-lane group "
                    f"{lane.get('runner_group')!r} and accepts "
                    f"volunteered_hardware — the lane-side declaration must agree "
                    f"with the policy's own standing-group list (spec R8)")
        if lane.get("runner_group") not in standing and \
                STANDING_GROUP_RX.search(str(lane.get("runner_group"))):
            # An incomplete standing list is how segregation degrades quietly:
            # rule (b) reads that list as the authority, so a standing lane
            # missing from it is a lane a temp lease may legally bind.
            f.warn("standing-group-list-incomplete",
                   f"{label}: execution_lanes[{i}] runner group "
                   f"{lane.get('runner_group')!r} reads as a standing execution "
                   f"lane but is not in standing_execution_lane_runner_groups, "
                   f"which is the list the segregation rule reads (spec R8)")
    for i, tier in enumerate(policy.get("trust_tiers") or []):
        if not isinstance(tier, dict):
            continue
        if tier.get("id") == "volunteered_hardware" and \
                tier.get("runner_group_projection") in standing:
            f.error("standing-lane-accepts-volunteered-hardware",
                    f"{label}: trust_tiers[{i}] projects volunteered_hardware onto "
                    f"standing execution-lane group "
                    f"{tier.get('runner_group_projection')!r} (spec R8)")


# --------------------------- per-record validation ---------------------------

def validate_record(
    f: Findings, label: str, doc: Any, registry: Registry, docs: dict[str, dict],
    scan: SecretScan, policy: dict | None,
) -> None:
    if not isinstance(doc, dict):
        f.error("shape", f"{label}: document is not a mapping")
        return
    kind = doc.get("kind")
    if kind not in KIND_TO_SCHEMA:
        f.error("unknown-kind", f"{label}: kind {kind!r} is not a worker-enrollment kind")
        return
    for err in sorted(validator_for(kind, registry, docs).iter_errors(doc),
                      key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        f.error("schema", f"{label}: {loc}: {err.message}")
    # The cross-shape rules run REGARDLESS of schema outcome: a negative fixture
    # must fail for the rule it names, not merely for the first schema slip.
    check_no_token(f, label, kind, doc, scan)
    if kind == "worker_lease":
        check_estate_coherence(f, label, kind, doc)
        check_temp_segregation(f, label, doc, policy)
        check_lease_cadence(f, label, doc)
        check_lease_floor(f, label, doc)
    elif kind == "worker_enrollment_grant":
        lease = doc.get("lease") or {}
        check_estate_coherence(f, label, "worker_lease", lease)
        check_temp_segregation(f, label, lease, policy)
        check_lease_cadence(f, label, lease)
        check_lease_floor(f, label, lease)
        check_package_split(f, label, doc, policy)
        check_token_lifetime(f, label, doc, policy)
    elif kind == "worker_lease_renewal":
        check_renewal(f, label, doc, policy)
    elif kind == "worker_enrollment_audit_record":
        check_estate_coherence(f, label, kind, doc)
    elif kind == "worker_removal_grant":
        # The removal grant carries the four coupled estate facts AND a
        # `binding.runner_group` that is the remove token's blast radius, so it takes
        # rules (e) and (b) exactly as a lease does — plus rule (i), the clock check
        # its transient token declaration would otherwise only assert.
        check_estate_coherence(f, label, kind, doc)
        check_temp_segregation(f, label, doc, policy)
        check_remove_token_lifetime(f, label, doc)
    elif kind == "worker_enrollment_policy":
        check_policy_lanes(f, label, doc)


# --------------------------- layer 1: packaged examples ---------------------------

def expected_failure(path: Path) -> tuple[str, str | None]:
    """A negative fixture declares the finding CODE it exists to provoke and MAY
    pin it further with a substring. The detail matters: `schema` is satisfied by
    any schema error whatsoever and `token-in-record` by a token-named property
    anywhere at any depth, so without it a fixture can be mutated into testing
    nothing while its self-test stays green."""
    code = detail = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            code = line.split(":", 1)[1].strip()
        elif line.startswith("# expected_failure_detail:"):
            detail = line.split(":", 1)[1].strip()
    if code is None:
        raise SystemExit(f"negative fixture missing '# expected_failure:' header: {path}")
    return code, detail


def codes_of(findings: list[str]) -> set[str]:
    return {m.group(1) for m in (re.match(r"ERROR \[([^]]+)]", line) for line in findings) if m}


def lines_for(findings: list[str], code: str) -> list[str]:
    return [line for line in findings if line.startswith(f"ERROR [{code}]")]


def self_test(
    f: Findings, registry: Registry, docs: dict[str, dict], scan: SecretScan,
) -> None:
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return
    # The packaged policy example is the segregation authority for the whole
    # self-test: rule (b) checks declared facts rather than a naming heuristic.
    policy_path = EXAMPLES_DIR / "worker-enrollment-policy.example.yaml"
    policy = load_yaml(policy_path) if policy_path.is_file() else None
    if policy is None:
        f.error("examples-missing",
                "no packaged worker-enrollment-policy.example.yaml: rule (b) cannot "
                "self-test its declared-facts path")

    valid_ok = 0
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        local = Findings()
        validate_record(local, f"examples/{path.name}", load_yaml(path),
                        registry, docs, scan, policy)
        if local.errors:
            f.errors.extend(f"{line} [expected a valid example]" for line in local.errors)
        else:
            valid_ok += 1
        f.warnings.extend(local.warnings)

    neg_ok = fallback_ok = 0
    if not NEGATIVE_DIR.is_dir():
        f.error("examples-missing", f"{NEGATIVE_DIR} not found")
    else:
        for path in sorted(NEGATIVE_DIR.glob("*.yaml")):
            code, detail = expected_failure(path)
            doc = load_yaml(path)
            local = Findings()
            validate_record(local, f"examples/negative/{path.name}", doc,
                            registry, docs, scan, policy)
            if not local.errors:
                f.error("negative-should-fail",
                        f"negative/{path.name}: expected invalid, validated cleanly")
            elif code not in codes_of(local.errors):
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: expected finding {code!r}, got "
                        f"{sorted(codes_of(local.errors))}")
            elif detail and not any(detail in line for line in lines_for(local.errors, code)):
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: finding {code!r} fired but not for "
                        f"{detail!r} — the fixture no longer tests the invariant it "
                        f"is named for: {lines_for(local.errors, code)}")
            else:
                neg_ok += 1
            # Rule (b)'s NO-POLICY fallback is the operative check in every real
            # deployment (leases live in the broker and host-app repos, the policy
            # in the managed-platform repo), so it gets its own self-test rather
            # than riding the policy-present path.
            if code == "temp-lease-in-standing-group":
                bare = Findings()
                validate_record(bare, f"examples/negative/{path.name}", doc,
                                registry, docs, scan, None)
                if code in codes_of(bare.errors):
                    fallback_ok += 1
                else:
                    f.error("negative-wrong-reason",
                            f"negative/{path.name}: rule (b) finds this with a policy "
                            f"in scope but NOT through the no-policy naming fallback, "
                            f"which is the path a broker or host-app checkout actually "
                            f"runs")
    f.note(f"self-test: {valid_ok} valid example(s) confirmed valid, {neg_ok} negative "
           f"example(s) confirmed invalid for their intended reason (detail-pinned "
           f"where the code alone is too coarse), {fallback_ok} of them re-confirmed "
           f"through rule (b)'s no-policy fallback")


# --------------------------- layer 2: real artifacts ---------------------------

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}


def repo_scan(
    f: Findings, target: Path, registry: Registry, docs: dict[str, dict], scan: SecretScan,
) -> None:
    sweep = target.is_dir()
    files = sorted(list(target.rglob("*.yaml")) + list(target.rglob("*.yml"))) \
        if sweep else [target]
    records: list[tuple[str, dict]] = []
    checked = skipped = 0
    for path in files:
        parts = set(path.parts)
        if parts & SKIP_DIR_NAMES or EXAMPLES_DIR in path.parents:
            continue
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            # A whole-checkout sweep is not the place to adjudicate unrelated
            # YAML: a file that does not parse cannot carry a family kind. An
            # explicitly named file is a different matter.
            if sweep:
                skipped += 1
                continue
            f.error("yaml", f"{path}: parse failure: {exc}")
            continue
        if not isinstance(doc, dict) or doc.get("kind") not in KIND_TO_SCHEMA:
            skipped += 1
            continue
        checked += 1
        records.append((str(path.relative_to(target) if target.is_dir() else path), doc))
    # A policy instance found in the tree is the segregation authority for the
    # records found beside it.
    policies = [d for _, d in records if d.get("kind") == "worker_enrollment_policy"]
    policy = policies[0] if len(policies) == 1 else None
    if len(policies) > 1:
        f.note(f"{len(policies)} policy instances in scope; rule (b) cannot choose "
               f"between them and uses its naming fallback")
    for label, doc in records:
        validate_record(f, label, doc, registry, docs, scan, policy)
    f.note(f"repo scan ({target}): {checked} artifact(s) checked, {skipped} skipped "
           f"(not a worker-enrollment kind); packaged examples/ excluded (layer 1 owns "
           f"them). Zero real artifacts is normal pre-realization — instances live in "
           f"the broker, the host app, and the managed-platform policy repo")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-worker-enrollment: {len(f.errors)} error(s), {len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="repo checkout (or single file) to scan for real "
                         "worker-enrollment artifacts; omit to self-test only")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()

    if not CONTRACT_DIR.is_dir():
        print(f"ERROR {CONTRACT_DIR} not found", file=sys.stderr)
        return 2
    try:
        registry, docs = build_registry()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2

    f = Findings()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")
        if not doc.get("$schema") or not doc.get("$id"):
            f.error("schema-identity-missing",
                    f"{name}: every schema in this family declares its dialect "
                    f"($schema) and an absolute $id, so a consumer's stock validator "
                    f"resolves the bundle the same way this one does")
    scan = load_secret_scan()
    if not scan.patterns:
        f.note(f"no shared redaction denylist at {REDACTION_DIR}; rule (a) runs on "
               f"property names and the token-shape heuristics only")

    try:
        self_test(f, registry, docs, scan)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, registry, docs, scan)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
