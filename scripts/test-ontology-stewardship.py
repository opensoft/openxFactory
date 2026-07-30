#!/usr/bin/env python3
"""Stewardship, maintenance, release, and readiness tests
(add-domain-ontology-layer, tasks 5.3-5.8; the 5.7 proof).

Builds a real package with the ontology-aware starter, then proves:

  * maintenance: a no-drift input records the completed check and never
    touches package content; threshold crossings open mode-mapped
    candidates append-only; a below-floor input fails closed
  * release: the accountable-steward gate publishes append-only (previous
    version retained byte-identically, new line on breaking), the policy
    quality gate blocks publication and only a recorded reviewed exception
    releases it, and a worker/agent identity can prepare but NEVER publish
  * readiness: domain_scaffold_required before publication and quality
    evidence; ontology_ready after

Run: python3 scripts/test-ontology-stewardship.py
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
MAINTENANCE = ROOT / "scripts" / "ontology-maintenance.py"
RELEASE = ROOT / "scripts" / "ontology-release.py"
ONTO = "hermes/domain/ontology"

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


ANSWERS = """schema_version: 1
kind: xfactory_instantiation_prerun_answers
ontology:
  answer_quality: approved
  subject_kinds: [patient]
  focal_item_kinds: [treatment]
  workflows: [intake_review]
  activities: []
  journey_states: [in intake]
  outcomes: [stabilized]
  interventions: []
  evidence_types: []
  external_terminologies: []
  ontology_sources:
    - system_id: intake-notes
      name: Intake design notes
      source_kind: internal_document
      license_class: open
      review_by: '2027-01-01'
  domain_boundaries: [no billing interpretation]
  prohibited_interpretations: []
  stewards:
    - steward_id: test-steward
      role: accountable_steward
      identity_kind: human
      name: Test Steward
    - steward_id: test-bot
      role: accountable_steward
      identity_kind: agent
      name: Preparation Agent
  required_reviewers: [test-council]
  unresolved_assumptions: []
"""

NO_DRIFT_INPUT = """schema_version: 1
kind: xfactory_ontology_maintenance_input
package_id: xf/testx
as_of: '2026-08-01'
unknown_terms: []
"""

DRIFT_INPUT = """schema_version: 1
kind: xfactory_ontology_maintenance_input
package_id: xf/testx
as_of: '2027-06-01'
unknown_terms:
  - term_form: mystery finding
    count: 30
    distinct_subjects: 9
    distinct_tenants: 2
appeals:
  - appeal_id: appeal-001
    concept_id: xf/testx/patient
    description: definition disputed by the review council
promotion_candidates:
  - promotion_ref: promo://reviewed/123
    review_evidence_ref: review://record/123
    proposed_concept_slug: escalation_pattern
"""

BELOW_FLOOR_INPUT = """schema_version: 1
kind: xfactory_ontology_maintenance_input
package_id: xf/testx
as_of: '2026-08-01'
unknown_terms:
  - term_form: rare identifying term
    count: 2
    distinct_subjects: 1
    distinct_tenants: 1
"""

GOOD_QUALITY = """schema_version: 1
kind: xfactory_ontology_quality_report
package_id: xf/testx
package_version: 0.1.0
package_digest: {digest}
window: {{from: '2026-07-01', to: '2026-07-28'}}
signals:
  - signal: intake_scope_coverage
    numerator: 18
    denominator: 20
    procedure_ref: docs/domain-ontology-semantic-decisions.md
aggregation_floor:
  distinct_subjects: 5
  distinct_tenants: 1
"""

POOR_QUALITY = GOOD_QUALITY.replace("numerator: 18", "numerator: 4")


def content_hash(pkg: Path) -> str:
    digest = hashlib.sha256()
    for name in ("package.yaml", "concepts.yaml", "sources.yaml", "stewardship.yaml"):
        digest.update((pkg / name).read_bytes())
    return digest.hexdigest()


def pkg_digest(pkg: Path) -> str:
    import yaml
    return yaml.safe_load((pkg / "package.yaml").read_text())["package_digest"]


def stamp_package(pkg: Path) -> str:
    """Restamp inventory sha256s + the package digest after a content edit
    (the same rule the canonical validator recomputes)."""
    import re
    import yaml
    mp = pkg / "package.yaml"
    text = mp.read_text()
    entries = []
    for entry in yaml.safe_load(text)["inventory"]:
        relp = entry["path"]
        digest = hashlib.sha256((pkg / relp).read_bytes()).hexdigest()
        pattern = re.compile(r"(- path: " + re.escape(relp) + r"\n(\s+)sha256: )[a-f0-9]+")
        text = pattern.sub(lambda m: m.group(1) + digest, text)
        entries.append(f"{relp} {digest}")
    pd = hashlib.sha256("\n".join(sorted(entries)).encode()).hexdigest()
    text = re.sub(r"(?m)^(package_digest: )[a-f0-9]+", r"\g<1>" + pd, text)
    mp.write_text(text)
    return pd


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ontology-stewardship-test-") as tmp:
        target = Path(tmp) / "repo"
        target.mkdir()
        (target / "instantiation-answers.yaml").write_text(ANSWERS)
        run(str(STARTER), str(target), "--product-name", "TestxFactory")
        pkg = target / ONTO
        check("setup: starter produced stewardship policy",
              (pkg / "stewardship.yaml").is_file())

        # -- readiness before anything: scaffold ---------------------------
        res = run(str(VALIDATOR), "--readiness", str(pkg))
        check("readiness: draft scaffold is domain_scaffold_required",
              res.returncode == 3 and "domain_scaffold_required" in res.stdout,
              res.stdout)

        # -- maintenance: no drift -----------------------------------------
        (target / "no-drift.yaml").write_text(NO_DRIFT_INPUT)
        before = content_hash(pkg)
        res = run(str(MAINTENANCE), str(pkg), "--input", str(target / "no-drift.yaml"))
        report = pkg / "maintenance-report-2026-08-01.yaml"
        check("maintenance: no-drift check recorded", res.returncode == 0
              and report.is_file() and "drift_found: false" in report.read_text(),
              res.stdout + res.stderr)
        check("maintenance: package content untouched", content_hash(pkg) == before)
        res = run(str(MAINTENANCE), str(pkg), "--input", str(target / "no-drift.yaml"))
        check("maintenance: identical rerun is append-only skip",
              res.returncode == 0 and "SKIPPED" in res.stdout, res.stdout)

        # -- maintenance: triggers fire ------------------------------------
        (target / "drift.yaml").write_text(DRIFT_INPUT)
        res = run(str(MAINTENANCE), str(pkg), "--input", str(target / "drift.yaml"))
        report2 = (pkg / "maintenance-report-2027-06-01.yaml").read_text()
        check("maintenance: drift evaluated", res.returncode == 0
              and "drift_found: true" in report2, res.stdout + res.stderr)
        check("maintenance: expired source opens refresh candidate",
              (pkg / "candidate-refresh-intake-notes.yaml").is_file()
              and "mode: refresh" in (pkg / "candidate-refresh-intake-notes.yaml").read_text())
        check("maintenance: unknown term opens extend candidate",
              (pkg / "candidate-unknown-mystery-finding.yaml").is_file())
        check("maintenance: appeal opens correct candidate",
              "mode: correct" in (pkg / "candidate-appeal-appeal-001.yaml").read_text())
        promo = (pkg / "candidate-promotion-escalation-pattern.yaml").read_text()
        check("maintenance: promotion candidate carries promotion provenance",
              "method: promotion" in promo and "review://record/123" in promo)
        check("maintenance: package content still untouched", content_hash(pkg) == before)

        # -- maintenance: privacy floor fails closed -----------------------
        (target / "below-floor.yaml").write_text(BELOW_FLOOR_INPUT)
        res = run(str(MAINTENANCE), str(pkg), "--input", str(target / "below-floor.yaml"))
        check("maintenance: below-floor input fails closed",
              res.returncode == 1 and "aggregation floor" in res.stderr, res.stderr)

        # -- release: agent identity can prepare, never publish (5.7) ------
        old_digest = pkg_digest(pkg)
        (pkg / "quality-0.2.0.yaml").write_text(GOOD_QUALITY.format(digest=old_digest))
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-bot", "--release-id", "rel-agent-try",
                  "--quality-report", "quality-0.2.0.yaml")
        check("release: agent accountable identity refused (5.7)",
              res.returncode == 1 and "never publish" in res.stderr, res.stderr)

        # -- release: draft terms cannot ride a publication (F18) -----------
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-draft-try",
                  "--quality-report", "quality-0.2.0.yaml")
        check("release: draft terms refuse publication (term-lifecycle)",
              res.returncode == 1 and "draft term" in res.stderr, res.stderr)
        # Steward act: mark every reviewed term published, restamp, and
        # refresh the quality report over the new content digest.
        concepts_path = pkg / "concepts.yaml"
        concepts_path.write_text(concepts_path.read_text().replace(
            "lifecycle_state: draft", "lifecycle_state: published"))
        stamp_package(pkg)
        old_digest = pkg_digest(pkg)
        (pkg / "quality-0.2.0.yaml").write_text(GOOD_QUALITY.format(digest=old_digest))

        # -- release: evidence paths cannot escape the package (F21) --------
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-escape-try",
                  "--quality-report", "../escape.yaml")
        check("release: evidence path escaping the package refused (F21)",
              res.returncode == 1 and "outside the package" in res.stderr,
              res.stderr)
        # A declared manifest field must survive the rewrite (F21): notes is
        # manifest metadata, outside the inventory digest.
        manifest_path = pkg / "package.yaml"
        manifest_path.write_text(manifest_path.read_text()
                                 + 'notes: "governed stewardship test package"\n')

        # -- release: quality gate blocks; exception releases ---------------
        (pkg / "poor-quality.yaml").write_text(POOR_QUALITY.format(digest=old_digest))
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-poor",
                  "--quality-report", "poor-quality.yaml")
        check("release: below-threshold quality blocks publication",
              res.returncode == 1 and "per-signal" in res.stderr, res.stderr)
        # A blanket exception no longer exists (release-review finding 9):
        # the old form is malformed, an exception without the measurement is
        # refused, and only signal=ref beside the report releases the block.
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-exception",
                  "--quality-exception", "review://exception/9")
        check("release: blanket exception form refused as malformed",
              res.returncode == 1 and "SIGNAL=REF" in res.stderr, res.stderr)
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-exception",
                  "--quality-exception",
                  "intake_scope_coverage=review://exception/9")
        check("release: exception without the measurement refused",
              res.returncode == 1 and "never the measurement" in res.stderr,
              res.stderr)
        res = run(str(RELEASE), str(pkg), "--new-version", "0.2.0",
                  "--compatibility-class", "additive",
                  "--decided-by", "test-steward", "--release-id", "rel-exception",
                  "--quality-report", "poor-quality.yaml",
                  "--quality-exception",
                  "intake_scope_coverage=review://exception/9")
        check("release: per-signal reviewed exception beside the report releases the block",
              res.returncode == 0, res.stderr)
        release_record = (pkg / "release-0.2.0.yaml").read_text()
        check("release: per-signal exception recorded on the release record",
              "quality_exceptions:" in release_record
              and "signal: intake_scope_coverage" in release_record
              and "review://exception/9" in release_record)
        check("release: previous version retained byte-identically",
              (pkg / "retained/0.1.0/package.yaml").is_file()
              and old_digest in (pkg / "retained/0.1.0/package.yaml").read_text())
        check("release: published version self-retained at publication",
              (pkg / "retained/0.2.0/package.yaml").is_file()
              and pkg_digest(pkg) in (pkg / "retained/0.2.0/package.yaml").read_text())
        check("release: retention truthful in both directions (F21/P1)",
              "lifecycle_state: superseded"
              in (pkg / "retained/0.1.0/package.yaml").read_text()
              and "lifecycle_state: published"
              in (pkg / "retained/0.2.0/package.yaml").read_text())
        check("release: declared manifest fields survive the rewrite (F21)",
              "governed stewardship test package"
              in (pkg / "package.yaml").read_text())

        # -- release: breaking requires migration; new line -----------------
        res = run(str(RELEASE), str(pkg), "--new-version", "1.0.0",
                  "--compatibility-class", "breaking",
                  "--decided-by", "test-steward", "--release-id", "rel-break")
        check("release: breaking without migration map refused",
              res.returncode == 1 and "migration" in res.stderr, res.stderr)
        (pkg / "migration.yaml").write_text("\n".join([
            "schema_version: 1", "kind: xfactory_ontology_migration_map",
            "from_package:", "  package_id: xf/testx",
            "  package_version: 0.2.0",
            f"  package_digest: {pkg_digest(pkg)}",
            "to_package:", "  package_id: xf/testx",
            "  package_version: 1.0.0",
            f"  package_digest: {'f' * 64}",
            "compatibility_class: breaking",
            "migrations:",
            "  - from_id: xf/testx/in_intake",
            "    disposition: replaced",
            "    to_ids: [xf/testx/in_intake]",
        ]) + "\n")
        res = run(str(RELEASE), str(pkg), "--new-version", "1.0.0",
                  "--compatibility-class", "breaking",
                  "--decided-by", "test-steward", "--release-id", "rel-break",
                  "--migration-map", "migration.yaml",
                  "--quality-report", "quality-0.2.0.yaml")
        check("release: breaking without consumer impact refused (finding 16)",
              res.returncode == 1 and "consumer-impact" in res.stderr, res.stderr)
        (pkg / "consumer-impact-1.0.0.yaml").write_text("\n".join([
            "schema_version: 1",
            "kind: xfactory_ontology_consumer_impact_report",
            "from_package:", "  package_id: xf/testx",
            "  package_version: 0.2.0",
            f"  package_digest: {pkg_digest(pkg)}",
            "to_package:", "  package_id: xf/testx",
            "  package_version: 1.0.0",
            "affected_terms:", "  - xf/testx/in_intake",
        ]) + "\n")
        res = run(str(RELEASE), str(pkg), "--new-version", "1.0.0",
                  "--compatibility-class", "breaking",
                  "--decided-by", "test-steward", "--release-id", "rel-break",
                  "--migration-map", "migration.yaml",
                  "--quality-report", "quality-0.2.0.yaml",
                  "--consumer-impact", "consumer-impact-1.0.0.yaml")
        check("release: breaking with migration + consumer impact publishes on a new line",
              res.returncode == 0 and "line xf/testx@2" in res.stdout, res.stderr)
        check("release: supersession flips exactly the prior snapshot's lifecycle (P1)",
              "lifecycle_state: superseded"
              in (pkg / "retained/0.2.0/package.yaml").read_text()
              and "lifecycle_state: published"
              in (pkg / "retained/1.0.0/package.yaml").read_text())

        # -- readiness after publication + quality over current digest -----
        new_digest = pkg_digest(pkg)
        (pkg / "quality-1.0.0.yaml").write_text(
            GOOD_QUALITY.format(digest=new_digest)
            .replace("package_version: 0.1.0", "package_version: 1.0.0"))
        res = run(str(VALIDATOR), "--readiness", str(pkg))
        check("readiness: published + quality evidence is ontology_ready",
              res.returncode == 0 and "ontology_ready" in res.stdout, res.stdout)

        # -- the whole tree still validates clean ---------------------------
        res = run(str(VALIDATOR), str(target))
        check("canonical validator green over the released tree",
              res.returncode == 0, res.stdout[-600:])

    if FAILURES:
        print(f"FAIL {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("OK ontology stewardship tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
