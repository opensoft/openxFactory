# Quickstart: running AT-R1, release 1's acceptance

**Feature**: [`spec.md`](./spec.md) § "AT-R1" defines the test.
T095 automates the HTTP half as a CI test in openDox-code. T096 runs the
browser half on the host.

The run needs the phase-3 tip of every repository, so every question that
blocks phases 2 and 3 is answered first. The steps below depend directly on
R1Q10, R1Q12 (the catalog's validators), R1Q13, R1Q15, R1Q16 and R1Q19. **Two
steps below are conditional**, and each is marked with the question it depends
on. Use whatever the openDox root's
`README.md` documents once 10.3 has landed: that README, not this file, is the
product's one documented command (requirement 10).

## 1. A clean machine, with openDox and nothing else

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time
: "${RELEASE1_TIP:?set RELEASE1_TIP to openDox-code's phase-3 tip}"
git clone -q https://github.com/opensoft/openDox-code "$W/openDox-code"
git -C "$W/openDox-code" checkout -q "$RELEASE1_TIP"
python3 -m venv --clear "$W/v"
. "$W/v/bin/activate"
pip install "$W/openDox-code"                         # CONDITIONAL (R1Q16): "$W/openDox-code[local]" if an extra is chosen
for s in openxdox ideation_dashboard doc_health corpus_adapter_openxfactory; do
  if python -c "import $s" 2>/dev/null; then echo "FAIL: $s is importable"; exit 1; fi
done
if command -v omp >/dev/null 2>&1; then echo "FAIL: a harness is installed, so no-model is not what this measures"; exit 1; fi
# ASSERTED, not assumed: no identity broker, and no database the user provided.
if command -v openprofiler-broker >/dev/null 2>&1; then echo "FAIL: an identity broker is installed"; exit 1; fi
unset OPENDOX_DATABASE_URL OPENDOX_MIGRATION_DATABASE_URL OPENDOX_OIDC_ISSUER OPENDOX_INSTALL_MODE DATABASE_URL PGHOST PGPORT PGDATABASE PGUSER
python3 - <<'PY'
import socket
for host in ("127.0.0.1", "::1"):
    try:
        s = socket.create_connection((host, 5432), timeout=1)
    except OSError:
        continue
    s.close()
    raise SystemExit(f"FAIL: a database already listens on {host}:5432")
print("no database listens on the default port")
PY
export OPENDOX_STATE_DIR=$(mktemp -d)                 # a state directory nothing else has touched
test -z "$(ls -A "$OPENDOX_STATE_DIR")"
```

T095 makes the same assertions in CI, and step 2 below asserts that neither
repository holds a model binding.

## 2. Two plain git repositories

```sh
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
A=$(mktemp -d)/plain-documents                        # (a) 5.0's fixture
cp -r "$W/openDox-code/tests/fixtures/plain-documents" "$A"
git -C "$A" init -q
git -C "$A" add -A
git -C "$A" commit -qm fixture
B=$(mktemp -d)/plain-notes                            # (b) ordinary Markdown with NO front matter at all
mkdir -p "$B"
printf '# Roadmap\n\nThe roadmap links to the [budget](budget.md) and the [notes](notes.md).\n' > "$B/roadmap.md"
printf '# Budget\n\nBudget figures for the roadmap.\n' > "$B/budget.md"
printf '# Meeting notes\n\nWe discussed the roadmap and the budget.\n' > "$B/notes.md"
git -C "$B" init -q
git -C "$B" add -A
git -C "$B" commit -qm notes
for R in "$A" "$B"; do                                # no model binding: doxbench_binding's DEFAULT_BINDINGS_RELPATH is absent
  if test -e "$R/ideation/dashboard/model-provider-bindings.yaml"; then echo "FAIL: $R holds a model binding"; exit 1; fi
done
```

## 3. The one documented command, then the HTTP half (T095)

Run §§ 3–5 once with `R="$A"`, then again with `R="$B"`. Each pass starts its
own server and stops it in § 5.

```sh
R="$A"
PORT=8080
python3 - "$PORT" <<'PY'
import socket, sys
port = int(sys.argv[1])
for host in ("127.0.0.1", "::1"):
    try:
        s = socket.create_connection((host, port), timeout=1)
    except OSError:
        continue
    s.close()
    raise SystemExit(f"FAIL: something already listens on {host}:{port}, so a ready answer would not come from this run")
print(f"port {port} is free")
PY
# CONDITIONAL (R1Q15): the recommended answer (b) selects local mode explicitly, shown here as --local.
opendox generate-and-open --local --repo-root "$R" --repository fixture --no-open --port "$PORT" &
SERVER=$!
trap 'kill "$SERVER" 2>/dev/null || true' EXIT
ready=0
for _ in $(seq 1 30); do
  kill -0 "$SERVER" 2>/dev/null || { echo "FAIL: the launched server exited before it answered"; exit 1; }
  if curl -sf "http://127.0.0.1:$PORT/" >/dev/null; then ready=1; break; fi
  sleep 1
done
test "$ready" -eq 1
kill -0 "$SERVER"                                     # the port was free before launch, so this process is the one answering
curl -sf "http://127.0.0.1:$PORT/" > "$W/index.html"
grep -qi '<html' "$W/index.html"
curl -sf "http://127.0.0.1:$PORT/snapshot.json" > "$W/snap.json"
curl -sf "http://127.0.0.1:$PORT/capabilities" > "$W/caps.json"
curl -sf "http://127.0.0.1:$PORT/workbench/model-catalog" > "$W/catalog.json"
python3 - "$W/snap.json" "$W/caps.json" "$W/catalog.json" <<'PY'
import json, sys
snap, caps, cat = (json.load(open(p)) for p in sys.argv[1:4])
assert snap.get("documents"), "the snapshot is empty"
assert (caps.get("install") or {}).get("mode") == "local", caps.get("install")
available = [m["model_id"] for m in cat["models"] if m["available"]]   # xfactory-workbench-model-catalog
assert not available, f"no model is configured, yet the catalog offers {available}"
print("HTTP half: bundle, neutral snapshot, local mode, and an empty catalog")
PY
```

The catalog's shape is openDox-spec's `xfactory-workbench-model-catalog`
schema, which requires `models[]`, and each model carries `model_id` and
`available`. T095 also requests every route the wheel, the lens and the chat
rail call when they load (`/workbench/thread` among them), and requires that
none of them answers 5xx.

## 4. The browser half (T096)

This needs Playwright and its Chromium on the host (`pip install playwright`,
then `python -m playwright install chromium`). The verdict comes from
openDox-code's `tests/smoke_signals.py`: every console error and every failed
request must be DECLARED, and `pageerror` cannot be declared at all. With the
server from § 3 running, in this order:

1. Load `http://127.0.0.1:$PORT/`, and collect `console`, `pageerror` and
   `requestfailed` from the first byte onwards.
2. **Wheel.** Click `#tab-wheel`. It must render a tile for every station
   that the snapshot fills.
3. **Radar lens.** Click `#tab-lens`. The bullseye must render the documents
   as dots, and the text "nothing on the radar" must be absent. The two seed
   actions must behave as R1Q19 decides; under (a), neither is offered.
4. **Chat.** On the wheel, use a grouping tile's `workbench` verb. The staging
   workbench must open, and BEFORE any turn its chat rail must show the "no
   model configured" state, naming how to configure a model. Attempting a turn
   must be refused with `model_capability_unavailable`. Both editors must stay
   usable. Repository (b) must also yield a grouping tile (R1Q13); if it
   yields none, the run FAILS and does not skip.
5. The verdict comes from `smoke_signals`: zero `pageerror`, nothing
   undeclared, and no 5xx.

Screenshots of steps 2–4 and the oracle's printed verdict go in
`specs/034-opendox-standalone-operation/evidence/at-r1/`, with no `Arc:`
trailer (R1Q20 (a), ruled in `5817152735`).

## 5. Tear down

```sh
kill "$SERVER"
wait "$SERVER" 2>/dev/null || true                    # the port is free again before the next pass
```

The bundled datastore stops with the entry point (R1Q16 (iv)). After the second
pass, with `R="$B"`, remove the scratch space: `rm -rf "$W" "$OPENDOX_STATE_DIR"`.
