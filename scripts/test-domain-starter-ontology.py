#!/usr/bin/env python3
"""Starter tests for the domain-ontology generation pipeline
(add-domain-ontology-layer, task 4.9).

Seven scenarios, each in a fresh temporary repo:

  1. empty repo          full scaffold generates; the canonical
                         domain-ontology validator passes the generated
                         package and the content-manifest cross-check
  2. partial answers     missing steward/subject kinds -> placeholders,
                         draft stays non-publishable, unresolved reported
  3. idempotent rerun    second run creates nothing and the ontology tree
                         is byte-identical (deterministic seeding)
  4. model-ingest rerun  a second extraction batch over unchanged sources
                         classifies proposals as new / duplicate /
                         conflicting; recorded dispositions survive
  5. legacy repo         pre-existing hermes/domain content is preserved;
                         the ontology tree and manifest declaration are
                         additive
  6. conflicting content a differing domain-owned concepts.yaml is
                         reported as a conflict and its bytes are what the
                         generated manifest digests
  7. overwrite attempt   reruns never change domain-owned ontology bytes

Run: python3 scripts/test-domain-starter-ontology.py
Exit codes: 0 ok, 1 failures, 2 harness error.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "scripts" / "apply-domain-starter.py"
VALIDATOR = ROOT / "scripts" / "validate-domain-ontology.py"
ONTO = "hermes/domain/ontology"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"ok   {name}")
    else:
        FAILURES.append(name)
        print(f"FAIL {name}{': ' + detail if detail else ''}")


def run_starter(target: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(STARTER), str(target), "--product-name",
         "TestxFactory", *extra],
        capture_output=True, text=True, check=False)


def run_validator(target: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True, text=True, check=False)


def tree_hash(base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((base / ONTO).rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(base)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def write_answers(target: Path, ontology_block: str) -> Path:
    path = target / "instantiation-answers.yaml"
    path.write_text(
        "schema_version: 1\n"
        "kind: xfactory_instantiation_prerun_answers\n"
        + ontology_block)
    return path


FULL_ANSWERS = """ontology:
  answer_quality: approved
  subject_kinds: [patient]
  focal_item_kinds: [treatment, care plan]
  workflows: [intake_review]
  activities: [chart review]
  journey_states: [in intake]
  outcomes: [stabilized]
  interventions: [follow up call]
  evidence_types: [lab report]
  external_terminologies:
    - system_id: example-terms
      name: Example Terminology
      version: '2026'
      license_class: no_redistribution
      permitted_use: [reference]
  ontology_sources:
    - system_id: intake-notes
      name: Intake design notes
      source_kind: internal_document
      license_class: open
  domain_boundaries: [no billing interpretation]
  prohibited_interpretations: []
  stewards:
    - steward_id: test-steward
      role: accountable_steward
      identity_kind: human
      name: Test Steward
  required_reviewers: [test-council]
  unresolved_assumptions: []
"""

BATCH_ONE = """schema_version: 1
kind: xfactory_ontology_extraction_batch
extraction_run_id: run-alpha-0001
method: model_extraction
source_refs: [intake-notes]
proposals:
  - id: xf/testx/care_gap
    label: care gap
    definition: Proposed concept from intake notes.
    parents: [xf/core/focal_item]
    confidence: 0.8
  - id: xf/testx/triage_call
    label: triage call
    definition: Proposed activity from intake notes.
    parents: [xf/core/activity]
    confidence: 0.6
"""

BATCH_TWO = """schema_version: 1
kind: xfactory_ontology_extraction_batch
extraction_run_id: run-beta-0002
method: model_extraction
source_refs: [intake-notes]
proposals:
  - id: xf/testx/care_gap
    label: care gap
    definition: A DIFFERENT definition from the second run.
    parents: [xf/core/focal_item]
    confidence: 0.9
  - id: xf/testx/new_idea
    label: new idea
    definition: A new proposal only the second run found.
    parents: [xf/core/outcome]
    confidence: 0.5
"""


def scenario_1_empty_repo(base: Path) -> Path:
    target = base / "s1"
    target.mkdir()
    write_answers(target, FULL_ANSWERS)
    result = run_starter(target)
    check("s1 starter exits 0", result.returncode == 0, result.stdout[-400:])
    for rel in (f"{ONTO}/package.yaml", f"{ONTO}/concepts.yaml",
                f"{ONTO}/sources.yaml", f"{ONTO}/STARTER.yaml",
                f"{ONTO}/coverage-gap-report.yaml", f"{ONTO}/review-fixtures.yaml",
                "hermes/domain/content-manifest.yaml"):
        check(f"s1 generates {rel}", (target / rel).is_file())
    manifest = (target / "hermes/domain/content-manifest.yaml").read_text()
    check("s1 manifest declares domain_ontology", "domain_ontology" in manifest)
    marker = (target / ONTO / "STARTER.yaml").read_text()
    check("s1 marker records ontology-aware version",
          "ontology_aware: true" in marker and "starter_version: 13" in marker)
    concepts = (target / ONTO / "concepts.yaml").read_text()
    check("s1 seeds subject specialization", "xf/testx/patient" in concepts
          and "xf/core/subject" in concepts)
    vres = run_validator(target)
    check("s1 canonical validator passes generated package",
          vres.returncode == 0, vres.stdout[-600:])
    return target


def scenario_2_partial_answers(base: Path) -> None:
    target = base / "s2"
    target.mkdir()
    write_answers(target, (
        "ontology:\n"
        "  answer_quality: draft\n"
        "  subject_kinds: [<primary-subject-kind>]\n"
        "  focal_item_kinds: []\n"
        "  ontology_sources: []\n"
        "  stewards: []\n"
        "  domain_boundaries: []\n"
        "  unresolved_assumptions: [pending intake session]\n"))
    result = run_starter(target)
    report = (target / "docs/starter-rerun-report.md").read_text()
    pkg = (target / ONTO / "package.yaml").read_text()
    concepts = (target / ONTO / "concepts.yaml").read_text()
    check("s2 placeholder concept seeded", "placeholder_subject" in concepts)
    check("s2 package stays draft", "lifecycle_state: draft" in pkg)
    check("s2 placeholder steward recorded", "UNASSIGNED" in pkg)
    check("s2 unresolved inputs reported",
          "Unresolved Semantic Inputs" in report and
          "accountable ontology steward unassigned" in report)
    check("s2 not-publishable note present", "NOT PUBLISHABLE" in pkg)
    vres = run_validator(target)
    check("s2 draft package still validates", vres.returncode == 0,
          vres.stdout[-400:])
    check("s2 starter exit reflects no hard errors", result.returncode == 0,
          result.stdout[-200:])


def scenario_3_idempotent_rerun(target: Path) -> None:
    before = tree_hash(target)
    result = run_starter(target)
    after = tree_hash(target)
    check("s3 rerun exits 0", result.returncode == 0)
    check("s3 ontology tree byte-identical on rerun", before == after)
    report = (target / "docs/starter-rerun-report.md").read_text()
    check("s3 rerun creates no ontology files",
          "| `hermes/domain/ontology/package.yaml` | ontology scaffold |"
          not in report.split("## Created Files")[1].split("## Updated Files")[0])


def scenario_4_ingest(target: Path) -> None:
    batch1 = target / "batch1.yaml"
    batch1.write_text(BATCH_ONE)
    result = run_starter(target, "--ingest-candidates", str(batch1))
    check("s4 first ingest exits 0", result.returncode == 0, result.stdout[-300:])
    cand = target / ONTO / "candidate-care-gap.yaml"
    check("s4 candidate written", cand.is_file())
    check("s4 candidate carries run identity",
          "extraction_run_id: run-alpha-0001" in cand.read_text())
    # Record a disposition, then re-ingest a differing + a duplicate + a new
    # proposal: the disposition and original bytes must survive.
    disposed = cand.read_text().replace(
        "review_state: open",
        "review_state: rejected\ndisposition:\n  decided_by: test-steward\n  decision: rejected")
    cand.write_text(disposed)
    batch2 = target / "batch2.yaml"
    batch2.write_text(BATCH_TWO)
    run_starter(target, "--ingest-candidates", str(batch2))
    report = (target / "docs/starter-rerun-report.md").read_text()
    check("s4 differing proposal reported as conflict",
          "candidate-care-gap.yaml" in report and
          "differs from the new proposal" in report)
    check("s4 disposition preserved (never resurrected)",
          "decision: rejected" in cand.read_text())
    check("s4 new proposal appended",
          (target / ONTO / "candidate-new-idea.yaml").is_file())
    dup = target / "batch1b.yaml"
    dup.write_text(BATCH_ONE.replace("run-alpha-0001", "run-alpha-0001"))
    run_starter(target, "--ingest-candidates", str(dup))
    report = (target / "docs/starter-rerun-report.md").read_text()
    check("s4 identical re-proposal reported duplicate",
          "duplicate candidate; unchanged" in report)
    # Unapproved source fails closed.
    bad = target / "bad-batch.yaml"
    bad.write_text(BATCH_ONE.replace("intake-notes", "unregistered-system"))
    result = run_starter(target, "--ingest-candidates", str(bad))
    check("s4 unapproved source fails closed", result.returncode == 1,
          result.stdout[-300:])


def scenario_5_legacy_repo(base: Path) -> None:
    target = base / "s5"
    (target / "hermes/domain/policies").mkdir(parents=True)
    legacy = target / "hermes/domain/policies/README.md"
    legacy.write_text("# Legacy domain policies\n\nAuthored before the ontology-aware starter.\n")
    result = run_starter(target)
    check("s5 legacy file preserved",
          legacy.read_text().startswith("# Legacy domain policies"))
    check("s5 ontology added additively", (target / ONTO / "package.yaml").is_file())
    manifest = (target / "hermes/domain/content-manifest.yaml").read_text()
    check("s5 manifest declared", "domain_ontology" in manifest)
    check("s5 run exits 0", result.returncode == 0, result.stdout[-200:])


def scenario_6_and_7_conflicting_content(base: Path) -> None:
    target = base / "s6"
    (target / ONTO).mkdir(parents=True)
    domain_owned = (
        "schema_version: 1\n"
        "kind: xfactory_ontology_concepts\n"
        "package_id: xf/testx\n"
        "concepts:\n"
        "  - id: xf/testx/domain_owned\n"
        "    label: \"Domain Owned\"\n"
        "    definition: \"Authored by Domain Hermes before a starter rerun.\"\n"
        "    parents: [xf/core/subject]\n"
        "    lifecycle_state: draft\n"
        "    effective_version: 0.1.0\n")
    (target / ONTO / "concepts.yaml").write_text(domain_owned)
    write_answers(target, FULL_ANSWERS)
    result = run_starter(target)
    check("s6 conflict exit code", result.returncode == 1)
    report = (target / "docs/starter-rerun-report.md").read_text()
    check("s6 conflict reported",
          "domain-owned ontology content differs from starter output" in report)
    check("s6 domain bytes untouched",
          (target / ONTO / "concepts.yaml").read_text() == domain_owned)
    pkg = (target / ONTO / "package.yaml").read_text()
    check("s6 manifest digests the preserved bytes",
          hashlib.sha256(domain_owned.encode()).hexdigest() in pkg)
    vres = run_validator(target)
    check("s6 preserved package still digest-valid", vres.returncode == 0,
          vres.stdout[-400:])
    # Scenario 7: a second rerun still refuses to overwrite.
    run_starter(target)
    check("s7 rerun never overwrites domain content",
          (target / ONTO / "concepts.yaml").read_text() == domain_owned)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="starter-ontology-test-") as tmp:
        base = Path(tmp)
        s1_target = scenario_1_empty_repo(base)
        scenario_2_partial_answers(base)
        scenario_3_idempotent_rerun(s1_target)
        scenario_4_ingest(s1_target)
        scenario_5_legacy_repo(base)
        scenario_6_and_7_conflicting_content(base)
    if FAILURES:
        print(f"FAIL {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("OK domain-starter ontology pipeline tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
