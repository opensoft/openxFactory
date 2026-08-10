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
commits to the CURRENT branch with explicit pathspecs and leaves branch /
rolling-PR mechanics to the workflow that invoked it (D1: the rolling
intents PR is custody, not decision).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard import gate_console as gc  # noqa: E402
from ideation_dashboard.gate_routes import run_gate_action  # noqa: E402

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

#: Verbs whose target is a possible entry in the cross-reference index —
#: their stale check compares the ENTRY, not the whole file, so an unrelated
#: disposition does not refuse an unrelated intent.
_POSSIBLE_VERBS = ("dispose-possible", "promote-to-staging", "research-brief")

#: Verbs whose target's material state is the change directory tree.
_CHANGE_VERBS = ("demote", "edit-apply", "ratify", "kickoff")

_INDEX_REL = "ideation/cross-reference.yaml"

_INTENT_BANNER = (
    "# gate-intent — one human's REQUEST for a gate-console action\n"
    "# (gate-intent.schema.yaml). The actor was stamped by the intent inbox\n"
    "# from the ingress-authenticated identity; the apply lane revalidated\n"
    "# everything server-side before this file gained its terminal status.\n"
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def intent_relpath(intents_dir: str, verb: str, target_id: str, at: str) -> str:
    """Mirror of gate_action_record_relpath, in the intents prefix."""
    prefix = intents_dir if intents_dir.endswith("/") else intents_dir + "/"
    stamp = at.replace(":", "").replace("-", "").replace("T", "-").rstrip("Z")
    return f"{prefix}{target_id}/{verb}-{stamp}.gate-intent.yaml"


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
    rev = intent.get("snapshot_rev_seen")
    if not isinstance(rev, str) or len(rev) < 7:
        return "snapshot_rev_seen must name the viewed snapshot revision"
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
    else:  # create-project / edit-project: the register's own CAS governs
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


def _existing_applied_key(root: Path, intents_dir: str, key: str | None) -> bool:
    if not key:
        return False
    base = root / intents_dir
    if not base.is_dir():
        return False
    for path in base.rglob("*.gate-intent.yaml"):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(doc, dict) and doc.get("idempotency_key") == key \
                and doc.get("status") == "applied":
            return True
    return False


def _write_intent(root: Path, intents_dir: str, intent: dict) -> Path:
    verb = intent["verb"]
    key = VERB_TARGET_KEY[verb]
    target_id = intent["target"][key]
    rel = intent_relpath(intents_dir, verb, target_id, intent["requested_at"]
                         if isinstance(intent.get("requested_at"), str)
                         else _utcnow())
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_INTENT_BANNER + yaml.safe_dump(intent, sort_keys=False),
                    encoding="utf-8")
    return path


def _commit(root: Path, message: str, report: ApplyReport, *,
            push: bool) -> bool:
    """Stage EVERYTHING the pass wrote (the clean-tree precondition makes
    'everything dirty' exactly 'everything gate-written'), commit, and
    optionally push with one rebase retry."""
    if _git(root, "add", "-A").returncode != 0:
        report.outcome, report.reason = "error", "git add failed"
        return False
    commit = _git(root, "commit", "-m", message)
    if commit.returncode != 0:
        report.outcome = "error"
        report.reason = "git commit failed: " + commit.stderr.strip()[:200]
        return False
    report.committed = _git(root, "rev-parse", "HEAD").stdout.strip()[:12]
    if push:
        for _ in range(2):
            if _git(root, "push").returncode == 0:
                report.pushed = True
                return True
            _git(root, "pull", "--rebase")
        report.outcome, report.reason = "error", "git push failed after rebase retry"
        return False
    return True


def apply_intent(repo_root: Path | str, intent: dict, *,
                 allowlist_path: Path | str,
                 records_dir: str = gc.DEFAULT_RECORDS_DIR,
                 intents_dir: str = DEFAULT_INTENTS_DIR,
                 index_validator: Path | None = None,
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

    if _existing_applied_key(root, intents_dir, intent.get("idempotency_key")):
        report.outcome = "skipped"
        report.reason = "an intent with this idempotency_key is already applied"
        return report

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

    stale = stale_reason(root, intent) if git else None
    if stale is not None:
        return refuse(stale)

    body = {**(intent.get("target") or {}), **(intent.get("args") or {})}
    status, response = run_gate_action(
        intent["verb"], body, checkout_root=root, actor=intent["actor"],
        records_dir=records_dir, index_validator=index_validator,
        provenance=gc.INTENT_INGRESS)
    report.response = response
    if status >= 400:
        return refuse(str(response.get("error") or response.get("detail")
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
    parser.add_argument("--no-git", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args(argv)

    if args.intent_json:
        intent = json.loads(args.intent_json)
    else:
        intent = yaml.safe_load(Path(args.intent_file).read_text(encoding="utf-8"))
    report = apply_intent(
        args.repo_root, intent, allowlist_path=args.allowlist,
        index_validator=Path(args.index_validator) if args.index_validator else None,
        git=not args.no_git, push=args.push)
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0 if report.outcome in ("applied", "refused", "skipped") else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
