"""The three gate-console trust gaps, each proven CLOSED BY REFUSAL.

`ideation/brainstorm/ideation-dashboard.md` item 25 recorded them as accepted v1
risks — "unauthenticated `--actor`, records-tree-trust ratification (forgeable),
un-confined `edit_apply` document path" — and
`contracts/identity-brokering/README.md` still names two of them in the present
tense as what blocks a write-enabled server-side phase.

Every test here asserts the REFUSAL, not the happy path, because a happy path
proves nothing about a trust boundary: the question is what the console does with
an invocation that should not be honoured. Each gap gets the forgery that used to
work, and each one must now be refused AND report why, with nothing written.

  1. `--actor` — a claim nobody checked. The exploit was `--actor "<anyone>"`:
     a governed, authority-bearing record naming a human who had nothing to do
     with the invocation. Now authenticated against the deployment's trusted
     principal, and refused with NO record when it cannot be established.
  2. RATIFICATION — trusted because it sat in the records tree. The exploit was
     dropping a hand-written `ratification-record` YAML into the records
     directory and having `kickoff` honour it. Now every candidate must carry a
     content digest matching its own content AND be committed at `HEAD`.
  3. `edit_apply` — an unconfined document path. The exploit was
     `--document ../../../..<anything>` or an absolute path or a planted
     symlink, which made a human gate action overwrite a file outside the
     repository entirely. Now confined to the permitted root, and REFUSED rather
     than clamped.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from conftest import BASE_REPO

from ideation_dashboard import actor_identity as actor_mod
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import kickoff as ko
from ideation_dashboard import record_binding as rb
from ideation_dashboard import serve as serve_mod
from ideation_dashboard.boundary import DOCUMENT_ESCAPE, BoundaryViolation, HumanGate

CHANGE = "add-ideation-governance"
DOC = f"openspec/changes/{CHANGE}/proposal.md"
AT = "2026-07-14T12:00:00Z"


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _gate(root: Path, actor: str = "brett") -> HumanGate:
    return HumanGate(root, [gc.DEFAULT_RECORDS_DIR], human_actor=actor)


def _records(root: Path) -> Path:
    return root / gc.DEFAULT_RECORDS_DIR


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(root),
         "-c", "user.name=Fixture Human", "-c", "user.email=human@example.test",
         "-c", "commit.gpgsign=false", *args],
        capture_output=True, text=True, timeout=60)


def _commit(root: Path, message: str = "records") -> None:
    if not (root / ".git").exists():
        _git(root, "init", "-q", "-b", "main")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--no-gpg-sign", "-m", message)


def _record_files(root: Path) -> list[Path]:
    records = _records(root)
    return sorted(records.rglob("*.yaml")) if records.is_dir() else []


# ============================================================================
# GAP 1 — the unauthenticated `--actor`
# ============================================================================

def test_an_unauthenticated_actor_claim_is_refused_and_writes_no_record(
        tmp_path, capsys, monkeypatch):
    """THE FORGERY THAT USED TO WORK. `--actor` was free text: this exact
    invocation once wrote a schema-valid, authority-bearing `ratify` record
    naming a human who had nothing to do with it. It must now be refused, with
    a non-zero exit and NOTHING on disk."""
    root = _tree(tmp_path)
    monkeypatch.setenv(actor_mod.ROSTER_ENV, "brett")   # the real principal

    code = cli_mod.main(["gate", "ratify", "--repo-root", str(root),
                         "--actor", "mallory", "--change-id", CHANGE])

    assert code == 1
    err = capsys.readouterr().err
    assert "refused" in err
    assert "not an authenticated principal" in err
    assert _record_files(root) == [], "a refused gate action wrote a record"


def test_a_gate_action_with_no_establishable_principal_fails_closed(
        tmp_path, capsys, monkeypatch):
    """FAIL CLOSED, not fail open. With no gateway identity, no launcher
    principal, no allowlist and a checkout carrying no git identity, there is
    nothing to authenticate against — and the answer is a refusal, never
    "record whatever the flag said"."""
    root = _tree(tmp_path)
    for name in (actor_mod.GATEWAY_ENV, actor_mod.PRINCIPAL_ENV,
                 actor_mod.ROSTER_ENV, actor_mod.ALLOWLIST_ENV):
        monkeypatch.delenv(name, raising=False)
    # a checkout with no git identity at all: `git config user.name` resolves
    # nothing, so the weakest source is unavailable too
    _git(root, "init", "-q", "-b", "main")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "absent-gitconfig"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(tmp_path / "absent-gitconfig"))

    code = cli_mod.main(["gate", "ratify", "--repo-root", str(root),
                         "--actor", "brett", "--change-id", CHANGE])

    assert code == 1
    assert "no authenticated principal" in capsys.readouterr().err
    assert _record_files(root) == []


def test_the_recorded_actor_is_the_trusted_spelling_not_the_caller_s(monkeypatch):
    """A lookalike cannot ride in on a real principal's coat-tails: the record
    carries the CANONICAL spelling the trusted source supplied."""
    monkeypatch.setenv(actor_mod.ROSTER_ENV, "Brett Heap")
    assert actor_mod.authenticate_actor("  brett   heap ").actor == "Brett Heap"
    with pytest.raises(actor_mod.ActorUnauthenticated):
        actor_mod.authenticate_actor("brett-heap")


def test_a_stronger_principal_source_is_never_widened_by_a_weaker_one(monkeypatch):
    """The gateway-verified user is the only identity a caller cannot spell for
    itself, so a roster sitting beside it must not add anyone to it."""
    monkeypatch.setenv(actor_mod.GATEWAY_ENV, "gateway-user")
    monkeypatch.setenv(actor_mod.ROSTER_ENV, "mallory, brett")
    resolved = actor_mod.trusted_principals()
    assert resolved.source == actor_mod.SOURCE_GATEWAY
    assert resolved.values == ("gateway-user",)
    with pytest.raises(actor_mod.ActorUnauthenticated):
        actor_mod.authenticate_actor("mallory")


def test_a_declared_but_empty_allowlist_admits_nobody(tmp_path, monkeypatch):
    """A configured control that resolves empty stays the answer. Falling
    through to the checkout's git identity would silently widen a control
    somebody deliberately put in place."""
    empty = tmp_path / "allowlist.json"
    empty.write_text('{"actors": {}}', encoding="utf-8")
    monkeypatch.delenv(actor_mod.GATEWAY_ENV, raising=False)
    monkeypatch.delenv(actor_mod.PRINCIPAL_ENV, raising=False)
    monkeypatch.delenv(actor_mod.ROSTER_ENV, raising=False)
    monkeypatch.setenv(actor_mod.ALLOWLIST_ENV, str(empty))
    with pytest.raises(actor_mod.ActorUnauthenticated):
        actor_mod.authenticate_actor("brett", checkout_root=Path.cwd())


def test_the_serve_actor_override_is_authenticated_and_fails_closed(
        tmp_path, monkeypatch):
    """The same claim on the served surface. `--actor` used to WIN OUTRIGHT
    here — whatever it carried became the identity every gate-action record the
    serve wrote would name. An unauthenticated override now resolves to None,
    which is this surface's fail-closed spelling (gate actions stay OFF)."""
    root = _tree(tmp_path)
    monkeypatch.setenv(actor_mod.ROSTER_ENV, "brett")
    assert serve_mod.resolve_actor(root, "mallory") is None
    assert serve_mod.resolve_actor(root, "brett") == "brett"


# ============================================================================
# GAP 2 — ratification trusted because of where the file sits
# ============================================================================

def _forged_ratification(root: Path, change_id: str = CHANGE) -> Path:
    """The forgery: a hand-written ratification dropped into the records tree.
    Nothing about it is invalid — it is exactly what the console writes, minus
    the two things a file cannot give itself."""
    folder = _records(root) / change_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "ratify-20260714T110000Z.ratification-record.yaml"
    path.write_text(yaml.safe_dump({
        "kind": "ratification-record", "schema_version": 1,
        "change_id": change_id, "ratifier": "Brett", "date": "2026-07-14",
    }, sort_keys=False), encoding="utf-8")
    return path


def test_a_dropped_ratification_file_is_not_a_ratification(tmp_path):
    """The whole gap in one assertion: writing the file used to BE the
    ratification. It is now refused, and the refusal names the reason."""
    root = _tree(tmp_path)
    _forged_ratification(root)

    unbound: list[str] = []
    assert ko.ratified_change_ids(records_root=_records(root),
                                  unbound=unbound) == set()
    assert unbound, "a refused ratification must be REPORTED, not silently dropped"
    assert "binding" in unbound[0]


def test_a_forged_ratification_cannot_unlock_kickoff(tmp_path):
    """The authority downstream of the forgery. `kickoff` is ratify-gated
    (D17), so a manufactured ratification used to hand a non-human caller the
    realization dispatch. It is refused, and nothing is written."""
    root = _tree(tmp_path)
    _forged_ratification(root)
    console = gc.GateConsole(_gate(root))

    with pytest.raises(gc.GateRefused) as ei:
        console.kickoff(CHANGE, at=AT)

    assert "VERIFY" in str(ei.value)
    assert not list(_records(root).rglob("*.workflow-job.yaml"))


def test_a_ratification_committed_but_then_edited_is_refused(tmp_path):
    """TAMPER-EVIDENCE, the half a git anchor alone does not give. A real
    ratification is committed, then its `ratifier` is edited in the working
    tree — the classic "make it say what I want" edit. Both bindings catch it:
    the digest no longer matches its content, and the file no longer matches
    HEAD."""
    root = _tree(tmp_path)
    res = gc.GateConsole(_gate(root)).ratify(CHANGE, "Brett", at=AT)
    _commit(root, "ratify")
    assert CHANGE in ko.ratified_change_ids(records_root=_records(root))

    doc = yaml.safe_load(res.ratification_path.read_text(encoding="utf-8"))
    doc["ratifier"] = "mallory"
    res.ratification_path.write_text(yaml.safe_dump(doc, sort_keys=False),
                                     encoding="utf-8")
    # and the ACTION record beside it, so nothing else vouches for the change
    action = yaml.safe_load(res.record_path.read_text(encoding="utf-8"))
    action["actor"] = "mallory"
    res.record_path.write_text(yaml.safe_dump(action, sort_keys=False),
                               encoding="utf-8")

    unbound: list[str] = []
    assert ko.ratified_change_ids(records_root=_records(root),
                                  unbound=unbound) == set()
    assert any("does not match its own content" in reason for reason in unbound)


def test_a_forger_who_recomputes_the_digest_still_has_no_commit_anchor(tmp_path):
    """The obvious next move, closed. The digest is recomputable by anyone, so a
    forger can make one that matches — and still cannot produce a commit. The
    anchor, not the digest, is what placement cannot forge."""
    root = _tree(tmp_path)
    _commit(root, "base")
    path = _forged_ratification(root)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    path.write_text(yaml.safe_dump(rb.with_binding(doc), sort_keys=False),
                    encoding="utf-8")
    assert rb.digest_verdict(yaml.safe_load(path.read_text(encoding="utf-8")))

    unbound: list[str] = []
    assert ko.ratified_change_ids(records_root=_records(root),
                                  unbound=unbound) == set()
    assert any("not committed at HEAD" in reason for reason in unbound)


def test_a_deployment_may_require_a_signed_anchoring_commit(tmp_path, monkeypatch):
    """The strongest available binding, opt-in. An unsigned commit anchors a
    ratification by default (this corpus's history is unsigned); a deployment
    that signs sets the flag and an unsigned anchor stops counting."""
    root = _tree(tmp_path)
    gc.GateConsole(_gate(root)).ratify(CHANGE, "Brett", at=AT)
    _commit(root, "ratify")
    assert CHANGE in ko.ratified_change_ids(records_root=_records(root))

    monkeypatch.setenv(rb.REQUIRE_SIGNED_ENV, "1")
    unbound: list[str] = []
    assert ko.ratified_change_ids(records_root=_records(root),
                                  unbound=unbound) == set()
    assert any("UNSIGNED commit" in reason for reason in unbound)


# ============================================================================
# GAP 3 — the un-confined `edit_apply` document path
# ============================================================================

@pytest.mark.parametrize("document", [
    "../../../../etc/hosts",                       # plain traversal
    "openspec/../../outside.md",                   # traversal through a real dir
    "/etc/hosts",                                  # absolute: `root / doc` == doc
    "   ",                                         # blank
])
def test_edit_apply_refuses_a_document_outside_the_permitted_root(
        tmp_path, document):
    """Each spelling of the escape, refused BEFORE any read or write, reported
    on the gate's own ledger, and never clamped back inside."""
    root = _tree(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("untouched\n", encoding="utf-8")
    gate = _gate(root)

    with pytest.raises(BoundaryViolation) as ei:
        gc.edit_apply(gate, CHANGE, document, gc.Redline(full_text="OWNED\n"), at=AT)

    assert ei.value.refusal.kind == DOCUMENT_ESCAPE
    assert gate.output.refusals[-1].kind == DOCUMENT_ESCAPE   # reported, not silent
    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert _record_files(root) == [], "a refused edit-apply wrote a record"


def test_edit_apply_refuses_a_symlink_that_escapes_the_root(tmp_path):
    """The escape that survives every string check. The path is relative, has no
    `..`, and resolves INSIDE the repo by name — but the name is a symlink, and
    following it lands outside. Confinement is compared against the RESOLVED
    root for exactly this reason."""
    root = _tree(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("untouched\n", encoding="utf-8")
    link = root / "openspec" / "changes" / CHANGE / "escape.md"
    link.symlink_to(outside)
    gate = _gate(root)

    with pytest.raises(BoundaryViolation) as ei:
        gc.edit_apply(gate, CHANGE, f"openspec/changes/{CHANGE}/escape.md",
                      gc.Redline(full_text="OWNED\n"), at=AT)

    assert ei.value.refusal.kind == DOCUMENT_ESCAPE
    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert _record_files(root) == []


def test_edit_apply_refuses_a_target_that_is_not_a_document(tmp_path):
    """A directory is not a document, and a document that does not exist is the
    authoring path's business. Both are refusals rather than a create."""
    root = _tree(tmp_path)
    gate = _gate(root)
    for target in (f"openspec/changes/{CHANGE}", "openspec/changes/absent/proposal.md"):
        with pytest.raises(BoundaryViolation) as ei:
            gc.edit_apply(gate, CHANGE, target, gc.Redline(full_text="x\n"), at=AT)
        assert ei.value.refusal.kind == DOCUMENT_ESCAPE


def test_the_cli_edit_apply_refuses_the_traversal_and_exits_nonzero(
        tmp_path, capsys, monkeypatch):
    """The gap as it is actually reachable: the CLI flag a human types. The
    refusal must be a refusal AND a non-zero exit — a wrapper script must not be
    able to mistake an escaped write for an applied redline."""
    root = _tree(tmp_path)
    monkeypatch.setenv(actor_mod.ROSTER_ENV, "brett")
    outside = tmp_path / "outside.md"
    outside.write_text("untouched\n", encoding="utf-8")
    payload = tmp_path / "payload.md"
    payload.write_text("OWNED\n", encoding="utf-8")

    code = cli_mod.main(["gate", "edit-apply", "--repo-root", str(root),
                         "--actor", "brett", "--change-id", CHANGE,
                         "--document", "../../outside.md",
                         "--full-text-file", str(payload)])

    assert code == 1
    err = capsys.readouterr().err
    assert "edit-apply refused" in err
    assert DOCUMENT_ESCAPE in err
    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert _record_files(root) == []


def test_edit_apply_still_applies_a_redline_inside_the_root(tmp_path):
    """The confinement narrows nothing legitimate: the ordinary in-tree redline
    still applies exactly, so the refusals above are about escapes and not about
    the verb."""
    root = _tree(tmp_path)
    before = (root / DOC).read_text(encoding="utf-8")
    marker = before.splitlines()[0]
    res = gc.edit_apply(_gate(root), CHANGE, DOC,
                        gc.Redline(old_text=marker, new_text=marker + " (revised)"),
                        at=AT)
    assert res.after == before.replace(marker, marker + " (revised)", 1)
    assert (root / DOC).read_text(encoding="utf-8") == res.after



# ============================================================================
# THE STRUCTURAL PIN — a future gate verb cannot forget to authenticate
# ============================================================================

def test_every_cli_gate_construction_authenticates_its_actor_first():
    """A CLOSED-WORLD check, not a denylist. The `--actor` gap was not a missing
    branch anywhere; it was that NOBODY asked. So the pin is over the whole
    surface: every function in `cli.py` that constructs a `HumanGate` must, in
    its own body, either authenticate the actor (`_gate_actor`) or first run the
    session identity gate (which authenticates). Add a gate verb without one and
    this fails, which is the point — the next verb inherits the control instead
    of re-deciding it."""
    import ast

    source = Path(cli_mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = ast.get_source_segment(source, node) or ""
        if "HumanGate(" not in body:
            continue
        if node.name in ("_gate_actor", "_session_identity_gate"):
            continue
        if "_gate_actor(" in body or "_session_identity_gate(" in body:
            continue
        offenders.append(node.name)
    assert offenders == [], (
        f"these cli.py functions build a HumanGate without authenticating the "
        f"actor claim first: {offenders}")
