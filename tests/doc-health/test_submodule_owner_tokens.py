"""One App installation token per governed submodule OWNER, in numbered slots.

opensoft/xFactory#366. The aggregation's governed submodule set spans
organizations, and an App INSTALLATION token reaches exactly one of them, so
the reusable workflow mints a token per foreign owner. The first cut of that
block handled ONE foreign owner and refused a second; when
`xFactories/LedgerxFactory` moved to `ledgerXfactory` (aggregation commit
99f1643, 2026-09-07) while the two Medx submodules stayed on `MedxSoft`, every
nightly from 2026-09-08 died in the detection step before building a bundle —
0 artifacts, which also starves the child lanes' provenance gate.

Two properties are pinned here, both of them things a refactor can drop
silently and neither of them visible in a green run:

  * THE SLOT COUNT IS ONE NUMBER. `FOREIGN_OWNER_SLOTS` feeds the refusal
    message, the detection's own slot loop, and (through the `slots` output)
    the rewrite step. If it stops matching the mint steps actually present,
    the workflow either refuses owners it could serve or reads an owner it
    never minted for — so the count is asserted against the steps in BOTH
    jobs, which are twins and drift apart exactly because nothing compares
    them.

  * EACH OWNER IS CREDENTIALED IN BOTH URL FORMS. `.gitmodules` is the
    authority on the URL as well as the owner and is free to spell either
    form: `xFactories/MedxEHR` declares its `spec`/`code` legs as
    `https://github.com/MedxSoft/...`, which an ssh-keyed `insteadOf` never
    matched, and that alone reddened the three nightlies of 2026-09-05..07
    with `fatal: could not read Username for 'https://github.com'`.

The structural assertions read the workflow; the behavioral ones RUN the two
shell steps against synthetic `.gitmodules` trees and read the git config they
produce back through `git ls-remote --get-url`, because prefix resolution
("longest match wins", which is what lets the broad org rewrite stay) is a
property of git and not of this file."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

WORKFLOW = (Path(__file__).resolve().parents[2]
            / ".github" / "workflows" / "doc-health-reusable.yml")

JOBS = ("prepare", "finalize")

DETECT = "Detect foreign submodule owners"
REWRITE = "Rewrite foreign-owner submodule URLs"
BROAD = "Rewrite ssh submodule URLs for token auth"
MINT = "Mint app token for foreign submodule owner {}"


def workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def steps(job):
    return workflow()["jobs"][job]["steps"]


def step(job, name):
    matches = [s for s in steps(job) if s.get("name") == name]
    assert len(matches) == 1, f"expected exactly one step named {name!r} in {job}"
    return matches[0]


def slots(job):
    return int(step(job, DETECT)["env"]["FOREIGN_OWNER_SLOTS"])


# --- the slot count is one number -----------------------------------------

def test_both_jobs_declare_the_same_slot_count():
    assert slots("prepare") == slots("finalize")


def test_the_slot_count_equals_the_mint_steps_present():
    for job in JOBS:
        count = slots(job)
        names = {s.get("name") for s in steps(job)}
        for index in range(1, count + 1):
            assert MINT.format(index) in names, \
                f"{job} declares {count} slots but has no step for slot {index}"
        assert MINT.format(count + 1) not in names, \
            f"{job} carries a mint step beyond its declared {count} slots"


def test_each_mint_step_reads_its_own_slot_and_defers_its_failure():
    for job in JOBS:
        for index in range(1, slots(job) + 1):
            mint = step(job, MINT.format(index))
            assert mint["id"] == f"foreign-app-token-{index}"
            assert mint["uses"] == "actions/create-github-app-token@v2"
            assert mint["with"]["owner"] == \
                "${{ steps.foreign-owner.outputs.owner_%d }}" % index
            assert mint["with"]["app-id"] == "${{ secrets.XFACTORY_APP_ID }}"
            assert mint["with"]["private-key"] == \
                "${{ secrets.XFACTORY_APP_PRIVATE_KEY }}"
            # The guard is the slot, not a single has_foreign flag.
            assert f"steps.foreign-owner.outputs.owner_{index} != ''" \
                in mint["if"]
            assert "env.HAS_APP_KEY == 'true'" in mint["if"]
            # Not a fallback: the rewrite step turns an unmintable owner into
            # a finding that names it. Losing this makes the failure opaque
            # again; adding a `|| github.token` would make it silent.
            assert mint["continue-on-error"] is True
            assert "github.token" not in yaml.safe_dump(mint["with"])


def test_the_rewrite_step_is_wired_to_every_slot():
    for job in JOBS:
        env = step(job, REWRITE)["env"]
        count = slots(job)
        assert env["SLOTS"] == "${{ steps.foreign-owner.outputs.slots }}", \
            "the slot count must reach the rewrite step from the detection, " \
            "not be typed a second time"
        for index in range(1, count + 1):
            assert env[f"OWNER_{index}"] == \
                "${{ steps.foreign-owner.outputs.owner_%d }}" % index
            assert env[f"TOKEN_{index}"] == \
                "${{ steps.foreign-app-token-%d.outputs.token }}" % index
        assert f"OWNER_{count + 1}" not in env


def test_the_detection_writes_every_slot_filled_or_empty():
    for job in JOBS:
        script = step(job, DETECT)["run"]
        assert 'echo "count=${COUNT}" >> "$GITHUB_OUTPUT"' in script
        assert 'echo "slots=${FOREIGN_OWNER_SLOTS}" >> "$GITHUB_OUTPUT"' \
            in script
        assert 'echo "owner_${slot}=${owner}" >> "$GITHUB_OUTPUT"' in script


def test_the_refusal_is_bounded_by_the_slots_not_by_one():
    for job in JOBS:
        script = step(job, DETECT)["run"]
        assert '[ "$COUNT" -gt "$FOREIGN_OWNER_SLOTS" ]' in script
        assert '[ "$COUNT" -gt 1 ]' not in script, \
            "refusing a SECOND owner is the #366 defect"
        assert "$FOREIGN_OWNER_SLOTS mint slots" in script, \
            "the refusal must name how many slots exist"


# --- both url forms, and the broad rewrite that stays ----------------------

def test_each_owner_is_credentialed_in_both_url_forms():
    for job in JOBS:
        script = step(job, REWRITE)["run"]
        ssh = ('git config --global --add '
               'url."https://x-access-token:${token}@github.com/${owner}/"'
               '.insteadOf "git@github.com:${owner}/"')
        https = ('git config --global --add '
                 'url."https://x-access-token:${token}@github.com/${owner}/"'
                 '.insteadOf "https://github.com/${owner}/"')
        assert ssh in script
        assert https in script, \
            "the https form is what MedxEHR's nested legs declare (#366)"


def test_the_broad_org_rewrite_stays_and_stays_broad():
    # Longest prefix wins, so the per-owner keys narrow this one rather than
    # replace it; removing it strands every same-org submodule.
    for job in JOBS:
        broad = step(job, BROAD)
        assert 'insteadOf "git@github.com:"' in broad["run"]
        assert broad["env"]["TOKEN"] == (
            "${{ steps.app-token.outputs.token || secrets.SUBMODULE_TOKEN "
            "|| github.token }}")


def test_the_missing_installation_is_a_named_finding():
    for job in JOBS:
        script = step(job, REWRITE)["run"]
        assert "::error::no GitHub App installation access token could be " \
            "minted for organization '${owner}'" in script
        assert "OPERATOR act" in script
        assert "rc=1" in script and 'exit "$rc"' in script, \
            "a missing installation must fail the run, not skip the repo"


def test_the_detection_and_the_init_share_one_governed_filter():
    for job in JOBS:
        detect = step(job, DETECT)["run"]
        init = step(job, "Init governed submodules only")["run"]
        assert "GOVERNED='^(openxFactory|xFactories/)'" in detect
        assert "grep -E '^(openxFactory|xFactories/)'" in init


def test_the_two_jobs_carry_the_identical_owner_token_block():
    # They are twins by construction and drift because nothing compares them.
    def block(job):
        names = [DETECT] + \
            [MINT.format(i) for i in range(1, slots(job) + 1)] + [REWRITE]
        return yaml.safe_dump([step(job, name) for name in names],
                              sort_keys=True)
    assert block("prepare") == block("finalize")


# --- behavioral: the two shell steps actually run --------------------------

def gitmodules(tmp_path, entries):
    text = "".join(
        f'[submodule "{path}"]\n\tpath = {path}\n\turl = {url}\n'
        for path, url in entries)
    (tmp_path / ".gitmodules").write_text(text, encoding="utf-8")
    return tmp_path


def run_detect(tmp_path, entries, slot_count=3, self_owner="opensoft"):
    root = gitmodules(tmp_path, entries)
    out = tmp_path / "github_output"
    out.write_text("", encoding="utf-8")
    done = subprocess.run(
        ["bash", "-c", step("prepare", DETECT)["run"]],
        cwd=root, capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin",
             "SELF_OWNER": self_owner,
             "FOREIGN_OWNER_SLOTS": str(slot_count),
             "GITHUB_OUTPUT": str(out)})
    outputs = dict(
        line.split("=", 1)
        for line in out.read_text(encoding="utf-8").splitlines() if line)
    return done, outputs


def test_two_foreign_owners_now_fill_two_slots(tmp_path):
    done, outputs = run_detect(tmp_path, [
        ("openxFactory", "git@github.com:opensoft/openxFactory.git"),
        ("xFactories/MedxFactory", "git@github.com:MedxSoft/MedxFactory.git"),
        ("xFactories/MedxEHR", "git@github.com:MedxSoft/MedxEHR.git"),
        ("xFactories/LedgerxFactory",
         "git@github.com:ledgerXfactory/LedgerxFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "2"
    assert outputs["slots"] == "3"
    assert {outputs["owner_1"], outputs["owner_2"]} == \
        {"MedxSoft", "ledgerXfactory"}
    assert outputs["owner_3"] == ""


def test_one_foreign_owner_still_behaves_as_before(tmp_path):
    done, outputs = run_detect(tmp_path, [
        ("xFactories/MedxFactory", "git@github.com:MedxSoft/MedxFactory.git"),
        ("xFactories/codexFactory", "git@github.com:opensoft/codexFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "1"
    assert outputs["owner_1"] == "MedxSoft"
    assert outputs["owner_2"] == "" and outputs["owner_3"] == ""


def test_no_foreign_owner_leaves_the_broad_rewrite_alone(tmp_path):
    done, outputs = run_detect(tmp_path, [
        ("openxFactory", "git@github.com:opensoft/openxFactory.git"),
        ("xFactories/codexFactory", "git@github.com:opensoft/codexFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "0"
    assert "the org-wide rewrite suffices" in done.stdout


def test_installs_are_not_governed_and_do_not_demand_a_slot(tmp_path):
    done, outputs = run_detect(tmp_path, [
        ("installs/hermes-install",
         "git@github.com:elsewhere/xFactory-Hermes-Install.git"),
        ("xFactories/codexFactory", "git@github.com:opensoft/codexFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "0"


def test_more_owners_than_slots_still_refuses_and_names_them(tmp_path):
    done, _ = run_detect(tmp_path, [
        (f"xFactories/R{n}", f"git@github.com:Org{n}/R{n}.git")
        for n in range(1, 5)
    ])
    assert done.returncode == 1
    assert "span 4 foreign owners" in done.stdout
    for n in range(1, 5):
        assert f"Org{n}" in done.stdout
    assert "3 mint slots" in done.stdout


def run_rewrite(tmp_path, pairs, slot_count=3, broad_token=None):
    config = tmp_path / "gitconfig"
    config.write_text("", encoding="utf-8")
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin",
           "GIT_CONFIG_GLOBAL": str(config),
           "GIT_CONFIG_NOSYSTEM": "1",
           "SLOTS": str(slot_count)}
    for index in range(1, slot_count + 1):
        owner, token = pairs.get(index, ("", ""))
        env[f"OWNER_{index}"] = owner
        env[f"TOKEN_{index}"] = token
    if broad_token is not None:
        subprocess.run(
            ["git", "config", "--global",
             f"url.https://x-access-token:{broad_token}@github.com/.insteadOf",
             "git@github.com:"], cwd=tmp_path, env=env, check=True)
    done = subprocess.run(
        ["bash", "-c", step("prepare", REWRITE)["run"]],
        cwd=tmp_path, capture_output=True, text=True, env=env)

    def resolve(url):
        return subprocess.run(
            ["git", "ls-remote", "--get-url", url],
            cwd=tmp_path, capture_output=True, text=True,
            env=env, check=True).stdout.strip()

    return done, resolve


def test_both_forms_resolve_to_the_owners_own_token(tmp_path):
    done, resolve = run_rewrite(tmp_path, {
        1: ("MedxSoft", "ghs_medx"),
        2: ("ledgerXfactory", "ghs_ledger"),
    })
    assert done.returncode == 0, done.stdout + done.stderr
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        "https://x-access-token:ghs_medx@github.com/MedxSoft/MedxEHR.git"
    # The form that reddened 2026-09-05..07: MedxEHR's nested legs.
    assert resolve("https://github.com/MedxSoft/MedxEHR-spec.git") == \
        "https://x-access-token:ghs_medx@github.com/MedxSoft/MedxEHR-spec.git"
    assert resolve("git@github.com:ledgerXfactory/LedgerxFactory.git") == \
        ("https://x-access-token:ghs_ledger@github.com/"
         "ledgerXfactory/LedgerxFactory.git")


def test_the_broad_rewrite_still_serves_every_other_owner(tmp_path):
    done, resolve = run_rewrite(
        tmp_path, {1: ("MedxSoft", "ghs_medx")}, broad_token="ghs_self")
    assert done.returncode == 0, done.stdout + done.stderr
    # Longest prefix wins in BOTH directions: the narrow key takes MedxSoft,
    # the broad one keeps everything else.
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        "https://x-access-token:ghs_medx@github.com/MedxSoft/MedxEHR.git"
    assert resolve("git@github.com:opensoft/codexFactory.git") == \
        "https://x-access-token:ghs_self@github.com/opensoft/codexFactory.git"


def test_an_unmintable_owner_fails_the_run_naming_the_owner(tmp_path):
    done, resolve = run_rewrite(tmp_path, {
        1: ("MedxSoft", "ghs_medx"),
        2: ("ledgerXfactory", ""),
    })
    assert done.returncode == 1
    assert "::error::" in done.stdout
    assert "'ledgerXfactory'" in done.stdout
    assert "OPERATOR act" in done.stdout
    # The owner that COULD be served still was, so the failure names one
    # organization rather than hiding behind the first one to break.
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        "https://x-access-token:ghs_medx@github.com/MedxSoft/MedxEHR.git"
    assert resolve("git@github.com:ledgerXfactory/LedgerxFactory.git") == \
        "git@github.com:ledgerXfactory/LedgerxFactory.git"
