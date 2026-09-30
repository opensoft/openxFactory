"""The PARENT SEAL — the bounded source artifact the credential-free child
consumes (openxFactory `add-nightly-dashboard-refresh`, re-realization S2).

What each block here pins.

  * THE VALIDATOR COMES FROM THE PRODUCT, NOT FROM THE CORPUS (#1158). The
    corpus these tests seal is shaped like openxFactory since the § 5.2 shed
    (`cc4ae9d3`): every baked path, and NO
    `scripts/validate-ideation-dashboard-contracts.py`. The seal used to ask
    `git archive` for that path, which refused every such corpus. Now it
    takes the openxdox product's own validator, through the snapshot lane's
    own resolver, composed with its schemas. It seals that unit under its own
    `validator/` root and RUNS the sealed copy once before it writes a
    manifest. A validator that cannot be resolved is a refusal that names
    where it was looked for. A unit that cannot be copied whole, or a copy
    that cannot run, is a refusal that names what was wrong. Most tests
    inject a stub unit, as they inject the recipe. It is a committed product
    tree whose HEAD the stand-in legs record, because the seal holds the
    validator to the render unit's openXdox leg and refuses a validator with
    no product revision. The tests that are about
    the validator use the REAL resolver over the real pinned legs. The
    DECISION set stays the baked set, and the real `find_validator`, run over
    a real sealed tree, is proven never to adopt the sealed copy
    (openXdox-code `e28930bf` confines the locator to the product's own
    tree).
  * THE RENDER UNIT RIDES IN THE SEAL (#1161). Since the shed the child's
    renderer is the two pinned products' `code` legs behind openxFactory's
    host bootstrap, so the seal carries both legs, archived at the commits the
    SEALED corpus pins them at, and refuses a parent whose products sit
    anywhere else. The leg tests build real products with real nested
    submodules; the rest inject a stand-in leg sealer, as they inject the
    recipe. Before it writes a manifest the parent renders the child's own
    snapshot FROM THE SEAL and runs the sealed validator over it under
    `--strict`; a rejection is `StrictGateRejected`, a verdict carrying the
    validator's findings. The mechanics are tested over a stand-in entry and
    validator, and one test seals THIS checkout, legs and all, and renders the
    real corpus from the seal. An audit-hook test repeats the measurement the
    render unit was declared from.
  * THE SERVE UNIT RIDES THERE TOO (#1164, seal 2.2.0). Since the post-shed
    recipe (Omnigent-Install `6b7da477`) the served image starts
    `scripts/ideation-dashboard-serve.py` from a runtime tree it copies out
    of the context the child assembles from the seal. So the seal carries
    that tree, the manifest names it (`serve_entry`, `serve_unit`), the
    intake requires each of its paths once, and the seal refuses first a
    corpus that lacks one. An audit-hook test measures the serve's build
    phase against the unit, and the recipe's own build step runs over the
    runtime tree copied out of a real seal of this checkout.
  * THE REVISION IS PROVEN, NOT ASSERTED. `git archive` records the commit it
    was made from in a global extended pax header; the seal refuses unless
    that header equals the `source_head` it is about to record. After this
    change the child's own one-revision check reads two fields of one manifest
    and is tautological alone, so the parent holds the end that still touches
    a repository.
  * THE DIGEST RULE TRAVELS WITH THE ARTIFACT. `tree_digest` is recomputed here
    from the rule `TREE_DIGEST_SPEC` states, by an INDEPENDENT implementation,
    so the manifest's stated rule is provably the implemented one — that is
    what makes the child's (S3) recomputation authorable from the manifest.
  * EVERY REFUSAL LEAVES NO MANIFEST. A seal the parent could not stand behind
    must not be downloadable, so the refusal paths assert the absence of
    `manifest.json` and not merely a raised exception.
  * NOTHING HERE BUILDS OR PUSHES. Every shell-out the seal makes through its
    own runner is `git`, which the tests assert over the recorded argv. The
    one other act is a single run of the SEALED validator copy, which has its
    own test. `gh` is unreachable by the suite's own hermeticity guard (the
    recipe read is injected).

No network: the corpus is a real `git init` under `tmp_path` (git is not a
guarded binary — `nlm`/`gh`/`omp` are), the recipe read is always injected, and
the validator unit, the legs and the pre-dispatch render are injected except
where a test says it uses the real one.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime
from pathlib import Path

import pytest

from conftest import REPO_ROOT
from ideation_dashboard import dashboard_refresh_lane as lane
from ideation_dashboard import nightly_lane
from openxdox import snapshot as snapshot_mod
from openxdox.generator import is_rfc3339_datetime

CORRELATION = "dashboard-refresh-4242-1"
COMMITTED_AT = "2026-09-04T01:02:03+00:00"


# ---------------------------------------------------------------------------
# EVERY SEALED RUN GOES THROUGH A STAND-IN DOCKER CLI HERE (#1191). The lane
# runs the probe, the pre-dispatch render and its --strict validation in a
# sealed container, by `/usr/bin/docker`. These tests hand it this stand-in
# instead: it takes the lane's `docker run` argv as the daemon would, maps
# each container path the lane names (/seal, /judged, /out, /tmp, and the
# image's /usr/local/bin/python3) to one on this host, and runs the command
# here with the environment the argv names and nothing else. So every test
# still drives the lane's own argv, its bounded reading and its check that no
# container is left, while the containment itself is held by the argv tests
# below and proven against a real daemon by
# tests/sealed-run-proof/sealed_run_containment_proof.py.
# ---------------------------------------------------------------------------

STAND_IN_IMAGE = "sha256:" + "5e" * 32
_SEALED_DOCKER_ENV = ("ACTIONS_ALLOW_UNSECURE_COMMANDS", "DOCKER_HOST",
                      "DOCKER_CONTEXT", "DOCKER_TLS", "DOCKER_TLS_VERIFY",
                      "DOCKER_CERT_PATH", "BUILDX_CONFIG", "BUILDX_BUILDER")
_STAND_IN_DOCKER = r"""#!PYTHON
import json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
config_file = HERE / "stand-in-docker.json"
config = json.loads(config_file.read_text()) if config_file.exists() else {}
with open(HERE / "stand-in-docker.log", "a", encoding="utf-8") as log:
    log.write(json.dumps({"argv": sys.argv[1:], "env": dict(os.environ)}) + "\n")
args = sys.argv[1:]
if args[0] == "ps":
    print("\n".join(config.get("running", [])))
    sys.exit(config.get("ps_exit", 0))
if args[0] == "rm":
    if config.get("rm_exit"):
        sys.exit(config["rm_exit"])
    config["running"] = [cid for cid in config.get("running", [])
                         if cid not in args[2:]]
    config_file.write_text(json.dumps(config))
    sys.exit(0)
assert args[0] == "run", args
BARE = {"--rm", "--init", "--read-only"}
i, mounts, env, workdir, tmpfs = 1, {}, {}, "/", []
while args[i].startswith("--"):
    flag = args[i]
    if flag in BARE:
        i += 1
        continue
    value, i = args[i + 1], i + 2
    if flag == "--mount":
        fields = dict(part.split("=", 1) for part in value.split(",") if "=" in part)
        mounts[fields["target"]] = fields["source"]
    elif flag == "--env":
        key, _, val = value.partition("=")
        env[key] = val
    elif flag == "--workdir":
        workdir = value
    elif flag == "--tmpfs":
        tmpfs.append(value.split(":", 1)[0])
command = args[i + 1:]
scratch = Path(tempfile.mkdtemp(prefix="stand-in-container-"))
for target in tmpfs:
    made = scratch / target.strip("/")
    made.mkdir(parents=True)
    mounts[target] = str(made)


def host(value):
    if value == "/usr/local/bin/python3":
        return sys.executable
    for target in sorted(mounts, key=len, reverse=True):
        if value == target or value.startswith(target + "/"):
            return mounts[target] + value[len(target):]
    return value


try:
    if config.get("hang"):
        time.sleep(3600)
    if "exit" in config:
        sys.stdout.write(config.get("stdout", ""))
        sys.stderr.write(config.get("stderr", ""))
        sys.stdout.flush()
        sys.exit(config["exit"])
    run_env = {"PATH": "/usr/local/bin:/usr/bin:/bin",
               **{key: host(val) for key, val in env.items()}}
    proc = subprocess.run([host(arg) for arg in command], cwd=host(workdir),
                          env=run_env)
    sys.exit(proc.returncode)
finally:
    shutil.rmtree(scratch, ignore_errors=True)
"""


@pytest.fixture(scope="session")
def _stand_in_docker_home(tmp_path_factory) -> Path:
    home = tmp_path_factory.mktemp("stand-in-docker")
    docker = home / "docker"
    docker.write_text(_STAND_IN_DOCKER.replace("#!PYTHON", f"#!{sys.executable}", 1),
                      encoding="utf-8")
    docker.chmod(0o755)
    return home


@pytest.fixture(autouse=True)
def stand_in_docker(_stand_in_docker_home, monkeypatch) -> Path:
    """The stand-in docker CLI, fresh for each test: no configuration, no
    log, `SEALED_IMAGE` set to an image id, and none of the variables the lane
    refuses."""
    for name in ("stand-in-docker.json", "stand-in-docker.log"):
        (_stand_in_docker_home / name).unlink(missing_ok=True)
    monkeypatch.setattr(lane, "DOCKER", str(_stand_in_docker_home / "docker"),
                        raising=False)
    monkeypatch.setenv("SEALED_IMAGE", STAND_IN_IMAGE)
    for name in (*_SEALED_DOCKER_ENV, "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT",
                 "RUNNER_TEMP"):
        monkeypatch.delenv(name, raising=False)
    return _stand_in_docker_home


def _docker_calls(home: Path) -> list[dict]:
    """Every call the stand-in docker CLI took this test, in order."""
    log = home / "stand-in-docker.log"
    if not log.exists():
        return []
    return [json.loads(line) for line in
            log.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed_runs(home: Path) -> list[list[str]]:
    """The argv, after `docker`, of every sealed run this test made."""
    return [call["argv"] for call in _docker_calls(home)
            if call["argv"][:1] == ["run"]]


def _stand_in_docker_config(home: Path, **config) -> None:
    (home / "stand-in-docker.json").write_text(json.dumps(config),
                                               encoding="utf-8")


def _instant(value: str) -> datetime:
    """The INSTANT a stamp denotes, not its spelling.

    `git show -s --format=%cI` renders a ZERO offset as `+00:00` on some git
    versions and as `Z` on others (measured: `+00:00` on git 2.43 locally,
    `Z` on the Actions runner), and the manifest records whatever git said
    VERBATIM — deliberately, because `--generated-at` is "recorded in the
    snapshot EXACTLY as given … never normalised". Both spellings are RFC 3339
    and both are accepted by `generator.is_rfc3339_datetime`, which is the
    property that matters; pinning one spelling would pin a git version."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
RECIPE_REV = "c" * 40
RECIPE_TEXT = "FROM python:3.12-slim\nCOPY openxFactory/docs /srv/source/docs\n"

# THE SERVE UNIT (#1164, seal 2.2.0): the runtime tree the served image's
# recipe copies, at Omnigent-Install `6b7da477`
# (`containers/ideation-dashboard/Dockerfile` lines 82-108), corpus-relative,
# a trailing `/` naming a tree as the recipe spells one. Spelled here as the
# tests' expectation; the lane's `SERVE_UNIT` is held to it.
SERVE_ENTRY = "scripts/ideation-dashboard-serve.py"
SERVE_UNIT = (
    "contracts/domain-profiles/openxfactory-engineering.yaml",
    "docs/opendox-carve-manifest.yaml",
    "openDox/code/src/",
    "openXdox/code/src/",
    "scripts/carved_reach.py",
    "scripts/doc_health/",
    SERVE_ENTRY,
    "scripts/ideation_dashboard/",
    "scripts/opendox_host.py",
    "scripts/profile_openxfactory.py",
    "scripts/wire_messages.py",
)
# What the intake requires AS serve-unit paths: the unit less its entry,
# which `serve_entry` names, and less what the render unit's own checks
# already require (the host bootstrap, and both legs' `src/`), so no missing
# path is reported twice.
SERVE_ONLY = ("contracts/domain-profiles/openxfactory-engineering.yaml",
              "docs/opendox-carve-manifest.yaml", "scripts/doc_health/",
              "scripts/ideation_dashboard/")


# ---------------------------------------------------------------------------
# helpers — a real, tiny corpus repository, and a stub recipe read
# ---------------------------------------------------------------------------

def _git(repo: Path, *argv: str) -> str:
    """Real git, in a real temp repository — hermetic (no remote is ever named)
    and NEVER a skip: the suite pins its skip count exactly, so a git that
    would not run has to fail loudly here rather than turn this file into
    twenty silent skips that red the gate with the wrong reason.

    The committer date is FIXED so the `source_committed_at` assertions can
    name the value the child will pass to `--generated-at`, and the config
    files are neutralised so the developer's own git config cannot change it.
    """
    env = dict(os.environ, **{
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_AUTHOR_DATE": COMMITTED_AT, "GIT_COMMITTER_DATE": COMMITTED_AT})
    proc = subprocess.run(["git", "-C", str(repo), *argv],
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 0, \
        f"git {' '.join(argv)} failed: {proc.stderr.strip()[:400]}"
    return proc.stdout.strip()


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    """A corpus checkout shaped like openxFactory since the § 5.2 shed
    (`cc4ae9d3`): every BAKED path, one file deep (a baked FILE path is the
    file itself), and NOT the top-level
    `scripts/validate-ideation-dashboard-contracts.py` the shed moved to
    openXdox-code. Built from `CORPUS_BAKED_PATHS`, never from the seal set, so
    the fixture cannot quietly re-grow the file the seal must stop asking for.
    It also carries each FILE of the serve unit (#1164) that no baked path
    makes: the served image's recipe copies two files out of `contracts/` and
    `docs/` by name.

    The two products are GITLINKS, and this fixture carries neither: the tests
    about the legs build `corpus_with_products`, and the rest inject a
    stand-in leg sealer, as they inject the recipe."""
    repo = tmp_path / "openxFactory-src"
    repo.mkdir()
    _git(repo, "init", "--quiet", "-b", "main")
    for relpath in lane.CORPUS_BAKED_PATHS:
        if relpath in lane.RENDER_LEG_GITLINKS:
            continue
        target = repo / relpath
        if relpath.endswith(".py"):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {relpath}\n", encoding="utf-8")
            continue
        target.mkdir(parents=True, exist_ok=True)
        (target / "a.md").write_text(f"# {relpath}\n", encoding="utf-8")
    for relpath in SERVE_UNIT:
        target = repo / relpath
        if (relpath.endswith("/") or target.exists()
                or relpath.split("/", 1)[0] in lane.RENDER_LEG_GITLINKS):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# {relpath}\n", encoding="utf-8")
    # A path OUTSIDE the seal set, to prove the seal is bounded.
    (repo / "experiments").mkdir()
    (repo / "experiments" / "huge.bin").write_text("x" * 1024, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "corpus")
    return repo


def _decision(corpus_revision: str, **kw) -> dict:
    payload = {"build": True, "outcome": "build",
               "reason": lane.REASON_CORPUS_MOVED,
               "corpus_revision": corpus_revision,
               "recipe_revision": RECIPE_REV}
    payload.update(kw)
    return payload


STUB_SCHEMA = lane.VALIDATOR_SNAPSHOT_SCHEMA
STUB_SCRIPT = "#!/usr/bin/env python3\nprint('ok')\n"


def _stub_validator(where: Path, *, script: str = STUB_SCRIPT
                    ) -> "lane.PinnedValidator":
    """A composed-unit STAND-IN: `scripts/` beside `contracts/schemas/`, the
    shape `nightly_lane._pinned_validator()` answers. The default script
    prints `ok` and exits 0, whatever it is handed, so it is always
    "available" and never a verdict on anything. Tests about the seal's own
    mechanics inject this, as they inject the recipe. Tests about the
    VALIDATOR use the real one.

    It is a COMMITTED PRODUCT TREE, and it is the unit's `product_root`, as
    every unit the real resolver answers has one. Every 2.1 seal carries the
    openXdox code leg, so the seal records the product revision its validator
    came from and refuses a unit that has none (Copilot, PR #1166). A test
    that needs another script hands it in here, so what it seals is committed
    bytes."""
    runnable = where / lane.VALIDATOR_SCRIPT_PATH
    runnable.parent.mkdir(parents=True, exist_ok=True)
    runnable.write_text(script, encoding="utf-8")
    schemas = where / lane.VALIDATOR_SCHEMAS_PATH
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / STUB_SCHEMA).write_text("{}\n", encoding="utf-8")
    if not (where / ".git").exists():
        _git(where, "init", "--quiet", "-b", "main")
    if _git(where, "status", "--porcelain"):
        _git(where, "add", "-A")
        _git(where, "commit", "--quiet", "-m", "a stand-in validator unit")
    return lane.PinnedValidator(runnable=runnable, product_root=where)


def _validator_head(pinned) -> str:
    """The revision a real seal records for `pinned`: the HEAD of the product
    tree it was resolved from. A unit with no tree of its own records none,
    and the seal refuses it before this stand-in value is compared with
    anything."""
    root = getattr(pinned, "product_root", None)
    if root is None or not (Path(root) / ".git").exists():
        return "e" * 40
    return _git(Path(root), "rev-parse", "HEAD")


_STUB = object()   # `_seal`'s default: inject the stand-in


def _product_head() -> str:
    """The HEAD of the real openXdox code leg this suite runs against. A real
    seal records it as that leg's revision whenever the validator it carries
    came from the real product, so the stand-in leg sealer records it too: a
    test that pairs the stand-in legs with the REAL resolver then seals one
    product revision, as a real parent does, rather than two."""
    root = snapshot_mod.product_root()
    return _git(root, "rev-parse", "HEAD") if root is not None else "e" * 40


# The product module the parent classifies the sealed validator's runs with.
# The stand-in legs carry the REAL one, since the parent imports it out of the
# seal (Copilot, PR #1166).
PRODUCT_MODULE_TEXT = Path(snapshot_mod.__file__).read_text(encoding="utf-8")


# The product modules the render unit's corpus side imports by name, per code
# leg, under `src/<package>/`: the entry's `opendox.cli`, the host bootstrap's
# imports, and the module the sealed validator's runs are classified with.
# Spelled here as the tests' expectation. The lane's `RENDER_LEG_MODULES`, and
# an `ast` read of the entry and its bootstrap, are both held to it.
RENDER_UNIT_IMPORTS = {
    # The four seam modules joined with plan 034 T046/T047: the host
    # bootstrap's `opendox_host.seams()` imports them.
    ("openDox", "code"): ("cli.py", "corpus_adapter.py", "domain_profile.py",
                          "doxbench_packet.py", "serve_wire.py",
                          "workbench.py"),
    ("openXdox", "code"): ("cli_gate.py", "domain_profile.py", "serve_gate.py",
                           "serve_projection.py", "snapshot.py",
                           "view_extensions.py"),
}
# The product modules the SERVE entry imports by name beyond those
# (#1164, seal 2.2.0): `opendox.serve`, which the image starts. The lane's
# `SERVE_LEG_MODULES`, and an `ast` read of the serve entry and its host
# bootstrap less the render unit's, are both held to it.
SERVE_UNIT_IMPORTS = {("openDox", "code"): ("serve.py",)}


def _named_leg_modules(gitlink: str, leg: str) -> tuple[str, ...]:
    """Every product module the render unit or the serve entry imports by
    name from one code leg."""
    return (*RENDER_UNIT_IMPORTS[(gitlink, leg)],
            *SERVE_UNIT_IMPORTS.get((gitlink, leg), ()))


def _recording_product_module(record: Path) -> str:
    """The real product module, whose `validate_snapshot` also appends the
    file it was loaded from to `record` on every call."""
    return PRODUCT_MODULE_TEXT + (
        f"\n\nRECORD = {str(record)!r}\n"
        "_products_own_validate_snapshot = validate_snapshot\n\n\n"
        "def validate_snapshot(*args, **kwargs):\n"
        "    with open(RECORD, 'a', encoding='utf-8') as handle:\n"
        "        handle.write(__file__ + '\\n')\n"
        "    return _products_own_validate_snapshot(*args, **kwargs)\n")


def _lying_product_module(**fields) -> str:
    """The real product module, whose `validate_snapshot` puts `fields` over the
    product's own result before it returns it: sealed code can print any
    verdict it likes, however it pairs."""
    return PRODUCT_MODULE_TEXT + (
        f"\n\nLIE = {fields!r}\n"
        "_products_own_validate_snapshot = validate_snapshot\n\n\n"
        "def validate_snapshot(*args, **kwargs):\n"
        "    result = _products_own_validate_snapshot(*args, **kwargs)\n"
        "    for name, value in LIE.items():\n"
        "        setattr(result, name, value)\n"
        "    return result\n")


def _stub_legs(*, corpus_checkout, source_head, corpus_root, runner):
    """A leg-sealer STAND-IN: one module per product under the path the real
    sealer extracts to, the real product module in the validator leg, and
    records shaped exactly like its own. This one stands in beside the REAL
    resolver, so its openXdox code leg records the real product's HEAD: a
    real parent's validator and legs are one checkout. Tests about the seal's
    other mechanics inject it, as they inject the recipe, and `_seal` injects
    one that records whichever validator it resolved. The tests about the
    legs run `seal_render_legs` over real nested submodules."""
    return _stub_leg_records(corpus_root, PRODUCT_MODULE_TEXT, _product_head())


def _stub_leg_records(corpus_root, product_module: str | None,
                      validator_revision: str) -> list[dict]:
    """The stand-in legs' tree and records. The openXdox code leg carries
    `product_module` as the product module the parent classifies with (None:
    none at all), and records `validator_revision` as its commit."""
    records = []
    for index, (gitlink, leg, package) in enumerate(lane.RENDER_LEGS):
        modules = Path(corpus_root) / gitlink / leg / "src" / package
        modules.mkdir(parents=True)
        (modules / "__init__.py").write_text(f"# stand-in {package}\n",
                                             encoding="utf-8")
        count = 1
        for module in _named_leg_modules(gitlink, leg):
            if module == lane.SEALED_PRODUCT_MODULE:
                if product_module is None:
                    continue
                text = product_module
            else:
                text = f"# stand-in {package}.{module[:-3]}\n"
            (modules / module).write_text(text, encoding="utf-8")
            count += 1
        records.append({
            "gitlink": gitlink, "gitlink_revision": str(index + 1) * 40,
            "leg": leg,
            "leg_revision": (validator_revision
                             if (gitlink, leg) == lane.VALIDATOR_LEG
                             else str(index + 5) * 40),
            "package": package,
            "relpath": f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/{leg}",
            "paths": list(lane.RENDER_LEG_PATHS), "file_count": count,
            "schema_leg": lane.SCHEMA_LEG,
            "schema_leg_revision": str(index + 7) * 40})
    return records


STUB_PRECHECK = {"entry": lane.RENDER_ENTRY, "documents": 0, "strict": True,
                 "outcome": lane.PRECHECK_VALIDATED, "returncode": 0}
# Each verdict beside the exit code it is read from, as the intake's refusals
# name them.
VERDICT_PAIRS = "validated with exit 0, or not-conformant with exit 1"
_ABSENT = object()   # a record field left out


def _stub_precheck(seal_root, *, source_head, source_committed_at,
                   container=None):
    """A pre-dispatch-render STAND-IN that passes. The render's own mechanics
    are tested over a stand-in entry, and the real render over this checkout."""
    return dict(STUB_PRECHECK)


def _seal(corpus: Path, seal_dir: Path, *, decision: dict | None = None,
          recipe: str | None = RECIPE_TEXT, resolve_validator=_STUB,
          seal_legs=_STUB, precheck_render=_STUB,
          product_module: str | None = PRODUCT_MODULE_TEXT, read_recipe=None,
          **kw) -> dict:
    """`seal_source` over the fixture corpus. `None` for `resolve_validator`,
    `seal_legs` or `precheck_render` means the REAL one (the snapshot lane's
    own resolver, `seal_render_legs`, `precheck_sealed_render`); the default
    injects the stand-in.

    The stand-in legs share one checkout with the validator, as a real
    parent's do. Their openXdox code leg records the HEAD of the product tree
    `seal_source` resolved its validator from, which it resolves before it
    seals the legs, and carries `product_module`, None for no product module
    at all. `read_recipe`, when given, reads the recipe instead of the
    stand-in that answers `recipe`."""
    head = _git(corpus, "rev-parse", "HEAD")
    if resolve_validator is _STUB:
        stub = _stub_validator(Path(seal_dir).parent / "stub-validator")
        resolve_validator = (lambda: stub)
    resolved: list = []

    def resolving():
        pinned = (resolve_validator or lane.resolve_pinned_validator)()
        resolved.append(pinned)
        return pinned

    def stand_in_legs(*, corpus_checkout, source_head, corpus_root, runner):
        return _stub_leg_records(corpus_root, product_module,
                                 _validator_head(resolved[-1]))

    return lane.seal_source(
        corpus_checkout=corpus, seal_dir=seal_dir,
        correlation_id=kw.pop("correlation_id", CORRELATION),
        decision=decision if decision is not None else _decision(head),
        corpus_ref=kw.pop("corpus_ref", "HEAD"),
        read_recipe=read_recipe or (lambda: recipe),
        resolve_validator=resolving,
        seal_legs=stand_in_legs if seal_legs is _STUB else seal_legs,
        precheck_render=(_stub_precheck if precheck_render is _STUB
                         else precheck_render),
        **kw)


class RecordingRunner:
    """Wraps the real runner and records every argv, and the environment each
    call was given, so "the seal speaks git and nothing else" is asserted on
    the calls rather than on the source."""

    def __init__(self, inner=lane.subprocess_runner) -> None:
        self.inner = inner
        self.calls: list[tuple[str, ...]] = []
        self.environments: list[dict | None] = []

    def __call__(self, argv, **kw):
        self.calls.append(tuple(str(a) for a in argv))
        self.environments.append(kw.get("env"))
        return self.inner(argv, **kw)


def _verb(argv) -> str:
    """The git subcommand of a recorded call: the first word after `git` that
    is neither a global option nor the directory `-C` takes."""
    words = list(argv[1:])
    while words:
        word = words.pop(0)
        if word == "-C":
            words.pop(0)
        elif not word.startswith("-"):
            return word
    return ""


def _assert_exact_reads(runner: "RecordingRunner") -> None:
    """Every git call was an EXACT-CONTENT read: replacement-free, and in the
    scrubbed environment, so no ambient redirection reached it."""
    for argv, env in zip(runner.calls, runner.environments):
        assert argv[:2] == ("git", "--no-replace-objects"), argv
        assert env is not None, argv
        assert env.get("GIT_NO_REPLACE_OBJECTS") == "1", argv
        for name in ("GIT_DIR", "GIT_OBJECT_DIRECTORY",
                     "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE",
                     "GIT_CONFIG_PARAMETERS", "GIT_WORK_TREE", "GIT_COMMON_DIR"):
            assert name not in env, (name, argv)


# ---------------------------------------------------------------------------
# the seal set, and the validator the product supplies since the shed (#1158)
# ---------------------------------------------------------------------------

def test_the_corpus_seal_set_is_the_baked_set_and_never_names_the_shed_path():
    """The corpus half of the seal is EXACTLY the baked set, less the two
    product gitlinks, whose legs are sealed on their own (#1161): `git
    archive` of a gitlink writes an empty directory, never the product. The
    one path that used to widen the set,
    `scripts/validate-ideation-dashboard-contracts.py`, left openxFactory at
    the § 5.2 shed (`cc4ae9d3`), and asking `git archive` for it refused every
    real corpus: `fatal: pathspec ... did not match any files`, measured at
    `1edbb3dd` (#1158)."""
    assert lane.CORPUS_SEAL_PATHS == tuple(
        path for path in lane.CORPUS_BAKED_PATHS
        if path not in lane.RENDER_LEG_GITLINKS)
    assert set(lane.CORPUS_BAKED_PATHS) - set(lane.CORPUS_SEAL_PATHS) == \
        set(lane.RENDER_LEG_GITLINKS)
    assert lane.RENDER_ENTRY in lane.CORPUS_SEAL_PATHS
    assert lane.VALIDATOR_SCRIPT_PATH not in lane.CORPUS_SEAL_PATHS
    # Sorted, like the baked tuple, because both are written into records that
    # compare scope for equality and two spellings would read as a change.
    assert list(lane.CORPUS_SEAL_PATHS) == sorted(lane.CORPUS_SEAL_PATHS)


def test_the_serve_unit_is_the_recipes_runtime_tree():
    """THE SERVE UNIT (#1164, seal 2.2.0). The recipe landed at
    Omnigent-Install `6b7da477` copies eleven paths out of the corpus to
    START the image: the serve's entry, the four host files it reaches, the
    two retained script packages, the carve manifest, the domain profile, and
    both legs' `src/`. The seal carries them and the manifest names them. The
    intake requires each ONCE: the entry by `serve_entry`, the host bootstrap
    and the legs by the render unit's own checks, which already name them,
    and the other four as serve-unit paths (`SERVE_ONLY`). Each is in this
    checkout."""
    assert lane.SEAL_SCHEMA_VERSION == "2.2.0"
    assert lane.SERVE_ENTRY == SERVE_ENTRY
    assert lane.SERVE_UNIT == SERVE_UNIT
    assert list(lane.SERVE_UNIT) == sorted(lane.SERVE_UNIT)
    assert lane.SERVE_ENTRY in lane.CORPUS_SEAL_PATHS
    assert lane.SERVE_ONLY == SERVE_ONLY
    held = [*lane.RENDER_BOOTSTRAP,
            *(f"{gitlink}/{leg}/{path}/" for gitlink, leg, _package
              in lane.RENDER_LEGS for path in lane.RENDER_LEG_PATHS)]
    # A partition: each path of the unit is required by exactly one check.
    assert sorted([SERVE_ENTRY, *SERVE_ONLY, *held]) == sorted(SERVE_UNIT)
    for path in SERVE_UNIT:
        target = REPO_ROOT / path
        assert (any(item.is_file() for item in target.rglob("*"))
                if path.endswith("/") else target.is_file()), path


def test_the_sealed_validator_path_is_the_products_own():
    """The unit-relative script path is spelled in the module, which has to
    import without the carve legs on disk. So it is held EQUAL to the product's
    own `snapshot.VALIDATOR_RELPATH` here rather than trusted to agree, and the
    unit's root is proven to be neither of the seal's other two roots."""
    assert lane.VALIDATOR_SCRIPT_PATH == snapshot_mod.VALIDATOR_RELPATH.as_posix()
    assert lane.SEAL_VALIDATOR_RELPATH == (
        f"{lane.SEAL_VALIDATOR_ROOT}/{lane.VALIDATOR_SCRIPT_PATH}")
    assert lane.SEAL_VALIDATOR_ROOT not in (
        lane.SEAL_CORPUS_RELPATH, lane.SEAL_RECIPE_RELPATH.split("/", 1)[0])
    # The run outcomes the intake accepts are the product's own two verdicts,
    # each beside the exit code the product reads it from.
    assert lane.VALIDATOR_VERDICT_OUTCOMES == (snapshot_mod.VALIDATED,
                                               snapshot_mod.NOT_CONFORMANT)
    assert lane.VALIDATOR_VERDICT_RETURNCODES == {
        snapshot_mod.VALIDATED: 0,
        snapshot_mod.NOT_CONFORMANT: snapshot_mod.FINDINGS_EXIT}


def test_the_decision_scope_does_not_follow_the_validator():
    """Adding the validator's path to `CORPUS_BAKED_PATHS` would make
    `_same_scope` fire `REASON_SCOPE_CHANGED` against every recorded pin and
    force exactly one rebuild for nothing (design open question 7). So the
    decision scope is pinned to the baked set here, and the cost of widening it
    is measured."""
    assert lane.VALIDATOR_SCRIPT_PATH not in lane.CORPUS_BAKED_PATHS
    # The scope itself is pinned beside the Dockerfile's copied set in
    # `test_dashboard_refresh_lane.py`.
    recorded = lane.Provenance(
        corpus_repo=lane.DEFAULT_CORPUS_REPO, corpus_revision="a" * 40,
        corpus_scope=lane.CORPUS_BAKED_PATHS,
        recipe_repo=lane.DEFAULT_RECIPE_REPO, recipe_revision="b" * 40,
        recipe_scope=lane.RECIPE_BAKED_PATHS)
    unchanged = lane.decide_refresh(corpus_revision="a" * 40,
                                   recipe_revision="b" * 40, recorded=recorded)
    assert unchanged.reason == lane.REASON_UNCHANGED
    widened_scope = tuple(sorted({*lane.CORPUS_BAKED_PATHS,
                                  lane.VALIDATOR_SCRIPT_PATH}))
    widened = lane.decide_refresh(corpus_revision="a" * 40,
                                  recipe_revision="b" * 40, recorded=recorded,
                                  corpus_scope=widened_scope)
    assert widened.reason == lane.REASON_SCOPE_CHANGED    # the cost, measured


def test_a_post_shed_corpus_seals_with_the_products_own_validator(corpus, tmp_path):
    """#1158, THE DEFECT ITSELF. The corpus is shaped like openxFactory since
    the § 5.2 shed: every baked path, and NO
    `scripts/validate-ideation-dashboard-contracts.py`. The code this replaces
    asked `git archive` for that shed path and refused every such corpus, so no
    real corpus could be sealed. Now it seals. The validator the seal carries
    is the openxdox product's OWN, resolved by the snapshot lane's own resolver
    and composed with the schemas the snapshot lane validates with. It has RUN,
    from the seal, and reached a verdict.

    NO resolver is injected: this is the real resolver over the real pinned
    legs, which is the point. A stub here could not show that the seal carries
    the right validator pointed at the right schemas."""
    shed = Path("scripts") / "validate-ideation-dashboard-contracts.py"
    assert not (corpus / shed).exists()
    seal = tmp_path / "seal"
    head = _git(corpus, "rev-parse", "HEAD")
    manifest = lane.seal_source(
        corpus_checkout=corpus, seal_dir=seal, correlation_id=CORRELATION,
        decision=_decision(head), corpus_ref="HEAD",
        read_recipe=(lambda: RECIPE_TEXT), seal_legs=_stub_legs,
        precheck_render=_stub_precheck)

    own = snapshot_mod.find_validator()
    assert own is not None
    sealed = seal / lane.SEAL_VALIDATOR_RELPATH
    assert sealed.read_bytes() == own.read_bytes()        # the product's bytes
    assert not (seal / lane.SEAL_CORPUS_RELPATH / shed).exists()
    # The schemas the snapshot lane validates with travel with it, byte for
    # byte, as regular files: the seal holds the pinned bytes, never a link.
    farm = nightly_lane._pinned_validator().parents[1] / lane.VALIDATOR_SCHEMAS_PATH
    carried = seal / lane.SEAL_VALIDATOR_ROOT / lane.VALIDATOR_SCHEMAS_PATH
    assert sorted(p.name for p in carried.iterdir()) == \
        sorted(p.name for p in farm.iterdir())
    for linked in farm.iterdir():
        copy = carried / linked.name
        assert not copy.is_symlink()
        assert copy.read_bytes() == linked.read_bytes(), linked.name
    assert (carried / "ideation-dashboard-snapshot.schema.yaml").is_file()
    assert manifest["validator_schema_count"] == len(list(farm.iterdir()))
    # It RAN, from the seal, and reached a verdict.
    assert manifest["validator_relpath"] == lane.SEAL_VALIDATOR_RELPATH
    assert manifest["validator_probe"]["kind"] == lane.VALIDATOR_PROBE["kind"]
    assert manifest["validator_probe"]["returncode"] in (0, 1)
    assert manifest["validator_probe"]["outcome"] != \
        snapshot_mod.VALIDATOR_UNAVAILABLE
    # And the seal records WHICH product revision the copy came from.
    assert manifest["validator_revision"] == \
        _git(snapshot_mod.product_root(), "rev-parse", "HEAD")
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


@pytest.mark.parametrize("product_tree", ["without-its-validator",
                                          "not-a-source-checkout"])
def test_a_genuinely_missing_validator_still_refuses_naming_where_it_looked(
        corpus, tmp_path, monkeypatch, product_tree):
    """FAIL-CLOSED STAYS. The seal refuses, and writes nothing, when the pinned
    product has no validator to give it. The refusal names the ONE place the
    default is looked for, the product's own tree, in the snapshot lane's own
    words (`nightly_lane._pinned_validator_missing`). It never names the
    corpus, which is no longer searched.

    The product's own locator is REAL here. Only the tree it is confined to is
    swapped for one that genuinely carries no validator, or for no source tree
    at all, the installed-wheel case. It is found out BEFORE the corpus is
    archived, so the seal directory is never even created."""
    root = None
    if product_tree == "without-its-validator":
        root = tmp_path / "openxdox-without-its-validator"
        root.mkdir()
    monkeypatch.setattr(nightly_lane.snapshot_mod, "product_root", lambda: root)
    head = _git(corpus, "rev-parse", "HEAD")
    with pytest.raises(lane.SealRefused) as refused:
        lane.seal_source(
            corpus_checkout=corpus, seal_dir=tmp_path / "seal",
            correlation_id=CORRELATION, decision=_decision(head),
            corpus_ref="HEAD", read_recipe=(lambda: RECIPE_TEXT))
    reason = str(refused.value)
    assert reason.startswith("the pinned openxdox validator was not found (")
    assert f"({nightly_lane._pinned_validator_missing()})" in reason
    if root is not None:
        assert str(root / "scripts" / "validate-ideation-dashboard-contracts.py") \
            in reason
    else:
        assert "not running from a source checkout" in reason
    assert "validator would be unreachable" in reason
    assert str(corpus) not in reason
    assert not (tmp_path / "seal").exists()


def test_unmaterialized_carve_legs_refuse_naming_the_legs(corpus, tmp_path,
                                                          monkeypatch):
    """A parent that has not materialized openxFactory's openXdox and openDox
    gitlinks (the nightly's finalize job, until #1161 mounted them) cannot
    resolve the validator, which is read through them. `carved_reach` refuses
    that read BY NAME, and the seal carries the refusal instead of a
    traceback: it is a SealRefused that names the gitlinks and the command,
    and nothing is sealed."""
    import carved_reach

    def unmaterialized():
        raise carved_reach.CarveReachUnavailable(
            "openxdox is read from a pinned carve leg, and no leg in this "
            "checkout carries it: the `openDox` and/or `openXdox` gitlinks are "
            f"not materialized. Run `{carved_reach.INIT_COMMAND}`")

    monkeypatch.setattr(nightly_lane, "_pinned_validator", unmaterialized)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=None)
    reason = str(refused.value)
    assert reason.startswith(
        "the pinned openxdox validator cannot be resolved on this parent "
        "(CarveReachUnavailable: ")
    assert "gitlinks are not materialized" in reason
    assert carved_reach.INIT_COMMAND in reason
    assert not (tmp_path / "seal").exists()


def _unit_without(where: Path, *, drop: str | None, keep_schemas: bool) -> Path:
    """The product's OWN script in a unit that lacks what it needs: no schemas
    at all (the code leg's copy exactly as it ships), or every composed schema
    but one."""
    script = where / lane.VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True)
    shutil.copyfile(snapshot_mod.find_validator(), script)
    if keep_schemas:
        farm = nightly_lane._pinned_validator().parents[1]
        target = where / lane.VALIDATOR_SCHEMAS_PATH
        target.mkdir(parents=True)
        for entry in (farm / lane.VALIDATOR_SCHEMAS_PATH).iterdir():
            if entry.name != drop:
                shutil.copyfile(entry, target / entry.name)
    return script


@pytest.mark.parametrize("drop, keep_schemas, said", [
    (None, False, "carries none of the family's"),
    (lane.VALIDATOR_SNAPSHOT_SCHEMA, True,
     f"{lane.VALIDATOR_SNAPSHOT_SCHEMA} is not carried under"),
], ids=["the-code-legs-own-copy-with-no-schemas", "every-schema-but-the-snapshots"])
def test_a_sealed_validator_that_cannot_run_is_refused(corpus, tmp_path, drop,
                                                       keep_schemas, said):
    """FOUND IS NOT RUNNABLE (#1157), so the seal RUNS what it carries, and a
    copy that cannot reach a verdict is refused in the validator's own words.
    Both units carry the product's real script. The first is the code leg's
    copy exactly as it ships, uncomposed: from the seal it finds no schemas at
    all. The second lacks only the snapshot schema, the one the child
    validates against. Either way the refusal says why and leaves no manifest
    behind."""
    script = _unit_without(tmp_path / "unit", drop=drop,
                           keep_schemas=keep_schemas)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal",
              resolve_validator=lambda: lane.PinnedValidator(runnable=script))
    reason = str(refused.value)
    assert reason.startswith("the sealed validator could NOT RUN")
    assert said in reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def _committed_unit(where: Path) -> tuple["lane.PinnedValidator", Path, Path]:
    """A composed unit built the way the product's composer builds one, from
    two committed repositories: the script COPIED from a product tree, and the
    snapshot schema LINKED into a spec tree."""
    product, spec = where / "product", where / "spec"
    for repo in (product, spec):
        repo.mkdir(parents=True)
        _git(repo, "init", "--quiet", "-b", "main")
    script = product / lane.VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True)
    script.write_text("print('ok')\n", encoding="utf-8")
    schema = spec / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA
    schema.parent.mkdir(parents=True)
    schema.write_text("{}\n", encoding="utf-8")
    for repo in (product, spec):
        _git(repo, "add", "-A")
        _git(repo, "commit", "--quiet", "-m", "committed")
    farm = where / "farm"
    runnable = farm / lane.VALIDATOR_SCRIPT_PATH
    runnable.parent.mkdir(parents=True)
    shutil.copyfile(script, runnable)
    (farm / lane.VALIDATOR_SCHEMAS_PATH).mkdir(parents=True)
    (farm / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA).symlink_to(schema)
    return (lane.PinnedValidator(runnable=runnable, product_root=product),
            product, spec)


@pytest.mark.parametrize("change, said", [
    ("the-script-edited", f"product/{lane.VALIDATOR_SCRIPT_PATH} (M)"),
    ("the-copy-differs", f"{lane.VALIDATOR_SCRIPT_PATH} (the unit's copy is "
                         "not the file at"),
    ("a-schema-edited",
     f"spec/{lane.VALIDATOR_SCHEMAS_PATH}/{STUB_SCHEMA} (M)"),
    ("a-schema-untracked",
     f"spec/{lane.VALIDATOR_SCHEMAS_PATH}/extra.schema.yaml (??)"),
], ids=["the-script-edited", "the-copy-differs", "a-schema-edited",
        "a-schema-untracked"])
def test_a_unit_composed_from_uncommitted_bytes_is_refused(corpus, tmp_path,
                                                           change, said):
    """The unit is composed from worktrees, and a HEAD says nothing about
    uncommitted bytes. So a validator unit whose script or schemas are not
    what their repositories' HEADs hold is refused, before it is copied or
    run (Copilot, PR #1166)."""
    pinned, product, spec = _committed_unit(tmp_path / "unit")
    schemas = Path(pinned.runnable).parents[1] / lane.VALIDATOR_SCHEMAS_PATH
    if change == "the-script-edited":
        (product / lane.VALIDATOR_SCRIPT_PATH).write_text(
            "print('edited')\n", encoding="utf-8")
        shutil.copyfile(product / lane.VALIDATOR_SCRIPT_PATH, pinned.runnable)
    elif change == "the-copy-differs":
        Path(pinned.runnable).write_text("print('other')\n", encoding="utf-8")
    elif change == "a-schema-edited":
        (spec / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA).write_text(
            "{'edited': 1}\n", encoding="utf-8")
    else:
        extra = spec / lane.VALIDATOR_SCHEMAS_PATH / "extra.schema.yaml"
        extra.write_text("{}\n", encoding="utf-8")
        (schemas / "extra.schema.yaml").symlink_to(extra)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=lambda: pinned)
    reason = str(refused.value)
    assert reason.startswith(
        "the validator unit is composed from uncommitted bytes: "), reason
    assert said in reason, reason
    assert "no commit describes" in reason
    assert not (tmp_path / "seal" / lane.SEAL_VALIDATOR_ROOT).exists()


@pytest.mark.parametrize("sealed", ["the-checkout-head", "another-revision",
                                    "a-revision-without-it"])
def test_a_unit_schema_from_the_corpus_must_be_the_sealed_revisions(
        corpus, tmp_path, sealed):
    """THE UNIT IS BOUND TO THE SEALED REVISION (Copilot, PR #1166). The
    composer fills in, from the corpus checkout's own `contracts/schemas/`,
    each schema the carve legs do not supply, and a real parent's checkout
    sits at the aggregation's pin while the seal is of `source_head`. So a
    schema the unit takes from the corpus checkout must be the bytes
    `source_head` holds at its path: committed at the checkout's HEAD is not
    enough. Here the checkout's HEAD carries a newer schema than the sealed
    revision, or the sealed revision carries none."""
    first = _git(corpus, "rev-parse", "HEAD")
    schema = corpus / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA
    schema.parent.mkdir(parents=True)
    schema.write_text("revision: older\n", encoding="utf-8")
    _git(corpus, "add", "-A")
    _git(corpus, "commit", "--quiet", "-m", "an older schema")
    older = _git(corpus, "rev-parse", "HEAD")
    schema.write_text("revision: newer\n", encoding="utf-8")
    _git(corpus, "commit", "--quiet", "-am", "a newer schema")
    product = tmp_path / "product"
    product.mkdir()
    _git(product, "init", "--quiet", "-b", "main")
    script = product / lane.VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True)
    script.write_text(STUB_SCRIPT, encoding="utf-8")
    _git(product, "add", "-A")
    _git(product, "commit", "--quiet", "-m", "product")
    farm = tmp_path / "farm"
    runnable = farm / lane.VALIDATOR_SCRIPT_PATH
    runnable.parent.mkdir(parents=True)
    shutil.copyfile(script, runnable)
    (farm / lane.VALIDATOR_SCHEMAS_PATH).mkdir(parents=True)
    (farm / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA).symlink_to(schema)
    unit = lane.PinnedValidator(runnable=runnable, product_root=product)
    ref = {"the-checkout-head": "HEAD", "another-revision": older,
           "a-revision-without-it": first}[sealed]
    seal = tmp_path / "seal"
    if sealed == "the-checkout-head":
        manifest = _seal(corpus, seal, resolve_validator=lambda: unit,
                         corpus_ref=ref)
        assert (seal / lane.SEAL_VALIDATOR_ROOT / lane.VALIDATOR_SCHEMAS_PATH
                / STUB_SCHEMA).read_text(encoding="utf-8") == "revision: newer\n"
        # Recorded beside its corpus path, so the child can hold the two to
        # one file's bytes (seal 2.2.0).
        assert manifest["validator_corpus_schemas"] == {
            STUB_SCHEMA: f"{lane.VALIDATOR_SCHEMAS_PATH}/{STUB_SCHEMA}"}
        assert lane.verify_seal(seal) == []
        assert manifest["source_head"] == _git(corpus, "rev-parse", "HEAD")
        return
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, resolve_validator=lambda: unit, corpus_ref=ref)
    assert str(refused.value).startswith(
        f"the validator unit carries corpus bytes that {lane._short(ref)} does "
        f"not hold: openxFactory-src/{lane.VALIDATOR_SCHEMAS_PATH}/"
        f"{STUB_SCHEMA}"), str(refused.value)
    assert "with schemas from another corpus revision" in str(refused.value)
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


def _unit_with_a_corpus_schema(corpus: Path, where: Path,
                               relpath: str) -> "lane.PinnedValidator":
    """A composed unit whose snapshot schema is LINKED into the corpus
    checkout at `relpath`, committed there, as the composer fills in a schema
    the carve legs do not supply. Its script is a committed product's."""
    schema = corpus / relpath
    schema.parent.mkdir(parents=True, exist_ok=True)
    schema.write_text("kind: from-the-corpus\n", encoding="utf-8")
    _git(corpus, "add", "-A")
    _git(corpus, "commit", "--quiet", "-m", f"a schema at {relpath}")
    product = where / "product"
    product.mkdir(parents=True)
    _git(product, "init", "--quiet", "-b", "main")
    script = product / lane.VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True)
    script.write_text(STUB_SCRIPT, encoding="utf-8")
    _git(product, "add", "-A")
    _git(product, "commit", "--quiet", "-m", "product")
    farm = where / "farm"
    runnable = farm / lane.VALIDATOR_SCRIPT_PATH
    runnable.parent.mkdir(parents=True)
    shutil.copyfile(script, runnable)
    (farm / lane.VALIDATOR_SCHEMAS_PATH).mkdir(parents=True)
    (farm / lane.VALIDATOR_SCHEMAS_PATH / STUB_SCHEMA).symlink_to(schema)
    return lane.PinnedValidator(runnable=runnable, product_root=product)


_CORPUS_SCHEMA = f"{lane.VALIDATOR_SCHEMAS_PATH}/{STUB_SCHEMA}"


@pytest.mark.parametrize("tamper", [
    "the-sealed-schema-rewritten", "the-corpus-copy-rewritten",
    "a-name-the-unit-lacks", "no-record", "not-a-mapping-of-paths"])
def test_verify_holds_each_corpus_schema_to_the_sealed_corpus(corpus,
                                                              tmp_path,
                                                              tamper):
    """WHICH SCHEMAS CAME FROM THE CORPUS (seal 2.2.0). The parent holds each
    schema the composer took from the corpus checkout to `source_head`'s bytes
    with git (Copilot, PR #1166). The child has no git, but the sealed corpus
    IS `source_head`'s tree, so the manifest names each such schema beside
    its corpus path, and the intake holds the two to one file's bytes. A
    record it cannot hold, or no record at all, is refused. Each tamper is
    made coherent, so only this requirement can see it."""
    unit = _unit_with_a_corpus_schema(corpus, tmp_path / "unit", _CORPUS_SCHEMA)
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, resolve_validator=lambda: unit)
    assert manifest["validator_corpus_schemas"] == {STUB_SCHEMA: _CORPUS_SCHEMA}
    assert lane.verify_seal(seal) == []
    schemas = f"{lane.SEAL_VALIDATOR_ROOT}/{lane.VALIDATOR_SCHEMAS_PATH}/"
    held = ("validator_corpus_schemas records {name!r} as the corpus's "
            "{relpath!r}, but the seal does not carry {schemas}{name} and "
            "openxFactory/{relpath} as the same bytes — the child would judge "
            "the render with a schema from another corpus revision")
    if tamper == "the-sealed-schema-rewritten":
        (seal / schemas / STUB_SCHEMA).write_text("kind: other\n",
                                                  encoding="utf-8")
        expected = [held.format(name=STUB_SCHEMA, relpath=_CORPUS_SCHEMA,
                                schemas=schemas)]
    elif tamper == "the-corpus-copy-rewritten":
        (seal / lane.SEAL_CORPUS_RELPATH / _CORPUS_SCHEMA).write_text(
            "kind: other\n", encoding="utf-8")
        expected = [held.format(name=STUB_SCHEMA, relpath=_CORPUS_SCHEMA,
                                schemas=schemas)]
    elif tamper == "a-name-the-unit-lacks":
        manifest["validator_corpus_schemas"]["other.schema.yaml"] = \
            _CORPUS_SCHEMA
        expected = [held.format(name="other.schema.yaml",
                                relpath=_CORPUS_SCHEMA, schemas=schemas)]
    elif tamper == "no-record":
        del manifest["validator_corpus_schemas"]
        expected = [NO_CORPUS_SCHEMAS]
    else:
        manifest["validator_corpus_schemas"] = {STUB_SCHEMA: 7}
        expected = [
            f"validator_corpus_schemas is {{{STUB_SCHEMA!r}: 7}} — the "
            "manifest does not record which of the sealed validator's schemas "
            "came from the corpus"]
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == expected


def test_a_corpus_schema_the_sealed_corpus_does_not_carry_is_refused(
        corpus, tmp_path):
    """The seal refuses first what the intake refuses: a schema the unit took
    from the corpus at a path the corpus archive does not carry (here
    `experiments/`, which is never sealed) could not be held to the sealed
    corpus by the child, so it is refused, naming it, and no manifest is
    written."""
    relpath = "experiments/extra.schema.yaml"
    unit = _unit_with_a_corpus_schema(corpus, tmp_path / "unit", relpath)
    seal = tmp_path / "seal"
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, resolve_validator=lambda: unit)
    assert str(refused.value) == (
        f"the validator unit takes {STUB_SCHEMA} from the corpus at "
        f"{relpath}, which the sealed corpus does not carry as the same bytes "
        "— the child could not hold the validator to the render's corpus")
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("shape", ["a-dangling-link", "a-directory"])
def test_a_unit_entry_that_is_not_a_regular_file_is_refused_by_name(
        corpus, tmp_path, shape):
    """The seal copies the composed unit's schemas THROUGH their links. An
    entry it cannot copy as a regular file is refused BY NAME, never skipped.
    A skipped schema would seal a narrower unit than the one the snapshot lane
    validates with, and the probe could not see it, because the validator asks
    for a family schema only when an instance needs one. The stub script here
    reaches a verdict on anything, so only the copy can refuse. The unit has
    no product tree, so the committed-bytes check, which runs first and would
    refuse the dangling link as a source in no repository, leaves the copy to
    refuse it: this test is about the copy."""
    stub = _stub_validator(tmp_path / "unit")
    unit = lane.PinnedValidator(runnable=stub.runnable)
    odd = (tmp_path / "unit" / lane.VALIDATOR_SCHEMAS_PATH
           / "ideation-dashboard-workbench.schema.yaml")
    if shape == "a-dangling-link":
        odd.symlink_to(tmp_path / "nowhere.schema.yaml")
    else:
        odd.mkdir()
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=lambda: unit)
    reason = str(refused.value)
    assert reason.startswith("the composed validator unit carries "
                             "ideation-dashboard-workbench.schema.yaml, which "
                             "does not resolve to a regular file")
    assert "narrower unit" in reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("answer", ["git-fails", "not-a-full-revision"])
def test_a_product_revision_that_cannot_be_read_refuses_the_seal(
        corpus, tmp_path, answer):
    """The manifest promises WHICH product revision the sealed validator came
    from. A unit resolved from a product tree whose HEAD cannot be read as a
    full revision is refused. It is never sealed with a null revision (Copilot
    review of #1162). A unit with no product tree at all records none, and
    the seal refuses that too, as a validator it cannot hold to the render
    (`test_a_validator_the_seal_cannot_hold_to_the_render_is_refused`). The
    runner answers the one product read here, so no real tree has to be
    broken to ask it."""
    stub = _stub_validator(tmp_path / "unit")
    product = tmp_path / "product"
    product.mkdir()
    pinned = lane.PinnedValidator(runnable=stub.runnable, product_root=product)
    asked = ("git", "--no-replace-objects", "-C", str(product), "rev-parse",
             "HEAD")

    def runner(argv, **kw):
        if tuple(str(a) for a in argv) == asked:
            if answer == "git-fails":
                return lane.CommandResult(asked, 128, "",
                                          "fatal: not a git repository")
            return lane.CommandResult(asked, 0, "abc1234\n", "")
        return lane.subprocess_runner(argv, **kw)

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", runner=runner,
              resolve_validator=lambda: pinned)
    reason = str(refused.value)
    assert reason.startswith("could not resolve the pinned product's revision "
                             f"at {product} to a commit")
    assert ("(read nothing)" if answer == "git-fails"
            else "(read 'abc1234')") in reason
    assert "provenance would go unrecorded" in reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("shape", ["no-product-tree", "no-validator-leg"])
def test_a_validator_the_seal_cannot_hold_to_the_render_is_refused(
        corpus, tmp_path, shape):
    """ONE PRODUCT REVISION, ALWAYS CHECKED (Copilot, PR #1166). The seal
    holds its validator to the render unit's openXdox code leg. A unit with
    no product tree records no revision to hold, and a render unit without
    that leg has nothing to hold it to. Both used to seal, with the check
    skipped, and the intake now refuses a null revision, so the seal refuses
    both first and leaves no manifest."""
    stub = _stub_validator(tmp_path / "unit")
    head = _validator_head(stub)
    injected = {}
    if shape == "no-product-tree":
        unit = lane.PinnedValidator(runnable=stub.runnable)
    else:
        unit = stub
        injected["seal_legs"] = lambda **legs: [
            record for record in _stub_leg_records(
                legs["corpus_root"], PRODUCT_MODULE_TEXT, head)
            if (record["gitlink"], record["leg"]) != lane.VALIDATOR_LEG]
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=lambda: unit,
              **injected)
    reason = str(refused.value)
    if shape == "no-product-tree":
        assert reason.startswith(
            "the sealed validator records no product revision (it was not "
            "resolved from a product tree), so it cannot be held to the "
            "render unit's openXdox code leg"), reason
    else:
        assert reason.startswith(
            f"the sealed validator was copied from openXdox code at "
            f"{lane._short(head)}, but the sealed render unit carries no "
            "openXdox code leg"), reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


_RECORDING_VALIDATOR = '''\
import json, os, sys
from pathlib import Path
with open(RECORD, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({
        "file": __file__, "argv": sys.argv[1:], "cwd": os.getcwd(),
        "env": dict(os.environ),
        "probe": json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")),
    }) + "\\n")
print("ok")
'''


def _recording_validator(where: Path, record: Path) -> "lane.PinnedValidator":
    """`_stub_validator`, whose script also appends one line to `record` for
    each run: the file that ran, its argv, the probe it was handed, its working
    directory and its environment. The evidence is what the VALIDATOR PROCESS
    saw, so nothing in this process is patched to observe it."""
    return _stub_validator(
        where, script=f"RECORD = {str(record)!r}\n" + _RECORDING_VALIDATOR)


# What the job holding the seal could export: its credentials, its GitHub and
# Git plumbing, an interpreter path override, and credentials a denylist would
# have had to name (Copilot, PR #1166). None of it may reach sealed code.
_JOB_ENVIRONMENT = {
    "GH_TOKEN": "t1", "GITHUB_TOKEN": "t2", "SUBMODULE_TOKEN": "t3",
    "AZURE_CLIENT_SECRET": "t4", "ACR_PASSWORD": "t5",
    "SIGNING_PRIVATE_KEY": "t6", "GITHUB_WORKSPACE": "/w",
    "GIT_ASKPASS": "/askpass", "GIT_CONFIG_PARAMETERS": "'http.extraheader=x'",
    "ACTIONS_RUNTIME_TOKEN": "t7", "SSH_AUTH_SOCK": "/s",
    "PYTHONPATH": "/elsewhere", "AWS_ACCESS_KEY_ID": "t8",
    "DOCKER_AUTH_CONFIG": "t9", "KUBECONFIG": "/runner/kube",
    "NPM_CONFIG_USERCONFIG": "/runner/npmrc", "VIRTUAL_ENV": "/runner/venv"}
_JOB_SECRETS = ("t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9")
# What a sealed run is given, and all it is given (#1191): four literals, and
# the PATH the stand-in docker CLI runs the host's interpreter by.
_SEALED_RUN_ENV = {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8",
                   "LANG": "C.UTF-8"}


def _export_the_job_environment(monkeypatch) -> None:
    for name, value in _JOB_ENVIRONMENT.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("LC_ALL", "C.UTF-8")


def _assert_the_renders_environment(env: dict, seal: Path) -> None:
    """NOTHING OF THE JOB'S reaches sealed code (#1191). A sealed run is given
    four literals and nothing else, and the stand-in docker CLI adds only the
    PATH it runs the host's interpreter by. HOME is the container's own /tmp,
    never the job's, and not even the job's locale crosses."""
    for name in _JOB_ENVIRONMENT:
        assert name not in env, name
    assert not any(value in _JOB_SECRETS for value in env.values())
    assert set(env) - {"PATH"} == {*_SEALED_RUN_ENV, "HOME"}, sorted(env)
    for name, value in _SEALED_RUN_ENV.items():
        assert env[name] == value, name
    assert env["HOME"] != os.environ.get("HOME")
    assert "LC_ALL" not in env


def test_the_one_run_is_of_the_sealed_copy_over_the_probe(corpus, tmp_path,
                                                          monkeypatch):
    """What the parent runs is the SEALED copy, from inside the seal. It is not
    the composed unit it was copied from, because the child will run the copy.
    It runs exactly once, over `VALIDATOR_PROBE`, and the probe itself is never
    part of the artifact. The copy is sealed code and this job holds
    credentials, so it runs in the render's allowlisted environment, from a
    scratch directory (Copilot, PR #1166)."""
    _export_the_job_environment(monkeypatch)
    record = tmp_path / "probe-runs.jsonl"
    stub = _recording_validator(tmp_path / "unit", record)
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, resolve_validator=lambda: stub)
    runs = [json.loads(line)
            for line in record.read_text(encoding="utf-8").splitlines()]
    assert len(runs) == 1
    (run,) = runs
    assert Path(run["file"]).resolve() == \
        (seal / lane.SEAL_VALIDATOR_RELPATH).resolve()
    assert run["probe"] == lane.VALIDATOR_PROBE
    assert run["argv"][1:] == []                     # no --strict
    assert not Path(run["argv"][0]).resolve().is_relative_to(seal.resolve())
    assert not any(key.endswith("validator-probe.json") for key in manifest["files"])
    _assert_the_renders_environment(run["env"], seal)
    assert not Path(run["cwd"]).resolve().is_relative_to(seal.resolve())
    assert Path(run["cwd"]).resolve() != Path.cwd().resolve()
    assert manifest["validator_probe"] == {
        "kind": lane.VALIDATOR_PROBE["kind"],
        "outcome": snapshot_mod.VALIDATED, "returncode": 0}


@pytest.mark.parametrize("change", ["a-file-rewritten", "a-file-added"])
def test_a_probe_that_changes_the_sealed_tree_is_refused(corpus, tmp_path,
                                                         change):
    """The probe runs sealed code with the seal writable, and it runs before
    the seal's index is taken. So the tree is indexed around the probe too,
    and a validator that rewrote or added a file while it ran is refused,
    never indexed and published (Copilot, PR #1166)."""
    target = ("docs/a.md" if change == "a-file-rewritten"
              else "docs/planted.md")
    stub = _stub_validator(tmp_path / "unit", script=(
        "from pathlib import Path\n"
        "seal = Path(__file__).resolve().parents[2]\n"
        f"(seal / 'openxFactory' / {target!r}).write_text('planted\\n')\n"
        "print('ok')\n"))
    if change == "a-file-rewritten":
        assert (corpus / target).is_file()
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=lambda: stub)
    assert str(refused.value) == (
        "the sealed validator's probe changed the sealed tree, so the seal "
        "would no longer be the tree its validator was run in")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_probe_is_classified_by_the_sealed_product_module(corpus,
                                                              tmp_path):
    """The probe's run is read by the product's own `validate_snapshot` as the
    SEAL carries it, out of the sealed openXdox leg, never by this parent's
    worktree copy, which could be dirty (Copilot, PR #1166)."""
    record = tmp_path / "classified-by.txt"
    seal = tmp_path / "seal"
    _seal(corpus, seal, product_module=_recording_product_module(record))
    assert record.read_text(encoding="utf-8").splitlines() == [
        str(lane.sealed_product_module(seal))]


@pytest.mark.parametrize("lie", [{"returncode": 2},
                                 {"outcome": "not-conformant"}],
                         ids=["validated-with-exit-2",
                              "not-conformant-with-exit-0"])
def test_a_probe_verdict_that_does_not_pair_with_its_exit_code_is_refused(
        corpus, tmp_path, lie):
    """The seal records what the intake reads, and nothing the intake would
    refuse. A sealed product module can print any pairing it likes, and one
    that is not a verdict as the validator reports one is refused at the
    seal, leaving no manifest (Copilot, opensoft/xFactory PR #526)."""
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal",
              product_module=_lying_product_module(**lie))
    outcome = lie.get("outcome", "validated")
    returncode = lie.get("returncode", 0)
    assert str(refused.value).startswith(
        f"the sealed validator's probe answered {outcome!r} with exit "
        f"{returncode!r}, which is not a verdict as the validator reports one "
        f"({VERDICT_PAIRS})"), str(refused.value)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_seal_without_the_product_module_cannot_classify_its_probe(
        corpus, tmp_path):
    """A sealed openXdox leg that carries no product module leaves the parent
    nothing to read the probe with, so the seal is refused, naming why."""
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", product_module=None)
    reason = str(refused.value)
    assert reason.startswith("the sealed validator could NOT RUN")
    assert "the validator's harness returned no verdict (exit 1)" in reason
    assert "cannot import name 'snapshot' from 'openxdox'" in reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_confined_locator_never_adopts_the_sealed_validator(corpus, tmp_path):
    """THE WALK THIS TEST ONCE PROVED IS GONE, ON PURPOSE. Since openXdox-code
    `e28930bf` (split-opendox-two-layer-product § 8.9 residue (iii)),
    `snapshot.find_validator` answers only for the product's OWN validator.
    There it CONFINED instead of walking up: a start outside the product's tree
    answered None. Since openXdox-code #36 (`6a3b93b9`, plan 034 T061, #1144
    7.3, RULED R1Q14 (a)) it IGNORES its start: it answers the installed
    distribution's own validator, which in a source checkout, the way
    openxFactory composes the leg, is that tree's own
    `scripts/validate-ideation-dashboard-contracts.py`. So the assertion is
    what this test is for, and it holds at both pins (plan 034 T066): whatever
    the locator answers for a start inside the seal, it is never the sealed
    copy, from where it sits, from the seal root, from the directory the child
    hands `--repo-root`, or from its own directory. A caller that means it
    passes it explicitly (`validate_snapshot(..., validator=...)`), and that
    channel is proven here too. As before, this runs the REAL locator over a
    REAL sealed tree rather than restating a path. Since #1158 the sealed copy
    lives under the seal's own `validator/` root, and the refresh lane's seal
    rationale says so.
    """
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    corpus_root = seal / lane.SEAL_CORPUS_RELPATH
    sealed = seal / lane.SEAL_VALIDATOR_RELPATH
    assert sealed.is_file()
    own = snapshot_mod.find_validator()
    assert own is None or not own.resolve().is_relative_to(seal.resolve())
    # Confined (None) at the older leg, the product's own at T061's: never an
    # enclosing tree's validator, and so never the sealed copy.
    for start in (seal, corpus_root, sealed.parent):
        found = snapshot_mod.find_validator(start)
        assert found is None or found == own, (start, found, own)
        assert found is None or not found.resolve().is_relative_to(
            seal.resolve()), (start, found)
    # Passed explicitly, the sealed copy is the one that runs. The stub unit's
    # script prints `ok` and exits 0, whatever it is handed.
    probe = tmp_path / "probe.json"
    probe.write_text("{}\n", encoding="utf-8")
    result = snapshot_mod.validate_snapshot(probe, validator=sealed)
    assert result.outcome == snapshot_mod.VALIDATED
    assert result.validator == sealed


def test_the_seal_is_bounded_to_the_seal_paths(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert not (seal / lane.SEAL_CORPUS_RELPATH / "experiments").exists()
    prefixes = {relpath.split("/", 1)[0] for relpath in manifest["files"]}
    assert prefixes == {lane.SEAL_CORPUS_RELPATH, "recipe",
                        lane.SEAL_VALIDATOR_ROOT}
    # The validator root holds the script and its schemas, and nothing else.
    unit = {relpath for relpath in manifest["files"]
            if relpath.startswith(lane.SEAL_VALIDATOR_ROOT + "/")}
    schemas = f"{lane.SEAL_VALIDATOR_ROOT}/{lane.VALIDATOR_SCHEMAS_PATH}/"
    assert lane.SEAL_VALIDATOR_RELPATH in unit
    assert unit - {lane.SEAL_VALIDATOR_RELPATH} == \
        {relpath for relpath in unit if relpath.startswith(schemas)}


# ---------------------------------------------------------------------------
# the manifest
# ---------------------------------------------------------------------------

def test_the_manifest_carries_every_field_the_child_reads(corpus, tmp_path):
    seal = tmp_path / "seal"
    head = _git(corpus, "rev-parse", "HEAD")
    manifest = _seal(corpus, seal)
    on_disk = json.loads((seal / lane.SEAL_MANIFEST_NAME).read_text(encoding="utf-8"))
    assert on_disk == manifest                      # written, not just returned
    assert manifest["schema_version"] == lane.SEAL_SCHEMA_VERSION
    assert manifest["kind"] == lane.SEAL_MANIFEST_KIND
    assert manifest["artifact_name"] == f"dashboard-image-source-{CORRELATION}"
    assert manifest["correlation_id"] == CORRELATION
    assert manifest["source_repo"] == lane.DEFAULT_CORPUS_REPO
    assert manifest["source_head"] == head
    assert manifest["corpus_revision"] == head
    assert manifest["corpus_baked_paths"] == list(lane.CORPUS_BAKED_PATHS)
    assert manifest["seal_paths"] == list(lane.CORPUS_SEAL_PATHS)
    assert manifest["recipe_repo"] == lane.DEFAULT_RECIPE_REPO
    assert manifest["recipe_revision"] == RECIPE_REV
    assert manifest["recipe_path"] == lane.RECIPE_DOCKERFILE_PATH
    assert manifest["recipe_relpath"] == lane.SEAL_RECIPE_RELPATH
    assert manifest["corpus_relpath"] == lane.SEAL_CORPUS_RELPATH
    assert manifest["validator_relpath"] == lane.SEAL_VALIDATOR_RELPATH
    assert manifest["validator_relpath"] in manifest["files"]
    assert manifest["validator_schema_count"] == 1        # the stub unit's one
    # The revision of the stand-in's committed tree, which is the revision
    # the stand-in legs record for the openXdox code leg.
    assert manifest["validator_revision"] == \
        _git(tmp_path / "stub-validator", "rev-parse", "HEAD")
    assert manifest["validator_revision"] == next(
        leg["leg_revision"] for leg in manifest["render_legs"]
        if (leg["gitlink"], leg["leg"]) == lane.VALIDATOR_LEG)
    assert manifest["validator_probe"] == {
        "kind": lane.VALIDATOR_PROBE["kind"],
        "outcome": snapshot_mod.VALIDATED, "returncode": 0}
    # The stand-in unit's one schema is its own tree's, not the corpus's.
    assert manifest["validator_corpus_schemas"] == {}
    # The render unit (#1161): the entry the child runs, both legs, and what
    # the pre-dispatch render answered.
    assert manifest["render_entry"] == lane.RENDER_ENTRY
    assert f"{lane.SEAL_CORPUS_RELPATH}/{lane.RENDER_ENTRY}" in manifest["files"]
    assert [(leg["gitlink"], leg["leg"], leg["package"])
            for leg in manifest["render_legs"]] == list(lane.RENDER_LEGS)
    assert manifest["precheck"] == STUB_PRECHECK
    # The serve unit (#1164, seal 2.2.0): the entry the served image starts,
    # and every path its recipe copies, each carried as rows of `files`.
    assert manifest["schema_version"] == "2.2.0"
    assert manifest.get("serve_entry") == SERVE_ENTRY
    assert manifest.get("serve_unit") == list(SERVE_UNIT)
    for path in SERVE_UNIT:
        carried = f"{lane.SEAL_CORPUS_RELPATH}/{path}"
        assert (any(key.startswith(carried) for key in manifest["files"])
                if path.endswith("/") else carried in manifest["files"]), path
    assert SERVE_ENTRY in manifest["seal_paths"]
    assert SERVE_ENTRY in manifest["corpus_baked_paths"]
    assert manifest["digest_algorithm"] == "sha256"
    assert manifest["decision"]["reason"] == lane.REASON_CORPUS_MOVED
    assert (seal / manifest["recipe_relpath"]).read_text(encoding="utf-8") \
        == RECIPE_TEXT
    # The measurement open question 2 asks for, recorded on every seal rather
    # than reconstructed from a run log.
    assert manifest["file_count"] == len(manifest["files"]) > 0
    assert manifest["total_bytes"] > 0


def test_the_manifest_names_the_field_that_feeds_generated_at(corpus, tmp_path):
    """`--generated-at` must receive the SOURCE COMMIT's committer date, never
    a wall clock: `generation.generated_at` is defined as that date and the
    snapshot render is canonical precisely because nothing in it reads the
    clock. So the manifest names the field, and the parent's own wall clock
    lives under a different name that the named field is proven not to be."""
    manifest = _seal(corpus, tmp_path / "seal")
    assert manifest["generated_at_field"] == "source_committed_at"
    stamp = manifest[manifest["generated_at_field"]]
    assert is_rfc3339_datetime(stamp)               # the flag will accept it
    assert _instant(stamp) == _instant(COMMITTED_AT)   # the commit's own date
    assert manifest["sealed_at"] != stamp
    assert manifest["generated_at_field"] != "sealed_at"


def test_the_manifest_is_not_in_its_own_index(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert lane.SEAL_MANIFEST_NAME not in manifest["files"]
    assert all(not key.startswith("/") for key in manifest["files"])


# ---------------------------------------------------------------------------
# the tree digest — the rule the child (S3) recomputes
# ---------------------------------------------------------------------------

def _independent_tree_digest(seal: Path) -> str:
    """The rule `TREE_DIGEST_SPEC` states, implemented from the prose rather
    than by calling the module — which is what makes the spec, and therefore
    the child's implementation, verifiable."""
    lines = []
    for path in sorted(seal.rglob("*"), key=lambda p: p.as_posix()):
        if not path.is_file():
            continue
        relpath = path.relative_to(seal).as_posix()
        if relpath == "manifest.json":
            continue
        lines.append((relpath.encode("utf-8"),
                      hashlib.sha256(path.read_bytes()).hexdigest()))
    body = b"".join(f"{digest}  ".encode("ascii") + relpath + b"\n"
                    for relpath, digest in sorted(lines))
    return hashlib.sha256(body).hexdigest()


def test_the_tree_digest_is_the_rule_the_manifest_states(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert manifest["tree_digest"] == _independent_tree_digest(seal)
    assert "sha256" in manifest["tree_digest_spec"]
    assert "manifest.json" in manifest["tree_digest_spec"]


def test_the_tree_digest_is_order_independent_and_content_sensitive():
    index = {"b.txt": "b" * 64, "a.txt": "a" * 64, "d/c.txt": "c" * 64}
    reordered = {key: index[key] for key in reversed(list(index))}
    assert lane.tree_digest(index) == lane.tree_digest(reordered)
    moved = dict(index, **{"a.txt": "0" * 64})
    assert lane.tree_digest(moved) != lane.tree_digest(index)
    renamed = {("z.txt" if key == "a.txt" else key): value
               for key, value in index.items()}
    assert lane.tree_digest(renamed) != lane.tree_digest(index)


def test_the_tree_digest_of_one_revision_is_stable_across_two_seals(corpus, tmp_path):
    first = _seal(corpus, tmp_path / "one")
    second = _seal(corpus, tmp_path / "two")
    assert first["tree_digest"] == second["tree_digest"]
    assert first["files"] == second["files"]
    assert first["source_head"] == second["source_head"]


# ---------------------------------------------------------------------------
# the parent-side one-revision assertion (design open question 1)
# ---------------------------------------------------------------------------

def test_git_records_the_archive_revision_and_the_seal_reads_it_back(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")
    archive = tmp_path / "probe.tar"
    _git(corpus, "archive", "--format=tar", f"--output={archive}", head, "--",
         *lane.CORPUS_SEAL_PATHS)
    assert lane.git_archive_revision(archive) == head


def test_an_archive_naming_another_revision_is_refused(corpus, tmp_path, monkeypatch):
    """The whole point of the parent-side assertion: a seal whose bytes came
    from a commit other than the one the manifest would record must not exist,
    because nothing downstream could ever disprove the manifest."""
    other = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "git_archive_revision", lambda _path: "f" * 40)
    with pytest.raises(lane.SealRefused, match="recorded revision"):
        _seal(corpus, tmp_path / "seal", decision=_decision(other))
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_an_archive_with_no_recorded_revision_is_refused(corpus, tmp_path, monkeypatch):
    monkeypatch.setattr(lane, "git_archive_revision", lambda _path: None)
    with pytest.raises(lane.SealRefused, match="absent"):
        _seal(corpus, tmp_path / "seal")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("name, match", [
    ("/etc/cron.d/evil", "absolute member path"),
    ("../../etc/cron.d/evil", "traversing member path"),
    ("docs/../../escape.txt", "traversing member path"),
])
def test_a_member_path_that_could_escape_the_seal_is_refused(tmp_path, name, match):
    """Checked on the NAMES, before extraction, so it holds on BOTH extraction
    branches — the `data` filter would catch these on a modern interpreter, but
    the `TypeError` fallback for an interpreter without extraction filters
    would not, and "git produced the archive so its names are fine" is exactly
    the assumption an extraction hazard is made of (Copilot, PR #648)."""
    archive = tmp_path / "escape.tar"
    with tarfile.open(archive, "w") as handle:
        payload = b"pwned\n"
        member = tarfile.TarInfo(name)
        member.size = len(payload)
        handle.addfile(member, __import__("io").BytesIO(payload))
    with pytest.raises(lane.SealRefused, match=match):
        lane._extract_seal_archive(archive, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()


def test_a_non_regular_archive_entry_is_refused(tmp_path):
    archive = tmp_path / "linky.tar"
    with tarfile.open(archive, "w") as handle:
        member = tarfile.TarInfo("docs/elsewhere")
        member.type = tarfile.SYMTYPE
        member.linkname = "/etc/passwd"
        handle.addfile(member)
    with pytest.raises(lane.SealRefused, match="non-regular"):
        lane._extract_seal_archive(archive, tmp_path / "out")


# ---------------------------------------------------------------------------
# refusals — and every one of them leaves no manifest
# ---------------------------------------------------------------------------

def test_a_decision_that_asked_for_no_build_seals_nothing(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")
    for decision in ({"build": False, "outcome": "no_change",
                      "corpus_revision": head, "recipe_revision": RECIPE_REV},
                     {"outcome": "undecidable"},
                     {}):
        with pytest.raises(lane.SealRefused, match="nothing to seal"):
            _seal(corpus, tmp_path / "seal", decision=decision)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("bad", [
    {"corpus_revision": ""},
    {"corpus_revision": "abc1234"},           # abbreviated is not a full sha
    {"corpus_revision": "z" * 40},
    {"recipe_revision": None},
    {"recipe_revision": "HEAD"},
])
def test_a_malformed_decision_revision_is_refused(corpus, tmp_path, bad):
    decision = _decision(_git(corpus, "rev-parse", "HEAD"))
    decision.update(bad)
    with pytest.raises(lane.SealRefused, match="no usable"):
        _seal(corpus, tmp_path / "seal", decision=decision)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("bad", ["", "  ", "a/b", "a:b", 'a"b', "-leading",
                                 "x" * 121, "a\nb"])
def test_a_correlation_id_that_cannot_name_an_artifact_is_refused(bad):
    with pytest.raises(lane.SealRefused, match="cannot name an Actions artifact"):
        lane.seal_artifact_name(bad)


def test_the_correlation_id_is_canonicalized_once(corpus, tmp_path):
    """The artifact NAME and the manifest's `correlation_id` are compared
    against each other by the child, so a value with surrounding whitespace
    must be stripped for both or neither — otherwise the child refuses a
    perfectly good seal over a space (Copilot, PR #648)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, correlation_id=f"  {CORRELATION}\n")
    assert manifest["correlation_id"] == CORRELATION
    assert manifest["artifact_name"] == \
        f"{lane.SEAL_ARTIFACT_PREFIX}{manifest['correlation_id']}"
    assert lane.verify_seal(seal, correlation_id=CORRELATION) == []


def test_the_artifact_name_is_the_prefix_plus_the_correlation_id():
    assert lane.seal_artifact_name(CORRELATION) == \
        f"dashboard-image-source-{CORRELATION}"
    assert lane.SEAL_ARTIFACT_PREFIX == "dashboard-image-source-"


@pytest.mark.parametrize("recipe", [None, "", "   \n"])
def test_an_unreadable_recipe_is_refused(corpus, tmp_path, recipe):
    with pytest.raises(lane.SealRefused, match="could not read"):
        _seal(corpus, tmp_path / "seal", recipe=recipe)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_an_unresolvable_source_ref_is_refused(corpus, tmp_path):
    with pytest.raises(lane.SealRefused, match="could not resolve"):
        _seal(corpus, tmp_path / "seal", corpus_ref="origin/nope")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_failing_archive_is_refused_rather_than_half_sealed(corpus, tmp_path):
    head = _git(corpus, "rev-parse", "HEAD")

    def runner(argv, **kw):
        if "archive" in [str(a) for a in argv]:
            return lane.CommandResult(tuple(str(a) for a in argv), 128, "",
                                      "fatal: not a tree object")
        return lane.subprocess_runner(argv, **kw)

    with pytest.raises(lane.SealRefused, match="archive failed"):
        _seal(corpus, tmp_path / "seal", decision=_decision(head), runner=runner)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_intermediate_archive_is_never_part_of_the_artifact(corpus, tmp_path):
    """The tar is staged outside the seal AND outside the checkout: it is not
    part of the artifact, and a `.tar` swept into the `files` index would be an
    8-figure byte count the child downloads twice."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert [path.name for path in tmp_path.rglob("*.tar")] == []
    assert not any(key.endswith(".tar") for key in manifest["files"])


# ---------------------------------------------------------------------------
# THE SEAL DIRECTORY IS THE LANE'S OWN (#1182). The lane makes it itself,
# exclusively, before anything is written into it and before any sealed code
# runs, and holds a handle on it from then on. Everything the lane writes
# under it goes through that handle, so a path swapped after the making
# redirects nothing, and a seal whose path no longer leads to the directory
# the lane made is refused.
# ---------------------------------------------------------------------------

def _existing_seal_path(seal: Path) -> str:
    return (f"the seal directory {seal} already exists: a seal is materialized "
            "only into a directory the lane creates itself, never into one it "
            "found")


def _linked_seal_path(seal: Path) -> str:
    return (f"the seal directory {seal} is not a directory of its own, but a "
            "link: a seal is materialized only into a directory the lane "
            "creates itself, and never through a link")


def _recording_resolver(where: Path, calls: list):
    """A stand-in resolver that records each time the seal resolves its
    validator, which it does before it makes the seal directory."""
    stub = _stub_validator(where)

    def resolving():
        calls.append(stub)
        return stub

    return resolving


def _what_is_at(path: Path):
    """What sits at `path`, to show nothing was written into it: a
    directory's listing, a file's bytes, or None."""
    if path.is_dir():
        return sorted(entry.name for entry in path.iterdir())
    return path.read_bytes() if path.exists() else None


def _identity(path) -> tuple[int, int]:
    """The directory `path` leads to, as `(st_dev, st_ino)`."""
    info = os.stat(path)
    return info.st_dev, info.st_ino


def _tree_state(root: Path) -> dict:
    """Every path under `root`, with what it is: a directory, a link and
    its target, or a file and its bytes."""
    state: dict = {}
    for path in sorted(root.rglob("*")):
        key = path.relative_to(root).as_posix()
        if path.is_symlink():
            state[key] = ("link", os.readlink(path))
        elif path.is_dir():
            state[key] = ("directory",)
        else:
            state[key] = ("file", path.read_bytes())
    return state


@pytest.mark.parametrize("found", ["an-empty-directory",
                                   "a-directory-holding-files", "a-file"])
def test_a_seal_directory_that_already_exists_is_refused(corpus, tmp_path,
                                                          found):
    """A SEAL IS A FRESH TREE THE LANE MAKES ITSELF (#1182). `files` is the
    authority on what the child must find, so a leftover from an earlier
    attempt would be indexed, digested and shipped as though the parent had
    sealed it, and a directory someone else made, empty or not, is one whose
    history the lane cannot vouch for. So anything already at the seal's
    path refuses the seal, before the validator is even resolved, and
    nothing is written into it."""
    seal = tmp_path / "seal"
    if found == "a-file":
        seal.write_text("not a directory\n", encoding="utf-8")
    else:
        seal.mkdir()
        if found == "a-directory-holding-files":
            (seal / "leftover.txt").write_text("from an earlier attempt\n",
                                               encoding="utf-8")
    before = _what_is_at(seal)
    calls: list = []
    resolving = _recording_resolver(tmp_path / "unit", calls)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, resolve_validator=resolving)
    assert str(refused.value) == _existing_seal_path(seal)
    assert calls == []
    assert _what_is_at(seal) == before


def test_a_seal_directory_that_appears_before_the_lane_makes_it_is_refused(
        corpus, tmp_path):
    """THE MAKING IS EXCLUSIVE (#1182). The lane looks for an existing path
    first, for a legible refusal, then makes the directory with a plain
    `mkdir`, which fails on anything already there. A directory that appears
    in between, here as the validator is resolved, is refused as one the lane
    found, never adopted."""
    seal = tmp_path / "seal"
    stub = _stub_validator(tmp_path / "unit")

    def appearing():
        seal.mkdir()
        return stub

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, resolve_validator=appearing)
    assert str(refused.value) == _existing_seal_path(seal)
    assert list(seal.iterdir()) == []


@pytest.mark.parametrize("swap", ["a-link-out", "a-directory-holding-files"])
def test_a_seal_directory_swapped_as_the_lane_makes_it_is_refused(
        corpus, tmp_path, monkeypatch, swap):
    """THE DIRECTORY HELD IS THE DIRECTORY MADE (#1182). Something acting in
    the instant between the lane's `mkdir` and its taking a handle could put
    a link, or another directory, at the seal's path. The handle is opened
    without following a link, relative to the directory the seal was made
    in, and a directory the lane has just made holds nothing, so either is
    refused, and nothing is written through it. The swap is made here as the
    lane's own `mkdir` of the seal returns."""
    seal = tmp_path / "seal"
    outside = tmp_path / "outside"
    outside.mkdir()
    make = os.mkdir

    def making_then_swapping(path, mode=0o777, *, dir_fd=None):
        make(path, mode, dir_fd=dir_fd)
        if dir_fd is None or os.fspath(path) != seal.name:
            return
        os.rename(seal.name, f"{seal.name}.made", src_dir_fd=dir_fd,
                  dst_dir_fd=dir_fd)
        if swap == "a-link-out":
            os.symlink(outside, seal.name, target_is_directory=True,
                       dir_fd=dir_fd)
        else:
            make(seal.name, mode, dir_fd=dir_fd)
            (seal / "planted.txt").write_text("planted\n", encoding="utf-8")

    monkeypatch.setattr(lane.os, "mkdir", making_then_swapping)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal)
    assert str(refused.value) == (
        f"the seal directory {seal} was replaced as the lane made it, and "
        "nothing is written into what took its place")
    assert list(outside.iterdir()) == []
    assert not (tmp_path / f"{seal.name}.made" / lane.SEAL_CORPUS_RELPATH
                ).exists()


def test_a_seal_directory_swapped_after_the_lane_made_it_gets_nothing_more(
        corpus, tmp_path):
    """A SWAPPED SEAL DIRECTORY GETS NOTHING MORE (#1182). Once the lane has
    made the seal directory, something may move it aside and put a link to
    another directory at its path, here as the legs are sealed. Nothing more
    is written, through the link or into the directory moved aside: the lane
    finds its path no longer leads to the directory it holds before it
    extracts the corpus, and refuses the seal. Before this, the corpus and
    the validator were extracted through the link, and the probe ran from
    the other directory."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"
    outside = tmp_path / "outside"
    outside.mkdir()
    stub = _stub_validator(tmp_path / "unit")

    def swapping_legs(*, corpus_checkout, source_head, corpus_root, runner):
        records = _stub_leg_records(corpus_root, PRODUCT_MODULE_TEXT,
                                    _validator_head(stub))
        seal.rename(moved)
        seal.symlink_to(outside, target_is_directory=True)
        return records

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, resolve_validator=lambda: stub,
              seal_legs=swapping_legs)
    assert sorted(path.name for path in outside.iterdir()) == []
    assert str(refused.value) == (
        "the seal directory is no longer the one the lane created: it was "
        "replaced after the lane made it, and the corpus is never written "
        "anywhere else")
    assert not (moved / lane.SEAL_CORPUS_RELPATH / "docs").exists()
    assert not (moved / lane.SEAL_VALIDATOR_ROOT).exists()
    assert not (moved / lane.SEAL_MANIFEST_NAME).exists()


def test_a_seal_directory_swapped_while_the_lane_writes_it_keeps_the_writes(
        corpus, tmp_path):
    """EVERY WRITE GOES THROUGH THE HANDLE (#1182). The corpus is extracted,
    and the validator copied, through the handle the lane holds on the
    directory it made, never through its path. So a swap of the path in the
    middle of the writing, here as the corpus archive is made, redirects
    nothing: the corpus lands in the directory the lane made, wherever that
    now is, and nothing lands where the link points. The next check refuses
    the seal, before the recipe is written."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"
    outside = tmp_path / "outside"
    outside.mkdir()
    swapped: list = []

    def runner(argv, **kw):
        result = lane.subprocess_runner(argv, **kw)
        if "archive" in [str(a) for a in argv] and not swapped:
            seal.rename(moved)
            seal.symlink_to(outside, target_is_directory=True)
            swapped.append(argv)
        return result

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, runner=runner)
    assert swapped, "the corpus archive was never made"
    assert sorted(path.name for path in outside.iterdir()) == []
    assert (moved / lane.SEAL_CORPUS_RELPATH / "docs" / "a.md").is_file()
    assert (moved / lane.SEAL_VALIDATOR_RELPATH).is_file()
    assert str(refused.value) == (
        "the seal directory is no longer the one the lane created: sealed "
        "code ran inside it, and the recipe is never written anywhere else")
    assert not (moved / "recipe").exists()
    assert not (moved / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("replacement", ["a-fresh-directory",
                                         "a-link-to-the-moved-one"])
def test_a_directory_on_the_way_swapped_as_the_seal_is_made_gets_nothing(
        corpus, tmp_path, monkeypatch, replacement):
    """THE WAY TO THE SEAL IS HELD AS WELL AS THE SEAL (Copilot, PR #1185).
    The walk from the root holds each directory on the way by a handle, and
    the seal is made relative to the last one. So a directory on the way
    that is moved out of the root after the walk opened it, and replaced,
    would have the seal made inside the moved one, out of the root, while
    its name led to the replacement, and the legs would be written there
    before any check of the name. Once the seal is made, its way is walked
    again from the root, by name and through no link, and a seal its name
    does not lead to is refused before anything is written into it. The
    swap is made here as the lane's own `mkdir` of the seal is called: `a`
    moves out of the root, and a fresh directory, or a link to where `a`
    went, takes its place."""
    root = tmp_path / "root"
    seal = root / "a" / "b" / "dfr-seal"
    seal.parent.mkdir(parents=True)
    moved = tmp_path / "moved"
    stub = _stub_validator(tmp_path / "unit")
    make = os.mkdir

    def swapping_then_making(path, mode=0o777, *, dir_fd=None):
        if (dir_fd is not None and os.fspath(path) == seal.name
                and not moved.exists()):
            (root / "a").rename(moved)
            if replacement == "a-fresh-directory":
                seal.parent.mkdir(parents=True)
            else:
                (root / "a").symlink_to(moved, target_is_directory=True)
        make(path, mode, dir_fd=dir_fd)

    monkeypatch.setattr(lane.os, "mkdir", swapping_then_making)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, seal_within=root, resolve_validator=lambda: stub)
    assert _what_is_at(moved / "b" / seal.name) == []
    assert str(refused.value) == (
        f"the seal directory {seal} was made where its path no longer leads: "
        f"a directory on its way from {root} was replaced as the lane made "
        "it, and nothing is written into it")
    if replacement == "a-fresh-directory":
        assert not os.path.lexists(seal)


@pytest.mark.parametrize("when", ["as-the-legs-are-sealed",
                                  "as-the-render-runs"])
def test_a_directory_on_the_way_swapped_for_a_link_gets_nothing_more(
        corpus, tmp_path, when):
    """THE NAME IS HELD TO THE SEAL THROUGH NO LINK (Copilot, PR #1185). A
    directory on the seal's way may be moved out of the root after the seal
    is made, and a link to it put in its place, here as the legs are sealed
    or as the render runs. The seal's path then still reaches the directory
    the lane made, but through a link, out of the root. Each check of the
    name walks it again from the root through no link, as the making did,
    so the seal is refused and nothing more is written into it. Before
    this, the check looked through the link, and the seal was completed,
    manifest and all, out of the root."""
    root = tmp_path / "root"
    seal = root / "a" / "b" / "dfr-seal"
    seal.parent.mkdir(parents=True)
    moved = tmp_path / "moved"
    stub = _stub_validator(tmp_path / "unit")

    def swap():
        (root / "a").rename(moved)
        (root / "a").symlink_to(moved, target_is_directory=True)

    def swapping_legs(*, corpus_checkout, source_head, corpus_root, runner):
        records = _stub_leg_records(corpus_root, PRODUCT_MODULE_TEXT,
                                    _validator_head(stub))
        if when == "as-the-legs-are-sealed":
            swap()
        return records

    def swapping_render(seal_root, *, source_head, source_committed_at,
                        container=None):
        if when == "as-the-render-runs":
            swap()
        return dict(STUB_PRECHECK)

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, seal_within=root, resolve_validator=lambda: stub,
              seal_legs=swapping_legs, precheck_render=swapping_render)
    what, after = (("corpus", "it was replaced after the lane made it")
                   if when == "as-the-legs-are-sealed"
                   else ("manifest", "sealed code ran inside it"))
    assert str(refused.value) == (
        f"the seal directory is no longer the one the lane created: {after}, "
        f"and the {what} is never written anywhere else")
    made = moved / "b" / seal.name
    assert made.is_dir()
    assert not (made / lane.SEAL_MANIFEST_NAME).exists()
    if when == "as-the-legs-are-sealed":
        assert not (made / lane.SEAL_CORPUS_RELPATH / "docs").exists()


@pytest.mark.parametrize("replacement", ["a-copy-in-its-place",
                                         "a-directory-of-its-own"])
def test_the_render_is_handed_the_directory_the_lane_made_not_its_name(
        corpus, tmp_path, monkeypatch, replacement):
    """THE RENDER RUNS FROM THE DIRECTORY THE LANE MADE (Copilot, PR #1185).
    The validator's probe is sealed code, run with the seal writable before
    the render, so the seal's name may lead somewhere else by the time the
    render runs. The render is handed the directory the lane holds, as the
    probe is, never the name. Here the seal is moved aside once the recipe
    is written, and a copy of it, or a directory of its own, is put at its
    name. The render still runs from the directory the lane made, and the
    seal is refused before its manifest, since its name no longer leads
    there."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"
    write_recipe = lane._write_new_recipe
    ran_in: list = []

    def writing_then_swapping(held, text, **kw):
        write_recipe(held, text, **kw)
        seal.rename(moved)
        if replacement == "a-copy-in-its-place":
            shutil.copytree(moved, seal)
        else:
            seal.mkdir()

    def recording(seal_root, *, source_head, source_committed_at,
                  container=None):
        # The first thing the real render does with what it is handed.
        ran_in.append(_identity(Path(seal_root).resolve()))
        return dict(STUB_PRECHECK)

    monkeypatch.setattr(lane, "_write_new_recipe", writing_then_swapping)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, precheck_render=recording)
    assert ran_in == [_identity(moved)]
    assert str(refused.value) == (
        "the seal directory is no longer the one the lane created: sealed "
        "code ran inside it, and the manifest is never written anywhere else")
    assert not (moved / lane.SEAL_MANIFEST_NAME).exists()
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("replacement", ["a-link-to-the-moved-seal",
                                         "a-copy-in-its-place"])
def test_a_seal_directory_swapped_as_its_manifest_is_written_is_not_published(
        corpus, tmp_path, monkeypatch, replacement):
    """THE NAME IS HELD ONCE MORE AFTER THE MANIFEST (Copilot, PR #1185). The
    manifest is the seal's publication marker, and once the lane records the
    seal sealed, the workflow uploads whatever the seal's name leads to. A
    name swapped while the manifest was written would publish something
    else. So the name is held to the directory once more after the write. A
    seal whose name no longer leads there is refused, and its manifest is
    withdrawn from the directory the lane made, through its handle. Here the
    seal is moved aside as the manifest's write returns, and a link to it,
    or a copy of it, is put at its name."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"
    write_manifest = lane._write_new_manifest

    def writing_then_swapping(held, text, **kw):
        write_manifest(held, text, **kw)
        seal.rename(moved)
        if replacement == "a-link-to-the-moved-seal":
            seal.symlink_to(moved, target_is_directory=True)
        else:
            shutil.copytree(moved, seal)

    monkeypatch.setattr(lane, "_write_new_manifest", writing_then_swapping)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal)
    assert not (moved / lane.SEAL_MANIFEST_NAME).exists()
    assert str(refused.value) == (
        "the seal directory is no longer the one the lane created: it was "
        "replaced as its manifest was written, so the seal is not published, "
        "and its manifest is withdrawn")


def test_a_confined_seal_is_never_made_by_its_path_alone(corpus, tmp_path,
                                                          monkeypatch):
    """A PLATFORM THAT HOLDS NO HANDLE MAKES NO CONFINED SEAL (Copilot, PR
    #1185). Where the platform opens nothing relative to a handle, the seal
    directory could only be made, written and checked by its path. A
    directory on its way replaced after `--seal-out` was checked would then
    redirect the whole writable tree, and a directory swapped in at its name
    would be taken for the one made. So a seal confined to a root, as `main`
    confines it to `--repo-root`, is refused there before anything is made.
    A direct call that confines nothing still makes its seal by the path, as
    the manifest's write always has where no handle can be opened."""
    root = tmp_path / "root"
    root.mkdir()
    seal = root / "dfr-seal"
    monkeypatch.setattr(lane, "_DIR_FD", False)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, seal_within=root)
    assert not os.path.lexists(seal)
    assert str(refused.value) == (
        f"the seal directory {seal} cannot be made here: this platform opens "
        f"nothing relative to a handle, and a seal confined to {root} is "
        "never made, written or checked by its path alone")
    free = tmp_path / "free"
    _seal(corpus, free)
    assert (free / lane.SEAL_MANIFEST_NAME).is_file()


def test_a_confined_seal_is_never_written_by_its_path(corpus, tmp_path,
                                                       monkeypatch):
    """NOR ONE THAT NAMES NO PATH THROUGH A HANDLE (Copilot, PR #1185). A
    platform can open a directory relative to a handle and still name no
    path through one (no `/proc/self/fd`). The seal would then be written,
    indexed and counted through its name, which sealed code may swap, and
    the handle would guard only the making. So a seal confined to a root is
    refused there too, before anything is made. A direct call that confines
    nothing still writes its seal through the name, as before. Here the
    handles' path names nothing (`_HANDLE_PATHS`)."""
    root = tmp_path / "root"
    root.mkdir()
    seal = root / "dfr-seal"
    monkeypatch.setattr(lane, "_HANDLE_PATHS", tmp_path / "no-handle-paths")
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, seal_within=root)
    assert not os.path.lexists(seal)
    assert str(refused.value) == (
        f"the seal directory {seal} cannot be made here: this platform names "
        f"no path through a handle, and a seal confined to {root} is never "
        "written or read by its path alone")
    free = tmp_path / "free"
    _seal(corpus, free)
    assert (free / lane.SEAL_MANIFEST_NAME).is_file()


@pytest.mark.parametrize("path", [path for path in SERVE_ONLY
                                  if not path.endswith("/")])
def test_a_corpus_without_a_serve_unit_file_is_refused(corpus, tmp_path,
                                                       path):
    """THE SEAL REFUSES FIRST WHAT THE INTAKE REFUSES (#1164). Two files of the
    serve unit sit inside directories the corpus archive names whole
    (`contracts`, `docs`), so the archive cannot promise them. A corpus that
    lacks one is refused, naming it, and no manifest is written."""
    _git(corpus, "rm", "--quiet", path)
    _git(corpus, "commit", "--quiet", "-m", f"drop {path}")
    seal = tmp_path / "seal"
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal)
    assert str(refused.value) == (
        f"the sealed corpus does not carry {lane.SEAL_CORPUS_RELPATH}/{path}, "
        "which the served image's recipe copies — the image the child builds "
        "could not start")
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("path", [path for path in SERVE_UNIT
                                  if not path.endswith("/")])
def test_a_serve_unit_file_that_is_a_directory_is_refused(corpus, tmp_path,
                                                          path):
    """A FILE OF THE UNIT MUST BE A FILE (Copilot, PR #1179). A directory at a
    file's path satisfies the corpus archive's pathspec, which names the path
    and whatever is under it. It satisfies neither the recipe, which copies a
    file there, nor the intake, which requires the file itself. So the seal
    checks every path of the unit its archive carries as the kind the unit
    names it, and refuses a directory at a file's path, naming it, before any
    manifest is written."""
    target = corpus / path
    _git(corpus, "rm", "--quiet", path)
    target.mkdir(parents=True)
    (target / "planted.py").write_text("# a directory, not the file\n",
                                       encoding="utf-8")
    _git(corpus, "add", "-A")
    _git(corpus, "commit", "--quiet", "-m", f"a directory at {path}")
    seal = tmp_path / "seal"
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal)
    assert str(refused.value) == (
        f"the sealed corpus does not carry {lane.SEAL_CORPUS_RELPATH}/{path}, "
        "which the served image's recipe copies — the image the child builds "
        "could not start")
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("path", [path for path in SERVE_UNIT
                                  if path.startswith("scripts/")])
def test_a_corpus_without_a_serve_unit_script_fails_its_archive(corpus,
                                                                tmp_path,
                                                                path):
    """Every script of the serve unit, the two packages included, is a
    pathspec of the corpus archive in its own right, so `git archive` refuses
    a corpus that lacks one, naming it, before anything is sealed. (A
    directory at one of their paths passes the archive, and the seal's own
    check refuses it, above. The legs are sealed whole by the leg sealer.)"""
    _git(corpus, "rm", "-r", "--quiet", path.rstrip("/"))
    _git(corpus, "commit", "--quiet", "-m", f"drop {path}")
    seal = tmp_path / "seal"
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal)
    reason = str(refused.value)
    assert reason.startswith("git archive failed at "), reason
    assert path.rstrip("/") in reason
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


# ---------------------------------------------------------------------------
# the child's intake check (S3's reference implementation)
# ---------------------------------------------------------------------------

def test_a_good_seal_verifies(corpus, tmp_path):
    seal = tmp_path / "seal"
    head = _git(corpus, "rev-parse", "HEAD")
    _seal(corpus, seal)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


def test_verify_reports_an_absent_required_path(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = sorted(manifest["files"])[0]
    (seal / victim).unlink()
    problems = lane.verify_seal(seal)
    assert any(victim in problem and "absent" in problem for problem in problems)


def test_verify_reports_a_tampered_file(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = next(key for key in sorted(manifest["files"])
                  if key.endswith(".md"))
    (seal / victim).write_text("tampered\n", encoding="utf-8")
    assert any("sha256 mismatch" in problem and victim in problem
               for problem in lane.verify_seal(seal))


# ---------------------------------------------------------------------------
# a tampered `files` index cannot walk `verify_seal` outside the seal
# (Copilot, PR #648). Every case here has an attacker who ALSO recomputes
# `tree_digest` over the tampered index — matching what a real forger would
# do, since `TREE_DIGEST_SPEC` is public — so a passing digest is never the
# thing standing between the seal and the escape; `_contained_relpath` is.
# ---------------------------------------------------------------------------

def test_verify_refuses_a_files_key_that_escapes_the_seal(corpus, tmp_path):
    """A `..` component reaching OUTSIDE the seal, with the outside file
    present and `tree_digest` recomputed to match, is refused before any join
    or open — so the outside file's contents are never in a `sha256 mismatch`
    or any other problem string."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    outside = tmp_path / "escape.txt"
    outside.write_text("stolen\n", encoding="utf-8")
    manifest["files"]["../escape.txt"] = lane.file_sha256(outside)
    manifest["tree_digest"] = lane.tree_digest(manifest["files"])
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert any("../escape.txt" in problem for problem in problems)
    assert not any("stolen" in problem for problem in problems)


def test_verify_refuses_an_absolute_files_key(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = sorted(manifest["files"])[0]
    manifest["files"]["/etc/passwd"] = manifest["files"].pop(victim)
    manifest["tree_digest"] = lane.tree_digest(manifest["files"])
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert any("absolute path" in problem and "/etc/passwd" in problem
               for problem in problems)


@pytest.mark.parametrize("extra", [
    "openxFactory/unindexed.txt",
    "openxFactory/openXdox/code/src/openxdox/unindexed.py",
    "openxFactory/openDox/code/src/json.py"],
    ids=["beside-the-corpus", "a-module-in-a-leg", "a-stdlib-shadow-in-a-leg"])
def test_verify_refuses_a_file_the_index_does_not_name(corpus, tmp_path,
                                                        extra):
    """`files` says what may exist, not only what must (Copilot, PR #1166).
    The child renders, validates and bakes out of the seal, so an unindexed
    file is bytes the digest never covered, and one under a leg's `src/`
    would be importable, here even shadowing a standard module."""
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    target = seal / extra
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("extra\n", encoding="utf-8")
    assert lane.verify_seal(seal) == [
        f"the seal holds {extra}, which its index does not name"]


def test_verify_bounds_the_unindexed_files_it_names(corpus, tmp_path):
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    for n in range(12):
        (seal / lane.SEAL_CORPUS_RELPATH / f"extra-{n:02d}.txt").write_text(
            "extra\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert len(problems) == 11
    assert problems[-1] == "... and 2 more the index does not name"


def test_verify_refuses_a_symlinked_entry(corpus, tmp_path):
    """The manifest still names a real path INSIDE the seal, but that path is
    now a symlink to a file outside — no `..`, no absolute path, nothing the
    literal-component checks alone would catch."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    victim = next(key for key in sorted(manifest["files"])
                  if key.endswith(".md"))
    target = seal / victim
    outside = tmp_path / "outside.md"
    outside.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
    target.unlink()
    target.symlink_to(outside)
    problems = lane.verify_seal(seal)
    assert any("symlinked path" in problem and victim in problem
               for problem in problems)


def test_verify_refuses_a_path_through_a_symlinked_directory(corpus, tmp_path):
    """`..`-free: the manifest key is `linked_dir/secret.txt`, a plain
    descendant-looking relative path. It only escapes because `linked_dir`
    itself — a directory ENTRY under the seal — is a symlink to somewhere
    else, so every component of the walk (not just the leaf) must be
    checked."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    outside_dir = tmp_path / "outside_dir"
    outside_dir.mkdir()
    secret = outside_dir / "secret.txt"
    secret.write_text("stolen\n", encoding="utf-8")
    linked = seal / "linked_dir"
    linked.symlink_to(outside_dir)
    manifest["files"]["linked_dir/secret.txt"] = lane.file_sha256(secret)
    manifest["tree_digest"] = lane.tree_digest(manifest["files"])
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert any("linked_dir/secret.txt" in problem for problem in problems)
    assert not any("stolen" in problem for problem in problems)


def test_verify_reports_a_digest_that_does_not_recompute(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["tree_digest"] = "0" * 64
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert any("tree_digest mismatch" in problem
               for problem in lane.verify_seal(seal))


def test_verify_reports_a_seal_that_is_not_the_dispatch(corpus, tmp_path):
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    problems = lane.verify_seal(seal, correlation_id="dashboard-refresh-9-9",
                                corpus_revision="a" * 40,
                                recipe_revision="b" * 40)
    assert len(problems) == 3
    assert any("correlation id mismatch" in problem for problem in problems)
    assert any("corpus revision mismatch" in problem for problem in problems)
    assert any("recipe revision mismatch" in problem for problem in problems)


def test_the_digest_check_is_not_suppressed_by_an_unrelated_problem(corpus, tmp_path):
    """`verify_seal` reports ALL of what is wrong in one pass, so an unrelated
    manifest problem must not swallow the whole-tree disagreement — the most
    useful line in the list (Copilot round 2, PR #648)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["kind"] = "something-else"
    manifest["tree_digest"] = "0" * 64
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal, correlation_id="dashboard-refresh-9-9")
    assert any("manifest kind is" in problem for problem in problems)
    assert any("correlation id mismatch" in problem for problem in problems)
    assert any("tree_digest mismatch" in problem for problem in problems)


@pytest.mark.parametrize("text", ["", "not json", "[]", '{"kind": "other"}'])
def test_verify_refuses_a_malformed_manifest(tmp_path, text):
    seal = tmp_path / "seal"
    seal.mkdir()
    (seal / lane.SEAL_MANIFEST_NAME).write_text(text, encoding="utf-8")
    assert lane.verify_seal(seal) != []


def test_verify_refuses_a_schema_version_it_cannot_read(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["schema_version"] = "9.0.0"
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert any("schema_version" in problem for problem in lane.verify_seal(seal))


def test_verify_refuses_a_seal_without_the_validator_or_the_recipe(corpus, tmp_path):
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    validator_key = lane.SEAL_VALIDATOR_RELPATH
    manifest["files"].pop(validator_key)
    manifest["files"].pop(lane.SEAL_RECIPE_RELPATH)
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    problems = lane.verify_seal(seal)
    assert any(validator_key in problem and "could not run" in problem
               for problem in problems)
    assert any("build recipe" in problem for problem in problems)


def test_verify_refuses_the_1x_layout_that_sealed_the_validator_in_the_corpus(
        corpus, tmp_path):
    """A 1.x seal carried its validator INSIDE the corpus, at
    `openxFactory/scripts/validate-ideation-dashboard-contracts.py`, and
    declared no `validator_relpath`. The reference intake reads a 2.x seal
    only, and says which of the two it was handed: a validator at the old
    place satisfies nothing, and the old major refuses by name."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    # Rebuilt as a COHERENT 1.x seal: the script moved to the old place, the
    # `validator/` root gone, the index and the tree digest recomputed. So the
    # only thing wrong with it is the layout itself.
    old_place = f"{lane.SEAL_CORPUS_RELPATH}/{lane.VALIDATOR_SCRIPT_PATH}"
    (seal / old_place).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(seal / lane.SEAL_VALIDATOR_RELPATH), str(seal / old_place))
    shutil.rmtree(seal / lane.SEAL_VALIDATOR_ROOT)
    manifest["files"] = lane.seal_file_index(seal)
    manifest["tree_digest"] = lane.tree_digest(manifest["files"])
    for field in ("validator_relpath", "validator_revision",
                  "validator_schema_count", "validator_probe",
                  "render_entry", "render_legs", "precheck", "serve_entry",
                  "serve_unit", "validator_corpus_schemas"):
        del manifest[field]                         # 2.x-only fields
    manifest["schema_version"] = "1.0.0"
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    schemas = f"{lane.SEAL_VALIDATOR_ROOT}/{lane.VALIDATOR_SCHEMAS_PATH}/"
    assert lane.verify_seal(seal) == [
        "manifest schema_version '1.0.0' is not readable by this reader "
        f"({lane.SEAL_SCHEMA_VERSION})",
        f"validator_relpath is None, expected {lane.SEAL_VALIDATOR_RELPATH!r}",
        f"the seal does not carry {lane.SEAL_VALIDATOR_RELPATH} — strict "
        "validation could not run",
        f"the seal indexes no schema under {schemas} — strict validation "
        "could not run",
        f"validator_schema_count is None, but the seal indexes 0 schema(s) "
        f"under {schemas}",
        f"the seal does not carry {schemas}{lane.VALIDATOR_SNAPSHOT_SCHEMA}, "
        "the schema the child validates against",
        "validator_probe is None — the manifest does not record that the "
        f"sealed validator ran to a verdict ({VERDICT_PAIRS})",
        "validator_revision is None, expected a full commit revision",
        NO_CORPUS_SCHEMAS,
        f"render_entry is None, expected {lane.RENDER_ENTRY!r} — the child "
        "would have no renderer to run",
        "render_legs is None — the seal records no render unit, so the "
        "child's render would reach no product",
        f"serve_entry is None, expected {SERVE_ENTRY!r} — the image the child "
        "builds could not start",
        "serve_unit is None — the seal records no serve unit, so the image the "
        "child builds could not start",
    ]
    assert lane.SEAL_SCHEMA_VERSION.split(".", 1)[0] == "2"


# What the intake says of a seal that records nothing about where its
# validator's schemas came from (seal 2.2.0).
NO_CORPUS_SCHEMAS = (
    "validator_corpus_schemas is None — the manifest does not record which of "
    "the sealed validator's schemas came from the corpus")


def _rewrite_coherently(seal: Path, manifest: dict) -> None:
    """Rewrite `manifest.json` after a tamper, with the files index and the
    tree digest recomputed, so the only thing wrong is what the tamper did."""
    manifest["files"] = lane.seal_file_index(seal)
    manifest["tree_digest"] = lane.tree_digest(manifest["files"])
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@pytest.mark.parametrize("tamper", ["schemas-removed", "count-disagrees",
                                    "snapshot-schema-renamed",
                                    "probe-unavailable"])
def test_verify_refuses_a_validator_unit_that_is_not_whole(corpus, tmp_path,
                                                           tamper):
    """The intake requires the UNIT, not only its script (Copilot review of
    #1162). The script alone exits 2 before it reads a snapshot. Each tamper is
    made COHERENT, with the index and the tree digest recomputed, so a digest
    check alone would pass it. The problems asserted are exactly what the
    tamper did."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert lane.verify_seal(seal) == []
    schemas_dir = seal / lane.SEAL_VALIDATOR_ROOT / lane.VALIDATOR_SCHEMAS_PATH
    if tamper == "schemas-removed":
        shutil.rmtree(schemas_dir)
    elif tamper == "count-disagrees":
        manifest["validator_schema_count"] = 5
    elif tamper == "snapshot-schema-renamed":
        (schemas_dir / lane.VALIDATOR_SNAPSHOT_SCHEMA).rename(
            schemas_dir / "some-other.schema.yaml")
    else:
        manifest["validator_probe"] = dict(
            manifest["validator_probe"],
            outcome=snapshot_mod.VALIDATOR_UNAVAILABLE)
    _rewrite_coherently(seal, manifest)
    schemas = f"{lane.SEAL_VALIDATOR_ROOT}/{lane.VALIDATOR_SCHEMAS_PATH}/"
    no_snapshot_schema = (
        f"the seal does not carry {schemas}{lane.VALIDATOR_SNAPSHOT_SCHEMA}, "
        "the schema the child validates against")
    expected = {
        "schemas-removed": [
            f"the seal indexes no schema under {schemas} — strict validation "
            "could not run",
            f"validator_schema_count is 1, but the seal indexes 0 schema(s) "
            f"under {schemas}",
            no_snapshot_schema],
        "count-disagrees": [
            f"validator_schema_count is 5, but the seal indexes 1 schema(s) "
            f"under {schemas}"],
        "snapshot-schema-renamed": [no_snapshot_schema],
        "probe-unavailable": [
            f"validator_probe is {manifest['validator_probe']!r} — the "
            "manifest does not record that the sealed validator ran to a "
            f"verdict ({VERDICT_PAIRS})"],
    }[tamper]
    assert lane.verify_seal(seal) == expected


@pytest.mark.parametrize("outcome, returncode, pairs", [
    ("validated", 0, True),
    ("not-conformant", 1, True),
    ("validated", 1, False),
    ("not-conformant", 0, False),
    ("validated", 2, False),
    ("validated", False, False),
    ("not-conformant", True, False),
    ("validated", 0.0, False),
    ("validated", "0", False),
    ("validated", _ABSENT, False),
    ("validator-unavailable", 2, False),
], ids=["validated-0", "not-conformant-1", "validated-1", "not-conformant-0",
        "validated-2", "a-bool-false", "a-bool-true", "a-float", "a-string",
        "no-returncode", "unavailable"])
def test_verify_holds_the_probe_verdict_to_its_exit_code(corpus, tmp_path,
                                                         outcome, returncode,
                                                         pairs):
    """A VERDICT AND THE EXIT CODE IT IS READ FROM ARE ONE FACT (Copilot,
    opensoft/xFactory PR #526, mirrored here). The validator exits 0 when it
    validates and 1 when it finds, and the product reads its verdict on a
    readable document from that number alone; the probe is the parent's own
    JSON. So the intake requires the pair, as a real `int`, because
    `True == 1` and `False == 0`. A record that pairs them otherwise, a
    harness failure recorded as `validated`, say, was not reached by the
    validator."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    probe = {"kind": lane.VALIDATOR_PROBE["kind"], "outcome": outcome}
    if returncode is not _ABSENT:
        probe["returncode"] = returncode
    manifest["validator_probe"] = probe
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == ([] if pairs else [
        f"validator_probe is {probe!r} — the manifest does not record that "
        f"the sealed validator ran to a verdict ({VERDICT_PAIRS})"])


@pytest.mark.parametrize("returncode, pairs", [
    (0, True), (1, False), (2, False), (False, False), (0.0, False),
    ("0", False), (_ABSENT, False),
], ids=["0", "1", "2", "a-bool", "a-float", "a-string", "no-returncode"])
def test_verify_holds_the_precheck_pass_to_its_exit_code(corpus, tmp_path,
                                                         returncode, pairs):
    """The pre-dispatch render's pass is `validated` beside exit 0, as a real
    `int`, and nothing else: the render's output is parsed before a copy of
    it is judged, so the product reads a pass from that number alone
    (Copilot, opensoft/xFactory PR #526, mirrored here)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    record = {key: value for key, value in STUB_PRECHECK.items()
              if key != "returncode"}
    if returncode is not _ABSENT:
        record["returncode"] = returncode
    record = dict(sorted(record.items()))     # as the manifest is written
    manifest["precheck"] = record
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == ([] if pairs else [
        f"precheck is {record!r} — the manifest does not record that the "
        "sealed render passed its own validator under --strict (validated "
        "with exit 0)"])


@pytest.mark.parametrize("recorded", [None, "abc1234", "", 40],
                         ids=["null", "abbreviated", "empty", "not-a-string"])
def test_verify_refuses_a_validator_revision_that_is_not_a_full_revision(
        corpus, tmp_path, recorded):
    """REQUIRED, NOT OPTIONAL (Copilot, PR #1166). Every 2.1 seal carries the
    openXdox code leg, and the validator's revision is what holds the sealed
    validator to that leg. A null used to verify, as the record of a unit
    with no product tree, so a tampered manifest could carry a validator
    copied from another product commit, null this one field, and pass. A
    null is refused like every other value that is not a full revision, and
    the seal refuses to write one."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert lane.verify_seal(seal) == []
    manifest["validator_revision"] = recorded
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == [
        f"validator_revision is {recorded!r}, expected a full commit revision"]


# ---------------------------------------------------------------------------
# the seal speaks git, and only git, beside one run of the sealed validator
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("resolve_validator", [_STUB, None],
                         ids=["stub-unit", "the-real-resolver"])
def test_the_seal_speaks_only_git_and_never_builds_or_pushes(corpus, tmp_path,
                                                             resolve_validator):
    """Every shell-out through the seal's runner is `git`: the archive, the two
    revision reads, and the product revision the sealed validator came from
    with the status read that holds its unit to committed bytes, for the
    stand-in unit's committed tree and the real resolver's product alike.
    The one run of the sealed validator is not a
    runner call; `test_the_one_run_is_of_the_sealed_copy_over_the_probe` pins
    it. The legs' own git reads are pinned over real submodules in
    `test_the_leg_sealer_speaks_only_git`."""
    runner = RecordingRunner()
    _seal(corpus, tmp_path / "seal", runner=runner,
          resolve_validator=resolve_validator)
    assert runner.calls, "the seal made no subprocess call at all"
    for argv in runner.calls:
        assert argv[0] == "git", argv
    verbs = {_verb(argv) for argv in runner.calls}
    assert verbs <= {"archive", "show", "rev-parse", "status", "diff"}, verbs
    _assert_exact_reads(runner)
    assert not hasattr(lane, "build_and_push")


# ---------------------------------------------------------------------------
# the CLI phase — the dispatch gate, and a refusal that never fails the run
# ---------------------------------------------------------------------------

def _cli_seal(tmp_path: Path) -> Path:
    """Where the CLI tests name the seal: inside the checkout the lane runs
    over, as the workflow's own `--seal-out dfr-seal` does (#1182)."""
    return tmp_path / "aggregation" / "dfr-seal"


def _seal_cli(tmp_path: Path, corpus: Path, *extra: str,
              decision: dict | None = None) -> dict | None:
    root = tmp_path / "aggregation"
    (root).mkdir(exist_ok=True)
    if decision is not None:
        (root / "dfr-decision.json").write_text(
            json.dumps(decision), encoding="utf-8")
    lane.main(["--repo-root", str(root), "--phase", "seal",
               "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
               "--decision-in", str(root / "dfr-decision.json"),
               "--seal-out", str(_cli_seal(tmp_path)),
               "--seal-result-out", str(root / "seal-result.json"),
               "--correlation-id", CORRELATION, *extra])
    try:
        return json.loads((root / "seal-result.json").read_text(encoding="utf-8"))
    except OSError:
        return None


def test_the_seal_phase_exists_and_is_not_a_build_phase(tmp_path):
    """`--phase seal` is the ONE materialization phase this module offers, and
    `--phase build` — the retired raw-clone recipe — stays refused."""
    with pytest.raises(SystemExit):
        lane.main(["--repo-root", str(tmp_path), "--phase", "build"])


def test_the_seal_phase_refuses_an_absent_decision_without_failing_the_run(
        corpus, tmp_path):
    result = _seal_cli(tmp_path, corpus)          # no decision file written
    assert result["sealed"] is False
    assert "no usable parent decision" in result["reason"]
    assert not (_cli_seal(tmp_path) / lane.SEAL_MANIFEST_NAME).exists()


def test_the_seal_phase_refuses_a_no_change_decision(corpus, tmp_path):
    result = _seal_cli(tmp_path, corpus,
                       decision={"build": False, "outcome": "no_change"})
    assert result["sealed"] is False
    assert "nothing to seal" in result["reason"]


def test_the_seal_phase_writes_the_dispatch_gate(corpus, tmp_path, monkeypatch):
    head = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "gh_read_file",
                        lambda *a, **kw: RECIPE_TEXT)
    # The CLI takes the module's own leg sealer and pre-dispatch render, so the
    # stand-ins are put where it looks for them.
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is True
    assert result["reason"] is None
    assert result["strict_failed"] is False
    assert result["detail"] == []
    assert result["artifact_name"] == f"dashboard-image-source-{CORRELATION}"
    assert result["source_head"] == head
    assert result["corpus_revision"] == head
    assert result["recipe_revision"] == RECIPE_REV
    assert _instant(result["source_committed_at"]) == _instant(COMMITTED_AT)
    assert is_rfc3339_datetime(result["source_committed_at"])
    assert len(result["tree_digest"]) == 64
    assert result["file_count"] > 0 and result["total_bytes"] > 0
    manifest = lane.read_seal_manifest(_cli_seal(tmp_path))
    assert manifest["tree_digest"] == result["tree_digest"]
    assert lane.verify_seal(_cli_seal(tmp_path), correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


def _a_directory_holding_links_out(where: Path, workspace_file: Path,
                                   workspace_dir: Path) -> None:
    """A real directory at `where`, holding a link to a workspace file, a link
    to a workspace directory, and a tree of its own: the lane removes all of
    it and follows none of it."""
    where.mkdir()
    (where / "to-a-file").symlink_to(workspace_file)
    (where / "to-a-directory").symlink_to(workspace_dir,
                                          target_is_directory=True)
    (where / "nested").mkdir()
    (where / "nested" / "planted.txt").write_text("planted\n",
                                                  encoding="utf-8")


def _a_workspace(root: Path) -> tuple[Path, Path]:
    """A workspace file and a workspace directory holding one, which nothing
    the seal phase does may touch."""
    root.mkdir(parents=True, exist_ok=True)
    workspace_file = root / "some-workspace-file.yml"
    workspace_file.write_text("untouched\n", encoding="utf-8")
    workspace_dir = root / "some-workspace-dir"
    workspace_dir.mkdir()
    (workspace_dir / "kept.txt").write_text("untouched\n", encoding="utf-8")
    return workspace_file, workspace_dir


@pytest.mark.parametrize("planted", ["a-link-to-a-workspace-file",
                                     "a-file-that-says-sealed",
                                     "a-directory-holding-links-out"])
def test_a_seal_result_sealed_code_planted_refuses_the_seal(
        corpus, tmp_path, monkeypatch, planted):
    """The seal result sits outside the seal, at the fixed path the workflow
    gates the dispatch on, and sealed code runs before it is written. An
    entry found there afterwards was made by that code. It is never written
    through: the seal is refused, and the lane's own result replaces it
    (Copilot, PR #1166). A real DIRECTORY there is removed too, with
    everything under it and without following a link inside it, so the
    record step reads the refusal rather than falling back to `unknown`
    (Copilot, PR #1166, the review of 2c4520e7)."""
    head = _git(corpus, "rev-parse", "HEAD")
    workspace_file, workspace_dir = _a_workspace(tmp_path / "aggregation")
    result_path = tmp_path / "aggregation" / "seal-result.json"

    def planting(seal_root, *, source_head, source_committed_at,
                 container=None):
        if planted == "a-link-to-a-workspace-file":
            result_path.symlink_to(workspace_file)
        elif planted == "a-file-that-says-sealed":
            result_path.write_text('{"sealed": true}\n', encoding="utf-8")
        else:
            _a_directory_holding_links_out(result_path, workspace_file,
                                           workspace_dir)
        return dict(STUB_PRECHECK)

    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", planting)
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert not result_path.is_symlink() and result_path.is_file()
    assert result["sealed"] is False
    assert result["reason"] == lane.SEAL_RESULT_PLANTED
    assert result["strict_failed"] is False
    assert workspace_file.read_text(encoding="utf-8") == "untouched\n"
    assert (workspace_dir / "kept.txt").read_text(encoding="utf-8") == \
        "untouched\n"


@pytest.mark.parametrize("stale", ["a-file", "a-link-to-a-workspace-file",
                                   "a-directory-holding-links-out"])
def test_a_stale_seal_result_is_cleared_before_the_seal_runs(
        corpus, tmp_path, monkeypatch, stale):
    """What sits at the result path BEFORE the seal starts is an earlier
    run's, not sealed code's. It is removed without being followed, a
    directory with everything under it, and the seal proceeds. A directory
    left there used to survive the clearing and then read as planted, and
    its result could not be written at all."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    workspace_file, workspace_dir = _a_workspace(root)
    result_path = root / "seal-result.json"
    if stale == "a-file":
        result_path.write_text('{"sealed": false}\n', encoding="utf-8")
    elif stale == "a-link-to-a-workspace-file":
        result_path.symlink_to(workspace_file)
    else:
        _a_directory_holding_links_out(result_path, workspace_file,
                                       workspace_dir)
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is True
    assert not result_path.is_symlink() and result_path.is_file()
    assert workspace_file.read_text(encoding="utf-8") == "untouched\n"
    assert (workspace_dir / "kept.txt").read_text(encoding="utf-8") == \
        "untouched\n"


@pytest.mark.parametrize("where", ["beside-the-checkout", "climbing-out-of-it",
                                   "through-a-link-inside-it",
                                   "not-a-json-file", "the-checkout-itself",
                                   "in-a-directory-that-does-not-exist"])
def test_a_seal_result_path_the_lane_may_not_clear_is_refused(
        corpus, tmp_path, monkeypatch, capsys, where):
    """The seal result is written only inside the checkout the lane runs
    over, the one place the record step reads it (`read_strict_verdict`),
    and only at a path naming a `.json` file. The lane REMOVES whatever sits
    at that path before it writes, a directory with everything under it, so
    a path out of the checkout, by itself, by `..` or through a link, or one
    that could name the checkout or a real directory in it, is refused
    before anything is removed. Nothing is sealed, since a seal whose result
    cannot be written could never be dispatched."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    victim = outside / "seal-result.json"
    victim.write_text("untouched\n", encoding="utf-8")
    kept = root / "health"
    kept.mkdir()
    (kept / "report.md").write_text("untouched\n", encoding="utf-8")
    if where == "through-a-link-inside-it":
        (root / "linked").symlink_to(outside, target_is_directory=True)
    given = {
        "beside-the-checkout": str(victim),
        "climbing-out-of-it": str(root / ".." / "outside" / "seal-result.json"),
        "through-a-link-inside-it": str(root / "linked" / "seal-result.json"),
        "not-a-json-file": str(kept),
        "the-checkout-itself": str(root),
        "in-a-directory-that-does-not-exist": str(root / "absent"
                                                  / "seal-result.json"),
    }[where]
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    code = lane.main(["--repo-root", str(root), "--phase", "seal",
                      "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
                      "--decision-in", str(root / "dfr-decision.json"),
                      "--seal-out", str(root / "dfr-seal"),
                      "--seal-result-out", given,
                      "--correlation-id", CORRELATION])
    # No result of the lane's own is written, so the step fails.
    assert code == lane.SEAL_RESULT_UNWRITTEN_EXIT
    assert victim.read_text(encoding="utf-8") == "untouched\n"
    assert (kept / "report.md").read_text(encoding="utf-8") == "untouched\n"
    assert (root / "dfr-decision.json").is_file()
    assert not os.path.lexists(root / "dfr-seal")
    said = capsys.readouterr().out
    assert "NOT SEALED" in said and "the seal result" in said


def _a_checkout_deciding_a_build(tmp_path: Path, corpus: Path) -> Path:
    root = tmp_path / "aggregation"
    root.mkdir()
    head = _git(corpus, "rev-parse", "HEAD")
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    return root


def _seal_phase(tmp_path: Path, corpus: Path, root: Path):
    return lane.main(["--repo-root", str(root), "--phase", "seal",
                      "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
                      "--decision-in", str(root / "dfr-decision.json"),
                      "--seal-out", str(root / "dfr-seal"),
                      "--seal-result-out", str(root / "seal-result.json"),
                      "--correlation-id", CORRELATION])


def test_a_seal_result_the_lane_cannot_write_fails_the_step(
        corpus, tmp_path, monkeypatch, capsys):
    """THE STEP FAILS WHEN THE LANE'S OWN RESULT CANNOT BE WRITTEN (Copilot,
    PR #1166). The workflow reads `sealed` from the seal result right after
    this phase, so a result the lane could not write cannot withhold the
    dispatch: whatever sits at its path is read in its place. Sealed code
    that plants a result saying `sealed: true`, and leaves it where the lane
    cannot remove it (a directory made read-only, stood in for here by a
    removal that fails), gets the plant refused and the phase's non-zero
    exit, which the step's `bash -e` stops on before `sealed` is read."""
    root = _a_checkout_deciding_a_build(tmp_path, corpus)
    result_path = root / "seal-result.json"
    planted = []
    clear = lane._clear_result_path

    def planting(seal_root, *, source_head, source_committed_at,
                 container=None):
        result_path.write_text(json.dumps({"sealed": True}), encoding="utf-8")
        planted.append(result_path)
        return dict(STUB_PRECHECK)

    def removing_until_planted(path, *, dir_fd=None):
        if planted:
            raise PermissionError(13, "Permission denied", os.fspath(path))
        return clear(path, dir_fd=dir_fd)

    monkeypatch.setattr(lane, "_clear_result_path", removing_until_planted)
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", planting)
    code = _seal_phase(tmp_path, corpus, root)
    assert planted, "the stand-in render never ran"
    assert code is not None and code != 0
    assert code == lane.SEAL_RESULT_UNWRITTEN_EXIT
    said = capsys.readouterr().out
    assert f"NOT SEALED — {lane.SEAL_RESULT_PLANTED}" in said
    assert "the seal result could not be written" in said
    # The plant is still there, and it is the step's failure, not the file,
    # that withholds the dispatch.
    assert json.loads(result_path.read_text(encoding="utf-8")) == \
        {"sealed": True}


def test_a_seal_result_path_the_lane_cannot_clear_seals_nothing(
        corpus, tmp_path, monkeypatch, capsys):
    """A result path the lane cannot clear before the seal starts is one it
    cannot write its own result at, and whatever sits there, a stale result
    saying `sealed: true` included, would be read in its place. So no sealed
    code runs, nothing is sealed, and the phase fails its step (Copilot,
    PR #1166)."""
    root = _a_checkout_deciding_a_build(tmp_path, corpus)
    stale = root / "seal-result.json"
    stale.write_text(json.dumps({"sealed": True}), encoding="utf-8")
    sealed = []

    def refusing_removal(path, *, dir_fd=None):
        raise PermissionError(13, "Permission denied", os.fspath(path))

    monkeypatch.setattr(lane, "_clear_result_path", refusing_removal)
    monkeypatch.setattr(lane, "seal_source", lambda **kw: sealed.append(kw))
    code = _seal_phase(tmp_path, corpus, root)
    assert sealed == [], "the seal ran although its result path held a stale result"
    assert code is not None and code != 0
    assert code == lane.SEAL_RESULT_UNWRITTEN_EXIT
    said = capsys.readouterr().out
    assert "NOT SEALED — the seal result's path could not be cleared" in said
    assert json.loads(stale.read_text(encoding="utf-8")) == {"sealed": True}


def test_a_result_directory_sealed_code_replaced_is_never_written_through(
        corpus, tmp_path, monkeypatch, capsys):
    """THE RESULT'S DIRECTORY IS HELD from before any sealed code runs
    (Copilot, PR #1166). Sealed code that moves the checkout aside and puts a
    link to another directory in its place gets nothing written, and nothing
    removed, through the link: every act at the result's path is relative to
    the directory the lane held. The lane's own result goes there, and it
    refuses the seal, since the path the workflow reads no longer leads to
    it."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "seal-result.json").write_text("untouched\n", encoding="utf-8")
    moved = tmp_path / "aggregation.moved"

    def replacing(seal_root, *, source_head, source_committed_at,
                  container=None):
        root.rename(moved)
        root.symlink_to(outside, target_is_directory=True)
        return dict(STUB_PRECHECK)

    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", replacing)
    lane.main(["--repo-root", str(root), "--phase", "seal",
               "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
               "--decision-in", str(root / "dfr-decision.json"),
               "--seal-out", str(root / "dfr-seal"),
               "--seal-result-out", str(root / "seal-result.json"),
               "--correlation-id", CORRELATION])
    assert (outside / "seal-result.json").read_text(encoding="utf-8") == \
        "untouched\n"
    assert sorted(path.name for path in outside.iterdir()) == \
        ["seal-result.json"]
    result = json.loads((moved / "seal-result.json").read_text(
        encoding="utf-8"))
    assert result["sealed"] is False
    assert result["reason"] == lane.SEAL_RESULT_DIRECTORY_REPLACED
    assert "NOT SEALED" in capsys.readouterr().out


def test_the_workflows_own_relative_spelling_seals(corpus, tmp_path,
                                                   monkeypatch):
    """The nightly runs the seal phase from the aggregation root with
    `--repo-root .`, and names the result and the seal relative to it. That
    spelling is inside the checkout, so holding the result's path there
    refuses nothing the workflow passes."""
    seal_step = _finalize_steps()[_step_index(_finalize_steps(),
                                              id="dfr-seal")]["run"]
    for spelling in ("--repo-root . --phase seal", "--seal-out dfr-seal",
                     "--seal-result-out dfr-seal-result.json",
                     "--decision-in dfr-decision.json"):
        assert spelling in seal_step, spelling
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    monkeypatch.chdir(root)
    # The spelling satisfies the rule `--seal-out` is held to (#1182): one
    # relative name inside the checkout, which no step before the seal step
    # makes or names, so the lane makes it fresh. The upload reads the same
    # name (`test_the_upload_names_the_artifact_the_child_downloads`).
    assert lane._seal_out_path("dfr-seal", Path(".").resolve()) == \
        (root / "dfr-seal").resolve()
    steps = _finalize_steps()
    for step in steps[:_step_index(steps, id="dfr-seal")]:
        assert not re.search(r"dfr-seal(?![-\w])", json.dumps(step)), \
            step.get("name")
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    lane.main(["--repo-root", ".", "--phase", "seal",
               "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
               "--decision-in", "dfr-decision.json",
               "--seal-out", "dfr-seal",
               "--seal-result-out", "dfr-seal-result.json",
               "--correlation-id", CORRELATION])
    result = json.loads((root / "dfr-seal-result.json").read_text(
        encoding="utf-8"))
    assert result["sealed"] is True, result["reason"]
    assert (root / "dfr-seal" / lane.SEAL_MANIFEST_NAME).is_file()


@pytest.mark.parametrize("where, clause", [
    ("beside-the-checkout", "is not inside the checkout"),
    ("climbing-out-of-it", "is not inside the checkout"),
    ("through-a-link-out-of-it", "is not inside the checkout"),
    ("through-a-link-inside-it", "leads through a link"),
    ("a-link-at-its-own-name", "leads through a link"),
    ("a-dangling-link-at-its-own-name", "leads through a link"),
    ("an-existing-directory-inside-it", "already exists"),
    ("in-a-directory-that-does-not-exist",
     "is in a directory that does not exist"),
])
def test_a_seal_out_the_lane_may_not_make_is_refused_before_anything_is_sealed(
        corpus, tmp_path, monkeypatch, capsys, where, clause):
    """--SEAL-OUT IS CONFINED TO THE CHECKOUT AND MADE FRESH (#1182). The seal
    directory is where sealed code runs with a writable tree, and where the
    workflow uploads from. So `--seal-out` must resolve inside `--repo-root`,
    through no link at any component, the last included, and name nothing
    that exists yet, in a directory that does. Anything else is refused
    before the seal starts: nothing of the seal runs, sealed code least of
    all, nothing is made or written anywhere, and the refusal is a recorded
    outcome, so the step succeeds and nothing is dispatched. Before this, a
    seal was made beside the checkout, out of it by `..` or through a link,
    in a directory it found, or in one `mkdir` made on the way."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    inside = root / "inside"
    inside.mkdir()
    if where == "through-a-link-out-of-it":
        (root / "linked").symlink_to(outside, target_is_directory=True)
    elif where == "through-a-link-inside-it":
        (root / "linked").symlink_to(inside, target_is_directory=True)
    elif where == "a-link-at-its-own-name":
        (root / "dfr-seal").symlink_to(inside, target_is_directory=True)
    elif where == "a-dangling-link-at-its-own-name":
        (root / "dfr-seal").symlink_to(root / "nowhere",
                                       target_is_directory=True)
    elif where == "an-existing-directory-inside-it":
        (root / "dfr-seal").mkdir()
    given = {
        "beside-the-checkout": str(tmp_path / "seal"),
        "climbing-out-of-it": str(root / ".." / "seal"),
        "through-a-link-out-of-it": str(root / "linked" / "dfr-seal"),
        "through-a-link-inside-it": str(root / "linked" / "dfr-seal"),
        "a-link-at-its-own-name": str(root / "dfr-seal"),
        "a-dangling-link-at-its-own-name": str(root / "dfr-seal"),
        "an-existing-directory-inside-it": str(root / "dfr-seal"),
        "in-a-directory-that-does-not-exist": str(root / "absent"
                                                  / "dfr-seal"),
    }[where]
    entered: list = []
    sealing = lane.seal_source

    def entering(**kw):
        entered.append(kw)
        return sealing(**kw)

    monkeypatch.setattr(lane, "seal_source", entering)
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    code = lane.main(["--repo-root", str(root), "--phase", "seal",
                      "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
                      "--decision-in", str(root / "dfr-decision.json"),
                      "--seal-out", given,
                      "--seal-result-out", str(root / "seal-result.json"),
                      "--correlation-id", CORRELATION])
    result = json.loads((root / "seal-result.json").read_text(
        encoding="utf-8"))
    assert result["sealed"] is False
    assert result["reason"].startswith(
        f"the seal cannot be made: --seal-out {given!r} {clause}"), \
        result["reason"]
    assert entered == []
    assert code is None
    assert sorted(path.name for path in outside.iterdir()) == []
    assert sorted(path.name for path in inside.iterdir()) == []
    assert not os.path.lexists(tmp_path / "seal")
    assert not os.path.lexists(root / "absent")
    assert "NOT SEALED — the seal cannot be made" in capsys.readouterr().out


@pytest.mark.parametrize("overlap", ["one-path-holding-a-seal",
                                     "one-free-path",
                                     "the-result-inside-the-seal",
                                     "the-seal-inside-the-result",
                                     "a-free-seal-inside-the-result",
                                     "a-link-to-the-result",
                                     "a-free-result-inside-an-existing-seal",
                                     "the-checkout-itself"])
def test_a_seal_out_that_overlaps_the_seal_result_is_never_touched(
        corpus, tmp_path, monkeypatch, capsys, overlap):
    """THE SEAL AND ITS RESULT ARE TWO PATHS (Copilot, PR #1185). The seal
    result's path is cleared before the seal runs, since whatever sits there
    is the lane's to remove (#1166). A `--seal-out` that is the same path,
    or holds it, or lies inside it, would have had an existing seal, or
    whatever it held, removed as a stale result, and the path then passed as
    fresh and been sealed into. So an overlap is found before anything is
    cleared, and on an overlap neither path is touched: nothing is removed,
    made, sealed or written, and the step fails, since the lane will not
    write its result at a path that is the seal's, or inside it, or holds
    it. A result written anyway would land inside an existing seal (Copilot,
    PR #1185, review 5331632101). The paths are compared as spelled and as
    resolved, so a `--seal-out` that is a link to the result's path overlaps
    it too, and the checkout itself overlaps every result path inside it. A
    `--seal-out` refused on its own keeps its own reason; a free one is
    refused for the overlap."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    if overlap in ("one-path-holding-a-seal", "one-free-path"):
        seal_out = result_out = root / "dfr-seal.json"
    elif overlap in ("the-result-inside-the-seal",
                     "a-free-result-inside-an-existing-seal"):
        seal_out = root / "dfr-seal"
        result_out = seal_out / "seal-result.json"
    elif overlap == "a-link-to-the-result":
        seal_out = root / "dfr-seal"
        result_out = root / "seal-result.json"
    elif overlap == "the-checkout-itself":
        seal_out = root
        result_out = root / "seal-result.json"
    else:
        result_out = root / "seal-result.json"
        seal_out = result_out / "dfr-seal"
    kept = seal_out / "kept.txt"
    free = overlap in ("one-free-path", "a-free-seal-inside-the-result")
    if overlap == "a-link-to-the-result":
        result_out.mkdir()
        (result_out / "kept.txt").write_text("an earlier seal\n",
                                             encoding="utf-8")
        seal_out.symlink_to(result_out, target_is_directory=True)
    elif not free:
        seal_out.mkdir(parents=True, exist_ok=overlap == "the-checkout-itself")
        kept.write_text("an earlier seal\n", encoding="utf-8")
    if overlap == "the-result-inside-the-seal":
        result_out.write_text('{"stale": true}\n', encoding="utf-8")
    if overlap == "a-free-seal-inside-the-result":
        result_out.mkdir()
    before = _tree_state(root)
    entered: list = []
    sealing = lane.seal_source

    def entering(**kw):
        entered.append(kw)
        return sealing(**kw)

    monkeypatch.setattr(lane, "seal_source", entering)
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    code = lane.main(["--repo-root", str(root), "--phase", "seal",
                      "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
                      "--decision-in", str(root / "dfr-decision.json"),
                      "--seal-out", str(seal_out),
                      "--seal-result-out", str(result_out),
                      "--correlation-id", CORRELATION])
    if not free:
        assert kept.read_text(encoding="utf-8") == "an earlier seal\n"
    if overlap == "the-result-inside-the-seal":
        assert result_out.read_text(encoding="utf-8") == '{"stale": true}\n'
    if overlap == "a-free-seal-inside-the-result":
        assert result_out.is_dir()
    assert entered == []
    if free:
        reason = (f"the seal cannot be made: --seal-out {str(seal_out)!r} and "
                  f"--seal-result-out {str(result_out)!r} overlap, and "
                  "neither is touched: the seal and its result are two "
                  "paths, never one inside the other")
    elif overlap == "a-link-to-the-result":
        reason = (f"the seal cannot be made: --seal-out {str(seal_out)!r} "
                  f"leads through a link (to {result_out}), and the seal is "
                  "never made through one")
    else:
        reason = (f"the seal cannot be made: --seal-out {str(seal_out)!r} "
                  "already exists, and the lane makes the seal only in a "
                  "directory it creates itself")
    assert f"NOT SEALED — {reason}" in capsys.readouterr().out
    assert _tree_state(root) == before
    assert code == lane.SEAL_RESULT_UNWRITTEN_EXIT


def test_a_link_put_on_the_seal_out_path_after_its_check_is_never_made_through(
        corpus, tmp_path, monkeypatch):
    """THE MAKING HOLDS THE RULE TOO (#1182). `--seal-out` is checked before
    the seal starts, and the seal directory is made later, once the validator
    is resolved. The lane makes it by walking from `--repo-root`, opening
    each directory on the way relative to the one before and without
    following a link, so a directory on the way swapped for a link in
    between, here as the validator is resolved, refuses the seal, and
    nothing is made where the link points."""
    head = _git(corpus, "rev-parse", "HEAD")
    root = tmp_path / "aggregation"
    root.mkdir()
    (root / "dfr-decision.json").write_text(json.dumps(_decision(head)),
                                            encoding="utf-8")
    (root / "a" / "b").mkdir(parents=True)
    outside = tmp_path / "outside"
    (outside / "b").mkdir(parents=True)
    seal = root / "a" / "b" / "dfr-seal"
    resolving = lane.resolve_pinned_validator

    def swapping():
        (root / "a").rename(root / "a.moved")
        (root / "a").symlink_to(outside, target_is_directory=True)
        return resolving()

    monkeypatch.setattr(lane, "resolve_pinned_validator", swapping)
    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", _stub_precheck)
    code = lane.main(["--repo-root", str(root), "--phase", "seal",
                      "--corpus-checkout", str(corpus), "--corpus-ref", "HEAD",
                      "--decision-in", str(root / "dfr-decision.json"),
                      "--seal-out", str(seal),
                      "--seal-result-out", str(root / "seal-result.json"),
                      "--correlation-id", CORRELATION])
    result = json.loads((root / "seal-result.json").read_text(
        encoding="utf-8"))
    assert sorted(path.name for path in (outside / "b").iterdir()) == []
    assert result["sealed"] is False
    assert result["reason"].startswith(
        f"the seal directory {seal} cannot be made: 'a', on its way from "
        f"{root}, is not a directory of its own"), result["reason"]
    assert code is None


def test_clearing_the_result_path_follows_no_link(tmp_path, monkeypatch):
    """A directory at the result path is removed with everything under it,
    and a link inside it is removed as the link, never followed. Where the
    platform's `shutil.rmtree` could follow a link swapped in while it runs,
    the directory is refused instead, and left as it was."""
    workspace_file, workspace_dir = _a_workspace(tmp_path / "workspace")
    planted = tmp_path / "seal-result.json"
    _a_directory_holding_links_out(planted, workspace_file, workspace_dir)
    monkeypatch.setattr(shutil.rmtree, "avoids_symlink_attacks", False)
    with pytest.raises(OSError, match="could follow a link"):
        lane._clear_result_path(planted)
    assert (planted / "nested" / "planted.txt").is_file()
    monkeypatch.undo()
    lane._clear_result_path(planted)
    assert not os.path.lexists(planted)
    assert workspace_file.read_text(encoding="utf-8") == "untouched\n"
    assert (workspace_dir / "kept.txt").read_text(encoding="utf-8") == \
        "untouched\n"


def test_the_seal_phase_reports_a_refusal_as_a_gate_not_an_exception(
        corpus, tmp_path, monkeypatch):
    head = _git(corpus, "rev-parse", "HEAD")
    monkeypatch.setattr(lane, "seal_source",
                        lambda **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is False
    assert result["reason"] == "RuntimeError: boom"
    assert result["strict_failed"] is False


def test_the_seal_phase_records_a_strict_verdict_with_its_findings(
        corpus, tmp_path, monkeypatch, capsys):
    """A snapshot the sealed validator REJECTS is a verdict, not a fault. The
    seal result says `strict_failed` and carries the findings, which is what
    the workflow's record step reads to record the verdict. Nothing is sealed,
    so nothing is dispatched, and the process still exits 0."""
    head = _git(corpus, "rev-parse", "HEAD")
    findings = ["ERROR [snapshot-dangling-cluster-ref] snapshot.json: one",
                "validate-ideation-dashboard-contracts: 1 error(s), 0 warning(s)"]

    def rejecting(seal_root, *, source_head, source_committed_at,
                  container=None):
        raise lane.StrictGateRejected("--strict REJECTED the snapshot this "
                                      "seal renders", detail=findings)

    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", rejecting)
    result = _seal_cli(tmp_path, corpus, decision=_decision(head))
    assert result["sealed"] is False
    assert result["strict_failed"] is True
    assert result["reason"] == "--strict REJECTED the snapshot this seal renders"
    assert result["detail"] == findings
    assert not (_cli_seal(tmp_path) / lane.SEAL_MANIFEST_NAME).exists()
    said = capsys.readouterr().out
    assert "STRICT FAILED" in said and findings[0] in said


def test_the_strict_findings_reach_the_log_inside_a_fence(
        corpus, tmp_path, monkeypatch, capsys):
    """The findings are the sealed validator's own output, and the runner
    takes a workflow command from any line a step prints. So they reach the
    job's log only inside a fence (#1191): `::stop-commands::` with a token
    drawn after the run, 128 random bits no sealed run saw, and the same
    token on a line of its own to resume. A finding that prints a command,
    or tries to open or close a fence of its own, stays inside."""
    head = _git(corpus, "rev-parse", "HEAD")
    findings = ["ERROR [snapshot-unknown-kind] ::add-path::/tmp/evil",
                "::set-env name=GH_TOKEN::stolen",
                "::stop-commands::0123456789abcdef0123456789abcdef",
                "::0123456789abcdef0123456789abcdef::"]

    def rejecting(seal_root, *, source_head, source_committed_at,
                  container=None):
        raise lane.StrictGateRejected("--strict REJECTED the snapshot this "
                                      "seal renders", detail=findings)

    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", rejecting)
    _seal_cli(tmp_path, corpus, decision=_decision(head))
    lines = capsys.readouterr().out.splitlines()
    opened = [n for n, line in enumerate(lines)
              if re.fullmatch(r"::stop-commands::[0-9a-f]{32}", line)]
    assert len(opened) == 1, lines
    token = lines[opened[0]].split("::")[2]
    closed = lines.index(f"::{token}::")
    assert lines[opened[0] + 1:closed] == [f"  {line}" for line in findings]
    assert token != "0123456789abcdef0123456789abcdef"
    assert not any(line.startswith("::") for line in lines[:opened[0]]
                   if "STRICT FAILED" not in line and "NOT SEALED" not in line
                   and not line.startswith("::warning::"))


@pytest.mark.parametrize("raised", ["refused", "rejected"])
def test_a_sealed_reason_reaches_the_log_as_one_warning_line(
        corpus, tmp_path, monkeypatch, capsys, raised):
    """A refusal can carry a line a sealed run printed (`_last_line`,
    `_validator_said`), and the seal phase prints its reason as the data of a
    `::warning::` line. The runner takes a workflow command only at the start
    of a line, so the reason is printed as one line whatever it holds, with
    `%` escaped as command data is (Copilot, PR #1192): nothing it carries
    starts a line of its own."""
    head = _git(corpus, "rev-parse", "HEAD")
    reason = ("the sealed render unit could not render the snapshot (exit 1): "
              "said\n::add-path::/tmp/evil\r::set-env name=GH_TOKEN::stolen"
              "\u2028::error::sealed %0A::stop-commands::guessed")

    def refusing(seal_root, *, source_head, source_committed_at,
                 container=None):
        if raised == "refused":
            raise lane.SealRefused(reason)
        raise lane.StrictGateRejected(reason, detail=["ERROR [x] a finding"])

    monkeypatch.setattr(lane, "gh_read_file", lambda *a, **kw: RECIPE_TEXT)
    monkeypatch.setattr(lane, "seal_render_legs", _stub_legs)
    monkeypatch.setattr(lane, "precheck_sealed_render", refusing)
    _seal_cli(tmp_path, corpus, decision=_decision(head))
    lines = capsys.readouterr().out.splitlines()
    fence = [n for n, line in enumerate(lines)
             if re.fullmatch(r"::stop-commands::[0-9a-f]{32}", line)]
    assert len(fence) == (1 if raised == "rejected" else 0), lines
    outside = lines[:fence[0]] if fence else lines
    warned = [line for line in outside if "add-path" in line]
    assert len(warned) == 1 and warned[0].startswith("::warning::"), lines
    assert "%250A::stop-commands::guessed" in warned[0]
    assert not any(line.lstrip().startswith("::")
                   and not line.startswith("::warning::")
                   for line in outside), lines


def test_each_fence_is_opened_with_a_token_of_its_own(capsys):
    """The fence's token is drawn at each print, never fixed, so no sealed
    run can have seen the one that closes it (#1191)."""
    tokens = set()
    for _ in range(3):
        lane._print_fenced(["::add-path::/tmp/evil"])
        lines = capsys.readouterr().out.splitlines()
        token = lines[0].removeprefix("::stop-commands::")
        assert re.fullmatch(r"[0-9a-f]{32}", token), lines
        assert lines[1:] == ["  ::add-path::/tmp/evil", f"::{token}::"]
        tokens.add(token)
    assert len(tokens) == 3


# ---------------------------------------------------------------------------
# the parent's own workflow stage — ordering, gating and the artifact's name
# ---------------------------------------------------------------------------

def _finalize_steps() -> list[dict]:
    import yaml
    from conftest import REPO_ROOT
    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml")
        .read_text(encoding="utf-8"))
    return workflow["jobs"]["finalize"]["steps"]


def _step_index(steps: list[dict], **match) -> int:
    for index, step in enumerate(steps):
        if all(step.get(key) == value for key, value in match.items()):
            return index
    raise AssertionError(f"no finalize step matching {match}")


def test_the_seal_step_runs_after_the_decision_and_before_the_dispatch():
    """The ordering IS the requirement: the seal must not run on a quiet night
    (the decision short-circuits first) and the child must not be dispatched
    against an artifact that does not exist yet."""
    steps = _finalize_steps()
    decide = _step_index(steps, id="dfr-decide")
    seal = _step_index(steps, id="dfr-seal")
    upload = _step_index(steps, id="dfr-upload")
    dispatch = _step_index(steps, id="dfr-dispatch")
    assert decide < seal < upload < dispatch


def test_the_seal_step_is_gated_on_movement_and_readiness():
    seal = _finalize_steps()[_step_index(_finalize_steps(), id="dfr-seal")]
    assert "steps.dfr-readiness.outputs.ready == 'true'" in seal["if"]
    assert "steps.dfr-decide.outputs.build == 'true'" in seal["if"]
    assert seal["continue-on-error"] is True     # a seal never fails the run
    run = seal["run"]
    assert "--phase seal" in run
    assert "--decision-in dfr-decision.json" in run
    assert "--seal-out dfr-seal" in run
    assert "--seal-result-out dfr-seal-result.json" in run
    assert '--correlation-id "$CORRELATION_ID"' in run


def test_the_upload_names_the_artifact_the_child_downloads():
    steps = _finalize_steps()
    upload = steps[_step_index(steps, id="dfr-upload")]
    assert upload["uses"].startswith("actions/upload-artifact@v4")
    with_ = upload["with"]
    assert with_["name"] == (
        "dashboard-image-source-"
        "${{ steps.dfr-readiness.outputs.correlation_id }}")
    assert with_["name"].startswith(lane.SEAL_ARTIFACT_PREFIX)
    # The seal's own output directory IS the uploaded path — one name, not two.
    seal = steps[_step_index(steps, id="dfr-seal")]
    assert f"--seal-out {with_['path']}" in seal["run"]
    # v4 drops dotfiles by default, and the manifest's index is the authority
    # on what the download must contain (design open question 3).
    assert with_["include-hidden-files"] is True
    assert with_["if-no-files-found"] == "error"
    assert int(with_["retention-days"]) <= 7


def test_the_dispatch_is_gated_on_a_seal_that_actually_uploaded():
    steps = _finalize_steps()
    dispatch = steps[_step_index(steps, id="dfr-dispatch")]
    assert "steps.dfr-seal.outputs.sealed == 'true'" in dispatch["if"]
    # `continue-on-error` makes the upload's CONCLUSION always success, so the
    # gate has to read its OUTCOME or a child could be dispatched against an
    # artifact that never uploaded.
    assert "steps.dfr-upload.outcome == 'success'" in dispatch["if"]


def test_an_unsealed_source_records_a_skip_rather_than_a_failure():
    steps = _finalize_steps()
    skip = steps[_step_index(
        steps, name="Ideation-dashboard image refresh — record skip (source not sealed)")]
    assert skip["continue-on-error"] is True
    assert "--skip-reason" in skip["run"]
    assert "steps.dfr-seal.outputs.sealed != 'true'" in skip["if"]
    assert "steps.dfr-upload.outcome != 'success'" in skip["if"]
    assert _step_index(steps, id="dfr-dispatch") > steps.index(skip)


def test_the_record_step_hands_on_a_strict_verdict_only_when_the_seal_says_so():
    """The record step passes the seal result on ONLY when the seal result
    says `strict_failed`. This workflow runs at openxFactory main while the
    scripts come from the aggregation's openxFactory pin, and a pin that
    predates the flag must be handed exactly the call it knows."""
    steps = _finalize_steps()
    run = steps[_step_index(
        steps,
        name="Ideation-dashboard image refresh — record skip (source not sealed)",
    )]["run"]
    assert 'get("strict_failed") is True' in run
    guard = run.index('if [ "$STRICT" = "true" ]; then')
    handoff = run.index("ARGS+=(--seal-result-in dfr-seal-result.json)")
    assert guard < handoff < run.index("fi", handoff)
    assert run.count("--seal-result-in") == 1
    assert run.index("STRICT=false") < guard              # defaulted first


def _run_the_seal_step(tmp_path, pinned: str, *, plant=None):
    """The seal step's own script, run under its own shell in a stand-in
    workspace whose pinned lane is `pinned` and whose nightly script only
    records that it ran. `plant` puts something at the result's path first."""
    steps = _finalize_steps()
    seal = steps[_step_index(steps, id="dfr-seal")]
    workspace = tmp_path / "workspace"
    package = workspace / "openxFactory" / "scripts" / "ideation_dashboard"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "dashboard_refresh_lane.py").write_text(pinned)
    (workspace / "openxFactory" / "scripts" /
     "dashboard-refresh-nightly.py").write_text(
        "import json, pathlib\n"
        "pathlib.Path('nightly-ran').write_text('')\n"
        "json.dump({'sealed': True}, open('dfr-seal-result.json', 'w'))\n")
    if plant is not None:
        plant(workspace / "dfr-seal-result.json")
    python = tmp_path / "python" / "bin"
    python.mkdir(parents=True)
    (python / "python3").symlink_to(sys.executable)
    script = tmp_path / "step.sh"
    script.write_text(seal["run"])
    output = tmp_path / "github-output"
    output.write_text("")
    proc = subprocess.run(
        ["/bin/bash", "--noprofile", "--norc", "-p", "-e", str(script)],
        cwd=workspace, capture_output=True, text=True, timeout=120,
        env={"PATH": "/usr/bin:/bin", "pythonLocation": str(python.parent),
             "GITHUB_OUTPUT": str(output), "CORRELATION_ID": "c-1"})
    return proc, workspace, output.read_text()


_A_LANE_FROM_BEFORE_1191 = "LANE = 'ideation-dashboard-refresh'\n"
_A_LANE_THAT_CONTAINS_ITS_RUNS = 'SEALED_IMAGE_ENV = "SEALED_IMAGE"\n'
_A_LANE_THAT_CANNOT_BE_IMPORTED = "raise SystemExit(0)\ndef (:\n"


@pytest.mark.parametrize("pinned, seals", [
    (_A_LANE_FROM_BEFORE_1191, False),
    (_A_LANE_THAT_CANNOT_BE_IMPORTED, False),
    (_A_LANE_THAT_CONTAINS_ITS_RUNS, True),
], ids=["a-lane-from-before-1191", "a-lane-that-cannot-be-imported",
        "a-lane-that-contains-its-runs"])
def test_the_seal_step_runs_no_lane_that_would_run_sealed_code_here(
        tmp_path, pinned, seals):
    """This workflow runs at openxFactory main, and the lane comes from the
    aggregation's pin. A lane from before #1191 ignores SEALED_IMAGE and runs
    the probe, the render and its --strict validation on this runner. So the
    seal step asks the pinned lane first, and runs it only when it names
    SEALED_IMAGE. Any other lane seals nothing, and the refusal is recorded as
    the seal's result, so the record step reports it and nothing is uploaded
    or dispatched (Copilot, PR #1192)."""
    proc, workspace, output = _run_the_seal_step(tmp_path, pinned)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    result = json.loads((workspace / "dfr-seal-result.json").read_text())
    assert (workspace / "nightly-ran").exists() is seals
    assert output == f"sealed={str(seals).lower()}\n"
    assert result["sealed"] is seals
    if not seals:
        assert "predates #1191" in result["reason"], result
        assert "::warning::" in proc.stdout and "NOT SEALED" in proc.stdout


@pytest.mark.parametrize("kind", ["a-link-out-of-the-checkout",
                                  "a-link-the-step-cannot-remove",
                                  "a-directory"])
def test_the_refusal_the_seal_step_records_follows_nothing_at_its_path(
        tmp_path, kind):
    """The seal step writes a pinned lane's refusal itself, since that lane
    cannot be trusted to. So it removes whatever sits at the result's path
    as the lane does, without following it, and creates the result
    exclusively, following no link. A link planted there never has its
    target written, and a directory there leaves no result at all, so the
    record step reads none and still nothing is sealed (Copilot, PR #1192)."""
    outside = tmp_path / "outside.json"
    outside.write_text("untouched")

    def plant(path):
        if kind.startswith("a-link"):
            path.symlink_to(outside)
        else:
            path.mkdir()
        if kind == "a-link-the-step-cannot-remove":
            path.parent.chmod(0o555)    # so `rm` leaves the link in place

    try:
        proc, workspace, output = _run_the_seal_step(
            tmp_path, _A_LANE_FROM_BEFORE_1191, plant=plant)
    finally:
        (tmp_path / "workspace").chmod(0o755)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert outside.read_text() == "untouched"
    assert output == "sealed=false\n"
    assert not (workspace / "nightly-ran").exists()
    result = workspace / "dfr-seal-result.json"
    if kind == "a-link-out-of-the-checkout":
        assert not result.is_symlink() and result.is_file()
        assert json.loads(result.read_text())["sealed"] is False
    elif kind == "a-link-the-step-cannot-remove":
        assert result.is_symlink()
    else:
        assert result.is_dir()


def test_the_seal_steps_failure_is_what_withholds_an_unwritten_result():
    """A seal phase that could not write its own result exits non-zero
    (`SEAL_RESULT_UNWRITTEN_EXIT`), and that is what withholds the dispatch
    then: the step runs under `bash -e`, by its absolute path since sealed
    code has run by then (#1191), so it stops at the lane's call before
    `sealed` is read from whatever sits at the result's path. So no job or
    workflow default names another shell, and nothing masks the lane's
    status (Copilot, PR #1166)."""
    import yaml
    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml")
        .read_text(encoding="utf-8"))
    assert "defaults" not in workflow
    assert "defaults" not in workflow["jobs"]["finalize"]
    steps = workflow["jobs"]["finalize"]["steps"]
    seal = steps[_step_index(steps, id="dfr-seal")]
    assert seal["shell"] == "/bin/bash --noprofile --norc -p -e {0}"
    run = seal["run"]
    call = run.index('"${pythonLocation:?}/bin/python3" '
                     "openxFactory/scripts/dashboard-refresh-nightly.py")
    read = run.index('SEALED="$("${pythonLocation:?}/bin/python3"')
    assert call < read
    assert "set +e" not in run
    invocation = run[call:read]
    assert "||" not in invocation and "&&" not in invocation
    assert "--seal-result-out dfr-seal-result.json" in invocation


def _the_build_step() -> dict:
    steps = _finalize_steps()
    return steps[_step_index(steps, id="dfr-sealed-image")]


def test_the_finalize_job_builds_the_sealed_image_before_the_seal():
    """The sealed runs' image is built in the finalize job, before the seal
    step, under the seal step's own condition, and handed on by its content
    id in SEALED_IMAGE (#1191). The workflow runs at openxFactory main while
    the lane comes from the aggregation's pin, so the id crosses by the
    environment, which a lane that predates it ignores, never by a flag it
    would refuse."""
    steps = _finalize_steps()
    build = _the_build_step()
    seal = steps[_step_index(steps, id="dfr-seal")]
    assert steps.index(build) == steps.index(seal) - 1
    assert build["if"] == seal["if"]
    assert build["continue-on-error"] is True
    assert build["shell"] == "/bin/bash --noprofile --norc -p -eo pipefail {0}"
    run = build["run"]
    assert "/usr/bin/docker build \\\n" in run
    assert ('--label "openxfactory.dashboard-refresh.sealed-run='
            '${GITHUB_RUN_ID:?}-${GITHUB_RUN_ATTEMPT:?}"') in run
    assert "--iidfile \"$IIDFILE\" - <<'DOCKERFILE'" in run
    assert 'echo "SEALED_IMAGE=$SEALED_IMAGE" >> "$GITHUB_ENV"' in run
    assert 'if [[ ! "$SEALED_IMAGE" =~ ^sha256:[0-9a-f]{64}$ ]]; then' in run
    assert lane.SEALED_IMAGE_ENV == "SEALED_IMAGE"
    assert "SEALED_IMAGE" not in (seal.get("env") or {})
    assert "--sealed-image" not in seal["run"]


def _dockerfile(run: str) -> str:
    return run.split("<<'DOCKERFILE'\n", 1)[1].split("\nDOCKERFILE", 1)[0]


def _lock_pins() -> dict[str, tuple[str, set[str]]]:
    """requirements/hermes-runtime-contracts.lock: name -> (version,
    hashes)."""
    pins: dict[str, tuple[str, set[str]]] = {}
    name = None
    lock = REPO_ROOT / "requirements" / "hermes-runtime-contracts.lock"
    for line in lock.read_text(encoding="utf-8").splitlines():
        head = re.match(r"^([A-Za-z0-9_.-]+)==(\S+)", line)
        if head:
            name = head.group(1).lower()
            pins[name] = (head.group(2), set())
        for digest in re.findall(r"--hash=sha256:([0-9a-f]{64})", line):
            pins[name][1].add(digest)
    return pins


def test_the_sealed_image_installs_exactly_what_the_lock_pins():
    """ONE FROM, by digest, and each wheel at the version
    requirements/hermes-runtime-contracts.lock pins, by a sha256 the lock
    lists, binary-only and with no resolution of pip's own (#1191): the
    child worker's image (opensoft/xFactory#526)."""
    dockerfile = _dockerfile(_the_build_step()["run"])
    froms = [line for line in dockerfile.splitlines() if line.startswith("FROM ")]
    assert froms == ["FROM python:3.12-slim@sha256:"
                     "f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f"]
    assert "--no-deps --only-binary=:all: --require-hashes" in dockerfile
    wheels = re.findall(r"'([a-z0-9-]+)==(\S+)((?: --hash=sha256:[0-9a-f]{64})+)'",
                        dockerfile)
    assert {name for name, _v, _h in wheels} == {
        "attrs", "jsonschema", "jsonschema-specifications", "pyyaml",
        "referencing", "rfc3339-validator", "rpds-py", "six",
        "typing-extensions"}
    pins = _lock_pins()
    for name, version, hashes in wheels:
        locked_version, locked_hashes = pins[name]
        assert version == locked_version, name
        named = set(re.findall(r"[0-9a-f]{64}", hashes))
        assert named and named <= locked_hashes, name


def test_the_build_step_refuses_what_would_take_the_calls_elsewhere():
    """Before anything is built, the step refuses ACTIONS_ALLOW_UNSECURE_COMMANDS
    and every variable that would send the docker CLI to another daemon or
    builder, the set the lane refuses before any sealed run (#1191)."""
    run = _the_build_step()["run"]
    assert 'if [ -n "${ACTIONS_ALLOW_UNSECURE_COMMANDS+set}" ]; then' in run
    listed = run.split("for name in ", 1)[1].split("; do", 1)[0]
    assert listed.replace("\\", " ").split() == list(_SEALED_DOCKER_ENV[1:])
    assert set(_SEALED_DOCKER_ENV) == set(lane._SEALED_REFUSED_ENV)
    assert run.index("ACTIONS_ALLOW_UNSECURE_COMMANDS") < run.index("docker build")


def test_the_job_removes_its_sealed_containers_and_image_last():
    """Every sealed run is `--rm`, and a cancelled run can still leave a
    container, and the image stays until something removes it. So the job's
    last step, always, removes what carries this run's label, and the image
    by its id (#1191)."""
    steps = _finalize_steps()
    scrub = steps[-1]
    assert scrub["if"] == "always()"
    assert scrub["continue-on-error"] is True
    run = scrub["run"]
    label = ('LABEL="openxfactory.dashboard-refresh.sealed-run='
             '${GITHUB_RUN_ID:?}-${GITHUB_RUN_ATTEMPT:?}"')
    assert label in run
    assert '/usr/bin/docker ps -aq --filter "label=$LABEL"' in run
    assert ('/usr/bin/xargs -r /usr/bin/env -i "${docker_env[@]}" '
            '/usr/bin/docker rm -f') in run
    assert '/usr/bin/docker image rm "$SEALED_IMAGE"' in run
    assert '/usr/bin/docker image ls -aq --no-trunc --filter "label=$LABEL"' in run
    assert lane.SEALED_RUN_LABEL == "openxfactory.dashboard-refresh.sealed-run"


# A stand-in for the scrub step's docker, found by its own path, since every
# call runs under `env -i`. It logs each call and the environment it sees,
# lists one container of this run's until `left` sweeps have seen it
# ("forever" never lets it go), refuses `rm -f` as docker does for a
# container already going away by its own `--rm`, and fails every `ps` once
# `ps-fails` exists. The recorded image is found while `image-stays` exists,
# an image with the run's label is listed while `labelled-image-stays` does,
# and the image listing fails while `image-ls-fails` does. An untagged image
# of the run, while `untagged-image` exists, is listed only to `-a`, as
# docker's containerd image store lists one, until it is removed.
_SCRUB_DOCKER = """\
import os, sys
from pathlib import Path
state = Path(sys.argv[0]).resolve().parent / "state"
with open(state / "calls", "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
    log.write("ENV " + " ".join(sorted(os.environ)) + "\\n")
if sys.argv[1:3] == ["image", "inspect"]:
    sys.exit(0 if (state / "image-stays").exists() else 1)
if sys.argv[1:3] == ["image", "ls"]:
    if (state / "image-ls-fails").exists():
        sys.exit(1)
    if (state / "labelled-image-stays").exists():
        print("sha256:" + "fe" * 32)
    if (state / "untagged-image").exists() and "-aq" in sys.argv:
        print("sha256:" + "0f" * 32)
if sys.argv[1:4] == ["image", "rm", "sha256:" + "0f" * 32]:
    (state / "untagged-image").unlink()
if sys.argv[1] == "ps":
    if (state / "ps-fails").exists():
        sys.exit(1)
    left = (state / "left").read_text().strip()
    if left == "forever":
        print("c0ffee")
    elif int(left) > 0:
        print("c0ffee")
        (state / "left").write_text(str(int(left) - 1))
elif sys.argv[1] == "rm":
    sys.exit("Error response from daemon: removal of container c0ffee is "
             "already in progress")
"""


# What a runner's job can hold that a docker call must never see: proxies,
# which the docker CLI honors from its environment, and a token.
_THE_JOBS_OWN_ENVIRONMENT = {
    "HTTP_PROXY": "http://user:secret@proxy.invalid:3128",
    "https_proxy": "http://user:secret@proxy.invalid:3128",
    "ALL_PROXY": "socks5://proxy.invalid:1080", "NO_PROXY": "",
    "GH_TOKEN": "a-token-no-docker-call-sees"}


def _run_the_scrub_step(tmp_path, *, left: str, ps_fails: bool = False,
                        flags=()):
    """The job's last step, run under its own shell, with its docker and its
    sleep swapped for stand-ins by their absolute paths."""
    run = _finalize_steps()[-1]["run"]
    state = tmp_path / "state"
    state.mkdir()
    (state / "left").write_text(left)
    if ps_fails:
        (state / "ps-fails").write_text("")
    for flag in flags:
        (state / flag).write_text("")
    docker = tmp_path / "docker"
    docker.write_text(f"#!{sys.executable}\n{_SCRUB_DOCKER}")
    docker.chmod(0o755)
    sleep = tmp_path / "sleep"
    sleep.write_text(f'#!/bin/sh\necho "sleep $*" >> "{state}/calls"\n')
    sleep.chmod(0o755)
    script = tmp_path / "step.sh"
    script.write_text(run.replace("/usr/bin/docker", str(docker))
                      .replace("/usr/bin/sleep", str(sleep)))
    runner_temp = tmp_path / "runner-temp"
    runner_temp.mkdir()
    proc = subprocess.run(
        ["/bin/bash", "--noprofile", "--norc", "-p", "-e", str(script)],
        env={"PATH": "/usr/bin:/bin", "GITHUB_RUN_ID": "4242",
             "GITHUB_RUN_ATTEMPT": "2", "RUNNER_TEMP": str(runner_temp),
             "SEALED_IMAGE": STAND_IN_IMAGE, "STAND_IN_STATE": str(state),
             **_THE_JOBS_OWN_ENVIRONMENT,
             **{name: "tcp://elsewhere.invalid:2376"
                for name in lane._SEALED_REFUSED_ENV[1:]}},
        capture_output=True, text=True, timeout=120)
    calls = (state / "calls").read_text().splitlines()
    return proc, calls


def test_the_scrub_sweeps_until_no_container_of_this_run_is_left(tmp_path):
    """A container already going away by its own `--rm` refuses `docker rm`
    and holds the sealed image until it is gone, which opensoft/xFactory#526
    found on real docker. So the last step sweeps this run's containers until
    none is left, and only then removes the image (#1191)."""
    proc, calls = _run_the_scrub_step(tmp_path, left="3")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    label = "label=openxfactory.dashboard-refresh.sealed-run=4242-2"
    sweeps = [call for call in calls if call == f"ps -aq --filter {label}"]
    assert len(sweeps) == 5    # three that list it, the one that does not, the check
    assert calls.count("rm -f c0ffee") == 3
    image = calls.index(f"image rm {STAND_IN_IMAGE}")
    assert image > max(i for i, call in enumerate(calls)
                       if call == "rm -f c0ffee")
    assert image > max(i for i, call in enumerate(calls[:image])
                       if call.startswith("ps "))
    assert "::error::" not in proc.stdout
    # Every call sees nothing of the job's environment but a fresh docker
    # configuration, as the build's and the lane's do, so it reaches the
    # local daemon they used, through no proxy and no routing variable
    # (Copilot, PR #1192).
    seen = {call for call in calls if call.startswith("ENV ")}
    assert seen == {"ENV DOCKER_CONFIG HOME LANG PATH"}, seen


@pytest.mark.parametrize("left, ps_fails", [("forever", False), ("0", True)],
                         ids=["a-container-that-never-goes",
                              "a-daemon-that-cannot-list"])
def test_a_container_the_scrub_could_not_remove_fails_the_step(
        tmp_path, left, ps_fails):
    """A container of this run's still there after 30 seconds of sweeping, or
    a daemon that cannot say whether one is, fails the step. The step is
    continue-on-error, so the nightly is never failed by it, and the run
    shows it (#1191, as opensoft/xFactory#526's last step does)."""
    proc, calls = _run_the_scrub_step(tmp_path, left=left, ps_fails=ps_fails)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "::error::a container of this run's sealed code" in proc.stdout
    assert f"image rm {STAND_IN_IMAGE}" in calls
    if left == "forever":
        assert calls.count("rm -f c0ffee") == 30
        assert "c0ffee" in proc.stdout
    assert _finalize_steps()[-1]["continue-on-error"] is True


def test_the_scrub_removes_an_untagged_image_of_this_run(tmp_path):
    """Docker's containerd image store lists an untagged image only with
    `--all`, which opensoft/xFactory#526 found on real docker. So the images
    carrying this run's label are listed with `-a` to be removed, and an
    untagged one goes too, leaving the step clean (#1191)."""
    proc, calls = _run_the_scrub_step(tmp_path, left="0",
                                      flags=("untagged-image",))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "image rm sha256:" + "0f" * 32 in calls
    assert "::error::" not in proc.stdout


@pytest.mark.parametrize("flag, said", [
    ("image-stays", f"the sealed image {STAND_IN_IMAGE} is still there"),
    ("labelled-image-stays", "an image carrying this run's label is still "
                             "there, or the daemon could not say: sha256:"),
    ("image-ls-fails", "an image carrying this run's label is still there, "
                       "or the daemon could not say"),
], ids=["the-recorded-image", "an-image-with-the-label",
        "a-daemon-that-cannot-list-images"])
def test_an_image_the_scrub_could_not_remove_fails_the_step(tmp_path, flag,
                                                            said):
    """The image the build step recorded, or any image carrying this run's
    label, still there after the removals, or a daemon that cannot say,
    fails the step, as a container left behind does (Copilot, PR #1192)."""
    proc, calls = _run_the_scrub_step(tmp_path, left="0", flags=(flag,))
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert f"::error::{said}" in proc.stdout, proc.stdout
    assert f"image rm {STAND_IN_IMAGE}" in calls


# A stand-in for the build step's docker, found by its own path, since the
# build runs under `env -i`. It records the environment it sees, fails while
# `build-fails` sits beside it, and otherwise records an image id in the
# `--iidfile` it is handed.
_BUILD_DOCKER = """\
import json, os, sys
from pathlib import Path
here = Path(sys.argv[0]).resolve().parent
(here / "seen").write_text(json.dumps(dict(os.environ)), encoding="utf-8")
if (here / "build-fails").exists():
    sys.exit("ERROR: failed to solve")
args = sys.argv[1:]
with open(args[args.index("--iidfile") + 1], "w", encoding="utf-8") as out:
    out.write("sha256:" + "ab" * 32)
"""


@pytest.mark.parametrize("fails", [True, False], ids=["a-build-that-stops",
                                                      "a-build-that-ends"])
def test_the_build_step_records_no_image_id_but_its_own(tmp_path, fails):
    """The step clears SEALED_IMAGE for every later step before it builds, so
    a build that stops leaves no image id behind it, whatever the job held
    before, and only a built and checked id is recorded (Copilot, PR #1192).
    GITHUB_ENV takes the last value written."""
    docker = tmp_path / "docker"
    docker.write_text(f"#!{sys.executable}\n{_BUILD_DOCKER}")
    docker.chmod(0o755)
    if fails:
        (tmp_path / "build-fails").write_text("")
    script = tmp_path / "step.sh"
    script.write_text(_the_build_step()["run"].replace("/usr/bin/docker",
                                                       str(docker)))
    github_env = tmp_path / "github-env"
    github_env.write_text("")
    runner_temp = tmp_path / "runner-temp"
    runner_temp.mkdir()
    proc = subprocess.run(
        ["/bin/bash", "--noprofile", "--norc", "-p", "-eo", "pipefail",
         str(script)],
        env={"PATH": "/usr/bin:/bin", "GITHUB_RUN_ID": "4242",
             "GITHUB_RUN_ATTEMPT": "2", "RUNNER_TEMP": str(runner_temp),
             "GITHUB_ENV": str(github_env), "SEALED_IMAGE": STAND_IN_IMAGE,
             **_THE_JOBS_OWN_ENVIRONMENT},
        capture_output=True, text=True, timeout=120)
    # The build sees nothing of the job's environment but a docker
    # configuration of its own, made fresh in the job's temporary directory,
    # so no login, plugin or proxy of the runner's reaches it (#1191;
    # Copilot, PR #1192).
    seen = json.loads((tmp_path / "seen").read_text(encoding="utf-8"))
    assert sorted(seen) == ["DOCKER_CONFIG", "HOME", "LANG", "PATH"], seen
    config = Path(seen["DOCKER_CONFIG"])
    assert seen["HOME"] == seen["DOCKER_CONFIG"]
    assert config.parent == runner_temp, config
    assert config.name.startswith("dfr-docker-config."), config
    recorded = [line for line in github_env.read_text().splitlines()
                if line.startswith("SEALED_IMAGE=")]
    assert recorded[0] == "SEALED_IMAGE="
    if fails:
        assert proc.returncode != 0
        assert recorded == ["SEALED_IMAGE="]
    else:
        assert proc.returncode == 0, proc.stderr
        assert recorded == ["SEALED_IMAGE=", "SEALED_IMAGE=sha256:" + "ab" * 32]
    for scope in (_workflow(), _workflow()["jobs"]["finalize"],
                  *_finalize_steps()):
        assert "SEALED_IMAGE" not in (scope.get("env") or {})


def _workflow() -> dict:
    import yaml
    return yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml")
        .read_text(encoding="utf-8"))


_HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
_COMMAND_AT = re.compile(r"(?:^|[;&|(!]|\$\()\s*([A-Za-z_][A-Za-z0-9_.+-]*)(?=\s|$|\))")
# A keyword that a command follows is a separator, never itself a command.
_KEYWORD = re.compile(r"\b(?:if|then|do|else|elif|while|until)\b")
# Commands a step may name bare: the shell's own builtins and keywords.
_BUILTINS = {"if", "then", "else", "elif", "fi", "for", "in", "do", "done",
             "while", "until", "case", "esac", "echo", "printf", "exit",
             "export", "set", "unset", "local", "read", "true", "false",
             "test", "cd", "shift", "return", "break", "continue", "trap",
             "wait", "declare", "readonly", "mapfile", "command", "type"}


def _outside_quotes(line: str) -> str:
    """`line` with quoted text blanked, keeping in view the command
    substitutions a double-quoted string runs, with their own quoted text
    blanked in turn."""
    out, i, n, depth, in_double = [], 0, len(line), 0, False
    while i < n:
        c = line[i]
        if c == "\\":
            out.append("  ")
            i += 2
        elif c == "'" and not (in_double and depth == 0):
            j = line.find("'", i + 1)
            j = n - 1 if j < 0 else j
            out.append(" " * (j - i + 1))
            i = j + 1
        elif c == '"' and in_double and depth:
            j = line.find('"', i + 1)
            j = n - 1 if j < 0 else j
            out.append(" " * (j - i + 1))
            i = j + 1
        elif c == '"':
            in_double = not in_double
            out.append(" ")
            i += 1
        elif in_double and line.startswith("$(", i):
            depth += 1
            out.append("$(")
            i += 2
        elif in_double and c == ")" and depth:
            depth -= 1
            out.append(")")
            i += 1
        else:
            out.append(c if not in_double or depth else " ")
            i += 1
    return "".join(out)


def _bare_commands(run: str) -> list[str]:
    """The bare command names of a step's script, outside comments, quoted
    text and heredoc bodies. A line a backslash continues is read as one
    with the next."""
    found, pending = [], []
    for raw in run.replace("\\\n", " ").splitlines():
        if pending:
            if raw.strip() == pending[0]:
                pending.pop(0)
            continue
        pending += [m.group(2) for m in _HEREDOC.finditer(raw)]
        if raw.lstrip().startswith("#"):
            continue
        line = re.sub(r"\$?\(\([^()]*\)\)", " ", raw)     # arithmetic
        line = _KEYWORD.sub(";", _outside_quotes(line))
        found += [name for name in _COMMAND_AT.findall(line.strip())
                  if name not in _BUILTINS]
    return found


def test_every_step_after_sealed_code_calls_its_tools_by_absolute_path():
    """From the step that builds the sealed image on, every step runs its
    shell by its absolute path and calls every tool by its absolute path,
    never by a name looked up on a PATH (#1191). Nothing sealed can reach
    this runner's PATH, since every sealed run is contained. This makes the
    later steps independent of that PATH as well, as the child worker's are
    (opensoft/xFactory#526)."""
    steps = _finalize_steps()
    later = steps[steps.index(_the_build_step()):]
    shells = []
    for step in later:
        if "run" not in step:
            continue
        shells.append(step["shell"])
        assert _bare_commands(step["run"]) == [], step.get("name")
    assert set(shells) == {"/bin/bash --noprofile --norc -p -e {0}",
                           "/bin/bash --noprofile --norc -p -eo pipefail {0}"}
    seal = steps[_step_index(steps, id="dfr-seal")]
    assert _bare_commands("python3 -c x; gh api y") == ["python3", "gh"]
    assert _bare_commands("if gh api y; then X=\"$(git log)\"; fi") == \
        ["gh", "git"]
    assert '"${pythonLocation:?}/bin/python3" -c' in seal["run"]


def test_the_record_step_reads_the_seal_result_only_after_a_seal_step_that_succeeded():
    """A seal step that failed wrote no seal result of its own: the lane
    fails its step exactly when it could not (`SEAL_RESULT_UNWRITTEN_EXIT`).
    Whatever sits at the result's path then is not the lane's, so the record
    step neither reads a reason from it nor hands it on as a strict verdict
    (Copilot, PR #1166)."""
    steps = _finalize_steps()
    skip = steps[_step_index(
        steps,
        name="Ideation-dashboard image refresh — record skip (source not sealed)",
    )]
    assert skip["env"]["SEAL_OUTCOME"] == "${{ steps.dfr-seal.outcome }}"
    run = skip["run"]
    failed = run.index('elif [ "$SEAL_OUTCOME" != "success" ]; then')
    assert run.index('if [ "$SEALED" = "true" ]; then') < failed
    assert failed < run.index('open("dfr-seal-result.json")')
    assert run.index("STRICT=false") < failed


def _job_steps(job: str) -> list[dict]:
    import yaml
    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml")
        .read_text(encoding="utf-8"))
    return workflow["jobs"][job]["steps"]


def test_the_finalize_job_mounts_both_products_and_their_legs():
    """#1161: every lane of `finalize` that renders or validates a snapshot
    reaches the products' legs, and the seal carries them. So `finalize` inits
    each product and each product's two legs, BY NAME (never `--recursive`,
    which would admit a leg's own submodules), each guarded on the
    `.gitmodules` that declares it. `prepare` reads neither product and inits
    neither."""
    finalize = _job_steps("finalize")
    run = finalize[_step_index(finalize, name="Init governed submodules only")]["run"]
    block = run[run.index("for product in openDox openXdox; do"):]
    assert '--get "submodule.${product}.path"' in block
    assert 'git -C openxFactory submodule update --init "$product"' in block
    assert "for leg in spec code; do" in block
    assert '--get "submodule.${leg}.path"' in block
    assert 'git -C "openxFactory/${product}" submodule update --init "$leg"' in block
    assert "--recursive" not in block
    assert {gitlink for gitlink, _leg, _pkg in lane.RENDER_LEGS} == \
        {"openDox", "openXdox"}
    assert {leg for _gitlink, leg, _pkg in lane.RENDER_LEGS} <= {"spec", "code"}
    # The mount precedes every step that reaches a product.
    mount = _step_index(finalize, name="Init governed submodules only")
    assert mount < _step_index(finalize, id="dfr-seal")
    prepare = _job_steps("prepare")
    prepare_run = prepare[_step_index(
        prepare, name="Init governed submodules only")]["run"]
    assert "openDox" not in prepare_run and "openXdox" not in prepare_run


def test_the_refresh_stage_materializes_nothing_by_a_worker_side_read():
    """The stage's own steps are the parent's. No step in it may introduce a
    second source materialization — the seal is the one place source crosses,
    and a `git clone` appearing anywhere in this stage would be the
    contradiction the re-realization exists to remove."""
    steps = _finalize_steps()
    first = _step_index(steps, id="dfr-readiness")
    stage = steps[first:_step_index(steps, id="dfr-dispatch") + 1]
    for step in stage:
        run = step.get("run") or ""
        assert "git clone" not in run, step.get("name")
        assert "GIT_SSH_COMMAND" not in run, step.get("name")
        assert "sparse-checkout" not in run, step.get("name")


# ---------------------------------------------------------------------------
# the render legs (#1161) — sealed at the commits the SEALED corpus pins, from
# real nested submodules, and refused whenever this parent holds anything else
# ---------------------------------------------------------------------------

def _product(where: Path, name: str, code_leg: str, package: str, *,
             omit: tuple[str, ...] = ()) -> Path:
    """A product shaped like openDox or openXdox: a repository whose `spec`
    and `code` legs are its own submodules. The code leg carries its package
    under `src/`, a module BESIDE the package (openXdox-code's `src/` has two),
    and a `tests/` tree and a `pyproject.toml` the render unit must not carry.
    openXdox's code leg also commits a stand-in validator unit, which a test
    resolves its validator from, as a real parent resolves the real one from
    the same checkout as its render legs. Every code leg carries the modules
    the render unit imports by name, less any in `omit`."""
    legs: dict[str, Path] = {}
    for leg in ("spec", code_leg):
        repo = where / f"{name}-{leg}"
        repo.mkdir(parents=True)
        _git(repo, "init", "--quiet", "-b", "main")
        if leg == code_leg:
            modules = repo / "src" / package
            modules.mkdir(parents=True)
            (modules / "__init__.py").write_text(f'"""{package}"""\n',
                                                 encoding="utf-8")
            (modules / "cli.py").write_text(
                "def main(argv=None):\n    return 0\n", encoding="utf-8")
            for module in _named_leg_modules(name, code_leg):
                if module not in ("cli.py", lane.SEALED_PRODUCT_MODULE):
                    (modules / module).write_text(
                        f'"""{package}.{module[:-3]}"""\n', encoding="utf-8")
            if package == "openxdox":
                # The product module the parent classifies with, out of the
                # sealed leg, and a stand-in validator unit outside `src/`,
                # which the leg sealer never archives.
                (modules / lane.SEALED_PRODUCT_MODULE).write_text(
                    PRODUCT_MODULE_TEXT, encoding="utf-8")
                script = repo / lane.VALIDATOR_SCRIPT_PATH
                script.parent.mkdir(parents=True)
                script.write_text(STUB_SCRIPT, encoding="utf-8")
                schemas = repo / lane.VALIDATOR_SCHEMAS_PATH
                schemas.mkdir(parents=True)
                (schemas / STUB_SCHEMA).write_text("{}\n", encoding="utf-8")
            (repo / "src" / "extension.py").write_text(
                "# beside the package\n", encoding="utf-8")
            (repo / "tests").mkdir()
            (repo / "tests" / "test_leg.py").write_text("# never sealed\n",
                                                        encoding="utf-8")
            (repo / "pyproject.toml").write_text(
                f'[project]\nname = "{package}"\n', encoding="utf-8")
        else:
            (repo / "README.md").write_text(f"# {name} spec\n", encoding="utf-8")
        for module in omit:
            (repo / "src" / package / module).unlink(missing_ok=True)
        _git(repo, "add", "-A")
        _git(repo, "commit", "--quiet", "-m", f"{name} {leg}")
        legs[leg] = repo
    product = where / name
    product.mkdir(parents=True)
    _git(product, "init", "--quiet", "-b", "main")
    (product / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    _git(product, "add", "README.md")
    for leg, repo in legs.items():
        _git(product, "-c", "protocol.file.allow=always", "submodule", "add",
             "--quiet", str(repo), leg)
    _git(product, "commit", "--quiet", "-m", name)
    return product


def _mount_products(corpus: Path, upstream: Path, *,
                    omit: dict[str, tuple[str, ...]] | None = None) -> Path:
    """Mount both products in `corpus`, as openxFactory mounts them: each a
    gitlink, each product's legs its own gitlinks, all materialized at the
    commits they are pinned at. `omit` leaves modules out of a product's code
    leg, by gitlink."""
    for gitlink, leg, package in lane.RENDER_LEGS:
        product = _product(upstream, gitlink, leg, package,
                           omit=(omit or {}).get(gitlink, ()))
        _git(corpus, "-c", "protocol.file.allow=always", "submodule", "add",
             "--quiet", str(product), gitlink)
    _git(corpus, "-c", "protocol.file.allow=always", "submodule", "update",
         "--init", "--recursive", "--quiet")
    _git(corpus, "commit", "--quiet", "-m", "mount the products")
    return corpus


@pytest.fixture
def corpus_with_products(corpus: Path, tmp_path: Path) -> Path:
    """The fixture corpus with both products MOUNTED (`_mount_products`)."""
    return _mount_products(corpus, tmp_path / "upstream")


def _product_leg_src(package: str, gitlink: str, leg: str) -> list[str]:
    """What `_product` puts under a code leg's `src/`, as leg-relative paths."""
    return sorted({"src/extension.py", f"src/{package}/__init__.py",
                   f"src/{package}/cli.py",
                   *(f"src/{package}/{module}"
                     for module in _named_leg_modules(gitlink, leg))})


def _leg_files(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix()
                  for path in root.rglob("*") if path.is_file())


def test_the_legs_are_sealed_at_the_commits_the_sealed_corpus_pins(
        corpus_with_products, tmp_path):
    """Each product's commit is read out of `source_head`'s own tree, each leg's
    out of THAT product commit's tree, and each leg's `src/` is archived at its
    commit: the package and the modules beside it, and nothing else of the
    product (no `tests/`, no `pyproject.toml`, no `spec` leg)."""
    corpus = corpus_with_products
    head = _git(corpus, "rev-parse", "HEAD")
    corpus_root = tmp_path / "seal" / lane.SEAL_CORPUS_RELPATH
    records = lane.seal_render_legs(corpus_checkout=corpus, source_head=head,
                                    corpus_root=corpus_root)
    assert [(record["gitlink"], record["leg"], record["package"])
            for record in records] == list(lane.RENDER_LEGS)
    for record in records:
        gitlink, leg, package = record["gitlink"], record["leg"], record["package"]
        pinned = _git(corpus, "rev-parse", f"{head}:{gitlink}")
        assert record["gitlink_revision"] == pinned
        assert record["leg_revision"] == \
            _git(corpus / gitlink, "rev-parse", f"{pinned}:{leg}")
        assert record["relpath"] == f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/{leg}"
        assert record["paths"] == ["src"]
        # The schema leg is held to its pin and recorded, never sealed.
        assert record["schema_leg"] == lane.SCHEMA_LEG
        assert record["schema_leg_revision"] == \
            _git(corpus / gitlink, "rev-parse", f"{pinned}:{lane.SCHEMA_LEG}")
        sealed = corpus_root / gitlink / leg
        carried = _product_leg_src(package, gitlink, leg)
        assert _leg_files(sealed) == carried
        assert record["file_count"] == len(carried)
        assert sorted(path.name for path in (corpus_root / gitlink).iterdir()) \
            == [leg]
    assert sorted(path.name for path in corpus_root.iterdir()) == \
        sorted(lane.RENDER_LEG_GITLINKS)


def test_a_seal_with_real_legs_verifies(corpus_with_products, tmp_path):
    """Real legs, and a validator resolved from the materialized openXdox code
    leg, as a real parent resolves it. The seal records the leg's own commit
    as the validator's revision, and it verifies."""
    corpus = corpus_with_products
    head = _git(corpus, "rev-parse", "HEAD")
    leg = corpus / "openXdox" / "code"
    unit = lane.PinnedValidator(runnable=leg / lane.VALIDATOR_SCRIPT_PATH,
                                product_root=leg)
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, seal_legs=None,
                     resolve_validator=lambda: unit)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []
    assert manifest["validator_revision"] == _git(leg, "rev-parse", "HEAD") \
        == manifest["render_legs"][1]["leg_revision"]
    legs = [key for key in manifest["files"]
            if key.split("/")[1:2] in (["openDox"], ["openXdox"])]
    assert len(legs) == sum(record["file_count"]
                            for record in manifest["render_legs"]) == sum(
        len(_product_leg_src(package, gitlink, leg))
        for gitlink, leg, package in lane.RENDER_LEGS)


def _commit_inside(checkout: Path) -> str:
    (checkout / "drift.txt").write_text("a commit the corpus does not pin\n",
                                        encoding="utf-8")
    _git(checkout, "add", "drift.txt")
    _git(checkout, "commit", "--quiet", "-m", "drift")
    return _git(checkout, "rev-parse", "HEAD")


@pytest.mark.parametrize("shape", [
    "no-gitlink", "product-not-materialized", "product-at-another-commit",
    "leg-not-materialized", "leg-at-another-commit",
    "schema-leg-not-materialized", "schema-leg-at-another-commit"])
def test_a_leg_this_parent_does_not_hold_at_its_pin_is_refused(
        corpus, tmp_path, shape, request):
    """NOTHING IS FETCHED. The legs are the ones this parent materialized, and
    a parent holding anything other than exactly the commits `source_head`
    pins refuses, naming both, before the corpus is archived. Sealing main's
    corpus with a renderer main does not pin would publish a snapshot no pin
    describes."""
    if shape != "no-gitlink":
        corpus = request.getfixturevalue("corpus_with_products")
    head = _git(corpus, "rev-parse", "HEAD")
    pinned = (_git(corpus, "rev-parse", f"{head}:openXdox")
              if shape != "no-gitlink" else None)
    if shape == "product-not-materialized":
        _git(corpus, "submodule", "deinit", "--quiet", "--force", "openXdox")
    elif shape == "product-at-another-commit":
        moved = _commit_inside(corpus / "openXdox")
    elif shape == "leg-not-materialized":
        _git(corpus / "openXdox", "submodule", "deinit", "--quiet", "--force",
             "code")
    elif shape == "leg-at-another-commit":
        leg_pin = _git(corpus / "openXdox", "rev-parse", f"{pinned}:code")
        moved = _commit_inside(corpus / "openXdox" / "code")
    elif shape == "schema-leg-not-materialized":
        _git(corpus / "openXdox", "submodule", "deinit", "--quiet", "--force",
             "spec")
    elif shape == "schema-leg-at-another-commit":
        leg_pin = _git(corpus / "openXdox", "rev-parse", f"{pinned}:spec")
        moved = _commit_inside(corpus / "openXdox" / "spec")
    seal = tmp_path / "seal"
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, seal_legs=None)
    reason = str(refused.value)
    short = lane._short
    if shape == "no-gitlink":
        expected = f"{short(head)} pins no openDox gitlink"
    elif shape == "product-not-materialized":
        expected = ("the pinned openXdox product is not materialized at "
                    f"{corpus / 'openXdox'}")
    elif shape == "product-at-another-commit":
        expected = (f"this parent's openXdox is at {short(moved)}, but "
                    f"{short(head)} pins openXdox@{short(pinned)}")
    elif shape == "leg-not-materialized":
        expected = ("the openXdox code leg is not materialized at "
                    f"{corpus / 'openXdox' / 'code'}")
    elif shape == "leg-at-another-commit":
        expected = (f"this parent's openXdox/code is at {short(moved)}, but "
                    f"openXdox@{short(pinned)} pins it at {short(leg_pin)}")
    elif shape == "schema-leg-not-materialized":
        expected = ("the openXdox spec leg is not materialized at "
                    f"{corpus / 'openXdox' / 'spec'}, and the sealed "
                    "validator's schemas are composed from it")
    else:
        expected = (f"this parent's openXdox/spec is at {short(moved)}, but "
                    f"openXdox@{short(pinned)} pins it at {short(leg_pin)} — "
                    "the seal would carry schemas its product does not pin")
    assert reason.startswith(expected), reason
    if shape in ("product-not-materialized", "leg-not-materialized",
                 "schema-leg-not-materialized"):
        assert "git submodule update --init --recursive openDox openXdox" in reason
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()
    # Found out BEFORE the corpus is archived: no corpus path was extracted.
    assert not (seal / lane.SEAL_CORPUS_RELPATH / "docs").exists()


def test_a_leg_archive_naming_another_commit_is_refused(corpus_with_products,
                                                        tmp_path, monkeypatch):
    """The leg archive's own recorded commit is checked, as the corpus half's
    is: a leg whose bytes came from another commit than the one its record
    names must not be sealed."""
    monkeypatch.setattr(lane, "git_archive_revision", lambda _path: "f" * 40)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus_with_products, tmp_path / "seal", seal_legs=None)
    assert str(refused.value).startswith(
        f"the openDox code leg archive's own recorded revision ({'f' * 40}) is "
        "not its pinned commit")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_validator_from_another_product_revision_is_refused(
        corpus_with_products, tmp_path):
    """ONE PRODUCT REVISION. The REAL resolver copies the validator out of the
    real openXdox code leg this suite runs against, while these legs are the
    fixture's own. A real parent reads both through one checkout. A parent
    whose two disagree would have the child judge the snapshot with a product
    revision its render did not use, so it is refused."""
    corpus = corpus_with_products
    head = _git(corpus, "rev-parse", "HEAD")
    pinned = _git(corpus, "rev-parse", f"{head}:openXdox")
    leg = _git(corpus / "openXdox", "rev-parse", f"{pinned}:code")
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", seal_legs=None, resolve_validator=None)
    assert str(refused.value).startswith(
        f"the sealed validator was copied from openXdox code at "
        f"{lane._short(_product_head())}, but the sealed render unit carries it "
        f"at {lane._short(leg)}")
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_leg_sealer_speaks_only_git(corpus_with_products, tmp_path):
    """The legs are read with `ls-tree`, `rev-parse` and `archive`, in
    checkouts this parent already holds: no fetch, no clone, no submodule
    command, and nothing that is not git."""
    runner = RecordingRunner()
    corpus = corpus_with_products
    lane.seal_render_legs(corpus_checkout=corpus,
                          source_head=_git(corpus, "rev-parse", "HEAD"),
                          corpus_root=tmp_path / "seal" / "openxFactory",
                          runner=runner)
    assert runner.calls
    assert all(argv[0] == "git" for argv in runner.calls)
    assert {_verb(argv) for argv in runner.calls} == {"ls-tree", "rev-parse",
                                                      "archive"}
    _assert_exact_reads(runner)


def test_ambient_git_redirection_cannot_change_what_is_sealed(
        corpus_with_products, tmp_path, monkeypatch):
    """The seal's reads are EXACT-CONTENT reads (Copilot, PR #1166). Here the
    pinned openXdox leg commit has a REPLACE REF naming another commit with
    other bytes, and the job's environment names another repository, another
    object store and a replace-ref base. A plain read would follow either one
    and still record the pinned commit's name. The seal holds the pinned
    commit's own bytes."""
    corpus = corpus_with_products
    head = _git(corpus, "rev-parse", "HEAD")
    pinned = _git(corpus, "rev-parse", f"{head}:openXdox")
    leg_dir = corpus / "openXdox" / "code"
    leg_pin = _git(corpus / "openXdox", "rev-parse", f"{pinned}:code")
    module = leg_dir / "src" / "openxdox" / "__init__.py"
    genuine = module.read_bytes()
    module.write_text("# the REPLACEMENT's bytes\n", encoding="utf-8")
    _git(leg_dir, "commit", "--quiet", "-am", "a replacement")
    replacement = _git(leg_dir, "rev-parse", "HEAD")
    _git(leg_dir, "checkout", "--quiet", "--detach", leg_pin)
    _git(leg_dir, "replace", leg_pin, replacement)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    _git(elsewhere, "init", "--quiet", "-b", "main")
    # From here on, no fixture git runs: the environment is the job's.
    monkeypatch.setenv("GIT_DIR", str(elsewhere / ".git"))
    monkeypatch.setenv("GIT_OBJECT_DIRECTORY", str(elsewhere / ".git" / "objects"))
    monkeypatch.setenv("GIT_ALTERNATE_OBJECT_DIRECTORIES",
                       str(elsewhere / ".git" / "objects"))
    monkeypatch.setenv("GIT_REPLACE_REF_BASE", "refs/replace/")
    corpus_root = tmp_path / "seal" / lane.SEAL_CORPUS_RELPATH
    records = lane.seal_render_legs(corpus_checkout=corpus, source_head=head,
                                    corpus_root=corpus_root)
    assert [record["leg_revision"] for record in records][1] == leg_pin
    sealed = corpus_root / "openXdox" / "code" / "src" / "openxdox" / "__init__.py"
    assert sealed.read_bytes() == genuine


def test_verify_refuses_a_seal_whose_render_unit_is_not_whole(corpus, tmp_path):
    """The intake requires the RENDER unit too. Each tamper is made coherent,
    the index and the tree digest recomputed, so the digest check alone would
    pass it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert lane.verify_seal(seal) == []
    base = json.loads(json.dumps(manifest))
    modules = f"{lane.SEAL_CORPUS_RELPATH}/openXdox/code/src/openxdox/"

    def problems(mutate) -> list[str]:
        candidate = json.loads(json.dumps(base))
        mutate(candidate)
        (seal / lane.SEAL_MANIFEST_NAME).write_text(
            json.dumps(candidate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        return lane.verify_seal(seal)

    assert problems(lambda m: m.update(render_entry="scripts/other.py")) == [
        "render_entry is 'scripts/other.py', expected "
        f"{lane.RENDER_ENTRY!r} — the child would have no renderer to run"]
    assert problems(lambda m: m["render_legs"].reverse()) == [
        f"render_legs records "
        f"{[(g, l, p) for g, l, p in reversed(lane.RENDER_LEGS)]!r}, expected "
        f"{list(lane.RENDER_LEGS)!r}"]
    assert problems(lambda m: m["render_legs"][1].update(
        leg_revision="abc1234")) == [
        "the openXdox code leg records leg_revision 'abc1234', expected a "
        "full commit revision"]
    assert problems(lambda m: m["render_legs"][0].update(file_count=99)) == [
        "the openDox code leg records file_count 99, but the seal indexes "
        f"{base['render_legs'][0]['file_count']} file(s) under "
        "openxFactory/openDox/code/"]
    assert problems(lambda m: m.update(precheck=dict(
        STUB_PRECHECK, outcome="not-conformant")))[0].startswith(
        "precheck is ")
    assert problems(lambda m: m.update(validator_revision="1" * 40)) == [
        f"validator_revision {'1' * 40!r} is not the sealed openXdox code "
        f"leg's revision {base['render_legs'][1]['leg_revision']!r}"]
    # And the modules themselves: the leg's package emptied, coherently.
    shutil.rmtree(seal / modules)
    candidate = json.loads(json.dumps(base))
    candidate["files"] = lane.seal_file_index(seal)
    candidate["tree_digest"] = lane.tree_digest(candidate["files"])
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == [
        f"the seal indexes no module under {modules} — the child's render "
        "could not import it",
        "the openXdox code leg records file_count "
        f"{base['render_legs'][1]['file_count']}, but the seal indexes 0 "
        "file(s) under openxFactory/openXdox/code/"]


@pytest.mark.parametrize("stray", ["openDox/code/tests/test_leg.py",
                                   "openXdox/code/pyproject.toml"])
def test_verify_refuses_a_leg_carrying_anything_beside_its_src(corpus,
                                                               tmp_path,
                                                               stray):
    """A leg is sealed as its `src/` alone. A file of the leg outside `src/`
    is refused even when the leg's `file_count` counts it, since the count
    alone cannot tell the render unit from a wider tree (Copilot,
    opensoft/xFactory PR #526)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    extra = seal / lane.SEAL_CORPUS_RELPATH / stray
    extra.parent.mkdir(parents=True, exist_ok=True)
    extra.write_text("# beside src\n", encoding="utf-8")
    gitlink = stray.split("/")[0]
    for record in manifest["render_legs"]:
        if record["gitlink"] == gitlink:
            record["file_count"] += 1
    _rewrite_coherently(seal, manifest)
    root = f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/code"
    assert lane.verify_seal(seal) == [
        f"the {gitlink} code leg indexes 1 file(s) outside {root}/src/ "
        f"({lane.SEAL_CORPUS_RELPATH}/{stray}), and a leg is sealed as its "
        "src/ alone"]


@pytest.mark.parametrize("change, said", [
    ({"schema_leg": None}, "records schema_leg None, expected 'spec'"),
    ({"schema_leg": "code"}, "records schema_leg 'code', expected 'spec'"),
    ({"schema_leg_revision": "f088b09"},
     "records schema_leg_revision 'f088b09', expected a full commit revision"),
    ({"schema_leg_revision": None},
     "records schema_leg_revision None, expected a full commit revision"),
], ids=["no-schema-leg", "another-schema-leg", "abbreviated-revision",
        "no-revision"])
def test_verify_refuses_a_leg_without_its_schema_provenance(corpus, tmp_path,
                                                            change, said):
    """The sealed validator's schemas come from each product's schema leg, so
    the manifest's record of that leg's pinned revision is required, not
    optional (Copilot, PR #1166)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    manifest["render_legs"][1].update(change)
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [f"the openXdox code leg {said}"]


def test_the_render_leg_modules_are_what_the_render_unit_imports_by_name():
    """THE MODULES THE INTAKE REQUIRES BY NAME (Copilot, PR #1166) are exactly
    the product modules the seal's own corpus side imports by name, read here
    with `ast` out of the entry and the four files of its host bootstrap, and
    the module the lane classifies the sealed validator's runs with. A render
    unit that grows such an import grows the requirement, or this fails. Each
    is a module the real legs carry at their pins."""
    package_leg = {package: (gitlink, leg)
                   for gitlink, leg, package in lane.RENDER_LEGS}
    named: dict[tuple[str, str], set[str]] = {key: set()
                                              for key in package_leg.values()}
    for relpath in (lane.RENDER_ENTRY, *lane.RENDER_BOOTSTRAP):
        tree = ast.parse((REPO_ROOT / relpath).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.ImportFrom) and node.level == 0
                    and node.module):
                top, _, rest = node.module.partition(".")
                if top in package_leg:
                    named[package_leg[top]].update(
                        [f"{rest.split('.')[0]}.py"] if rest
                        else [f"{alias.name}.py" for alias in node.names])
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    top, _, rest = alias.name.partition(".")
                    if top in package_leg and rest:
                        named[package_leg[top]].add(f"{rest.split('.')[0]}.py")
    named[lane.VALIDATOR_LEG].add(lane.SEALED_PRODUCT_MODULE)
    assert {key: tuple(sorted(modules))
            for key, modules in named.items()} == RENDER_UNIT_IMPORTS
    assert lane.RENDER_LEG_MODULES == RENDER_UNIT_IMPORTS
    for gitlink, leg, package in lane.RENDER_LEGS:
        for module in RENDER_UNIT_IMPORTS[(gitlink, leg)]:
            assert (REPO_ROOT / gitlink / leg / "src" / package / module
                    ).is_file(), (gitlink, module)


@pytest.mark.parametrize("gitlink, module", [
    (gitlink, module) for (gitlink, _leg), modules in RENDER_UNIT_IMPORTS.items()
    for module in modules])
def test_verify_refuses_a_leg_without_a_module_the_render_unit_imports(
        corpus, tmp_path, gitlink, module):
    """The intake asked each product's package for SOME module, so a leg that
    had lost `opendox/cli.py`, or a module the host bootstrap or the verdict
    classifier imports, passed it and failed only at the child's import
    (Copilot, PR #1166). Each such module is required by name, as the corpus
    side's bootstrap is. The removal is made coherent, so only the
    requirement can see it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    package = next(package for name, _leg, package in lane.RENDER_LEGS
                   if name == gitlink)
    relpath = f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/code/src/{package}/{module}"
    (seal / relpath).unlink()
    for record in manifest["render_legs"]:
        if record["gitlink"] == gitlink:
            record["file_count"] -= 1
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        f"the seal does not carry {relpath}, which the render unit imports "
        "by name"]


def test_the_serve_leg_modules_are_what_the_serve_entry_imports_by_name():
    """THE SERVE ENTRY'S NAMED IMPORTS (#1164, seal 2.2.0). The product modules
    the serve entry and its host bootstrap import by name, read with `ast`,
    less those the render unit already requires, are exactly
    `SERVE_LEG_MODULES`: today `opendox.serve`, which the image starts. So a
    serve entry that grows such an import grows the requirement, or this
    fails, and no module is required twice. Each is a module the real legs
    carry at their pins."""
    package_leg = {package: (gitlink, leg)
                   for gitlink, leg, package in lane.RENDER_LEGS}
    named: dict[tuple[str, str], set[str]] = {key: set()
                                              for key in package_leg.values()}
    for relpath in (lane.SERVE_ENTRY, *lane.RENDER_BOOTSTRAP):
        tree = ast.parse((REPO_ROOT / relpath).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.ImportFrom) and node.level == 0
                    and node.module):
                top, _, rest = node.module.partition(".")
                if top in package_leg:
                    named[package_leg[top]].update(
                        [f"{rest.split('.')[0]}.py"] if rest
                        else [f"{alias.name}.py" for alias in node.names])
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    top, _, rest = alias.name.partition(".")
                    if top in package_leg and rest:
                        named[package_leg[top]].add(f"{rest.split('.')[0]}.py")
    beyond = {key: tuple(sorted(modules - set(RENDER_UNIT_IMPORTS[key])))
              for key, modules in named.items()}
    assert {key: modules for key, modules in beyond.items() if modules} == \
        SERVE_UNIT_IMPORTS
    assert lane.SERVE_LEG_MODULES == SERVE_UNIT_IMPORTS
    for gitlink, leg, package in lane.RENDER_LEGS:
        for module in SERVE_UNIT_IMPORTS.get((gitlink, leg), ()):
            assert (REPO_ROOT / gitlink / leg / "src" / package / module
                    ).is_file(), (gitlink, module)


@pytest.mark.parametrize("gitlink, module", [
    (gitlink, module) for (gitlink, _leg), modules in SERVE_UNIT_IMPORTS.items()
    for module in modules])
def test_verify_refuses_a_leg_without_a_module_the_serve_entry_imports(
        corpus, tmp_path, gitlink, module):
    """The serve entry imports `opendox.serve` by name, so a leg that lost it
    would pass an intake that asked the render unit's questions only, and the
    image would fail at start. It is required by name, once. The removal is
    made coherent, so only the requirement can see it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    package = next(package for name, _leg, package in lane.RENDER_LEGS
                   if name == gitlink)
    relpath = f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/code/src/{package}/{module}"
    (seal / relpath).unlink(missing_ok=True)
    for record in manifest["render_legs"]:
        if record["gitlink"] == gitlink:
            record["file_count"] = sum(
                1 for path in (seal / record["relpath"]).rglob("*")
                if path.is_file())
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        f"the seal does not carry {relpath}, which the serve entry imports "
        "by name"]


@pytest.mark.parametrize("gitlink, module", [
    (gitlink, module) for (gitlink, _leg), modules in SERVE_UNIT_IMPORTS.items()
    for module in modules])
def test_a_leg_without_a_module_the_serve_entry_imports_is_refused(
        corpus, tmp_path, gitlink, module):
    """The leg sealer refuses first what the intake refuses: a product whose
    pinned code leg lacks a module the serve entry imports by name is never
    sealed, and the refusal names the module."""
    _mount_products(corpus, tmp_path / "upstream", omit={gitlink: (module,)})
    package = next(package for name, _leg, package in lane.RENDER_LEGS
                   if name == gitlink)
    head = _git(corpus, "rev-parse", "HEAD")
    with pytest.raises(lane.SealRefused) as refused:
        lane.seal_render_legs(
            corpus_checkout=corpus, source_head=head,
            corpus_root=tmp_path / "seal" / lane.SEAL_CORPUS_RELPATH)
    assert str(refused.value) == (
        f"the sealed {gitlink} code leg carries no src/{package}/{module}, "
        "which the serve entry imports by name, so the image the child builds "
        "could not start")


@pytest.mark.parametrize("gitlink, module", [("openDox", "domain_profile.py"),
                                             ("openXdox", "serve_gate.py")])
def test_a_leg_without_a_module_the_render_unit_imports_is_refused(
        corpus, tmp_path, gitlink, module):
    """The leg sealer refuses first what the intake refuses: a product whose
    pinned code leg lacks a module the render unit imports by name is never
    sealed, and the refusal names the module."""
    _mount_products(corpus, tmp_path / "upstream", omit={gitlink: (module,)})
    package = next(package for name, _leg, package in lane.RENDER_LEGS
                   if name == gitlink)
    head = _git(corpus, "rev-parse", "HEAD")
    with pytest.raises(lane.SealRefused) as refused:
        lane.seal_render_legs(
            corpus_checkout=corpus, source_head=head,
            corpus_root=tmp_path / "seal" / lane.SEAL_CORPUS_RELPATH)
    assert str(refused.value).startswith(
        f"the sealed {gitlink} code leg carries no src/{package}/{module}, "
        "which the render unit imports by name"), str(refused.value)


def test_the_render_bootstrap_is_what_the_entry_imports_first():
    """The four host-bootstrap files the entry imports before it reaches
    either product: the render paths less the gitlinks and the entry."""
    assert lane.RENDER_BOOTSTRAP == (
        "scripts/carved_reach.py", "scripts/opendox_host.py",
        "scripts/profile_openxfactory.py", "scripts/wire_messages.py")


@pytest.mark.parametrize("dropped", lane.RENDER_BOOTSTRAP)
def test_verify_refuses_a_seal_missing_a_bootstrap_file(corpus, tmp_path,
                                                         dropped):
    """The entry imports its host bootstrap before either product, so a seal
    without one of those files would pass an intake that checked the entry
    alone and fail only once the render started (Copilot, opensoft/xFactory
    PR #526). The removal is made coherent, so only the requirement can see
    it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    (seal / lane.SEAL_CORPUS_RELPATH / dropped).unlink()
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        f"the seal does not carry {lane.SEAL_CORPUS_RELPATH}/{dropped}, which "
        "the renderer imports before it reaches either product"]


def test_verify_refuses_the_2_0_layout_that_carried_no_render_unit(corpus,
                                                                   tmp_path):
    """A 2.0.0 seal (#1162) carried the validator unit and no render unit. The
    major is the same, so it is read, and it is refused for exactly what it
    lacks, each named: the child could not render from it, and it lacks what
    a 2.1 seal lacks too, the corpus-schema record and the serve unit."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    shutil.rmtree(seal / lane.SEAL_CORPUS_RELPATH / "openDox")
    shutil.rmtree(seal / lane.SEAL_CORPUS_RELPATH / "openXdox")
    (seal / lane.SEAL_CORPUS_RELPATH / lane.RENDER_ENTRY).unlink()
    (seal / lane.SEAL_CORPUS_RELPATH / SERVE_ENTRY).unlink()
    for field in ("render_entry", "render_legs", "precheck", "serve_entry",
                  "serve_unit", "validator_corpus_schemas"):
        del manifest[field]
    manifest["schema_version"] = "2.0.0"
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        NO_CORPUS_SCHEMAS,
        f"render_entry is None, expected {lane.RENDER_ENTRY!r} — the child "
        "would have no renderer to run",
        "render_legs is None — the seal records no render unit, so the "
        "child's render would reach no product",
        f"serve_entry is None, expected {SERVE_ENTRY!r} — the image the child "
        "builds could not start",
        "serve_unit is None — the seal records no serve unit, so the image the "
        "child builds could not start"]


# ---------------------------------------------------------------------------
# the serve unit (#1164, seal 2.2.0) — what the served image's recipe copies
# out of the context the child assembles from the seal, to start the image
# ---------------------------------------------------------------------------

def test_verify_refuses_the_2_1_layout_that_carried_no_serve_unit(corpus,
                                                                  tmp_path):
    """A 2.1.0 seal (#1166) carried the render unit, but not the serve's entry,
    named no serve unit, and recorded none of its validator's schemas as the
    corpus's. The major is the same, so it is read, and it is refused for
    exactly what it lacks, each named: the child could not hold the
    validator to the sealed corpus, and the image built from it could not
    start (#1164). So 2.2.0 is the floor, by those named lacks rather than by
    a version comparison, as 2.1 was for a 2.0 seal. The fixture keeps a real
    2.1 seal's shape, which predates all three fields, so it lacks all three.
    Each lack is also refused alone, by the serve record's and the corpus
    schemas' own tests (Copilot, PR #1179)."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    (seal / lane.SEAL_CORPUS_RELPATH / SERVE_ENTRY).unlink(missing_ok=True)
    for field in ("serve_entry", "serve_unit", "validator_corpus_schemas"):
        manifest.pop(field, None)
    manifest["schema_version"] = "2.1.0"
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        NO_CORPUS_SCHEMAS,
        f"serve_entry is None, expected {SERVE_ENTRY!r} — the image the child "
        "builds could not start",
        "serve_unit is None — the seal records no serve unit, so the image the "
        "child builds could not start"]


_NO_CARVE_MANIFEST = [path for path in SERVE_UNIT
                      if path != "docs/opendox-carve-manifest.yaml"]


@pytest.mark.parametrize("field, value, said", [
    ("serve_entry", _ABSENT,
     f"serve_entry is None, expected {SERVE_ENTRY!r} — the image the child "
     "builds could not start"),
    ("serve_entry", "scripts/ideation-dashboard-cli.py",
     "serve_entry is 'scripts/ideation-dashboard-cli.py', expected "
     f"{SERVE_ENTRY!r} — the image the child builds could not start"),
    ("serve_unit", _ABSENT,
     "serve_unit is None — the seal records no serve unit, so the image the "
     "child builds could not start"),
    ("serve_unit", "scripts",
     "serve_unit is 'scripts' — the seal records no serve unit, so the image "
     "the child builds could not start"),
    ("serve_unit", list(reversed(SERVE_UNIT)),
     f"serve_unit records {list(reversed(SERVE_UNIT))!r}, expected "
     f"{list(SERVE_UNIT)!r}"),
    ("serve_unit", _NO_CARVE_MANIFEST,
     f"serve_unit records {_NO_CARVE_MANIFEST!r}, expected "
     f"{list(SERVE_UNIT)!r}"),
], ids=["no-serve-entry", "the-render-entry-named-as-the-serve-entry",
        "no-serve-unit", "not-a-list", "out-of-order", "a-path-left-out"])
def test_verify_holds_the_serve_record_to_the_readers_own(corpus, tmp_path,
                                                          field, value, said):
    """The manifest names the serve unit, and the intake holds that record to
    its OWN `SERVE_ENTRY` and `SERVE_UNIT`. A parent and a child that disagree
    about what the image copies, or a tampered record, is refused by name.
    The files are untouched, so the record is the only thing wrong: a record
    that leaves a path out changes nothing about what the intake requires."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    if value is _ABSENT:
        manifest.pop(field, None)
    else:
        manifest[field] = value
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == [said]


def test_verify_refuses_a_serve_entry_the_seal_does_not_carry(corpus,
                                                              tmp_path):
    """Named is not carried: the entry the served image starts must be
    indexed. The removal is made coherent, so only the requirement can see
    it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    (seal / lane.SEAL_CORPUS_RELPATH / SERVE_ENTRY).unlink(missing_ok=True)
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        f"the seal does not carry {lane.SEAL_CORPUS_RELPATH}/{SERVE_ENTRY}, "
        "the entry the served image starts"]


@pytest.mark.parametrize("path", SERVE_ONLY)
def test_verify_refuses_a_seal_missing_a_serve_only_path(corpus, tmp_path,
                                                          path):
    """The recipe copies each of these out of the context the child assembles
    from the seal, so a seal that lacks one builds no image, and the render
    unit names none of them. So the serve unit requires them, by the reader's
    own list, whatever the manifest records: a file must be indexed, and a
    tree must hold an indexed file. The removal is made coherent, so only the
    requirement can see it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    target = seal / lane.SEAL_CORPUS_RELPATH / path
    if path.endswith("/"):
        shutil.rmtree(target)
        said = (f"the seal indexes no file under {lane.SEAL_CORPUS_RELPATH}/"
                f"{path}, which the served image's recipe copies")
    else:
        target.unlink()
        said = (f"the seal does not carry {lane.SEAL_CORPUS_RELPATH}/{path}, "
                "which the served image's recipe copies")
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [said]


@pytest.mark.parametrize("path", SERVE_UNIT)
def test_every_serve_unit_path_is_required_once(corpus, tmp_path, path):
    """THE WHOLE UNIT IS REQUIRED, EACH PATH ONCE. Whichever check names it,
    the serve entry's, the render unit's (the host bootstrap, and the legs'
    `src/`) or the serve unit's own, a seal that lacks any path of the unit
    is refused by exactly one problem naming that path. The removal is made
    coherent, so only the requirement can see it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    target = seal / lane.SEAL_CORPUS_RELPATH / path
    if path.endswith("/"):
        shutil.rmtree(target)
    else:
        target.unlink(missing_ok=True)
    _rewrite_coherently(seal, manifest)
    problems = lane.verify_seal(seal)
    named = f"{lane.SEAL_CORPUS_RELPATH}/{path}"
    assert [problem for problem in problems if named in problem] != [], \
        problems
    assert sum(named in problem for problem in problems) == 1, problems


# ---------------------------------------------------------------------------
# the pre-dispatch render (#1161) — the child's own render and --strict, run
# on the parent over the seal, before anything is dispatched
# ---------------------------------------------------------------------------

_STAND_IN_ENTRY = '''\
"""A stand-in RENDER_ENTRY: records how it was run, then renders per mode.
Its configuration is a file whose path is written into this script, because
the render's environment carries none of the test's own variables."""
import hashlib, json, os, sys
from pathlib import Path

config = json.loads(Path(CONFIG).read_text(encoding="utf-8"))
args = sys.argv[1:]
Path(config["entry_record"]).write_text(json.dumps(
    {"argv": args, "cwd": os.getcwd(), "env": dict(os.environ)}),
    encoding="utf-8")
mode = config.get("render", "ok")
if mode == "fail":
    print("Traceback: the render could not import opendox", file=sys.stderr)
    sys.exit(3)
output = Path(args[args.index("--output") + 1])
revision = args[args.index("--source-revision") + 1]
stamp = args[args.index("--generated-at") + 1]
if mode == "drop-anchors":
    revision = "0" * 40
text = json.dumps({"kind": "ideation-dashboard-snapshot",
    "generation": {"source_revision": revision, "generated_at": stamp},
    "documents": [{"id": "a"}, {"id": "b"}, {"id": "c"}]})
if mode in ("link-out", "hard-link"):
    # A file elsewhere on the host, readable and a valid snapshot, handed to
    # the parent through a link at the output path.
    host = Path(config["host_file"])
    host.write_text(text, encoding="utf-8")
    (output.symlink_to if mode == "link-out" else output.hardlink_to)(host)
elif mode == "swap-scratch":
    # A valid snapshot written elsewhere, and the scratch directory's own
    # path swapped for a link to it.
    host = Path(config["host_dir"])
    host.mkdir(exist_ok=True)
    (host / output.name).write_text(text, encoding="utf-8")
    scratch = output.parent
    scratch.rename(str(scratch) + ".moved")
    scratch.symlink_to(host, target_is_directory=True)
elif mode == "directory":
    output.mkdir()
elif mode == "fifo":
    os.mkfifo(output)
else:
    output.write_text(text, encoding="utf-8")
    Path(config["entry_record"] + ".sha256").write_text(
        hashlib.sha256(output.read_bytes()).hexdigest(), encoding="utf-8")
'''

_STAND_IN_VALIDATOR = '''\
"""A stand-in sealed validator: records how it was run and what it was
handed, then answers per mode."""
import hashlib, json, os, sys
from pathlib import Path

config = json.loads(Path(CONFIG).read_text(encoding="utf-8"))
Path(config["validator_record"]).write_text(json.dumps(
    {"argv": sys.argv[1:], "cwd": os.getcwd(), "env": dict(os.environ),
     "sha256": hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()}),
    encoding="utf-8")
mode = config.get("validator", "ok")
target = sys.argv[1]
if mode == "many-findings":
    for n in range(60):
        print(f"ERROR [snapshot-unknown-kind] {target}: filler {n}")
    print(f"ERROR [snapshot-dangling-cluster-ref] {target}: possible 'pos-z' "
          "claiming_clusters references unknown cluster 'cl-plane-1'")
    print("validate-ideation-dashboard-contracts: 61 error(s), 0 warning(s)")
    sys.exit(1)
if mode == "findings":
    for pos in ("pos-a", "pos-b", "pos-c"):
        print(f"ERROR [snapshot-dangling-cluster-ref] {target}: possible "
              f"{pos!r} claiming_clusters references unknown cluster "
              "'cl-plane-1'")
    print(f"ERROR [snapshot-dangling-cluster-ref] {target}: possible 'pos-d' "
          "claiming_clusters references unknown cluster 'cl-other-2'")
    print("validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)")
    sys.exit(1)
if mode == "harness":
    print("ERROR harness failure: jsonschema is not installed", file=sys.stderr)
    sys.exit(2)
print("validate-ideation-dashboard-contracts: 0 error(s), 0 warning(s)")
'''

HEAD_REV = "1" * 40


def _configure(tmp_path: Path, **modes) -> None:
    """Set the stand-ins' modes (`render=`, `validator=`) for the next run."""
    (tmp_path / "stand-in-config.json").write_text(json.dumps({
        "entry_record": str(tmp_path / "entry.json"),
        "validator_record": str(tmp_path / "validator.json"),
        "host_file": str(tmp_path / "host-file.json"),
        "host_dir": str(tmp_path / "host-dir"), **modes}),
        encoding="utf-8")


@pytest.fixture
def stand_in_seal(tmp_path) -> Path:
    """A seal holding a stand-in render entry and a stand-in sealed validator
    at the paths the real ones occupy, with their records wired up through a
    configuration file named inside each script."""
    seal = tmp_path / "seal"
    config = repr(str(tmp_path / "stand-in-config.json"))
    entry = seal / lane.SEAL_CORPUS_RELPATH / lane.RENDER_ENTRY
    entry.parent.mkdir(parents=True)
    entry.write_text(f"CONFIG = {config}\n" + _STAND_IN_ENTRY, encoding="utf-8")
    validator = seal / lane.SEAL_VALIDATOR_RELPATH
    validator.parent.mkdir(parents=True)
    validator.write_text(f"CONFIG = {config}\n" + _STAND_IN_VALIDATOR,
                         encoding="utf-8")
    module = lane.sealed_product_module(seal)
    module.parent.mkdir(parents=True)
    module.write_text(PRODUCT_MODULE_TEXT, encoding="utf-8")
    _configure(tmp_path)
    return seal


def _precheck(seal: Path) -> dict:
    return lane.precheck_sealed_render(seal, source_head=HEAD_REV,
                                       source_committed_at=COMMITTED_AT)


def test_the_pre_dispatch_render_is_the_childs_own_invocation(
        stand_in_seal, tmp_path, stand_in_docker):
    """The entry runs from the SEALED corpus root, with the seal's two anchors
    and `--no-validate`, word for word the child worker's generate, writing
    into the container's own /out (#1191). Then the SEALED validator runs over
    what it streamed, under `--strict`. The record it returns is what the
    manifest's `precheck` says."""
    record = _precheck(stand_in_seal)
    assert record == {"entry": lane.RENDER_ENTRY, "documents": 3,
                      "strict": True, "outcome": lane.PRECHECK_VALIDATED,
                      "returncode": 0}
    ran = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))
    corpus_root = stand_in_seal / lane.SEAL_CORPUS_RELPATH
    output = ran["argv"][ran["argv"].index("--output") + 1]
    assert ran["argv"] == [
        "generate", "--repo-root", ".", "--repository", "openxFactory",
        "--no-validate", "--source-revision", HEAD_REV,
        "--generated-at", COMMITTED_AT, "--output", output]
    assert Path(ran["cwd"]).resolve() == corpus_root.resolve()
    assert output.endswith("/out/openxFactory-snapshot.json")
    assert not Path(output).resolve().is_relative_to(stand_in_seal.resolve())
    render, validator = _sealed_runs(stand_in_docker)
    assert render[render.index(lane.SEALED_PYTHON):] == [
        lane.SEALED_PYTHON, lane.RENDER_ENTRY, "generate", "--repo-root", ".",
        "--repository", "openxFactory", "--no-validate",
        "--source-revision", HEAD_REV, "--generated-at", COMMITTED_AT,
        "--output", lane.SEALED_RENDER_OUTPUT]
    # The validator judges a COPY of exactly the bytes the render streamed, in
    # a directory made for it and mounted read-only, under `--strict`.
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    handed = Path(judged["argv"][0])
    assert judged["argv"][1:] == ["--strict"]
    assert handed.name == "snapshot.json" and handed.is_absolute()
    assert handed.parent != Path(output).resolve().parent
    assert not handed.is_relative_to(stand_in_seal.resolve())
    assert judged["sha256"] == \
        (tmp_path / "entry.json.sha256").read_text(encoding="utf-8")
    module = lane.sealed_product_module(stand_in_seal).resolve()
    assert validator[-4:] == [
        "/seal/" + module.relative_to(stand_in_seal.resolve()).as_posix(),
        f"{lane.SEALED_JUDGED}/snapshot.json",
        f"/seal/{lane.SEAL_VALIDATOR_RELPATH}", "strict"]


# ---------------------------------------------------------------------------
# #1191: every sealed run is one `docker run` in the child worker's shape
# ---------------------------------------------------------------------------

_LABEL_4242 = "openxfactory.dashboard-refresh.sealed-run=4242-1"


def _the_childs_shape(seal: Path, label: str) -> list[str]:
    """The `docker run` every sealed run starts with, written out here word
    for word, so no flag can drop out of the lane's unnoticed: the flags
    opensoft/xFactory#526 runs the child's sealed render and validator
    with."""
    return ["run", "--rm", "--init", "--pull", "never",
            "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m",
            "--network", "none", "--ipc", "none",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--pids-limit", "128", "--memory", "1g", "--memory-swap", "1g",
            "--cpus", "1", "--label", label, "--log-driver", "none",
            "--env", "PYTHONDONTWRITEBYTECODE=1",
            "--env", "PYTHONIOENCODING=utf-8",
            "--env", "HOME=/tmp", "--env", "LANG=C.UTF-8",
            "--mount", f"type=bind,source={seal.resolve()},target=/seal,readonly"]


def test_every_sealed_run_is_one_docker_run_in_the_childs_shape(
        stand_in_seal, stand_in_docker, monkeypatch):
    """THE PRE-DISPATCH RENDER AND ITS VALIDATOR RUN IN THE CHILD'S CONTAINER
    (#1191, "(b) for the finalize job too"). Each is one `docker run` of the
    image the build step recorded, by id, with the seal read-only at /seal,
    a read-only root, no network, no capability, this runner's non-root uid,
    bounded processes, memory and CPU, this run's label, four literals of
    environment, `--init` and `--rm`. The render's one writable place is a
    tmpfs of its own at /out. The validator sees the judged copy's directory,
    read-only, at /judged, and nothing else of the runner's."""
    monkeypatch.setenv("GITHUB_RUN_ID", "4242")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    _precheck(stand_in_seal)
    render, validator = _sealed_runs(stand_in_docker)
    shape = _the_childs_shape(stand_in_seal, _LABEL_4242)
    assert render[:len(shape)] == shape
    assert render[len(shape):render.index(lane.SEALED_PYTHON)] == [
        "--tmpfs", "/out:rw,noexec,nosuid,nodev,size=32m",
        "--workdir", "/seal/openxFactory", STAND_IN_IMAGE,
        "/bin/sh", "-c", lane._SEALED_RENDER_WRAPPER, "render",
        "/out/openxFactory-snapshot.json"]
    assert validator[:len(shape)] == shape
    judged = validator[len(shape) + 1]
    assert re.fullmatch(r"type=bind,source=/\S+/dfr-judged-\w+,target=/judged,"
                        r"readonly", judged), judged
    assert validator[len(shape)] == "--mount"
    assert validator[len(shape) + 2:len(shape) + 7] == [
        "--workdir", "/tmp", STAND_IN_IMAGE, "/usr/local/bin/python3", "-c"]


def test_the_probe_runs_in_a_sealed_container_never_on_the_runner(
        corpus, tmp_path, stand_in_docker, monkeypatch):
    """THE PROBE IS SEALED CODE, AND IT RUNS IN A CONTAINER (#1191). The
    sealed validator's run over the probe is one `docker run` in the child's
    shape, over the probe's own directory mounted read-only at /judged. Not
    one sealed run reaches this runner's own interpreter."""
    monkeypatch.setenv("GITHUB_RUN_ID", "4242")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    runs = _sealed_runs(stand_in_docker)
    assert runs, "the probe ran on this runner, not in a sealed container"
    probe = runs[0]
    shape = _the_childs_shape(seal, _LABEL_4242)
    assert probe[:len(shape)] == shape
    # The harness's four arguments, then each other sealed code leg's `src/`
    # (`lane.sealed_leg_sources`, plan 034 T066): the openDox leg, which the
    # seal carries at both pins.
    legs = ["/seal/" + src.relative_to(seal.resolve()).as_posix()
            for src in lane.sealed_leg_sources(seal)]
    assert legs, "the seal carries no code leg beside the validator's"
    assert probe[-(4 + len(legs)):] == [
        "/seal/" + lane.sealed_product_module(seal).resolve().relative_to(
            seal.resolve()).as_posix(),
        f"{lane.SEALED_JUDGED}/validator-probe.json",
        f"/seal/{lane.SEAL_VALIDATOR_RELPATH}", "lenient", *legs]
    assert re.fullmatch(r"type=bind,source=/\S+/dfr-probe-\w+,target=/judged,"
                        r"readonly", probe[len(shape) + 1])


@pytest.mark.parametrize("image", [None, "", "latest", "python:3.12-slim",
                                   "sha256:" + "a" * 63, "sha256:" + "A" * 64,
                                   "sha256:" + "a" * 64 + "\n"],
                         ids=["unset", "empty", "a-tag", "a-name",
                              "a-short-id", "upper-case", "a-trailing-newline"])
def test_no_sealed_code_runs_without_the_image_the_build_step_records(
        corpus, tmp_path, stand_in_docker, monkeypatch, image):
    """The sealed runs run in the image the finalize job's build step made,
    named by the content id it recorded in `SEALED_IMAGE`, never by a name a
    pull or a tag could move. Anything else refuses the seal before the
    corpus is archived, and no sealed code runs at all: not in a container,
    and not on this runner in its place (#1191)."""
    if image is None:
        monkeypatch.delenv("SEALED_IMAGE")
    else:
        monkeypatch.setenv("SEALED_IMAGE", image)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal")
    assert str(refused.value) == (
        f"SEALED_IMAGE is {image or ''!r}, not the image id the finalize "
        "job's build step records, so no sealed code runs")
    assert _docker_calls(stand_in_docker) == []
    assert not (tmp_path / "seal" / lane.SEAL_CORPUS_RELPATH).exists()


@pytest.mark.parametrize("name", _SEALED_DOCKER_ENV)
def test_a_variable_that_would_take_the_calls_elsewhere_refuses_every_sealed_run(
        corpus, tmp_path, stand_in_docker, monkeypatch, name):
    """Set at all, whatever its value, each of these would send the docker
    CLI's calls to another daemon or builder than the one the build step
    used, or, for ACTIONS_ALLOW_UNSECURE_COMMANDS, let a line printed by a
    step set a variable or a PATH entry for a later one. The seal is refused
    and no sealed code runs (#1191)."""
    monkeypatch.setenv(name, "")
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal")
    if name == "ACTIONS_ALLOW_UNSECURE_COMMANDS":
        assert str(refused.value) == (
            "ACTIONS_ALLOW_UNSECURE_COMMANDS is set, so output this job does "
            "not control could set a variable or a PATH entry for a later "
            "step: no sealed code runs")
    else:
        assert str(refused.value) == (
            f"{name} is set, so the docker CLI would not send its calls to the "
            "local daemon the build step used: no sealed code runs")
    assert _docker_calls(stand_in_docker) == []


def test_a_root_uid_runs_no_sealed_code(corpus, tmp_path, stand_in_docker,
                                        monkeypatch):
    """The sealed runs take this runner's own uid and gid, and never root's
    (#1191)."""
    monkeypatch.setattr(lane.os, "getuid", lambda: 0)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal")
    assert str(refused.value) == (
        "the sealed runs take this runner's uid and gid, and they are root's, "
        "so no sealed code runs")
    assert _docker_calls(stand_in_docker) == []


def test_no_docker_cli_at_its_absolute_path_runs_no_sealed_code(
        corpus, tmp_path, stand_in_docker, monkeypatch):
    """The docker CLI is called by its absolute path, never looked up on a
    PATH, and a runner without it runs no sealed code (#1191)."""
    monkeypatch.setattr(lane, "DOCKER", str(tmp_path / "no-docker-here"))
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal")
    assert str(refused.value) == (
        f"there is no docker CLI at {tmp_path / 'no-docker-here'}, so no "
        "sealed code runs")
    assert lane.DOCKER.startswith("/")


def test_the_real_lane_calls_docker_by_its_absolute_system_path(monkeypatch):
    monkeypatch.undo()
    assert lane.DOCKER == "/usr/bin/docker"


def test_a_container_left_running_is_removed_and_refuses_the_seal(
        stand_in_seal, stand_in_docker, monkeypatch):
    """`--init` and `--rm` in the foreground end every process of a run with
    its container. The lane still asks the daemon, after each run, for any
    container of this run's label still running. One that is has sealed
    code that could still act: it is removed, and the seal is refused
    (#1191)."""
    monkeypatch.setenv("GITHUB_RUN_ID", "4242")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    _stand_in_docker_config(stand_in_docker, running=["c0ffee"])
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert str(refused.value) == (
        "a container of the sealed render was still running after it "
        "returned, so sealed code could still act: it is removed, and the "
        "seal is refused")
    calls = [call["argv"] for call in _docker_calls(stand_in_docker)]
    listing = ["ps", "-q", "--filter", f"label={_LABEL_4242}"]
    assert ["rm", "-f", "c0ffee"] in calls
    # Asked again after the removal, and gone.
    assert calls[calls.index(["rm", "-f", "c0ffee"]) + 1] == listing


def test_a_container_the_daemon_cannot_remove_refuses_the_seal_saying_so(
        stand_in_seal, stand_in_docker, monkeypatch):
    """A removal the daemon rejects leaves the container running, so the
    refusal says so rather than that it was removed. The seal is refused
    either way, and the job's last step removes what the run left, or fails
    (Copilot, PR #1192)."""
    monkeypatch.setenv("GITHUB_RUN_ID", "4242")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    _stand_in_docker_config(stand_in_docker, running=["c0ffee"], rm_exit=1)
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert str(refused.value) == (
        "a container of the sealed render was still running after it "
        "returned, so sealed code could still act, and the daemon could not "
        "remove it (c0ffee): the seal is refused, and the job's last step "
        "removes what this run left")


def test_a_daemon_that_cannot_list_the_runs_refuses_the_seal(
        stand_in_seal, stand_in_docker):
    """A run the daemon cannot account for is not known to be gone
    (#1191)."""
    _stand_in_docker_config(stand_in_docker, ps_exit=1)
    with pytest.raises(lane.SealRefused, match="could not list this job's "
                                               "sealed containers"):
        _precheck(stand_in_seal)


def test_the_docker_cli_runs_with_none_of_the_jobs_environment(
        stand_in_seal, stand_in_docker, monkeypatch):
    """The docker CLI itself is handed system tool directories and a fresh
    configuration directory of its own, and nothing else of the job's: no
    credential, and no plugin, proxy setting or login of the runner user's
    (#1191)."""
    _export_the_job_environment(monkeypatch)
    _precheck(stand_in_seal)
    calls = _docker_calls(stand_in_docker)
    assert calls, "no sealed run went through the docker CLI"
    for call in calls:
        env = call["env"]
        assert set(env) <= {"PATH", "HOME", "DOCKER_CONFIG", "LANG"}, sorted(env)
        assert env["PATH"] == "/usr/sbin:/usr/bin:/sbin:/bin"
        assert env["DOCKER_CONFIG"] == env["HOME"]
        assert Path(env["DOCKER_CONFIG"]).name.startswith("dfr-docker-config-")
        assert not any(value in _JOB_SECRETS for value in env.values())


@pytest.mark.parametrize("name", ["a,b", 'a"b'], ids=["a-comma", "a-quote"])
def test_a_mount_source_that_could_add_a_field_is_refused(tmp_path, name):
    """A mount is written as comma-separated fields, so a source holding a
    comma or a quote could add a field of its own, `readonly=false` among
    them. Such a path is refused, not mounted (#1191)."""
    seal = tmp_path / name
    seal.mkdir()
    container = lane.resolve_sealed_container()
    with pytest.raises(lane.SealRefused, match="a mount source must be an "
                                               "absolute path with no comma"):
        container.argv(seal, workdir="/tmp")


def test_the_label_is_this_runs_when_the_job_names_it(monkeypatch):
    """The build step labels the image, and the job's last step removes
    what carries the label, by this run's id and attempt. A run outside a
    job gets a label of its own (#1191)."""
    monkeypatch.setenv("GITHUB_RUN_ID", "4242")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    assert lane.resolve_sealed_container().label == _LABEL_4242
    monkeypatch.delenv("GITHUB_RUN_ID")
    first = lane.resolve_sealed_container().label
    assert re.fullmatch(r"openxfactory\.dashboard-refresh\.sealed-run="
                        r"local-[0-9a-f]{16}", first)
    assert lane.resolve_sealed_container().label != first


def test_the_verdict_is_read_by_the_sealed_product_module(stand_in_seal,
                                                         tmp_path):
    """The pre-dispatch verdict is the product's own reading, as the SEAL
    carries it (Copilot, PR #1166)."""
    record = tmp_path / "classified-by.txt"
    lane.sealed_product_module(stand_in_seal).write_text(
        _recording_product_module(record), encoding="utf-8")
    assert _precheck(stand_in_seal)["outcome"] == lane.PRECHECK_VALIDATED
    assert record.read_text(encoding="utf-8").splitlines() == [
        str(lane.sealed_product_module(stand_in_seal))]


def test_a_seal_named_relative_to_the_working_directory_still_renders(
        stand_in_seal, tmp_path, monkeypatch, stand_in_docker):
    """The nightly names its seal `dfr-seal`, relative to the job's working
    directory. The container mounts the seal from where it is, by its
    absolute path, and the render runs from inside it at /seal. A relative
    source would be refused by the daemon, and every nightly seal with it."""
    monkeypatch.chdir(tmp_path)
    record = lane.precheck_sealed_render(Path(stand_in_seal.name),
                                         source_head=HEAD_REV,
                                         source_committed_at=COMMITTED_AT)
    assert record["outcome"] == lane.PRECHECK_VALIDATED
    assert record["documents"] == 3
    for run in _sealed_runs(stand_in_docker):
        assert (f"type=bind,source={stand_in_seal.resolve()},target=/seal,"
                "readonly") in run
    ran = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))
    corpus_root = (stand_in_seal / lane.SEAL_CORPUS_RELPATH).resolve()
    assert Path(ran["cwd"]).resolve() == corpus_root
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    assert Path(judged["argv"][0]).is_absolute()


def test_the_pre_dispatch_render_holds_no_credential_and_no_repository(
        stand_in_seal, tmp_path, monkeypatch):
    """It runs code read OUT OF THE SEAL, in a job that holds the App token and
    a token-bearing git configuration. So its container is given none of the
    job's variables: no credential, none of the job's GitHub or Git
    variables, no interpreter path override, and HOME its own /tmp (#1191).
    No git or repository is mounted into it at all."""
    _export_the_job_environment(monkeypatch)
    _precheck(stand_in_seal)
    env = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))["env"]
    _assert_the_renders_environment(env, stand_in_seal)


def test_the_sealed_validator_runs_in_the_renders_environment_too(
        stand_in_seal, tmp_path, monkeypatch):
    """The sealed validator is sealed code as well. The product's
    `validate_snapshot` launches it with no environment of its own, so a call
    made in this process would have handed it every credential of the job
    (Copilot, PR #1166). It runs in a sealed container of its own, from that
    container's /tmp, outside the seal (#1191)."""
    _export_the_job_environment(monkeypatch)
    _precheck(stand_in_seal)
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    _assert_the_renders_environment(judged["env"], stand_in_seal)
    cwd = Path(judged["cwd"]).resolve()
    assert not cwd.is_relative_to(stand_in_seal.resolve())
    assert cwd != Path.cwd().resolve()


@pytest.mark.parametrize("mode, said", [
    ("fail", "the sealed render unit could not render the snapshot (exit 3), "
             "so the child's generate would fail the same way: Traceback: the "
             "render could not import opendox"),
    ("drop-anchors", "the sealed render did not carry the seal's two anchors "
                     f"(source_revision {'0' * 40!r}"),
], ids=["the-render-fails", "an-anchor-is-dropped"])
def test_a_sealed_render_that_would_fail_the_child_is_refused(
        stand_in_seal, tmp_path, mode, said):
    _configure(tmp_path, render=mode)
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    assert str(refused.value).startswith(said)


@pytest.mark.parametrize("mode", ["link-out", "directory", "fifo"],
                         ids=["a-link-out-of-its-directory", "a-directory",
                              "a-fifo"])
def test_render_output_that_is_not_a_file_of_its_own_is_refused(
        stand_in_seal, tmp_path, mode):
    """The snapshot leaves the render's container by stdout alone, and the
    child worker's own wrapper streams it only when the render left a regular
    file of its own at /out (#1191). A link there, a directory or a fifo is
    refused inside the container with exit 3, and nothing is streamed, read
    or validated."""
    _configure(tmp_path, render=mode)
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    assert re.fullmatch(
        r"the sealed render unit could not render the snapshot \(exit 3\), "
        r"so the child's generate would fail the same way: the sealed render "
        r"left no regular file at \S+/out/openxFactory-snapshot\.json",
        str(refused.value)), str(refused.value)
    assert not (tmp_path / "validator.json").exists()      # nothing judged


def test_the_snapshot_leaves_the_render_by_stdout_bounded(
        stand_in_seal, tmp_path, monkeypatch):
    """Nothing the render writes lands on this runner. Its snapshot is
    streamed out of its container, and the host keeps at most one byte past
    `SEALED_SNAPSHOT_LIMIT`: a render that streams more is refused before
    anything is parsed, copied or validated (#1191)."""
    monkeypatch.setattr(lane, "SEALED_SNAPSHOT_LIMIT", 64)
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert str(refused.value) == (
        "the sealed render streamed more than 64 bytes, which no snapshot "
        "needs, so its output is refused")
    assert not (tmp_path / "validator.json").exists()      # nothing judged


def test_a_render_that_prints_past_the_log_bound_is_refused(
        stand_in_seal, tmp_path, monkeypatch):
    """What a sealed run prints for the log is bounded too
    (`SEALED_LOG_LIMIT`), and a run past it is refused, whatever it
    exited with (#1191)."""
    monkeypatch.setattr(lane, "SEALED_LOG_LIMIT", 16)
    _configure(tmp_path, render="fail")
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert str(refused.value) == (
        "the sealed render printed more than 16 bytes for the log, which no "
        "render needs, so it is refused")


@pytest.mark.parametrize("replacement", ["a-link-to-the-moved-seal",
                                         "a-copy-in-its-place"])
def test_a_seal_directory_the_render_replaced_gets_no_manifest(
        corpus, tmp_path, replacement):
    """Sealed code runs inside the seal directory, so it could move it and
    put a link, or a copy with the same content, where it was. The index
    would match either. The directory is held by identity from its creation,
    so either is refused, and no manifest is written anywhere (Copilot,
    PR #1166). The render is handed the directory the lane holds (Copilot,
    PR #1185), so the stand-in moves the seal by its name, as sealed code
    that knows where it runs would."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"

    def replacing(seal_root, *, source_head, source_committed_at,
                  container=None):
        seal.rename(moved)
        if replacement == "a-link-to-the-moved-seal":
            seal.symlink_to(moved, target_is_directory=True)
        else:
            shutil.copytree(moved, seal)
        return dict(STUB_PRECHECK)

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, precheck_render=replacing)
    assert str(refused.value) == (
        "the seal directory is no longer the one the lane created: sealed "
        "code ran inside it, and the manifest is never written anywhere else")
    assert not (moved / lane.SEAL_MANIFEST_NAME).exists()
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


def test_the_manifest_is_written_only_into_the_directory_created(tmp_path):
    """The write itself holds the identity too: handed another directory, or
    a link, it writes nothing."""
    created = tmp_path / "created"
    created.mkdir()
    identity = lane._seal_directory_identity(created)
    other = tmp_path / "other"
    other.mkdir()
    link = tmp_path / "link"
    link.symlink_to(created, target_is_directory=True)
    for target in (other, link):
        with pytest.raises(lane.SealRefused,
                           match="no longer the one the lane created"):
            lane._write_new_manifest(target, "{}\n", identity=identity)
    assert not any(path.name == lane.SEAL_MANIFEST_NAME
                   for path in tmp_path.rglob("*"))
    lane._write_new_manifest(created, "{}\n", identity=identity)
    assert (created / lane.SEAL_MANIFEST_NAME).read_bytes() == b"{}\n"


@pytest.mark.parametrize("leads_to", ["an-empty-directory",
                                      "a-directory-holding-files", "nothing"])
def test_a_seal_directory_that_is_a_link_is_refused(corpus, tmp_path,
                                                    leads_to):
    """A LINK AT THE SEAL'S OWN NAME IS NEVER FOLLOWED (#1182). It is refused
    before the validator is resolved, whatever it leads to, and nothing is
    read or written through it. Before this, the lane looked through it to
    ask whether its target was empty, adopted an empty one as far as its
    `mkdir`, and let a dangling one escape as a bare `FileExistsError`."""
    target = tmp_path / "target"
    if leads_to != "nothing":
        target.mkdir()
        if leads_to == "a-directory-holding-files":
            (target / "kept.txt").write_text("untouched\n", encoding="utf-8")
    before = _what_is_at(target)
    link = tmp_path / "seal"
    link.symlink_to(target, target_is_directory=True)
    calls: list = []
    resolving = _recording_resolver(tmp_path / "unit", calls)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, link, resolve_validator=resolving)
    assert str(refused.value) == _linked_seal_path(link)
    assert calls == []
    assert link.is_symlink()
    assert _what_is_at(target) == before


def test_a_sealed_validator_that_cannot_run_over_the_render_is_refused(
        stand_in_seal, tmp_path):
    _configure(tmp_path, validator="harness")
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    reason = str(refused.value)
    assert reason.startswith("the sealed validator could NOT RUN over the "
                             "snapshot this seal renders")
    assert "jsonschema is not installed" in reason


# A STAND-IN TRACKING ROW for the citation machinery. The production table,
# `lane.KNOWN_STRICT_FINDINGS`, is empty since #1159's row was dropped, so the
# tests of the machinery install this row instead. It keeps the shape of the
# stand-in validator's `cl-plane-1` findings, under an issue that is not real.
_TRACKED_ROW = ("snapshot-dangling-cluster-ref", "'cl-plane-1'",
                "stand-in/tracker#1")


def test_a_strict_rejection_is_a_verdict_carrying_the_findings(
        stand_in_seal, tmp_path):
    """`StrictGateRejected`: the validator's own findings, with the scratch
    path reduced to the file's name. No finding is tracked today, so the
    reason cites no issue, not even for the `cl-plane-1` findings #1159 once
    tracked: a recurrence reads as a rejection of its own."""
    _configure(tmp_path, validator="findings")
    with pytest.raises(lane.StrictGateRejected) as rejected:
        _precheck(stand_in_seal)
    assert str(rejected.value) == (
        "--strict REJECTED the snapshot this seal renders "
        "(validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)); "
        "the child's publication gate would refuse it the same way, so "
        "nothing is dispatched")
    assert rejected.value.detail == [
        *(f"ERROR [snapshot-dangling-cluster-ref] snapshot.json: possible "
          f"{pos!r} claiming_clusters references unknown cluster 'cl-plane-1'"
          for pos in ("pos-a", "pos-b", "pos-c")),
        "ERROR [snapshot-dangling-cluster-ref] snapshot.json: possible 'pos-d' "
        "claiming_clusters references unknown cluster 'cl-other-2'",
        "validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)"]


def test_a_strict_rejection_cites_the_issue_of_every_finding_it_tracks(
        stand_in_seal, tmp_path, monkeypatch):
    """With a row in the table, the reason cites its issue and counts the
    findings it tracks, so a rejection that also carries a new finding never
    reads as fully tracked."""
    monkeypatch.setattr(lane, "KNOWN_STRICT_FINDINGS", (_TRACKED_ROW,))
    _configure(tmp_path, validator="findings")
    with pytest.raises(lane.StrictGateRejected) as rejected:
        _precheck(stand_in_seal)
    assert str(rejected.value) == (
        "--strict REJECTED the snapshot this seal renders "
        "(validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)), a "
        "known defect, tracked as stand-in/tracker#1 (3 of 4 finding(s); 1 "
        "tracked by no known issue); the child's publication gate would "
        "refuse it the same way, so nothing is dispatched")


def test_a_tracked_finding_past_the_detail_cap_is_still_cited(
        stand_in_seal, tmp_path, monkeypatch):
    """The citation reads EVERY line the validator wrote, and only the detail
    the verdict carries is capped (Copilot, PR #1166). Here the one tracked
    finding is the 61st, past `DETAIL_CAP`."""
    monkeypatch.setattr(lane, "KNOWN_STRICT_FINDINGS", (_TRACKED_ROW,))
    _configure(tmp_path, validator="many-findings")
    with pytest.raises(lane.StrictGateRejected) as rejected:
        _precheck(stand_in_seal)
    assert "tracked as stand-in/tracker#1 (1 of 61 finding(s); 60 " \
        "tracked by no known issue)" in str(rejected.value)
    assert len(rejected.value.detail) == lane.DETAIL_CAP
    assert not any("cl-plane-1" in line for line in rejected.value.detail)


@pytest.mark.parametrize("lie", [
    {"returncode": 2},
    {"outcome": "not-conformant"},
    {"outcome": "not-conformant", "returncode": 1},
], ids=["validated-with-exit-2", "not-conformant-with-exit-0",
        "a-finding-passed-as-ok"])
def test_a_pre_dispatch_verdict_that_does_not_pair_is_refused(
        stand_in_seal, lie):
    """The sealed validator's verdict over the render is read from its exit
    code, and the flag that says it passed must agree. A sealed product module
    that answers otherwise reached no verdict: the seal is refused as one
    whose validator could not judge the render, never recorded as a pass for
    the intake to refuse, and never reported as a verdict on the corpus
    (Copilot, opensoft/xFactory PR #526)."""
    lane.sealed_product_module(stand_in_seal).write_text(
        _lying_product_module(**lie), encoding="utf-8")
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    outcome = lie.get("outcome", "validated")
    returncode = lie.get("returncode", 0)
    assert str(refused.value).startswith(
        f"the sealed validator answered {outcome!r} with exit {returncode!r} "
        "(ok=True) over the snapshot this seal renders, which is not a "
        f"verdict as the validator reports one ({VERDICT_PAIRS})"), \
        str(refused.value)


def test_a_render_that_does_not_finish_is_refused(stand_in_seal,
                                                  stand_in_docker):
    """A sealed run is bounded. One past its bound is killed with its
    container, and the lane looks for anything the run left before it
    refuses the seal (#1191)."""
    _stand_in_docker_config(stand_in_docker, hang=True)
    with pytest.raises(lane.SealRefused, match="did not finish within 2s"):
        lane.precheck_sealed_render(stand_in_seal, source_head=HEAD_REV,
                                    source_committed_at=COMMITTED_AT,
                                    timeout=2)
    calls = [call["argv"] for call in _docker_calls(stand_in_docker)]
    assert calls[0][0] == "run"
    assert any(call[:4] == ["ps", "-a", "-q", "--filter"]
               and call[4].startswith(f"label={lane.SEALED_RUN_LABEL}=")
               for call in calls[1:]), calls


_A_VALIDATED_VERDICT = json.dumps({
    "ok": True, "returncode": 0, "stdout": "", "stderr": "",
    "outcome": "validated", "unavailable_reason": None})


def test_each_sealed_run_is_read_to_its_own_bound(stand_in_seal):
    """What the host reads of a run is bounded by what that run may print:
    the render's snapshot by SEALED_SNAPSHOT_LIMIT, and a validator's verdict
    by SEALED_LOG_LIMIT (#1191)."""
    container = _AnsweringContainer(
        lane.resolve_sealed_container(),
        lambda: lane.SealedRunResult(0, (_A_VALIDATED_VERDICT + "\n").encode(),
                                     b""))
    lane.precheck_sealed_render(stand_in_seal, source_head=HEAD_REV,
                                source_committed_at=COMMITTED_AT,
                                container=container, timeout=7)
    assert container.limits == [("render", lane.SEALED_SNAPSHOT_LIMIT),
                                ("validator", lane.SEALED_LOG_LIMIT)]
    assert (lane.SEALED_SNAPSHOT_LIMIT, lane.SEALED_LOG_LIMIT) == (33554432,
                                                                  1048576)


class _AnsweringContainer:
    """The real stand-in container for the render, and one canned answer for
    every validator run."""

    def __init__(self, real, answer):
        self.real, self.answer, self.timeouts = real, answer, []
        self.limits = []

    def run(self, what, seal_root, command, **kw):
        self.limits.append((what, kw["stdout_limit"]))
        if what == "render":
            return self.real.run(what, seal_root, command, **kw)
        self.timeouts.append(kw["timeout"])
        return self.answer()


def _answer(harness):
    if harness == "cannot-launch":
        raise lane.SealRefused("the sealed validator could not be launched in "
                               "its container (OSError: exec format error)")
    if harness == "hangs":
        return lane.SealedRunResult(-9, b"", b"", timed_out=True)
    if harness == "prints-past-the-bound":
        return lane.SealedRunResult(0, _A_VALIDATED_VERDICT.encode(), b"",
                                    stdout_over=True)
    stdout = {"says-nothing": "",
              "prints-no-object": "[]\n",
              "prints-another-shape": _A_VALIDATED_VERDICT.replace(
                  '"validated"', '"maybe"') + "\n",
              "exits-non-zero": _A_VALIDATED_VERDICT + "\n"}[harness]
    return lane.SealedRunResult(1 if harness == "exits-non-zero" else 0,
                                stdout.encode(), b"")


@pytest.mark.parametrize("harness, said", [
    ("hangs", "the validator did not finish within 7s"),
    ("cannot-launch", "the sealed validator could not be launched in its "
                      "container (OSError: exec format error)"),
    ("says-nothing", "the validator's harness returned no verdict (exit 0)"),
    ("prints-no-object", "the validator's harness returned no verdict (exit 0)"),
    ("prints-another-shape", "the validator's harness returned no verdict "
                             "(exit 0)"),
    ("exits-non-zero", "the validator's harness returned no verdict (exit 1)"),
    ("prints-past-the-bound", "the validator's run printed more than "
                              "1048576 bytes, which no verdict needs"),
], ids=["hangs", "cannot-launch", "says-nothing", "prints-no-object",
        "prints-another-shape", "exits-non-zero", "prints-past-the-bound"])
def test_a_validator_run_that_reaches_no_verdict_is_refused(stand_in_seal,
                                                            harness, said):
    """The validator's run is bounded, and only a harness that exits cleanly
    with a verdict of the product's own shape has answered. Anything else is
    the product's own "could not run", never a verdict on the corpus. That
    holds even for a harness that printed "validated" before exiting non-zero,
    and for one that printed past its bound. The render is real here, and
    only the validator's run is stood in for."""
    container = _AnsweringContainer(lane.resolve_sealed_container(),
                                    lambda: _answer(harness))
    with pytest.raises(lane.SealRefused) as refused:
        lane.precheck_sealed_render(stand_in_seal, source_head=HEAD_REV,
                                    source_committed_at=COMMITTED_AT,
                                    container=container, timeout=7)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    reason = str(refused.value)
    if harness == "cannot-launch":
        assert reason == said
        return
    assert reason.startswith("the sealed validator could NOT RUN over the "
                             "snapshot this seal renders")
    assert said in reason
    assert container.timeouts == [7]          # the validator's run is bounded


_MODAL_VALIDATOR = '''\
import sys
print("checked", *sys.argv[1:])
if MODE == "findings":
    print("ERROR [snapshot-unknown-kind] a finding")
    sys.exit(1)
if MODE == "harness":
    print("ERROR harness failure: jsonschema is not installed", file=sys.stderr)
    sys.exit(2)
'''


@pytest.mark.parametrize("mode, target_text, strict", [
    ("ok", "{}\n", False),
    ("ok", "{}\n", True),
    ("findings", "{}\n", True),
    ("harness", "{}\n", True),
    ("harness", "{not json", True),
    ("a-directory", "{}\n", True),
], ids=["validated", "validated-strict", "not-conformant", "unavailable",
        "an-unreadable-target-is-the-datas", "not-a-file"])
def test_the_fenced_call_answers_what_the_products_own_call_answers(
        tmp_path, mode, target_text, strict):
    """Moving the call into a sealed container changes WHERE it runs, never
    what it answers. Over each of the product's outcomes, including its
    own attribution of a harness exit over an unreadable target to the data,
    the fenced call returns the product's in-process result, field for
    field."""
    seal = tmp_path / "seal"
    package = seal / "src" / "openxdox"
    shutil.copytree(Path(snapshot_mod.__file__).parent, package,
                    ignore=shutil.ignore_patterns("__pycache__"))
    # Each other code leg, where a real seal carries it: from openXdox-code #35
    # the product module imports openDox's `projection_seams`, and the parent
    # hands the harness that leg's `src/` (`lane.sealed_leg_sources`, plan 034
    # T066). At a leg whose product module imports none, it is read by nothing.
    import importlib
    for gitlink, leg, name in lane.RENDER_LEGS:
        if (gitlink, leg) != lane.VALIDATOR_LEG:
            shutil.copytree(
                Path(importlib.import_module(name).__file__).parent,
                seal / lane.SEAL_CORPUS_RELPATH / gitlink / leg / "src" / name,
                ignore=shutil.ignore_patterns("__pycache__"))
    validator = seal / "validator.py"
    if mode == "a-directory":
        validator.mkdir()
    else:
        validator.write_text(f"MODE = {mode!r}\n" + _MODAL_VALIDATOR,
                             encoding="utf-8")
    judged = tmp_path / "judged"
    judged.mkdir()
    target = judged / "target.json"
    target.write_text(target_text, encoding="utf-8")
    fenced = lane.validate_in_render_environment(
        snapshot_mod, target, validator=validator, strict=strict,
        seal_root=seal, module_file=package / "snapshot.py",
        container=lane.resolve_sealed_container())
    own = snapshot_mod.validate_snapshot(target, validator=validator,
                                         strict=strict)
    for name in ("ok", "returncode", "stdout", "stderr", "outcome",
                 "unavailable_reason"):
        assert getattr(fenced, name) == getattr(own, name), name
    assert fenced.validator == Path(own.validator).resolve()


def test_no_strict_finding_is_tracked_today():
    """THE TABLE IS EMPTY. #1184 repaired the corpus and #1159 closed, so its
    one row tracked nothing and was dropped. Its finding, should it recur,
    draws no citation, rather than one naming a closed issue."""
    assert lane.KNOWN_STRICT_FINDINGS == ()
    assert lane.known_finding_citation(
        ["ERROR [snapshot-dangling-cluster-ref] s.json: x 'cl-plane-1'"] * 3
    ) == ""


@pytest.mark.parametrize("lines, cited", [
    (["ERROR [snapshot-dangling-cluster-ref] s.json: x 'cl-plane-1'"] * 3,
     "known defect, tracked as stand-in/tracker#1 (3 of 3 finding(s))"),
    (["ERROR [snapshot-dangling-cluster-ref] s.json: x 'cl-plane-10'"], ""),
    (["ERROR [snapshot-unknown-kind] s.json: x 'cl-plane-1'"], ""),
    (["validate-ideation-dashboard-contracts: 0 error(s), 1 warning(s)"], ""),
    ([], ""),
], ids=["all-known", "another-cluster", "another-code", "no-finding-line",
        "nothing"])
def test_a_citation_is_made_only_for_the_finding_it_tracks(
        lines, cited, monkeypatch):
    """The citation retires itself: once the corpus is fixed the finding is
    gone, and a different finding, even one naming a lookalike value or the
    same value under another code, is never cited against an issue that is
    not its own. Run against the stand-in row, since no row is real today."""
    monkeypatch.setattr(lane, "KNOWN_STRICT_FINDINGS", (_TRACKED_ROW,))
    assert lane.known_finding_citation(lines) == cited


def test_the_precheck_outcome_is_the_products_own_spelling():
    assert lane.PRECHECK_VALIDATED == snapshot_mod.VALIDATED


@pytest.mark.parametrize("planted", [
    "a-link-out-at-the-recipe", "a-link-out-for-its-directory",
    "a-hard-link-at-the-recipe", "a-directory-of-its-own",
    "the-seal-directory-replaced", "the-seal-directory-replaced-by-a-copy"])
def test_the_recipe_is_never_written_through_anything_sealed_code_left(
        corpus, tmp_path, planted):
    """THE RECIPE IS WRITTEN AS THE MANIFEST IS (Copilot, PR #1166). The
    validator's probe runs sealed code with the seal writable before the
    recipe is written, and the probe's after-index cannot see what a process
    it left behind puts at the recipe's path later. So the recipe's directory
    is made exclusively and the recipe created `O_EXCL|O_NOFOLLOW`, relative
    to the seal directory as created. Whatever is already there refuses the
    seal, and nothing is written through it: no host file, no host directory,
    no replaced seal directory, whether a link or a copy stands in for it.
    The entry is planted here as the recipe is read, just before it is
    written."""
    host_file = tmp_path / "host-file.txt"
    host_file.write_text("untouched\n", encoding="utf-8")
    host_dir = tmp_path / "host-dir"
    host_dir.mkdir()
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"
    folder = seal / lane.SEAL_RECIPE_RELPATH.split("/")[0]

    def planting():
        if planted == "a-link-out-at-the-recipe":
            folder.mkdir()
            (folder / "Dockerfile").symlink_to(host_file)
        elif planted == "a-link-out-for-its-directory":
            folder.symlink_to(host_dir, target_is_directory=True)
        elif planted == "a-hard-link-at-the-recipe":
            folder.mkdir()
            (folder / "Dockerfile").hardlink_to(host_file)
        elif planted == "a-directory-of-its-own":
            folder.mkdir()
        else:
            seal.rename(moved)
            if planted == "the-seal-directory-replaced":
                seal.symlink_to(moved, target_is_directory=True)
            else:
                shutil.copytree(moved, seal)
        return RECIPE_TEXT

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, seal, read_recipe=planting)
    reason = str(refused.value)
    if planted.startswith("the-seal-directory-replaced"):
        assert reason == (
            "the seal directory is no longer the one the lane created: sealed "
            "code ran inside it, and the recipe is never written anywhere "
            "else")
        assert not os.path.lexists(moved / "recipe")
        assert not os.path.lexists(seal / "recipe")
    else:
        assert reason == (
            "the seal already holds recipe/ that the lane did not make: sealed "
            "code ran inside the seal before the recipe was written, and the "
            "recipe is never written through anything it left"), reason
    assert host_file.read_text(encoding="utf-8") == "untouched\n"
    assert list(host_dir.iterdir()) == []
    assert not (seal / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("swap", ["a-link-out-for-its-directory",
                                  "a-link-out-at-the-recipe"])
def test_the_recipe_directory_is_held_from_its_making_to_the_recipe(
        corpus, tmp_path, monkeypatch, swap):
    """A process sealed code left behind could act in the instant between the
    lane making `recipe/` and creating the recipe in it: put a link where the
    directory was, or a link inside it. The directory is opened without
    following a link, and the recipe created `O_EXCL|O_NOFOLLOW`, so either
    is refused as a seal refusal, and nothing is written through it. The swap
    is made here as the lane's own `mkdir` of `recipe/` returns."""
    host_file = tmp_path / "host-file.txt"
    host_file.write_text("untouched\n", encoding="utf-8")
    host_dir = tmp_path / "host-dir"
    host_dir.mkdir()
    folder = lane.SEAL_RECIPE_RELPATH.split("/")[0]
    make = os.mkdir

    def making_then_swapping(path, mode=0o777, *, dir_fd=None):
        make(path, mode, dir_fd=dir_fd)
        if dir_fd is None or os.fspath(path) != folder:
            return
        if swap == "a-link-out-for-its-directory":
            os.rename(folder, folder + ".made", src_dir_fd=dir_fd,
                      dst_dir_fd=dir_fd)
            os.symlink(host_dir, folder, target_is_directory=True,
                       dir_fd=dir_fd)
        else:
            os.symlink(host_file, f"{folder}/Dockerfile", dir_fd=dir_fd)

    monkeypatch.setattr(lane.os, "mkdir", making_then_swapping)
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal")
    assert str(refused.value) == (
        "the seal already holds recipe/ that the lane did not make: sealed "
        "code ran inside the seal before the recipe was written, and the "
        "recipe is never written through anything it left")
    assert host_file.read_text(encoding="utf-8") == "untouched\n"
    assert list(host_dir.iterdir()) == []


def test_a_precheck_that_changes_the_sealed_tree_is_refused(corpus, tmp_path):
    def writing(seal_root, *, source_head, source_committed_at,
                container=None):
        (Path(seal_root) / lane.SEAL_CORPUS_RELPATH / "docs" / "new.md"
         ).write_text("written by the render\n", encoding="utf-8")
        return dict(STUB_PRECHECK)

    with pytest.raises(lane.SealRefused, match="changed the sealed tree"):
        _seal(corpus, tmp_path / "seal", precheck_render=writing)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_rejected_precheck_leaves_no_manifest(corpus, tmp_path):
    def rejecting(seal_root, *, source_head, source_committed_at,
                  container=None):
        raise lane.StrictGateRejected("--strict REJECTED", detail=["x"])

    with pytest.raises(lane.StrictGateRejected):
        _seal(corpus, tmp_path / "seal", precheck_render=rejecting)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


@pytest.mark.parametrize("planted, what", [
    ("a-link-out-of-the-seal", "a symbolic link"),
    ("a-dangling-link", "a symbolic link"),
    ("a-file", "a file"),
    ("a-directory", "a directory"),
], ids=["a-link-out-of-the-seal", "a-dangling-link", "a-file", "a-directory"])
def test_a_manifest_the_lane_did_not_write_refuses_the_seal(corpus, tmp_path,
                                                            planted, what):
    """Sealed code runs before the manifest is written: the validator's probe
    and the pre-dispatch render. The index cannot see `manifest.json`, the one
    path it excludes. So whatever either leaves there refuses the seal, and
    nothing is written through it (Copilot, PR #1166). A link out of the seal
    would otherwise have had the manifest written wherever it pointed."""
    outside = tmp_path / "outside.json"
    outside.write_text("untouched\n", encoding="utf-8")
    nowhere = tmp_path / "nowhere.json"

    def planting(seal_root, *, source_head, source_committed_at,
                 container=None):
        path = Path(seal_root) / lane.SEAL_MANIFEST_NAME
        if planted == "a-link-out-of-the-seal":
            path.symlink_to(outside)
        elif planted == "a-dangling-link":
            path.symlink_to(nowhere)
        elif planted == "a-file":
            path.write_text("{}\n", encoding="utf-8")
        else:
            path.mkdir()
        return dict(STUB_PRECHECK)

    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", precheck_render=planting)
    assert str(refused.value) == (
        f"the seal already holds a {lane.SEAL_MANIFEST_NAME} the lane did not "
        f"write ({what}): sealed code runs before the manifest is written, and "
        "the manifest is never written through anything it left")
    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert not nowhere.exists() and not nowhere.is_symlink()


@pytest.mark.parametrize("points_at", ["a-file-out-of-the-seal", "nothing"])
def test_the_manifest_is_created_exclusively(tmp_path, points_at):
    """What the check cannot see, a link put in place after it, the write
    refuses too: `O_EXCL` creates the file or fails, and never follows a
    link."""
    seal = tmp_path / "seal"
    seal.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("untouched\n", encoding="utf-8")
    target = outside if points_at == "a-file-out-of-the-seal" \
        else tmp_path / "nowhere.json"
    (seal / lane.SEAL_MANIFEST_NAME).symlink_to(target)
    with pytest.raises(lane.SealRefused,
                       match="one that appeared while the lane was writing it"):
        lane._write_new_manifest(seal, "{}\n")
    assert outside.read_text(encoding="utf-8") == "untouched\n"
    assert not (tmp_path / "nowhere.json").exists()
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    lane._write_new_manifest(fresh, '{"a": 1}\n')
    assert (fresh / lane.SEAL_MANIFEST_NAME).read_bytes() == b'{"a": 1}\n'


# ---------------------------------------------------------------------------
# THIS CHECKOUT, sealed for real, and its real corpus rendered from the seal
# ---------------------------------------------------------------------------

def test_this_checkout_seals_and_its_corpus_renders_from_the_seal(tmp_path):
    """The whole chain over the real repository: the corpus half at HEAD, both
    real legs at the commits HEAD pins, the real resolver's validator, and the
    REAL pre-dispatch render, the child's own invocation, run FROM THE SEAL
    with `git` fenced out of this checkout. The render must reach a verdict.
    Whether the verdict is `validated` is a property of the corpus, not of the
    seal, so both are accepted here. A rejection must carry the validator's
    finding lines (#1159's three dangling `cl-plane-1` refs, at the time of
    writing). The seal itself is then verified whole."""
    head = _git(REPO_ROOT, "rev-parse", "HEAD")
    verdict: dict = {}

    def precheck(seal_root, **anchors):
        try:
            verdict["record"] = lane.precheck_sealed_render(seal_root, **anchors)
        except lane.StrictGateRejected as rejected:
            verdict["rejected"] = rejected
            return dict(STUB_PRECHECK)      # so the seal can be verified below
        return verdict["record"]

    seal = tmp_path / "seal"
    manifest = lane.seal_source(
        corpus_checkout=REPO_ROOT, seal_dir=seal, correlation_id=CORRELATION,
        decision=_decision(head), corpus_ref="HEAD",
        read_recipe=(lambda: RECIPE_TEXT), precheck_render=precheck)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []
    for record in manifest["render_legs"]:
        pinned = _git(REPO_ROOT, "rev-parse", f"HEAD:{record['gitlink']}")
        assert record["gitlink_revision"] == pinned
        assert record["leg_revision"] == _git(
            REPO_ROOT / record["gitlink"], "rev-parse",
            f"{pinned}:{record['leg']}")
    (validator_leg,) = [record for record in manifest["render_legs"]
                        if (record["gitlink"], record["leg"]) == lane.VALIDATOR_LEG]
    assert manifest["validator_revision"] == validator_leg["leg_revision"]
    if "rejected" in verdict:
        findings = [line for line in verdict["rejected"].detail
                    if lane._FINDING_LINE_RE.match(line)]
        assert findings, verdict["rejected"].detail
        assert not any(str(tmp_path) in line or "dfr-precheck-" in line
                       for line in verdict["rejected"].detail)
    else:
        assert verdict["record"]["outcome"] == lane.PRECHECK_VALIDATED
        assert verdict["record"]["documents"] > 0


_CLOSURE_HARNESS = '''\
"""Run RENDER_ENTRY under an audit hook; record every checkout path opened or
listed (lane openxfactory-4, #1161)."""
import os, runpy, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
record = Path(sys.argv[2])
seen = set()


def note(path):
    try:
        seen.add(Path(os.fsdecode(path)).resolve().relative_to(root).as_posix())
    except (TypeError, ValueError, OSError):
        pass


def hook(event, args):
    if event in ("open", "os.listdir", "os.scandir") and args and \\
            isinstance(args[0], (str, bytes, os.PathLike)):
        note(args[0])


sys.addaudithook(hook)
sys.argv = [str(root / sys.argv[3]), *sys.argv[4:]]
code = 0
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
except SystemExit as exc:
    code = exc.code or 0
for module in list(sys.modules.values()):
    if getattr(module, "__file__", None):
        note(module.__file__)
record.write_text("\\n".join(sorted(seen)) + "\\n", encoding="utf-8")
sys.exit(code)
'''


def test_the_render_reads_nothing_outside_the_render_unit(tmp_path):
    """THE MEASUREMENT THE UNIT WAS DECLARED FROM, repeated. The real render,
    through `RENDER_ENTRY`, over this checkout, under an audit hook: every path
    it opens or lists under the checkout is inside the sealed corpus paths or
    a leg's `src/` (or is a directory above one, which the import system
    lists). And every declared file is actually read, so the unit is neither
    too narrow for the child nor wider than the render."""
    head = _git(REPO_ROOT, "rev-parse", "HEAD")
    stamp = _git(REPO_ROOT, "show", "-s", "--format=%cI", head, "--")
    harness = tmp_path / "harness.py"
    harness.write_text(_CLOSURE_HARNESS, encoding="utf-8")
    record = tmp_path / "opened.txt"
    env = {key: value for key, value in os.environ.items()
           if key != "PYTHONPATH"}
    env.update(PYTHONDONTWRITEBYTECODE="1",
               PYTHONPYCACHEPREFIX=str(tmp_path / "pycache"))
    proc = subprocess.run(
        [sys.executable, str(harness), str(REPO_ROOT), str(record),
         lane.RENDER_ENTRY, "generate", "--repo-root", str(REPO_ROOT),
         "--repository", "openxFactory", "--source-revision", head,
         "--generated-at", stamp, "--output", str(tmp_path / "snapshot.json"),
         "--no-validate"],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True,
        timeout=600)
    assert proc.returncode == 0, proc.stderr[-2000:]
    opened = set(record.read_text(encoding="utf-8").split())
    files = {path for path in lane.CORPUS_SEAL_PATHS if path.endswith(".py")}
    roots = [path for path in lane.CORPUS_SEAL_PATHS if not path.endswith(".py")]
    roots += [f"{gitlink}/{leg}/{path}" for gitlink, leg, _package
              in lane.RENDER_LEGS for path in lane.RENDER_LEG_PATHS]
    above = {"/".join(parts[:depth])
             for entry in (*files, *roots) for parts in [entry.split("/")]
             for depth in range(1, len(parts))}
    outside = sorted(
        path for path in opened
        if path not in files and path not in above
        and not any(path == root or path.startswith(root + "/")
                    for root in roots))
    assert outside == []
    # Every file the RENDER unit declares is read by the render. The seal
    # carries the serve's entry as well, which the render never reads: the
    # serve unit is measured on its own, below.
    unit = {path for path in lane.CORPUS_RENDER_PATHS
            if path not in lane.RENDER_LEG_GITLINKS}
    assert unit <= files
    assert unit <= opened, sorted(unit - opened)
    for gitlink, leg, package in lane.RENDER_LEGS:
        assert any(path.startswith(f"{gitlink}/{leg}/src/{package}/")
                   for path in opened), gitlink


# The profile facets the serve reads when the image starts, beyond its build
# step: `ROUTE_EXTENSIONS` for `opendox.serve.build_server()`, and `DISPLAY`
# for its `/capabilities` payload (`scripts/opendox_host.py`, `FACETS`). The
# host profile imports `scripts/profile_openxfactory.py` only when one is
# read, so a build step alone never reaches it.
SERVE_FACETS = ("ROUTE_EXTENSIONS", "DISPLAY")

_SERVE_BUILD_HARNESS = '''\
"""Run SERVE_ENTRY's start under an audit hook, as the served image runs it:
the module body, which is the whole host bootstrap, the web root it composes,
and the profile facets the server reads when it is built (argv[4:]), never
the server loop. Record every checkout path opened, listed or linked
(#1164)."""
import os, runpy, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
record = Path(sys.argv[2])
seen = set()


def note(path):
    try:
        seen.add(Path(os.fsdecode(path)).resolve().relative_to(root).as_posix())
    except (TypeError, ValueError, OSError):
        pass


def hook(event, args):
    if event in ("open", "os.listdir", "os.scandir") and args and \\
            isinstance(args[0], (str, bytes, os.PathLike)):
        note(args[0])


sys.addaudithook(hook)
entry = runpy.run_path(str(root / sys.argv[3]), run_name="image_build")
web_root = Path(entry["_composed_web_root"]())
for linked in sorted(web_root.rglob("*")):
    if linked.is_symlink():
        note(os.readlink(linked))
import opendox_host
profile = opendox_host.profile()
for facet in sys.argv[4:]:
    getattr(profile, facet)
for module in list(sys.modules.values()):
    if getattr(module, "__file__", None):
        note(module.__file__)
record.write_text("\\n".join(sorted(seen)) + "\\n", encoding="utf-8")
'''


def _without_the_checkout_on_the_path(tmp_path: Path) -> dict[str, str]:
    """This process's environment with no `PYTHONPATH`, and bytecode written
    nowhere near a tree under test."""
    env = {key: value for key, value in os.environ.items()
           if key != "PYTHONPATH"}
    env.update(PYTHONDONTWRITEBYTECODE="1",
               PYTHONPYCACHEPREFIX=str(tmp_path / "pycache"))
    return env


def test_the_serve_start_reads_nothing_outside_the_serve_unit(tmp_path):
    """THE MEASUREMENT THE SERVE UNIT WAS DECLARED FROM, repeated (#1164). The
    served image's build step loads `SERVE_ENTRY` as a module, which performs
    its whole host bootstrap, and composes the web root from the carve
    manifest. At start the server then reads its profile facets
    (`SERVE_FACETS`). Run that way over this checkout, under an audit hook,
    every checkout path it opens, lists or links is in the serve unit, a file
    of it or under a tree of it, or is a directory above one, which the
    import system lists. And it reads every file of the unit, and something
    under every tree, so the unit is neither too narrow for the image nor
    wider than its start. The #1164 writer's own measurement, at `c415c3d1`,
    adds every route, and found nothing further."""
    harness = tmp_path / "harness.py"
    harness.write_text(_SERVE_BUILD_HARNESS, encoding="utf-8")
    record = tmp_path / "opened.txt"
    proc = subprocess.run(
        [sys.executable, str(harness), str(REPO_ROOT), str(record),
         lane.SERVE_ENTRY, *SERVE_FACETS],
        cwd=str(tmp_path), env=_without_the_checkout_on_the_path(tmp_path),
        capture_output=True, text=True, timeout=600)
    assert proc.returncode == 0, proc.stderr[-2000:]
    opened = set(record.read_text(encoding="utf-8").split())
    files = {path for path in lane.SERVE_UNIT if not path.endswith("/")}
    trees = [path for path in lane.SERVE_UNIT if path.endswith("/")]
    above = {"/".join(parts[:depth]) for entry in lane.SERVE_UNIT
             for parts in [entry.rstrip("/").split("/")]
             for depth in range(1, len(parts))}
    outside = sorted(
        path for path in opened
        if path not in files and path not in above
        and not any(f"{path}/".startswith(tree) for tree in trees))
    assert outside == []
    assert files <= opened, sorted(files - opened)
    for tree in trees:
        assert any(path.startswith(tree) for path in opened), tree


_RECIPE_BUILD_STEP = '''\
"""The served image's recipe's build step (Omnigent-Install `6b7da477`,
`containers/ideation-dashboard/Dockerfile`), over the runtime tree at argv[1]:
load the entry as a module, which performs its whole host bootstrap, and copy
the web root it composes to argv[2]. A composed link that leads out of the
runtime tree is refused, since a copy that read this checkout would pass here
and fail in the image. Then the profile facets the server reads when the
image starts (argv[3:]), each resolved from the runtime tree."""
import runpy, shutil, sys
from pathlib import Path

app, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
entry = runpy.run_path(str(app / "scripts" / "ideation-dashboard-serve.py"),
                       run_name="image_build")
web_root = Path(entry["_composed_web_root"]())
for linked in sorted(web_root.rglob("*")):
    if linked.is_symlink() and not linked.resolve().is_relative_to(app):
        sys.exit(f"{linked} leads out of the runtime tree, to "
                 f"{linked.resolve()}")
shutil.copytree(web_root, out)
import opendox_host
profile = opendox_host.profile()
for facet in sys.argv[3:]:
    getattr(profile, facet)
# Every module of the unit's own packages came from the runtime tree, a
# namespace package's every path included. `route_extension` too: the lane
# column imports it by its bare name, and the checkout also has a copy at
# `scripts/route_extension.py`, which the unit does not carry. It must be a
# leg's replica, inside the tree (Copilot, PR #1179).
OWN = {"carved_reach", "doc_health", "ideation_dashboard", "opendox",
       "opendox_host", "openxdox", "profile_openxfactory", "route_extension",
       "wire_messages"}
for name, module in sorted(sys.modules.items()):
    if name.split(".")[0] not in OWN:
        continue
    places = ([module.__file__] if getattr(module, "__file__", None)
              else list(getattr(module, "__path__", [])))
    for place in places:
        if not Path(place).resolve().is_relative_to(app):
            sys.exit(f"{name} was imported from outside the runtime tree, "
                     f"from {place}")
'''


def test_the_served_image_starts_from_a_seal_of_this_checkout(tmp_path):
    """THE IMAGE THE CHILD BUILDS CAN START (#1164), short of a container. A
    real seal of this checkout, both legs at the commits HEAD pins. The
    runtime tree is copied out of the SEALED corpus as the recipe copies it,
    `serve_unit` path by path, and the recipe's own build step runs over that
    tree with nothing of this checkout on the path. The host bootstrap
    completes, the web root it composes is whole, every link inside the tree,
    carrying the index and openxFactory's one retained view, and the profile
    facets the server reads at start resolve, every module imported from the
    tree."""
    head = _git(REPO_ROOT, "rev-parse", "HEAD")
    seal = tmp_path / "seal"
    manifest = lane.seal_source(
        corpus_checkout=REPO_ROOT, seal_dir=seal, correlation_id=CORRELATION,
        decision=_decision(head), corpus_ref="HEAD",
        read_recipe=(lambda: RECIPE_TEXT), precheck_render=_stub_precheck)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []
    assert manifest["serve_unit"] == list(SERVE_UNIT)
    # The real unit fills in from the corpus the schemas the legs do not
    # supply, so the record is not empty, and each schema it names is the
    # sealed corpus's own bytes (seal 2.2.0).
    corpus_schemas = manifest["validator_corpus_schemas"]
    assert corpus_schemas
    for name, relpath in corpus_schemas.items():
        assert (seal / lane.SEAL_VALIDATOR_ROOT / lane.VALIDATOR_SCHEMAS_PATH
                / name).read_bytes() == \
            (seal / lane.SEAL_CORPUS_RELPATH / relpath).read_bytes(), name
    corpus_root = seal / lane.SEAL_CORPUS_RELPATH
    app = tmp_path / "app" / "openxFactory"
    for path in manifest["serve_unit"]:
        source, target = corpus_root / path, app / path
        if path.endswith("/"):
            shutil.copytree(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    harness = tmp_path / "build-step.py"
    harness.write_text(_RECIPE_BUILD_STEP, encoding="utf-8")
    web = tmp_path / "web"
    proc = subprocess.run(
        [sys.executable, str(harness), str(app), str(web), *SERVE_FACETS],
        cwd=str(tmp_path), env=_without_the_checkout_on_the_path(tmp_path),
        capture_output=True, text=True, timeout=600)
    assert proc.returncode == 0, proc.stderr[-2000:]
    assert (web / "index.html").is_file()
    assert (web / "views" / "intent-feed.js").is_file()
