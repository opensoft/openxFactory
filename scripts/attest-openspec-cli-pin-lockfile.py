#!/usr/bin/env python3
"""ATTEST the integrity values the pinned CLI's vendored lockfile records —
task 6.1 of `pin-openspec-cli-dependency-closure`, the gap that packet named
rather than shut.

WHAT WAS OPEN, in the archived packet's own words. `tasks.md` § 6.1 asks for
"an independent attestation of the 79 registry integrity values captured in the
lockfile — a provenance attestation, a mirrored registry, or a second capture
from an independent network path compared against this one", and records that
"NOTHING HAS ATTESTED THEM: the 79 values are still trust-on-first-use, captured
once against the live registry on 2026-09-08 and never compared against a second
source". `design.md` § 6.1 states the same limit precisely: the closure made the
tree "FIXED and AUDITABLE rather than VERIFIED-FROM-FIRST-PRINCIPLES", the CLI's
own entry being corroborated by the pin's `integrity:` while "the other 79 are
corroborated by nothing outside the lockfile itself".

THIS MODULE TAKES THE FIRST OF THE THREE NAMED MECHANISMS — the provenance
attestation — AND CHAINS IT TO THE LOCKFILE IN TWO LINKS, because one link alone
attests the wrong thing and saying so is the point.

  * LINK A, MEASURED HERE. For every entry in the committed lockfile, the
    registry's version document is fetched a SECOND TIME, on a later date, and
    its `dist.integrity` is compared BYTE FOR BYTE against the value the
    lockfile recorded. A disagreement is a refusal, not a note.
  * LINK B, MEASURED BY npm. `npm audit signatures` verifies, for every
    installed package, the registry's ECDSA signature over
    `<name>@<version>:<dist.integrity>` against npm's published signing keys,
    and verifies the Sigstore provenance attestation wherever the publisher
    produced one.

WHY BOTH LINKS ARE NEEDED, and it is a real subtlety rather than belt and
braces. `npm audit signatures` resolves each installed `name@version` through
`pacote.manifest(..., {verifySignatures: true})`, so the integrity value inside
the signed payload is the one the REGISTRY serves at audit time — not the one
this repository committed. Run alone it therefore proves the registry is
internally consistent and says nothing whatever about our lockfile. Link A is
what makes the signature bind OUR bytes: once the registry's served integrity is
known to equal the lockfile's recorded integrity, npm's verified signature over
the served value is a verified signature over the recorded value. Link B alone
would be a proof about somebody else's file; Link A alone would be a second
capture with no cryptography in it. Together they say the thing § 6.1 asked for.

WHAT THIS DOES NOT CLAIM, stated here rather than discovered later.

  1. THE SECOND CAPTURE SHARES THIS ONE'S NETWORK PATH. § 6.1's third mechanism
     asks for a capture "from an independent network path"; this is the same
     path at a later time, so it detects post-hoc mutation of the registry's
     published values and does not by itself exclude an adversary who controlled
     that path on both dates. The cryptographic weight is carried by Link B,
     whose keys and transparency-log entries are not the tarball delivery path,
     rather than by the re-capture.
  2. A REGISTRY SIGNATURE IS NOT A BUILD PROVENANCE. Every package on a registry
     serving signing keys is expected to carry the registry's own signature —
     it attests what npm published, not how it was built. Only the subset
     carrying Sigstore `attestations` (recorded per package below) is attested
     back to a source commit and a builder.
  3. THIS RUN IS A CAPTURE, NOT A GATE. Nothing in CI invokes this module.
     Making the attestation a standing obligation of the pin — re-run at every
     bump, refusing when a value is unattested — would change what
     `contracts/openspec-cli-pin.yaml` declares and what `neutral-product-pin`
     requires of it, and a contract change is an OpenSpec act rather than a
     script's side effect. The pin's declared shortfall paragraph is therefore
     left exactly as ratified; this record is evidence beside it, not an
     amendment to it.

THE LOCKFILE IS VERIFIED BEFORE IT IS ATTESTED. `verify_lockfile` from
`scripts/validate-openspec-cli-pin.py` runs first, so an attestation can never
be produced for a file that disagrees with the pin it belongs to: attesting the
values in an unverified lockfile would put a signature's worth of confidence
behind bytes nothing had checked.

EXITS, on the entrypoint's own convention: 0 attested, 1 a disagreement found,
2 a refusal (a malformed pin, an unverifiable lockfile, an unreachable registry,
a missing npm).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "validate-openspec-cli-pin.py"
DEFAULT_REGISTRY = "https://registry.npmjs.org"
KEYS_PATH = "/-/npm/v1/keys"
TIMEOUT = 60

# The packet whose § 6.1 this module answers, at its ARCHIVED path. Cited in the
# record so a reader lands on the deferral rather than on this file's claim about
# it.
CLOSURE = ("openspec/changes/archive/"
           "2026-09-09-pin-openspec-cli-dependency-closure")


class Refusal(Exception):
    """A question this run cannot answer, raised rather than reported as a pass."""


def checked_registry(raw: str) -> str:
    """The origin to re-capture from, REFUSED unless it is a bare https origin.

    THE SCHEME IS A CHECK AND NOT A PREFERENCE HERE, which is why this refuses
    rather than warns. An attestation is worth exactly what the channel that
    delivered it is worth: values re-captured over plaintext attest nothing a
    network position could not have written, and this tool exists precisely to
    stop trusting a value on the strength of having once received it. § 6.1's
    second named mechanism is a MIRRORED REGISTRY, so the host stays the
    operator's to choose — the scheme does not.

    The flag is narrowed to an ORIGIN for the same reason: a path, a query or
    embedded credentials would send the request somewhere the printed record
    does not name, and a record that misstates where it read from is worse than
    no record. What comes back is rebuilt from the parsed host and port, so
    nothing but a validated origin reaches a request.
    """
    parsed = urlsplit(raw.strip().rstrip("/"))
    if parsed.scheme != "https":
        raise Refusal(f"--registry must be https, not {parsed.scheme or raw!r}: "
                      "an attestation re-captured over plaintext attests "
                      "nothing the channel could not have written")
    if not parsed.hostname:
        raise Refusal(f"--registry names no host: {raw!r}")
    if parsed.path or parsed.query or parsed.fragment or parsed.username:
        raise Refusal("--registry takes a bare origin — no path, query, "
                      f"fragment or credentials: {raw!r}")
    port = f":{parsed.port}" if parsed.port else ""
    return f"https://{parsed.hostname}{port}"


def checked_npm(raw: str) -> str:
    """The npm executable, RESOLVED to an absolute path or refused.

    Resolved rather than passed through so the record's provenance names the
    binary that actually ran, and so a typo refuses with its own cause instead
    of surfacing as a bare `FileNotFoundError` from the first install. `shell`
    is never used and every argument list is a literal, so nothing here is
    parsed by a shell.
    """
    resolved = shutil.which(raw)
    if resolved is None:
        raise Refusal(f"npm executable not found: {raw!r}")
    path = Path(resolved)
    if not path.is_file():
        raise Refusal(f"npm executable is not a file: {path}")
    return str(path.resolve())


def checked_destination(raw: str, default: Path) -> Path:
    """Where the record lands, REFUSED outside this repository.

    A record is a governed artifact of THIS repository — reviewed in its diff
    and indexed in its README — so a destination outside the tree is a record
    nothing reviews. The parent must already exist: creating directories on the
    way to writing a record would invent a home for it rather than land it in
    the one the convention names.
    """
    if not raw:
        return default
    destination = Path(raw).expanduser().resolve()
    root = ROOT.resolve()
    if root != destination and root not in destination.parents:
        raise Refusal(f"--write must land inside {root}, not {destination}")
    if not destination.parent.is_dir():
        raise Refusal(f"--write parent directory does not exist: "
                      f"{destination.parent}")
    return destination


def load_verifier() -> ModuleType:
    """The pin's own entrypoint, imported for its readers.

    IMPORTED AND NOT REIMPLEMENTED. The pin's shape, its lockfile address and
    its staging manifest all have exactly one reader in this repository, and a
    second copy of any of them would be a second declaration that moves
    separately — the defect the pin itself exists to end.
    """
    spec = importlib.util.spec_from_file_location("oscli_pin_verifier", VERIFIER)
    if spec is None or spec.loader is None:            # pragma: no cover
        raise Refusal(f"the pin entrypoint is not importable: {VERIFIER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url, headers={"Accept": "application/json",
                      "User-Agent": "openxfactory-pin-attestation"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    # `HTTPError` is a SUBCLASS of `URLError` and naming both would be a
    # redundant arm, not a second case. `TimeoutError` is not: `urlopen`'s
    # socket timeout surfaces as the builtin.
    except (urllib.error.URLError, TimeoutError) as error:
        raise Refusal(f"{url} could not be read: {error}") from error
    except json.JSONDecodeError as error:
        raise Refusal(f"{url} did not answer with JSON: {error}") from error


def registry_keys(registry: str) -> dict[str, dict]:
    """npm's published signing keys, by keyid.

    Fetched so that a recorded `keyid` can be checked against the set the
    registry actually publishes: a signature by an unpublished key is not a
    signature this attestation may count.
    """
    document = fetch_json(registry.rstrip("/") + KEYS_PATH)
    keys = document.get("keys")
    if not isinstance(keys, list) or not keys:
        raise Refusal(f"{registry}{KEYS_PATH} published no keys")
    return {key["keyid"]: key for key in keys if isinstance(key, dict)
            and "keyid" in key}


def entry_name(path: str) -> str:
    """The package name a lockfile `packages` key addresses.

    The tree is not flat — ten `@inquirer/core` entries sit nested under their
    dependents at versions the hoisted copy does not carry — so the name is the
    segment after the LAST `node_modules/` and never the whole key.
    """
    marker = "node_modules/"
    index = path.rfind(marker)
    if index < 0:
        raise Refusal(f"lockfile entry is not a node_modules path: {path!r}")
    return path[index + len(marker):]


def lockfile_entries(document: dict) -> list[dict]:
    """Every content-addressed entry in the lockfile, in lockfile order.

    The root entry carries no `integrity` — it is this repository's derived
    staging wrapper, not a fetched artifact — and is deliberately absent from
    the attestation rather than silently counted as attested.
    """
    packages = document.get("packages")
    if not isinstance(packages, dict):
        raise Refusal("the lockfile carries no `packages` object")
    entries = []
    for path, entry in packages.items():
        if not path or not isinstance(entry, dict):
            continue
        integrity = entry.get("integrity")
        version = entry.get("version")
        if not integrity or not version:
            continue
        entries.append({"path": path, "name": entry_name(path),
                        "version": version, "integrity": integrity})
    if not entries:
        raise Refusal("the lockfile records no integrity values to attest")
    return entries


def registry_version(registry: str, name: str, version: str) -> dict:
    """The registry's document for one exact version.

    The scope separator is percent-encoded because the registry addresses
    `@scope/name` as `@scope%2fname`; `quote` with no safe characters would also
    escape the `@`, which the registry does not accept.
    """
    escaped = quote(name, safe="@")
    return fetch_json(f"{registry.rstrip('/')}/{escaped}/{quote(version)}")


def recapture(registry: str, entries: list[dict],
              keys: dict[str, dict]) -> tuple[list[dict], list[str]]:
    """LINK A — compare every recorded integrity against a fresh registry read.

    Distinct `name@version` pairs are fetched ONCE and the answer reused for
    every lockfile entry naming that pair, so the ten duplicated `@inquirer/core`
    entries cost one round trip each rather than one per position in the tree.
    """
    seen: dict[tuple[str, str], dict] = {}
    rows: list[dict] = []
    disagreements: list[str] = []
    for entry in entries:
        pair = (entry["name"], entry["version"])
        if pair not in seen:
            document = registry_version(registry, *pair)
            dist = document.get("dist")
            if not isinstance(dist, dict):
                raise Refusal(f"{pair[0]}@{pair[1]} has no `dist` in the registry")
            signatures = dist.get("signatures") or []
            keyids = [s.get("keyid") for s in signatures if isinstance(s, dict)]
            seen[pair] = {
                "served_integrity": dist.get("integrity"),
                "keyids": keyids,
                "unpublished_keyids": [k for k in keyids if k not in keys],
                "attested": bool(dist.get("attestations")),
                "predicate": (dist.get("attestations", {})
                              .get("provenance", {}).get("predicateType")),
            }
        answer = seen[pair]
        row = dict(entry, **answer)
        row["agrees"] = answer["served_integrity"] == entry["integrity"]
        rows.append(row)
        if not row["agrees"]:
            disagreements.append(
                f"{entry['name']}@{entry['version']} at {entry['path']}: "
                f"lockfile records {entry['integrity']} and the registry now "
                f"serves {answer['served_integrity']}")
        elif not answer["keyids"]:
            disagreements.append(
                f"{entry['name']}@{entry['version']}: the registry serves no "
                f"signature over its integrity, so no key attests this value")
        elif answer["unpublished_keyids"]:
            disagreements.append(
                f"{entry['name']}@{entry['version']}: signed by "
                f"{answer['unpublished_keyids']}, which "
                f"{registry}{KEYS_PATH} does not publish")
    return rows, disagreements


def audit_signatures(verifier: ModuleType, lockfile_bytes: bytes, package: str,
                     npm: str) -> dict:
    """LINK B — npm verifies its own signatures over the tree the lockfile locks.

    The tree is built by the CLEAN-INSTALL verb through the committed lockfile,
    with the staging manifest DERIVED from the lockfile's own root entry, which
    is the install `neutral-product-pin` requires of every consumer of this pin.
    An `npm install` here would re-resolve the ranges and audit a tree the
    lockfile does not describe.
    """
    document = verifier.read_lockfile(lockfile_bytes)
    manifest = verifier.staging_manifest(document, package)
    with tempfile.TemporaryDirectory(prefix="openspec-cli-pin-attest-") as scratch:
        staging = Path(scratch)
        (staging / "package.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (staging / "package-lock.json").write_bytes(lockfile_bytes)
        # `npm` is the absolute path `checked_npm` resolved and the rest are
        # literals, passed as an ARGUMENT LIST with no shell: the verbs cannot
        # be rewritten by anything the caller supplies.
        install = subprocess.run(
            [npm, "ci", "--ignore-scripts"], cwd=staging, text=True,
            capture_output=True, check=False, shell=False)
        if install.returncode != 0:
            raise Refusal("`npm ci --ignore-scripts` through the committed "
                          f"lockfile failed:\n{install.stderr.strip()}")
        human = subprocess.run(
            [npm, "audit", "signatures"], cwd=staging, text=True,
            capture_output=True, check=False, shell=False)
        machine = subprocess.run(
            [npm, "audit", "signatures", "--json"], cwd=staging, text=True,
            capture_output=True, check=False, shell=False)
    # THE HUMAN RUN'S EXIT CODE IS THE VERDICT, and the JSON run carries the
    # lists it counted. `--json` reports only `invalid` and `missing`, so the
    # counts a reader wants live in the text output and are recorded verbatim.
    try:
        report = json.loads(machine.stdout or "{}")
    except json.JSONDecodeError as error:
        raise Refusal(f"`npm audit signatures --json` was unreadable: {error}")
    return {
        "install_stdout": install.stdout.strip(),
        "text": human.stdout.strip(),
        "text_exit": human.returncode,
        "json_exit": machine.returncode,
        "invalid": report.get("invalid") or [],
        "missing": report.get("missing") or [],
    }


def paragraph(text: str) -> str:
    """One paragraph, hard-wrapped to the width the corpus is written at.

    The house style is hard-wrapped prose; assembling a paragraph from
    pre-broken fragments produces the right words at the wrong wrap points, so
    the fragments are joined and re-wrapped once here instead.
    """
    return textwrap.fill(" ".join(text.split()), width=78,
                         break_long_words=False, break_on_hyphens=False)


def render(context: dict) -> str:
    """The dated record, written once.

    A CAPTURE and not a projection, on `docs/document-lifecycle.md`'s own test:
    a second run writes a different path rather than rewriting this one, so
    there is captured state for `Status: record` to protect.
    """
    rows = context["rows"]
    attested = [r for r in rows if r["attested"]]
    signed = [r for r in rows if r["keyids"]]
    audit = context["audit"]
    lines = [
        "# Evidence: the pinned CLI's lockfile integrity values, attested "
        f"{context['date']}",
        "",
        "Status: record",
        "Kind: report",
        "",
        paragraph(
            f"Task **6.1** of [`pin-openspec-cli-dependency-closure`]"
            f"(../{CLOSURE}/tasks.md) asked for an independent attestation of "
            "the registry integrity values the vendored lockfile captured, and "
            "recorded that nothing had attested them. This is that attestation, "
            "produced by `scripts/attest-openspec-cli-pin-lockfile.py` — read "
            "its module header for what the two links prove and, precisely, "
            "what they do not."),
        "",
        paragraph(
            f"Captured {context['generated_at']} against "
            f"`{context['registry']}` with `npm {context['npm_version']}` and "
            f"`node {context['node_version']}`, at repository revision "
            f"`{context['revision']}`. Every number below is a command's own "
            "output."),
        "",
        "## The subject",
        "",
        f"- pin: `{context['pin_path']}` at "
        f"`{context['package']}@{context['version']}`",
        f"- lockfile: `{context['lockfile_name']}`, verified against the pin's",
        "  `lockfile_integrity:` before anything was attested",
        f"- content-addressed entries: **{len(rows)}** — {len(rows) - 1} "
        "dependencies plus the",
        "  pinned CLI, whose own value the pin already corroborates",
        "",
        "## Link A — the recorded values, re-captured and compared",
        "",
        paragraph(
            f"Every one of the **{len(rows)}** recorded `integrity` values "
            "EQUALS the value the registry serves for that exact "
            "`name@version` today. The registry serves a signature over "
            f"**{len(signed)}** of them, and every keyid it signed with is "
            f"published at `{context['registry']}{KEYS_PATH}`."),
        "",
        "```",
        f"entries compared:                {len(rows)}",
        f"distinct name@version fetched:   {context['distinct']}",
        f"disagreements:                   {len(context['disagreements'])}",
        "```",
        "",
        "## Link B — `npm audit signatures` over the locked tree",
        "",
        paragraph(
            "Installed with the clean-install verb through the committed "
            "lockfile, the staging manifest derived from its own root entry:"),
        "",
        "```",
        audit["text"],
        "```",
        "",
        "```",
        f"npm audit signatures exit: {audit['text_exit']}",
        f"invalid:                   {len(audit['invalid'])}",
        f"missing:                   {len(audit['missing'])}",
        "```",
        "",
        paragraph(
            f"**{len(attested)}** of the {len(rows)} entries additionally carry "
            "a Sigstore provenance attestation, verified in the same run; the "
            "rest carry the registry's signature alone, which attests what npm "
            "published rather than how it was built."),
        "",
        "## Per-entry record",
        "",
        "| package | version | registry agrees | signed | provenance |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['name']}` | `{row['version']}` | "
            f"{'yes' if row['agrees'] else '**NO**'} | "
            f"{'yes' if row['keyids'] else '**no**'} | "
            f"{row['predicate'] or '—'} |")
    lines += [
        "",
        "## What stays open",
        "",
        paragraph(
            "The re-capture shares the original capture's NETWORK PATH — a "
            "later read over the same route, not the independent route § 6.1 "
            "also names — so the cryptographic weight rests on Link B's keys "
            "and transparency-log entries rather than on the second read."),
        "",
        paragraph(
            "And this run is a CAPTURE, not a gate: nothing in CI invokes it. "
            "Making the attestation a standing obligation of the pin, refused "
            "when a value is unattested, would change what "
            "`contracts/openspec-cli-pin.yaml` declares and what "
            "`neutral-product-pin` requires of it — an OpenSpec act, not a "
            "script's side effect. The pin's declared-shortfall paragraph is "
            "therefore untouched, and this record sits beside it as evidence "
            "rather than amending it."),
        "",
    ]
    return "\n".join(lines)


def command_output(argv: list[str]) -> str:
    """One command's own stdout, or a refusal naming it.

    Used only for the record's provenance lines — the npm and node versions and
    the revision the attestation was taken at — so a fault here must refuse
    rather than let a record claim a provenance it could not read.
    """
    # ARGUMENT LIST, NEVER A SHELL STRING, and every element is either a literal
    # or a path already resolved by `checked_npm` / `shutil.which`, so there is
    # no string a shell parses and no unresolved name to be found on a PATH the
    # run does not control.
    result = subprocess.run(argv, text=True, capture_output=True, check=False,
                            shell=False)
    if result.returncode != 0:
        raise Refusal(f"{argv[0]} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="attest-openspec-cli-pin-lockfile.py",
        description=("Attest the integrity values in the pinned CLI's vendored "
                     "lockfile against the registry's published, signed values "
                     "(closure task 6.1)."))
    parser.add_argument("--write", metavar="PATH", nargs="?", const="",
                        default=None,
                        help=("write the dated record; with no PATH it lands at "
                              "docs/openspec-cli-pin-lockfile-attestation-"
                              "<YYYY-MM-DD>.md"))
    parser.add_argument("--registry", default=DEFAULT_REGISTRY,
                        help=("the https ORIGIN to re-capture from (a mirrored "
                              "registry is § 6.1's second mechanism); a "
                              "non-https or non-bare origin is refused"))
    parser.add_argument("--npm", metavar="BIN", default="npm",
                        help=("the npm executable to install and audit with, "
                              "resolved to an absolute path or refused"))
    parser.add_argument("--pin", metavar="PATH", default=None,
                        help="an alternative pin file (tests)")
    parser.add_argument("--skip-audit", action="store_true",
                        help=("run Link A only, and say so; the record is NOT "
                              "written, a half-chain being evidence of nothing"))
    return parser


def main(argv: list[str] | None = None) -> int:
    """Return 0 attested, 1 a disagreement, 2 a refusal.

    EVERY ARGUMENT IS CHECKED BEFORE A ROUND TRIP IS SPENT, on the same
    reasoning the pin's own entrypoint settles its shape checks before it
    fetches: this run costs seventy-one registry reads and a clean install, and
    learning only afterwards that the record has nowhere to land tells a reader
    nothing the question had already told them. So the destination is resolved
    up front and discarded, even though it is not used until the end.
    """
    args = build_parser().parse_args(argv)
    now = datetime.now(timezone.utc)
    try:
        registry = checked_registry(args.registry)
        npm = checked_npm(args.npm)
        destination = None if args.write is None else checked_destination(
            args.write,
            ROOT / "docs" /
            f"openspec-cli-pin-lockfile-attestation-{now:%Y-%m-%d}.md")
        verifier = load_verifier()
        pin_path = Path(args.pin) if args.pin else verifier.PIN_PATH
        pin = verifier.read_pin(pin_path)
        package = verifier.pinned_package(pin)
        version = verifier.pinned_version(pin)
        integrity, _ = verifier.pinned_integrity(pin)
        lockfile, lockfile_integrity, lockfile_packages = verifier.pinned_lockfile(
            pin, pin_path)
        # The lockfile is verified against the pin BEFORE it is attested: an
        # attestation of unverified bytes would lend a signature's confidence to
        # a file nothing had checked.
        lockfile_bytes = verifier.verify_lockfile(
            lockfile, lockfile_integrity, lockfile_packages, package, integrity)
        document = verifier.read_lockfile(lockfile_bytes)
        entries = lockfile_entries(document)

        keys = registry_keys(registry)
        rows, disagreements = recapture(registry, entries, keys)
        print(f"LINK A — {len(rows)} recorded integrity values re-captured from "
              f"{registry}: {len(rows) - len(disagreements)} agree, "
              f"{len(disagreements)} do not")
        for line in disagreements:
            print(f"  DISAGREEMENT {line}")

        if args.skip_audit:
            print("LINK B — SKIPPED by --skip-audit. No record is written"
                  f"{' (--write ignored)' if destination else ''}: a re-capture "
                  "with no signature verification behind it attests nothing, "
                  "and a file saying otherwise would be worse than none.")
            return 1 if disagreements else 0

        audit = audit_signatures(verifier, lockfile_bytes, package, npm)
        print(audit["text"])
        print(f"LINK B — npm audit signatures exit={audit['text_exit']} "
              f"invalid={len(audit['invalid'])} missing={len(audit['missing'])}")
        if audit["text_exit"] != 0 or audit["invalid"] or audit["missing"]:
            disagreements.append(
                f"`npm audit signatures` exited {audit['text_exit']} with "
                f"{len(audit['invalid'])} invalid and {len(audit['missing'])} "
                f"missing signatures")

        if disagreements:
            print(f"\nNOT ATTESTED: {len(disagreements)} disagreement(s). No "
                  "record is written.")
            return 1

        revision = command_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
        record = render({
            "rows": rows,
            "audit": audit,
            "disagreements": disagreements,
            "distinct": len({(r["name"], r["version"]) for r in rows}),
            "date": now.strftime("%Y-%m-%d"),
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "registry": registry,
            "npm_version": command_output([npm, "--version"]),
            "node_version": command_output([checked_npm("node"), "--version"]),
            "revision": revision,
            "pin_path": pin_path.relative_to(ROOT).as_posix()
            if pin_path.is_absolute() else str(pin_path),
            "package": package,
            "version": version,
            "lockfile_name": lockfile.name,
        })
        print(f"\nATTESTED: {len(rows)} values, {len(rows)} agreeing with the "
              f"registry and every signature verified.")
        if destination is not None:
            destination.write_text(record, encoding="utf-8")
            print(f"record written: {destination}")
        return 0
    except Refusal as refusal:
        print(f"REFUSED: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:                        # noqa: BLE001
        # A refusal names its cause; an unexpected fault must not be reported as
        # a clean attestation, so it exits on the refusal code too.
        print(f"REFUSED: unexpected fault — {type(error).__name__}: {error}",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
