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

A THIRD OWNER ARRIVED WITH THE ORG MOVE, and this file is where that is
measured (slice B1b of `adopt-codexfactory-repository-identity`;
codeXfactory/codexFactory#279, the 6.5 precheck ruling of 2026-09-09T15:25Z).
`xFactories/codexFactory` left `opensoft` for its own enterprise organization
`codeXfactory`, so the repository these fixtures used as the SAME-ORG,
not-foreign, needs-no-slot control is now the very thing that DEMANDS a slot.
Respelling the string alone would have made three tests assert something now
false, which is why the ruling classes it a rename that is not a `sed`:

  * the same-org controls moved to submodules that genuinely stayed in
    `opensoft` — `xFactories/OpsxFactory` and `openxFactory` itself.
    `xFactories/MedxFactory` cannot serve: it lives in `MedxSoft`;
  * `codeXfactory` is asserted as a foreign owner that fills a slot and is
    credentialed from its OWN installation (App `4253636` `openxfactory`, the
    App behind `XFACTORY_APP_ID`, installation `160352673` on `codeXfactory`),
    NOT from the caller-org token the broad rewrite hands every same-org
    submodule;
  * and the slot count is measured, never assumed: the behavioral cases read
    `FOREIGN_OWNER_SLOTS` out of the workflow rather than typing a literal, so
    the day the aggregation declares a fourth owner these tests move with the
    file instead of passing against a number nobody re-derived.

The structural assertions read the workflow; the behavioral ones RUN the two
shell steps against synthetic `.gitmodules` trees and read the git config they
produce back through `git ls-remote --get-url`, because prefix resolution
("longest match wins", which is what lets the broad org rewrite stay) is a
property of git and not of this file."""

from __future__ import annotations

import os
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


def declared_slots():
    """The slot count the workflow itself carries, for the behavioral cases.

    Read rather than typed (slice B1b): a literal `3` in a fixture is a second
    place the count lives, and the whole point of `FOREIGN_OWNER_SLOTS` is that
    there is exactly one. `test_both_jobs_declare_the_same_slot_count` proves
    the two jobs agree, so either job answers for both.
    """
    return slots("prepare")


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

def clean_env(**overrides):
    """The ambient environment, minus anything that would let the host's git
    identity or config leak into a step under test.

    Inherited rather than replaced: `tests/hermeticity.py` works by PATH, so
    a hardcoded PATH here would step around it, and a hardcoded one is also
    how a suite that passes on a runner fails on a developer's machine."""
    env = dict(os.environ)
    # The per-slot names are DERIVED from the declared count, not listed: a
    # hand-written list silently stops covering the newest slot the moment the
    # count rises, which is how an inherited `OWNER_4` would have leaked into a
    # case that meant to leave slot 4 empty. One past the count, so a stray
    # variable for a slot the workflow does not carry is cleared too.
    per_slot = [f"{name}_{index}"
                for index in range(1, declared_slots() + 2)
                for name in ("OWNER", "TOKEN")]
    for leak in ["GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_COUNT",
                 "SELF_OWNER", "FOREIGN_OWNER_SLOTS", "GITHUB_OUTPUT",
                 "SLOTS"] + per_slot:
        env.pop(leak, None)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env.update(overrides)
    return env


def gitmodules(tmp_path, entries):
    text = "".join(
        f'[submodule "{path}"]\n\tpath = {path}\n\turl = {url}\n'
        for path, url in entries)
    (tmp_path / ".gitmodules").write_text(text, encoding="utf-8")
    return tmp_path


def run_detect(tmp_path, entries, slot_count=None, self_owner="opensoft"):
    if slot_count is None:
        slot_count = declared_slots()
    root = gitmodules(tmp_path, entries)
    out = tmp_path / "github_output"
    out.write_text("", encoding="utf-8")
    done = subprocess.run(
        ["bash", "-c", step("prepare", DETECT)["run"]],
        cwd=root, capture_output=True, text=True,
        env=clean_env(SELF_OWNER=self_owner,
                      FOREIGN_OWNER_SLOTS=str(slot_count),
                      GITHUB_OUTPUT=str(out)))
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
    assert outputs["slots"] == str(declared_slots())
    # A SET, not positions: the owners come out of `sort -u`, whose ordering of
    # `MedxSoft` against `ledgerXfactory` is a property of the runner's locale
    # rather than of this workflow.
    assert {outputs["owner_1"], outputs["owner_2"]} == \
        {"MedxSoft", "ledgerXfactory"}
    for index in range(3, declared_slots() + 1):
        assert outputs[f"owner_{index}"] == "", \
            f"slot {index} should be spare with two owners declared"


def test_one_foreign_owner_still_behaves_as_before(tmp_path):
    # THE SAME-ORG CONTROL IS `OpsxFactory`, NOT A Medx MEMBER AND NO LONGER
    # `codexFactory` (slice B1b). `xFactories/MedxFactory` lives in `MedxSoft`
    # and `xFactories/codexFactory` now lives in `codeXfactory`; either one
    # here would make this a TWO-owner tree and the test would assert the
    # opposite of its own name. `OpsxFactory` is a governed `xFactories/`
    # member that stayed in `opensoft`.
    done, outputs = run_detect(tmp_path, [
        ("xFactories/MedxFactory", "git@github.com:MedxSoft/MedxFactory.git"),
        ("xFactories/OpsxFactory", "git@github.com:opensoft/OpsxFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "1"
    assert outputs["owner_1"] == "MedxSoft"
    for index in range(2, declared_slots() + 1):
        assert outputs[f"owner_{index}"] == ""


def test_no_foreign_owner_leaves_the_broad_rewrite_alone(tmp_path):
    # Both rows are genuinely `opensoft` AFTER the org move (slice B1b): the
    # reusable workflow's own repository and a governed `xFactories/` member
    # that stayed. `codexFactory` used to be the second row and can no longer
    # stand for "no foreign owner" at all.
    done, outputs = run_detect(tmp_path, [
        ("openxFactory", "git@github.com:opensoft/openxFactory.git"),
        ("xFactories/OpsxFactory", "git@github.com:opensoft/OpsxFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "0"
    assert "the org-wide rewrite suffices" in done.stdout


def test_installs_are_not_governed_and_do_not_demand_a_slot(tmp_path):
    # The pair is deliberate (slice B1b): an `installs/` submodule in a foreign
    # organization NEXT TO a governed one in a foreign organization. Only the
    # governed one may reach a slot, so the filter is proved by the DIFFERENCE
    # between the two rows rather than by a tree in which nothing is foreign —
    # which is what the old same-org `codexFactory` row made it.
    done, outputs = run_detect(tmp_path, [
        ("installs/hermes-install",
         "git@github.com:elsewhere/xFactory-Hermes-Install.git"),
        ("xFactories/codexFactory",
         "git@github.com:codeXfactory/codexFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "1"
    assert outputs["owner_1"] == "codeXfactory"
    # `elsewhere` reaches neither a slot nor the fallback step's owner list.
    assert "elsewhere" not in outputs["owners_all"]
    assert outputs["owners_all"].split() == ["codeXfactory"]


def test_the_moved_core_becomes_a_foreign_owner_and_gets_a_slot(tmp_path):
    """The invariant slice B1b exists for (codeXfactory/codexFactory#279).

    The tree is the aggregation's own governed shape AS OF
    opensoft/xFactory#376 — the commit that flips `xFactories/codexFactory`
    from `opensoft` to `codeXfactory` and lands AFTER this pull request. Three
    foreign owners then, and the third has to be SERVED rather than refused.

    Nothing in the workflow names `codeXfactory`, which is why the readiness
    can be proved before the flip: the owner comes out of `.gitmodules` and
    `actions/create-github-app-token@v2` resolves the installation from its own
    `owner:` input (App `4253636` `openxfactory`, installation `160352673` on
    `codeXfactory`, created 2026-09-09). So what is asserted here is that the
    DETECTION admits the owner, that the file carries a mint step for whatever
    slot it lands in, and that a spare slot survives — the reason the count
    moved 3 -> 4 in the same commit, since three owners in three slots would
    leave the NEXT repoint to red the nightly in the refusal below (#366
    again, one organization later).

    THE PRE-FLIP SHAPE IS NOT REPEATED HERE, and deliberately: today's
    aggregation `.gitmodules` is exactly the tree
    `test_two_foreign_owners_now_fill_two_slots` already runs — `MedxSoft`
    twice, `ledgerXfactory` once — so that test is the proof that this change
    is a no-op until #376 lands, and this one carries no pre-move URL
    literal for the identity sweep to have to disposition.
    """
    done, outputs = run_detect(tmp_path, [
        ("openxFactory", "git@github.com:opensoft/openxFactory.git"),
        ("xFactories/OpsxFactory", "git@github.com:opensoft/OpsxFactory.git"),
        ("xFactories/MedxFactory", "git@github.com:MedxSoft/MedxFactory.git"),
        ("xFactories/MedxEHR", "git@github.com:MedxSoft/MedxEHR.git"),
        ("xFactories/LedgerxFactory",
         "git@github.com:ledgerXfactory/LedgerxFactory.git"),
        ("xFactories/codexFactory",
         "git@github.com:codeXfactory/codexFactory.git"),
    ])
    assert done.returncode == 0, done.stdout + done.stderr
    assert outputs["count"] == "3", \
        "the moved core must be DETECTED as a third foreign owner"
    filled = {index: outputs[f"owner_{index}"]
              for index in range(1, declared_slots() + 1)
              if outputs[f"owner_{index}"]}
    assert set(filled.values()) == \
        {"MedxSoft", "ledgerXfactory", "codeXfactory"}
    assert "codeXfactory" in outputs["owners_all"].split()

    # The slot it lands in has a mint step, in BOTH jobs — the position comes
    # out of `sort -u` and is locale-dependent, so it is looked up rather than
    # assumed.
    core_slot = next(index for index, owner in filled.items()
                     if owner == "codeXfactory")
    for job in JOBS:
        mint = step(job, MINT.format(core_slot))
        assert mint["with"]["app-id"] == "${{ secrets.XFACTORY_APP_ID }}", \
            "the moved core is minted from the same App as every other owner"

    # And a spare remains, so the NEXT repoint is a `.gitmodules` edit.
    assert declared_slots() > 3
    assert outputs[f"owner_{declared_slots()}"] == ""


def test_more_owners_than_slots_still_refuses_and_names_them(tmp_path):
    # ONE MORE OWNER THAN THE FILE DECLARES, derived from the declared count
    # rather than typed: with a literal 4 this stopped being an
    # over-the-limit tree the moment the fourth slot landed.
    over = declared_slots() + 1
    done, _ = run_detect(tmp_path, [
        (f"xFactories/R{n}", f"git@github.com:Org{n}/R{n}.git")
        for n in range(1, over + 1)
    ])
    assert done.returncode == 1
    assert f"span {over} foreign owners" in done.stdout
    for n in range(1, over + 1):
        assert f"Org{n}" in done.stdout
    assert f"{declared_slots()} mint slots" in done.stdout


def credentialed(token, owner, repo):
    """The URL git must resolve to when `owner`'s submodule is credentialed.

    Built here rather than typed at each call site (Copilot, PR #831): three
    duplicated full-URL literals are three places for the expectation to drift
    from the rewrite, and a reader should not have to reassemble a credential
    shape by eye to see which token an owner routes to. Strict equality on the
    WHOLE string stays — that is the "longest prefix wins" claim, and a
    substring check would pass for the right owner routed to the wrong token,
    which is the failure this file exists to catch.
    """
    return f"https://x-access-token:{token}@github.com/{owner}/{repo}.git"


# THE PLACEHOLDER TOKENS ARE DELIBERATELY NOT TOKEN-SHAPED. A `ghs_`-prefixed
# literal reads as a real installation token to a secret scanner and to a
# reader, and both of those cost more than the realism buys (Copilot, PR #831).
# The full rewritten URL IS still asserted verbatim, because "longest prefix
# wins" is precisely a claim about the WHOLE resolved string — a substring
# check would pass for a rewrite that routed the right owner to the wrong
# token, which is the failure this file exists to catch.
def run_rewrite(tmp_path, pairs, slot_count=None, broad_token=None):
    if slot_count is None:
        slot_count = declared_slots()
    config = tmp_path / "gitconfig"
    config.write_text("", encoding="utf-8")
    env = clean_env(GIT_CONFIG_GLOBAL=str(config), SLOTS=str(slot_count))
    # A malformed slot count is a case under test, so the env is still built
    # with as many pairs as the caller passed pairs for.
    declared = slot_count if isinstance(slot_count, int) else max(pairs, default=0)
    for index in range(1, declared + 1):
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
        1: ("MedxSoft", "medx-installation-token"),
        2: ("ledgerXfactory", "ledger-installation-token"),
    })
    assert done.returncode == 0, done.stdout + done.stderr
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        credentialed("medx-installation-token", "MedxSoft", "MedxEHR")
    # The form that reddened 2026-09-05..07: MedxEHR's nested legs.
    assert resolve("https://github.com/MedxSoft/MedxEHR-spec.git") == \
        credentialed("medx-installation-token", "MedxSoft", "MedxEHR-spec")
    assert resolve("git@github.com:ledgerXfactory/LedgerxFactory.git") == \
        credentialed("ledger-installation-token", "ledgerXfactory",
                     "LedgerxFactory")


def test_the_broad_rewrite_still_serves_every_other_owner(tmp_path):
    done, resolve = run_rewrite(tmp_path, {
        1: ("MedxSoft", "medx-installation-token"),
        2: ("codeXfactory", "codexfactory-installation-token"),
    }, broad_token="caller-org-token")
    assert done.returncode == 0, done.stdout + done.stderr
    # Longest prefix wins in BOTH directions: the narrow keys take their own
    # owners, the broad one keeps everything else.
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        credentialed("medx-installation-token", "MedxSoft", "MedxEHR")
    # THE MOVED CORE ROUTES TO ITS OWN INSTALLATION (slice B1b). Before the org
    # move this line read `credentialed("caller-org-token", "opensoft",
    # "codexFactory")` — the broad key served it because it was same-org. It is
    # foreign now, and a broad-key resolution here would mean the nightly
    # cloning it with a token minted for `opensoft`, which is the 422 the
    # transfer's own precheck measured.
    assert resolve("git@github.com:codeXfactory/codexFactory.git") == \
        credentialed("codexfactory-installation-token", "codeXfactory",
                     "codexFactory")
    # A submodule that STAYED in `opensoft` is what proves the broad key is
    # still doing its job.
    assert resolve("git@github.com:opensoft/OpsxFactory.git") == \
        credentialed("caller-org-token", "opensoft", "OpsxFactory")


def test_an_unmintable_owner_fails_the_run_naming_the_owner(tmp_path):
    done, resolve = run_rewrite(tmp_path, {
        1: ("MedxSoft", "medx-installation-token"),
        2: ("ledgerXfactory", ""),
    })
    assert done.returncode == 1
    assert "::error::" in done.stdout
    assert "'ledgerXfactory'" in done.stdout
    assert "OPERATOR act" in done.stdout
    # The owner that COULD be served still was, so the failure names one
    # organization rather than hiding behind the first one to break.
    assert resolve("git@github.com:MedxSoft/MedxEHR.git") == \
        credentialed("medx-installation-token", "MedxSoft", "MedxEHR")
    assert resolve("git@github.com:ledgerXfactory/LedgerxFactory.git") == \
        "git@github.com:ledgerXfactory/LedgerxFactory.git"


def test_a_slot_count_that_did_not_arrive_is_its_own_refusal(tmp_path):
    # `[ n -lt "" ]` would abort and `[ n -lt 0 ]` would loop zero times; both
    # end with this step reporting success having credentialed nothing, which
    # is a silent pass on exactly the path #366 is about.
    for bad in ("", "0", "three"):
        done, _ = run_rewrite(
            tmp_path, {1: ("MedxSoft", "medx-installation-token")}, slot_count=bad)
        assert done.returncode == 1, f"SLOTS={bad!r} did not refuse"
        assert "no usable slot count" in done.stdout


def test_the_slot_guard_is_in_both_jobs():
    for job in JOBS:
        script = step(job, REWRITE)["run"]
        assert "grep -qE '^[1-9][0-9]*$'" in script


# --- the documented PAT fallback (Codex, PR #831) ---------------------------

FALLBACK = "Rewrite governed submodule https URLs for the fallback token"


def test_the_fallback_step_runs_exactly_when_there_is_no_app_key():
    for job in JOBS:
        fallback = step(job, FALLBACK)
        assert fallback["if"] == "env.HAS_APP_KEY != 'true'"
        # The App path and the fallback path are mutually exclusive, and the
        # per-owner mints are the App path.
        assert step(job, REWRITE)["if"].startswith("env.HAS_APP_KEY == 'true'")
        assert fallback["env"]["TOKEN"] == \
            "${{ secrets.SUBMODULE_TOKEN || github.token }}"
        assert fallback["env"]["OWNERS"] == \
            "${{ steps.foreign-owner.outputs.owners_all }}"


def test_the_fallback_rewrite_is_scoped_to_declared_owners():
    # A broad `https://github.com/` key would also capture the checked-out
    # repository's own origin URL, which the delivery lanes push through.
    for job in JOBS:
        script = step(job, FALLBACK)["run"]
        assert 'insteadOf "https://github.com/${owner}/"' in script
        assert 'insteadOf "https://github.com/"' not in script


def test_the_detection_reports_every_governed_owner_for_the_fallback():
    for job in JOBS:
        script = step(job, DETECT)["run"]
        assert 'echo "owners_all=' in script


def test_owners_all_carries_self_and_foreign_owners(tmp_path):
    _, outputs = run_detect(tmp_path, [
        ("openxFactory", "git@github.com:opensoft/openxFactory.git"),
        ("xFactories/MedxEHR", "git@github.com:MedxSoft/MedxEHR.git"),
        ("xFactories/LedgerxFactory",
         "git@github.com:ledgerXfactory/LedgerxFactory.git"),
        # Not governed: it must not reach the fallback rewrite either.
        ("installs/hermes-install",
         "git@github.com:elsewhere/xFactory-Hermes-Install.git"),
    ])
    assert set(outputs["owners_all"].split()) == \
        {"opensoft", "MedxSoft", "ledgerXfactory"}


def run_fallback(tmp_path, owners, token):
    config = tmp_path / "gitconfig"
    config.write_text("", encoding="utf-8")
    env = clean_env(GIT_CONFIG_GLOBAL=str(config), TOKEN=token,
                    OWNERS=" ".join(owners))
    done = subprocess.run(
        ["bash", "-c", step("prepare", FALLBACK)["run"]],
        cwd=tmp_path, capture_output=True, text=True, env=env)

    def resolve(url):
        return subprocess.run(
            ["git", "ls-remote", "--get-url", url],
            cwd=tmp_path, capture_output=True, text=True,
            env=env, check=True).stdout.strip()

    return done, resolve


def test_the_fallback_token_reaches_a_private_https_leg(tmp_path):
    # The exact URL `Init governed submodules only` failed on, 2026-09-05..07.
    done, resolve = run_fallback(
        tmp_path, ["opensoft", "MedxSoft"], "fallback-pat")
    assert done.returncode == 0, done.stdout + done.stderr
    assert resolve("https://github.com/MedxSoft/MedxEHR-spec.git") == \
        credentialed("fallback-pat", "MedxSoft", "MedxEHR-spec")
    assert resolve("https://github.com/opensoft/openXwallet.git") == \
        credentialed("fallback-pat", "opensoft", "openXwallet")


def test_the_fallback_never_captures_the_repositorys_own_origin(tmp_path):
    done, resolve = run_fallback(tmp_path, ["MedxSoft"], "fallback-pat")
    assert done.returncode == 0, done.stdout + done.stderr
    # An owner nobody declared is left exactly as it was.
    assert resolve("https://github.com/opensoft/xFactory") == \
        "https://github.com/opensoft/xFactory"


def test_an_empty_owner_list_is_a_no_op_not_a_failure(tmp_path):
    done, _ = run_fallback(tmp_path, [], "fallback-pat")
    assert done.returncode == 0, done.stdout + done.stderr
