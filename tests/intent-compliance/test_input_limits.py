from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts.intent_compliance import input_io
from scripts.intent_compliance.discovery import bounded_record_paths
from scripts.intent_compliance.model import (
    InputLimitError,
    RecordDocument,
    bounded_yaml_text,
    load_record_documents,
    load_single_mapping_text,
    regular_file_size,
)
from scripts.intent_compliance.schema_validation import (
    schema_findings,
    schema_validators,
)

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "contracts" / "intent-compliance"


def test_inputs_when_aggregate_bytes_exceed_budget_then_rejected(tmp_path: Path) -> None:
    # Given
    paths: list[Path] = []
    for index in range(5):
        path = tmp_path / f"bytes-{index}.yaml"
        path.write_text("kind: compliance_decision\npadding: " + "x" * 900_000)
        paths.append(path)

    # When / Then
    with pytest.raises(InputLimitError, match="aggregate input exceeds"):
        load_record_documents(paths)


def test_inputs_when_aggregate_documents_exceed_budget_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    paths: list[Path] = []
    documents = "\n---\n".join("kind: compliance_decision" for _ in range(64))
    for index in range(5):
        path = tmp_path / f"documents-{index}.yaml"
        path.write_text(documents)
        paths.append(path)

    # When / Then
    with pytest.raises(InputLimitError, match="aggregate document count exceeds"):
        load_record_documents(paths)


def test_inputs_when_aggregate_nodes_exceed_budget_then_rejected(tmp_path: Path) -> None:
    # Given
    paths: list[Path] = []
    document = "items:\n" + "  - null\n" * 9_990
    for index in range(11):
        path = tmp_path / f"nodes-{index}.yaml"
        path.write_text(document)
        paths.append(path)

    # When / Then
    with pytest.raises(InputLimitError, match="aggregate node count exceeds"):
        load_record_documents(paths)


def test_input_when_depth_exceeds_budget_then_rejected_before_construction(
    tmp_path: Path,
) -> None:
    path = tmp_path / "deep.yaml"
    path.write_text("value: " + "[" * 33 + "null" + "]" * 33)

    with pytest.raises(InputLimitError, match="exceeds depth"):
        load_record_documents([path])


def test_input_when_nodes_exceed_budget_then_rejected_before_construction(
    tmp_path: Path,
) -> None:
    path = tmp_path / "many-nodes.yaml"
    path.write_text("items:\n" + "  - null\n" * 10_001)

    with pytest.raises(InputLimitError, match="exceeds 10000 nodes"):
        load_record_documents([path])


def test_discovery_when_eligible_inputs_exceed_budget_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    for index in range(257):
        (tmp_path / f"record-{index}.yaml").write_text("kind: compliance_decision\n")

    # When / Then
    with pytest.raises(InputLimitError, match="eligible input count exceeds"):
        bounded_record_paths(tmp_path)


def test_discovery_when_unrelated_files_exceed_scan_cap_then_rejected(
    tmp_path: Path,
) -> None:
    for index in range(1_025):
        (tmp_path / f"unrelated-{index}.txt").write_text("ignored")

    with pytest.raises(InputLimitError, match="discovery entry count exceeds"):
        bounded_record_paths(tmp_path)


def test_discovery_when_repository_has_many_unrelated_yaml_files_then_ignores_them(
    tmp_path: Path,
) -> None:
    for index in range(300):
        (tmp_path / f"workflow-{index}.yaml").write_text(
            "name: build\non: push\njobs: {}\n", encoding="utf-8"
        )

    assert bounded_record_paths(tmp_path) == []


@pytest.mark.parametrize(
    "content",
    [
        'schema_version: 1\nkind: "compliance_decision"\n',
        "{schema_version: 1, kind: compliance_decision}\n",
        "padding: " + "x" * 5_000 + "\nkind: compliance_decision\n",
    ],
)
def test_discovery_when_governed_kind_is_valid_yaml_then_path_is_eligible(
    tmp_path: Path, content: str
) -> None:
    path = tmp_path / "record.yaml"
    path.write_text(content, encoding="utf-8")

    assert bounded_record_paths(tmp_path) == [path]


def test_discovery_when_flow_yaml_breaks_after_governed_kind_then_path_is_eligible(
    tmp_path: Path,
) -> None:
    path = tmp_path / "record.yaml"
    path.write_text("{kind: compliance_decision, bad: [}", encoding="utf-8")

    assert bounded_record_paths(tmp_path) == [path]


def test_discovery_when_target_ancestor_is_named_examples_then_record_is_eligible(
    tmp_path: Path,
) -> None:
    target = tmp_path / "examples" / "consumer"
    target.mkdir(parents=True)
    path = target / "record.yaml"
    path.write_text("kind: compliance_decision\n", encoding="utf-8")

    assert bounded_record_paths(target) == [path]


@pytest.mark.parametrize(
    "content",
    [
        "kind_value: &kind_value compliance_decision\nkind: *kind_value\n",
        "kind_key: &kind_key kind\n*kind_key: compliance_decision\n",
        "base: &base\n  kind: compliance_decision\n<<: *base\n",
        "base: &base\n  kind: compliance_decision\n!!merge '<<': *base\n",
    ],
)
def test_discovery_when_root_kind_can_be_supplied_by_alias_then_path_is_eligible(
    tmp_path: Path, content: str
) -> None:
    path = tmp_path / "record.yaml"
    path.write_text(content, encoding="utf-8")

    assert bounded_record_paths(tmp_path) == [path]


def test_discovery_when_target_is_absent_then_rejected(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(InputLimitError, match="target does not exist"):
        bounded_record_paths(missing)


def test_regular_file_when_absent_then_preserves_missing_input_diagnostic(
    tmp_path: Path,
) -> None:
    with pytest.raises(InputLimitError, match="input does not exist"):
        regular_file_size(tmp_path / "missing.yaml")


def test_regular_file_when_fstat_fails_then_descriptor_is_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    closed: list[int] = []

    def fail_fstat(descriptor: int) -> os.stat_result:
        raise OSError(descriptor, "fstat failed")

    monkeypatch.setattr(input_io, "_open_without_symlinks", lambda _: 47)
    monkeypatch.setattr(input_io.os, "fstat", fail_fstat)
    monkeypatch.setattr(input_io.os, "close", closed.append)

    with pytest.raises(InputLimitError, match="regular file"):
        input_io._open_regular(Path("record.yaml"))

    assert closed == [47]


@pytest.mark.parametrize(
    "value",
    ["2026-01-01", "!!binary SGVsbG8=", "!!set {restricted: null}"],
)
def test_input_when_yaml_constructs_non_json_type_then_rejected(
    tmp_path: Path, value: str
) -> None:
    path = tmp_path / "non-json.yaml"
    path.write_text(f"kind: compliance_decision\nvalue: {value}\n")

    with pytest.raises(InputLimitError, match="JSON-native"):
        load_record_documents([path])


def test_single_mapping_when_constructor_fails_then_error_is_wrapped(
    tmp_path: Path,
) -> None:
    source = tmp_path / "authority.yaml"

    with pytest.raises(InputLimitError, match="duplicate YAML key"):
        load_single_mapping_text("kind: first\nkind: second\n", source)


def test_single_mapping_when_duplicate_key_contains_secret_then_error_redacts_it(
    tmp_path: Path,
) -> None:
    source = tmp_path / "authority.yaml"
    secret = "sk_live_abcdefghijklmnopqrstuvwxyz123456"

    with pytest.raises(InputLimitError) as captured:
        load_single_mapping_text(f"{secret}: first\n{secret}: second\n", source)

    assert secret not in str(captured.value)


def test_single_mapping_when_yaml_tag_contains_secret_then_error_redacts_it(
    tmp_path: Path,
) -> None:
    source = tmp_path / "authority.yaml"
    secret = "sk_live_abcdefghijklmnopqrstuvwxyz123456"

    with pytest.raises(InputLimitError) as captured:
        load_single_mapping_text(f"kind: !{secret} value\n", source)

    assert secret not in str(captured.value)


def test_schema_when_invalid_value_contains_secret_then_diagnostic_redacts_it() -> None:
    secret = "sk_live_abcdefghijklmnopqrstuvwxyz123456"
    document = RecordDocument(
        Path("candidate.yaml"),
        {"schema_version": 1, "kind": "compliance_decision", "outcome": secret},
    )

    findings = schema_findings(document, schema_validators(FAMILY))

    assert findings
    assert all(secret not in finding.message for finding in findings)
    assert all(len(finding.message) <= 256 for finding in findings)


def test_input_when_path_is_replaced_by_symlink_after_preflight_then_rejected(
    tmp_path: Path,
) -> None:
    path = tmp_path / "record.yaml"
    target = tmp_path / "target.yaml"
    path.write_text("kind: compliance_decision\n", encoding="utf-8")
    target.write_text("kind: policy_allowance\n", encoding="utf-8")
    size = regular_file_size(path)
    path.unlink()
    path.symlink_to(target)

    with pytest.raises(InputLimitError, match="regular file"):
        bounded_yaml_text(path, size=size)


def test_input_when_parent_is_replaced_by_symlink_after_preflight_then_rejected(
    tmp_path: Path,
) -> None:
    parent = tmp_path / "parent"
    replacement = tmp_path / "replacement"
    parent.mkdir()
    replacement.mkdir()
    path = parent / "record.yaml"
    path.write_text("kind: compliance_decision\n", encoding="utf-8")
    (replacement / "record.yaml").write_text(
        "kind: policy_allowance\n", encoding="utf-8"
    )
    size = regular_file_size(path)
    parent.rename(tmp_path / "original-parent")
    parent.symlink_to(replacement, target_is_directory=True)

    with pytest.raises(InputLimitError, match="regular file"):
        bounded_yaml_text(path, size=size)


def test_discovery_when_root_is_symlink_then_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    root = tmp_path / "root"
    root.symlink_to(target, target_is_directory=True)

    with pytest.raises(InputLimitError, match="must not be a symlink"):
        bounded_record_paths(root)


def test_discovery_when_yaml_path_is_fifo_then_rejected(tmp_path: Path) -> None:
    fifo = tmp_path / "record.yaml"
    os.mkfifo(fifo)

    with pytest.raises(InputLimitError, match="regular file"):
        bounded_record_paths(tmp_path)
