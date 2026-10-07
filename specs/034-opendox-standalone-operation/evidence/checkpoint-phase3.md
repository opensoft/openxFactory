# Phase 3 checkpoint (T089)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T089
([`tasks.md`](../tasks.md)) · **Run**: 2026-10-05, 14:19–14:25Z, at openDox-code `dede32b4`, openXdox-code `56e1c238`
and openxFactory `36908480` · **Lane**: `openxfactory-4` (authored by lane
`openXfactory-3`, delegated: `#656` comment `5984809456`)

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`; T091). It runs and quotes every check T089 names, at the
commits phase 3 pinned: F4.1; F10.1 and F13.1, both as batch H amends them;
F16.1 as batches M and P amend it, with T100's named test; F5.2 whole, as T007's
batches C, F, G and K amend it, after T086's repair; then T098's interim F11.1.
Every check passes. F5.2's box closes here (RULED `5962785556`, item 1: *"F5.2's
box closes at phase 3's checkpoint (T089)"*), and so does F4.1's (plan 034's
box map: `F4.1 → T089`). T097 ticks both in #1144; this record ticks nothing
there. The last section records T092's phase-3 notes, which ride in this PR on
the holder's decision of 2026-10-05 (lane openxfactory-4's round-2
delegation, D5).

## Verdict

| # | T089's check | where it ran | result |
|---|---|---|---|
| 1 | F4.1 | openDox-code `dede32b4` | **PASS**, exit 0: `1 passed`, `1 passed`, then `no deferred reach names the consumer or the publisher` |
| 2 | F10.1, as batch H amends it | openDox-code `dede32b4`, `pip install ".[local]"` (`opendox-0.1.0`), `:8080` | **PASS**, exit 0: the bundled database, migrations `['0001', '0002']`; `0 violations`; `serving http://127.0.0.1:8080/index.html` |
| 3 | F13.1, as batch H amends it | openDox-code `dede32b4`, `:8080`-`:8083` | **PASS**, exit 0: the bundled database, migrations `['0001', '0002']`; every assertion holds, the last `grep -q OPENDOX_OIDC_ISSUER …/default.err` |
| 4 | F16.1, as batches M and P amend it, with T100's named test | openDox-code `dede32b4` | **PASS**, exit 0: `24 passed` (16.6), the dialect line, `no model configured: the catalog offers nothing`, `83 passed` (`tests/test_chat_model_configuration.py`), `532 passed` (`tests/test_model_binding_trust.py`, batch M's line) |
| 5 | F5.2 whole, as T007's batches C, F, G and K amend it, after T086's repair | openXdox-code `56e1c238`, openDox-code `dede32b4` installed over it, `OPENXFACTORY` at `36908480` | **PASS**, exit 0: the seven suites pass whole (45 passed, 23 passed, 18 passed, 6 passed, 40 passed, 9 passed, 12 passed); `test -s` holds; 5 `admitted:` lines and `ok: 5 protected edit(s), each entered and holding` |
| 6 | T098's interim F11.1 | openxFactory, `ARC_TIP` at `36908480` | **PASS**: quoted from T098's record (#1237 → `20ce593e`), and re-run here with the same line, `requirement 1 holds: 0 note(s) annotated, every other path a declared surface (11.1)` |

## The pins

Read from openxFactory `36908480` with `openDox` and `openXdox` initialized
recursively at its own gitlinks (`pins.sh`; every equality T090 keeps holds):

| where | pin | resolves to |
|---|---|---|
| openxFactory `openDox` gitlink and `contracts/opendox-pin.yaml` | openDox root `e1e3a3c3` | `code` → openDox-code `dede32b4`; `spec` → `f7ee3c76` |
| openxFactory `openXdox` gitlink and `contracts/openxdox-pin.yaml` | openXdox root `9564d5d9` | `code` → openXdox-code `56e1c238`; `spec` → `f088b097`; its own `contracts/opendox-pin.yaml` → openDox `e1e3a3c3` |
| openXdox-code `pyproject.toml` | `opendox @ git+https://github.com/opensoft/openDox-code@dede32b4b6f3d0f147d599776f83628c5af8ff3d` | the commit F5.2's suites would install, replaced by `OPENDOX_CODE` |

```
openxFactory HEAD 36908480b40b32509c308087d9d54e6c9d81759d  openDox root e1e3a3c3f8dd38214510412b71a2e858c6179532  openXdox root 9564d5d9462ffd1a3155d9177206368e5061efa8
ok    openDox root gitlink == contracts/opendox-pin.yaml commit: e1e3a3c3f8dd38214510412b71a2e858c6179532
ok    openXdox root gitlink == contracts/openxdox-pin.yaml commit: 9564d5d9462ffd1a3155d9177206368e5061efa8
ok    openDox root code gitlink == its contracts/code-pin.yaml commit: dede32b4b6f3d0f147d599776f83628c5af8ff3d
ok    openXdox root code gitlink == its contracts/code-pin.yaml commit: 56e1c238681a7693a4d8d42a62c1523cf4d4ab91
ok    openXdox-code's pyproject pins openDox-code at the openDox root's code commit (T090 step 3): dede32b4b6f3d0f147d599776f83628c5af8ff3d
ok    openXdox root's contracts/opendox-pin.yaml names the openDox root (T090 step 5): e1e3a3c3f8dd38214510412b71a2e858c6179532
```

The run's commits ARE the pinned ones: openDox-code `dede32b4` is the openDox root's `code`, and openXdox-code `56e1c238` the openXdox root's.

## How each check ran

- **The text is #1144's own.** Each block was extracted byte for byte from
  `openspec/changes/add-neutral-product-standalone-operability/tasks.md` at
  openxFactory `36908480` (sha256 `48db295594a6…`), BY ANCHOR (the block after its
  `FALSIFIED BY` line, never a fixed line number), and dedented by its six-space
  block indent. Each ruled amendment is an exact replacement that must match
  once. Every extraction reproduces the sha256 the earlier records quote:

  | falsifier | lines | as written | as run | amended by |
  |---|---|---|---|---|
  | F4.1 | `:500-549` | `8900b985e72f` | `8900b985e72f` | none (batches A, G and L are addenda that leave its Python alone) |
  | F10.1 | `:1548-1571` | `d94265449831` | `2358bd8f76ab` | batch H: `.[local]` and `--local` |
  | F13.1 | `:2668-2767` | `1e1f7da5564a` | `0a47fa31f5e0` | batch H: `.[local]` |
  | F16.1 | `:3604-3647` + `:3666-3667` | `fe22ec4873d1` | `619b32a955e2` | batch M: one line after the block's last (batch P adds notes and no line) |
  | F5.2 | `:698-721` | `808619e066fa` | `4b1512c26814` | batch G (`OPENXFACTORY`), batches C, F and K (`--chains`) |
  | F11.1 | `:1654-1733` | `60beede1244b` | `60beede1244b` | none (batches A and E widened it in place) |

- **Each ran from a fresh detached worktree** of its leg at the commit named,
  named exactly `openDox-code` or `openXdox-code`, with an empty
  `git status --porcelain --ignored`, from the checkout root, under `bash -x`,
  in the foreground of its wrapper. F11.1 ran from the root of the openxFactory
  checkout, which was clean too.
- **A scrubbed environment.** Each ran under `env -i` with only `HOME`, `USER`,
  `LOGNAME`, `SHELL`, `LANG=C.UTF-8`, `PATH`, `TMPDIR` and
  `PYTHONDONTWRITEBYTECODE=1` (and the variables each block itself requires),
  so no `GIT_*`, `XF_*`, `PG*`, `OPENDOX_*` or colour variable is inherited, and
  `omp` is on no run's `PATH`. Python 3.12.3, git 2.43.0, node v24.21.0
  (one F5.2 suite runs a node probe), curl 8.5.0; `python` resolves to the host's
  Python 3 through a `PATH` shim, because the host has no `python`.
- **A short `TMPDIR`.** The launch suite puts the bundled PostgreSQL's socket
  under pytest's base directory, and a socket path longer than 107 bytes
  fails, so every `TMPDIR` is short.
- **Ports.** F10.1 and F13.1 fix `:8080` (and F13.1 `:8081`-`:8083`), so they
  ran one after the other, each after a check that the four ports were free.
  F10.1 sets no `OPENDOX_STATE_DIR`, so its run was given its own short one.
- **`/tmp`.** `tests/standalone_child.py` writes each chat-suite child server's
  state directory as `/tmp/odx-child-*`, which no wrapper can redirect; the
  harness removes each on teardown.
- **pip's install log is elided.** Each block quotes the output after pip's
  last line, `Successfully installed …`, which is quoted too. In the quoted
  output the scratch directory's host path is written `<workdir>`, and the
  user `<user>` (Principle IV).

## 1. F4.1 (openDox-code `dede32b4`)

As extracted (sha256 `8900b985e72f`), run unchanged:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v4"                       # a FRESH environment: nothing already installed stands in
. "$W/v4/bin/activate"
pip install ".[test]"
if python -c "import corpus_adapter_openxfactory" 2>/dev/null; then echo "FAIL: the publisher's adapter is importable"; exit 1; fi
python3 - <<'PY'
import opendox.authoring as a
from opendox import corpus_adapter as ca
try:                                                  # NOTHING is registered in this process (4.2)
    got = a.required_header_fields()
except ModuleNotFoundError as e:
    raise SystemExit(f"FAIL: the deferred reach still imports a publisher module: {e}")
except ca.CorpusRefused as e:                         # the interface's ONE exception, and nothing else
    r = e.refusal
    assert r.kind == ca.ADAPTER_NOT_REGISTERED, f"refused for another reason: {r.kind!r}"
    assert "corpus_adapter" in r.subject, f"the refusal does not name the seam: {r.subject!r}"
    assert "register_home" in r.detail, f"the refusal does not name the remedy: {r.detail!r}"
else:
    raise SystemExit(f"FAIL: nothing is registered, yet the verb answered {got!r}")
PY
# ...a REGISTERED adapter answers through the seam, not through a name (4.1):
python -m pytest -q "tests/test_authoring_seam.py::test_required_header_fields_come_from_the_registered_adapter"
# ...and an ENTRY POINT registers openDox's own LocalGitCorpus where no host has (4.1a):
python -m pytest -q "tests/test_authoring_seam.py::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has"
# ...and NO deferred reach anywhere in the package names the consumer or the publisher (4.3):
if [ -e src/opendox/consumer_reach.py ]; then echo "FAIL: the late stand-in consumer_reach.py survives"; exit 1; fi
python3 - src/opendox <<'PY'
import ast, pathlib, sys
FOREIGN = ("openxdox", "ideation_dashboard", "corpus_adapter_openxfactory", "doc_health")
def named(node):
    if isinstance(node, ast.Import):
        return [a.name for a in node.names]
    if isinstance(node, ast.ImportFrom):
        return [node.module] if node.level == 0 and node.module else []
    if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
            and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("import_module", "__import__"):
        return [node.args[0].value] if isinstance(node.args[0].value, str) else []
    return []
def deferred(tree):                                   # every reach written INSIDE a function body
    for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))):
        for node in ast.walk(fn):
            yield from ((node.lineno, name) for name in named(node))
hits = sorted({f"{p}:{line}: {name}"
               for p in pathlib.Path(sys.argv[1]).rglob("*.py")
               for line, name in deferred(ast.parse(p.read_text(), str(p)))
               if any(name == f or name.startswith(f + ".") for f in FOREIGN)})
assert not hits, f"{len(hits)} deferred reach(es) still name the consumer or the publisher:\n  " + "\n  ".join(hits)
print("no deferred reach names the consumer or the publisher")
PY
```

**Exit 0.** The output, after pip:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 fastapi-0.142.2 fasteners-0.20 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.1.0 opentelemetry-api-1.45.0 packaging-26.3 pixeltable-pgserver-0.6.0 platformdirs-4.12.3 pluggy-1.6.0 psutil-7.2.2 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.4 setuptools-84.0.0 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 websockets-17.2
.                                                                        [100%]
1 passed in 0.54s
.                                                                        [100%]
1 passed in 0.73s
no deferred reach names the consumer or the publisher
```

## 2. F10.1, as batch H amends it (openDox-code `dede32b4`)

As extracted (sha256 `d94265449831`), with its amendment; the run (sha256
`2358bd8f76ab`) differs from the text as written by exactly these lines:

```diff
--- F10.1.as-written.sh
+++ F10.1.sh
@@ -5 +5 @@
-pip install .
+pip install ".[local]"
@@ -14 +14 @@
-opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
+opendox generate-and-open --local --repo-root "$R" --repository fixture --no-open --port 8080 &
```

The block as run:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v10"                      # a FRESH environment: nothing already installed stands in
. "$W/v10/bin/activate"
pip install ".[local]"
if python -c "import openxdox" 2>/dev/null; then echo "FAIL: sibling present"; exit 1; fi
opendox --help >/dev/null                       # the console script MUST exist
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
R=$(mktemp -d)/plain-documents
cp -r tests/fixtures/plain-documents "$R"   # a FRESH repository (preamble)
git -C "$R" init -q
git -C "$R" add -A
git -C "$R" commit -qm fixture
opendox generate-and-open --local --repo-root "$R" --repository fixture --no-open --port 8080 &
SERVER=$!
trap 'kill "$SERVER" 2>/dev/null || true' EXIT   # cleanup cannot mask the verdict
ready=0
for _ in $(seq 1 30); do
  if curl -sf http://127.0.0.1:8080/ >/dev/null; then ready=1; break; fi
  sleep 1
done
test "$ready" -eq 1                              # a server that never started FAILS here
curl -sf http://127.0.0.1:8080/ > "$W/bundle.html"   # no pipeline: curl's status is the status
grep -qi '<html' "$W/bundle.html"                # and it is really the bundle
```

**Exit 0.** The output, after pip:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 fastapi-0.142.2 fasteners-0.20 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 opendox-0.1.0 opentelemetry-api-1.45.0 pixeltable-pgserver-0.6.0 platformdirs-4.12.3 psutil-7.2.2 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 python-dotenv-1.2.4 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 websockets-17.2
  database <workdir>/state/st/C-F10.1/postgres/run (bundled, pid 3719075, migrations applied now: ['0001', '0002'])
wrote <workdir>/state/t/C-F10.1/opendox-2whw4dgg/snapshot.json
  repository=fixture kind=opendox-snapshot
  source_revision=98897b02ae98b11f9c58c45d450d9f332b350fb7
  generated_at=2026-10-05T14:19:55+00:00
  documents=8 clusters=2 possibles=1 staged_topics=1 changes=2 keywords=28
  validation: opendox-snapshot: 0 violations, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
  serving http://127.0.0.1:8080/index.html
  snapshot http://127.0.0.1:8080/snapshot.json
  console file://<workdir>/state/st/C-F10.1/console/8080.html (this user's private copy, mode 0600: open it to open the console page again)
  if your browser cannot open this file (a snap or Flatpak browser, or a Windows browser under WSL), set OPENDOX_STATE_DIR to a folder that is not hidden and start again
http://127.0.0.1:8080/index.html
  serving until interrupted (Ctrl-C to stop)
```

## 3. F13.1, as batch H amends it (openDox-code `dede32b4`)

As extracted (sha256 `1e1f7da5564a`), with its amendment; the run (sha256
`0a47fa31f5e0`) differs from the text as written by exactly these lines:

```diff
--- F13.1.as-written.sh
+++ F13.1.sh
@@ -6 +6 @@
-pip install .
+pip install ".[local]"
```

The block as run:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
# the install is group 10's, unchanged — one entry point, one command:
python -m venv "$W/v13"
. "$W/v13/bin/activate"
pip install ".[local]"
unset OPENDOX_DATABASE_URL OPENDOX_MIGRATION_DATABASE_URL OPENDOX_OIDC_ISSUER OPENDOX_INSTALL_MODE   # NONE of them set
export OPENDOX_STATE_DIR=$(mktemp -d)                 # a state directory NOTHING else has touched
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
R=$(mktemp -d)/plain-documents
cp -r tests/fixtures/plain-documents "$R"   # this group's OWN corpus, not Group 12's
git -C "$R" init -q
git -C "$R" add -A
git -C "$R" commit -qm fixture
opendox --help >/dev/null
# LOCAL mode starts, with no broker and no operator-supplied database:
OPENDOX_INSTALL_MODE=local opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8080/ >/dev/null && { ready=1; break; }; sleep 1; done
test "$ready" -eq 1
# the SERVING process reports its OWN mode and datastore, so the claim is about the server
# the user reached on :8080 and not about a second process that read the same settings:
curl -sf http://127.0.0.1:8080/capabilities > "$W/caps.json"
python3 - "$W/caps.json" <<'PY'
import json, os, sys
inst = json.load(open(sys.argv[1])).get("install") or {}
assert inst.get("mode") == "local", f"the server on :8080 is not in local mode: {inst}"
state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
for key in ("data_dir", "socket_dir"):
    got = os.path.realpath((inst.get("database_bundle") or {}).get(key, ""))
    assert got.startswith(state + os.sep), f"the served process uses {key} {got!r}, not the bundle under {state!r}"
PY
# and the bundled server has NO TCP listener, checked at the OS and not by self-report:
python3 - "$W/caps.json" <<'PY'
import json, os, re, sys
pid = ((json.load(open(sys.argv[1])).get("install") or {}).get("database_bundle") or {}).get("pid")
assert isinstance(pid, int), f"the bundle reports no server pid: {pid!r}"
inodes = set()
for fd in os.listdir(f"/proc/{pid}/fd"):
    try:
        m = re.match(r"socket:\[(\d+)\]", os.readlink(f"/proc/{pid}/fd/{fd}"))
    except OSError:
        continue
    if m:
        inodes.add(m.group(1))
listening = [(tbl, row.split()[1]) for tbl in ("/proc/net/tcp", "/proc/net/tcp6")
             for row in open(tbl).read().splitlines()[1:]
             if row.split()[3] == "0A" and row.split()[9] in inodes]   # 0A = TCP LISTEN
assert not listening, f"the bundled server listens on TCP: {listening}"
PY
# ...and what it answered from is the BUNDLED datastore, migrated (requirement 12):
OPENDOX_INSTALL_MODE=local opendox-runtime runtime status --probe-timeout 10 > "$W/status.json"
python3 - "$W/status.json" <<'PY'
import json, os, sys
s = json.load(open(sys.argv[1]))
assert s.get("database") == "reachable", f"no bundled database answered: {s}"
assert s.get("applied_migrations") and not s.get("pending_migrations"), f"not migrated: {s}"
state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
bundle = s.get("database_bundle") or {}
for key in ("data_dir", "socket_dir"):                 # the server that answered is the INSTALL'S OWN
    got = os.path.realpath(bundle.get(key, ""))
    assert got.startswith(state + os.sep), f"{key} {got!r} is not under the install's state dir {state!r}"
PY
kill "$SERVER"; wait "$SERVER" 2>/dev/null || true
# LOCAL mode REFUSES a non-loopback bind, BOUNDED, naming the rule (13.4):
rc=0
OPENDOX_INSTALL_MODE=local timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --host 0.0.0.0 --port 8083 >/dev/null 2>"$W/bind.err" || rc=$?
test "$rc" -ne 0                                      # refused, never started
test "$rc" -ne 124                                    # and not merely killed by the bound
grep -qi "loopback" "$W/bind.err"
# ONE DIALECT, and the two connections NOT COLLAPSED (13.2, 13.3), asked of the
# loader directly, with every other setting well-formed so the DSN is the only fault:
python3 - <<'PY'
from opendox.runtime.config import ConfigurationError, load_settings
OK = {"OPENDOX_OIDC_ISSUER": "https://issuer.example.invalid/realms/fixture",
      "OPENDOX_OIDC_AUDIENCE": "fixture"}
def refusal(**dsns):
    try:
        load_settings({**OK, **dsns})
    except ConfigurationError as e:
        return str(e)
    raise AssertionError(f"accepted: {dsns}")
m = refusal(OPENDOX_DATABASE_URL="sqlite:///x.db", OPENDOX_MIGRATION_DATABASE_URL="sqlite:///x.db")
assert "postgres" in m.lower(), f"a second dialect was refused for the wrong reason: {m}"
one = "postgresql://one@127.0.0.1/opendox"
m = refusal(OPENDOX_DATABASE_URL=one, OPENDOX_MIGRATION_DATABASE_URL=one)
assert "OPENDOX_MIGRATION_DATABASE_URL" in m, f"a collapsed pair was refused for the wrong reason: {m}"
PY
# every setting a HOSTED install needs EXCEPT the issuer, so the issuer is the only fault:
export OPENDOX_DATABASE_URL=postgresql://serve@127.0.0.1:1/opendox OPENDOX_MIGRATION_DATABASE_URL=postgresql://migrate@127.0.0.1:1/opendox OPENDOX_OIDC_AUDIENCE=fixture
# a HOSTED install with no issuer REFUSES — same server path, BOUNDED, naming the setting:
rc=0; OPENDOX_INSTALL_MODE=hosted timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8081 >/dev/null 2>"$W/hosted.err" || rc=$?
test "$rc" -ne 0
test "$rc" -ne 124   # refused: neither started, nor killed by the bound
grep -q "OPENDOX_OIDC_ISSUER" "$W/hosted.err"
# and the DEFAULT is hosted: the same install with the selector UNSET refuses identically:
rc=0; timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8082 >/dev/null 2>"$W/default.err" || rc=$?
test "$rc" -ne 0
test "$rc" -ne 124
grep -q "OPENDOX_OIDC_ISSUER" "$W/default.err"
```

**Exit 0.** The output, after pip:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 fastapi-0.142.2 fasteners-0.20 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 opendox-0.1.0 opentelemetry-api-1.45.0 pixeltable-pgserver-0.6.0 platformdirs-4.12.3 psutil-7.2.2 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 python-dotenv-1.2.4 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 websockets-17.2
  database <workdir>/state/t/C-F13.1/tmp.EQa3rzbMcH/postgres/run (bundled, pid 3723795, migrations applied now: ['0001', '0002'])
wrote <workdir>/state/t/C-F13.1/opendox-bsixxxv3/snapshot.json
  repository=fixture kind=opendox-snapshot
  source_revision=7139f371f8ed6fd1ab99f9e84636bd77b75abeee
  generated_at=2026-10-05T14:20:23+00:00
  documents=8 clusters=2 possibles=1 staged_topics=1 changes=2 keywords=28
  validation: opendox-snapshot: 0 violations, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
  serving http://127.0.0.1:8080/index.html
  snapshot http://127.0.0.1:8080/snapshot.json
  console file://<workdir>/state/t/C-F13.1/tmp.EQa3rzbMcH/console/8080.html (this user's private copy, mode 0600: open it to open the console page again)
  if your browser cannot open this file (a snap or Flatpak browser, or a Windows browser under WSL), set OPENDOX_STATE_DIR to a folder that is not hidden and start again
http://127.0.0.1:8080/index.html
  serving until interrupted (Ctrl-C to stop)
```

Its assertions print nothing when they hold. In the `bash -x` trace the block's last
command is `grep -q OPENDOX_OIDC_ISSUER <workdir>/state/t/C-F13.1/tmp.E8w167R73Q/default.err`, and then the
block's EXIT trap stops the local server it started.

## 4. F16.1, as batches M and P amend it (openDox-code `dede32b4`)

As extracted (sha256 `fe22ec4873d1`), with its amendment; the run (sha256
`619b32a955e2`) differs from the text as written by exactly these lines:

```diff
--- F16.1.as-written.sh
+++ F16.1.sh
@@ -44,0 +45,2 @@
+# a served repository's bindings are trusted per machine (16.3a):
+python -m pytest -q tests/test_model_binding_trust.py
```

The block as run:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v16"                      # a FRESH environment: nothing already installed stands in
. "$W/v16/bin/activate"
pip install ".[test]"
for sibling in openxdox ideation_dashboard; do        # chat is judged with no consumer and no publisher
  if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
done
if command -v omp >/dev/null 2>&1; then echo "FAIL: a harness is installed, so no-model is not what this measures"; exit 1; fi
# the boundary is ONE module wide, and its instrument passes WHOLE (16.6):
python -m pytest -q tests/test_provider_boundary.py
# the OpenAI-compatible dialect and the model name are declared (16.1, 16.2), and a raw key is refused (16.3):
python3 - <<'PY'
from opendox import doxbench_binding as b
assert "openai-chat-v1" in b.DIALECTS, f"no OpenAI-compatible dialect: {b.DIALECTS}"
assert "model" in b.BINDING_FIELDS, f"the record names no model: {b.BINDING_FIELDS}"
rec = {f: "stand-in" for f in b.BINDING_FIELDS}
rec.update(auth_kind=b.AUTH_KINDS[0], dialect="openai-chat-v1", endpoint="http://127.0.0.1:9/v1/chat/completions")
if "broker_argv" in rec:
    rec["broker_argv"] = ["stand-in-broker"]
b.ModelProviderBinding.from_record(rec)               # the control: a clean record is accepted
for bad in (dict(rec, endpoint="https://user:sk-stand-in@api.example.invalid/v1"),
            dict(rec, endpoint="https://api.example.invalid/v1?api_key=sk-stand-in"),
            dict(rec, api_key="sk-stand-in")):
    try:
        b.ModelProviderBinding.from_record(bad)
    except b.BindingRefused:
        continue
    raise SystemExit(f"FAIL: a raw key was accepted in {[k for k in bad if bad.get(k) != rec.get(k)]}")
print("dialect and model declared; a raw key is refused in a field and in the URL")
PY
# NO MODEL CONFIGURED is a state the catalog reports before any turn (16.4):
python3 - "$W" <<'PY'
import pathlib, sys
from opendox import doxbench_install as inst
root = pathlib.Path(sys.argv[1]) / "no-model"
root.mkdir()
port = inst.declared_model_port_factory(root / "sessions", checkout_root=root)()
offered = [e.model_id for e in port.catalog().available_entries()]
assert not offered, f"no model is configured, yet the catalog offers {offered}"
print("no model configured: the catalog offers nothing")
PY
# ...a turn reaches a stand-in OpenAI-compatible server on loopback, and every other surface answers with none (16.1-16.5):
python -m pytest -q tests/test_chat_model_configuration.py
# a served repository's bindings are trusted per machine (16.3a):
python -m pytest -q tests/test_model_binding_trust.py
```

**Exit 0.** The output, after pip:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 fastapi-0.142.2 fasteners-0.20 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.1.0 opentelemetry-api-1.45.0 packaging-26.3 pixeltable-pgserver-0.6.0 platformdirs-4.12.3 pluggy-1.6.0 psutil-7.2.2 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.4 setuptools-84.0.0 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 websockets-17.2
........................                                                 [100%]
24 passed in 0.84s
dialect and model declared; a raw key is refused in a field and in the URL
no model configured: the catalog offers nothing
........................................................................ [ 86%]
...........                                                              [100%]
83 passed in 32.79s
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 40%]
........................................................................ [ 54%]
........................................................................ [ 67%]
........................................................................ [ 81%]
........................................................................ [ 94%]
............................                                             [100%]
532 passed in 286.33s (0:04:46)
```

## 5. F5.2 whole, as batches C, F, G and K amend it (openXdox-code `56e1c238`, openDox-code `dede32b4`, openxFactory `36908480`)

F5.2 as extracted (sha256 `808619e066fa`), with batch G's environment lines and batches
C, F and K's last step; the run (sha256 `4b1512c26814`) differs from the text as written by:

```diff
--- F5.2.as-written.sh
+++ F5.2.sh
@@ -7,0 +8,4 @@
+# --- AS AMENDED, T007 batch G (5850003126, R1Q23 (a)): after the two installs, compose openxFactory at a NAMED commit.
+: "${OPENXFACTORY:?set OPENXFACTORY to an openxFactory checkout at a named commit}"
+export PYTHONPATH="$OPENXFACTORY/scripts"                                  # doc_health lives in that directory
+echo "=== OPENXFACTORY (an openxFactory checkout) at $(git -C "$OPENXFACTORY" rev-parse HEAD)"
@@ -17,8 +21,3 @@
-python3 - "$W/x-paths.txt" "$W/gen-suites.txt" <<'PY'
-import sys
-touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
-suites = {l.strip() for l in open(sys.argv[2]) if l.strip()}
-edited = sorted(touched & suites)
-if edited:
-    sys.exit("FAIL: the arc edited the governed projection's own proofs: " + ", ".join(edited))
-PY
+# --- AS AMENDED, T007 batches C, F and K (5817152735 R1Q7 (a); 5850003126 R1Q14 (a); 5916000030 item 4): the last step,
+# the inline Python that intersected the two lists, becomes the reviewed allow-list check, passing --chains.
+python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/gen-suites.txt")"
```

`OPENDOX_CODE` is a fresh openDox-code worktree at the commit above; `OPENXFACTORY`
is the openxFactory checkout, with `openDox` and `openXdox` initialized
recursively at its own gitlinks; `ARC_BASE` is openXdox-code's `e28930bf` (T003,
[`arc-base.md`](arc-base.md)).

### 5a. The run

**Exit 0.**

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.1.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.9.1 six-1.17.0 typing-extensions-4.16.0
Successfully installed opendox-0.1.0
=== OPENXFACTORY (an openxFactory checkout) at 36908480b40b32509c308087d9d54e6c9d81759d
.............................................                            [100%]
=================== open extraction: the declared exclusion ====================
declared exclusion: 66 files, listed in tests/declared_exclusion.yaml. 65 are left out of this run, and 1 is collected all the same, since pytest collects a file named on the command line whatever collect_ignore says. It is an OPEN extraction: each file runs again once its reason is cleared.
  reason doc_health (60 files): reaches openxFactory's doc_health, which openxFactory packages nowhere and no lone checkout supplies; open until the doc_health direction arc (plan 034 T008); ruled R1Q6 (d), openxFactory#656 comment 5817152735
  reason status-exemption-rail (3 files): needs openxFactory's status-exemption rail, which only openxFactory registers at openDox's status-exemption seam; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason openxfactory-contracts (5 files): reads openxFactory's contracts (the contract family's validator, schemas and examples, or its contracts/manifest.yaml) where openxFactory's tree keeps them, which is outside this checkout; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  excluded tests/test_authoring_agent.py: doc_health
  excluded tests/test_branch_session.py: doc_health
  excluded tests/test_canvas.py: doc_health
  excluded tests/test_column_contributions_governed.py: doc_health
  excluded tests/test_completeness.py: doc_health
  excluded tests/test_create_document_cli.py: doc_health
  excluded tests/test_create_project.py: doc_health
  excluded tests/test_doxbench_abstract_envelope.py: status-exemption-rail
  excluded tests/test_doxbench_abstract_route.py: doc_health
  excluded tests/test_doxbench_blank_reason.py: doc_health, openxfactory-contracts
  excluded tests/test_doxbench_knowledge_service.py: doc_health
  excluded tests/test_doxbench_mutation_boundary.py: doc_health
  excluded tests/test_doxbench_packet.py: doc_health, status-exemption-rail
  excluded tests/test_doxbench_request_handling.py: doc_health
  excluded tests/test_doxbench_save.py: doc_health
  excluded tests/test_doxbench_scope.py: doc_health
  excluded tests/test_doxbench_share.py: doc_health
  excluded tests/test_doxbench_thread_wiring.py: doc_health
  excluded tests/test_doxbench_threads.py: doc_health
  excluded tests/test_doxbench_transport.py: doc_health
  excluded tests/test_doxbench_turns.py: status-exemption-rail
  excluded tests/test_doxchat_model_intake.py: doc_health
  excluded tests/test_edit_action.py: doc_health
  excluded tests/test_edit_project.py: doc_health
  excluded tests/test_explorer_viewer.py: doc_health
  excluded tests/test_gate_console.py: doc_health
  excluded tests/test_gate_failure_diagnostics.py: doc_health
  excluded tests/test_gateway_provenance.py: doc_health
  excluded tests/test_generated_at_anchor.py: doc_health
  collected tests/test_generator.py: doc_health
  excluded tests/test_grouping.py: doc_health
  excluded tests/test_header_value_readers.py: doc_health
  excluded tests/test_hermeticity_gate_verbs.py: doc_health
  excluded tests/test_hosted_actor.py: doc_health
  excluded tests/test_kickoff.py: doc_health
  excluded tests/test_notebook_action.py: doc_health
  excluded tests/test_project_action_contracts.py: openxfactory-contracts
  excluded tests/test_project_aggregates.py: doc_health
  excluded tests/test_project_schema_election.py: openxfactory-contracts
  excluded tests/test_readiness_gate.py: doc_health
  excluded tests/test_register_edit_lane.py: doc_health
  excluded tests/test_renderer.py: doc_health
  excluded tests/test_repo_root_guard.py: doc_health
  excluded tests/test_repo_selector.py: doc_health
  excluded tests/test_round_trip.py: doc_health
  excluded tests/test_session_commits.py: doc_health
  excluded tests/test_session_confinement.py: doc_health
  excluded tests/test_session_document_ownership.py: doc_health
  excluded tests/test_session_gates.py: doc_health
  excluded tests/test_session_lifecycle.py: doc_health
  excluded tests/test_session_notebook.py: doc_health
  excluded tests/test_session_records.py: doc_health
  excluded tests/test_session_runbook.py: doc_health
  excluded tests/test_session_snapshot.py: doc_health
  excluded tests/test_session_transaction.py: doc_health
  excluded tests/test_session_verbs.py: doc_health
  excluded tests/test_snapshot_determinism.py: doc_health
  excluded tests/test_snapshot_registry.py: doc_health
  excluded tests/test_snapshot_validation_launch.py: doc_health
  excluded tests/test_source_dot_directories.py: doc_health
  excluded tests/test_staging_workbench.py: doc_health
  excluded tests/test_trust_gaps.py: doc_health
  excluded tests/test_validate_ideation_dashboard_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_action_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_model.py: doc_health
  excluded tests/test_wheel_verbs_cli.py: doc_health
45 passed in 3.29s
.......................                                                  [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_session_snapshot.py: doc_health
23 passed in 10.72s
..................                                                       [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. It has no `collected` line here, since the file this run names is not in the exclusion]
18 passed in 1.31s
......                                                                   [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_determinism.py: doc_health
6 passed in 0.79s
........................................                                 [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_registry.py: doc_health
40 passed in 1.66s
.........                                                                [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_validation_launch.py: doc_health
9 passed in 0.96s
............                                                             [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 5a, elided. It has no `collected` line here, since the file this run names is not in the exclusion]
12 passed in 0.62s
admitted: 839492d905f4 tests/test_session_snapshot.py, by entry 3 of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot.py, by entries 4, 5, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validation_launch.py, by entries 7, 8, 9, 10, 11, 12, 13, 14, 15, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validator_home.py, by entry 6 of tests/protected_suite_respellings.yaml
admitted: 56e1c238681a tests/test_session_snapshot.py, by entries 16, 17, 19, in that order, of tests/protected_suite_respellings.yaml
ok: 5 protected edit(s), each entered and holding
```

## 6. T098's interim F11.1

T098 ran F11.1 by T093's procedure, and its own PR recorded the run in
[`f11.1-phase3.txt`](f11.1-phase3.txt) (opensoft/openxFactory#1237 →
`20ce593e`), with `PACKET_MERGE=94b6f7f13b45c351b9142345738965c974b7dd37` and
`ARC_TIP=36908480b40b32509c308087d9d54e6c9d81759d`, T094's landing.

**Re-run here.** The same extraction (`:1654-1733`, sha256 `60beede1244b`),
in the openxFactory checkout at `36908480` with an empty `git status`, with the same
`PACKET_MERGE` and `ARC_TIP`. Exit 0, stderr empty:

```
requirement 1 holds: 0 note(s) annotated, every other path a declared surface (11.1)
```

The guard's count of annotated notes is 0 because no arc landing touches the
manifest. T092's phase-3 notes below are in this bookkeeping PR, which
carries no `Arc:` trailer, so the guard never reads them.

## T092's phase-3 notes, carried in this PR

T092 puts one `edits[].note` in `docs/opendox-carve-manifest.yaml` for each
reach a phase closed. Each phase's notes were to ride in its openxFactory pin
PR (T047, T064, T094). On the holder's decision of 2026-10-05, recorded in
lane openxfactory-4's round-2 delegation (D5) and in this PR's body, phase 3's
ride in this checkpoint PR instead, as phase 1's rode in T049's and phase 2's
in T063's. There are three notes on three rows (two added, one extended),
for the eleven reaches phase 3 closed.

This PR carries no `Arc:` trailer, so F11.1's count of annotated notes never
includes these notes. The checks below run F11.1's content rule over them
directly.

**The reaches phase 3 closed.** F4.1's scan (extracted at `:527-549`, sha256
`2c1bbe9f49f2`), run over `src/opendox` at five openDox-code commits, names
27 deferred reaches at `1e4a57fb` (4.3's measurement), 19 at `2d116415` (phase
1's pin), 11 at `047bb4fa` (phase 2's), and none at `e49b17c3` or at `dede32b4`
(T087's pin). Along the first-parent history from `047bb4fa` to `dede32b4`, the
count drops once, at T084's landing (openDox-code#77 → `e49b17c3`), which also
retires `consumer_reach.py`:

```
047bb4fa  11 reach(es)  consumer_reach.py=present  T058, the post-render validator in the generate verbs (7.2 part) (plan 034) (#68)
2680eb5e  11 reach(es)  consumer_reach.py=present  T085, the standalone doxBench defaults for T027's seams, and T058's two workbench rules move into opendox.validator (plan 034) (#71)
d0d3cee6  11 reach(es)  consumer_reach.py=present  T088, the lens's two seed actions are offered only where a binding answers them (R1Q19 (a)) (plan 034) (#65)
7ff434d9  11 reach(es)  consumer_reach.py=present  T071, 13.2 and 13.3: load_settings refuses a non-PostgreSQL DSN and a collapsed DSN pair (plan 034) (#60)
8a98e317  11 reach(es)  consumer_reach.py=present  T078, 16.1: the OpenAI-compatible dialect joins DIALECTS (plan 034) (#61)
66ff7257  11 reach(es)  consumer_reach.py=present  T070, 13.4-13.6: OPENDOX_INSTALL_MODE and generate-and-open --local (plan 034) (#67)
2fc714d2  11 reach(es)  consumer_reach.py=present  T079, 16.2: a model field the provider receives (plan 034) (#62)
9a490405  11 reach(es)  consumer_reach.py=present  T081, 16.4: "no model configured" is a state, shown before any turn (plan 034) (#74)
1130e996  11 reach(es)  consumer_reach.py=present  T080, 16.3: the credential stays a reference, and a raw key is refused (plan 034) (#63)
5e7ab003  11 reach(es)  consumer_reach.py=present  T072, 13.1: the bundled PostgreSQL server, the local install's own child (plan 034) (#69)
9197ccdd  11 reach(es)  consumer_reach.py=present  T075, 10.2 and 10.2a — an installed entry point serves all 42 bundle files; intent-feed.js is not owed (plan 034) (#73)
8e377823  11 reach(es)  consumer_reach.py=present  Broker-path credential hardening (follows T080): a minted token keeps a built-in credential's rules (plan 034) (#64)
90ac7033  11 reach(es)  consumer_reach.py=present  T073, 13.4a — /capabilities gains an install block, read from the serving process's own settings (plan 034) (#72)
e49b17c3   0 reach(es)  consumer_reach.py=GONE  T084, 4.3: the last deferred reaches through declared seams; consumer_reach retired (plan 034) (#77)   <-- drops
390e2c28   0 reach(es)  consumer_reach.py=GONE  T103, every loopback route checks the Host (DNS rebinding) (plan 034) (#80)
0116293a   0 reach(es)  consumer_reach.py=GONE  T102, the staging workbench offers the editors and the chat rail by scope (plan 034) (#81)
c4b55cc4   0 reach(es)  consumer_reach.py=GONE  T102 follow-on: the chat rail reads a thread only with a branch session (plan 034) (#85)
ca9e1bd5   0 reach(es)  consumer_reach.py=GONE  T082, 16.5: every other surface works with no model (plan 034) (#76)
38d3350e   0 reach(es)  consumer_reach.py=GONE  T100, 16.3a: a served repository's bindings are trusted per machine (plan 034) (#82)
32943cbf   0 reach(es)  consumer_reach.py=GONE  T104, the console token travels in the opened URL, not /capabilities (plan 034) (#84)
651c35fe   0 reach(es)  consumer_reach.py=GONE  T100 follow-on: the trust store's review findings (plan 034) (#86)
d59f3f26   0 reach(es)  consumer_reach.py=GONE  T099, publish openDox to PyPI by trusted publishing (10.3's install line) (plan 034) (#78)
dede32b4   0 reach(es)  consumer_reach.py=GONE  T099 release step: version 0.1.0 (plan 034) (#79)
```

The eleven are 4.3's last reaches into openXdox, and the three rows of
openXdox-code's ratchet `OPENDOX_BACK_IMPORTS` at phase 2's pins
(`branch_session.py` `(0, 2)`, `serve_project.py` `(0, 2)`, `serve_workbench.py`
`(0, 7)`). At `1e4a57fb`, where #1144 names them, they are
`branch_session.py:1587` and `:2005`, `serve_project.py:246` and `:247`, and
`serve_workbench.py:347`, `:407`, `:408`, `:544`, `:1215`, `:1665` and `:2607`.
Each is among the reaches T084's own text routes. At `047bb4fa` the scan
names them as:

```
  src/opendox/branch_session.py:1592: openxdox.register
  src/opendox/branch_session.py:2010: openxdox
  src/opendox/serve_project.py:271: openxdox.gate_console
  src/opendox/serve_project.py:272: openxdox.kickoff
  src/opendox/serve_workbench.py:351: openxdox
  src/opendox/serve_workbench.py:411: openxdox
  src/opendox/serve_workbench.py:412: openxdox
  src/opendox/serve_workbench.py:548: openxdox
  src/opendox/serve_workbench.py:1219: openxdox
  src/opendox/serve_workbench.py:1669: openxdox
  src/opendox/serve_workbench.py:2611: openxdox
```

The scan reads blobs, so it needs no checkout. Its `FOREIGN`, `named()` and
`deferred()` are F4.1's, byte for byte, and it lists git's tracked `*.py` files
under `src/opendox` where F4.1 globs a checkout. Its count at each of the
five commits (each hit is listed in the run's own output):

```python
"""reach-scan.py <openDox-code clone> <rev>... : F4.1's AST scan (#1144 4.3's measurement, the block's own `named` and
`deferred` logic, copied verbatim from the extracted F4.1 script) run over the BLOBS of src/opendox at each rev, with no
checkout. Prints, per rev, the count and the sorted `path:line: name` hits, plus whether src/opendox/consumer_reach.py
exists there. With --walk A..B it walks the first-parent commits of A..B (oldest first) and prints each commit's count, so
the landing that drops a reach is named, as T063's record did for phase 2."""
import ast, subprocess, sys

FOREIGN = ("openxdox", "ideation_dashboard", "corpus_adapter_openxfactory", "doc_health")
def named(node):
    if isinstance(node, ast.Import):
        return [a.name for a in node.names]
    if isinstance(node, ast.ImportFrom):
        return [node.module] if node.level == 0 and node.module else []
    if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
            and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("import_module", "__import__"):
        return [node.args[0].value] if isinstance(node.args[0].value, str) else []
    return []
def deferred(tree):                                   # every reach written INSIDE a function body
    for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))):
        for node in ast.walk(fn):
            yield from ((node.lineno, name) for name in named(node))

repo = sys.argv[1]
def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
def scan(rev):
    files = [p for p in git("ls-tree", "-r", "--name-only", rev, "--", "src/opendox").split() if p.endswith(".py")]
    hits = set()
    for p in files:
        src = git("show", f"{rev}:{p}")
        for line, name in deferred(ast.parse(src, p)):
            if any(name == f or name.startswith(f + ".") for f in FOREIGN):
                hits.add(f"{p}:{line}: {name}")
    return sorted(hits, key=lambda h: (h.split(":")[0], int(h.split(":")[1]))), ("src/opendox/consumer_reach.py" in files)

args = sys.argv[2:]
if args and args[0] == "--walk":
    a, b = args[1].split("..")
    revs = git("rev-list", "--first-parent", "--reverse", f"{a}..{b}").split()
    prev = None
    for r in [a] + revs:
        hits, cr = scan(r)
        subj = git("log", "-1", "--format=%s", r).strip()
        mark = "" if prev is None or len(hits) == prev else "   <-- drops" if len(hits) < prev else "   <-- RISES"
        print(f"{r[:8]}  {len(hits):2d} reach(es)  consumer_reach.py={'present' if cr else 'GONE'}  {subj}{mark}")
        prev = len(hits)
else:
    for r in args:
        hits, cr = scan(r)
        print(f"== {r}: {len(hits)} deferred reach(es) naming the consumer or the publisher; consumer_reach.py {'present' if cr else 'GONE'}")
        for h in hits:
            print("  " + h)
```

```
== 1e4a57fb: 27 deferred reach(es) naming the consumer or the publisher; consumer_reach.py present
== 2d116415: 19 deferred reach(es) naming the consumer or the publisher; consumer_reach.py present
== 047bb4fa: 11 deferred reach(es) naming the consumer or the publisher; consumer_reach.py present
== e49b17c3: 0 deferred reach(es) naming the consumer or the publisher; consumer_reach.py GONE
== dede32b4: 0 deferred reach(es) naming the consumer or the publisher; consumer_reach.py GONE
```

**The stand-ins `consumer_reach.py` still held take no note**, on the holder's
ruling (A) (`#656` comment `5994463071`). At `047bb4fa` it held five late
names, `gate_console`, `serve_gate`, `serve_projection`,
`LateGateRoutes` and `LateProjectionRoutes`, and T084 retires the file with
them: F4.1 checks that the file is gone, and it is gone at `dede32b4`. They are not among
4.3's counted reaches, which the scan reads, and the ruling reads T092 as
phase 2 did: T055 retired ten of the file's stand-ins (`snapshot`, `snapshot_registry`,
`corpus_root`, `generator`, `find_validator`, `corpus_root_refusal`,
`generate_snapshot`, `hosted_ref_refused`, `is_rfc3339_datetime` and
`scanned_roots`), and T063's three notes cover only the eight reaches the
scan counted.

**Each reach is a declared carve line.** The manifest numbers its lines in
the carve blob (`carve_commit` `b075fd91`). The carve rewrote each of these
eleven lines from an `ideation_dashboard` or relative import to `openxdox`,
so none is byte-identical to its carve line. Each sits in a `replace` block
of `difflib` over `carve_lines.text_records()` of the two blobs, with as many
lines on each side, so the pairing is exact. The carve line is in the `lines`
of one `import rewrites` entry, as the mapping prints (after this PR's
notes). The script is T063's, generalized to `equal` blocks too:

```python
# usage: PYTHONDONTWRITEBYTECODE=1 t092-reach-mapping-p3.py <openxFactory clone> <openDox-code clone> [manifest.yaml]
# Maps each reach phase 3 closes (#1144's 4.3 reaches into openXdox that F4.1's scan still names at phase 2's pin
# 047bb4fa, named here at openDox-code 1e4a57fb, where #1144 measures them) to its line in the carve blob (openxFactory
# carve_commit b075fd91, the manifest's numbering), through difflib over carve_lines.text_records() of the two blobs
# (T063's t092-reach-mapping-p2.py, generalized to `equal` as well as `replace` blocks), and names the edits[] entry
# whose `lines` hold that carve line, with whether it carries a note (in the manifest given, else origin/main's).
import difflib, pathlib, subprocess, sys, yaml
OXF, ODC = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
CARVE = "b075fd91dc8fced8e1373825ba80220c33536bae"; AT = "1e4a57fb"
sys.path.insert(0, str(OXF / "scripts")); import carve_lines
REACHES = [("branch_session.py", 1587), ("branch_session.py", 2005),
           ("serve_project.py", 246), ("serve_project.py", 247),
           ("serve_workbench.py", 347), ("serve_workbench.py", 407), ("serve_workbench.py", 408),
           ("serve_workbench.py", 544), ("serve_workbench.py", 1215), ("serve_workbench.py", 1665),
           ("serve_workbench.py", 2607)]
def blob(repo, rev, path):
    return subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], check=True, capture_output=True).stdout
manifest = yaml.safe_load(open(sys.argv[3], encoding="utf-8") if len(sys.argv) > 3 else
                         subprocess.run(["git", "-C", str(OXF), "show", "origin/main:docs/opendox-carve-manifest.yaml"],
                                        check=True, capture_output=True, text=True).stdout)
rows = {r["source_path"]: r for r in manifest["rows"]}
bad = 0
for f, n in REACHES:
    carve = carve_lines.text_records(blob(OXF, CARVE, f"scripts/ideation_dashboard/{f}"))
    arrived = carve_lines.text_records(blob(ODC, AT, f"src/opendox/{f}"))
    sm = difflib.SequenceMatcher(None, carve, arrived, autojunk=False)
    hit = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if j1 <= n - 1 < j2]
    tag, i1, i2, j1, j2 = hit[0]; k = n - 1 - j1
    if tag == "insert":
        print(f"{f}:{n} @{AT} -> NO carve line (insert arrived[{j1}:{j2}]): the line was added after the carve"); bad += 1; continue
    if tag == "replace" and (i2 - i1) != (j2 - j1):
        print(f"{f}:{n} @{AT} -> UNEVEN {tag} carve[{i1}:{i2}]/arrived[{j1}:{j2}]; the line below is by offset only")
    c = i1 + k + 1
    print(f"{f}:{n} @{AT} -> carve line {c} ({tag} carve[{i1}:{i2}]/arrived[{j1}:{j2}] offset {k})")
    print(f"    arrived: {arrived[n - 1].rstrip(chr(10))!r}")
    print(f"    carve  : {carve[c - 1].rstrip(chr(10))!r}")
    row = rows[f"scripts/ideation_dashboard/{f}"]
    ent = [(i, e) for i, e in enumerate(row.get("edits") or []) if c in e.get("lines", [])]
    for i, e in ent:
        print(f"    declared by: {row['source_path']} edits[{i}] ({e['class']}), note present: {'note' in e}")
    if len(ent) != 1:
        print(f"    !! carve line {c} is in {len(ent)} edits[] entries"); bad += 1
sys.exit(1 if bad else 0)
```

```
branch_session.py:1587 @1e4a57fb -> carve line 1574 (replace carve[1573:1574]/arrived[1586:1587] offset 0)
    arrived: '    from openxdox.register import CrossReferenceIndexAdapter'
    carve  : '    from .register import CrossReferenceIndexAdapter'
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
branch_session.py:2005 @1e4a57fb -> carve line 1992 (replace carve[1991:1992]/arrived[2004:2005] offset 0)
    arrived: "    from openxdox import kickoff as kickoff_mod   # lazy: mirrors gate_console's cycle note"
    carve  : "    from . import kickoff as kickoff_mod   # lazy: mirrors gate_console's cycle note"
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
serve_project.py:246 @1e4a57fb -> carve line 246 (replace carve[245:247]/arrived[245:247] offset 0)
    arrived: '        from openxdox.gate_console import DEFAULT_RECORDS_DIR'
    carve  : '        from ideation_dashboard.gate_console import DEFAULT_RECORDS_DIR'
    declared by: scripts/ideation_dashboard/serve_project.py edits[0] (import rewrites), note present: True
serve_project.py:247 @1e4a57fb -> carve line 247 (replace carve[245:247]/arrived[245:247] offset 1)
    arrived: '        from openxdox.kickoff import ('
    carve  : '        from ideation_dashboard.kickoff import ('
    declared by: scripts/ideation_dashboard/serve_project.py edits[0] (import rewrites), note present: True
serve_workbench.py:347 @1e4a57fb -> carve line 346 (replace carve[345:346]/arrived[346:347] offset 0)
    arrived: '        from openxdox import doxbench_scope'
    carve  : '        from ideation_dashboard import doxbench_scope'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:407 @1e4a57fb -> carve line 406 (replace carve[405:407]/arrived[406:408] offset 0)
    arrived: '        from openxdox import gate_console'
    carve  : '        from ideation_dashboard import gate_console'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:408 @1e4a57fb -> carve line 407 (replace carve[405:407]/arrived[406:408] offset 1)
    arrived: '        from openxdox import gate_routes'
    carve  : '        from ideation_dashboard import gate_routes'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:544 @1e4a57fb -> carve line 543 (replace carve[542:543]/arrived[543:544] offset 0)
    arrived: '        from openxdox import doxbench_scope'
    carve  : '        from ideation_dashboard import doxbench_scope'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:1215 @1e4a57fb -> carve line 1214 (replace carve[1212:1214]/arrived[1213:1215] offset 1)
    arrived: '        from openxdox import gate_console'
    carve  : '        from ideation_dashboard import gate_console'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:1665 @1e4a57fb -> carve line 1664 (replace carve[1661:1665]/arrived[1662:1666] offset 2)
    arrived: '        from openxdox import doxbench_scope'
    carve  : '        from ideation_dashboard import doxbench_scope'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
serve_workbench.py:2607 @1e4a57fb -> carve line 2606 (replace carve[2603:2607]/arrived[2604:2608] offset 2)
    arrived: '        from openxdox import doxbench_scope'
    carve  : '        from ideation_dashboard import doxbench_scope'
    declared by: scripts/ideation_dashboard/serve_workbench.py edits[0] (import rewrites), note present: True
```

**Each note is on the entry that declares its line**, and records the close:

```python
# usage: t092-note-check-p3.py <manifest.yaml> [AB]
# Each carve line phase 3 closed is in the `lines` of exactly one edits[] entry of its row,
# and that entry's note records the close (names phase 3 and the carve line). AB adds group B,
# the late stand-ins consumer_reach.py still held at phase 2's pin.
import sys, yaml
CLOSED = {"branch_session.py": [1574, 1992], "serve_project.py": [246, 247],
          "serve_workbench.py": [346, 406, 407, 543, 1214, 1664, 2606]}
if sys.argv[2:] == ["AB"]:
    CLOSED["branch_session.py"].append(77); CLOSED.update({"cli.py": [72], "serve.py": [628, 629]})
rows = {r["source_path"]: r for r in yaml.safe_load(open(sys.argv[1]))["rows"]}
ok = True
for f, lines in CLOSED.items():
    row = rows[f"scripts/ideation_dashboard/{f}"]
    for c in lines:
        ent = [(i, e) for i, e in enumerate(row.get("edits") or []) if c in e.get("lines", [])]
        closed = len(ent) == 1 and "CLOSED IN PHASE 3" in (ent[0][1].get("note") or "") and str(c) in ent[0][1]["note"].split("CLOSED IN PHASE 3", 1)[1]
        ok &= closed
        print(f"  {f} carve line {c}: " + ", ".join(f"edits[{i}] ({e['class']})" for i, e in ent) + f", note closed: {closed}")
print("every reach's carve line is in exactly one edits[] entry, and its note records the close" if ok else "FAIL")
sys.exit(0 if ok else 1)
```

```
  branch_session.py carve line 1574: edits[0] (import rewrites), note closed: True
  branch_session.py carve line 1992: edits[0] (import rewrites), note closed: True
  serve_project.py carve line 246: edits[0] (import rewrites), note closed: True
  serve_project.py carve line 247: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 346: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 406: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 407: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 543: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 1214: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 1664: edits[0] (import rewrites), note closed: True
  serve_workbench.py carve line 2606: edits[0] (import rewrites), note closed: True
every reach's carve line is in exactly one edits[] entry, and its note records the close
```

**F11.1's content rule holds.** The rule is the guard's `notes()` and
`without_notes()`, copied from #1144's `tasks.md`, and applied to `main`'s
manifest and this PR's. The script is T049's (`checkpoint-phase1.md`), byte
for byte. With every note removed, the two are equal. Two notes are new,
and the other begins with the note it extends (branch_session.py's first entry):

```python
# usage: t092-content-rule.py <manifest-before.yaml> <manifest-after.yaml>
# F11.1's manifest content rule (notes() and without_notes() copied from the committed guard,
# #1144 tasks.md), applied to one pair of manifests instead of to each Arc landing:
# with every edits[].note removed the two documents must be equal, and a note that
# already existed may only be extended.
import copy, sys, yaml
def notes(doc):
    return [[e.get("note") for e in (row.get("edits") or [])] for row in doc["rows"]]
def without_notes(doc):
    doc = copy.deepcopy(doc)
    for row in doc["rows"]:
        for e in row.get("edits") or []:
            e.pop("note", None)
    return doc
before, after = (yaml.safe_load(open(p)) for p in sys.argv[1:3])
if without_notes(before) != without_notes(after):
    sys.exit("FAIL: the manifest changed beyond an edit's note (a row, a field, a digest)")
breach, annotated = [], 0
for row, old_row, new_row in zip(after["rows"], notes(before), notes(after)):
    for i, (old, new) in enumerate(zip(old_row, new_row)):
        if old != new:
            annotated += 1
            kind = "added" if old is None else ("extended" if (new or "").startswith(old) else "REWRITTEN")
            print(f"  {kind}: {row['source_path']} edits[{i}]")
            if kind == "REWRITTEN":
                breach.append(f"{row['source_path']} edits[{i}]: rewrote an existing note instead of extending it")
if breach:
    sys.exit("FAIL:\n  " + "\n  ".join(breach))
print(f"F11.1's manifest content rule holds: {annotated} note(s) annotated, nothing else in the manifest moved")
```

```
  extended: scripts/ideation_dashboard/branch_session.py edits[0]
  added: scripts/ideation_dashboard/serve_project.py edits[0]
  added: scripts/ideation_dashboard/serve_workbench.py edits[0]
F11.1's manifest content rule holds: 3 note(s) annotated, nothing else in the manifest moved
```

`scripts/validate-carve-manifest.py` accepts the manifest:

```
OK docs/opendox-carve-manifest.yaml: phase post-shed, 456 row(s) at opensoft/openxFactory@b075fd91dc8f (opendox-carve-0), verified at 20ce593e8659 — 142 moved_verbatim, 176 moved_with_declared_edit, 138 not_moved; 318 digest(s) recomputed; 456 file(s) in the declared surface with none undeclared; 319 shed row(s) absent at source as declared; 4 row(s) RE-DESTINED by ruling (RULED Q6); 2 row(s) RETIRED by ruling (RULED 5656343213)
```

**Each landing the notes cite, re-verified at this run** (`closers-p3.py`:
GitHub's merge commit for each PR, its place on its repository's first-parent
line, and what the note says the landing did):

```
ok: T084: openDox-code#77 MERGED as e49b17c3 on main's first-parent line; consumer_reach.py present before, absent after; F4.1's scan 11 -> 0
ok: T086: openXdox-code#37 MERGED as 56e1c238 on main's first-parent line; OPENDOX_BACK_IMPORTS = {} with the (0, 0) assertion, its three rows dropped in the landing; column_contributions.register defined; openDox-code pin dede32b4, moved in this landing from 047bb4fa
ok: T087: openDox#18 MERGED as e1e3a3c3 on the openDox root's first-parent line; its `code` gitlink and code-pin.yaml name dede32b4, T086's pin; it carries e49b17c3; F4.1's scan reads 0 there and consumer_reach.py is absent
ok: T094: openxFactory#1236 MERGED as 36908480 on main's first-parent line with the Arc: trailer; its diff names column_contributions, and the host calls column_contributions.register (1 call site(s) under scripts/: scripts/opendox_host.py:949)
ok: T094's openDox gitlink e1e3a3c3 is on the openDox root's first-parent line at or after T087's e1e3a3c3, and pins the same openDox-code dede32b4
closers-p3: every landing T092's phase-3 notes cite is re-verified: {"T084_SHA8": "e49b17c3", "T086_PR": 37, "T086_SHA": "56e1c238681a7693a4d8d42a62c1523cf4d4ab91", "T086_SHA8": "56e1c238", "T087_ROOT": "e1e3a3c3f8dd38214510412b71a2e858c6179532", "T087_PIN": "dede32b4b6f3d0f147d599776f83628c5af8ff3d", "T094_OPENDOX_ROOT": "e1e3a3c3f8dd38214510412b71a2e858c6179532", "T094_PR": 1236, "T094_SHA": "36908480b40b32509c308087d9d54e6c9d81759d", "T094_SHA8": "36908480", "group": "A"}
```

