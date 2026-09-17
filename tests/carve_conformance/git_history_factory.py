"""A reader whose corpus is GIT HISTORY, and the transposition it addresses —
openxFactory's own evidence that RULED Q-F1 (a) works end to end.

WHAT THIS IS NOT. It is not a destination's reader, it is not shipped as one,
and no verdict about openDox or openXdox may be read off it. openDox's real
reader is `opendox.runtime.local_git_adapter.LocalGitCorpus` and its
transposition is `opendox.runtime.conformance_corpus.transpose()`, both of them
openDox's own, in openDox's own repository, measured by a run recorded in
openDox's own pull request.

WHAT IT IS FOR. RULED Q-F1 (a) (Brett Heap, 2026-09-17, `#656` comment
`5714365086`) lets a destination whose corpus is history rather than a working
tree TRANSPOSE the neutral corpus into the storage form its reader addresses,
bytes unchanged, and obliges `verify-carve-conformance.py` to prove the
transposition faithful. A claim of that shape has to be tested against a reader
of that shape, and openxFactory's own adapter is not one: it reads files. A
test that used the home reader over a COPY of the fixtures would exercise the
comparison and never the case the ruling was written for — no working tree at
all, an empty state carrying no placeholder files, documents that exist only
as blobs at a revision. So this file supplies the smallest honest one: about a
hundred lines over `git cat-file` and `git ls-tree`, stdlib plus the interface,
constructed from nothing, and it holds THE CORPUS'S OWN terms (its two-field
header vocabulary) as construction data rather than as module constants —
which is the property `floor37` measured to be the whole distance between a
git reader that passes this corpus and one that does not.

WHY IT SITS BESIDE `home_factory.py` AND NOT IN A TEST MODULE. The runner
imports a factory BY NAME off `--sys-path`, so the thing under test has to be
an importable module on disk rather than a class defined inside a test
function; `home_factory.py` is the precedent and the same directory is the
place. It is not collected by `pytest` (no `test_` prefix) and nothing outside
`tests/carve_conformance/` imports it.

THE TRANSPOSITION IS BUILT THE WAY A DESTINATION'S WOULD BE. `transpose()`
lays the same three documents down as blobs at the same relative keys in a
BARE repository per corpus state — no working tree, so the bytes can only be
reached through the history — copies `not-a-directory` verbatim, and never
creates the absent name. The empty state is a bare repository whose initial
commit carries an empty tree: a git corpus holds an empty directory as the
ABSENCE of a blob, which is why the fixtures' two `.gitkeep` placeholders (a
filesystem corpus's only way to carry an empty directory) are not imported.
Nothing about the documents changes, which is what `--corpus`'s fidelity proof
then measures rather than assumes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from corpus_adapter import (  # noqa: E402
    CORPUS_ABSENT,
    CORPUS_READ_ONLY,
    CORPUS_UNCLASSIFIABLE,
    CORPUS_UNREADABLE,
    DOCUMENT_UNKNOWN,
    REVISION_UNKNOWN,
    SCOPE_ALL,
    SCOPE_UNKNOWN,
    Classification,
    CorpusRefused,
    Document,
    DocumentId,
    Refusal,
    ResolvedCorpus,
)

#: The NEUTRAL corpus's own header vocabulary, held as construction data and
#: never as a module constant — the corpus declares its terms and the reader
#: is handed them, which is what lets one reader answer for a corpus it does
#: not own.
NEUTRAL_KIND_FIELD = "Type"
NEUTRAL_REQUIRED_FIELDS = ("Type", "Title")
HEADER_SCAN_LINES = 6

#: Enough to author a commit where no ambient git identity exists, which is
#: the state `pytest-suite.yml` deliberately runs in
#: (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`).
GIT_ENV = {
    "GIT_AUTHOR_NAME": "the conformance corpus transposition",
    "GIT_AUTHOR_EMAIL": "transposition@example.invalid",
    "GIT_COMMITTER_NAME": "the conformance corpus transposition",
    "GIT_COMMITTER_EMAIL": "transposition@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def _git(*args: str, cwd: Path | None = None, stdin: bytes | None = None,
         env_extra: dict[str, str] | None = None
         ) -> subprocess.CompletedProcess:
    import os
    env = dict(os.environ)
    # AMBIENT GIT POINTERS ARE DROPPED, NOT INHERITED. `GIT_DIR` and
    # `GIT_WORK_TREE` would override every `cwd=` below and silently aim
    # these plumbing calls at whatever repository the process was started
    # in — the same class of environment dependence `pytest-suite.yml`
    # denies with `GIT_CONFIG_GLOBAL=/dev/null`, and the one this file can
    # least afford, since what it writes are commits.
    for pointer in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                    "GIT_OBJECT_DIRECTORY", "GIT_COMMON_DIR"):
        env.pop(pointer, None)
    env.update(GIT_ENV)
    if env_extra:
        env.update(env_extra)
    # `--no-replace-objects`, which is this repository's own rule for every
    # git reader it owns (`validate-carve-manifest.py:862`,
    # `carved_reach.py:796`, `hermes_runtime_validation/content.py:106` and
    # four more) and applies here for the sharper reason (Copilot, round 2):
    # an ambient replacement ref would make `ls-tree` and `cat-file` serve
    # objects OTHER than the ones this transposition wrote, so the fixture
    # could prove a history it never laid down.
    return subprocess.run(["git", "--no-replace-objects", *args],
                          cwd=str(cwd) if cwd else None,
                          input=stdin, capture_output=True, env=env,
                          check=False)


class GitHistoryCorpus:
    """The six operations over a bare repository's HISTORY.

    "The corpus is the history, not the working tree": every read below goes
    through `cat-file` and `ls-tree` at a revision, and there is no working
    tree to fall back to. That is the property that makes this a fair stand-in
    for a destination whose corpus really is git.
    """

    def __init__(self, *, kind_field: str | None = NEUTRAL_KIND_FIELD,
                 required_fields: tuple[str, ...] = NEUTRAL_REQUIRED_FIELDS,
                 write_path: str | None = None) -> None:
        self._kind_field = kind_field
        self._required_fields = required_fields
        self._write_path = write_path

    # -- resolve ----------------------------------------------------------
    def resolve(self, ref) -> ResolvedCorpus:
        location = Path(ref.location)
        if not location.exists():
            raise CorpusRefused(Refusal(
                kind=CORPUS_ABSENT, subject=ref.location,
                detail="no such location"))
        if not location.is_dir():
            raise CorpusRefused(Refusal(
                kind=CORPUS_UNREADABLE, subject=ref.location,
                detail="the location is a file, not a repository directory"))
        # THE REPOSITORY MUST BE THIS LOCATION AND NOT AN ENCLOSING ONE.
        # `rev-parse --git-dir` walks UP, so a plain directory inside somebody
        # else's checkout would otherwise resolve as that checkout — a corpus
        # the caller never named.
        top = _git("rev-parse", "--git-dir", cwd=location)
        if top.returncode != 0:
            raise CorpusRefused(Refusal(
                kind=CORPUS_UNCLASSIFIABLE, subject=ref.location,
                detail="the directory is not a git repository"))
        resolved = Path(top.stdout.decode().strip())
        if not resolved.is_absolute():
            resolved = (location / resolved).resolve()
        if resolved != location.resolve():
            raise CorpusRefused(Refusal(
                kind=CORPUS_UNCLASSIFIABLE, subject=ref.location,
                detail=f"the repository at this location is {resolved}, "
                       "which is not this location"))
        head = _git("rev-parse", "HEAD", cwd=location)
        if head.returncode != 0:
            raise CorpusRefused(Refusal(
                kind=CORPUS_UNREADABLE, subject=ref.location,
                detail="the repository carries no HEAD"))
        revision = head.stdout.decode().strip()
        if ref.revision is not None and ref.revision != revision:
            raise CorpusRefused(Refusal(
                kind=REVISION_UNKNOWN, subject=ref.revision,
                detail="this reader serves only the location's own HEAD"))
        return ResolvedCorpus(
            ref=ref, location=str(location.resolve()), revision=revision,
            scopes=(SCOPE_ALL,), write_path=self._write_path,
            write_path_available=self._write_path is not None)

    # -- list -------------------------------------------------------------
    def list_documents(self, corpus, scope: str = SCOPE_ALL):
        if scope not in corpus.scopes:
            raise CorpusRefused(Refusal(
                kind=SCOPE_UNKNOWN, subject=scope,
                detail=f"this corpus declares {corpus.scopes!r}"))
        listed = _git("ls-tree", "-r", "--name-only", str(corpus.revision),
                      cwd=Path(corpus.location))
        if listed.returncode != 0:
            raise CorpusRefused(Refusal(
                kind=CORPUS_UNREADABLE, subject=corpus.ref.name,
                detail=listed.stderr.decode().strip()))
        keys = sorted(line for line in listed.stdout.decode().splitlines()
                      if line.endswith(".md"))
        return tuple(DocumentId(corpus=corpus.ref.name, key=key)
                     for key in keys)

    # -- read -------------------------------------------------------------
    def read(self, corpus, document, revision: str | None = None) -> Document:
        at = corpus.revision if revision is None else revision
        if revision is not None and revision != corpus.revision:
            known = _git("rev-parse", "--verify", f"{revision}^{{commit}}",
                         cwd=Path(corpus.location))
            if known.returncode != 0:
                raise CorpusRefused(Refusal(
                    kind=REVISION_UNKNOWN, subject=str(revision),
                    detail="this repository carries no such revision"))
        blob = _git("cat-file", "blob", f"{at}:{document.key}",
                    cwd=Path(corpus.location))
        if blob.returncode != 0:
            raise CorpusRefused(Refusal(
                kind=DOCUMENT_UNKNOWN, subject=document.key,
                detail=f"not present at revision {at}"))
        return Document(id=document, content=blob.stdout, revision=at)

    # -- classify ---------------------------------------------------------
    def classify(self, corpus, document) -> Classification:
        content = self.read(corpus, document).content
        header: dict[str, str] = {}
        for line in content.decode("utf-8", "replace").splitlines()[
                :HEADER_SCAN_LINES]:
            if ":" in line:
                field, _, value = line.partition(":")
                header[field.strip()] = value.strip()
        kind = header.get(self._kind_field) if self._kind_field else None
        if not kind:
            return Classification(
                id=document, kind=None, required_fields=(),
                missing_fields=(),
                unclassifiable=f"{document.key} carries no "
                               f"{self._kind_field!r} header")
        missing = tuple(f for f in self._required_fields
                        if not header.get(f))
        return Classification(id=document, kind=kind,
                              required_fields=self._required_fields,
                              missing_fields=missing)

    # -- check ------------------------------------------------------------
    def check(self, corpus, subjects=None):
        """No verdict machinery of its own, honestly answered: `()`."""
        return ()

    # -- write_back -------------------------------------------------------
    def write_back(self, corpus, document, content: bytes, *, actor: str,
                   basis_revision: str, reason: str = ""):
        if corpus.write_path is None:
            raise CorpusRefused(Refusal(
                kind=CORPUS_READ_ONLY, subject=corpus.ref.name,
                detail="this corpus declares no governed write path"))
        raise CorpusRefused(Refusal(
            kind=CORPUS_READ_ONLY, subject=corpus.ref.name,
            detail="this reader dispatches nothing"))


def reader(name: str, location: str) -> GitHistoryCorpus:
    """The factory `verify-carve-conformance.py` asks for."""
    del name, location
    return GitHistoryCorpus()


# ==========================================================================
# the transposition
# ==========================================================================


def _seed(repo: Path, documents: list[tuple[str, bytes]]) -> str:
    """One bare repository holding `documents` at their own keys, and nothing
    else. Built through git's own plumbing so no working tree ever exists."""
    repo.mkdir(parents=True, exist_ok=True)
    repo = repo.resolve()   # `GIT_INDEX_FILE` is read relative to the repo
    init = _git("init", "--quiet", "--bare", "--initial-branch=main",
                str(repo))
    if init.returncode != 0:  # pragma: no cover - a broken git
        raise RuntimeError(init.stderr.decode())
    index = repo / "transposition-index"
    env = {"GIT_INDEX_FILE": str(index)}
    for key, content in documents:
        blob = _git("hash-object", "-w", "--stdin", cwd=repo, stdin=content)
        if blob.returncode != 0:  # pragma: no cover
            raise RuntimeError(blob.stderr.decode())
        added = _git("update-index", "--add", "--cacheinfo",
                     f"100644,{blob.stdout.decode().strip()},{key}",
                     cwd=repo, env_extra=env)
        if added.returncode != 0:  # pragma: no cover
            raise RuntimeError(added.stderr.decode())
    tree = _git("write-tree", cwd=repo, env_extra=env)
    if tree.returncode != 0:  # pragma: no cover
        raise RuntimeError(tree.stderr.decode())
    commit = _git("commit-tree", tree.stdout.decode().strip(), "-m",
                  "Transpose the neutral conformance corpus", cwd=repo,
                  env_extra=env)
    if commit.returncode != 0:  # pragma: no cover
        raise RuntimeError(commit.stderr.decode())
    revision = commit.stdout.decode().strip()
    _git("update-ref", "refs/heads/main", revision, cwd=repo)
    _git("symbolic-ref", "HEAD", "refs/heads/main", cwd=repo)
    index.unlink(missing_ok=True)
    return revision


def transpose(fixtures: Path, out: Path, *, populated: str = "neutral",
              empty: str = "empty",
              unreadable: str = "not-a-directory") -> Path:
    """Lay the corpus at `fixtures` down as one BARE repository per state.

    The documents, their bytes and their relative keys are unchanged; only
    the storage form is. Returns `out`, which is what `--corpus` is handed.
    """
    import shutil
    fixtures = fixtures.resolve()
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    source = fixtures / populated
    documents = sorted(
        (path.relative_to(source).as_posix(), path.read_bytes())
        for path in source.rglob("*") if path.is_file())
    _seed(out / populated, documents)
    # A git corpus carries an empty directory as the ABSENCE of a blob, so the
    # empty state is an empty tree and the fixtures' `.gitkeep` placeholders
    # (which exist only so a FILESYSTEM corpus can carry an empty directory)
    # are not imported.
    _seed(out / empty, [])
    shutil.copyfile(fixtures / unreadable, out / unreadable)
    return out
