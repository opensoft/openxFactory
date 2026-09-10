#!/usr/bin/env python3
"""FLOOR PART 3's runner: put ONE destination's corpus reader through the
neutral conformance corpus (`split-opendox-two-layer-product` § 3.7, design
§ D6 part 3, RULED OQ-1).

WHAT THE FLOOR ASKS FOR, AND WHICH HALF WAS MISSING. Design § D6 (3) is "A
NEUTRAL CONFORMANCE CORPUS EVERY DESTINATION PASSES ... a corpus with no
`openspec/`, no `contracts/`, no lifecycle headers", and the ruling's own word
is EVERY: "openXdox's adapter implementation and `openxFactory`'s own adapter
run it too, which is the only mechanical proof that `corpus-adapter-seam`'s
no-privileged-route requirement holds for the home corpus". Two halves. The
CORPUS half landed with § 2.2a under RULING OQ-3 ("SEED HERE") and is
`tests/corpus-adapter/fixtures/` — three documents in two roots of their own, a
two-field header vocabulary belonging to no governed repository, an empty
sibling and a non-directory. The half that did not exist is a way to put a
reader THIS REPOSITORY DID NOT AUTHOR through it: the seed runs under `pytest`
against a factory named in the file, which is exactly one reader, in one
checkout, chosen at author time. This file is the other half.

WHY IT LIVES HERE AND IS NEVER COPIED INTO SIX REPOSITORIES, which is
`verify-carve-arrival.py`'s rule and holds for the same reason: the floor is
one obligation of one change, and a runner copied six ways is six things to
keep in step with one definition of passing. The CHECKS themselves are neutral
and portable — `scripts/carve_conformance.py`, stdlib plus the interface, held
to the interface's own no-home-vocabulary bar — so a destination that would
rather run them inside its own suite imports that module and never this one.

THE READER IS NAMED BY THE OPERATOR, NOT DISCOVERED. `--adapter
<module>:<factory>`, on `--allow-created`'s and `--replica-at`'s reasoning:
an operator declares the thing, and the declaration is then written down in
the pull request that reports the run. The alternative — a convention this
file would go looking for, `src/<something>/adapter.py` and a name — would be
this repository deciding how another repository lays its reader out, which is
the privileged route the seam's fourth requirement forbids, wearing a helpful
face. It also could not be satisfied by a destination that has not been
written yet, whereas a flag can be pointed at whatever a destination ends up
calling its reader.

WHAT A FACTORY IS. A callable `(name, location) -> reader`. Four locations get
pointed at, because three of the corpus's negative confirmations are about
what happens at RESOLUTION time and a single constructed object could not
carry them. `openxFactory`'s own is `tests/carve_conformance/home_factory.py`,
which is a nine-line file and is the worked example a destination copies.

THE DESTINATIONS ARE THE MANIFEST'S, PLUS ONE THE MANIFEST HAS NO KEY FOR.
`--destination` takes a key of `docs/opendox-carve-manifest.yaml`'s
`destinations:` map, so a typo refuses rather than passing for "not carved
yet", and additionally `openxfactory` — § 3.7's third named destination, which
the manifest gives no key because it RECEIVES no row and RETAINS its own
reader instead. That is the same escape `verify-carve-arrival.py` cuts for an
assembly root, for the same reason: the document is a map of where rows GO.

Exit codes, and there are two:
  0  the reader passed every check, or no destination was named
  2  ANY refusal, a failed check included, and any environment failure

  There is deliberately NO exit 1, on `verify-carve-arrival.py`'s reasoning
  and enforced the same way: `main()` catches every `Exception` its own checks
  did not name and renders it as `conformance-unreadable`, so the contract
  does not rest on a reader auditing every raise site. `KeyboardInterrupt` and
  `SystemExit` are the operator's acts and are left alone.

THE SEAT-HOLDING PASS. Given NO `--destination` this prints `NO DESTINATION`
and exits 0 — `verify-carve-arrival.py`'s branch, adopted for its reason: this
file lands BEFORE the readers it runs, so § 3.7's seat in
`tests/carve_conformance/` must be able to assert that the documented
invocation answers without asserting that any destination has authored a
reader. It keys off `--destination` being ABSENT and never off a lookup
failing.

Run:
    python3 scripts/verify-carve-conformance.py \\
        --destination openxfactory \\
        --dest-root   . \\
        --adapter     home_factory:neutral_reader \\
        --sys-path    tests/carve_conformance
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - the repository ships PyYAML
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

# `scripts/` goes on the path because `carve_conformance` and `corpus_adapter`
# both live there and this file is a hyphenated entry point its own tests load
# by `spec_from_file_location`, where Python inserts nothing. GUARDED and
# therefore idempotent, on `scripts/proposal-support.py`'s idiom and for its
# stated reason: a test module that loads this file more than once would
# otherwise prepend a duplicate entry per load.
_SCRIPTS_DIR = str(ROOT / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import carve_conformance  # noqa: E402

MANIFEST_RELPATH = "docs/opendox-carve-manifest.yaml"

#: § 3.7's third destination. The manifest has no key for it — it receives no
#: row — and the ruling names it anyway, because openxFactory's own reader
#: passing the same corpus is "the only mechanical proof that the home corpus
#: has no privileged route".
HOME_DESTINATION = "openxfactory"

#: Where the seed corpus lives, relative to this repository. RULED OQ-3 put it
#: beside the suite that seeded it and eleven manifest rows now name those
#: exact paths as `replicated_at_destination`, so it is not relocated here: a
#: second copy at a second path would be the floor forked in two.
CORPUS_RELPATH = "tests/corpus-adapter/fixtures"

#: The corpus's four states, by the names the seed laid them down under.
POPULATED = "neutral"
EMPTY = "empty"
UNREADABLE = "not-a-directory"

#: A name under the corpus directory that is never created. Resolution against
#: it must refuse rather than list nothing.
ABSENT = "no-corpus-was-ever-placed-here"

#: Import roots added under `--dest-root`, and they are the only thing this
#: file assumes about a destination. They are LAYOUT and not vocabulary: every
#: one is a Python source-root convention, none names a package, a module or a
#: repository, and `--sys-path` adds more where a destination differs.
IMPORT_ROOTS = ("", "src", "scripts")

REFUSAL_CODES: tuple[str, ...] = (
    "conformance-adapter-undeclared",
    "conformance-adapter-unresolvable",
    "conformance-corpus-missing",
    "conformance-check-failed",
    "conformance-unreadable",
)

REMEDIATION = (
    "Remediation: fix the READER, never the corpus — a corpus edited to match "
    "a reader that answered wrong is FLOOR PART 3 deleted, and the ruling's "
    "word is that every destination passes THE SAME corpus. A failing check "
    "names what it asked and what came back; the seam's own rules are in "
    "`openspec/changes/split-opendox-two-layer-product/specs/"
    "corpus-adapter-seam/spec.md`. Where a destination has authored no reader "
    "at all, that is the destination's build task and not a finding against "
    "the corpus."
)


class ConformanceRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so
    a caller can branch on the code without parsing prose. `render()` is the
    ONE place the human message is assembled, and `main()` prints exactly
    that, so the remediation trailer cannot be dropped by a caller that forgot
    it exists.
    """

    def __init__(self, code: str, detail: str) -> None:
        # THE VOCABULARY IS ENFORCED HERE AND NOT ONLY DECLARED ABOVE.
        # `verify-carve-arrival.py` and `validate-carve-manifest.py` both
        # declare their code tuple and let a test pin it, which catches a
        # rename of the CONSTANT and not a raise site that invented a code
        # the tuple never carried. An operator's runbook and a caller's
        # branch both read these strings, so the cheaper guarantee is taken
        # here: a code outside the ratified set cannot be raised at all. The
        # exit contract is unaffected — this `ValueError` is raised inside
        # `main()`'s try and arrives as `conformance-unreadable`, exit 2.
        if code not in REFUSAL_CODES:
            raise ValueError(
                f"{code!r} is not one of this runner's ratified refusal "
                f"codes ({', '.join(REFUSAL_CODES)}); a caller branching on "
                "the vocabulary would never see it")
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def render(self, where: str) -> str:
        return f"FAIL {where}: {self.code} — {self.detail}\n{REMEDIATION}"


def read_destinations(manifest_path: Path) -> list[str]:
    """The manifest's destination keys, plus the home one.

    An unreadable manifest is not fatal HERE: the keys are used to refuse a
    typo, and a run naming `openxfactory` — the one key the manifest does not
    carry — must not be held hostage to a document it does not consult.
    """
    try:
        with manifest_path.open("r", encoding="utf-8") as handle:
            doc = yaml.safe_load(handle)
        keys = sorted(doc["destinations"])
    except Exception:  # noqa: BLE001 - see the docstring
        keys = []
    return keys + [HOME_DESTINATION]


def resolve_factory(spec: str, dest_root: Path,
                    extra_paths: list[str]) -> Any:
    """Import `<module>:<factory>` with the destination's roots on the path.

    THE PATH IS RESTORED AFTERWARDS. This process may run several
    destinations in a session — the tests do — and a root left on `sys.path`
    would let the SECOND destination import the FIRST one's modules and pass
    on them. That is the privileged route again, arriving by accident, so the
    insertion is undone in a `finally` and the imported module is held by
    reference rather than by name.
    """
    if ":" not in spec:
        raise ConformanceRefusal(
            "conformance-adapter-unresolvable",
            f"--adapter {spec!r} is not <module>:<factory>. The colon is "
            "required: a bare module name would leave this file guessing "
            "which of its callables is the factory")
    module_name, _, attr = spec.partition(":")
    if not module_name or not attr:
        raise ConformanceRefusal(
            "conformance-adapter-unresolvable",
            f"--adapter {spec!r} names an empty module or an empty factory")

    roots = [str((dest_root / part).resolve()) if part else str(dest_root)
             for part in IMPORT_ROOTS]
    roots += [str((dest_root / p).resolve()) if not Path(p).is_absolute()
              else str(Path(p).resolve()) for p in extra_paths]
    added = [r for r in roots if r not in sys.path and Path(r).is_dir()]
    for root in reversed(added):
        sys.path.insert(0, root)
    try:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            raise ConformanceRefusal(
                "conformance-adapter-unresolvable",
                f"importing {module_name!r} raised {type(exc).__name__}: "
                f"{exc}. Roots searched under --dest-root: "
                f"{', '.join(added) or '(none of them exist)'}") from exc
        factory = getattr(module, attr, None)
        if factory is None:
            raise ConformanceRefusal(
                "conformance-adapter-unresolvable",
                f"{module_name!r} carries no {attr!r}. It declares: "
                f"{', '.join(n for n in sorted(dir(module)) if not n.startswith('_')) or '(nothing public)'}")
        if not callable(factory):
            raise ConformanceRefusal(
                "conformance-adapter-unresolvable",
                f"{module_name}:{attr} is {type(factory).__name__} and a "
                "factory has to be callable — it is handed a name and a "
                "location and returns a reader pointed at it")
        return factory
    finally:
        for root in added:
            try:
                sys.path.remove(root)
            except ValueError:  # pragma: no cover - defensive
                pass


def corpus_locations(corpus_root: Path) -> dict[str, str]:
    """The four states, checked for presence before a reader is blamed."""
    if not corpus_root.is_dir():
        raise ConformanceRefusal(
            "conformance-corpus-missing",
            f"the neutral corpus is not at {corpus_root}. It is "
            f"{CORPUS_RELPATH} in openxFactory (RULED OQ-3's seed); point "
            "--corpus at a checkout that carries it")
    populated = corpus_root / POPULATED
    empty = corpus_root / EMPTY
    unreadable = corpus_root / UNREADABLE
    for label, path, want_dir in ((POPULATED, populated, True),
                                  (EMPTY, empty, True),
                                  (UNREADABLE, unreadable, False)):
        if want_dir and not path.is_dir():
            raise ConformanceRefusal(
                "conformance-corpus-missing",
                f"the corpus at {corpus_root} carries no {label!r} directory. "
                "A run over a partial corpus would report a reader as passing "
                "checks that were never put to it")
        if not want_dir and not path.is_file():
            raise ConformanceRefusal(
                "conformance-corpus-missing",
                f"the corpus at {corpus_root} carries no {label!r} file, so "
                "the unreadable-corpus confirmation has nothing to point at")
    absent = corpus_root / ABSENT
    if absent.exists():  # pragma: no cover - the name exists to never exist
        raise ConformanceRefusal(
            "conformance-corpus-missing",
            f"{absent} EXISTS, and it is the path the absent-corpus "
            "confirmation points at. Remove it: a reader would be asked to "
            "refuse a corpus that is there")
    return {"populated": str(populated), "empty": str(empty),
            "unreadable": str(unreadable), "absent": str(absent)}


def run_corpus(factory: Any, locations: dict[str, str], destination: str,
               dest_root: Path, corpus_root: Path,
               adapter: str) -> dict[str, Any]:
    outcomes = carve_conformance.run(factory, **locations)
    passed, total, failed = carve_conformance.verdict(outcomes)
    summary: dict[str, Any] = {
        "result": "ok" if not failed else "refused",
        "destination": destination,
        "dest_root": str(dest_root),
        "corpus": str(corpus_root),
        "adapter": adapter,
        "checks_declared": len(carve_conformance.CHECKS),
        "checks_run": total,
        "passed": passed,
        "failed": list(failed),
        "outcomes": [{"check": o.check, "passed": o.passed,
                      "detail": o.detail} for o in outcomes],
    }
    if failed:
        lines = "\n".join(
            f"  - {o.check}: {o.detail}" for o in outcomes if not o.passed)
        raise ConformanceRefusal(
            "conformance-check-failed",
            f"{destination} passed {passed} of {total} check(s) in the "
            f"neutral conformance corpus; {len(failed)} did not:\n{lines}")
    return summary


def _refused(exc: ConformanceRefusal, args: argparse.Namespace,
             where: str) -> int:
    """The ONE refusal exit: `--json` object or the rendered human message."""
    if args.json:
        print(json.dumps({"result": "refused", "code": exc.code,
                          "detail": exc.detail,
                          "destination": args.destination,
                          "dest_root": args.dest_root,
                          "adapter": args.adapter}))
    else:
        print(exc.render(where), file=sys.stderr)
    return 2


def _print_ok(summary: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary))
        return
    print(f"OK {summary['dest_root']}: {summary['destination']} passed the "
          f"neutral conformance corpus — {summary['passed']} of "
          f"{summary['checks_run']} check(s), reader "
          f"{summary['adapter']}, corpus {summary['corpus']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify-carve-conformance.py",
        description=("Run the neutral conformance corpus against ONE "
                     "destination's corpus reader — FLOOR PART 3 of "
                     "split-opendox § D6 (RULED OQ-1)."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--manifest", metavar="PATH", default=None,
        help=f"the manifest whose destination keys are accepted (default: "
             f"{MANIFEST_RELPATH})")
    parser.add_argument(
        "--destination", metavar="KEY", default=None,
        help=("a key of the manifest's `destinations:` map, e.g. "
              f"opendox_code, or {HOME_DESTINATION} — § 3.7's third "
              "destination, which the manifest gives no key because it "
              "receives no row"))
    parser.add_argument(
        "--dest-root", metavar="DIR", default=None,
        help="the destination checkout whose reader is under test")
    parser.add_argument(
        "--adapter", metavar="MODULE:FACTORY", default=None,
        help=("the destination's OWN corpus reader, declared by the operator: "
              "a callable of (name, location) returning a reader. Nothing is "
              "discovered — see the module docstring"))
    parser.add_argument(
        "--sys-path", metavar="DIR", action="append", default=[],
        help=("an extra import root, relative to --dest-root or absolute; "
              f"repeatable. {', '.join(repr(r or '.') for r in IMPORT_ROOTS)} "
              "under --dest-root are added already"))
    parser.add_argument(
        "--corpus", metavar="DIR", default=None,
        help=f"the neutral corpus (default: <this repository>/{CORPUS_RELPATH})")
    parser.add_argument(
        "--json", action="store_true",
        help="print one JSON object on stdout instead of the human line")
    args = parser.parse_args(argv)

    manifest_path = (Path(args.manifest).resolve() if args.manifest
                     else (ROOT / MANIFEST_RELPATH).resolve())

    # THE SEAT-HOLDING PASS, and the one place here that is not fail-closed.
    if args.destination is None:
        known = read_destinations(manifest_path)
        if args.json:
            print(json.dumps({"result": "no-destination",
                              "manifest": str(manifest_path),
                              "destinations": known,
                              "checks": list(carve_conformance.CHECKS)}))
        else:
            print(f"NO DESTINATION (nothing to run; name one of: "
                  f"{', '.join(known)})")
        return 0

    where = args.dest_root or args.destination
    try:
        known = read_destinations(manifest_path)
        if args.destination not in known:
            raise ConformanceRefusal(
                "conformance-unreadable",
                f"--destination {args.destination!r} is neither a key of the "
                f"manifest's `destinations:` map nor {HOME_DESTINATION!r} "
                f"({', '.join(known)}). The seat-holding pass covers a run "
                "with NO destination, before the readers exist; it does not "
                "extend to one the caller named, because a typo must not be "
                "indistinguishable from `not yet authored`")
        if args.dest_root is None:
            raise ConformanceRefusal(
                "conformance-unreadable",
                "--dest-root is required with --destination: this runner "
                "imports a reader out of a destination checkout and has no "
                "default for one")
        dest_root = Path(args.dest_root).resolve()
        if not dest_root.is_dir():
            raise ConformanceRefusal(
                "conformance-unreadable",
                f"--dest-root {args.dest_root!r} resolves to {dest_root}, "
                "which is not a directory")
        where = str(dest_root)
        corpus_root = (Path(args.corpus).resolve() if args.corpus
                       else (ROOT / CORPUS_RELPATH).resolve())
        locations = corpus_locations(corpus_root)
        if args.adapter is None:
            raise ConformanceRefusal(
                "conformance-adapter-undeclared",
                f"--adapter is required and {args.destination} declared none. "
                "FLOOR PART 3 is a claim about a READER — 'every destination "
                "passes it' — so a run with no reader named has nothing to "
                "put through the corpus and must not be recorded as a pass. "
                "Where the destination has authored no reader yet, THAT is "
                "the finding, and it belongs to that destination's build "
                "task rather than to this corpus")
        factory = resolve_factory(args.adapter, dest_root, args.sys_path)
        summary = run_corpus(factory, locations, args.destination, dest_root,
                             corpus_root, args.adapter)
    except ConformanceRefusal as exc:
        return _refused(exc, args, where)
    # THE EXIT CONTRACT, HELD BY CODE AND NOT BY INSPECTION. Everything above
    # refuses in this file's own vocabulary; anything that does not — a reader
    # whose constructor raises, an `OSError` the checks did not name, a bug
    # here — would otherwise leave `main()` as a traceback and EXIT 1, which
    # the module docstring says does not exist. It is `Exception` and not
    # `BaseException`: a `KeyboardInterrupt` or a `SystemExit` is the
    # operator's act and must not be re-labelled a finding.
    except Exception as exc:  # noqa: BLE001
        return _refused(
            ConformanceRefusal(
                "conformance-unreadable",
                f"{type(exc).__name__}: {exc}"),
            args, where)
    _print_ok(summary, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
