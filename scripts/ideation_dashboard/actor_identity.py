"""Actor authentication for gate actions — closing the unauthenticated `--actor`.

THE GAP THIS CLOSES (`ideation/brainstorm/ideation-dashboard.md` item 25;
`contracts/identity-brokering/README.md`: "`--actor` is unauthenticated"). Every
gate entrypoint took the acting human's identity as FREE TEXT on a flag. The only
check anywhere was `HumanGate`'s non-blankness test, so `--actor "anyone"` wrote a
governed, authority-bearing `gate-action-record` naming a person who had nothing
to do with the invocation. Every record the console has ever written is therefore
unattributable: the field says WHO acted and nothing established that it was true.

WHAT THIS MODULE DOES, and what it deliberately does not. It does NOT invent an
authentication system — the identity work is D22 / the identity-brokering family,
and that is where a real IdP-backed principal will come from. It BINDS the claim
to whatever identity the surrounding deployment already proves, and it FAILS
CLOSED when nothing proves one: no principal, no gate action, no record.

The trusted sources, STRONGEST FIRST. The first source that is configured/
available wins outright — a weaker source never widens a stronger one, so a
deployment that stamps a gateway identity cannot be broadened by a stray
environment variable or by the checkout's git config:

  1. `XF_AUTH_REQUEST_USER` (`gateway-auth`) — the username the dox-auth gateway
     verified. The hosted plane already stamps it into `X-Auth-Request-User` on
     every proxied request, having STRIPPED any client-supplied value first
     (`serve.py` surfaces it as the display-only `hosted_actor`), so it is the
     one identity in this system a caller cannot spell for itself. A hosted
     entrypoint exports the stamped value into the process environment under
     this name; nothing else may set it.
  2. `XF_GATE_PRINCIPAL` (`env-principal`) — a single principal supplied by a
     TRUSTED LAUNCHER (a pod entrypoint, a broker-issued session). Same
     contract as (1) with a weaker provenance: the process was started by
     something that already knew who the human was.
  3. `XF_GATE_PRINCIPALS` (`env-roster`) / `XF_GATE_ACTOR_ALLOWLIST`
     (`allowlist-file`) — an explicit allowlist of the humans this console may
     record. The file shape is the intent plane's own committed map
     (`{"actors": {"<actor>": [...verbs]}}`) or a bare JSON list; membership is
     what is checked here, and per-verb scoping stays the intent lane's job.
  4. The checkout's own git identity (`git-identity`) — `user.name` /
     `user.email` of the repository the action is being taken in. This is the
     LOCAL CLI's honest answer to "who is this?": a person acting in their own
     checkout, recorded as the name their commits already carry.

THE RESIDUAL, stated plainly rather than left ambient. Sources (2)-(4) are
process-local: an agent running AS the engineer, in the engineer's checkout, can
satisfy them — exactly the residual `console_presence` already records for the
human-console test (D23, Brett's 2026-07-27 ruling). What this module removes is
the strictly larger hole underneath it: an invocation that named a human it had
NO relationship to at all. Only source (1) survives that residual, and it is the
one the identity-brokering family is being built to make universal.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

# ---- the environment contract (names are part of the deployment interface) ----
GATEWAY_ENV = "XF_AUTH_REQUEST_USER"
PRINCIPAL_ENV = "XF_GATE_PRINCIPAL"
ROSTER_ENV = "XF_GATE_PRINCIPALS"
ALLOWLIST_ENV = "XF_GATE_ACTOR_ALLOWLIST"

# ---- how the principal was established (recorded in refusals, and available to
# callers that want to tag a record with it) ----
SOURCE_GATEWAY = "gateway-auth"
SOURCE_ENV_PRINCIPAL = "env-principal"
SOURCE_ROSTER = "env-roster"
SOURCE_ALLOWLIST = "allowlist-file"
SOURCE_GIT_IDENTITY = "git-identity"

# Ordered strongest-first; `trusted_principals` returns the FIRST that resolves.
SOURCE_ORDER = (SOURCE_GATEWAY, SOURCE_ENV_PRINCIPAL, SOURCE_ROSTER,
                SOURCE_ALLOWLIST, SOURCE_GIT_IDENTITY)

NO_PRINCIPAL_REFUSAL = (
    "no authenticated principal could be established for this invocation, so "
    "the acting human cannot be verified and no governed record may be written. "
    f"A gate action needs one of: the gateway-verified user ({GATEWAY_ENV}), a "
    f"launcher-supplied principal ({PRINCIPAL_ENV}), an explicit allowlist "
    f"({ROSTER_ENV} or {ALLOWLIST_ENV}), or a checkout whose `git config "
    "user.name`/`user.email` names the acting human")


class ActorUnauthenticated(Exception):
    """The claimed actor could not be bound to an authenticated principal.

    Raised BEFORE any governed write. Callers turn it into a refusal + a
    non-zero exit; nothing about the action proceeds."""


@dataclass(frozen=True)
class AuthenticatedActor:
    """A claim that was checked. `actor` is the CANONICAL spelling taken from the
    trusted source, never the caller's spelling — so a record cannot carry a
    lookalike variant of a real principal's name."""

    actor: str
    source: str


# The sources that name ONE human, possibly in more than one spelling. A git
# identity yields `user.name` AND `user.email` — two spellings of the same
# person, not two people — so an unnamed actor there is not ambiguous, it is
# that person under their primary spelling. A ROSTER or an ALLOWLIST is the
# opposite: several entries mean several humans, and choosing one would be
# guessing whose authority is being exercised.
SINGLE_IDENTITY_SOURCES = (SOURCE_GATEWAY, SOURCE_ENV_PRINCIPAL,
                           SOURCE_GIT_IDENTITY)


@dataclass(frozen=True)
class TrustedPrincipals:
    source: str
    values: tuple[str, ...]

    def __bool__(self) -> bool:
        return bool(self.values)

    @property
    def primary(self) -> str:
        """The canonical spelling to adopt when no actor was named."""
        return self.values[0] if self.values else ""

    @property
    def names_one_human(self) -> bool:
        return bool(self.values) and (
            len(self.values) == 1 or self.source in SINGLE_IDENTITY_SOURCES)


def _clean(value: object) -> str:
    """Whitespace-normalised text, or "" — the shape a principal is compared in."""
    return " ".join(str(value or "").split())


def _key(value: object) -> str:
    """The comparison key: whitespace-normalised, case-folded. Deliberately NOT
    a looser match — a fuzzy identity comparison is how a lookalike gets in."""
    return _clean(value).casefold()


def _split_roster(raw: str) -> tuple[str, ...]:
    parts: list[str] = []
    for chunk in str(raw).replace("\n", ",").replace(";", ",").split(","):
        cleaned = _clean(chunk)
        if cleaned:
            parts.append(cleaned)
    return tuple(dict.fromkeys(parts))


def load_actor_allowlist(path: Path | str) -> tuple[str, ...]:
    """The committed allowlist of humans this console may record.

    Accepts the intent plane's own map shape (`{"actors": {name: [verbs]}}`,
    `intent_apply_lane.load_allowlist`) or a bare JSON list of names. Missing or
    malformed resolves EMPTY — nobody may act — which is the same fail-closed
    reading the intent lane already uses."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    if isinstance(data, list):
        return tuple(dict.fromkeys(_clean(v) for v in data if _clean(v)))
    if isinstance(data, dict):
        actors = data.get("actors")
        if isinstance(actors, dict):
            return tuple(dict.fromkeys(_clean(a) for a in actors if _clean(a)))
        if isinstance(actors, list):
            return tuple(dict.fromkeys(_clean(v) for v in actors if _clean(v)))
    return ()


def git_identity(checkout_root: Path | str | None) -> tuple[str, ...]:
    """`user.name` and `user.email` of the checkout the action acts on.

    Not a strong authenticator and never described as one — it is the identity
    the human's own commits in this repository already carry, which is exactly
    the attribution a local CLI gate action lands under."""
    if checkout_root is None:
        return ()
    found: list[str] = []
    for key in ("user.name", "user.email"):
        try:
            proc = subprocess.run(
                ["git", "-C", str(checkout_root), "config", key],
                capture_output=True, text=True, timeout=10)
        except (OSError, subprocess.SubprocessError):
            return ()
        value = _clean(proc.stdout)
        if proc.returncode == 0 and value:
            found.append(value)
    return tuple(dict.fromkeys(found))


def trusted_principals(checkout_root: Path | str | None = None, *,
                       env: Mapping[str, str] | None = None) -> TrustedPrincipals:
    """The principals this invocation may act as, from the STRONGEST source that
    resolves. An empty result means nothing proved an identity — the caller must
    refuse, never guess."""
    env = os.environ if env is None else env

    gateway = _clean(env.get(GATEWAY_ENV))
    if gateway:
        return TrustedPrincipals(SOURCE_GATEWAY, (gateway,))

    principal = _clean(env.get(PRINCIPAL_ENV))
    if principal:
        return TrustedPrincipals(SOURCE_ENV_PRINCIPAL, (principal,))

    roster = _split_roster(env.get(ROSTER_ENV) or "")
    if roster:
        return TrustedPrincipals(SOURCE_ROSTER, roster)

    allowlist_path = _clean(env.get(ALLOWLIST_ENV))
    if allowlist_path:
        # A DECLARED allowlist that resolves empty stays the answer: it was
        # configured, so falling through to the git identity would be a silent
        # widening of a control someone deliberately put in place.
        return TrustedPrincipals(SOURCE_ALLOWLIST,
                                 load_actor_allowlist(allowlist_path))

    identity = git_identity(checkout_root)
    if identity:
        return TrustedPrincipals(SOURCE_GIT_IDENTITY, identity)

    return TrustedPrincipals("", ())


def _refuse_unknown(claim: str, principals: TrustedPrincipals) -> ActorUnauthenticated:
    known = ", ".join(repr(v) for v in principals.values)
    return ActorUnauthenticated(
        f"actor {claim!r} is not an authenticated principal of this invocation. "
        f"The {principals.source} source establishes {known}; an actor claim is "
        "recorded on an authority-bearing gate-action record, so a claim that "
        "cannot be verified is refused rather than written")


def authenticate_actor(claimed: str | None, *,
                       checkout_root: Path | str | None = None,
                       env: Mapping[str, str] | None = None) -> AuthenticatedActor:
    """Bind a claimed `--actor` to an authenticated principal, or REFUSE.

    Three outcomes and no fourth:

      * the claim matches a trusted principal -> the principal's CANONICAL
        spelling is returned and is what the record must carry;
      * no claim was made and exactly ONE principal is established -> that
        principal is adopted (the flag is then a confirmation, not an
        assertion). Several principals with no claim is AMBIGUOUS and refused —
        picking one would be guessing at whose authority is being exercised;
      * anything else -> `ActorUnauthenticated`, raised BEFORE any write.
    """
    principals = trusted_principals(checkout_root, env=env)
    if not principals:
        raise ActorUnauthenticated(NO_PRINCIPAL_REFUSAL)

    claim = _clean(claimed)
    if not claim:
        if principals.names_one_human:
            return AuthenticatedActor(principals.primary, principals.source)
        raise ActorUnauthenticated(
            "no actor was named and the authenticated identity is ambiguous "
            f"({principals.source} establishes "
            f"{', '.join(repr(v) for v in principals.values)}). Name the acting "
            "human explicitly; the console never picks one")

    for value in principals.values:
        if _key(value) == _key(claim):
            return AuthenticatedActor(value, principals.source)
    raise _refuse_unknown(claim, principals)


def authenticated_actor_or_none(claimed: str | None, *,
                                checkout_root: Path | str | None = None,
                                env: Mapping[str, str] | None = None) -> str | None:
    """`authenticate_actor` for the callers whose fail-closed spelling is
    ABSENCE rather than an exception (`serve.resolve_actor`: no identity keeps
    gate actions unavailable). Never returns a guessed actor."""
    try:
        return authenticate_actor(claimed, checkout_root=checkout_root,
                                  env=env).actor
    except ActorUnauthenticated:
        return None


def describe_sources(principals: TrustedPrincipals | None = None) -> str:
    """Human-readable one-liner for refusal prose and diagnostics."""
    if principals is None or not principals:
        return "none"
    return f"{principals.source}: " + ", ".join(principals.values)


__all__: Sequence[str] = (
    "ALLOWLIST_ENV", "GATEWAY_ENV", "PRINCIPAL_ENV", "ROSTER_ENV",
    "SOURCE_ALLOWLIST", "SOURCE_ENV_PRINCIPAL", "SOURCE_GATEWAY",
    "SOURCE_GIT_IDENTITY", "SOURCE_ORDER", "SOURCE_ROSTER",
    "ActorUnauthenticated", "AuthenticatedActor", "TrustedPrincipals",
    "authenticate_actor", "authenticated_actor_or_none", "describe_sources",
    "git_identity", "load_actor_allowlist", "trusted_principals",
)

