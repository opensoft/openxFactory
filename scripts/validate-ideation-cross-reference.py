#!/usr/bin/env python3
"""Validate the ideation cross-reference readiness index (add-ideation-cross-reference-readiness).

Change task 2.3 (`openspec/changes/add-ideation-cross-reference-readiness/tasks.md`):
a strict validator for the unified cross-stage cross-reference readiness index —
the structured `ideation/cross-reference.yaml` (source of truth; `.md` is a
generated projection, task 2.4). It layers the deterministic, corpus-resolving
invariants JSON Schema alone cannot express (documented in
`contracts/schemas/ideation-cross-reference.schema.yaml`'s own CO-LOAD /
validator-side notes — those comments ARE the requirements) on top of plain
draft-2020-12 validation, and attaches a `FormatChecker` so `date`/`date-time`
are enforced, not merely annotated.

FOUR-schema co-load (schema CO-LOAD block; extends review condition C3's named
two to four). Every cross-file `$ref` resolves in one offline registry:
    ideation-cross-reference.schema.yaml       (kind: ideation-cross-reference)
    ideation-possibles-register.schema.yaml    (`possibles_register` embed)
    ideation-dashboard-snapshot.schema.yaml    (`generation`, `lifecycle_status`,
                                                and transitively `evidence_pin`)
    xfactory-idea-routing-reference.schema.yaml (structured member/score refs)

Validator-side rules (beyond plain schema conformance):

  Extension-fit resolution
      Every `extension_fit` with `has_promoted_fit: true` MUST name a
      `promoted_spec` that resolves to a promoted-or-being-promoted capability:
      a directory under `openspec/specs/<name>/`, OR a spec-delta capability
      directory `openspec/changes/<change>/specs/<name>/` of a NON-archived
      change (a capability this or a sibling active change promotes, e.g.
      `ideation-cross-reference`). A `promoted_spec` that is a path/folder
      (contains `/`, e.g. an `openspec/changes/archive/...` pointer) or a bare
      name that resolves to neither set is an error (spec "Extension-fit
      citation"; scenario "A fit note cites only an archive folder" -> the
      readiness lane emits an `ideation-readiness` finding). Schema alone cannot
      resolve a name against the promoted spec set; the negative fixture
      `archive-pointer-only-fit.yaml` is schema-VALID by design and fails HERE.

      IMPLEMENTATION CHOICE (needs spec confirmation, task 3.4): the resolution
      set includes active-change capability deltas, not only promoted
      `openspec/specs/` dirs, so a cluster may cite a capability that a sibling
      active change is promoting (as the packaged valid example cites
      `ideation-cross-reference`). The spec's own words are "the specific
      promoted spec OR capability"; the discriminator the spec draws is
      capability-NAME vs archive-FOLDER, which this preserves.

  Gate arithmetic (min >= 8)
      A `recommendation.flagged: true` is legitimate IFF all three tiers
      (domain, company, project) are present AND scored AND the MINIMUM of the
      three scores is >= 8 (spec "Readiness recommendation gate"; scenarios
      "All tiers agree" / "One tier disagrees"). Flagged with an absent or
      unscored tier, or flagged below the min-8 threshold, is an error; and a
      gate that SHOULD have fired (all three scored, min >= 8) but is
      `flagged: false` is an error (the gate is deterministic, not discretionary).

  Spread-conflict consistency
      A wide inter-tier spread SHALL be surfaced as a `tier-spread` conflict flag
      even below the min-8 threshold (spec "Readiness recommendation gate";
      scenario "Tiers diverge below threshold"). The spec does not fix a numeric
      threshold; this validator uses SPREAD_THRESHOLD = 4 over the SCORED tiers
      (max score - min score >= 4 requires a `tier-spread` flag) and DOCUMENTS
      it as an implementation choice needing spec confirmation (task 3.4). A
      declared `spread` value on the flag that disagrees with the computed
      scored spread is a WARNING (determinism nudge), not an error.

  Topic-entry id uniqueness
      `topic_entry.id` is unique across the index (the snapshot's `cluster.id`
      join and a possible's `claiming_clusters` edge both key on it).

  Member stage vocabulary and unscored-reason completeness are SCHEMA-enforced
  (member `stage` $refs `lifecycle_status`; a tier without `score` requires
  `unscored_reason` via the schema's `allOf`); they surface as schema-layer
  errors and need no separate rule here.

  Ownership line (C3): register-entry shapes/transitions are NOT re-validated
  here. An embedded `possibles_register` is confirmed structurally
  present-and-parseable (its entry SHAPES are validated by the schema `$ref`,
  its id-uniqueness and cross-snapshot TRANSITIONS are DELEGATED to
  `scripts/validate-ideation-dashboard-contracts.py` — run it separately).

Usage:
    # Default: self-test the packaged examples and scan the checkout for the
    # real index (ideation/cross-reference.yaml).
    python3 scripts/validate-ideation-cross-reference.py [--repo REPO] [--strict]

    # Validate one file (kind auto-detected) or a directory sweep.
    python3 scripts/validate-ideation-cross-reference.py PATH [--strict]

Exit codes: 0 ok, 1 findings (or warnings under --strict), 2 harness error.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "ideation-cross-reference"

# The four schemas the index's cross-file `$ref`s resolve into (schema CO-LOAD).
SCHEMA_FILENAMES = [
    "ideation-cross-reference.schema.yaml",
    "ideation-possibles-register.schema.yaml",
    "ideation-dashboard-snapshot.schema.yaml",
    "xfactory-idea-routing-reference.schema.yaml",
]

INDEX_KIND = "ideation-cross-reference"
INDEX_SCHEMA = "ideation-cross-reference.schema.yaml"

# Documented implementation choice (see module docstring): the scored-tier
# spread at or above which a `tier-spread` conflict flag is mandatory.
SPREAD_THRESHOLD = 4
TIER_NAMES = ("domain", "company", "project")

# A single FormatChecker shared by every validator run: date/date-time enforced.
FORMAT_CHECKER = FormatChecker()

# Negative fixtures and the rule (error-code prefix) each is expected to trip,
# so the self-test proves each negative fails for its INTENDED reason.
NEGATIVE_EXPECTED = {
    "score-out-of-range": "schema",     # tier score 11 > 10 -> schema layer
    "archive-pointer-only-fit": "xref-fit",  # archive-folder fit note -> validator layer
}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(f"note  {msg}")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline registry over all four schemas so the index's cross-file `$ref`s
    (routing-reference kernel, snapshot `generation`/`lifecycle_status`, and the
    possibles-register embed that transitively `$ref`s the snapshot's
    `evidence_pin`) resolve — same approach as the sibling dashboard validator."""
    resources = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(SCHEMAS_DIR / name)
        docs[name] = doc
        rid = doc.get("$id", name)
        resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
    return Registry().with_resources(resources), docs


def index_validator(registry: Registry, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(docs[INDEX_SCHEMA], registry=registry, format_checker=FORMAT_CHECKER)


def iter_errors(validator: Draft202012Validator, instance: Any):
    return sorted(validator.iter_errors(instance), key=lambda e: [str(p) for p in e.absolute_path])


def detect(doc: Any) -> str | None:
    """Return the index kind if this is an ideation-cross-reference document."""
    if isinstance(doc, dict) and doc.get("kind") == INDEX_KIND:
        return INDEX_KIND
    return None


# ------------------- promoted / active capability resolution -------------------

def resolve_capability_set(repo: Path) -> set[str]:
    """Names that a `promoted_spec` may legitimately cite: promoted spec
    directories under `openspec/specs/`, plus spec-delta capability directories
    of NON-archived changes under `openspec/changes/<change>/specs/`. The
    archive subtree is excluded so an archive-folder pointer never resolves."""
    caps: set[str] = set()
    specs_dir = repo / "openspec" / "specs"
    if specs_dir.is_dir():
        caps |= {p.name for p in specs_dir.iterdir() if p.is_dir()}
    changes_dir = repo / "openspec" / "changes"
    if changes_dir.is_dir():
        for change in changes_dir.iterdir():
            if not change.is_dir() or change.name == "archive":
                continue
            delta_specs = change / "specs"
            if delta_specs.is_dir():
                caps |= {p.name for p in delta_specs.iterdir() if p.is_dir()}
    return caps


# --------------------- per-instance validation (schema + rules) ---------------------

def validate_instance(
    f: Findings, label: str, doc: Any, registry: Registry, docs: dict[str, dict],
    capability_set: set[str],
) -> str | None:
    """Validate one loaded document: schema conformance plus the index's
    validator-side rules. Returns the routing tag, or None if unrecognized."""
    tag = detect(doc)
    if tag is None:
        f.error("kind", f"{label}: unrecognized document (kind is not {INDEX_KIND!r})")
        return None

    for e in iter_errors(index_validator(registry, docs), doc):
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        f.error("schema", f"{label}: {loc}: {e.message}")

    check_extension_fit(f, label, doc, capability_set)
    check_gate_arithmetic(f, label, doc)
    check_spread_conflict(f, label, doc)
    check_topic_id_uniqueness(f, label, doc)
    note_possibles_register(f, label, doc)
    return tag


# --------------------------- extension-fit resolution ---------------------------

def check_extension_fit(f: Findings, label: str, doc: dict, capability_set: set[str]) -> None:
    for entry in doc.get("topic_entries") or []:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id", "<no-id>")
        fit = entry.get("extension_fit")
        if not isinstance(fit, dict):
            continue  # schema already flags a missing/mistyped extension_fit
        if not fit.get("has_promoted_fit"):
            continue  # a no-fit statement carries no promoted_spec to resolve
        spec = fit.get("promoted_spec")
        if not isinstance(spec, str) or not spec:
            continue  # schema requires a non-empty promoted_spec when has_promoted_fit
        if "/" in spec or "\\" in spec:
            hint = ""
            if "changes/archive/" in spec or spec.startswith("openspec/changes/"):
                hint = " (an archived change folder alone does not satisfy the citation)"
            f.error("xref-fit-not-a-capability",
                    f"{label}: topic entry {eid!r} extension_fit.promoted_spec {spec!r} names a "
                    f"path/folder, not a promoted spec or capability{hint}")
            continue
        if spec not in capability_set:
            f.error("xref-fit-dangling",
                    f"{label}: topic entry {eid!r} extension_fit.promoted_spec {spec!r} resolves to no "
                    f"promoted spec (openspec/specs/) or active-change capability delta")


# --------------------------- gate arithmetic ---------------------------

def _scored_tiers(readiness: Any) -> dict[str, Any]:
    """Map tier name -> assessment for tiers that carry a numeric `score`."""
    out: dict[str, Any] = {}
    if not isinstance(readiness, dict):
        return out
    for t in readiness.get("tiers") or []:
        if isinstance(t, dict) and isinstance(t.get("score"), int) and t.get("tier"):
            out[t["tier"]] = t
    return out


def _all_tiers(readiness: Any) -> set[str]:
    names: set[str] = set()
    if isinstance(readiness, dict):
        for t in readiness.get("tiers") or []:
            if isinstance(t, dict) and t.get("tier"):
                names.add(t["tier"])
    return names


def gate_eligible(readiness: Any) -> tuple[bool, str]:
    """A recommendation may legitimately fire IFF all three tiers are present,
    scored, and their minimum is >= 8. Returns (eligible, reason-if-not)."""
    scored = _scored_tiers(readiness)
    present = _all_tiers(readiness)
    missing_or_unscored = [n for n in TIER_NAMES if n not in scored]
    if missing_or_unscored:
        absent = [n for n in TIER_NAMES if n not in present]
        unscored = [n for n in missing_or_unscored if n in present]
        bits = []
        if absent:
            bits.append(f"absent tier(s) {absent}")
        if unscored:
            bits.append(f"unscored tier(s) {unscored}")
        return False, "; ".join(bits)
    scores = [scored[n]["score"] for n in TIER_NAMES]
    if min(scores) < 8:
        return False, f"minimum tier score is {min(scores)} (< 8): {dict(zip(TIER_NAMES, scores))}"
    return True, ""


def check_gate_arithmetic(f: Findings, label: str, doc: dict) -> None:
    for entry in doc.get("topic_entries") or []:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id", "<no-id>")
        readiness = entry.get("readiness")
        rec = readiness.get("recommendation") if isinstance(readiness, dict) else None
        if not isinstance(rec, dict) or "flagged" not in rec:
            continue  # unscored / un-run entry carries no recommendation to gate
        flagged = rec.get("flagged")
        eligible, reason = gate_eligible(readiness)
        if flagged and not eligible:
            f.error("xref-gate-flagged-ineligible",
                    f"{label}: topic entry {eid!r} recommendation.flagged is true but the gate is not "
                    f"eligible — {reason}. The gate fires only when all three tiers score with minimum >= 8")
        elif flagged is False and eligible:
            f.error("xref-gate-should-fire",
                    f"{label}: topic entry {eid!r} has all three tiers scored with minimum >= 8 but "
                    f"recommendation.flagged is false — the min>=8 gate is deterministic, not discretionary")


# --------------------------- spread-conflict consistency ---------------------------

def check_spread_conflict(f: Findings, label: str, doc: dict) -> None:
    for entry in doc.get("topic_entries") or []:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id", "<no-id>")
        scored = _scored_tiers(entry.get("readiness"))
        if len(scored) < 2:
            continue  # a spread needs at least two scored tiers
        scores = [t["score"] for t in scored.values()]
        computed_spread = max(scores) - min(scores)
        flags = entry.get("conflict_flags") or []
        spread_flags = [c for c in flags if isinstance(c, dict) and c.get("kind") == "tier-spread"]
        if computed_spread >= SPREAD_THRESHOLD and not spread_flags:
            f.error("xref-spread-unflagged",
                    f"{label}: topic entry {eid!r} scored-tier spread is {computed_spread} "
                    f"(>= {SPREAD_THRESHOLD}) but no tier-spread conflict flag is present — a wide "
                    f"inter-tier spread must be surfaced as signal even below the min-8 gate")
        for c in spread_flags:
            declared = c.get("spread")
            if isinstance(declared, (int, float)) and declared != computed_spread:
                f.warn("xref-spread-mismatch",
                       f"{label}: topic entry {eid!r} tier-spread flag declares spread={declared} but the "
                       f"scored max-min is {computed_spread}")


# --------------------------- topic-entry id uniqueness ---------------------------

def check_topic_id_uniqueness(f: Findings, label: str, doc: dict) -> None:
    seen: dict[str, int] = {}
    for entry in doc.get("topic_entries") or []:
        if isinstance(entry, dict) and "id" in entry:
            seen[entry["id"]] = seen.get(entry["id"], 0) + 1
    for tid, n in seen.items():
        if n > 1:
            f.error("xref-duplicate-topic-id", f"{label}: topic entry id {tid!r} appears {n} times")


# --------------------------- possibles-register delegation ---------------------------

def note_possibles_register(f: Findings, label: str, doc: dict) -> None:
    """C3 ownership line: confirm the embed is present-and-parseable, then
    DELEGATE its entry-shape/id-uniqueness/transition validation to the
    dashboard validator (schema `$ref` already validates the entry shapes)."""
    reg = doc.get("possibles_register")
    if reg is None:
        return
    if not isinstance(reg, list):
        f.error("xref-register-not-a-list",
                f"{label}: possibles_register is present but is not a list/array")
        return
    f.note(f"{label}: embedded possibles_register present ({len(reg)} entry/entries) — entry "
           f"id-uniqueness and cross-snapshot transitions delegated to "
           f"validate-ideation-dashboard-contracts.py (C3 ownership line)")


# --------------------- layer 1: packaged reference examples ---------------------

def check_examples(f: Findings, registry: Registry, docs: dict[str, dict], capability_set: set[str]) -> None:
    """GATES self-test: every valid example validates clean, and each negative
    fails for its INTENDED reason (NEGATIVE_EXPECTED), including
    archive-pointer-only-fit failing at THIS validator's fit-resolution layer."""
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return

    valid_count = 0
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        sub = Findings()
        validate_instance(sub, path.name, load_yaml(path), registry, docs, capability_set)
        if sub.errors:
            for e in sub.errors:
                f.error("example-invalid", f"{path.name}: expected valid: {e}")
        f.warnings.extend(sub.warnings)
        valid_count += 1

    invalid_count = check_negative_examples(f, registry, docs, capability_set)
    f.note(f"examples: {valid_count} valid example(s) confirmed valid, "
           f"{invalid_count} negative example(s) confirmed invalid for their intended reason")


def check_negative_examples(
    f: Findings, registry: Registry, docs: dict[str, dict], capability_set: set[str],
) -> int:
    neg_dir = EXAMPLES_DIR / "negative"
    if not neg_dir.is_dir():
        f.error("examples-missing", f"{neg_dir} not found")
        return 0
    checked = 0
    for path in sorted(neg_dir.glob("*.yaml")):
        sub = Findings()
        validate_instance(sub, f"negative/{path.name}", load_yaml(path), registry, docs, capability_set)
        if not sub.errors:
            f.error("example-should-fail",
                    f"negative/{path.name}: expected invalid, produced no error")
            continue
        expected = NEGATIVE_EXPECTED.get(path.stem)
        if expected and not any(f"[{expected}" in e for e in sub.errors):
            f.error("example-wrong-reason",
                    f"negative/{path.name}: expected a [{expected}...] error but got: {sub.errors}")
            continue
        checked += 1
    return checked


# --------------------- layer 2: real repository instance ---------------------

def check_repo_tree(
    f: Findings, registry: Registry, docs: dict[str, dict], repo: Path, capability_set: set[str],
) -> None:
    """Validate any real ideation-cross-reference index committed under the repo
    (the bootstrap `ideation/cross-reference.yaml`), excluding the reference
    examples tree and the schema files."""
    checked = 0
    for path in sorted(list(repo.rglob("*.yaml")) + list(repo.rglob("*.yml"))):
        rel = path.relative_to(repo).as_posix()
        if rel.startswith("examples/") or rel.startswith("contracts/schemas/") or "/__pycache__/" in rel:
            continue
        try:
            doc = load_yaml(path)
        except yaml.YAMLError:
            continue
        if detect(doc) is None:
            continue
        validate_instance(f, rel, doc, registry, docs, capability_set)
        checked += 1
    f.note(f"repo tree ({repo}): {checked} real ideation-cross-reference index/indices checked "
           f"(one — ideation/cross-reference.yaml — is expected post-bootstrap)")


# --------------------------- orchestration ---------------------------

def run_default(repo: Path, strict: bool) -> int:
    f = Findings()
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2
    registry, docs = build_registry()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")
    capability_set = resolve_capability_set(repo)
    f.note(f"capability set: {len(capability_set)} promoted/active-change capability name(s) "
           f"resolvable for extension-fit citations")
    check_examples(f, registry, docs, capability_set)
    check_repo_tree(f, registry, docs, repo, capability_set)
    return report(f, strict)


def run_path(path: Path, repo: Path, strict: bool) -> int:
    f = Findings()
    registry, docs = build_registry()
    capability_set = resolve_capability_set(repo)
    if path.is_dir():
        checked = 0
        for fp in sorted(list(path.rglob("*.yaml")) + list(path.rglob("*.yml"))):
            try:
                doc = load_yaml(fp)
            except yaml.YAMLError as exc:
                f.error("yaml", f"{fp}: {exc}")
                continue
            if detect(doc) is None:
                continue
            validate_instance(f, str(fp), doc, registry, docs, capability_set)
            checked += 1
        f.note(f"directory sweep {path}: {checked} index/indices checked")
    elif path.is_file():
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            return 2
        validate_instance(f, str(path), doc, registry, docs, capability_set)
    else:
        print(f"ERROR path not found: {path}", file=sys.stderr)
        return 2
    return report(f, strict)


def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    n_e, n_w = len(f.errors), len(f.warnings)
    print(f"\nvalidate-ideation-cross-reference: {n_e} error(s), {n_w} warning(s)")
    if n_e or (strict and n_w):
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="file (kind auto-detected) or directory to validate; "
                         "omit to self-test packaged examples and scan this checkout")
    ap.add_argument("--repo", type=Path, default=ROOT,
                    help="repo root for capability resolution / default scan (default: this checkout)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    try:
        if args.path is not None:
            return run_path(Path(args.path).resolve(), Path(args.repo).resolve(), args.strict)
        return run_default(Path(args.repo).resolve(), args.strict)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
