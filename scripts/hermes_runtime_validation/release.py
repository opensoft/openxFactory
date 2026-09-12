"""Closed release digest inventory build and exact-object verification (T068/T074).

The release digest inventory published at ``contracts/releases/<bundle-tag>.digests.yaml``
lists every release member as a repository-relative regular-file path together
with the SHA-256 of its raw Git blob bytes.  Membership is closed and derived
from the canonical registrations (research Decision 10); verification reads
mode and blob bytes from an exact commit through
``content.resolve_git_object`` and never trusts the working tree
(research Decision 11).  Findings use the ``HGR-RELEASE-*`` namespace; an
unavailable or unsafe dependency raises :class:`ReleaseDependencyError`
(CLI exit code 2).
"""

from __future__ import annotations

import hashlib
import posixpath
import re
import subprocess
from collections.abc import Iterable, Mapping
from pathlib import Path

import yaml

from scripts.hermes_runtime_validation.content import (
    CONTENT_PATH_ABSENT,
    ContentResolutionError,
    _sanitized_git_environment,
    resolve_git_object,
)

RELEASE_INVENTORY_KIND = "openxfactory-contract-release-digest-inventory"
RELEASE_REPOSITORY = "opensoft/openxFactory"
DIGEST_ALGORITHM = "sha256"
DIGEST_SOURCE = "raw_git_blob"
PATH_ORDER = "bytewise_utf8"

FAMILY_PREFIX = "contracts/hermes-runtime/"
FIXTURE_PREFIX = "contracts/hermes-runtime/fixtures/"
CATALOG_PATH = "contracts/hermes-runtime/contract-index.yaml"
FIXTURE_INDEX_PATH = "contracts/hermes-runtime/fixtures/index.yaml"
INVENTORY_SCHEMA_PATH = "contracts/releases/release-digest-inventory.schema.yaml"
MANIFEST_PATH = "contracts/manifest.yaml"
RELEASES_DIRECTORY = "contracts/releases"
VALIDATOR_PACKAGE = "scripts/hermes_runtime_validation"
INTENT_CONTRACT_PREFIX = "contracts/intent-compliance"
INTENT_IMPLEMENTATION_PACKAGE = "scripts/intent_compliance"
INTENT_TEST_PACKAGE = "tests/intent-compliance"
INTENT_VALIDATOR_PATH = "scripts/validate-intent-compliance.py"
INTENT_RELEASE_FLOOR = (2, 3)
INTENT_REQUIRED_REGISTRATIONS = (
    (
        "intent-compliance-veto-class-vocabulary",
        "contracts/intent-compliance/veto-class-vocabulary.schema.yaml",
        "schema",
    ),
    (
        "intent-compliance-policy-allowance",
        "contracts/intent-compliance/policy-allowance.schema.yaml",
        "schema",
    ),
    (
        "intent-compliance-policy-allowance-revocation",
        "contracts/intent-compliance/policy-allowance-revocation.schema.yaml",
        "schema",
    ),
    (
        "intent-compliance-policy-allowance-registry",
        "contracts/intent-compliance/policy-allowance-registry.schema.yaml",
        "schema",
    ),
    (
        "intent-compliance-decision",
        "contracts/intent-compliance/compliance-decision.schema.yaml",
        "schema",
    ),
    (
        "intent-compliance-conformance-validator",
        INTENT_VALIDATOR_PATH,
        "tool",
    ),
)

# The `contracts/clearing/` family (openxFactory issue #722): registered in
# `contracts/manifest.yaml`'s generic `contracts:` list with its own per-row
# sha256 — a closed-corpus mechanism `scripts/validate-clearing-dispatch.py`
# and `tests/clearing/test_clearing_manifest_rows.py` already enforce — but
# never a member of THIS inventory: `FAMILY_PREFIX` never pointed at it and no
# other block swept its paths in, so a cut's release-digest inventory stayed
# silent on the clearing family's contract bytes even across cuts that
# registered new clearing schemas. Unlike `INTENT_CONTRACT_PREFIX` above, this
# family needs no registration-completeness invariant of its own: the
# manifest rows already close that corpus, so `_collect_members` below only
# has to sweep the family's tree into the same closed membership every other
# family joins, conditional on presence alone (the same "join only when
# present at the source" reading `NORMATIVE_DOCS` uses) — AND, like
# `INTENT_CONTRACT_PREFIX`, gated by a release-semantic floor.
#
# RULED (Brett Heap, 2026-09-12 ~14:55Z, openxFactory #745, PR #1000 review
# thread PRRT_kwDOTAvnrs6hsjob). `_collect_members` is the canonical source
# `verify_inventory_against_commit` reads too, so an unconditional,
# presence-only join changes the meaning of ALREADY-PUBLISHED inventories:
# `contract-v4.0`'s own commit already contains the clearing family, but its
# recorded `contract-v4.0.digests.yaml` (cut before this family was swept in)
# does not list it — re-verifying that published tag against its own recorded
# inventory would newly report every clearing path `HGR-RELEASE-MEMBER-
# MISSING`, where it verified clean before this fix existed. `CLEARING_
# RELEASE_FLOOR` below closes that hole exactly the way `INTENT_RELEASE_FLOOR`
# already does: the family is a release member only for a declared bundle
# version at or after `(4, 1)` — the first cut that follows `contract-v4.0` —
# so every already-published tag through `contract-v4.0` keeps verifying
# exactly, and a build for a `(4, 1)`-or-later bundle is the first to record
# the family.
CLEARING_CONTRACT_PREFIX = "contracts/clearing"
CLEARING_TEST_PACKAGE = "tests/clearing"
CLEARING_VALIDATOR_PATH = "scripts/validate-clearing-dispatch.py"
CLEARING_RELEASE_FLOOR = (4, 1)

NAMED_VALIDATORS = (
    "scripts/validate-hermes-runtime-contracts.py",
    "scripts/validate-contract-release.py",
    "scripts/hermes-runtime-dataset-digest.py",
    "scripts/validate-ideation-dashboard-contracts.py",
    # CLEARING_VALIDATOR_PATH is NOT here: like INTENT_VALIDATOR_PATH, it
    # joins explicitly inside its own family's floor-gated block below, not
    # through this unconditional, presence-only loop.
)
AUXILIARY_MEMBERS = (
    "requirements/hermes-runtime-contracts.in",
    "requirements/hermes-runtime-contracts.lock",
    "tests/hermes_runtime_contracts/postgres/images.lock.yaml",
    INVENTORY_SCHEMA_PATH,
    "contracts/manifest.yaml",
    "contracts/CHANGELOG.md",
    "contracts/README.md",
)
NORMATIVE_DOCS = (
    "docs/contract-versioning-policy.md",
    "docs/xfactory-domain-factory-model.md",
    "docs/terminology-and-repo-topology.md",
)
RELEASE_SURFACE_PATHS = (
    "contracts/manifest.yaml",
    "contracts/CHANGELOG.md",
    "contracts/README.md",
    "contracts/hermes-runtime/README.md",
    "docs/contract-versioning-policy.md",
)



def _shed_aware(target: Path) -> Path:
    """`target`, or the pinned-leg copy of it when the § 5.2 shed moved it.

    RULED (a) POST-SHED MODE (`#656` comment `5625573095`). Three release
    members of this repository's own registration — `gate-action-record`,
    `xfactory-workbench-chat-turn` and `xfactory-workbench-model-catalog` — are
    `moved_verbatim` manifest rows, and every byte of them arrived unchanged, so
    the digest this source computes is the digest it has always computed. The
    containment check below is unaffected: a pinned leg is mounted INSIDE this
    repository, so a resolved destination is still under `self.root`.

    Answers `target` unchanged for any other repository, any path in no row, and
    any `not_moved` row — so a candidate-mode release run over a domain mirror
    is untouched.
    """
    try:
        from carved_reach import shed_destination
    except ImportError:
        return target
    moved = shed_destination(target)
    return moved if moved is not None else target


def _shed_aware_commit(root: Path, commit: str, path: str):
    """The pinned leg's `(repo, commit, path)` for a member the § 5.2 shed moved
    — or `None`, in which case this repository's own answer stands.

    `_shed_aware` above, in the direction `_CommitSource` reads: from one exact
    commit and never from the working tree. `content.resolve_git_object` reads
    ONE repository's object store, and post-shed the three moved members of this
    repository's own registration have their bytes in a LEG's, reachable from
    the verified commit through the gitlink THAT COMMIT records —
    `carved_reach.shed_commit_object` walks that chain and answers what to read
    instead.

    The exactness is preserved rather than traded away: the leg commit comes from
    the verified commit's own tree, so verifying an older commit reads the leg
    that commit pinned. A commit from BEFORE the shed records no such gitlink and
    answers `None`, which is right — there the member is still in this
    repository's tree and the ordinary read already found it. A root that is not
    this repository answers `None` too, so a candidate-mode run over a domain
    mirror is untouched.
    """
    try:
        from carved_reach import REPO_ROOT as CARVE_ROOT, shed_commit_object
    except ImportError:
        return None
    try:
        if Path(root).resolve() != CARVE_ROOT.resolve():
            return None
    except OSError:
        return None
    return shed_commit_object(commit, path)


class ReleaseDependencyError(RuntimeError):
    """An unavailable or unsafe release dependency (CLI exit code 2)."""

    exit_code = 2

    def __init__(self, message: str, *, code: str = "HGR-RELEASE-DEPENDENCY") -> None:
        super().__init__(message)
        self.code = code


def _finding(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _require_schema_pin(catalog_entry: Mapping[str, object]) -> int:
    """The catalog is read as raw YAML here, so a schema/release-schema member
    missing `contract_schema_version` must become a clean dependency error,
    not an int(None) traceback."""

    raw = catalog_entry.get("contract_schema_version")
    try:
        return int(raw)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ReleaseDependencyError(
            "catalog entry "
            f"{catalog_entry.get('contract_id')!r} declares no usable "
            f"contract_schema_version (got {raw!r})"
        ) from exc


def _sorted(findings: Iterable[Mapping[str, object]]) -> list[dict[str, str]]:
    return sorted(
        (dict(item) for item in findings),
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )


def _bytewise(paths: Iterable[str]) -> list[str]:
    return sorted(paths, key=lambda value: value.encode("utf-8"))


def _is_release_inventory_path(path: object) -> bool:
    return (
        isinstance(path, str)
        and path.startswith(RELEASES_DIRECTORY + "/")
        and path.endswith(".digests.yaml")
    )


def _run_git(
    repo: Path, *arguments: str, binary: bool = False, allow_failure: bool = False
) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), *arguments],
            capture_output=True,
            text=not binary,
            check=False,
            timeout=30,
            env=_sanitized_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReleaseDependencyError("Git command is unavailable") from exc
    if result.returncode != 0 and not allow_failure:
        raise ReleaseDependencyError("Git command failed")
    return result


def _full_commit(repo: Path, revision: str) -> str:
    result = _run_git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")
    commit = str(result.stdout).strip()
    if not commit:
        raise ReleaseDependencyError("exact commit is unavailable")
    return commit


def _list_tree(repo: Path, commit: str, prefix: str) -> list[str]:
    result = _run_git(
        repo,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        "--name-only",
        commit,
        "--",
        prefix,
        binary=True,
    )
    return [
        entry.decode("utf-8") for entry in bytes(result.stdout).split(b"\0") if entry
    ]


def _ls_remote(repo: Path, remote: str, *patterns: str) -> list[tuple[str, str]]:
    result = _run_git(repo, "ls-remote", remote, *patterns)
    rows: list[tuple[str, str]] = []
    for line in str(result.stdout).splitlines():
        if not line.strip():
            continue
        object_id, _, reference = line.partition("\t")
        rows.append((object_id.strip(), reference.strip()))
    return rows


def _resolve_remote_object(repo: Path, remote: str, object_id: str) -> None:
    """Make a remote-derived object locally readable before anything reads it.

    Online release verification asks the canonical remote what its ``main`` and
    its tags point at, then answers questions about those object ids inside the
    local clone.  The two halves have different ages: a clone is fixed at the
    moment it was taken, the remote's refs are not.  When ``main`` advances
    after the clone, every local operation over the advertised object fails for
    that reason alone -- ``git merge-base --is-ancestor`` exits 128, a tree read
    fails outright, and a blob read resolves to nothing.

    The obligation is therefore on the OPERAND rather than on any one
    comparison: resolve the object where it enters the local world, and all
    four of its readers are covered by construction.  Probe first, so the
    common case of an already-current clone costs nothing and the verifier
    performs no network write at all; fetch only the single named object, never
    a ref, so the clone's remote-tracking refs and ``FETCH_HEAD`` are left
    exactly as they were.

    Q1, MEASURED 2026-08-26 and decided on the measurement: no ref-fetch
    fallback.  ``git fetch <remote> <oid>`` against the canonical remote
    (``git@github.com:opensoft/openxFactory.git``) returned 0 for an object
    under no ref the clone tracked, twice -- by hand on the live failure, and
    from a depth-1 clone fetching a commit 25 behind the tip in 4.80s, well
    inside ``_run_git``'s 30-second cap.  A remote that declines to serve an
    advertised object is therefore the fail-closed case below, not a case for a
    speculative wider fetch nobody has needed.

    Raises ``ReleaseDependencyError`` naming the RETRIEVAL that failed, which
    is a fact about the environment rather than a verdict about the release.
    The reason names the fetch, the remote, the object and git's exit status,
    and deliberately claims NO cause beyond that: a fetch can fail for a
    refused credential, an unreachable host, a timeout or a remote that
    declines the object, and asserting one of them would be the same failure of
    diagnosis as announcing that reachability "could not be determined".
    Subprocess output is not embedded, following ``_run_git``'s own terseness
    and so that a remote URL never travels inside a dependency error.
    """

    probe = _run_git(
        repo, "cat-file", "-e", f"{object_id}^{{object}}", allow_failure=True
    )
    if probe.returncode == 0:
        return
    fetch = _run_git(
        repo,
        "fetch",
        "--no-tags",
        "--no-write-fetch-head",
        remote,
        object_id,
        allow_failure=True,
    )
    if fetch.returncode != 0:
        raise ReleaseDependencyError(
            f"remote object fetch failed: {remote} {object_id} "
            f"(git exit {fetch.returncode})"
        )
    confirm = _run_git(
        repo, "cat-file", "-e", f"{object_id}^{{object}}", allow_failure=True
    )
    if confirm.returncode != 0:
        raise ReleaseDependencyError(
            f"remote object fetch did not provide {object_id} from {remote}"
        )


def _is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    result = _run_git(
        repo, "merge-base", "--is-ancestor", ancestor, descendant, allow_failure=True
    )
    if result.returncode not in (0, 1):
        raise ReleaseDependencyError("commit reachability could not be determined")
    return result.returncode == 0


def _refuse_unreachable_in_a_shallow_clone(
    repo: Path, ancestor: str, descendant: str
) -> None:
    """Refuse a NEGATIVE ancestor verdict that a truncated history cannot earn.

    Resolving a remote-derived operand makes the OBJECT present.  It does not
    make the ANCESTRY present.  In a shallow clone the graft boundary tells git
    that a commit has no parents, so ``git merge-base --is-ancestor`` returns 1
    -- a definite "no" -- for a commit that is perfectly reachable on the real
    history.  Reporting that as ``HGR-RELEASE-*-UNREACHABLE`` would be a verdict
    invented from an absence, which is the same fault as reporting an absent
    object as unreachable and is what requirement 2 of
    ``fix-release-reachability-race`` forbids.

    The asymmetry is the whole rule, and it is why this is not a blanket refusal
    on shallow clones: a POSITIVE verdict is trustworthy in any store, because a
    path git found is a path that exists.  Only the NEGATIVE is suspect, so only
    the negative is re-examined -- which also keeps the cost off the common path,
    one ``rev-parse`` on the false branch and nothing at all otherwise.

    A shallow clone that genuinely holds a non-ancestor gets this refusal too,
    rather than the finding it would have earned.  That is deliberate: the
    verifier cannot tell the two apart, and a fail-closed dependency refusal
    naming the truncated history is the honest outcome for both.  Deepen the
    clone, or verify from a full one.

    Ruled by Brett on 2026-08-26 (fold-in of ``tasks.md`` § 6.4, raised on a
    measurement and independently on openxFactory pull request #390's review).
    """

    result = _run_git(repo, "rev-parse", "--is-shallow-repository", allow_failure=True)
    if result.returncode != 0 or str(result.stdout).strip() != "true":
        return
    raise ReleaseDependencyError(
        f"ancestry cannot be judged in a shallow clone: {ancestor} against {descendant}"
    )


def _resolution_established_absence(
    exc: ContentResolutionError, commit: str, path: str
) -> bool:
    """Whether ``exc`` established that ``path`` is absent from ``commit``'s tree.

    Fifteen refusals reach this from ``resolve_git_object`` and exactly one of
    them is a fact about the release: the tree was read and the path was not in
    it.  The other fourteen say the commit is not in the store, the repository
    cannot be opened, git cannot be run, the read timed out, the argument was
    malformed, or an unsafe or inexact object was refused — and none of them
    establishes anything about the release.

    Spelling all fifteen the same way is how a verification reports a surface
    it never read.  It fails in BOTH directions and the quiet one is worse: a
    failure on one side of a comparison manufactures a drift finding out of an
    environment fact, and a failure on BOTH sides makes two identical
    non-answers compare EQUAL and reports the surface undrifted, emitting
    nothing a reader could notice.  So everything but the one data condition
    becomes a fail-closed dependency refusal whose reason names the CONDITION
    OBSERVED rather than a conclusion about the release.

    The condition is read off the resolver's DECLARED code and never off its
    message (OD-4): a message is prose, and a near-miss match on edited prose
    would silently reclassify a safety refusal as release data.

    `HGR-RELEASE-PATH-UNRESOLVABLE` at the inventory-path read is deliberately
    NOT routed through here — it already emits a named finding rather than a
    silent value, and changing what a published finding code means to consumers
    is a contract question rather than a defect fix
    (`fix-content-resolution-conflation` OD-3, tasks.md § 7.1).
    """

    if exc.code == CONTENT_PATH_ABSENT:
        return True
    raise ReleaseDependencyError(
        f"release content could not be resolved at {commit}: {path}: {exc}"
    ) from exc


def _blob_object_id(repo: Path, commit: str, path: str) -> str | None:
    """The blob object id at ``commit``, or ``None`` ONLY for an established absence."""

    try:
        return resolve_git_object(repo, commit, path).blob_oid
    except ContentResolutionError as exc:
        _resolution_established_absence(exc, commit, path)
        return None


class _WorkingTreeSource:
    """Read the candidate release from repository working-tree bytes."""

    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def load_yaml(self, path: str) -> object:
        target = self.root / path
        try:
            text = target.read_text(encoding="utf-8")
        except OSError as exc:
            raise ReleaseDependencyError(
                f"release registration is unavailable: {path}"
            ) from exc
        return yaml.safe_load(text)

    def exists(self, path: str) -> bool:
        target = _shed_aware(self.root / path)
        return target.is_file() and not target.is_symlink()

    def list_python(self, package: str) -> list[str]:
        return [member for member in self.list_files(package) if member.endswith(".py")]

    def list_files(self, directory: str) -> list[str]:
        base = self.root / directory
        if not base.is_dir():
            return []
        members: list[str] = []
        for candidate in base.rglob("*"):
            if candidate.is_file() and not candidate.is_symlink():
                members.append(candidate.relative_to(self.root).as_posix())
        return members

    def list_release_inventories(self) -> list[str]:
        base = self.root / RELEASES_DIRECTORY
        if not base.is_dir():
            return []
        return _bytewise(
            candidate.relative_to(self.root).as_posix()
            for candidate in base.glob("*.digests.yaml")
            if candidate.is_file() and not candidate.is_symlink()
        )

    def read_member(self, path: str) -> tuple[bytes, str, str]:
        target = _shed_aware(self.root / path)
        # Defense in depth beneath the membership guard: a normalized path
        # outside the repository root is refused here too, so no caller of
        # this source can ever digest bytes from beyond the tree.
        try:
            target.resolve().relative_to(self.root.resolve())
        except ValueError:
            raise ReleaseDependencyError(
                f"release member path escapes the repository root: {path}",
                code="HGR-RELEASE-MEMBER-ESCAPES",
            ) from None
        if target.is_symlink() or not target.is_file():
            raise ContentResolutionError(
                f"release member is not a regular file: {path}"
            )
        data = target.read_bytes()
        mode = "100755" if target.stat().st_mode & 0o111 else "100644"
        digest = f"sha256:{hashlib.sha256(data).hexdigest()}"
        return data, mode, digest

    def head_commit(self) -> str:
        return _full_commit(self.root, "HEAD")


class _CommitSource:
    """Read a release from one exact commit; never from the working tree."""

    def __init__(self, repo_root: Path, commit: str) -> None:
        self.root = repo_root
        self.commit = commit

    def load_yaml(self, path: str) -> object:
        try:
            resolved = resolve_git_object(self.root, self.commit, path)
        except ContentResolutionError as exc:
            raise ReleaseDependencyError(
                f"release registration is unavailable at the pinned commit: {path}"
            ) from exc
        return yaml.safe_load(resolved.data)

    def exists(self, path: str) -> bool:
        """Presence at the pinned commit, or a refusal — never a manufactured absence.

        Four callers consume this answer as data: two decide whether a
        validator or a normative doc is a release member, one decides whether
        ``contracts/manifest.yaml`` is present at the commit, and one decides
        membership for a listed path.  A ``False`` produced by an environment
        failure is a verdict about the release read off a fact about the
        machine.
        """

        moved = _shed_aware_commit(self.root, self.commit, path)
        if moved is not None:
            try:
                resolve_git_object(*moved)
            except ContentResolutionError as leg_exc:
                _resolution_established_absence(leg_exc, moved[1], moved[2])
                return False
            return True
        try:
            resolve_git_object(self.root, self.commit, path)
        except ContentResolutionError as exc:
            _resolution_established_absence(exc, self.commit, path)
            return False
        return True

    def list_python(self, package: str) -> list[str]:
        return [entry for entry in self.list_files(package) if entry.endswith(".py")]

    def list_files(self, directory: str) -> list[str]:
        return _list_tree(self.root, self.commit, directory)

    def list_release_inventories(self) -> list[str]:
        return _bytewise(
            entry
            for entry in _list_tree(self.root, self.commit, RELEASES_DIRECTORY)
            if entry.endswith(".digests.yaml")
        )

    def read_member(self, path: str) -> tuple[bytes, str, str]:
        """The member's bytes AT THE PINNED COMMIT, from the leg when the shed
        moved it.

        THE LEG IS ASKED FIRST, not as a fallback (Copilot
        `PRRT_kwDOTAvnrs6hfEoe`). A post-shed commit whose tree still carries a
        stale file at the pre-shed source path would satisfy the ordinary read,
        and a fallback-shaped order would then hash THOSE bytes and call the
        release verified. For a MOVED row the destination is what this
        repository publishes, so it is the only answer; `_shed_aware_commit`
        answers `None` for every row that stayed, for a path in no row, for a
        root that is not this repository and for a commit from before the shed
        (its tree records no such gitlink), which is what keeps the ordinary
        read the answer everywhere else.
        """
        moved = _shed_aware_commit(self.root, self.commit, path)
        if moved is not None:
            resolved = resolve_git_object(*moved)
        else:
            resolved = resolve_git_object(self.root, self.commit, path)
        return resolved.data, resolved.git_mode, resolved.digest


def _classify_type(path: str) -> str:
    if path == "contracts/manifest.yaml":
        return "manifest"
    if path == "contracts/CHANGELOG.md":
        return "changelog"
    if path in {
        "requirements/hermes-runtime-contracts.in",
        "requirements/hermes-runtime-contracts.lock",
    }:
        return "requirements"
    if path == "tests/hermes_runtime_contracts/postgres/images.lock.yaml":
        return "image-lock"
    if path.startswith("scripts/") and path.endswith(".py"):
        return "validator"
    if path.endswith(".schema.yaml"):
        return "schema"
    if path.endswith(".sql"):
        return "migration" if "/migrations/" in path else "sql"
    if path.startswith(FIXTURE_PREFIX):
        return "fixture"
    return "documentation"


def _artifact_id(path: str) -> str:
    return path.lower().replace("/", "-")


def _collect_members(
    source: _WorkingTreeSource | _CommitSource,
) -> tuple[list[str], dict[str, Mapping[str, object]]]:
    catalog = source.load_yaml(CATALOG_PATH)
    if not isinstance(catalog, Mapping):
        raise ReleaseDependencyError("contract catalog is not a mapping")
    catalog_map: dict[str, Mapping[str, object]] = {}
    members: set[str] = set()
    for entry in catalog.get("contracts", []) or []:
        if not isinstance(entry, Mapping):
            continue
        # Invariant (FR-032): a contract the catalog marks as a semantic member
        # must also be a release member. A catalog that marks a file semantic
        # but not release-member would silently drop it from the closed bundle,
        # so fail closed as an unusable dependency input instead.
        if entry.get("semantic_member") and not entry.get("release_member"):
            contract_id = entry.get("contract_id") or entry.get("path") or "<unknown>"
            raise ReleaseDependencyError(
                "catalog marks a semantic member that is not a release member: "
                f"{contract_id}",
                code="HGR-RELEASE-SEMANTIC-NOT-RELEASED",
            )
        if not entry.get("release_member"):
            continue
        relative = entry.get("path")
        if not isinstance(relative, str):
            continue
        # Catalog paths are family-relative; `..` segments let the canonical
        # index name cross-family release members (the doxBench wire schemas
        # live in contracts/schemas/). Normalized here so both the working-tree
        # and the git-object sources see one canonical repo path.
        repo_path = posixpath.normpath(FAMILY_PREFIX + relative)
        # Fail closed on a path that would leave the repository: content from
        # outside the tree must never be digested into a release inventory
        # (PR #45 review finding 1).
        if repo_path == ".." or repo_path.startswith("../"):
            raise ReleaseDependencyError(
                f"catalog path escapes the repository after normalization: {relative}",
                code="HGR-RELEASE-MEMBER-ESCAPES",
            )
        # Two DISTINCT entries normalizing to one repository file would let a
        # silent overwrite swap catalog metadata inside the closed membership
        # (PR #45 review blocker 5) — refuse loudly instead.
        if repo_path in catalog_map:
            raise ReleaseDependencyError(
                "two catalog entries normalize to the same release member: "
                f"{relative!r} -> {repo_path}",
                code="HGR-RELEASE-MEMBER-COLLISION",
            )
        catalog_map[repo_path] = entry
        members.add(repo_path)

    manifest = source.load_yaml(MANIFEST_PATH)
    if not isinstance(manifest, Mapping):
        raise ReleaseDependencyError("contract manifest is not a mapping")
    raw_bundle_tag = manifest.get("contract_bundle_version")
    bundle_match = (
        re.fullmatch(r"contract-v(\d+)\.(\d+)", raw_bundle_tag)
        if isinstance(raw_bundle_tag, str)
        else None
    )
    release_version = (
        (int(bundle_match.group(1)), int(bundle_match.group(2)))
        if bundle_match is not None
        else None
    )
    intent_floor_active = (
        release_version is not None and release_version >= INTENT_RELEASE_FLOOR
    )
    # Same computation, same `release_version`, for the clearing family's own
    # floor (RULED, #745, PR #1000 thread PRRT_kwDOTAvnrs6hsjob) — a version
    # this cannot parse (`release_version is None`) gates OFF exactly as it
    # does for intent, so an un-declared or malformed bundle never gains a
    # member it cannot make sense of.
    clearing_floor_active = (
        release_version is not None and release_version >= CLEARING_RELEASE_FLOOR
    )
    intent_registrations = []
    for entry in manifest.get("contracts", []) or []:
        if not isinstance(entry, Mapping):
            continue
        identifier = entry.get("id")
        path = entry.get("path")
        if (
            isinstance(identifier, str) and identifier.startswith("intent-compliance-")
        ) or (
            isinstance(path, str)
            and (
                path.startswith(INTENT_CONTRACT_PREFIX + "/")
                or path == INTENT_VALIDATOR_PATH
            )
        ):
            intent_registrations.append(entry)

    intent_contract_members = source.list_files(INTENT_CONTRACT_PREFIX)
    intent_implementation_members = source.list_python(INTENT_IMPLEMENTATION_PACKAGE)
    intent_test_members = source.list_python(INTENT_TEST_PACKAGE)
    intent_surface_present = bool(
        intent_contract_members
        or intent_implementation_members
        or intent_test_members
        or source.exists(INTENT_VALIDATOR_PATH)
    )

    if intent_floor_active or intent_registrations or intent_surface_present:
        registration_identities = [
            (entry.get("id"), entry.get("path"), entry.get("type"))
            for entry in intent_registrations
        ]
        registrations_by_identity = {
            identity: entry
            for identity, entry in zip(
                registration_identities, intent_registrations, strict=True
            )
        }
        missing = set(INTENT_REQUIRED_REGISTRATIONS) - registrations_by_identity.keys()
        unexpected = registrations_by_identity.keys() - set(
            INTENT_REQUIRED_REGISTRATIONS
        )
        registrations_are_exact = (
            len(registration_identities) == len(INTENT_REQUIRED_REGISTRATIONS)
            and not missing
            and not unexpected
        )
        if missing or (intent_floor_active and not registrations_are_exact):
            missing_ids = ", ".join(sorted(identifier for identifier, _, _ in missing))
            unexpected_ids = ", ".join(
                sorted(str(identifier) for identifier, _, _ in unexpected)
            )
            raise ReleaseDependencyError(
                "intent-compliance release registration must contain exactly six "
                "canonical tuples; missing: "
                f"{missing_ids or '<none>'}; unexpected: "
                f"{unexpected_ids or '<none>'}",
                code="HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE",
            )
        for identity in INTENT_REQUIRED_REGISTRATIONS:
            identifier, path, artifact_type = identity
            if not source.exists(path):
                raise ReleaseDependencyError(
                    f"intent-compliance required release member is unavailable: {path}",
                    code="HGR-RELEASE-INTENT-MEMBER-MISSING",
                )
            members.add(path)
            if artifact_type != "schema":
                continue
            registration = registrations_by_identity[identity]
            catalog_map[path] = {
                "contract_id": identifier,
                "contract_schema_version": registration.get("schema_version"),
                "type": artifact_type,
            }
        for member in intent_contract_members:
            members.add(member)
        for member in intent_implementation_members:
            members.add(member)
        for member in intent_test_members:
            members.add(member)
        members.add(INTENT_VALIDATOR_PATH)
        members.add("scripts/__init__.py")

    # Clearing family (issue #722), floor-gated (RULED, #745, PR #1000 thread
    # PRRT_kwDOTAvnrs6hsjob): the whole `contracts/clearing/` tree (schemas,
    # registry instance, README, packaged examples), its pytest wiring, and
    # `CLEARING_VALIDATOR_PATH` join the closed membership only for a
    # declared bundle at or after `CLEARING_RELEASE_FLOOR` — mirroring how
    # `INTENT_VALIDATOR_PATH` above joins inside the intent floor's own gate
    # rather than through the unconditional `NAMED_VALIDATORS` loop below.
    # Below the floor (every already-published tag through `contract-v4.0`)
    # this adds nothing, whether or not the tree already carries the family:
    # presence alone is not sufficient, because membership without the floor
    # is exactly what made re-verifying an already-published tag disagree
    # with what it already recorded. At or after the floor this still only
    # joins what is actually present at the source (a build for a bundle past
    # the floor, cut before the family itself lands, sweeps in nothing) — the
    # same "join only when present" reading `NORMATIVE_DOCS` uses.
    if clearing_floor_active:
        for member in source.list_files(CLEARING_CONTRACT_PREFIX):
            members.add(member)
        for member in source.list_python(CLEARING_TEST_PACKAGE):
            members.add(member)
        if source.exists(CLEARING_VALIDATOR_PATH):
            members.add(CLEARING_VALIDATOR_PATH)

    fixture_index = source.load_yaml(FIXTURE_INDEX_PATH)
    if not isinstance(fixture_index, Mapping):
        raise ReleaseDependencyError("fixture index is not a mapping")
    for case in fixture_index.get("cases", []) or []:
        if not isinstance(case, Mapping):
            continue
        for raw_input in case.get("inputs", []) or []:
            if isinstance(raw_input, str):
                members.add(FIXTURE_PREFIX + raw_input)

    for member in source.list_python(VALIDATOR_PACKAGE):
        members.add(member)
    for validator in NAMED_VALIDATORS:
        if source.exists(validator):
            members.add(validator)
    # Decision-10 mandatory auxiliaries are unconditional release members: each
    # is added with no exists() guard, mirroring how the catalog release_member
    # entries are added above. An auxiliary absent at the pinned commit then
    # surfaces downstream as a read_member/ContentResolutionError dependency
    # failure rather than being silently omitted from the closed bundle, which
    # preserves FR-032's guarantee that every required semantic file is pinned.
    for extra in AUXILIARY_MEMBERS:
        members.add(extra)
    # Normative docs are genuinely conditional ("modified normative docs") and
    # join the bundle only when present at the source.
    for extra in NORMATIVE_DOCS:
        if source.exists(extra):
            members.add(extra)

    members = {member for member in members if not _is_release_inventory_path(member)}
    return _bytewise(members), catalog_map


def _entry_for(
    path: str,
    catalog_map: Mapping[str, Mapping[str, object]],
    git_mode: str,
    digest: str,
) -> dict[str, object]:
    catalog_entry = catalog_map.get(path)
    if catalog_entry is not None:
        artifact_type = str(catalog_entry.get("type", _classify_type(path)))
        entry: dict[str, object] = {
            "artifact_id": str(catalog_entry.get("contract_id", _artifact_id(path))),
            "path": path,
            "type": artifact_type,
            "git_mode": git_mode,
        }
        if artifact_type in {"schema", "release-schema"}:
            entry["schema_id"] = str(catalog_entry.get("contract_id"))
            entry["schema_version"] = _require_schema_pin(catalog_entry)
        entry["digest"] = digest
        return entry
    return {
        "artifact_id": _artifact_id(path),
        "path": path,
        "type": _classify_type(path),
        "git_mode": git_mode,
        "digest": digest,
    }


def _build_inventory(
    source: _WorkingTreeSource | _CommitSource, *, bundle_tag: str
) -> dict[str, object]:
    members, catalog_map = _collect_members(source)
    entries: list[dict[str, object]] = []
    for path in members:
        _, git_mode, digest = source.read_member(path)
        entries.append(_entry_for(path, catalog_map, git_mode, digest))
    entries.sort(key=lambda entry: str(entry["path"]).encode("utf-8"))
    return {
        "schema_version": 1,
        "kind": RELEASE_INVENTORY_KIND,
        "bundle_tag": bundle_tag,
        "repository": RELEASE_REPOSITORY,
        "digest_algorithm": DIGEST_ALGORITHM,
        "digest_source": DIGEST_SOURCE,
        "path_order": PATH_ORDER,
        "entries": entries,
    }


def release_membership(repo_root: Path) -> list[Path]:
    """Return the closed, bytewise-sorted release membership from the working tree."""

    members, _ = _collect_members(_WorkingTreeSource(repo_root))
    return [Path(member) for member in members]


def build_release_inventory(repo_root: Path, *, bundle_tag: str) -> dict[str, object]:
    """Build the candidate inventory from working-tree bytes; excludes itself."""

    return _build_inventory(_WorkingTreeSource(repo_root), bundle_tag=bundle_tag)


def dump_inventory(inventory: Mapping[str, object]) -> str:
    """Serialize an inventory deterministically for byte-stable candidate output."""

    return yaml.safe_dump(dict(inventory), sort_keys=False, allow_unicode=False)


def _inventory_path_for_tag(tag: str) -> str:
    return f"{RELEASES_DIRECTORY}/{tag}.digests.yaml"


def _manifest_bundle_tag(source: object) -> str | None:
    if not source.exists(MANIFEST_PATH):  # type: ignore[attr-defined]
        return None
    manifest = source.load_yaml(MANIFEST_PATH)  # type: ignore[attr-defined]
    if not isinstance(manifest, Mapping):
        return None
    tag = manifest.get("contract_bundle_version")
    return tag if isinstance(tag, str) else None


def _load_inventory(source: object, path: str) -> dict[str, object] | None:
    if not source.exists(path):  # type: ignore[attr-defined]
        return None
    document = source.load_yaml(path)  # type: ignore[attr-defined]
    if not isinstance(document, Mapping):
        raise ReleaseDependencyError("release inventory is not a mapping")
    return dict(document)


def resolve_committed_inventory(
    repo_root: Path, commit: str
) -> tuple[str, dict[str, object]] | None:
    """Return the current release inventory recorded at ``commit`` or ``None``.

    The current bundle is resolved from ``contracts/manifest.yaml`` at the exact
    commit so that historical inventories from earlier releases are ignored.
    """

    commit_oid = _full_commit(repo_root, commit)
    source = _CommitSource(repo_root, commit_oid)
    tag = _manifest_bundle_tag(source)
    if tag is None:
        return None
    inventory_path = _inventory_path_for_tag(tag)
    document = _load_inventory(source, inventory_path)
    if document is None:
        return None
    return inventory_path, document


def verify_inventory_against_commit(
    repo_root: Path, commit: str, inventory: Mapping[str, object]
) -> list[dict[str, str]]:
    """Verify an inventory against exact commit bytes, ignoring the working tree."""

    commit_oid = _full_commit(repo_root, commit)
    source = _CommitSource(repo_root, commit_oid)
    bundle_tag = inventory.get("bundle_tag")
    canonical = _build_inventory(
        source, bundle_tag=bundle_tag if isinstance(bundle_tag, str) else ""
    )
    canonical_by_path = {str(entry["path"]): entry for entry in canonical["entries"]}

    findings: list[dict[str, str]] = []
    if "commit" in inventory:
        findings.append(
            _finding(
                "HGR-RELEASE-SELF-REFERENCE",
                "commit",
                "release inventory must not record its own commit",
            )
        )

    provided = [
        entry
        for entry in (inventory.get("entries", []) or [])
        if isinstance(entry, Mapping)
    ]
    provided_paths = [str(entry.get("path")) for entry in provided]
    if provided_paths != _bytewise(provided_paths):
        findings.append(
            _finding(
                "HGR-RELEASE-PATH-ORDER",
                "entries",
                "entries must be bytewise sorted by path",
            )
        )
    seen: set[str] = set()
    for path in provided_paths:
        if path in seen:
            findings.append(
                _finding(
                    "HGR-RELEASE-PATH-DUPLICATE",
                    path,
                    "duplicate inventory path",
                )
            )
        seen.add(path)

    observed: set[str] = set()
    for entry in provided:
        path = str(entry.get("path"))
        observed.add(path)
        if _is_release_inventory_path(path):
            findings.append(
                _finding(
                    "HGR-RELEASE-SELF-REFERENCE",
                    path,
                    "release inventory must not contain a release inventory instance",
                )
            )
            continue
        try:
            _, git_mode, digest = source.read_member(path)
        except ContentResolutionError:
            findings.append(
                _finding(
                    "HGR-RELEASE-PATH-UNRESOLVABLE",
                    path,
                    "inventory path is not an exact regular-file Git object",
                )
            )
            continue
        canonical_entry = canonical_by_path.get(path)
        if canonical_entry is None:
            findings.append(
                _finding(
                    "HGR-RELEASE-MEMBER-EXTRA",
                    path,
                    "inventory path is not a closed release member",
                )
            )
            continue
        if entry.get("digest") != digest:
            findings.append(
                _finding(
                    "HGR-RELEASE-DIGEST-MISMATCH",
                    path,
                    "digest does not match the raw Git blob at the pinned commit",
                )
            )
        if entry.get("git_mode") != git_mode:
            findings.append(
                _finding(
                    "HGR-RELEASE-MODE-MISMATCH",
                    path,
                    "git_mode does not match the pinned commit",
                )
            )
        if entry.get("type") != canonical_entry["type"]:
            findings.append(
                _finding(
                    "HGR-RELEASE-TYPE-MISMATCH",
                    path,
                    "artifact type does not match the canonical registration",
                )
            )
        canonical_schema_id = canonical_entry.get("schema_id")
        if canonical_schema_id is not None:
            if entry.get("schema_id") != canonical_schema_id or entry.get(
                "schema_version"
            ) != canonical_entry.get("schema_version"):
                findings.append(
                    _finding(
                        "HGR-RELEASE-SCHEMA-PIN-MISMATCH",
                        path,
                        "schema pin does not match the canonical registration",
                    )
                )
        elif "schema_id" in entry or "schema_version" in entry:
            findings.append(
                _finding(
                    "HGR-RELEASE-SCHEMA-PIN-MISMATCH",
                    path,
                    "non-schema member must not declare a schema pin",
                )
            )

    for path in canonical_by_path:
        if path not in observed:
            findings.append(
                _finding(
                    "HGR-RELEASE-MEMBER-MISSING",
                    path,
                    "required release member is absent from the inventory",
                )
            )
    return _sorted(findings)


def _surface_drift(repo_root: Path, commit: str, main_oid: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    surfaces = set(RELEASE_SURFACE_PATHS)
    surfaces.update(_CommitSource(repo_root, commit).list_release_inventories())
    surfaces.update(_CommitSource(repo_root, main_oid).list_release_inventories())
    for path in _bytewise(surfaces):
        if _blob_object_id(repo_root, commit, path) != _blob_object_id(
            repo_root, main_oid, path
        ):
            findings.append(
                _finding(
                    "HGR-RELEASE-SURFACE-DRIFT",
                    path,
                    "reviewed release-surface blob drifted from published main",
                )
            )
    return findings


def verify_promotion(
    repo_root: Path, *, commit: str, remote: str, tag: str
) -> list[dict[str, str]]:
    """Prove a candidate is promotable immediately before tagging."""

    commit_oid = _full_commit(repo_root, commit)
    findings: list[dict[str, str]] = []

    if _ls_remote(repo_root, remote, f"refs/tags/{tag}"):
        findings.append(
            _finding(
                "HGR-RELEASE-TAG-EXISTS",
                f"refs/tags/{tag}",
                "the bundle tag already exists on the remote",
            )
        )

    main_rows = _ls_remote(repo_root, remote, "refs/heads/main")
    if not main_rows:
        raise ReleaseDependencyError("remote main is unavailable")
    main_oid = main_rows[0][0]
    # Resolve the live operand where it enters the local world: the ancestor
    # check below and BOTH of `_surface_drift`'s reads at :732 answer out of the
    # local object store.
    _resolve_remote_object(repo_root, remote, main_oid)

    if not _is_ancestor(repo_root, commit_oid, main_oid):
        _refuse_unreachable_in_a_shallow_clone(repo_root, commit_oid, main_oid)
        findings.append(
            _finding(
                "HGR-RELEASE-CANDIDATE-UNREACHABLE",
                commit_oid,
                "the reviewed candidate is not reachable from remote main",
            )
        )

    findings.extend(_surface_drift(repo_root, commit_oid, main_oid))
    findings.extend(_verify_release_at(repo_root, commit_oid, tag))
    return _sorted(findings)


def _verify_release_at(
    repo_root: Path, commit_oid: str, tag: str
) -> list[dict[str, str]]:
    """Verify the tag-named inventory and its version agreement at a commit."""

    findings: list[dict[str, str]] = []
    source = _CommitSource(repo_root, commit_oid)
    inventory_path = _inventory_path_for_tag(tag)
    inventory = _load_inventory(source, inventory_path)
    if inventory is None:
        findings.append(
            _finding(
                "HGR-RELEASE-INVENTORY-MISSING",
                inventory_path,
                "the pinned commit records no release digest inventory for the tag",
            )
        )
        return findings
    if inventory.get("bundle_tag") != tag:
        findings.append(
            _finding(
                "HGR-RELEASE-BUNDLE-TAG-MISMATCH",
                inventory_path,
                "inventory bundle_tag does not match the release tag",
            )
        )
    if _manifest_bundle_tag(source) != tag:
        findings.append(
            _finding(
                "HGR-RELEASE-VERSION-MISMATCH",
                MANIFEST_PATH,
                "manifest contract_bundle_version does not match the release tag",
            )
        )
    findings.extend(verify_inventory_against_commit(repo_root, commit_oid, inventory))
    return findings


def verify_tag(repo_root: Path, *, remote: str, tag: str) -> list[dict[str, str]]:
    """Prove a published annotated tag peels to a verified main-line release."""

    findings: list[dict[str, str]] = []
    # An exact ref query does not peel annotated tags; a glob does. Filter the
    # glob result back to the exact ref and its peel to avoid prefix collisions.
    rows = _ls_remote(repo_root, remote, f"refs/tags/{tag}*")
    direct = [row for row in rows if row[1] == f"refs/tags/{tag}"]
    peeled = [row for row in rows if row[1] == f"refs/tags/{tag}^{{}}"]
    if not direct:
        findings.append(
            _finding(
                "HGR-RELEASE-TAG-MISSING",
                f"refs/tags/{tag}",
                "the bundle tag is absent on the remote",
            )
        )
        return _sorted(findings)
    if not peeled:
        findings.append(
            _finding(
                "HGR-RELEASE-TAG-NOT-ANNOTATED",
                f"refs/tags/{tag}",
                "the bundle tag is not an annotated tag object",
            )
        )
    peeled_commit = peeled[0][0] if peeled else direct[0][0]
    # A tag published since the clone was taken is absent for the same reason
    # main's new tip is, and `_verify_release_at` at :816 walks this commit's
    # tree and blobs locally.
    _resolve_remote_object(repo_root, remote, peeled_commit)

    main_rows = _ls_remote(repo_root, remote, "refs/heads/main")
    if not main_rows:
        raise ReleaseDependencyError("remote main is unavailable")
    main_oid = main_rows[0][0]
    _resolve_remote_object(repo_root, remote, main_oid)
    if not _is_ancestor(repo_root, peeled_commit, main_oid):
        _refuse_unreachable_in_a_shallow_clone(repo_root, peeled_commit, main_oid)
        findings.append(
            _finding(
                "HGR-RELEASE-TAG-UNREACHABLE",
                peeled_commit,
                "the tagged commit is not reachable from published main",
            )
        )

    findings.extend(_verify_release_at(repo_root, peeled_commit, tag))
    return _sorted(findings)


def _load_inventory_schema() -> dict[str, object]:
    schema_path = Path(__file__).resolve().parents[2] / INVENTORY_SCHEMA_PATH
    document = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ReleaseDependencyError("release inventory schema is unavailable")
    return document


def inventory_schema_findings(
    inventory: Mapping[str, object], *, path: str
) -> list[dict[str, str]]:
    """Return structural findings for an inventory instance against the schema."""

    from jsonschema import Draft202012Validator, FormatChecker

    schema = _load_inventory_schema()
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    if next(iter(validator.iter_errors(inventory)), None) is None:
        return []
    return [
        _finding(
            "HGR-RELEASE-INVENTORY-SHAPE",
            path,
            "release inventory does not satisfy its self-contained schema",
        )
    ]


def _catalog_pin_findings(
    catalog: Mapping[str, object], inventory: Mapping[str, object]
) -> list[dict[str, str]]:
    schema_pins: dict[str, int] = {}
    for entry in catalog.get("contracts", []) or []:
        if (
            isinstance(entry, Mapping)
            and entry.get("release_member")
            and entry.get("type") in {"schema", "release-schema"}
        ):
            schema_pins[str(entry.get("contract_id"))] = _require_schema_pin(entry)
    inventory_pins = {
        str(entry.get("schema_id")): entry.get("schema_version")
        for entry in (inventory.get("entries", []) or [])
        if isinstance(entry, Mapping)
        and entry.get("type") in {"schema", "release-schema"}
        and entry.get("schema_id")
    }
    findings: list[dict[str, str]] = []
    for schema_id, version in schema_pins.items():
        if inventory_pins.get(schema_id) != version:
            findings.append(
                _finding(
                    "HGR-RELEASE-SCHEMA-PIN-MISMATCH",
                    schema_id,
                    "catalog schema pin is not reproduced by the release inventory",
                )
            )
    return findings


def validate_candidate(
    repo_root: Path, *, catalog: Mapping[str, object]
) -> list[dict[str, str]]:
    """Validate the realized inventory against the exact HEAD candidate commit."""

    source = _WorkingTreeSource(repo_root)
    tag = _manifest_bundle_tag(source)
    document = None
    inventory_path = _inventory_path_for_tag(tag) if tag else RELEASES_DIRECTORY
    if tag is not None:
        document = _load_inventory(source, inventory_path)
    if document is None:
        return [
            _finding(
                "HGR-RELEASE-INVENTORY-MISSING",
                inventory_path,
                "no realized release digest inventory is present for the candidate",
            )
        ]
    findings = inventory_schema_findings(document, path=inventory_path)
    if findings:
        return _sorted(findings)
    if document.get("bundle_tag") != tag:
        findings.append(
            _finding(
                "HGR-RELEASE-BUNDLE-TAG-MISMATCH",
                inventory_path,
                "inventory bundle_tag does not match the manifest bundle version",
            )
        )
    head = source.head_commit()
    findings.extend(verify_inventory_against_commit(repo_root, head, document))
    findings.extend(_catalog_pin_findings(catalog, document))
    return _sorted(findings)


def validate_realization(
    repo_root: Path, *, catalog: Mapping[str, object], remote: str = "origin"
) -> list[dict[str, str]]:
    """Validate the realized inventory plus the published annotated tag."""

    findings = validate_candidate(repo_root, catalog=catalog)
    if any(
        finding["code"]
        in {"HGR-RELEASE-INVENTORY-MISSING", "HGR-RELEASE-INVENTORY-SHAPE"}
        for finding in findings
    ):
        return findings
    bundle_tag = _manifest_bundle_tag(_WorkingTreeSource(repo_root))
    if not isinstance(bundle_tag, str):
        return _sorted(
            [
                *findings,
                _finding(
                    "HGR-RELEASE-VERSION-MISMATCH",
                    MANIFEST_PATH,
                    "manifest declares no contract_bundle_version for realization",
                ),
            ]
        )
    findings.extend(verify_tag(repo_root, remote=remote, tag=bundle_tag))
    return _sorted(findings)
