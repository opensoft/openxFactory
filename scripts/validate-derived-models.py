#!/usr/bin/env python3
"""Validate governed-derived-model conformance declarations (add-governed-derived-model).

The openxFactory-owned canonical validator for the kind
`xfactory_derived_model_conformance`
(`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`).
Run from the pinned openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-derived-models.py [DOMAIN_REPO_PATH]

Two layers run:

1. Packaged reference examples (`examples/derived-models/`): every
   `*/declaration.example.yaml` must pass; every
   `negative/*/declaration.yaml` must fail for its INTENDED reason
   (declared in its `# expected_failure:` header) — the self-test fails
   closed if any negative stops failing for its reason or any positive
   example fails.
2. Optional real declaration under DOMAIN_REPO_PATH at the convention
   path `models/derived-model-conformance.yaml`; absence is not a
   failure (conformance is opt-in), presence validates fully including
   template deep checks.

Deterministic checks the schema shape cannot express:
  - at least one `role: model` member per family; no duplicate member
    kinds;
  - tier `calibrated` requires `dials.calibration_writer`, never a
    member kind (writer separation);
  - identity `real_entity` requires `identity_subject_kind`, never a
    member kind (the two-object split);
  - `person_modeling: identified_persons_under_policy` requires
    `dials.person_modeling_policy` (existing path when a base dir is
    known);
  - scope `subject` requires `dials.isolation_boundary` (`per_*`);
  - template deep checks: model members carry single-value
    `authority_status: [non_authoritative]`; provenance bindings resolve;
    scenario output-status enums are exactly
    hypothesis_proposed|no_signal|discarded; access bindings resolve as
    single-value field locks or present gates.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples" / "derived-models"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
DECLARATION_CONVENTION = "models/derived-model-conformance.yaml"

TIERS = {"governed", "calibrated"}
ROLES = {"model", "scenario"}
IDENTITIES = {"synthetic", "synthetic_aggregate", "real_entity"}
SCOPES = {"domain", "subject"}
TRUTH_STORE_CLASSES = {"hermes_memory", "external_enforcement"}
PERSON_MODELING = {
    "synthetic_only",
    "aggregated_only",
    "identified_organizations_only",
    "identified_persons_under_policy",
}
PROVENANCE_FORMS = {"assumption_register", "assumptions_forbidden"}
HYPOTHESIS_VALUES = {"hypothesis_proposed", "no_signal", "discarded"}
REQUIRED_DIALS = (
    "identity",
    "scope",
    "truth_store",
    "truth_store_class",
    "promoting_authority",
    "person_modeling",
)


def _fail(findings: list[str], message: str) -> None:
    findings.append(message)


def _load_yaml(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _field(template: object, name: str) -> dict | None:
    if not isinstance(template, dict):
        return None
    fields = template.get("fields")
    if not isinstance(fields, dict):
        return None
    field = fields.get(name)
    return field if isinstance(field, dict) else None


def _field_values(template: object, name: str) -> list | None:
    field = _field(template, name)
    if field is None:
        return None
    values = field.get("values")
    return values if isinstance(values, list) else None


def _gate_present(template: object, gate: str) -> bool:
    if not isinstance(template, dict):
        return False
    gates = template.get("gates")
    if isinstance(gates, dict):
        return bool(gates.get(gate))
    if isinstance(gates, list):
        return any(isinstance(g, dict) and g.get("id") == gate for g in gates)
    return False


def _check_access_binding(
    binding: object,
    template: object | None,
    label: str,
    expect_value: str,
    context: str,
    findings: list[str],
) -> None:
    if not isinstance(binding, dict):
        return _fail(findings, f"{context}: {label} binding must be a mapping")
    if "gate" in binding:
        if template is None:
            return
        gate = binding.get("gate")
        if not isinstance(gate, str) or not _gate_present(template, gate):
            _fail(findings, f"{context}: {label} gate '{gate}' not present in template gates")
        return
    if "field" in binding:
        value = binding.get("value", expect_value)
        if value != expect_value:
            _fail(findings, f"{context}: {label} field binding value must be '{expect_value}'")
        if template is None:
            return
        values = _field_values(template, binding["field"])
        if values != [expect_value]:
            _fail(
                findings,
                f"{context}: {label} field '{binding['field']}' must be a "
                f"single-value enum [{expect_value}]",
            )
        return
    _fail(findings, f"{context}: {label} binding needs 'field' or 'gate'")


def _check_provenance(
    provenance: object, template: object | None, context: str, findings: list[str]
) -> None:
    if not isinstance(provenance, dict):
        return _fail(findings, f"{context}: model member missing provenance block")
    form = provenance.get("form")
    if form not in PROVENANCE_FORMS:
        return _fail(findings, f"{context}: provenance.form must be one of {sorted(PROVENANCE_FORMS)}")
    if form == "assumption_register":
        register_field = provenance.get("assumption_register_field")
        if not isinstance(register_field, str) or not register_field:
            return _fail(findings, f"{context}: assumption register field binding missing")
        if template is not None and _field(template, register_field) is None:
            _fail(
                findings,
                f"{context}: assumption register field '{register_field}' missing from template",
            )
        evidence_field = provenance.get("evidence_field")
        if (
            isinstance(evidence_field, str)
            and evidence_field
            and template is not None
            and _field(template, evidence_field) is None
        ):
            _fail(findings, f"{context}: evidence field '{evidence_field}' missing from template")
        return
    # assumptions_forbidden
    evidence_field = provenance.get("evidence_field")
    invented_field = provenance.get("invented_facts_field")
    if not isinstance(evidence_field, str) or not evidence_field:
        _fail(findings, f"{context}: assumptions-forbidden form needs evidence_field")
    if not isinstance(invented_field, str) or not invented_field:
        _fail(findings, f"{context}: assumptions-forbidden form needs invented_facts_field")
    if template is None:
        return
    if isinstance(evidence_field, str) and evidence_field:
        field = _field(template, evidence_field)
        if field is None:
            _fail(findings, f"{context}: evidence field '{evidence_field}' missing from template")
        elif not field.get("required") and not field.get("min_items"):
            _fail(
                findings,
                f"{context}: evidence field '{evidence_field}' must be required or min_items >= 1",
            )
    if isinstance(invented_field, str) and invented_field:
        if _field_values(template, invented_field) != ["none"]:
            _fail(
                findings,
                f"{context}: invented-facts field '{invented_field}' must be a single-value enum [none]",
            )


def validate_declaration(doc: object, base_dir: Path | None, findings: list[str]) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "declaration document is not a mapping")
    if doc.get("kind") != "xfactory_derived_model_conformance":
        return _fail(findings, "kind is not xfactory_derived_model_conformance")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    if doc.get("conforms_to") != "governed-derived-model":
        _fail(findings, "conforms_to must be governed-derived-model")
    domain = doc.get("domain")
    if not isinstance(domain, dict) or not isinstance(domain.get("id"), str) or not domain.get("id"):
        _fail(findings, "missing or empty domain.id")
    families = doc.get("families")
    if not isinstance(families, list) or not families:
        return _fail(findings, "families must be a non-empty list")
    for family in families:
        if not isinstance(family, dict):
            _fail(findings, "family entry is not a mapping")
            continue
        fid = family.get("id") if isinstance(family.get("id"), str) else "<unnamed>"
        tier = family.get("tier")
        if tier not in TIERS:
            _fail(findings, f"family {fid}: tier must be one of {sorted(TIERS)}")
        members = family.get("members")
        if not isinstance(members, list) or not members:
            _fail(findings, f"family {fid}: members must be a non-empty list")
            continue
        member_kinds: list[str] = []
        model_count = 0
        for member in members:
            if not isinstance(member, dict):
                _fail(findings, f"family {fid}: member entry is not a mapping")
                continue
            kind = member.get("kind")
            role = member.get("role")
            context = f"family {fid} member {kind if isinstance(kind, str) else '<unnamed>'}"
            if role not in ROLES:
                _fail(findings, f"{context}: role must be one of {sorted(ROLES)}")
            if not isinstance(kind, str) or not kind:
                _fail(findings, f"{context}: missing member kind")
            else:
                if kind in member_kinds:
                    _fail(findings, f"family {fid}: duplicate member kind '{kind}'")
                member_kinds.append(kind)
            if role == "model":
                model_count += 1
            template_path = member.get("template")
            template: object | None = None
            if not isinstance(template_path, str) or not template_path:
                _fail(findings, f"{context}: missing template path")
            elif base_dir is not None:
                resolved = base_dir / template_path
                if not resolved.is_file():
                    _fail(findings, f"{context}: template not found at {template_path}")
                else:
                    template = _load_yaml(resolved)
            if role == "model":
                if template is not None and _field_values(template, "authority_status") != [
                    "non_authoritative"
                ]:
                    _fail(
                        findings,
                        f"{context}: authority_status must be a single-value enum [non_authoritative]",
                    )
                _check_provenance(member.get("provenance"), template, context, findings)
            if role == "scenario":
                output_field = member.get("output_status_field")
                if not isinstance(output_field, str) or not output_field:
                    _fail(findings, f"{context}: scenario needs output_status_field")
                elif template is not None:
                    values = _field_values(template, output_field)
                    if values is None or set(values) != HYPOTHESIS_VALUES:
                        _fail(
                            findings,
                            f"{context}: output status enum '{output_field}' must be exactly "
                            f"{sorted(HYPOTHESIS_VALUES)}",
                        )
                action_bindings = member.get("action_authority")
                if not isinstance(action_bindings, list) or not action_bindings:
                    _fail(findings, f"{context}: scenario needs at least one action_authority binding")
                else:
                    for binding in action_bindings:
                        _check_access_binding(
                            binding, template, "action authority", "none", context, findings
                        )
            _check_access_binding(
                member.get("truth_store_access"),
                template,
                "truth-store access",
                "read_only",
                context,
                findings,
            )
            locks = member.get("locks")
            if isinstance(locks, list) and template is not None:
                for lock in locks:
                    if not isinstance(lock, dict) or "field" not in lock or "value" not in lock:
                        _fail(findings, f"{context}: lock entries need field and value")
                        continue
                    if _field_values(template, lock["field"]) != [lock["value"]]:
                        _fail(
                            findings,
                            f"{context}: lock field '{lock['field']}' must be a "
                            f"single-value enum [{lock['value']}]",
                        )
        if model_count == 0:
            _fail(findings, f"family {fid}: at least one role: model member is required")
        dials = family.get("dials")
        if not isinstance(dials, dict):
            _fail(findings, f"family {fid}: missing dials block")
            continue
        for dial in REQUIRED_DIALS:
            if not isinstance(dials.get(dial), str) or not dials.get(dial):
                _fail(findings, f"family {fid}: missing dial '{dial}'")
        if dials.get("identity") not in IDENTITIES:
            _fail(findings, f"family {fid}: identity must be one of {sorted(IDENTITIES)}")
        if dials.get("scope") not in SCOPES:
            _fail(findings, f"family {fid}: scope must be one of {sorted(SCOPES)}")
        if dials.get("truth_store_class") not in TRUTH_STORE_CLASSES:
            _fail(
                findings,
                f"family {fid}: truth_store_class must be one of {sorted(TRUTH_STORE_CLASSES)}",
            )
        if dials.get("person_modeling") not in PERSON_MODELING:
            _fail(findings, f"family {fid}: person_modeling must be one of {sorted(PERSON_MODELING)}")
        if dials.get("scope") == "subject":
            boundary = dials.get("isolation_boundary")
            if not isinstance(boundary, str) or not boundary.startswith("per_"):
                _fail(findings, f"family {fid}: scope subject requires isolation_boundary 'per_*'")
        if dials.get("person_modeling") == "identified_persons_under_policy":
            policy = dials.get("person_modeling_policy")
            if not isinstance(policy, str) or not policy:
                _fail(
                    findings,
                    f"family {fid}: identified_persons_under_policy requires person_modeling_policy",
                )
            elif base_dir is not None and not (base_dir / policy).is_file():
                _fail(
                    findings,
                    f"family {fid}: person_modeling_policy not found at {policy}",
                )
        if tier == "calibrated":
            writer = dials.get("calibration_writer")
            if not isinstance(writer, str) or not writer:
                _fail(findings, f"family {fid}: tier calibrated requires dials.calibration_writer")
            elif writer in member_kinds:
                _fail(
                    findings,
                    f"family {fid}: calibration_writer '{writer}' must not be a family member "
                    "(writer separation)",
                )
        if dials.get("identity") == "real_entity":
            identity_kind = family.get("identity_subject_kind")
            if not isinstance(identity_kind, str) or not identity_kind:
                _fail(
                    findings,
                    f"family {fid}: identity real_entity requires identity_subject_kind",
                )
            elif identity_kind in member_kinds:
                _fail(
                    findings,
                    f"family {fid}: identity_subject_kind '{identity_kind}' must not be a "
                    "family member (two-object split)",
                )


def _expected_failure(path: Path) -> str | None:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("# expected_failure:"):
                return stripped.split(":", 1)[1].strip()
            if stripped and not stripped.startswith("#"):
                break
    return None


def run_self_test() -> bool:
    ok = True
    positives = sorted(EXAMPLES_DIR.glob("*/declaration.example.yaml"))
    negatives = sorted(NEGATIVE_DIR.glob("*/declaration.yaml"))
    if not positives or not negatives:
        print("self-test: packaged examples missing", file=sys.stderr)
        return False
    for path in positives:
        findings: list[str] = []
        validate_declaration(_load_yaml(path), path.parent, findings)
        if findings:
            ok = False
            print(f"self-test FAIL (positive) {path.parent.name}:", file=sys.stderr)
            for finding in findings:
                print(f"  - {finding}", file=sys.stderr)
        else:
            print(f"self-test ok (positive) {path.parent.name}")
    for path in negatives:
        expected = _expected_failure(path)
        findings = []
        validate_declaration(_load_yaml(path), path.parent, findings)
        if not findings:
            ok = False
            print(
                f"self-test FAIL (negative passed unexpectedly) {path.parent.name}",
                file=sys.stderr,
            )
        elif expected and not any(expected in finding for finding in findings):
            ok = False
            print(
                f"self-test FAIL (negative failed for the wrong reason) {path.parent.name}: "
                f"expected '{expected}', got {findings}",
                file=sys.stderr,
            )
        else:
            print(f"self-test ok (negative) {path.parent.name}")
    return ok


def validate_repo(repo_path: Path) -> bool:
    declaration = repo_path / DECLARATION_CONVENTION
    if not declaration.is_file():
        print(f"no declaration at {DECLARATION_CONVENTION} — conformance not declared (ok)")
        return True
    findings: list[str] = []
    validate_declaration(_load_yaml(declaration), repo_path, findings)
    if findings:
        print(f"FAIL {declaration}:", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return False
    print(f"ok {declaration}")
    return True


def main(argv: list[str]) -> int:
    ok = run_self_test()
    if len(argv) > 1:
        repo_path = Path(argv[1]).resolve()
        if not repo_path.is_dir():
            print(f"domain repo path not found: {repo_path}", file=sys.stderr)
            return 1
        ok = validate_repo(repo_path) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
