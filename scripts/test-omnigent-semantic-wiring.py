#!/usr/bin/env python3
"""Omnigent semantic-wiring tests (add-omnigent-semantic-wiring).

Constructs real trees and proves, fail-closed:

  * repo mode: a domain overlay's worker semantic_context declaration
    resolves to an inventoried profile of the declared package with a
    matching worker_scope; unresolved, wrong-package, scope-mismatched,
    and no-ontology-tree declarations all fail
  * install wiring: both-direction completeness against the pinned
    overlay (declaring worker without a pinned context; unclaimed context
    entry) and per-artifact agreement (content digest, kernel/package
    pins, worker scope) — exercised over a REAL artifact produced by
    scripts/ontology-compile-context.py
  * seam hardening: compilation refuses drifted package bytes (F20), and
    truncation itemizes the closure TRANSITIVELY (F19)

Run: python3 scripts/test-omnigent-semantic-wiring.py
Exit codes: 0 ok, 1 failures, 2 harness error.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OMNIGENT_VALIDATOR = ROOT / "scripts" / "validate-omnigent-contracts.py"
COMPILE = ROOT / "scripts" / "ontology-compile-context.py"
CORE_MANIFEST = ROOT / "contracts" / "domain-ontology" / "core" / "package.yaml"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"ok   {name}")
    else:
        FAILURES.append(name)
        print(f"FAIL {name}{': ' + detail if detail else ''}")


def run(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *argv], capture_output=True,
                          text=True, check=False)


def load_module():
    spec = importlib.util.spec_from_file_location("omnigent_validator",
                                                  OMNIGENT_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules["omnigent_validator"] = module
    spec.loader.exec_module(module)
    return module


def stamp(pkg_dir: Path) -> str:
    mp = pkg_dir / "package.yaml"
    text = mp.read_text()
    entries = []
    for entry in yaml.safe_load(text)["inventory"]:
        relp = entry["path"]
        digest = hashlib.sha256((pkg_dir / relp).read_bytes()).hexdigest()
        pattern = re.compile(r"(- path: " + re.escape(relp) + r"\n(\s+)sha256: )[a-f0-9]+")
        text = pattern.sub(lambda m: m.group(1) + digest, text)
        entries.append(f"{relp} {digest}")
    pd = hashlib.sha256("\n".join(sorted(entries)).encode()).hexdigest()
    text = re.sub(r"(?m)^(package_digest: )[a-f0-9]+", r"\g<1>" + pd, text)
    mp.write_text(text)
    return pd


def build_domain_repo(root: Path, *, chain: bool = False) -> tuple[Path, str, str]:
    """A minimal domain repo: omnigent overlay + stamped ontology package
    with one verify profile. With chain=True the concepts form a two-step
    specialization chain for the truncation probe."""
    kernel = yaml.safe_load(CORE_MANIFEST.read_text())
    kd = kernel["package_digest"]
    pkg = root / "hermes" / "domain" / "ontology"
    pkg.mkdir(parents=True)
    if chain:
        concepts = "\n".join([
            "schema_version: 1", "kind: xfactory_ontology_concepts",
            "package_id: xf/wired", "concepts:",
            "  - id: xf/wired/a_leaf", "    label: A Leaf",
            "    definition: A fixture concept.",
            "    parents: [xf/wired/b_mid]",
            "    lifecycle_state: published", "    effective_version: 1.0.0",
            "  - id: xf/wired/b_mid", "    label: B Mid",
            "    definition: A fixture concept.",
            "    parents: [xf/core/subject]",
            "    lifecycle_state: published", "    effective_version: 1.0.0"]) + "\n"
        required = "  - xf/wired/a_leaf"
    else:
        concepts = "\n".join([
            "schema_version: 1", "kind: xfactory_ontology_concepts",
            "package_id: xf/wired", "concepts:",
            "  - id: xf/wired/case", "    label: Case",
            "    definition: A fixture concept.",
            "    parents: [xf/core/subject]",
            "    lifecycle_state: published", "    effective_version: 1.0.0"]) + "\n"
        required = "  - xf/wired/case"
    (pkg / "concepts.yaml").write_text(concepts)
    (pkg / "profile-verify.yaml").write_text("\n".join([
        "schema_version: 1", "kind: xfactory_semantic_context_profile",
        "profile_id: prof-wired-verify", "package_id: xf/wired",
        "purpose: verification context", "worker_scope:",
        "  worker_archetype: verify",
        "truncation_allowed: true",
        "required_terms:", required]) + "\n")
    (pkg / "package.yaml").write_text("\n".join([
        "schema_version: 1", "kind: xfactory_ontology_package_manifest",
        "package_id: xf/wired", "package_version: 1.0.0",
        "namespace: xf/wired", "is_kernel: false",
        "lifecycle_state: published",
        "owner:", "  layer: domain_hermes", "  name: Wired fixture owner",
        "stewards:",
        "  - steward_id: wired-steward", "    role: accountable_steward",
        "    identity_kind: human",
        "kernel_import:", "  package_id: xf/core",
        f"  package_version: {kernel['package_version']}",
        f"  package_digest: {kd}",
        "inventory:",
        f"  - path: concepts.yaml\n    sha256: {'0' * 64}",
        f"  - path: profile-verify.yaml\n    sha256: {'0' * 64}",
        f"package_digest: {'0' * 64}",
        "compatibility:", "  class: initial", "  line: xf/wired@1"]) + "\n")
    pd = stamp(pkg)
    (root / "omnigent").mkdir()
    (root / "omnigent" / "domain-overlay.yaml").write_text("\n".join([
        "schema_version: 1", "kind: omnigent_domain_overlay",
        "domain:", "  id: wired", "  orchestrator_profile: fixture",
        "composition:", "  operations_contract: domain_installation_overlay",
        "  stricter_rule_wins: true",
        "workers:",
        "  - id: check_runner", "    archetype: verify",
        "    semantic_context:",
        "      profile_id: prof-wired-verify",
        "      package_id: xf/wired",
        "    responsibility: Verify things.",
        "    inputs: [artifact]", "    outputs: [report]",
        "    permissions:",
        "      read_workspace: true", "      write_artifacts: true",
        "      run_validations: true", "      propose_admission: false",
        "      execute_final_action: false", "      access_secrets: false",
        "  - id: scope_framer", "    archetype: frame",
        "    responsibility: Frame things.",
        "    inputs: [intent]", "    outputs: [frame]",
        "    permissions:",
        "      read_workspace: true", "      write_artifacts: true",
        "      run_validations: false", "      propose_admission: false",
        "      execute_final_action: false", "      access_secrets: false",
        "credential_requirements:",
        "  all_classes: [workspace_read]",
        "  never_assignable: [final_action_execute]",
        "routing:", "  scope_ambiguity: intent_owner",
        "stop_conditions:", "  - missing_approved_scope"]) + "\n")
    return pkg, pd, kd


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="omnigent-wiring-test-") as tmp:
        base = Path(tmp)

        # -- repo mode -----------------------------------------------------
        repo = base / "repo"
        repo.mkdir()
        pkg, pd, kd = build_domain_repo(repo)
        res = run(str(OMNIGENT_VALIDATOR), str(repo))
        check("repo mode: resolving declaration validates",
              res.returncode == 0 and "repo overlay validates" in res.stdout,
              res.stdout[-400:])

        overlay_path = repo / "omnigent" / "domain-overlay.yaml"
        original_overlay = overlay_path.read_text()
        overlay_path.write_text(original_overlay.replace(
            "profile_id: prof-wired-verify", "profile_id: prof-wired-ghost"))
        res = run(str(OMNIGENT_VALIDATOR), str(repo))
        check("repo mode: unresolved profile fails",
              res.returncode == 1 and "not an inventoried profile" in res.stdout,
              res.stdout[-400:])
        overlay_path.write_text(original_overlay.replace(
            "  - id: check_runner\n    archetype: verify",
            "  - id: check_runner\n    archetype: challenge"))
        res = run(str(OMNIGENT_VALIDATOR), str(repo))
        check("repo mode: worker_scope mismatch fails",
              res.returncode == 1 and "matches neither" in res.stdout,
              res.stdout[-400:])
        overlay_path.write_text(original_overlay)

        bare = base / "bare"
        bare.mkdir()
        build_domain_repo(bare)
        import shutil
        shutil.rmtree(bare / "hermes")
        res = run(str(OMNIGENT_VALIDATOR), str(bare))
        check("repo mode: declaration without an ontology tree fails",
              res.returncode == 1 and "no hermes/domain/ontology" in res.stdout,
              res.stdout[-400:])

        # -- install wiring over a REAL compiled artifact --------------------
        install = base / "install"
        (install / "rendered").mkdir(parents=True)
        artifact = install / "rendered" / "ctx-wired-verify.yaml"
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-wired-verify",
                  "--profile", "profile-verify.yaml", "--out", str(artifact))
        check("install wiring: real artifact compiles from the fixture package",
              res.returncode == 0, res.stderr)
        ctx = yaml.safe_load(artifact.read_text())
        overlay = yaml.safe_load(original_overlay)
        manifest = {
            "semantic_contexts": {
                "kernel": {"package_id": "xf/core",
                           "package_version": ctx["kernel_pin"]["package_version"],
                           "package_digest": kd},
                "ontology_package": {"package_id": "xf/wired",
                                     "package_version": "1.0.0",
                                     "package_digest": pd},
                "contexts": [{"worker_class": "check_runner",
                              "context_id": "ctx-wired-verify",
                              "content_digest": ctx["content_digest"],
                              "path": "rendered/ctx-wired-verify.yaml"}],
            }
        }
        errors = module.install_wiring_errors(manifest, overlay, install)
        check("install wiring: wired install has no errors", not errors,
              "; ".join(errors))

        empty = {"semantic_contexts": {"kernel": manifest["semantic_contexts"]["kernel"],
                                       "ontology_package": manifest["semantic_contexts"]["ontology_package"],
                                       "contexts": [{"worker_class": "scope_framer",
                                                     "context_id": "ctx-unclaimed",
                                                     "content_digest": "a" * 64,
                                                     "path": "rendered/ghost.yaml"}]}}
        errors = module.install_wiring_errors(empty, overlay, install)
        check("install wiring: declaring worker without a context fails",
              any("has no pinned compiled context" in e for e in errors),
              "; ".join(errors))
        check("install wiring: unclaimed context entry fails",
              any("names no declaring worker" in e for e in errors),
              "; ".join(errors))

        tampered = yaml.safe_load(yaml.safe_dump(manifest))
        tampered["semantic_contexts"]["contexts"][0]["content_digest"] = "b" * 64
        errors = module.install_wiring_errors(tampered, overlay, install)
        check("install wiring: content-digest disagreement fails",
              any("content_digest disagrees" in e for e in errors),
              "; ".join(errors))

        wrong_pin = yaml.safe_load(yaml.safe_dump(manifest))
        wrong_pin["semantic_contexts"]["ontology_package"]["package_digest"] = "c" * 64
        errors = module.install_wiring_errors(wrong_pin, overlay, install)
        check("install wiring: package-pin disagreement fails",
              any("package_pin disagrees" in e for e in errors),
              "; ".join(errors))

        scoped = yaml.safe_load(original_overlay)
        scoped["workers"][0]["archetype"] = "challenge"
        errors = module.install_wiring_errors(manifest, scoped, install)
        check("install wiring: worker-scope disagreement fails",
              any("matches neither" in e for e in errors),
              "; ".join(errors))

        # -- F20: drifted package bytes refuse compilation -------------------
        (pkg / "concepts.yaml").write_text(
            (pkg / "concepts.yaml").read_text() + "# drift\n")
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-drift-try",
                  "--profile", "profile-verify.yaml")
        check("F20: compilation refuses drifted package bytes",
              res.returncode == 1 and "drifted bytes" in res.stderr, res.stderr)
        stamp(pkg)
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-drift-restamped",
                  "--profile", "profile-verify.yaml")
        check("F20: restamped package compiles again", res.returncode == 0,
              res.stderr)

        # -- F19: truncation itemization is transitive -----------------------
        chain_repo = base / "chain"
        chain_repo.mkdir()
        cpkg, _, _ = build_domain_repo(chain_repo, chain=True)
        res = run(str(COMPILE), str(cpkg), "--context-id", "ctx-chain-trunc",
                  "--profile", "profile-verify.yaml", "--truncate")
        doc = yaml.safe_load(res.stdout)
        omitted = set((doc.get("closure") or {}).get("omitted") or [])
        check("F19: truncation itemizes the closure transitively",
              res.returncode == 0
              and omitted == {"xf/wired/b_mid", "xf/core/subject"},
              f"omitted={sorted(omitted)}")

    if FAILURES:
        print(f"FAIL {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("OK omnigent semantic-wiring tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
