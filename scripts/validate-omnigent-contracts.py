#!/usr/bin/env python3
"""Validate the omnigent contract family (add-omnigent-domain-overlay).

Checks, fail-closed:
  1. Both schemas under contracts/omnigent/ parse and are valid
     Draft 2020-12 JSON Schemas.
  2. Positive examples validate against their schema.
  3. Every negative fixture FAILS validation, and at least one reported
     violation matches the fixture's leading ``# expect: <substring>``
     marker (matched against the error message plus its JSON path).
  4. Semantic invariants the schema cannot express:
     - credential tier disjointness: no family listed in
       ``never_assignable`` may appear in ``all_classes``, ``by_class``,
       or ``unassigned_by_default``;
     - worker ids are unique;
     - canonical vocabulary lint: no mapping key in an instance document
       contains a ``customer`` or ``client`` word segment (legacy layer
       vocabulary; the pinned upstream Hermes runtime manifest is outside
       these documents);
     - crystallized-executor bindings (add-crystallizer-contracts): a
       class marked ``crystallized`` carries capability_ref /
       automation_rung / replaces_configuration / throttle, resolves its
       replaced class in the same overlay, and never exceeds it in
       permissions or by_class credential families (authority
       conservation);
     - rung_ceilings categories are unique;
     - install ``semantic_contexts`` entries are unique per worker class
       (add-omnigent-semantic-wiring).
  5. Repo mode: ``validate-omnigent-contracts.py <domain-repo>`` validates
     the repo's omnigent/domain-overlay.yaml (schema + semantics) and,
     when hermes/domain/ontology/ exists, resolves every worker
     ``semantic_context`` declaration to an inventoried
     xfactory_semantic_context_profile with the declared package_id whose
     worker_scope matches the worker (archetype or class equality) —
     unresolved or scope-mismatched declarations fail.

Exit code 0 only if every check passes.
"""

from __future__ import annotations

import functools
import hashlib
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

# Running this file as a script puts only the `scripts/` directory on sys.path;
# add the repository root so the sibling reader is imported under the SAME
# spelling the test suite uses (`scripts.standards_body_registry`) rather than a
# second, bare one. The pattern is `validate-contract-release.py`'s, which does
# this for the same reason: a hyphenated entrypoint cannot itself be imported as
# a module, so the shared code lives in an importable sibling and both callers
# must agree on how to name it.
_ENTRYPOINT_REPO = Path(__file__).resolve().parent.parent
if str(_ENTRYPOINT_REPO) not in sys.path:
    sys.path.insert(0, str(_ENTRYPOINT_REPO))

from scripts.standards_body_registry import (  # noqa: E402
    DuplicateRegistryKey,
    load_registry,
    registry_errors,
)

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = ROOT / "contracts" / "omnigent"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "fixtures" / "negative"

SCHEMA_FILES = {
    "omnigent_domain_overlay": CONTRACT_DIR / "omnigent-domain-overlay.schema.yaml",
    "omnigent_install_manifest": CONTRACT_DIR / "omnigent-install-manifest.schema.yaml",
}
POSITIVE_EXAMPLES = {
    "omnigent_domain_overlay": EXAMPLES_DIR / "omnigent-domain-overlay.example.yaml",
    "omnigent_install_manifest": EXAMPLES_DIR / "omnigent-install-manifest.example.yaml",
}

LEGACY_KEY_SEGMENT = re.compile(r"(^|_)(customer|client)(_|$)")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)
    print(f"FAIL {message}")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def schema_kind_for(path: Path) -> str:
    return "omnigent_domain_overlay" if path.name.startswith("overlay-") else "omnigent_install_manifest"


def iter_keys(node, prefix="$"):
    if isinstance(node, dict):
        for key, value in node.items():
            yield f"{prefix}.{key}", key
            yield from iter_keys(value, f"{prefix}.{key}")
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from iter_keys(item, f"{prefix}[{index}]")


STANDARDS_BODIES = ROOT / "contracts" / "policies" / "standards-bodies.yaml"
# Resolved once, because `Path.relative_to` raises when the registry sits
# outside ROOT and the reporting lines below must not be the thing that fails.
REGISTRY_REL = "contracts/policies/standards-bodies.yaml"


@functools.lru_cache(maxsize=1)
def standards_body_ids() -> frozenset[str]:
    """Canonical standards-body ids a terminology crosswalk may reference.

    Returns an empty `frozenset()` when the registry is absent so the check
    degrades to a no-op rather than failing every overlay in a checkout
    without it.

    CACHED because it is called once per example, fixture and repo argument,
    and the registry cannot change inside one run. Without it a duplicate-key
    refusal is REPORTED ONCE PER CALLER — the same defect printed eighteen times
    — and 77 KB of YAML is re-parsed for each.

    READS THROUGH `load_registry`, NOT `load_yaml`. This function is the OTHER
    reader of the same file, and leaving it on `yaml.safe_load` would re-open
    the exact duplicate-key collapse `load_registry` was added to close — worse
    here than anywhere, because this set decides which crosswalk ids RESOLVE:
    a duplicated `id` key would silently change the resolved set and a crosswalk
    would be accepted or rejected on a document nobody wrote. A duplicate is
    reported once and the set degrades to empty, matching the absent-file arm
    above rather than raising through `semantic_errors`.
    """
    if not STANDARDS_BODIES.is_file():
        return frozenset()
    try:
        doc = load_registry(STANDARDS_BODIES) or {}
    except DuplicateRegistryKey as exc:
        fail(f"standards-body registry: {exc}")
        return frozenset()
    except yaml.YAMLError as exc:
        # A registry that does not PARSE is a validator failure, never a
        # traceback: `load_registry` raises `YAMLError` for a syntax error and
        # for the `ConstructorError` an unhashable key produces, and
        # `DuplicateRegistryKey` is a `ValueError`, so neither `except` covers
        # the other. `yaml.safe_load` behaved this way here before the loader
        # swap too — this arm makes the "degrades to a no-op" the docstring
        # already promised actually true, rather than repairing a regression.
        fail(f"standards-body registry does not parse: {exc}")
        return frozenset()
    return frozenset(
        body["id"]
        for body in (doc.get("bodies") or [])
        if isinstance(body, dict) and body.get("id")
    )


def semantic_errors(kind: str, doc) -> list[str]:
    errors: list[str] = []
    for path, key in iter_keys(doc):
        # Terminology keys are REFERENCES to ids the overlay already declares
        # (the orphan check below enforces that), not new governance
        # vocabulary — and some declared ids legitimately carry a frozen
        # machine key such as `client_infrastructure_request` from the neutral
        # contract. Without this exemption the same string is legal as a
        # job_types array item and illegal as its own terminology key, which
        # is a lint artifact rather than the rule's intent. Surfaced by the
        # first real population (OpsxFactory, 2026-08-09).
        if path.startswith("$.terminology."):
            continue
        if LEGACY_KEY_SEGMENT.search(key):
            errors.append(f"{path}: legacy vocabulary key '{key}' (use subject/tenant/domain spellings)")
    if kind == "omnigent_domain_overlay" and isinstance(doc, dict):
        workers = doc.get("workers") or []
        ids = [w.get("id") for w in workers if isinstance(w, dict)]
        for worker_id in {i for i in ids if ids.count(i) > 1}:
            errors.append(f"$.workers: duplicate worker id '{worker_id}'")
        creds = doc.get("credential_requirements") or {}
        never = set(creds.get("never_assignable") or [])
        assignable: set[str] = set(creds.get("all_classes") or [])
        assignable.update(creds.get("unassigned_by_default") or [])
        for families in (creds.get("by_class") or {}).values():
            assignable.update(families or [])
        for family in sorted(never & assignable):
            errors.append(
                f"$.credential_requirements: never_assignable family '{family}' "
                "is also declared grantable (no approval path may override never_assignable)"
            )
        workers_by_id = {w.get("id"): w for w in workers if isinstance(w, dict)}
        by_class = creds.get("by_class") or {}
        for worker in workers:
            if not isinstance(worker, dict) or not worker.get("crystallized"):
                continue
            wid = worker.get("id")
            for required_field in ("capability_ref", "automation_rung", "replaces_configuration", "throttle"):
                if not worker.get(required_field):
                    errors.append(
                        f"$.workers[{wid}]: crystallized class missing '{required_field}'"
                    )
            replaced_id = worker.get("replaces_configuration")
            replaced = workers_by_id.get(replaced_id) if replaced_id else None
            if replaced_id and replaced is None:
                errors.append(
                    f"$.workers[{wid}]: replaces_configuration '{replaced_id}' "
                    "does not name a worker class in this overlay"
                )
            if isinstance(replaced, dict):
                own_perms = worker.get("permissions") or {}
                replaced_perms = replaced.get("permissions") or {}
                for perm, value in own_perms.items():
                    if value is True and replaced_perms.get(perm) is not True:
                        errors.append(
                            f"$.workers[{wid}]: permission '{perm}' exceeds "
                            f"replaces_configuration '{replaced_id}' "
                            "(authority conservation: crystallization never widens)"
                        )
                own_families = set(by_class.get(wid) or [])
                replaced_families = set(by_class.get(replaced_id) or [])
                for family in sorted(own_families - replaced_families):
                    errors.append(
                        f"$.workers[{wid}]: credential family '{family}' exceeds "
                        f"replaces_configuration '{replaced_id}' "
                        "(authority conservation: crystallization never widens)"
                    )
        # Terminology (add-omnigent-domain-terminology): display labels are
        # presentation only, but they must describe THIS overlay — an orphan
        # label names a class/condition that does not exist, and a duplicate
        # label makes two different things read identically in a notice.
        terminology = doc.get("terminology") or {}
        if isinstance(terminology, dict):
            declared = {
                "workers": {w.get("id") for w in workers if isinstance(w, dict)},
                "job_types": set(doc.get("job_types") or []),
                "stop_conditions": set(doc.get("stop_conditions") or []),
                "routing": set((doc.get("routing") or {}).keys()),
            }
            for vocabulary, entries in terminology.items():
                if not isinstance(entries, dict):
                    continue
                known = declared.get(vocabulary, set())
                seen_labels: dict[str, str] = {}
                for key, value in entries.items():
                    if key not in known:
                        errors.append(
                            f"$.terminology.{vocabulary}: '{key}' does not name a "
                            f"{vocabulary} id declared in this overlay"
                        )
                    label = (
                        value.get("display_label")
                        if isinstance(value, dict)
                        else value
                    )
                    if isinstance(label, str):
                        if label in seen_labels:
                            errors.append(
                                f"$.terminology.{vocabulary}: duplicate display label "
                                f"'{label}' on '{key}' and '{seen_labels[label]}' "
                                "(two ids would read identically in a notice)"
                            )
                        else:
                            seen_labels[label] = key
                    # Crosswalks: one entry per standards body, each body id
                    # resolving to the canonical registry (five repos writing
                    # free-text names would drift itil/ITIL v4/itil4), and the
                    # honesty rule per body — declaring no counterpart is legal
                    # and preferred over a forced mapping, but must say why.
                    if isinstance(value, dict):
                        known_bodies = standards_body_ids()
                        for body, entry in (value.get("standards_alignment") or {}).items():
                            if known_bodies and body not in known_bodies:
                                errors.append(
                                    f"$.terminology.workers.{key}.standards_alignment: "
                                    f"'{body}' does not resolve to a body in "
                                    "contracts/policies/standards-bodies.yaml"
                                )
                            if not isinstance(entry, dict):
                                continue
                            if (
                                entry.get("mapping") == "no_clean_equivalent"
                                and not entry.get("note")
                            ):
                                errors.append(
                                    f"$.terminology.workers.{key}.standards_alignment."
                                    f"{body}: 'no_clean_equivalent' requires a note "
                                    "saying why"
                                )
        seen_categories: set[str] = set()
        for entry in doc.get("rung_ceilings") or []:
            if not isinstance(entry, dict):
                continue
            category = entry.get("category")
            if category in seen_categories:
                errors.append(f"$.rung_ceilings: duplicate category '{category}'")
            if category is not None:
                seen_categories.add(category)
    if kind == "omnigent_install_manifest" and isinstance(doc, dict):
        sem = doc.get("semantic_contexts") or {}
        entries = sem.get("contexts") or []
        classes = [e.get("worker_class") for e in entries if isinstance(e, dict)]
        for wc in sorted({c for c in classes if classes.count(c) > 1}):
            errors.append(f"$.semantic_contexts: duplicate worker_class '{wc}' "
                          "(one compiled context per declaring worker)")
    return errors


def overlay_profile_errors(overlay: dict, ontology_dir: Path) -> list[str]:
    """Repo-mode cross-check (add-omnigent-semantic-wiring): every worker
    semantic_context declaration resolves to an inventoried profile of the
    declared package whose worker_scope matches the worker."""
    errors: list[str] = []
    manifest = load_yaml(ontology_dir / "package.yaml") or {}
    profiles: dict[str, dict] = {}
    for item in manifest.get("inventory", []) or []:
        fp = ontology_dir / item.get("path", "")
        if not fp.is_file():
            continue
        doc = load_yaml(fp)
        if isinstance(doc, dict) and doc.get("kind") == "xfactory_semantic_context_profile":
            profiles[str(doc.get("profile_id"))] = doc
    for worker in overlay.get("workers") or []:
        if not isinstance(worker, dict):
            continue
        sem = worker.get("semantic_context")
        if not sem:
            continue
        wid = worker.get("id")
        prof = profiles.get(str(sem.get("profile_id")))
        if prof is None:
            errors.append(
                f"$.workers[{wid}]: semantic_context profile "
                f"'{sem.get('profile_id')}' is not an inventoried profile of "
                "the domain ontology package")
            continue
        if prof.get("package_id") != sem.get("package_id"):
            errors.append(
                f"$.workers[{wid}]: profile '{sem.get('profile_id')}' belongs to "
                f"package '{prof.get('package_id')}', declared "
                f"'{sem.get('package_id')}'")
        scope = prof.get("worker_scope") or {}
        if scope.get("worker_archetype") != worker.get("archetype") and \
                scope.get("worker_class") != wid:
            errors.append(
                f"$.workers[{wid}]: profile '{sem.get('profile_id')}' worker_scope "
                f"(archetype={scope.get('worker_archetype')!r}, "
                f"class={scope.get('worker_class')!r}) matches neither the "
                f"worker's archetype '{worker.get('archetype')}' nor its class")
    return errors


def install_wiring_errors(manifest: dict, overlay: dict,
                          install_root: Path) -> list[str]:
    """Canonical install-side wiring checks (add-omnigent-semantic-wiring):
    both-direction completeness against the pinned overlay's declaring
    workers, and per-artifact pin/digest/scope agreement. The caller
    supplies the resolved overlay document (installs keep exact pinned
    copies per the consumption rule); deep context semantics stay with the
    canonical ontology validator over the same artifact bytes."""
    errors: list[str] = []
    sem = (manifest or {}).get("semantic_contexts") or {}
    entry_list = [e for e in sem.get("contexts") or [] if isinstance(e, dict)]
    classes = [str(e.get("worker_class")) for e in entry_list]
    for wc in sorted({c for c in classes if classes.count(c) > 1}):
        # Standalone parity with semantic_errors (review finding N6): the
        # canonical function must not silently collapse duplicates.
        errors.append(f"$.semantic_contexts: duplicate worker_class '{wc}' "
                      "(one compiled context per declaring worker)")
    entries = {str(e.get("worker_class")): e for e in entry_list}
    declaring = {str(w.get("id")): w for w in (overlay or {}).get("workers") or []
                 if isinstance(w, dict) and w.get("semantic_context")}
    for wid in sorted(set(declaring) - set(entries)):
        errors.append(f"$.semantic_contexts: declaring worker '{wid}' has no "
                      "pinned compiled context — a worker never launches "
                      "without the bounded meaning its overlay declares")
    for wid in sorted(set(entries) - set(declaring)):
        errors.append(f"$.semantic_contexts: context entry '{wid}' names no "
                      "declaring worker in the pinned overlay")
    kernel_pin = sem.get("kernel") or {}
    package_pin = sem.get("ontology_package") or {}
    for wid in sorted(set(declaring) & set(entries)):
        entry = entries[wid]
        worker = declaring[wid]
        fp = install_root / str(entry.get("path"))
        if not fp.is_file():
            errors.append(f"$.semantic_contexts[{wid}]: committed artifact "
                          f"missing: {entry.get('path')}")
            continue
        doc = load_yaml(fp) or {}
        if doc.get("kind") != "xfactory_semantic_context":
            errors.append(f"$.semantic_contexts[{wid}]: artifact is not an "
                          "xfactory_semantic_context document")
            continue
        if doc.get("content_digest") != entry.get("content_digest"):
            errors.append(f"$.semantic_contexts[{wid}]: artifact content_digest "
                          "disagrees with the pinned entry")
        # The digest is a SEAL, not a label (review finding N5): recompute it
        # from the artifact bytes with the compile tool's own derivation, so
        # a widened body with an untouched digest line fails closed.
        raw = fp.read_text(encoding="utf-8")
        body, sep, _tail = raw.rpartition("\ncontent_digest: ")
        recomputed = (hashlib.sha256((body + "\ncontent_digest:").encode("utf-8"))
                      .hexdigest() if sep else None)
        if recomputed != entry.get("content_digest"):
            errors.append(f"$.semantic_contexts[{wid}]: content_digest does not "
                          "recompute from the artifact bytes — the worker would "
                          "receive terms its profile never authorized")
        for pin_name, pin in (("kernel_pin", kernel_pin),
                              ("package_pin", package_pin)):
            embedded = doc.get(pin_name) or {}
            if embedded.get("package_id") != pin.get("package_id") or \
                    embedded.get("package_digest") != pin.get("package_digest"):
                errors.append(f"$.semantic_contexts[{wid}]: artifact {pin_name} "
                              "disagrees with the section pin")
        scope = doc.get("worker_scope") or {}
        if scope.get("worker_archetype") != worker.get("archetype") and \
                scope.get("worker_class") != wid:
            errors.append(f"$.semantic_contexts[{wid}]: artifact worker_scope "
                          "matches neither the worker's archetype nor its class")
    return errors


def validate_repo(repo: Path, validators: dict[str, Draft202012Validator]) -> None:
    overlay_path = repo / "omnigent" / "domain-overlay.yaml"
    if not overlay_path.is_file():
        fail(f"repo mode: {overlay_path} not found")
        return
    overlay = load_yaml(overlay_path)
    violations = all_violations(validators["omnigent_domain_overlay"],
                                "omnigent_domain_overlay", overlay)
    ontology_dir = repo / "hermes" / "domain" / "ontology"
    if ontology_dir.is_dir():
        violations.extend(overlay_profile_errors(overlay, ontology_dir))
    else:
        for worker in (overlay or {}).get("workers") or []:
            if isinstance(worker, dict) and worker.get("semantic_context"):
                violations.append(
                    f"$.workers[{worker.get('id')}]: semantic_context declared "
                    "but the repository has no hermes/domain/ontology package "
                    "to resolve it against")
    if violations:
        fail(f"repo overlay rejected: {overlay_path}")
        for violation in violations:
            print(f"       {violation}")
    else:
        print(f"ok   repo overlay validates: {overlay_path}")


def all_violations(validator: Draft202012Validator, kind: str, doc) -> list[str]:
    violations = [
        f"{error.json_path}: {error.message}"
        for error in validator.iter_errors(doc)
    ]
    violations.extend(semantic_errors(kind, doc))
    return violations


def main() -> int:
    validators: dict[str, Draft202012Validator] = {}
    for kind, path in SCHEMA_FILES.items():
        schema = load_yaml(path)
        Draft202012Validator.check_schema(schema)
        validators[kind] = Draft202012Validator(schema)
        print(f"ok   schema parses and is valid: {path.relative_to(ROOT)}")

    # The registry is validated BEFORE the overlays that resolve ids through it,
    # so an incomplete current-publication record or an unqualified operator
    # override is reported as the registry defect it is rather than as a
    # downstream crosswalk failure. The absent-file case DEGRADES TO A NO-OP
    # rather than raising, matching `standards_body_ids()` above: a checkout
    # without the registry must not fail every check that mentions it.
    if not STANDARDS_BODIES.is_file():
        print(f"skip standards-body registry absent: {REGISTRY_REL}")
    else:
        try:
            registry_findings = registry_errors(load_registry(STANDARDS_BODIES))
        except DuplicateRegistryKey as exc:
            # A duplicate key is refused at LOAD time, so there is no document
            # to check: report it as the one finding it is rather than letting
            # the traceback stand in for a validator failure.
            fail(f"standards-body registry: {exc}")
        except yaml.YAMLError as exc:
            # Same reasoning, one class wider: a registry that does not parse
            # at all. THIS arm is new behaviour rather than preserved — `main()`
            # did not read the registry before this change, so without it the
            # change would have introduced a traceback where the validator used
            # to report findings.
            fail(f"standards-body registry does not parse: {exc}")
        else:
            for violation in registry_findings:
                fail(f"standards-body registry: {violation}")
            if not registry_findings:
                print(
                    "ok   standards-body registry current-publication and "
                    f"override records: {REGISTRY_REL}"
                )

    for kind, path in POSITIVE_EXAMPLES.items():
        violations = all_violations(validators[kind], kind, load_yaml(path))
        if violations:
            fail(f"positive example rejected: {path.relative_to(ROOT)}")
            for violation in violations:
                print(f"       {violation}")
        else:
            print(f"ok   positive example validates: {path.relative_to(ROOT)}")

    negative_fixtures = sorted(NEGATIVE_DIR.glob("*.yaml"))
    if not negative_fixtures:
        fail(f"no negative fixtures found under {NEGATIVE_DIR.relative_to(ROOT)}")
    for path in negative_fixtures:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        marker = re.match(r"#\s*expect:\s*(\S+)", first_line)
        if not marker:
            fail(f"negative fixture missing '# expect:' marker: {path.relative_to(ROOT)}")
            continue
        expected = marker.group(1)
        kind = schema_kind_for(path)
        violations = all_violations(validators[kind], kind, load_yaml(path))
        if not violations:
            fail(f"negative fixture unexpectedly validates: {path.relative_to(ROOT)}")
        elif not any(expected in violation for violation in violations):
            fail(
                f"negative fixture failed for the wrong reason: {path.relative_to(ROOT)} "
                f"(expected a violation mentioning '{expected}')"
            )
            for violation in violations:
                print(f"       {violation}")
        else:
            print(f"ok   negative fixture rejected as expected ({expected}): {path.relative_to(ROOT)}")

    for repo_arg in sys.argv[1:]:
        validate_repo(Path(repo_arg).resolve(), validators)

    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nAll omnigent contract checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
