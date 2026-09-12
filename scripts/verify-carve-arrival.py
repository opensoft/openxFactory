#!/usr/bin/env python3
"""Verify a CARVE DESTINATION against `docs/opendox-carve-manifest.yaml` — the
half of FLOOR PART 1 that lives at the destination.

WHY THIS FILE EXISTS. `scripts/validate-carve-manifest.py` validates the
manifest AGAINST openxFactory: every row's digest at the carve commit, the
surface's completeness, the closed vocabularies. It says nothing about whether
anything ARRIVED, and the ruling's sentence — "a file in no row, or an edit in
no class, is an UNDECLARED MOVEMENT and the carve REFUSES" — is a claim about
BOTH trees. The moves memo (§ 2.3, 2026-09-09) names the gap in one line:
"This needs a verifier that does not exist." This is it, and
`docs/opendox-cutover-runbook.md` is the procedure it serves.

IT LIVES IN openxFactory AND IS NEVER COPIED INTO SIX REPOSITORIES. The
manifest lives here; a verifier copied six ways is six things to keep in step
with one document. It runs from here with a destination checkout in hand:

    python3 scripts/verify-carve-arrival.py \\
        --destination opendox_code --dest-root ../openDox-code \\
        --source-repo . --phase A

THE TWO PHASES ARE THE TWO COMMITS, and the runbook § 5.5 explains why the leg
lands as two. Commit A places every row's blob byte-identical to `carve_commit`,
so `--phase A` can prove EVERY moved row of a destination at its strongest — the
analogue of the openXwallet extraction's "100/100 at the carve layer". Commit B
applies that destination's declared edits and nothing else, so `--phase B`
checks that the arrived blob differs from the carve blob ONLY on lines the row's
own `edits[].lines` declare. A reviewer then reads the declared lines rather
than the whole leg.

FIVE FINDINGS AND ONE ENVIRONMENT CODE, closed and ordered by the check that
raises them, on `validate-carve-manifest.py`'s own idiom:

  `arrival-missing`               a row for this destination has no file at its
                                  `destination_path`.
  `arrival-digest-mismatch`       the arrived bytes or the arrived mode are not
                                  the row's. Every moved row at phase A; every
                                  `moved_verbatim` row at BOTH phases, because
                                  verbatim means verbatim in every phase; and
                                  every DECLARED replica — in both phases where
                                  its row declares no line, at phase A where it
                                  does (RULED Q-L7 (a)).
  `arrival-undeclared-edit`       phase B only: the arrived blob differs from
                                  the carve blob on a line no `edits[].lines`
                                  declares. The refusal NAMES THE LINES and
                                  carries a unified-diff excerpt. A declared
                                  replica whose row declares lines is held to
                                  the same bound at the path `--replica-at`
                                  names.
  `arrival-undeclared-file`       an ENTRY under one of this destination's
                                  DECLARED ROOTS that no row places and no
                                  admission rule admits — a file, a symlink,
                                  or a symlink to a DIRECTORY, which git
                                  stores as a `120000` blob and which
                                  `os.walk` would otherwise hand to
                                  `dirnames` and never read. A file admitted
                                  as SCAFFOLD whose bytes are not the
                                  destination's own at `--dest-base` refuses
                                  here too: the admission is by name, and a
                                  name is not a licence to carry content.
  `arrival-carved-from-mismatch`  an ASSEMBLY ROOT's `contracts/manifest.yaml`
                                  carries no `carved_from:`, or one naming
                                  another repository or another commit
                                  (RULED OQ-I).
  `arrival-unreadable`            THE ENVIRONMENT AND THE ENCODING: no git, an
                                  unreadable or unparseable manifest, an unknown
                                  `--destination`, a `--dest-root` that is not a
                                  directory, a `--dest-base` that resolves to no
                                  commit, `--destination` and `--assembly-root`
                                  together, a `--source-repo` that does not
                                  carry `carve_commit`, or a source repository
                                  that disagrees with the manifest about a row's
                                  digest. ALSO a declared admissions file this
                                  tool cannot trust: unparseable, not a mapping,
                                  naming a destination id the manifest's own
                                  `destinations:` does not carry, repeating a
                                  `path:` under one destination, or listing one
                                  out of alphabetical order (RULED, #656 comment
                                  5639058687 — see `read_admissions()`). There
                                  is no second validator for THAT document, so
                                  its shape is this file's own finding, on
                                  `read_manifest`'s reasoning for the manifest.
                                  It is also the CATCH-ALL that holds
                                  the exit contract: any exception this file did
                                  not name reaches the caller as this code and
                                  exit 2, never as a traceback and exit 1.

THE SPLIT BETWEEN THIS FILE'S CODES AND THE MANIFEST VALIDATOR'S is ownership,
not taste. Every `carve-*` code is a manifest that disagrees with openxFactory;
every `arrival-*` code is a DESTINATION that disagrees with the manifest. So
this file re-owns nothing: a manifest whose shape is wrong, whose digests do not
match openxFactory at the carve commit, or whose surface is incomplete is
`validate-carve-manifest.py`'s finding, and this file refuses such a document as
`arrival-unreadable` NAMING THAT TOOL rather than inventing a second, weaker
opinion about the same bytes. Both are run; neither substitutes for the other.

WHAT A LINE IS, AND WHY IT IS DEFINED IN A THIRD FILE (RULED Q-L8 (c)). The
manifest declares 899 edit lines BY NUMBER, this file decides whether a diff
touches only them, and `validate-carve-manifest.py` bounds them against the
carve blob — so a number must mean the same thing in both tools, and it did
not: this one split with `str.splitlines()` and that one counted `b"\\n"`, which
disagree on any file carrying `U+2028`, `U+2029`, `\\v`, `\\f`, `\\x1c`-`\\x1e`
or `\\x85` inside a line. Three rows of the landed manifest do, and six
declared lines over two of them were unappliable at the destination as a
result — carve leg 3 measured it and reported it rather than narrowing around
it. `scripts/carve_lines.py` now holds the ONE definition and both tools import
it: a line is a `\\n`-terminated record of the raw bytes, which is what `git
diff`, `grep -n` and the manifest's authors already counted.

WHAT IT DELIBERATELY DOES NOT PROVE, stated because a floor that overstates its
reach is worse than one that does not reach.

  * A `replicated_at_destination` row carries NO `destination`, NO
    `destination_path` and NO digest — by the row grammar, and RULED OQ-C is the
    reason: "this manifest declares what LEAVES, not what the destination
    assembles." So a replica's ARRIVAL is undeclared BY THE MANIFEST, and
    nothing here derives it: a guess at `src/<pkg>/<basename>` would be
    inventing the answer it then checked. Two readings, and both are offered.
    UNDECLARED, this file ADMITS a destination file whose bytes still equal a
    replica's NON-EMPTY blob at `carve_commit` and reports the count — empty
    bytes identify no file, and two of the landed manifest's 20 replica rows
    are `fixtures/empty/*/.gitkeep`, so an empty-digest admission would let any
    empty created file ride in as "a replica"; such a replica is admitted only
    by `--replica-at`, which admits by name; it cannot say
    whether the replica is there at all, and it cannot refuse one that drifted.
    DECLARED with `--replica-at <source>=<destpath>` — the runbook's per-leg
    table in machine form, restated in the pull request that places it — the
    replica is answered with the two codes a row is answered with,
    `arrival-missing` and `arrival-digest-mismatch`, and is admitted in the
    walk by NAME rather than by a coincidence of bytes. Drift is EXPECTED in at
    least one case the memo names —
    `tests/corpus-adapter/test_conformance.py`'s implementation-aware block
    imports the home factory and MUST be rewritten at each destination — and
    that copy is simply not declared, which leaves it exactly where it was. A
    row that is neither verbatim nor declared-edit is not made falsifiable by
    wishing; it is made falsifiable by somebody declaring where it went.
  * "APPLIED IDENTICALLY AT EVERY REPLICA" IS A BOUND ON LINES, NOT A
    CROSS-DESTINATION COMPARISON (RULED Q-L7 (a)). A replica row may now
    declare `edits:`, and this file verifies the declaration exactly as it
    verifies a moved row's: byte-identical at phase A, and at phase B a diff
    against the carve blob that touches only the row's own
    `edits[].lines`. ONE DESTINATION IS VERIFIED PER RUN — that is what
    `--destination` means — so two legs placing the same replica are two runs,
    and nothing here compares their two copies with each other. Two replicas
    edited DIFFERENTLY on the same declared line therefore both pass, and the
    identity of the applied text is the operator's claim in the pull request
    plus each leg's own `validate`. An UNAPPLIED declared edit on a replica
    does not refuse either, on the same reasoning as a moved row's (below):
    its diff touches no undeclared line, which is the only question the
    ruling's sentence asks. It is COUNTED in `declared_edits_unapplied`
    alongside the moved rows', and what refuses an unapplied
    `REPO_ROOT = HERE.parent.parent` is the destination's own suite, where a
    root pointing outside the repository is 391 setup errors and not an
    opinion.
  * A MOVED ROW THE MANIFEST ALSO REPLICATES ELSEWHERE
    (`also_replicated_to:`, RULED Q-L7 (a)) is a MOVE at the destination its
    `destination:` names and a REPLICA at each destination the list names. At
    the listed destination it is answered exactly as a replica is: undeclared,
    admitted by identity with its blob at `carve_commit`; declared with
    `--replica-at`, present and within its bound. `--replica-at` admits such a
    row ONLY when the destination being verified is in that list AND is not
    the row's own — so the flag still cannot re-point an arrival the manifest
    declared, which is what it was narrowed for. The row's `git_mode` IS
    compared at such a replica, because a moved row declares one; a
    `replicated_at_destination` row declares none and its replica's mode is
    still unchecked.
  * A file CREATED at a destination has no row either (RULED OQ-C) — the import
    root, `pyproject.toml`, `pytest.ini`, `conftest.py`, and openXdox-code's
    `openxfactory_surface.py` (RULED OQ-L). Each is named on the command line
    with `--allow-created`, once, so an unplaced file at a destination is either
    admitted by a rule that can be read here or written down in the pull request
    that admits it. There is deliberately no wildcard. AS OF RULED #656 (Brett
    Heap, 2026-09-11, comment 5639058687) the GOVERNED form of that admission is
    a `created:` entry in the destination's own block of
    `docs/opendox-carve-admissions.yaml`, read automatically by
    `read_admissions()` and applied exactly as `--allow-created` admits — so a
    NEW admission is a reviewed one-line diff in the pull request that bumps
    the destination's pin, rather than a flag typed once and recorded nowhere.
    `--allow-created` still works, for an ad-hoc run over a tree with no
    admissions file yet, and `main()` prints one line saying the declared form
    is the governed one.
  * A declared edit that has NOT BEEN APPLIED does not refuse. Its diff touches
    no undeclared line, which is the only question the ruling's sentence asks,
    and the destination's own `validate` refuses a leg whose imports still name
    `ideation_dashboard`. It is COUNTED and PRINTED (`unapplied`) rather than
    passed over in silence, because a phase-B run reporting 62 rows diffed and a
    phase-B run reporting 0 are very different events wearing the same `OK`.

ADDRESSING AN ASSEMBLY ROOT THE MANIFEST GIVES NO KEY. `destinations:` is a map
of the places ROWS GO. RULED OQ-I puts `carved_from:` in EACH assembly root's
`contracts/manifest.yaml`, and the runbook writes one at § 6 and another at § 7
— but the landed manifest declares `opendox_root` and NO `openxdox_root`,
because openXdox's assembly root receives no row and so has no key. Addressed
only by key, half the provenance the ruling requires would be uncheckable by the
tool that checks the other half. So `--assembly-root <owner>/<name>` addresses a
root BY THE REPOSITORY IT IS, runs the `carved_from:` check and nothing else,
and reports the `destinations:` key beside it where there is one. The check does
not depend on which root is read — it compares `carved_from` with the manifest's
`source_repository` and `carve_commit` — which is exactly why a root the
manifest never names can still be held to it.

THE SCAFFOLD ADMISSIONS ARE BY NAME, AND `--dest-base` IS WHAT MAKES A NAME
SAFE. A leg's own files sit under declared roots — `.gitkeep` in every empty
role directory, `tests/test_leg_shape.py` and everything its `REQUIRED_FILES`
lists, `docs/branch-protection.md` — and each is admitted by NAME, because
`--allow-created` would record in the pull request that the destination
ASSEMBLED a file the scaffold shipped. A name alone, though, admits whatever is
written at it: a payload at `docs/branch-protection.md`, a `.gitkeep` with
content, a path added to the destination's own `REQUIRED_FILES` in the arrival
commit — a check taking its allowlist from the tree it is checking. So the
allowlist is read from `--dest-base` (default `origin/main` where the
destination is a git repository carrying it) and every scaffold admission's
BYTES must equal the destination's own copy at that revision. Where there is no
baseline — an export, an unpushed tree — the name alone is still the admission,
and both the summary and the human line SAY SO rather than letting the weaker
claim pass for the stronger.

THE DECLARED ROOTS are computed from the manifest, never configured: for one
destination, the MINIMAL set of directories under which every one of its rows
lands. For `opendox_code` that is `src/opendox/` and `tests/`; for
`openxdox_code`, `scripts/`, `src/openxdox/` and `tests/`. A destination
declaring no rows — `opendox_root`, where the release identity is cut (§ 3.8)
— has no roots and no walk, and the `carved_from:` check is its whole job.

Exit codes:
  0  the destination verifies, or no destination was named
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1, on `validate-carve-manifest.py`'s reasoning:
  the gate's only question is "did this leg arrive as declared", and the answer
  is the same for "a digest drifted" and "the bytes could not be read". That is
  ENFORCED and not merely intended: `main()` catches every `Exception` its own
  checks did not name — a `KeyError` from a manifest row missing
  `destination_path:` is the measured case — and renders it as
  `arrival-unreadable`, so the contract does not depend on a reader auditing
  every raise site. `KeyboardInterrupt` and `SystemExit` are the operator's
  acts and are left alone.

THE SEAT-HOLDING PASS. Given NO `--destination`, this prints
`NO DESTINATION …` and exits 0. That is the same deliberate not-fail-closed
branch `validate-carve-manifest.py` carries for its default manifest path, and
it exists for the same reason: this file lands BEFORE the trees it checks. No
destination checkout exists on any machine until Phase 2 of the runbook runs,
and the § 8.2 seat in `tests/carve_arrival/` must be able to assert that the
DOCUMENTED INVOCATION answers, inside openxFactory's own required suite, without
asserting that a carve has happened. It keys off `--destination` being ABSENT
and never off a lookup failing: a caller who NAMES a destination and misspells
it refuses `arrival-unreadable`, because a typo must not be indistinguishable
from "not yet carved".

Run: `python3 scripts/verify-carve-arrival.py --destination <key> --dest-root
<dir> --phase A|B [--dest-base <ref>] [--admissions <path>]`, or
`--assembly-root <owner>/<name> --dest-root <dir>` for a root's `carved_from:`;
driven by `tests/carve_arrival/test_verify_carve_arrival.py`.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import ntpath
import os
import posixpath
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - the repository ships PyYAML
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

# THE FLOOR'S ONE DEFINITION OF A LINE (RULED Q-L8 (c)), shared with
# `validate-carve-manifest.py` so that a declared line number means the same
# thing where it is BOUNDED and where it is CHECKED. `scripts/` goes on the
# path because both tools are hyphenated entry points their own tests load by
# `spec_from_file_location`, where Python inserts nothing; GUARDED and therefore
# idempotent, on `scripts/proposal-support.py`'s idiom and for its stated
# reason — `tests/carve_arrival/` loads this file at import and
# `tests/carve_manifest/` loads it again in four cases, so an unguarded insert
# would prepend a duplicate entry per load and move import precedence under
# everything else in the session.
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import carve_lines  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# The ruled path, shared with `validate-carve-manifest.py` (RULED OQ-E).
# Relative, so `--source-repo` moves the question to another tree without
# moving the path.
MANIFEST_RELPATH = "docs/opendox-carve-manifest.yaml"

# The tool that OWNS the manifest's agreement with openxFactory. Named in every
# `arrival-unreadable` refusal that is really a manifest defect, so a reader is
# never left choosing between two opinions about the same bytes.
MANIFEST_VALIDATOR = "scripts/validate-carve-manifest.py"

# THE DECLARED ADMISSIONS FILE (RULED — the arrival-admission repair, Brett
# Heap, 2026-09-11, `#656` comment `5639058687`, "Declared per-leg admissions
# file"). Beside the manifest by default, exactly as `MANIFEST_RELPATH` sits
# beside this script's own reasoning for `--manifest`: a caller who moves the
# manifest with `--manifest` moves the admissions file with it, because the
# two are one destination's governance and not two independently-addressed
# documents. See `read_admissions()`.
ADMISSIONS_BASENAME = "opendox-carve-admissions.yaml"

# THE EXACT ENVELOPE VALUES (Copilot review, PR #979) — `validate-carve-
# manifest.py`'s own SCHEMA_VERSION/KIND idiom for `schema_version`, mirrored
# here rather than a bare `isinstance(…, int)` / `isinstance(…, str)` TYPE
# check: a type check alone accepts `schema_version: 999` as readable and
# `schema_version: true` as version 1 (`isinstance(True, int)` is `True` in
# Python — a bool satisfies an int type check while never equalling the
# version this reader knows), and accepts ANY string as `kind:`. This
# document OWNS its shape (there is no second validator for it), so this is
# the one place its exact envelope is checked, not merely its Python type.
ADMISSIONS_SCHEMA_VERSION = 1
ADMISSIONS_KIND = "opendox-carve-admissions"

MOVED_DISPOSITIONS: tuple[str, ...] = ("moved_verbatim",
                                       "moved_with_declared_edit")
REPLICA_REASON = "replicated_at_destination"
ASSEMBLY_LEG = "assembly"
PHASES: tuple[str, ...] = ("A", "B")

# FIXED, COMPLETE and ordered by the check that raises it. Other code may branch
# on the CODE, so no failure path here may invent one, and
# `tests/carve_arrival/test_verify_carve_arrival.py` scans this file's own
# `ArrivalRefusal(...)` sites and fails if any code is missing from this tuple.
REFUSAL_CODES: tuple[str, ...] = (
    "arrival-missing",
    "arrival-digest-mismatch",
    "arrival-undeclared-edit",
    "arrival-undeclared-file",
    "arrival-carved-from-mismatch",
    "arrival-unreadable",
)

REMEDIATION = (
    "Remediation: fix the DESTINATION, never the manifest — a manifest edited "
    "to match a tree that arrived wrong is the floor deleted. Re-place the "
    "row's blob from the carve commit (`git cat-file blob "
    "<carve_commit>:<source_path>`) for a phase-A mismatch; move an undeclared "
    "edit out of commit B, or re-cut the manifest row that should have "
    "declared it; name a file the destination legitimately assembles with "
    "`--allow-created <path>` and say why in the pull request. Where the "
    "manifest itself disagrees with openxFactory, that is "
    f"`{MANIFEST_VALIDATOR}`'s finding and not this one."
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# The scaffold placeholder every `openRepoShape` leg carries in its empty role
# directories. Admitted by NAME rather than by digest: an empty file's digest is
# the empty digest, which several replica rows also carry, and admitting a
# `.gitkeep` as "a replica" would be a true statement about the bytes and a
# false one about the file.
GITKEEP = ".gitkeep"

# The destination's PRE-CARVE baseline, read when the destination is a git
# repository and `--dest-base` names nothing else. Every SCAFFOLD admission is
# by NAME — `.gitkeep`, the leg-shape test's `REQUIRED_FILES`, the posture
# document — and a name is not a licence to carry content: without a baseline
# to compare against, a payload written to `docs/branch-protection.md`, to any
# `.gitkeep`, or to any path a destination's own `REQUIRED_FILES` happens to
# name is admitted on the strength of its filename. Compared against this ref
# the admission says what it means: this file is the destination's own, byte
# for byte, from before the carve began.
DEST_BASE_DEFAULT = "origin/main"

# `--dest-base` is the ONE value here that reaches git having come from the
# command line rather than from the manifest, so it is validated at the
# boundary before any process is started. Conservative on purpose: a revision
# git would accept can carry far more than this, and nothing this tool needs to
# name does. It excludes whitespace, shell metacharacters and — the one that is
# an actual attack rather than a nuisance — a LEADING DASH, which `git
# rev-parse` would read as an option rather than a revision. `--end-of-options`
# is passed as well, so the two defences are independent.
DEST_BASE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/@^~{}-]{0,255}$")

# `--assembly-root <owner>/<name>`. Shape only: an assembly root the manifest
# does not declare has nothing here to be checked against, which is the whole
# reason the flag exists.
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")

# The leg scaffold's own test module. It lives under `tests/`, which IS a
# declared root for both `-code` legs, so it must be admitted or every arrived
# code leg refuses on the file that proves it is a leg.
LEG_SHAPE_TEST = "tests/test_leg_shape.py"

# The scaffold's own DOCUMENT under a declared root — the one admission
# `REQUIRED_FILES` cannot supply, because no leg's list names it.
# `docs/branch-protection.md` ships with the leg scaffold (measured
# 2026-09-09 in `opensoft/openDox`, `openDox-spec` and `openDox-code`; owed to
# the three openXdox repositories by RULED OQ-O's levelling), and `docs/` IS a
# declared root for `opendox_spec`, which receives
# `docs/ideation-dashboard-session-runbook.md`. MEASURED against the landed
# manifest, an openDox-spec leg built from its 56 rows refuses
# `arrival-undeclared-file` on the scaffold's own posture document — a leg that
# arrived perfectly, failed on a file the carve never touched.
#
# It is admitted as SCAFFOLD rather than left to `--allow-created`, because the
# two say different things: `--allow-created` records in the pull request that
# the destination ASSEMBLED this file, and a document whose whole subject is
# provenance may not arrive carrying a false one. Named here, and not read from
# the destination, because nothing at the destination declares it.
SCAFFOLD_DOCS: frozenset[str] = frozenset({"docs/branch-protection.md"})


class ArrivalRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so a
    caller can branch on the code without parsing prose. `render()` is the ONE
    place the human message is assembled, and `main()` prints exactly that, so
    the remediation trailer cannot be dropped by a caller that forgot it exists.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def render(self, where: str) -> str:
        """Always printable, even over a path Unicode cannot hold: a
        `surrogateescape`-decoded name reaches stderr under CPython's pinned
        `backslashreplace` handler and is escaped rather than raising."""
        return f"FAIL {where}: {self.code} — {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# git and the filesystem
# --------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """git, capturing BYTES — blob contents must not go through a decoder."""
    try:
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, check=False)
    except OSError as exc:  # pragma: no cover - no git on the host
        raise ArrivalRefusal("arrival-unreadable",
                             f"git could not be run in {repo}: {exc}") from exc


def require_commit(repo: Path, commit: str) -> None:
    """`commit` must name a COMMIT OBJECT this repository carries.

    `^{commit}` and not a bare rev-parse, for `validate-carve-manifest.py`'s
    reason: an annotated tag's object id is also 40 hex and git would peel it
    silently, so the referent would be a tag beside the commit rather than the
    commit. The carve tag is a LABEL and never the referent.
    """
    done = _git(repo, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    if done.returncode != 0 or not done.stdout.strip():
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{repo} does not carry the manifest's carve_commit {commit[:12]} "
            "as a commit object; the declared-edit diff is taken against that "
            "revision's blobs, so a source repository without it cannot answer "
            "the question. Point --source-repo at an openxFactory checkout or "
            "mirror whose history contains it")


def blob_at(repo: Path, commit: str, path: str) -> bytes | None:
    """The RAW bytes of `path` at `commit`, or None where it is not a blob."""
    done = _git(repo, "cat-file", "blob", f"{commit}:{path}")
    if done.returncode != 0:
        return None
    return done.stdout


def read_arrived(target: Path) -> tuple[str, bytes]:
    """The arrived file as git would see it: `(mode, bytes)`.

    A DESTINATION IS A WORKING TREE AND NOT NECESSARILY A REPOSITORY — the
    runbook's phase-A run happens on a merge that has not been pushed, and a
    reviewer may point this at an export — so the mode is derived from the
    filesystem exactly as git derives it when it stages a file: `120000` for a
    symlink, whose content is the TARGET PATH's bytes and not the target's
    content; `100755` when the OWNER execute bit is set (git records no other
    execute bit); `100644` otherwise.
    """
    try:
        st = os.lstat(target)
    except OSError as exc:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{target} could not be stat'd: {exc}") from exc
    if stat.S_ISLNK(st.st_mode):
        return "120000", os.readlink(target).encode("utf-8", "surrogateescape")
    if not stat.S_ISREG(st.st_mode):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{target} is not a regular file or a symlink; git carries no mode "
            "for it and no row can have placed it")
    try:
        data = target.read_bytes()
    except OSError as exc:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{target} could not be read: {exc}") from exc
    return ("100755" if st.st_mode & stat.S_IXUSR else "100644"), data


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _plain_relative_path(value: str) -> str | None:
    """The POSIX-normalised form of `value`, or None where it is not a plain
    path relative to some root: empty, absolute, drive/UNC-prefixed, carrying
    a `.`/`..` segment, or a `\\` this host does not treat as a separator.

    SHARED BY `dest_relative` (a CLI flag's right-hand side) and by every
    admissions-file `path:` (`_admission_path`, RULED #656) — the same hazard
    either way: `Path("/dest") / "/etc/passwd"` is `/etc/passwd`, an absolute
    value REPLACES the root it is joined to, and a `..` segment walks out of
    it, so a typo would answer a question about a file the run is not about
    and report it as the destination's.

    NON-CANONICAL FORMS ARE REFUSED RATHER THAN NORMALISED. A caller's value
    has to EQUAL a path the walk produced, and the walk produces canonical
    ones, so `src/./pkg/x.py` would silently never match; refusing says so.

    A REMAINING BACKSLASH IS ONE OF THOSE FORMS, and `os.sep` alone does not
    catch it. On a POSIX host `os.sep` is `/`, so the replacement is a no-op and
    `src\\pkg\\x.py` passed the canonicality test as a single filename — then
    matched nothing, because the walk joins with `/`. The replacement runs
    FIRST, so on a Windows host a backslash path is converted as intended; what
    is refused is a backslash that SURVIVES it.

    A DRIVE OR UNC PREFIX IS REFUSED TOO, and `posixpath.isabs` does not see
    one: `C:/x` is not POSIX-absolute, but on Windows `Path(dest) / "C:/x"`
    leaves the destination root, and on POSIX it is a filename with a colon in
    it that can never match a walked path. `ntpath.splitdrive` names both forms
    — a drive letter and a `//server/share` UNC root — on every platform, which
    is why the check does not depend on where this runs.
    """
    relpath = value.replace(os.sep, "/")
    normalised = posixpath.normpath(relpath) if relpath else ""
    if (not relpath or "\\" in relpath or posixpath.isabs(relpath)
            or ntpath.splitdrive(relpath)[0] or relpath != normalised
            or normalised in (".", "..") or normalised.startswith("../")):
        return None
    return relpath


def dest_relative(value: str, flag: str) -> str:
    """A path INSIDE `--dest-root`, or a refusal.

    `--replica-at`'s right-hand side and every `--allow-created` value come
    from the command line and are joined to `--dest-root` or compared with a
    path the walk produced. The estate already treats this as a hard
    requirement rather than a nicety (`scripts/proposal-support.py` rejects
    absolute and `..` paths after normalisation), and this is the same guard,
    over `_plain_relative_path`'s one definition of what a plain path is.
    """
    result = _plain_relative_path(value)
    if result is None:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{flag} {value!r} is not a plain path inside --dest-root: it is "
            "empty, absolute (POSIX-absolute, or carrying a `C:` drive or a "
            "`//server/share` UNC prefix), or carries `.`/`..` segments or a "
            "`\\` this host does not treat as a separator. An absolute "
            "right-hand side REPLACES the destination root when it is joined, "
            "and `..` walks out of it, so such a value would answer a "
            "question about a file this run is not about. Give the path "
            "relative to --dest-root, in the canonical form the walk reports")
    return result


def _admission_path(value: Any, where: str, admissions_path: Path) -> str:
    """One admissions-file entry's `path:`, held to `dest_relative`'s shape
    (`_plain_relative_path`, shared) but refused as an ADMISSIONS FILE defect
    — naming the file and the field — rather than as a command-line one,
    because `--allow-created` was never involved in raising it.
    """
    if not isinstance(value, str) or not value:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {admissions_path} declares {where} as "
            f"{value!r}, not a non-empty string")
    result = _plain_relative_path(value)
    if result is None:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {admissions_path} declares {where} as "
            f"{value!r}, which is not a plain path relative to --dest-root: "
            "empty, absolute (a POSIX-absolute path, or one carrying a `C:` "
            "drive or a `//server/share` UNC prefix), or carrying a `.`/`..` "
            "segment or a `\\` this host does not treat as a separator — the "
            "same shape `--allow-created` itself is held to")
    return result


# --------------------------------------------------------------------------
# the manifest, read but NOT re-validated
# --------------------------------------------------------------------------

def read_manifest(path: Path) -> dict[str, Any]:
    """The manifest as a document.

    EVERY failure here is `arrival-unreadable` and every message names
    `validate-carve-manifest.py`. This file does not re-own the manifest's
    shape: two tools with two opinions about one document is how a reader ends
    up believing the weaker one. What it does own is refusing to proceed on a
    document it cannot read the fields it needs out of.
    """
    try:
        text = path.read_text(encoding="utf-8")
    # `ValueError` covers `UnicodeDecodeError`: bytes that never became a
    # document must reach the reader as this named exit-2 refusal rather than
    # as a traceback and exit 1.
    except (OSError, ValueError) as exc:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the manifest at {path} could not be read: {exc}") from exc
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        at = (f" at line {mark.line + 1} column {mark.column + 1}"
              if mark is not None else "")
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the manifest at {path} is not parseable YAML{at}: {exc}. Its "
            f"shape is `{MANIFEST_VALIDATOR}`'s finding, not this one") from exc
    if not isinstance(doc, dict):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the manifest at {path} is not a mapping (parsed as "
            f"{type(doc).__name__}); run {MANIFEST_VALIDATOR}")
    for key, kind in (("carve_commit", str), ("source_repository", str),
                      ("destinations", dict), ("rows", list)):
        if not isinstance(doc.get(key), kind):
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"the manifest at {path} carries no usable `{key}:`; this "
                f"verifier reads it and does not repair it — run "
                f"{MANIFEST_VALIDATOR}")
    if not COMMIT_RE.match(doc["carve_commit"]):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the manifest's carve_commit {doc['carve_commit']!r} is not 40 "
            f"lowercase hex; run {MANIFEST_VALIDATOR}")
    return doc


# --------------------------------------------------------------------------
# the declared admissions file (RULED — the arrival-admission repair,
# Brett Heap, 2026-09-11, `#656` comment 5639058687)
# --------------------------------------------------------------------------

def default_admissions_path(manifest_path: Path) -> Path:
    """The declared admissions file, BESIDE the manifest by default — same
    directory, so a `--manifest` override moves both together and a caller
    pointing this tool at another checkout gets that checkout's own
    admissions rather than this repository's."""
    return manifest_path.parent / ADMISSIONS_BASENAME


ADMISSIONS_ENTRY_FIELDS: tuple[str, ...] = ("path", "reason", "since")


class _DuplicateAdmissionsKeyError(yaml.constructor.ConstructorError):
    """A repeated mapping key in the admissions file, refused BY
    CONSTRUCTION rather than resolved by `yaml.safe_load`'s own
    last-duplicate-wins (Copilot review, PR #979): a `destinations:` block
    naming the same id twice, or a `created[]` entry repeating `path:` (or
    `reason:`/`since:`), would show a reviewer the FIRST value in a diff
    while this tool silently trusted the LAST — the same show-one-admit-
    another defect the admissions file exists to prevent, now inside the
    admission document itself. A subclass of `yaml.constructor
    .ConstructorError` (itself a `YAMLError`) so it carries `.problem` and
    `.problem_mark` on the same idiom as every other refusal below, and so a
    caller wanting the ORDINARY "not parseable YAML" message need only add
    one more specific `except` before it — it is not silently swallowed by
    the general handler."""


def _admissions_construct_mapping(loader: yaml.SafeLoader, node: Any,
                                  deep: bool = False) -> dict[Any, Any]:
    """`SafeConstructor.construct_mapping`, with every key checked against
    the keys already seen at this SAME mapping level before it is accepted.

    Mirrors `scripts/frontmatter_strict.py`'s `StrictLoader` /
    `_strict_construct_mapping` duplicate-key idiom without importing it:
    that module is the loader for a DIFFERENT ratified requirement (the
    realization-axis front-matter block — fenced prose with a byte ceiling
    and its own refused set of anchors/aliases/merge keys/directives/
    multi-document), not a general-purpose YAML utility, and this reader
    owns a plain standalone document with a narrower guard — only a
    repeated KEY is refused here, because every VALUE `read_admissions`
    reads is already checked against an exact shape a few lines below (an
    anchor's or alias's resolved value is checked the same as any other
    value's; only a silently-overwritten KEY would escape those checks, and
    that is the one gap this closes)."""
    seen: set[Any] = set()
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        hashable = key if isinstance(
            key, (str, int, float, bool, tuple)) else str(key)
        if hashable in seen:
            raise _DuplicateAdmissionsKeyError(
                None, None, f"duplicate key {key!r}", key_node.start_mark)
        seen.add(hashable)
    return yaml.constructor.SafeConstructor.construct_mapping(
        loader, node, deep=deep)


class _AdmissionsLoader(yaml.SafeLoader):
    """`SafeLoader` with duplicate mapping keys refused rather than
    silently resolved last-wins (Copilot review, PR #979). Nothing else
    about `SafeLoader` changes — anchors, aliases and merge keys still
    resolve, because their resolved VALUES are re-validated exactly as any
    other value's below; only the one gap that check cannot see, a key
    silently overwritten before any value is ever read, is closed here."""


_AdmissionsLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _admissions_construct_mapping)


def read_admissions(path: Path, doc: dict[str, Any]
                    ) -> dict[str, list[dict[str, str]]]:
    """The declared per-destination admissions file: each destination's
    `created:` list, applied exactly as `--allow-created` admits today, but as
    a REVIEWED ONE-LINE DIFF in the pin-bump pull request rather than typed on
    a command line (RULED — the arrival-admission repair, Brett Heap,
    2026-09-11, `#656` comment 5639058687, "Declared per-leg admissions
    file").

    ABSENT IS NOT A REFUSAL. A destination with no admissions file adopted
    yet — or a caller who has not adopted one at all — gets no declared
    admissions here, and `--allow-created` alone still works exactly as it did
    before this function existed. This is `resolve_dest_base`'s own treatment
    of a DEFAULT that is allowed to be missing, for the same reason: nothing
    has asked for this file by name.

    PRESENT AND MALFORMED IS `arrival-unreadable`, on `read_manifest`'s own
    reasoning: this file OWNS the admissions document's shape — there is no
    second validator to defer to the way the carve manifest defers to
    `validate-carve-manifest.py` — so a document this tool cannot trust is an
    environment/encoding failure and not a destination's arrival finding.

    THE CHECK GUARDS ITS OWN INPUT (RULED), because a hand-edited governance
    file must not be able to quietly admit less, or more, than it appears to:

      * every destination id must be a key of the MANIFEST's own
        `destinations:` map — an id the manifest does not carry can declare
        nothing this tool can check, and a typo must not silently admit
        nothing at every real destination while looking like it admits
        something at one;
      * every entry is `{path, reason, since}` of non-empty strings: `path`
        shaped exactly as `--allow-created`'s own value is (`_admission_path`),
        `reason` a ONE-LINE why (no embedded newline), `since` the 40-hex LEG
        commit that introduced the file — falsifiable the same way the
        manifest's own `carve_commit:` is;
      * no destination's `created:` list may repeat a `path:`;
      * every destination's `created:` list must already be SORTED by
        `path:` — the ruling's whole reason for this file existing is that a
        NEW admission is a one-line diff, which an unsorted list defeats the
        moment a second entry lands out of order.

    Returns `{destination_id: [{"path", "reason", "since"}, …]}`, one key per
    destination the FILE declares (never every destination the manifest
    carries — an omitted destination simply has no declared admissions).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as exc:
        # Anything other than "does not exist" — a permission failure, an
        # I/O error, `path` naming a directory — is NOT the same finding as
        # "no admissions file adopted yet" (Copilot review, PR #979): treating
        # every OSError as absence would silently disable the governed
        # admissions and let the run fall through to an unrelated
        # undeclared-file result instead of naming the real cause.
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} could not be read: {exc}"
        ) from exc
    except ValueError as exc:  # pragma: no cover - undecodable bytes
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} could not be decoded: {exc}"
        ) from exc
    try:
        raw = yaml.load(text, Loader=_AdmissionsLoader)
    except _DuplicateAdmissionsKeyError as exc:
        # Caught BEFORE the general `yaml.YAMLError` below, and named
        # precisely rather than falling into "is not parseable YAML"
        # (Copilot review, PR #979): a duplicate key is syntactically valid
        # YAML that `yaml.safe_load` would accept and silently resolve
        # last-duplicate-wins — this is a REFUSAL this reader chooses, on
        # its own "guards its own input" rule above, not a parse failure.
        mark = exc.problem_mark
        at = (f" at line {mark.line + 1} column {mark.column + 1}"
              if mark is not None else "")
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} declares a duplicate mapping "
            f"key{at} ({exc.problem}): `yaml.safe_load` would resolve this "
            "SILENTLY as last-duplicate-wins, showing a reviewer one value "
            "and admitting from another"
        ) from exc
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        at = (f" at line {mark.line + 1} column {mark.column + 1}"
              if mark is not None else "")
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} is not parseable YAML{at}: {exc}"
        ) from exc
    # An EXISTING file that parses to nothing — empty, or comments-only, so
    # `yaml.safe_load` hands back `None` — is PRESENT AND MALFORMED, not
    # ABSENT (Copilot review, PR #979): treating it as absent here would let
    # a file present on disk (the summary would still report it as this
    # destination's `admissions_file`) silently disable every declared
    # admission it was supposed to carry. ABSENT is only a file that does
    # not exist at all (`FileNotFoundError`, above). `isinstance(None, dict)`
    # is `False`, so this falls straight into the very next check with no
    # special case needed — its message names `NoneType` on the same idiom
    # as any other wrong-shaped document.
    if not isinstance(raw, dict):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} is not a mapping (parsed as "
            f"{type(raw).__name__})")
    version = raw.get("schema_version")
    if (not isinstance(version, int) or isinstance(version, bool)
            or version != ADMISSIONS_SCHEMA_VERSION):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} carries `schema_version: "
            f"{version!r}`; this reader knows the INTEGER "
            f"{ADMISSIONS_SCHEMA_VERSION} only. `true` and `1.0` are both "
            "EQUAL to 1 in Python, and a bool or a float must not satisfy "
            "an integer schema check any more than it would for the "
            "manifest's own `schema_version:`")
    if raw.get("kind") != ADMISSIONS_KIND:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} carries `kind: "
            f"{raw.get('kind')!r}`, not {ADMISSIONS_KIND!r}")
    if not isinstance(raw.get("destinations"), dict):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"the admissions file at {path} carries no usable "
            "`destinations:`")
    known = set(doc["destinations"])
    result: dict[str, list[dict[str, str]]] = {}
    for dest_id, entry in raw["destinations"].items():
        if dest_id not in known:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"the admissions file at {path} declares destination "
                f"{dest_id!r}, which is not a key of the manifest's "
                f"`destinations:` map ({', '.join(sorted(known))}). An "
                "admissions file for a destination the manifest does not "
                "name can declare nothing this tool can check")
        if not isinstance(entry, dict) or not isinstance(
                entry.get("created"), list):
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"the admissions file at {path} carries no usable "
                f"`destinations.{dest_id}.created:` list")
        seen: set[str] = set()
        parsed: list[dict[str, str]] = []
        for index, item in enumerate(entry["created"]):
            if not isinstance(item, dict):
                raise ArrivalRefusal(
                    "arrival-unreadable",
                    f"the admissions file at {path} has a "
                    f"`destinations.{dest_id}.created[{index}]` that is not "
                    f"a mapping: {item!r}")
            for field in ADMISSIONS_ENTRY_FIELDS:
                value = item.get(field)
                if not isinstance(value, str) or not value:
                    raise ArrivalRefusal(
                        "arrival-unreadable",
                        f"the admissions file at {path} has a "
                        f"`destinations.{dest_id}.created[{index}]` with no "
                        f"usable `{field}:` (a non-empty string)")
                if field == "reason" and "\n" in value:
                    raise ArrivalRefusal(
                        "arrival-unreadable",
                        f"the admissions file at {path} has a "
                        f"`destinations.{dest_id}.created[{index}].reason` "
                        "carrying a newline; the ruling asks for a ONE-LINE "
                        "reason")
                if field == "since" and not COMMIT_RE.fullmatch(value):
                    # `.fullmatch`, not `.match`: `$` matches just before a
                    # trailing newline as well as at the true end of the
                    # string, so `.match` alone would admit 40 hex characters
                    # plus a trailing "\n" as if it were a clean 40-hex commit
                    # (Copilot review, PR #979). `.fullmatch` requires the
                    # match to cover the ENTIRE string, which the `\n` can't
                    # be pulled into, so it correctly refuses.
                    raise ArrivalRefusal(
                        "arrival-unreadable",
                        f"the admissions file at {path} has a "
                        f"`destinations.{dest_id}.created[{index}].since` of "
                        f"{value!r}, which is not 40 lowercase hex. `since:` "
                        "is the LEG commit that introduced the file and must "
                        "be falsifiable the same way `carve_commit:` is")
            admitted_path = _admission_path(
                item["path"],
                f"destinations.{dest_id}.created[{index}].path", path)
            if admitted_path in seen:
                raise ArrivalRefusal(
                    "arrival-unreadable",
                    f"the admissions file at {path} declares "
                    f"{admitted_path!r} twice under {dest_id!r}; one "
                    "admission per path, so a reader can trust the list")
            seen.add(admitted_path)
            parsed.append({"path": admitted_path, "reason": item["reason"],
                            "since": item["since"]})
        ordered = sorted(parsed, key=lambda e: e["path"])
        if [e["path"] for e in parsed] != [e["path"] for e in ordered]:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"the admissions file at {path} lists destination "
                f"{dest_id!r}'s `created:` out of alphabetical order by "
                "`path:`. The ruling's reason for declaring admissions here "
                "is that a NEW one is a ONE-LINE diff; an unsorted list "
                "defeats that the moment a reviewer has to find where a new "
                "entry belongs")
        result[dest_id] = parsed
    return result


def rows_for(doc: dict[str, Any], destination: str) -> list[dict[str, Any]]:
    """The MOVED rows this destination is owed, in manifest order."""
    return [row for row in doc["rows"]
            if isinstance(row, dict)
            and row.get("disposition") in MOVED_DISPOSITIONS
            and row.get("destination") == destination]


def replica_rows(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """The `not_moved / replicated_at_destination` rows — every destination's,
    because a replica row names none."""
    return [row for row in doc["rows"]
            if isinstance(row, dict)
            and row.get("disposition") == "not_moved"
            and row.get("reason") == REPLICA_REASON]


def _also_replicated_labels(row: dict[str, Any]) -> list[str]:
    """A row's `also_replicated_to:` read as A LIST OF STRINGS OR NOTHING.

    GUARDED AT EVERY LEVEL, exactly as `_declared_line_set` guards
    `edits[].lines`, and for the same reason: this file READS the manifest and
    does not revalidate it — a mis-shaped `also_replicated_to:` is
    `validate-carve-manifest.py`'s `carve-shape-invalid`, tested there, and not
    this file's finding — but it must not ACT on the mis-shape either. A bare
    STRING is the case that matters, because a string is an iterable of
    characters: a plain `in` test against one admits every destination key that
    is a SUBSTRING of it, which would let a hand-edited document be read as
    replicating a file at a leg it never named. Anything that is not a list
    declares nothing here, and a non-string entry inside a list is dropped
    rather than compared.
    """
    value = row.get("also_replicated_to")
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, str)]


def also_replicated_rows(doc: dict[str, Any],
                         destination: str) -> list[dict[str, Any]]:
    """The MOVED rows this destination receives as a REPLICA rather than as a
    move — `also_replicated_to:` listing it (RULED Q-L7 (a)).

    THE ROW'S OWN DESTINATION IS EXCLUDED, even where a document lists it.
    Such a manifest is `validate-carve-manifest.py`'s
    `carve-disposition-inconsistent` and this file does not re-own its shape;
    what it must not do is ACT on it, because at that one destination the row
    already declares an arrival by `destination_path:` and admitting it here as
    a replica would let `--replica-at` re-point it — the single thing that flag
    was narrowed to prevent.
    """
    return [row for row in doc["rows"]
            if isinstance(row, dict)
            and row.get("disposition") in MOVED_DISPOSITIONS
            and row.get("destination") != destination
            and destination in _also_replicated_labels(row)]


def declared_roots(rows: list[dict[str, Any]]) -> list[str]:
    """The MINIMAL directories under which every one of `rows` lands.

    Computed from the manifest and never configured, so a destination's walk is
    a function of the same document the arrivals are. Minimal rather than
    top-level: `src/opendox` and not `src`, so the walk does not sweep the
    scaffold's own `src/.gitkeep` into the undeclared set and then need a rule
    to take it back out.
    """
    dirs = sorted({os.path.dirname(row["destination_path"])
                   for row in rows
                   if isinstance(row.get("destination_path"), str)})
    minimal = [d for d in dirs
               if not any(other != d and d.startswith(other + "/")
                          for other in dirs)]
    # A row placed at the top level makes the whole tree the walk's scope; that
    # is the honest reading and the admission rules below then do the work.
    return sorted(set(minimal))


def under_roots(relpath: str, roots: list[str]) -> bool:
    """SEGMENT-AWARE, never a bare `startswith`: `tests_helpers/x.py` is not
    under `tests`, and a prefix test that says it is quietly widens the walk."""
    for root in roots:
        if root == "":
            return True
        if relpath == root or relpath.startswith(root + "/"):
            return True
    return False


# --------------------------------------------------------------------------
# check 1 — arrival, digests and modes
# --------------------------------------------------------------------------

def check_arrivals(rows: list[dict[str, Any]], dest_root: Path,
                   source_repo: Path, carve_commit: str,
                   phase: str) -> dict[str, int]:
    """Every moved row present, and its bytes what the phase requires."""
    counts = {"rows": len(rows), "digests_verified": 0, "diffed": 0,
              "unapplied": 0}
    for row in rows:
        relpath = row["destination_path"]
        target = dest_root / relpath
        if not os.path.lexists(target):
            raise ArrivalRefusal(
                "arrival-missing",
                f"the row for {row['source_path']} places a file at "
                f"{relpath} and {target} does not exist. Every moved row of a "
                "destination is owed at that destination; a leg missing one is "
                "a leg the manifest does not describe")
        mode, data = read_arrived(target)
        if mode != row.get("git_mode"):
            raise ArrivalRefusal(
                "arrival-digest-mismatch",
                f"{relpath} arrived with mode {mode} where the row for "
                f"{row['source_path']} records {row.get('git_mode')!r}. The "
                "mode is part of the blob's identity — git records it, the "
                "manifest declares it, and an executable bit gained or lost in "
                "transit is a change no digest comparison would name")
        # `moved_verbatim` is verbatim in EVERY phase; commit B touches only the
        # rows that declare edits, so a verbatim row that moved at commit B has
        # moved undeclared and the digest is where that surfaces.
        verbatim_here = (row["disposition"] == "moved_verbatim"
                         or phase == "A")
        if verbatim_here:
            got = digest(data)
            if got != row.get("sha256"):
                raise ArrivalRefusal(
                    "arrival-digest-mismatch",
                    f"{relpath} has sha256 {got} where the row for "
                    f"{row['source_path']} records {row.get('sha256')}"
                    + ("" if row["disposition"] == "moved_verbatim" else
                       " and PHASE A requires the carve commit's bytes exactly")
                    + (". `moved_verbatim` means the destination's bytes equal "
                       "this digest, in every phase and in every commit"
                       if row["disposition"] == "moved_verbatim" else
                       ". Commit A places the blob byte-identical; the declared "
                       "edits are commit B"))
            counts["digests_verified"] += 1
            continue
        # phase B, `moved_with_declared_edit`
        carve = _referent_blob(source_repo, carve_commit, row)
        if carve == data:
            counts["unapplied"] += 1
            continue
        _check_declared_lines(row, carve, data)
        counts["diffed"] += 1
    return counts


def _referent_blob(source_repo: Path, carve_commit: str,
                   row: dict[str, Any]) -> bytes:
    """The row's blob AT THE CARVE COMMIT, guarded against a source repository
    that disagrees with the manifest about it.

    Without the guard, a phase-B diff taken against the wrong bytes would report
    undeclared edits that are really the source repository's drift — a refusal
    naming the destination for the source's fault. The guard's own finding is
    NOT a `carve-*` code wearing a new name: it is `arrival-unreadable` naming
    the tool that owns the question, because "this manifest disagrees with
    openxFactory" is exactly what `validate-carve-manifest.py` exists to say.
    """
    data = blob_at(source_repo, carve_commit, row["source_path"])
    if data is None:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{source_repo} carries no blob at {carve_commit[:12]}:"
            f"{row['source_path']}, which the phase-B diff is taken against; "
            f"run {MANIFEST_VALIDATOR}, whose `carve-path-absent` owns this")
    got = digest(data)
    if got != row.get("sha256"):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"{source_repo} at {carve_commit[:12]} has sha256 {got} for "
            f"{row['source_path']} where the manifest records "
            f"{row.get('sha256')}. The source disagrees with the manifest "
            "about its own referent, so no diff taken here would be about the "
            f"destination; run {MANIFEST_VALIDATOR}")
    return data


# --------------------------------------------------------------------------
# check 2 — phase B: the diff touches ONLY declared lines
# --------------------------------------------------------------------------

def _declared_line_set(row: dict[str, Any]) -> set[int]:
    declared: set[int] = set()
    for edit in row.get("edits") or []:
        if isinstance(edit, dict):
            for line in edit.get("lines") or []:
                if isinstance(line, int):
                    declared.add(line)
    return declared


def _check_declared_lines(row: dict[str, Any], carve: bytes,
                          arrived: bytes, at: str | None = None) -> None:
    """Refuse unless every changed line is one the row declares.

    `at` is the ARRIVED PATH the refusal names, defaulting to the row's own
    `destination_path`. It is a parameter because a REPLICA of this row (RULED
    Q-L7 (a)) arrives at a path `--replica-at` names and not at any path the
    row carries — and a `replicated_at_destination` row carries no
    `destination_path` at all, so a message that read one would raise a
    `KeyError` where it meant to report a finding.

    THE LINE NUMBERS ARE THE CARVE COMMIT'S, which is what makes them
    falsifiable: a destination-side numbering would move under the very edits it
    is meant to bound. AND THEY ARE THE MANIFEST VALIDATOR'S NUMBERING — both
    tools split lines with `scripts/carve_lines.py` (RULED Q-L8 (c)), so the
    number this check reads is the number `validate-carve-manifest.py` bounded
    and the manifest's author counted. It did not use to be: this function used
    `str.splitlines()`, which also breaks on `\\v`, `\\f`, `\\x1c`-`\\x1e`,
    `\\x85`, `U+2028` and `U+2029`, so on the three landed rows carrying
    `U+2028` inside a line it read line numbers the validator had never issued
    and six declared lines over two `openxdox_code` rows were unappliable at
    the destination. One definition, in one module, imported by both.

    So the comparison walks `difflib`'s opcodes over the two line lists and
    asks, for each non-`equal` opcode, which CARVE-SIDE lines it touches:

      * `replace` / `delete` touch carve lines `i1+1 … i2` (1-based) and every
        one of them must be declared.
      * `insert` touches NO carve line — a line that did not exist at the carve
        commit has no number there. An insertion is therefore declared by naming
        a line it is inserted BESIDE, and the test is that at least one of the
        two neighbours (`i1`, `i1+1`, clamped into the file) is declared. That
        is the tightest statement a line-numbered grammar can make about an
        insertion, and it is stated here rather than left to a reader to infer
        from a passing run.

    A CHANGE NO LINE NUMBER CAN NAME still refuses, and under the floor's
    definition there is exactly ONE such change: a FINAL NEWLINE gained or lost
    (`b"a\\nb\\n"` and `b"a\\nb"` have the same records). If the bytes differ
    and the record lists do not, the difference is that, and it refuses rather
    than passing as "no changed line". A CRLF/LF flip is no longer in this
    class and is no longer answered this way: `\\r` is CONTENT under
    `carve_lines.records()`, so a flipped terminator is a change AT a line
    number, named and held to the row's declaration like any other.
    """
    declared = _declared_line_set(row)
    arrived_at = at if at is not None else row.get("destination_path")
    carve_records = carve_lines.text_records(carve)
    arrived_records = carve_lines.text_records(arrived)
    if carve_records == arrived_records:
        raise ArrivalRefusal(
            "arrival-undeclared-edit",
            f"{arrived_at} differs from the carve commit's blob "
            "in a way no line number can name — a final newline gained or "
            "lost, the one difference the floor's line definition cannot "
            f"express ({carve_lines.DEFINITION}). The declared-edit grammar "
            "bounds LINES, so a change outside them is undeclared whatever "
            "its size")
    undeclared: list[int] = []
    matcher = difflib.SequenceMatcher(a=carve_records, b=arrived_records,
                                      autojunk=False)
    for tag, i1, i2, _j1, _j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            neighbours = {n for n in (i1, i1 + 1)
                          if 1 <= n <= len(carve_records)}
            # An insertion into an EMPTY carve blob has no neighbour to name;
            # `declared` must then be non-empty for the edit to be declared at
            # all, and the row's own class says what it is.
            if neighbours and not (neighbours & declared):
                undeclared.extend(sorted(neighbours))
            elif not neighbours and not declared:
                undeclared.append(1)
            continue
        undeclared.extend(n for n in range(i1 + 1, i2 + 1)
                          if n not in declared)
    if undeclared:
        shown = sorted(set(undeclared))
        excerpt = "\n".join(list(difflib.unified_diff(
            carve_records, arrived_records,
            fromfile=f"carve:{row['source_path']}",
            tofile=f"arrived:{arrived_at}",
            lineterm="", n=1))[:24])
        classes = ", ".join(sorted({
            str(edit.get("class")) for edit in row.get("edits") or []
            if isinstance(edit, dict)})) or "none"
        raise ArrivalRefusal(
            "arrival-undeclared-edit",
            f"{arrived_at} was edited at carve-commit line(s) "
            f"{shown} which the row for {row['source_path']} does not declare; "
            f"it declares {sorted(declared)} under class(es) {classes}. "
            "Commit B applies the declared edits and nothing else — an edit in "
            "no class is an UNDECLARED MOVEMENT and the carve refuses (RULED "
            f"OQ-1).\n{excerpt}")


# --------------------------------------------------------------------------
# check 2b — replicas the OPERATOR declares (the manifest cannot)
# --------------------------------------------------------------------------

def parse_replica_placements(values: list[str], doc: dict[str, Any],
                             destination: str) -> dict[str, str]:
    """`--replica-at SOURCE=DESTPATH`, parsed against the manifest's replicas.

    THE LEFT SIDE IS A REPLICA ROW'S `source_path`, OR — RULED Q-L7 (a) — a
    MOVED row's, IFF the manifest lists the destination being verified in that
    row's `also_replicated_to:` and that destination is not the row's own. The
    `destination` argument is what makes the second half an `iff` rather than
    a widening: the same flag naming the same row is admitted at the leg the
    manifest replicates it to and REFUSED at every other leg, including the one
    the row already moves to. A flag that could name any moved row would let a
    caller re-point an arrival the manifest declared, which is the one thing
    the manifest is for.

    WHY A COMMAND-LINE DECLARATION AND NOT A DERIVATION. Measured over the
    landed manifest, all 20 `not_moved / replicated_at_destination` rows carry
    NO `destination`, NO `destination_path`, NO `sha256` and NO `git_mode` —
    the row grammar gives a `not_moved` row none of them, and RULED OQ-C is the
    reason ("this manifest declares what LEAVES, not what the destination
    assembles"). So there is nothing in the document to derive a replica's
    arrival from, and a verifier that guessed — `src/<pkg>/<basename>`, say —
    would be inventing the answer it then checked. The only party who knows
    where a replica landed is the operator who placed it, and the runbook's
    per-leg table is where that is written down; this flag is that table in
    machine form, restated in the pull request that makes the placement.

    IT NARROWS NOTHING THAT PASSES TODAY. An UNDECLARED replica is still
    admitted by identity with its blob at the carve commit and still counted
    (`admitted.replica`); this adds a stronger claim for the operator willing
    to make it, and does not withdraw the weaker one. What the declaration buys
    is the two questions the digest admission cannot ask: whether the replica
    is THERE AT ALL — a destination importing a module that never arrived is
    the memo's own worry about `scripts/corpus_adapter.py` — and whether it is
    the carve's bytes at the path the operator says it is, rather than at some
    path under a declared root where a coincidence of bytes let it in.

    IT WIDENS NO VOCABULARY. A declared replica is answered with the two codes
    a ROW is answered with — `arrival-missing` and `arrival-digest-mismatch` —
    because a declaration makes it exactly as falsifiable as a row, and a
    seventh code for the same two failures would be a second name for one
    thing.
    """
    replicas = {row["source_path"] for row in replica_rows(doc)}
    also = {row["source_path"]
            for row in also_replicated_rows(doc, destination)}
    placements: dict[str, str] = {}
    for value in values:
        source_path, sep, relpath = value.partition("=")
        if not sep or not source_path or not relpath:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--replica-at {value!r} is not SOURCE=DESTPATH: the left side "
                "is a replica row's source_path in openxFactory and the right "
                "is where it landed, relative to --dest-root")
        relpath = dest_relative(relpath, "--replica-at")
        if source_path not in replicas and source_path not in also:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--replica-at names {source_path!r}, which at destination "
                f"{destination!r} is neither a `not_moved / {REPLICA_REASON}` "
                "row of this manifest nor a moved row whose "
                "`also_replicated_to:` lists this destination (RULED Q-L7 "
                "(a)). A moved row's arrival is declared by its own "
                "`destination_path:`, and a flag that could name one would let "
                "a caller re-point a row the manifest already placed — so a "
                "moved row is admitted here only where the manifest itself "
                "says these bytes are ALSO replicated at the destination being "
                "verified, and never at the destination the row moves to")
        if source_path in placements:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--replica-at names {source_path!r} twice "
                f"({placements[source_path]!r} and {relpath!r}); one replica "
                "lands at one path per destination, and a repeated key would "
                "silently keep whichever was parsed last")
        placements[source_path] = relpath
    return placements


def check_replicas(placements: dict[str, str], dest_root: Path,
                   source_repo: Path, carve_commit: str,
                   doc: dict[str, Any], phase: str) -> dict[str, int]:
    """Every DECLARED replica present, and its bytes what the phase requires.

    BYTE-IDENTICAL TO THE CARVE BLOB, except where the replica's ROW DECLARES
    LINES (RULED Q-L7 (a)) and the phase is B — the two phases being the two
    commits, at a replica exactly as at a moved row: commit A places the copy,
    commit B applies the declared edit. So the answer is the same code path a
    moved row's is, `_check_declared_lines` included, with the arrived path
    coming from `--replica-at` rather than from a `destination_path:` the row
    may not have.

    THE MODE IS COMPARED ONLY WHERE THE ROW DECLARES ONE. A moved row also
    replicated here carries `git_mode:`; a `replicated_at_destination` row
    carries none, and inventing an expectation for it would be this file
    deriving a claim the manifest does not make — the same reason it does not
    derive the replica's PATH.
    """
    counts = {"verified": 0, "diffed": 0, "unapplied": 0}
    rows = {row["source_path"]: row for row in doc["rows"]
            if isinstance(row, dict) and isinstance(row.get("source_path"), str)}
    for source_path, relpath in sorted(placements.items()):
        row = rows.get(source_path, {})
        declared = _declared_line_set(row)
        target = dest_root / relpath
        if not os.path.lexists(target):
            raise ArrivalRefusal(
                "arrival-missing",
                f"--replica-at declares the replica of {source_path} at "
                f"{relpath} and {target} does not exist. RULED OQ-A places a "
                "replica AT the destination and RETAINS it here; a replica "
                "that never arrived leaves the leg importing a module that is "
                "not there, which its own `validate` finds later and less "
                "clearly")
        mode, data = read_arrived(target)
        expected_mode = row.get("git_mode")
        if isinstance(expected_mode, str) and mode != expected_mode:
            raise ArrivalRefusal(
                "arrival-digest-mismatch",
                f"the replica of {source_path} at {relpath} arrived with mode "
                f"{mode} where its row records {expected_mode!r}. This row "
                "MOVES to another destination and is ALSO replicated here "
                "(RULED Q-L7 (a)), so it declares a mode — and an executable "
                "bit gained or lost in transit is a change no digest "
                "comparison would name")
        carve = blob_at(source_repo, carve_commit, source_path)
        if carve is None:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"{source_repo} carries no blob at {carve_commit[:12]}:"
                f"{source_path}, which the declared replica is compared "
                f"against; run {MANIFEST_VALIDATOR}")
        if declared and phase == "B":
            if data == carve:
                # UNAPPLIED, AND LAWFUL, on the moved row's own reasoning: the
                # diff touches no undeclared line. Counted with the moved
                # rows' unapplied edits, because a phase-B run in which the
                # replica's declared line was applied and one in which it was
                # not are very different events wearing the same `OK`.
                counts["unapplied"] += 1
            else:
                _check_declared_lines(row, carve, data, at=relpath)
                counts["diffed"] += 1
            counts["verified"] += 1
            continue
        if data != carve:
            raise ArrivalRefusal(
                "arrival-digest-mismatch",
                f"the replica of {source_path} at {relpath} has sha256 "
                f"{digest(data)} where its blob at {carve_commit[:12]} has "
                f"{digest(carve)}. A replica is a COPY (RULED OQ-A) and the "
                "manifest records no digest for one, so DECLARING it is what "
                "makes the copy checkable — a declared replica that drifted is "
                "a claim withdrawn, not a fidelity this file never had."
                + (" Its row DECLARES lines (RULED Q-L7 (a)) and PHASE A "
                   "requires the carve commit's bytes exactly: commit A places "
                   "the copy, commit B applies the declared edit, at a replica "
                   "exactly as at a moved row." if declared else "")
                + " Where the copy MUST differ at this destination and no line "
                "declares it — `tests/corpus-adapter/test_conformance.py`'s "
                "implementation-aware block names the home factory and is "
                "rewritten at each destination — do not declare it with "
                "--replica-at; it is then admitted, uncounted as verified, on "
                "the same terms as before")
        counts["verified"] += 1
    return counts


# --------------------------------------------------------------------------
# check 3 — nothing under a declared root that no row places
# --------------------------------------------------------------------------

def resolve_dest_base(dest_root: Path, dest_base: str | None) -> str | None:
    """The destination's PRE-CARVE baseline revision, or None where the
    destination cannot supply one.

    A NAMED `--dest-base` that does not resolve REFUSES: an operator who asked
    for the strong admission must not silently get the weak one. The DEFAULT
    (`origin/main`) is allowed to be absent, because a destination is a working
    tree and not necessarily a repository — the runbook's phase-A run happens on
    an unpushed merge, and a reviewer may point this at an export. The summary
    then carries `dest_base: null` and the human line says so, so the weaker
    claim is never mistaken for the stronger one.
    """
    ref = dest_base or DEST_BASE_DEFAULT
    if not DEST_BASE_RE.fullmatch(ref):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"--dest-base {dest_base!r} is not a plain revision name. It is "
            "the one value this tool passes to git that came from the command "
            "line rather than from the manifest, so it is validated before a "
            "process is started: letters, digits, `.`, `_`, `/`, `@`, `^`, "
            "`~`, `{`, `}` and `-`, and never a LEADING dash, which "
            "`git rev-parse` would read as an option and not a revision")
    done = _git(dest_root, "rev-parse", "--verify", "--quiet",
                "--end-of-options", f"{ref}^{{commit}}")
    if done.returncode == 0 and done.stdout.strip():
        return done.stdout.decode("ascii", "replace").strip()
    if dest_base is not None:
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"--dest-base {dest_base!r} does not resolve to a commit in "
            f"{dest_root}. It names the destination's own pre-carve revision — "
            "the one every SCAFFOLD admission is checked against — and a run "
            "that fell back to admitting scaffold names on trust would answer "
            "a weaker question than the one it was asked")
    return None


def scaffold_allowlist(dest_root: Path, dest_base: str | None) -> set[str]:
    """The leg scaffold's OWN files, read from the destination rather than
    hard-coded here.

    `tests/test_leg_shape.py` names them: its `REQUIRED_FILES` list is the
    bootstrap posture every leg must carry (`tasks.md` § 1.3-1.5), and reading
    that list is how this verifier learns the scaffold WITHOUT a second copy of
    it drifting in openxFactory. The module is parsed with `ast.literal_eval`
    over the assignment, never imported: a destination checkout is untrusted
    input and importing it would execute it.

    READ FROM `dest_base` AND NOT FROM THE WORKING TREE where a baseline exists.
    The allowlist is otherwise taken from the very tree being checked: adding a
    path to the destination's own `tests/test_leg_shape.py` in the arrival
    commit admits that path, which is a check consulting its subject for its own
    rules. At the baseline the list is the scaffold's, from before the carve.

    The test module itself is added, because it lives under `tests/` — a
    declared root for both `-code` legs — and a leg that refused on the file
    proving it is a leg would be unusable. `SCAFFOLD_DOCS` is added for the
    same reason one level over: `docs/branch-protection.md` is under
    `opendox_spec`'s declared `docs/` root and is in no leg's
    `REQUIRED_FILES`. Both are NAMES only: `check_undeclared_files` still
    compares the bytes against `dest_base`.
    """
    allowed = {LEG_SHAPE_TEST} | set(SCAFFOLD_DOCS)
    if dest_base is not None:
        blob = blob_at(dest_root, dest_base, LEG_SHAPE_TEST)
        if blob is None:
            # A baseline with no leg-shape test is a `-spec` leg's business or
            # an assembly root's; the walk simply has one fewer admission rule.
            return allowed
        try:
            text = blob.decode("utf-8")
        except ValueError:  # pragma: no cover - a scaffold that is not text
            return allowed
    else:
        source = dest_root / LEG_SHAPE_TEST
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, ValueError):
            return allowed
    try:
        tree = ast.parse(text)
    except SyntaxError:  # pragma: no cover - a scaffold that does not parse
        return allowed
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "REQUIRED_FILES" not in names:
            continue
        try:
            value = ast.literal_eval(node.value)
        # `ast.literal_eval` raises `SyntaxError` as well as `ValueError` — and
        # `TypeError`, `MemoryError` and `RecursionError` over a hostile
        # literal. A destination checkout is untrusted input, so every one of
        # them is "this scaffold declares no readable list" and none of them is
        # a traceback and exit 1.
        except (ValueError, SyntaxError, TypeError, MemoryError,
                RecursionError):  # pragma: no cover - a non-literal list
            continue
        if isinstance(value, (list, tuple)):
            allowed.update(str(v) for v in value)
    return allowed


def check_undeclared_files(dest_root: Path, roots: list[str],
                           placed: set[str], replicas: set[str],
                           allow_created: set[str],
                           dest_base: str | None) -> dict[str, Any]:
    """Walk the declared roots; every entry is placed, or admitted, or refused.

    THE ADMISSION RULES ARE ORDERED and the order is a claim. A `.gitkeep` is
    admitted as SCAFFOLD before it can be admitted as a replica, because the
    empty digest belongs to several replica rows and calling the scaffold's
    placeholder "a replica" would be true about the bytes and false about the
    file.

    EVERY ENTRY, AND NOT EVERY FILE. A symlink pointing at a DIRECTORY lands in
    `os.walk`'s `dirnames`, is not descended into, and would never be read or
    counted — so an undeclared tracked directory symlink under a declared root
    would return `OK` while carrying a whole tree of undeclared content behind
    one name. git stores such a link as a BLOB of mode `120000` whose content is
    the target path, so it is pulled out of `dirnames` and answered here exactly
    as any other entry is.

    A SCAFFOLD ADMISSION IS BY NAME AND ITS BYTES ARE CHECKED. Where
    `dest_base` gives a baseline, an admitted scaffold file must equal the
    destination's own copy at that revision. Without it the name alone is the
    admission — `docs/branch-protection.md`, any `.gitkeep`, anything the
    destination's own `REQUIRED_FILES` lists — and a payload written at one of
    those names rides in.
    """
    admitted = {"scaffold": 0, "replica": 0, "created": 0}
    # THE SPECIFIC PATHS admitted via `allow_created`, tracked (and not just
    # counted) so a caller can tell a DECLARED admission that was actually
    # NEEDED from one that was not — a stale declared admission is a finding,
    # not silent (RULED, #656). Separate from `admitted["created"]`, which
    # this file's own callers already read as a plain count.
    created_paths: set[str] = set()
    scaffold = scaffold_allowlist(dest_root, dest_base)
    walked = 0
    for root in roots:
        base = dest_root / root if root else dest_root
        if not base.is_dir():
            # A declared root that does not exist is not this check's finding:
            # every row under it has already refused `arrival-missing`, which is
            # the more precise statement and the one a reader can act on.
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            linked_dirs = [d for d in dirnames
                           if d != ".git"
                           and os.path.islink(os.path.join(dirpath, d))]
            skip = set(linked_dirs) | {".git"}
            dirnames[:] = sorted(d for d in dirnames if d not in skip)
            for name in sorted([*filenames, *linked_dirs]):
                full = Path(dirpath) / name
                relpath = os.path.relpath(full, dest_root).replace(os.sep, "/")
                walked += 1
                if relpath in placed:
                    continue
                _mode, data = read_arrived(full)
                if name == GITKEEP or relpath in scaffold:
                    if dest_base is not None:
                        was = blob_at(dest_root, dest_base, relpath)
                        if was != data:
                            raise ArrivalRefusal(
                                "arrival-undeclared-file",
                                f"{relpath} is admitted as SCAFFOLD by name, "
                                "and its bytes are not the destination's own "
                                f"copy at {dest_base[:12]} "
                                + ("(no such path there)" if was is None else
                                   f"(sha256 {digest(data)} here, "
                                   f"{digest(was)} there)")
                                + ". Every scaffold admission is by NAME — a "
                                "`.gitkeep`, the leg-shape test's "
                                "`REQUIRED_FILES`, the posture document — and "
                                "a name is not a licence to carry content: a "
                                "file arriving at a scaffold's name with other "
                                "bytes is an UNDECLARED MOVEMENT wearing that "
                                "name. Restore the destination's own copy, or "
                                f"name the change with `--allow-created "
                                f"{relpath}` and say why in the pull request")
                    admitted["scaffold"] += 1
                    continue
                if relpath in allow_created:
                    admitted["created"] += 1
                    created_paths.add(relpath)
                    continue
                # EMPTY BYTES IDENTIFY NOTHING, so they admit nothing: the
                # empty digest is excluded from `replicas` upstream (see
                # `verify`), and an empty arrived file falls through to the
                # refusal rather than being recorded as a replica it cannot be.
                if data and digest(data) in replicas:
                    admitted["replica"] += 1
                    continue
                raise ArrivalRefusal(
                    "arrival-undeclared-file",
                    f"{relpath} sits under a declared root and no row places "
                    "it, no scaffold file is named that, and its bytes are no "
                    "replica's at the carve commit"
                    + (" — it is EMPTY, and empty bytes identify no file, so "
                       "no replica row admits it however many replicas are "
                       "themselves empty" if not data else "")
                    + ". A file in no row is an "
                    "UNDECLARED MOVEMENT and the carve refuses (RULED OQ-1). "
                    "If it IS a replica this destination places, declare it "
                    f"with `--replica-at <source_path>={relpath}` — which is "
                    "also the ONLY way a replica whose row declares lines "
                    "(RULED Q-L7 (a)) can be read as one, because its edited "
                    "bytes match no blob at the carve commit and the "
                    "byte-identity admission cannot see it. If instead the "
                    "destination legitimately assembles it (RULED OQ-C — the "
                    "import root, a created surface module), name it with "
                    f"`--allow-created {relpath}` and say why in the pull "
                    "request")
    admitted["walked"] = walked
    admitted["created_paths"] = created_paths
    return admitted


# --------------------------------------------------------------------------
# check 4 — `carved_from:` at an assembly root (RULED OQ-I)
# --------------------------------------------------------------------------

def check_carved_from(dest_root: Path, doc: dict[str, Any]) -> dict[str, str]:
    """The machine-read provenance record, at the object whose one commit names
    both legs.

    Only the two ASSEMBLY ROOTS carry `contracts/manifest.yaml`; the four legs
    have no `contracts/` at all, which is why RULED OQ-I places the record here
    and not in each leg. The file is hand-authored and validated by nothing —
    `validate-manifest.py` reads `project.yaml`, and it is digest-pinned by
    `contracts/shape-pin.yaml`, so it must not be edited into reading this — so
    this check is the only running code that says the record is right.
    """
    path = dest_root / "contracts" / "manifest.yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        raise ArrivalRefusal(
            "arrival-carved-from-mismatch",
            f"{path} could not be read ({exc}); an assembly root carries "
            "`contracts/manifest.yaml` and RULED OQ-I puts `carved_from:` "
            "in it") from exc
    try:
        root_doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ArrivalRefusal(
            "arrival-carved-from-mismatch",
            f"{path} is not parseable YAML: {exc}") from exc
    carved = (root_doc or {}).get("carved_from") if isinstance(root_doc, dict) \
        else None
    if not isinstance(carved, dict):
        raise ArrivalRefusal(
            "arrival-carved-from-mismatch",
            f"{path} carries no `carved_from:` mapping. RULED OQ-I: the "
            "machine-read provenance record is `carved_from: {repository, "
            "commit}` in each assembly root's contracts/manifest.yaml — the "
            "wallet extraction's three records, one level down")
    for key, expected in (("repository", doc["source_repository"]),
                          ("commit", doc["carve_commit"])):
        got = carved.get(key)
        if got != expected:
            raise ArrivalRefusal(
                "arrival-carved-from-mismatch",
                f"{path} declares `carved_from.{key}: {got!r}` where the "
                f"manifest names {expected!r}. A provenance record that names "
                "another referent is worse than none: it is read by machines "
                "and it would send them to the wrong tree")
    tag = carved.get("carve_tag")
    declared_tag = doc.get("carve_tag")
    if tag is not None and declared_tag is not None and tag != declared_tag:
        raise ArrivalRefusal(
            "arrival-carved-from-mismatch",
            f"{path} declares `carved_from.carve_tag: {tag!r}` where the "
            f"manifest's label is {declared_tag!r}. The tag is a LABEL beside "
            "the commit and never the referent, but a label that names a "
            "different carve is a reader sent to the wrong one")
    return {"repository": str(carved.get("repository")),
            "commit": str(carved.get("commit"))}


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------

def verify_assembly_root(doc: dict[str, Any], repository: str,
                         dest_root: Path) -> dict[str, Any]:
    """An ASSEMBLY ROOT's `carved_from:` record, addressed BY THE REPOSITORY IT
    IS rather than by a manifest `destinations:` key.

    WHY THIS MODE EXISTS. RULED OQ-I puts the machine-read provenance record in
    EACH assembly root's `contracts/manifest.yaml`, and the runbook's § 6 and
    § 7 both write one. But `destinations:` is a map of the places ROWS GO, and
    the landed manifest declares `opendox_root` and no `openxdox_root` —
    openXdox's assembly root receives no row, so it has no key. Addressed only
    by key, half of the provenance the ruling requires would be uncheckable by
    the tool that checks the other half, and § 7's record would rest on a
    reading of the file by eye.

    The check itself is the same one: `carved_from.repository` and
    `carved_from.commit` name the manifest's source and carve commit. It does
    not depend on WHICH root is being read, which is exactly why a root the
    manifest never names can still be held to it. Where the repository IS a
    declared destination the key is reported beside it, so the two addressing
    modes agree on the roots they both reach.
    """
    if not REPOSITORY_RE.match(repository):
        raise ArrivalRefusal(
            "arrival-unreadable",
            f"--assembly-root {repository!r} is not an `<owner>/<name>` "
            "repository. This mode names the ASSEMBLY ROOT REPOSITORY rather "
            "than a `destinations:` key, because an assembly root that "
            "receives no row has no key — `opensoft/openXdox` is the measured "
            "case (RULED OQ-L, runbook § 7)")
    key = None
    for name, entry in (doc["destinations"] or {}).items():
        if not isinstance(entry, dict) or entry.get("repository") != repository:
            continue
        if entry.get("leg") != ASSEMBLY_LEG:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--assembly-root {repository!r} is destination {name!r}, "
                f"whose leg is {entry.get('leg')!r} and not "
                f"{ASSEMBLY_LEG!r}. RULED OQ-I puts `carved_from:` in the "
                "ASSEMBLY ROOTS and the four legs carry no `contracts/` at "
                f"all; verify a leg with `--destination {name}`")
        key = name
        break
    carved_from = check_carved_from(dest_root, doc)
    return {
        "result": "ok",
        "mode": "assembly-root",
        "assembly_root": repository,
        "destination": key,
        "repository": repository,
        "leg": ASSEMBLY_LEG,
        "dest_root": str(dest_root),
        "phase": None,
        "carve_commit": doc["carve_commit"],
        "carve_tag": doc.get("carve_tag"),
        "source_repository": doc["source_repository"],
        "declared_by_the_manifest": key is not None,
        "carved_from": carved_from,
    }


def verify(doc: dict[str, Any], destination: str, dest_root: Path,
           source_repo: Path, phase: str,
           declared_created: set[str], cli_created: set[str],
           replica_placements: dict[str, str],
           dest_base: str | None,
           admissions_file: Path | None) -> dict[str, Any]:
    """The checks in order, first failure wins.

    `declared_created` and `cli_created` are the SAME admission
    (`--allow-created`'s own meaning) from the two sources RULED #656 allows:
    the declared admissions file and the command line, kept apart here only so
    the summary can report which of each was actually needed — the union is
    what the walk itself admits against.
    """
    allow_created = declared_created | cli_created
    carve_commit = doc["carve_commit"]
    rows = rows_for(doc, destination)
    if rows or replica_placements:
        require_commit(source_repo, carve_commit)
    counts = check_arrivals(rows, dest_root, source_repo, carve_commit, phase)
    replica_counts = check_replicas(replica_placements, dest_root,
                                    source_repo, carve_commit, doc, phase)
    # A REPLICA'S DECLARED EDIT IS COUNTED WHERE A MOVED ROW'S IS (RULED Q-L7
    # (a)), in the two counters a reader already knows how to read, rather than
    # in two new summary fields that would ask every consumer to learn a second
    # accounting for the same event. `replicas_verified` keeps its own meaning:
    # the declared replicas whose presence and bytes were answered.
    counts["diffed"] += replica_counts["diffed"]
    counts["unapplied"] += replica_counts["unapplied"]
    replicas_verified = replica_counts["verified"]

    roots = declared_roots(rows)
    # A DECLARED replica is admitted BY NAME, so it no longer rides into the
    # walk on a coincidence of bytes: the operator said where it is, and that
    # path is the one admitted.
    placed = {row["destination_path"] for row in rows}
    placed.update(replica_placements.values())
    # EMPTY REPLICA BLOBS ADMIT NOTHING. Two of the landed manifest's 20
    # replica rows are `fixtures/empty/*/.gitkeep`, whose blob is empty, so an
    # admission by byte-identity would let ANY empty file under a declared root
    # — a created `__init__.py`, a truncated module — in as "a replica", which
    # is a true statement about the bytes and a false one about the file. The
    # `.gitkeep`-by-name rule already refused to call the scaffold's
    # placeholder a replica for the same reason; this is the rest of it.
    # A replica whose carve blob is empty is admitted only by `--replica-at`,
    # which admits BY NAME and is the stronger claim anyway.
    # A MOVED ROW THE MANIFEST ALSO REPLICATES HERE is admitted in the walk on
    # a replica's terms too (RULED Q-L7 (a)): the manifest says these bytes
    # arrive at this destination as a copy, so a file carrying exactly them is
    # no more undeclared than any other replica's. Where such a row DECLARES
    # LINES the arrived copy is edited and its bytes match nothing here, which
    # is the honest outcome — an edited replica must be DECLARED with
    # `--replica-at` to be read as one, and undeclared it refuses
    # `arrival-undeclared-file` naming that flag.
    replicas: set[str] = set()
    for row in [*replica_rows(doc), *also_replicated_rows(doc, destination)]:
        data = blob_at(source_repo, carve_commit, row["source_path"])
        if data:
            replicas.add(digest(data))
    admitted = check_undeclared_files(dest_root, roots, placed, replicas,
                                      allow_created, dest_base)

    leg = (doc["destinations"].get(destination) or {}).get("leg")
    carved_from = (check_carved_from(dest_root, doc)
                   if leg == ASSEMBLY_LEG else None)

    # WHICH ADMISSIONS WERE USED, AND WHICH DECLARED ONES WERE NOT NEEDED
    # (RULED #656): a stale declared admission — a `created:` entry the walk
    # never consumed, because the file it names is not there or is admitted
    # some other way — is a FINDING to report, not silence to pass through.
    used_created: set[str] = admitted["created_paths"]
    declared_admissions_used = sorted(declared_created & used_created)
    declared_admissions_unused = sorted(declared_created - used_created)
    ad_hoc_allow_created = sorted(cli_created)

    return {
        "result": "ok",
        "mode": "destination",
        "destination": destination,
        "repository": (doc["destinations"].get(destination) or {}).get(
            "repository"),
        "leg": leg,
        "dest_root": str(dest_root),
        "phase": phase,
        "dest_base": dest_base,
        "carve_commit": carve_commit,
        "carve_tag": doc.get("carve_tag"),
        "source_repository": doc["source_repository"],
        "rows": counts["rows"],
        "digests_verified": counts["digests_verified"],
        "declared_edits_diffed": counts["diffed"],
        "declared_edits_unapplied": counts["unapplied"],
        "replicas_declared": len(replica_placements),
        "replicas_verified": replicas_verified,
        "declared_roots": roots,
        "files_walked": admitted["walked"],
        "admitted": {k: admitted[k] for k in ("scaffold", "replica", "created")},
        "carved_from": carved_from,
        "admissions_file": str(admissions_file) if admissions_file else None,
        "declared_admissions_used": declared_admissions_used,
        "declared_admissions_unused": declared_admissions_unused,
        "ad_hoc_allow_created": ad_hoc_allow_created,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify-carve-arrival.py",
        description=("Verify a carve DESTINATION against "
                     "docs/opendox-carve-manifest.yaml — the destination half "
                     "of FLOOR PART 1 (split-opendox § D6, RULED OQ-1)."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--manifest", metavar="PATH", default=None,
        help=f"the manifest to read (default: <source-repo>/{MANIFEST_RELPATH})")
    parser.add_argument(
        "--destination", metavar="KEY", default=None,
        help="a KEY of the manifest's `destinations:` map, e.g. opendox_code")
    parser.add_argument(
        "--assembly-root", metavar="REPOSITORY", default=None,
        help=("verify an ASSEMBLY ROOT's `carved_from:` by the repository it "
              "is, e.g. opensoft/openXdox — the root that receives no row and "
              "therefore has no `destinations:` key (RULED OQ-I, OQ-L)"))
    parser.add_argument(
        "--dest-root", metavar="DIR", default=None,
        help="the destination checkout to verify")
    parser.add_argument(
        "--source-repo", metavar="DIR", default=None,
        help=("an openxFactory checkout or mirror carrying carve_commit, whose "
              "blobs the phase-B diff is taken against (default: this one)"))
    parser.add_argument(
        "--dest-base", metavar="REF", default=None,
        help=("the destination's PRE-CARVE revision, against which every "
              f"SCAFFOLD admission's bytes are checked (default: "
              f"{DEST_BASE_DEFAULT} where the destination is a git repository "
              "carrying it; without one the scaffold admissions are by name "
              "alone and the summary says so)"))
    parser.add_argument(
        "--phase", choices=PHASES, default=None,
        help=("A: every moved row byte-identical to the carve commit (commit "
              "A). B: declared-edit rows may differ ONLY on their declared "
              "lines (commit B)"))
    parser.add_argument(
        "--allow-created", metavar="PATH", action="append", default=[],
        help=("a file the destination legitimately assembles and no row places "
              "(RULED OQ-C); repeatable, exact destination-relative paths. "
              "The AD-HOC form — prefer a `created:` entry in the declared "
              "admissions file, RULED #656"))
    parser.add_argument(
        "--admissions", metavar="PATH", default=None,
        help=("the declared per-destination admissions file `--destination` "
              f"reads by default (default: beside the manifest, "
              f"{ADMISSIONS_BASENAME}). Its `created:` list for this "
              "destination is applied exactly as --allow-created admits "
              "(RULED #656) — the GOVERNED form: a new admission is a "
              "reviewed one-line diff in the pin-bump pull request"))
    parser.add_argument(
        "--replica-at", metavar="SOURCE=PATH", action="append", default=[],
        help=("where a `not_moved / replicated_at_destination` row landed at "
              "this destination — or a MOVED row whose `also_replicated_to:` "
              "lists this destination (RULED Q-L7 (a)); the manifest declares "
              "no path for a replica, so declaring one here makes the copy "
              "checkable"))
    parser.add_argument(
        "--json", action="store_true",
        help="print one JSON object on stdout instead of the human line")
    args = parser.parse_args(argv)

    source_repo = (Path(args.source_repo).resolve() if args.source_repo
                   else ROOT)
    # A RELATIVE `--manifest` resolves against `--source-repo`, not the
    # caller's CWD, on `validate-carve-manifest.py`'s reasoning: the help text
    # says "default: <source-repo>/…", and a relative override that silently
    # changed referent to CWD would read the wrong file the moment
    # `--source-repo` names a tree other than the one the caller stands in.
    if args.manifest:
        given = Path(args.manifest)
        manifest_path = (given if given.is_absolute()
                         else source_repo / given).resolve()
    else:
        manifest_path = (source_repo / MANIFEST_RELPATH).resolve()

    # `--admissions` resolves exactly as `--manifest` does — relative to
    # `--source-repo`, not the caller's CWD — for the same reason: a relative
    # override that silently changed referent to CWD would read the wrong
    # file the moment `--source-repo` names a tree other than the one the
    # caller stands in. The DEFAULT is beside the manifest
    # (`default_admissions_path`), so a `--manifest` override moves both
    # together.
    if args.admissions:
        given = Path(args.admissions)
        admissions_path = (given if given.is_absolute()
                           else source_repo / given).resolve()
    else:
        admissions_path = default_admissions_path(manifest_path)

    # THE SEAT-HOLDING PASS, and the one place here that is not fail-closed.
    # See the module docstring: it keys off `--destination` being ABSENT, never
    # off a lookup failing.
    if args.destination is None and args.assembly_root is None:
        known: list[str] = []
        unreadable = False
        try:
            known = sorted(read_manifest(manifest_path)["destinations"])
        except ArrivalRefusal:
            unreadable = True
        if args.json:
            # A LIST and never the human sentence: `--json` is consumed by
            # machines, and a field that is sometimes comma-joined prose and
            # sometimes an apology is a field every consumer has to parse twice.
            print(json.dumps({"result": "no-destination",
                              "manifest": str(manifest_path),
                              "destinations": known,
                              "destinations_unreadable": unreadable}))
        else:
            names = ("(the manifest could not be read)" if unreadable
                     else ", ".join(known))
            print(f"NO DESTINATION (nothing to verify; name one of: {names})")
        return 0

    where = args.dest_root or args.destination or args.assembly_root or "-"
    try:
        if args.destination is not None and args.assembly_root is not None:
            raise ArrivalRefusal(
                "arrival-unreadable",
                "--destination and --assembly-root name a destination two "
                "ways and this run would have to choose between them. "
                "`--destination` is a `destinations:` key and walks that "
                "destination's rows; `--assembly-root` is a repository and "
                "checks only `carved_from:`, for the root the manifest gives "
                "no key")
        doc = read_manifest(manifest_path)
        if args.dest_root is None:
            raise ArrivalRefusal(
                "arrival-unreadable",
                "--dest-root is required with --destination or "
                "--assembly-root: this verifier reads a destination checkout "
                "and has no default for one")
        dest_root = Path(args.dest_root).resolve()
        if not dest_root.is_dir():
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--dest-root {args.dest_root!r} resolves to {dest_root}, "
                "which is not a directory")
        where = str(dest_root)
        if args.assembly_root is not None:
            summary = verify_assembly_root(doc, args.assembly_root, dest_root)
            _print_ok(summary, args.json)
            return 0
        if args.destination not in doc["destinations"]:
            raise ArrivalRefusal(
                "arrival-unreadable",
                f"--destination {args.destination!r} is not a key of the "
                f"manifest's `destinations:` map ({', '.join(sorted(doc['destinations']))}). "
                "The seat-holding pass covers a run with NO destination, "
                "before the legs exist; it does not extend to one the caller "
                "named, because a typo must not be indistinguishable from "
                "`not yet carved`")
        if args.phase is None:
            raise ArrivalRefusal(
                "arrival-unreadable",
                "--phase is required with --destination and has no default. "
                "The two phases are the two commits a leg lands as (runbook "
                "§ 5.5), and a run that guessed would prove the weaker claim "
                "silently")
        declared_created = {
            entry["path"] for entry in
            read_admissions(admissions_path, doc).get(args.destination, [])}
        cli_created = {dest_relative(p, "--allow-created")
                       for p in args.allow_created}
        # THE NOTICE (RULED #656): --allow-created still works for an ad-hoc
        # run, but a caller using it is told the declared form is governed.
        # Only in HUMAN mode — `--json` promises ONE object on stdout, so the
        # same fact reaches a machine caller as `ad_hoc_allow_created` in the
        # summary instead of a second line breaking that contract.
        if args.allow_created and not args.json:
            print(
                "NOTE --allow-created is the AD-HOC form. The governed one "
                f"(RULED, openxFactory#656) is a `created:` entry in "
                f"{admissions_path}, applied automatically: add "
                f"`{{path: <path>, reason: <why>, since: <leg commit>}}` "
                f"under `destinations.{args.destination}.created`, "
                "alphabetically by path, as a reviewed one-line diff in the "
                "pin-bump pull request.", file=sys.stderr)
        summary = verify(doc, args.destination, dest_root, source_repo,
                         args.phase, declared_created, cli_created,
                         parse_replica_placements(args.replica_at, doc,
                                                  args.destination),
                         resolve_dest_base(dest_root, args.dest_base),
                         admissions_path if admissions_path.is_file()
                         else None)
    except ArrivalRefusal as exc:
        return _refused(exc, args, where)
    # THE EXIT CONTRACT, HELD BY CODE AND NOT BY INSPECTION. Everything above
    # refuses in this file's own vocabulary; anything that does not — a
    # `KeyError` from a manifest row missing `destination_path:`, an `OSError`
    # the checks did not name, a bug here — would otherwise leave `main()` as a
    # traceback and EXIT 1, which the module docstring says does not exist.
    # A guarantee a reader has to audit every raise site to believe is not a
    # guarantee, so it is enforced at the one place that owns the exit status.
    # It is `Exception` and not `BaseException`: a `KeyboardInterrupt` or a
    # `SystemExit` is the operator's act and must not be re-labelled a finding.
    except Exception as exc:  # noqa: BLE001 - see above
        return _refused(ArrivalRefusal(
            "arrival-unreadable",
            f"the run raised {type(exc).__name__}: {exc}. This verifier READS "
            "the manifest and does not repair it, so a document whose shape it "
            f"cannot follow is `{MANIFEST_VALIDATOR}`'s finding; anything else "
            "here is a defect in this file. Either way the answer is exit 2 — "
            "there is deliberately no exit 1"), args, where)

    _print_ok(summary, args.json)
    return 0


def _refused(exc: ArrivalRefusal, args: argparse.Namespace, where: str) -> int:
    """The ONE refusal exit: `--json` object or the rendered human message."""
    if args.json:
        print(json.dumps({"result": "refused", "code": exc.code,
                          "detail": exc.detail,
                          "destination": args.destination,
                          "assembly_root": args.assembly_root,
                          "dest_root": args.dest_root}))
    else:
        print(exc.render(where), file=sys.stderr)
    return 2


def _print_ok(summary: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary))
        return
    if summary["mode"] == "assembly-root":
        declared = ("destination " + str(summary["destination"])
                    if summary["declared_by_the_manifest"]
                    else "no `destinations:` key — the root receives no row")
        print(f"OK {summary['dest_root']}: assembly root "
              f"{summary['assembly_root']} ({declared}) — carved_from "
              f"{summary['carved_from']['repository']}@"
              f"{summary['carved_from']['commit'][:12]}, which is "
              f"{summary['source_repository']}@"
              f"{summary['carve_commit'][:12]} ({summary['carve_tag']})")
        return
    adm = summary["admitted"]
    roots = ", ".join(summary["declared_roots"]) or "(none declared)"
    line = (f"OK {summary['dest_root']}: {summary['destination']} "
            f"({summary['repository']}) at "
            f"{summary['source_repository']}@"
            f"{summary['carve_commit'][:12]} ({summary['carve_tag']}), "
            f"phase {summary['phase']} — {summary['rows']} row(s) arrived, "
            f"{summary['digests_verified']} digest(s) verified, "
            f"{summary['declared_edits_diffed']} declared-edit row(s) "
            f"within their lines, "
            f"{summary['declared_edits_unapplied']} unapplied; "
            f"{summary['replicas_verified']} of "
            f"{summary['replicas_declared']} declared replica(s) verified "
            f"(byte-identical, or — where the row declares lines — differing "
            f"only on them); "
            f"{summary['files_walked']} file(s) under {roots} with none "
            f"undeclared ({adm['scaffold']} scaffold, {adm['replica']} "
            f"replica, {adm['created']} created)")
    line += ("; scaffold admissions checked against "
             f"{summary['dest_base'][:12]}"
             if summary["dest_base"] is not None else
             "; scaffold admissions by NAME ONLY (no --dest-base and no "
             f"{DEST_BASE_DEFAULT} at the destination)")
    if summary["carved_from"] is not None:
        line += (f"; carved_from {summary['carved_from']['repository']}@"
                 f"{summary['carved_from']['commit'][:12]}")
    # WHICH ADMISSIONS WERE USED, AND WHICH DECLARED ONES WERE NOT NEEDED
    # (RULED #656) — a stale declared admission is a finding, printed here and
    # not only counted, so a reader does not have to reach for `--json` to see
    # it. `admissions_file` is None where the file is simply absent (feature
    # not yet adopted at this manifest), never where it was read and empty.
    if summary["admissions_file"] is not None:
        used = summary["declared_admissions_used"]
        unused = summary["declared_admissions_unused"]
        line += (f"; {len(used)} declared admission(s) used "
                 f"({Path(summary['admissions_file']).name})")
        if unused:
            line += (f", {len(unused)} STALE (declared but not needed): "
                     f"{', '.join(unused)}")
    if summary["ad_hoc_allow_created"]:
        line += (f"; {len(summary['ad_hoc_allow_created'])} admitted via "
                 "ad-hoc --allow-created (declare these in the admissions "
                 "file instead)")
    print(line)


if __name__ == "__main__":
    sys.exit(main())
