"""Canonical membership loader for the Hermes runtime contract family."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from .loader import YamlLoadError, load_yaml_document


CATALOG_KIND = "openxfactory-hermes-runtime-contract-index"
SCHEMA_KIND = "openxfactory-hermes-runtime-contract-schema"
SCHEMA_META = "https://json-schema.org/draft/2020-12/schema"
CANONICAL_SCHEMA_BASE = "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"

_CONTRACT_ID = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$")
_MEMBER_TYPE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
_ENTRY_FIELDS = frozenset(
    {
        "contract_id",
        "path",
        "type",
        "contract_schema_version",
        "consumers",
        "semantic_member",
        "release_member",
    }
)


class CatalogError(ValueError):
    """Raised when the family catalog is incomplete, ambiguous, or unsafe."""


@dataclass(frozen=True, slots=True)
class ContractMember:
    contract_id: str
    path: str
    type: str
    contract_schema_version: int
    consumers: tuple[str, ...]
    semantic_member: bool
    release_member: bool
    absolute_path: Path


# Public compatibility name for callers which prefer catalog terminology.
CatalogEntry = ContractMember


@dataclass(frozen=True, slots=True)
class ContractCatalog:
    index_path: Path
    family_root: Path
    schema_version: int
    kind: str
    entries: tuple[ContractMember, ...]
    documents: Mapping[str, Any]
    by_id: Mapping[str, ContractMember]
    by_path: Mapping[str, ContractMember]

    def __iter__(self) -> Iterator[ContractMember]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def schema_entries(self) -> tuple[ContractMember, ...]:
        return tuple(entry for entry in self.entries if entry.type == "schema")

    def document_for(self, entry_or_path: ContractMember | str) -> Any:
        path = entry_or_path.path if isinstance(entry_or_path, ContractMember) else entry_or_path
        try:
            return self.documents[path]
        except KeyError as exc:
            raise CatalogError(f"catalog member {path!r} is not a YAML document") from exc


def _require_mapping(value: Any, context: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise CatalogError(f"{context}: mapping required")
    return value


def _require_nonempty_string(value: Any, context: str) -> str:
    if type(value) is not str or not value:
        raise CatalogError(f"{context}: non-empty string required")
    return value


def _require_positive_integer(value: Any, context: str) -> int:
    if type(value) is not int or value < 1:
        raise CatalogError(f"{context}: positive integer required")
    return value


def _normalized_member_path(value: Any, context: str) -> str:
    path = _require_nonempty_string(value, context)
    if "\\" in path or "\x00" in path:
        raise CatalogError(f"{context}: POSIX repository-relative path required")
    pure = PurePosixPath(path)
    if pure.is_absolute() or path != pure.as_posix():
        raise CatalogError(f"{context}: normalized repository-relative path required")
    # A LEADING `..` run names a cross-family member (e.g. the doxBench wire
    # schemas under contracts/schemas/, catalogued as ../schemas/...); it is
    # confined to the repository root at resolution time
    # (_contained_regular_file). INTERIOR traversal and empty segments stay
    # forbidden exactly as before.
    parts = pure.parts
    lead = 0
    while lead < len(parts) and parts[lead] == "..":
        lead += 1
    tail = parts[lead:]
    if not tail or any(part in {"", ".", ".."} for part in tail):
        raise CatalogError(f"{context}: traversal and empty path segments are forbidden")
    if any(re.fullmatch(r"[A-Za-z0-9._-]+", part) is None for part in tail):
        raise CatalogError(f"{context}: path segments contain non-canonical characters")
    return path


def _shed_destination(candidate: Path) -> Path | None:
    """`carved_reach.shed_destination()`, imported lazily and never required.

    Lazily because this package is imported by lanes that run over checkouts
    with no carve manifest at all (a domain mirror, a consumer's pinned copy);
    `None` on ImportError keeps every one of those answering exactly as before.
    """
    try:
        from carved_reach import shed_destination
    except ImportError:
        return None
    return shed_destination(candidate)


def _contained_regular_file(root: Path, member_path: str, context: str) -> Path:
    parts = PurePosixPath(member_path).parts
    candidate = root.joinpath(*parts)
    # Cross-family members (leading `..`) are confined to the REPOSITORY root
    # -- the family root's grandparent (contracts/<family> is two levels below
    # it) -- everything else stays confined to the family root. Fail closed
    # either way (HRC-CATALOG-INVALID semantics preserved).
    if parts and parts[0] == "..":
        try:
            boundary = root.parents[1]
        except IndexError as exc:
            raise CatalogError(
                f"{context}: member escapes the repository root") from exc
        escape_message = "member escapes the repository root"
    else:
        boundary = root
        escape_message = "member escapes the family root"
    # THE § 5.2 SHED (RULED (a), `#656` comment `5625573095`). Two of this
    # family's members — the workbench model-catalog and chat-turn schemas —
    # are `moved_verbatim` manifest rows: their bytes left for the openDox-spec
    # leg this repository pins, and a member row that names the pre-shed path is
    # a RETAINED CONSUMER of a moved file, which reads it from the leg. Nothing
    # is transcribed here and nothing is restored into this tree: the row says
    # where it went. `shed_destination()` answers `None` for every other root,
    # so a candidate-mode run over a domain mirror still reports the mirror's
    # own missing member as its own finding.
    #
    # ASKED UNCONDITIONALLY, not only when the local path is missing (Copilot
    # `PRRT_kwDOTAvnrs6hfEn7`): for a MOVED row the pinned leg holds the bytes
    # this repository publishes, so a file reintroduced or left stale at the
    # pre-shed path must never win over the destination the manifest declares —
    # under a "missing first" test it would be validated instead, silently. The
    # resolver already answers `None` for every path that stayed (`not_moved`,
    # including the replica and `deleted_at_carve` rows), for a path in no row
    # and for any root that is not this repository, so asking first narrows the
    # answer to exactly the rows whose destination IS authoritative.
    moved = _shed_destination(candidate)
    if moved is not None:
        candidate = moved
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise CatalogError(f"{context}: member is unavailable: {exc}") from exc
    try:
        resolved.relative_to(boundary)
    except ValueError as exc:
        raise CatalogError(f"{context}: {escape_message}") from exc
    if candidate.is_symlink() or not resolved.is_file():
        raise CatalogError(f"{context}: regular non-symlink file required")
    return resolved


def _parse_entry(raw: Any, index: int, root: Path) -> ContractMember:
    context = f"contracts[{index}]"
    doc = _require_mapping(raw, context)
    missing = _ENTRY_FIELDS - doc.keys()
    unknown = doc.keys() - _ENTRY_FIELDS
    if missing:
        raise CatalogError(f"{context}: missing fields {sorted(missing)}")
    if unknown:
        raise CatalogError(f"{context}: unknown fields {sorted(unknown)}")

    contract_id = _require_nonempty_string(doc["contract_id"], f"{context}.contract_id")
    if not _CONTRACT_ID.fullmatch(contract_id):
        raise CatalogError(f"{context}.contract_id: non-canonical contract identifier")
    path = _normalized_member_path(doc["path"], f"{context}.path")
    member_type = _require_nonempty_string(doc["type"], f"{context}.type")
    if not _MEMBER_TYPE.fullmatch(member_type):
        raise CatalogError(f"{context}.type: canonical lower-kebab member type required")
    if member_type == "schema" and not path.endswith(".schema.yaml"):
        raise CatalogError(f"{context}.path: schema members must end in .schema.yaml")
    version = _require_positive_integer(
        doc["contract_schema_version"], f"{context}.contract_schema_version"
    )

    raw_consumers = doc["consumers"]
    if type(raw_consumers) is not list or not raw_consumers:
        raise CatalogError(f"{context}.consumers: non-empty list required")
    consumers = tuple(
        _require_nonempty_string(value, f"{context}.consumers[{position}]")
        for position, value in enumerate(raw_consumers)
    )
    if len(consumers) != len(set(consumers)):
        raise CatalogError(f"{context}.consumers: duplicate consumers are forbidden")

    semantic_member = doc["semantic_member"]
    release_member = doc["release_member"]
    if type(semantic_member) is not bool or type(release_member) is not bool:
        raise CatalogError(f"{context}: semantic_member and release_member must be booleans")

    absolute_path = _contained_regular_file(root, path, context)
    return ContractMember(
        contract_id=contract_id,
        path=path,
        type=member_type,
        contract_schema_version=version,
        consumers=consumers,
        semantic_member=semantic_member,
        release_member=release_member,
        absolute_path=absolute_path,
    )


def _validate_schema_annotations(entry: ContractMember, document: Any) -> None:
    doc = _require_mapping(document, entry.path)
    required = {
        "schema_version",
        "kind",
        "$schema",
        "$id",
        "contract_id",
        "contract_schema_version",
    }
    missing = required - doc.keys()
    if missing:
        raise CatalogError(f"{entry.path}: missing schema annotations {sorted(missing)}")
    schema_version = _require_positive_integer(
        doc["schema_version"], f"{entry.path}.schema_version"
    )
    if schema_version != 1:
        raise CatalogError(f"{entry.path}.schema_version: expected 1")
    if doc["kind"] != SCHEMA_KIND:
        raise CatalogError(f"{entry.path}.kind: expected {SCHEMA_KIND!r}")
    if doc["$schema"] != SCHEMA_META:
        raise CatalogError(f"{entry.path}.$schema: Draft 2020-12 URI required")
    if doc["contract_id"] != entry.contract_id:
        raise CatalogError(f"{entry.path}: contract_id does not match catalog")
    if doc["contract_schema_version"] != entry.contract_schema_version:
        raise CatalogError(f"{entry.path}: contract_schema_version does not match catalog")


def load_contract_catalog(index_path: str | Path, family_root: str | Path) -> ContractCatalog:
    """Load and validate exact canonical contract-family membership."""

    try:
        root = Path(family_root).resolve(strict=True)
    except OSError as exc:
        raise CatalogError(f"{family_root}: family root is unavailable: {exc}") from exc
    if not root.is_dir():
        raise CatalogError(f"{root}: family root must be a directory")
    raw_index = Path(index_path)
    try:
        index = raw_index.resolve(strict=True)
    except OSError as exc:
        raise CatalogError(f"{index_path}: contract index is unavailable: {exc}") from exc
    try:
        index.relative_to(root)
    except ValueError as exc:
        raise CatalogError(f"{index}: contract index must be within the family root") from exc
    if raw_index.is_symlink() or not index.is_file():
        raise CatalogError(f"{index}: regular non-symlink contract index required")

    try:
        raw = load_yaml_document(index)
    except YamlLoadError as exc:
        raise CatalogError(str(exc)) from exc
    doc = _require_mapping(raw, str(index))
    expected_fields = {"schema_version", "kind", "contracts"}
    missing = expected_fields - doc.keys()
    unknown = doc.keys() - expected_fields
    if missing:
        raise CatalogError(f"{index}: missing fields {sorted(missing)}")
    if unknown:
        raise CatalogError(f"{index}: unknown fields {sorted(unknown)}")
    schema_version = _require_positive_integer(doc["schema_version"], f"{index}.schema_version")
    if schema_version != 1:
        raise CatalogError(f"{index}.schema_version: expected 1")
    if doc["kind"] != CATALOG_KIND:
        raise CatalogError(f"{index}.kind: expected {CATALOG_KIND!r}")
    raw_entries = doc["contracts"]
    if type(raw_entries) is not list or not raw_entries:
        raise CatalogError(f"{index}.contracts: non-empty list required")

    entries = tuple(_parse_entry(raw_entry, position, root) for position, raw_entry in enumerate(raw_entries))
    ids = [entry.contract_id for entry in entries]
    paths = [entry.path for entry in entries]
    if len(ids) != len(set(ids)):
        raise CatalogError("contract catalog contains duplicate contract_id values")
    if len(paths) != len(set(paths)):
        raise CatalogError("contract catalog contains duplicate member paths")

    documents: dict[str, Any] = {}
    for entry in entries:
        if entry.type == "schema" or entry.path.endswith((".yaml", ".yml")):
            try:
                member_doc = load_yaml_document(entry.absolute_path)
            except YamlLoadError as exc:
                raise CatalogError(str(exc)) from exc
            documents[entry.path] = member_doc
            if entry.type == "schema":
                _validate_schema_annotations(entry, member_doc)

    by_id = {entry.contract_id: entry for entry in entries}
    by_path = {entry.path: entry for entry in entries}
    return ContractCatalog(
        index_path=index,
        family_root=root,
        schema_version=schema_version,
        kind=CATALOG_KIND,
        entries=entries,
        documents=MappingProxyType(documents),
        by_id=MappingProxyType(by_id),
        by_path=MappingProxyType(by_path),
    )
