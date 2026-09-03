"""`scripts/mint-factory-origin-key.py`: every refusal, and the whole mint.

WHAT IS PROVEN HERE, AND WHY EACH PIECE IS SEPARATE.

THE REAL `gh` IS NEVER REACHED, TWICE OVER. `tests/hermeticity.py` puts a
refusing `gh` first on `PATH` for the whole session, and every test in this
module injects a `FakeRunner` at the program's single process seam. That is
not belt-and-braces for its own sake: the one call this program makes that
CANNOT be undone is `gh secret set FACTORY_ORIGIN_SIGNING_KEY`, and a test that
reached it would provision a throwaway seed into the real originating
repository's real environment and permanently block the operator's mint at the
`secret-already-exists` refusal.

THE PREFLIGHT REFUSALS EACH GET THEIR OWN TREE. A fail-closed program is only
as good as the condition it actually notices, and a refusal proven only against
the shipped artifact stops being proven the moment the artifact changes.

THE SEED IS PROVEN UNOBSERVABLE, not asserted to be. The end-to-end test
inspects every argv the program passed to a child process and every line it
printed, and requires the 64-hex seed to appear in none of them — while
separately confirming it DID reach `gh secret set`'s stdin, because a custody
rule that also failed to store the key would pass an absence check trivially.

THE DERIVE PATH IS PROVEN TO BE THE VALIDATOR'S. `test_the_derive_path_is_the_
validators_own` runs `validate-factory-identity.py --derive` as a SUBPROCESS —
the runbook's own invocation — and requires the three values the mint program
computed in-process to be character-for-character identical. A second
implementation of base58btc or of the fingerprint spelling is the defect the
whole register family exists to prevent.
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MINT_SCRIPT = REPO_ROOT / "scripts" / "mint-factory-origin-key.py"
VALIDATOR = REPO_ROOT / "scripts" / "validate-factory-identity.py"
PINNED_READER = REPO_ROOT / "openXwallet" / "scripts" / "validate-openxwallet.py"

FAMILY_REL = "governance/factory-identity"
REVIEW_REL = "governance/review-authority"

SEED_HEX_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")

pytestmark = pytest.mark.skipif(
    not PINNED_READER.is_file(),
    reason="the pinned openXwallet reader is not initialized "
           "(`git submodule update --init openXwallet`); the mint program "
           "REFUSES rather than deriving keys with arithmetic of its own")


# --------------------------------------------------------------- the module

def load(name: str, path: Path):
    """Import a hyphenated script as a module, REGISTERED IN `sys.modules`.

    The registration is not optional and the failure without it is obscure:
    both this suite and the program itself carry `from __future__ import
    annotations`, so a `@dataclass`'s field types are strings, and
    `dataclasses` resolves them through `sys.modules[cls.__module__].__dict__`.
    A module executed but never registered leaves that lookup returning `None`
    and every dataclass in the file raises `AttributeError` at class-creation
    time. Measured here on the first run.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def mint():
    """The mint program, imported as a module.

    Its filename carries hyphens, so `import` cannot reach it; the same
    `importlib` route the program itself uses to reach the register reader is
    used here to reach the program.
    """
    return load("_mint_program", MINT_SCRIPT)


# --------------------------------------------------------------- the doubles

class FakeRunner:
    """The program's process seam, doubled. NOTHING here starts a process.

    Every answer is a knob, so a refusal test says exactly which condition it
    is asserting: `auth_ok=False` is the unauthenticated run, `secrets=(NAME,)`
    is the already-minted store, `verify_rc=1` is the gate that refuses the
    fill.

    `secret_stdin` is the one place a test sees the private half, and it is
    deliberate: proving the seed never reached argv or stdout is worth nothing
    unless the same test proves it DID reach the store.
    """

    def __init__(self, *, auth_ok: bool = True, env_ok: bool = True,
                 secrets: tuple[str, ...] = (), secret_set_rc: int = 0,
                 branches: dict[str, str] | None = None,
                 dirty: dict[str, str] | None = None,
                 pr_numbers: dict[str, str] = None,
                 verify_rc: int = 0, disjointness: str = "0 shared") -> None:
        self.auth_ok = auth_ok
        self.env_ok = env_ok
        self.secrets = secrets
        self.secret_set_rc = secret_set_rc
        self.branches = branches or {}
        self.dirty = dirty or {}
        self.pr_numbers = pr_numbers or {}
        self.verify_rc = verify_rc
        self.disjointness = disjointness
        self.log: list[tuple[tuple[str, ...], str | None, int | None]] = []
        self.secret_stdin: bytes | None = None

    # -- the seam ----------------------------------------------------------
    def run(self, argv, *, cwd=None, stdin=None):
        args = tuple(str(a) for a in argv)
        self.log.append((args, str(cwd) if cwd is not None else None,
                         None if stdin is None else len(stdin)))
        if args[0] == "gh":
            return self._gh(args, stdin)
        if args[0] == "git":
            return self._git(args)
        return self._python(args)

    def argvs(self) -> list[tuple[str, ...]]:
        return [entry[0] for entry in self.log]

    def spoke(self, *needle: str) -> bool:
        """Did any invocation carry these words, in order?

        A SUBSEQUENCE match, not a prefix one, and the difference is load
        bearing: every git call this program makes is
        `git -C <root> <verb> …`, so a prefix test for `("git", "commit")`
        matches nothing and every NEGATIVE assertion built on it would pass
        vacuously — which is exactly what the first run of this suite did until
        `test_the_whole_mint`'s positive `spoke("git", "push")` caught it.
        """
        for args in self.argvs():
            remaining = list(needle)
            for word in args:
                if remaining and word == remaining[0]:
                    remaining.pop(0)
            if not remaining:
                return True
        return False

    # -- the answers -------------------------------------------------------
    def _gh(self, args, stdin):
        if args[1:3] == ("auth", "status"):
            return (0, "logged in") if self.auth_ok else (1, "not logged in")
        if args[1] == "api" and "/environments/" in args[2]:
            return (0, args[2].rsplit("/", 1)[-1]) if self.env_ok \
                else (1, "HTTP 404: Not Found")
        if args[1] == "api":
            return 0, "true\ttrue\ttrue"
        if args[1:3] == ("secret", "list"):
            return 0, "".join(f"{name}\t2026-08-28T07:43:12Z\n"
                              for name in self.secrets)
        if args[1:3] == ("secret", "set"):
            self.secret_stdin = stdin
            return (self.secret_set_rc,
                    "" if self.secret_set_rc == 0 else "HTTP 403")
        if args[1:3] == ("pr", "list"):
            repo = args[args.index("--repo") + 1]
            return 0, self.pr_numbers.get(repo, "1\n")
        if args[1:3] == ("pr", "ready"):
            return 0, ""
        raise AssertionError(f"the mint program spoke an unmodelled gh: {args}")

    def _git(self, args):
        root = args[2]
        rest = args[3:]
        if rest[:2] == ("rev-parse", "--abbrev-ref"):
            return 0, self.branches.get(root, "detached") + "\n"
        if rest[0] == "rev-parse":
            return 0, "0" * 40 + "\n"
        if rest[:2] == ("status", "--porcelain"):
            return 0, self.dirty.get(root, "")
        if rest[0] in ("commit", "add", "push"):
            return 0, ""
        raise AssertionError(f"the mint program spoke an unmodelled git: {args}")

    def _python(self, args):
        if "validate-factory-identity.py" in " ".join(args):
            return (self.verify_rc,
                    f"note  factory-identity: disjointness holds "
                    f"({self.disjointness})\n\n"
                    f"validate-factory-identity: 0 error(s)\n")
        return self.verify_rc, "ok\n"


# --------------------------------------------------------------- the fixtures

def build_openx(tmp_path: Path) -> Path:
    """An openxFactory-shaped tree carrying the REAL family, reader and pin.

    The shipped register family is COPIED rather than synthesized, so the
    sentinel accounting, the expiry pair and the wallet/grant/row joins these
    tests exercise are the ones the operator's mint will actually meet. The
    `openXwallet` gitlink is symlinked: the reader must import the PINNED
    decoders or refuse, and a copy of them would be a second pin.
    """
    root = tmp_path / "openxFactory"
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(VALIDATOR, root / "scripts" / VALIDATOR.name)
    shutil.copytree(REPO_ROOT / FAMILY_REL, root / FAMILY_REL)
    (root / REVIEW_REL).mkdir(parents=True)
    (root / REVIEW_REL / "register.yaml").write_text(
        yaml.safe_dump({"register_version": 1,
                        "revocation_staleness_bound": "P7D", "rows": []}),
        encoding="utf-8")
    (root / "openXwallet").symlink_to(REPO_ROOT / "openXwallet",
                                      target_is_directory=True)
    return root


def build_codex(tmp_path: Path) -> Path:
    root = tmp_path / "codexFactory"
    root.mkdir(parents=True)
    return root


def runner_for(mint, openx: Path, codex: Path, **kwargs) -> FakeRunner:
    kwargs.setdefault("branches", {str(openx): mint.REGISTER_BRANCH,
                                   str(codex): mint.FLOOR_BRANCH})
    kwargs.setdefault("pr_numbers", {mint.REGISTER_REPO: "610\n",
                                     mint.TARGET_REPO: "182\n"})
    return FakeRunner(**kwargs)


def invoke(mint, openx: Path, codex: Path, runner, *extra: str) -> int:
    return mint.main(["--openxfactory-root", str(openx),
                      "--codex-worktree", str(codex),
                      "--today", "2026-09-03", *extra], runner=runner)


@pytest.fixture
def tree(tmp_path: Path):
    return build_openx(tmp_path), build_codex(tmp_path)


# --------------------------------------------------------------- --help

def test_help_documents_the_whole_ceremony() -> None:
    """`--help` is the runbook's step list now, so it has to carry it."""
    proc = subprocess.run([sys.executable, str(MINT_SCRIPT), "--help"],
                          capture_output=True, text=True)
    assert proc.returncode == 0
    text = proc.stdout
    for phrase in (
            "--dry-run",
            "PREFLIGHT",
            "gh-auth",
            "openxwallet-gitlink",
            "mint-sentinels",
            "secret-absent",
            "CUSTODY",
            "--body -",
            "never a temp file",
            "character-for-character",
            "VERIFY",
            "0 shared",
            "MODIFIED AND UNCOMMITTED",
            "does NOT merge",
            "IDEMPOTENCE",
            "secret-already-exists",
            "register-already-minted"):
        assert phrase in text, f"--help does not document {phrase!r}"


def test_the_secret_is_never_named_inside_the_register_family(mint) -> None:
    """The ratified requirement forbids a resolvable secret name in that family.

    The mint program has to know the name, so it names it — and it lives in
    `scripts/`, which is not the family. This test is the guard that it stays
    there: `validate-factory-identity.py` checks the family over RAW BYTES, and
    a future edit that moved this constant into a governance file would refuse
    the whole tree.
    """
    assert mint.SECRET_NAME == "FACTORY_ORIGIN_SIGNING_KEY"
    for path in sorted((REPO_ROOT / FAMILY_REL).rglob("*")):
        if path.is_file():
            assert mint.SECRET_NAME not in path.read_text(
                encoding="utf-8", errors="replace"), (
                f"{path} names the secret; the ratified requirement forbids "
                f"'a secret name resolvable to key material' in this family")


# --------------------------------------------------------------- preflight

def test_an_unauthenticated_run_refuses_before_anything_is_spent(
        mint, tree, capsys) -> None:
    openx, codex = tree
    runner = runner_for(mint, openx, codex, auth_ok=False)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    assert "refused [gh-unauthenticated]" in capsys.readouterr().err
    assert not runner.spoke("gh", "secret", "set")


def test_a_missing_environment_refuses(mint, tree, capsys) -> None:
    openx, codex = tree
    runner = runner_for(mint, openx, codex, env_ok=False)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    assert "refused [environment-absent]" in capsys.readouterr().err


def test_an_absent_openxwallet_gitlink_refuses_before_minting(
        mint, tree, capsys) -> None:
    """The reader exits 2 without the pin, so a mint performed now would emit
    values no gate could judge. Refuse BEFORE the seed exists."""
    openx, codex = tree
    (openx / "openXwallet").unlink()
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    err = capsys.readouterr().err
    assert "refused [openxwallet-gitlink-absent]" in err
    assert "git submodule update --init openXwallet" in err
    assert not runner.spoke("gh", "secret", "set")


def test_a_worktree_on_the_wrong_branch_refuses(mint, tree, capsys) -> None:
    openx, codex = tree
    runner = runner_for(mint, openx, codex,
                        branches={str(openx): "main",
                                  str(codex): mint.FLOOR_BRANCH})
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    assert "refused [worktree-wrong-branch]" in capsys.readouterr().err


def test_a_dirty_worktree_refuses(mint, tree, capsys) -> None:
    openx, codex = tree
    runner = runner_for(mint, openx, codex,
                        dirty={str(codex): " M some/other/file.md\n"})
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    err = capsys.readouterr().err
    assert "refused [worktree-dirty]" in err
    assert "some/other/file.md" in err


def test_a_filled_register_refuses_a_second_mint(mint, tree, capsys) -> None:
    """ONE ORIGIN IDENTITY PER REPOSITORY. This is half of the idempotence
    story: a run against an already-minted tree stops here and names why."""
    openx, codex = tree
    wallet = openx / mint.WALLET_REL
    wallet.write_text(wallet.read_text(encoding="utf-8").replace(
        "did: FILL-IN-AT-MINT", 'did: "did:key:zAlreadyMinted"'),
        encoding="utf-8")
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    err = capsys.readouterr().err
    assert "refused [register-already-minted]" in err
    assert "supersedes" in err
    assert not runner.spoke("gh", "secret", "set")


def test_an_existing_secret_refuses_a_second_mint(mint, tree, capsys) -> None:
    """The other half of idempotence, and the one that matters most: a present
    secret means a private half is already held."""
    openx, codex = tree
    runner = runner_for(mint, openx, codex, secrets=(mint.SECRET_NAME,))
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    err = capsys.readouterr().err
    assert "refused [secret-already-exists]" in err
    assert not runner.spoke("gh", "secret", "set")


def test_the_other_seat_secrets_do_not_look_like_this_one(mint, tree) -> None:
    """`COUNCIL_SEAT_SIGNING_KEY_*` sit in the SAME environment. A substring
    match on the list would refuse a first mint forever."""
    openx, codex = tree
    runner = runner_for(mint, openx, codex, secrets=(
        "COUNCIL_SEAT_SIGNING_KEY_LEAD_QUALITY",
        "COUNCIL_SEAT_SIGNING_KEY_LEAD_SECURITY"))
    assert invoke(mint, openx, codex, runner, "--dry-run") == 0


def test_an_existing_mint_record_refuses(mint, tree, capsys) -> None:
    openx, codex = tree
    record = codex / mint.RECORD_DIR_REL / mint.RECORD_BASENAME.format(
        date="2026-09-03")
    record.parent.mkdir(parents=True)
    record.write_text("# already recorded\n", encoding="utf-8")
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    assert "refused [record-already-exists]" in capsys.readouterr().err


def test_expiries_that_already_disagree_refuse(mint, tree, capsys) -> None:
    """Two expiries for one authority is one of them being wrong, and it is not
    the mint's job to pick which."""
    openx, codex = tree
    register = openx / mint.REGISTER_REL
    register.write_text(register.read_text(encoding="utf-8").replace(
        'expires_at: "2026-12-01T00:00:00Z"',
        'expires_at: "2027-01-01T00:00:00Z"'), encoding="utf-8")
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 1
    assert "refused [expiry-already-disagrees]" in capsys.readouterr().err


def test_a_missing_codex_worktree_argument_is_a_usage_refusal(mint, capsys) -> None:
    assert mint.main(["--dry-run"], runner=FakeRunner()) == 2
    assert "refused [codex-worktree-unset]" in capsys.readouterr().err


# --------------------------------------------------------------- --dry-run

def test_the_dry_run_spends_nothing_and_prints_the_plan(
        mint, tree, capsys) -> None:
    openx, codex = tree
    before = {path: path.read_bytes()
              for path in sorted((openx / FAMILY_REL).rglob("*"))
              if path.is_file()}
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 0
    out = capsys.readouterr().out

    assert "DRY RUN" in out
    for name in ("gh-auth", "environment", "openxwallet-gitlink",
                 "openxFactory-clean", "codexFactory-clean", "mint-sentinels",
                 "secret-absent", "mint-record-absent", "expiry"):
        assert f"ok [{name}]" in out, f"the plan does not report {name!r}"
    assert "would generate" in out
    assert "would store" in out
    assert "would verify" in out
    assert "will NOT merge" in out

    for command in (("gh", "secret", "set"), ("git", "commit"),
                    ("git", "push"), ("gh", "pr", "ready")):
        assert not runner.spoke(*command), (
            f"the dry run spoke {' '.join(command)}")
    after = {path: path.read_bytes()
             for path in sorted((openx / FAMILY_REL).rglob("*"))
             if path.is_file()}
    assert after == before, "the dry run modified the register family"
    assert not (codex / mint.RECORD_DIR_REL).exists()


def test_the_dry_run_reaches_the_secret_existence_check(mint, tree) -> None:
    """The task the dry run has to be trusted with: it must actually ASK
    GitHub whether the secret is there, not assume it is not."""
    openx, codex = tree
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner, "--dry-run") == 0
    assert runner.spoke("gh", "secret", "list")


# --------------------------------------------------------------- the whole mint

def test_the_whole_mint(mint, tree, capsys) -> None:
    """END TO END, with every process faked: fill, verify, record, land.

    One test rather than eight, because the properties it asserts are about the
    RUN and not about a step: that the seed reached exactly one destination and
    no other, that the five sentinels are gone and the three public values are
    in their places, that the two expiries agree character for character after
    the re-stamp, that both commits name their pathspecs, and that neither pull
    request was merged.
    """
    openx, codex = tree
    runner = runner_for(mint, openx, codex)
    assert invoke(mint, openx, codex, runner) == 0
    out = capsys.readouterr().out

    # -- the register is filled, and the sentinel is gone from the family
    for path in sorted((openx / FAMILY_REL).rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        values = [line for line in text.splitlines()
                  if "FILL-IN-AT-MINT" in line
                  and not line.lstrip().startswith("#")]
        assert not values, f"{path} still carries {values}"

    wallet = yaml.safe_load(
        (openx / mint.WALLET_REL).read_text(encoding="utf-8"))
    ref = wallet["key_reference"]
    assert ref["did"] == f"did:key:{ref['public_key_multibase']}"
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", ref["key_fingerprint"])
    assert ref["public_key_multibase"].startswith("z")

    attestation = yaml.safe_load(
        (openx / mint.ATTESTATION_REL).read_text(encoding="utf-8"))
    assert attestation["attested_key_fingerprint"] == ref["key_fingerprint"]
    instant = attestation["verified_at"]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", str(instant))

    # -- the expiry re-stamp, character for character on grant and row
    grant = yaml.safe_load((openx / mint.GRANT_REL).read_text(encoding="utf-8"))
    register = yaml.safe_load(
        (openx / mint.REGISTER_REL).read_text(encoding="utf-8"))
    assert grant["issued_at"] == "2026-09-03T00:00:00Z"
    assert grant["expires_at"] == "2026-12-02T00:00:00Z"
    assert register["rows"][0]["expires_at"] == grant["expires_at"]

    # -- the comments are untouched: this is a targeted fill, not a YAML rewrite
    assert "NOT YET MINTED — AND THE PLACEHOLDER IS THE POINT" in \
        (openx / mint.WALLET_REL).read_text(encoding="utf-8")

    # -- custody: exactly one destination, and it is stdin
    seed_hex = runner.secret_stdin.decode("ascii")
    assert re.fullmatch(r"[0-9a-f]{64}", seed_hex), (
        "the seed did not reach `gh secret set` on stdin as 64 lowercase hex "
        "characters")
    set_calls = [args for args in runner.argvs()
                 if args[:3] == ("gh", "secret", "set")]
    assert len(set_calls) == 1
    assert set_calls[0] == ("gh", "secret", "set", mint.SECRET_NAME,
                            "--env", mint.ENVIRONMENT,
                            "--repo", mint.TARGET_REPO, "--body", "-")

    # -- and nowhere else: not in an argv, not on stdout, not on disk
    for args in runner.argvs():
        assert seed_hex not in " ".join(args), f"the seed is in argv {args}"
        assert not SEED_HEX_RE.search(" ".join(args)), (
            f"a 64-hex run is in argv {args}")
    assert seed_hex not in out
    assert not SEED_HEX_RE.search(out.replace(ref["key_fingerprint"], "")), (
        "a 64-hex run reached stdout; the only one that may appear there is "
        "the fingerprint, which is a REFERENCE and not a key")
    written_files = [path for path in
                     list((openx / FAMILY_REL).rglob("*")) + list(codex.rglob("*"))
                     if path.is_file()]
    assert written_files
    for path in written_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        assert seed_hex not in text, f"the seed was written to {path}"

    # -- verification ran, all four, as CI runs them
    joined = [" ".join(args) for args in runner.argvs()]
    assert any("verify-openxwallet-pin.py" in j for j in joined)
    assert any(j.endswith("openXwallet/scripts/validate-openxwallet.py .")
               for j in joined)
    assert any(j.endswith("scripts/validate-factory-identity.py .")
               for j in joined)
    assert any("-m pytest tests/factory_identity -q" in j for j in joined)

    # -- the record, in the originating repository
    record = codex / mint.RECORD_DIR_REL / "2026-09-03-factory-origin-key-minted.md"
    assert record.is_file()
    body = record.read_text(encoding="utf-8")
    assert "Status: record" in body
    assert ref["key_fingerprint"] in body
    assert ref["did"] in body
    assert str(instant) in body
    assert mint.SECRET_NAME in body
    assert mint.ENVIRONMENT in body
    assert "#610" in body and "#182" in body
    assert seed_hex not in body

    # -- both commits name their pathspecs; neither is a bare commit
    commits = [args for args in runner.argvs() if "commit" in args]
    assert len(commits) == 2
    for args in commits:
        assert "--" in args, f"the commit {args} used no pathspec"
        assert args[args.index("--") + 1:], "the pathspec list is empty"

    # -- landed, readied, NOT merged
    assert runner.spoke("git", "push")
    ready = [args for args in runner.argvs() if args[:3] == ("gh", "pr", "ready")]
    assert {args[3] for args in ready} == {"610", "182"}
    assert not any("merge" in args for args in runner.argvs()), (
        "the program merged a pull request; governance/factory-identity/ is a "
        "permanently human-only surface")

    # -- and the operator is handed the two merge commands
    assert "gh pr merge 610 --squash --repo opensoft/openxFactory" in out
    assert "gh pr merge 182 --squash --repo opensoft/codexFactory" in out
    for value in (ref["did"], ref["key_fingerprint"],
                  ref["public_key_multibase"]):
        assert value in out, "the public values are not printed on success"


def test_a_failed_secret_set_aborts_before_any_register_edit(
        mint, tree, capsys) -> None:
    """generate -> store -> fill, never generate -> fill -> store. A register
    naming a public half nobody holds is worse than a sentinel: it merges."""
    openx, codex = tree
    before = {path: path.read_bytes()
              for path in sorted((openx / FAMILY_REL).rglob("*"))
              if path.is_file()}
    runner = runner_for(mint, openx, codex, secret_set_rc=1)
    assert invoke(mint, openx, codex, runner) == 1
    assert "refused [secret-set-failed]" in capsys.readouterr().err
    after = {path: path.read_bytes()
             for path in sorted((openx / FAMILY_REL).rglob("*"))
             if path.is_file()}
    assert after == before, "the register was edited after custody failed"
    assert not runner.spoke("git", "commit")


def test_a_failing_gate_leaves_the_tree_modified_and_uncommitted(
        mint, tree, capsys) -> None:
    openx, codex = tree
    runner = runner_for(mint, openx, codex, verify_rc=1)
    assert invoke(mint, openx, codex, runner) == 1
    err = capsys.readouterr().err
    assert "refused [verification-failed]" in err
    assert "MODIFIED AND UNCOMMITTED" in err
    # LEFT MODIFIED, deliberately: the remediation for a bad fill is to read the
    # diff, and a program that reverted the tree would take that away.
    values = [line for line in (openx / mint.WALLET_REL).read_text(
        encoding="utf-8").splitlines()
        if "FILL-IN-AT-MINT" in line and not line.lstrip().startswith("#")]
    assert not values, "the fill was rolled back; the diff is the remediation"
    assert not runner.spoke("git", "commit")
    assert not runner.spoke("git", "push")


def test_a_green_gate_that_adjudicated_nothing_is_refused(
        mint, tree, capsys) -> None:
    """A register reader that exits 0 without a disjointness note opened no
    register. That is the vacuous pass the whole gate exists to close."""
    openx, codex = tree
    runner = runner_for(mint, openx, codex, disjointness="not adjudicated")
    assert invoke(mint, openx, codex, runner) == 1
    assert "refused [verification-not-adjudicated]" in capsys.readouterr().err
    assert not runner.spoke("git", "commit")


# --------------------------------------------------------------- the fill rules

def test_a_sentinel_is_replaced_exactly_once(mint) -> None:
    text = ("key_reference:\n"
            "  # did: FILL-IN-AT-MINT is what the comment says\n"
            "  did: FILL-IN-AT-MINT\n"
            "  key_id: key-factory-codexfactory-0001\n")
    out = mint.replace_sentinel_once(text, "did", '"did:key:zABC"',
                                     sentinel="FILL-IN-AT-MINT", where="w")
    assert out.splitlines()[2] == '  did: "did:key:zABC"'
    assert out.splitlines()[1] == \
        "  # did: FILL-IN-AT-MINT is what the comment says", \
        "the comment was rewritten; the fill must be line-anchored, and a " \
        "comment line starts with '#', which is not whitespace"
    assert out.count("did:key:zABC") == 1


def test_a_missing_sentinel_refuses(mint) -> None:
    with pytest.raises(mint.Refusal) as excinfo:
        mint.replace_sentinel_once("  did: did:key:zAlreadyThere\n", "did", "x",
                                   sentinel="FILL-IN-AT-MINT", where="w")
    assert excinfo.value.code == "sentinel-not-exactly-once"
    assert "found 0" in str(excinfo.value)


def test_a_duplicated_sentinel_refuses(mint) -> None:
    with pytest.raises(mint.Refusal) as excinfo:
        mint.replace_sentinel_once(
            "  did: FILL-IN-AT-MINT\n  did: FILL-IN-AT-MINT\n", "did", "x",
            sentinel="FILL-IN-AT-MINT", where="w")
    assert excinfo.value.code == "sentinel-not-exactly-once"
    assert "found 2" in str(excinfo.value)


def test_the_restamp_matches_on_the_old_value_not_only_the_field(mint) -> None:
    """`register.yaml` is a ROWS file. A field-name-only match would re-stamp
    whichever `expires_at:` came first the day a second row lands."""
    text = ('rows:\n'
            '  - row_id: a\n'
            '    expires_at: "2026-12-01T00:00:00Z"\n'
            '  - row_id: b\n'
            '    expires_at: "2027-03-01T00:00:00Z"\n')
    out = mint.replace_quoted_value_once(
        text, "expires_at", "2027-03-01T00:00:00Z", "2026-12-02T00:00:00Z",
        where="r")
    assert '    expires_at: "2026-12-01T00:00:00Z"' in out
    assert '    expires_at: "2026-12-02T00:00:00Z"' in out
    assert "2027-03-01" not in out


def test_an_unmatched_restamp_refuses(mint) -> None:
    with pytest.raises(mint.Refusal) as excinfo:
        mint.replace_quoted_value_once('expires_at: "2026-12-01T00:00:00Z"\n',
                                       "expires_at", "2025-01-01T00:00:00Z",
                                       "x", where="r")
    assert excinfo.value.code == "restamp-not-exactly-once"


# --------------------------------------------------------------- the expiry math

@pytest.mark.parametrize("issued_at,today,expected", [
    # The shipped case: drafted 2026-09-02, minted the next day.
    ("2026-09-02T00:00:00Z", date(2026, 9, 3),
     ("2026-09-03T00:00:00Z", "2026-12-02T00:00:00Z")),
    # Same day: no re-stamp. The drafted issuance is still true.
    ("2026-09-02T00:00:00Z", date(2026, 9, 2), None),
    # An earlier clock is never a re-stamp: this is not a back-dating tool.
    ("2026-09-02T00:00:00Z", date(2026, 9, 1), None),
    # Across a leap day, because 90 days is COUNTED and never approximated.
    ("2027-11-30T00:00:00Z", date(2027, 12, 1),
     ("2027-12-01T00:00:00Z", "2028-02-29T00:00:00Z")),
    # Across a year boundary.
    ("2026-12-30T00:00:00Z", date(2026, 12, 31),
     ("2026-12-31T00:00:00Z", "2027-03-31T00:00:00Z")),
])
def test_the_restamp_arithmetic(mint, issued_at, today, expected) -> None:
    assert mint.restamp_dates(issued_at, today, 90) == expected


def test_the_restamp_lands_exactly_on_the_readers_ceiling(mint) -> None:
    """The reader refuses a grant running MORE than `MAX_GRANT_DAYS`. Midnight
    on both ends is what makes the difference exactly 90.0 and not 90.0000001 —
    which is the whole reason the re-stamp is not the provisioning instant."""
    validator_days = _validator_module().MAX_GRANT_DAYS
    issued, expires = mint.restamp_dates("2026-09-02T00:00:00Z",
                                         date(2026, 9, 3), validator_days)
    from datetime import datetime, timezone

    def parse(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(
            timezone.utc)

    days = (parse(expires) - parse(issued)).total_seconds() / 86400
    assert days == float(validator_days)
    assert not days > validator_days


def _validator_module():
    return load("_restamp_validator", VALIDATOR)


def test_the_mint_program_takes_the_ceiling_from_the_reader(mint) -> None:
    """One number, one place. A ceiling the mint believed and the reader did not
    would produce a grant the REQUIRED check refuses."""
    assert mint.GRANT_DAYS_FALLBACK == _validator_module().MAX_GRANT_DAYS


# --------------------------------------------------------------- the derive path

def test_the_derive_path_is_the_validators_own() -> None:
    """THE POINT OF THE WHOLE FILE. The three values the mint program writes
    into the register must be character-for-character what the runbook's own
    `validate-factory-identity.py --derive` prints for the same public half.

    The public half here is a labelled sha256 digest, so it is visible at a
    glance that nobody holds a private half for it.
    """
    import base64
    import hashlib

    validator = load("_derive_validator", VALIDATOR)
    pinned = validator.load_pinned_reader(PINNED_READER)
    mint = load("_derive_mint", MINT_SCRIPT)

    raw = hashlib.sha256(b"mint-script test / not a real key").digest()
    public = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    in_process = mint.derive_public_values(validator, pinned, public)

    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--derive", public],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr

    printed = {}
    for line in proc.stdout.splitlines():
        match = mint.DERIVE_VALUE_RE.match(line)
        if match and not line.lstrip().startswith("#"):
            printed[match.group(1)] = match.group(2).strip().strip('"')

    assert in_process == printed
    assert set(printed) == set(mint.DERIVE_KEYS)
    assert in_process["did"] == f"did:key:{in_process['public_key_multibase']}"
    assert in_process["key_fingerprint"] == \
        "sha256:" + hashlib.sha256(raw).hexdigest()


def test_a_seed_shaped_input_is_refused_by_the_derive_path(mint) -> None:
    """`--derive` takes the PUBLIC half only, and the mint program inherits that
    refusal rather than re-checking it: a 64-hex seed fails by SHAPE."""
    validator = _validator_module()
    pinned = validator.load_pinned_reader(PINNED_READER)
    with pytest.raises(mint.Refusal) as excinfo:
        mint.derive_public_values(validator, pinned, "0" * 64)
    assert excinfo.value.code == "derive-refused"
