#!/usr/bin/env python3
"""Compile a bounded semantic-context artifact (add-domain-ontology-layer, 6.1).

Deterministically compiles one purpose-bounded `xfactory_semantic_context`
from the exact kernel and domain package pins:

    python3 scripts/ontology-compile-context.py <package-dir> \
        --context-id ctx-... \
        (--terms xf/d/a,xf/d/b | --profile <package-relative profile file>) \
        [--purpose "..."] [--tenant-binding <file>] [--truncate] \
        [--compiled-at 2026-07-29T00:00:00Z] [--ttl 3600] [--out FILE]

Rules (kernel spec "Bounded semantic context"):

  * There is NO unrestricted mode: a term subset or a worker profile is
    required, and the subset is CLOSED over specialization ancestors up to
    the kernel and every included relation's domain/range concepts — or,
    with --truncate (profile `truncation_allowed` respected), an itemized
    truncation names each omitted closure member.
  * An unresolvable requested term fails closed. A retired or superseded
    package refuses new compilation (historical interpretation keeps its
    original pins; new classification needs a live pin).
  * A tenant binding must declare THIS package's exact identity and every
    bound target must resolve — a wrong-package or unresolvable binding
    fails closed, which is how a tenant discovers a supersession at
    adoption rather than at runtime.
  * The artifact carries no permission or authority field; presence of
    semantic context never changes any rail or matrix.
  * `compiled_at`/`ttl` are DATA (never a wall clock); the content digest
    is sha256 over the canonical rendering with the digest line blank, so
    the same inputs always produce the same artifact.

Exit codes: 0 compiled, 1 refused, 2 harness error.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

OPENX_ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = OPENX_ROOT / "contracts" / "domain-ontology" / "core"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def refuse(message: str) -> int:
    print(f"REFUSED {message}", file=sys.stderr)
    return 1


def load_terms(pkg_dir: Path, manifest: dict) -> tuple[dict, dict]:
    concepts: dict[str, dict] = {}
    relations: dict[str, dict] = {}
    for item in manifest.get("inventory", []):
        fp = pkg_dir / item.get("path", "")
        if not fp.is_file():
            continue
        doc = load(fp)
        if not isinstance(doc, dict):
            continue
        for c in doc.get("concepts", []) or []:
            concepts.setdefault(c["id"], c)
        for r in doc.get("relations", []) or []:
            relations.setdefault(r["id"], r)
    return concepts, relations


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package_dir", type=Path)
    ap.add_argument("--context-id", required=True)
    ap.add_argument("--terms")
    ap.add_argument("--profile")
    ap.add_argument("--purpose")
    ap.add_argument("--tenant-binding", type=Path)
    ap.add_argument("--truncate", action="store_true")
    ap.add_argument("--compiled-at")
    ap.add_argument("--ttl", type=int)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    pkg_dir = args.package_dir.resolve()
    manifest = load(pkg_dir / "package.yaml")
    package_id = manifest.get("package_id", "?")
    if manifest.get("lifecycle_state") in ("retired", "superseded"):
        return refuse(f"package lifecycle is {manifest.get('lifecycle_state')}; new "
                      "classification against it fails closed — re-pin a live version")

    kernel_manifest = load(CORE_DIR / "package.yaml")
    kernel_concepts, kernel_relations = load_terms(CORE_DIR, kernel_manifest)
    concepts, relations = load_terms(pkg_dir, manifest)

    worker_scope: dict = {}
    purpose = args.purpose
    requested: list[str] = []
    truncation_allowed = args.truncate
    if args.profile:
        prof = load(pkg_dir / args.profile)
        if prof.get("kind") != "xfactory_semantic_context_profile":
            return refuse("profile has the wrong kind")
        requested = list(prof.get("required_terms", []))
        purpose = purpose or prof.get("purpose")
        worker_scope = prof.get("worker_scope") or {}
        truncation_allowed = truncation_allowed and bool(prof.get("truncation_allowed"))
        if args.truncate and not prof.get("truncation_allowed"):
            return refuse("profile does not allow truncation")
    elif args.terms:
        requested = [t.strip() for t in args.terms.split(",") if t.strip()]
    if not requested:
        return refuse("a bounded term subset is required (--terms or --profile); "
                      "there is no unrestricted ontology mode")
    if not purpose:
        return refuse("--purpose is required when no profile supplies one")

    def lookup_concept(tid: str) -> dict | None:
        return concepts.get(tid) or kernel_concepts.get(tid)

    def lookup_relation(tid: str) -> dict | None:
        return relations.get(tid) or kernel_relations.get(tid)

    for tid in requested:
        if lookup_concept(tid) is None and lookup_relation(tid) is None:
            return refuse(f"requested term {tid} does not resolve in the package or kernel")

    # Closure over specialization ancestors and relation endpoints.
    subset = set(requested)
    omitted: set[str] = set()
    queue = list(requested)
    while queue:
        tid = queue.pop()
        cdef = lookup_concept(tid)
        members: list[str] = []
        if cdef is not None:
            members = list(cdef.get("parents", []))
        else:
            rdef = lookup_relation(tid)
            if rdef is not None:
                members = list(rdef.get("domain", [])) + list(rdef.get("range", []))
        for member in members:
            if member in subset or member in omitted:
                continue
            if truncation_allowed:
                omitted.add(member)
            else:
                subset.add(member)
                queue.append(member)

    # Tenant binding: exact package identity, every target resolves.
    binding_block: list[str] = []
    binding_ref = None
    if args.tenant_binding:
        binding = load(args.tenant_binding)
        if binding.get("package_id") != package_id or \
                binding.get("package_digest") != manifest.get("package_digest"):
            return refuse("tenant binding is pinned to a different package identity; "
                          "the tenant re-validates its bindings at adoption")
        for entry in binding.get("bindings", []) or []:
            target = entry.get("concept_id")
            cdef = lookup_concept(target)
            if cdef is None or cdef.get("lifecycle_state") == "retired":
                return refuse(f"tenant binding target {target} is retired or absent "
                              "from the pinned package")
        binding_ref = binding.get("binding_id")
        binding_block = [
            "tenant_binding:",
            f"  binding_id: {binding_ref}",
            f"  package_id: {package_id}",
            f"  package_digest: {manifest.get('package_digest')}",
        ]

    lines = [
        "schema_version: 1",
        "kind: xfactory_semantic_context",
        f"context_id: {args.context_id}",
        f"purpose: {purpose}",
    ]
    if worker_scope:
        lines.append("worker_scope:")
        if worker_scope.get("worker_archetype"):
            lines.append(f"  worker_archetype: {worker_scope['worker_archetype']}")
        if worker_scope.get("worker_class"):
            lines.append(f"  worker_class: {worker_scope['worker_class']}")
    lines += [
        "kernel_pin:",
        f"  package_id: {kernel_manifest.get('package_id')}",
        f"  package_version: {kernel_manifest.get('package_version')}",
        f"  package_digest: {kernel_manifest.get('package_digest')}",
        "package_pin:",
        f"  package_id: {package_id}",
        f"  package_version: {manifest.get('package_version')}",
        f"  package_digest: {manifest.get('package_digest')}",
    ]
    lines += binding_block
    lines.append("terms:")
    lines += [f"  - {t}" for t in sorted(subset)]
    lines.append("closure:")
    if omitted:
        lines.append("  status: truncated")
        lines.append("  omitted:")
        lines += [f"    - {t}" for t in sorted(omitted)]
    else:
        lines.append("  status: closed")
    if args.compiled_at or args.ttl:
        lines.append("freshness:")
        if args.compiled_at:
            lines.append(f"  compiled_at: \"{args.compiled_at}\"")
        if args.ttl:
            lines.append(f"  ttl_seconds: {args.ttl}")
    body = "\n".join(lines)
    digest = hashlib.sha256((body + "\ncontent_digest:").encode("utf-8")).hexdigest()
    artifact = body + f"\ncontent_digest: {digest}\n"

    if args.out:
        args.out.write_text(artifact, encoding="utf-8")
        print(f"COMPILED {args.context_id} -> {args.out} "
              f"({len(subset)} term(s), {'truncated' if omitted else 'closed'})")
    else:
        sys.stdout.write(artifact)
    return 0


if __name__ == "__main__":
    sys.exit(main())
