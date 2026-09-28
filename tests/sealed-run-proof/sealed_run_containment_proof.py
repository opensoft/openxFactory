#!/usr/bin/env python3
"""The real-docker proof for #1191: every sealed run of the finalize job runs
in a container, and what a hostile seal does there stays there.

NOT A TEST MODULE. pytest collects `test_*.py` and `*_test.py` only, so this
file is never collected, and CI's pytest-suite counts are unchanged by it
(the tests run the lane against a stand-in docker instead). It needs a docker
daemon, the network the first time the image is built, and a working
directory the daemon can mount from:

    python3 tests/sealed-run-proof/sealed_run_containment_proof.py \\
        --work-dir DIR [--daemon-path-map LOCAL=DAEMON] [--fresh-build] \\
        [--skip-real-seal] [--keep]

It lives outside `tests/ideation-dashboard/`, which is the openDox carve
surface (`docs/opendox-carve-manifest.yaml`). A file that appears there
needs a re-cut of the manifest, and a proof is no reason for one.

`--daemon-path-map` is for a checkout in a dev container that reaches the
host's daemon through its socket, where the daemon sees the same directory
under another path. The lane resolves each mount source to its real path
(`_mountable`), which is right on a runner, where the daemon shares the job's
filesystem, so the proof rewrites the `source=` of each `--mount`, and nothing
else, from LOCAL to DAEMON. The argv it prints is the lane's, before that.

What runs, each through the lane's own functions and the workflow's own
steps, never through copies of them:
  1. the finalize job's build step, read out of the workflow and run under
     its own shell, which records SEALED_IMAGE;
  2. a hostile seal, run through the lane's `SealedContainer`: planted PATH
     executables and writes aimed at the runner, a detached nohup child and
     a double-forked daemon that ignore every signal (with a control run on
     the runner, as the lane ran sealed code before #1191), a
     workflow-command flood past each bound and through the fence, a
     snapshot that is not a regular file, a render that never finishes, and
     the process and memory bounds;
  3. the real seal phase of this checkout, as the seal step runs it
     (`dashboard_refresh_lane.main`, which `scripts/dashboard-refresh-nightly.py`
     calls), whose probe, render and `--strict` validation run as three
     containers of the run's label;
  4. the job's last step, read out of the workflow, after which no container
     and no image of the run is left.
Each check prints PASS or FAIL. The exit status is 1 when any check failed.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import textwrap
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from ideation_dashboard import dashboard_refresh_lane as lane  # noqa: E402

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml"
DOCKER = "/usr/bin/docker"
SOURCE_HEAD = "5eed" * 10
COMMITTED_AT = "2026-09-27T00:00:00Z"
CANARIES = {"GH_TOKEN": "canary-gh-token-1191",
            "GITHUB_TOKEN": "canary-github-token-1191",
            "ACTIONS_RUNTIME_TOKEN": "canary-runtime-token-1191",
            "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "canary-oidc-token-1191"}
FAILURES: list[str] = []
RUNS: list[dict] = []


def check(ok: bool, what: str, detail: str = "") -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {what}"
          + (f"\n        {detail}" if detail else ""))
    if not ok:
        FAILURES.append(what)
    return bool(ok)


def heading(text: str) -> None:
    print(f"\n== {text}")


# THE LANE, OBSERVED. Every sealed run goes through `SealedContainer.run`,
# which builds its argv with `SealedContainer.argv`. Both are wrapped at the
# class, so the lane's own instances are observed too: the argv is recorded
# as the lane built it, then mapped for the daemon when a map is given, and
# each run's result is recorded as the lane received it.
def observe_the_lane(path_map: tuple[str, str] | None) -> None:
    built_argv = lane.SealedContainer.argv
    built_run = lane.SealedContainer.run

    def argv(self, *args, **kwargs):
        made = built_argv(self, *args, **kwargs)
        RUNS.append({"argv": list(made)})
        if path_map is None:
            return made
        local, daemon = path_map
        return [part.replace(f"source={local}", f"source={daemon}", 1)
                if part.startswith("type=bind,") else part for part in made]

    def run(self, what, seal_root, command, **kwargs):
        start = time.monotonic()
        try:
            result = built_run(self, what, seal_root, command, **kwargs)
        except lane.SealRefused as exc:
            RUNS[-1].update(what=what, command=list(command),
                            refused=str(exc),
                            seconds=round(time.monotonic() - start, 2))
            raise
        RUNS[-1].update(what=what, command=list(command), result=result,
                        seconds=round(time.monotonic() - start, 2))
        return result

    lane.SealedContainer.argv = argv
    lane.SealedContainer.run = run


def docker(*args: str, check_rc: bool = False) -> subprocess.CompletedProcess:
    done = subprocess.run([DOCKER, *args], capture_output=True, text=True,
                          timeout=300)
    if check_rc and done.returncode != 0:
        raise SystemExit(f"docker {' '.join(args)} failed: {done.stderr}")
    return done


def containers_of(label: str) -> list[str]:
    return docker("ps", "-aq", "--filter", f"label={label}").stdout.split()


def finalize_step(**match) -> dict:
    import yaml
    steps = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))[
        "jobs"]["finalize"]["steps"]
    if not match:
        return steps[-1]
    return next(step for step in steps
                if all(step.get(k) == v for k, v in match.items()))


def run_step(step: dict, script: Path, env: dict, *,
             rewrite=None) -> subprocess.CompletedProcess:
    """A workflow step's own script under its own shell, as the runner runs
    it: `shell` with `{0}` the script's path."""
    text = step["run"] if rewrite is None else rewrite(step["run"])
    script.write_text(text, encoding="utf-8")
    argv = [part if part != "{0}" else str(script)
            for part in step["shell"].split()]
    return subprocess.run(argv, env=env, capture_output=True, text=True,
                          timeout=900)


def tree_listing(root: Path) -> dict[str, str]:
    """Every entry under `root`, directories and links included, as what it
    is: its kind, mode and size, a file's digest, a link's target."""
    listing: dict[str, str] = {}
    for base, dirs, files in os.walk(root):
        for name in sorted(dirs + files):
            path = Path(base) / name
            info = path.lstat()
            kind = stat.S_IFMT(info.st_mode)
            entry = f"{kind:o} {stat.S_IMODE(info.st_mode):o} {info.st_size}"
            if stat.S_ISREG(info.st_mode):
                entry += " " + hashlib.sha256(path.read_bytes()).hexdigest()
            elif stat.S_ISLNK(info.st_mode):
                entry += " -> " + os.readlink(path)
            listing[str(path.relative_to(root))] = entry
    return listing


# THE HOSTILE SEAL. Each render below is sealed code: the child's own render
# entry, `scripts/ideation-dashboard-cli.py`, as a hostile seal would carry
# it. The lane runs it as `RENDER_ENTRY generate ... --output /out/...` from
# the sealed corpus root, inside the wrapper, in the container.
PRELUDE = textwrap.dedent('''\
    import json, os, sys
    ARGS = sys.argv[1:]

    def arg(name):
        return ARGS[ARGS.index(name) + 1]

    def write_snapshot(proof=None):
        record = {"generation": {"source_revision": arg("--source-revision"),
                                 "generated_at": arg("--generated-at")},
                  "documents": []}
        if proof is not None:
            record["proof"] = proof
        with open(arg("--output"), "w", encoding="utf-8") as handle:
            json.dump(record, handle)
    ''')

PLANT_TARGETS = ("/seal/openxFactory/gh", "/seal/gh", "/usr/local/bin/gh",
                 "/usr/bin/gh", "/bin/gh", "/tmp/gh", "/out/gh",
                 "/proc/1/root/usr/local/bin/gh", "/home/runner/work/_temp/gh",
                 "/github/workspace/gh")

RENDER_PLANT = PRELUDE + textwrap.dedent(f'''\
    import shutil, socket, subprocess
    report = {{}}
    status = dict(line.split(":", 1) for line in
                  open("/proc/self/status").read().splitlines() if ":" in line)
    report["id"] = f"{{os.getuid()}}:{{os.getgid()}}"
    report["CapEff"] = status["CapEff"].strip()
    report["NoNewPrivs"] = status["NoNewPrivs"].strip()
    report["environ"] = dict(os.environ)
    report["which"] = {{name: shutil.which(name) for name in
                        ("python3", "sh", "cat", "git", "gh", "docker")}}
    plant = {{}}
    for target in {PLANT_TARGETS!r}:
        try:
            with open(target, "w") as handle:
                handle.write("#!/bin/sh\\necho PLANTED-BY-THE-RENDER\\n")
            os.chmod(target, 0o755)
        except OSError as exc:
            plant[target] = f"not written: {{exc.strerror}}"
            continue
        try:
            ran = subprocess.run([target], capture_output=True, timeout=5)
            plant[target] = f"written, and it RAN: exit {{ran.returncode}}"
        except OSError as exc:
            plant[target] = f"written in the run's own tmpfs, cannot run: {{exc.strerror}}"
    report["plant"] = plant
    network = {{}}
    for host, port in (("140.82.112.3", 443), ("1.1.1.1", 53)):
        try:
            socket.create_connection((host, port), timeout=3).close()
            network[f"{{host}}:{{port}}"] = "CONNECTED"
        except OSError as exc:
            network[f"{{host}}:{{port}}"] = f"refused: {{exc.strerror or exc}}"
    try:
        socket.getaddrinfo("github.com", 443)
        network["dns github.com"] = "RESOLVED"
    except OSError as exc:
        network["dns github.com"] = f"refused: {{exc}}"
    report["network"] = network
    report["docker_socket"] = [path for path in
                               ("/var/run/docker.sock", "/run/docker.sock")
                               if os.path.exists(path)]
    report["mounts"] = {{line.split()[1]: line.split()[3] for line in
                        open("/proc/self/mounts").read().splitlines()
                        if line.split()[1] in ("/", "/seal", "/tmp", "/out")}}
    print("::add-path::/seal/openxFactory")
    write_snapshot(report)
    ''')

RENDER_DETACH = PRELUDE + textwrap.dedent('''\
    import signal, subprocess, time
    pids = os.environ.get("PROOF_PIDS")
    nohup = subprocess.Popen(
        ["nohup", "/bin/sh", "-c",
         "trap '' HUP INT TERM; i=0; while [ $i -lt 90 ]; do "
         "echo still-here >&2; i=$((i+1)); sleep 1; done"],
        start_new_session=True)
    first = os.fork()
    if first == 0:
        os.setsid()
        if os.fork() == 0:
            for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, signal.SIG_IGN)
            if pids:
                with open(pids, "a") as handle:
                    handle.write(f"{os.getpid()}\\n")
            time.sleep(90)
            os._exit(0)
        os._exit(0)
    os.waitpid(first, 0)
    if pids:
        with open(pids, "a") as handle:
            handle.write(f"{nohup.pid}\\n")
    time.sleep(1)
    write_snapshot({"nohup_pid": nohup.pid})
    ''')

FLOOD_LINES = ("::add-path::/seal/openxFactory\n"
               "::set-env name=GH_TOKEN::pwned\n"
               "::add-mask::pwned\n"
               "::stop-commands::0123456789abcdef0123456789abcdef\n"
               "::error title=sealed::a flood\n")

RENDER_FLOOD_LOG = PRELUDE + textwrap.dedent(f'''\
    chunk = ({FLOOD_LINES!r} * 2000).encode()
    sent = 0
    while sent < 3 * 1024 * 1024:
        os.write(2, chunk)
        sent += len(chunk)
    write_snapshot({{"stderr_bytes": sent}})
    ''')

# The wrapper sends the render's stdout to the log stream, and `/out` is a
# 32 MiB tmpfs, but the container's own stdout is reachable through
# /proc/1/fd/1 (docker-init's). So the stdout bound is the one that holds.
RENDER_FLOOD_STDOUT = PRELUDE + textwrap.dedent('''\
    chunk = b"::add-path::/seal/openxFactory\\n" * 32768
    with open("/proc/1/fd/1", "wb", buffering=0) as stdout:
        for _ in range(40):
            stdout.write(chunk)
    write_snapshot({"stdout_bytes": 40 * len(chunk)})
    ''')

RENDER_HANG = PRELUDE + textwrap.dedent('''\
    import signal, time
    for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, signal.SIG_IGN)
    time.sleep(3600)
    ''')

RENDER_KINDS = {
    "a link to a sealed file": PRELUDE + textwrap.dedent('''\
        os.symlink("/seal/openxFactory/scripts/ideation-dashboard-cli.py",
                   arg("--output"))
        '''),
    "a directory": PRELUDE + "os.mkdir(arg('--output'))\n",
    "a fifo": PRELUDE + "os.mkfifo(arg('--output'))\n",
}

RENDER_PIDS = PRELUDE + textwrap.dedent('''\
    import subprocess
    children, refused = [], None
    for _ in range(400):
        try:
            children.append(subprocess.Popen(["/usr/bin/sleep", "30"]))
        except OSError as exc:
            refused = f"{exc.strerror} after {len(children)} processes"
            break
    for child in children:
        child.kill()
    for child in children:
        child.wait()
    write_snapshot({"started": len(children), "refused": refused})
    ''')

RENDER_MEMORY = PRELUDE + textwrap.dedent('''\
    blocks = [bytearray(64 * 1024 * 1024) for _ in range(24)]
    write_snapshot({"allocated_mib": 64 * len(blocks)})
    ''')

RENDER_HONEST = PRELUDE + "write_snapshot()\n"

GUESS = "0123456789abcdef0123456789abcdef"
HOSTILE_FINDINGS = [
    "::add-path::/seal/openxFactory",
    "::set-env name=GH_TOKEN::pwned",
    f"::stop-commands::{GUESS}",
    f"::{GUESS}::",
    "::error title=sealed::the seal says it passed",
    "::set-output name=sealed::true",
    "ERROR [sealed-code] snapshot.json: a finding sealed code wrote",
]

# The sealed product module the validator's runs are read by is sealed code
# too, so a hostile seal answers a verdict of its own, carrying a flood.
PRODUCT_HOSTILE = textwrap.dedent(f'''\
    from dataclasses import dataclass

    @dataclass
    class _Result:
        ok: bool
        returncode: int
        stdout: str
        stderr: str
        outcome: str
        unavailable_reason: object = None

    def validate_snapshot(target, *, validator, strict):
        lines = {HOSTILE_FINDINGS!r} * 10
        return _Result(False, 1, "\\n".join(lines), "", "not-conformant")
    ''')

PLANTED_NAMES = ("python3", "sh", "cat", "git", "gh", "docker")


def make_seal(root: Path, render: str, *, product: str | None = None) -> Path:
    """A hostile seal: `render` as the render entry, an executable named
    after each tool a step or a sealed run calls, beside the render's working
    directory and in a `bin/` of its own, and a sealed product module."""
    corpus = root / lane.SEAL_CORPUS_RELPATH
    (corpus / "scripts").mkdir(parents=True)
    (corpus / lane.RENDER_ENTRY).write_text(render, encoding="utf-8")
    for where in (corpus, root / "bin"):
        where.mkdir(exist_ok=True)
        for name in PLANTED_NAMES:
            planted = where / name
            planted.write_text(f"#!/bin/sh\necho 'PLANTED {name} RAN' >&2\n"
                               f"echo 'PLANTED {name} RAN'\n")
            planted.chmod(0o755)
    module = lane.sealed_product_module(root)
    module.parent.mkdir(parents=True)
    (module.parent / "__init__.py").write_text("")
    module.write_text(product or "raise SystemExit('no product here')\n")
    validator = root / lane.SEAL_VALIDATOR_RELPATH
    validator.parent.mkdir(parents=True)
    validator.write_text("# the validator the sealed product is handed\n")
    return root


def render(seal: Path, container, *, timeout: int = 120):
    """The lane's own sealed render: `_run_the_sealed_render`."""
    return lane._run_the_sealed_render(
        seal, source_head=SOURCE_HEAD, source_committed_at=COMMITTED_AT,
        container=container, timeout=timeout)


def refused_by(call) -> str | None:
    try:
        call()
    except lane.SealRefused as exc:
        return str(exc)
    return None


def nothing_left(label: str, what: str) -> None:
    left = containers_of(label)
    check(not left, f"no container of the run's label is left after {what}",
          f"docker ps -a --filter label={label}: {left or 'none'}")


def prove_the_build(work: Path, env: dict, fresh: bool) -> str:
    heading("1. The finalize job's build step, run under its own shell")
    step = finalize_step(id="dfr-sealed-image")
    github_env = work / "github-env"
    github_env.write_text("")
    started = time.monotonic()
    done = run_step(step, work / "build-step.sh",
                    {**env, "GITHUB_ENV": str(github_env)},
                    rewrite=(lambda text: text.replace(
                        "/usr/bin/docker build \\",
                        "/usr/bin/docker build --no-cache \\", 1))
                    if fresh else None)
    print(f"  shell: {step['shell']}  ({round(time.monotonic() - started)} s,"
          f" exit {done.returncode}{', --no-cache' if fresh else ''})")
    for line in (done.stdout + done.stderr).splitlines():
        if ("Successfully installed" in line or "Downloading" in line
                or "CACHED" in line or "naming to" in line):
            print(f"    {line.strip()[:160]}")
    recorded = dict(line.split("=", 1) for line in
                    github_env.read_text().splitlines() if "=" in line)
    image = recorded.get("SEALED_IMAGE", "")
    check(done.returncode == 0 and lane._SEALED_IMAGE_RE.fullmatch(image)
          is not None, "the build step records the image id in GITHUB_ENV",
          f"SEALED_IMAGE={image}")
    if done.returncode != 0:
        print(done.stdout[-3000:], done.stderr[-3000:])
        raise SystemExit(1)
    labels = json.loads(docker("image", "inspect", "--format",
                               "{{json .Config.Labels}}", image).stdout)
    label = (f"{lane.SEALED_RUN_LABEL}={env['GITHUB_RUN_ID']}-"
             f"{env['GITHUB_RUN_ATTEMPT']}")
    check(labels.get(lane.SEALED_RUN_LABEL) == label.split("=", 1)[1],
          "the image carries this run's label from the moment it exists",
          f"{lane.SEALED_RUN_LABEL}={labels.get(lane.SEALED_RUN_LABEL)}")
    return image


def prove_the_image_holds_the_lock(work: Path, container) -> None:
    empty = work / "empty-seal"
    empty.mkdir()
    run = container.run(
        "listing", empty,
        [lane.SEALED_PYTHON, "-m", "pip", "list", "--format=freeze",
         "--disable-pip-version-check"],
        workdir="/tmp", stdout_limit=lane.SEALED_LOG_LIMIT, timeout=120)
    def normal(name: str) -> str:    # PEP 503's normalized name
        return re.sub(r"[-_.]+", "-", name).lower()

    installed = {normal(line.split("==")[0]): line.split("==")[1]
                 for line in run.stdout.decode().split() if "==" in line}
    installed.pop("pip", None)
    pinned = {normal(name): version for name, version in re.findall(
        r"'([A-Za-z0-9_.-]+)==(\S+) --hash=",
        finalize_step(id="dfr-sealed-image")["run"])}
    locked = {}
    lock = REPO_ROOT / "requirements" / "hermes-runtime-contracts.lock"
    for line in lock.read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith((" ", "#")):
            name, version = line.split(" ")[0].split("==")
            locked[normal(name)] = version
    check(installed == pinned and len(pinned) == 9
          and all(locked.get(name) == version
                  for name, version in pinned.items()),
          "the image holds exactly the nine distributions the build step "
          "pins, each at the lock's version, and pip",
          ", ".join(f"{k}=={v}" for k, v in sorted(installed.items())))


def prove_the_planted_executables(work: Path, container, label: str) -> None:
    heading("2a. Planted PATH executables, and writes aimed at the runner")
    seal = make_seal(work / "seal-plant", RENDER_PLANT)
    before_seal = tree_listing(seal)
    before_work = tree_listing(work)
    snapshot = json.loads(render(seal, container))
    report = snapshot["proof"]
    run = RUNS[-1]["result"]
    print("  the render reported, from inside its container:")
    for target, outcome in report["plant"].items():
        print(f"    plant {target}: {outcome}")
    for name, where in report["which"].items():
        print(f"    which {name}: {where}")
    for key in ("id", "CapEff", "NoNewPrivs"):
        print(f"    {key}: {report[key]}")
    for mount, options in report["mounts"].items():
        print(f"    mount {mount}: {options.split(',lowerdir')[0]}")
    for probe, outcome in report["network"].items():
        print(f"    network {probe}: {outcome}")
    print(f"    environment: {sorted(report['environ'])}")
    check(not any("RAN" in outcome for outcome in report["plant"].values()),
          "nothing the render planted could run: each write is refused by "
          "the read-only root and seal, or lands in its own noexec tmpfs")
    check(all(outcome.startswith("not written")
              for target, outcome in report["plant"].items()
              if not target.startswith(("/tmp/", "/out/"))),
          "no write reaches the seal, the image, or any path of the runner's")
    check(b"PLANTED" not in run.stderr and b"PLANTED" not in run.stdout,
          "none of the executables the seal plants beside the render's "
          "working directory ran: every command is called by its absolute path")
    check(report["which"]["gh"] is None and report["which"]["git"] is None
          and report["which"]["docker"] is None,
          "no planted gh, git or docker is on the run's PATH")
    uid_gid = f"{os.getuid()}:{os.getgid()}"
    check(report["id"] == uid_gid and report["CapEff"] == "0000000000000000"
          and report["NoNewPrivs"] == "1",
          "the run is this runner's non-root uid, with no capability and no "
          "new privileges", f"{report['id']}, CapEff {report['CapEff']}")
    check(report["mounts"].get("/", "").startswith("ro")
          and report["mounts"].get("/seal", "").startswith("ro")
          and "noexec" in report["mounts"].get("/tmp", "")
          and "noexec" in report["mounts"].get("/out", ""),
          "the root and the seal are read-only, /tmp and /out noexec")
    check(all(not outcome.startswith(("CONNECTED", "RESOLVED"))
              for outcome in report["network"].values())
          and not report["docker_socket"],
          "no network, and no docker socket")
    env_values = " ".join(f"{k}={v}" for k, v in report["environ"].items())
    check(not any(value in env_values for value in CANARIES.values())
          and not any(name in report["environ"] for name in CANARIES)
          and not any(name.startswith(("GITHUB_", "ACTIONS_", "RUNNER_"))
                      for name in report["environ"]),
          "none of the job's variables reaches the run, the canary tokens "
          "set in this process least of all")
    check(tree_listing(seal) == before_seal,
          "the seal is byte for byte as it was, every entry and mode")
    after_work = tree_listing(work)
    check(after_work == before_work,
          "nothing new anywhere under the proof's working directory, which "
          "holds the job's temporary directory",
          f"{len(set(after_work) ^ set(before_work))} entries differ")
    nothing_left(label, "the planted render")


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    try:
        state = Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1][0]
    except (OSError, IndexError):
        return True
    return state != "Z"


def prove_the_detached_children(work: Path, container, label: str) -> None:
    heading("2b. A detached nohup child and a double-forked daemon")
    # THE CONTROL: the same render, run on this runner as the lane ran sealed
    # code before #1191. Its children are benign (they sleep, then exit, and
    # are killed here), and they show what the container stops.
    control = work / "control-detach"
    (control / "scripts").mkdir(parents=True)
    entry = control / lane.RENDER_ENTRY
    entry.write_text(RENDER_DETACH, encoding="utf-8")
    pids_file = control / "pids"
    proc = subprocess.Popen(
        [sys.executable, str(entry), "generate", "--source-revision",
         SOURCE_HEAD, "--generated-at", COMMITTED_AT, "--output",
         str(control / "snapshot.json")],
        cwd=control, env={"PATH": "/usr/bin:/bin", "PROOF_PIDS": str(pids_file)},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.communicate(timeout=10)
        held_open = False
    except subprocess.TimeoutExpired:
        held_open = True
    render_done = proc.poll() is not None
    pids = [int(line) for line in pids_file.read_text().split()] \
        if pids_file.exists() else []
    alive = [pid for pid in pids if _alive(pid)]
    check(render_done and held_open and len(alive) == 2,
          "control, on the runner: the render returned, and 10 s later its "
          "two children are alive and still hold its output open",
          f"render exited {proc.returncode}; children {pids}, alive {alive}")
    for pid in pids:
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, signal.SIGKILL)
    with contextlib.suppress(subprocess.TimeoutExpired):
        proc.communicate(timeout=15)
    # THE SEALED RUN: the same render, through the lane.
    seal = make_seal(work / "seal-detach", RENDER_DETACH)
    started = time.monotonic()
    written = render(seal, container)
    took = time.monotonic() - started
    run = RUNS[-1]["result"]
    lines = run.stderr.decode().count("still-here")
    check(json.loads(written)["proof"]["nohup_pid"] > 0 and took < 20,
          "in its container, the run returns as soon as the render does: "
          "its children die with the container's init",
          f"{took:.1f} s; 'still-here' printed {lines} time(s) of the 90 "
          "it would print")
    nothing_left(label, "the detached render")
    time.sleep(3)
    nothing_left(label, "3 s more")


def prove_the_floods(work: Path, container, label: str) -> None:
    heading("2c. A workflow-command flood")
    seal = make_seal(work / "seal-flood-log", RENDER_FLOOD_LOG)
    reason = refused_by(lambda: render(seal, container))
    run = RUNS[-1]["result"]
    check(reason is not None and "for the log" in reason
          and "::" not in reason,
          "a flood of workflow commands past the log bound is refused, and "
          "the refusal carries none of it", reason or "not refused")
    check(run.stderr_over and len(run.stderr) == lane.SEALED_LOG_LIMIT,
          "the lane kept exactly the bound of it",
          f"kept {len(run.stderr)} of the 3 MiB+ it printed")
    nothing_left(label, "the log flood")

    seal = make_seal(work / "seal-flood-stdout", RENDER_FLOOD_STDOUT)
    reason = refused_by(lambda: render(seal, container))
    run = RUNS[-1]["result"]
    check(reason is not None and "streamed more than" in reason,
          "a flood written past the wrapper, into the container's own stdout, "
          "is refused at the snapshot bound", reason or "not refused")
    check(run.stdout_over and len(run.stdout) == lane.SEALED_SNAPSHOT_LIMIT,
          "the lane kept exactly the bound of it",
          f"kept {len(run.stdout)} of the 40 MiB it wrote")
    nothing_left(label, "the stdout flood")

    heading("2d. The strict findings of a hostile seal, into the job's log")
    seal = make_seal(work / "seal-fence", RENDER_HONEST, product=PRODUCT_HOSTILE)
    try:
        lane.precheck_sealed_render(
            seal, source_head=SOURCE_HEAD, source_committed_at=COMMITTED_AT,
            container=container, timeout=120)
        rejected = None
    except lane.StrictGateRejected as exc:
        rejected = exc
    except lane.SealRefused as exc:
        rejected = None
        print(f"    refused instead: {exc}")
    check(rejected is not None and rejected.detail,
          "the hostile verdict reaches the lane as a strict rejection with "
          "its findings, as the seal phase records one",
          f"{len(rejected.detail) if rejected else 0} finding lines")
    if rejected is None:
        return
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        lane._print_fenced(rejected.detail)
    lines = printed.getvalue().splitlines()
    token = lines[0].removeprefix("::stop-commands::")
    body = lines[1:-1]
    print("  what the seal phase prints after its STRICT FAILED warning:")
    for line in lines[:5] + ["  ..."] + lines[-2:]:
        print(f"    {line}")
    check(lines[0] == f"::stop-commands::{token}" and len(token) == 32
          and lines[-1] == f"::{token}::" and token != GUESS
          and all(token not in line for line in rejected.detail),
          "every line sealed code wrote sits inside a fence whose token it "
          "never saw, so the runner takes none of its workflow commands")
    check(body == [f"  {line}" for line in rejected.detail]
          and any("::stop-commands::" in line for line in body)
          and any(f"::{GUESS}::" in line for line in body),
          "the guessed fence and its guessed close are inside it, as text")
    nothing_left(label, "the fenced verdict")


def prove_the_rest(work: Path, container, label: str) -> None:
    heading("2e. A render that never finishes")
    seal = make_seal(work / "seal-hang", RENDER_HANG)
    started = time.monotonic()
    reason = refused_by(lambda: render(seal, container, timeout=5))
    took = time.monotonic() - started
    check(reason is not None and "did not finish within 5s" in reason
          and took < 60,
          "a render that ignores every signal is refused at its timeout, "
          "and its container is removed", f"{took:.1f} s: {reason}")
    nothing_left(label, "the render that never finished")

    heading("2f. A snapshot that is not a regular file of the render's own")
    for kind, source in RENDER_KINDS.items():
        seal = make_seal(work / f"seal-kind-{kind.split()[-1]}", source)
        reason = refused_by(lambda seal=seal: render(seal, container))
        check(reason is not None and "(exit 3)" in reason
              and "left no regular file" in reason,
              f"{kind} at the output path is refused by the wrapper, exit 3",
              reason or "not refused")
    nothing_left(label, "the output kinds")

    heading("2g. The process and memory bounds")
    seal = make_seal(work / "seal-pids", RENDER_PIDS)
    proof = json.loads(render(seal, container))["proof"]
    check(proof["refused"] is not None and proof["started"] < 128,
          "the run cannot start more than --pids-limit 128 processes",
          f"started {proof['started']}, then: {proof['refused']}")
    seal = make_seal(work / "seal-memory", RENDER_MEMORY)
    reason = refused_by(lambda: render(seal, container))
    check(reason is not None and "(exit 137)" in reason,
          "a render past --memory 1g is killed, and refused",
          reason or "not refused")
    nothing_left(label, "the bounds")


def prove_the_real_seal(work: Path, env: dict, label: str) -> None:
    heading("3. The real seal phase of this checkout, as the seal step runs it")
    corpus_head = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", lane.DEFAULT_CORPUS_REF],
        capture_output=True, text=True, check=True).stdout.strip()
    recipe_revision = subprocess.run(
        ["gh", "api", f"repos/{lane.DEFAULT_RECIPE_REPO}/commits/"
         f"{lane.DEFAULT_RECIPE_REF}", "--jq", ".sha"],
        capture_output=True, text=True, check=True).stdout.strip()
    workspace = work / "workspace"
    workspace.mkdir()
    (workspace / "dfr-decision.json").write_text(json.dumps({
        "build": True, "outcome": "build", "reason": "the #1191 proof",
        "result": "ok", "corpus_revision": corpus_head,
        "recipe_revision": recipe_revision}))
    # The seal step's own arguments, run from the job's workspace, with the
    # corpus checkout named by its path rather than as `openxFactory` in it.
    argv = ["--repo-root", ".", "--phase", "seal",
            "--corpus-checkout", str(REPO_ROOT),
            "--decision-in", "dfr-decision.json",
            "--seal-out", "dfr-seal",
            "--seal-result-out", "dfr-seal-result.json",
            "--correlation-id", "proof-1191"]
    print(f"  dashboard-refresh-nightly.py {shlex.join(argv)}")
    print(f"  corpus {lane.DEFAULT_CORPUS_REF} = {corpus_head}, recipe "
          f"{lane.DEFAULT_RECIPE_REPO}@{recipe_revision}")
    first = len(RUNS)
    since = f"{time.time():.9f}"
    saved = os.getcwd()
    os.chdir(workspace)
    try:
        started = time.monotonic()
        status = lane.main(argv)
        took = time.monotonic() - started
    finally:
        os.chdir(saved)
    until = str(int(time.time()) + 1)
    result = json.loads((workspace / "dfr-seal-result.json").read_text())
    check(status is None and result.get("sealed") is True,
          "the seal phase seals this checkout's corpus",
          f"{took:.0f} s; sealed={result.get('sealed')}, "
          f"reason={result.get('reason')}")
    runs = RUNS[first:]
    for run in runs:
        outcome = run.get("result")
        print(f"    {run.get('what')}: exit "
              f"{outcome.returncode if outcome else '-'}, "
              f"{len(outcome.stdout) if outcome else 0} bytes out, "
              f"{run.get('seconds')} s{', refused: ' + run['refused'] if 'refused' in run else ''}")
    check([run.get("what") for run in runs]
          == ["validator", "render", "validator"]
          and all(run.get("result") and run["result"].returncode == 0
                  for run in runs),
          "the probe, the render and its --strict validation each ran as "
          "one sealed container, each to exit 0")
    events = docker("events", "--since", since, "--until", until,
                    "--filter", "type=container", "--filter",
                    f"label={label}", "--format",
                    "{{.Action}} {{.Actor.ID}} "
                    "{{index .Actor.Attributes \"exitCode\"}}").stdout
    # Per container that STARTED in the seal's window: how it died, and
    # whether its --rm destroyed it.
    actions: dict[str, list[str]] = {}
    for line in events.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            actions.setdefault(parts[1], []).append(
                parts[0] if parts[0] != "die" else f"die:{parts[2:] and parts[2]}")
    started_here = {cid: seen for cid, seen in actions.items()
                    if "start" in seen}
    check(len(started_here) == 3
          and all("die:0" in seen and "destroy" in seen
                  for seen in started_here.values()),
          "the daemon's own events: three containers of the run's label "
          "started during the seal, each died with exit 0 and was destroyed "
          "by its --rm",
          "; ".join(f"{cid[:12]}: {' '.join(seen)}"
                    for cid, seen in started_here.items()))
    precheck = json.loads((workspace / "dfr-seal" / "manifest.json")
                          .read_text())["precheck"]
    check(precheck.get("outcome") == "validated" and precheck.get("strict")
          and precheck.get("documents", 0) > 0,
          "the manifest's precheck is the containers' verdict: --strict "
          "validated the render of the sealed corpus",
          json.dumps(precheck, sort_keys=True))
    render_run = next(run for run in runs if run.get("what") == "render")
    print("\n  THE INVOCATION, verbatim as the lane built it for the render"
          " (before any daemon path map):")
    print("    " + shlex.join(render_run["argv"] + render_run["command"]))
    nothing_left(label, "the real seal")


def prove_the_scrub(work: Path, env: dict, image: str, label: str) -> None:
    heading("4. The job's last step, run under its own shell")
    step = finalize_step()
    done = run_step(step, work / "scrub-step.sh",
                    {**env, "SEALED_IMAGE": image})
    check(done.returncode == 0 and "::error::" not in done.stdout,
          "the last step ends clean", f"exit {done.returncode}"
          + (f": {done.stdout.strip()}" if done.stdout.strip() else ""))
    gone = docker("image", "inspect", image).returncode != 0
    labelled = docker("image", "ls", "-aq", "--no-trunc", "--filter",
                      f"label={label}").stdout.split()
    check(gone and not labelled and not containers_of(label),
          "no image and no container of the run is left",
          f"image inspect {'fails' if gone else 'still finds it'}; "
          f"labelled images {labelled or 'none'}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--work-dir", required=True, type=Path,
                        help="a directory the docker daemon can mount from")
    parser.add_argument("--daemon-path-map", default=None,
                        help="LOCAL=DAEMON: where the daemon sees LOCAL")
    parser.add_argument("--fresh-build", action="store_true",
                        help="build with --no-cache, so every wheel is "
                             "downloaded and checked against its hash")
    parser.add_argument("--skip-real-seal", action="store_true")
    parser.add_argument("--keep", action="store_true",
                        help="keep this run's working directory")
    args = parser.parse_args()
    path_map = tuple(args.daemon_path_map.split("=", 1)) \
        if args.daemon_path_map else None
    work = args.work_dir.resolve() / f"run-{int(time.time())}"
    work.mkdir(parents=True)
    runner_temp = work / "runner-temp"
    runner_temp.mkdir()
    run_id = f"9{int(time.time())}"
    env = {"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "HOME": str(work),
           "RUNNER_TEMP": str(runner_temp), "GITHUB_RUN_ID": run_id,
           "GITHUB_RUN_ATTEMPT": "1"}
    label = f"{lane.SEALED_RUN_LABEL}={run_id}-1"
    print(f"#1191 real-docker proof: {work}")
    print(f"  docker {docker('version', '--format', '{{.Client.Version}} client / {{.Server.Version}} server').stdout.strip()}")
    print(f"  this runner's uid:gid {os.getuid()}:{os.getgid()}; label {label}")
    if path_map:
        print(f"  daemon path map: mount sources under {path_map[0]} are "
              f"mounted from {path_map[1]}")
    image = prove_the_build(work, env, args.fresh_build)
    observe_the_lane(path_map)
    os.environ.update(RUNNER_TEMP=str(runner_temp), TMPDIR=str(runner_temp),
                      SEALED_IMAGE=image, GITHUB_RUN_ID=run_id,
                      GITHUB_RUN_ATTEMPT="1")
    container = lane.resolve_sealed_container()
    check(container.label == label and container.image == image
          and container.docker == DOCKER,
          "the lane resolves its container from the build step's record",
          f"{container.image} as {container.uid}:{container.gid}, "
          f"{container.label}, {container.docker}")
    prove_the_image_holds_the_lock(work, container)
    os.environ.update(CANARIES)
    try:
        prove_the_planted_executables(work, container, label)
        prove_the_detached_children(work, container, label)
        prove_the_floods(work, container, label)
        prove_the_rest(work, container, label)
    finally:
        for name in CANARIES:
            os.environ.pop(name, None)
    if not args.skip_real_seal:
        prove_the_real_seal(work, env, label)
    prove_the_scrub(work, env, image, label)
    print(f"\n{len(FAILURES)} check(s) failed" if FAILURES
          else "\nevery check passed")
    for failure in FAILURES:
        print(f"  FAILED: {failure}")
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
