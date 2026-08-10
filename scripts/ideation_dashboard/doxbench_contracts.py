"""Pinned doxBench wire schemas: exact loading, digest verification, structural
validation, and DELEGATED semantics (plan "doxbench_contracts.py"; T021).

Nothing normative is restated here. The two schemas are read READ-ONLY from the
pinned openxFactory checkout, and every rule the shape cannot express — content
identity recomputation, the one-outline-one-document pairing, the limit-failure
data pairing, the public-only credential scan — belongs to
`scripts/validate-ideation-dashboard-contracts.py`, the family's declared owner.
`delegated_semantic_validation` runs THAT script; this module never re-derives its
verdict (see snapshot.py for the same delegation discipline).

Three things are verified before a schema is trusted, and each one refuses rather
than warns (a schema copy that is not the released bytes is not the contract):

  1. the file's sha256 equals the pinned digest in `SCHEMA_DIGESTS`;
  2. the checkout's OWN `contracts/manifest.yaml` entry for that file records the
     same digest — manifest parity, so a coherent release is distinguished from a
     directory that merely contains a file with the right name; and
  3. `stack.yaml`'s `xfactory.contract_ref` still equals `CONTRACT_REF`, so a
     consumer can never read one release while the repository declares another.

The chat-turn FILE holds three closed envelopes under a `oneOf`, discriminated by
`kind`. Consumers dispatch on the INSTANCE kind, so the per-kind mapping resolves
each envelope individually through a `$ref` into that file — the same
registry-backed pattern the openxFactory validator uses for the possibles-register
kernel section.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

# --------------------------- the pin ---------------------------
#
# THE RELEASE IS IMMUTABLE (research R13): these literals name content that
# already exists — contract-v1.27, annotated tag object
# fb912b9a542da7aeec7fd35fb2aeeb551bd5a733 — never a future tag and never the
# latest sibling checkout. The pin moves ONLY through the normal xFactory
# workflow (T006: openxFactory releases additively, then `stack.yaml` is
# updated), so editing a digest here without that release is a defect, not a
# refresh. `stack.yaml` carries the same three values in comments beside the ref
# it declares; the parity check below is what keeps the two from drifting apart
# silently.

CONTRACT_REF = "ff64e81a967b75f92b3f5af9204aeb54c59a15d3"
CONTRACT_TAG = "contract-v1.28"

CATALOG_SCHEMA_FILE = "xfactory-workbench-model-catalog.schema.yaml"
CHAT_TURN_SCHEMA_FILE = "xfactory-workbench-chat-turn.schema.yaml"

# sha256 over each schema file's exact bytes at the release.
SCHEMA_DIGESTS = {
    CATALOG_SCHEMA_FILE:
        "0e6e7e946268b220918a426c6df399a9e01d064ee5dcbe22f8381dbf39aef1e0",
    CHAT_TURN_SCHEMA_FILE:
        "8386566ef881661659d38f6d6c27c723a7ddaf5dd3b8e18ead854c40a2a876bb",
}

# The four doxBench INSTANCE kinds. The catalog kind is a whole-document schema;
# the three turn kinds all live in the chat-turn file, under these `$defs`.
KIND_MODEL_CATALOG = "workbench-model-catalog"
KIND_CHAT_TURN = "workbench-chat-turn"
KIND_CHAT_TURN_SUCCESS = "workbench-chat-turn-success"
KIND_CHAT_TURN_FAILURE = "workbench-chat-turn-failure"

CHAT_TURN_DEFS = {
    KIND_CHAT_TURN: "request",
    KIND_CHAT_TURN_SUCCESS: "success",
    KIND_CHAT_TURN_FAILURE: "failure",
}

WIRE_KINDS = (KIND_MODEL_CATALOG, KIND_CHAT_TURN, KIND_CHAT_TURN_SUCCESS,
              KIND_CHAT_TURN_FAILURE)

# --------------------------- checkout location ---------------------------
#
# The same convention snapshot.py established (`VALIDATOR_RELPATH`, walk up to
# the aggregation checkout), plus an explicit `root` parameter and one env
# override. No other discovery: a consumer that cannot say which checkout it
# means should not be guessing at a contract pin.

CHECKOUT_RELPATH = Path("openxFactory")
VALIDATOR_IN_CHECKOUT = Path("scripts") / "validate-ideation-dashboard-contracts.py"
VALIDATOR_RELPATH = CHECKOUT_RELPATH / VALIDATOR_IN_CHECKOUT
SCHEMAS_RELPATH = Path("contracts") / "schemas"
MANIFEST_RELPATH = Path("contracts") / "manifest.yaml"

OPENXFACTORY_ROOT_ENV = "OPENXFACTORY_ROOT"

REPO_ROOT = Path(__file__).resolve().parents[2]
STACK_FILE = "stack.yaml"

# One FormatChecker, shared by every validator, exactly as the delegated
# validator does it: `date`/`date-time` are enforced, not merely annotated.
FORMAT_CHECKER = FormatChecker()


class ContractPinError(Exception):
    """The pinned contract could not be read AS PINNED.

    One exception for every way that can happen — an unreachable checkout, an
    absent schema, a digest mismatch, a manifest that disagrees with its own
    bytes, a drifted `stack.yaml` ref, an unknown instance kind — because they
    share one consequence: nothing may be treated as contract-conformant.
    """


def resolve_root(root: Path | str | None = None, *,
                 start: Path | None = None) -> Path:
    """Locate the pinned openxFactory checkout.

    Precedence: an explicit `root`, then `OPENXFACTORY_ROOT`, then a walk up from
    this repository to the aggregation checkout's `openxFactory/`. Fails closed
    when none of the three yields a checkout — "I could not find the contract" is
    never an implicit pass."""
    if root is not None:
        return Path(root)
    declared = os.environ.get(OPENXFACTORY_ROOT_ENV)
    if declared:
        return Path(declared)
    base = (start or REPO_ROOT).resolve()
    for directory in [base, *base.parents]:
        if (directory / VALIDATOR_RELPATH).is_file():
            return directory / CHECKOUT_RELPATH
    raise ContractPinError(
        f"no openxFactory checkout is reachable from {base} (looked for "
        f"{VALIDATOR_RELPATH}); pass root= or set {OPENXFACTORY_ROOT_ENV} to a "
        f"checkout at {CONTRACT_TAG} ({CONTRACT_REF})")


# --------------------------- declared-pin parity ---------------------------

# T104 final queue Q-2 (ruled 2026-08-09), the parse memo: yaml parsing is
# what actually costs (~100 ms for the 181-entry manifest — the jsonschema
# compile is cheap by comparison), so every INPUT keeps its per-request
# byte-read + digest while only the PARSE of bytes that already proved
# themselves is reused. A changed byte makes a new key, so nothing stale can
# ever be served — the fail-closed chain sees every drift on the request that
# carries it.
_PARSED_BY_DIGEST: dict[tuple[str, str], Any] = {}


def _parsed_yaml(path: Path, raw: bytes, *, what: str) -> Any:
    key = (str(path), hashlib.sha256(raw).hexdigest())
    if key in _PARSED_BY_DIGEST:
        return _PARSED_BY_DIGEST[key]
    try:
        doc = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as error:
        raise ContractPinError(f"{path}: unreadable {what} ({error})") from error
    _PARSED_BY_DIGEST[key] = doc
    return doc


def verify_stack_pin(repo_root: Path | str | None = None) -> str:
    """Return `stack.yaml`'s declared `xfactory.contract_ref`, refusing unless it
    equals `CONTRACT_REF`. A drifted pin is an error, never a silent pass: the
    schemas this module hard-pins are only meaningful at the ref the repository
    declares it consumes."""
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    stack = root / STACK_FILE
    if not stack.is_file():
        raise ContractPinError(f"{stack}: no {STACK_FILE} to verify the "
                               f"{CONTRACT_TAG} pin against")
    try:
        raw = stack.read_bytes()
    except OSError as error:
        raise ContractPinError(f"{stack}: unreadable ({error})") from error
    declared = _parsed_yaml(stack, raw, what="stack declaration")
    section = declared.get("xfactory") if isinstance(declared, dict) else None
    ref = section.get("contract_ref") if isinstance(section, dict) else None
    if not isinstance(ref, str) or not ref:
        raise ContractPinError(
            f"{stack}: no xfactory.contract_ref is declared; the pinned "
            f"{CONTRACT_TAG} contract ({CONTRACT_REF}) cannot be confirmed")
    if ref != CONTRACT_REF:
        raise ContractPinError(
            f"{stack}: xfactory.contract_ref is {ref}, not the pinned "
            f"{CONTRACT_REF} ({CONTRACT_TAG}) — repin through the xFactory "
            f"workflow before consuming these schemas")
    return ref


# --------------------------- exact loading ---------------------------

@dataclass(frozen=True)
class ReleasedSchemas:
    """The verified release, as one value: where it came from, the two schema
    documents, the registry their `$ref`s resolve through, and the per-kind
    schemas consumers dispatch on."""

    root: Path
    documents: dict[str, dict]
    registry: Registry
    schemas: dict[str, dict]


def _manifest_digests(root: Path) -> dict[str, Any]:
    """The checkout's own per-file digests, keyed by the repository-relative
    `path` its manifest records."""
    path = root / MANIFEST_RELPATH
    if not path.is_file():
        raise ContractPinError(
            f"{path}: the checkout carries no contracts/manifest.yaml, so its "
            f"self-description cannot be checked against the pinned bytes")
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ContractPinError(f"{path}: unreadable manifest ({error})") from error
    doc = _parsed_yaml(path, raw, what="manifest")
    entries = doc.get("contracts") if isinstance(doc, dict) else None
    if not isinstance(entries, list):
        raise ContractPinError(f"{path}: manifest declares no contracts list")
    return {entry["path"]: entry.get("sha256")
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)}


def _verified_bytes(root: Path, name: str, manifest: dict[str, Any]) -> bytes:
    """Read one pinned schema's BYTES, refusing unless they hash to the pinned
    digest AND the checkout's manifest records that same digest. The whole
    fail-closed chain lives here — `_verified_document` adds only the parse —
    so the validator cache's per-request re-verification (T104 final queue
    Q-2) runs exactly these refusals, never a restatement of them."""
    path = root / SCHEMAS_RELPATH / name
    if not path.is_file():
        raise ContractPinError(
            f"{name}: pinned schema is absent from the checkout at {root} "
            f"(expected {path}; {CONTRACT_TAG} {CONTRACT_REF})")
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    expected = SCHEMA_DIGESTS[name]
    if actual != expected:
        raise ContractPinError(
            f"{name}: sha256 {actual} does not match the pinned {expected} "
            f"({CONTRACT_TAG}) — these are not the released bytes")
    relpath = (SCHEMAS_RELPATH / name).as_posix()
    if relpath not in manifest:
        raise ContractPinError(
            f"{name}: the checkout's contracts/manifest.yaml carries no entry "
            f"for {relpath}, so the release does not describe this schema")
    recorded = manifest[relpath]
    if recorded != actual:
        raise ContractPinError(
            f"{name}: the checkout's contracts/manifest.yaml records sha256 "
            f"{recorded} but the bytes hash to {actual} — the checkout is not a "
            f"coherent {CONTRACT_TAG} release")
    return raw


def _verified_document(root: Path, name: str, manifest: dict[str, Any]) -> dict:
    """One pinned schema, parsed — every refusal is `_verified_bytes`'s."""
    raw = _verified_bytes(root, name, manifest)
    try:
        doc = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as error:
        raise ContractPinError(f"{name}: unparseable schema ({error})") from error
    if not isinstance(doc, dict) or not isinstance(doc.get("$id"), str):
        raise ContractPinError(f"{name}: schema declares no $id to resolve "
                               f"cross-file $refs against")
    return doc


def load_release(root: Path | str | None = None, *,
                 repo_root: Path | str | None = None) -> ReleasedSchemas:
    """Load and verify the pinned release, returning everything derived from it.

    Verification order is deliberate: the DECLARED pin first (a drifted
    `stack.yaml` makes every digest question moot), then the bytes."""
    verify_stack_pin(repo_root)
    checkout = resolve_root(root)
    manifest = _manifest_digests(checkout)
    documents = {name: _verified_document(checkout, name, manifest)
                 for name in sorted(SCHEMA_DIGESTS)}
    registry = Registry().with_resources([
        (doc["$id"], Resource.from_contents(doc, default_specification=DRAFT202012))
        for doc in documents.values()
    ])

    turn_id = documents[CHAT_TURN_SCHEMA_FILE]["$id"]
    turn_defs = documents[CHAT_TURN_SCHEMA_FILE].get("$defs") or {}
    schemas: dict[str, dict] = {KIND_MODEL_CATALOG: documents[CATALOG_SCHEMA_FILE]}
    for kind, definition in CHAT_TURN_DEFS.items():
        if definition not in turn_defs:
            raise ContractPinError(
                f"{CHAT_TURN_SCHEMA_FILE}: no $defs/{definition} envelope for "
                f"kind {kind} at {CONTRACT_TAG}")
        schemas[kind] = {"$ref": f"{turn_id}#/$defs/{definition}"}
    return ReleasedSchemas(checkout, documents, registry, schemas)


def load_released_schemas(root: Path | str | None = None, *,
                          repo_root: Path | str | None = None) -> dict[str, dict]:
    """The per-kind schemas from the pinned release: the catalog kind's whole
    document, and one `$ref` per chat-turn envelope."""
    return load_release(root, repo_root=repo_root).schemas


# --------------------------- structural validation ---------------------------

# T104 final queue Q-2 (ruled 2026-08-09): the plan's 100 ms pre-dispatch p95
# target STANDS, so compiled validators are reused across calls — keyed on the
# digests the per-call verification just PROVED, never on time or on trust.
# Every call still runs the whole fail-closed chain (declared pin, checkout
# resolution, manifest parity, released bytes); only the yaml parse, the
# registry build, and the jsonschema compilation are amortized. A drifted byte
# refuses on the very request that sees it, because the key is derived FROM
# the verified bytes (pinned by
# test_the_cache_never_shortcuts_the_byte_verification).
_VALIDATOR_CACHE: dict[tuple, dict[str, Draft202012Validator]] = {}


def validators(root: Path | str | None = None, *,
               repo_root: Path | str | None = None
               ) -> dict[str, Draft202012Validator]:
    """One draft-2020-12 validator per instance kind, each resolving `$ref`s
    through the offline registry built from the released documents.

    Returns a fresh dict per call (a caller mutating its copy cannot poison
    the cache); the VALIDATOR objects are shared once their bytes verify."""
    verify_stack_pin(repo_root)
    checkout = resolve_root(root)
    manifest = _manifest_digests(checkout)
    for name in sorted(SCHEMA_DIGESTS):
        _verified_bytes(checkout, name, manifest)
    key = (str(Path(checkout).resolve()), tuple(sorted(SCHEMA_DIGESTS.items())))
    cached = _VALIDATOR_CACHE.get(key)
    if cached is not None:
        return dict(cached)
    release = load_release(root, repo_root=repo_root)
    built = {kind: Draft202012Validator(schema, registry=release.registry,
                                        format_checker=FORMAT_CHECKER)
             for kind, schema in release.schemas.items()}
    _VALIDATOR_CACHE[key] = built
    return dict(built)


def _dispatch_kind(doc: Any) -> str:
    if not isinstance(doc, dict):
        raise ContractPinError(
            f"instance is a {type(doc).__name__}, not a mapping carrying a "
            f"doxBench `kind`")
    kind = doc.get("kind")
    if kind not in WIRE_KINDS:
        raise ContractPinError(
            f"{kind!r}: not a doxBench wire kind at {CONTRACT_TAG} "
            f"(expected one of {', '.join(WIRE_KINDS)})")
    return kind


def validate_instance(doc: Any, root: Path | str | None = None, *,
                      repo_root: Path | str | None = None) -> list[str]:
    """Structurally validate one instance against its kind's released schema.

    Returns the error strings (empty means structurally valid). An unknown kind
    RAISES instead: no schema means no verdict, and an empty error list would
    read as "valid"."""
    kind = _dispatch_kind(doc)
    validator = validators(root, repo_root=repo_root)[kind]
    errors = sorted(validator.iter_errors(doc),
                    key=lambda error: [str(part) for part in error.absolute_path])
    return [f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
            f"{error.message}" for error in errors]


# --------------------------- delegated semantics ---------------------------

def delegated_semantic_validation(paths, root: Path | str | None = None
                                  ) -> tuple[int, str]:
    """Run the PINNED openxFactory validator over instance files.

    The consumption rule is DELEGATION: the semantic rules are the release's, and
    the returned exit code is the validator's own (0 ok, 1 findings, 2 harness
    error — its documented contract). Nothing here interprets the instances.

    One invocation PER PATH, because the released CLI takes a single positional
    path; the first non-zero exit is reported, and every invocation's output is
    kept so a caller sees each file's findings."""
    targets = [Path(path) for path in paths]
    if not targets:
        raise ValueError("no instance paths were supplied to validate")
    checkout = resolve_root(root)
    validator = checkout / VALIDATOR_IN_CHECKOUT
    if not validator.is_file():
        raise ContractPinError(
            f"{validator}: the pinned validator is absent from the checkout at "
            f"{checkout}, so semantic validation cannot be delegated")

    returncode = 0
    chunks: list[str] = []
    for target in targets:
        chunks.append(f"$ {validator} {target}")
        try:
            proc = subprocess.run(
                [sys.executable, str(validator), str(target)],
                capture_output=True, text=True)
        except OSError as error:
            raise ContractPinError(
                f"{validator}: could not be launched with {sys.executable} "
                f"({error})") from error
        chunks.append(proc.stdout + proc.stderr)
        if proc.returncode != 0 and returncode == 0:
            returncode = proc.returncode
    return returncode, "\n".join(chunks)
