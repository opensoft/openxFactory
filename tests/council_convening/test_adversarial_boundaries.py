from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.council_convening_validation.models import (
    BooleanEqualsPredicate,
    ConditionalRule,
    GovernedRule,
    HarnessError,
    RelativePath,
    ResolverInput,
)
from scripts.council_convening_validation.provenance import (
    ProvenanceRefused,
    evaluate_provenance,
)
from scripts.council_convening_validation.yaml_io import load_yaml
from tests.council_convening.support import (
    mapping_at,
    valid_convening,
    validation_keywords,
)


@pytest.mark.parametrize(
    "rule_path",
    [
        r"C:\Users\brett\rules.yaml",
        "C:/Users/brett/rules.yaml",
        r"\\server\share\rules.yaml",
        r"rules\..\private.yaml",
        "/rules/ordinary.yaml",
        "rules/../private.yaml",
    ],
)
def test_governed_rule_path_rejects_non_portable_paths(rule_path: str) -> None:
    document = valid_convening()
    mapping_at(document, "required_seats_provenance", "governed_rule")["path"] = (
        rule_path
    )

    assert "pattern" in validation_keywords(document)


def test_invalid_utf8_is_a_deterministic_encoding_error(tmp_path: Path) -> None:
    document = tmp_path / "invalid-utf8.yaml"
    _ = document.write_bytes(b"kind: \xff\n")

    with pytest.raises(HarnessError) as caught:
        _ = load_yaml(document, RelativePath("invalid-utf8.yaml"))

    assert caught.value.finding.code == "CC-DOCUMENT-ENCODING"


@pytest.mark.parametrize("contents", ["scalar\n", "2026-08-29\n"])
def test_non_mapping_yaml_root_is_a_deterministic_shape_error(
    tmp_path: Path,
    contents: str,
) -> None:
    document = tmp_path / "non-mapping.yaml"
    _ = document.write_text(contents, encoding="utf-8")

    with pytest.raises(HarnessError) as caught:
        _ = load_yaml(document, RelativePath("non-mapping.yaml"))

    assert caught.value.finding.code == "CC-YAML-SHAPE"


def test_duplicate_yaml_keys_are_rejected(tmp_path: Path) -> None:
    document = tmp_path / "duplicate-key.yaml"
    _ = document.write_text("kind: expected\nkind: overwritten\n", encoding="utf-8")

    with pytest.raises(HarnessError) as caught:
        _ = load_yaml(document, RelativePath("duplicate-key.yaml"))

    assert caught.value.finding.code == "CC-YAML-SHAPE"


@pytest.mark.parametrize(
    "contents",
    [
        "base: &base {key: one}\ntarget: {<<: *base, key: two}\n",
        "container:\n  base: &base {key: one}\n  target:\n    <<: *base\n    key: two\n",
        (
            "left: &left {key: one}\n"
            "right: &right {other: two}\n"
            "target:\n  <<: [*left, *right]\n  key: two\n"
        ),
    ],
)
def test_conflicting_yaml_merge_keys_are_rejected(
    tmp_path: Path,
    contents: str,
) -> None:
    document = tmp_path / "conflicting-merge-key.yaml"
    _ = document.write_text(contents, encoding="utf-8")

    with pytest.raises(HarnessError) as caught:
        _ = load_yaml(document, RelativePath("conflicting-merge-key.yaml"))

    assert caught.value.finding.code == "CC-YAML-SHAPE"


def test_repeated_literal_yaml_merge_keys_are_rejected(tmp_path: Path) -> None:
    document = tmp_path / "repeated-merge-key.yaml"
    _ = document.write_text(
        """left: &left {first: one}
right: &right {second: two}
target:
  <<: *left
  <<: *right
""",
        encoding="utf-8",
    )

    with pytest.raises(HarnessError) as caught:
        _ = load_yaml(document, RelativePath("repeated-merge-key.yaml"))

    assert caught.value.finding.code == "CC-YAML-SHAPE"


@pytest.mark.parametrize(
    "contents",
    [
        "base: &base {inherited: one}\ntarget: {<<: *base, local: two}\n",
        (
            "left: &left {first: one}\n"
            "right: &right {second: two}\n"
            "container:\n  target: {<<: [*left, *right], local: three}\n"
        ),
        "base: &base {key: one}\ncopy: *base\n",
    ],
)
def test_non_conflicting_yaml_merge_keys_are_accepted(
    tmp_path: Path,
    contents: str,
) -> None:
    document = tmp_path / "non-conflicting-merge-key.yaml"
    _ = document.write_text(contents, encoding="utf-8")

    loaded = load_yaml(document, RelativePath("non-conflicting-merge-key.yaml"))

    assert loaded


def _run_isolated_yaml_loader(document: Path) -> subprocess.CompletedProcess[str]:
    program = (
        "from pathlib import Path; "
        "from scripts.council_convening_validation.models import HarnessError, RelativePath; "
        "from scripts.council_convening_validation.yaml_io import load_yaml; "
        f"target=Path({str(document)!r}); "
        "\ntry:\n load_yaml(target, RelativePath(target.name))\n"
        "except HarnessError as error:\n print(error.finding.code); raise SystemExit(2)\n"
        "print('ACCEPT')"
    )
    return subprocess.run(
        [sys.executable, "-c", program],
        cwd=Path.cwd(),
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )


@pytest.mark.parametrize(
    "contents",
    [
        "root: &root\n  self: *root\n",
        "root: " + "{key: " * 1200 + "value" + "}" * 1200 + "\n",
    ],
)
def test_recursive_yaml_is_a_bounded_shape_error(
    tmp_path: Path,
    contents: str,
) -> None:
    document = tmp_path / "recursive.yaml"
    _ = document.write_text(contents, encoding="utf-8")

    result = _run_isolated_yaml_loader(document)

    assert result.returncode == 2
    assert result.stdout == "CC-YAML-SHAPE\n"
    assert result.stderr == ""


def _resolver(
    *,
    standing_seats: tuple[str, ...],
    duplicate_condition: bool = False,
) -> ResolverInput:
    conditional = ConditionalRule(
        seat="company-policy",
        condition_ref="pull-in-company-policy",
        predicate=BooleanEqualsPredicate(
            fact="touches_company_policy",
            expected=True,
        ),
    )
    return ResolverInput(
        candidate_head="0123456789abcdef0123456789abcdef01234567",
        governed_rule=GovernedRule(
            repository="example/governed-rules",
            path="candidate-classes/ordinary.yaml",
            revision="89abcdef0123456789abcdef0123456789abcdef",
            matched_class="ordinary-change",
            standing_seats=standing_seats,
            conditional_seats=(conditional, conditional)
            if duplicate_condition
            else (conditional,),
        ),
    )


def test_duplicate_authoritative_standing_seats_are_refused() -> None:
    document = valid_convening()
    result = evaluate_provenance(
        document,
        _resolver(standing_seats=("domain-policy", "client-interest", "domain-policy")),
        RelativePath("duplicate-standing.yaml"),
    )

    assert result == ProvenanceRefused("standing_seat_drift")


def test_duplicate_identical_condition_evaluations_are_refused() -> None:
    document = valid_convening()
    result = evaluate_provenance(
        document,
        _resolver(
            standing_seats=("domain-policy", "client-interest"),
            duplicate_condition=True,
        ),
        RelativePath("duplicate-condition.yaml"),
    )

    assert result == ProvenanceRefused("condition_result_drift")
