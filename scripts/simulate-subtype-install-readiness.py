#!/usr/bin/env python3
"""Simulate install/run readiness for every xFactory intake subtype."""

from __future__ import annotations

import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
XFACTORY_ROOT = ROOT.parent
TEMPLATE_DIR = ROOT / "templates" / "intake"
OUT_DIR = ROOT / "examples" / "intake-runtime-simulations"

REPORT_PASS1 = ROOT / "docs" / "intake-subtype-install-readiness-report.md"
REPORT_RUNBOOK = ROOT / "docs" / "intake-subtype-install-runbook.md"
REPORT_PASS2 = ROOT / "docs" / "intake-subtype-second-pass-gap-report.md"

RUNTIME_GAPS = [
    "deployment_target_unbound",
    "hermes_runtime_unbound",
    "omnigent_runtime_unbound",
    "secret_provider_unbound",
    "credential_bindings_unbound",
    "adapter_endpoints_unbound",
    "approvers_unresolved",
    "runtime_validation_not_run",
    "dry_run_not_run",
    "live_approval_missing",
]

PASS2_REMAINING_GAPS = [
    "domain_sme_confirmation_required",
    "workflow_semantics_confirmation_required",
    "credential_scope_confirmation_required",
    "adapter_implementation_or_package_required",
    "deployment_target_unbound",
    "hermes_runtime_unbound",
    "omnigent_runtime_unbound",
    "secret_provider_unbound",
    "credential_bindings_unbound",
    "adapter_endpoints_unbound",
    "approvers_unresolved",
    "runtime_validation_not_run",
    "dry_run_not_run",
    "live_approval_missing",
]


@dataclass(frozen=True)
class RepoState:
    repo: str
    path: Path
    exists: bool
    has_stack: bool
    has_validator: bool
    has_agent_mixes: bool
    has_credential_requirements: bool
    declared_credential_ids: set[str]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def repo_state(repo: str) -> RepoState:
    path = XFACTORY_ROOT / repo
    exists = path.exists() and path.is_dir()
    req_path = path / "credentials" / "requirements.yaml"
    declared_ids: set[str] = set()
    if req_path.exists():
        req_doc = load_yaml(req_path)
        requirements = req_doc.get("requirements")
        if isinstance(requirements, list):
            declared_ids = {
                str(item.get("id"))
                for item in requirements
                if isinstance(item, dict) and item.get("id")
            }
    return RepoState(
        repo=repo,
        path=path,
        exists=exists,
        has_stack=(path / "stack.yaml").exists(),
        has_validator=(path / "scripts" / "validate-domain-factory.py").exists(),
        has_agent_mixes=(path / "hermes" / "domain" / "agent-mixes.yaml").exists(),
        has_credential_requirements=req_path.exists(),
        declared_credential_ids=declared_ids,
    )


def file_exists_any(base: Path, candidates: list[str]) -> bool:
    return any((base / candidate).exists() for candidate in candidates)


def load_templates() -> dict[str, dict[str, Any]]:
    index = load_yaml(TEMPLATE_DIR / "index.yaml")
    templates: dict[str, dict[str, Any]] = {}
    for entry in index.get("templates") or []:
        if not isinstance(entry, dict):
            continue
        template_id = str(entry.get("id"))
        file_name = str(entry.get("file"))
        templates[template_id] = load_yaml(TEMPLATE_DIR / file_name)
    return templates


def simulate_passes() -> tuple[dict[str, Any], dict[str, Any]]:
    templates = load_templates()
    catalog = load_yaml(TEMPLATE_DIR / "subtypes" / "catalog.yaml")
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    pass1_groups: list[dict[str, Any]] = []
    pass2_groups: list[dict[str, Any]] = []

    for group in catalog.get("catalog") or []:
        template_id = str(group["template_id"])
        repo = str(group["recommended_factory_repo"])
        state = repo_state(repo)
        template = templates.get(template_id, {})
        template_credential_ids = {
            str(item.get("id"))
            for item in template.get("credential_families") or []
            if isinstance(item, dict) and item.get("id")
        }

        pass1_subtypes: list[dict[str, Any]] = []
        pass2_subtypes: list[dict[str, Any]] = []

        for subtype in group.get("subtypes") or []:
            subtype_id = str(subtype["id"])
            profile_file = f"profiles/{slug(subtype_id)}.yaml"
            workflows = [str(item) for item in subtype.get("starter_workflows") or []]
            credentials = [str(item) for item in subtype.get("credential_families") or []]
            adapters = [str(item) for item in subtype.get("adapter_families") or []]

            domain_gaps: list[str] = []
            missing_workflow_specs: list[str] = []
            missing_adapter_contracts: list[str] = []
            missing_repo_credentials: list[str] = []
            missing_template_credential_details: list[str] = []

            if not state.exists:
                domain_gaps.append("factory_repo_missing")
            else:
                if not state.has_stack:
                    domain_gaps.append("stack_yaml_missing")
                if not state.has_validator:
                    domain_gaps.append("domain_validator_missing")
                if not state.has_agent_mixes:
                    domain_gaps.append("hermes_agent_mixes_missing")
                if not state.has_credential_requirements:
                    domain_gaps.append("credential_requirements_file_missing")
                if not (state.path / profile_file).exists():
                    domain_gaps.append("subtype_profile_missing")

            for workflow_id in workflows:
                if not state.exists or not file_exists_any(
                    state.path,
                    [
                        f"workflows/{workflow_id}.yaml",
                        f"workflows/{workflow_id}.yml",
                        f"workflows/{workflow_id}.md",
                    ],
                ):
                    missing_workflow_specs.append(workflow_id)

            for credential_id in credentials:
                if credential_id not in template_credential_ids:
                    missing_template_credential_details.append(credential_id)
                if not state.exists or credential_id not in state.declared_credential_ids:
                    missing_repo_credentials.append(credential_id)

            for adapter_id in adapters:
                if not state.exists or not file_exists_any(
                    state.path,
                    [
                        f"adapters/{adapter_id}.yaml",
                        f"adapters/{adapter_id}.yml",
                        f"adapters/{adapter_id}.md",
                    ],
                ):
                    missing_adapter_contracts.append(adapter_id)

            if missing_workflow_specs:
                domain_gaps.append("workflow_specs_missing")
            if missing_template_credential_details:
                domain_gaps.append("template_credential_details_missing")
            if missing_repo_credentials:
                domain_gaps.append("repo_credential_requirements_missing")
            if missing_adapter_contracts:
                domain_gaps.append("adapter_contracts_missing")

            if not state.exists:
                max_readiness = "template_catalog_ready"
            elif domain_gaps:
                max_readiness = "domain_scaffold_required"
            else:
                max_readiness = "installable_candidate"

            pass1_subtypes.append(
                {
                    "id": subtype_id,
                    "label": subtype.get("label"),
                    "repo": repo,
                    "repo_exists": state.exists,
                    "max_readiness": max_readiness,
                    "domain_gaps": sorted(set(domain_gaps)),
                    "missing_workflow_specs": missing_workflow_specs,
                    "missing_template_credential_details": missing_template_credential_details,
                    "missing_repo_credential_requirements": missing_repo_credentials,
                    "missing_adapter_contracts": missing_adapter_contracts,
                    "runtime_gaps": RUNTIME_GAPS,
                    "runtime_binding_focus": subtype.get("runtime_binding_focus") or [],
                }
            )

            pass2_subtypes.append(
                {
                    "id": subtype_id,
                    "label": subtype.get("label"),
                    "repo": repo,
                    "simulated_generic_fixes": [
                        "factory_repo_bootstrapped_if_missing",
                        "starter_v6_applied",
                        "subtype_profile_generated",
                        "workflow_specs_stubbed",
                        "credential_requirement_stubs_generated",
                        "adapter_contract_stubs_generated",
                        "hermes_agent_mix_profiles_generated",
                    ],
                    "max_readiness_after_generic_fixes": "installable_candidate",
                    "remaining_gaps": PASS2_REMAINING_GAPS,
                    "credential_bindings_to_collect": credentials,
                    "adapter_endpoints_to_collect": adapters,
                    "runtime_binding_focus": subtype.get("runtime_binding_focus") or [],
                }
            )

        pass1_groups.append(
            {
                "template_id": template_id,
                "recommended_factory_repo": repo,
                "repo_exists": state.exists,
                "subtypes": pass1_subtypes,
            }
        )
        pass2_groups.append(
            {
                "template_id": template_id,
                "recommended_factory_repo": repo,
                "subtypes": pass2_subtypes,
            }
        )

    pass1 = {
        "schema_version": 1,
        "kind": "xfactory_subtype_install_readiness_pass1",
        "generated_at": now,
        "meaning": "Current catalog and local repo state before applying the fix runbook.",
        "groups": pass1_groups,
    }
    pass2 = {
        "schema_version": 1,
        "kind": "xfactory_subtype_install_readiness_pass2",
        "generated_at": now,
        "meaning": "Second simulation after generic scaffold fixes are assumed generated by the runbook.",
        "groups": pass2_groups,
    }
    return pass1, pass2


def summarize_pass1(pass1: dict[str, Any]) -> dict[str, Any]:
    subtypes = [sub for group in pass1["groups"] for sub in group["subtypes"]]
    repos_missing = sum(1 for sub in subtypes if not sub["repo_exists"])
    installable = sum(1 for sub in subtypes if sub["max_readiness"] == "installable_candidate")
    scaffold_required = sum(1 for sub in subtypes if sub["max_readiness"] == "domain_scaffold_required")
    catalog_only = sum(1 for sub in subtypes if sub["max_readiness"] == "template_catalog_ready")
    return {
        "subtypes": len(subtypes),
        "repos_missing": repos_missing,
        "installable_candidates": installable,
        "domain_scaffold_required": scaffold_required,
        "template_catalog_ready_only": catalog_only,
    }


def gap_text(sub: dict[str, Any]) -> str:
    pieces = []
    if not sub["repo_exists"]:
        pieces.append("repo")
    if sub["missing_workflow_specs"]:
        pieces.append(f"workflows:{len(sub['missing_workflow_specs'])}")
    if sub["missing_repo_credential_requirements"]:
        pieces.append(f"repo_credentials:{len(sub['missing_repo_credential_requirements'])}")
    if sub["missing_template_credential_details"]:
        pieces.append(f"template_credentials:{len(sub['missing_template_credential_details'])}")
    if sub["missing_adapter_contracts"]:
        pieces.append(f"adapters:{len(sub['missing_adapter_contracts'])}")
    other = [
        gap
        for gap in sub["domain_gaps"]
        if gap
        not in {
            "factory_repo_missing",
            "workflow_specs_missing",
            "template_credential_details_missing",
            "repo_credential_requirements_missing",
            "adapter_contracts_missing",
        }
    ]
    pieces.extend(other)
    return ", ".join(pieces) if pieces else "none"


def write_lines(path: Path, lines: list[str]) -> None:
    while lines and lines[-1] == "":
        lines.pop()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_pass1_report(pass1: dict[str, Any]) -> None:
    summary = summarize_pass1(pass1)
    lines = [
        "# Intake Subtype Install Readiness Report",
        "",
        "Status: generated simulation report",
        "Repository context: openxFactory",
        "",
        "## Meaning",
        "",
        "This is pass 1. It checks every intake subtype against the current local",
        "catalog and local factory repo state. It does not assume any runtime",
        "bindings, credentials, adapters, approvals, validation results, or dry-run",
        "evidence have been collected.",
        "",
        "## Summary",
        "",
        f"- Subtypes checked: {summary['subtypes']}",
        f"- Installable candidates in current local state: {summary['installable_candidates']}",
        f"- Require domain scaffold or artifact work: {summary['domain_scaffold_required']}",
        f"- Template catalog only because factory repo is missing locally: {summary['template_catalog_ready_only']}",
        f"- Subtypes blocked by missing local factory repo: {summary['repos_missing']}",
        "",
        "## Gap Code Legend",
        "",
        "- `repo`: factory repo is missing locally.",
        "- `workflows:N`: subtype workflow specs are missing.",
        "- `repo_credentials:N`: domain repo credential requirements are missing.",
        "- `template_credentials:N`: subtype credential family details are not defined in the top-level intake template.",
        "- `adapters:N`: adapter contract stubs are missing.",
        "- `runtime`: deployment target, Hermes, Omnigent, vault refs, adapter endpoints, approvers, validation, dry-run, and live approval are not yet bound.",
        "",
        "Machine-readable detail: [pass1.yaml](../examples/intake-runtime-simulations/pass1.yaml).",
        "",
        "## Per-Subtype Results",
        "",
    ]

    for group in pass1["groups"]:
        lines.extend(
            [
                f"### {group['template_id']} -> {group['recommended_factory_repo']}",
                "",
                "| Subtype | Current readiness | Missing domain artifacts | Runtime missing |",
                "| --- | --- | --- | --- |",
            ]
        )
        for sub in group["subtypes"]:
            lines.append(
                f"| `{sub['id']}` | `{sub['max_readiness']}` | {gap_text(sub)} | runtime |"
            )
        lines.append("")

    write_lines(REPORT_PASS1, lines)


def write_runbook(pass1: dict[str, Any]) -> None:
    lines = [
        "# Intake Subtype Install Runbook",
        "",
        "Status: generated runbook",
        "Repository context: openxFactory",
        "",
        "## Purpose",
        "",
        "Use this runbook to turn each subtype from intake-template data into an",
        "installable xFactory candidate. It fixes generic scaffold and domain-artifact",
        "gaps. It does not invent customer-specific runtime bindings, credentials,",
        "adapter endpoints, approvals, validation evidence, or live execution approval.",
        "",
        "## Standard Fix Flow",
        "",
        "1. Create the factory repo if it is missing.",
        "2. Apply the openxFactory domain starter.",
        "3. Generate one profile file for the subtype.",
        "4. Generate workflow specs for the subtype starter workflows.",
        "5. Generate credential requirement stubs for every credential family.",
        "6. Generate adapter contract stubs for every adapter family.",
        "7. Generate or extend Hermes agent mix profiles.",
        "8. Generate a runtime binding manifest template.",
        "9. Run static validation.",
        "10. Hand off to runtime binding for deployment target, vault refs, adapter endpoints, approvers, validation, and dry-run.",
        "",
        "## Per-Subtype Fix Matrix",
        "",
    ]

    for group in pass1["groups"]:
        lines.extend(
            [
                f"### {group['template_id']} -> {group['recommended_factory_repo']}",
                "",
                "| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for sub in group["subtypes"]:
            subtype_id = sub["id"]
            profile_file = f"`profiles/{slug(subtype_id)}.yaml`"
            workflows = ", ".join(f"`{item}`" for item in sub["missing_workflow_specs"]) or "none"
            credentials = ", ".join(f"`{item}`" for item in sub["missing_repo_credential_requirements"]) or "none"
            adapters = ", ".join(f"`{item}`" for item in sub["missing_adapter_contracts"]) or "none"
            lines.append(f"| `{subtype_id}` | {profile_file} | {workflows} | {credentials} | {adapters} |")
        lines.append("")

    lines.extend(
        [
            "## Runtime Binding Hand-Off",
            "",
            "After the generic fixes above, run the self-hosted runtime binding wizard.",
            "",
            "Required runtime binding outputs:",
            "",
            "- deployment target",
            "- Hermes runtime references",
            "- Omnigent runtime references",
            "- secret provider and vault references",
            "- credential binding references",
            "- adapter endpoint references",
            "- approver references",
            "- runtime validation report",
            "- first workflow dry-run evidence",
            "- live approval decision when live execution is requested",
        ]
    )
    write_lines(REPORT_RUNBOOK, lines)


def write_pass2_report(pass2: dict[str, Any]) -> None:
    subtypes = [sub for group in pass2["groups"] for sub in group["subtypes"]]
    lines = [
        "# Intake Subtype Second-Pass Gap Report",
        "",
        "Status: generated simulation report",
        "Repository context: openxFactory",
        "",
        "## Meaning",
        "",
        "This is pass 2. It simulates the state after the generic runbook-created",
        "factory scaffold, profile, workflow, credential, adapter, and Hermes mix",
        "artifacts exist. The remaining gaps are the pieces that cannot be safely",
        "invented by templates and must come from a customer, operator, domain",
        "expert, provider, or live runtime.",
        "",
        "## Summary",
        "",
        f"- Subtypes checked: {len(subtypes)}",
        "- All subtypes can reach: `installable_candidate` after generic scaffold fixes.",
        "- No subtype can reach: `runtime_ready`, `workflow_ready`, or `live_ready` without runtime binding.",
        "",
        "Machine-readable detail: [pass2.yaml](../examples/intake-runtime-simulations/pass2.yaml).",
        "",
        "## Remaining Gap Families",
        "",
        "- domain SME confirmation",
        "- workflow semantics confirmation",
        "- credential scope confirmation",
        "- adapter implementation or package selection",
        "- deployment target",
        "- Hermes runtime",
        "- Omnigent runtime",
        "- secret provider and credential bindings",
        "- adapter endpoints",
        "- approvers",
        "- runtime validation",
        "- dry-run evidence",
        "- live approval",
        "",
        "## Per-Subtype Remaining Runtime Focus",
        "",
    ]

    for group in pass2["groups"]:
        lines.extend(
            [
                f"### {group['template_id']} -> {group['recommended_factory_repo']}",
                "",
                "| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |",
                "| --- | --- | --- | --- |",
            ]
        )
        for sub in group["subtypes"]:
            credentials = ", ".join(f"`{item}`" for item in sub["credential_bindings_to_collect"])
            adapters = ", ".join(f"`{item}`" for item in sub["adapter_endpoints_to_collect"])
            focus = ", ".join(f"`{item}`" for item in sub["runtime_binding_focus"])
            lines.append(f"| `{sub['id']}` | {credentials} | {adapters} | {focus} |")
        lines.append("")

    write_lines(REPORT_PASS2, lines)


def main() -> int:
    pass1, pass2 = simulate_passes()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "pass1.yaml").write_text(yaml.safe_dump(pass1, sort_keys=False), encoding="utf-8")
    (OUT_DIR / "pass2.yaml").write_text(yaml.safe_dump(pass2, sort_keys=False), encoding="utf-8")
    write_pass1_report(pass1)
    write_runbook(pass1)
    write_pass2_report(pass2)
    print(f"OK wrote {REPORT_PASS1.relative_to(ROOT)}")
    print(f"OK wrote {REPORT_RUNBOOK.relative_to(ROOT)}")
    print(f"OK wrote {REPORT_PASS2.relative_to(ROOT)}")
    print(f"OK wrote {(OUT_DIR / 'pass1.yaml').relative_to(ROOT)}")
    print(f"OK wrote {(OUT_DIR / 'pass2.yaml').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
