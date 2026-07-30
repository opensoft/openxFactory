#!/usr/bin/env python3
"""Evaluate ontology maintenance triggers (add-domain-ontology-layer, 5.4).

Deterministically evaluates one governed maintenance input
(`xfactory_ontology_maintenance_input`) against a package's stewardship
policy, opens candidate records for every fired trigger, and writes the
append-only maintenance report. `as_of` comes from the INPUT, never a wall
clock, so the same package + policy + input always produce the same bytes.

    python3 scripts/ontology-maintenance.py <package-dir> --input <file> [--dry-run]

Hard rules (lifecycle spec "Domain Hermes ontology stewardship" /
"Canonical ontology fill and maintenance modes"):

  * The tool NEVER mutates package content — it writes only candidate
    records and the maintenance report, both beside the inventory.
  * Candidates are append-only: an existing candidate (or its recorded
    disposition) is never deleted, replaced, or resurrected; an identical
    re-proposal is a skip, a differing one is a reported conflict.
  * A below-floor term-level entry in the input fails closed (the
    aggregation floor is the package policy's standing floor).
  * An identifier-shaped string anywhere in the input (SSN/email/long digit
    run) fails the run closed BEFORE any candidate bytes are written — a
    governed maintenance input carries aggregate, de-identified forms only
    (release-review finding 6).
  * When nothing fires, the report records the completed check and the
    active package and pins stay untouched.

Exit codes: 0 evaluated (report written), 1 conflicts or fail-closed input,
2 harness error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

TRIGGER_ORDER = [
    "source_expiry", "unknown_terms", "mapping_failures", "low_confidence",
    "workflow_drift", "subdomain_requests", "appeals", "promotion_candidates",
]

# Mirrors the canonical validator's identifier heuristics: an SSN shape, an
# email address, or a 7+ digit run has no place in a governed, aggregate
# maintenance input.
IDENTIFIER_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\d{7,}"),
]


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def slugify(text: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")[:48] or "item"


def date_le(a: str, b: str) -> bool:
    return str(a) <= str(b)


class Emitter:
    def __init__(self, pkg_dir: Path, package_id: str, dry_run: bool):
        self.pkg_dir = pkg_dir
        self.package_id = package_id
        self.dry_run = dry_run
        self.created: list[str] = []
        self.skipped: list[str] = []
        self.conflicts: list[str] = []

    def candidate(self, slug: str, mode: str, description: str,
                  provenance_method: str, source_ref: str,
                  retire_target: str | None = None) -> str:
        name = f"candidate-{slug}.yaml"
        path = self.pkg_dir / name
        lines = [
            "schema_version: 1",
            "kind: xfactory_ontology_candidate_record",
            f"candidate_id: cand-{slug}",
            f"package_id: {self.package_id}",
            f"mode: {mode}",
            "proposed:",
        ]
        if retire_target:
            lines += ["  retirements:", f"    - {retire_target}"]
        else:
            lines += [
                "  concepts:",
                f"    - id: {self.package_id}/{slug.replace('-', '_')}",
                f"      label: {json.dumps(slug.replace('-', ' ').title())}",
                f"      definition: {json.dumps(description)}",
            ]
        lines += [
            "provenance:",
            f"  method: {provenance_method}",
            "  source_refs:",
            f"    - {json.dumps(source_ref)}",
            "review_state: open",
        ]
        content = "\n".join(lines) + "\n"
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if existing == content:
                self.skipped.append(name)
            else:
                self.conflicts.append(name)
            return name
        if not self.dry_run:
            path.write_text(content, encoding="utf-8")
        self.created.append(name)
        return name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package_dir", type=Path)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pkg_dir = args.package_dir.resolve()
    manifest = load(pkg_dir / "package.yaml")
    package_id = manifest.get("package_id", "?")
    policy_path = None
    for item in manifest.get("inventory", []):
        candidate = pkg_dir / item.get("path", "")
        if candidate.is_file():
            doc = load(candidate)
            if isinstance(doc, dict) and doc.get("kind") == "xfactory_ontology_stewardship_policy":
                policy_path = candidate
    if policy_path is None:
        print("ERROR no stewardship policy inventoried in the package", file=sys.stderr)
        return 1
    policy = load(policy_path)
    triggers = policy.get("triggers", {})
    floor = policy.get("aggregation_floor", {})
    sources_doc = {}
    for item in manifest.get("inventory", []):
        doc = load(pkg_dir / item["path"]) if (pkg_dir / item["path"]).is_file() else {}
        if isinstance(doc, dict) and doc.get("kind") == "xfactory_ontology_source_inventory":
            sources_doc = doc

    data = load(args.input)
    if data.get("kind") != "xfactory_ontology_maintenance_input":
        print("ERROR input kind must be xfactory_ontology_maintenance_input", file=sys.stderr)
        return 1
    if data.get("package_id") not in (None, package_id):
        print("ERROR input package_id does not match the package", file=sys.stderr)
        return 1
    as_of = str(data.get("as_of"))

    # De-identification fail-closed (release-review finding 6): candidate
    # prose embeds input strings verbatim, so an identifier-shaped value
    # anywhere in the input refuses the whole run before any bytes land.
    def scan_identifiers(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                yield from scan_identifiers(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from scan_identifiers(v, f"{path}[{i}]")
        elif isinstance(node, str):
            if any(p.search(node) for p in IDENTIFIER_PATTERNS):
                yield path

    leaks = list(scan_identifiers(data, "input"))
    if leaks:
        print("ERROR input carries identifier-shaped values (SSN/email/long "
              f"digit run) at: {', '.join(leaks[:5])}; de-identify the input "
              "before evaluation", file=sys.stderr)
        return 1

    # Privacy fail-closed: every term-level entry meets the standing floor.
    fs = floor.get("distinct_subjects", 1)
    ft = floor.get("distinct_tenants", 1)
    for entry in data.get("unknown_terms") or []:
        if entry.get("distinct_subjects", 0) < fs or entry.get("distinct_tenants", 0) < ft:
            print("ERROR input carries a term-level entry below the policy's "
                  f"aggregation floor ({entry.get('term_form')!r}); withhold it "
                  "into an aggregate count instead", file=sys.stderr)
            return 1

    emitter = Emitter(pkg_dir, package_id, args.dry_run)
    evaluated: list[dict] = []

    def record(trigger: str, fired: bool, detail: str = "", mode: str = "",
               refs: list[str] | None = None) -> None:
        entry: dict = {"trigger": trigger, "fired": fired}
        if detail:
            entry["detail"] = detail[:400]
        if fired:
            entry["mode"] = mode
            entry["candidate_refs"] = refs or []
        evaluated.append(entry)

    # source_expiry: any registered source whose review_by is on/before as_of.
    expired = [s for s in sources_doc.get("sources", [])
               if s.get("review_by") and date_le(s["review_by"], as_of)]
    if expired:
        mode = policy.get("source_review", {}).get("expired_source_mode", "refresh")
        refs = [emitter.candidate(
            f"refresh-{slugify(s['system_id'])}", mode,
            f"Source {s['system_id']} reached its review deadline {s['review_by']}; "
            "re-evaluate dependent terms and mappings.",
            "telemetry_trigger", f"source:{s['system_id']}")
            for s in expired]
        record("source_expiry", True,
               f"{len(expired)} source(s) at/past review_by", mode, refs)
    else:
        record("source_expiry", False)

    unknown = [u for u in (data.get("unknown_terms") or [])
               if u.get("count", 0) >= triggers.get("unknown_term_count_threshold", 10**9)]
    if unknown:
        mode = triggers.get("unknown_term_mode", "extend")
        refs = [emitter.candidate(
            f"unknown-{slugify(u['term_form'])}", mode,
            f"Unmapped term form observed {u['count']} times at/above the "
            "domain threshold; propose a concept or mapping.",
            "telemetry_trigger", f"unknown_term:{u['term_form']}")
            for u in unknown]
        record("unknown_terms", True, f"{len(unknown)} term form(s) over threshold",
               mode, refs)
    else:
        record("unknown_terms", False)

    failures = [f for f in (data.get("mapping_failures") or [])
                if f.get("count", 0) >= triggers.get("mapping_failure_count_threshold", 10**9)]
    if failures:
        mode = triggers.get("mapping_failure_mode", "refresh")
        refs = [emitter.candidate(
            f"mapfail-{slugify(f['system_id'])}", mode,
            f"Mapping failures against {f['system_id']} reached the domain "
            "threshold; re-verify the mapping set.",
            "telemetry_trigger", f"mapping_failures:{f['system_id']}")
            for f in failures]
        record("mapping_failures", True, f"{len(failures)} system(s) over threshold",
               mode, refs)
    else:
        record("mapping_failures", False)

    lowconf = [l for l in (data.get("low_confidence") or [])
               if l.get("count", 0) >= triggers.get("low_confidence_count_threshold", 10**9)
               and l.get("mean_confidence", 1) <= triggers.get("low_confidence_threshold", 0)]
    if lowconf:
        mode = triggers.get("low_confidence_mode", "reconcile")
        refs = [emitter.candidate(
            f"lowconf-{slugify(l['concept_id'].rsplit('/', 1)[-1])}", mode,
            f"Repeated low-confidence classification against {l['concept_id']}; "
            "reconcile the definition or split the concept.",
            "telemetry_trigger", f"low_confidence:{l['concept_id']}")
            for l in lowconf]
        record("low_confidence", True, f"{len(lowconf)} concept(s) over threshold",
               mode, refs)
    else:
        record("low_confidence", False)

    drift = data.get("workflow_drift") or []
    if drift:
        mode = triggers.get("workflow_drift_mode", "reconcile")
        refs = [emitter.candidate(
            f"drift-{slugify(d['workflow_ref'])}", mode,
            f"Workflow drift reported: {d['description']}",
            "telemetry_trigger", f"workflow:{d['workflow_ref']}")
            for d in drift]
        record("workflow_drift", True, f"{len(drift)} drift report(s)", mode, refs)
    else:
        record("workflow_drift", False)

    subdomains = data.get("subdomain_requests") or []
    if subdomains:
        mode = triggers.get("subdomain_request_mode", "extend")
        refs = [emitter.candidate(
            f"subdomain-{slugify(s['request_id'])}", mode,
            f"Sub-domain expansion request: {s['description']}",
            "human_authored", f"subdomain:{s['request_id']}")
            for s in subdomains]
        record("subdomain_requests", True, f"{len(subdomains)} request(s)", mode, refs)
    else:
        record("subdomain_requests", False)

    appeals = data.get("appeals") or []
    if appeals:
        mode = triggers.get("appeal_mode", "correct")
        refs = [emitter.candidate(
            f"appeal-{slugify(a['appeal_id'])}", mode,
            f"Appeal against {a['concept_id']}: {a['description']}",
            "human_authored", f"appeal:{a['appeal_id']}",
            retire_target=None)
            for a in appeals]
        record("appeals", True, f"{len(appeals)} appeal(s)", mode, refs)
    else:
        record("appeals", False)

    promotions = data.get("promotion_candidates") or []
    if promotions:
        mode = triggers.get("promotion_mode", "extend")
        refs = [emitter.candidate(
            f"promotion-{slugify(p.get('proposed_concept_slug') or p['promotion_ref'])}",
            mode,
            "Reviewed de-identified promotion candidate; contains the reusable "
            "abstraction and evidence references only.",
            "promotion", p["review_evidence_ref"])
            for p in promotions]
        record("promotion_candidates", True, f"{len(promotions)} candidate(s)",
               mode, refs)
    else:
        record("promotion_candidates", False)

    drift_found = any(e["fired"] for e in evaluated)
    report_lines = [
        "schema_version: 1",
        "kind: xfactory_ontology_maintenance_report",
        f"package_id: {package_id}",
        f"package_digest: {manifest.get('package_digest')}",
        f"as_of: '{as_of}'",
        f"input_ref: {json.dumps(args.input.name)}",
        "triggers_evaluated:",
    ]
    for e in evaluated:
        report_lines += [f"  - trigger: {e['trigger']}",
                         f"    fired: {'true' if e['fired'] else 'false'}"]
        if e.get("detail"):
            report_lines.append(f"    detail: {json.dumps(e['detail'])}")
        if e.get("mode"):
            report_lines.append(f"    mode: {e['mode']}")
        if e.get("candidate_refs"):
            report_lines.append("    candidate_refs:")
            report_lines += [f"      - {r}" for r in e["candidate_refs"]]
    report_lines.append(f"drift_found: {'true' if drift_found else 'false'}")
    report_content = "\n".join(report_lines) + "\n"
    report_path = pkg_dir / f"maintenance-report-{as_of}.yaml"
    if report_path.exists():
        if report_path.read_text(encoding="utf-8") == report_content:
            emitter.skipped.append(report_path.name)
        else:
            emitter.conflicts.append(report_path.name)
    else:
        if not args.dry_run:
            report_path.write_text(report_content, encoding="utf-8")
        emitter.created.append(report_path.name)

    print(f"MAINTENANCE {package_id} as_of {as_of}: "
          f"{'drift found' if drift_found else 'no drift; check recorded'}")
    for name in emitter.created:
        print(f"CREATED {name}")
    for name in emitter.skipped:
        print(f"SKIPPED {name} (identical; append-only)")
    for name in emitter.conflicts:
        print(f"CONFLICT {name} differs from the existing record; never overwritten")
    return 1 if emitter.conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
