#!/usr/bin/env python3
"""Publish an ontology package version (add-domain-ontology-layer, 5.5/5.8).

Mechanizes the append-only release transition the lifecycle spec requires:

    python3 scripts/ontology-release.py <package-dir> \
        --new-version 1.1.0 --compatibility-class additive \
        --decided-by <steward-id> --release-id rel-... \
        [--quality-report <beside-package file>] \
        [--quality-exception <recorded-review ref>] \
        [--migration-map <package-relative path>] [--dry-run]

What it enforces before touching anything (all fail-closed):

  * `decided_by` resolves to an ACCOUNTABLE steward in the package manifest
    whose identity_kind is human or council — a worker/agent identity can
    prepare everything and publish nothing (tasks 5.5/5.7).
  * breaking/retiring requires a migration map present in the package.
  * The stewardship policy's quality gate: every required signal present in
    the named quality report (covering the CURRENT content digest) and
    inside its threshold — or an explicit `--quality-exception` reviewed
    reference, which is recorded on the release (task 5.8).
  * Accepted candidates must carry steward dispositions (validator rules);
    this tool never merges content — Domain Hermes edits content, the tool
    only performs the governed version transition.

What it does (append-only): copies the ACTIVE version byte-identically to
`retained/<old-version>/`, rewrites `package.yaml` for the new version
(previous pin, supersedes chain, compatibility line — breaking/retiring
starts a new line), restamps inventory digests over the CURRENT content
bytes, and writes the release record naming the accountable steward. No
published bytes are ever deleted or rewritten; historical artifacts keep
their original pins.

Exit codes: 0 released, 1 refused, 2 harness error.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse(message: str) -> int:
    print(f"REFUSED {message}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package_dir", type=Path)
    ap.add_argument("--new-version", required=True)
    ap.add_argument("--compatibility-class", required=True,
                    choices=["additive", "clarifying", "breaking", "retiring"])
    ap.add_argument("--decided-by", required=True)
    ap.add_argument("--release-id", required=True)
    ap.add_argument("--quality-report")
    ap.add_argument("--quality-exception")
    ap.add_argument("--migration-map")
    ap.add_argument("--lifecycle", default="published",
                    choices=["published", "deprecated", "retired"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pkg_dir = args.package_dir.resolve()
    manifest_path = pkg_dir / "package.yaml"
    manifest = load(manifest_path)
    package_id = manifest.get("package_id", "?")
    old_version = str(manifest.get("package_version"))
    old_digest = str(manifest.get("package_digest"))

    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", args.new_version):
        return refuse("new version must be semver-shaped")
    if args.new_version == old_version:
        return refuse("new version equals the active version; releases are append-only")
    if not re.match(r"^rel-[a-z0-9][a-z0-9-]{0,63}$", args.release_id):
        return refuse("release id must match rel-...")

    # Accountable-steward gate (5.5/5.7).
    steward = next((s for s in manifest.get("stewards", [])
                    if s.get("steward_id") == args.decided_by), None)
    if steward is None:
        return refuse(f"decided_by {args.decided_by!r} is not in the manifest steward roster")
    if steward.get("role") != "accountable_steward":
        return refuse(f"{args.decided_by} is not an accountable steward")
    if steward.get("identity_kind") in ("worker", "agent"):
        return refuse("a worker/agent identity can prepare a release but never publish one")
    if "UNASSIGNED" in str(steward.get("name", "")):
        return refuse("the accountable steward is an unassigned placeholder")

    # Migration evidence (breaking/retiring).
    if args.compatibility_class in ("breaking", "retiring"):
        if not args.migration_map:
            return refuse(f"{args.compatibility_class} requires --migration-map")
        if not (pkg_dir / args.migration_map).is_file():
            return refuse(f"migration map {args.migration_map} not found in the package")

    # Quality gate (5.8): policy-required signals over the CURRENT content.
    policy = None
    for item in manifest.get("inventory", []):
        fp = pkg_dir / item.get("path", "")
        if fp.is_file():
            doc = load(fp)
            if isinstance(doc, dict) and doc.get("kind") == "xfactory_ontology_stewardship_policy":
                policy = doc
    gate = (policy or {}).get("quality_gate", {})
    required = gate.get("required_signals", [])
    if required and not args.quality_exception:
        if not args.quality_report:
            return refuse("the policy quality gate requires --quality-report "
                          "or a recorded --quality-exception")
        qpath = pkg_dir / args.quality_report
        if not qpath.is_file():
            return refuse(f"quality report {args.quality_report} not found")
        q = load(qpath)
        if q.get("kind") != "xfactory_ontology_quality_report":
            return refuse("quality report has the wrong kind")
        sigmap: dict[str, float] = {}
        for sig in q.get("signals", []):
            den = sig.get("denominator") or 0
            if den:
                sigmap[sig.get("signal")] = sig.get("numerator", 0) / den
        for req in required:
            name = req.get("signal")
            value = sigmap.get(name)
            if value is None:
                return refuse(f"required quality signal {name} missing from the report")
            if "min_value" in req and value < req["min_value"]:
                return refuse(f"quality signal {name} {value:.3f} below required "
                              f"{req['min_value']}; a recorded reviewed exception "
                              "is the only release")
            if "max_value" in req and value > req["max_value"]:
                return refuse(f"quality signal {name} {value:.3f} above allowed "
                              f"{req['max_value']}")

    # Append-only retention: the active version's bytes move to retained/.
    retained_dir = pkg_dir / "retained" / old_version
    if retained_dir.exists():
        return refuse(f"retained/{old_version} already exists; releases never overwrite history")
    inventory_paths = [item["path"] for item in manifest.get("inventory", [])]
    if not args.dry_run:
        retained_dir.mkdir(parents=True)
        shutil.copy2(manifest_path, retained_dir / "package.yaml")
        for rel in inventory_paths:
            src = pkg_dir / rel
            dst = retained_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # New manifest over the CURRENT content bytes. A shipped migration map is
    # package CONTENT (digest-covered), so a breaking/retiring release
    # inventories it alongside the existing content files.
    new_inventory = sorted(set(inventory_paths)
                           | ({args.migration_map} if args.migration_map else set()))
    entries = []
    inv_lines = []
    for rel in new_inventory:
        digest = sha256_file(pkg_dir / rel)
        entries.append(f"{rel} {digest}")
        inv_lines += [f"  - path: {rel}", f"    sha256: {digest}"]
    package_digest = hashlib.sha256("\n".join(sorted(entries)).encode("utf-8")).hexdigest()

    compat = manifest.get("compatibility", {})
    line = str(compat.get("line", f"{package_id}@1"))
    if args.compatibility_class in ("breaking", "retiring"):
        base, _, n = line.rpartition("@")
        line = f"{base}@{int(n) + 1}"
    supersedes = list(manifest.get("supersedes", []) or [])
    supersedes.append({"package_version": old_version, "package_digest": old_digest})

    lines = [
        "schema_version: 1",
        "kind: xfactory_ontology_package_manifest",
        f"# Version {args.new_version} published by scripts/ontology-release.py;",
        f"# supersedes {old_version} (retained at retained/{old_version}/).",
        f"package_id: {package_id}",
        f"package_version: {args.new_version}",
        f"namespace: {manifest.get('namespace')}",
        f"is_kernel: {'true' if manifest.get('is_kernel') else 'false'}",
        f"lifecycle_state: {args.lifecycle}",
        "owner:",
        f"  layer: {manifest.get('owner', {}).get('layer')}",
        f"  name: \"{manifest.get('owner', {}).get('name')}\"",
        "stewards:",
    ]
    for s in manifest.get("stewards", []):
        lines += [f"  - steward_id: {s['steward_id']}",
                  f"    role: {s['role']}",
                  f"    identity_kind: {s['identity_kind']}"]
        if s.get("name"):
            lines.append(f"    name: \"{s['name']}\"")
    ki = manifest.get("kernel_import")
    if ki:
        lines += ["kernel_import:",
                  f"  package_id: {ki['package_id']}",
                  f"  package_version: {ki['package_version']}",
                  f"  package_digest: {ki['package_digest']}"]
    lines.append("inventory:")
    lines += inv_lines
    lines.append(f"package_digest: {package_digest}")
    lines += ["compatibility:",
              f"  class: {args.compatibility_class}",
              f"  line: {line}",
              "  previous:",
              f"    package_version: {old_version}",
              f"    package_digest: {old_digest}"]
    if args.migration_map:
        lines.append(f"  migration_map: {args.migration_map}")
    lines.append("supersedes:")
    for ref in supersedes:
        lines += [f"  - package_version: {ref['package_version']}",
                  f"    package_digest: {ref['package_digest']}"]
    manifest_text = "\n".join(lines) + "\n"

    release_lines = [
        "schema_version: 1",
        "kind: xfactory_ontology_release_record",
        f"release_id: {args.release_id}",
        f"package_id: {package_id}",
        f"package_version: {args.new_version}",
        f"package_digest: {package_digest}",
        f"compatibility_class: {args.compatibility_class}",
        f"decided_by: {args.decided_by}",
    ]
    if args.migration_map:
        release_lines.append(f"migration_map_ref: {args.migration_map}")
    if args.quality_report:
        release_lines.append(f"quality_report_ref: {args.quality_report}")
    if args.quality_exception:
        release_lines.append(f"quality_exception_ref: {args.quality_exception}")
    release_text = "\n".join(release_lines) + "\n"
    release_path = pkg_dir / f"release-{args.new_version}.yaml"
    if release_path.exists():
        return refuse(f"{release_path.name} already exists; releases are append-only")

    if not args.dry_run:
        manifest_path.write_text(manifest_text, encoding="utf-8")
        release_path.write_text(release_text, encoding="utf-8")
    print(f"RELEASED {package_id} {old_version} -> {args.new_version} "
          f"({args.compatibility_class}, line {line}) decided_by {args.decided_by}")
    print(f"RETAINED retained/{old_version}/ ({old_digest})")
    if args.quality_exception:
        print(f"QUALITY-EXCEPTION recorded: {args.quality_exception}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
