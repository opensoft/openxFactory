"""The family's schema registry, whole-match identifiers, and the refusal type.

T017. Four things live here, and every other module in the package uses them:

* `load_schemas` loads every family schema plus the one digest construction the
  family takes by `$ref`, checks each against the 2020-12 metaschema, and builds
  one `referencing.Registry` keyed by `$id`, so no reference is resolved off the
  network or off a guessed path.
* The VALIDATOR CLASS extends `Draft202012Validator` in exactly two places, and
  both make the reference implementation read the contract the way the contract
  is written:
    - `pattern` matches the WHOLE string. JSON Schema's regex dialect is
      ECMA-262, where `$` matches only at the end of input; Python's `$` also
      matches before a final newline, so an unextended validator would accept
      `seat-alpha` plus a newline. A pattern's closing `$` is read as `\\Z`.
    - `x-max-utf8-bytes` bounds a string in UTF-8 BYTES, which `maxLength`, a
      count of code points, cannot say (`shared-definitions.schema.yaml`).
  `format` is asserted, through a `FormatChecker` that must carry `date-time`:
  jsonschema registers that checker only when `rfc3339-validator` is importable,
  and a validator that silently skipped calendar validity would fail OPEN, so
  loading fails instead.
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

import yaml
from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validators as jsonschema_validators
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

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
    the corpus's `registry_status` rule needs. It takes no part in comparison.
    """

    outcome: str
    refusal: str | None = None
    findings: tuple[str, ...] = ()
    derived: Mapping[str, Any] = field(default_factory=dict)
    status_read: bool = field(default=False, compare=False)

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


def _format_checker() -> FormatChecker:
    checker = FormatChecker()
    if "date-time" not in checker.checkers:
        raise SchemaLoadError(
            "jsonschema has no date-time format checker: install rfc3339-validator "
            "(requirements/hermes-runtime-contracts.lock). Without it calendar "
            "validity would be skipped, which fails open")
    return checker


# --------------------------------------------------------------------------
# Loading.
# --------------------------------------------------------------------------

def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise SchemaLoadError(f"{path.name}: unreadable ({type(exc).__name__})") from exc
    except yaml.YAMLError as exc:
        raise SchemaLoadError(f"{path.name}: does not parse as YAML") from exc


def _check_schema(name: str, document: Any) -> None:
    if not isinstance(document, dict):
        raise SchemaLoadError(f"{name}: is not a schema object")
    try:
        Draft202012Validator.check_schema(document)
    except jsonschema_exceptions.SchemaError as exc:
        raise SchemaLoadError(f"{name}: is not a valid 2020-12 schema") from exc


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

    resources = [(doc["$id"], Resource.from_contents(doc, default_specification=DRAFT202012))
                 for doc in [*family.values(), construction]]
    registry = Registry().with_resources(resources)
    return SchemaSet(root=root, family=family, digest_construction=construction,
                     registry=registry, format_checker=_format_checker())


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
