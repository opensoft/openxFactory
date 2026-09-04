#!/usr/bin/env python3
"""The FACTORY-IDENTITY register reader, and the CHECKED DISJOINTNESS RULE.

Realization of the ratified change `add-cpc-clearing-boundary` (capability
`factory-origin-identity`), tasks 2.5 and 2.6. It ships WITH the register, not
after it: a register nothing reads confers nothing, and the ratified
requirement's enforceable half IS this file.

WHAT IT ENFORCES, and why each rule is here rather than somewhere else.

(a) THE REGISTER IS THE SHAPE. `governance/factory-identity/register.yaml` is
    deliberately kindless (design D3), so no JSON Schema closes it. This reader
    closes it instead — the top level and every row are compared as EXACT SETS,
    the way the pinned intake reader closes its own register — because a
    governed declaration nobody reads passes silently, which is the vacuous-pass
    class this estate has already been bitten by twice.

(b) NO SEAT SPELLING (ratified scenario, design D2). An originating repository
    is an ORGANISATION holder. A `seat_keys` block, an `agent:` holder prefix or
    a per-seat key shape in this family is a MISFILED ROW and is refused by
    name, not left to be inferred from an omission.

(c) ONE ACTIVE ORIGIN ROW PER ORIGINATING REPOSITORY (ratified). Rotation
    supersedes; it never adds a second concurrent row.

(d) PUBLIC KEY REFERENCES ONLY, AND NO SECRET NAME. The ratified requirement is
    stricter than the intake register's practice: this family may not carry "a
    private key, a seed, a passphrase, A SECRET NAME RESOLVABLE TO KEY MATERIAL,
    or any credential value". The secret-name rule is checked over the RAW BYTES
    of every file in the family, comments included, because a comment naming the
    variable is exactly as resolvable as a field naming it.

(e) THE DISJOINTNESS RULE — the ratified requirement's whole enforceable half.
    No `key_id`, no decentralized identifier and no public-key fingerprint may
    appear in BOTH `governance/factory-identity/` and
    `governance/review-authority/`. It is asserted over the RECORDS because that
    is what two trees can prove today. IT IS NOT WAIVABLE by declaring different
    acts on the two rows: the check never reads `act`.

    WHAT THIS RULE IS NOT. A refusal AT READ TIME — an origin-registered key
    presented for a review act being rejected by the review reader — IS NOT IN
    FORCE and must not be claimed. The pinned openXwallet reader indexes every
    wallet and grant record in a scanned tree into ONE context, so a wallet
    record in this sibling tree remains resolvable BY IT as a review row's
    `wallet_ref`. That reader is pinned vocabulary owned outside this
    repository; scoping it is an openXwallet dependency (tasks 5.1/5.2, OQ3).
    Until it lands, this rule is the whole of the enforcement, and the ratified
    spec carries a scenario that REFUSES any document claiming otherwise.

(f) THE PLACEHOLDER REFUSAL. Every value the mint produces is written as the
    literal sentinel `FILL-IN-AT-MINT` until an operator mints the key. This
    reader refuses the tree while any sentinel stands, with a named finding, so
    the register CANNOT MERGE holding a placeholder — and so that nobody is
    tempted to invent a plausible 43-character base64url literal that would pass
    a scanner and a reader alike. A value that looks like a key is worse than no
    value, because it merges.

(g) THE UNATTESTED CAP (ratified). An origin key whose custody is undeclared or
    unattested caps at the authority the custody vocabulary assigns to unattested
    custody — `request` — and is NOT evidence that the originating repository
    itself acted. A grant declaring more than that with no completed attestation
    beside it is refused.

ONE DERIVATION, ONE PLACE. Every public-key decoding and every fingerprint in
this file comes from the PINNED openXwallet reader
(`openXwallet/scripts/validate-openxwallet.py`), imported rather than copied:
`decode_public_key_multibase` (base58btc + ed25519 multicodec, the `did:key`
encoding), `_decode_public_key` (canonical unpadded base64url) and
`fingerprint_of_public_key` / `_fingerprint_of` (the one fingerprint spelling
the mint record, the intake register reader and hermes-install all compute). A
SECOND IMPLEMENTATION IS THE DEFECT: two spellings of one key are two keys to
anything comparing strings. If the pinned reader cannot be imported this program
REFUSES (exit 2) rather than falling back to arithmetic of its own — a fallback
would be that second implementation, arriving exactly when nobody is looking.

USAGE
    python3 scripts/validate-factory-identity.py .
    python3 scripts/validate-factory-identity.py --derive <public-key-base64url>

`--derive` is the MINT HELPER the runbook drives
(`docs/factory-origin-key-mint-runbook.md`). It takes the PUBLIC half only —
never a seed, never a private key — and emits the three register values,
round-tripping each one back through the pinned decoders before printing, so the
encoder in this file cannot disagree with the reader that will judge it.

EXIT CODES
    0  clean
    1  findings
    2  the reader could not run at all (no target, no pinned reader, bad usage)
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a finding
    print("validate-factory-identity: PyYAML is required", file=sys.stderr)
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
PINNED_READER = REPO_ROOT / "openXwallet" / "scripts" / "validate-openxwallet.py"

FAMILY_DIR_PARTS = ("governance", "factory-identity")
REVIEW_DIR_PARTS = ("governance", "review-authority")
REGISTER_FILE = "register.yaml"
WALLETS_DIR = "wallets"
GRANTS_DIR = "grants"
ATTESTATIONS_DIR = "attestations"

#: The literal the mint replaces. One spelling, so it is greppable and so a
#: half-completed mint is as loud as an untouched one.
SENTINEL = "FILL-IN-AT-MINT"

#: The register's top level, closed. Adding a governed declaration here without
#: teaching this reader about it is the vacuous pass the intake register already
#: suffered once (its `revocation_staleness_bound` went unread inside a REQUIRED
#: check), so closure is the reader's job or it is nobody's.
REGISTER_TOP_LEVEL_REQUIRED = {
    "register_version", "revocation_staleness_bound",
    "revocation_staleness_ceiling", "rows",
}
REGISTER_TOP_LEVEL_FIELDS = set(REGISTER_TOP_LEVEL_REQUIRED)

#: The SIX facts the ratified row enumeration names, plus `row_id`, which is the
#: row's own NAME rather than a seventh fact — the ratified revocation scenario
#: requires a resuming row to NAME the row it supersedes, and a row with no name
#: cannot be named.
ROW_REQUIRED_FIELDS = {
    "row_id", "holder_ref", "wallet_ref", "act", "grant_ref", "expires_at",
    "state",
}
#: Legal ONLY on a row that replaces another.
ROW_OPTIONAL_FIELDS = {"supersedes"}

#: THE FIELD THAT IS NOT HERE. There is no `authority_tier` column: the
#: authority a key may carry is a property of the GRANT and of the custody
#: attestation, and a register column restating it is two places for one fact to
#: disagree (task 2.1).
ROW_REFUSED_FIELDS = {"authority_tier", "public_key", "key_id", "seat_id"}

#: Refused at the register's top level by name rather than only by set closure,
#: so the finding says WHY (design D2) instead of "unknown key".
SEAT_SPELLING_TOP_LEVEL = {"seat_keys", "seats", "council_ref", "council_id"}
SEAT_HOLDER_PREFIX = "agent:"

ROW_STATES = {"active", "superseded", "revoked", "expired"}
REQUIRED_HOLDER_CLASS = "organisation"

#: Weeks/days/hours/minutes/seconds only. Years and months are refused for the
#: reason the intake register records: a trust window whose width depends on the
#: calendar is not a bound anybody declared.
STALENESS_RE = re.compile(
    r"^P(?!$)(\d+W)?(\d+D)?(T(?!$)(\d+H)?(\d+M)?(\d+S)?)?$")

#: The ceiling this realization adopts for an origin grant, in days. An origin
#: key lives in a hosted CI environment, and this estate has no projection path
#: that could revoke it at the moment of clearing, so a short unconditional
#: expiry is the only propagation mechanism that works today.
MAX_GRANT_DAYS = 90

#: The authority the custody vocabulary assigns to UNATTESTED custody. A grant
#: reaching past it needs a completed attestation beside it.
UNATTESTED_TIER = "request"
TIER_RANK = {"attest": 0, "request": 1, "act": 2, "act_unsupervised": 3}

#: An environment-variable-shaped token that names key material. Checked over
#: RAW BYTES, comments included: the ratified requirement forbids "a secret name
#: resolvable to key material" in this family, and a comment naming the variable
#: is exactly as resolvable as a field naming it.
SECRET_NAME_RE = re.compile(
    r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
SECRET_NAME_TOKENS = ("KEY", "SECRET", "TOKEN", "PASSPHRASE", "SEED",
                      "CREDENTIAL", "PRIVATE")

#: Armored private keys and bare 32-byte seeds. The seed form matters here more
#: than in a wallet record: an ed25519 private half IS 64 hex characters, and it
#: is the single most likely thing to be pasted where a public half belongs.
PRIVATE_BLOCK_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----", re.I)
SEED_HEX_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")

ED25519_MULTICODEC = b"\xed\x01"
_B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


# --------------------------------------------------------------- the pinned reader

def load_pinned_reader(path: Path = PINNED_READER):
    """Import the PINNED openXwallet reader, or refuse.

    There is no fallback ON PURPOSE. A local reimplementation of base58btc or of
    the fingerprint spelling would be the second implementation this file exists
    to prevent, and it would arrive silently on the one run where the gitlink
    was not initialized — which is precisely the run nobody inspects.
    """
    if not path.is_file():
        raise SystemExit(
            f"validate-factory-identity: the pinned openXwallet reader is not "
            f"at {path}. Run `git submodule update --init openXwallet`. This "
            f"program REFUSES rather than deriving keys with arithmetic of its "
            f"own: one derivation, one place.")
    spec = importlib.util.spec_from_file_location(
        "_pinned_openxwallet_reader", path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise SystemExit(f"validate-factory-identity: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("decode_public_key_multibase", "fingerprint_of_public_key",
                 "_decode_public_key", "_fingerprint_of",
                 "PUBLIC_KEY_B64U_LEN"):
        if not hasattr(module, name):
            raise SystemExit(
                f"validate-factory-identity: the pinned reader at {path} has no "
                f"{name!r}; the pin predates the derivation path this reader "
                f"reuses, and inventing a local one is refused")
    return module


def b58encode(raw: bytes) -> str:
    """base58btc. THE ONLY ENCODER IN THIS FILE, and it is never trusted on its
    own: every value it produces is fed straight back through the PINNED
    decoder before it is printed or compared, so an encoder that disagreed with
    the reader would refuse rather than publish."""
    number = int.from_bytes(raw, "big")
    out = ""
    while number:
        number, rest = divmod(number, 58)
        out = _B58_ALPHABET[rest] + out
    leading = 0
    for byte in raw:
        if byte:
            break
        leading += 1
    return _B58_ALPHABET[0] * leading + out


# --------------------------------------------------------------- findings

class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"error [{code}] {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(f"note  {msg}")


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _mapping(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _sequence(value: Any) -> list:
    return value if isinstance(value, list) else []


def _walk_strings(node: Any, path: str = ""):
    """Every STRING VALUE in a document, with its dotted path.

    VALUES ONLY. An earlier draft also yielded each property NAME, which made
    the disjointness rule report `did`, `key_id` and `key_fingerprint` as
    identifiers shared between the two families — a spectacular false positive
    that would have been indistinguishable from the real finding on the day a
    real one fired. A rule whose alarm is always ringing is a rule nobody reads.
    """
    if isinstance(node, dict):
        for name, value in node.items():
            here = f"{path}.{name}" if path else str(name)
            yield from _walk_strings(value, here)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _walk_strings(item, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


# --------------------------------------------------------------- the family

def family_files(root: Path) -> list[Path]:
    base = root.joinpath(*FAMILY_DIR_PARTS)
    if not base.is_dir():
        return []
    return sorted(p for p in base.rglob("*") if p.is_file())


def review_files(root: Path) -> list[Path]:
    base = root.joinpath(*REVIEW_DIR_PARTS)
    if not base.is_dir():
        return []
    return sorted(p for p in base.rglob("*.yaml") if p.is_file())


def check_no_key_material_or_secret_names(f: Findings, root: Path,
                                          paths: list[Path]) -> None:
    """Rule (d), over RAW BYTES. Comments included, deliberately."""
    for path in paths:
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:  # pragma: no cover
            continue
        if PRIVATE_BLOCK_RE.search(text):
            f.error("factory-identity-key-material",
                    f"{rel}: an armored PRIVATE KEY block appears in the "
                    f"factory-identity family; this family holds key REFERENCES "
                    f"only and possession of a record must confer no ability to "
                    f"sign")
        for hexrun in SEED_HEX_RE.findall(text):
            if hexrun.lower() == hexrun and "sha256:" + hexrun in text:
                continue  # a fingerprint, which is a reference and not a key
            f.error("factory-identity-key-material",
                    f"{rel}: a bare 64-character hex run appears outside a "
                    f"`sha256:` fingerprint; an ed25519 PRIVATE half is exactly "
                    f"64 hex characters, and this family may carry none")
        for token in set(SECRET_NAME_RE.findall(text)):
            if any(word in token for word in SECRET_NAME_TOKENS):
                f.error("factory-identity-secret-name-recorded",
                        f"{rel}: the environment-variable-shaped token {token!r} "
                        f"names key material. The ratified requirement forbids "
                        f"'a secret name resolvable to key material' anywhere in "
                        f"this family — record it once in "
                        f"docs/factory-origin-key-mint-runbook.md instead")


def check_placeholders(f: Findings, root: Path, paths: list[Path]) -> None:
    """Rule (f). Named, so the refusal reads as a step not yet taken rather than
    as a defect, and so `grep -rn FILL-IN-AT-MINT` finds every one of them."""
    for path in paths:
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:  # pragma: no cover
            continue
        hits = [n for n, line in enumerate(text.splitlines(), 1)
                if SENTINEL in line and not line.lstrip().startswith("#")]
        for line_no in hits:
            f.error("factory-identity-placeholder-unminted",
                    f"{rel}:{line_no}: the value is the mint sentinel "
                    f"{SENTINEL!r}. The per-factory origin key has NOT been "
                    f"minted, so this register confers nothing and MUST NOT "
                    f"merge. Perform the mint "
                    f"(docs/factory-origin-key-mint-runbook.md), paste the real "
                    f"public values, and re-run this reader. Do NOT substitute a "
                    f"plausible literal to make this pass: a value that looks "
                    f"like a key is worse than no value, because it merges")


def check_register(f: Findings, root: Path, pinned) -> dict:
    """Rules (a) (b) (c), plus the wallet/grant joins. Returns the parsed
    register (empty on refusal) so the caller can index it for rule (e)."""
    reg_path = root.joinpath(*FAMILY_DIR_PARTS, REGISTER_FILE)
    rel = reg_path.relative_to(root)
    if not reg_path.is_file():
        f.error("factory-identity-register-missing",
                f"{rel}: no factory-identity register at this tree. An origin "
                f"signature would be verified against nothing")
        return {}
    try:
        reg = load_yaml(reg_path)
    except yaml.YAMLError as exc:
        f.error("factory-identity-register-malformed", f"{rel}: {exc}")
        return {}
    if not isinstance(reg, dict):
        f.error("factory-identity-register-malformed",
                f"{rel}: the register is not a mapping")
        return {}

    seat = sorted(set(reg) & SEAT_SPELLING_TOP_LEVEL)
    if seat:
        f.error("factory-identity-seat-spelling",
                f"{rel}: the register carries the council-seat spelling "
                f"{seat} at its top level. An originating repository is an "
                f"ORGANISATION holder, not a seated agent; a per-seat key block "
                f"here is a MISFILED ROW (ratified scenario, design D2)")
    unknown = sorted(set(reg) - REGISTER_TOP_LEVEL_FIELDS - set(seat))
    if unknown:
        f.error("factory-identity-register-malformed",
                f"{rel}: unknown top-level field(s) {unknown}; the register is "
                f"deliberately kindless, so THIS READER is its shape and a "
                f"declaration it does not know is a declaration nothing reads")
    missing = sorted(REGISTER_TOP_LEVEL_REQUIRED - set(reg))
    if missing:
        f.error("factory-identity-register-malformed",
                f"{rel}: missing required top-level field(s) {missing}")

    _check_staleness(f, reg, rel)

    wallets = _load_side(root, WALLETS_DIR)
    grants = _load_side(root, GRANTS_DIR)
    attestations = _load_side(root, ATTESTATIONS_DIR)

    rows = _sequence(reg.get("rows"))
    if not rows:
        f.error("factory-identity-register-malformed",
                f"{rel}: the register declares no rows")
    seen_row_ids: set[str] = set()
    active_holders: dict[str, str] = {}
    for index, row in enumerate(rows):
        row = _mapping(row)
        label = f"{rel}: rows[{index}]"
        refused = sorted(set(row) & ROW_REFUSED_FIELDS)
        if refused:
            f.error("factory-identity-row-malformed",
                    f"{label}: carries refused field(s) {refused}. The register "
                    f"names six facts and the row's own name; authority is a "
                    f"property of the GRANT and its custody attestation, and a "
                    f"key belongs in the wallet record, not in a register column")
        extra = sorted(set(row) - ROW_REQUIRED_FIELDS - ROW_OPTIONAL_FIELDS
                       - set(refused))
        if extra:
            f.error("factory-identity-row-malformed",
                    f"{label}: unknown field(s) {extra}")
        absent = sorted(ROW_REQUIRED_FIELDS - set(row))
        if absent:
            f.error("factory-identity-row-malformed",
                    f"{label}: missing field(s) {absent}")
            continue

        row_id = str(row["row_id"])
        holder = str(row["holder_ref"])
        if row_id in seen_row_ids:
            f.error("factory-identity-row-malformed",
                    f"{label}: duplicate row_id {row_id!r}")
        seen_row_ids.add(row_id)

        if holder.startswith(SEAT_HOLDER_PREFIX):
            f.error("factory-identity-seat-spelling",
                    f"{label}: holder_ref {holder!r} carries the seated-agent "
                    f"prefix {SEAT_HOLDER_PREFIX!r}. An originating repository "
                    f"is an ORGANISATION holder; this row is misfiled")

        state = str(row["state"])
        if state not in ROW_STATES:
            f.error("factory-identity-row-malformed",
                    f"{label}: state {state!r} is not one of {sorted(ROW_STATES)}")
        if state == "active":
            # HAS THE MOMENT PASSED? `state` records what a human last wrote;
            # `expires_at` records what time has since done, and the two are not
            # the same fact. Everything else this reader does with an expiry
            # COMPARES it — the row against its grant, character for character —
            # or CAPS the window at MAX_GRANT_DAYS. Neither asks the question a
            # consumer actually needs answered.
            #
            # IT BELONGS HERE, AND AS AN ERROR, on this file's own reasoning:
            # the expiry-window rule below says in as many words that "no
            # projection path can revoke an origin row at clearing ... so a
            # short unconditional expiry is the only propagation mechanism that
            # works today". A propagation mechanism nothing enforces is not a
            # mechanism, and a register still recording `state: active` past
            # that moment is asserting an authority that has lapsed — a stale
            # claim in the bytes, which is exactly what this reader adjudicates.
            #
            # THE CONSEQUENCE IS CHOSEN, NOT OVERLOOKED. This reader runs inside
            # the REQUIRED `wallet-validation` check, which asserts that no
            # `factory-identity-*` code appears at all, so on the day a row
            # lapses that check goes RED for every pull request until the row is
            # superseded or marked revoked. That is the forcing function, and it
            # is affordable precisely because the 90-day ceiling is deliberately
            # short and the remedy is a one-row governed edit. The alternative —
            # inventing a warning tier this family does not have, so the finding
            # could be printed and ignored — would be adding a severity in order
            # to avoid the consequence the rule exists to produce.
            expires_at = _parse_dt(row.get("expires_at"))
            if expires_at is not None and expires_at <= _now():
                f.error("factory-identity-row-expired",
                        f"{label}: the row is recorded `state: active` but its "
                        f"declared expiry {row.get('expires_at')!r} has PASSED. "
                        f"Nothing revokes an origin row at clearing, so this "
                        f"expiry is the only revocation that propagates and it "
                        f"has propagated: the key it points at may no longer "
                        f"evidence that this repository acted. Supersede the "
                        f"row with a new one naming it, or mark it revoked — a "
                        f"revoked row never returns to active")
            if holder in active_holders:
                f.error("factory-identity-second-active-row",
                        f"{label}: a SECOND active origin row for {holder!r} "
                        f"(the first is {active_holders[holder]!r}). Exactly one "
                        f"origin identity per originating repository is ratified; "
                        f"rotation SUPERSEDES a row rather than adding one")
            else:
                active_holders[holder] = row_id
        if "supersedes" in row:
            target = str(row["supersedes"])
            if target not in seen_row_ids and target not in {
                    str(_mapping(r).get("row_id")) for r in rows}:
                f.error("factory-identity-row-malformed",
                        f"{label}: supersedes {target!r}, which is not a row in "
                        f"this register")

        wallet_ref = str(row["wallet_ref"])
        grant_ref = str(row["grant_ref"])
        wallet = wallets.get(wallet_ref)
        grant = grants.get(grant_ref)
        if wallet is None:
            f.error("factory-identity-row-unresolved",
                    f"{label}: wallet_ref {wallet_ref!r} resolves to no record "
                    f"under {'/'.join(FAMILY_DIR_PARTS)}/{WALLETS_DIR}/")
        if grant is None:
            f.error("factory-identity-row-unresolved",
                    f"{label}: grant_ref {grant_ref!r} resolves to no record "
                    f"under {'/'.join(FAMILY_DIR_PARTS)}/{GRANTS_DIR}/")
        if wallet is not None:
            _check_wallet(f, label, wallet_ref, wallet, row, pinned)
        if grant is not None:
            _check_grant(f, label, grant_ref, grant, row, wallet_ref,
                         attestations)

    f.note(f"factory-identity register read: {rel} ({len(rows)} row(s))")
    f.note(f"factory-identity register: {len(active_holders)} active origin "
           f"row(s) over {len(active_holders)} originating repository(ies)")
    return reg


def _check_staleness(f: Findings, reg: dict, rel: Path) -> None:
    bound = reg.get("revocation_staleness_bound")
    ceiling = reg.get("revocation_staleness_ceiling")
    for name, value in (("revocation_staleness_bound", bound),
                        ("revocation_staleness_ceiling", ceiling)):
        if value is None:
            continue
        if not isinstance(value, str) or not STALENESS_RE.match(value):
            f.error("factory-identity-staleness-malformed",
                    f"{rel}: {name} {value!r} is not a weeks/days/hours/"
                    f"minutes/seconds ISO-8601 duration; years and months are "
                    f"refused because a trust window whose width depends on the "
                    f"calendar is not a bound anybody declared")
            continue
        if not any(int(n) for n in re.findall(r"(\d+)", value)):
            f.error("factory-identity-staleness-malformed",
                    f"{rel}: {name} {value!r} names a zero-length window; no "
                    f"view could ever be read inside it, which disables the "
                    f"rule rather than tightening it")
    if isinstance(bound, str) and isinstance(ceiling, str) \
            and STALENESS_RE.match(bound) and STALENESS_RE.match(ceiling):
        if _duration_seconds(bound) > _duration_seconds(ceiling):
            f.error("factory-identity-staleness-exceeds-ceiling",
                    f"{rel}: revocation_staleness_bound {bound!r} is WIDER than "
                    f"the ceiling {ceiling!r} this register declares for itself. "
                    f"An artifact must never be able to widen its own trust "
                    f"window; tighten the bound, or move the ceiling in a "
                    f"governed act with its own record")


def _duration_seconds(value: str) -> int:
    units = {"W": 604800, "D": 86400, "H": 3600, "M": 60, "S": 1}
    total = 0
    for number, unit in re.findall(r"(\d+)([WDHMS])", value):
        total += int(number) * units[unit]
    return total


def _load_side(root: Path, folder: str) -> dict[str, dict]:
    base = root.joinpath(*FAMILY_DIR_PARTS, folder)
    out: dict[str, dict] = {}
    if not base.is_dir():
        return out
    for path in sorted(base.glob("*.yaml")):
        try:
            doc = load_yaml(path)
        except yaml.YAMLError:
            continue
        if not isinstance(doc, dict):
            continue
        key = doc.get("wallet_id") or doc.get("grant_id") \
            or doc.get("attestation_id")
        if isinstance(key, str):
            out[key] = doc
    return out


def _check_wallet(f: Findings, label: str, wallet_ref: str, wallet: dict,
                  row: dict, pinned) -> None:
    holder = _mapping(wallet.get("holder"))
    holder_class = holder.get("holder_class")
    if holder_class != REQUIRED_HOLDER_CLASS:
        f.error("factory-identity-seat-spelling",
                f"{label}: wallet {wallet_ref!r} declares holder_class "
                f"{holder_class!r}; the ratified requirement fixes it at "
                f"{REQUIRED_HOLDER_CLASS!r} — an originating repository is an "
                f"organisation holder, not a seated agent")
    if str(holder.get("holder_id")) != str(row.get("holder_ref")):
        f.error("factory-identity-row-unresolved",
                f"{label}: wallet {wallet_ref!r} is held by "
                f"{holder.get('holder_id')!r}, not by the row's holder_ref "
                f"{row.get('holder_ref')!r}")
    if "keys" in wallet:
        f.error("factory-identity-seat-spelling",
                f"{label}: wallet {wallet_ref!r} declares a `keys:` SET. Exactly "
                f"ONE origin identity per originating repository is ratified; a "
                f"declared key set expresses a plurality the contract refuses")

    ref = _mapping(wallet.get("key_reference"))
    did = ref.get("did")
    multibase = ref.get("public_key_multibase")
    fingerprint = ref.get("key_fingerprint")
    if not isinstance(multibase, str) or SENTINEL in str(multibase):
        return  # the placeholder rule has already named this
    raw = pinned.decode_public_key_multibase(multibase)
    if raw is None:
        f.error("factory-identity-key-encoding",
                f"{label}: wallet {wallet_ref!r} declares public_key_multibase "
                f"{multibase!r}, which does not decode as base58btc carrying the "
                f"ed25519 multicodec prefix and 32 raw bytes")
        return
    expected = pinned.fingerprint_of_public_key(raw)
    if isinstance(fingerprint, str) and fingerprint != expected:
        f.error("factory-identity-fingerprint-mismatch",
                f"{label}: wallet {wallet_ref!r} declares key_fingerprint "
                f"{fingerprint!r}, but its own public half recomputes to "
                f"{expected!r}. A fingerprint and the public half beside it are "
                f"two spellings of one key; a transcription slip is refused here "
                f"rather than recorded")
    if isinstance(did, str) and did != f"did:key:{multibase}":
        f.error("factory-identity-key-encoding",
                f"{label}: wallet {wallet_ref!r} declares did {did!r}, which is "
                f"not `did:key:` + its own public_key_multibase. For an ed25519 "
                f"key the anchor is DERIVED from the public half, never invented")


def _check_grant(f: Findings, label: str, grant_ref: str, grant: dict,
                 row: dict, wallet_ref: str,
                 attestations: dict[str, dict]) -> None:
    audience = _mapping(grant.get("audience"))
    if audience.get("wallet_ref") != wallet_ref:
        f.error("factory-identity-row-unresolved",
                f"{label}: grant {grant_ref!r} is addressed to wallet "
                f"{audience.get('wallet_ref')!r}, not to the row's wallet "
                f"{wallet_ref!r}")
    scope = _mapping(grant.get("scope"))
    acts = _sequence(scope.get("acts"))
    if str(row.get("act")) not in [str(a) for a in acts]:
        f.error("factory-identity-row-unresolved",
                f"{label}: the row's act {row.get('act')!r} is not among the "
                f"grant's acts {acts}; the row would record an authority the "
                f"grant does not confer")
    if grant.get("expires_at") != row.get("expires_at"):
        f.error("factory-identity-expiry-mismatch",
                f"{label}: the row expires at {row.get('expires_at')!r} and its "
                f"grant at {grant.get('expires_at')!r}. The two are compared "
                f"character for character: two expiries for one authority is one "
                f"of them being wrong")
    issued = _parse_dt(grant.get("issued_at"))
    expires = _parse_dt(grant.get("expires_at"))
    if issued is not None and expires is not None:
        days = (expires - issued).total_seconds() / 86400
        if days > MAX_GRANT_DAYS:
            f.error("factory-identity-expiry-window",
                    f"{label}: grant {grant_ref!r} runs {days:.0f} days, past "
                    f"the {MAX_GRANT_DAYS}-day ceiling this realization adopts. "
                    f"No projection path can revoke an origin row at clearing "
                    f"(design D9, OQ1 open), so a short unconditional expiry is "
                    f"the only propagation mechanism that works today")
    tier = str(scope.get("authority_tier"))
    attested = _attestation_for(attestations, wallet_ref)
    if TIER_RANK.get(tier, 99) > TIER_RANK[UNATTESTED_TIER] and not attested:
        f.error("factory-identity-tier-unattested",
                f"{label}: grant {grant_ref!r} declares authority_tier {tier!r} "
                f"with no COMPLETED custody attestation for wallet "
                f"{wallet_ref!r}. An origin key whose custody is undeclared or "
                f"UNATTESTED caps at {UNATTESTED_TIER!r} and is NOT evidence "
                f"that the originating repository itself acted")


def _attestation_for(attestations: dict[str, dict], wallet_ref: str) -> bool:
    for doc in attestations.values():
        if doc.get("subject_wallet_ref") != wallet_ref:
            continue
        values = [value for _, value in _walk_strings(doc)]
        if any(SENTINEL in value for value in values):
            return False
        return True
    return False


def _now():
    """The evaluation instant, in one place so a test can hold it still."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)


def _parse_dt(value: Any):
    from datetime import datetime, timezone
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


# --------------------------------------------------------------- rule (e)

def _identifiers(paths: list[Path], root: Path) -> dict[str, set[str]]:
    """Every `key_id`, decentralized identifier and public-key fingerprint a
    tree records, wherever they sit. The walk is over VALUES and not over a
    field list, because a family that grows a record shape must not quietly grow
    a hole in the disjointness rule."""
    out: dict[str, set[str]] = {}
    for path in paths:
        try:
            doc = load_yaml(path)
        except (yaml.YAMLError, OSError):
            continue
        rel = str(path.relative_to(root))
        for where, value in _walk_strings(doc):
            leaf = where.rsplit(".", 1)[-1].split("[")[0]
            if leaf in ("key_id", "did", "public_key_multibase",
                        "key_fingerprint", "attested_key_fingerprint",
                        "public_key"):
                if SENTINEL in value:
                    continue
                out.setdefault(value, set()).add(f"{rel}:{where}")
    return out


def check_disjointness(f: Findings, root: Path) -> None:
    """THE RATIFIED RULE. Not waivable by declaring different acts on the two
    rows — this check never reads `act`."""
    ours = _identifiers(family_files(root), root)
    theirs = _identifiers(review_files(root), root)
    shared = sorted(set(ours) & set(theirs))
    for value in shared:
        f.error("factory-identity-registers-not-disjoint",
                f"the identifier {value!r} appears in BOTH register families: "
                f"factory-identity at {sorted(ours[value])} and review-authority "
                f"at {sorted(theirs[value])}. The origin act and the review or "
                f"seat act are distinct acts carried by DISTINCT KEYS in "
                f"distinct registers. This condition is NOT waivable by "
                f"declaring different acts on the two rows")
    f.note(f"factory-identity: disjointness holds against "
           f"{'/'.join(REVIEW_DIR_PARTS)}/ "
           f"({len(ours)} identifier(s) here, {len(theirs)} identifier(s) there, "
           f"{len(shared)} shared)")


# --------------------------------------------------------------- derive

def derive(pinned, public_key_b64u: str) -> int:
    """The MINT HELPER. Public half only — never a seed, never a private key."""
    raw = pinned._decode_public_key(public_key_b64u)
    if raw is None:
        print(f"error [derive-input] {public_key_b64u!r} is not a CANONICAL "
              f"unpadded base64url ed25519 public key "
              f"({pinned.PUBLIC_KEY_B64U_LEN} characters, 32 raw bytes, "
              f"re-encoding to itself). Two spellings of one key are two keys.",
              file=sys.stderr)
        return 2
    if len(raw) == 32 and raw == b"\x00" * 32:
        print("error [derive-input] the all-zero key is not a key",
              file=sys.stderr)
        return 2
    multibase = "z" + b58encode(ED25519_MULTICODEC + raw)
    # THE ROUND TRIP. The encoder above is never trusted on its own: the pinned
    # DECODER must return the same 32 bytes, and the pinned fingerprint spelling
    # must agree with itself across both encodings, or nothing is printed.
    back = pinned.decode_public_key_multibase(multibase)
    if back != raw:
        print("error [derive-roundtrip] the multibase this program encoded does "
              "not decode back to the same 32 bytes under the PINNED reader; "
              "refusing to publish a value the gate would reject",
              file=sys.stderr)
        return 2
    fingerprint = pinned.fingerprint_of_public_key(raw)
    if fingerprint != pinned._fingerprint_of(back):
        print("error [derive-roundtrip] the two pinned fingerprint spellings "
              "disagree; refusing", file=sys.stderr)
        return 2
    if base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") \
            != public_key_b64u:
        print("error [derive-roundtrip] base64url round trip failed; refusing",
              file=sys.stderr)
        return 2
    if hashlib.sha256(raw).hexdigest() != fingerprint.split(":", 1)[1]:
        print("error [derive-roundtrip] fingerprint disagreement; refusing",
              file=sys.stderr)
        return 2
    print("# Derived from the PUBLIC half only, through the pinned openXwallet")
    print("# decoders. Paste into governance/factory-identity/wallets/<wallet>.yaml:")
    print(f"  did: \"did:key:{multibase}\"")
    print(f"  key_fingerprint: {fingerprint}")
    print(f"  public_key_multibase: {multibase}")
    print()
    print("# The same key's base64url spelling, for the mint record's table:")
    print(f"  public_key: {public_key_b64u}")
    return 0


# --------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read the factory-identity register and assert that it "
                    "shares no key with the review-authority register.")
    parser.add_argument("path", nargs="?",
                        help="repository root to read (e.g. `.`)")
    parser.add_argument("--derive", metavar="PUBLIC_KEY_BASE64URL",
                        help="mint helper: derive did / fingerprint / multibase "
                             "from a PUBLIC key, verified against the pinned "
                             "decoders")
    args = parser.parse_args(argv)

    pinned = load_pinned_reader()

    if args.derive:
        return derive(pinned, args.derive)
    if args.path is None:
        parser.print_usage(sys.stderr)
        print("validate-factory-identity: a target path is REQUIRED. A run with "
              "no target reads no register, and a green check that opened no "
              "register is a vacuous pass.", file=sys.stderr)
        return 2

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"validate-factory-identity: {root} is not a directory; the "
              f"reader sweeps a tree and refuses a single file target",
              file=sys.stderr)
        return 2

    f = Findings()
    paths = family_files(root)
    check_no_key_material_or_secret_names(f, root, paths)
    check_placeholders(f, root, paths)
    check_register(f, root, pinned)
    check_disjointness(f, root)

    for line in f.notes:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-factory-identity: {len(f.errors)} error(s)")
    return 1 if f.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
