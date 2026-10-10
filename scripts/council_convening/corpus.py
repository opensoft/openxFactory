"""The conformance corpus: index closure, raw-byte digests, adjudication, coverage.

T019, per contracts/conformance-corpus.md (feature 035). The corpus is shared by
three independent implementations, and this module is the provider's: it reads
the index, verifies every vector's bytes, joins `$parts`, dispatches each vector
to the handler for its `boundary`, and compares the reference implementation's
answer with the vector's `expected`, exactly.

WHAT IS CHECKED, AND UNDER WHICH CODE.

* `council-convening-index-closure`: the index in both directions. Every file
  under `conformance/` except `index.json` is a row and every row's file exists;
  rows are in bytewise UTF-8 path order; `case_id` is unique and equals its
  file's basename under `vectors/<area>/`; every row agrees with its vector;
  the totals recount; the index carries no member the format does not have.
* `council-convening-index-digest`: a row's `sha256` is not the SHA-256 of the
  file's RAW BYTES.
* `council-convening-schema`: a vector breaks the vector format, or its JSON byte
  form (no byte-order mark, LF only, exactly one trailing newline), or carries
  inputs its boundary cannot take.
* `council-convening-vector-outcome-mismatch`: the reference implementation's
  outcome, refusal, findings or `derived` differ from `expected`, or no handler
  exists for the vector's boundary at this commit.
* `council-convening-vector-registry-status-missing`: the answer read a registry
  status and the vector carries no `registry_status` override for it.
* `council-convening-vector-identity-map-missing`: from Phase 5, a vector whose
  boundary reads the repository identity map (`binding`, `registration`,
  `admission`) carries no `repository_identity` oracle. Such a vector is not
  adjudicated: its outcome would depend on a map no digest covers.
* `council-convening-refusal-code-without-probe`,
  `council-convening-finding-code-without-probe` and
  `council-convening-requirement-without-probe`: coverage AT THE COMMIT. Every
  member of `refusal_code` and `finding_code` as landed, and every requirement
  in the index's `coverage_floor`, needs a vector.

JSON IS READ STRICTLY. A repeated member name, or `NaN` or `Infinity`, is
refused rather than resolved, because two readers that resolved them differently
would disagree on what a vector says. For the same reason a corpus file carries
no integral number spelled as a float (`2.0`, `2e0`; `IntegralFloatToken`).

THE DISPATCH TABLE. Phase 1 registers `definition` and `classification`,
Phase 2 `commission` (handled in `resolution`), Phase 3 `admission`, once, for
both its input roles (the commission record, through `resolution`, and the
snapshot half), Phase 5 `binding` (data-model E10), and Phase 4
`registration`, `return` and `completion` (over `signing`). Each later phase
registers its boundaries through `register_handler`, naming the oracles its
vectors may carry.

THE FIXTURES (Phase 5). The index's `fixtures` lists every corpus-owned fixture
with its raw SHA-256, in bytewise path order, under the same closure: a file
under `conformance/` is a `cases` row or a `fixtures` row. The one fixture is the
frozen identity map, `fixtures/repository-identity.json` (round 7, R7-M1): the
map text every map-reading vector carries, so no vector's outcome depends on the
live `contracts/policies/repository-identity.yaml`.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from . import binding, classification, records

CONFORMANCE_REL = records.FAMILY_REL / "conformance"
INDEX_NAME = "index.json"
INDEX_KIND = "openxfactory-council-convening-conformance-index"
VECTOR_KIND = "openxfactory-council-convening-conformance-vector"
CORPUS_ID = "council-convening-conformance"

AREAS = ("foundation", "resolution", "assignment", "signing", "binding", "migration")
BOUNDARIES = ("definition", "classification", "commission", "admission", "registration",
              "return", "completion", "binding", "selection", "activation", "historical")
OUTCOMES = ("accept", "refuse", "route")
SIDES = ("producer", "consumer")
ORIGINS = ("hand", "generated")
ORACLES = ("governed_history", "governed", "governed_repositories", "rules", "facts",
           "live_heads", "head_refs", "resolved_candidate", "issued", "identity",
           "repository_identity", "registry_status")

INDEX_MEMBERS = ("schema_version", "kind", "corpus_id", "protocol", "coverage_floor",
                 "cases", "totals", "fixtures")
FIXTURE_ROW_MEMBERS = ("name", "path", "sha256")
FIXTURE_KIND = "openxfactory-council-convening-conformance-fixture"
FIXTURE_MEMBERS = ("schema_version", "kind", "name", "text")
#: The corpus-owned fixtures, closed: name to path relative to `conformance/`.
FIXTURES = {"repository-identity": "fixtures/repository-identity.json"}
IDENTITY_FIXTURE = FIXTURES["repository-identity"]

#: The boundaries whose vectors read the repository identity map, and so must
#: carry the `repository_identity` oracle (contracts/conformance-corpus.md):
#: `binding`; `registration`, which runs E10 at E7 step 5; and `admission`, which
#: runs E10 as E2 steps A1 and A4 (T055). At `admission` only the commission
#: record's role reads it: the snapshot half (`inputs.snapshot`, data-model E4)
#: judges no binding, so it reads no map (`reads_identity_map`).
IDENTITY_MAP_BOUNDARIES = ("binding", "registration", "admission")


def reads_identity_map(vector: Mapping[str, Any]) -> bool:
    """Whether `vector`'s adjudication reads the repository identity map."""
    if vector.get("boundary") not in IDENTITY_MAP_BOUNDARIES:
        return False
    inputs = vector.get("inputs")
    return not (vector["boundary"] == "admission" and isinstance(inputs, Mapping)
                and "snapshot" in inputs)
ROW_MEMBERS = ("case_id", "area", "boundary", "applies_to", "requirement_ids", "path",
               "sha256", "expected")
ROW_FROM_VECTOR = ("case_id", "area", "boundary", "applies_to", "requirement_ids",
                   "expected")
TOTALS_MEMBERS = ("by_area", "by_outcome", "both_sides", "vectors")
VECTOR_REQUIRED = ("schema_version", "kind", "case_id", "area", "boundary",
                   "applies_to", "requirement_ids", "evaluation_time", "inputs",
                   "expected")
VECTOR_OPTIONAL = ("environment",)
EXPECTED_MEMBERS = ("outcome", "refusal", "findings", "derived", "derived_origin")

REQUIREMENT_ID = re.compile(r"(FR-0(0[1-9]|1[0-2])|SC-00[1-4])\Z")
CASE_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}\Z")
PARTS = "$parts"


@dataclass(frozen=True)
class Finding:
    """One validator finding. `message` names members and paths, never values."""

    severity: str
    code: str
    message: str

    def line(self) -> str:
        label = "ERROR" if self.severity == "ERROR" else "WARN "
        return f"{label} [{self.code}] {self.message}"


def _error(code: str, message: str) -> Finding:
    return Finding("ERROR", code, message)


class PartsError(ValueError):
    """A malformed `$parts` sentinel."""


class VectorInputError(ValueError):
    """A vector whose inputs its boundary cannot take: a malformed vector."""


class NotAdjudicable(LookupError):
    """A vector the reference implementation cannot answer at this commit."""


# --------------------------------------------------------------------------
# Bytes: the deterministic form, raw digests and strict reading.
# --------------------------------------------------------------------------

def dump_json(value: Any) -> bytes:
    """The corpus's deterministic JSON: sorted members, two-space indentation,
    ASCII with escapes, LF, exactly one trailing newline (R18)."""
    text = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                      allow_nan=False)
    return (text + "\n").encode("ascii")


def raw_sha256(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _refuse_constant(name: str) -> Any:
    raise ValueError(f"{name} is not JSON")


def _refuse_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("a member name is repeated")
        result[key] = value
    return result


class IntegralFloatToken(ValueError):
    """A corpus number spelled with a fraction or an exponent whose value is an
    integer (`2.0`, `2e0`). Readers split on it: jsonschema's `integer` accepts
    `2.0`, `xfc-jcs-sha256-1` refuses it as a non-integer number, and a reader
    whose numbers are all doubles cannot tell it from `2`. The corpus carries no
    such token rather than pin one reading."""

    MESSAGE = ("carries a number spelled with a fraction or an exponent whose value "
               "is an integer; readers disagree whether it is one")

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)


def _corpus_float(token: str) -> float:
    value = float(token)
    if value.is_integer():
        raise IntegralFloatToken()
    return value


def loads_strict(text: str, *, corpus_tokens: bool = False) -> Any:
    """Parse JSON refusing repeated member names, `NaN` and `Infinity`. With
    `corpus_tokens`, as for every corpus file, an integral number spelled as a
    float is refused too (`IntegralFloatToken`)."""
    return json.loads(text, object_pairs_hook=_refuse_duplicates,
                      parse_constant=_refuse_constant,
                      parse_float=_corpus_float if corpus_tokens else float)


def byte_form_problem(raw: bytes) -> str | None:
    """What is wrong with a corpus file's byte form, or None."""
    if raw.startswith(b"\xef\xbb\xbf"):
        return "starts with a byte-order mark"
    if b"\r" in raw:
        return "carries a carriage return; line endings are LF only"
    if not raw.endswith(b"\n"):
        return "does not end with a newline"
    if raw.endswith(b"\n\n"):
        return "ends with more than one newline"
    return None


# --------------------------------------------------------------------------
# The `$parts` sentinel.
# --------------------------------------------------------------------------

def join_parts(value: Any) -> Any:
    """Replace every `{"$parts": [...]}` with the concatenation of its parts.

    The sentinel is exactly one member, a non-empty list of strings. Any other
    object carrying `$parts` is malformed, never silently half-joined.
    """
    if isinstance(value, dict):
        if PARTS in value:
            parts = value[PARTS]
            if len(value) != 1:
                raise PartsError("a $parts object carries another member")
            if (not isinstance(parts, list) or not parts
                    or not all(isinstance(part, str) for part in parts)):
                raise PartsError("$parts is not a non-empty list of strings")
            return "".join(parts)
        return {key: join_parts(item) for key, item in value.items()}
    if isinstance(value, list):
        return [join_parts(item) for item in value]
    return value


def _contains_parts(value: Any) -> bool:
    if isinstance(value, dict):
        return PARTS in value or any(_contains_parts(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_parts(item) for item in value)
    return False


# --------------------------------------------------------------------------
# The dispatch table.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Context:
    schemas: records.SchemaSet
    registry: classification.Registry


Handler = Callable[[Mapping[str, Any], Context], records.Outcome]


@dataclass(frozen=True)
class Boundary:
    handler: Handler
    oracles: frozenset[str]


HANDLERS: dict[str, Boundary] = {}


def register_handler(boundary: str, handler: Handler, oracles: Iterable[str] = ()) -> None:
    """Register the adjudicator for `boundary`, and the oracles its vectors may
    carry. A later phase's module calls this for its own boundaries."""
    if boundary not in BOUNDARIES:
        raise ValueError(f"{boundary!r} is not a corpus boundary")
    unknown = set(oracles) - set(ORACLES)
    if unknown:
        raise ValueError(f"unknown oracle(s) {sorted(unknown)}")
    HANDLERS[boundary] = Boundary(handler, frozenset(oracles))


def _closed_inputs(inputs: Any, members: tuple[str, ...]) -> Mapping[str, Any]:
    if not isinstance(inputs, dict) or set(inputs) != set(members):
        raise VectorInputError(f"inputs must be exactly {{{', '.join(members)}}}")
    return inputs


def _definition(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    inputs = _closed_inputs(vector["inputs"], ("definition", "value"))
    name = inputs["definition"]
    if not isinstance(name, str) or name not in context.schemas.definition_names:
        raise VectorInputError("inputs.definition names no shared definition")
    value = join_parts(inputs["value"])
    try:
        context.schemas.check_definition(name, value)
    except records.Refused as refused:
        return records.Outcome("refuse", refused.code)
    return records.Outcome("accept")


def _statuses(environment: Mapping[str, Any], context: Context) -> dict[str, str] | None:
    overrides = environment.get("registry_status")
    if overrides is None:
        return None
    if not isinstance(overrides, dict) or not overrides:
        raise VectorInputError("environment.registry_status is not a non-empty object")
    for protocol_id, status in overrides.items():
        try:
            entry = context.registry.entry(protocol_id)
        except KeyError:
            raise VectorInputError(
                "environment.registry_status names no registry entry") from None
        if status not in classification.ROLE_STATUSES.get(entry.get("role"), ()):
            raise VectorInputError(
                "environment.registry_status gives an entry a status outside its role")
    return overrides


def _classification(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    inputs = _closed_inputs(vector["inputs"], ("record", "selected_protocol"))
    record = join_parts(inputs["record"])
    if not isinstance(record, dict):
        raise VectorInputError("inputs.record is not an object")
    kind = record.get("kind")
    if isinstance(kind, str) and kind in classification.JUDGED_BY_KIND_KINDS:
        raise VectorInputError(
            "inputs.record is a kind judged by kind, which is never classified")
    selected = inputs["selected_protocol"]
    if selected is not None and selected not in context.registry.entries:
        raise VectorInputError("inputs.selected_protocol names no registry entry")
    statuses = _statuses(vector.get("environment", {}), context)
    try:
        return classification.classify_and_select(record, selected, context.registry,
                                                  statuses)
    except classification.EffectNotLanded as exc:
        raise NotAdjudicable(str(exc)) from None


def _binding(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    """The `binding` boundary, data-model E10 steps 1 to 14 (Phase 5). The map is
    the vector's own `repository_identity` oracle, materialized under a
    temporary root, never the live file (R7-M1)."""
    inputs = _closed_inputs(vector["inputs"], ("binding", "operation", "governed"))
    if inputs["operation"] not in binding.OPERATIONS:
        raise VectorInputError("inputs.operation is not commission or seat_execution")
    if not isinstance(inputs["governed"], dict):
        raise VectorInputError("inputs.governed is not an object")
    joined = dict(vector)
    joined["inputs"] = join_parts(vector["inputs"])
    joined["environment"] = join_parts(vector.get("environment", {}))
    try:
        outcome, code = binding.evaluate_vector(joined, schemas=context.schemas)
    except ValueError as exc:
        raise VectorInputError(f"the binding vector cannot be run: {exc}") from None
    return records.Outcome(outcome, code)


register_handler("definition", _definition)
register_handler("classification", _classification, oracles=("registry_status",))
register_handler("binding", _binding,
                 oracles=("identity", "repository_identity", "governed_history"))

# Phase 2 (T032): the commission record's two boundaries (data-model E2). The
# handler lives in `resolution`, which imports this module only inside the
# handler, so the registration here closes no import cycle.
from . import resolution as _resolution  # noqa: E402

register_handler("commission", _resolution.corpus_handler, oracles=_resolution.ORACLES_READ)
# `admission` is registered once, below, by Phase 3 (T040): one handler for its
# two input roles, the commission record (this handler, with retry identity at
# E2 step A3) and the snapshot half (E4).


# --------------------------------------------------------------------------
# Phase 4 (T048): `registration`, `return` and `completion` (data-model E7, E8).
# --------------------------------------------------------------------------

from . import signing  # noqa: E402  (signing imports records and classification only)


def _selected(inputs: Mapping[str, Any], context: Context) -> str | None:
    selected = inputs["selected_protocol"]
    if selected is not None and selected not in context.registry.entries:
        raise VectorInputError("inputs.selected_protocol names no registry entry")
    return selected


def _object(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise VectorInputError(f"{name} is not an object")
    return value


def _snapshot(value: Any, context: Context) -> Mapping[str, Any]:
    """A signing vector's frozen snapshot, which must be one E4 accepts (Phase
    3's `check_snapshot`, steps 2 to 7): the consumer froze it, so a snapshot E4
    refuses, or one whose instants do not parse, cannot be run, and is a
    schema finding rather than a refusal or a traceback."""
    from . import assignments as _assignments

    snapshot = _object(value, "inputs.snapshot")
    if not isinstance(snapshot.get("assignments"), list):
        raise VectorInputError("inputs.snapshot carries no list of assignments")
    try:
        _assignments.check_snapshot(snapshot, context.schemas)
    except records.Refused as refused:
        raise VectorInputError(f"inputs.snapshot is not a frozen snapshot E4 accepts "
                               f"({refused.code} at {refused.member})") from None
    except (KeyError, TypeError, ValueError):
        raise VectorInputError("inputs.snapshot is not a frozen snapshot E4 can "
                               "judge") from None
    return snapshot


def _signed(call, selected: str | None, context: Context) -> records.Outcome:
    """Run one signing boundary and say its answer as an `Outcome`. A refusal
    under a legacy selection is classification's, which read the legacy
    status; nothing later can run under a legacy selection."""
    status_read = selected is not None and selected == context.registry.legacy_id
    try:
        derived = call()
    except signing.Routed as routed:
        return routed.outcome
    except records.Refused as refused:
        return records.Outcome("refuse", refused.code, status_read=status_read)
    except classification.EffectNotLanded as exc:
        raise NotAdjudicable(str(exc)) from None
    except (signing.InconsistentEnvironment, KeyError, TypeError, ValueError) as exc:
        raise VectorInputError(f"the vector's inputs or oracles are inconsistent "
                               f"({type(exc).__name__}: {exc})") from None
    return records.Outcome("accept", derived=derived)


def _registration(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    inputs = join_parts(_closed_inputs(vector["inputs"], (
        "registration", "snapshot", "bindings", "selected_protocol")))
    environment = join_parts(dict(vector.get("environment", {})))
    _statuses(environment, context)
    selected = _selected(inputs, context)
    if not isinstance(inputs["bindings"], list):
        raise VectorInputError("inputs.bindings is not a list")
    snapshot = _snapshot(inputs["snapshot"], context)
    return _signed(lambda: signing.check_registration(
        inputs["registration"], snapshot=snapshot, bindings=inputs["bindings"],
        environment=environment, evaluation_time=vector["evaluation_time"],
        selected_protocol=selected, schemas=context.schemas, registry=context.registry),
        selected, context)


def _return(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    inputs = join_parts(_closed_inputs(vector["inputs"], (
        "return", "snapshot", "selected_protocol")))
    environment = join_parts(dict(vector.get("environment", {})))
    _statuses(environment, context)
    selected = _selected(inputs, context)
    snapshot = _snapshot(inputs["snapshot"], context)
    return _signed(lambda: signing.check_return(
        inputs["return"], snapshot=snapshot, environment=environment,
        evaluation_time=vector["evaluation_time"], selected_protocol=selected,
        schemas=context.schemas, registry=context.registry), selected, context)


def _completion(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    inputs = join_parts(_closed_inputs(vector["inputs"], ("snapshot", "returns")))
    snapshot = _snapshot(inputs["snapshot"], context)
    returns = inputs["returns"]
    if not isinstance(returns, list) or not all(isinstance(r, dict) for r in returns):
        raise VectorInputError("inputs.returns is not a list of records")
    # The `rules`, `governed` and `governed_history` oracles a completion vector
    # may carry are never read: completion follows the frozen snapshot, so a
    # rule changed after freezing changes nothing (US2 scenario 4). The vector
    # carries them, the changed rule at the governed tip, to show exactly that.
    return _signed(lambda: signing.check_completion(
        snapshot, returns, environment=vector.get("environment")), None, context)


register_handler("registration", _registration, oracles=(
    "issued", "identity", "repository_identity", "governed_history", "registry_status"))
register_handler("return", _return, oracles=("issued", "registry_status"))
register_handler("completion", _completion, oracles=("rules", "governed", "governed_history"))


# --------------------------------------------------------------------------
# The vector format.
# --------------------------------------------------------------------------

def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def vector_format_problems(schemas: records.SchemaSet, vector: Any) -> list[str]:
    """Every way `vector` breaks the vector format, as messages without values."""
    if not isinstance(vector, dict):
        return ["is not a JSON object"]
    problems: list[str] = []
    members = set(vector)
    missing = [m for m in VECTOR_REQUIRED if m not in members]
    unknown = sorted(members - set(VECTOR_REQUIRED) - set(VECTOR_OPTIONAL))
    if missing:
        problems.append(f"lacks {', '.join(missing)}")
    if unknown:
        problems.append(f"carries members the format does not have: {', '.join(unknown)}")
    if not (_is_int(vector.get("schema_version")) and vector.get("schema_version") == 1):
        problems.append("schema_version is not 1")
    if vector.get("kind") != VECTOR_KIND:
        problems.append(f"kind is not {VECTOR_KIND}")
    case_id = vector.get("case_id")
    if not isinstance(case_id, str) or not CASE_ID.match(case_id):
        problems.append("case_id is not a corpus case identifier")
    if vector.get("area") not in AREAS:
        problems.append("area is not a corpus area")
    if vector.get("boundary") not in BOUNDARIES:
        problems.append("boundary is not a corpus boundary")
    applies_to = vector.get("applies_to")
    if (not isinstance(applies_to, list) or not applies_to
            or applies_to != [side for side in SIDES if side in applies_to]):
        problems.append("applies_to is not a non-empty, ordered subset of [producer, consumer]")
    requirement_ids = vector.get("requirement_ids")
    if (not isinstance(requirement_ids, list) or not requirement_ids
            or len(set(map(str, requirement_ids))) != len(requirement_ids)
            or not all(isinstance(r, str) and REQUIREMENT_ID.match(r)
                       for r in requirement_ids)):
        problems.append("requirement_ids is not a non-empty list of distinct FR/SC ids")
    if "evaluation_time" in vector:
        try:
            schemas.check_definition("utc_instant", vector["evaluation_time"])
        except records.Refused:
            problems.append("evaluation_time is not a utc_instant")
    if "inputs" in vector and not isinstance(vector["inputs"], dict):
        problems.append("inputs is not an object")
    if "environment" in vector:
        environment = vector["environment"]
        if not isinstance(environment, dict) or not environment:
            problems.append("environment is present but not a non-empty object")
        else:
            strange = sorted(set(environment) - set(ORACLES))
            if strange:
                problems.append(f"environment names no oracle the format has: "
                                f"{', '.join(strange)}")
            boundary = HANDLERS.get(vector.get("boundary"))
            if boundary is not None:
                unused = sorted(set(environment) & set(ORACLES) - boundary.oracles)
                if unused:
                    problems.append(f"environment carries oracles boundary "
                                    f"{vector.get('boundary')} does not use: "
                                    f"{', '.join(unused)}")
    problems.extend(_expected_problems(schemas, vector.get("expected")))
    outside = {key: value for key, value in vector.items()
               if key not in ("inputs", "environment")}
    if _contains_parts(outside):
        problems.append("a $parts object appears outside inputs and environment")
    return problems


def _expected_problems(schemas: records.SchemaSet, expected: Any) -> list[str]:
    if not isinstance(expected, dict):
        return ["expected is not an object"]
    problems: list[str] = []
    if set(expected) != set(EXPECTED_MEMBERS):
        problems.append(f"expected is not exactly {{{', '.join(EXPECTED_MEMBERS)}}}")
        return problems
    outcome, refusal, findings = expected["outcome"], expected["refusal"], expected["findings"]
    if outcome not in OUTCOMES:
        problems.append("expected.outcome is not accept, refuse or route")
    refusal_codes = schemas.enum("refusal_code")
    finding_codes = schemas.enum("finding_code")
    if outcome == "refuse":
        if refusal not in refusal_codes:
            problems.append("expected.refusal is not in refusal_code as landed")
    elif refusal is not None:
        problems.append("expected.refusal is set on an outcome that is not refuse")
    if (not isinstance(findings, list)
            or not all(isinstance(f, str) and f in finding_codes for f in findings)
            or len(set(findings)) != len(findings)):
        problems.append("expected.findings is not a list of distinct finding_code members")
    elif outcome == "route" and not findings:
        problems.append("expected.findings is empty on a route")
    elif outcome != "route" and findings:
        problems.append("expected.findings is not empty on an outcome that is not route")
    if not isinstance(expected["derived"], dict):
        problems.append("expected.derived is not an object")
    if expected["derived_origin"] not in ORIGINS:
        problems.append("expected.derived_origin is not hand or generated")
    return problems


def adjudicate(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    """The reference implementation's answer to one well-formed vector."""
    boundary = HANDLERS.get(vector["boundary"])
    if boundary is None:
        raise NotAdjudicable(f"no handler for boundary {vector['boundary']} at this commit")
    return boundary.handler(vector, context)


# --------------------------------------------------------------------------
# The index.
# --------------------------------------------------------------------------

def _path_order(path: str) -> bytes:
    return path.encode("utf-8")


def totals_for(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    by_area: dict[str, int] = {}
    by_outcome: dict[str, int] = {}
    for row in rows:
        by_area[row["area"]] = by_area.get(row["area"], 0) + 1
        outcome = row["expected"]["outcome"]
        by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
    return {
        "by_area": by_area,
        "by_outcome": by_outcome,
        "both_sides": sum(1 for row in rows if row["applies_to"] == list(SIDES)),
        "vectors": len(rows),
    }


def build_index(entries: Iterable[tuple[str, bytes, Mapping[str, Any]]],
                coverage_floor: Iterable[str], protocol: str,
                fixtures: Iterable[tuple[str, str, bytes]] = ()) -> dict[str, Any]:
    """The index for `(path, raw bytes, vector)` entries and `(name, path, raw
    bytes)` fixtures, paths relative to `conformance/`."""
    rows = []
    for path, raw, vector in sorted(entries, key=lambda entry: _path_order(entry[0])):
        row = {member: vector[member] for member in ROW_FROM_VECTOR}
        row["path"] = path
        row["sha256"] = raw_sha256(raw)
        rows.append(row)
    return {
        "schema_version": 1,
        "kind": INDEX_KIND,
        "corpus_id": CORPUS_ID,
        "protocol": protocol,
        "coverage_floor": list(coverage_floor),
        "cases": rows,
        "totals": totals_for(rows),
        "fixtures": [{"name": name, "path": path, "sha256": raw_sha256(raw)}
                     for name, path, raw in sorted(fixtures,
                                                   key=lambda f: _path_order(f[1]))],
    }


def corpus_files(conformance: Path) -> list[str]:
    """Every file under `conformance/` except the index, relative and POSIX."""
    if not conformance.is_dir():
        return []
    found = []
    for path in conformance.rglob("*"):
        if path.is_file():
            relative = path.relative_to(conformance).as_posix()
            if relative != INDEX_NAME:
                found.append(relative)
    return sorted(found, key=_path_order)


@dataclass
class CorpusReport:
    findings: list[Finding] = field(default_factory=list)
    corpus_id: str | None = None
    protocol: str | None = None
    index_sha256: str | None = None
    vectors: int = 0
    both_sides: int = 0
    totals: dict[str, Any] = field(default_factory=dict)
    adjudicated: tuple[int, int] = (0, 0)
    refusals_probed: tuple[int, int] = (0, 0)
    findings_probed: tuple[int, int] = (0, 0)
    requirements_probed: tuple[int, int] = (0, 0)
    coverage_floor: list[str] = field(default_factory=list)


def adjudication_findings(label: str, vector: Mapping[str, Any],
                          context: Context) -> tuple[list[Finding], bool]:
    """The findings for adjudicating one WELL-FORMED vector, and whether the
    reference reproduced its expectation. Shared by the corpus check and by
    `check` on a single vector, so the two can never judge a vector differently.
    """
    if (reads_identity_map(vector)
            and "repository_identity" not in vector.get("environment", {})):
        # Phase 5: not adjudicated, because its outcome would depend on a map
        # no digest covers (R7-M1).
        return [_error(
            "council-convening-vector-identity-map-missing",
            f"{label}: boundary {vector['boundary']} reads the repository identity "
            f"map, and the vector carries no repository_identity oracle")], False
    try:
        outcome = adjudicate(vector, context)
    except (VectorInputError, PartsError) as exc:
        return [_error("council-convening-schema", f"{label}: {exc}")], False
    except NotAdjudicable as exc:
        return [_error("council-convening-vector-outcome-mismatch", f"{label}: {exc}")], False
    findings: list[Finding] = []
    want = {k: vector["expected"][k] for k in ("outcome", "refusal", "findings", "derived")}
    got = outcome.as_expected()
    matched = got == want
    if not matched:
        findings.append(_error(
            "council-convening-vector-outcome-mismatch",
            f"{label}: expected {_summary(want)}, the reference gives {_summary(got)}"))
    if outcome.status_read:
        overrides = vector.get("environment", {}).get("registry_status") or {}
        if context.registry.legacy_id not in overrides:
            findings.append(_error(
                "council-convening-vector-registry-status-missing",
                f"{label}: the outcome reads the legacy entry's status, and the "
                f"vector carries no registry_status override for it"))
    return findings, matched


def index_problems(index: Any, registry: classification.Registry) -> list[str]:
    """Every way `index` breaks the index FORMAT, as messages without values.
    Its closure against a tree (rows, files, digests, totals) is `check_corpus`'s."""
    if not isinstance(index, dict):
        return ["the index is not a JSON object"]
    problems = []
    members = set(index)
    if members != set(INDEX_MEMBERS):
        missing = [m for m in INDEX_MEMBERS if m not in members]
        unknown = sorted(members - set(INDEX_MEMBERS))
        if missing:
            problems.append(f"the index lacks {', '.join(missing)}")
        if unknown:
            problems.append(f"the index carries members the format does not have: "
                            f"{', '.join(unknown)}")
    if not (_is_int(index.get("schema_version")) and index.get("schema_version") == 1):
        problems.append("the index's schema_version is not 1")
    if index.get("kind") != INDEX_KIND:
        problems.append(f"the index's kind is not {INDEX_KIND}")
    if index.get("corpus_id") != CORPUS_ID:
        problems.append(f"the index's corpus_id is not {CORPUS_ID}")
    if index.get("protocol") != registry.replacement_id:
        problems.append("the index's protocol is not the registry's replacement")
    floor = index.get("coverage_floor")
    if (not isinstance(floor, list)
            or not all(isinstance(r, str) and REQUIREMENT_ID.match(r) for r in floor)
            or len(set(floor)) != len(floor)):
        problems.append("the index's coverage_floor is not a list of distinct FR/SC ids")
    if not isinstance(index.get("cases"), list):
        problems.append("the index's cases is not a list")
    if not isinstance(index.get("fixtures"), list):
        problems.append("the index's fixtures is not a list")
    totals = index.get("totals")
    if not isinstance(totals, dict) or set(totals) != set(TOTALS_MEMBERS):
        problems.append(f"the index's totals is not exactly {{{', '.join(TOTALS_MEMBERS)}}}")
    return problems


def check_corpus(root: Path | None = None, schemas: records.SchemaSet | None = None,
                 registry: classification.Registry | None = None) -> CorpusReport:
    """Check the corpus under `root` and adjudicate every vector.

    A schema or registry that does not load raises `records.SchemaLoadError`,
    the harness failure; every other problem is a finding in the report.
    """
    root = Path(root) if root is not None else records.REPO_ROOT
    schemas = schemas if schemas is not None else records.load_schemas(root)
    registry = registry if registry is not None else classification.load_registry(root)
    context = Context(schemas, registry)
    report = CorpusReport()
    findings = report.findings
    conformance = root / CONFORMANCE_REL
    index_path = conformance / INDEX_NAME

    def closure(message: str) -> None:
        findings.append(_error("council-convening-index-closure", message))

    if not index_path.is_file():
        closure(f"{CONFORMANCE_REL.as_posix()}/{INDEX_NAME} is absent")
        return report
    index_raw = index_path.read_bytes()
    report.index_sha256 = raw_sha256(index_raw)
    form = byte_form_problem(index_raw)
    if form:
        closure(f"{INDEX_NAME} {form}")
    try:
        index = loads_strict(index_raw.decode("utf-8"), corpus_tokens=True)
    except IntegralFloatToken as exc:
        closure(f"{INDEX_NAME} {exc}")
        return report
    except (UnicodeDecodeError, ValueError):
        closure(f"{INDEX_NAME} does not parse as strict JSON")
        return report
    for problem in index_problems(index, registry):
        closure(problem)
    if not isinstance(index, dict) or not isinstance(index.get("cases"), list):
        return report
    report.corpus_id = index.get("corpus_id")
    report.protocol = index.get("protocol")
    floor = index.get("coverage_floor") if isinstance(index.get("coverage_floor"), list) else []
    report.coverage_floor = [r for r in floor if isinstance(r, str)]

    rows = [row for row in index["cases"] if isinstance(row, dict)]
    if len(rows) != len(index["cases"]):
        closure("a row of cases is not an object")
    report.vectors = len(rows)
    paths = [row.get("path") for row in rows]
    if any(not isinstance(path, str) for path in paths):
        closure("a row's path is not a string")
    string_paths = [path for path in paths if isinstance(path, str)]
    if string_paths != sorted(string_paths, key=_path_order):
        closure("rows are not in bytewise UTF-8 order of path")
    if len(set(string_paths)) != len(string_paths):
        closure("a path is indexed twice")
    case_ids = [row.get("case_id") for row in rows]
    if len(set(map(str, case_ids))) != len(case_ids):
        closure("a case_id is repeated")
    fixture_paths = _check_fixtures(index, conformance, findings, closure)
    on_disk = corpus_files(conformance)
    for path in on_disk:
        if path not in string_paths and path not in fixture_paths:
            closure(f"{path} is under conformance/ and not indexed")

    vectors: list[Mapping[str, Any]] = []
    adjudicated_ok = 0
    for row in rows:
        unknown = sorted(set(row) - set(ROW_MEMBERS))
        missing = [m for m in ROW_MEMBERS if m not in row]
        if unknown or missing:
            closure(f"row {row.get('case_id')!s}: is not exactly the row members")
        path = row.get("path")
        if not isinstance(path, str):
            continue
        file = conformance / path
        if not file.is_file():
            closure(f"{path} is indexed and absent")
            continue
        raw = file.read_bytes()
        if row.get("sha256") != raw_sha256(raw):
            findings.append(_error("council-convening-index-digest",
                                   f"{path}: the row's sha256 is not the file's raw bytes"))
        form = byte_form_problem(raw)
        if form:
            findings.append(_error("council-convening-schema", f"{path} {form}"))
        try:
            vector = loads_strict(raw.decode("utf-8"), corpus_tokens=True)
        except IntegralFloatToken as exc:
            findings.append(_error("council-convening-schema", f"{path} {exc}"))
            continue
        except (UnicodeDecodeError, ValueError):
            findings.append(_error("council-convening-schema",
                                   f"{path} does not parse as strict JSON"))
            continue
        problems = vector_format_problems(schemas, vector)
        for problem in problems:
            findings.append(_error("council-convening-schema", f"{path}: {problem}"))
        if problems:
            continue
        vectors.append(vector)
        if path != f"vectors/{vector['area']}/{vector['case_id']}.json":
            closure(f"{path}: is not vectors/<area>/<case_id>.json for its own case")
        for member in ROW_FROM_VECTOR:
            if row.get(member) != vector.get(member):
                closure(f"{path}: the row's {member} disagrees with the vector")
        found, matched = adjudication_findings(path, vector, context)
        findings.extend(found)
        adjudicated_ok += matched
    report.adjudicated = (adjudicated_ok, len(rows))

    try:
        recount = totals_for(rows)
    except (KeyError, TypeError):
        recount = None
    if recount is None or index.get("totals") != recount:
        closure("the index's totals do not recount from its rows")
    report.totals = index.get("totals") if isinstance(index.get("totals"), dict) else {}
    report.both_sides = sum(1 for row in rows if row.get("applies_to") == list(SIDES))

    refusal_codes = schemas.enum("refusal_code")
    finding_codes = schemas.enum("finding_code")
    probed_refusals = {v["expected"]["refusal"] for v in vectors}
    probed_findings = {f for v in vectors for f in v["expected"]["findings"]}
    cited = {r for v in vectors for r in v["requirement_ids"]}
    for code in refusal_codes:
        if code not in probed_refusals:
            findings.append(_error("council-convening-refusal-code-without-probe",
                                   f"refusal code {code} has no vector"))
    for code in finding_codes:
        if code not in probed_findings:
            findings.append(_error("council-convening-finding-code-without-probe",
                                   f"finding code {code} has no vector"))
    for requirement in report.coverage_floor:
        if requirement not in cited:
            findings.append(_error("council-convening-requirement-without-probe",
                                   f"coverage_floor requirement {requirement} is cited "
                                   f"by no vector"))
    report.refusals_probed = (sum(c in probed_refusals for c in refusal_codes),
                              len(refusal_codes))
    report.findings_probed = (sum(c in probed_findings for c in finding_codes),
                              len(finding_codes))
    report.requirements_probed = (sum(r in cited for r in report.coverage_floor),
                                  len(report.coverage_floor))
    return report


def _check_fixtures(index: Mapping[str, Any], conformance: Path,
                    findings: list[Finding], closure: Callable[[str], None]) -> set[str]:
    """Check the index's `fixtures` rows and the files they name. Returns the
    paths the rows name, for the closure."""
    rows = index.get("fixtures")
    if not isinstance(rows, list):
        return set()
    paths: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != set(FIXTURE_ROW_MEMBERS):
            closure("a fixtures row is not exactly {name, path, sha256}")
            continue
        name, path = row["name"], row["path"]
        if not isinstance(path, str) or FIXTURES.get(name) != path:
            closure("a fixtures row names no corpus fixture at its own path")
            continue
        paths.append(path)
        file = conformance / path
        if not file.is_file():
            closure(f"{path} is indexed and absent")
            continue
        raw = file.read_bytes()
        if row["sha256"] != raw_sha256(raw):
            findings.append(_error("council-convening-index-digest",
                                   f"{path}: the row's sha256 is not the file's raw bytes"))
        form = byte_form_problem(raw)
        if form:
            findings.append(_error("council-convening-schema", f"{path} {form}"))
        try:
            fixture = loads_strict(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            findings.append(_error("council-convening-schema",
                                   f"{path} does not parse as strict JSON"))
            continue
        if (not isinstance(fixture, dict) or set(fixture) != set(FIXTURE_MEMBERS)
                or not (_is_int(fixture.get("schema_version"))
                        and fixture["schema_version"] == 1)
                or fixture.get("kind") != FIXTURE_KIND or fixture.get("name") != name
                or not isinstance(fixture.get("text"), str)):
            findings.append(_error(
                "council-convening-schema",
                f"{path}: is not a corpus fixture {{schema_version: 1, kind: "
                f"{FIXTURE_KIND}, name, text}} named as its row"))
    if paths != sorted(paths, key=_path_order) or len(set(paths)) != len(paths):
        closure("fixtures rows are not in bytewise UTF-8 order of path, or repeat one")
    return set(paths)


def _summary(expected: Mapping[str, Any]) -> str:
    """An outcome in words, naming codes and the classification only."""
    text = str(expected.get("outcome"))
    if expected.get("refusal"):
        text += f" {expected['refusal']}"
    if expected.get("findings"):
        text += f" [{', '.join(expected['findings'])}]"
    derived = expected.get("derived") or {}
    if derived:
        text += f" with derived {sorted(derived)}"
        if "classification" in derived:
            text += f" (classification {derived['classification']})"
    return text


# --------------------------------------------------------------------------
# Phase 3 (T040): the snapshot half of `admission`.
# --------------------------------------------------------------------------

from . import assignments  # noqa: E402  (registered below the dispatch table)


def _selected_protocol(inputs: Mapping[str, Any], context: Context) -> str | None:
    selected = inputs["selected_protocol"]
    if selected is not None and selected not in context.registry.entries:
        raise VectorInputError("inputs.selected_protocol names no registry entry")
    return selected


def _admission_snapshot(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    """A snapshot judged in the E4 order (data-model E4): classification, then
    `snapshot_malformed`, `assignment_malformed`, `digest_construction_mismatch`,
    `assignment_set_mismatch`, `assignment_duplicate`, `assignment_shared_holder`."""
    inputs = _closed_inputs(vector["inputs"], ("snapshot", "selected_protocol"))
    snapshot = join_parts(inputs["snapshot"])
    if not isinstance(snapshot, dict):
        raise VectorInputError("inputs.snapshot is not an object")
    selected = _selected_protocol(inputs, context)
    statuses = _statuses(vector.get("environment", {}), context)
    try:
        return assignments.snapshot_outcome(snapshot, selected_protocol=selected,
                                            schemas=context.schemas,
                                            registry=context.registry,
                                            statuses=statuses)
    except classification.EffectNotLanded as exc:
        raise NotAdjudicable(str(exc)) from None


def _admission(vector: Mapping[str, Any], context: Context) -> records.Outcome:
    """`admission` takes one of two input roles: `snapshot`, the snapshot half
    (E4), or `record`, the commission record in the E2 admission order, with
    retry identity at step A3 (`resolution`)."""
    inputs = vector["inputs"]
    if isinstance(inputs, dict) and "snapshot" in inputs:
        return _admission_snapshot(vector, context)
    return _resolution.corpus_handler(vector, context)


register_handler("admission", _admission, oracles=_resolution.ADMISSION_ORACLES_READ)
