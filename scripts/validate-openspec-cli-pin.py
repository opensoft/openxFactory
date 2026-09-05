#!/usr/bin/env python3
"""Run OpenSpec strict validation through the PINNED CLI, and refuse otherwise.

This file is TWO things at once, and the doubling is the design rather than an
economy. It is the VERIFIER of `contracts/openspec-cli-pin.yaml` — the running
code `neutral-product-pin` requires a pin to have — and it is the CONSUMER
ENTRYPOINT through which every repository in the estate runs
`openspec validate … --strict`. They are one file because separating them would
reintroduce exactly the defect the pin exists to close: a verifier nobody is
obliged to call, standing beside a bare `openspec` invocation that answers with
whatever is on PATH.

WHAT WAS WRONG BEFORE. The OpenSpec CLI was UNPINNED fleet-wide. The only pin in
the estate was one literal line in this repository's test workflow
(`.github/workflows/pytest-suite.yml`, `npm install -g @fission-ai/openspec@1.2.0`),
installed so `tests/proposal-support/` could drive the real binary; no consuming
repository read it, nothing verified it, and nothing refused when a different
version answered. `openspec validate --all --strict` — the gate a delta passes
before it may archive — ran in NO repository's CI at all. Every engineer and
every agent validated and archived with whatever `openspec` happened to be
installed.

THE TRUSTED REFERENT IS THE TARBALL'S INTEGRITY, NOT THE VERSION STRING. A
version number is a NAME that a registry's policy keeps stable; a SHA-512 over
the published bytes is a CONTENT ADDRESS that nothing can move. So this tool does
NOT trust `npx -y @fission-ai/openspec@1.2.0` to have resolved the right artifact.
It FETCHES the tarball, RECOMPUTES its SHA-512 and its SHA-1, refuses
`pin-integrity-mismatch` unless both equal the pin — and only then installs and
invokes it. `neutral-product-pin` requires that ordering in as many words: the
pin's digests are verified BEFORE the pinned reader is invoked, "by running code
rather than by a stated obligation".

SIX CHECKS, ORDERED, FIRST FAILURE WINS.

  1. the pin's SHAPE — `revision_kind: package_integrity`, an EXACT version (no
     range, no caret, no dist-tag), a well-formed `sha512-` integrity, a 40-hex
     `shasum`, and — where the pin declares any — WELL-FORMED DISPOSITIONS
  2. a SCAN TARGET was given — `--all`, or at least one change id
  3. the fetched artifact's recomputed SHA-512 and SHA-1 EQUAL the pin
  4. the resolved binary REPORTS the pinned version
  5. `openspec validate <target> --strict` runs, and its findings are read
  6. every ERROR-level finding is matched by exactly one IN-SCOPE disposition,
     and every in-scope disposition is matched by a finding that STILL OCCURS

DISPOSITIONS, AND WHY THE MECHANISM EXISTS AT ALL. A pinned tool is a foreign
judgment about a local corpus, and the two can genuinely disagree. Measured at
`1.12.0` on 2026-09-05 (`openspec/changes/prepare-openspec-1.12-readiness/
evidence/openspec-1.12-readiness-2026-09-05.md`), exactly two ERROR-level
findings in this corpus are that disagreement: 1.12.0's scenario-currency check
demands the restoration of two scenario titles whose omission this estate
DECLARED with its reserved ``**Merged into `<destination>` by <change> (<date>):**``
marker — a convention `doc-health`'s own promoted requirement carries, using one
of those two pairs as its WORKED EXAMPLE. The check is marker-blind. The only
edit that satisfies it reverts two ratified decisions. So the finding is not a
defect to be fixed; it is an exception to be ACCEPTED, in writing, with a
citation — and this file is where "accepted" is made checkable rather than
remembered.

A disposition therefore carries a CITATION or it is not a disposition. An
exception with no `cited_to:` is an uncited exception, which is the thing this
estate refuses everywhere else it appears (`doc-health`'s uncited-resolution
rule, `health/dispositions.yaml`'s required `cite`), so a disposition missing
one is `pin-disposition-malformed` and the whole run refuses — never "the
disposition is ignored", because ignoring it would silently re-fail a finding
somebody believed was settled.

THE ASYMMETRY: AN UNMATCHED FINDING FAILS (exit 1), AN UNMATCHED DISPOSITION
REFUSES (exit 2). They are different defects with different owners. An
undispositioned finding is a statement about the DELTAS — somebody wrote
something the pinned tool rejects, and the remedy is theirs: fix it, or
disposition it with a citation. A disposition matched by nothing is a statement
about the PIN — the exception outlived the condition it was granted for, and the
remedy is to edit this repository's pin file. Silently tolerating the second is
how a suppression list rots into a blanket: `add-composed-view-authoring` has ONE
open task left and archives the moment a human takes it, at which point its
finding disappears from every run and its disposition would sit here forever,
suppressing a class of finding nobody re-examined. Refusing makes the archive
itself the event that forces the re-examination. Dispositions are therefore
UPGRADE-COUPLED and ARCHIVE-COUPLED: they are re-derived at every pin bump and
retired the moment their finding stops occurring.

SCOPE, AND WHY A DISPOSITION NAMES A REPOSITORY. One pin file governs every
repository in the estate, and this entrypoint is invoked with `--repo` against
consuming trees that carry none of openxFactory's changes. Without scoping,
`add-chain-attestation` — absent from OpsxFactory's corpus because it was never
in it — would be indistinguishable from `add-composed-view-authoring` absent from
openxFactory's corpus because it archived, and the second MUST refuse while the
first must not. So each disposition declares `repo:`, the run resolves the
validated tree's identity from `git config --get remote.origin.url`, and a
disposition naming another repository is OUT OF SCOPE: neither applied nor
checked for staleness. Where dispositions are declared and that identity cannot
be resolved, the run refuses `pin-repo-unidentified` rather than guessing which
half of the file applies.

Check 2 is second and not last on purpose. `neutral-product-pin` says a pinned
validator invoked with no scan target must REFUSE rather than self-test, "because
a self-test that opens no governed surface is a green check that verified
nothing" — so the refusal must arrive before any expensive, green-looking work
happens, not after it. For the same reason THIS TOOL HAS NO `--verify-only` MODE:
a flag that verifies the pin and validates nothing is precisely the target-less
green check that requirement forbids, and offering it would put the hole back
behind a convenience.

TWO MODES, AND THE DEFAULT IS THE ONE PATH CANNOT AFFECT.

  * PINNED (default) — the artifact is fetched from the registry, verified, and
    installed into a private prefix. Whatever `openspec` is on PATH is
    IRRELEVANT: it is never consulted, so it cannot make a gate pass or fail.
    This is the mode every required check uses.
  * `--path-mode` — the `openspec` on PATH is used, and is REFUSED
    `pin-version-mismatch` unless it reports exactly the pinned version. It
    exists because a developer iterating locally should not pay a registry round
    trip per run, and because "your PATH binary is the wrong version" is a far
    more useful thing to be told than a silent divergence. It is not for gates,
    and the gate does not pass it.

STANDARD LIBRARY ONLY, on the sibling verifiers' reasoning: the pin's grammar is
a fixed, small subset this repository authors, so `read_pin` parses exactly that
subset and REFUSES anything outside it rather than guessing. An unparseable line
is `pin-unreadable`, never a skipped rule — a line a narrow reader does not
understand must stop the run, because a skipped line is a rule that silently did
not apply.

Exit codes:
  0  the pin is satisfied AND every ERROR-level finding the pinned CLI reported
     is covered by an in-scope, cited disposition (usually: there were none)
  1  the pin is satisfied, the pinned CLI RAN, and it reported ERROR-level
     findings this pin does not disposition
  2  ANY refusal, and any environment failure — INCLUDING a malformed or a STALE
     disposition, both of which are defects of the PIN rather than of the deltas

  A STALE DISPOSITION EXITS 2 AND NOT 3, deliberately. Exit 2 already means "the
  pin could not be trusted", and a suppression this pin grants for a condition
  that no longer occurs is exactly that: the pin is asserting something about the
  corpus that is no longer true, and the remedy — edit
  `contracts/openspec-cli-pin.yaml` — is the same remedy every other exit 2
  carries. A third exit code would also silently reclassify the run for every
  caller that branches on 0/1/2 today, `.github/workflows/openspec-cli-pin-gate.yml`
  included, which is a compatibility break bought for a distinction the refusal
  CODE already draws.

  The sibling verifiers have no exit 1, deliberately, because their only question
  is "may this pull request proceed" and a stale pin and an unresolvable tree are
  the same answer to it. This tool asks a SECOND question the siblings do not:
  having established which tool adjudicates, what did that tool say? "The pin
  could not be trusted" and "the pin held and your deltas are invalid" send a
  reader to completely different remedies — re-cut the pin, versus fix the delta
  — and collapsing them would hide the ordinary finding inside the extraordinary
  one. Both are non-zero, so no gate is weakened by the distinction.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "openspec-cli-pin.yaml"

# The ONE fixed remediation trailer for every fail-closed refusal (the form
# `neutral-product-pin` requires: a refusal that names what is wrong without
# naming what to run puts the exit in tribal memory instead of in the message).
REMEDIATION = (
    "Remediation: run strict validation through this entrypoint and nothing "
    "else, e.g. `python3 scripts/validate-openspec-cli-pin.py --all` from the "
    "repository root, or `--change <id>` for one change; add `--repo PATH` to "
    "validate a consuming repository's tree from this pinned checkout. If the "
    "run cannot reach the registry, install the pinned artifact once "
    "(`npm pack @fission-ai/openspec@<version>`) and pass "
    "`--tarball <path/to/.tgz>`; the digest is checked either way. If a local "
    "`openspec` is the problem, either stop using it — the default mode never "
    "reads PATH — or install the pinned version. If the PIN itself is stale "
    "rather than the environment, a version bump is a HUMAN-ONLY governed "
    "change that re-cuts contracts/openspec-cli-pin.yaml from the real "
    "registry bytes and lands `--all --strict` proof at the target version in "
    "the same change; never edit an integrity value to make this pass. See "
    "docs/contract-versioning-policy.md."
)

# The refusal vocabulary, fixed. Other code may branch on the CODE, so no
# failure path here may invent one.
#
# `pin-unreadable` is NOT in the vocabulary and its absence is the point, on the
# siblings' reasoning: the five below describe an ENVIRONMENT that disagrees with
# a well-formed pin, each a finding a reviewer can act on. `pin-unreadable`
# describes a state in which no finding can be reached at all. It still exits 2 —
# excluded from the vocabulary, not from fail-closure.
REFUSAL_CODES: tuple[str, ...] = (
    "pin-tag-only",
    "pin-no-target",
    "pin-unresolvable",
    "pin-integrity-mismatch",
    "pin-version-mismatch",
    "pin-disposition-malformed",
    "pin-disposition-stale",
    "pin-report-unreadable",
    "pin-repo-unidentified",
)

# The four codes above the line are ENVIRONMENT disagreements with a well-formed
# pin. The four below are the disposition mechanism's own, and they are in the
# vocabulary on the same test the first five passed: each describes a finding a
# REVIEWER CAN ACT ON, in a place a reviewer can reach.
#
#   pin-disposition-malformed  an exception was declared without a citation, or
#                              without the keys that decide what it matches
#   pin-disposition-stale      an exception is matched by no finding in this run
#   pin-report-unreadable      the pinned CLI produced no machine-readable
#                              verdict, so no finding could be reconciled against
#                              anything — refused rather than degraded to the
#                              streaming path, because a run that cannot read its
#                              own findings cannot honour a disposition and would
#                              re-fail conditions the pin has settled
#   pin-repo-unidentified      dispositions are declared and the validated tree's
#                              identity is unresolvable, so which of them are in
#                              scope is unanswerable

# The disposition keys, split into what MUST be present and what MAY be. The
# split is a declaration rather than a chain of `if key not in entry`, so
# admitting a key later is an edit to this tuple and to the prose beside it.
#
# `finding` is the CLI's message text and it is matched WHOLE, remedy sentence
# and all, after whitespace normalization — see `normalized_finding`.
DISPOSITION_REQUIRED: tuple[str, ...] = (
    "repo", "item", "path", "finding", "why", "cited_to")

# Either spelling of the authority is accepted and exactly one is required.
# `ratified_by` is the act of a convener; `recorded_by` is the weaker claim a
# lane may make where a human ruling is recorded rather than given. A
# disposition carrying NEITHER is anonymous, and an anonymous exception is not
# an exception anybody granted.
DISPOSITION_AUTHORITY: tuple[str, ...] = ("ratified_by", "recorded_by")

# The finding levels this tool RECONCILES. Everything else the CLI emits —
# `WARNING`, `INFO` — is reported and counted but never blocks and never needs a
# disposition, because the CLI's own verdict does not turn on it.
BLOCKING_LEVELS: frozenset[str] = frozenset({"ERROR"})

# An EXACT semantic version and nothing else. Ranges (`^1.2.0`, `~1.2`, `1.x`,
# `>=1.2.0`), dist-tags (`latest`, `next`) and bare majors all fail this and are
# refused `pin-tag-only`: the moment a pin trusts a range the fail-closed
# property is gone, which is `neutral-product-pin`'s own words about a range.
VERSION_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
INTEGRITY_RE = re.compile(r"^sha512-[A-Za-z0-9+/]+={0,2}$")
SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")
PACKAGE_RE = re.compile(r"^(?:@[a-z0-9][\w.-]*/)?[a-z0-9][\w.-]*$")

# The digest kinds the pin may declare as its referent. Exactly one today; the
# tuple exists so that admitting a second is an edit to a declaration rather than
# to a condition buried in a branch.
CONTENT_ADDRESSED_KINDS: tuple[str, ...] = ("package_integrity",)


class PinRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so a
    caller can branch on the code without parsing prose, while `str(exc)` renders
    the whole thing — code, detail and the fixed remediation trailer — as the
    message a human reads. `main()` prints exactly `str(exc)`; nothing
    re-assembles the message anywhere else, so the trailer cannot be dropped by a
    caller that forgot it exists.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def __str__(self) -> str:
        return f"REFUSE {self.code}: {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# reading the pin — the exact subset this pin is written in, and nothing else
# --------------------------------------------------------------------------

_SCALAR = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*): (?P<value>.+)$")
_SEQ_STR = re.compile(r"^  - (?P<value>\S.*)$")
_SEQ_MAP_HEAD = re.compile(r"^  - (?P<key>[A-Za-z_][A-Za-z0-9_]*): (?P<value>.+)$")
_SEQ_MAP_TAIL = re.compile(r"^    (?P<key>[A-Za-z_][A-Za-z0-9_]*): (?P<value>.+)$")

# ONE nested level, and exactly one, admitted for `cited_to:`. A disposition's
# citations are a LIST because an exception rests on more than one act — a
# promoted requirement, the council item, the pull request that landed it, the
# measurement — and flattening them into one delimited string would make the
# reader guess a delimiter that a citation could itself contain. The nesting stops
# here on the same argument the flat grammar was written on: this reader parses
# the pin's own language and refuses everything else, so each level admitted is a
# deliberate widening rather than a general YAML parser arriving by accident.
_SEQ_MAP_LIST_HEAD = re.compile(r"^    (?P<key>[A-Za-z_][A-Za-z0-9_]*):$")
_SEQ_MAP_LIST_ITEM = re.compile(r"^      - (?P<value>\S.*)$")

# `>-`, the FOLDED scalar, and only that one. A disposition says in a sentence
# why an exception is lawful, and a sentence forced onto one physical line is a
# sentence nobody reviews in a diff. `>-` is the form the rest of this estate's
# YAML already writes prose in (`.openspec.yaml`'s `reason:` and `approved_by:`),
# so admitting it here keeps ONE house form rather than inventing a second.
# `|`, `|-` and `>+` are NOT admitted: their whitespace semantics differ, and a
# reader that guessed between them would be guessing at the content of a
# citation. A pin using one is `pin-unreadable`, which is the correct answer to
# a form this reader does not implement.
_FOLD_OPENER = ">-"
_FOLD_CONTINUATION = "      "


def _unquote(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_pin(pin_path: Path = PIN_PATH) -> dict:
    """The pin as a mapping, or `pin-unreadable`.

    ONE GRAMMAR, SHARED WITH THE SIBLING PIN VERIFIERS, and the sequence support
    is retained here even though this pin declares no sequence: the point of
    `neutral-product-pin` is that there is one pin shape, and a reader that
    accepted a strictly smaller language would make this pin a dialect the
    moment a member list is ever added to it.
    """
    if not pin_path.is_file():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} does not exist; openxFactory runs the "
            "OpenSpec CLI only through this pin, so its absence is not an "
            "unpinned pass but an unanswerable question")
    try:
        text = pin_path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - filesystem failure
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} could not be read: {exc}") from exc

    pin: dict = {}
    section: str | None = None
    nested: str | None = None
    folding: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            folding = None if not stripped else folding
            continue
        if folding is not None:
            if line.startswith(_FOLD_CONTINUATION):
                held = pin[section][-1][folding]
                pin[section][-1][folding] = (held + " " + stripped).strip()
                continue
            folding = None
        if not line.startswith(" "):
            section = None
            nested = None
            if stripped.endswith(":") and " " not in stripped[:-1]:
                section = stripped[:-1]
                pin[section] = []
                continue
            match = _SCALAR.match(line)
            if not match:
                raise PinRefusal(
                    "pin-unreadable",
                    f"{pin_path}:{number}: this reader parses only the pin's own "
                    f"grammar and does not understand {line!r}")
            pin[match.group("key")] = _unquote(match.group("value"))
            continue
        if section is None:
            raise PinRefusal(
                "pin-unreadable",
                f"{pin_path}:{number}: indented line outside any block: {line!r}")
        nested_item = _SEQ_MAP_LIST_ITEM.match(line)
        if nested_item:
            if nested is None or not pin[section] or not isinstance(
                    pin[section][-1], dict):
                raise PinRefusal(
                    "pin-unreadable",
                    f"{pin_path}:{number}: nested list item with no key open: "
                    f"{line!r}")
            pin[section][-1][nested].append(_unquote(nested_item.group("value")))
            continue
        head = _SEQ_MAP_HEAD.match(line)
        if head:
            nested = None
            pin[section].append({head.group("key"): _unquote(head.group("value"))})
            continue
        tail = _SEQ_MAP_TAIL.match(line)
        if tail:
            nested = None
            if not pin[section] or not isinstance(pin[section][-1], dict):
                raise PinRefusal(
                    "pin-unreadable",
                    f"{pin_path}:{number}: continuation with no mapping entry "
                    f"open: {line!r}")
            key, value = tail.group("key"), tail.group("value").strip()
            if value == _FOLD_OPENER:
                folding = key
                pin[section][-1][key] = ""
                continue
            pin[section][-1][key] = _unquote(value)
            continue
        nested_head = _SEQ_MAP_LIST_HEAD.match(line)
        if nested_head:
            if not pin[section] or not isinstance(pin[section][-1], dict):
                raise PinRefusal(
                    "pin-unreadable",
                    f"{pin_path}:{number}: nested block with no mapping entry "
                    f"open: {line!r}")
            nested = nested_head.group("key")
            pin[section][-1][nested] = []
            continue
        item = _SEQ_STR.match(line)
        if item:
            nested = None
            pin[section].append(_unquote(item.group("value")))
            continue
        raise PinRefusal(
            "pin-unreadable",
            f"{pin_path}:{number}: this reader parses only the pin's own grammar "
            f"and does not understand {line!r}")
    return pin


# --------------------------------------------------------------------------
# check 1 — the pin's shape
# --------------------------------------------------------------------------

def pinned_version(pin: dict) -> str:
    """The EXACT version label, or `pin-tag-only`.

    Evaluated FIRST, ahead of every check that compares against it, so a
    malformed pin is reported as a defect of the PIN rather than as a
    disagreement of the ENVIRONMENT — a `pin-version-mismatch` over a pin that
    records `latest` would send a reviewer to the wrong place entirely.
    """
    revision_kind = pin.get("revision_kind")
    if revision_kind not in CONTENT_ADDRESSED_KINDS:
        raise PinRefusal(
            "pin-tag-only",
            f"the pin declares revision_kind {revision_kind!r}, which is not one "
            f"of {', '.join(CONTENT_ADDRESSED_KINDS)}; the trusted referent is a "
            "content address over the published artifact, and a pin that names "
            "only a version name is trusting a registry's policy rather than the "
            "bytes")
    version = pin.get("version")
    if not isinstance(version, str) or not VERSION_RE.match(version.strip()):
        raise PinRefusal(
            "pin-tag-only",
            f"the pin records version {version!r}, which is not an exact "
            "semantic version; a range, a caret, an `x` or a dist-tag such as "
            "`latest` is a moving reference and not a compatibility pin")
    return version.strip()


def pinned_integrity(pin: dict) -> tuple[str, str]:
    """The `(integrity, shasum)` referent pair, or `pin-tag-only`.

    Both are required, and a missing or malformed one is refused as a defect of
    the PIN rather than tolerated: a version label with no content address beside
    it is exactly the unpinned state this file exists to end, and it would verify
    green against literally any bytes the registry chose to serve.
    """
    integrity = pin.get("integrity")
    if not isinstance(integrity, str) or not INTEGRITY_RE.match(integrity.strip()):
        raise PinRefusal(
            "pin-tag-only",
            f"the pin records integrity {integrity!r}, which is not a "
            "`sha512-<base64>` content address; a version with no content "
            "address beside it is a name, and a name is not the thing being "
            "trusted")
    try:
        raw = base64.b64decode(integrity.strip()[len("sha512-"):], validate=True)
    except (ValueError, TypeError) as exc:
        raise PinRefusal(
            "pin-tag-only",
            f"the pin's integrity {integrity!r} is not decodable base64: "
            f"{exc}") from exc
    if len(raw) != 64:
        raise PinRefusal(
            "pin-tag-only",
            f"the pin's integrity decodes to {len(raw)} bytes, not the 64 a "
            "SHA-512 digest occupies; a truncated address addresses nothing")
    shasum = pin.get("shasum")
    if not isinstance(shasum, str) or not SHA1_RE.match(shasum.strip()):
        raise PinRefusal(
            "pin-tag-only",
            f"the pin records shasum {shasum!r}, which is not 40 hex "
            "characters; the pin declares the registry's legacy address and "
            "this verifier checks it, so an unusable value is a defect rather "
            "than a field to skip")
    return integrity.strip(), shasum.strip().lower()


def pinned_package(pin: dict) -> str:
    raw = pin.get("package")
    if not isinstance(raw, str) or not PACKAGE_RE.match(raw.strip()):
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `package` (got {raw!r}); a pin with no "
            "product cannot be resolved against anything")
    return raw.strip()


def pinned_binary(pin: dict) -> str:
    raw = pin.get("binary")
    if not isinstance(raw, str) or not raw.strip() or "/" in raw:
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `binary` (got {raw!r}); the executable "
            "the artifact installs is asserted by name so a repointed `bin` "
            "block is a refusal rather than a silent substitution")
    return raw.strip()


def normalized_finding(text: str) -> str:
    """The finding text this tool matches on, with whitespace collapsed.

    WHAT IS MATCHED, AND WHY IT IS THE WHOLE MESSAGE. The CLI's machine-readable
    report gives three stable fields per finding: the item `id` (a change id or a
    spec id), the `path` (the capability's delta file, e.g.
    `signed-execution-chain/spec.md`), and the `message`. A disposition matches on
    ALL THREE, plus the repository, because none of the first three is unique on
    its own: one change can carry several findings against one path, and one
    message shape recurs across changes.

    The message is matched WHOLE — including the trailing remedy sentence — and
    normalized only for WHITESPACE, because whitespace is the one difference a
    line-wrapping edit to this pin file can introduce without changing what the
    tool said. Everything else in the message is a substantive part of the
    verdict: the requirement title it quotes and the scenario titles it names are
    precisely what the disposition is accepting. Matching a PREFIX, or the
    requirement title alone, would let one written exception silently absorb a
    second, different finding that the author never read.

    THIS IS ALSO HOW UPGRADE-COUPLING IS ENFORCED rather than merely promised. A
    later CLI that rewords this message produces a finding no disposition matches
    (exit 1, named) AND a disposition no finding matches (`pin-disposition-stale`,
    exit 2). Both fire, loudly, on the run that first meets the new wording, which
    is the run at which a human is re-deciding whether the exception still holds.
    """
    return " ".join(text.split())


def pinned_dispositions(pin: dict) -> list[dict]:
    """The declared exceptions, checked for shape, or `pin-disposition-malformed`.

    Evaluated as part of check 1 — with the pin's other shape rules and BEFORE
    anything is fetched — because a malformed exception is a defect of the PIN,
    and a defect of the pin must not be discovered only after a registry round
    trip and a full corpus validation have been spent reaching it.

    A MISSING `dispositions:` KEY AND AN EMPTY ONE ARE THE SAME FACT here and are
    both an empty list: the pin declares no exception. They are deliberately NOT
    kept apart the way the sequenced-after ledger keeps absence apart from `[]`,
    because there is no third reading — a pin that grants no exception grants no
    exception, however it says so.
    """
    raw = pin.get("dispositions")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise PinRefusal(
            "pin-disposition-malformed",
            f"`dispositions:` is {type(raw).__name__} and not a list of entries; "
            "an exception this reader cannot enumerate is an exception nobody "
            "can review")
    entries: list[dict] = []
    for index, entry in enumerate(raw, start=1):
        where = f"dispositions[{index}]"
        if not isinstance(entry, dict):
            raise PinRefusal(
                "pin-disposition-malformed",
                f"{where} is a bare value ({entry!r}) rather than a mapping; a "
                "disposition is a claim with a citation and an author, not a name")
        missing = [key for key in DISPOSITION_REQUIRED if not entry.get(key)]
        if missing:
            raise PinRefusal(
                "pin-disposition-malformed",
                f"{where} ({entry.get('item') or 'unnamed'}) is missing "
                f"{', '.join(missing)}. A disposition names the repository, the "
                "item, the delta path and the finding text it accepts, says WHY "
                "in one line, and CITES the canon that makes the acceptance "
                "lawful; a disposition without `cited_to:` is an uncited "
                "exception, which is the thing this estate refuses")
        citations = entry.get("cited_to")
        if not isinstance(citations, list) or not citations:
            raise PinRefusal(
                "pin-disposition-malformed",
                f"{where} ({entry.get('item')}) records `cited_to: "
                f"{citations!r}`, which is not a NON-EMPTY list. The citation is "
                "the whole difference between an accepted exception and a "
                "suppression, so an empty one is refused rather than read as "
                "'none needed'")
        if not any(entry.get(key) for key in DISPOSITION_AUTHORITY):
            raise PinRefusal(
                "pin-disposition-malformed",
                f"{where} ({entry.get('item')}) names no authority: exactly one "
                f"of {' or '.join(DISPOSITION_AUTHORITY)} is required. An "
                "exception nobody is recorded as having granted is an exception "
                "nobody granted")
        entries.append(dict(entry))
    return entries


def repository_identity(repo: Path) -> str:
    """The validated tree's repository name, or `pin-repo-unidentified`.

    READ FROM `git config --get remote.origin.url` AND NOT FROM THE DIRECTORY
    NAME, because the directory name is wrong in exactly the situation this
    estate works in: every change is authored in a `git worktree` whose directory
    is named for the branch, so a basename rule would read `openxFactory`'s own
    corpus as some repository called `oxf-bump` and quietly place every
    disposition out of scope. The remote URL survives worktrees, clones,
    relocations and renamed parent directories.

    ONLY CONSULTED WHERE DISPOSITIONS ARE DECLARED. A pin that grants no
    exception never asks this question, so a checkout with no origin — an export,
    a tarball, a vendored copy — keeps working exactly as it did before this
    mechanism existed.
    """
    result = _run(["git", "-C", str(repo), "config", "--get",
                   "remote.origin.url"])
    url = (result.stdout or "").strip()
    if result.returncode != 0 or not url:
        raise PinRefusal(
            "pin-repo-unidentified",
            f"{repo} declares no `remote.origin.url`, so this run cannot say "
            "WHICH repository's tree it is validating. The pin declares "
            "dispositions, and a disposition is scoped to one repository — "
            "applying them all would suppress findings in a tree they were never "
            "written about, and applying none would refuse this run for "
            "exceptions that are simply out of scope. Neither guess is taken")
    name = url.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    if name.endswith(".git"):
        name = name[: -len(".git")]
    if not name:
        raise PinRefusal(
            "pin-repo-unidentified",
            f"{repo}: `remote.origin.url` is {url!r}, from which no repository "
            "name can be read")
    return name


# --------------------------------------------------------------------------
# digests over the real bytes
# --------------------------------------------------------------------------

def integrity_of(payload: bytes) -> str:
    """npm's `sha512-<base64>` form, recomputed over bytes we hold."""
    return "sha512-" + base64.b64encode(hashlib.sha512(payload).digest()).decode()


def shasum_of(payload: bytes) -> str:
    return hashlib.sha1(payload).hexdigest()


def verify_artifact(tarball: Path, integrity: str, shasum: str) -> None:
    """Check 3: the artifact on disk IS the artifact the pin names.

    BOTH addresses are compared and the SHA-512 is compared FIRST, because it is
    the referent and the SHA-1 is corroboration; reporting a SHA-1 disagreement
    over bytes whose SHA-512 already disagrees would name the weaker fact.
    """
    try:
        payload = tarball.read_bytes()
    except OSError as exc:
        raise PinRefusal(
            "pin-unresolvable",
            f"the fetched artifact {tarball} could not be read: {exc}; an "
            "unverified artifact is never an implicitly trusted one") from exc
    actual_integrity = integrity_of(payload)
    if actual_integrity != integrity:
        raise PinRefusal(
            "pin-integrity-mismatch",
            f"{tarball.name}: INTEGRITY DRIFT\n"
            f"  recorded   {integrity}\n"
            f"  recomputed {actual_integrity}\n"
            "the bytes the registry served are not the bytes this repository "
            "pins; the version label matching proves nothing, because the label "
            "is not the referent")
    actual_shasum = shasum_of(payload)
    if actual_shasum != shasum:
        raise PinRefusal(
            "pin-integrity-mismatch",
            f"{tarball.name}: SHASUM DRIFT\n"
            f"  recorded   {shasum}\n"
            f"  recomputed {actual_shasum}\n"
            "the SHA-512 agreed and the registry's legacy address did not, "
            "which is a disagreement about the same bytes and is refused rather "
            "than reconciled")


# --------------------------------------------------------------------------
# resolving the CLI — the pinned artifact, or an explicitly requested PATH
# --------------------------------------------------------------------------

def _run(argv: list[str], **kwargs) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(argv, capture_output=True, text=True, check=False,
                              **kwargs)
    except (OSError, ValueError) as exc:
        raise PinRefusal(
            "pin-unresolvable",
            f"`{argv[0]}` could not be run ({exc}); the pinned artifact cannot "
            "be resolved, and an unresolved pin is not a satisfied one") from exc


def fetch_artifact(package: str, version: str, destination: Path,
                   npm: str = "npm") -> Path:
    """Download the published tarball into `destination` and return its path.

    `npm pack <package>@<version>` is used rather than a direct HTTPS GET of the
    `tarball:` URL because it goes through the SAME resolution and the same local
    cache the rest of the estate's npm use does — so the bytes checked here are
    the bytes an ordinary install would get, rather than a second, privileged
    path that could agree with the pin while everyone else's npm disagrees.
    Whatever it returns is checked against the content address regardless.
    """
    if shutil.which(npm) is None:
        raise PinRefusal(
            "pin-unresolvable",
            f"`{npm}` is not on PATH, so the pinned artifact cannot be fetched "
            "or verified. This tool refuses rather than falling back to an "
            "ambient `openspec`: an unanswerable question is never an implicit "
            "pass")
    destination.mkdir(parents=True, exist_ok=True)
    result = _run([npm, "pack", f"{package}@{version}",
                   "--pack-destination", str(destination),
                   "--no-audit", "--no-fund"])
    if result.returncode != 0:
        raise PinRefusal(
            "pin-unresolvable",
            f"`npm pack {package}@{version}` failed with exit "
            f"{result.returncode}: "
            f"{(result.stderr or result.stdout).strip() or 'no output'}")
    tarballs = sorted(destination.glob("*.tgz"))
    if len(tarballs) != 1:
        raise PinRefusal(
            "pin-unresolvable",
            f"`npm pack` left {len(tarballs)} tarball(s) in {destination}; "
            "exactly one artifact is expected, and an ambiguous fetch is not a "
            "resolved one")
    return tarballs[0]


def install_artifact(tarball: Path, prefix: Path, binary: str,
                     npm: str = "npm") -> Path:
    """Install the VERIFIED tarball into a private prefix; return the executable.

    `--ignore-scripts` is not optional. The artifact's own bytes are verified,
    but its nine dependencies are declared at caret ranges and npm resolves them
    here — so a lifecycle script belonging to an unpinned transitive dependency
    would otherwise run inside a gate. The pin's header states this shortfall in
    full rather than leaving it to be discovered; this flag mitigates it and does
    not repair it.

    `--global` with an explicit `--prefix` is what makes PATH irrelevant: the
    executable is a path this function returns, never a name a shell resolves.
    """
    prefix.mkdir(parents=True, exist_ok=True)
    result = _run([npm, "install", "--global", "--prefix", str(prefix),
                   "--ignore-scripts", "--no-audit", "--no-fund",
                   str(tarball)])
    executable = prefix / "bin" / binary
    if result.returncode != 0 or not executable.exists():
        raise PinRefusal(
            "pin-unresolvable",
            f"installing the verified artifact into {prefix} failed (exit "
            f"{result.returncode}, executable "
            f"{'present' if executable.exists() else 'absent'}): "
            f"{(result.stderr or result.stdout).strip() or 'no output'}")
    return executable


def assert_reported_version(executable: Path, version: str) -> str:
    """Check 4: the resolved binary reports the pinned version.

    Asserted in BOTH modes, and in the pinned mode it is true by construction —
    which is exactly why it is still asserted. A check that is true by
    construction today is a check that stops being asserted when the construction
    changes, and the construction here is an `npm install` whose behaviour this
    repository does not own.
    """
    result = _run([str(executable), "--version"])
    reported = (result.stdout or "").strip().splitlines()
    reported = reported[-1].strip() if reported else ""
    if result.returncode != 0 or not reported:
        raise PinRefusal(
            "pin-unresolvable",
            f"`{executable} --version` failed with exit {result.returncode}: "
            f"{(result.stderr or result.stdout).strip() or 'no output'}; a "
            "binary that cannot say what it is cannot be the pinned one")
    if reported != version:
        raise PinRefusal(
            "pin-version-mismatch",
            f"{executable} reports version {reported!r}, but the pin records "
            f"{version!r}. Strict validation and archive verdicts differ "
            "between OpenSpec versions — trees clean at the pin fail under a "
            "later CLI on pre-existing conditions — so a run at the wrong "
            "version is not a weaker check but a different one, and it is "
            "refused rather than reported")
    return reported


def path_executable(binary: str) -> Path:
    """The `openspec` on PATH, for `--path-mode` only.

    The default mode never calls this, and that is the property the whole design
    turns on: a gate that cannot read PATH cannot be made to pass or fail by what
    an engineer happens to have installed.
    """
    found = shutil.which(binary)
    if found is None:
        raise PinRefusal(
            "pin-unresolvable",
            f"--path-mode was requested and no `{binary}` is on PATH; the mode "
            "exists to check a local install, and there is none to check")
    return Path(found)


# --------------------------------------------------------------------------
# check 5 — the governed surface is actually opened
# --------------------------------------------------------------------------

def validation_targets(args: argparse.Namespace) -> list[list[str]]:
    """Check 2: the argument lists this run will pass to `validate`.

    REFUSES when there is no scan target. `neutral-product-pin`: a pinned
    validator invoked with no scan target must refuse rather than self-test,
    "because a self-test that opens no governed surface is a green check that
    verified nothing". `--strict` is appended unconditionally and no flag drops
    it: a non-strict pass is not the act this pin governs.
    """
    if args.all and args.change:
        raise PinRefusal(
            "pin-no-target",
            "--all and --change were given together; `--all` already names "
            "every item, so the pair states two different scan targets and "
            "decides neither")
    if args.all:
        return [["validate", "--all", "--strict"]]
    if args.change:
        return [["validate", name, "--strict"] for name in args.change]
    raise PinRefusal(
        "pin-no-target",
        "no scan target was given. Pass --all to validate every change and "
        "specification, or --change <id> (repeatable) for named ones. Refusing "
        "rather than self-testing, because a run that opens no governed surface "
        "is a green result that verified nothing")


def assert_governed_surface(repo: Path) -> None:
    if not (repo / "openspec").is_dir():
        raise PinRefusal(
            "pin-no-target",
            f"{repo} carries no `openspec/` directory, so there is no governed "
            "surface here to validate; pass --repo PATH naming the consuming "
            "repository's ROOT rather than a directory beside it")


def validation_environment() -> dict:
    environment = dict(os.environ)
    environment.setdefault("OPENSPEC_TELEMETRY", "0")
    return environment


def run_validation(executable: Path, repo: Path,
                   targets: list[list[str]]) -> int:
    """Invoke the pinned CLI once per target; return the WORST exit code.

    THE PATH TAKEN WHEN THE PIN DECLARES NO DISPOSITION, and it is byte-for-byte
    the behaviour that shipped with the pin: no `--json`, no parsing, the CLI's
    own exit code as the verdict. The disposition machinery is not merely inert
    for such a pin — it is not on the path at all — so a pin that grants no
    exception cannot be made to fail by a defect in a mechanism it never uses.

    Every target is run even after one fails, because the caller asked about all
    of them and stopping at the first would report a subset as though it were the
    whole answer. The verdict returned is the worst seen, so a single failure
    cannot be averaged away by later successes.

    Output is streamed to this process's own stdout/stderr rather than captured:
    the CLI's findings ARE the product of this run, and a gate log that showed
    only "validation failed" would name a fact whose remedy is in the output it
    swallowed.
    """
    assert_governed_surface(repo)
    environment = validation_environment()
    worst = 0
    for argv in targets:
        print(f"-> {executable} {' '.join(argv)}  (in {repo})", flush=True)
        try:
            completed = subprocess.run([str(executable), *argv], cwd=str(repo),
                                       env=environment, check=False)
        except OSError as exc:
            raise PinRefusal(
                "pin-unresolvable",
                f"the pinned CLI could not be executed: {exc}") from exc
        worst = max(worst, completed.returncode)
    return worst


# --------------------------------------------------------------------------
# check 5, reported — the same run, read as data so findings can be reconciled
# --------------------------------------------------------------------------

def parse_report(payload: str, argv: list[str]) -> tuple[list[dict], dict]:
    """The CLI's `--json` verdict as `(items, totals)`, or `pin-report-unreadable`.

    TWO ARRAY KEYS ARE ACCEPTED AND THE SHAPE IS OTHERWISE IDENTICAL, verified by
    running both versions rather than assumed: `1.2.0` and `1.12.0` both emit
    `{items[], summary{totals{items,passed,failed}}}` with each item carrying
    `id`, `type`, `valid` and `issues[{level, path, message}]`; `1.12.0`'s
    `--report findings` variant renames the array `itemFindings` and returns only
    items that carry findings. That the two pinned-era versions agree is what
    makes a ROLLBACK to `1.2.0` a pin edit rather than a code change.

    A LEADING BANNER IS TOLERATED, NOTHING ELSE IS. The payload is parsed whole
    first, and only on failure is the span from the first `{` to the last `}`
    retried — enough to survive a wrapper that prints a line before the document,
    and not enough to make an unparseable verdict into a soft one.
    """
    document = None
    try:
        document = json.loads(payload)
    except ValueError:
        start, end = payload.find("{"), payload.rfind("}")
        if start != -1 and end > start:
            try:
                document = json.loads(payload[start:end + 1])
            except ValueError:
                document = None
    if not isinstance(document, dict):
        excerpt = " ".join(payload.split())[:200] or "no output"
        raise PinRefusal(
            "pin-report-unreadable",
            f"`{' '.join(argv)}` produced no parseable JSON report ({excerpt}); "
            "the pin declares dispositions, and a run whose findings cannot be "
            "read cannot honour one — so this refuses rather than falling back "
            "to a streamed run that would re-fail conditions the pin settles")
    for key in ("items", "itemFindings"):
        if isinstance(document.get(key), list):
            items = document[key]
            break
    else:
        raise PinRefusal(
            "pin-report-unreadable",
            f"`{' '.join(argv)}` emitted a JSON document carrying neither "
            f"`items` nor `itemFindings` (keys: "
            f"{', '.join(sorted(map(str, document))) or 'none'}); the report "
            "shape this tool reconciles against is not the shape that arrived")
    totals = ((document.get("summary") or {}).get("totals") or {})
    if not isinstance(totals, dict):
        totals = {}
    return items, totals


def collect_findings(items: list, target: str) -> list[dict]:
    """Flatten the report into one row per finding, blocking or not.

    AN ITEM MARKED INVALID THAT CARRIES NO `ERROR` ISSUE STILL PRODUCES A
    BLOCKING ROW. The two facts are supposed to move together and in every
    measured run they do, but if they ever part this tool must report the
    failure rather than lose it: a `valid: false` with nothing to name is
    precisely the shape in which a real failure would go missing.
    """
    findings: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("id") or "")
        issues = item.get("issues") or []
        levels = set()
        for issue in issues:
            if not isinstance(issue, dict):
                continue
            level = str(issue.get("level") or "").upper()
            levels.add(level)
            findings.append({
                "target": target,
                "item": identifier,
                "type": str(item.get("type") or ""),
                "level": level,
                "path": str(issue.get("path") or ""),
                "message": str(issue.get("message") or ""),
                "normalized": normalized_finding(str(issue.get("message") or "")),
                "blocking": level in BLOCKING_LEVELS,
            })
        if item.get("valid") is False and not (levels & BLOCKING_LEVELS):
            message = (f"{identifier}: the report marks this item INVALID and "
                       "names no ERROR-level issue for it")
            findings.append({
                "target": target,
                "item": identifier,
                "type": str(item.get("type") or ""),
                "level": "ERROR",
                "path": "",
                "message": message,
                "normalized": normalized_finding(message),
                "blocking": True,
            })
    return findings


def run_reported_validation(executable: Path, repo: Path,
                            targets: list[list[str]]
                            ) -> tuple[int, list[dict], dict]:
    """Run every target with `--json`, and return `(worst exit, findings, totals)`.

    `--json` REPLACES THE STREAM, AND THE FINDINGS ARE RE-RENDERED FROM IT rather
    than dropped: `render_findings` prints every row this returns, in the CLI's
    own `LEVEL path: message` shape, so the log a reader gets is the same log —
    the difference is that this run also HOLDS the findings and can say which of
    them the pin has already accepted. Running the CLI twice, once streamed and
    once as JSON, was the alternative; it doubles a minute-long corpus validation
    to preserve bytes this function reproduces.
    """
    assert_governed_surface(repo)
    environment = validation_environment()
    worst = 0
    findings: list[dict] = []
    totals = {"items": 0, "passed": 0, "failed": 0}
    for argv in targets:
        reported = [*argv, "--json"]
        print(f"-> {executable} {' '.join(reported)}  (in {repo})", flush=True)
        try:
            completed = subprocess.run([str(executable), *reported],
                                       cwd=str(repo), env=environment,
                                       capture_output=True, text=True,
                                       check=False)
        except OSError as exc:
            raise PinRefusal(
                "pin-unresolvable",
                f"the pinned CLI could not be executed: {exc}") from exc
        if completed.stderr:
            print(completed.stderr.rstrip(), file=sys.stderr, flush=True)
        items, target_totals = parse_report(completed.stdout or "", reported)
        findings.extend(collect_findings(items, " ".join(argv)))
        for key in totals:
            value = target_totals.get(key)
            totals[key] += value if isinstance(value, int) else 0
        worst = max(worst, completed.returncode)
    blocking = [row for row in findings if row["blocking"]]
    if worst != 0 and not blocking:
        raise PinRefusal(
            "pin-report-unreadable",
            f"the pinned CLI exited {worst} and its JSON report names no "
            "ERROR-level finding. The verdict and the report disagree, and this "
            "tool reconciles dispositions against the REPORT — so a failure the "
            "report does not carry would be silently dispositioned away")
    return worst, findings, totals


def render_findings(findings: list[dict]) -> None:
    """Print the CLI's findings, grouped by item, in the CLI's own vocabulary."""
    glyph = {"ERROR": "\u2717", "WARNING": "\u26a0"}
    current = None
    for row in sorted(findings, key=lambda r: (r["item"], r["level"], r["path"])):
        if row["item"] != current:
            current = row["item"]
            print(f"{row['type'] or 'item'}/{current}", flush=True)
        mark = glyph.get(row["level"], "\u2139")
        location = f"{row['path']}: " if row["path"] else ""
        print(f"  {mark} [{row['level']}] {location}{row['message']}", flush=True)


# --------------------------------------------------------------------------
# check 6 — findings against declared dispositions, in both directions
# --------------------------------------------------------------------------

def reconcile(findings: list[dict], dispositions: list[dict],
              identity: str) -> tuple[list[tuple[dict, dict]], list[dict],
                                      list[dict]]:
    """Match blocking findings to in-scope dispositions, BOTH WAYS.

    Returns `(applied, undispositioned, stale)`:

      applied          `(disposition, finding)` pairs — an accepted exception
                       whose condition still occurs
      undispositioned  blocking findings no disposition covers — exit 1, theirs
                       to fix or to disposition
      stale            in-scope dispositions no finding matches — exit 2, ours to
                       remove from the pin

    OUT-OF-SCOPE DISPOSITIONS ARE IN NEITHER LIST. A disposition naming another
    repository is not applied here and is not stale here: it is simply not about
    this tree. That is the whole reason `repo:` is a match key — see
    `repository_identity`.

    EXACTLY ONE DISPOSITION MAY COVER A FINDING. Two entries matching the same
    finding would each look satisfied while only one of them was doing any work,
    and the redundant one would then never go stale — a permanent, invisible
    suppression sitting behind a live one. So a duplicate is refused as a
    malformed pin rather than tolerated as harmless.
    """
    in_scope = [entry for entry in dispositions if entry.get("repo") == identity]
    keyed: dict[tuple[str, str, str], dict] = {}
    for entry in in_scope:
        key = (str(entry["item"]), str(entry["path"]),
               normalized_finding(str(entry["finding"])))
        if key in keyed:
            raise PinRefusal(
                "pin-disposition-malformed",
                f"two dispositions in {identity} name the same finding "
                f"({key[0]} / {key[1]}); exactly one exception may cover a "
                "finding, or the redundant one is a suppression that can never "
                "go stale")
        keyed[key] = entry

    applied: list[tuple[dict, dict]] = []
    undispositioned: list[dict] = []
    matched: set[tuple[str, str, str]] = set()
    for row in findings:
        if not row["blocking"]:
            continue
        key = (row["item"], row["path"], row["normalized"])
        entry = keyed.get(key)
        if entry is None:
            undispositioned.append(row)
            continue
        matched.add(key)
        applied.append((entry, row))
    stale = [entry for key, entry in keyed.items() if key not in matched]
    return applied, undispositioned, stale


def report_dispositions(identity: str, applied: list[tuple[dict, dict]],
                        stale: list[dict]) -> None:
    """Print every applied exception BY NAME, before any verdict is announced.

    THIS IS NOT DECORATION AND IT IS NOT OPTIONAL. A run that suppresses two
    ERROR-level findings and then prints `OK` has told its reader something
    false by omission: the tree is not clean, it is clean-except-for-two-things
    somebody decided in advance were acceptable. The whole legitimacy of a
    disposition rests on it being READ — so the exception, its one-line reason,
    its citations and the human who granted it are printed on every run, in the
    log a reviewer already looks at, whether or not anybody asks.
    """
    if not applied:
        # A run whose only disposition news is a STALE entry says nothing here:
        # the refusal that follows names every orphan, and a header reading
        # "0 applied" over an empty list would be noise standing where a finding
        # ought to be.
        return
    print(f"openspec-cli-pin: DISPOSITIONED FINDINGS in {identity} "
          f"({len(applied)} applied) — this run is NOT a clean tree:",
          flush=True)
    for entry, row in applied:
        authority = entry.get("ratified_by") or entry.get("recorded_by") or ""
        print(f"  ✗→D {row['item']} / {row['path']}", flush=True)
        print(f"        {row['message']}", flush=True)
        print(f"        why: {entry.get('why')}", flush=True)
        print(f"        cited to: {'; '.join(entry.get('cited_to') or [])}",
              flush=True)
        print(f"        accepted by: {authority}", flush=True)


# --------------------------------------------------------------------------
# resolution, with a cache keyed by the CONTENT ADDRESS
# --------------------------------------------------------------------------

def default_cache_root() -> Path:
    declared = os.environ.get("OPENSPEC_CLI_PIN_CACHE")
    if declared:
        return Path(declared)
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "openxfactory" / "openspec-cli-pin"


def resolve_pinned(package: str, version: str, integrity: str, shasum: str,
                   binary: str, workspace: Path, cache_root: Path | None,
                   npm: str = "npm") -> Path:
    """Fetch, VERIFY, install (or reuse) and return the pinned executable.

    THE TARBALL IS RE-VERIFIED ON EVERY RUN, cache or no cache. Only the INSTALL
    is reused, and only from a directory NAMED BY the verified content address
    and stamped with it. That split is deliberate: the fetch is cheap (npm serves
    a 200 KB artifact from its own local cache) while the install is not, so
    there is no reason to buy speed by trusting a previous run's verdict about
    bytes. The stamp is then a statement about which artifact this directory was
    built from, checked before the directory is used, rather than a substitute
    for checking the artifact.
    """
    tarball = fetch_artifact(package, version, workspace / "fetch", npm=npm)
    verify_artifact(tarball, integrity, shasum)

    if cache_root is None:
        return install_artifact(tarball, workspace / "prefix", binary, npm=npm)

    prefix = cache_root / f"{package.replace('/', '__')}-{version}-{shasum}"
    stamp = prefix / ".pin-verified"
    executable = prefix / "bin" / binary
    if executable.exists() and stamp.is_file():
        try:
            if stamp.read_text(encoding="utf-8").strip() == integrity:
                return executable
        except OSError:
            pass
    if prefix.exists():
        shutil.rmtree(prefix, ignore_errors=True)
    executable = install_artifact(tarball, prefix, binary, npm=npm)
    try:
        stamp.write_text(integrity + "\n", encoding="utf-8")
    except OSError:
        # A cache that cannot be stamped is a cache that will be rebuilt next
        # run. That costs time and nothing else, so it is never a reason to
        # refuse a run whose artifact verified.
        pass
    return executable


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate-openspec-cli-pin.py",
        description=("Run `openspec validate … --strict` through the CLI pinned "
                     "by contracts/openspec-cli-pin.yaml, verifying the "
                     "artifact's content address before it is invoked."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--all", action="store_true",
        help="validate every change and specification (`validate --all --strict`)")
    parser.add_argument(
        "--change", metavar="ID", action="append", default=[],
        help="validate one change by id (repeatable)")
    parser.add_argument(
        "--strict", action="store_true",
        help=("accepted and IGNORED: strict is always on. The flag exists so "
              "the habitual `--all --strict` reaches this entrypoint unchanged, "
              "and there is deliberately no `--no-strict` — a non-strict pass "
              "is not the act this pin governs"))
    parser.add_argument(
        "--repo", metavar="PATH", default=None,
        help=("the consuming repository ROOT whose `openspec/` is validated "
              "(default: this repository)"))
    parser.add_argument(
        "--path-mode", action="store_true",
        help=("use the `openspec` on PATH, refusing unless it reports the "
              "pinned version; never for a required check"))
    parser.add_argument(
        "--tarball", metavar="PATH", default=None,
        help=("verify and install this already-downloaded artifact instead of "
              "fetching it; the content address is checked either way"))
    parser.add_argument(
        "--no-cache", action="store_true",
        help="install into a temporary prefix discarded when the run ends")
    parser.add_argument(
        "--cache-dir", metavar="PATH", default=None,
        help="where verified installs are reused from")
    parser.add_argument(
        "--npm", metavar="BIN", default="npm",
        help="the npm executable to fetch and install with (tests)")
    parser.add_argument(
        "--pin", metavar="PATH", default=None,
        help="an alternative pin file (tests)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Return 0 on a clean run, 1 on validation failures, 2 on any refusal.

    The ORDER of the block below is the ordering the module docstring states, and
    it is load-bearing: the pin's shape and the presence of a scan target are
    both settled before anything is fetched, so a target-less invocation cannot
    spend a registry round trip on its way to refusing.
    """
    args = build_parser().parse_args(argv)

    try:
        pin = read_pin(Path(args.pin) if args.pin else PIN_PATH)
        version = pinned_version(pin)                       # check 1
        integrity, shasum = pinned_integrity(pin)
        package = pinned_package(pin)
        binary = pinned_binary(pin)
        dispositions = pinned_dispositions(pin)
        targets = validation_targets(args)                  # check 2
        repo = Path(args.repo).resolve() if args.repo else ROOT
        # Asked BEFORE anything is fetched, for the same reason the shape checks
        # are: a pin whose exceptions cannot be scoped is unusable, and learning
        # that only after a registry round trip and a full corpus validation
        # tells a reviewer nothing the question had already told them.
        identity = repository_identity(repo) if dispositions else ""

        with tempfile.TemporaryDirectory(prefix="openspec-cli-pin-") as scratch:
            workspace = Path(scratch)
            if args.path_mode:
                # No fetch: the mode's whole subject is the LOCAL install, and
                # downloading the artifact in order to check a binary we are
                # about to run from PATH anyway would verify bytes nobody runs.
                executable = path_executable(binary)
            elif args.tarball is not None:
                supplied = Path(args.tarball)
                verify_artifact(supplied, integrity, shasum)   # check 3
                executable = install_artifact(supplied, workspace / "prefix",
                                              binary, npm=args.npm)
            else:
                cache_root = None if args.no_cache else (
                    Path(args.cache_dir) if args.cache_dir
                    else default_cache_root())
                executable = resolve_pinned(                   # check 3
                    package, version, integrity, shasum, binary, workspace,
                    cache_root, npm=args.npm)
            reported = assert_reported_version(executable, version)  # check 4
            mode = "PATH" if args.path_mode else "pinned artifact"
            print(f"openspec-cli-pin: {package}@{reported} from {mode} "
                  f"({executable}); integrity {integrity[:23]}… verified",
                  flush=True)
            if not dispositions:
                verdict = run_validation(executable, repo, targets)   # check 5
                applied, undispositioned, stale = [], [], []
            else:
                verdict, findings, totals = run_reported_validation(  # check 5
                    executable, repo, targets)
                render_findings(findings)
                print(f"Totals: {totals.get('passed', 0)} passed, "
                      f"{totals.get('failed', 0)} failed "
                      f"({totals.get('items', 0)} items)", flush=True)
                applied, undispositioned, stale = reconcile(          # check 6
                    findings, dispositions, identity)
                report_dispositions(identity, applied, stale)
                if stale:
                    raise PinRefusal(
                        "pin-disposition-stale",
                        "the pin disposes findings this run did not produce:\n"
                        + "\n".join(
                            f"  • {entry['item']} / {entry['path']} "
                            f"(repo {entry['repo']})" for entry in stale)
                        + "\n\nThe condition each was granted for no longer "
                        "occurs — typically because the change archived out of "
                        "the `--all` corpus, or because the pinned CLI now words "
                        "the finding differently. A suppression that outlives "
                        "its condition is a standing exemption nobody re-read, "
                        "so it is REFUSED rather than tolerated: delete the "
                        "entry from `dispositions:` in "
                        "contracts/openspec-cli-pin.yaml, in a change that says "
                        "the condition is gone")
                # THE VERDICT IS DERIVED FROM THE RECONCILED FINDINGS AND NOT
                # FROM THE CLI'S EXIT CODE, which is the whole mechanism: the
                # tool exits non-zero over findings this pin has accepted in
                # writing, and a pass here is a statement about UNDISPOSITIONED
                # failures rather than an agreement with that exit code.
                verdict = 1 if undispositioned else 0
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if verdict != 0:
        if not undispositioned:
            # The disposition-free path, whose message is the one that shipped
            # with the pin: nothing was reconciled, so nothing may be implied
            # about what was or was not dispositioned.
            print(f"openspec-cli-pin: the pinned CLI reported failures (exit "
                  f"{verdict}). The PIN held — this is a finding about the "
                  f"deltas, not about which tool ran.", file=sys.stderr)
            return 1
        detail = ""
        if undispositioned:
            detail = ("\n" + "\n".join(
                f"  ✗ {row['item']} / {row['path']}: {row['message']}"
                for row in undispositioned)
                + "\n  Remedy for each: FIX IT, or DISPOSITION IT in "
                  "contracts/openspec-cli-pin.yaml with a canon citation "
                  "(`cited_to:`, non-empty) and an authority (`ratified_by:`). "
                  "An undispositioned ERROR is not a tolerated one, and a "
                  "disposition with no citation is refused rather than read as "
                  "'none needed'.")
        count = len(undispositioned)
        print(f"openspec-cli-pin: the pinned CLI reported {count} failure(s) "
              f"this pin does not disposition. The PIN held — this is a "
              f"finding about the deltas, not about which tool "
              f"ran.{detail}", file=sys.stderr)
        return 1
    if applied:
        print(f"OK openspec-cli-pin: {package}@{version} verified against its "
              f"content address; every target validated --strict with 0 "
              f"UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: "
              f"{len(applied)} finding(s) are ACCEPTED EXCEPTIONS, named above.")
        return 0
    print(f"OK openspec-cli-pin: {package}@{version} verified against its "
          f"content address and every target validated --strict clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
