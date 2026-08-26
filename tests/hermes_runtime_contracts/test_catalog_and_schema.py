"""RED contract for the T006 loader, catalog, and offline schema registry."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


BASE = "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
META = "https://json-schema.org/draft/2020-12/schema"


@pytest.fixture
def api():
    return (
        importlib.import_module("scripts.hermes_runtime_validation.loader"),
        importlib.import_module("scripts.hermes_runtime_validation.catalog"),
        importlib.import_module("scripts.hermes_runtime_validation.schema_registry"),
    )


def _write_schema(root: Path, name: str, **changes: object) -> Path:
    doc: dict[str, object] = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-contract-schema",
        "$schema": META,
        "$id": BASE + name,
        "contract_id": name.removesuffix(".schema.yaml"),
        "contract_schema_version": 2,
        "type": "object",
        "additionalProperties": False,
    }
    doc.update(changes)
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _write_catalog(root: Path, paths: list[Path]) -> Path:
    entries = []
    for path in paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        entries.append(
            {
                # Keep catalog metadata complete when a negative case removes
                # the corresponding annotation from the schema under test.
                "contract_id": doc.get(
                    "contract_id", path.name.removesuffix(".schema.yaml")
                ),
                "path": path.relative_to(root).as_posix(),
                "type": "schema",
                "contract_schema_version": doc.get("contract_schema_version", 2),
                "consumers": ["openxfactory-validator"],
                "semantic_member": True,
                "release_member": True,
            }
        )
    path = root / "contract-index.yaml"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "openxfactory-hermes-runtime-contract-index",
                "contracts": entries,
            }
        ),
        encoding="utf-8",
    )
    return path


def test_json_compatible_yaml_loads_without_coercion(api, tmp_path: Path) -> None:
    loader, _, _ = api
    path = tmp_path / "valid.yaml"
    path.write_text('created_at: "2026-07-12T00:00:00Z"\nvalue: 1\n', encoding="utf-8")
    assert loader.load_yaml_document(path) == {
        "created_at": "2026-07-12T00:00:00Z",
        "value": 1,
    }


@pytest.mark.parametrize(
    "source",
    [
        "value: 1\nvalue: 2\n",
        "base: &base\n  value: 1\ncopy:\n  <<: *base\n",
        "first: &item [1]\nsecond: *item\n",
        "value: !custom tagged\n",
        "1: value\n",
        "created_at: 2026-07-12T00:00:00Z\n",
        "value: .nan\n",
        "value: .inf\n",
    ],
)
def test_non_json_or_ambiguous_yaml_is_rejected(api, tmp_path: Path, source: str) -> None:
    loader, _, _ = api
    path = tmp_path / "invalid.yaml"
    path.write_text(source, encoding="utf-8")
    with pytest.raises(loader.YamlLoadError):
        loader.load_yaml_document(path)


@pytest.mark.parametrize(
    "missing",
    ["schema_version", "kind", "$schema", "$id", "contract_id", "contract_schema_version"],
)
def test_every_schema_requires_canonical_annotations(api, tmp_path: Path, missing: str) -> None:
    _, catalog, registry = api
    schema = _write_schema(tmp_path, "shared-definitions.schema.yaml")
    doc = json.loads(schema.read_text(encoding="utf-8"))
    del doc[missing]
    schema.write_text(json.dumps(doc), encoding="utf-8")
    index = _write_catalog(tmp_path, [schema])
    with pytest.raises((catalog.CatalogError, registry.SchemaRegistryError)):
        registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))


def test_catalog_rejects_duplicate_contract_ids_and_paths(api, tmp_path: Path) -> None:
    _, catalog, _ = api
    first = _write_schema(tmp_path, "first.schema.yaml")
    second = _write_schema(tmp_path, "second.schema.yaml")
    index = _write_catalog(tmp_path, [first, second])
    doc = json.loads(index.read_text(encoding="utf-8"))
    doc["contracts"][1]["contract_id"] = doc["contracts"][0]["contract_id"]
    index.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(catalog.CatalogError):
        catalog.load_contract_catalog(index, tmp_path)

    doc["contracts"][1]["contract_id"] = "second"
    doc["contracts"][1]["path"] = doc["contracts"][0]["path"]
    index.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(catalog.CatalogError):
        catalog.load_contract_catalog(index, tmp_path)


def test_registry_rejects_noncanonical_or_duplicate_schema_ids(api, tmp_path: Path) -> None:
    _, catalog, registry = api
    first = _write_schema(tmp_path, "first.schema.yaml")
    second = _write_schema(tmp_path, "second.schema.yaml", **{"$id": BASE + "first.schema.yaml"})
    index = _write_catalog(tmp_path, [first, second])
    with pytest.raises((catalog.CatalogError, registry.SchemaRegistryError)):
        registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))

    second = _write_schema(tmp_path, "second.schema.yaml", **{"$id": "https://example.invalid/schema"})
    index = _write_catalog(tmp_path, [first, second])
    with pytest.raises((catalog.CatalogError, registry.SchemaRegistryError)):
        registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))


def test_relative_refs_close_offline_and_unregistered_refs_fail(api, tmp_path: Path) -> None:
    _, catalog, registry = api
    shared = _write_schema(
        tmp_path,
        "shared-definitions.schema.yaml",
        **{"$defs": {"scope": {"type": "string"}}},
    )
    topology = _write_schema(
        tmp_path,
        "runtime-topology.schema.yaml",
        properties={"scope": {"$ref": "shared-definitions.schema.yaml#/$defs/scope"}},
    )
    index = _write_catalog(tmp_path, [shared, topology])
    registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))

    topology = _write_schema(
        tmp_path,
        "runtime-topology.schema.yaml",
        properties={"scope": {"$ref": "missing.schema.yaml#/$defs/scope"}},
    )
    index = _write_catalog(tmp_path, [shared, topology])
    with pytest.raises(registry.SchemaRegistryError):
        registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))


def test_parent_segment_ref_alias_is_rejected(api, tmp_path: Path) -> None:
    _, catalog, registry = api
    shared = _write_schema(
        tmp_path,
        "shared-definitions.schema.yaml",
        **{"$defs": {"scope": {"type": "string"}}},
    )
    nested = _write_schema(
        tmp_path,
        "nested/runtime-topology.schema.yaml",
        contract_id="runtime-topology",
        properties={
            "scope": {"$ref": "../shared-definitions.schema.yaml#/$defs/scope"}
        },
    )
    index = _write_catalog(tmp_path, [shared, nested])

    with pytest.raises(registry.SchemaRegistryError):
        registry.build_offline_registry(catalog.load_contract_catalog(index, tmp_path))


def test_yaml_aliases_are_rejected_before_schema_registration(api, tmp_path: Path) -> None:
    loader, _, _ = api
    path = tmp_path / "aliased.schema.yaml"
    path.write_text("root: &root {type: string}\ncopy: *root\n", encoding="utf-8")
    with pytest.raises(loader.YamlLoadError):
        loader.load_yaml_document(path)


# ---- cross-family catalog members (PR #45 Copilot blocker 1) -----------------
#
# The doxBench wire schemas live in contracts/schemas/ and are catalogued from
# the family index via `../schemas/...`. The loader accepts a LEADING `..` run
# that resolves inside the repository root (two levels above the family root);
# interior traversal stays forbidden and an escape beyond the repository stays
# a CatalogError — HRC-CATALOG-INVALID semantics preserved either way.

def _family_root(tmp_path: Path) -> Path:
    family = tmp_path / "contracts" / "hermes-runtime"
    family.mkdir(parents=True)
    return family


def test_cross_family_member_paths_resolve_inside_the_repository(api, tmp_path: Path) -> None:
    _, catalog, _ = api
    family = _family_root(tmp_path)
    first = _write_schema(family, "first.schema.yaml")
    _write_schema(tmp_path / "contracts" / "schemas", "wire.schema.yaml")
    index = _write_catalog(family, [first])
    doc = json.loads(index.read_text(encoding="utf-8"))
    doc["contracts"].append({
        "contract_id": "wire", "path": "../schemas/wire.schema.yaml",
        "type": "schema", "contract_schema_version": 2,
        "consumers": ["openxfactory-validator"],
        "semantic_member": True, "release_member": True,
    })
    index.write_text(json.dumps(doc), encoding="utf-8")
    loaded = catalog.load_contract_catalog(index, family)
    assert any(entry.path == "../schemas/wire.schema.yaml"
               for entry in loaded.entries)


def test_release_only_cross_family_schema_is_not_a_hermes_semantic_schema(
    api, tmp_path: Path
) -> None:
    _, catalog, _ = api
    family = _family_root(tmp_path)
    first = _write_schema(family, "first.schema.yaml")
    wire_dir = tmp_path / "contracts" / "schemas"
    wire_dir.mkdir(parents=True)
    (wire_dir / "wire.schema.yaml").write_text(
        json.dumps({
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "wire.schema.yaml",
            "contract_schema_version": 1,
            "type": "object",
        }),
        encoding="utf-8",
    )
    index = _write_catalog(family, [first])
    doc = json.loads(index.read_text(encoding="utf-8"))
    doc["contracts"].append({
        "contract_id": "wire", "path": "../schemas/wire.schema.yaml",
        "type": "release-schema", "contract_schema_version": 1,
        "consumers": ["openxfactory-release-verifier"],
        "semantic_member": False, "release_member": True,
    })
    index.write_text(json.dumps(doc), encoding="utf-8")

    loaded = catalog.load_contract_catalog(index, family)

    assert loaded.by_id["wire"].type == "release-schema"
    assert "wire" not in {entry.contract_id for entry in loaded.schema_entries()}


def test_interior_traversal_segments_stay_forbidden(api, tmp_path: Path) -> None:
    _, catalog, _ = api
    family = _family_root(tmp_path)
    first = _write_schema(family, "first.schema.yaml")
    index = _write_catalog(family, [first])
    doc = json.loads(index.read_text(encoding="utf-8"))
    doc["contracts"][0]["path"] = "sub/../first.schema.yaml"
    index.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(catalog.CatalogError):
        catalog.load_contract_catalog(index, family)


def test_cross_family_escape_beyond_the_repository_fails_closed(api, tmp_path: Path) -> None:
    _, catalog, _ = api
    family = _family_root(tmp_path)
    first = _write_schema(family, "first.schema.yaml")
    index = _write_catalog(family, [first])
    doc = json.loads(index.read_text(encoding="utf-8"))
    doc["contracts"].append({
        "contract_id": "outside", "path": "../../../outside.schema.yaml",
        "type": "schema", "contract_schema_version": 2,
        "consumers": ["openxfactory-validator"],
        "semantic_member": True, "release_member": True,
    })
    index.write_text(json.dumps(doc), encoding="utf-8")
    (tmp_path.parent / "outside.schema.yaml").write_text("{}", encoding="utf-8")
    with pytest.raises(catalog.CatalogError):
        catalog.load_contract_catalog(index, family)
