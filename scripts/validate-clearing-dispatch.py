#!/usr/bin/env python3
"""Validate the `clearing` contract family — the neutral clearing-dispatch boundary.

The openxFactory-owned canonical validator for the six kinds
`xfactory_sealed_bundle_manifest`,
`xfactory_clearing_permitted_operations_registry`,
`xfactory_clearing_operation_report`,
`xfactory_clearing_deliberation_return`,
`xfactory_clearing_dispatch_record` and
`xfactory_clearing_single_door_attestation`
(`contracts/clearing/*.schema.yaml`). Run from the pinned openxFactory checkout,
never copied into a domain repo:

    python3 scripts/validate-clearing-dispatch.py [REPO_PATH] [--strict]

REALIZATION of the RATIFIED change `add-clearing-dispatch-boundary` (PR #555,
squash `ab0bb2dd`, merged 2026-09-02), capability `clearing-dispatch-boundary`,
tasks.md 6.7 — as MODIFIED by `add-cpc-clearing-boundary` (merged `c0270d28`),
whose two tightenings this file enforces: field (10) is a REQUIRED ORIGIN
SIGNATURE where the originating repository holds an active row in the neutral
factory-identity register, and the POLICY-CHECKED FIELDS ARE RESOLVED FROM the
closed permitted-operations register rather than read from the bundle.

TWO LAYERS RUN.

1. THE PACKAGED CORPUS (`contracts/clearing/examples/`). Every `*.example.yaml`
   must validate clean; every file under `negative/` must FAIL for the INTENDED
   reason declared in its own `# expected_failure:` header, optionally pinned
   further by an `# expected_failure_detail:` substring. Every member of the
   CLOSED refusal set must be red-proven by at least one fixture, or the run
   reports `clearing-refusal-code-without-probe` — a refusal nobody has seen fire
   is a refusal nobody has tested.

2. OPTIONAL REAL ARTIFACTS under REPO_PATH: every `*.y*ml` whose top-level
   `kind` is one of the six family kinds is validated. The packaged examples
   tree is excluded, because layer 1 already adjudicates exactly how each of
   those fails. ZERO REAL ARTIFACTS IS THE EXPECTED STATE until a clearing
   implementation writes its first neutral record — `opensoft/xFactory`'s
   clearing lane emits `clearing.*=` key-value ledger lines today — and zero is
   reported as a NOTE rather than as a pass with nothing behind it.

WHAT THIS FILE DERIVES: NOTHING OF ITS OWN.

  * The digest construction is `signed-execution-chain`'s
    `scripts/signed_execution_chain/canonical.py` — one construction, one
    implementation. The subject `sealed_bundle_manifest` was admitted to THAT
    family's closed enumeration at tranche three; this family declares none.
  * Signature verification is that same family's
    `scripts/signed_execution_chain/ed25519.py`.
  * Public-key DECODING and the fingerprint spelling come from the PINNED
    openXwallet reader, imported rather than copied, exactly as
    `scripts/validate-factory-identity.py` does — and this program REFUSES,
    rather than falling back to arithmetic of its own, when the gitlink is
    absent. One derivation, one place.

WHAT THIS FILE DELIBERATELY DOES NOT DO.

  * IT DOES NOT CONTACT A PROVIDER API. Provider-side resolution is the CLEARING
    IMPLEMENTATION's obligation. What the neutral validator checks is that a
    record CARRIES the resolved value beside the claimed one, and that a
    policy-checked field is never reported as provider-verified.
  * IT DOES NOT EVALUATE REVOCATION AT THE MOMENT OF CLEARING. The
    factory-identity register declares that unrealizable until a projection path
    exists, and any statement to the contrary is refused by that capability's own
    scenario. The declared staleness bound is read and reported as a note.
  * IT DOES NOT VERIFY A SEALED RETURN. No return shape ships in this family.

THE CLOSED REGISTER'S CLOSURE IS ENFORCED HERE, AND THE LIMIT IS STATED. JSON
Schema constrains a document; it cannot constrain a decision. So the ratified
member set is a frozen constant below and an instance member outside it is
refused. That refusal is a TRIPWIRE — this file, the register and the test that
pins it share a repository with the changes they police, so one diff can edit
every side. What it guarantees is that an addition cannot be made SILENTLY. It is
backed by review of any diff touching either, and it is not an unforgeable
refusal.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError as exc:  # pragma: no cover - environment failure
    print(f"ERROR jsonschema/referencing unavailable: {exc}", file=sys.stderr)
    raise SystemExit(2)

try:  # the format checker must actually check date-time, or `expires_at` is prose
    import rfc3339_validator  # noqa: F401
except ImportError:  # pragma: no cover - environment failure
    print("ERROR rfc3339-validator is not importable; `format: date-time` would "
          "be advisory and an expiry check would be reading prose",
          file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.signed_execution_chain import canonical, ed25519  # noqa: E402

CONTRACT_DIR = ROOT / "contracts" / "clearing"
EXAMPLES = CONTRACT_DIR / "examples"
NEGATIVES = EXAMPLES / "negative"
REGISTRY_INSTANCE = CONTRACT_DIR / "permitted-operations.registry.yaml"
FIXTURE_IDENTITY = EXAMPLES / "factory-identity-fixture"
LIVE_IDENTITY = ROOT / "governance" / "factory-identity"
PINNED_READER = ROOT / "openXwallet" / "scripts" / "validate-openxwallet.py"

SCHEMA_FILENAMES = (
    "sealed-bundle-manifest.schema.yaml",
    "permitted-operations.schema.yaml",
    "operation-report.schema.yaml",
    "deliberation-return.schema.yaml",
    "dispatch-record.schema.yaml",
    "single-door-attestation.schema.yaml",
)

#: A RECORD IS ROUTED TO ITS SCHEMA BY ITS `kind`, AND AN UNROUTED KIND IS NOT
#: VALIDATED LOOSELY — IT IS NOT VALIDATED AT ALL. `validate_record` below does
#: `KIND_TO_SCHEMA.get(kind)` and returns immediately on `None`, so a row missing
#: here is a shape nothing checks and a verdict scan nothing reaches.
KIND_TO_SCHEMA = {
    "xfactory_sealed_bundle_manifest": "sealed-bundle-manifest.schema.yaml",
    "xfactory_clearing_permitted_operations_registry": "permitted-operations.schema.yaml",
    "xfactory_clearing_operation_report": "operation-report.schema.yaml",
    "xfactory_clearing_deliberation_return": "deliberation-return.schema.yaml",
    "xfactory_clearing_dispatch_record": "dispatch-record.schema.yaml",
    "xfactory_clearing_single_door_attestation": "single-door-attestation.schema.yaml",
}

#: THE TEN DECLARED FIELDS, in the ratified order. The completeness rule names a
#: missing one rather than reporting "a required property is absent", because the
#: ratified scenario asks for the FIELD to be named.
DECLARED_FIELDS = (
    "origin",
    "source_commit",
    "job",
    "selected_files",
    "operation",
    "worker_profile",
    "lane",
    "output_schema_ref",
    "data_handling",
    "origin_attestation",
)

#: THE RATIFIED MEMBER SET of the closed permitted-operations register. TWO
#: members: `readiness-diagnostic`, register entry number one
#: (`add-clearing-dispatch-boundary`, ratified 2026-09-01), and `deliberation`,
#: register entry number two (`admit-deliberation-clearing-operation`, ratified
#: 2026-09-04, merged `3cf917b7`).
#:
#: `coding` is the next real LATER GOVERNED CHANGE and is deliberately absent —
#: `add-clearing-dispatch-boundary` design D11 names it, the estate already holds
#: its lane and its grandfathered worker, and
#: `examples/negative/register-carrying-an-unratified-operation.yaml` uses it as
#: the fixture that proves this refusal fires. Adding a name here without the
#: spec delta that ratifies it is the self-service widening the closed register
#: exists to end.
#:
#: THIS IS COPY 1 OF FIVE. The others are the INDEPENDENT constant in
#: `tests/clearing/test_register_closure.py`, the register instance itself,
#: `.github/workflows/clearing-dispatch-gate.yml`'s literal member-count grep,
#: and the test that pins that grep from a second file. Do not import one from
#: another: the independence is the control.
RATIFIED_OPERATIONS = frozenset({"readiness-diagnostic", "deliberation"})

#: The digest subject this family's manifest is admitted under, in
#: `signed-execution-chain`'s closed enumeration.
MANIFEST_SUBJECT = "sealed_bundle_manifest"

#: The NAME ALLOWLIST for the operation report's environment echo. Held here as
#: well as in the schema so a widening of one without the other is a finding
#: rather than a silent divergence.
ENVIRONMENT_ALLOWLIST = frozenset({
    "RUNNER_NAME", "RUNNER_OS", "RUNNER_ARCH", "RUNNER_TEMP", "COMPUTERNAME",
    "USERNAME", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS",
    "GITHUB_WORKSPACE",
})

#: Words that turn an evidence report into a DECISION. The ratified scenario
#: refuses a change that would treat the operation report as the awaited
#: infrastructure-readiness result, or add an eligibility verdict to it; a schema
#: closed to unknown members cannot recognise intent, so the name scan is the
#: other half.
#:
#: THE SCAN REACHES TWO KINDS, NOT ONE. `admit-deliberation-clearing-operation`
#: requires it of `xfactory_clearing_deliberation_return` as well, in as many
#: words: "a refusal that fires only on a kind this operation never emits is no
#: refusal at all for it". It is applied by ONE function called from both check
#: paths rather than copied, because two copies of a word list are two word lists.
VERDICT_WORDS = ("verdict", "eligib", "readiness_decision", "decision",
                 "go_no_go", "approved", "ready_for", "recommendation")

#: THE CLOSED REFUSAL SET. Every member must be red-proven by a packaged negative
#: fixture. `schema` is the shape refusal and is not a member: it is not this
#: family's rule, it is JSON Schema's.
REFUSAL_CODES = frozenset({
    "clearing-manifest-field-missing",
    "clearing-manifest-file-hash-missing",
    "clearing-manifest-hash-not-byte-tagged",
    "clearing-manifest-expired",
    "clearing-manifest-digest-construction",
    "clearing-unregistered-operation",
    "clearing-lane-not-permitted",
    "clearing-bundle-disagrees-with-register",
    "clearing-origin-row-expired",
    "clearing-origin-signature-missing",
    "clearing-origin-signature-invalid",
    "clearing-origin-signature-partial",
    "clearing-register-member-unratified",
    "clearing-register-entry-incomplete",
    "clearing-readonly-entry-claims-effect",
    "clearing-report-carries-a-verdict",
    "clearing-report-environment-not-allowlisted",
    "clearing-report-lane-reported-as-observed",
    "clearing-record-refusal-ground-unknown",
    "clearing-record-cleared-with-refusal",
    "clearing-record-disposal-unattested",
    "clearing-record-policy-field-reported-verified",
    "clearing-attestation-expected-set-not-per-group",
    "clearing-attestation-dark-lane-as-breach",
    "clearing-attestation-overclaims-completeness",
    "clearing-artifact-unparseable",
})


# --------------------------------------------------------------- findings

@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


CODE_RE = re.compile(r"^(?:ERROR|WARN) +\[([^\]]+)\]")


def codes_of(lines: list[str]) -> set[str]:
    out = set()
    for line in lines:
        m = CODE_RE.match(line)
        if m:
            out.add(m.group(1))
    return out


def lines_for(lines: list[str], code: str) -> list[str]:
    return [line for line in lines if CODE_RE.match(line)
            and CODE_RE.match(line).group(1) == code]


# --------------------------------------------------------------- loading

def parse_instant(value: Any) -> datetime | None:
    """An RFC 3339 instant, normalised to UTC, or None when it is not one.

    Shared by the manifest's own expiry check and the origin row's, because two
    parsers for one grammar is two answers to one question.
    """
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else moment.replace(
        tzinfo=timezone.utc)


def row_has_lapsed(row: dict, now: datetime) -> bool:
    """Whether an origin row's declared expiry has PASSED.

    Deliberately distinct from `state != "active"`. A row can be `active` and
    lapsed at the same time, and that combination is the one this predicate
    exists for: nothing revokes an origin row at clearing today — the
    factory-identity register says so in its own header, and `OQ1` names four
    candidate projection shapes and chooses none — so THE DECLARED EXPIRY IS THE
    ONLY REVOCATION THAT PROPAGATES. A reader that filtered on `state` alone
    would credit a signature made by an authority that has run out, which is the
    one failure mode the short 90-day ceiling exists to bound.
    """
    expires = parse_instant(row.get("expires_at"))
    return expires is not None and expires <= now


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_registry() -> tuple[Registry, dict[str, dict]]:
    resources: list[tuple[str, Resource]] = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(CONTRACT_DIR / name)
        docs[name] = doc
        resource = Resource.from_contents(doc, default_specification=DRAFT202012)
        resources.append((name, resource))
        if doc.get("$id"):
            resources.append((doc["$id"], resource))
    return Registry().with_resources(resources), docs


def load_pinned_reader(path: Path = PINNED_READER):
    """Import the PINNED openXwallet reader, or REFUSE.

    There is no fallback ON PURPOSE, and the reasoning is
    `scripts/validate-factory-identity.py`'s verbatim: a local reimplementation
    of base58btc or of the fingerprint spelling would be the second
    implementation this family exists to prevent, and it would arrive silently on
    the one run where the gitlink was not initialized — precisely the run nobody
    inspects.
    """
    if not path.is_file():
        raise SystemExit(
            f"validate-clearing-dispatch: the pinned openXwallet reader is not "
            f"at {path}. Run `git submodule update --init openXwallet`. This "
            f"program REFUSES rather than decoding keys with arithmetic of its "
            f"own: one derivation, one place.")
    spec = importlib.util.spec_from_file_location(
        "_pinned_openxwallet_reader_clearing", path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise SystemExit(f"validate-clearing-dispatch: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("decode_public_key_multibase", "fingerprint_of_public_key"):
        if not hasattr(module, name):
            raise SystemExit(
                f"validate-clearing-dispatch: the pinned reader at {path} has "
                f"no {name!r}; the pin predates the decoding path this reader "
                f"reuses, and inventing a local one is refused")
    return module


EXPECTED_RE = re.compile(r"^#\s*expected_failure:\s*(\S+)\s*$")
DETAIL_RE = re.compile(r"^#\s*expected_failure_detail:\s*(.+?)\s*$")


def expected_failure(path: Path) -> tuple[str | None, str | None]:
    code = detail = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            break
        m = EXPECTED_RE.match(line)
        if m:
            code = m.group(1)
        m = DETAIL_RE.match(line)
        if m:
            detail = m.group(1)
    return code, detail


# ------------------------------------------------------- the origin register

def read_origin_register(f: Findings, base: Path, pinned) -> dict[str, dict]:
    """Index the factory-identity register by originating repository.

    A row confers nothing unless it is ACTIVE, so only active rows are indexed:
    a revoked or superseded row must not make a producer look registered.
    """
    register = base / "register.yaml"
    if not register.is_file():
        return {}
    doc = load_yaml(register) or {}
    bound = doc.get("revocation_staleness_bound")
    if bound:
        f.note(f"factory-identity register read: {register.relative_to(ROOT)} "
               f"(declared revocation staleness bound {bound}; revocation AT "
               f"CLEARING is not claimed and is not checked here)")
    out: dict[str, dict] = {}
    for row in doc.get("rows") or []:
        if row.get("state") != "active":
            continue
        holder = row.get("holder_ref")
        if not holder:
            continue
        entry = dict(row)
        wallet_id = row.get("wallet_ref")
        wallet_path = base / "wallets" / f"{wallet_id}.yaml"
        if wallet_path.is_file():
            wallet = load_yaml(wallet_path) or {}
            key = wallet.get("key_reference") or {}
            entry["_key_reference"] = key
            multibase = key.get("public_key_multibase")
            raw = pinned.decode_public_key_multibase(multibase) if multibase else None
            entry["_public_key"] = raw
            if raw is not None and key.get("key_fingerprint"):
                recomputed = pinned.fingerprint_of_public_key(raw)
                if recomputed != key["key_fingerprint"]:
                    f.error("clearing-origin-signature-invalid",
                            f"{wallet_path.name}: the recorded key fingerprint "
                            f"{key['key_fingerprint']} is not the fingerprint of "
                            f"the recorded public half ({recomputed}); a key "
                            f"that disagrees with itself verifies nothing")
        out[holder] = entry
    if out:
        lapsed = sorted(holder for holder, row in out.items()
                        if row_has_lapsed(row, datetime.now(timezone.utc)))
        f.note(f"origin identities indexed: {len(out)} active row(s) over "
               f"{len(out)} originating repository(ies); "
               f"{len(lapsed)} LAPSED and creditable for nothing"
               + (f" ({', '.join(lapsed)})" if lapsed else ""))
    return out


# ------------------------------------------------------------- the register

REQUIRED_ENTRY_MEMBERS = (
    "operation_id", "title", "permitted_semantics", "class_constraints",
    "worker_profile", "lanes", "output_schema_ref", "data_handling",
    "repository_affecting_output",
)


def check_register(f: Findings, doc: Any, where: str) -> dict[str, dict]:
    """The CLOSED register: closure, entry completeness, and the read-only bound."""
    entries: dict[str, dict] = {}
    if not isinstance(doc, dict):
        return entries
    operations = doc.get("operations")
    if not isinstance(operations, list):
        return entries
    for entry in operations:
        if not isinstance(entry, dict):
            continue
        op = entry.get("operation_id")
        entries[op] = entry
        if op not in RATIFIED_OPERATIONS:
            f.error("clearing-register-member-unratified",
                    f"{where}: {op!r} is not in the ratified member set "
                    f"{sorted(RATIFIED_OPERATIONS)}. Adding an operation is a "
                    f"GOVERNED CONTRACT CHANGE with a spec delta and a reviewer, "
                    f"not an edit to the register instance — an operation set "
                    f"any lane author may extend is a self-service widening of "
                    f"what the estate's hosts do")
        missing = [m for m in REQUIRED_ENTRY_MEMBERS if entry.get(m) is None]
        if missing:
            f.error("clearing-register-entry-incomplete",
                    f"{where}: entry {op!r} declares none of {missing}; the "
                    f"ratified entry list requires every one of them, and a "
                    f"constraint with no representation cannot be checked")
        if entry.get("repository_affecting_output") is False:
            cc = entry.get("class_constraints") or {}
            offending = [k for k in ("writes", "checks_out_code") if cc.get(k)]
            if offending:
                f.error("clearing-readonly-entry-claims-effect",
                        f"{where}: entry {op!r} declares "
                        f"repository_affecting_output: false while its class "
                        f"constraints permit {offending}; an operation declaring "
                        f"no repository-affecting output is PREVENTED from "
                        f"having one, and a change that gives it an effect is a "
                        f"change to this entry")
    return entries


# ------------------------------------------------------------ the manifest

def signable_subject(manifest: dict) -> dict:
    """THE SUBJECT AN ORIGIN SIGNATURE COVERS: exactly the ten declared fields.

    `origin_attestation` is carried WITHOUT its own signature and without the
    digest VALUE, because a signature cannot cover itself and a digest cannot
    commit to its own output. Everything else — the per-file hashes included — is
    inside, which is what makes "no field can be altered after signing without
    detection" true rather than asserted.
    """
    subject = {name: copy.deepcopy(manifest.get(name)) for name in DECLARED_FIELDS}
    attestation = subject.get("origin_attestation")
    if isinstance(attestation, dict):
        attestation.pop("signature", None)
        digest = attestation.get("manifest_digest")
        if isinstance(digest, dict):
            digest.pop("value", None)
    return subject


def check_manifest(f: Findings, doc: dict, where: str,
                   entries: dict[str, dict], origins: dict[str, dict],
                   now: datetime) -> None:
    # --- the ten-field completeness rule, which NAMES the missing field ------
    for name in DECLARED_FIELDS:
        value = doc.get(name)
        if value is None or value == "" or value == [] or value == {}:
            f.error("clearing-manifest-field-missing",
                    f"{where}: declared field {name!r} is missing or empty. All "
                    f"TEN declared fields are present in a sealed bounded "
                    f"request, and a missing one refuses the request with the "
                    f"field named")

    # --- field (4): a file without its hash, and hashes that are not bytes ----
    for item in doc.get("selected_files") or []:
        if not isinstance(item, dict):
            continue
        path = item.get("path", "<unnamed>")
        content_hash = item.get("content_hash")
        if not content_hash:
            f.error("clearing-manifest-file-hash-missing",
                    f"{where}: selected file {path!r} carries no content hash; a "
                    f"bundle carrying selected files without their hashes is "
                    f"refused")
            continue
        if isinstance(content_hash, dict):
            f.error("clearing-manifest-hash-not-byte-tagged",
                    f"{where}: selected file {path!r} states its content hash as "
                    f"a canonical-JSON digest object. PER-FILE CONTENT HASHES "
                    f"ARE NOT JSON VALUES: a canonical-JSON construction has "
                    f"nothing to canonicalize in a byte stream, so this is a "
                    f"category error rather than a stricter rule — an "
                    f"algorithm-tagged SHA-256 over the file's bytes is what "
                    f"belongs here")
        elif isinstance(content_hash, str) and not re.fullmatch(
                r"sha256:[0-9a-f]{64}", content_hash):
            f.error("clearing-manifest-hash-not-byte-tagged",
                    f"{where}: selected file {path!r} carries {content_hash!r}, "
                    f"which is not an algorithm-tagged SHA-256 over the file's "
                    f"bytes")

    # --- field (3): expiry ---------------------------------------------------
    job = doc.get("job") or {}
    expires = job.get("expires_at")
    if isinstance(expires, str):
        moment = parse_instant(expires)
        if moment is not None:
            if moment <= now:
                f.error("clearing-manifest-expired",
                        f"{where}: the request expired at {expires} and is "
                        f"refused rather than served. This is an EXPIRY refusal, "
                        f"a decided outcome, and not a transient failure to be "
                        f"retried")

    # --- field (10): the digest construction ---------------------------------
    attestation = doc.get("origin_attestation") or {}
    kind = attestation.get("attestation_type")
    if kind == "origin_signature":
        digest = attestation.get("manifest_digest") or {}
        construction = digest.get("construction")
        subject = digest.get("subject")
        if construction != canonical.CONSTRUCTION:
            f.error("clearing-manifest-digest-construction",
                    f"{where}: the manifest digest declares construction "
                    f"{construction!r}; the ONE construction in force is "
                    f"{canonical.CONSTRUCTION!r}, and this capability defines no "
                    f"second one")
        if subject != MANIFEST_SUBJECT:
            f.error("clearing-manifest-digest-construction",
                    f"{where}: the manifest digest declares subject {subject!r}; "
                    f"the admitted subject is {MANIFEST_SUBJECT!r}, a tranche-3 "
                    f"widening of signed-execution-chain's closed enumeration")
        elif subject not in canonical.SUBJECTS:  # pragma: no cover - guard
            f.error("clearing-manifest-digest-construction",
                    f"{where}: {subject!r} is not admitted by the shipped reader's "
                    f"frozen subject set; the contract and the reader disagree")

    # --- field (5)/(7): the register governs ---------------------------------
    operation = doc.get("operation")
    entry = entries.get(operation)
    if operation is not None and entry is None:
        f.error("clearing-unregistered-operation",
                f"{where}: operation {operation!r} has no entry in the closed "
                f"permitted-operations register, so the dispatch is refused "
                f"before any runner is selected and NO RUNNER IS SELECTED")
    elif entry is not None:
        lane = doc.get("lane") or {}
        permitted = [(l.get("runner_group"), l.get("dispatch_label"))
                     for l in entry.get("lanes") or []]
        asked = (lane.get("runner_group"), lane.get("dispatch_label"))
        if asked not in permitted:
            f.error("clearing-lane-not-permitted",
                    f"{where}: the request asks for lane {asked}, which entry "
                    f"{operation!r} does not permit. Permitted: {permitted}")
        for field_name, entry_key in (("worker_profile", "worker_profile"),
                                      ("output_schema_ref", "output_schema_ref"),
                                      ("data_handling", "data_handling")):
            claimed = doc.get(field_name)
            resolved = entry.get(entry_key)
            if claimed is not None and resolved is not None and claimed != resolved:
                f.error("clearing-bundle-disagrees-with-register",
                        f"{where}: the bundle claims {field_name}={claimed!r} "
                        f"while the register entry for {operation!r} resolves "
                        f"{resolved!r}. THE REGISTER GOVERNS: the request is "
                        f"refused and the disagreement recorded, and the "
                        f"dispatch proceeds on NEITHER value — only that denies "
                        f"a producer the ability to choose its own worker "
                        f"profile, lane, or output schema by writing them into "
                        f"a bundle it controls")

    # --- field (10): the origin check ----------------------------------------
    origin = doc.get("origin") or {}
    repository = origin.get("repository")
    row = origins.get(repository)
    if row is not None and row_has_lapsed(row, now):
        # REFUSED IN BOTH DIRECTIONS, and the ordering is the point. A lapsed row
        # must not credit a signature — the authority behind the key has run out.
        # It must ALSO not quietly drop the producer back to "unregistered", which
        # is what skipping the row would do: hosted provenance would then satisfy
        # field (10) and an EXPIRY would have LOOSENED the boundary. Registering an
        # identity tightens a producer and never loosens one; so does letting one
        # lapse.
        f.error("clearing-origin-row-expired",
                f"{where}: {repository} resolves to origin row "
                f"{row.get('row_id')!r}, which is still recorded `state: active` "
                f"but EXPIRED at {row.get('expires_at')}. Nothing revokes an "
                f"origin row at clearing today, so the declared expiry is the "
                f"only revocation that propagates and it has propagated. The "
                f"request is refused whichever field (10) it carries: a "
                f"signature is not credited against a lapsed authority, and "
                f"hosted provenance is not accepted in its place — an expiry "
                f"that widened what a producer may present would invert the "
                f"rule it exists to enforce. The remedy is a governed register "
                f"act: supersede the row, or mark it revoked")
    elif kind == "hosted_workflow_provenance" and row is not None:
        f.error("clearing-origin-signature-missing",
                f"{where}: {repository} holds an ACTIVE registered origin "
                f"identity (row {row.get('row_id')}), so field (10) is an ORIGIN "
                f"SIGNATURE over the manifest and trusted hosted-workflow "
                f"provenance alone does not satisfy it. The missing origin "
                f"signature is the refusal; field (10) is NOT present")
    elif kind == "origin_signature":
        covered = doc.get("origin_attestation", {}).get("covered_fields") or []
        if set(covered) != set(DECLARED_FIELDS):
            f.error("clearing-origin-signature-partial",
                    f"{where}: the origin signature declares coverage of "
                    f"{sorted(covered)}, which is not the ten declared fields. A "
                    f"signature covering some of the ten but not all of them, or "
                    f"not covering the per-file hashes, is not a signed manifest")
        if row is None:
            f.warn("clearing-origin-signature-unregistered-producer",
                   f"{where}: {repository} holds no active origin row, so the "
                   f"signature cannot be resolved to a registered key. Field "
                   f"(10) is satisfiable by hosted provenance for this producer; "
                   f"a signature nothing can verify is reported rather than "
                   f"credited")
        else:
            verify_origin_signature(f, doc, where, row)


def verify_origin_signature(f: Findings, doc: dict, where: str, row: dict) -> None:
    attestation = doc.get("origin_attestation") or {}
    public = row.get("_public_key")
    key_reference = row.get("_key_reference") or {}
    if public is None:
        f.error("clearing-origin-signature-invalid",
                f"{where}: the origin row for {row.get('holder_ref')} carries no "
                f"decodable public half, so nothing can be verified against it. "
                f"An unresolvable key REFUSES; it does not pass")
        return
    declared_key = attestation.get("key_id")
    if declared_key and key_reference.get("key_id") and \
            declared_key != key_reference["key_id"]:
        f.error("clearing-origin-signature-invalid",
                f"{where}: the manifest names key {declared_key!r} while the "
                f"register row resolves {key_reference['key_id']!r}")
        return
    signature = attestation.get("signature") or ""
    try:
        raw_signature = _b64u_decode(signature)
    except ValueError:
        f.error("clearing-origin-signature-invalid",
                f"{where}: field (10)'s signature is not decodable unpadded "
                f"base64url")
        return
    subject = signable_subject(doc)
    try:
        message = canonical.serialize(subject).encode("utf-8")
    except canonical.ConstructionError as exc:
        f.error("clearing-manifest-digest-construction",
                f"{where}: the manifest is not serializable under "
                f"{canonical.CONSTRUCTION}: {exc}")
        return
    declared_digest = (attestation.get("manifest_digest") or {}).get("value")
    recomputed = canonical.digest(subject)
    if declared_digest and declared_digest != recomputed:
        f.error("clearing-manifest-digest-construction",
                f"{where}: the manifest digest records {declared_digest} but the "
                f"subject hashes to {recomputed}; a digest that does not commit "
                f"to the bytes beside it commits to nothing")
        return
    if len(raw_signature) != ed25519.SIGNATURE_BYTES or \
            not ed25519.verify(public, message, raw_signature):
        f.error("clearing-origin-signature-invalid",
                f"{where}: field (10)'s origin signature does not verify against "
                f"the public key registered for {row.get('holder_ref')}. "
                f"Provider-confirmed provenance does NOT cure this: the provider "
                f"says which run produced the object, and the signature says the "
                f"originating repository's hosted environment intended THIS "
                f"manifest")


def _b64u_decode(text: str) -> bytes:
    import base64
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


# ------------------------------------------------------- the operation report

def check_no_verdict(f: Findings, doc: dict, where: str, tail: str) -> None:
    """THE NAME SCAN, shared by every evidence shape this family carries.

    A schema closed to unknown members refuses a member it does not know; it
    cannot refuse one it DOES know whose name announces a decision. This is the
    other half, and it is one function rather than one per kind: the ratified
    entry-two requirement demands the same scan over
    `xfactory_clearing_deliberation_return`, and a copied word list drifts.

    `tail` is the half of the message that differs by subject — the argument for
    WHY this particular shape may not carry a verdict. The CODE is the same, and
    is not widened: `clearing-report-carries-a-verdict` already exists and is
    already red-proven.
    """
    for name in _member_names(doc):
        lowered = name.lower()
        if any(word in lowered for word in VERDICT_WORDS):
            f.error("clearing-report-carries-a-verdict",
                    f"{where}: member {name!r} reads as an eligibility verdict. "
                    f"{tail}")


OPERATION_REPORT_VERDICT_TAIL = (
    "The operation report is EVIDENCE produced BY passing through the boundary; "
    "it is not, and may not grow into, the neutral infrastructure-readiness "
    "result that the promoted document-cataloging and ideation-routing "
    "preflights await — that is a decision input consulted BEFORE dispatch")

DELIBERATION_RETURN_VERDICT_TAIL = (
    "The deliberation return is EVIDENCE: what the seats produce is their "
    "output, and the outcome is computed by the runtime from the SIGNED "
    "returns, downstream of and outside this boundary. A return that carried "
    "the outcome would move the decision onto the governed host, which is the "
    "one thing this entry's whole class of constraints exists to prevent")


def check_operation_report(f: Findings, doc: dict, where: str) -> None:
    check_no_verdict(f, doc, where, OPERATION_REPORT_VERDICT_TAIL)
    for lane_key, lane in (doc.get("lanes") or {}).items():
        if not isinstance(lane, dict):
            continue
        for name in lane.keys():
            if "observed" in name.lower():
                f.error("clearing-report-lane-reported-as-observed",
                        f"{where}: lane {lane_key!r} carries {name!r}. Group and "
                        f"label in this report are DECLARED, never observed: the "
                        f"provider exposes no runner-group context to a running "
                        f"job, and a job reporting its own group would be the "
                        f"bundle-trust error moved onto the host. OBSERVED "
                        f"membership is established only by the single-door "
                        f"attestation reading the provider's API")
        for name in (lane.get("environment") or {}):
            if name not in ENVIRONMENT_ALLOWLIST:
                f.error("clearing-report-environment-not-allowlisted",
                        f"{where}: lane {lane_key!r} echoes environment variable "
                        f"{name!r}, which is not on the name allowlist "
                        f"{sorted(ENVIRONMENT_ALLOWLIST)}. The echo is a NAME "
                        f"ALLOWLIST and never a wholesale dump, so a credential "
                        f"that someday appears in the host's process environment "
                        f"cannot be printed into a run log by accident")


def _member_names(value: Any, depth: int = 0) -> list[str]:
    if depth > 6 or not isinstance(value, dict):
        return []
    names: list[str] = []
    for key, sub in value.items():
        names.append(key)
        names.extend(_member_names(sub, depth + 1))
    return names


# --------------------------------------------------- the deliberation return

def check_deliberation_return(f: Findings, doc: dict, where: str) -> None:
    """Register entry number two's declared return shape, beyond its schema.

    The schema does the structural half — the root and every nested object are
    closed, the three binding identifiers are required, and there is no signature
    member to put a host-side signature in. What a schema cannot do is recognise
    a member whose name announces an outcome, so the shared name scan is applied
    here for the same reason it is applied to the operation report, and with the
    SAME finding code: this entry mints none.
    """
    check_no_verdict(f, doc, where, DELIBERATION_RETURN_VERDICT_TAIL)


# ------------------------------------------------------- the dispatch record

def check_dispatch_record(f: Findings, doc: dict, where: str,
                          schema: dict) -> None:
    cleared = doc.get("cleared")
    refusal = doc.get("refusal")
    if cleared is True and refusal:
        f.error("clearing-record-cleared-with-refusal",
                f"{where}: the record says cleared: true and carries a refusal "
                f"ground {refusal.get('ground')!r}. A dispatch is admitted or "
                f"refused; a record asserting both evidences neither")
    if cleared is False and not refusal:
        f.error("clearing-record-cleared-with-refusal",
                f"{where}: the record says cleared: false and names no refusal "
                f"ground. A refusal is recorded with its ground named FROM THE "
                f"CLOSED ENUMERATION, because a boundary that logs only "
                f"successes cannot evidence what it stopped")
    if isinstance(refusal, dict):
        allowed = _refusal_grounds(schema)
        ground = refusal.get("ground")
        if ground not in allowed:
            f.error("clearing-record-refusal-ground-unknown",
                    f"{where}: refusal ground {ground!r} is not a member of the "
                    f"closed enumeration {sorted(allowed)}. A ground absent from "
                    f"that enumeration is added by a GOVERNED CHANGE to the "
                    f"schema rather than recorded as free text — a boundary that "
                    f"logs prose cannot be counted")
    disposal = doc.get("workspace_disposal")
    if not disposal or disposal.get("disposed") is None or \
            not disposal.get("method"):
        f.error("clearing-record-disposal-unattested",
                f"{where}: the workspace-disposal field is absent or empty. It "
                f"is NOT evidence of a clean host, and the periodic attestation "
                f"reports it as an UNATTESTED DISPOSAL rather than counting the "
                f"dispatch as clean. Disposal happens on failure, refusal and "
                f"timeout exactly as on success")
    verification = doc.get("verification") or {}
    policy_fields = {"operation", "worker_profile", "lane", "output_schema_ref",
                     "data_handling", "class_constraints"}
    for row in verification.get("provider_verified") or []:
        if isinstance(row, dict) and row.get("field") in policy_fields:
            f.error("clearing-record-policy-field-reported-verified",
                    f"{where}: {row.get('field')!r} is reported inside the "
                    f"provider-verified set. It has NO authoritative provider "
                    f"answer: it is POLICY-CHECKED against the register, and "
                    f"'verified' applied to a field nothing could verify is "
                    f"precisely the false assurance this boundary exists to "
                    f"prevent")
    signature_outcome = verification.get("origin_signature")
    if isinstance(signature_outcome, dict):
        for row in verification.get("provider_verified") or []:
            if isinstance(row, dict) and row.get("field") == "origin_signature":
                f.error("clearing-record-policy-field-reported-verified",
                        f"{where}: the origin-signature outcome is folded into "
                        f"the provider-verified set. It is a THIRD verification "
                        f"class with its own outcome, naming the register row "
                        f"and the key it resolved")


def _refusal_grounds(schema: dict) -> set[str]:
    return set(schema.get("$defs", {}).get("refusal_ground", {}).get("enum", []))


# -------------------------------------------------------- the attestation

def check_attestation(f: Findings, doc: dict, where: str) -> None:
    groups = doc.get("groups") or []
    expected_sets = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        expected_sets.append(tuple(sorted(group.get("expected_allowlist") or [])))
        for finding in group.get("findings") or []:
            if not isinstance(finding, dict):
                continue
            klass = finding.get("finding_class")
            subject = finding.get("subject")
            if klass == "widening":
                declared_absent = {
                    m.get("workflow") for m in group.get("enumerated_members") or []
                    if m.get("declared_allowlist_status") == "absent"}
                observed = set(group.get("observed_allowlist") or [])
                if subject in declared_absent and subject not in observed:
                    f.error("clearing-attestation-dark-lane-as-breach",
                            f"{where}: group {group.get('runner_group')!r} files "
                            f"{subject!r} as a WIDENING. It is an ENUMERATED "
                            f"MEMBER WITH NO OBSERVED ALLOWLIST ENTRY, which is "
                            f"ALREADY FAILING CLOSED — nothing reaches the host "
                            f"through it — and is a DARK-LANE DISPOSITION ITEM, "
                            f"not a breach. Treating an unreachable lane as a "
                            f"breach makes the attestation red for a condition "
                            f"strictly safer than the expectation")
                if subject == doc.get("clearing_workflow_path") and \
                        group.get("clearing_path_admitted") is False:
                    f.error("clearing-attestation-dark-lane-as-breach",
                            f"{where}: group {group.get('runner_group')!r} files "
                            f"the clearing workflow's own absent path as a "
                            f"WIDENING. Convergence is a TERMINAL STATE, not an "
                            f"entry condition: before the operator's one console "
                            f"act that path is absent by construction, and it is "
                            f"reported as convergence not yet reached")

    if len(expected_sets) > 1 and len(set(expected_sets)) == 1:
        f.error("clearing-attestation-expected-set-not-per-group",
                f"{where}: every group declares the SAME expected allowlist "
                f"{list(expected_sets[0])}. THE EXPECTED SET IS COMPUTED PER "
                f"GROUP — the clearing workflow's path UNION the members "
                f"enumerated FOR THAT GROUP whose status is `present`. One "
                f"estate-wide set reports every group as diverging from every "
                f"other group's members, which cannot be green while more than "
                f"one group exists")

    claim = doc.get("completeness_claim") or {}
    if claim.get("strength") == "full_post_admission":
        unconverged = [g.get("runner_group") for g in groups
                       if isinstance(g, dict) and
                       g.get("clearing_path_admitted") is False]
        if unconverged:
            f.error("clearing-attestation-overclaims-completeness",
                    f"{where}: the record claims the FULL completeness strength "
                    f"while {unconverged} have not admitted the clearing "
                    f"workflow's path. Before those operator acts a green "
                    f"attestation supports the NARROWER claim only — that no "
                    f"allowlist entry outside each group's expected set exists — "
                    f"while the ledger is complete only for dispatches that came "
                    f"THROUGH THE DOOR")


# ---------------------------------------------------------- adjudication

def validate_record(f: Findings, doc: Any, where: str, registry: Registry,
                    docs: dict[str, dict], entries: dict[str, dict],
                    origins: dict[str, dict], now: datetime) -> None:
    if not isinstance(doc, dict):
        return
    kind = doc.get("kind")
    schema_name = KIND_TO_SCHEMA.get(kind)
    if schema_name is None:
        return
    schema = docs[schema_name]
    validator = Draft202012Validator(schema, registry=registry,
                                     format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in error.path) or "<root>"
        f.error("schema", f"{where}: {location}: {error.message}")
    if kind == "xfactory_sealed_bundle_manifest":
        check_manifest(f, doc, where, entries, origins, now)
    elif kind == "xfactory_clearing_permitted_operations_registry":
        check_register(f, doc, where)
    elif kind == "xfactory_clearing_operation_report":
        check_operation_report(f, doc, where)
    elif kind == "xfactory_clearing_deliberation_return":
        check_deliberation_return(f, doc, where)
    elif kind == "xfactory_clearing_dispatch_record":
        check_dispatch_record(f, doc, where, schema)
    elif kind == "xfactory_clearing_single_door_attestation":
        check_attestation(f, doc, where)


def load_records(path: Path) -> list[Any]:
    """A fixture may carry more than one record, `---`-separated."""
    with path.open(encoding="utf-8") as handle:
        return [doc for doc in yaml.safe_load_all(handle) if doc is not None]


def note_unparseable(f: Findings, path: Path, exc: Exception, where: str) -> None:
    """A file this reader could not parse is NOT a file this reader cleared.

    Skipping silently is the failure mode this exists to close: a file carrying
    one of the family's kinds, broken badly enough not to parse, was reported as
    "0 artifact(s) checked" and the run exited 0 — a green sweep whose greenness
    came from the file being UNREADABLE rather than conformant. That is the
    unreadable-API error moved onto the local disk, and this capability refuses
    it everywhere else by name.

    THE TEXT SCAN IS THE ONLY THING AVAILABLE, and its limit is stated rather
    than hidden: with no parse there is no `kind` to dispatch on, so the raw
    bytes are searched for one of the five kind tokens. A file that mentions a
    kind in a comment is a FALSE POSITIVE, and that is the direction this errs in
    on purpose — a spurious finding names a file a human checks in seconds, while
    a missed one is a hole in a sweep nobody re-runs. A file with no family token
    stays skipped: this reader is not the repository's YAML linter.
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:  # pragma: no cover - unreadable file
        raw = ""
    named = sorted(k for k in KIND_TO_SCHEMA if k in raw)
    if not named:
        return
    detail = str(exc).splitlines()[0] if str(exc) else "(no detail)"
    f.error("clearing-artifact-unparseable",
            f"{where}: names {named} but does not parse as YAML, so it was NOT "
            f"adjudicated: {exc.__class__.__name__}: {detail}. An artifact this "
            f"sweep could not read is not an artifact this sweep cleared")


NOW_SENTINEL = datetime(2026, 9, 3, 12, 0, 0, tzinfo=timezone.utc)


def self_test(f: Findings, registry: Registry, docs: dict[str, dict],
              entries: dict[str, dict], origins: dict[str, dict]) -> None:
    if not EXAMPLES.is_dir():
        f.error("clearing-examples-missing",
                f"{EXAMPLES} is absent; the corpus IS the proof that each closed "
                f"refusal fires, and a family with no corpus proves nothing")
        return

    positives = sorted(p for p in EXAMPLES.glob("*.example.yaml"))
    count = 0
    for path in positives:
        for index, doc in enumerate(load_records(path)):
            count += 1
            validate_record(f, doc, f"examples/{path.name}#{index}", registry,
                            docs, entries, origins, NOW_SENTINEL)

    probed: set[str] = set()
    negatives = sorted(NEGATIVES.glob("*.yaml")) if NEGATIVES.is_dir() else []
    for path in negatives:
        code, detail = expected_failure(path)
        if code is None:
            f.error("clearing-negative-wrong-reason",
                    f"negative/{path.name}: no `# expected_failure:` header. A "
                    f"fixture that does not declare WHY it is invalid pins "
                    f"nothing — any failure would satisfy it")
            continue
        local = Findings()
        try:
            fixture_records = load_records(path)
        except yaml.YAMLError as exc:
            # A FIXTURE MAY BE UNPARSEABLE ON PURPOSE. `clearing-artifact-unparseable`
            # can only fire on a file that does not parse, so the only fixture
            # that can red-prove it is one that does not parse — and the
            # `# expected_failure:` header still reads, because that header is
            # parsed from raw lines rather than from YAML.
            note_unparseable(local, path, exc, f"negative/{path.name}")
            fixture_records = []
        for index, doc in enumerate(fixture_records):
            validate_record(local, doc, f"negative/{path.name}#{index}", registry,
                            docs, entries, origins, NOW_SENTINEL)
        found = codes_of(local.errors)
        if not local.errors:
            f.error("clearing-negative-wrong-reason",
                    f"negative/{path.name}: validated cleanly; it declares "
                    f"{code!r}")
            continue
        if code not in found:
            f.error("clearing-negative-wrong-reason",
                    f"negative/{path.name}: declares {code!r} but failed for "
                    f"{sorted(found)}")
            continue
        if detail and not any(detail in line for line in lines_for(local.errors, code)):
            f.error("clearing-negative-wrong-reason",
                    f"negative/{path.name}: {code!r} fired but not for "
                    f"{detail!r}")
            continue
        probed.add(code)

    f.note(f"self-test: {count} packaged record(s) validated, "
           f"{len(negatives)} negative fixture(s) refused")

    unprobed = sorted(REFUSAL_CODES - probed)
    f.note(f"{len(REFUSAL_CODES & probed)}/{len(REFUSAL_CODES)} closed refusal "
           f"codes red-proven")
    for code in unprobed:
        f.error("clearing-refusal-code-without-probe",
                f"{code}: no packaged negative fixture makes this refusal fire. "
                f"A closed refusal code nobody has seen go red is a refusal "
                f"nobody has tested")


SKIP_DIRS = {".git", "node_modules", "__pycache__", "openXwallet",
             "installs", "_previous_clones"}


def repo_scan(f: Findings, target: Path, registry: Registry,
              docs: dict[str, dict], entries: dict[str, dict],
              origins: dict[str, dict]) -> None:
    now = datetime.now(timezone.utc)
    checked = 0
    if target.is_file():
        candidates = [target]
    else:
        candidates = [p for p in target.rglob("*.y*ml")
                      if not any(part in SKIP_DIRS for part in p.parts)
                      and EXAMPLES not in p.parents]
    for path in sorted(candidates):
        try:
            records = load_records(path)
        except yaml.YAMLError as exc:
            try:
                where = str(path.relative_to(target))
            except ValueError:  # pragma: no cover - single-file target
                where = path.name
            note_unparseable(f, path, exc, where)
            continue
        for index, doc in enumerate(records):
            if not isinstance(doc, dict) or doc.get("kind") not in KIND_TO_SCHEMA:
                continue
            if path == REGISTRY_INSTANCE:
                continue  # adjudicated once, as the register, above
            checked += 1
            try:
                where = str(path.relative_to(target))
            except ValueError:  # pragma: no cover - single-file target
                where = path.name
            validate_record(f, doc, f"{where}#{index}", registry, docs, entries,
                            origins, now)
    f.note(f"repo scan ({target}): {checked} artifact(s) checked")
    if checked == 0:
        f.note("zero real artifacts is the EXPECTED state until a clearing "
               "implementation writes its first neutral record; the clearing "
               "lane emits key=value ledger lines today")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-clearing-dispatch: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", default=None,
                        help="repo checkout (or single file) to scan for real "
                             "clearing artifacts; omit to self-test only")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    args = parser.parse_args(argv)

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
            f.error("clearing-schema-meta-invalid", f"{name}: {exc}")
        if not doc.get("$schema") or not doc.get("$id"):
            f.error("clearing-schema-identity-missing",
                    f"{name}: every schema in this family declares its dialect "
                    f"($schema) and an absolute $id, so a consumer's stock "
                    f"validator resolves the bundle the same way this one does")

    pinned = load_pinned_reader()
    f.note(f"pinned openXwallet decoders read from "
           f"{PINNED_READER.relative_to(ROOT)}")

    if not REGISTRY_INSTANCE.is_file():
        print(f"ERROR {REGISTRY_INSTANCE} not found", file=sys.stderr)
        return 2
    register_doc = load_yaml(REGISTRY_INSTANCE)
    validate_record(f, register_doc, "permitted-operations.registry.yaml",
                    registry, docs, {}, {}, NOW_SENTINEL)
    entries = check_register(f, register_doc, "permitted-operations.registry.yaml")
    # THE COUNT IS A LITERAL THE CI GATE GREPS FOR, and the plural agrees with it.
    # `clearing-dispatch-gate.yml` pins the exact sentence this line prints, so a
    # register that gained a member and a reader that still said "1 registered
    # operation" would disagree in the one place the gate is looking.
    plural = "" if len(entries) == 1 else "s"
    f.note(f"permitted-operations register read: "
           f"{REGISTRY_INSTANCE.relative_to(ROOT)} "
           f"({len(entries)} registered operation{plural})")

    try:
        fixture_origins = read_origin_register(f, FIXTURE_IDENTITY, pinned)
        live_origins = read_origin_register(f, LIVE_IDENTITY, pinned)
        self_test(f, registry, docs, entries, fixture_origins)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, registry, docs, entries, live_origins)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
