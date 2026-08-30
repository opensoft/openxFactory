from __future__ import annotations

from doc_health import pin_class


def test_provider_validation_evidence_has_one_exact_non_member_declaration() -> None:
    evidence_path = (
        "openspec/changes/add-resolved-council-seats/evidence/"
        "provider-local-validation.yaml"
    )
    declarations = tuple(
        row for row in pin_class.NON_MEMBERS if evidence_path in row.paths
    )

    assert len(declarations) == 1
    assert declarations[0].paths == (evidence_path,)
    assert pin_class.non_member_reason(evidence_path) is not None
    assert (
        pin_class.non_member_reason(evidence_path.replace("provider", "consumer"))
        is None
    )
