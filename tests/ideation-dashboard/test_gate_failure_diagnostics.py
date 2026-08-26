"""Three T092 acceptance-sweep findings about what a gate verb does when it goes
wrong — the log, the derived name, and the refusal that mutated anyway.

  * DEFECT 3 — every gate 500 says "gate action failed; see the server log", and
    the log received NOTHING: byte-identical before and after three separate
    500s, because `serve.py`'s `except Exception` sent the message and wrote
    nowhere, while `http.server`'s own request logging is suppressed by the
    `log_message` override. The notebook route in the SAME run logged nlm's real
    reason verbatim, which is what proved this a gap rather than an environment
    artifact. Two assertions together are the contract: a clean 500 with NO
    traceback on the wire, AND a traceback on stderr.

  * DEFECT 2 — `lens-save-recipe` returned an unhandled `OSError: [Errno 36] File
    name too long` at ~13-14 checked keywords, i.e. ordinary usage of a shipped
    gated verb. The default set name is machine-derived ("lens " + every checked
    keyword), and the crash happened inside `_refuse_duplicate_set`'s `.exists()`
    — in the DUPLICATE CHECK, before any write, so the verb could not even
    refuse. Tested at the BOUNDARY (the length either side of the bound), not at
    fixture scale, which never approaches it.

  * DEFECT 4 — a REFUSED save-recipe left its manifest on disk: 720 bytes, fully
    populated, unrecorded (a refusal writes no gate-action record) and POISONING
    the retry, because the identical recipe then refused with "a workbench set
    named … already exists". `workbench.save()` wrote through the boundary and
    validated afterwards. The test the suite lacked is the filesystem one: the
    existing tests asserted the RAISE and never what was left behind.

Hermetic: scratch trees under `tmp_path`, a local stub validator script run
through `sys.executable`, no network, no real `gh`/`nlm`, no real checkout.
"""

from __future__ import annotations

import http.client
import json
import os
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit
from session_fixtures import build_scratch_repo

from ideation_dashboard import gate_routes as gr
from ideation_dashboard import serve as serve_mod
from ideation_dashboard import workbench as wb
from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
REPO = "openxFactory"
RECORDS = "ideation/dashboard/gate-records/"


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())


# --------------------------------------------------------------------------
# DEFECT 3 — the log the message names
# --------------------------------------------------------------------------

@contextmanager
def _serving(repo, snapshot_path, *, actor="tester"):
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, actor=actor)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    bind_host, port = httpd.server_address[:2]
    try:
        yield ("127.0.0.1" if bind_host in ("0.0.0.0", "") else bind_host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _post(host, port, path, body):
    raw = json.dumps(body).encode("utf-8")
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("GET", "/capabilities")
    caps = json.loads(conn.getresponse().read().decode("utf-8"))
    conn.close()
    headers = {"Content-Type": "application/json", "Content-Length": str(len(raw))}
    if caps.get("console_token"):
        headers["X-XF-Console-Token"] = caps["console_token"]
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request("POST", path, body=raw, headers=headers)
    response = conn.getresponse()
    payload = json.loads(response.read().decode("utf-8"))
    conn.close()
    return response.status, payload


class _Sentinel(RuntimeError):
    """A failure shape no route defines, so nothing can be catching it already."""


def test_an_unexpected_gate_failure_reaches_the_server_log_with_a_traceback(
        tmp_path, capsys, monkeypatch):
    """Fault injection, because no committed test provokes a gate exception at all
    — the fakes make the routes succeed, which is why a 500 that logged nothing
    went unnoticed through a whole feature.

    BOTH halves are asserted in one test on purpose: they are one contract, and
    each is wrong without the other. A traceback on the wire would be an
    information leak; a traceback nowhere is an undiagnosable failure."""
    repo = build_scratch_repo(tmp_path, repository=REPO)
    served = tmp_path / "served.json"
    served.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                      encoding="utf-8")

    def _boom(verb, body, **kwargs):
        raise _Sentinel("the engine blew up: /a/secret/path")

    monkeypatch.setattr(gr, "run_gate_action", _boom)
    capsys.readouterr()                       # drop the serve's startup banner

    with _serving(repo, served) as (host, port):
        status, payload = _post(host, port, "/actions/gate/ratify",
                                {"change_id": "a-change",
                                 "secret_field": "do-not-echo-me"})

    err = capsys.readouterr().err

    # the WIRE: the fixed catalog answer, and nothing else
    assert status == 500, payload
    assert payload == {"ok": False, "error": "action_failed",
                       "message": "gate action failed; see the server log"}
    assert "Traceback" not in json.dumps(payload)
    assert "_Sentinel" not in json.dumps(payload)
    assert "secret" not in json.dumps(payload)
    # the LOG: the verb, the exception type, and a real traceback
    assert "[actions/gate]" in err
    assert "ratify" in err
    assert "_Sentinel" in err
    assert "Traceback (most recent call last)" in err
    assert "the engine blew up" in err
    # and the request's own body is not what got logged — the verb is a
    # dispatch value, not free text from the caller
    assert "do-not-echo-me" not in err


# --------------------------------------------------------------------------
# DEFECT 2 — a machine-derived name is a BOUNDED filename component
# --------------------------------------------------------------------------

# 255 bytes is the component limit every mainstream filesystem enforces, and it
# is what `OSError: [Errno 36]` was reporting.
_FS_COMPONENT_LIMIT = 255


def test_a_derived_set_name_never_exceeds_the_filename_limit_at_the_boundary():
    """The BOUNDARY, not a fixture: one character under the bound, exactly on it,
    and one over — plus the shape the sweep actually hit (a "lens " + keywords
    name at 14 and at 30 keywords)."""
    for length in (wb.MAX_SLUG_CHARS - 1, wb.MAX_SLUG_CHARS,
                   wb.MAX_SLUG_CHARS + 1, 400, 4000):
        name = "a" * length
        slug = wb.slug(name)
        assert len(slug) <= wb.MAX_SLUG_CHARS, (length, len(slug))
        basename = Path(wb.manifest_relpath(name)).name
        assert len(basename.encode("utf-8")) <= _FS_COMPONENT_LIMIT, (
            length, len(basename))
    # at or under the bound the slug is UNCHANGED — every existing set keeps the
    # path it already has
    exact = "a" * wb.MAX_SLUG_CHARS
    assert wb.slug(exact) == exact
    assert wb.slug("lens doc-health") == "lens-doc-health"

    keywords = ["doc-management", "doc-workflow", "ideation-dashboard",
                "client-hermes", "domain-hermes", "roles-authority-model",
                "codexfactory", "feat-request", "keyword-lens", "plane-1",
                "possibles-register", "auto-clear-envelope", "avatar-client",
                "company-policy", "credential-contracts", "doc-health",
                "ideation-cross-reference", "ideation-lifecycle"]
    for count in (13, 14, 18, 30):
        derived = "lens " + " ".join((keywords * 3)[:count])
        basename = Path(wb.manifest_relpath(derived)).name
        assert len(basename.encode("utf-8")) <= _FS_COMPONENT_LIMIT, count


def test_two_different_long_set_names_do_not_collapse_onto_one_manifest():
    """Truncation alone would map two long derived names onto ONE path — and the
    long names here are DERIVED from a checked-keyword set, so two of them
    routinely differ only in the tail that truncation removes. The digest is what
    keeps the derivation injective (the same shape `branch_session.notebook_alias`
    uses, for the same reason).

    HONESTLY: unlike its neighbours this one does NOT fail against the old code —
    an unbounded slug is trivially injective. It guards the property the FIX
    could plausibly have broken (and that a bare `value[:200]` would have broken
    silently, one set overwriting another's manifest), which is why it is here."""
    stem = "lens " + " ".join(f"keyword-{i:03d}" for i in range(40))
    a, b = f"{stem} alpha", f"{stem} omega"
    assert wb.slug(a) != wb.slug(b)
    assert wb.manifest_relpath(a) != wb.manifest_relpath(b)
    assert wb.notebook_alias(a) != wb.notebook_alias(b)


_SLUG_IN_A_FRESH_INTERPRETER = """\
import sys
sys.path.insert(0, sys.argv[1])
from ideation_dashboard.workbench import slug
print(slug(sys.argv[2]))
"""


def _slug_in_another_process(name: str, *, hash_seed: str) -> str:
    """`workbench.slug(name)`, computed by a NEW interpreter under an explicit
    `PYTHONHASHSEED`. The seed is the point: it is the one input a same-process
    repeat holds fixed and a real second run does not."""
    return subprocess.run(
        [sys.executable, "-c", _SLUG_IN_A_FRESH_INTERPRETER,
         str(REPO_ROOT / "scripts"), name],
        capture_output=True, text=True, check=True,
        env={**os.environ, "PYTHONHASHSEED": hash_seed}).stdout.strip()


def test_a_truncated_slug_is_the_same_slug_in_the_next_process():
    """The keyed slug is a PERSISTED PATH KEY, so "deterministic" has to mean
    stable across PROCESSES, not within one.

    A same-process repeat (`slug(a) == slug(a)`) cannot show that and does not
    even fail against the way this would realistically break: swap FNV-1a for
    the builtin `hash()` — the obvious shortcut, since `_slug_key_digest` exists
    only to disambiguate — and the digest is stable within a run and DIFFERENT
    in the next one, because `PYTHONHASHSEED` randomizes str hashing per
    interpreter. A set saved today would then be unreachable tomorrow: `save`
    writes `<stem>-k<digest>.workbench.yaml`, and every later load, duplicate
    check and notebook alias re-derives that path from the name.

    So the comparison is against slugs computed in FRESH interpreters under two
    DIFFERENT explicit hash seeds — different actual and expected expressions,
    and the seeds are the axis the hazard lives on. Only a name past
    `MAX_SLUG_CHARS` exercises the digest; the short control confirms the long
    case is really the keyed branch."""
    long_name = "lens " + " ".join(f"keyword-{i:03d}" for i in range(40))
    here = wb.slug(long_name)
    # the premise, read off workbench itself rather than transcribed
    assert wb._SLUG_KEY_SEPARATOR in here and len(here) == wb.MAX_SLUG_CHARS, here
    short_name, short_here = "lens doc-health", wb.slug("lens doc-health")

    for seed in ("0", "1", "4294967295"):
        long_elsewhere = _slug_in_another_process(long_name, hash_seed=seed)
        short_elsewhere = _slug_in_another_process(short_name, hash_seed=seed)
        assert long_elsewhere == here, (seed, long_elsewhere)
        assert short_elsewhere == short_here, (seed, short_elsewhere)


def test_the_duplicate_check_refuses_instead_of_crashing_on_an_impossible_path(
        tmp_path, monkeypatch):
    """The crash was INSIDE the duplicate check, so the verb could not even
    refuse. `slug` is bounded now, which is the real fix; this pins the
    belt-and-braces half, because asking the filesystem about a path is a
    question that can always answer with an error."""
    (tmp_path / "ideation" / "workbench").mkdir(parents=True)
    # the parent must EXIST for the kernel to answer ENAMETOOLONG rather than
    # ENOENT — which is also why the sweep only hit this on a real corpus
    monkeypatch.setattr(wb, "manifest_relpath",
                        lambda name: f"ideation/workbench/{'x' * 400}.workbench.yaml")

    with pytest.raises(wb.WorkbenchError) as excinfo:
        gr._refuse_duplicate_set(tmp_path, "a set")

    assert "could not be checked" in str(excinfo.value)
    assert "Nothing was written" in str(excinfo.value)


def test_the_lens_save_recipe_route_survives_an_ordinary_wide_keyword_set(
        tmp_path):
    """End to end on the ROUTE at the scale that crashed it: the verb answers,
    the manifest lands, and the path it landed at is one the filesystem accepts.

    Not asserted as a refusal, deliberately — a wide lens set is ORDINARY usage of
    a shipped verb, and refusing it would be the second-best answer. It is now a
    bounded path instead."""
    snapshot = _snapshot()
    keywords = sorted({k for d in snapshot.get("documents", [])
                       for k in (d.get("topics") or [])})
    checked = keywords[:14] or keywords
    if len(checked) < 2:
        pytest.skip("the fixture corpus declares too few keywords")
    name = "lens " + " ".join(checked * 4)          # comfortably past the limit
    snapshot_path = tmp_path / "snapshot.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    root = tmp_path / "corpus"
    (root / "ideation" / "workbench").mkdir(parents=True)

    status, payload = gr.run_gate_action(
        "lens-save-recipe",
        {"name": name, "checked": checked, "pinned": [],
         "repository": snapshot["repository"]},
        checkout_root=root, actor="brett", snapshot_path=snapshot_path,
        # a stub that ACCEPTS: this test is about the derived PATH, and the
        # pinned validator is unreachable from a tmp_path corpus anyway
        manifest_validator=_passing_validator(tmp_path))

    assert status == 200, payload
    manifest = root / payload["manifest"]
    assert manifest.is_file()
    assert len(manifest.name.encode("utf-8")) <= _FS_COMPONENT_LIMIT


# --------------------------------------------------------------------------
# DEFECT 4 — a refusal leaves NOTHING behind
# --------------------------------------------------------------------------

def _failing_validator(tmp_path: Path) -> Path:
    """A stub pinned validator that always refuses — the shape the sweep hit was
    an UNREACHABLE validator, and a failing one is the same arm of the same
    branch, with the advantage of being hermetic and deterministic."""
    path = tmp_path / "refusing-validator.py"
    path.write_text("import sys\n"
                    "print('1 error(s): the stub validator refuses')\n"
                    "sys.exit(1)\n", encoding="utf-8")
    return path


def _passing_validator(tmp_path: Path) -> Path:
    path = tmp_path / "accepting-validator.py"
    path.write_text("print('0 error(s), 0 warning(s)')\n", encoding="utf-8")
    return path


def _workbench(name: str):
    return wb.Workbench.create("fixture-repo", name, now="2026-07-28T00:00:00Z")


def test_a_save_whose_validation_fails_writes_nothing_and_frees_the_name(
        tmp_path):
    """The unit test the suite never had: the existing ones assert the RAISE and
    never the filesystem afterwards.

    Three assertions, and the third is the one the human hit: the file is gone,
    the directory is as it was, and the IDENTICAL retry then succeeds — the name
    was permanently poisoned by an action the human was told had failed."""
    root = tmp_path / "corpus"
    (root / "ideation" / "workbench").mkdir(parents=True)
    boundary = HumanGate(root, [wb.WORKBENCH_DIR], human_actor="brett").output
    manifest = _workbench("refused set")
    rel = wb.manifest_relpath("refused set")

    with pytest.raises(wb.ManifestInvalid) as excinfo:
        wb.save(manifest, boundary, validate=True,
                validator=_failing_validator(tmp_path))

    assert not (root / rel).exists(), "a refusal must leave nothing behind"
    assert list((root / "ideation" / "workbench").iterdir()) == []
    assert "unwound" in str(excinfo.value)
    # …and the name is free: the identical retry succeeds
    written = wb.save(_workbench("refused set"), boundary, validate=True,
                      validator=_passing_validator(tmp_path))
    assert written.is_file() and written == root / rel


def test_a_failed_revalidation_restores_the_previous_manifest_byte_for_byte(
        tmp_path):
    """The other arm of the unwind: when the save OVERWROTE an existing manifest,
    "leave nothing behind" means the previous bytes, not an empty slot."""
    root = tmp_path / "corpus"
    (root / "ideation" / "workbench").mkdir(parents=True)
    boundary = HumanGate(root, [wb.WORKBENCH_DIR], human_actor="brett").output
    first = wb.save(_workbench("kept set"), boundary)
    before = first.read_bytes()
    second = _workbench("kept set")
    second.data["updated"] = "2026-07-28T01:00:00Z"

    with pytest.raises(wb.ManifestInvalid):
        wb.save(second, boundary, validate=True,
                validator=_failing_validator(tmp_path))

    assert first.read_bytes() == before


def test_a_refused_lens_save_recipe_leaves_no_manifest_and_no_record(tmp_path):
    """The route-level statement of the same thing, in the shape the human met it:
    `refused ✕`, HTTP 409 — and nothing on disk, so the retry is not blocked by an
    action that failed."""
    snapshot = _snapshot()
    keywords = sorted({k for d in snapshot.get("documents", [])
                       for k in (d.get("topics") or [])})[:2]
    if len(keywords) < 2:
        pytest.skip("the fixture corpus declares too few keywords")
    snapshot_path = tmp_path / "snapshot.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    root = tmp_path / "corpus"
    (root / "ideation" / "workbench").mkdir(parents=True)
    body = {"name": "lens " + " ".join(keywords), "checked": keywords,
            "pinned": [], "repository": snapshot["repository"]}

    status, payload = gr.run_gate_action(
        "lens-save-recipe", body, checkout_root=root, actor="brett",
        snapshot_path=snapshot_path,
        manifest_validator=_failing_validator(tmp_path))

    assert status == 409, payload
    assert payload["error"] == "gate_refused"
    assert list((root / "ideation" / "workbench").iterdir()) == [], (
        "the refused manifest is still on disk — it poisons the retry")
    assert not (root / RECORDS).exists() or not list(
        (root / RECORDS).rglob("*.gate-action.yaml"))
    # the retry, with a validator that accepts, is NOT blocked by a duplicate name
    retry_status, retry = gr.run_gate_action(
        "lens-save-recipe", body, checkout_root=root, actor="brett",
        snapshot_path=snapshot_path,
        manifest_validator=_passing_validator(tmp_path))
    assert retry_status == 200, retry
