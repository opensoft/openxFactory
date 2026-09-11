"""The intent APPLY lane (add-ideation-intent-plane task 4.3).

Replays ONE dispatched `gate-intent` through the gate-console engine — the
same `run_gate_action` dispatcher the local action center drives — with full
server-side revalidation, and commits the applied intent, its gate-action
record, and the updated governed artifacts TOGETHER. The browser (and the
inbox) are untrusted: everything the inbox already checked is checked again
here, against the checkout the verbs actually execute in.

Fail-closed, and never silent:
  * the lane runs only on a CLEAN checkout (the spec's "fresh checkout" —
    a dirty tree refuses before anything is read);
  * the actor->verbs allowlist is REQUIRED and rechecked (no allowlist, no
    apply);
  * an intent whose `snapshot_rev_seen` this checkout does not know, or whose
    target has materially advanced past it, is REFUSED (design D4);
  * every refusal is WRITTEN as a `status: refused` intent and committed —
    the feed reads committed intents, so a refusal is as durable as an
    application;
  * an already-applied idempotency key SKIPS without a second application.

The lane is transport-simple like its sibling `register_edit_lane`: it
commits to the CURRENT branch and leaves branch / rolling-PR mechanics to
the workflow that invoked it (D1: the rolling intents PR is custody, not
decision). The `git=False` keyword is an internal TEST seam (it skips the
clean-tree gate and the commit, never the stale-view check); the public
CLI always runs with git on.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py
    sys.path.insert(0, str(_SCRIPTS_DIR))

# § 5.2 SHED REACH (RULED (a) / RULED Q7, `#656`): the modules this file reads
# from `opendox.*` / `openxdox.*` below left openxFactory at the carve and are
# read from the two PINNED legs through the ONE resolver. See
# `scripts/carved_reach.py`.
from carved_reach import install as _install_carved_reach  # noqa: E402

_install_carved_reach()

from openxdox import gate_console as gc  # noqa: E402
from openxdox.gate_routes import run_gate_action  # noqa: E402

#: Committed intents live beside the gate records they precede.
DEFAULT_INTENTS_DIR = "ideation/dashboard/intents/"

#: The intent-transportable verbs and each verb's required target key —
#: mirrored from contracts/schemas/gate-intent.schema.yaml (grow together).
VERB_TARGET_KEY = {
    "demote": "change_id",
    "edit-apply": "change_id",
    "ratify": "change_id",
    "kickoff": "change_id",
    "dispose-possible": "possible_id",
    "propose": "topic_id",
    "promote-to-staging": "possible_id",
    "derive-possibles": "cluster_id",
    "research-brief": "possible_id",
    "create-project": "project_id",
    "edit-project": "project_id",
}

#: Kernel-transportable verbs the routes layer cannot yet execute — the
#: dispatcher has no branch for them (they remain local-console verbs). An
#: intent for one is REFUSED with a reason that says exactly that, rather
#: than dying as an anonymous unknown-verb 404 (Codex P2, PR #157).
LANE_DEFERRED_VERBS = ("edit-apply", "kickoff")

#: Verbs whose executing route refuses without a served snapshot: the lane
#: generates a FRESH one from the checkout it replays in (which is also the
#: revalidation posture the spec wants) and hands its path through.
SNAPSHOT_VERBS = ("demote", "derive-possibles")

#: A target id is a register id or change id, never a path: one safe
#: segment, or the intent is refused before anything derives from it
#: (Codex P1, PR #157 — path traversal out of the intents prefix).
_SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

#: The viewed revision is an IMMUTABLE commit id, never a symbolic ref —
#: `refs/heads/main` resolves to whatever is current, which would make the
#: stale-view guard compare the target with itself (Codex round-10 P1,
#: PR #157). Hex spelling here; resolution to the full object id happens
#: against the checkout before identity or staleness derive from it.
_HEX_REV = re.compile(r"^[0-9a-f]{7,40}$")

#: Verbs whose target is a possible entry in the cross-reference index —
#: their stale check compares the ENTRY, not the whole file, so an unrelated
#: disposition does not refuse an unrelated intent.
_POSSIBLE_VERBS = ("dispose-possible", "promote-to-staging", "research-brief")

#: Verbs whose target's material state is the change directory tree.
_CHANGE_VERBS = ("demote", "edit-apply", "ratify", "kickoff")

#: Every target key the kernel knows; the terminal artifact keeps only
#: these (non-empty strings), so wire junk never rides a target into the
#: committed feed.
_TARGET_KEYS = ("change_id", "possible_id", "cluster_id", "topic_id",
                "project_id", "document")

_INDEX_REL = "ideation/cross-reference.yaml"

_INTENT_BANNER = (
    "# gate-intent — one human's REQUEST for a gate-console action\n"
    "# (gate-intent.schema.yaml). The actor was stamped by the intent inbox\n"
    "# from the ingress-authenticated identity; the apply lane revalidated\n"
    "# everything server-side before this file gained its terminal status.\n"
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


#: RFC 3339 date-time: full date, explicit time, explicit offset — the
#: kernel's `format: date-time` as the delegated FormatChecker enforces it
#: (`fromisoformat` alone admits date-only and offset-less spellings).
_RFC3339 = re.compile(
    r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    r"[Tt]([01]\d|2[0-3]):[0-5]\d:[0-5]\d(\.\d+)?"
    r"([Zz]|[+-]([01]\d|2[0-3]):[0-5]\d)$")


def _parses_as_datetime(value: str) -> bool:
    if not _RFC3339.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00").replace("z", "+00:00"))
    except ValueError:
        return False
    return True


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, timeout=180)


def load_allowlist(path: Path) -> dict[str, list[str]]:
    """The committed actor -> verbs map (the inbox's own config shape).
    Missing or malformed resolves EMPTY: nobody may do anything."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    actors = data.get("actors") if isinstance(data, dict) else None
    if not isinstance(actors, dict):
        return {}
    return {str(a): [str(v) for v in verbs]
            for a, verbs in actors.items() if isinstance(verbs, list)}


def canonical_target(verb: str, target: dict) -> dict:
    """Exactly the verb's own target member — the ONE form the digest, the
    committed artifact, and the dispatched body all use (Codex round-8 and
    round-10 P1s, PR #157: a stray extra member — even a kernel-known one
    the verb ignores — must not mint a fresh request identity, or a replay
    re-queues the same governed edit)."""
    key = VERB_TARGET_KEY[verb]
    value = target.get(key)
    return {key: value} if isinstance(value, str) and value else {}


def request_digest(intent: dict) -> str:
    """A stable identity for ONE request, computed lane-side from the
    validated fields (never trusted from the body): distinct actors or
    views acting on the same target in the same second get distinct
    artifacts (Codex round-2 P1, PR #157). The target enters in canonical
    form, so a wire spelling and its stored normalization agree."""
    import hashlib
    target = intent.get("target")
    verb = intent.get("verb")
    canonical = json.dumps(
        {"actor": intent.get("actor"), "verb": verb,
         "target": canonical_target(verb, target)
         if isinstance(target, dict) and verb in VERB_TARGET_KEY else target,
         "rev": intent.get("snapshot_rev_seen")},
        sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def intent_relpath(intents_dir: str, verb: str, target_id: str, at: str,
                   digest: str) -> str:
    """Mirror of gate_action_record_relpath, in the intents prefix, made
    unique per request identity by the lane-computed digest fragment."""
    prefix = intents_dir if intents_dir.endswith("/") else intents_dir + "/"
    stamp = at.replace(":", "").replace("-", "").replace("T", "-").rstrip("Z")
    stamp = "".join(c for c in stamp if c.isalnum() or c == "-") or "undated"
    return f"{prefix}{target_id}/{verb}-{stamp}-{digest[:10]}.gate-intent.yaml"


def shape_error(intent: dict) -> str | None:
    """Kernel-shape recheck (the inbox is untrusted here too)."""
    if not isinstance(intent, dict):
        return "intent must be a mapping"
    if intent.get("kind") != "gate-intent" or intent.get("schema_version") != 1:
        return "not a schema_version-1 gate-intent"
    actor = intent.get("actor")
    if not isinstance(actor, str) or not actor.strip():
        return "intent carries no actor"
    verb = intent.get("verb")
    if verb not in VERB_TARGET_KEY:
        return f"unknown or non-transportable verb: {verb!r}"
    target = intent.get("target")
    key = VERB_TARGET_KEY[verb]
    if not isinstance(target, dict) or not isinstance(target.get(key), str) \
            or not target.get(key):
        return f"verb {verb} requires target.{key}"
    if not _SAFE_SEGMENT.match(target[key]):
        return (f"target.{key} {target[key]!r} is not a safe path segment "
                "(one segment, no separators)")
    args = intent.get("args")
    if args is not None and not isinstance(args, dict):
        return "args must be an object"
    clash = sorted(set(args or ()) & set(VERB_TARGET_KEY.values()))
    if clash:
        return ("args must not carry target keys (the validated target is "
                "the only target): " + ", ".join(clash))
    requested_at = intent.get("requested_at")
    if not isinstance(requested_at, str) or not _parses_as_datetime(requested_at):
        return ("requested_at must be an RFC 3339 date-time with explicit "
                "time and offset (the kernel requires format: date-time)")
    rev = intent.get("snapshot_rev_seen")
    if not isinstance(rev, str) or not _HEX_REV.match(rev):
        return ("snapshot_rev_seen must be the viewed snapshot's commit id "
                "(7-40 hex characters, never a symbolic ref)")
    if intent.get("status") != "pending":
        return f"only a pending intent is applicable (got {intent.get('status')!r})"
    return None


# --------------------------------------------------------------------------
# the stale-view check (design D4)
# --------------------------------------------------------------------------

def _entry_from_index_text(text: str, possible_id: str):
    try:
        index = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    if not isinstance(index, dict):
        return None
    for entry in index.get("possibles_register") or []:
        if isinstance(entry, dict) and entry.get("id") == possible_id:
            return entry
    return None


def _show_at(root: Path, rev: str, rel: str) -> str | None:
    proc = _git(root, "show", f"{rev}:{rel}")
    return proc.stdout if proc.returncode == 0 else None


def stale_reason(root: Path, intent: dict) -> str | None:
    """None when the view is current enough to act on; otherwise the refusal.

    `snapshot_rev_seen` must be a commit this checkout knows — an
    unverifiable view refuses (fail closed). Possible-targeted verbs compare
    the target ENTRY between the seen revision and the working tree; change
    verbs compare the change directory's git object; propose compares the
    staging topic's tree; derive-possibles conservatively compares the whole
    index object. The project verbs' register carries its own fingerprint
    CAS in the gate handlers, so the engine's check is the material one.
    """
    rev = str(intent.get("snapshot_rev_seen"))
    verb = str(intent.get("verb"))
    target = intent.get("target") or {}
    if _git(root, "cat-file", "-t", rev).stdout.strip() != "commit":
        return (f"snapshot_rev_seen {rev} is not a commit this checkout "
                "knows — the viewed state is unverifiable")

    if verb in _POSSIBLE_VERBS:
        pid = target.get("possible_id")
        seen_text = _show_at(root, rev, _INDEX_REL)
        if seen_text is None:
            return f"the cross-reference index did not exist at {rev}"
        try:
            now_text = (root / _INDEX_REL).read_text(encoding="utf-8")
        except OSError:
            return "the cross-reference index is unreadable in this checkout"
        seen = _entry_from_index_text(seen_text, pid)
        now = _entry_from_index_text(now_text, pid)
        if seen is None:
            return f"possible {pid} was not in the register at {rev}"
        if now != seen:
            return (f"possible {pid} has materially advanced past the view "
                    f"at {rev}")
        return None

    if verb in _CHANGE_VERBS:
        rel = f"openspec/changes/{target.get('change_id')}"
    elif verb == "propose":
        rel = f"ideation/staging/{target.get('topic_id')}"
    elif verb == "derive-possibles":
        rel = _INDEX_REL
    else:
        # create-project / edit-project: DISPOSED, not deferred (Codex
        # round-2, PR #157). The register is aggregation-owned — a corpus
        # revision cannot resolve its history, so a snapshot_rev_seen CAS is
        # unimplementable here. The ruled semantics stand in for it: the
        # gate verb only RECORDS a commission (D2 boundary), edits QUEUE by
        # design (add-opendox-project-header D18), and the register-edit
        # lane refuses already-a-member / not-a-member conflicts against
        # the LIVE register at fulfilment time — the register's own
        # material check.
        return None
    seen_obj = _git(root, "rev-parse", f"{rev}:{rel}")
    now_obj = _git(root, "rev-parse", f"HEAD:{rel}")
    if seen_obj.returncode != 0:
        return f"{rel} did not exist at the viewed revision {rev}"
    if now_obj.returncode != 0 or seen_obj.stdout != now_obj.stdout:
        return f"{rel} has materially advanced past the view at {rev}"
    return None


# --------------------------------------------------------------------------
# the pass
# --------------------------------------------------------------------------

@dataclass
class ApplyReport:
    outcome: str = "error"                 # applied | refused | skipped | error
    reason: str | None = None
    intent_path: str | None = None         # committed intent, repo-relative
    record: str | None = None              # applied gate-action record
    committed: str | None = None
    pushed: bool = False
    response: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"outcome": self.outcome, "reason": self.reason,
                "intent_path": self.intent_path, "record": self.record,
                "committed": self.committed, "pushed": self.pushed,
                "response": self.response}


def _terminal_intent(intent: dict, digest: str) -> dict:
    """The committed artifact, rebuilt from VALIDATED fields only — a wire
    intent may carry schema-known fields with unvalidated values
    (`applied_record: []`, `refusal_reason: []`) or junk keys, and copying
    it would poison the validator-clean feed (Codex round-7, PR #157).
    The lane's own terminal fields (status, refusal_reason,
    applied_record, applied_at) are added by the paths that own them."""
    return {
        "schema_version": 1,
        "kind": "gate-intent",
        "actor": intent["actor"],
        "verb": intent["verb"],
        "target": canonical_target(intent["verb"], intent["target"]),
        "args": dict(intent.get("args") or {}),
        "requested_at": intent["requested_at"],
        "snapshot_rev_seen": intent["snapshot_rev_seen"],
        "status": "pending",
        "idempotency_key": digest,
    }


def _already_applied(root: Path, intents_dir: str, digest: str,
                     args: dict) -> bool:
    """True when a committed APPLIED intent has the same request identity
    AND the same arguments. The identity is RECOMPUTED from each stored
    intent's own fields — a supplied or stored `idempotency_key` string is
    data, never an authority to suppress execution (Codex round-5,
    PR #157). Argument equivalence is checked on top (Codex round-11 P1):
    successive edit-project commissions from ONE view legitimately differ
    only in args — the D18 queueing rule — so identity alone must not
    swallow a distinct decision."""
    base = root / intents_dir
    if not base.is_dir():
        return False
    for path in base.rglob("*.gate-intent.yaml"):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(doc, dict) and doc.get("status") == "applied" \
                and request_digest(doc) == digest \
                and (doc.get("args") or {}) == args:
            return True
    return False


def _write_intent(root: Path, intents_dir: str, intent: dict) -> Path:
    verb = intent["verb"]
    key = VERB_TARGET_KEY[verb]
    target_id = intent["target"][key]
    rel = intent_relpath(intents_dir, verb, target_id,
                         intent["requested_at"], request_digest(intent))
    path = (root / rel).resolve()
    base = (root / intents_dir).resolve()
    if base not in path.parents:
        raise ValueError(f"intent path escaped the intents prefix: {rel!r}")
    ordinal = 2
    while path.exists():  # same request re-decided: never overwrite history
        path = path.with_name(path.name.replace(
            ".gate-intent.yaml", f"-{ordinal}.gate-intent.yaml"))
        ordinal += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_INTENT_BANNER + yaml.safe_dump(intent, sort_keys=False),
                    encoding="utf-8")
    return path


def _commit(root: Path, message: str, report: ApplyReport, *,
            push: bool) -> bool:
    """Stage EVERYTHING the pass wrote (the clean-tree precondition makes
    'everything dirty' exactly 'everything gate-written') and commit. A
    rejected push RESETS the lane's own commit and fails the run: rebasing
    an already-decided action onto someone else's new state and pushing it
    would republish the decision without rerunning the duplicate guard,
    the stale-view check, or the engine (Codex round-9 P1, PR #157 — two
    overlapping propose runs could each enqueue a commission). A fresh run
    revalidates everything against the state that won."""
    before = _git(root, "rev-parse", "HEAD").stdout.strip()

    def _rollback() -> None:
        # the clean-tree precondition makes every untracked file lane-
        # written, so a hard reset plus clean restores exactly the
        # pre-pass checkout instead of stranding a dirty tree that bricks
        # every later run at the clean-tree gate (Codex round-10 P2)
        _git(root, "reset", "--hard", before)
        _git(root, "clean", "-fd")

    if _git(root, "add", "-A").returncode != 0:
        _rollback()
        report.outcome, report.reason = "error", "git add failed (rolled back)"
        return False
    commit = _git(root, "commit", "-m", message)
    if commit.returncode != 0:
        _rollback()
        report.outcome = "error"
        report.reason = ("git commit failed (rolled back): "
                         + commit.stderr.strip()[:200])
        return False
    report.committed = _git(root, "rev-parse", "HEAD").stdout.strip()[:12]
    if push:
        if _git(root, "push").returncode == 0:
            report.pushed = True
            return True
        _git(root, "reset", "--hard", before)
        report.committed = None
        report.outcome = "error"
        report.reason = ("push rejected — the decided commit was reset and "
                         "nothing landed; a fresh run revalidates against "
                         "the state that won")
        return False
    return True


#: Verbs whose route validates members against the reachable-repository
#: roster (Codex round-3, PR #157): without one, a repository that is
#: registered but not yet in any project refuses as unknown.
_ROSTER_VERBS = ("create-project", "edit-project")

#: Session-bearing lane verbs (Codex round-6, PR #157): their routes guard
#: against acting over an unresolved branch session, and that guard
#: DISABLES when the registry is None — so the lane rehydrates the live
#: sessions from the checkout exactly as the CLI does, through the one
#: bootstrap every session-bearing verb goes through.
_SESSION_VERBS = ("propose",)


def _live_session_registry(root: Path, repository: str):
    """The rehydrated session registry, mirroring `cli._session_registry`:
    live sessions derive from the worktrees and branches beside the
    checkout; half-signals are reported on stderr and never repaired."""
    # Sessions are reached THROUGH openXdox, never from openDox directly:
    # `bootstrap_sessions` lives in `branch_session` (openDox under design D3)
    # and this lane is openxFactory's own adapter, which RULING OQ-2 forbids
    # from importing openDox at all. OQ-B re-plumb B-3, ruled on `#656`
    # 2026-09-09. Same object, same call, same behaviour.
    from openxdox.openxdox_surface import bootstrap_sessions
    from openxdox.snapshot_registry import SnapshotRegistry

    registry = SnapshotRegistry()
    report = bootstrap_sessions(
        registry, repository=repository or "", checkout_root=root)
    for note in report.stale:
        print(f"  session note ({note.kind}): {note.reason}", file=sys.stderr)
    for message in report.errors:
        print(f"  session note: {message}", file=sys.stderr)
    return registry


def _project_roster(root: Path, project_register: Path | None = None):
    """A duck-typed registry (`entries()` rows carrying `.repository`) for
    the project verbs, built from the aggregation project register — the
    union of every project's members PLUS the published snapshot index
    beside it, so a registered repository not yet assigned to any project
    is still reachable. An unresolvable register contributes an EMPTY
    roster: the route then refuses new members, which is the fail-closed
    behaviour a bare corpus checkout deserves."""
    from types import SimpleNamespace

    from openxdox.kickoff import discover_project_register

    register = project_register or discover_project_register(root)
    names: set[str] = set()
    if register is not None and Path(register).is_file():
        try:
            doc = yaml.safe_load(Path(register).read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            doc = None
        for project in (doc or {}).get("projects") or []:
            if isinstance(project, dict):
                for repo in project.get("repositories") or []:
                    if isinstance(repo, str) and repo:
                        names.add(repo)
        index = Path(register).parent / "health" / "ideation-dashboard" / "index.json"
        if index.is_file():
            try:
                entries = json.loads(index.read_text(encoding="utf-8")).get("entries")
            except (OSError, ValueError):
                entries = None
            for entry in entries or []:
                if isinstance(entry, dict) and isinstance(entry.get("repository"), str):
                    names.add(entry["repository"])
    rows = tuple(SimpleNamespace(repository=name) for name in sorted(names))
    return SimpleNamespace(entries=lambda: rows)


def _fresh_snapshot(root: Path, repository: str) -> Path:
    """A snapshot generated from THIS checkout, for the routes that demand
    one — the freshest possible server-side state, written to an OS temp
    file the caller removes after dispatch."""
    import json as json_mod
    import tempfile

    from openxdox.generator import generate_snapshot

    head = _git(root, "rev-parse", "HEAD").stdout.strip() or "unknown"
    snapshot = generate_snapshot(root, repository, source_revision=head,
                                 generated_at=_utcnow())
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".snapshot.json", delete=False, encoding="utf-8")
    with handle as fh:
        json_mod.dump(snapshot, fh)
    return Path(handle.name)


def apply_intent(repo_root: Path | str, intent: dict, *,
                 allowlist_path: Path | str,
                 records_dir: str = gc.DEFAULT_RECORDS_DIR,
                 intents_dir: str = DEFAULT_INTENTS_DIR,
                 index_validator: Path | None = None,
                 repository: str = "openxFactory",
                 project_register: Path | None = None,
                 git: bool = True, push: bool = False) -> ApplyReport:
    """Replay one intent. Refusals are committed intents too — the only
    outcome that persists nothing is a shape error (there is no honest
    artifact to write for a body that is not an intent)."""
    report = ApplyReport()
    root = Path(repo_root).resolve()

    reason = shape_error(intent)
    if reason is not None:
        report.outcome, report.reason = "error", reason
        return report

    if git and _git(root, "status", "--porcelain").stdout.strip():
        report.outcome = "error"
        report.reason = ("the checkout is not clean — the lane replays "
                         "intents only against a fresh checkout")
        return report

    if git:
        resolved = _git(root, "rev-parse", "--verify", "--quiet",
                        intent["snapshot_rev_seen"] + "^{commit}").stdout.strip()
        if resolved:
            # abbreviated and full spellings of one commit share one
            # identity; stale checks run against the resolved object
            intent = {**intent, "snapshot_rev_seen": resolved}

    digest = request_digest(intent)
    canonical_args = dict(intent.get("args") or {})
    if _already_applied(root, intents_dir, digest, canonical_args):
        report.outcome = "skipped"
        report.reason = ("an intent with this request identity (actor, verb, "
                         "target, snapshot_rev_seen) and the same arguments "
                         "is already applied")
        return report
    # everything the lane persists derives from this validated rebuild —
    # the wire intent is never copied into the feed
    intent = _terminal_intent(intent, digest)

    if git:
        # ANY failure between here and the landed commit rolls the
        # checkout back to this revision — a half-written pass (the intent
        # write throwing after the engine already updated governed
        # artifacts, Codex round-11 P2) must not strand a dirty tree that
        # bricks every later run at the clean-tree gate.
        pass_base = _git(root, "rev-parse", "HEAD").stdout.strip()
        try:
            return _decide_and_land(root, intent, report, allowlist_path=
                                    Path(allowlist_path),
                                    records_dir=records_dir,
                                    intents_dir=intents_dir,
                                    index_validator=index_validator,
                                    repository=repository,
                                    project_register=project_register,
                                    git=git, push=push)
        except Exception as exc:  # noqa: BLE001 — rolled back, then surfaced
            _git(root, "reset", "--hard", pass_base)
            _git(root, "clean", "-fd")
            report.outcome = "error"
            report.reason = f"rolled back after failure: {exc}"
            return report
    return _decide_and_land(root, intent, report,
                            allowlist_path=Path(allowlist_path),
                            records_dir=records_dir, intents_dir=intents_dir,
                            index_validator=index_validator,
                            repository=repository,
                            project_register=project_register,
                            git=git, push=push)


def _decide_and_land(root: Path, intent: dict, report: ApplyReport, *,
                     allowlist_path: Path, records_dir: str, intents_dir: str,
                     index_validator: Path | None, repository: str,
                     project_register: Path | None, git: bool,
                     push: bool) -> ApplyReport:
    """The decision half of the pass: allowlist, deferral, staleness,
    dispatch, terminal write, commit. Extracted so `apply_intent` can wrap
    it in one rollback scope."""

    def refuse(why: str) -> ApplyReport:
        refused = dict(intent)
        refused["status"] = "refused"
        refused["refusal_reason"] = why
        path = _write_intent(root, intents_dir, refused)
        report.outcome, report.reason = "refused", why
        report.intent_path = str(path.relative_to(root))
        if git:
            _commit(root,
                    f"Refuse intent: {intent['verb']} "
                    f"({why[:120]})\n\n"
                    "Recorded by the intent apply lane "
                    "(add-ideation-intent-plane); a refusal is feed-visible, "
                    "never dropped.\n\n"
                    "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>",
                    report, push=push)
        return report

    allowed = load_allowlist(Path(allowlist_path)).get(intent["actor"], [])
    if intent["verb"] not in allowed:
        return refuse(f"verb {intent['verb']} is outside {intent['actor']}'s "
                      "allowlist (lane recheck)")

    if intent["verb"] in LANE_DEFERRED_VERBS:
        return refuse(f"verb {intent['verb']} is kernel-transportable but "
                      "not yet routable through the apply lane — it remains "
                      "a local-console verb until its executing route lands")

    stale = stale_reason(root, intent)
    if stale is not None:
        return refuse(stale)

    # The validated target WINS any args collision (shape_error already
    # refused overt clashes; this is the belt under that brace), and it is
    # dispatched in canonical form — junk members never reach the engine.
    body = {**(intent.get("args") or {}), **intent["target"]}
    snapshot_path = None
    if intent["verb"] in SNAPSHOT_VERBS:
        snapshot_path = _fresh_snapshot(root, repository)
    registry = None
    if intent["verb"] in _ROSTER_VERBS:
        registry = _project_roster(root, project_register)
    elif intent["verb"] in _SESSION_VERBS:
        registry = _live_session_registry(root, repository)
    try:
        status, response = run_gate_action(
            intent["verb"], body, checkout_root=root, actor=intent["actor"],
            records_dir=records_dir, index_validator=index_validator,
            snapshot_path=snapshot_path, session_registry=registry,
            repository=(repository
                        if intent["verb"] in _SESSION_VERBS else None),
            project_register=(project_register
                              if intent["verb"] in _ROSTER_VERBS else None),
            provenance=gc.INTENT_INGRESS)
    finally:
        if snapshot_path is not None:
            snapshot_path.unlink(missing_ok=True)
    report.response = response
    if status >= 400:
        return refuse(str(response.get("message") or response.get("error")
                          or f"gate refused (HTTP {status})"))

    applied = dict(intent)
    applied["status"] = "applied"
    applied["applied_at"] = _utcnow()
    record = response.get("record")
    if record:
        applied["applied_record"] = str(record)
        report.record = str(record)
    path = _write_intent(root, intents_dir, applied)
    report.outcome = "applied"
    report.intent_path = str(path.relative_to(root))
    if git:
        target_id = intent["target"][VERB_TARGET_KEY[intent["verb"]]]
        _commit(root,
                f"Apply intent: {intent['verb']} {target_id} "
                f"(actor {intent['actor']})\n\n"
                "Intent, gate-action record, and updated artifacts land "
                "together (add-ideation-intent-plane: applied atomically); "
                "replayed through the gate-console engine with the "
                "intent-plane provenance.\n\n"
                "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>",
                report, push=push)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--allowlist", required=True,
                        help="committed actor->verbs map (no allowlist, no apply)")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--intent-json", help="the gate-intent as a JSON string")
    source.add_argument("--intent-file", help="path to a gate-intent JSON/YAML file")
    parser.add_argument("--index-validator", default=None)
    parser.add_argument("--repository", default="openxFactory",
                        help="repository id stamped on lane-generated snapshots")
    parser.add_argument("--project-register", default=None,
                        help="aggregation project register (roster source for "
                             "the project verbs; discovered upward when omitted)")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args(argv)

    if args.intent_json:
        intent = json.loads(args.intent_json)
    else:
        intent = yaml.safe_load(Path(args.intent_file).read_text(encoding="utf-8"))
    report = apply_intent(
        args.repo_root, intent, allowlist_path=args.allowlist,
        index_validator=Path(args.index_validator) if args.index_validator else None,
        repository=args.repository,
        project_register=Path(args.project_register) if args.project_register else None,
        push=args.push)
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0 if report.outcome in ("applied", "refused", "skipped") else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
