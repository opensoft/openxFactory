"""THE INTENT-PLANE BOUNDARY SUITE — `add-ideation-intent-plane` task 5.1.

Six proofs, one file, one-to-one with the task's own list:

  1. a forged actor is IGNORED                    `test_forged_actor_is_ignored`
  2. an unauthorized verb is REFUSED              `test_unauthorized_verb_is_refused`
  3. a stale view is REFUSED at the lane          `test_stale_view_is_refused`
  4. an application is ATOMIC (and rolls back)    `test_applied_atomically`
  5. hosted and local dispositions are EQUIVALENT `test_hosted_and_local_equivalent`
  6. the serving pod stays CREDENTIAL-FREE        `test_serving_pod_is_credential_free`

WHY A SUITE AND NOT SIX SCATTERED TESTS. Five of the six already held
SOMEWHERE — two of them in Omnigent-Install, three in this repository's lane
and route suites — and nowhere as one statement. The completion bar for this
change is not "each fact is asserted by somebody"; it is that the BOUNDARY
holds, and a boundary that is only ever checked one plank at a time is one
refactor away from a hole nobody owns. So the six live here, together, each
naming the spec scenario and design decision it discharges, and each failing
for its own reason.

WHAT THIS FILE DOES *NOT* DO. Two of the six proofs have an ingress half that
lives in another repository and is NOT re-implemented here (that repository is
not changed by this work, and a copied test proves only that the copy still
runs):

  * `Omnigent-Install tests/test_intent_inbox.py::test_forged_actor_is_stamped_over`
    and `::test_unauthorized_verb_refused_recorded_zero_dispatch` — the INBOX
    halves of proofs 1 and 2;
  * `Omnigent-Install tests/test_intent_plane_deploy.py` — the DEPLOYMENT half
    of proof 6 (no manifest carries a secret value; only the inbox mounts the
    dispatch token; both pods run locked down).

What this file asserts instead is the openxFactory SIDE of each of those
boundaries — the half that is this repository's to keep, and the half that
still has to hold when the inbox is compromised, which design D2 says in as
many words: "Compromising the inbox yields the ability to submit well-formed
intents as the ingress-authenticated user — which the apply lane revalidates
anyway (verb allowlist, target existence, lifecycle legality, stale-view
check)." Every proof below is therefore written from the position that the
inbox told the truth about NOTHING except which authenticated user it stamped.

Proof 5 is NEW. No test anywhere compared a hosted-applied record with a
locally applied one, which left the ratified scenario "Hosted and local trays
agree ... equivalent gate-action records differing only in transport
provenance" resting on reading the code. It now rests on two records.

D-2 (Brett Heap, openxFactory #656): the LIVE half — one real dispatch and one
real refusal on QA AKS — is a separate act, authorized only once this suite is
green. Nothing here touches a network, a cluster or a live credential.
"""

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import gate_console as gc
from ideation_dashboard import intent_apply_lane as lane

from test_gate_routes import _get, _post, _register, _serving
from test_intent_apply_lane import PID, _apply, _corpus, _intent

#: A pinned instant for the equivalence proof. `at` is wall-clock (a gate
#: record is a live audit entry, not the deterministic snapshot), so the two
#: halves of proof 5 would differ in it for a reason that has nothing to do
#: with transport. It is PINNED rather than excluded: an excluded field proves
#: nothing, and the ratified scenario says "differing only in transport
#: provenance" — so provenance must be the only survivor.
FROZEN_AT = "2026-09-06T12:00:00Z"

#: The one block the design says legitimately differs between the two doors
#: (design D23, "which door the action came through and how console presence
#: was shown"; the ratified scenario's "transport provenance"). Every other
#: key of the two records must agree, and the test fails naming any that does
#: not.
PROVENANCE_KEY = "provenance"


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=False)


def _records(root: Path) -> list[Path]:
    """Every gate-action record on disk, hosted or local."""
    return sorted(root.rglob("*.gate-action.yaml"))


def _entry(root: Path) -> dict:
    """The one possible both doors dispose, read out of the live register."""
    return next(e for e in _register(root) if e["id"] == PID)


def _allowlist(tmp_path: Path, actors: dict) -> Path:
    path = tmp_path / "boundary-allowlist.json"
    path.write_text(json.dumps({"actors": actors}), encoding="utf-8")
    return path


# ==========================================================================
# PROOF 1 — a forged actor is ignored
#
# Spec: "Minimal-authority intent inbox" / Scenario "A forged actor is
# ignored". Design D2 (the inbox stamps the actor and the lane revalidates
# anyway), design D23 (provenance is an OBSERVED fact, never a supplied one).
#
# The inbox half — a body-claimed `actor` overwritten by the ingress identity —
# is Omnigent-Install's `test_forged_actor_is_stamped_over`. THIS half is what
# holds when that stamping is subverted: the lane derives authority, the
# record's actor, the register's authority and the record's gateway block from
# the STAMPED fields alone, and there is no wire spelling of any of them.
# ==========================================================================

def test_forged_actor_is_ignored(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    # A body that claims everything it could possibly claim: a different
    # actor, a different authority, and a self-declared gateway.
    forged_args = {"outcome": "accepted", "note": "n",
                   "actor": "mallory", "authority": "mallory",
                   "ratifier": "mallory",
                   "provenance": {"surface": "cli",
                                  "console_presence": "tty"}}
    report = _apply(root, _intent(rev, args=forged_args), allowlist, tmp_path)
    assert report.outcome == "applied", report.reason

    record = yaml.safe_load((root / report.record).read_text("utf-8"))
    # the ACT is attributed to the stamped identity, never the claimed one
    assert record["actor"] == "brett"
    assert "mallory" not in json.dumps(record)
    # the gateway block is the lane's own observation (D23), not the body's
    assert record[PROVENANCE_KEY] == {"surface": "intent-plane",
                                      "console_presence": "ingress-auth"}
    # and the register's disposition authority follows the same stamp
    assert _entry(root)["derivation"]["human_disposition"]["authority"] == "brett"

    # The REQUEST is preserved verbatim in the committed intent — the claim is
    # auditable, it is simply powerless. (An intent that quietly dropped what
    # was asked would lose the evidence that a forgery was attempted.)
    intent_doc = yaml.safe_load((root / report.intent_path).read_text("utf-8"))
    assert intent_doc["actor"] == "brett"
    assert intent_doc["args"]["actor"] == "mallory"


def test_forged_actor_cannot_borrow_another_actors_authority(tmp_path):
    """The same proof from the other side: authority is read off the STAMPED
    actor, so an identity the inbox stamped with no verbs cannot buy any by
    naming one that has them."""
    root, rev, allowlist = _corpus(tmp_path)      # viewer: [] ; brett: [...]
    report = _apply(root, _intent(rev, actor="viewer",
                                  args={"outcome": "accepted",
                                        "actor": "brett"}),
                    allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "viewer's allowlist" in report.reason
    assert _records(root) == []                       # nothing executed
    assert "human_disposition" not in _entry(root)["derivation"]


def test_a_supplied_provenance_mapping_cannot_reach_a_record():
    """The STRUCTURAL reason proof 1 holds rather than a behavioural sample:
    `provenance` is a type the gateway constructs, and a mapping — which is
    the only thing a request body could ever carry — is refused at the record
    builder (design D23)."""
    with pytest.raises(gc.GateRefused) as exc:
        gc.build_gate_action_record(
            actor="brett", action="dispose-possible", at=FROZEN_AT,
            possible_id=PID, outcome="accepted", artifacts=[],
            provenance={"surface": "intent-plane",
                        "console_presence": "ingress-auth"})
    assert "OBSERVED fact" in str(exc.value)


# ==========================================================================
# PROOF 2 — an unauthorized verb is refused
#
# Spec: "Minimal-authority intent inbox" / Scenario "An unauthorized verb is
# refused at the inbox". Design D6 (per-actor verb allowlist, static first),
# design D2 (the lane rechecks it).
#
# The inbox half is Omnigent-Install's
# `test_unauthorized_verb_refused_recorded_zero_dispatch`. THIS half is the
# recheck against the checkout the verbs actually execute in — the one that
# still refuses when a dispatch arrives without ever passing the inbox.
# ==========================================================================

def test_unauthorized_verb_is_refused(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    allowlist = _allowlist(tmp_path, {"brett": ["dispose-possible"],
                                      "auditor": []})

    # a verb the actor is NOT allowed, on a target that exists
    report = _apply(root, _intent(rev, verb="ratify",
                                  target={"change_id": "some-change"},
                                  args={}),
                    allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "verb ratify is outside brett's allowlist" in report.reason
    # refused, RECORDED, and nothing executed: no gate-action record exists
    refusal = yaml.safe_load((root / report.intent_path).read_text("utf-8"))
    assert refusal["status"] == "refused"
    assert refusal["refusal_reason"] == report.reason
    assert _records(root) == []
    assert not _git(root, "status", "--porcelain").stdout.strip()

    # an actor with an EMPTY allowlist gets nothing either
    report = _apply(root, _intent(rev, actor="auditor"), allowlist, tmp_path)
    assert report.outcome == "refused" and "allowlist" in report.reason

    # and an unresolvable allowlist means NOBODY may do anything (fail-closed:
    # `load_allowlist` resolves missing or malformed to empty)
    report = _apply(root, _intent(rev, args={"outcome": "deferred"}),
                    allowlist, tmp_path,
                    allowlist_path=tmp_path / "there-is-no-allowlist.json")
    assert report.outcome == "refused" and "allowlist" in report.reason

    assert _records(root) == []
    assert "human_disposition" not in _entry(root)["derivation"]


# ==========================================================================
# PROOF 3 — a stale view is refused at the lane
#
# Spec: "Apply lane revalidates and commits atomically" / Scenario "A
# stale-view intent is refused". Design D4 (`snapshot_rev_seen`, the register
# fingerprint CAS precedent).
# ==========================================================================

def test_stale_view_is_refused(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    allowlist = _allowlist(tmp_path, {"brett": ["dispose-possible"],
                                      "casey": ["dispose-possible"]})

    first = _apply(root, _intent(rev), allowlist, tmp_path)
    assert first.outcome == "applied", first.reason

    # casey decided while LOOKING at `rev` — a view the first application has
    # since moved past. A distinct request identity, so this is a refusal and
    # not the idempotent skip.
    stale = _apply(root, _intent(rev, actor="casey",
                                 args={"outcome": "rejected",
                                       "reason": "r", "citation": "c"}),
                   allowlist, tmp_path)
    assert stale.outcome == "refused"
    assert "materially advanced past the view" in stale.reason

    # the refusal is COMMITTED (a refusal is as durable as an application)...
    refusal = yaml.safe_load((root / stale.intent_path).read_text("utf-8"))
    assert refusal["status"] == "refused" and refusal["refusal_reason"]
    assert not _git(root, "status", "--porcelain").stdout.strip()
    # ...and the second decision landed NOTHING: one record, the first outcome
    assert len(_records(root)) == 1
    assert _entry(root)["derivation"]["human_disposition"]["outcome"] == "accepted"


def test_an_unverifiable_view_is_refused_fail_closed(tmp_path):
    """The other half of D4: a `snapshot_rev_seen` this checkout cannot
    resolve is not "probably fine" — it is unverifiable, and the lane refuses
    rather than comparing the target with itself."""
    root, _rev, allowlist = _corpus(tmp_path)
    report = _apply(root, _intent("f" * 40), allowlist, tmp_path)
    assert report.outcome == "refused"
    assert "unverifiable" in report.reason
    assert _records(root) == []


# ==========================================================================
# PROOF 4 — applied atomically, with no partial state on failure
#
# Spec: "Apply lane revalidates and commits atomically" / Scenario "Applied
# atomically". Design D1 (the rolling PR is CUSTODY over an already-decided
# act, so the decision must be whole before it travels).
# ==========================================================================

def test_applied_atomically(tmp_path):
    root, rev, allowlist = _corpus(tmp_path)
    seed = _git(root, "rev-parse", "HEAD").stdout.strip()

    report = _apply(root, _intent(rev), allowlist, tmp_path)
    assert report.outcome == "applied", report.reason

    # ONE commit past the seed, carrying all three artifact classes together
    assert _git(root, "rev-list", "--count", f"{seed}..HEAD").stdout.strip() == "1"
    files = _git(root, "show", "--name-only", "--format=", "HEAD").stdout.split()
    assert report.intent_path in files                 # the request
    assert report.record in files                      # the act
    assert "ideation/cross-reference.yaml" in files    # the governed artifact
    # nothing left over: the tree is clean and the intent chains to its record
    assert not _git(root, "status", "--porcelain").stdout.strip()
    intent_doc = yaml.safe_load((root / report.intent_path).read_text("utf-8"))
    assert intent_doc["status"] == "applied"
    assert intent_doc["applied_record"] == report.record


def test_no_partial_state_survives_a_failed_pass(tmp_path, monkeypatch):
    """The half that makes "atomic" mean something. The engine writes the
    register and the record BEFORE the terminal intent is written, so a
    failure in between is exactly the window where half a decision could
    land — and a stranded dirty tree would then brick every later run at the
    lane's clean-checkout gate."""
    root, rev, allowlist = _corpus(tmp_path)
    seed = _git(root, "rev-parse", "HEAD").stdout.strip()

    def _boom(*_a, **_k):
        raise OSError("disk went away between the act and its record")

    monkeypatch.setattr(lane, "_write_intent", _boom)
    report = _apply(root, _intent(rev), allowlist, tmp_path)

    assert report.outcome == "error"
    assert "rolled back" in report.reason
    # the checkout is EXACTLY as it was: same HEAD, clean tree, no artifacts
    assert _git(root, "rev-parse", "HEAD").stdout.strip() == seed
    assert not _git(root, "status", "--porcelain").stdout.strip()
    assert _records(root) == []
    assert "human_disposition" not in _entry(root)["derivation"]


# ==========================================================================
# PROOF 5 — hosted and local dispositions produce equivalent records  (NEW)
#
# Spec: "Dispose tray is the first verb" / Scenario "Hosted and local trays
# agree": "both produce the same register lifecycle outcome and equivalent
# gate-action records differing only in transport provenance". Design D5
# (local-first, the identical tray retargeted), design D23 (the gateway fact
# is the ONE thing the two doors legitimately disagree about).
#
# The two halves are driven through their REAL entrypoints — the apply lane
# replaying a dispatched intent, and a loopback serve's
# `POST /actions/gate/dispose-possible` over real HTTP — into two separate
# checkouts seeded to the same register state.
#
# EXCLUDED FROM THE COMPARISON: `provenance`, and nothing else. `at` is
# PINNED (both doors read `gate_console._utcnow`), which is why the record
# FILENAMES can be compared too — a record path is derived from `at`, so
# equal paths say the two doors file their evidence in the same place.
# ==========================================================================

def test_hosted_and_local_equivalent(tmp_path, monkeypatch):
    monkeypatch.setattr(gc, "_utcnow", lambda: FROZEN_AT)
    disposition = {"possible_id": PID, "outcome": "accepted",
                   "note": "the same decision, twice"}

    # --- the LOCAL door: a loopback serve's executing gate route (D5) -------
    # Entered first so its `monkeypatch.setenv` for the hermetic .md renderer
    # is in force for BOTH halves — the two doors must differ in transport and
    # in nothing else, environment included.
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    with _serving(local_dir, monkeypatch=monkeypatch) as (host, port, local_root):
        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             dict(disposition))
    assert status == 200, body
    local_record = yaml.safe_load((local_root / body["record"]).read_text("utf-8"))

    # --- the HOSTED door: an intent replayed by the apply lane (D1/D2) -----
    hosted_dir = tmp_path / "hosted"
    hosted_root, rev, allowlist = _corpus(hosted_dir)
    report = _apply(hosted_root, _intent(rev, args={
        "outcome": disposition["outcome"], "note": disposition["note"]}),
        allowlist, hosted_dir)
    assert report.outcome == "applied", report.reason
    hosted_record = yaml.safe_load(
        (hosted_root / report.record).read_text("utf-8"))

    # --- they differ in the gateway block, and in NOTHING else -------------
    assert PROVENANCE_KEY in hosted_record and PROVENANCE_KEY in local_record, (
        "both doors MUST stamp a gateway block — an unstamped record is not "
        "'equivalent', it is unattributed (design D23)")
    differing = {key for key in set(hosted_record) | set(local_record)
                 if hosted_record.get(key) != local_record.get(key)}
    assert differing == {PROVENANCE_KEY}, (
        "hosted and local gate-action records must differ only in transport "
        f"provenance; these keys also differ: {sorted(differing - {PROVENANCE_KEY})}")
    assert hosted_record[PROVENANCE_KEY] == {"surface": "intent-plane",
                                             "console_presence": "ingress-auth"}
    assert local_record[PROVENANCE_KEY] == {"surface": "http",
                                            "console_presence": "console-token"}

    # the same act, filed in the same place under the same identity
    assert report.record == body["record"]
    assert hosted_record["actor"] == local_record["actor"] == "brett"
    assert hosted_record["action"] == "dispose-possible"
    assert hosted_record["target"] == {"possible_id": PID,
                                       "outcome": "accepted"}

    # ...and the SAME register lifecycle outcome, which is the other half of
    # the ratified scenario (a matching record over a diverged register would
    # prove nothing)
    assert _entry(hosted_root) == _entry(local_root)


# ==========================================================================
# PROOF 6 — the serving pod stays credential-free
#
# Spec: "Intents are requests, never writes" / Scenario "The serving pod stays
# credential-free". Design D16 (read-only by construction), design D2 (the
# inbox is the ONLY new credentialed component), Brett Heap's ruling D-1 on
# #656 (the applied/refused feed is served from the CORPUS — no new write
# path).
#
# The DEPLOYMENT half — no manifest carries a secret value, only the inbox
# mounts the dispatch token, both pods run locked down — is Omnigent-Install's
# `test_intent_plane_deploy.py`. THIS half is the CODE that pod runs: the
# hosted plane offers no executing gate route, and the two modules that answer
# its intent traffic can hold no credential because they never read one, never
# spawn anything, and never open a socket.
# ==========================================================================

#: Names that would give the serving path an authority it must not have: a
#: secret to read, a process to spawn, a socket to open, or a write. Matched
#: as a WHOLE name or the tail of a dotted spelling (`os.environ`,
#: `path.write_text`) against every name and attribute the AST carries — so an
#: import alias does not hide one, and an innocent identifier that merely
#: CONTAINS one of these words does not trip it.
FORBIDDEN_SPELLINGS = (
    "environ", "getenv", "putenv", "getpass", "netrc",
    "subprocess", "Popen", "check_output", "check_call",
    "socket", "urlopen", "urlretrieve", "sendall", "connect",
    "write_text", "write_bytes", "mkdir", "unlink", "rename", "rmtree",
)

#: Module roots that carry credential, process or network authority. The
#: serving path imports none of them — which is the strongest statement this
#: repository can make about a pod it does not itself deploy.
FORBIDDEN_IMPORT_ROOTS = frozenset({
    "os", "subprocess", "socket", "ssl", "http", "urllib", "requests",
    "netrc", "getpass", "shutil", "tempfile", "secrets",
})


def _dotted(node) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def _named_spellings(tree) -> set[str]:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            names.add(node.attr)
            names.add(_dotted(node))
        elif isinstance(node, ast.Name):
            names.add(node.id)
    return {n for n in names if n}


def _import_roots(tree) -> set[str]:
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            roots.add((node.module or "").split(".")[0])
    return {r for r in roots if r}


def _assert_no_authority(tree, label: str) -> None:
    spellings = _named_spellings(tree)
    for forbidden in FORBIDDEN_SPELLINGS:
        offenders = sorted(n for n in spellings
                           if n == forbidden or n.endswith("." + forbidden))
        assert not offenders, (
            f"{label} names {offenders} — the hosted serving path must hold "
            "no credential, spawn nothing, open no socket and write nothing "
            "(design D16; spec 'The serving pod stays credential-free')")


def test_serving_pod_is_credential_free(tmp_path, monkeypatch):
    # ---- (a) the hosted PLANE offers no write authority at all ------------
    # A served (non-loopback) bind is the hosted shape. `gate` — the only
    # capability that executes anything — is false there by construction, and
    # `intent` (a REQUEST, revalidated and refusable by the lane) is the only
    # capability true off loopback.
    hosted_dir = tmp_path / "hosted-plane"
    hosted_dir.mkdir()
    with _serving(hosted_dir, host="0.0.0.0",
                  monkeypatch=monkeypatch) as (host, port, root):
        _s, caps = _get(host, port, "/capabilities")
        assert caps["actions"]["gate"] is False
        assert caps["actions"]["intent"] is True
        assert caps["actor"] is None
        assert caps["actions"]["session"] is False
        assert caps["actions"]["edit"] is False

        status, body = _post(host, port, "/actions/gate/dispose-possible",
                             {"possible_id": PID, "outcome": "accepted"})
        assert status == 403 and body["error"] == "loopback_only"

        # ---- (b) the feed it DOES serve is a read of the corpus -----------
        # No credential is presented and none is needed: every byte here is
        # already readable through `/source/` on the same serve.
        status, feed = _get(host, port, "/committed-intents.json")
        assert status == 200
        assert feed["kind"] == "committed-intent-feed"
        assert feed["intents"] == []

    # nothing the hosted plane did touched the register
    assert "human_disposition" not in _entry(root)["derivation"]
    assert _records(root) == []

    # ---- (c) the CODE that answers hosted intent traffic ------------------
    # `intent_feed` is the module the pod imports for the feed route. It is
    # stdlib-pure by necessity (the image is `python:3.12-slim` with no pip
    # dependencies, so PyYAML is not importable there) and authority-free by
    # design: a module that imports no `os` cannot read a token out of the
    # environment however it is later edited.
    feed_src = (REPO_ROOT / "scripts" / "ideation_dashboard"
                / "intent_feed.py").read_text("utf-8")
    feed_tree = ast.parse(feed_src)
    assert not (_import_roots(feed_tree) & FORBIDDEN_IMPORT_ROOTS), (
        "intent_feed imports a credential/process/network-bearing module: "
        f"{sorted(_import_roots(feed_tree) & FORBIDDEN_IMPORT_ROOTS)}")
    _assert_no_authority(feed_tree, "intent_feed")

    # ...and the serve handler that calls it: parsing a query string and
    # handing back bytes, with no environment read, no spawn, no socket of its
    # own and no write.
    serve_tree = ast.parse((REPO_ROOT / "scripts" / "ideation_dashboard"
                            / "serve.py").read_text("utf-8"))
    handler = next(
        node for node in ast.walk(serve_tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "_serve_committed_intents")
    _assert_no_authority(handler, "serve._serve_committed_intents")


# ==========================================================================
# The suite's own guard: six proofs, and the file says which is which.
# ==========================================================================

PROOFS = {
    "forged actor ignored": "test_forged_actor_is_ignored",
    "unauthorized verb refused": "test_unauthorized_verb_is_refused",
    "stale view refused at the lane": "test_stale_view_is_refused",
    "atomic commit shape": "test_applied_atomically",
    "hosted and local dispositions equivalent": "test_hosted_and_local_equivalent",
    "serving pod credential-free": "test_serving_pod_is_credential_free",
}


def test_the_suite_carries_all_six_named_proofs():
    """Task 5.1 names six proofs. If one is ever deleted or renamed away, this
    fails rather than the suite quietly shrinking to five."""
    present = set(globals())
    missing = {proof: name for proof, name in PROOFS.items()
               if name not in present}
    assert not missing, f"task 5.1 proofs with no test in this file: {missing}"
    assert len(PROOFS) == 6
