#!/usr/bin/env python3
"""The canonical validator for the `council-convening` contract family.

    python3 scripts/validate-council-convening.py [--strict]
    python3 scripts/validate-council-convening.py check [--strict] PATH...
    python3 scripts/validate-council-convening.py corpus [--json]

T021, per specs/035-renew-resolved-council-protocol/contracts/validator-cli.md.
A THIN CLI over the reference implementation in `scripts/council_convening/`,
on the house pattern of `scripts/validate-contract-release.py` over
`scripts/hermes_runtime_validation/`. It derives nothing of its own: the digest
construction is `scripts/signed_execution_chain/canonical.py`, and every rule is
the package's.

THE MODES.

* No subcommand: THE SELF-TEST. It loads every family schema and the digest
  construction, checks that the protocol registry is closed, checks the corpus
  index's closure and raw-byte digests, adjudicates every vector, checks coverage
  of every refusal code, finding code and `coverage_floor` requirement at this
  commit, and regenerates the corpus byte for byte. It prints the proof-of-work
  notes the CI gate asserts.
* `check PATH...`: dispatches each record by `kind`. A protocol-carrying record,
  or one with no family kind, is CLASSIFIED FIRST, offline (no selected
  protocol). A commission record (Phase 2) is then judged on data-model E2's
  offline rules, in its order, and every rule that needs an environment oracle
  is named in a `not checkable offline` note. A legacy record is ROUTED to the legacy verifier and given no
  verdict. A registry, binding, selection or activation record is judged by its
  kind and never classified. A replacement record of a kind whose schema has not
  landed at this commit is an ERROR. The family's three NON-RECORD kinds are
  judged, never waved through: a family schema must carry the full house header
  (`schema_version` 1, a `name`, the 2020-12 `$schema`, an `$id` under the
  family base) and no protocol shape; a vector is ADJUDICATED against its own
  expectation; an index's format is checked, its closure against a tree being
  the self-test's. A `kind` that is not a string is malformed. Nothing is
  classified against a registry that is not closed. Every PATH must resolve,
  after `..` and symbolic links, inside the directory `check` is invoked
  from; any other is refused as a harness failure (exit 2) and never read.
  Exit 0 covers the offline-checkable rules only, and is never evidence of
  admission. A PRODUCER BINDING (Phase 5) is judged by data-model E10 steps 1
  to 6, against the identity map `contracts/policies/repository-identity.yaml`
  of the tree the validator runs in, which at a consumer's pin is that pin's
  map (Brett Heap's OPEN-2 ruling, "Consumer's runtime config
  (Recommended)"); the `.template.yaml` stub is refused as live; and steps 7
  to 14, which need the verified claims, are each reported as not checkable
  offline.
* `corpus [--json]`: the index summary: totals, the agreement-set count and the
  index's raw SHA-256. `--json` prints it for successor tooling.

`select` and `check --historical` land in Phase 6; until then they are argparse's
exit 2.

EXIT CODES. 0 is no ERROR and no routed record (WARNs allowed unless `--strict`).
1 is findings. 2 is a harness or dependency failure, never reported as a finding.
3 is `check` only: at least one record ROUTED and nothing an ERROR. A route is
never a pass. Exit 3 follows `scripts/validate-consent-instruments.py`'s
`EXIT_NEEDS_DECISION = 3`; here it means another verifier must give the verdict.

OUTPUT. `ERROR [code] message`, `WARN  [code] message`, or `note  message`, one
per line. Messages name members and paths, never a record's values.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

_ENTRYPOINT_REPO = Path(__file__).resolve().parents[1]
# Run as `python3 scripts/validate-council-convening.py`, Python puts only the
# scripts directory on sys.path; the package is imported as
# `scripts.council_convening`, never under its bare name.
if str(_ENTRYPOINT_REPO) not in sys.path:
    sys.path.insert(0, str(_ENTRYPOINT_REPO))

from scripts.council_convening import (  # noqa: E402
    binding,
    classification,
    corpus,
    generate,
    predicates,
    records,
    resolution,
)

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_HARNESS = 2
EXIT_ROUTED = 3

ROUTED_CODE = "council-convening-legacy-protocol-routed"

#: Record kinds whose schema has landed at this commit, mapped to it. Phase 1
#: lands none of the protocol-carrying or judged-by-kind record schemas other
#: than the registry's; each later phase adds its own. Phase 2 lands the
#: commission record (data-model E2) and the predicate registry (E3), which
#: `check` judges by kind.
LANDED_RECORD_SCHEMAS: dict[str, str] = {
    resolution.KIND: "council-convening.schema.yaml",
}

NOT_OFFLINE_CODE = "council-convening-not-offline-checkable"


def _say(line: str) -> None:
    print(line, flush=True)


def _harness(message: str) -> int:
    print(f"validate-council-convening: harness failure: {message}", file=sys.stderr)
    return EXIT_HARNESS


def _refusal_code(code: str) -> str:
    return "council-convening-" + code.replace("_", "-")


# --------------------------------------------------------------------------
# The self-test.
# --------------------------------------------------------------------------

def self_test(root: Path, strict: bool) -> int:
    try:
        schemas = records.load_schemas(root)
        registry_doc = classification.load_registry_doc(root)
    except records.SchemaLoadError as exc:
        return _harness(str(exc))
    errors: list[corpus.Finding] = []
    _say(f"note  schemas loaded: {len(schemas.family)} (family) + digest-construction")

    registry_problems = classification.registry_findings(schemas, registry_doc)
    if registry_problems:
        for code, message in registry_problems:
            _say(corpus.Finding("ERROR", code, message).line())
        _say("note  the corpus was not adjudicated: the protocol registry is not closed, "
             "and nothing is classified against it")
        return EXIT_FINDINGS
    _say(f"note  protocol registry closed: {len(registry_doc['protocols'])} entries")
    try:
        predicate_doc = predicates.load_registry_doc(root)
    except records.SchemaLoadError as exc:
        return _harness(str(exc))
    predicate_problems = predicates.registry_findings(schemas, predicate_doc)
    errors.extend(corpus.Finding("ERROR", code, message)
                  for code, message in predicate_problems)
    if not predicate_problems:
        _say(f"note  {predicates.REGISTRY_NOTE}")
    try:
        registry = classification.Registry(registry_doc)
    except ValueError as exc:
        _say(f"note  the corpus was not adjudicated: {exc}")
        return EXIT_FINDINGS

    try:
        report = corpus.check_corpus(root, schemas, registry)
    except records.SchemaLoadError as exc:
        return _harness(str(exc))
    errors.extend(report.findings)
    digest = report.index_sha256 or "sha256:unavailable"
    _say(f"note  corpus index: {report.vectors} vectors, {report.both_sides} both-sides, "
         f"{digest}")
    _say("note  vectors adjudicated: %d/%d" % report.adjudicated)
    _say("note  refusal codes probed: %d/%d" % report.refusals_probed)
    _say("note  finding codes probed: %d/%d" % report.findings_probed)
    _say("note  requirements probed: %d/%d (%s)" % (*report.requirements_probed,
                                                    ", ".join(report.coverage_floor)))

    # The findings collected so far are printed BEFORE the generator runs, so
    # whatever the generator does, they are on the record.
    for finding in errors:
        _say(finding.line())
    try:
        drift = generate.check(root)
    except records.SchemaLoadError as exc:
        return _harness(str(exc))
    drift_findings = [corpus.Finding("ERROR", "council-convening-generator-drift", line)
                      for line in drift]
    for finding in drift_findings:
        _say(finding.line())
    errors.extend(drift_findings)
    if not drift:
        _say("note  generator reproduced corpus byte-for-byte")

    failing = [f for f in errors if f.severity == "ERROR" or strict]
    warnings = sum(1 for f in errors if f.severity != "ERROR")
    _say(f"note  self-test: {sum(1 for f in errors if f.severity == 'ERROR')} error(s), "
         f"{warnings} warning(s)")
    return EXIT_FINDINGS if failing else EXIT_OK


# --------------------------------------------------------------------------
# `check`.
# --------------------------------------------------------------------------

class _Unreadable(Exception):
    pass


def _within_invocation_directory(given: str) -> str:
    """`given`, canonicalized, once it is shown to lie inside the directory
    `check` was invoked from; `_Unreadable` otherwise.

    A validator an agent may drive reads only where it was started (Sonar
    `pythonsecurity:S8707`, after that rule's own compliant form): the path is
    canonicalized with `os.path.realpath`, which resolves `..` and symbolic
    links, and only then compared with the canonical working directory plus a
    separator, so `/base/dir-other` never passes for `/base/dir`. A successor
    checks its own records by running `check` from its own checkout.
    """
    resolved = os.path.realpath(given)
    base_dir = os.path.realpath(os.getcwd())
    if resolved != base_dir and not resolved.startswith(base_dir + os.sep):
        raise _Unreadable(f"{given}: outside the directory check was invoked from "
                          f"({base_dir}); run check from a directory that holds it")
    return resolved


def _read(path: Path) -> tuple[Any, str | None, str]:
    """`(document, None, text)`, or `(None, problem, text)` for a file that does
    not parse. An unreadable file raises `_Unreadable`, the harness failure.
    YAML is read STRICTLY: a repeated key is refused, never resolved."""
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise _Unreadable(f"{path}: unreadable ({type(exc).__name__})") from exc
    if path.suffix in (".yaml", ".yml"):
        try:
            return records.strict_yaml(raw, path.name), None, text
        except ValueError:
            return None, "does not parse as strict YAML (a repeated key, an alias, a merge key, a non-string key or an implicit timestamp)", text
    try:
        return corpus.loads_strict(text), None, text
    except ValueError:
        return None, "does not parse as strict JSON", text


_SCHEMA_ID = re.compile(re.escape(records.ID_BASE) + r"[a-z0-9][a-z0-9-]*\.schema\.yaml\Z")


def _family_schema_problems(document: dict, schemas: records.SchemaSet,
                            registry: classification.Registry) -> list[str]:
    """What keeps `document` from being a family schema: the full house header,
    no protocol shape, the 2020-12 metaschema, and only asserted formats."""
    problems = []
    if not (isinstance(document.get("schema_version"), int)
            and not isinstance(document.get("schema_version"), bool)
            and document.get("schema_version") == 1):
        problems.append("schema_version is not 1")
    if not isinstance(document.get("name"), str) or not document.get("name"):
        problems.append("carries no name")
    if document.get("$schema") != records.DIALECT_2020_12:
        problems.append("$schema is not the 2020-12 dialect")
    schema_id = document.get("$id")
    if not isinstance(schema_id, str) or not _SCHEMA_ID.match(schema_id):
        problems.append(f"$id is not a .schema.yaml under {records.ID_BASE}")
    if classification.carries_protocol_shape(document, registry):
        problems.append("carries a protocol member or a legacy recognition shape, "
                        "which no family schema carries")
    for nested in records.headers_below_root(document):
        problems.append(f"carries {nested.rsplit('/', 1)[-1]} below its root, at {nested}; "
                        f"a resource header belongs only at a document's root")
    if isinstance(schema_id, str) and _SCHEMA_ID.match(schema_id):
        family = {**schemas.family, schema_id: document}
        for outside in records.references_outside(family, schemas.digest_construction):
            if outside.startswith(f"{schema_id}: "):
                problems.append(outside.split(": ", 1)[1]
                                + ", outside the loaded documents")
    try:
        records._check_schema("document", document)
    except records.SchemaLoadError:
        problems.append("is not a valid 2020-12 schema")
    unasserted = sorted(set(records.format_targets(document)) - set(records.ASSERTED_FORMATS))
    if unasserted:
        problems.append(f"uses a format this family does not assert: {', '.join(unasserted)}")
    return problems


BINDING_KIND = "xfactory_council_producer_binding"

#: What each E10 refusal says when `check` finds it, naming members only.
_BINDING_MESSAGES = {
    "binding_malformed": "fails producer-binding.schema.yaml (E10 step 1)",
    "binding_wildcard": "carries a wildcard (E10 step 2)",
    "issuer_mismatch": "names an issuer of neither allowed form (E10 step 3)",
    "repository_identity_unavailable": (
        "the identity map is absent, unreadable or malformed (E10 step 4)"),
    "repository_identity_former": (
        "names a former spelling or a non-canonical case variant (E10 step 4)"),
    "subject_workflow_conflation": (
        "its subject template is a bare workflow reference (E10 step 5)"),
    "subject_template_mismatch": (
        "its subject template does not parse, or names another repository "
        "(E10 step 6)"),
}


def _check_binding(path: Path, document: dict, schemas: records.SchemaSet,
                   root: Path) -> list[corpus.Finding]:
    """E10 steps 1 to 6 on a producer binding, offline; steps 7 to 14 are each
    reported as not checkable offline, never passed."""
    try:
        binding.check_offline(document, identity_root=root, schemas=schemas)
    except records.Refused as refused:
        message = _BINDING_MESSAGES.get(refused.code, "is refused")
        if refused.member == "instantiation_stub":
            message = ("is the .template.yaml stub, which is never accepted as a "
                       "live binding (E10 step 1)")
        member = f" at {refused.member}" if refused.member else ""
        return [corpus.Finding("ERROR", _refusal_code(refused.code),
                               f"{path}: producer binding {message}{member}")]
    _say(f"note  {path}: producer binding passes E10 steps 1 to 6 (offline), "
         f"against {binding.IDENTITY_MAP.as_posix()} at this tree")
    for step, code in enumerate(binding.CLAIM_RULES, start=7):
        _say(f"note  not checkable offline: {path}: E10 step {step} {code}")
    return []


def _check_one(path: Path, document: Any, schemas: records.SchemaSet,
               registry: classification.Registry,
               text: str,
               root: Path = records.REPO_ROOT) -> tuple[list[corpus.Finding], bool]:
    """Findings for one record, and whether it was routed."""
    def error(code: str, message: str) -> list[corpus.Finding]:
        return [corpus.Finding("ERROR", code, f"{path}: {message}")]

    if not isinstance(document, dict):
        return error("council-convening-schema", "is not a record object"), False
    if "kind" in document and not isinstance(document["kind"], str):
        return error("council-convening-schema", "kind is not a string"), False
    kind = document.get("kind")
    if kind == BINDING_KIND:
        return _check_binding(path, document, schemas, root), False
    if kind == classification.REGISTRY_KIND:
        problems = classification.registry_findings(schemas, document)
        if problems:
            return [corpus.Finding("ERROR", code, f"{path}: {message}")
                    for code, message in problems], False
        _say(f"note  {path}: protocol registry valid and closed "
             f"({len(document['protocols'])} entries)")
        return [], False
    if kind == predicates.REGISTRY_KIND:
        problems = predicates.registry_findings(schemas, document)
        if problems:
            return [corpus.Finding("ERROR", code, f"{path}: {message}")
                    for code, message in problems], False
        _say(f"note  {path}: {predicates.REGISTRY_NOTE}")
        return [], False
    if kind in classification.JUDGED_BY_KIND_KINDS:
        return error("council-convening-kind-unknown",
                     f"a record of kind {kind}, whose schema has not landed at this "
                     f"commit; judged by kind and never classified"), False
    if kind == records.SCHEMA_KIND:
        problems = _family_schema_problems(document, schemas, registry)
        if problems:
            return [corpus.Finding("ERROR", "council-convening-schema", f"{path}: {p}")
                    for p in problems], False
        _say(f"note  {path}: family schema carries the house header and is a valid "
             f"2020-12 schema")
        return [], False
    if kind in (corpus.VECTOR_KIND, corpus.INDEX_KIND):
        try:
            corpus.loads_strict(text, corpus_tokens=True)
        except corpus.IntegralFloatToken as exc:
            return error("council-convening-schema", str(exc)), False
        except ValueError:
            return error("council-convening-schema", "does not parse as strict JSON"), False
    if kind == corpus.VECTOR_KIND:
        problems = corpus.vector_format_problems(schemas, document)
        if problems:
            return [corpus.Finding("ERROR", "council-convening-schema", f"{path}: {p}")
                    for p in problems], False
        found, matched = corpus.adjudication_findings(
            str(path), document, corpus.Context(schemas, registry))
        if not found and matched:
            _say(f"note  {path}: vector adjudicated to its expected outcome")
        return found, False
    if kind == corpus.INDEX_KIND:
        problems = corpus.index_problems(document, registry)
        if problems:
            return [corpus.Finding("ERROR", "council-convening-index-closure", f"{path}: {p}")
                    for p in problems], False
        _say(f"note  {path}: corpus index format valid; closure against its tree is "
             f"the self-test's")
        return [], False

    outcome = classification.classify_and_select(document, None, registry)
    if outcome.outcome == "route":
        _say(f"note  [{ROUTED_CODE}] {path}: a legacy record, routed to the legacy "
             f"verifier; this family gives it no verdict")
        return [], True
    if outcome.outcome == "refuse":
        return error(_refusal_code(outcome.refusal),
                     "classifies under no registry entry (data-model E1)"), False
    if kind not in LANDED_RECORD_SCHEMAS:
        what = (f"of kind {kind}" if kind in classification.PROTOCOL_CARRYING_KINDS
                else "that names no family record kind")
        return error("council-convening-kind-unknown",
                     f"a replacement record {what}, whose schema has not landed at "
                     f"this commit"), False
    return _check_commission_record(path, document, schemas, registry), False


def _check_commission_record(path: Path, document: Any, schemas: records.SchemaSet,
                             registry: classification.Registry) -> list[corpus.Finding]:
    """The offline E2 rules (T032): data-model E2's order with every rule that
    needs an environment oracle skipped and named, never passed."""
    result = resolution.check_offline(document, schemas, registry)
    for rule in result.not_checkable:
        _say(f"note  [{NOT_OFFLINE_CODE}] {path}: not checkable offline: {rule}")
    if result.refusal is None:
        _say(f"note  {path}: commission record passes every offline-checkable E2 rule")
        return []
    where = f" at {result.member}" if result.member else ""
    found = [corpus.Finding("ERROR", _refusal_code(result.refusal),
                            f"{path}: refused {result.refusal}{where} (data-model E2)")]
    if result.refusal == "convening_malformed":
        found.insert(0, corpus.Finding("ERROR", "council-convening-schema",
                                       f"{path}: fails council-convening.schema.yaml or "
                                       f"its structural rules"))
    return found


def _registry_not_closed(exc: "classification.RegistryNotClosed", what: str) -> int:
    for code, message in exc.findings:
        _say(corpus.Finding("ERROR", code, message).line())
    _say(f"note  {what}: the protocol registry in this checkout is not closed, and "
         f"nothing is classified against it")
    return EXIT_FINDINGS


def check(paths: list[str], root: Path, strict: bool) -> int:
    try:
        schemas = records.load_schemas(root)
        registry = classification.load_closed_registry(root, schemas)
    except classification.RegistryNotClosed as exc:
        return _registry_not_closed(exc, "check: no record was classified")
    except (records.SchemaLoadError, ValueError) as exc:
        return _harness(str(exc))
    findings: list[corpus.Finding] = []
    routed = 0
    for name in paths:
        path = Path(name)  # as given, for messages; the read is the canonical one
        try:
            document, problem, text = _read(Path(_within_invocation_directory(name)))
        except _Unreadable as exc:
            return _harness(str(exc))
        if problem:
            findings.append(corpus.Finding("ERROR", "council-convening-schema",
                                           f"{path}: {problem}"))
            continue
        found, was_routed = _check_one(path, document, schemas, registry, text, root)
        findings.extend(found)
        routed += was_routed
    for finding in findings:
        _say(finding.line())
    failing = [f for f in findings if f.severity == "ERROR" or strict]
    _say(f"note  check: {len(paths)} record(s), {routed} routed, "
         f"{len({f.message.split(':', 1)[0] for f in failing})} with errors; "
         f"offline-checkable rules only, so exit 0 is never evidence of admission "
         f"and a route is never a pass")
    if failing:
        return EXIT_FINDINGS
    return EXIT_ROUTED if routed else EXIT_OK


# --------------------------------------------------------------------------
# `corpus`.
# --------------------------------------------------------------------------

def corpus_summary(root: Path, as_json: bool) -> int:
    try:
        schemas = records.load_schemas(root)
        registry = classification.load_closed_registry(root, schemas)
        report = corpus.check_corpus(root, schemas, registry)
    except classification.RegistryNotClosed as exc:
        return _registry_not_closed(exc, "corpus: the index was not summarized")
    except (records.SchemaLoadError, ValueError) as exc:
        return _harness(str(exc))
    if as_json:
        summary = {
            "corpus_id": report.corpus_id,
            "protocol": report.protocol,
            "index_sha256": report.index_sha256,
            "vectors": report.vectors,
            "agreement_set": report.both_sides,
            "totals": report.totals,
            "coverage_floor": report.coverage_floor,
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
        for finding in report.findings:
            print(finding.line(), file=sys.stderr)
    else:
        _say(f"note  corpus {report.corpus_id}: {report.vectors} vectors, agreement set "
             f"{report.both_sides} (applies to both sides), index {report.index_sha256}")
        by_area = report.totals.get("by_area", {})
        by_outcome = report.totals.get("by_outcome", {})
        _say("note  by area: " + (", ".join(f"{k}={v}" for k, v in sorted(by_area.items()))
                                  or "none"))
        _say("note  by outcome: " + (", ".join(f"{k}={v}"
                                               for k, v in sorted(by_outcome.items()))
                                     or "none"))
        for finding in report.findings:
            _say(finding.line())
    return EXIT_FINDINGS if report.findings else EXIT_OK


# --------------------------------------------------------------------------
# The command line.
# --------------------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate-council-convening.py",
        description="The canonical validator for the council-convening contract family.")
    parser.add_argument("--strict", action="store_true", help="treat a WARN as an ERROR")
    modes = parser.add_subparsers(dest="mode")
    check_mode = modes.add_parser("check", help="check records offline")
    check_mode.add_argument("--strict", action="store_true", dest="check_strict",
                            help="treat a WARN as an ERROR")
    check_mode.add_argument("paths", nargs="+", metavar="PATH")
    corpus_mode = modes.add_parser("corpus", help="print the corpus index summary")
    corpus_mode.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    """The CLI. `root` is for in-process tests over a copy of the family; the
    command line always uses this checkout."""
    args = _parser().parse_args(argv)
    root = Path(root) if root is not None else records.REPO_ROOT
    if args.mode == "check":
        return check(args.paths, root, args.strict or args.check_strict)
    if args.mode == "corpus":
        return corpus_summary(root, args.json)
    return self_test(root, args.strict)


if __name__ == "__main__":
    sys.exit(main())
