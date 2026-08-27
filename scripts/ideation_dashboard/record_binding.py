"""Record binding — a ratification is trusted for a REASON, not for its location.

THE GAP THIS CLOSES (`ideation/brainstorm/ideation-dashboard.md` item 25;
`contracts/identity-brokering/README.md`: "a ratification record's actor is
forgeable"). `kickoff.ratified_change_ids` walked the records tree, loaded every
`*.yaml`, and counted any document that SAID `kind: gate-action-record` +
`action: ratify` (or `kind: ratification-record`) as proof that a change had been
ratified. The entire proof was FILE PLACEMENT: anyone able to drop a file into the
records directory — an agent with a write path, a bug, a stray editor, a `cp` —
manufactured a ratification and, with it, the kickoff authority downstream of it.

WHAT A RATIFICATION MUST NOW CARRY. Two bindings, both required, neither of which
file placement can supply:

  1. A CONTENT DIGEST (`binding.digest`), written by the console at ratify time
     over the record's own content with the binding block itself excluded. It
     does not prove authorship — the digest is recomputable by anyone — but it
     makes the record TAMPER-EVIDENT as a unit: the ratifier, the date and the
     change id can no longer be edited in place, because the edit invalidates
     the digest the record carries.
  2. A GIT COMMIT ANCHOR. The record file must be TRACKED AT `HEAD` and its
     working-tree bytes must match what `HEAD` holds. This is the verifiable
     property file placement cannot forge: a dropped, untracked, or
     locally-edited file is not committed, and committing one means a real
     commit in a review-gated repository with a recorded author/committer
     identity that the anchor reads back and reports.

Together they mean a ratification is an entry in an append-only, attributable
ledger the repository already keeps — its git history — rather than a filename in
a directory.

FAIL CLOSED. No binding block, a digest that does not match, an untracked file, a
working-tree copy that differs from `HEAD`, no git at all: the ratification is
REFUSED. It is not silently ignored either — `verify_ratification` returns the
REASON, and `kickoff` surfaces it, so a human whose real ratification is merely
uncommitted is told to commit it rather than left guessing.

THE RESIDUAL, marked here rather than left ambient. A git anchor proves that
SOMEONE WITH COMMIT ACCESS committed this record and names the identity git
recorded for them; it does not cryptographically prove that the human named in
`ratifier` consented. Closing that needs signed commits or a signed ratification
artifact — the identity-brokering / D22 work. The strongest available step in that
direction IS available here and is opt-in per deployment: set
`XF_GATE_REQUIRE_SIGNED_RATIFICATION=1` and the anchoring commit must additionally
carry a signature git verifies (`%G?` in `G`/`U`). It is off by default only
because this corpus's history is unsigned; a deployment that signs should set it.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from collections.abc import Mapping as _MappingABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

# ---- the binding block (an ADDITIVE record property; the gate-action-record
# schema sets no `additionalProperties: false` and states "consumers MUST ignore
# unknown properties", so no schema bump and no pre-existing record is invalid) --
BINDING_KEY = "binding"
BINDING_KIND = "content-digest"
BINDING_ALGORITHM = "sha256"

ANCHOR_GIT_COMMIT = "git-commit"

REQUIRE_SIGNED_ENV = "XF_GATE_REQUIRE_SIGNED_RATIFICATION"
_TRUTHY = ("1", "true", "yes", "on")

# git's own signature verdicts (`--format=%G?`): G good, U good-but-untrusted,
# X good-but-expired-key, Y good key expired, R revoked, B bad, E cannot check,
# N none. Only a signature git actually verified counts.
_ACCEPTED_SIGNATURES = ("G", "U")


class BindingRefused(Exception):
    """A ratification was found and REFUSED for want of a verifiable binding."""


@dataclass(frozen=True)
class GitAnchor:
    """The commit a governed record is anchored to."""

    commit: str
    author: str
    email: str
    committed_at: str
    signature: str

    def describe(self) -> str:
        signed = "" if self.signature not in _ACCEPTED_SIGNATURES else " (signed)"
        return (f"commit {self.commit[:12]} by {self.author} <{self.email}> "
                f"at {self.committed_at}{signed}")


@dataclass(frozen=True)
class Verdict:
    """Bound, or not, and WHY not. A refusal always carries a reason a human can
    act on — an unverifiable ratification is reported, never silently dropped."""

    bound: bool
    reason: str = ""
    anchor: GitAnchor | None = None
    kind: str = ""

    def __bool__(self) -> bool:
        return self.bound


# --------------------------------------------------------------------------
# the content digest
# --------------------------------------------------------------------------

def content_digest(doc: Mapping[str, Any]) -> str:
    """`sha256` over the record's content with the binding block EXCLUDED.

    Canonicalised as sorted-key, separator-tight JSON — the same shape the intent
    lane's `request_digest` uses — so the digest depends on the record's VALUES
    and not on YAML spelling, key order, or the comment banner above it."""
    payload = {k: v for k, v in dict(doc).items() if k != BINDING_KEY}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           default=str, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def binding_block(doc: Mapping[str, Any]) -> dict:
    """The binding a governed record carries. Built from the record itself, so a
    caller cannot supply a digest of something else."""
    return {"kind": BINDING_KIND, "algorithm": BINDING_ALGORITHM,
            "digest": content_digest(doc)}


def with_binding(doc: Mapping[str, Any]) -> dict:
    """`doc` plus its binding block (idempotent: an existing block is recomputed
    from the rest of the content, never trusted)."""
    body = {k: v for k, v in dict(doc).items() if k != BINDING_KEY}
    body[BINDING_KEY] = binding_block(body)
    return body


def digest_verdict(doc: Mapping[str, Any]) -> Verdict:
    """Whether `doc` carries a well-formed binding matching its own content."""
    binding = doc.get(BINDING_KEY)
    if not isinstance(binding, _MappingABC):
        return Verdict(False, "carries no `binding` block: a ratification whose "
                              "only claim to authenticity is its location in the "
                              "records tree is refused")
    if binding.get("kind") != BINDING_KIND or binding.get("algorithm") != BINDING_ALGORITHM:
        return Verdict(False, f"carries an unrecognised binding "
                              f"({binding.get('kind')!r}/{binding.get('algorithm')!r}); "
                              f"expected {BINDING_KIND}/{BINDING_ALGORITHM}")
    claimed = binding.get("digest")
    actual = content_digest(doc)
    if not isinstance(claimed, str) or claimed != actual:
        return Verdict(False, "binding digest does not match its own content — the "
                              "record was altered after it was written")
    return Verdict(True, kind=BINDING_KIND)


# --------------------------------------------------------------------------
# the git commit anchor
# --------------------------------------------------------------------------

def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["git", "-C", str(cwd), *args],
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None


def repository_root(path: Path | str) -> Path | None:
    """The git work-tree `path` lives in, or None when it is not in one."""
    start = Path(path)
    start = start if start.is_dir() else start.parent
    proc = _git(start, "rev-parse", "--show-toplevel")
    if proc is None or proc.returncode != 0:
        return None
    top = (proc.stdout or "").strip()
    return Path(top).resolve() if top else None


def git_anchor(path: Path | str) -> Verdict:
    """Verify that `path` is committed at `HEAD` with no working-tree drift, and
    report the commit identity that anchors it.

    Three checks, each its own refusal, because "it was not committed" and "it
    was committed and then edited" are very different facts to hand a human."""
    file_path = Path(path).resolve()
    root = repository_root(file_path)
    if root is None:
        return Verdict(False, "is not inside a git work tree, so no commit "
                              "anchors it (the records tree must be a checkout "
                              "for a ratification to be verifiable)")
    try:
        rel = file_path.relative_to(root).as_posix()
    except ValueError:  # pragma: no cover - `repository_root` derived from it
        return Verdict(False, "resolves outside its own git work tree")

    at_head = _git(root, "rev-parse", f"HEAD:{rel}")
    if at_head is None or at_head.returncode != 0 or not (at_head.stdout or "").strip():
        return Verdict(False, "is not committed at HEAD — an uncommitted file in "
                              "the records tree proves nothing about who ratified "
                              "what. Commit the records tree, then retry")

    clean = _git(root, "diff", "--quiet", "HEAD", "--", rel)
    if clean is None or clean.returncode != 0:
        return Verdict(False, "differs from the committed copy at HEAD — the "
                              "working tree was edited after the record was "
                              "committed, so the commit anchors different content")

    meta = _git(root, "log", "-1",
                "--format=%H%x1f%an%x1f%ae%x1f%cI%x1f%G?", "--", rel)
    if meta is None or meta.returncode != 0 or not (meta.stdout or "").strip():
        return Verdict(False, "has no commit in this repository's history")
    fields = (meta.stdout or "").strip().split("\x1f")
    while len(fields) < 5:
        fields.append("")
    anchor = GitAnchor(fields[0], fields[1], fields[2], fields[3], fields[4])
    return Verdict(True, anchor=anchor, kind=ANCHOR_GIT_COMMIT)


def require_signed(env: Mapping[str, str] | None = None) -> bool:
    """Whether this deployment demands a git-verified signature on the anchoring
    commit (`XF_GATE_REQUIRE_SIGNED_RATIFICATION`). Off by default only because
    this corpus's history is unsigned — see the module docstring's residual."""
    env = os.environ if env is None else env
    return str(env.get(REQUIRE_SIGNED_ENV, "")).strip().lower() in _TRUTHY


# --------------------------------------------------------------------------
# the whole verdict
# --------------------------------------------------------------------------

def verify_ratification(doc: Mapping[str, Any], path: Path | str, *,
                        env: Mapping[str, str] | None = None) -> Verdict:
    """Is this on-disk ratification document authentic enough to be RELIED ON?

    Both bindings are required, and the digest is checked FIRST so a tampered
    record is named as tampered even when it happens to be committed."""
    digest = digest_verdict(doc)
    if not digest:
        return digest

    anchor = git_anchor(path)
    if not anchor:
        return anchor

    if require_signed(env) and (anchor.anchor is None
                                or anchor.anchor.signature not in _ACCEPTED_SIGNATURES):
        return Verdict(
            False,
            f"is anchored to an UNSIGNED commit and {REQUIRE_SIGNED_ENV} is set; "
            "this deployment requires a signature git can verify on the commit "
            "that carries a ratification", anchor=anchor.anchor)

    return Verdict(True, anchor=anchor.anchor, kind=ANCHOR_GIT_COMMIT)
