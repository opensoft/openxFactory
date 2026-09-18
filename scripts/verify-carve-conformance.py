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

A DESTINATION MAY TRANSPOSE THE CORPUS, AND THIS RUNNER PROVES THE
TRANSPOSITION FAITHFUL (RULED Q-F1 (a), Brett Heap 2026-09-17, `#656` comment
`5714365086`). The corpus is laid down as a PLAIN DIRECTORY TREE, and a
destination whose corpus is git HISTORY rather than a working tree cannot
address it in that form at all — measured: openDox's reader, pointed at the
fixtures as they ship, refuses at resolution and reaches ONE of the seventeen
checks. The ruling's answer is that the DESTINATION transposes the same
documents into the storage form its own reader addresses, bytes unchanged, and
says so; `--corpus <transposition>` is how the transposed corpus is handed in.
Narrowing the corpus to what a reader passes today would be FLOOR PART 3
deleted to tick FLOOR PART 3, so the permission comes with a PROOF rather than
with trust:

  * the REFERENCE side is computed here, from files, with no reader involved:
    `{key: sha256(bytes)}` over every document of `tests/corpus-adapter/
    fixtures/neutral` in the checkout this file runs from;
  * the CANDIDATE side is what the READER UNDER TEST serves out of the
    transposition — `list_documents` at the corpus's declared revision, then
    `read` for each — and it must be that table EXACTLY: the same keys, and
    the same bytes under each key;
  * a difference refuses `conformance-corpus-unfaithful` and NAMES the keys,
    before any of the seventeen checks runs, because a reader measured against
    a corpus nobody compared is not measured at all;
  * the proof is taken again AFTER the seventeen, through the very reader
    `carve_conformance.run` built for the populated corpus, which is what
    the verdict's closing `unmoved across the run` reports: it catches a
    corpus that moved under the measurement and a factory that served the
    shipped bytes to the proof and something else to the checks. A reader
    answering differently on two CALLS to one instance is outside what any
    bracketing can see, and is named here so nobody reads more into a green
    verdict than it measured;
  * and the verdict line and the `--json` payload carry the transposition —
    its path, its document count, the revision it was proven at and the
    table's digest — so the evidence a pull request records says
    "transposed, faithful" rather than "passed", and a reader of that
    evidence can recompute the digest.

The proof is taken ONLY when `--corpus` resolves somewhere other than this
repository's own fixtures: the default run is the shipped corpus compared with
itself, so it is left exactly as it was. Where the reader cannot RESOLVE or
LIST the location at all there is nothing to compare, and the seventeen checks
are the better instrument — they report `resolve-populated` or
`list-population` failing and the rest as not reached. That path cannot be
recorded as a pass either: a run whose seventeen all passed over a
transposition that was never proven faithful refuses
`conformance-corpus-unfaithful` at the end rather than printing OK.

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

and, for a destination that has TRANSPOSED the corpus (RULED Q-F1 (a)), the
same command with the transposition named — the run then prints TRANSPOSED
and FAITHFUL, its document count, the revision it was proven at and the
key/sha256 table's digest, or refuses `conformance-corpus-unfaithful` naming
the keys:

    python3 scripts/verify-carve-conformance.py \\
        --destination <key> \\
        --dest-root   <the destination checkout> \\
        --adapter     <module>:<factory> \\
        --corpus      <the transposition>
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

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
from corpus_adapter import CorpusRef  # noqa: E402

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
    "conformance-corpus-unfaithful",
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
    "the corpus. And where a TRANSPOSITION does not carry the corpus's own "
    "documents, what is fixed is the transposition, at the destination that "
    "laid it down: that is the one thing RULED Q-F1 (a) permits to move, and "
    "it is not the corpus."
)


#: "the attribute is not there at all", which is a DIFFERENT answer from any
#: value the attribute could legally hold. `Document.revision` may lawfully be
#: `None` — a corpus with no revision notion reports one — so a `getattr(...,
#: None)` default would read a reader that omits the field entirely as one
#: that answered `None` correctly (Copilot, round 4).
_ABSENT = object()


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

    THE PATH IS RESTORED AFTERWARDS, AND SO IS THE MODULE CACHE — THE WHOLE
    CHAIN OF IT. This process may run several destinations in a session — the
    tests do — and a root left on `sys.path` would let the SECOND destination
    import the FIRST one's modules and pass on them. That is the privileged
    route again, arriving by accident, so the insertion is undone in a
    `finally`. `sys.path` is not the only cache a second destination can
    inherit from the first, though: `importlib.import_module` also caches by
    name in `sys.modules`, and restoring `sys.path` alone does not undo that
    — the plausible case is exact, since `home_factory.py` is documented as
    "the worked example a destination copies" and a destination that copies
    the file keeps its name too. So any prior `sys.modules` entry OWNED by
    this import is evicted before the import, forcing a fresh read off the
    roots just inserted, and whatever the import leaves behind is evicted
    again in the `finally` and the prior entries (if any) restored — the same
    discipline `sys.path` already gets.

    OWNED IS THE WHOLE CHAIN, NOT ONLY THE LEAF. A first pass here evicted
    `module_name` and its submodules and missed its PARENT PACKAGES: a
    dotted `--adapter opendox.reader:factory` imports `opendox` before it can
    import `opendox.reader`, and importing it caches `opendox` in
    `sys.modules` too — a package object whose `__path__` was resolved off
    THIS destination's roots. A second destination also declaring
    `opendox.reader` would then inherit the FIRST destination's cached
    `opendox` package unchanged, and Python would search for `.reader` inside
    it rather than under the second destination's own roots — the identical
    failure one level up, and restoring `sys.path` would not touch it either,
    for the same reason it does not touch the leaf. So every ancestor
    package of `module_name` is owned too, evicted and restored exactly as
    the leaf and its submodules are, and the module really is "held by
    reference rather than by name" once this call returns rather than merely
    being described that way.
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

    #: `module_name` itself, every package it is nested in ("a" and "a.b"
    #: for "a.b.c"), and every submodule importing it might leave behind —
    #: the whole chain `importlib.import_module` can populate or consult,
    #: not only the leaf.
    _parts = module_name.split(".")
    _ancestors = {".".join(_parts[:i]) for i in range(1, len(_parts))}

    def _owned(name: str) -> bool:
        return (name == module_name or name.startswith(module_name + ".")
                or name in _ancestors)

    stale = {name: mod for name, mod in sys.modules.items() if _owned(name)}
    for name in stale:
        del sys.modules[name]
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
        for name in [n for n in sys.modules if _owned(n)]:
            del sys.modules[name]
        sys.modules.update(stale)


def corpus_locations(corpus_root: Path) -> dict[str, str]:
    """The four states, checked for presence before a reader is blamed."""
    if not corpus_root.is_dir():
        raise ConformanceRefusal(
            "conformance-corpus-missing",
            f"the neutral corpus is not at {corpus_root}. It is "
            f"{CORPUS_RELPATH} in openxFactory (RULED OQ-3's seed); point "
            "--corpus at that directory, or at a destination's TRANSPOSITION "
            "of it — RULED Q-F1 (a) lets a destination lay the same documents "
            "down in the storage form its own reader addresses, and a "
            "transposition need not sit inside any checkout. Whichever it "
            "is, the four states are looked for by these names and a "
            "transposition is then proven faithful before a reader is "
            "measured")
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


def shipped_corpus_root() -> Path:
    """The corpus AS THIS REPOSITORY SHIPS IT, which is the reference side of
    the fidelity proof and never the thing under test."""
    return (ROOT / CORPUS_RELPATH).resolve()


def document_fingerprint(populated: Path) -> dict[str, str]:
    """`{key: sha256(bytes)}` over the populated corpus, read off the FILES.

    No reader is involved and none can be: this is the table a transposition
    is held to, so computing it through the very reader under test would be
    the measurement grading its own homework. Keys are POSIX-relative to the
    populated state, which is the spelling a reader that laid the same
    documents down serves them under.

    EVERY FILE UNDER THE POPULATED STATE COUNTS, and that is deliberate
    rather than an oversight about what a "document" is: a transposition
    that dropped one by deciding it was not a document would be exactly the
    quiet narrowing RULED Q-F1 (a) is guarded against. The corpus holds
    three files and three documents; if it ever held a file no reader
    serves, that is a change to the corpus and it belongs in a change, not
    in a reader's judgement at run time.
    """
    table: dict[str, str] = {}
    for path in sorted(populated.rglob("*")):
        if not path.is_file():
            continue
        key = path.relative_to(populated).as_posix()
        table[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return table


def fingerprint_digest(table: dict[str, str]) -> str:
    """One value naming a whole `{key: sha256}` table.

    A verdict line cannot carry three keys and three digests and stay
    readable, and evidence that says "faithful" without a value nobody can
    recompute is a claim rather than a measurement. Keys are sorted, so the
    digest is a property of the table and not of the order it was built in,
    and the framing is `carve_conformance._digest_tree`'s: key, NUL, digest,
    newline, so a key ending where another begins cannot collide.
    """
    digest = hashlib.sha256()
    for key in sorted(table):
        digest.update(key.encode("utf-8"))
        digest.update(b"\0")
        digest.update(table[key].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _unfaithful(corpus_root: Path, shipped: Path,
                detail: str) -> NoReturn:
    raise ConformanceRefusal(
        "conformance-corpus-unfaithful",
        f"the corpus at {corpus_root} is not the corpus this runner ships at "
        f"{shipped}, so a reader measured against it would be measured "
        f"against something nobody compared. {detail}")


def prove_transposition(factory: Any, populated: str, corpus_root: Path,
                        shipped: Path, reader: Any = None,
                        reference: dict[str, str] | None = None
                        ) -> dict[str, Any]:
    """Hold a `--corpus` that is not the shipped one to the shipped one's
    documents, keys and bytes — RULED Q-F1 (a), and the whole of what that
    ruling buys a destination.

    THE COMPARISON IS DELIBERATELY ASYMMETRIC. The reference comes off the
    files; the candidate comes through the READER, because a transposition
    into git history has no files to compare against and the only lawful way
    to ask what it holds is to ask the reader that addresses it. That is not
    a weaker claim than a file comparison: a transposition and a reader that
    were BOTH wrong in exactly the same way would still have to serve the
    shipped bytes under the shipped keys to get past this.

    KEYS ARE COMPARED AND NEVER PARSED, which is the interface's own rule —
    "a consumer may compare it, sort it and hand it back, and may not parse
    it". Nothing here reads a key to decide which document it is holding; it
    reads the key to decide whether the transposition put the document where
    the corpus has it. A destination that would rather serve its own key
    spelling is not transposing this corpus, it is authoring another one, and
    that is the case this refusal exists to name.

    RETURNS a record for the verdict rather than a bare bool, because a run
    over a transposition has to be able to SAY it was transposed. `proven`
    is False only where the reader could not be put to the corpus at all —
    resolution or listing raised — and that case is handed to the seventeen
    checks, which report it far better than one line here could; `main()`
    then refuses rather than printing OK if the seventeen somehow passed
    anyway. A reader that ANSWERS and answers differently refuses here.
    """
    # THE REFERENCE MAY BE PINNED BY THE CALLER, AND `main()` PINS IT
    # (Copilot, round 9). `resolve_factory` imports the DESTINATION's module,
    # which is arbitrary code running in this process, and it ran before this
    # table was ever computed: an import that rewrote the shipped fixtures
    # would have made the altered tree the reference, and the run would
    # report FAITHFUL for bytes nobody shipped. `main()` therefore takes this
    # table BEFORE the import and hands it in here. The AFTER-the-checks
    # proof deliberately does not take it — it recomputes from the files, and
    # `confirm_transposition_unmoved` compares the two digests, so a rewrite
    # at any point after the snapshot is what that comparison now catches.
    if reference is None:
        reference = document_fingerprint(shipped / POPULATED)
    if not reference:
        raise ConformanceRefusal(
            "conformance-corpus-missing",
            f"the corpus this runner compares a transposition against is not "
            f"at {shipped / POPULATED} (it is {CORPUS_RELPATH}/{POPULATED} in "
            "openxFactory), so --corpus cannot be proven faithful to "
            "anything. Run from a checkout that carries the corpus")
    record: dict[str, Any] = {
        "path": str(corpus_root),
        "shipped": str(shipped),
        "documents": len(reference),
        "digest": fingerprint_digest(reference),
        #: The revision the transposition was PROVEN at, so the evidence
        #: names it rather than naming a path that may have moved since
        #: (Copilot, round 1). `None` where the corpus carries no revision
        #: notion, which the interface permits -- a directory corpus reports
        #: none, and `confirm_transposition_unmoved` then re-PROVES it rather
        #: than comparing a value that does not exist.
        "revision": None,
        "proven": False,
        "reason": None,
    }

    requested = CorpusRef(name="populated", location=populated)
    try:
        # `reader` is the instance the SEVENTEEN used, when a caller has one
        # to hand (Copilot, round 8); otherwise the factory builds a fresh
        # one, which is the ordinary before-the-checks case.
        if reader is None:
            reader = factory(requested.name, populated)
        corpus = reader.resolve(requested)
        documents = tuple(reader.list_documents(corpus))
    except Exception as exc:  # noqa: BLE001 - see the docstring
        record["reason"] = (f"the reader could not be put to it: "
                            f"{type(exc).__name__}: {exc}")
        return record

    # THE ANCHOR IS THE REQUEST, NOT WHAT CAME BACK (Copilot, round 6). Every
    # identity below is held to the reference the resolution carries — and
    # `ResolvedCorpus.ref` is the reader's own return value, so a reader
    # could resolve under `name="other"`, list and read every document under
    # `"other"`, and satisfy both this proof AND the seventeen, which read
    # the same returned ref. The interface's contract is that `ref` is the
    # REQUEST ("the caller's REQUEST for a corpus, before anything has been
    # resolved"), so it is compared with the request this runner made before
    # anything is anchored to it — ALL THREE of its fields, `revision`
    # INCLUDED (Copilot, round 7). `CorpusRef.revision` is part of what a
    # caller asks for ("None means 'whatever the location currently is'"), so
    # a resolution that comes back carrying a different revision than the one
    # requested has answered a question nobody asked, and every later
    # comparison here would be anchored to that substitution.
    # `ResolvedCorpus.location` is deliberately NOT compared: that one is
    # documented as "resolved, absolute" and is allowed to differ from the
    # location asked for.
    ref = getattr(corpus, "ref", None)
    ref_name = getattr(ref, "name", _ABSENT)
    ref_location = getattr(ref, "location", _ABSENT)
    ref_revision = getattr(ref, "revision", _ABSENT)
    if ((ref_name, ref_location, ref_revision)
            != (requested.name, requested.location, requested.revision)):
        shown = tuple("(absent)" if value is _ABSENT else value
                      for value in (ref_name, ref_location, ref_revision))
        _unfaithful(corpus_root, shipped,
                    f"it was asked to resolve "
                    f"{(requested.name, requested.location, requested.revision)!r}"
                    f" and came back carrying the reference {shown!r}. "
                    "Every identity below is anchored to the reference a "
                    "resolution carries, so a reference that is not the one "
                    "asked for anchors nothing")
    # READ ONCE, AND EVERY COMPARISON BELOW READS THIS LOCAL (Copilot, round
    # 7). `ResolvedCorpus.revision` is a REQUIRED field of the interface
    # whose `None` is legal ("None where this corpus carries no revision
    # notion"), so a resolution that omits it altogether is MALFORMED rather
    # than a corpus without revisions — and reading it straight off `corpus`
    # at the per-document comparison would raise `AttributeError` out of a
    # proof whose whole contract is to refuse by name, which `main()` would
    # then report as the generic `conformance-unreadable`. Reading it once
    # also denies a reader the trick of answering one revision at the top of
    # the proof and another inside the loop.
    corpus_revision = getattr(corpus, "revision", _ABSENT)
    if corpus_revision is _ABSENT:
        _unfaithful(corpus_root, shipped,
                    "the resolution it answered with carries no `revision` "
                    "field at all. `None` is a legal answer there — a corpus "
                    "that carries no revision notion — and silence is not: a "
                    "transposition cannot be proven at a revision nobody "
                    "reports")
    # AND IT MUST BE OF THE TYPE THE INTERFACE DECLARES (Copilot, round 8).
    # `ResolvedCorpus.revision` is `str | None`, and none of these return
    # types is enforced at runtime — the seam is structural. A reader
    # answering an int, consistently from `resolve` and from `read`, would
    # satisfy every comparison here and be recorded at a revision the
    # EVIDENCE then laundered into a string through `str()`: the verdict line
    # would name a revision that is not the object the reader used.
    if corpus_revision is not None and not isinstance(corpus_revision, str):
        _unfaithful(corpus_root, shipped,
                    f"the resolution it answered with carries revision "
                    f"{corpus_revision!r}, which is "
                    f"{type(corpus_revision).__name__} where the interface's "
                    "`ResolvedCorpus.revision` is `str | None`. A revision "
                    "this runner has to stringify before it can be recorded "
                    "is not the revision anything was proven at")
    record["revision"] = (str(corpus_revision)
                          if corpus_revision is not None else None)

    served: dict[str, str] = {}
    for document in documents:
        key = getattr(document, "key", None)
        if not isinstance(key, str):
            _unfaithful(corpus_root, shipped,
                        f"the listing served {document!r}, which carries no "
                        "string key, so what it holds cannot be compared with "
                        "what the corpus holds")
        # THE LISTING'S OWN IDENTITIES ARE CHECKED TOO, not only what `read`
        # answers with (Copilot, round 5). `DocumentId.corpus` is half of the
        # interface's identity and every adapter builds it from
        # `corpus.ref.name`; a reader that listed every key under some OTHER
        # corpus name and then echoed that same identity back from `read`
        # would satisfy the comparison below, the key/bytes table AND
        # `read-round-trip` — all three compare against the same wrong
        # object. The name it is held to is the one the anchor above already
        # proved equal to the REQUEST, read from that local rather than back
        # through `corpus.ref` on every pass.
        listed_corpus = getattr(document, "corpus", _ABSENT)
        if listed_corpus != ref_name:
            _unfaithful(corpus_root, shipped,
                        f"it listed {key!r} under corpus "
                        f"{'(absent)' if listed_corpus is _ABSENT else repr(listed_corpus)}"
                        f", and the corpus it resolved is "
                        f"{ref_name!r}. A listing under another "
                        "corpus's identity says nothing about this one")
        try:
            got = reader.read(corpus, document)
        except Exception as exc:  # noqa: BLE001
            _unfaithful(corpus_root, shipped,
                        f"it lists {key!r} and will not serve it: reading at "
                        f"the corpus's declared revision raised "
                        f"{type(exc).__name__}: {exc}. A document a reader "
                        "will not serve is a document the transposition does "
                        "not carry")
        # THE IDENTITY THE BYTES CAME BACK UNDER, read STRUCTURALLY — by
        # `corpus` and `key`, never by dataclass equality, because a reader
        # authored elsewhere holds its own replica of the interface and its
        # `DocumentId` is a different class object with the same shape.
        # Without this the proof would record the bytes under the key it
        # ASKED for while the reader answered for another document, and the
        # seventeen would not catch it: `read-round-trip` checks the identity
        # of the FIRST document only (Copilot, round 4).
        got_id = getattr(got, "id", None)
        got_corpus = getattr(got_id, "corpus", _ABSENT)
        got_key = getattr(got_id, "key", _ABSENT)
        if got_corpus is _ABSENT or got_key is _ABSENT:
            _unfaithful(corpus_root, shipped,
                        f"reading {key!r} returned an object carrying no "
                        "document identity, so what it answered for cannot "
                        "be compared with what was asked for")
        # AGAINST THE IDENTITY AS IT WAS LISTED, captured before `read` ran
        # (Copilot, round 8). `document` is the READER's object and the
        # interface's `DocumentId` is frozen only in this repository's
        # replica; a foreign mutable one could be rewritten by the `read`
        # call itself, so that the identity answered for and the identity
        # re-read here agree — on a document nobody listed.
        if (got_corpus, got_key) != (listed_corpus, key):
            _unfaithful(corpus_root, shipped,
                        f"it was asked for "
                        f"{(listed_corpus, key)!r} and answered for "
                        f"{(got_corpus, got_key)!r}. Bytes served under an "
                        "identity nobody asked for say nothing about the "
                        "document that was requested")
        # THE REVISION THE BYTES CAME FROM, and it is the interface's own
        # contract rather than an extra demand (Copilot, round 2):
        # "`revision=None` means the revision `corpus` was resolved at", and
        # `Document.revision` reports which one it was. A reader that resolves
        # one revision and serves another — a working tree, an older commit —
        # would otherwise be recorded FAITHFUL on bytes that answer a question
        # nobody asked, and the seventeen checks do not inspect
        # `Document.revision` either, so this is the only place it is held.
        # THE SENTINEL IS LOAD-BEARING (Copilot, round 4): `None` is a LEGAL
        # value of this field, so a `getattr` default of `None` would read a
        # reader that omits `revision` altogether as one that answered
        # correctly for a corpus that declares no revision.
        served_at = getattr(got, "revision", _ABSENT)
        if served_at is _ABSENT:
            _unfaithful(corpus_root, shipped,
                        f"reading {key!r} returned an object with no "
                        "`revision` field at all. `None` is a legal answer "
                        "there and silence is not: the interface's contract "
                        "is that a document reports the revision it was read "
                        "at")
        # AND OF THE TYPE THE INTERFACE DECLARES, BEFORE IT IS COMPARED
        # (the follow-up to #1086's registered finding 1). `Document.revision`
        # is `str | None`, and the equality below is the READER's `__eq__`: a
        # structurally loaded object can claim equality with the declared
        # string and pass, and the proof would then certify a malformed
        # document response. `ResolvedCorpus.revision` is already held to its
        # declared type twelve lines up (round 8); this is the same check on
        # the other half of the same contract, and it has to run BEFORE the
        # comparison rather than after it, because after it the comparison has
        # already been decided by the object under test.
        if served_at is not None and not isinstance(served_at, str):
            _unfaithful(corpus_root, shipped,
                        f"reading {key!r} answered with revision "
                        f"{served_at!r}, which is "
                        f"{type(served_at).__name__} where the interface's "
                        "`Document.revision` is `str | None`. A revision this "
                        "runner would have to stringify before it could be "
                        "recorded is not the revision anything was served at")
        if served_at != corpus_revision:
            _unfaithful(corpus_root, shipped,
                        f"it served {key!r} at revision {served_at!r} while "
                        f"the corpus it resolved declares {corpus_revision!r}. "
                        "A reader answering out of a revision the caller did "
                        "not ask for has not shown that the transposition "
                        "holds anything")
        content = getattr(got, "content", None)
        if not isinstance(content, bytes):
            _unfaithful(corpus_root, shipped,
                        f"reading {key!r} returned {type(content).__name__} "
                        "where the interface's `Document.content` is bytes")
        # A key listed TWICE collapses here rather than refusing, because a
        # duplicate listing is a READER defect and `list-stable` is the check
        # that owns it (`unique=False`). The corpus is still compared
        # correctly: a duplicate cannot hide a missing or an extra document.
        served[key] = hashlib.sha256(content).hexdigest()

    missing = sorted(set(reference) - set(served))
    extra = sorted(set(served) - set(reference))
    changed = sorted(k for k in set(reference) & set(served)
                     if reference[k] != served[k])
    if missing or extra or changed:
        parts = []
        if missing:
            parts.append(f"documents the corpus holds and it does not serve: "
                         f"{', '.join(repr(k) for k in missing)}")
        if extra:
            parts.append(f"documents it serves and the corpus does not hold: "
                         f"{', '.join(repr(k) for k in extra)}")
        if changed:
            # WHOLE DIGESTS, never prefixes (Copilot, round 1). A mismatch a
            # reader cannot recompute from the failure output is a claim
            # rather than a measurement, and twelve hex characters is not
            # something anybody can check a sha256 against.
            parts.append("documents whose bytes differ: " + ", ".join(
                f"{k!r} (corpus {reference[k]}, served {served[k]})"
                for k in changed))
        _unfaithful(
            corpus_root, shipped,
            "; ".join(parts) + ". RULED Q-F1 (a) lets a destination TRANSPOSE "
            "the corpus into the storage form its reader addresses, with the "
            "documents, the keys and the BYTES unchanged; this is a different "
            "corpus, and remediating it by editing the shipped one is FLOOR "
            "PART 3 deleted")

    record["proven"] = True
    record["served_digest"] = fingerprint_digest(served)
    return record


def witnessed_factory(factory: Any, seen: dict[str, Any]) -> Any:
    """Hand `carve_conformance.run` the REAL reader and keep a reference.

    COPILOT'S ROUND-8 FINDING, AND IT IS THE LAST GAP BETWEEN THE PROOF AND
    THE MEASUREMENT. `carve_conformance.run` builds its own readers —
    `factory("populated", ...)` and one per other state — so the instance the
    seventeen measure is not the instance the proof read. A STATEFUL FACTORY
    could serve the shipped bytes to the proof and altered bytes to the run:
    `CorpusExpectation` is counts and explicitly "not the documents' names
    and not their bytes", so a document whose content moved without changing
    its classification passes all seventeen, and the verdict would read
    FAITHFUL over bytes nothing proved.

    THIS IS A FUNCTION AND NOT A PROXY OBJECT, deliberately. A wrapper object
    would become what `structural-conformance` inspects — that check is
    `isinstance(reader, CorpusAdapter)` on whatever the factory returned — and
    the first of the seventeen would then measure this file instead of the
    destination's reader. What comes back here is the reader itself,
    unwrapped; only a reference to it is kept.

    WHAT IT STILL DOES NOT CATCH, named rather than left to be discovered: a
    reader that answers differently on two CALLS to the same instance. No
    bracketing can close that one — the proof and the checks are different
    calls by construction — and a destination doing it is forging its own
    § 3.7 evidence rather than defeating a measurement.
    """
    def make(name: str, location: str) -> Any:
        reader = factory(name, location)
        seen.setdefault(name, reader)
        return reader
    return make


def confirm_transposition_unmoved(factory: Any, populated: str,
                                  corpus_root: Path, shipped: Path,
                                  record: dict[str, Any],
                                  reader: Any = None) -> None:
    """Re-prove the transposition AFTER the seventeen, and refuse if it moved.

    COPILOT'S ROUND-1 FINDING, AND IT IS A REAL WINDOW. `prove_transposition`
    resolves the corpus and reads it; `carve_conformance.run` then builds its
    OWN readers off the same path and resolves again. Between those two the
    location can move — a git `HEAD` advanced by something else, a directory
    rewritten — and the seventeen would have measured a revision nobody
    proved while the verdict said FAITHFUL.

    IT IS CLOSED BY DETECTION AND NOT BY PINNING, deliberately: pinning would
    mean handing `carve_conformance.run` a pre-resolved corpus, and that
    module's signature is the one thing every destination runs. This is the
    discipline `write-back-leaves-the-tree` already uses one level down —
    digest before, digest again after.

    It re-PROVES rather than comparing revisions, which is what catches the
    case a revision comparison cannot: a directory corpus reports
    `revision=None` (the interface permits it), so content rewritten under a
    revision that cannot move is caught by the proof itself, naming the
    document. The revision comparison on top of that catches the other shape
    — the same three documents at a DIFFERENT revision, where the content
    table is identical and only the revision moved.

    It runs ONLY after a fully green run — `run_corpus` raises on any failed
    check first — so it can never mask `write-back-leaves-the-tree`: a tree
    that moved under the write-back would have failed that check and never
    reached here.
    """
    after = prove_transposition(factory, populated, corpus_root, shipped,
                                reader=reader)
    if not after["proven"]:
        _unfaithful(corpus_root, shipped,
                    "it was proven faithful before the seventeen checks and "
                    f"could not be read after them: {after['reason']}")
    if after["digest"] != record["digest"]:
        # THE REFERENCE SIDE CAN MOVE TOO (Copilot, round 6). `after` is a
        # whole fresh proof, so it recomputed the SHIPPED table as well; if
        # that table changed under the run — a transposition sharing files
        # with the fixtures through hard links, a reader that wrote both
        # sides — the candidate could match the NEW reference while the
        # verdict still carried the old digest. Then "faithful to
        # <digest>" would name a corpus that no longer exists.
        _unfaithful(corpus_root, shipped,
                    f"the corpus this runner ships MOVED under the "
                    f"measurement: its key/sha256 table was "
                    f"{record['digest']} when the transposition was proven "
                    f"against it and is {after['digest']} now, so the "
                    "verdict's digest names a corpus that is no longer there")
    if after["revision"] != record["revision"]:
        _unfaithful(corpus_root, shipped,
                    f"it moved UNDER the measurement: proven at revision "
                    f"{record['revision']!r} and now at {after['revision']!r}, "
                    "so the seventeen checks did not measure the revision "
                    "this run proved")
    # NO SECOND CONTENT COMPARISON HERE, and the omission is measured rather
    # than an oversight: the call above already held the corpus to the
    # SHIPPED table, so content that changed under the run refuses inside it,
    # NAMING THE KEY — a better message than any digest-to-digest line here.
    # A digest comparison at this point could only compare two values both
    # equal to the reference, which is a check that cannot fail.
    record["revision_confirmed"] = True


def run_corpus(factory: Any, locations: dict[str, str], destination: str,
               dest_root: Path, corpus_root: Path, adapter: str,
               transposition: dict[str, Any] | None = None) -> dict[str, Any]:
    outcomes = carve_conformance.run(factory, **locations)
    passed, total, failed = carve_conformance.verdict(outcomes)
    summary: dict[str, Any] = {
        "result": "ok" if not failed else "refused",
        "destination": destination,
        "dest_root": str(dest_root),
        "corpus": str(corpus_root),
        #: `None` where `--corpus` is this repository's own fixtures — the
        #: shipped corpus compared with itself proves nothing and is not
        #: claimed. A record here is RULED Q-F1 (a)'s evidence.
        "transposition": transposition,
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


def _refused(exc: ConformanceRefusal, args: argparse.Namespace, where: str,
             corpus_root: Path | None = None,
             transposition: dict[str, Any] | None = None) -> int:
    """The ONE refusal exit: `--json` object or the rendered human message."""
    if args.json:
        print(json.dumps({"result": "refused", "code": exc.code,
                          "detail": exc.detail,
                          "destination": args.destination,
                          "dest_root": args.dest_root,
                          # THE PROOF RIDES THROUGH THE REFUSAL TOO (the
                          # follow-up to #1086's registered finding 2). A
                          # `--corpus` run can be proven faithful and then
                          # refuse `conformance-check-failed`, and the runbook
                          # promises machine consumers the transposition's
                          # path, shipped corpus, document count and table
                          # digest. Dropping the record here left them
                          # reconstructing it from prose, or unable to tell
                          # WHICH proven transposition a failure covered. Same
                          # key and same shape as the success payload, `null`
                          # where nothing was proven.
                          "transposition": transposition,
                          # WHICH corpus was refused against, because a
                          # `conformance-corpus-unfaithful` object that does
                          # not name the corpus leaves a caller reading the
                          # prose to find out. THE RESOLVED PATH AND NOT THE
                          # FLAG (Copilot, round 1): `args.corpus` is `null`
                          # on a default run and an uncanonicalized relative
                          # path when one was given, so a caller comparing a
                          # refusal with a summary — which carries the
                          # resolved path — would be comparing two spellings
                          # of one directory, or nothing at all.
                          "corpus": (str(corpus_root) if corpus_root
                                     else args.corpus),
                          "adapter": args.adapter}))
    else:
        print(exc.render(where), file=sys.stderr)
    return 2


def _print_ok(summary: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary))
        return
    # A TRANSPOSED corpus says so IN THE VERDICT, and carries the value that
    # backs the word: § 3.7's evidence is a line somebody pastes into a pull
    # request, and "passed" over a corpus laid down somewhere else, with no
    # way to tell which corpus it was, is the one reading RULED Q-F1 (a)
    # cannot afford.
    transposed = ""
    record = summary.get("transposition")
    if record:
        # AN EMPTY REVISION IS NOT AN ABSENT ONE (Copilot, round 9). The
        # interface permits any `str`, the empty one included, and a
        # truthiness test rendered it as "no declared revision" — the human
        # line then contradicting the `--json` record, which carries `""`.
        at = ("no declared revision" if record["revision"] is None
              else f"revision {record['revision']}" if record["revision"]
              else "an empty declared revision")
        transposed = (f", TRANSPOSED and FAITHFUL to {record['shipped']} — "
                      f"{record['documents']} document(s) at {at}, key/sha256 "
                      f"table {record['digest']}, unmoved across the run")
    print(f"OK {summary['dest_root']}: {summary['destination']} passed the "
          f"neutral conformance corpus — {summary['passed']} of "
          f"{summary['checks_run']} check(s), reader "
          f"{summary['adapter']}, corpus {summary['corpus']}{transposed}")


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
        help=(f"the neutral corpus (default: <this repository>/"
              f"{CORPUS_RELPATH}), or a destination's TRANSPOSITION of it — "
              "RULED Q-F1 (a). A transposition is proven faithful to the "
              "shipped corpus, document by document and byte by byte, before "
              "any check runs, and is named in the verdict"))
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
    # DECLARED here and RESOLVED inside the `try`, and the split is the whole
    # of two findings at once. Declared here so that every refusal below can
    # name the corpus it was about, in the same spelling a successful summary
    # uses (Copilot, round 1); resolved inside, because `Path.resolve()` is
    # an `OSError` away from a traceback — a `--corpus` symlink loop is the
    # exact case — and this file has no exit 1 (Copilot, round 2). Where the
    # resolution itself fails it stays `None` and `_refused` falls back to
    # the raw flag, which is all there is to name at that point.
    corpus_root: Path | None = None
    #: The fidelity proof, declared out here for the same reason `corpus_root`
    #: is: every refusal below has to be able to name the transposition it was
    #: about (the follow-up to #1086's registered finding 2). It stays `None`
    #: until `prove_transposition` returns, so a refusal raised before that
    #: carries `null` rather than a half-built record.
    transposition: dict[str, Any] | None = None
    try:
        corpus_root = (Path(args.corpus).resolve() if args.corpus
                       else (ROOT / CORPUS_RELPATH).resolve())
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
        # THE REFERENCE IS TAKEN BEFORE THE DESTINATION'S CODE IS IMPORTED
        # (Copilot, round 9). `resolve_factory` imports an arbitrary module
        # out of `--dest-root`, and a module-level statement there could
        # rewrite the shipped fixtures; a reference computed afterwards would
        # be the destination's own work. Taken here it is not, and any later
        # rewrite refuses at `confirm_transposition_unmoved`, which recomputes
        # the table and compares it with this one.
        shipped = shipped_corpus_root()
        pinned = (document_fingerprint(shipped / POPULATED)
                  if corpus_root != shipped else None)
        factory = resolve_factory(args.adapter, dest_root, args.sys_path)
        # RULED Q-F1 (a), and the order is the whole of it: a transposition is
        # proven faithful BEFORE the seventeen, because a reader measured
        # against a corpus nobody compared is not measured. The shipped corpus
        # compared with itself is not a transposition and is not claimed as
        # one, so the default run is untouched.
        if corpus_root != shipped:
            transposition = prove_transposition(
                factory, locations["populated"], corpus_root, shipped,
                reference=pinned)
        #: The instances `carve_conformance.run` built, by corpus state. The
        #: re-proof below is put to the POPULATED one — the reader the
        #: seventeen actually measured (Copilot, round 8).
        seen: dict[str, Any] = {}
        summary = run_corpus(witnessed_factory(factory, seen), locations,
                             args.destination, dest_root, corpus_root,
                             args.adapter, transposition)
        if transposition is not None and transposition["proven"]:
            confirm_transposition_unmoved(
                factory, locations["populated"], corpus_root, shipped,
                transposition, reader=seen.get("populated"))
        if transposition is not None and not transposition["proven"]:
            # The seventeen passed over a corpus this run could not compare.
            # Every ordinary way of reaching here fails a check first
            # (`resolve-populated`, `list-population`), so this is the last
            # gate rather than the expected one — and it is fail-closed
            # because the alternative is an OK line that says "faithful"
            # about a corpus nobody proved anything about.
            raise ConformanceRefusal(
                "conformance-corpus-unfaithful",
                f"the seventeen checks passed over the corpus at "
                f"{corpus_root}, and it was never proven faithful to the one "
                f"this runner ships at {shipped}: "
                f"{transposition['reason']}. A pass recorded against an "
                "unproven transposition is FLOOR PART 3 recorded against a "
                "corpus nobody compared")
    except ConformanceRefusal as exc:
        return _refused(exc, args, where, corpus_root, transposition)
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
            args, where, corpus_root, transposition)
    _print_ok(summary, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
