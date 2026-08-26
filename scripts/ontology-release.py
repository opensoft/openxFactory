#!/usr/bin/env python3
"""Publish an ontology package version (add-domain-ontology-layer, 5.5/5.8).

Mechanizes the append-only release transition the lifecycle spec requires:

    python3 scripts/ontology-release.py <package-dir> \
        --new-version 1.1.0 --compatibility-class additive \
        --decided-by <steward-id> --release-id rel-... \
        [--quality-report <beside-package file>] \
        [--quality-exception SIGNAL=<recorded-review ref>]... \
        [--migration-map <package-relative path>] \
        [--consumer-impact <beside-package file>] [--dry-run]

What it enforces before touching anything (all fail-closed):

  * `decided_by` resolves to an ACCOUNTABLE steward in the package manifest
    whose identity_kind is human or council — a worker/agent identity can
    prepare everything and publish nothing (tasks 5.5/5.7).
  * breaking/retiring requires a migration map present in the package AND a
    prepared consumer-impact report (`--consumer-impact`) whose from-pin
    matches the active version exactly (release-review finding 16).
  * The stewardship policy's quality gate: when the policy requires signals,
    a quality report is ALWAYS required — an exception releases a threshold,
    never the measurement. Each `--quality-exception SIGNAL=REF` releases
    exactly one named signal with its recorded review; there is no blanket
    exception (task 5.8; release-review finding 9).
  * Accepted candidates must carry steward dispositions (validator rules);
    this tool never merges content — Domain Hermes edits content, the tool
    only performs the governed version transition.

What it does (append-only): writes `retained/<new-version>/` from the exact
bytes it publishes (so history never depends on later edits; the active
version's snapshot truthfully states `published`, and the NEXT release
flips exactly that lifecycle line to `superseded` — review P1), rewrites
`package.yaml` for the new version (previous pin, supersedes chain,
compatibility line — breaking/retiring starts a new line), restamps
inventory digests over the CURRENT content bytes, and writes the release
record naming the accountable steward. When the previous version predates
this self-retention (no `retained/<old-version>/`), the tool falls back to
copying the current bytes — but only after verifying each file still hashes
to the previous manifest's recorded digest; an in-place edit of published
bytes is REFUSED, never silently retained as history.

Exit codes: 0 released, 1 refused, 2 harness error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
    ap.add_argument("--quality-exception", action="append", default=[],
                    metavar="SIGNAL=REF",
                    help="release ONE named quality signal with its recorded "
                         "review reference; repeatable, never blanket")
    ap.add_argument("--migration-map")
    ap.add_argument("--consumer-impact",
                    help="prepared xfactory_ontology_consumer_impact_report "
                         "beside the package (required for breaking/retiring)")
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

    # Evidence-path containment (add-ontology-stewardship-hardening, F21):
    # every release-evidence reference resolves INSIDE the package.
    for flag_name, value in (("--migration-map", args.migration_map),
                             ("--quality-report", args.quality_report),
                             ("--consumer-impact", args.consumer_impact)):
        if value is None:
            continue
        try:
            (pkg_dir / value).resolve().relative_to(pkg_dir)
        except ValueError:
            return refuse(f"{flag_name} {value!r} resolves outside the package "
                          "directory; evidence lives inside the package")

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

    # Term-level lifecycle (add-ontology-term-lifecycle-enforcement):
    # publication is a per-term steward decision — refuse while any term is
    # draft rather than silently promoting it. Deprecation/retirement of the
    # package itself is exempt (the package is leaving service, not landing).
    if args.lifecycle == "published":
        draft_terms: list[str] = []
        for item in manifest.get("inventory", []):
            fp = pkg_dir / item.get("path", "")
            if fp.is_file():
                doc = load(fp)
                if isinstance(doc, dict):
                    for term in (doc.get("concepts") or []) + (doc.get("relations") or []):
                        if term.get("lifecycle_state") == "draft":
                            draft_terms.append(str(term.get("id")))
        if draft_terms:
            shown = ", ".join(sorted(draft_terms)[:5])
            more = f" (+{len(draft_terms) - 5} more)" if len(draft_terms) > 5 else ""
            return refuse(f"draft term(s) cannot ride a publication: {shown}{more}; "
                          "mark each term published (or retire it) before release")

    # Migration + consumer-impact evidence (breaking/retiring).
    if args.compatibility_class in ("breaking", "retiring"):
        if not args.migration_map:
            return refuse(f"{args.compatibility_class} requires --migration-map")
        if not (pkg_dir / args.migration_map).is_file():
            return refuse(f"migration map {args.migration_map} not found in the package")
        if not args.consumer_impact:
            return refuse(f"{args.compatibility_class} requires --consumer-impact "
                          "(a prepared consumer-impact report beside the package)")
        cpath = pkg_dir / args.consumer_impact
        if not cpath.is_file():
            return refuse(f"consumer-impact report {args.consumer_impact} not found in the package")
        impact = load(cpath)
        if impact.get("kind") != "xfactory_ontology_consumer_impact_report":
            return refuse("consumer-impact report has the wrong kind")
        fpin = impact.get("from_package", {})
        if (str(fpin.get("package_id")), str(fpin.get("package_version")),
                str(fpin.get("package_digest"))) != (package_id, old_version, old_digest):
            return refuse("consumer-impact from_package must pin the active version exactly")
        if str(impact.get("to_package", {}).get("package_version")) != args.new_version:
            return refuse("consumer-impact to_package must name the new version")
        if not impact.get("affected_terms"):
            return refuse("consumer-impact report names no affected terms")

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
    exceptions: dict[str, str] = {}
    for spec in args.quality_exception:
        signal, sep, review_ref = spec.partition("=")
        if not sep or not signal or not review_ref:
            return refuse(f"--quality-exception must be SIGNAL=REF, got {spec!r}")
        if signal in exceptions:
            return refuse(f"duplicate --quality-exception for signal {signal}")
        exceptions[signal] = review_ref
    required_names = {r.get("signal") for r in required}
    for signal in exceptions:
        if signal not in required_names:
            return refuse(f"--quality-exception names {signal}, which the policy "
                          "quality gate does not require")
    if required:
        if not args.quality_report:
            return refuse("the policy quality gate requires --quality-report; an "
                          "exception releases a threshold, never the measurement")
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
            if name in exceptions:
                continue
            value = sigmap.get(name)
            if value is None:
                return refuse(f"required quality signal {name} missing from the report; "
                              "a reviewed per-signal --quality-exception is the only release")
            if "min_value" in req and value < req["min_value"]:
                return refuse(f"quality signal {name} {value:.3f} below required "
                              f"{req['min_value']}; a reviewed per-signal "
                              "--quality-exception is the only release")
            if "max_value" in req and value > req["max_value"]:
                return refuse(f"quality signal {name} {value:.3f} above allowed "
                              f"{req['max_value']}")

    # Append-only retention. This release self-retains the bytes it publishes
    # under retained/<new-version>/ below; the previous version normally has
    # its own snapshot already. The fallback (previous version published
    # before self-retention existed) copies current bytes ONLY when they
    # still hash to the previous manifest's recorded digests — an in-place
    # edit of published bytes would rewrite history and is refused.
    retained_new = pkg_dir / "retained" / args.new_version
    if retained_new.exists():
        return refuse(f"retained/{args.new_version} already exists; "
                      "releases never overwrite history")
    retained_old = pkg_dir / "retained" / old_version
    inventory_paths = [item["path"] for item in manifest.get("inventory", [])]
    if not retained_old.exists():
        for item in manifest.get("inventory", []):
            if sha256_file(pkg_dir / item["path"]) != item.get("sha256"):
                return refuse(f"{item['path']} no longer hashes to the digest recorded "
                              f"for {old_version}; restore the published bytes before "
                              "releasing — history is never rewritten")
        if not args.dry_run:
            retained_old.mkdir(parents=True)
            # A snapshot is history from BIRTH (F21): its manifest declares
            # superseded so no consumer mistakes it for the active state.
            # Content bytes are copied verbatim; only the snapshot manifest's
            # lifecycle line differs, and it is never mutated afterward.
            retained_manifest = re.sub(r"(?m)^lifecycle_state: .*$",
                                       "lifecycle_state: superseded",
                                       manifest_path.read_text(encoding="utf-8"),
                                       count=1)
            (retained_old / "package.yaml").write_text(retained_manifest,
                                                       encoding="utf-8")
            for rel in inventory_paths:
                src = pkg_dir / rel
                dst = retained_old / rel
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
    # Faithful rewrite (add-ontology-stewardship-hardening, F21): every
    # declared field of the ratified shape survives the transition — a
    # kernel release never sheds its adoption evidence.
    if manifest.get("adoption") is not None:
        adoption = manifest["adoption"]
        lines.append("adoption:")
        lines.append(f"  status: {adoption.get('status')}")
        if adoption.get("adopters"):
            lines.append("  adopters:")
            for adopter in adoption["adopters"]:
                lines += [f"    - kind: {adopter.get('kind')}",
                          f"      ref: {adopter.get('ref')}"]
    if manifest.get("notes"):
        lines.append(f"notes: {json.dumps(str(manifest['notes']))}")
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
    if exceptions:
        release_lines.append("quality_exceptions:")
        for signal in sorted(exceptions):
            release_lines += [f"  - signal: {signal}",
                              f"    review_ref: {json.dumps(exceptions[signal])}"]
    if args.consumer_impact:
        release_lines.append(f"consumer_impact_ref: {args.consumer_impact}")
    release_text = "\n".join(release_lines) + "\n"
    release_path = pkg_dir / f"release-{args.new_version}.yaml"
    if release_path.exists():
        return refuse(f"{release_path.name} already exists; releases are append-only")

    if not args.dry_run:
        manifest_path.write_text(manifest_text, encoding="utf-8")
        release_path.write_text(release_text, encoding="utf-8")
        # Self-retention: the published bytes become their own history NOW,
        # so no later edit can ever masquerade as this version. The ACTIVE
        # version's snapshot states the truth — published (review P1); the
        # supersession flip below happens when the NEXT release lands.
        retained_new.mkdir(parents=True)
        (retained_new / "package.yaml").write_text(manifest_text,
                                                   encoding="utf-8")
        # Supersession flip (review P1): the OLD version's snapshot, written
        # published at ITS release, now becomes history — exactly one
        # lifecycle line changes under this governed transition; every
        # content byte of the snapshot stays verified untouched.
        old_snapshot = retained_old / "package.yaml"
        if old_snapshot.is_file():
            old_snapshot.write_text(
                re.sub(r"(?m)^lifecycle_state: .*$",
                       "lifecycle_state: superseded",
                       old_snapshot.read_text(encoding="utf-8"), count=1),
                encoding="utf-8")
        for rel in new_inventory:
            src = pkg_dir / rel
            dst = retained_new / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print(f"RELEASED {package_id} {old_version} -> {args.new_version} "
          f"({args.compatibility_class}, line {line}) decided_by {args.decided_by}")
    print(f"RETAINED retained/{old_version}/ ({old_digest})")
    for signal in sorted(exceptions):
        print(f"QUALITY-EXCEPTION {signal} released by review: {exceptions[signal]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
