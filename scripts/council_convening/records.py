"""The family's schema registry, whole-match identifiers, and the refusal type.

T017. Four things live here, and every other module in the package uses them:

* `load_schemas` loads every family schema plus the one digest construction the
  family takes by `$ref`, checks each against the 2020-12 metaschema, and builds
  one `referencing.Registry` keyed by `$id`, so no reference is resolved off the
  network or off a guessed path, and every `$ref` must name a loaded document
  (`references_outside`). The registry serves each document WITHOUT its
  `$schema` header (`_registered_resource`), and a document carrying `$schema`
  or `$id` BELOW its root is refused (`headers_below_root`), so the family
  validator below holds at every depth of every document.
* The VALIDATOR CLASS extends `Draft202012Validator` in exactly two places, and
  both make the reference implementation read the contract the way the contract
  is written:
    - `pattern` matches the WHOLE string. JSON Schema's regex dialect is
      ECMA-262, where `$` matches only at the end of input; Python's `$` also
      matches before a final newline, so an unextended validator would accept
      `seat-alpha` plus a newline. A pattern's closing `$` is read as `\\Z`.
    - `x-max-utf8-bytes` bounds a string in UTF-8 BYTES, which `maxLength`, a
      count of code points, cannot say (`shared-definitions.schema.yaml`).
  `format` is asserted, through a `FormatChecker` built from the explicit
  allowlist `ASSERTED_FORMATS` (only `date-time`), never from whatever optional
  libraries are installed. jsonschema registers the `date-time` checker only
  when `rfc3339-validator` is importable, and a validator that silently skipped
  calendar validity would fail OPEN, so loading fails instead; a family schema
  using any `format` outside the allowlist is refused at load for the same
  reason.
* Family YAML is read STRICTLY (`strict_yaml`): a repeated key is refused,
  never resolved.
* `check_canonicalizable` is the pre-check every digest is taken behind: a value
  `canonical.serialize` refuses is `value_not_canonicalizable`, before any digest
  exists.
* `Refused(code, member)` is the one refusal type. Its message names the code and
  the member, and NEVER the value: a refused value may be exactly the thing a
  secret detector exists to catch.

`Outcome` is the reference implementation's answer at a boundary, in the shape a
corpus vector's `expected` compares against.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, Mapping
from urllib.parse import urldefrag, urljoin

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validators as jsonschema_validators
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from ..hermes_runtime_validation.loader import YamlLoadError, load_yaml_bytes
from ..signed_execution_chain import canonical

REPO_ROOT = Path(__file__).resolve().parents[2]
FAMILY_REL = Path("contracts") / "council-convening"
DIGEST_CONSTRUCTION_REL = (
    Path("contracts") / "signed-execution-chain" / "digest-construction.schema.yaml")

ID_BASE = "https://xforge.us/schemas/openxfactory/council-convening/v1/"
SHARED_DEFINITIONS_ID = ID_BASE + "shared-definitions.schema.yaml"
DIGEST_CONSTRUCTION_ID = (
    "https://xforge.us/schemas/openxfactory/signed-execution-chain/v1/"
    "digest-construction.schema.yaml")
SCHEMA_KIND = "openxfactory-council-convening-contract-schema"
DIALECT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
UTF8_BYTES_KEYWORD = "x-max-utf8-bytes"


class Refused(Exception):
    """A refusal under the family's closed vocabulary.

    `code` is a `refusal_code` member; `member` names where it was found. The
    message carries those two and never the refused value.
    """

    def __init__(self, code: str, member: str | None = None):
        self.code = code
        self.member = member
        super().__init__(code if member is None else f"{code} at {member}")


class SchemaLoadError(Exception):
    """A harness failure: a schema that does not load, a missing file, or a
    missing dependency. Never reported as a finding (validator exit 2)."""


@dataclass(frozen=True)
class Outcome:
    """The reference implementation's answer at one boundary.

    `status_read` records whether the answer depended on a registry status, which
    the corpus's `registry_status` rule needs, and `statuses_read` which entries'
    statuses it read, in the order read (Phase 6: a selection reads the
    replacement's status too). Neither takes part in comparison.
    """

    outcome: str
    refusal: str | None = None
    findings: tuple[str, ...] = ()
    derived: Mapping[str, Any] = field(default_factory=dict)
    status_read: bool = field(default=False, compare=False)
    statuses_read: tuple[str, ...] = field(default=(), compare=False)

    def as_expected(self) -> dict[str, Any]:
        """The members a vector's `expected` compares, in its own spelling."""
        return {"outcome": self.outcome, "refusal": self.refusal,
                "findings": list(self.findings), "derived": dict(self.derived)}


# --------------------------------------------------------------------------
# The validator class: whole-match patterns and the UTF-8 byte bound.
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def whole_match(pattern: str) -> re.Pattern[str]:
    """`pattern` compiled so that a closing `$` anchors at the very end.

    A `$` preceded by an odd number of backslashes is a literal dollar and is
    left alone.

    KNOWN LIMIT: only the pattern's FINAL `$` is rewritten. A `$` inside an
    alternation, a group or a lookahead keeps Python's meaning, which also
    matches before a final newline. Two family patterns carry one, each inside a
    NEGATIVE lookahead in a pattern whose characters exclude U+000A
    (`relative_path`'s `.`/`..` segment refusal, `decimal_string`'s `-0`), where
    the extra match can only add a refusal of a string already refused.
    `tests/council_convening/test_shared_definitions.py` pins exactly those two;
    any other would need this rewrite extended first.
    """
    if pattern.endswith("$"):
        backslashes = len(pattern[:-1]) - len(pattern[:-1].rstrip("\\"))
        if backslashes % 2 == 0:
            pattern = pattern[:-1] + r"\Z"
    return re.compile(pattern)


def _pattern(validator, pattern, instance, schema) -> Iterator[ValidationError]:
    if validator.is_type(instance, "string") and not whole_match(pattern).search(instance):
        yield ValidationError("does not match the pattern, matched whole")


def _max_utf8_bytes(validator, limit, instance, schema) -> Iterator[ValidationError]:
    if validator.is_type(instance, "string"):
        # `surrogatepass`: a lone surrogate has no UTF-8 encoding, and it is the
        # canonicalizability pre-check's job, not this bound's, to refuse it.
        if len(instance.encode("utf-8", "surrogatepass")) > limit:
            yield ValidationError(f"is longer than {limit} UTF-8 bytes")


FamilyValidator = jsonschema_validators.extend(
    Draft202012Validator,
    validators={"pattern": _pattern, UTF8_BYTES_KEYWORD: _max_utf8_bytes},
)


#: The formats this family asserts, and the only ones its checker carries.
#: `FormatChecker()` with no argument asserts whatever optional libraries happen
#: to be installed (`rfc3986-validator`, `rfc3987-syntax`, `fqdn`, ...), so two
#: machines could validate the same schema differently. A family schema that
#: uses any other `format` is refused at load (`format_targets`).
ASSERTED_FORMATS = ("date-time",)


def _format_checker() -> FormatChecker:
    missing = [name for name in ASSERTED_FORMATS if name not in FormatChecker.checkers]
    if missing:
        raise SchemaLoadError(
            "jsonschema has no date-time format checker: install rfc3339-validator "
            "(requirements/hermes-runtime-contracts.lock). Without it calendar "
            "validity would be skipped, which fails open")
    return FormatChecker(formats=ASSERTED_FORMATS)


def format_targets(node: Any) -> Iterator[str]:
    """Every `format` keyword's value in a schema document, as written."""
    if isinstance(node, Mapping):
        for key, value in node.items():
            if key == "format" and isinstance(value, str):
                yield value
            else:
                yield from format_targets(value)
    elif isinstance(node, list):
        for item in node:
            yield from format_targets(item)


# --------------------------------------------------------------------------
# Loading.
# --------------------------------------------------------------------------

def strict_yaml(raw: bytes, name: str) -> Any:
    """`raw` parsed as JSON-compatible YAML, or `YamlLoadError` (a `ValueError`).

    The Hermes runtime family's fail-closed loader, reused rather than copied: a
    REPEATED KEY is refused, never resolved (a record carrying the legacy
    `protocol` and then the replacement one would otherwise classify as
    replacement), and so are aliases, anchors, merge keys, non-string keys and
    implicit timestamps. The error names the file; callers report a
    member-free message, since the loader's own text quotes the document.
    """
    return load_yaml_bytes(raw, name)


def _load_yaml(path: Path) -> Any:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SchemaLoadError(f"{path.name}: unreadable ({type(exc).__name__})") from exc
    try:
        return strict_yaml(raw, path.name)
    except YamlLoadError as exc:
        raise SchemaLoadError(f"{path.name}: does not parse as strict YAML") from exc


def _check_schema(name: str, document: Any) -> None:
    if not isinstance(document, dict):
        raise SchemaLoadError(f"{name}: is not a schema object")
    try:
        Draft202012Validator.check_schema(document)
    except jsonschema_exceptions.SchemaError as exc:
        raise SchemaLoadError(f"{name}: is not a valid 2020-12 schema") from exc


RESOURCE_HEADERS = ("$schema", "$id")


def headers_below_root(document: Any) -> list[str]:
    """Where `$schema` or `$id` appears BELOW `document`'s root, as `/`-joined
    member paths. 2020-12 allows `$schema` only at a resource root, and the
    metaschema check does not enforce it; jsonschema re-selects the validator
    class at ANY subschema that carries one, so a nested `$schema` would hand
    that subtree back to the plain dialect validator. An embedded `$id` opens a
    resource `references_outside` does not track. Both are refused at load."""
    found: list[str] = []

    def walk(node: Any, at: tuple[str, ...]) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                if at and key in RESOURCE_HEADERS:
                    found.append("/".join((*at, str(key))))
                walk(value, (*at, str(key)))
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, (*at, str(index)))

    walk(document, ())
    return found


def reference_targets(node: Any) -> Iterator[str]:
    """Every `$ref` and `$dynamicRef` string in a schema document, as written."""
    if isinstance(node, Mapping):
        for key, value in node.items():
            if key in ("$ref", "$dynamicRef") and isinstance(value, str):
                yield value
            else:
                yield from reference_targets(value)
    elif isinstance(node, list):
        for item in node:
            yield from reference_targets(item)


def references_outside(family: Mapping[str, dict], construction: dict) -> list[str]:
    """Every `$ref` (or `$dynamicRef`) in the loaded documents whose target is
    not itself a loaded document, as `name: target` lines, sorted.

    jsonschema resolves against these documents COMBINED with the bundled
    dialect metaschemas, so without this a `$ref` to a metaschema would resolve
    (and validate under the plain dialect), and one to an absent family document
    would surface only at validation time. A reference is resolved against its
    document's `$id`: no family document embeds a second `$id`, and one that did
    would need this walk to track it.
    """
    documents = {**family, DIGEST_CONSTRUCTION_REL.name: construction}
    loaded = {document["$id"] for document in documents.values()}
    problems = []
    for name, document in documents.items():
        for reference in reference_targets(document):
            target, _fragment = urldefrag(urljoin(document["$id"], reference))
            if target not in loaded:
                problems.append(f"{name}: a `$ref` names {target}")
    return sorted(problems)


def _registered_resource(name: str, document: dict) -> Resource:
    """The copy of `document` the registry serves: its `$schema` header removed.

    jsonschema re-selects the validator class from `$schema` every time it
    descends into a document (`evolve` calls `validator_for(schema,
    default=cls)`). A whole family document carries the house header, so a
    `$ref` into one used to swap `FamilyValidator` for plain
    `Draft202012Validator` for that document and everything beneath it, and
    whole-string `pattern` and `x-max-utf8-bytes` silently stopped applying: a
    record validated FAIL OPEN. With no `$schema` in what the registry serves,
    and none below any root (`headers_below_root`, refused at load),
    `validator_for` keeps the family validator at every depth.

    The header is dropped only because it names the one dialect
    `FamilyValidator` implements; any other dialect is refused here rather than
    re-read as 2020-12. The metaschema check has already run on the document as
    written, and `SchemaSet.family` keeps it as written.
    """
    declared = document.get("$schema")
    if declared is not None and declared != DIALECT_2020_12:
        raise SchemaLoadError(f"{name}: declares a dialect other than 2020-12")
    served = {key: value for key, value in document.items() if key != "$schema"}
    return Resource.from_contents(served, default_specification=DRAFT202012)


@dataclass
class SchemaSet:
    """Every family schema and the digest construction, behind one registry."""

    root: Path
    family: dict[str, dict]
    digest_construction: dict
    registry: Registry
    format_checker: FormatChecker
    _validators: dict = field(default_factory=dict, repr=False)

    @property
    def shared(self) -> dict:
        return self.family["shared-definitions.schema.yaml"]

    @property
    def definition_names(self) -> tuple[str, ...]:
        return tuple(self.shared["$defs"])

    def enum(self, definition: str) -> list[str]:
        """A closed enumeration in the shared definitions, as landed."""
        return list(self.shared["$defs"][definition]["enum"])

    def validator(self, ref: str):
        """One validator per reference, built once."""
        if ref not in self._validators:
            self._validators[ref] = FamilyValidator(
                {"$ref": ref}, registry=self.registry, format_checker=self.format_checker)
        return self._validators[ref]

    def errors(self, ref: str, instance: Any) -> list[ValidationError]:
        """Every schema error for `instance` under `ref`, in a stable order."""
        found = list(self.validator(ref).iter_errors(instance))
        return sorted(found, key=lambda error: (list(map(str, error.absolute_path)),
                                                str(error.validator)))

    def check_definition(self, name: str, value: Any) -> None:
        """The `definition` boundary: `value` alone against one shared grammar.

        The grammar first (`value_malformed`), then admissibility under
        `xfc-jcs-sha256-1` (`value_not_canonicalizable`). An unknown definition
        name is a `KeyError`, a harness error and never a refusal.
        """
        if name not in self.definition_names:
            raise KeyError(name)
        if self.errors(f"{SHARED_DEFINITIONS_ID}#/$defs/{name}", value):
            raise Refused("value_malformed", member=name)
        check_canonicalizable(value, member=name)


def load_schemas(root: Path | None = None) -> SchemaSet:
    """Load the family's schemas and the digest construction under `root`."""
    root = Path(root) if root is not None else REPO_ROOT
    family_dir = root / FAMILY_REL
    if not family_dir.is_dir():
        raise SchemaLoadError(f"{FAMILY_REL.as_posix()}: the family directory is absent")
    family: dict[str, dict] = {}
    for path in sorted(family_dir.glob("*.schema.yaml")):
        document = _load_yaml(path)
        _check_schema(path.name, document)
        if document.get("kind") != SCHEMA_KIND:
            raise SchemaLoadError(f"{path.name}: kind is not {SCHEMA_KIND}")
        if document.get("$id") != ID_BASE + path.name:
            raise SchemaLoadError(f"{path.name}: $id does not name this file")
        family[path.name] = document
    if "shared-definitions.schema.yaml" not in family:
        raise SchemaLoadError("shared-definitions.schema.yaml is absent")

    construction_path = root / DIGEST_CONSTRUCTION_REL
    if not construction_path.is_file():
        raise SchemaLoadError(
            f"{DIGEST_CONSTRUCTION_REL.as_posix()}: the digest construction is absent")
    construction = _load_yaml(construction_path)
    _check_schema(construction_path.name, construction)
    if construction.get("$id") != DIGEST_CONSTRUCTION_ID:
        raise SchemaLoadError(f"{construction_path.name}: unexpected $id")

    for name, document in [*family.items(), (construction_path.name, construction)]:
        nested = headers_below_root(document)
        if nested:
            raise SchemaLoadError(
                f"{name}: carries {nested[0].rsplit('/', 1)[-1]} below its root, at "
                f"{nested[0]}; a resource header belongs only at a document's root")
    outside = references_outside(family, construction)
    if outside:
        raise SchemaLoadError(f"{outside[0]}, outside the loaded documents")
    format_checker = _format_checker()
    for name, document in [*family.items(), (construction_path.name, construction)]:
        for fmt in format_targets(document):
            if fmt not in format_checker.checkers:
                raise SchemaLoadError(
                    f"{name}: uses format {fmt!r}, which this family's checker does "
                    f"not assert (ASSERTED_FORMATS); it would be skipped, which fails open")
    resources = [(doc["$id"], _registered_resource(name, doc))
                 for name, doc in [*family.items(), (construction_path.name, construction)]]
    registry = Registry().with_resources(resources)
    return SchemaSet(root=root, family=family, digest_construction=construction,
                     registry=registry, format_checker=format_checker)


# --------------------------------------------------------------------------
# The canonicalizability pre-check.
# --------------------------------------------------------------------------

def check_canonicalizable(value: Any, code: str = "value_not_canonicalizable",
                          member: str | None = None) -> None:
    """Refuse `value` unless `xfc-jcs-sha256-1` can serialize it.

    No non-integer number, no integer outside ±(2**53 - 1), no unpaired
    surrogate. `code` lets a later boundary name its own malformed code where
    the data model says so; the default is the shared one.
    """
    try:
        canonical.serialize(value)
    except canonical.ConstructionError:
        raise Refused(code, member=member) from None
