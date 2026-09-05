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

FIVE CHECKS, ORDERED, FIRST FAILURE WINS.

  1. the pin's SHAPE — `revision_kind: package_integrity`, an EXACT version (no
     range, no caret, no dist-tag), a well-formed `sha512-` integrity and a
     40-hex `shasum`
  2. a SCAN TARGET was given — `--all`, or at least one change id
  3. the fetched artifact's recomputed SHA-512 and SHA-1 EQUAL the pin
  4. the resolved binary REPORTS the pinned version
  5. `openspec validate <target> --strict` runs, and its verdict is this tool's

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
  0  the pin is satisfied AND the pinned CLI reported no validation failures
  1  the pin is satisfied, the pinned CLI RAN, and it reported failures
  2  ANY refusal, and any environment failure

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
)

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
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" "):
            section = None
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
        head = _SEQ_MAP_HEAD.match(line)
        if head:
            pin[section].append({head.group("key"): _unquote(head.group("value"))})
            continue
        tail = _SEQ_MAP_TAIL.match(line)
        if tail:
            if not pin[section] or not isinstance(pin[section][-1], dict):
                raise PinRefusal(
                    "pin-unreadable",
                    f"{pin_path}:{number}: continuation with no mapping entry "
                    f"open: {line!r}")
            pin[section][-1][tail.group("key")] = _unquote(tail.group("value"))
            continue
        item = _SEQ_STR.match(line)
        if item:
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


def run_validation(executable: Path, repo: Path,
                   targets: list[list[str]]) -> int:
    """Invoke the pinned CLI once per target; return the WORST exit code.

    Every target is run even after one fails, because the caller asked about all
    of them and stopping at the first would report a subset as though it were the
    whole answer. The verdict returned is the worst seen, so a single failure
    cannot be averaged away by later successes.

    Output is streamed to this process's own stdout/stderr rather than captured:
    the CLI's findings ARE the product of this run, and a gate log that showed
    only "validation failed" would name a fact whose remedy is in the output it
    swallowed.
    """
    if not (repo / "openspec").is_dir():
        raise PinRefusal(
            "pin-no-target",
            f"{repo} carries no `openspec/` directory, so there is no governed "
            "surface here to validate; pass --repo PATH naming the consuming "
            "repository's ROOT rather than a directory beside it")
    environment = dict(os.environ)
    environment.setdefault("OPENSPEC_TELEMETRY", "0")
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
        targets = validation_targets(args)                  # check 2
        repo = Path(args.repo).resolve() if args.repo else ROOT

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
            verdict = run_validation(executable, repo, targets)       # check 5
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if verdict != 0:
        print(f"openspec-cli-pin: the pinned CLI reported failures (exit "
              f"{verdict}). The PIN held — this is a finding about the deltas, "
              f"not about which tool ran.", file=sys.stderr)
        return 1
    print(f"OK openspec-cli-pin: {package}@{version} verified against its "
          f"content address and every target validated --strict clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
