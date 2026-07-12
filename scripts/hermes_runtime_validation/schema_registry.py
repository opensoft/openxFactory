"""Draft 2020-12 registry assembled solely from canonical catalog members."""

from __future__ import annotations

from typing import Any, Iterator
from urllib.parse import unquote, urldefrag, urljoin, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from .catalog import CANONICAL_SCHEMA_BASE, ContractCatalog


class SchemaRegistryError(ValueError):
    """Raised when schemas or their offline reference graph are not canonical."""


def _iter_refs(node: Any, location: str = "$") -> Iterator[tuple[str, str]]:
    if type(node) is dict:
        for key, value in node.items():
            child = f"{location}/{key}"
            if key == "$ref":
                if type(value) is not str or not value:
                    raise SchemaRegistryError(f"{child}: non-empty string required")
                yield child, value
            else:
                yield from _iter_refs(value, child)
    elif type(node) is list:
        for index, value in enumerate(node):
            yield from _iter_refs(value, f"{location}/{index}")


def _validate_reference_shape(schema_id: str, location: str, ref: str) -> str:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc:
        raise SchemaRegistryError(
            f"{schema_id} {location}: absolute $ref values are forbidden; use a family-relative reference"
        )
    if parsed.query or "\\" in ref or unquote(ref) != ref:
        raise SchemaRegistryError(f"{schema_id} {location}: non-canonical $ref {ref!r}")
    if parsed.path:
        parts = parsed.path.split("/")
        if parsed.path.startswith("/") or any(part in {"", ".", ".."} for part in parts):
            raise SchemaRegistryError(f"{schema_id} {location}: non-canonical relative $ref {ref!r}")

    absolute = urljoin(schema_id, ref)
    target_uri, _ = urldefrag(absolute)
    if not target_uri.startswith(CANONICAL_SCHEMA_BASE):
        raise SchemaRegistryError(f"{schema_id} {location}: $ref escapes canonical schema base")
    return absolute


def _reject_nested_schema_ids(document: dict[str, Any], schema_id: str) -> None:
    """Forbid embedded resource aliases not represented by catalog membership."""

    def visit(node: Any, location: str, *, root: bool = False) -> None:
        if type(node) is dict:
            if not root and "$id" in node:
                raise SchemaRegistryError(
                    f"{schema_id} {location}/$id: nested schema IDs are forbidden; "
                    "publish a separately cataloged schema instead"
                )
            for key, value in node.items():
                visit(value, f"{location}/{key}")
        elif type(node) is list:
            for index, value in enumerate(node):
                visit(value, f"{location}/{index}")

    visit(document, "$", root=True)


def build_offline_registry(catalog: ContractCatalog) -> Registry:
    """Compile all cataloged schemas and close their reference graph offline.

    The returned ``referencing.Registry`` has no retrieval callback, so a
    missing member can never fall back to the network or local filesystem.
    """

    if not isinstance(catalog, ContractCatalog):
        raise SchemaRegistryError("ContractCatalog required")
    schema_entries = catalog.schema_entries()
    if not schema_entries:
        raise SchemaRegistryError("contract catalog contains no schema members")

    resources: list[tuple[str, Resource[Any]]] = []
    documents_by_id: dict[str, dict[str, Any]] = {}
    for entry in schema_entries:
        document = catalog.document_for(entry)
        if type(document) is not dict:
            raise SchemaRegistryError(f"{entry.path}: schema must be a mapping")
        expected_id = CANONICAL_SCHEMA_BASE + entry.path
        schema_id = document.get("$id")
        if schema_id != expected_id:
            raise SchemaRegistryError(
                f"{entry.path}: $id must be canonical {expected_id!r}, got {schema_id!r}"
            )
        if schema_id in documents_by_id:
            raise SchemaRegistryError(f"duplicate schema $id {schema_id!r}")
        _reject_nested_schema_ids(document, schema_id)
        try:
            Draft202012Validator.check_schema(document)
            resource = Resource.from_contents(document, default_specification=DRAFT202012)
        except Exception as exc:
            # ``referencing`` uses several focused exception types; normalize
            # them at this contract boundary without leaking implementation API.
            raise SchemaRegistryError(f"{entry.path}: invalid Draft 2020-12 schema: {exc}") from exc
        documents_by_id[schema_id] = document
        resources.append((schema_id, resource))

    registry: Registry = Registry().with_resources(resources)
    format_checker = FormatChecker()
    for schema_id, document in documents_by_id.items():
        # Construction fixes both the offline registry and the explicit format
        # checker used by every structural validator built from this bundle.
        Draft202012Validator(document, registry=registry, format_checker=format_checker)
        for location, ref in _iter_refs(document):
            _validate_reference_shape(schema_id, location, ref)
            try:
                registry.resolver(base_uri=schema_id).lookup(ref)
            except Exception as exc:  # referencing lookup/pointer exceptions
                raise SchemaRegistryError(
                    f"{schema_id} {location}: unresolved offline $ref {ref!r}: {exc}"
                ) from exc
    return registry
