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
    inject a stub unit, as they inject the recipe. The tests that are about
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

import hashlib
import json
import os
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


def _stub_validator(where: Path) -> "lane.PinnedValidator":
    """A composed-unit STAND-IN: `scripts/` beside `contracts/schemas/`, the
    shape `nightly_lane._pinned_validator()` answers. The script prints `ok`
    and exits 0, whatever it is handed, so it is always "available" and never
    a verdict on anything. Tests about the seal's own mechanics inject this,
    as they inject the recipe. Tests about the VALIDATOR use the real one."""
    script = where / lane.VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
    schemas = where / lane.VALIDATOR_SCHEMAS_PATH
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / STUB_SCHEMA).write_text("{}\n", encoding="utf-8")
    return lane.PinnedValidator(runnable=script)


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


def _stub_legs_carrying(product_module: str | None):
    """A leg-sealer STAND-IN whose openXdox leg carries `product_module` as the
    product module the parent classifies with, or none at all."""
    def stub_legs(*, corpus_checkout, source_head, corpus_root, runner):
        return _stub_leg_records(corpus_root, product_module)
    return stub_legs


def _stub_legs(*, corpus_checkout, source_head, corpus_root, runner):
    """A leg-sealer STAND-IN: one module per product under the path the real
    sealer extracts to, the real product module in the validator leg, and
    records shaped exactly like its own. Tests about the seal's other
    mechanics inject it, as they inject the recipe. The tests about the legs
    run `seal_render_legs` over real nested submodules."""
    return _stub_leg_records(corpus_root, PRODUCT_MODULE_TEXT)


def _stub_leg_records(corpus_root, product_module: str) -> list[dict]:
    records = []
    for index, (gitlink, leg, package) in enumerate(lane.RENDER_LEGS):
        modules = Path(corpus_root) / gitlink / leg / "src" / package
        modules.mkdir(parents=True)
        (modules / "__init__.py").write_text(f"# stand-in {package}\n",
                                             encoding="utf-8")
        count = 1
        if (gitlink, leg) == lane.VALIDATOR_LEG and product_module is not None:
            (modules / lane.SEALED_PRODUCT_MODULE).write_text(
                product_module, encoding="utf-8")
            count = 2
        records.append({
            "gitlink": gitlink, "gitlink_revision": str(index + 1) * 40,
            "leg": leg,
            "leg_revision": (_product_head() if (gitlink, leg) == lane.VALIDATOR_LEG
                             else str(index + 5) * 40),
            "package": package,
            "relpath": f"{lane.SEAL_CORPUS_RELPATH}/{gitlink}/{leg}",
            "paths": list(lane.RENDER_LEG_PATHS), "file_count": count,
            "schema_leg": lane.SCHEMA_LEG,
            "schema_leg_revision": str(index + 7) * 40})
    return records


STUB_PRECHECK = {"entry": lane.RENDER_ENTRY, "documents": 0, "strict": True,
                 "outcome": lane.PRECHECK_VALIDATED, "returncode": 0}


def _stub_precheck(seal_root, *, source_head, source_committed_at):
    """A pre-dispatch-render STAND-IN that passes. The render's own mechanics
    are tested over a stand-in entry, and the real render over this checkout."""
    return dict(STUB_PRECHECK)


def _seal(corpus: Path, seal_dir: Path, *, decision: dict | None = None,
          recipe: str | None = RECIPE_TEXT, resolve_validator=_STUB,
          seal_legs=_STUB, precheck_render=_STUB, **kw) -> dict:
    """`seal_source` over the fixture corpus. `None` for `resolve_validator`,
    `seal_legs` or `precheck_render` means the REAL one (the snapshot lane's
    own resolver, `seal_render_legs`, `precheck_sealed_render`); the default
    injects the stand-in."""
    head = _git(corpus, "rev-parse", "HEAD")
    if resolve_validator is _STUB:
        stub = _stub_validator(Path(seal_dir).parent / "stub-validator")
        resolve_validator = (lambda: stub)
    return lane.seal_source(
        corpus_checkout=corpus, seal_dir=seal_dir,
        correlation_id=kw.pop("correlation_id", CORRELATION),
        decision=decision if decision is not None else _decision(head),
        corpus_ref=kw.pop("corpus_ref", "HEAD"),
        read_recipe=(lambda: recipe),
        resolve_validator=resolve_validator,
        seal_legs=_stub_legs if seal_legs is _STUB else seal_legs,
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
    # The run outcomes the intake accepts are the product's own two verdicts.
    assert lane.VALIDATOR_VERDICT_OUTCOMES == (snapshot_mod.VALIDATED,
                                               snapshot_mod.NOT_CONFORMANT)


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


@pytest.mark.parametrize("shape", ["a-dangling-link", "a-directory"])
def test_a_unit_entry_that_is_not_a_regular_file_is_refused_by_name(
        corpus, tmp_path, shape):
    """The seal copies the composed unit's schemas THROUGH their links. An
    entry it cannot copy as a regular file is refused BY NAME, never skipped.
    A skipped schema would seal a narrower unit than the one the snapshot lane
    validates with, and the probe could not see it, because the validator asks
    for a family schema only when an instance needs one. The stub script here
    reaches a verdict on anything, so only the copy can refuse."""
    stub = _stub_validator(tmp_path / "unit")
    odd = (tmp_path / "unit" / lane.VALIDATOR_SCHEMAS_PATH
           / "ideation-dashboard-workbench.schema.yaml")
    if shape == "a-dangling-link":
        odd.symlink_to(tmp_path / "nowhere.schema.yaml")
    else:
        odd.mkdir()
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", resolve_validator=lambda: stub)
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
    review of #1162). Only a unit with no product tree at all records none,
    which is what the stub unit seals. The runner answers the one product
    read here, so no real tree has to be broken to ask it."""
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
    stub = _stub_validator(where)
    stub.runnable.write_text(f"RECORD = {str(record)!r}\n" + _RECORDING_VALIDATOR,
                             encoding="utf-8")
    return stub


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
# What the render's environment adds to the allowlisted names.
_RENDER_ENV_GIVEN = {"HOME", "PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING",
                     "GIT_CEILING_DIRECTORIES", "GIT_CONFIG_GLOBAL",
                     "GIT_CONFIG_NOSYSTEM"}


def _export_the_job_environment(monkeypatch) -> None:
    for name, value in _JOB_ENVIRONMENT.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("LC_ALL", "C.UTF-8")


def _assert_the_renders_environment(env: dict, seal: Path) -> None:
    """ALLOWLISTED: nothing of the job's reaches sealed code but the kept names
    and what the render is given. (An interpreter adds nothing to its own
    environ.) Git reads no configuration of the job's and cannot climb out of
    the seal, and HOME is a scratch directory."""
    for name in _JOB_ENVIRONMENT:
        assert name not in env, name
    assert not any(value in _JOB_SECRETS for value in env.values())
    assert {name for name in env
            if name not in lane._RENDER_ENV_KEPT and name not in _RENDER_ENV_GIVEN
            and not name.startswith(lane._RENDER_ENV_KEPT_PREFIXES)} == set()
    assert env["LC_ALL"] == "C.UTF-8"
    assert env["PYTHONDONTWRITEBYTECODE"] == "1"
    assert str(seal.resolve()) in env["GIT_CEILING_DIRECTORIES"].split(os.pathsep)
    assert env["GIT_CONFIG_GLOBAL"] == os.devnull
    assert env["GIT_CONFIG_NOSYSTEM"] == "1"
    assert env["HOME"] != os.environ.get("HOME")
    assert not Path(env["HOME"]).resolve().is_relative_to(seal.resolve())
    assert "PATH" in env                     # the interpreter still resolves


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
    stub = _stub_validator(tmp_path / "unit")
    target = ("docs/a.md" if change == "a-file-rewritten"
              else "docs/planted.md")
    stub.runnable.write_text(
        "from pathlib import Path\n"
        "seal = Path(__file__).resolve().parents[2]\n"
        f"(seal / 'openxFactory' / {target!r}).write_text('planted\\n')\n"
        "print('ok')\n", encoding="utf-8")
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
    _seal(corpus, seal, seal_legs=_stub_legs_carrying(
        _recording_product_module(record)))
    assert record.read_text(encoding="utf-8").splitlines() == [
        str(lane.sealed_product_module(seal))]


def test_a_seal_without_the_product_module_cannot_classify_its_probe(
        corpus, tmp_path):
    """A sealed openXdox leg that carries no product module leaves the parent
    nothing to read the probe with, so the seal is refused, naming why."""
    with pytest.raises(lane.SealRefused) as refused:
        _seal(corpus, tmp_path / "seal", seal_legs=_stub_legs_carrying(None))
    reason = str(refused.value)
    assert reason.startswith("the sealed validator could NOT RUN")
    assert "the validator's harness returned no verdict (exit 1)" in reason
    assert "cannot import name 'snapshot' from 'openxdox'" in reason
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_the_confined_locator_never_adopts_the_sealed_validator(corpus, tmp_path):
    """THE WALK THIS TEST ONCE PROVED IS GONE, ON PURPOSE. Since openXdox-code
    `e28930bf` (split-opendox-two-layer-product § 8.9 residue (iii)),
    `snapshot.find_validator` answers only for the product's OWN validator. It
    CONFINES instead of walking up: a start outside the product's tree answers
    None. So the sealed copy is never adopted from where it sits, from the seal
    root, from the directory the child hands `--repo-root`, or from its own
    directory. A caller that means it passes it explicitly
    (`validate_snapshot(..., validator=...)`), and that channel is proven here
    too. As before, this runs the REAL locator over a REAL sealed tree rather
    than restating a path. Since #1158 the sealed copy lives under the seal's
    own `validator/` root, and the refresh lane's seal rationale says so.
    """
    seal = tmp_path / "seal"
    _seal(corpus, seal)
    corpus_root = seal / lane.SEAL_CORPUS_RELPATH
    sealed = seal / lane.SEAL_VALIDATOR_RELPATH
    assert sealed.is_file()
    for start in (seal, corpus_root, sealed.parent):
        assert snapshot_mod.find_validator(start) is None, start
    own = snapshot_mod.find_validator()
    assert own is None or not own.resolve().is_relative_to(seal.resolve())
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
    assert manifest["validator_revision"] is None         # the stub has no tree
    assert manifest["validator_probe"] == {
        "kind": lane.VALIDATOR_PROBE["kind"],
        "outcome": snapshot_mod.VALIDATED, "returncode": 0}
    # The render unit (#1161): the entry the child runs, both legs, and what
    # the pre-dispatch render answered.
    assert manifest["render_entry"] == lane.RENDER_ENTRY
    assert f"{lane.SEAL_CORPUS_RELPATH}/{lane.RENDER_ENTRY}" in manifest["files"]
    assert [(leg["gitlink"], leg["leg"], leg["package"])
            for leg in manifest["render_legs"]] == list(lane.RENDER_LEGS)
    assert manifest["precheck"] == STUB_PRECHECK
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


def test_a_non_empty_seal_directory_is_refused(corpus, tmp_path):
    """A seal is a FRESH tree, never an overlay on one. `files` is the
    authority on what the child must find, so a leftover from an earlier
    attempt would be indexed, digested and shipped as though the parent had
    sealed it."""
    seal = tmp_path / "seal"
    seal.mkdir()
    (seal / "leftover.txt").write_text("from an earlier attempt\n",
                                       encoding="utf-8")
    with pytest.raises(lane.SealRefused, match="not empty"):
        _seal(corpus, seal)
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
                  "render_entry", "render_legs", "precheck"):
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
        "sealed validator ran to a verdict",
        f"render_entry is None, expected {lane.RENDER_ENTRY!r} — the child "
        "would have no renderer to run",
        "render_legs is None — the seal records no render unit, so the "
        "child's render would reach no product",
    ]
    assert lane.SEAL_SCHEMA_VERSION.split(".", 1)[0] == "2"


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
            "verdict"],
    }[tamper]
    assert lane.verify_seal(seal) == expected


def test_verify_refuses_a_validator_revision_that_is_not_a_full_revision(
        corpus, tmp_path):
    """Null is what a unit with no product tree records, and it verifies. A
    revision that IS recorded must be a full one. The seal refuses to write
    anything else, so a manifest carrying anything else was not written by
    it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    assert manifest["validator_revision"] is None
    assert lane.verify_seal(seal) == []
    manifest["validator_revision"] = "abc1234"
    (seal / lane.SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert lane.verify_seal(seal) == [
        "validator_revision is 'abc1234', expected a full commit revision or "
        "null"]


# ---------------------------------------------------------------------------
# the seal speaks git, and only git, beside one run of the sealed validator
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("resolve_validator", [_STUB, None],
                         ids=["stub-unit", "the-real-resolver"])
def test_the_seal_speaks_only_git_and_never_builds_or_pushes(corpus, tmp_path,
                                                             resolve_validator):
    """Every shell-out through the seal's runner is `git`: the archive, the two
    revision reads and, with the real resolver, the product revision the
    sealed validator came from. The one run of the sealed validator is not a
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
    assert verbs <= {"archive", "show", "rev-parse"}, verbs
    _assert_exact_reads(runner)
    assert not hasattr(lane, "build_and_push")


# ---------------------------------------------------------------------------
# the CLI phase — the dispatch gate, and a refusal that never fails the run
# ---------------------------------------------------------------------------

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
               "--seal-out", str(tmp_path / "seal"),
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
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


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
    manifest = lane.read_seal_manifest(tmp_path / "seal")
    assert manifest["tree_digest"] == result["tree_digest"]
    assert lane.verify_seal(tmp_path / "seal", correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []


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

    def rejecting(seal_root, *, source_head, source_committed_at):
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
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()
    said = capsys.readouterr().out
    assert "STRICT FAILED" in said and findings[0] in said


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

def _product(where: Path, name: str, code_leg: str, package: str) -> Path:
    """A product shaped like openDox or openXdox: a repository whose `spec`
    and `code` legs are its own submodules. The code leg carries its package
    under `src/`, a module BESIDE the package (openXdox-code's `src/` has two),
    and a `tests/` tree and a `pyproject.toml` the render unit must not carry."""
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
            if package == "openxdox":
                # The product module the parent classifies with, out of the
                # sealed leg.
                (modules / lane.SEALED_PRODUCT_MODULE).write_text(
                    PRODUCT_MODULE_TEXT, encoding="utf-8")
            (repo / "src" / "extension.py").write_text(
                "# beside the package\n", encoding="utf-8")
            (repo / "tests").mkdir()
            (repo / "tests" / "test_leg.py").write_text("# never sealed\n",
                                                        encoding="utf-8")
            (repo / "pyproject.toml").write_text(
                f'[project]\nname = "{package}"\n', encoding="utf-8")
        else:
            (repo / "README.md").write_text(f"# {name} spec\n", encoding="utf-8")
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


@pytest.fixture
def corpus_with_products(corpus: Path, tmp_path: Path) -> Path:
    """The fixture corpus with both products MOUNTED, as openxFactory mounts
    them: each a gitlink, each product's legs its own gitlinks, all
    materialized at the commits they are pinned at."""
    upstream = tmp_path / "upstream"
    for gitlink, leg, package in lane.RENDER_LEGS:
        product = _product(upstream, gitlink, leg, package)
        _git(corpus, "-c", "protocol.file.allow=always", "submodule", "add",
             "--quiet", str(product), gitlink)
    _git(corpus, "-c", "protocol.file.allow=always", "submodule", "update",
         "--init", "--recursive", "--quiet")
    _git(corpus, "commit", "--quiet", "-m", "mount the products")
    return corpus


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
        carried = ["src/extension.py", f"src/{package}/__init__.py",
                   f"src/{package}/cli.py"]
        if (gitlink, leg) == lane.VALIDATOR_LEG:
            carried.append(f"src/{package}/{lane.SEALED_PRODUCT_MODULE}")
        assert _leg_files(sealed) == sorted(carried)
        assert record["file_count"] == len(carried)
        assert sorted(path.name for path in (corpus_root / gitlink).iterdir()) \
            == [leg]
    assert sorted(path.name for path in corpus_root.iterdir()) == \
        sorted(lane.RENDER_LEG_GITLINKS)


def test_a_seal_with_real_legs_verifies(corpus_with_products, tmp_path):
    corpus = corpus_with_products
    head = _git(corpus, "rev-parse", "HEAD")
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal, seal_legs=None)
    assert lane.verify_seal(seal, correlation_id=CORRELATION,
                            corpus_revision=head,
                            recipe_revision=RECIPE_REV) == []
    legs = [key for key in manifest["files"]
            if key.split("/")[1:2] in (["openDox"], ["openXdox"])]
    assert len(legs) == sum(record["file_count"]
                            for record in manifest["render_legs"]) == 7


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
    assert problems(lambda m: m["render_legs"][0].update(file_count=9)) == [
        "the openDox code leg records file_count 9, but the seal indexes 1 "
        "file(s) under openxFactory/openDox/code/"]
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
        "the openXdox code leg records file_count 2, but the seal indexes 0 "
        "file(s) under openxFactory/openXdox/code/"]


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
    lacks: the child could not render from it."""
    seal = tmp_path / "seal"
    manifest = _seal(corpus, seal)
    shutil.rmtree(seal / lane.SEAL_CORPUS_RELPATH / "openDox")
    shutil.rmtree(seal / lane.SEAL_CORPUS_RELPATH / "openXdox")
    (seal / lane.SEAL_CORPUS_RELPATH / lane.RENDER_ENTRY).unlink()
    for field in ("render_entry", "render_legs", "precheck"):
        del manifest[field]
    manifest["schema_version"] = "2.0.0"
    _rewrite_coherently(seal, manifest)
    assert lane.verify_seal(seal) == [
        f"render_entry is None, expected {lane.RENDER_ENTRY!r} — the child "
        "would have no renderer to run",
        "render_legs is None — the seal records no render unit, so the "
        "child's render would reach no product"]


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
        stand_in_seal, tmp_path, monkeypatch):
    """The entry runs from the SEALED corpus root, with the seal's two anchors
    and `--no-validate`, writing outside the seal. Then the SEALED validator
    runs over what it wrote, under `--strict`. The record it returns is what
    the manifest's `precheck` says."""
    record = _precheck(stand_in_seal)
    assert record == {"entry": lane.RENDER_ENTRY, "documents": 3,
                      "strict": True, "outcome": lane.PRECHECK_VALIDATED,
                      "returncode": 0}
    ran = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))
    corpus_root = stand_in_seal / lane.SEAL_CORPUS_RELPATH
    output = ran["argv"][ran["argv"].index("--output") + 1]
    assert ran["argv"] == [
        "generate", "--repo-root", str(corpus_root),
        "--repository", "openxFactory", "--source-revision", HEAD_REV,
        "--generated-at", COMMITTED_AT, "--output", output, "--no-validate"]
    assert Path(ran["cwd"]).resolve() == corpus_root.resolve()
    assert not Path(output).resolve().is_relative_to(stand_in_seal.resolve())
    # The validator judges a COPY of exactly the bytes the render wrote, in a
    # directory the render never saw, under `--strict`.
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    handed = Path(judged["argv"][0])
    assert judged["argv"][1:] == ["--strict"]
    assert handed.name == "snapshot.json" and handed.is_absolute()
    assert handed.parent != Path(output).resolve().parent
    assert not handed.is_relative_to(stand_in_seal.resolve())
    assert judged["sha256"] == \
        (tmp_path / "entry.json.sha256").read_text(encoding="utf-8")


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
        stand_in_seal, tmp_path, monkeypatch):
    """The nightly names its seal `dfr-seal`, relative to the job's working
    directory, and the render runs from INSIDE the seal. So every path the
    render and the validator are handed is absolute. A relative one would be
    read from the wrong directory, and every nightly seal would be refused
    as a render that could not run."""
    monkeypatch.chdir(tmp_path)
    record = lane.precheck_sealed_render(Path(stand_in_seal.name),
                                         source_head=HEAD_REV,
                                         source_committed_at=COMMITTED_AT)
    assert record["outcome"] == lane.PRECHECK_VALIDATED
    assert record["documents"] == 3
    ran = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))
    corpus_root = (stand_in_seal / lane.SEAL_CORPUS_RELPATH).resolve()
    assert ran["argv"][ran["argv"].index("--repo-root") + 1] == str(corpus_root)
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    assert Path(judged["argv"][0]).is_absolute()


def test_the_pre_dispatch_render_holds_no_credential_and_no_repository(
        stand_in_seal, tmp_path, monkeypatch):
    """It runs code read OUT OF THE SEAL, in a job that holds the App token and
    a token-bearing git configuration. So it receives neither: no credential,
    none of the job's GitHub or Git variables, no interpreter path override, a
    scratch HOME, no bytecode written, and git may not climb out of the seal
    into the aggregation checkout it sits in, which the child's seal never
    has above it."""
    _export_the_job_environment(monkeypatch)
    _precheck(stand_in_seal)
    env = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))["env"]
    _assert_the_renders_environment(env, stand_in_seal)
    assert env["GIT_CEILING_DIRECTORIES"] == str(stand_in_seal.resolve())


def test_the_sealed_validator_runs_in_the_renders_environment_too(
        stand_in_seal, tmp_path, monkeypatch):
    """The sealed validator is sealed code as well. The product's
    `validate_snapshot` launches it with no environment of its own, so a call
    made in this process would have handed it every credential of the job
    (Copilot, PR #1166). It runs in the render's allowlisted environment, from
    a scratch directory outside the seal, and git can climb out of neither."""
    _export_the_job_environment(monkeypatch)
    _precheck(stand_in_seal)
    judged = json.loads((tmp_path / "validator.json").read_text(encoding="utf-8"))
    env = judged["env"]
    _assert_the_renders_environment(env, stand_in_seal)
    cwd = Path(judged["cwd"]).resolve()
    assert not cwd.is_relative_to(stand_in_seal.resolve())
    assert cwd != Path.cwd().resolve()
    assert str(cwd.parent) in env["GIT_CEILING_DIRECTORIES"].split(os.pathsep)


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


@pytest.mark.parametrize("mode, what", [
    ("link-out", "a symbolic link"),
    ("hard-link", "a hard link to another file"),
    ("directory", "a directory"),
    ("fifo", "not a regular file"),
], ids=["a-link-out-of-the-scratch-directory", "a-hard-link", "a-directory",
        "a-fifo"])
def test_render_output_that_is_not_a_file_of_its_own_is_refused(
        stand_in_seal, tmp_path, mode, what):
    """The render is sealed code, and its output is read by the parent, then
    validated and quoted in the findings. A link there would hand the parent
    any file on this host, here a valid snapshot the render put elsewhere
    (Copilot, PR #1166). So the output must be a regular file of its own, and
    nothing else is read or validated."""
    _configure(tmp_path, render=mode)
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    assert str(refused.value) == (
        f"the sealed render's output is {what}, not a file of its own, so the "
        "parent will not read it: a link could hand the parent any file on "
        "this host to validate and quote")
    assert not (tmp_path / "validator.json").exists()      # nothing judged


def test_a_scratch_directory_the_render_swapped_is_never_read_through(
        stand_in_seal, tmp_path):
    """The render may replace the scratch directory's path with a link to
    another directory holding a valid snapshot (Copilot, PR #1166). The
    parent reads through the handle it took on the directory it made, before
    the render ran, and that directory holds no output. So nothing is
    validated, and the refusal is the render's own failure."""
    _configure(tmp_path, render="swap-scratch")
    with pytest.raises(lane.SealRefused) as refused:
        _precheck(stand_in_seal)
    assert str(refused.value).startswith(
        "the sealed render unit could not render the snapshot (exit 0)")
    assert not (tmp_path / "validator.json").exists()      # nothing judged
    ran = json.loads((tmp_path / "entry.json").read_text(encoding="utf-8"))
    scratch = Path(ran["argv"][ran["argv"].index("--output") + 1]).parent
    assert scratch.is_symlink()                  # the swap really happened
    scratch.unlink()
    shutil.rmtree(str(scratch) + ".moved")


@pytest.mark.parametrize("replacement", ["a-link-to-the-moved-seal",
                                         "a-copy-in-its-place"])
def test_a_seal_directory_the_render_replaced_gets_no_manifest(
        corpus, tmp_path, replacement):
    """Sealed code runs inside the seal directory, so it could move it and
    put a link, or a copy with the same content, where it was. The index
    would match either. The directory is held by identity from its creation,
    so either is refused, and no manifest is written anywhere (Copilot,
    PR #1166)."""
    seal = tmp_path / "seal"
    moved = tmp_path / "seal.moved"

    def replacing(seal_root, *, source_head, source_committed_at):
        Path(seal_root).rename(moved)
        if replacement == "a-link-to-the-moved-seal":
            Path(seal_root).symlink_to(moved, target_is_directory=True)
        else:
            shutil.copytree(moved, seal_root)
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


def test_a_seal_directory_that_is_a_link_is_refused(corpus, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    link = tmp_path / "seal"
    link.symlink_to(empty, target_is_directory=True)
    with pytest.raises(lane.SealRefused, match="is not a directory of its own"):
        _seal(corpus, link)
    assert list(empty.iterdir()) == []


def test_a_render_output_swapped_after_its_check_is_refused(tmp_path,
                                                            monkeypatch):
    """The output is checked, then opened without following a link, and
    checked again through the descriptor. A swap between the two is
    refused."""
    first = tmp_path / "snapshot.json"
    first.write_text("{}", encoding="utf-8")
    other = tmp_path / "other.json"
    other.write_text("{}", encoding="utf-8")
    checked, real = os.lstat(other), os.stat
    monkeypatch.setattr(
        lane.os, "stat",
        lambda path, *a, **kw: checked if Path(path) == first
        else real(path, *a, **kw))
    with pytest.raises(lane.SealRefused, match="a file that was swapped after "
                                               "it was checked"):
        lane._read_render_output(first)
    monkeypatch.undo()
    assert lane._read_render_output(first) == b"{}"


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


def test_a_strict_rejection_is_a_verdict_carrying_the_findings(
        stand_in_seal, tmp_path):
    """`StrictGateRejected`: the validator's own findings, with the scratch
    path reduced to the file's name, and the tracking issue of every finding
    it knows, counted, so a rejection that also carries a new finding never
    reads as fully tracked."""
    _configure(tmp_path, validator="findings")
    with pytest.raises(lane.StrictGateRejected) as rejected:
        _precheck(stand_in_seal)
    reason = str(rejected.value)
    assert reason.startswith(
        "--strict REJECTED the snapshot this seal renders "
        "(validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)), a "
        "known defect, tracked as opensoft/openxFactory#1159 (3 of 4 "
        "finding(s); 1 tracked by no known issue); the child's publication "
        "gate would refuse it the same way, so nothing is dispatched")
    assert rejected.value.detail == [
        *(f"ERROR [snapshot-dangling-cluster-ref] snapshot.json: possible "
          f"{pos!r} claiming_clusters references unknown cluster 'cl-plane-1'"
          for pos in ("pos-a", "pos-b", "pos-c")),
        "ERROR [snapshot-dangling-cluster-ref] snapshot.json: possible 'pos-d' "
        "claiming_clusters references unknown cluster 'cl-other-2'",
        "validate-ideation-dashboard-contracts: 4 error(s), 0 warning(s)"]


def test_a_tracked_finding_past_the_detail_cap_is_still_cited(
        stand_in_seal, tmp_path):
    """The citation reads EVERY line the validator wrote, and only the detail
    the verdict carries is capped (Copilot, PR #1166). Here the one tracked
    finding is the 61st, past `DETAIL_CAP`."""
    _configure(tmp_path, validator="many-findings")
    with pytest.raises(lane.StrictGateRejected) as rejected:
        _precheck(stand_in_seal)
    assert "tracked as opensoft/openxFactory#1159 (1 of 61 finding(s); 60 " \
        "tracked by no known issue)" in str(rejected.value)
    assert len(rejected.value.detail) == lane.DETAIL_CAP
    assert not any("cl-plane-1" in line for line in rejected.value.detail)


def test_a_render_that_does_not_finish_is_refused(stand_in_seal):
    def hanging(argv, **kw):
        raise subprocess.TimeoutExpired(argv, kw.get("timeout"))

    with pytest.raises(lane.SealRefused, match="did not finish within 7s"):
        lane.precheck_sealed_render(stand_in_seal, source_head=HEAD_REV,
                                    source_committed_at=COMMITTED_AT,
                                    run=hanging, timeout=7)


_A_VALIDATED_VERDICT = json.dumps({
    "ok": True, "returncode": 0, "stdout": "", "stderr": "",
    "outcome": "validated", "unavailable_reason": None})


@pytest.mark.parametrize("harness, said", [
    ("hangs", "the validator did not finish within 7s"),
    ("cannot-launch", "the validator could not be launched in the render's "
                      "environment (OSError: exec format error)"),
    ("says-nothing", "the validator's harness returned no verdict (exit 0)"),
    ("prints-no-object", "the validator's harness returned no verdict (exit 0)"),
    ("prints-another-shape", "the validator's harness returned no verdict "
                             "(exit 0)"),
    ("exits-non-zero", "the validator's harness returned no verdict (exit 1)"),
], ids=["hangs", "cannot-launch", "says-nothing", "prints-no-object",
        "prints-another-shape", "exits-non-zero"])
def test_a_validator_run_that_reaches_no_verdict_is_refused(stand_in_seal,
                                                            harness, said):
    """The validator's run is bounded, and only a harness that exits cleanly
    with a verdict of the product's own shape has answered. Anything else is
    the product's own "could not run", never a verdict on the corpus. That
    holds even for a harness that printed "validated" before exiting non-zero.
    The render is real here, and only the harness is stood in for."""
    bounds: list = []

    def run(argv, **kw):
        if argv[1:2] != ["-c"]:
            return subprocess.run(argv, **kw)
        bounds.append(kw.get("timeout"))
        if harness == "hangs":
            raise subprocess.TimeoutExpired(argv, kw.get("timeout"))
        if harness == "cannot-launch":
            raise OSError("exec format error")
        stdout = {"says-nothing": "",
                  "prints-no-object": "[]\n",
                  "prints-another-shape": _A_VALIDATED_VERDICT.replace(
                      '"validated"', '"maybe"') + "\n",
                  "exits-non-zero": _A_VALIDATED_VERDICT + "\n"}[harness]
        return subprocess.CompletedProcess(
            argv, 1 if harness == "exits-non-zero" else 0, stdout, "")

    with pytest.raises(lane.SealRefused) as refused:
        lane.precheck_sealed_render(stand_in_seal, source_head=HEAD_REV,
                                    source_committed_at=COMMITTED_AT,
                                    run=run, timeout=7)
    assert not isinstance(refused.value, lane.StrictGateRejected)
    reason = str(refused.value)
    assert reason.startswith("the sealed validator could NOT RUN over the "
                             "snapshot this seal renders")
    assert said in reason
    assert bounds == [7]                      # the validator's run is bounded


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
    """Moving the call into the render's environment changes WHERE it runs,
    never what it answers. Over each of the product's outcomes, including its
    own attribution of a harness exit over an unreadable target to the data,
    the fenced call returns the product's in-process result, field for
    field."""
    validator = tmp_path / "validator.py"
    if mode == "a-directory":
        validator.mkdir()
    else:
        validator.write_text(f"MODE = {mode!r}\n" + _MODAL_VALIDATOR,
                             encoding="utf-8")
    target = tmp_path / "target.json"
    target.write_text(target_text, encoding="utf-8")
    fenced = lane.validate_in_render_environment(
        snapshot_mod, target, validator=validator, strict=strict,
        seal_root=tmp_path, module_file=Path(snapshot_mod.__file__))
    own = snapshot_mod.validate_snapshot(target, validator=validator,
                                         strict=strict)
    for name in ("ok", "returncode", "stdout", "stderr", "outcome",
                 "unavailable_reason"):
        assert getattr(fenced, name) == getattr(own, name), name
    assert fenced.validator == Path(own.validator).resolve()


@pytest.mark.parametrize("lines, cited", [
    (["ERROR [snapshot-dangling-cluster-ref] s.json: x 'cl-plane-1'"] * 3,
     "known defect, tracked as opensoft/openxFactory#1159 (3 of 3 finding(s))"),
    (["ERROR [snapshot-dangling-cluster-ref] s.json: x 'cl-plane-10'"], ""),
    (["ERROR [snapshot-unknown-kind] s.json: x 'cl-plane-1'"], ""),
    (["validate-ideation-dashboard-contracts: 0 error(s), 1 warning(s)"], ""),
    ([], ""),
], ids=["all-known", "another-cluster", "another-code", "no-finding-line",
        "nothing"])
def test_a_citation_is_made_only_for_the_finding_it_tracks(lines, cited):
    """The citation retires itself: once the corpus is fixed the finding is
    gone, and a different finding, even one naming a lookalike value or the
    same value under another code, is never cited against an issue that is
    not its own."""
    assert lane.known_finding_citation(lines) == cited


def test_the_precheck_outcome_is_the_products_own_spelling():
    assert lane.PRECHECK_VALIDATED == snapshot_mod.VALIDATED


def test_a_precheck_that_changes_the_sealed_tree_is_refused(corpus, tmp_path):
    def writing(seal_root, *, source_head, source_committed_at):
        (Path(seal_root) / lane.SEAL_CORPUS_RELPATH / "docs" / "new.md"
         ).write_text("written by the render\n", encoding="utf-8")
        return dict(STUB_PRECHECK)

    with pytest.raises(lane.SealRefused, match="changed the sealed tree"):
        _seal(corpus, tmp_path / "seal", precheck_render=writing)
    assert not (tmp_path / "seal" / lane.SEAL_MANIFEST_NAME).exists()


def test_a_rejected_precheck_leaves_no_manifest(corpus, tmp_path):
    def rejecting(seal_root, *, source_head, source_committed_at):
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

    def planting(seal_root, *, source_head, source_committed_at):
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
    assert files <= opened, sorted(files - opened)
    for gitlink, leg, package in lane.RENDER_LEGS:
        assert any(path.startswith(f"{gitlink}/{leg}/src/{package}/")
                   for path in opened), gitlink
