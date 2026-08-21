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
     CONSUMER can never read one release while its repository declares another.

The third check applies to consumers only. This module is hosted INSIDE the
publisher (`adopt-neutral-tooling-home`, 2026-08-03), and a publisher declares no
consumption pin on itself — openxFactory has no `stack.yaml` and under the
family's working rules must not grow one. Asking the release which release it
consumes is vacuous, so `verify_stack_pin` answers it structurally when the
hosting repository IS a release (`is_publisher_checkout`) and runs the consumer
refusals unchanged otherwise. Nothing else relaxes: checks 1 and 2 are the whole
fail-closed chain, they run per request in both modes, and they are anchored to
this module's own literals rather than to anything the checkout claims about
itself — which is what makes publisher mode safe rather than merely convenient.

The chat-turn FILE holds six closed envelopes under a `oneOf`, discriminated by
`kind`: the three v1 envelopes and the three co-resident widened ones
contract-v1.34 added beside them (`add-doxbench-editing-phase-b` design D15).
Consumers dispatch on the INSTANCE kind, so the per-kind mapping resolves each
envelope individually through a `$ref` into that file — the same registry-backed
pattern the openxFactory validator uses for the possibles-register kernel
section, and the reason a second family costs this module a mapping entry rather
than a branch.
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
# already exists — contract-v1.31, annotated tag object
# fc66fa38b999ea15ce74bf00410afe189cc3a5d6 — never a future tag and never the
# latest sibling checkout. The pin moves ONLY through the normal xFactory
# workflow (T006: openxFactory releases additively, then the consuming
# declaration is updated), so editing a digest here without that release is a
# defect, not a refresh.
#
# Moved v1.28 -> v1.31 by `align-doxbench-contract-pin-to-publisher`
# (2026-08-10). The repin is DIGEST-NEUTRAL and deliberately so: both wire
# schemas are byte-identical across v1.28, v1.29, v1.30 and v1.31, and v1.31's
# own `contracts/manifest.yaml` records exactly the two digests already pinned
# below. It re-declares which release is read and changes no verified byte, so
# no conformance question reopens — which is why it was safe to settle the
# currency question in the same change that fixed the publisher-mode refusal.
#
# codexFactory's `stack.yaml` declares contract-v1.30 and this pin does not.
# That divergence is not drift: codexFactory hosted this runtime until
# `adopt-neutral-tooling-home` and is now merely another consumer, so the two
# pins move independently. A future reader comparing them should stop here.
#
# Moved v1.31 -> v1.34 by `add-doxbench-editing-phase-b` §13. This repin is NOT
# digest-neutral, and could not be: the release widens
# `xfactory-workbench-chat-turn.schema.yaml` itself, so the chat-turn digest
# below is the widened file's and the catalog's is unmoved. The repin lands in
# the same change as the release because the fail-closed chain is byte-exact —
# a runtime pinned to v1.31's digest cannot read v1.34's schema at all, which is
# the check working, not a reason to relax it.
#
# THE REF WAS RESOLVED at contract-v1.34: it was published (annotated tag object
# 439d76b88044edbb22ccf677d57e76dd8a6da350) and the pin named the commit it
# dereferences to, exactly as the v1.31 pin named its own. It carried the
# `unpublished:contract-v1.34` sentinel across the realization branch, because
# the versioning policy allocates the version and builds the digest inventory AT
# REALIZATION (steps 1-2) and publishes the tag against the commit that actually
# lands (step 5) -- so until that commit existed there was nothing honest to
# name, and the sentinel was spelled as a value no `stack.yaml` can declare so a
# consumer comparing against it REFUSED rather than matched by accident.
#
# Moved v1.34 -> v1.38 by `add-doxbench-editing-phase-b` §11.7. Not
# digest-neutral, and could not be: the release grows
# `xfactory-workbench-model-catalog.schema.yaml` itself with the routing-rule
# declaration, so the CATALOG digest below is the grown file's and the
# chat-turn's is unmoved -- the exact mirror image of the v1.34 repin. The repin
# lands in the same change as the release for the same reason it did then: the
# fail-closed chain is byte-exact, so a runtime pinned to v1.34's catalog digest
# cannot read v1.38's schema at all. That is the check working.
#
# WHY v1.38 AND NOT v1.37: the version is allocated AT REALIZATION against
# what is available, and `contract-v1.37` was taken while this slice was in
# flight -- 6cbb4495 (PR #235, identity-brokering + trust-anchor) landed it on
# main, its own squash message still saying v1.36. CHANGELOG presence is the
# availability test, not tag presence, so v1.38 is the next available number.
#
# THE REF IS THE SENTINEL AGAIN, deliberately, and on the same precedent: the
# tag is cut at the realization squash, so on this branch there is no release
# commit to name and `unpublished:contract-v1.38` is the only honest value. A
# follow-up commit resolves it to the published commit, exactly as 7c544c84 did
# for v1.34 while ticking 13.3.

CONTRACT_REF = "unpublished:contract-v1.38"
CONTRACT_TAG = "contract-v1.38"

CATALOG_SCHEMA_FILE = "xfactory-workbench-model-catalog.schema.yaml"
CHAT_TURN_SCHEMA_FILE = "xfactory-workbench-chat-turn.schema.yaml"

# sha256 over each schema file's exact bytes at the release.
SCHEMA_DIGESTS = {
    CATALOG_SCHEMA_FILE:
        "692dad330c5958720d9ba6ef8f6ce1a19dec715547a087e0b08ccd30a9aaa26d",
    CHAT_TURN_SCHEMA_FILE:
        "2eb2a834d4cd50a15838e0e7197b6ddaa6f33aee7d24ff8075e0df8deab0b7e5",
}

# The seven doxBench INSTANCE kinds. The catalog kind is a whole-document schema;
# the six turn kinds all live in the chat-turn file, under these `$defs` — the
# three v1 envelopes and, since contract-v1.34, the three co-resident widened
# ones. Both families are DISPATCHABLE: the v1 kinds are deprecated, not
# withdrawn, and a release that stopped resolving them would break the very
# clients the deprecation exists to keep working.
KIND_MODEL_CATALOG = "workbench-model-catalog"
KIND_CHAT_TURN = "workbench-chat-turn"
KIND_CHAT_TURN_SUCCESS = "workbench-chat-turn-success"
KIND_CHAT_TURN_FAILURE = "workbench-chat-turn-failure"
KIND_CHAT_TURN_V2 = "workbench-chat-turn-v2"
KIND_CHAT_TURN_V2_SUCCESS = "workbench-chat-turn-v2-success"
KIND_CHAT_TURN_V2_FAILURE = "workbench-chat-turn-v2-failure"

CHAT_TURN_DEFS = {
    KIND_CHAT_TURN: "request",
    KIND_CHAT_TURN_SUCCESS: "success",
    KIND_CHAT_TURN_FAILURE: "failure",
    KIND_CHAT_TURN_V2: "request_v2",
    KIND_CHAT_TURN_V2_SUCCESS: "success_v2",
    KIND_CHAT_TURN_V2_FAILURE: "failure_v2",
}

# The DEPRECATED family, named here so a caller can ask rather than pattern-match
# on a kind string. The removal target is the schema's own
# `deprecated_envelopes` record and the CHANGELOG's migration note; this tuple
# states only WHICH kinds are deprecated.
DEPRECATED_CHAT_TURN_KINDS = (KIND_CHAT_TURN, KIND_CHAT_TURN_SUCCESS,
                              KIND_CHAT_TURN_FAILURE)

WIRE_KINDS = (KIND_MODEL_CATALOG, KIND_CHAT_TURN, KIND_CHAT_TURN_SUCCESS,
              KIND_CHAT_TURN_FAILURE, KIND_CHAT_TURN_V2,
              KIND_CHAT_TURN_V2_SUCCESS, KIND_CHAT_TURN_V2_FAILURE)

# --------------------------- checkout location ---------------------------
#
# The same convention snapshot.py established (`VALIDATOR_RELPATH`, walk up to
# the aggregation checkout), plus an explicit `root` parameter and one env
# override. No other discovery: a consumer that cannot say which checkout it
# means should not be guessing at a contract pin.
#
# `VALIDATOR_RELPATH` carries the `openxFactory/` prefix, which is right for the
# aggregation-relative walk it was written for and wrong for a runtime hosted
# INSIDE openxFactory: it searches one level below where it stands, so from the
# publisher it walks past itself every time and lands on the aggregation's
# submodule — a shared tree sessions move between branches. Hence the publisher
# rung in `resolve_root`. The walk-up keeps this shape because the consumer case
# still needs exactly it.

CHECKOUT_RELPATH = Path("openxFactory")
VALIDATOR_IN_CHECKOUT = Path("scripts") / "validate-ideation-dashboard-contracts.py"
VALIDATOR_RELPATH = CHECKOUT_RELPATH / VALIDATOR_IN_CHECKOUT
SCHEMAS_RELPATH = Path("contracts") / "schemas"
MANIFEST_RELPATH = Path("contracts") / "manifest.yaml"

# What makes a directory a RELEASE rather than a consumer of one. All three are
# required together: any single marker is satisfied by a tree that merely
# contains a similarly named file, which is the same distinction manifest parity
# draws for one schema, applied to the checkout as a whole.
PUBLISHER_MARKERS = (MANIFEST_RELPATH, SCHEMAS_RELPATH, VALIDATOR_IN_CHECKOUT)

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


def is_publisher_checkout(root: Path | str) -> bool:
    """True when `root` IS a release rather than a consumer of one.

    Every marker in `PUBLISHER_MARKERS` must be present; see that constant for
    why all three and not any one. This is a STRUCTURAL question about a
    directory — it reads no digest and grants no trust, it only decides which of
    the two verification postures applies."""
    base = Path(root)
    return all((base / marker).exists() for marker in PUBLISHER_MARKERS)


def resolve_root(root: Path | str | None = None, *,
                 start: Path | None = None) -> Path:
    """Locate the pinned openxFactory checkout.

    Precedence, highest first: an explicit `root`; `OPENXFACTORY_ROOT`; the
    hosting repository when it is ITSELF a publisher checkout; then a walk up
    from this repository to the aggregation checkout's `openxFactory/`. Fails
    closed when none of them yields a checkout — "I could not find the contract"
    is never an implicit pass.

    The third rung is what keeps a serve reading the tree it was launched from
    rather than a sibling checkout on whatever branch another session left it
    (`align-doxbench-contract-pin-to-publisher`, 2026-08-10). Only that rung was
    added; nothing above or below it moved, so the consumer case still reaches
    the walk exactly as before."""
    if root is not None:
        return Path(root)
    declared = os.environ.get(OPENXFACTORY_ROOT_ENV)
    if declared:
        return Path(declared)
    base = (start or REPO_ROOT).resolve()
    if is_publisher_checkout(base):
        return base
    for directory in [base, *base.parents]:
        if (directory / VALIDATOR_RELPATH).is_file():
            return directory / CHECKOUT_RELPATH
    raise ContractPinError(
        f"no openxFactory checkout is reachable from {base} (it carries no "
        f"{', '.join(str(marker) for marker in PUBLISHER_MARKERS)} of its own, "
        f"and no ancestor holds {VALIDATOR_RELPATH}); pass root= or set "
        f"{OPENXFACTORY_ROOT_ENV} to a checkout at {CONTRACT_TAG} "
        f"({CONTRACT_REF})")


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
    """Return the hosting repository's consumed `xfactory.contract_ref`, refusing
    unless it equals `CONTRACT_REF`. A drifted pin is an error, never a silent
    pass: the schemas this module hard-pins are only meaningful at the ref the
    repository declares it consumes.

    PUBLISHER MODE. When the hosting repository is itself a release
    (`is_publisher_checkout`) the consumed ref is `CONTRACT_REF` by construction
    and there is no declaration to read — the publisher pins no consumption of
    itself. The declared-pin check exists so a CONSUMER cannot read one release
    while its repository declares another; that gap needs two places a human
    edits, and a publisher has only one. Refusing here would not be strictness,
    it would be a question with no honest answer.

    This drops nothing that was protecting anything. The digest and
    manifest-parity checks are anchored to this module's own literals, never to
    what a checkout says about itself, so WHICH release gets read is governed by
    them in both modes — see `_verified_bytes`, which this branch does not touch.

    A tighter same-tree rule (publisher mode only when the RESOLVED checkout is
    the hosting repo) was considered and rejected while implementing: it adds no
    safety for exactly the reason above, and it would break the documented
    `OPENXFACTORY_ROOT=<some other released checkout>` integration rung."""
    root = Path(repo_root) if repo_root is not None else REPO_ROOT
    if is_publisher_checkout(root):
        return CONTRACT_REF
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
