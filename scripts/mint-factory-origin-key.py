#!/usr/bin/env python3
"""THE MINT, as ONE PROGRAM the operator runs in his own terminal.

`docs/factory-origin-key-mint-runbook.md` used to be a six-step manual
checklist: generate a seed in a heredoc, copy a public half into a second
command, paste three derived values into two files by hand, re-stamp two
expiries in two more files so they match character for character, run four
gates, write a record in a second repository, then ready two draft pull
requests. Every one of those steps is mechanical, and every one of them is a
place where a hand-performed mint can go half-done — which is the one outcome
the register family cannot hold. A half-filled register is louder than an
untouched one only because a validator says so; it is still a broken governed
surface, and the operator discovers it after the seed is already provisioned
and unrecoverable.

So the checklist is this file. The ceremony's JUDGEMENT stays with the operator
(he decides that the mint happens, and he is the only party who ever sees the
private half); its BOOKKEEPING is executed.

WHAT THIS PROGRAM WILL NOT DO, and why each refusal is here.

(1) IT DERIVES NOTHING. `did`, `key_fingerprint` and `public_key_multibase` are
    obtained by CALLING `scripts/validate-factory-identity.py`'s own `derive`
    entry point IN-PROCESS and reading the values it prints. That reader in
    turn refuses to run at all unless the PINNED openXwallet decoders are
    importable, and round-trips every value back through them before printing.
    So the encodings this program writes into the register are, by
    construction, the encodings the REQUIRED `wallet-validation` check will
    judge them by. A second implementation of base58btc or of the fingerprint
    spelling is the defect the whole family exists to prevent: two spellings of
    one key are two keys to anything comparing strings.

(2) IT NEVER LETS THE PRIVATE HALF BE OBSERVABLE. The 32-byte seed is generated
    in this process, handed to `gh secret set` on the child's STDIN — with NO
    `--body` flag, which is what makes gh read stdin at all (see
    `store_private_half`) — and then overwritten and deleted. It is never an
    argv element (argv is world-readable in /proc), never an environment
    variable (inherited by every descendant, and printed by any `env` in a
    shell hook), never a temporary file (survives a crash, lands in a backup),
    and never printed or logged. The command log this program keeps records
    argv and the LENGTH of anything written to a child's stdin, never its
    bytes.

(3) IT REFUSES TO RE-MINT. The ratified requirement admits EXACTLY ONE origin
    identity per originating repository. Two independent preflight checks stand
    on that: the five `FILL-IN-AT-MINT` sentinels must still be present (a
    filled register means the mint already happened), and the environment
    secret must NOT already exist (a present secret means a private half is
    already held, and overwriting it silently orphans every signature made
    under it). Either one absent is a NAMED refusal, not a warning. That is
    also this program's idempotence story: a second run stops at preflight and
    says which of the two conditions ended it.

(4) IT ABORTS BEFORE TOUCHING THE REGISTER IF CUSTODY FAILS. The order is
    generate -> store -> fill, never generate -> fill -> store. A register
    naming a public half whose private half reached no destination is a
    published identity nobody holds — worse than a sentinel, because it merges.

(5) IT COMMITS NOTHING IT HAS NOT VERIFIED. All four gates from the runbook run
    against the modified working tree BEFORE either commit. Any failure leaves
    the tree MODIFIED AND UNCOMMITTED for inspection and exits non-zero: the
    remediation for a bad fill is to look at the diff, not to re-mint.

(6) IT DOES NOT MERGE. Both pull requests are moved out of draft; the two merge
    commands are PRINTED for the operator. `governance/factory-identity/` is a
    permanently human-only surface, entered by name in codexFactory's
    never-clearable floor, and a program that merged it would be the exact
    autonomous landing that floor exists to refuse.

USAGE

    python3 scripts/mint-factory-origin-key.py --dry-run \\
        --codex-worktree /path/to/codexFactory-worktree
    python3 scripts/mint-factory-origin-key.py \\
        --codex-worktree /path/to/codexFactory-worktree

Run `--dry-run` first, always. It performs every preflight check — including
the two read-only GitHub ones — and prints the exact plan, then stops without
generating a seed, writing a file, committing, or pushing.

EXIT CODES
    0  the mint completed (or the dry run's plan is clean)
    1  a NAMED refusal: preflight, a fill that did not match exactly once, or a
       verification gate. The reason is printed with a `refused [<code>]` prefix
    2  the program could not run at all (no pinned reader, bad usage)
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import importlib.util
import io
import re
import secrets
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_REL = "scripts/validate-factory-identity.py"
PINNED_READER_REL = "openXwallet/scripts/validate-openxwallet.py"

#: The literal the mint replaces. ONE spelling, shared with the validator so a
#: divergence is impossible: this module imports the constant rather than
#: restating it (see `load_validator`).
SENTINEL_FALLBACK = "FILL-IN-AT-MINT"

#: THE ONLY PLACE IN THIS REPOSITORY'S CODE THAT NAMES THE SECRET, beside the
#: runbook. The ratified requirement forbids "a secret name resolvable to key
#: material" anywhere under `governance/factory-identity/`, and
#: `validate-factory-identity.py` refuses that tree over its RAW BYTES if an
#: environment-variable-shaped token naming key material appears in it. This
#: file is `scripts/`, not that family, so the name is legal here — and it has
#: to live somewhere a program can read it.
SECRET_NAME = "FACTORY_ORIGIN_SIGNING_KEY"
ENVIRONMENT = "worker-credentials"
TARGET_REPO = "opensoft/codexFactory"

#: The ceiling this realization adopts for an origin grant, in days. The same
#: number `validate-factory-identity.MAX_GRANT_DAYS` enforces; imported from it
#: at run time rather than trusted from here.
GRANT_DAYS_FALLBACK = 90

WALLET_REL = ("governance/factory-identity/wallets/"
              "wal-origin-codexfactory-0001.yaml")
ATTESTATION_REL = ("governance/factory-identity/attestations/"
                   "custody-attest-wal-origin-codexfactory-0001.yaml")
GRANT_REL = ("governance/factory-identity/grants/"
             "grant-origin-codexfactory-0001.yaml")
REGISTER_REL = "governance/factory-identity/register.yaml"

#: The five FILL-IN-AT-MINT sentinels, by the file and field each sits on, and
#: the derived value each is replaced by. The distribution is asserted (3 + 2)
#: rather than only the total, so a sentinel that MOVED between files is a
#: refusal instead of a pass.
WALLET_FIELDS = ("did", "key_fingerprint", "public_key_multibase")
ATTESTATION_FIELDS = ("attested_key_fingerprint", "verified_at")
EXPECTED_SENTINEL_TOTAL = len(WALLET_FIELDS) + len(ATTESTATION_FIELDS)

REGISTER_BRANCH = "realize/factory-identity-register"
FLOOR_BRANCH = "realize/factory-identity-floor-entry"
REGISTER_REPO = "opensoft/openxFactory"

RECORD_DIR_REL = "hermes/domain/factory-identity/records"
RECORD_BASENAME = "{date}-factory-origin-key-minted.md"

REGISTER_COMMIT_SUBJECT = "Mint the codexFactory origin key: register filled at {instant}"
FLOOR_COMMIT_SUBJECT = "Record the codexFactory origin-key mint"

#: Preferred merge method, first one the repository actually allows. Printed,
#: never executed: this surface is human-only by ratified requirement.
MERGE_METHOD_PREFERENCE = ("squash", "merge", "rebase")


class Refusal(Exception):
    """A NAMED stop. Every refusal this program can make carries a code, so the
    operator's next action is determined by the code rather than by reading
    prose — and so a second run's refusal says WHICH condition ended it."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


# --------------------------------------------------------------- the process seam

@dataclass
class Invocation:
    """One child process, as recorded. `stdin_bytes` is a LENGTH, never bytes:
    the only thing this program ever writes to a child's stdin is the private
    seed, and a log that carried it would defeat the custody rule this whole
    file is built around."""

    argv: tuple[str, ...]
    cwd: str | None
    stdin_bytes: int | None


class SubprocessRunner:
    """THE ONE PLACE a child process is started.

    It exists as a seam so the test suite can inject a double: `gh` is
    unreachable from a test by construction (`tests/hermeticity.py` puts a
    refusing shim first on PATH), and `gh secret set` must never be reached by
    a test even if it were.
    """

    def __init__(self) -> None:
        self.log: list[Invocation] = []

    def run(self, argv, *, cwd: Path | str | None = None,
            stdin: bytes | None = None) -> tuple[int, str]:
        args = [str(a) for a in argv]
        self.log.append(Invocation(tuple(args),
                                   str(cwd) if cwd is not None else None,
                                   None if stdin is None else len(stdin)))
        proc = subprocess.run(
            args, cwd=None if cwd is None else str(cwd), input=stdin,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


# --------------------------------------------------------------- the pinned path

def load_validator(root: Path):
    """Import `scripts/validate-factory-identity.py` as a module.

    The register reader is IMPORTED rather than shelled out to, because this
    program needs its `derive` return path and its `check_placeholders` rule as
    VALUES. Shelling out would give a text stream and an exit code, and the
    sentinel accounting would then be a second parser of the same rule.
    """
    path = root / VALIDATOR_REL
    if not path.is_file():
        raise SystemExit(f"mint-factory-origin-key: no register reader at {path}; "
                         f"this program derives nothing of its own and cannot "
                         f"proceed without it")
    spec = importlib.util.spec_from_file_location("_mint_fi_validator", path)
    if spec is None or spec.loader is None:  # pragma: no cover - importlib shape
        raise SystemExit(f"mint-factory-origin-key: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    # REGISTERED before execution, not after. Both files carry `from __future__
    # import annotations`, so a `@dataclass` in the imported module resolves its
    # field types through `sys.modules[cls.__module__].__dict__` — which is
    # `None` for a module that was executed but never registered, and every
    # dataclass then raises at class-creation time.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_pinned(validator, root: Path):
    """The PINNED openXwallet decoders, through the validator's own loader.

    The loader raises `SystemExit` when the gitlink is absent. That is the
    correct behaviour for the reader and the wrong behaviour here — this
    program must refuse BEFORE MINTING with a named code the operator can act
    on — so the file's presence is checked first and the named refusal is
    raised from here.
    """
    pinned_path = root / PINNED_READER_REL
    if not pinned_path.is_file():
        raise Refusal(
            "openxwallet-gitlink-absent",
            f"the pinned openXwallet reader is not at {pinned_path}. The "
            f"register reader exits 2 without it and this program derives "
            f"nothing of its own, so a mint performed now would produce values "
            f"no gate could judge. Run `git submodule update --init "
            f"openXwallet` in {root} and re-run.")
    return validator.load_pinned_reader(pinned_path)


DERIVE_VALUE_RE = re.compile(
    r"^\s*(did|key_fingerprint|public_key_multibase|public_key):\s*(.+?)\s*$")
DERIVE_KEYS = ("did", "key_fingerprint", "public_key_multibase", "public_key")


def derive_public_values(validator, pinned,
                         public_key_b64u: str) -> dict[str, str]:
    """The four public values, from THE REGISTER READER'S OWN `derive`.

    THERE IS NO DERIVATION IN THIS FUNCTION. `validator.derive` is called
    in-process, its stdout captured, and the values it printed parsed back. Its
    contract is exactly what this program needs: public half only, every value
    round-tripped through the PINNED decoders before printing, and a non-zero
    return rather than a printed value when any round trip disagrees.

    Capturing print output is uglier than calling a function that returns a
    dict — and it is the RIGHT ugliness. The alternative is either a second
    derivation here (the defect) or a refactor of the reader that would change
    the code the REQUIRED check runs in the same commit as the mint.
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = validator.derive(pinned, public_key_b64u)
    if code != 0:
        raise Refusal(
            "derive-refused",
            f"the register reader's own derive path refused this public half "
            f"(exit {code}). Nothing was written. This is the round-trip guard "
            f"firing, not a transcription slip — see its stderr above.")
    values: dict[str, str] = {}
    for line in buffer.getvalue().splitlines():
        if line.lstrip().startswith("#"):
            continue
        match = DERIVE_VALUE_RE.match(line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    missing = [key for key in DERIVE_KEYS if key not in values]
    if missing:
        raise Refusal(
            "derive-unparsed",
            f"the register reader's derive output did not carry {missing}. Its "
            f"printed shape changed and this program's parse of it did not; "
            f"refusing rather than writing a partial key reference into the "
            f"register.")
    if values["did"] != f"did:key:{values['public_key_multibase']}":
        raise Refusal(
            "derive-inconsistent",
            f"the derived did {values['did']!r} is not `did:key:` + its own "
            f"multibase {values['public_key_multibase']!r}; refusing")
    if values["public_key"] != public_key_b64u:
        raise Refusal(
            "derive-inconsistent",
            "the derived base64url spelling does not round-trip to the public "
            "half this program generated; refusing")
    return values


# --------------------------------------------------------------- targeted edits

def _sentinel_pattern(field_name: str, sentinel: str) -> re.Pattern[str]:
    return re.compile(
        rf"^(?P<indent>[ \t]*){re.escape(field_name)}:[ \t]+"
        rf"{re.escape(sentinel)}[ \t]*$", re.MULTILINE)


def replace_sentinel_once(text: str, field_name: str, value: str, *,
                          sentinel: str, where: str) -> str:
    """Replace EXACTLY ONE `<field>: FILL-IN-AT-MINT` line, or refuse.

    Not a `str.replace`, and not a YAML round trip. `str.replace` would happily
    fill zero occurrences or six; a YAML round trip would rewrite every comment
    in the file, and these files are 80% comment by line count — the comments
    are the governed record of WHY each field is shaped as it is, and a mint is
    not authorized to reflow them.

    The line anchor (`^[ \\t]*<field>:`) is what keeps the prose out of scope: a
    comment mentioning the sentinel starts with `#`, which is not whitespace,
    so it cannot match. Zero matches means the mint already happened or the
    field was renamed; two means the file grew a duplicate. Both are refusals.
    """
    matches = list(_sentinel_pattern(field_name, sentinel).finditer(text))
    if len(matches) != 1:
        raise Refusal(
            "sentinel-not-exactly-once",
            f"{where}: expected exactly ONE `{field_name}: {sentinel}` line, "
            f"found {len(matches)}. Zero means this field is already filled (so "
            f"the mint already happened — see the runbook's rotation section, "
            f"which SUPERSEDES a row and never re-fills one) or was renamed; "
            f"two means the file carries a duplicate. Nothing was written.")
    match = matches[0]
    return (text[:match.start()]
            + f"{match.group('indent')}{field_name}: {value}"
            + text[match.end():])


def replace_quoted_value_once(text: str, field_name: str, old: str, new: str, *,
                              where: str) -> str:
    """Re-stamp EXACTLY ONE `<field>: "<old>"` line, or refuse.

    The OLD value is part of the pattern on purpose. Matching on the field name
    alone would re-stamp whichever `expires_at:` came first, and `register.yaml`
    is a rows file — the day a second row lands, a field-name match would move
    the wrong one and the character-for-character comparison the reader makes
    would still pass, because it compares the grant against the row it names.
    """
    pattern = re.compile(
        rf"^(?P<indent>[ \t]*){re.escape(field_name)}:[ \t]+"
        rf"\"{re.escape(old)}\"[ \t]*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise Refusal(
            "restamp-not-exactly-once",
            f"{where}: expected exactly ONE `{field_name}: \"{old}\"` line, "
            f"found {len(matches)}. Nothing was written.")
    match = matches[0]
    return (text[:match.start()]
            + f"{match.group('indent')}{field_name}: \"{new}\""
            + text[match.end():])


# --------------------------------------------------------------- the expiry math

def restamp_dates(issued_at: str, today: date, grant_days: int):
    """`(new_issued_at, new_expires_at)`, or `None` when no re-stamp is due.

    THE RULE THE RUNBOOK STATES: if the mint happens on a later date than the
    register's drafted `issued_at`, re-stamp the grant's `issued_at` to today
    and its `expires_at` to today + 90 days, and make the backing row's
    `expires_at` character-for-character equal.

    MIDNIGHT UTC, not the provisioning instant, and the choice is recorded
    rather than left to be inferred. The drafted values are midnight, the seat
    grants beside them are midnight, and midnight makes `expires_at - issued_at`
    exactly `grant_days` days by integer arithmetic — so the reader's
    `days > MAX_GRANT_DAYS` comparison lands on 90.0 and not on 90.0000001. The
    provisioning INSTANT is recorded where it belongs and where it is a fact
    about custody rather than about issuance: the attestation's `verified_at`.
    """
    issued_date = date.fromisoformat(issued_at[:10])
    if today <= issued_date:
        return None
    expires_date = today + timedelta(days=grant_days)
    return (f"{today.isoformat()}T00:00:00Z",
            f"{expires_date.isoformat()}T00:00:00Z")


# --------------------------------------------------------------- preflight

@dataclass
class Check:
    name: str
    detail: str


@dataclass
class Plan:
    openx_root: Path
    codex_root: Path
    today: date
    grant_issued_at: str
    grant_expires_at: str
    row_expires_at: str
    restamp: tuple[str, str] | None
    record_path: Path
    register_pr: int
    floor_pr: int
    checks: list[Check] = field(default_factory=list)
    #: The PINNED openXwallet decoder module, loaded during preflight so the
    #: gitlink refusal happens before anything is spent and the mint does not
    #: load it a second time.
    pinned: object | None = None


SENTINEL_FINDING_RE = re.compile(
    r"^error \[factory-identity-placeholder-unminted\] "
    r"(?P<rel>[^\s:]+):(?P<line>\d+): ")


def sentinel_distribution(validator, root: Path) -> dict[str, int]:
    """Where the mint sentinels are, BY THE REGISTER READER'S OWN RULE.

    `check_placeholders` is called rather than re-implemented, so "a sentinel"
    means here exactly what it means in the REQUIRED check — including the part
    that is easy to get wrong twice, that a sentinel inside a COMMENT is prose
    and not a value.
    """
    findings = validator.Findings()
    validator.check_placeholders(findings, root, validator.family_files(root))
    out: dict[str, int] = {}
    for line in findings.errors:
        match = SENTINEL_FINDING_RE.match(line)
        if match is None:  # pragma: no cover - the reader's message shape moved
            raise Refusal(
                "sentinel-accounting-unparsed",
                f"the register reader's placeholder finding no longer parses: "
                f"{line!r}. Refusing rather than guessing where the sentinels "
                f"are.")
        out[match.group("rel")] = out.get(match.group("rel"), 0) + 1
    return out


def _git(runner, root: Path, *args) -> tuple[int, str]:
    return runner.run(["git", "-C", str(root), *args])


def check_worktree(runner, root: Path, branch: str, label: str) -> Check:
    code, out = _git(runner, root, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0:
        raise Refusal("worktree-not-a-checkout",
                      f"{label}: {root} is not a git checkout: {out.strip()}")
    head = out.strip()
    if head != branch:
        raise Refusal(
            "worktree-wrong-branch",
            f"{label}: {root} is on {head!r}, not on {branch!r}. The mint "
            f"lands on the branch its draft pull request already carries; a "
            f"commit on another branch has to be cherry-picked back out.")
    code, out = _git(runner, root, "status", "--porcelain")
    if code != 0:
        raise Refusal("worktree-unreadable",
                      f"{label}: cannot read the working tree of {root}")
    dirty = [line for line in out.splitlines() if line.strip()]
    if dirty:
        raise Refusal(
            "worktree-dirty",
            f"{label}: {root} has {len(dirty)} uncommitted change(s):\n  "
            + "\n  ".join(dirty[:20])
            + f"\nThis program commits with explicit pathspecs, so foreign "
              f"changes would not be swept in — but it also VERIFIES the tree "
              f"before committing, and an unrelated edit makes that "
              f"verification meaningless. Commit or stash first.")
    return Check(f"{label}-clean", f"{root} on {branch}, clean")


def discover_pr(runner, repo: str, branch: str, override: int | None) -> int:
    if override is not None:
        return override
    code, out = runner.run(
        ["gh", "pr", "list", "--repo", repo, "--head", branch, "--state", "open",
         "--json", "number", "--jq", ".[].number"])
    if code != 0:
        raise Refusal("pr-lookup-failed",
                      f"cannot list open pull requests for {repo} head "
                      f"{branch}: {out.strip()}")
    numbers = [line.strip() for line in out.splitlines() if line.strip()]
    if len(numbers) != 1:
        raise Refusal(
            "pr-not-unique",
            f"{repo} head {branch} resolves to {len(numbers)} open pull "
            f"request(s) {numbers}; expected exactly one. Pass the number "
            f"explicitly if this is deliberate.")
    return int(numbers[0])


def preflight(runner, validator, args, openx_root: Path,
              codex_root: Path) -> Plan:
    """FAIL-CLOSED, and in this order. Every check that can refuse without
    spending anything runs before the one that spends something."""
    checks: list[Check] = []

    code, out = runner.run(["gh", "auth", "status"])
    if code != 0:
        raise Refusal(
            "gh-unauthenticated",
            f"`gh auth status` exited {code}. The mint stores a secret and "
            f"readies two pull requests; an unauthenticated run would fail "
            f"AFTER generating a seed.\n{out.strip()}")
    checks.append(Check("gh-auth", "authenticated"))

    code, out = runner.run(
        ["gh", "api", f"repos/{TARGET_REPO}/environments/{ENVIRONMENT}",
         "--jq", ".name"])
    if code != 0 or out.strip() != ENVIRONMENT:
        raise Refusal(
            "environment-absent",
            f"the {ENVIRONMENT!r} environment of {TARGET_REPO} did not resolve "
            f"(exit {code}): {out.strip()}. The private half has EXACTLY ONE "
            f"admitted destination and that is it; there is no fallback.")
    checks.append(Check("environment",
                        f"{TARGET_REPO} environment {ENVIRONMENT} exists"))

    pinned = load_pinned(validator, openx_root)
    checks.append(Check("openxwallet-gitlink",
                        f"pinned decoders importable from {PINNED_READER_REL}"))

    checks.append(check_worktree(runner, openx_root, REGISTER_BRANCH,
                                 "openxFactory"))
    checks.append(check_worktree(runner, codex_root, FLOOR_BRANCH,
                                 "codexFactory"))

    distribution = sentinel_distribution(validator, openx_root)
    total = sum(distribution.values())
    expected = {WALLET_REL: len(WALLET_FIELDS),
                ATTESTATION_REL: len(ATTESTATION_FIELDS)}
    if distribution != expected:
        raise Refusal(
            "register-already-minted",
            f"the mint sentinels are not where an unminted register carries "
            f"them. Expected {expected}, found {distribution or '{}'} "
            f"({total} of {EXPECTED_SENTINEL_TOTAL}).\nONE ORIGIN IDENTITY PER "
            f"REPOSITORY is ratified: a filled register means the mint already "
            f"happened, and the answer to a lost or rotated key is a NEW "
            f"wallet, grant and row whose `supersedes:` names this one — never "
            f"a re-fill of these fields. See the runbook's rotation section.")
    checks.append(Check("mint-sentinels",
                        f"{total} sentinel(s) present, {expected}"))

    code, out = runner.run(
        ["gh", "secret", "list", "--env", ENVIRONMENT, "--repo", TARGET_REPO])
    if code != 0:
        raise Refusal(
            "secret-list-failed",
            f"cannot list the secrets of {TARGET_REPO} environment "
            f"{ENVIRONMENT} (exit {code}): {out.strip()}. This program will "
            f"not mint over a store it could not read.")
    existing = {line.split()[0] for line in out.splitlines() if line.split()}
    if SECRET_NAME in existing:
        raise Refusal(
            "secret-already-exists",
            f"{SECRET_NAME} already exists in {TARGET_REPO} environment "
            f"{ENVIRONMENT}. A private half is already held there, and "
            f"overwriting it would silently orphan every signature ever made "
            f"under it while leaving the register pointing at a public half "
            f"nobody holds. Rotation SUPERSEDES a row — see the runbook.")
    checks.append(Check("secret-absent",
                        f"{SECRET_NAME} not present in {ENVIRONMENT} "
                        f"({len(existing)} other secret(s) there)"))

    today = args.today or datetime.now(timezone.utc).date()
    record_path = (codex_root / RECORD_DIR_REL
                   / RECORD_BASENAME.format(date=today.isoformat()))
    if record_path.exists():
        raise Refusal(
            "record-already-exists",
            f"{record_path} already exists. A mint record is an immutable "
            f"record; this program will not overwrite one.")
    checks.append(Check("mint-record-absent", str(record_path)))

    import yaml  # the reader already required it; local so --help never needs it
    grant = yaml.safe_load((openx_root / GRANT_REL).read_text(encoding="utf-8"))
    register = yaml.safe_load(
        (openx_root / REGISTER_REL).read_text(encoding="utf-8"))
    row = register["rows"][0]
    grant_days = getattr(validator, "MAX_GRANT_DAYS", GRANT_DAYS_FALLBACK)
    restamp = restamp_dates(str(grant["issued_at"]), today, grant_days)
    if grant["expires_at"] != row["expires_at"]:
        raise Refusal(
            "expiry-already-disagrees",
            f"the grant expires at {grant['expires_at']!r} and its backing row "
            f"at {row['expires_at']!r} BEFORE the mint. Two expiries for one "
            f"authority is one of them being wrong; fix that first.")
    checks.append(Check(
        "expiry",
        f"grant issued_at {grant['issued_at']}, expires_at "
        f"{grant['expires_at']}"
        + (f" -> re-stamp to {restamp[0]} / {restamp[1]} (today is "
           f"{today.isoformat()}, {grant_days} days)"
           if restamp else f" -> no re-stamp (today is {today.isoformat()})")))

    plan = Plan(
        openx_root=openx_root, codex_root=codex_root, today=today,
        grant_issued_at=str(grant["issued_at"]),
        grant_expires_at=str(grant["expires_at"]),
        row_expires_at=str(row["expires_at"]),
        restamp=restamp, record_path=record_path,
        register_pr=discover_pr(runner, REGISTER_REPO, REGISTER_BRANCH,
                                args.register_pr),
        floor_pr=discover_pr(runner, TARGET_REPO, FLOOR_BRANCH, args.floor_pr),
        checks=checks, pinned=pinned)
    return plan


# --------------------------------------------------------------- the mint

def store_private_half(runner, seed_hex: str) -> str:
    """`gh secret set`, reading the seed from THIS PROCESS'S stdin pipe, and the
    RFC3339 instant it succeeded at.

    STDIN RATHER THAN AN ARGUMENT is the whole point: a value passed as
    `--body <value>` sits in the child's argv, which is world-readable in
    `/proc/<pid>/cmdline` for the life of the call and lands in the shell
    history of anyone who reconstructs the command.

    THERE IS NO `--body -`, AND WRITING ONE WOULD STORE THE STRING "-". `gh
    secret set --help` (2.86.0): "-b, --body string   The value for the secret
    (READS FROM STANDARD INPUT IF NOT SPECIFIED)". The flag takes no magic
    dash — `--body -` is a body whose value is one hyphen, and `gh` would exit
    0 having stored a one-character secret while this program reported a
    successful mint. The stdin path is reached by OMITTING the flag, which is
    also what `gh`'s own documented example does (`gh secret set MYSECRET <
    myfile.txt`). Nothing prompts, because stdin is a pipe.

    No trailing newline is written, so nothing depends on `gh`'s trimming.

    THEN IT CONFIRMS THE STORE LANDED. A secret's value cannot be read back, so
    the check is that the name now EXISTS where it did not before preflight —
    which is the strongest available evidence that the exchange did something,
    and it catches a `gh` that exits 0 having stored nothing.
    """
    code, out = runner.run(
        ["gh", "secret", "set", SECRET_NAME, "--env", ENVIRONMENT,
         "--repo", TARGET_REPO],
        stdin=seed_hex.encode("ascii"))
    if code != 0:
        raise Refusal(
            "secret-set-failed",
            f"`gh secret set {SECRET_NAME}` exited {code}: {out.strip()}\n"
            f"NOTHING WAS WRITTEN to the register. The seed generated for this "
            f"run reached no destination and is being discarded; re-run to mint "
            f"a fresh one. Do NOT hand-copy a seed from anywhere.")
    instant = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, out = runner.run(
        ["gh", "secret", "list", "--env", ENVIRONMENT, "--repo", TARGET_REPO])
    stored = {line.split()[0] for line in out.splitlines() if line.split()}
    if code != 0 or SECRET_NAME not in stored:
        raise Refusal(
            "secret-set-unconfirmed",
            f"`gh secret set` exited 0 but {SECRET_NAME} does not appear in "
            f"{TARGET_REPO} environment {ENVIRONMENT} (list exit {code}): "
            f"{out.strip()}\nNOTHING WAS WRITTEN to the register. Do not "
            f"proceed: a register naming a public half whose private half "
            f"reached no destination is a published identity nobody holds.")
    return instant


def fill_register(plan: Plan, values: dict[str, str], instant: str, *,
                  sentinel: str) -> list[Path]:
    """The five sentinels and, when due, the two expiries plus the row's.

    Every write is a targeted single-occurrence replacement that refuses rather
    than guessing (see `replace_sentinel_once`). The files are read, edited in
    memory and written once each, so a refusal partway through leaves the ones
    before it written and the ones after it untouched — which is why the
    accounting refusal above runs BEFORE any of this, and why verification runs
    after all of it.
    """
    written: list[Path] = []

    wallet_path = plan.openx_root / WALLET_REL
    text = wallet_path.read_text(encoding="utf-8")
    for field_name in WALLET_FIELDS:
        # `did` carries two colons and no space, so it is a legal YAML plain
        # scalar — but the reader's own derive output QUOTES it, and the
        # register is read by more than one parser. Quote what it quotes.
        rendered = (f'"{values[field_name]}"' if field_name == "did"
                    else values[field_name])
        text = replace_sentinel_once(text, field_name, rendered,
                                     sentinel=sentinel, where=WALLET_REL)
    wallet_path.write_text(text, encoding="utf-8")
    written.append(wallet_path)

    attest_path = plan.openx_root / ATTESTATION_REL
    text = attest_path.read_text(encoding="utf-8")
    text = replace_sentinel_once(text, "attested_key_fingerprint",
                                 values["key_fingerprint"],
                                 sentinel=sentinel, where=ATTESTATION_REL)
    text = replace_sentinel_once(text, "verified_at", f'"{instant}"',
                                 sentinel=sentinel, where=ATTESTATION_REL)
    attest_path.write_text(text, encoding="utf-8")
    written.append(attest_path)

    if plan.restamp is not None:
        new_issued, new_expires = plan.restamp
        grant_path = plan.openx_root / GRANT_REL
        text = grant_path.read_text(encoding="utf-8")
        text = replace_quoted_value_once(text, "issued_at",
                                         plan.grant_issued_at, new_issued,
                                         where=GRANT_REL)
        text = replace_quoted_value_once(text, "expires_at",
                                         plan.grant_expires_at, new_expires,
                                         where=GRANT_REL)
        grant_path.write_text(text, encoding="utf-8")
        written.append(grant_path)

        register_path = plan.openx_root / REGISTER_REL
        text = register_path.read_text(encoding="utf-8")
        text = replace_quoted_value_once(text, "expires_at",
                                         plan.row_expires_at, new_expires,
                                         where=REGISTER_REL)
        register_path.write_text(text, encoding="utf-8")
        written.append(register_path)

    return written


# --------------------------------------------------------------- verification

def verification_commands(openx_root: Path) -> list[tuple[str, list[str]]]:
    """The runbook's four gates, as the CI and the REQUIRED check run them.

    The invocations are the literal ones: `verify-openxwallet-pin.py` with no
    argument (`openxwallet-consumer-gate.yml`), the PINNED validator with the
    scan target `.` present and equal to `.` (a missing or file-valued argument
    is a green check that opened no register), the register reader the same way,
    and the collected test directory. A gate run differently from CI is not the
    gate.
    """
    return [
        ("openxwallet pin",
         [sys.executable, "scripts/verify-openxwallet-pin.py"]),
        ("pinned openXwallet validator (wallet-validation)",
         [sys.executable, "openXwallet/scripts/validate-openxwallet.py", "."]),
        ("factory-identity register reader",
         [sys.executable, "scripts/validate-factory-identity.py", "."]),
        ("tests/factory_identity",
         [sys.executable, "-m", "pytest", "tests/factory_identity", "-q"]),
    ]


def verify(runner, plan: Plan) -> None:
    for label, argv in verification_commands(plan.openx_root):
        code, out = runner.run(argv, cwd=plan.openx_root)
        print(f"  {label}: exit {code}")
        if code != 0:
            raise Refusal(
                "verification-failed",
                f"{label} refused the filled tree (exit {code}):\n{out}\n"
                f"THE TREE IS LEFT MODIFIED AND UNCOMMITTED so you can inspect "
                f"the diff — `git -C {plan.openx_root} diff`. The private half "
                f"IS ALREADY STORED in {TARGET_REPO} / {ENVIRONMENT}; do not "
                f"re-run this program (it will refuse at "
                f"`secret-already-exists`). Repair the fill by hand against the "
                f"public values printed above, or revert the working tree and "
                f"delete the secret to start over.")
        if label.endswith("register reader"):
            if "0 shared" not in out:
                raise Refusal(
                    "verification-not-adjudicated",
                    f"the register reader ran clean but its log carries no "
                    f"disjointness note ending `0 shared`. A green run that "
                    f"adjudicated nothing is a vacuous pass.\n{out}")
            print("    disjointness adjudicated: 0 shared")


# --------------------------------------------------------------- the record

RECORD_TEMPLATE = """# Record: the codexFactory origin signing key is minted and provisioned

Status: record
Qualifies: tasks 2.1-2.4 of openxFactory `add-cpc-clearing-boundary`
  (capability `factory-origin-identity`), and task 4.2 of the same packet's
  codexFactory realization.
Recorded: {today}
Ruled by: Brett Heap, in session {today} — "mint the codexFactory origin key".

## The obligation this discharges

The ratified requirement admits ONE Ed25519 origin identity per originating
repository and refuses the register family while any mint sentinel stands.
openxFactory PR #{register_pr} shipped that family with five `FILL-IN-AT-MINT`
sentinels and both readers refusing it; this record is the other half of the act
that filled them.

**Named as explicitly as what changed: what did NOT.** The four council seat
signing keys are untouched. No existing key was re-minted. No custody
declaration moved — `wal-agent-mrc-0001` and its `keys:` block are unchanged,
and this key appears in no review-authority record, which
`scripts/validate-factory-identity.py`'s disjointness rule CHECKS rather than
assumes.

## What was minted

One Ed25519 key pair, the ORIGIN identity of `opensoft/codexFactory`. Exactly
one: the ratified requirement admits one origin identity per originating
repository, and a second concurrent row is refused.

| Repository | Key id | Public key (unpadded base64url, 32 raw bytes) | Key fingerprint |
| --- | --- | --- | --- |
| `opensoft/codexFactory` | `key-factory-codexfactory-0001` | `{public_key}` | `{key_fingerprint}` |

The fingerprint is the one spelling the estate computes everywhere —
`"sha256:" + sha256(raw 32-byte public key).hexdigest()` — and it RECOMPUTES
from the public key beside it, which is what
`scripts/validate-factory-identity.py` checks rather than trusts, through the
PINNED openXwallet decoder rather than a second implementation.

The `did` and `public_key_multibase` recorded in the wallet record are
`did:key`'s own encoding of that same public half: `z` + base58btc of the
ed25519 multicodec prefix and the 32 raw bytes.

- `did`: `{did}`
- `public_key_multibase`: `{public_key_multibase}`

## Where the private half is, and where it is not

The private half is a 32-byte Ed25519 seed, held ONLY as an encrypted GitHub
Actions secret in the `{environment}` environment of `{target_repo}`, under the
name `{secret_name}`. It was provisioned at **{instant}**, which is the instant
recorded as `verified_at` on the custody attestation.

There is no suffix because there is exactly one origin identity. There is no
second copy: not on a governed execution host, not on a workstation, not on a
shared runner, not in any bundle, not in a vault.

**No private half was written to any git working tree, appeared in any log, or
left the minting process.** The mint was performed by
`openxFactory scripts/mint-factory-origin-key.py`, which generates the seed with
`secrets.token_bytes(32)` in its own process, writes it to
`gh secret set` on the child's STDIN — never as an argv element, never as an
environment variable, never as a temporary file — confirms the name now exists
in that environment, and then overwrites and deletes the variable. Its command log records argv and the LENGTH of anything
written to a child's stdin, never the bytes. The seed was never printed.

**The encoding is 64 lowercase hex characters of the raw seed**, matching the
seat keys, because its length alone disambiguates it from a base64url public
half — the property that makes a mis-set secret fail by name.

## How the encoding was proven, not assumed

The three public values were not computed by the mint program. It called
`scripts/validate-factory-identity.py`'s own `derive` entry point IN-PROCESS and
read back what that reader printed — and that reader refuses to run at all
unless the PINNED openXwallet decoders
(`openXwallet/scripts/validate-openxwallet.py`, gitlink `{pinned_gitlink}`) are
importable, then round-trips every value through them before printing: the
multibase it encoded decoded back to the same 32 bytes under
`decode_public_key_multibase`, both pinned fingerprint spellings agreed, the
base64url spelling re-encoded to itself, and the fingerprint recomputed from the
raw bytes. So the encodings in the register are, by construction, the encodings
the REQUIRED `wallet-validation` check judges them by.

Then all four gates ran against the filled tree BEFORE either commit:

| Gate | Result |
| --- | --- |
| `python3 scripts/verify-openxwallet-pin.py` | clean |
| `python3 openXwallet/scripts/validate-openxwallet.py .` (as `wallet-validation` runs it) | clean |
| `python3 scripts/validate-factory-identity.py .` | 0 errors, disjointness `0 shared` |
| `python3 -m pytest tests/factory_identity -q` | green |

The mint program refuses to commit anything it has not verified, and a failure
leaves the tree modified and uncommitted for inspection.

## What this pairs with

- openxFactory `{register_branch}` — the filled register family
  (PR #{register_pr}), commit `{openx_commit}`.
- codexFactory `{floor_branch}` — the never-clearable floor entry
  (PR #{floor_pr}), which this record accompanies.

## What this does NOT discharge

1. this record (done) — the mint, the public half, the custody attestation;
2. the `digest_subject` tranche widening
   (`contracts/signed-execution-chain/digest-construction.schema.yaml`): the
   enumeration is CLOSED at seventeen members and none of them is a request,
   return or bundle manifest, so an origin signature over the manifest has no
   admitted subject yet and the requirement reports UNREALIZABLE rather than
   satisfied (tasks 2.9);
3. the register PROJECTION path to the clearing workflow — OQ1 names four
   shapes and chooses none. Until one is settled, revocation propagates no
   faster than the view a consumer holds, and the register's declared
   `revocation_staleness_bound` (P7D) is the honest ceiling on that lag.
   **Origin revocation at the moment of clearing is NOT in force and must not
   be claimed** (tasks 3.5);
4. the openXwallet reader scoping (tasks 5.1/5.2) — until it lands, the
   read-time refusal of an origin key presented for a review act is NOT in
   force, and the checked disjointness rule is the whole of the enforcement;
5. the hosted packaging workflow that actually signs with this key
   (tasks 4.1-4.3).
"""


def write_record(runner, plan: Plan, values: dict[str, str],
                 instant: str) -> Path:
    code, out = _git(runner, plan.openx_root, "rev-parse", "HEAD")
    openx_commit = out.strip() if code == 0 else "<unknown>"
    code, out = _git(runner, plan.openx_root, "rev-parse", "HEAD:openXwallet")
    pinned_gitlink = out.strip() if code == 0 else "<unknown>"
    plan.record_path.parent.mkdir(parents=True, exist_ok=True)
    plan.record_path.write_text(
        RECORD_TEMPLATE.format(
            today=plan.today.isoformat(), instant=instant,
            public_key=values["public_key"],
            key_fingerprint=values["key_fingerprint"],
            did=values["did"],
            public_key_multibase=values["public_key_multibase"],
            secret_name=SECRET_NAME, environment=ENVIRONMENT,
            target_repo=TARGET_REPO, register_pr=plan.register_pr,
            floor_pr=plan.floor_pr, register_branch=REGISTER_BRANCH,
            floor_branch=FLOOR_BRANCH, openx_commit=openx_commit,
            pinned_gitlink=pinned_gitlink),
        encoding="utf-8")
    return plan.record_path


# --------------------------------------------------------------- landing

def land(runner, plan: Plan, written: list[Path], instant: str) -> None:
    """Two pathspec commits, two pushes, two `pr ready`. NO MERGE.

    PATHSPEC COMMITS, not `git add -A` and not a bare `git commit`. These
    checkouts are shared with other sessions, staged state lingers in the index
    mid-operation, and a bare commit takes whatever ANY session has staged.
    Every commit here names its files.
    """
    register_paths = [str(p.relative_to(plan.openx_root)) for p in written]
    code, out = _git(runner, plan.openx_root, "commit", "-m",
                     REGISTER_COMMIT_SUBJECT.format(instant=instant),
                     "-m", _register_commit_body(plan, instant),
                     "--", *register_paths)
    if code != 0:
        raise Refusal("commit-failed",
                      f"the register commit failed (exit {code}): {out}")
    print(f"  committed {len(register_paths)} file(s) in {plan.openx_root}")

    record_rel = str(plan.record_path.relative_to(plan.codex_root))
    code, out = _git(runner, plan.codex_root, "add", "--", record_rel)
    if code != 0:
        raise Refusal("record-add-failed",
                      f"cannot stage {record_rel} (exit {code}): {out}")
    code, out = _git(runner, plan.codex_root, "commit", "-m",
                     FLOOR_COMMIT_SUBJECT, "-m",
                     _record_commit_body(plan, instant),
                     "--", record_rel)
    if code != 0:
        raise Refusal("commit-failed",
                      f"the record commit failed (exit {code}): {out}")
    print(f"  committed {record_rel} in {plan.codex_root}")

    for root, branch in ((plan.openx_root, REGISTER_BRANCH),
                         (plan.codex_root, FLOOR_BRANCH)):
        code, out = _git(runner, root, "push", "origin",
                         f"HEAD:refs/heads/{branch}")
        if code != 0:
            raise Refusal(
                "push-failed",
                f"pushing {branch} failed (exit {code}): {out}\nBoth commits "
                f"exist locally. Pushes race in this estate — `git pull "
                f"--rebase` and push again by hand; do NOT re-run this "
                f"program.")
        print(f"  pushed {branch}")

    for repo, number in ((REGISTER_REPO, plan.register_pr),
                         (TARGET_REPO, plan.floor_pr)):
        code, out = runner.run(["gh", "pr", "ready", str(number),
                                "--repo", repo])
        if code != 0:
            raise Refusal("pr-ready-failed",
                          f"`gh pr ready {number}` on {repo} failed "
                          f"(exit {code}): {out}")
        print(f"  {repo}#{number} is out of draft")


def _register_commit_body(plan: Plan, instant: str) -> str:
    lines = [
        f"The operator minted the ONE Ed25519 origin identity of {TARGET_REPO}",
        f"and provisioned its private half at {instant}. The five",
        "FILL-IN-AT-MINT sentinels are replaced by the public values the",
        "register reader's own derive path produced through the PINNED",
        "openXwallet decoders; nothing here was computed by a second",
        "implementation.",
        "",
        "The private half exists only as an encrypted environment secret in",
        f"{TARGET_REPO}'s own hosted {ENVIRONMENT} environment. It entered no",
        "git working tree, no log and no argv.",
    ]
    if plan.restamp is not None:
        lines += [
            "",
            f"The grant is re-stamped to issued_at {plan.restamp[0]} and",
            f"expires_at {plan.restamp[1]} because the mint happened after the",
            "drafted issuance date; the backing row's expires_at is",
            "character-for-character equal, which the reader compares.",
        ]
    lines += [
        "",
        "All four gates ran clean against this tree before this commit: the",
        "openXwallet pin, the PINNED validator as wallet-validation runs it,",
        "the factory-identity register reader (0 errors, 0 shared), and",
        "tests/factory_identity.",
    ]
    return "\n".join(lines)


def _record_commit_body(plan: Plan, instant: str) -> str:
    return "\n".join([
        f"Pairs with openxFactory {REGISTER_BRANCH} "
        f"(PR #{plan.register_pr}), where the register family is filled.",
        "",
        f"The record names the public half, the {SECRET_NAME} secret and its",
        f"{ENVIRONMENT} environment, the provisioning instant {instant}, and",
        "the four gates that ran before either commit. The private half is not",
        "in it, has no second copy, and never left the minting process.",
    ])


def merge_commands(runner, plan: Plan) -> list[str]:
    out_lines = []
    for repo, number in ((REGISTER_REPO, plan.register_pr),
                         (TARGET_REPO, plan.floor_pr)):
        method = "merge"
        code, out = runner.run(["gh", "api", f"repos/{repo}", "--jq",
                                "[.allow_squash_merge, .allow_merge_commit, "
                                ".allow_rebase_merge] | @tsv"])
        if code == 0:
            allowed = dict(zip(MERGE_METHOD_PREFERENCE, out.strip().split()))
            for candidate in MERGE_METHOD_PREFERENCE:
                if allowed.get(candidate) == "true":
                    method = candidate
                    break
        out_lines.append(f"gh pr merge {number} --{method} --repo {repo}")
    return out_lines


# --------------------------------------------------------------- reporting

def print_plan(plan: Plan, *, dry_run: bool) -> None:
    print()
    print("PLAN" if dry_run else "PREFLIGHT")
    for check in plan.checks:
        print(f"  ok [{check.name}] {check.detail}")
    verb = "would" if dry_run else "will "
    print()
    print(f"  {verb} generate a 32-byte Ed25519 seed with "
          f"`secrets.token_bytes(32)`")
    print(f"  {verb} store it as {SECRET_NAME} in "
          f"{TARGET_REPO} / {ENVIRONMENT} via `gh secret set` on stdin, then "
          f"confirm the name appears")
    print(f"  {verb} fill {EXPECTED_SENTINEL_TOTAL} "
          f"sentinel(s): {len(WALLET_FIELDS)} in {WALLET_REL}, "
          f"{len(ATTESTATION_FIELDS)} in {ATTESTATION_REL}")
    if plan.restamp:
        print(f"  {verb} re-stamp the grant to "
              f"issued_at {plan.restamp[0]} / expires_at {plan.restamp[1]} and "
              f"the row's expires_at to match character for character")
    else:
        print(f"  {verb} leave the expiries as "
              f"drafted (no re-stamp due)")
    for label, argv in verification_commands(plan.openx_root):
        printable = " ".join(["python3"] + [str(a) for a in argv[1:]])
        print(f"  {verb} verify — {printable}")
    print(f"  {verb} write "
          f"{plan.record_path.relative_to(plan.codex_root)} in "
          f"{plan.codex_root}")
    print(f"  {verb} commit (pathspec) and push "
          f"{REGISTER_BRANCH} and {FLOOR_BRANCH}")
    print(f"  {verb} `gh pr ready` "
          f"{REGISTER_REPO}#{plan.register_pr} and "
          f"{TARGET_REPO}#{plan.floor_pr}")
    print("  will NOT merge either pull request — "
          "governance/factory-identity/ is a permanently human-only surface")


# --------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mint-factory-origin-key.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Mint the ONE Ed25519 origin key an originating repository holds, "
            "and land its public half — as one program instead of the mint "
            "runbook's manual checklist."),
        epilog="""\
WHAT IT DOES, in order, and every step fails closed.

PREFLIGHT (all read-only; a refusal here spends nothing)
  gh-auth              `gh auth status` succeeds
  environment          repos/{repo}/environments/{env} resolves
  openxwallet-gitlink  the PINNED openXwallet decoders are importable — the
                       register reader exits 2 without them, so a mint
                       performed now would produce values no gate could judge
  *-clean              BOTH worktrees are clean and on their expected branches
                       (openxFactory {register_branch}; codexFactory
                       {floor_branch})
  mint-sentinels       all five FILL-IN-AT-MINT sentinels are still present,
                       3 in the wallet and 2 in the attestation. A filled
                       register means the mint already happened: ONE origin
                       identity per repository is ratified, and the answer to a
                       rotation is a NEW row whose `supersedes:` names the old
                       one, never a re-fill
  secret-absent        {secret} does NOT already exist in that environment.
                       Overwriting it would orphan every signature made under it
  mint-record-absent   today's mint record does not already exist
  expiry               the grant and its backing row already agree

MINT
  generates the 32-byte seed with `secrets.token_bytes(32)`, derives the public
  half, and obtains `did` / `key_fingerprint` / `public_key_multibase` by
  CALLING the register reader's own `derive` entry point in-process — never a
  second implementation of base58btc or of the fingerprint spelling

CUSTODY, minimal exposure
  writes the seed to `gh secret set` on the child's STDIN — never argv, never
  a temp file, never an environment variable; the stdin path is reached by
  OMITTING `--body`, because that flag takes no magic dash and `--body -`
  would store the string "-" — then CONFIRMS the name now exists, records the
  RFC3339 provisioning instant, and overwrites and deletes the variable. The
  seed is never printed, logged or written to disk. If the store fails or
  cannot be confirmed, the program aborts BEFORE any register edit

FILL
  replaces the five sentinels with the derived public values and the
  provisioning instant, by targeted single-occurrence replacement that REFUSES
  if a sentinel is missing or found twice. If today is later than the grant's
  drafted `issued_at`, re-stamps `issued_at` to today and `expires_at` to
  today + 90 days, and makes the backing row's `expires_at`
  character-for-character equal

VERIFY, all four, exactly as CI runs them
  verify-openxwallet-pin.py; the PINNED validator as `wallet-validation` runs
  it; the register reader (0 errors AND a disjointness note ending `0 shared`,
  because a green run that adjudicated nothing is a vacuous pass); and
  tests/factory_identity. ANY failure leaves the tree MODIFIED AND UNCOMMITTED
  for inspection and exits 1

RECORD, LAND, and STOP
  writes the runbook's mint record into the codexFactory worktree, commits both
  worktrees with explicit pathspecs, pushes both, and moves both pull requests
  out of draft. It does NOT merge — the two merge commands are printed for you

IDEMPOTENCE
  a second run refuses at preflight with a named reason:
  `secret-already-exists` or `register-already-minted`.

ALWAYS RUN --dry-run FIRST. It performs every preflight check above, including
the two read-only GitHub ones, and prints the plan — then stops without
generating a seed, writing a file, committing or pushing.
""".format(repo=TARGET_REPO, env=ENVIRONMENT, secret=SECRET_NAME,
           register_branch=REGISTER_BRANCH, floor_branch=FLOOR_BRANCH))
    parser.add_argument(
        "--dry-run", action="store_true",
        help="run every preflight check and print the plan; generate no seed, "
             "store nothing, write nothing, commit nothing, push nothing")
    parser.add_argument(
        "--codex-worktree", metavar="PATH",
        help=f"the codexFactory checkout on {FLOOR_BRANCH}, where the mint "
             f"record lands. REQUIRED: it is a different repository and this "
             f"program will not guess at a path outside its own tree")
    parser.add_argument(
        "--openxfactory-root", metavar="PATH", default=str(SCRIPT_ROOT),
        help="the openxFactory checkout carrying the register family "
             "(default: this script's own repository root)")
    parser.add_argument(
        "--today", metavar="YYYY-MM-DD", type=date.fromisoformat,
        help="the date the expiry re-stamp is computed from (default: today "
             "UTC). Present so the re-stamp arithmetic is testable, not so a "
             "mint can be back-dated")
    parser.add_argument("--register-pr", metavar="N", type=int,
                        help=f"the {REGISTER_REPO} pull request to ready "
                             f"(default: the one open on {REGISTER_BRANCH})")
    parser.add_argument("--floor-pr", metavar="N", type=int,
                        help=f"the {TARGET_REPO} pull request to ready "
                             f"(default: the one open on {FLOOR_BRANCH})")
    return parser


def run_mint(args, runner) -> int:
    openx_root = Path(args.openxfactory_root).resolve()
    if args.codex_worktree is None:
        print("refused [codex-worktree-unset] --codex-worktree is REQUIRED: "
              "the mint record lands in the codexFactory checkout on "
              f"{FLOOR_BRANCH}, which is a different repository, and this "
              "program will not guess at a path outside its own tree.",
              file=sys.stderr)
        return 2
    codex_root = Path(args.codex_worktree).resolve()

    validator = load_validator(openx_root)
    sentinel = getattr(validator, "SENTINEL", SENTINEL_FALLBACK)

    plan = preflight(runner, validator, args, openx_root, codex_root)
    print_plan(plan, dry_run=args.dry_run)
    if args.dry_run:
        print()
        print("DRY RUN — nothing was generated, stored, written, committed or "
              "pushed. Re-run without --dry-run to perform the mint.")
        return 0

    print()
    print("MINT")
    seed = secrets.token_bytes(32)
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey)
        public_raw = Ed25519PrivateKey.from_private_bytes(seed).public_key(
        ).public_bytes(encoding=serialization.Encoding.Raw,
                       format=serialization.PublicFormat.Raw)
        seed_hex = seed.hex()
    finally:
        seed = b"\x00" * 32
        del seed
    public_b64u = base64.urlsafe_b64encode(public_raw).decode("ascii").rstrip("=")
    values = derive_public_values(validator, plan.pinned, public_b64u)
    print("  seed generated; the public half is derived and round-tripped "
          "through the PINNED decoders")

    try:
        instant = store_private_half(runner, seed_hex)
    finally:
        seed_hex = "0" * 64
        del seed_hex
    print(f"  {SECRET_NAME} stored in {TARGET_REPO} / {ENVIRONMENT} at "
          f"{instant}")
    print("  the seed is overwritten and deleted; it was never printed, "
          "logged, or written to disk")

    print()
    print("FILL")
    written = fill_register(plan, values, instant, sentinel=sentinel)
    for path in written:
        print(f"  wrote {path.relative_to(plan.openx_root)}")

    print()
    print("VERIFY")
    verify(runner, plan)

    print()
    print("RECORD")
    record = write_record(runner, plan, values, instant)
    print(f"  wrote {record.relative_to(plan.codex_root)}")

    print()
    print("LAND")
    land(runner, plan, written, instant)

    print()
    print("=" * 72)
    print("THE MINT IS COMPLETE. The public values, which are safe to publish:")
    print(f"  did:                  {values['did']}")
    print(f"  key_fingerprint:      {values['key_fingerprint']}")
    print(f"  public_key_multibase: {values['public_key_multibase']}")
    print(f"  public_key (base64url, for the record's table): "
          f"{values['public_key']}")
    print(f"  provisioned at:       {instant}")
    print()
    print("The private half is in exactly one place and there is no backup: "
          f"{SECRET_NAME}")
    print(f"in {TARGET_REPO} / {ENVIRONMENT}. If it is lost, the recovery is a "
          "FRESH MINT that")
    print("SUPERSEDES this row — never a second copy of this one.")
    print()
    print("BOTH PULL REQUESTS ARE OUT OF DRAFT AND NEITHER IS MERGED. "
          "governance/factory-identity/")
    print("is a permanently human-only surface. Merge them yourself, register "
          "first:")
    print()
    for command in merge_commands(runner, plan):
        print(f"  {command}")
    print()
    return 0


def main(argv: list[str] | None = None, runner=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run_mint(args, runner if runner is not None else SubprocessRunner())
    except Refusal as refusal:
        print(f"\nrefused [{refusal.code}] {refusal}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
