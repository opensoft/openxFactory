#!/usr/bin/env python3
"""Verify openxFactory's CONSUMPTION of opensoft/openRepoShape against its pin.

openxFactory RATIFIES the project repository schema's doctrine
(`docs/project-repo-schema.md`) and CONSUMES its mechanics at a commit and a set
of digests. `contracts/openreposhape-pin.yaml` is the whole of that claim and
this file is the running code that checks it. Everything the pin asserts is
checked here, and nothing that is not asserted is inferred.

THE TRUSTED REFERENT IS `commit` PLUS THE DIGESTED MEMBERS' `sha256`s. A pin
that declares `revision_kind` anything other than `commit`, or a `commit` that
is not exactly 40 hex, is refused `pin-tag-only` rather than being resolved — a
movable name is not a compatibility pin, and resolving one is a network read
made to look like a check.

THERE IS NO GITLINK HERE, AND ITS ABSENCE IS THE DESIGN. The sibling
`scripts/verify-openxwallet-pin.py` compares a RECORDED gitlink and a CHECKED-OUT
revision because openxFactory MOUNTS openXwallet as a submodule and runs the
pinned reader out of that checkout. openxFactory does not mount openRepoShape: it
cites the standard, and the standard runs in the projects that fork it. So this
tool has no tree of its own to read and must be TOLD where the bytes are — a
local checkout (`--checkout`) or the host API (`--from-gh`). Given neither, it
REFUSES `pin-unresolvable` rather than passing: an unanswerable question is never
an implicit pass, which is `neutral-product-pin`'s rule and not a local
preference.

FIVE CHECKS, ORDERED, FIRST FAILURE WINS.

  1. the pin's SHAPE — `revision_kind: commit`, 40 hex, non-empty `files:`
  2. the resolved source is AT `commit` (a checkout is asked `rev-parse HEAD`;
     the host API is asked for the tree OF that commit, so the question cannot
     be answered by the wrong revision)
  3. every digested member RECOMPUTES to its recorded sha256
  4. every `pinned_by_commit_only:` member is PRESENT
  5. SURFACE COMPLETENESS — every file at the pinned commit appears in exactly
     one of the two lists

Check 5 is the one the sibling does not have, and it exists because
`neutral-product-pin`'s own scenario says an artifact appearing in neither list
"is an undeclared consumption, not a permitted omission". Without it a pin could
name half a product and verify green.

STANDARD LIBRARY ONLY, and deliberately so. The pin's grammar is a fixed, small
subset this repository authors, so `_read_pin` parses exactly that subset and
REFUSES anything outside it rather than guessing. PyYAML would have been the
easier road and is what the sibling takes; it is declined here because the
standard this tool checks insists on running where nothing can be installed, and
a verifier that needed a package to check a package-free standard would be
carrying an assumption the standard exists to refuse. The narrowness is
fail-closed: an unparseable line is `pin-unreadable`, never a skipped rule.

Exit codes:
  0  the pin is satisfied
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1. The gate's only question is "may this pull
  request proceed", and the answer is identical for "the pin is stale" and "the
  bytes could not be resolved". A two-valued failure invites a workflow that
  treats one of them as a warning.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "openreposhape-pin.yaml"

# The ONE fixed remediation trailer for every fail-closed refusal (the form
# `neutral-product-pin` requires: a refusal that names what is wrong without
# naming what to run puts the exit in tribal memory instead of in the message).
REMEDIATION = (
    "Remediation: resolve the standard's bytes and re-run, e.g. "
    "`git clone https://github.com/opensoft/openRepoShape /tmp/ors && "
    "git -C /tmp/ors checkout <commit> && "
    "python3 scripts/validate-openreposhape-pin.py --checkout /tmp/ors`, or "
    "`python3 scripts/validate-openreposhape-pin.py --from-gh` where the GitHub "
    "API is reachable. If the PIN is stale rather than the tree, re-cut "
    "contracts/openreposhape-pin.yaml at the new commit — recompute every "
    "sha256 from the real bytes, never edit a digest to make this pass — and "
    "record why in the change that moves it."
)

# The refusal vocabulary, fixed. Other code may branch on the CODE, so no
# failure path here may invent one.
#
# `pin-unreadable` is NOT in the vocabulary and its absence is the point, on the
# sibling's reasoning: the five describe a SOURCE that disagrees with a
# well-formed pin, each a finding a reviewer can act on. `pin-unreadable`
# describes an environment in which no finding can be reached at all. It still
# exits 2 — excluded from the vocabulary, not from fail-closure.
REFUSAL_CODES: tuple[str, ...] = (
    "pin-tag-only",
    "pin-unresolvable",
    "pin-revision-mismatch",
    "pin-digest-mismatch",
    "pin-member-missing",
    "pin-surface-undeclared",
)

# Exactly 40 / 64 hex, case-insensitive, normalized to lowercase before any
# comparison. The shape stays strict — 40 means 40, so an abbreviated oid or a
# branch name cannot pass — but case is normalized rather than rejected: git
# emits lowercase, so an uppercase value in the pin is a hand-edit rather than a
# movable reference, and refusing it as `pin-tag-only` would name the wrong
# defect.
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

API = "https://api.github.com"


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

    Parses ONLY the grammar this pin is written in — top-level `key: value`
    scalars, a `files:` sequence of two-key mappings, and a
    `pinned_by_commit_only:` sequence of strings — plus comments and blank lines.
    ANY other construction is `pin-unreadable` with the offending line quoted,
    which is the fail-closed reading of a narrow parser: a line this reader does
    not understand must stop the run rather than be skipped, because a skipped
    line is a rule that silently did not apply.
    """
    if not pin_path.is_file():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin file {pin_path} does not exist; openxFactory consumes "
            "openRepoShape only through this pin, so its absence is not an "
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


def pinned_commit(pin: dict) -> str:
    """The 40-hex referent, lowercased, or `pin-tag-only`.

    Evaluated FIRST, ahead of every check that compares against it, so a
    malformed pin is reported as a defect of the PIN rather than as a
    disagreement of the SOURCE — a `pin-revision-mismatch` over a pin that
    records a branch name would send a reviewer to the wrong repository.
    """
    revision_kind = pin.get("revision_kind")
    if revision_kind != "commit":
        raise PinRefusal(
            "pin-tag-only",
            f"the pin declares revision_kind {revision_kind!r}, not 'commit'; "
            "the trusted referent is a commit plus digests, and resolving a "
            "movable name would require exactly the network read this verifier "
            "refuses to perform")
    commit = pin.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit.strip()):
        raise PinRefusal(
            "pin-tag-only",
            f"the pin records commit {commit!r}, which is not exactly 40 hex "
            "characters; an abbreviated oid, a branch or a tag is not a "
            "compatibility pin")
    return commit.strip().lower()


def _source_repository(pin: dict) -> str:
    raw = pin.get("source_repository")
    if not isinstance(raw, str) or raw.count("/") != 1 or not raw.strip():
        raise PinRefusal(
            "pin-unreadable",
            f"the pin declares no usable `source_repository` (got {raw!r}); a "
            "pin with no product cannot be resolved against anything")
    return raw.strip()


# --------------------------------------------------------------------------
# resolving the bytes — a checkout, or the host API
# --------------------------------------------------------------------------

class Source:
    """Where the standard's bytes come from, and what revision they are.

    Two implementations, one interface, so the five checks below are written
    once. `paths()` is what makes check 5 possible: a resolver that could list
    only the files the pin already names could never report an undeclared one.
    """

    def revision(self) -> str: ...
    def paths(self) -> set[str]: ...
    def read(self, path: str) -> bytes | None: ...
    def describe(self) -> str: ...


class CheckoutSource(Source):
    """A local clone. The revision is `git rev-parse HEAD`, so a checkout sitting
    at the wrong commit is check 2's finding rather than a pile of digest
    mismatches."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        if not (self.root / ".git").exists():
            raise PinRefusal(
                "pin-unresolvable",
                f"{self.root} is not a git checkout (no .git); the verifier "
                "compares the pin against a REVISION, and a bare directory of "
                "files carries none")

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args],
                              capture_output=True, text=True, check=False)

    def revision(self) -> str:
        head = self._git("rev-parse", "HEAD")
        if head.returncode != 0:
            raise PinRefusal(
                "pin-unresolvable",
                f"`git -C {self.root} rev-parse HEAD` failed, so the checkout's "
                "revision cannot be compared against the pin: "
                f"{head.stderr.strip() or 'no error output'}")
        return head.stdout.strip().lower()

    def paths(self) -> set[str]:
        listing = self._git("ls-tree", "-r", "--name-only", "HEAD")
        if listing.returncode != 0:
            raise PinRefusal(
                "pin-unresolvable",
                f"`git -C {self.root} ls-tree` failed, so the pinned surface "
                "cannot be enumerated and completeness cannot be asserted: "
                f"{listing.stderr.strip() or 'no error output'}")
        return {line.strip() for line in listing.stdout.splitlines() if line.strip()}

    def read(self, path: str) -> bytes | None:
        target = self.root / path
        # Presence is asked of the WORKING TREE, deliberately: a member deleted
        # after checkout is exactly what the commit does not catch, and is what
        # check 4 exists for.
        return target.read_bytes() if target.is_file() else None

    def describe(self) -> str:
        return f"checkout {self.root}"


class GhSource(Source):
    """The host API, read AT the pinned commit.

    The tree is fetched for the COMMIT the pin names rather than for a branch, so
    check 2 is satisfied by construction — there is no revision this resolver
    could return that is not the pinned one. It is asserted anyway, because a
    check that is true by construction today is a check that stops being asserted
    when the construction changes.
    """

    def __init__(self, repository: str, commit: str, token: str | None) -> None:
        self.repository = repository
        self.commit = commit
        self.token = token
        self._tree: dict[str, str] | None = None

    def _get(self, url: str) -> dict:
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("User-Agent", "openxfactory-openreposhape-pin")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raise PinRefusal(
                "pin-unresolvable",
                f"the host API could not be read at {url}: {exc}; the pin's "
                "bytes were not resolved, and an unresolved pin is not a "
                "satisfied one") from exc

    def _load(self) -> dict[str, str]:
        if self._tree is None:
            payload = self._get(
                f"{API}/repos/{self.repository}/git/trees/{self.commit}"
                "?recursive=1")
            if payload.get("truncated"):
                raise PinRefusal(
                    "pin-unresolvable",
                    "the host API truncated the recursive tree listing, so the "
                    "pinned surface cannot be enumerated and completeness "
                    "cannot be asserted; re-run with --checkout")
            self._tree = {
                entry["path"]: entry["sha"]
                for entry in payload.get("tree") or []
                if entry.get("type") == "blob"
            }
        return self._tree

    def revision(self) -> str:
        # The tree is fetched FOR this commit; asking the API to confirm its own
        # operand would prove nothing the request did not already fix.
        self._load()
        return self.commit

    def paths(self) -> set[str]:
        return set(self._load())

    def read(self, path: str) -> bytes | None:
        blob_sha = self._load().get(path)
        if blob_sha is None:
            return None
        payload = self._get(f"{API}/repos/{self.repository}/git/blobs/{blob_sha}")
        if payload.get("encoding") != "base64":
            raise PinRefusal(
                "pin-unresolvable",
                f"the host API returned {path} with encoding "
                f"{payload.get('encoding')!r}, which this verifier does not "
                "decode; re-run with --checkout")
        return base64.b64decode(payload.get("content") or "")

    def describe(self) -> str:
        return f"{self.repository}@{self.commit[:12]} via the host API"


# --------------------------------------------------------------------------
# the five checks
# --------------------------------------------------------------------------

def verify(source: Source, pin: dict) -> dict:
    """Run the five ordered checks against `source`; return a summary on success.

    Raises `PinRefusal` on the FIRST failure and never continues past it. The
    checks are ORDERED because each later one is only meaningful once the earlier
    ones hold: a digest recomputed against the WRONG revision reports drift when
    the actual defect is that the wrong bytes were resolved. First failure, named
    correctly, beats a pile of failures that need triage.

    Prints nothing and exits nothing: it raises, and the caller decides.
    """
    commit = pinned_commit(pin)

    # ---- check 2: the resolved source IS the pinned revision ----------------
    revision = source.revision()
    if revision != commit:
        raise PinRefusal(
            "pin-revision-mismatch",
            f"{source.describe()} is at {revision}, but the pin records "
            f"{commit}; the digests below are recomputed against the resolved "
            "bytes, so comparing them now would report content drift when the "
            "real defect is that the wrong revision was resolved")

    # ---- check 3: every digested member recomputes --------------------------
    entries = pin.get("files")
    if not isinstance(entries, list) or not entries:
        raise PinRefusal(
            "pin-unreadable",
            "the pin lists no `files:` members, so it pins no bytes; an empty "
            "claim is not a satisfied claim")
    digested: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise PinRefusal(
                "pin-unreadable",
                f"the pin's files[{index}] is malformed ({entry!r}); every "
                "member must declare a `path`")
        rel = entry["path"]
        digested.add(rel)
        recorded = entry.get("sha256")
        if not isinstance(recorded, str) or not SHA256_RE.match(recorded.strip()):
            # A recomputed digest can never equal an absent or malformed
            # recorded one, so this is DRIFT and not a shape complaint: the
            # member is unverifiable, which is the same operational fact as a
            # member that verified wrongly.
            raise PinRefusal(
                "pin-digest-mismatch",
                f"{rel}: the pin records sha256 {recorded!r}, which is not 64 "
                "hex characters; a recomputed digest can never equal a digest "
                "that is not one")
        content = source.read(rel)
        if content is None:
            raise PinRefusal(
                "pin-member-missing",
                f"{rel} is MISSING from {source.describe()}, but the pin records "
                f"a sha256 for it; openRepoShape@{commit[:12]} is expected to "
                "carry every digested member")
        actual = hashlib.sha256(content).hexdigest()
        if actual != recorded.strip().lower():
            raise PinRefusal(
                "pin-digest-mismatch",
                f"{rel}: DIGEST DRIFT\n"
                f"  recorded   {recorded.strip().lower()}\n"
                f"  recomputed {actual}\n"
                f"the bytes at {source.describe()} are not the bytes the pin "
                f"consumes at openRepoShape@{commit[:12]}")

    # ---- check 4: every path-only member is PRESENT -------------------------
    # Presence only, and that is not the weaker check it looks. Identity comes
    # from check 2: the resolved revision is already pinned to `commit`, so a
    # swap of any of these files is a swap of the commit. What the commit does
    # NOT catch is a member deleted from a WORKING TREE after checkout, which is
    # what this check is for.
    path_only = pin.get("pinned_by_commit_only") or []
    if not isinstance(path_only, list):
        raise PinRefusal(
            "pin-unreadable",
            f"the pin's `pinned_by_commit_only` is not a list ({path_only!r})")
    declared = set(digested)
    for entry in path_only:
        if not isinstance(entry, str) or not entry.strip():
            raise PinRefusal(
                "pin-unreadable",
                f"the pin's `pinned_by_commit_only` holds a non-path entry "
                f"({entry!r})")
        rel = entry.strip()
        if rel in declared:
            raise PinRefusal(
                "pin-unreadable",
                f"{rel} appears in BOTH `files:` and `pinned_by_commit_only:`; "
                "a member is digested or it is content-addressed by commit, and "
                "a pin that says both says neither")
        declared.add(rel)
        if source.read(rel) is None:
            raise PinRefusal(
                "pin-member-missing",
                f"{rel} is MISSING from {source.describe()}; the pin declares it "
                f"content-addressed by openRepoShape@{commit[:12]}, and a member "
                "absent from the resolved source is not content-addressed by "
                "anything")

    # ---- check 5: the declared surface is COMPLETE --------------------------
    # `neutral-product-pin`: an artifact in neither list "is an undeclared
    # consumption, not a permitted omission". Without this check a pin could name
    # half a product and verify green, which is the one failure mode per-file
    # digests cannot see — they say nothing about a file nobody listed.
    present = source.paths()
    undeclared = sorted(present - declared)
    if undeclared:
        raise PinRefusal(
            "pin-surface-undeclared",
            f"openRepoShape@{commit[:12]} carries {len(undeclared)} file(s) the "
            "pin names in NEITHER `files:` nor `pinned_by_commit_only:`: "
            + ", ".join(undeclared[:10])
            + (" …" if len(undeclared) > 10 else "")
            + " — an artifact in neither list is an undeclared consumption, not "
              "a permitted omission")
    absent = sorted(declared - present)
    if absent:
        # Reachable only where a resolver reports a path it cannot read, or
        # vice versa; named rather than left to fall through, because a
        # declared-but-absent member is the same operational fact as a missing
        # one and must not be reported under a code about UNDECLARED files.
        raise PinRefusal(
            "pin-member-missing",
            f"the pin declares {len(absent)} member(s) that "
            f"openRepoShape@{commit[:12]} does not carry: " + ", ".join(absent))

    return {
        "commit": commit,
        "source": source.describe(),
        "digested": len(digested),
        "path_only": len(path_only),
        "surface": len(present),
    }


# --------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------

def build_source(args: argparse.Namespace, pin: dict, commit: str) -> Source:
    if args.checkout is not None:
        return CheckoutSource(Path(args.checkout))
    if args.from_gh:
        return GhSource(_source_repository(pin), commit, args.token)
    raise PinRefusal(
        "pin-unresolvable",
        "no source of openRepoShape bytes was given. openxFactory CITES this "
        "standard rather than mounting it, so this verifier has no tree of its "
        "own to read and must be told where the bytes are: pass --checkout PATH "
        "or --from-gh. Refusing rather than passing, because an unanswerable "
        "question is never an implicit pass")


def main(argv: list[str] | None = None) -> int:
    """Print one line and return 0, or print the refusal to stderr and return 2.

    Every failure path returns 2; see the module docstring for why there is no
    exit 1.
    """
    parser = argparse.ArgumentParser(
        prog="validate-openreposhape-pin.py",
        description=("Verify contracts/openreposhape-pin.yaml against the real "
                     "opensoft/openRepoShape bytes at the pinned commit."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--checkout", metavar="PATH", default=None,
        help="a local git checkout of opensoft/openRepoShape to verify against")
    parser.add_argument(
        "--from-gh", action="store_true",
        help="resolve the bytes from the GitHub API at the pinned commit")
    parser.add_argument(
        "--token", metavar="TOKEN", default=None,
        help="bearer token for --from-gh (optional; the product is public)")
    parser.add_argument(
        "--pin", metavar="PATH", default=None,
        help="an alternative pin file (tests)")
    args = parser.parse_args(argv)

    try:
        pin = read_pin(Path(args.pin) if args.pin else PIN_PATH)
        commit = pinned_commit(pin)
        summary = verify(build_source(args, pin, commit), pin)
    except PinRefusal as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"OK openreposhape-pin verified: "
          f"{_source_repository(pin)}@{summary['commit']} "
          f"from {summary['source']}, {summary['digested']} digest(s) "
          f"recomputed, {summary['path_only']} member(s) present, "
          f"{summary['surface']} file(s) declared with none undeclared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
