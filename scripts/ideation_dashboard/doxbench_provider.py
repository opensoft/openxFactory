"""THE ONE MODULE IN THIS REPOSITORY THAT MAY HOLD A PROVIDER ENDPOINT, A
MINTED TOKEN, OR A CREDENTIAL IN FLIGHT (add-model-provider-broker tasks
1.3/2.1/2.2/2.4).

Until this module existed, no provider was contacted from anywhere in this
repository, and a test read the source to keep it true. Minting means the
dashboard becomes a provider client, so the invariant NARROWS rather than
disappearing: exactly one module may hold those three things, this is that
module, it says so in its own `PROVIDER_CLIENT_MODULE` constant, and
`tests/ideation-dashboard/test_provider_boundary.py` sweeps every other module
in the package to keep the rest of the boundary exactly where it was. The views
clause stays ABSOLUTE — no browser module is exempt from anything, because a
token in a page is exfiltratable by anything able to run script there.

WHAT HAPPENS HERE, in the order a turn meets it:

  * the BROKER is invoked — the binding's declared argv, substituted from the
    binding's own fields, executed with a scrubbed environment. Two operations,
    both a JSON request on the child's standard input: ENROLL hands a human's
    credential to the broker and keeps the reference it returns; MINT asks for a
    short-lived, scoped token and gets back the token, its expiry, the endpoint
    it is good at, and the dialect that endpoint speaks;
  * the PROVIDER is called with that token, server-side, from the loopback
    console process. Brett's ruling of 2026-08-08: the broker mints, doxBench
    calls, because a broker in the request path adds a hop to every turn and to
    every chunk of a streamed one;
  * EXPIRY is handled by the 2026-08-26 ruling: re-mint and retry ONCE, with the
    re-mint and the paid retry visibly recorded, and a second expiry inside one
    turn surfaces the standard refusal rather than buying a third call.

WHAT NEVER HAPPENS HERE:

  * a credential is never held. `hand_off_credential` streams the human's value
    from an open source straight into the broker's standard input and never
    materialises it as a value of its own — no variable that outlives the call,
    no file, no echo in a return value, and nothing in any exception;
  * a minted token is never written to a file, never placed in a response,
    never logged, and never survives the process. `MintedToken` carries a
    redacting `__repr__`, so even a traceback frame or a debugger `print` of the
    object discloses nothing;
  * a broker's or a provider's own words never reach a caller. Every refusal
    this module raises carries one of the FIXED sentences below, composed from
    nothing the broker or the provider said, so `doxbench_model.dispatch_turn`
    maps it onto the same redacted `model_failed` every other adapter failure
    already maps onto.

THE BROKER IS DECLARED, NOT WRITTEN INTO CODE. openProfiler is not built; task
0.2's declaration of its CLI surface is dispatched but not landed. So no command
line appears in this file: the binding carries the argv template and this module
substitutes and executes it. When openProfiler ships with a different surface,
the binding changes and no code does.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Mapping
from datetime import datetime, timezone

from ideation_dashboard import doxbench_binding as binding_mod
from ideation_dashboard import doxbench_bridge as bridge_mod
from ideation_dashboard import doxbench_model as model_mod

#: THIS MODULE'S OWN NAME, declared so the structural boundary test and the
#: module cannot drift into naming two different files. The test asserts the
#: two are equal and that this file really is the one holding the transport, so
#: the exemption can never become vacuous.
PROVIDER_CLIENT_MODULE = "doxbench_provider.py"

# ---------------------------------------------------------------------------
# the broker's stdin/stdout contract (task 2.1)
# ---------------------------------------------------------------------------

#: The request document written to the broker's standard input, first line.
BROKER_REQUEST_SCHEMA_VERSION = 1
BROKER_REQUEST_KIND = "model-provider-broker-request"

#: The two operations the request may name. CLOSED: a broker that cannot tell
#: an enrolment from a mint would treat a credential hand-off as a mint request.
OPERATION_ENROLL = "enroll"
OPERATION_MINT = "mint"
OPERATIONS: tuple[str, ...] = (OPERATION_ENROLL, OPERATION_MINT)

#: The answers the broker writes to standard output, one JSON document each.
BROKER_ENROLLMENT_KIND = "model-provider-broker-enrollment"
BROKER_MINT_KIND = "model-provider-broker-mint"

#: The mint answer's required keys, exactly. A minted token that did not say
#: what it expires at, where it is good, and what that endpoint speaks is a
#: token this client could only use by guessing.
MINT_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "token", "expires_at", "endpoint", "dialect")

#: The enrolment answer's required keys, exactly.
ENROLLMENT_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "credential_ref")

#: The CLOSED dialect vocabulary the provider client can speak. ONE member
#: today: this repository's own already-declared turn shape — a prompt in, an
#: `assistant_prose` out — which is the shape `doxbench_model.dispatch_turn`
#: validates on the way back, so no second response grammar exists to keep
#: honest. It is closed rather than open because an UNKNOWN dialect must REFUSE
#: rather than be guessed at: sending an assembled prompt to an endpoint whose
#: grammar this client does not know is a paid call that cannot succeed.
#: openProfiler's task-0.2 declaration is what adds the second member, and it
#: adds an arm here beside it rather than loosening this check.
DIALECT_XFACTORY_PROMPT_V1 = "xfactory-prompt-v1"
DIALECTS: tuple[str, ...] = (DIALECT_XFACTORY_PROMPT_V1,)

#: How long a broker invocation may take. A mint is a local process doing local
#: custody work; a broker that cannot answer in this long is a broker that
#: cannot answer.
BROKER_TIMEOUT_SECONDS = 30.0

#: The largest answer a broker may write. A bound, not a policy: an unbounded
#: read of a child's stdout is a way to spend this process's memory by
#: misconfiguring a binding.
MAX_BROKER_ANSWER_BYTES = 65_536

# ---------------------------------------------------------------------------
# fixed, redacted refusals (the shape `dispatch_turn` already defines)
# ---------------------------------------------------------------------------

#: Every sentence this module may raise, composed from NOTHING the broker or
#: the provider said. A broker's stderr, a provider's error body and an
#: exception's text are all dropped unread at the boundary that observes them,
#: exactly as `dispatch_turn` drops a provider exception's text.
DIAG_BROKER_UNREACHABLE = (
    "the credential broker could not be started, so no token could be minted")
DIAG_BROKER_REFUSED = (
    "the credential broker refused, so no token could be minted")
DIAG_BROKER_MALFORMED = (
    "the credential broker's answer did not match the declared mint contract")
DIAG_BROKER_TIMEOUT = (
    "the credential broker did not answer within the declared timeout")
DIAG_DIALECT_UNKNOWN = (
    "the minted endpoint declares a dialect this client does not speak")
DIAG_PROVIDER_UNREACHABLE = (
    "the provider could not be reached and its details are withheld by design")
DIAG_PROVIDER_REFUSED = (
    "the provider refused and its details are withheld by design")
DIAG_PROVIDER_MALFORMED = (
    "the provider response did not match the expected shape")
DIAG_TOKEN_EXPIRED_TWICE = (
    "the minted token expired twice within one turn; a further paid call is "
    "not made on a turn that has already been retried once")

#: The closed set, so a test can assert no other sentence can be raised.
FIXED_DIAGNOSTICS: frozenset[str] = frozenset({
    DIAG_BROKER_UNREACHABLE, DIAG_BROKER_REFUSED, DIAG_BROKER_MALFORMED,
    DIAG_BROKER_TIMEOUT, DIAG_DIALECT_UNKNOWN, DIAG_PROVIDER_UNREACHABLE,
    DIAG_PROVIDER_REFUSED, DIAG_PROVIDER_MALFORMED, DIAG_TOKEN_EXPIRED_TWICE,
})


class BrokerRefused(RuntimeError):
    """A broker or a provider could not answer, stated in one of
    ``FIXED_DIAGNOSTICS`` and nothing else.

    Deliberately carries no payload, no status code, no stderr and no response
    body: there is no attribute a caller could log that discloses provider or
    broker detail, which is the same discipline `TurnDispatchFailure` keeps."""

    def __init__(self, diagnostic: str) -> None:
        if diagnostic not in FIXED_DIAGNOSTICS:
            raise AssertionError(
                "a broker refusal carries a FIXED diagnostic; composing one "
                "from what the broker or the provider said is exactly what "
                "this class exists to prevent")
        super().__init__(diagnostic)
        self.diagnostic = diagnostic


class _TokenExpired(Exception):
    """The provider said the presented token is no longer valid.

    PRIVATE and never raised out of this module: it is the signal the
    expiry ruling turns on, and it becomes either a re-mint or a
    ``BrokerRefused`` before any caller sees anything."""


# ---------------------------------------------------------------------------
# the minted token (task 2.1: memory only, never written, never logged)
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class MintedToken:
    """One short-lived, scoped token, as the broker issued it.

    IN PROCESS MEMORY ONLY. Nothing here writes it, returns it to a route, or
    puts it in a record; the port below holds at most one of these at a time and
    drops it at expiry, and the object dies with the process that minted it.

    ``__repr__`` REDACTS, and that is not decoration. A frozen dataclass's
    generated repr prints every field, so an exception chain, a debugger, a
    `print(port.__dict__)`, or a future `logging` call that formats an object
    would each have disclosed the token. Redacting at the type means every one
    of those routes discloses the same nothing."""

    token: str
    expires_at: float
    endpoint: str
    dialect: str

    def __repr__(self) -> str:
        return (f"MintedToken(token=<redacted>, expires_at={self.expires_at!r},"
                f" endpoint={self.endpoint!r}, dialect={self.dialect!r})")

    __str__ = __repr__

    def expired(self, now: float) -> bool:
        """Whether this token has passed the expiry the broker DECLARED.

        Compared against the broker's own `expires_at` rather than against a
        lifetime this client assumed: the broker is the authority on how long
        what it issued is good for."""
        return now >= self.expires_at


def _parse_expires_at(value: object) -> float:
    """The broker's declared expiry, as epoch seconds.

    Accepts an ISO-8601 instant (the spelling `credential-contracts` uses for
    its own `expires_at`) or a plain number of epoch seconds. A naive instant is
    read as UTC — the alternative, reading it in the console host's local zone,
    would make a token's life depend on where the operator lives."""
    if isinstance(value, bool):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value.strip():
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        moment = datetime.fromisoformat(text)
    except ValueError as error:
        raise BrokerRefused(DIAG_BROKER_MALFORMED) from error
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.timestamp()


# ---------------------------------------------------------------------------
# the broker runner seam
# ---------------------------------------------------------------------------


def subprocess_broker_runner(argv, *, request: Mapping, source=None,
                             timeout: float = BROKER_TIMEOUT_SECONDS) -> str:
    """Run the declared broker invocation and return its standard output.

    THE STDIN CONTRACT, in two parts and in this order:

      1. one line of JSON — the request document (`BROKER_REQUEST_KIND`), which
         names the operation, the binding and the credential reference. Never
         the credential;
      2. for an ENROLMENT only, the credential itself, streamed verbatim from
         `source` until end of file. STREAMED, not read: `shutil.copyfileobj`
         moves it in chunks from the operator's handle to the child's pipe, so
         the whole value never becomes a string in this process and there is no
         variable holding it to outlive the call.

    The child's environment is the same scrubbed allowlist the harness bridge
    already uses (`doxbench_bridge.INHERITED_ENVIRONMENT`), reused rather than
    respelled: a broker inherits a PATH and a HOME and nothing else, so no
    credential-shaped variable of this process's environment can reach it and
    no accident can turn an ambient variable into an implicit credential.

    Stderr is CAPTURED AND DROPPED. A broker's own words must never reach a
    caller, and letting them inherit this process's stderr would put them on the
    console instead."""
    try:
        child = subprocess.Popen(  # noqa: S603 - argv from a declared binding, never a shell string
            list(argv),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=bridge_mod.child_environment(os.environ),
            text=True,
        )
    except (OSError, ValueError) as error:
        raise BrokerRefused(DIAG_BROKER_UNREACHABLE) from error
    try:
        child.stdin.write(json.dumps(request, sort_keys=True))
        child.stdin.write("\n")
        if source is not None:
            # The credential's ONLY path through this process: handle to pipe,
            # in chunks, never assembled.
            shutil.copyfileobj(source, child.stdin)
        child.stdin.close()
        # `communicate` flushes `child.stdin` before reading, which raises on a
        # handle this function has already closed — and closing it IS the
        # signal a streamed credential's end of file needs. Dropping the
        # reference is the documented way to say "stdin is finished with", and
        # it is also the last place in this process that could have held the
        # pipe the credential travelled down.
        child.stdin = None
        answer, _dropped_stderr = child.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        child.kill()
        child.communicate()
        raise BrokerRefused(DIAG_BROKER_TIMEOUT) from error
    except OSError as error:
        child.kill()
        child.communicate()
        raise BrokerRefused(DIAG_BROKER_UNREACHABLE) from error
    if child.returncode != 0:
        raise BrokerRefused(DIAG_BROKER_REFUSED)
    if len(answer.encode("utf-8")) > MAX_BROKER_ANSWER_BYTES:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return answer


def _broker_request(binding, operation: str) -> dict:
    """The request document, which names the REFERENCE and never a secret."""
    return {
        "schema_version": BROKER_REQUEST_SCHEMA_VERSION,
        "kind": BROKER_REQUEST_KIND,
        "operation": operation,
        "binding_id": binding.id,
        "credential_ref": binding.credential_ref,
        "auth_kind": binding.auth_kind,
    }


def _answer_document(text: object, kind: str, fields) -> dict:
    if not isinstance(text, str):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    try:
        document = json.loads(text)
    except (ValueError, TypeError) as error:
        raise BrokerRefused(DIAG_BROKER_MALFORMED) from error
    if not isinstance(document, dict):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if document.get("schema_version") != BROKER_REQUEST_SCHEMA_VERSION:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if document.get("kind") != kind:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if any(field not in document for field in fields):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return document


# ---------------------------------------------------------------------------
# the credential hand-off (task 1.3)
# ---------------------------------------------------------------------------


def hand_off_credential(binding, source, *,
                        runner=subprocess_broker_runner) -> str:
    """Hand a human's credential to the broker and keep only the reference.

    `source` is an OPEN HANDLE the caller supplies — `sys.stdin`, a pipe, a
    test's `io.StringIO` — and never a string. That signature is the enforcement
    rather than a convention: a caller cannot pass a credential VALUE to this
    function, so no caller can be holding one either, and the value's whole
    journey is handle to pipe to broker.

    Returns the reference the broker gives back. That reference is the only
    thing that then lives in a binding, in a file, in a log or in a review."""
    answer = runner(tuple(binding.substituted_argv()),
                    request=_broker_request(binding, OPERATION_ENROLL),
                    source=source)
    document = _answer_document(answer, BROKER_ENROLLMENT_KIND,
                                ENROLLMENT_FIELDS)
    reference = document["credential_ref"]
    if not isinstance(reference, str) or not reference.strip():
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return reference


# ---------------------------------------------------------------------------
# minting (task 2.1)
# ---------------------------------------------------------------------------


def mint(binding, *, runner=subprocess_broker_runner) -> MintedToken:
    """Ask the broker for a short-lived, scoped token.

    Returns the token IN MEMORY. Nothing in this function writes it, and its
    only caller is the port below, which holds at most one at a time."""
    answer = runner(tuple(binding.substituted_argv()),
                    request=_broker_request(binding, OPERATION_MINT))
    document = _answer_document(answer, BROKER_MINT_KIND, MINT_FIELDS)
    token = document["token"]
    endpoint = document["endpoint"]
    dialect = document["dialect"]
    for value in (token, endpoint, dialect):
        if not isinstance(value, str) or not value.strip():
            raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if dialect not in DIALECTS:
        raise BrokerRefused(DIAG_DIALECT_UNKNOWN)
    return MintedToken(token=token,
                       expires_at=_parse_expires_at(document["expires_at"]),
                       endpoint=endpoint, dialect=dialect)


# ---------------------------------------------------------------------------
# the provider transport
# ---------------------------------------------------------------------------

#: The provider request's own field names, in the ONE dialect this client
#: speaks. Named constants rather than inline literals so the boundary test can
#: assert they exist only here.
PROVIDER_REQUEST_MODEL_FIELD = "model"
PROVIDER_REQUEST_PROMPT_FIELD = "prompt"
PROVIDER_RESPONSE_PROSE_FIELD = "assistant_prose"

#: The status a provider returns when the presented token is no longer good.
#: 401 only: a 403 is an authorization verdict about what the token may do,
#: which re-minting the same scope cannot change, and retrying it would buy a
#: second refusal.
PROVIDER_STATUS_TOKEN_EXPIRED = 401


def _post_to_provider(token: MintedToken, *, model_id: str, prompt: str,
                      timeout: float, opener) -> str:
    """The ONE place a provider is contacted. Returns the assistant prose.

    The token travels in the request's authorization header and nowhere else;
    it is not in the URL (which a proxy logs), not in the body (which an error
    handler might echo), and not in this function's return value."""
    body = json.dumps({
        PROVIDER_REQUEST_MODEL_FIELD: model_id,
        PROVIDER_REQUEST_PROMPT_FIELD: prompt,
    }).encode("utf-8")
    request = urllib.request.Request(  # noqa: S310 - endpoint declared by the broker's mint answer
        token.endpoint, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {token.token}")
    try:
        with opener(request, timeout=timeout) as response:
            payload = response.read()
    except urllib.error.HTTPError as error:
        # The error body is DROPPED UNREAD: a provider's own words must never
        # reach a caller, and a 401 is the only status whose MEANING this client
        # acts on.
        status = getattr(error, "code", None)
        error.close()
        if status == PROVIDER_STATUS_TOKEN_EXPIRED:
            raise _TokenExpired from None
        raise BrokerRefused(DIAG_PROVIDER_REFUSED) from None
    except (urllib.error.URLError, OSError, ValueError) as error:
        raise BrokerRefused(DIAG_PROVIDER_UNREACHABLE) from error
    try:
        document = json.loads(payload.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as error:
        raise BrokerRefused(DIAG_PROVIDER_MALFORMED) from error
    if not isinstance(document, dict):
        raise BrokerRefused(DIAG_PROVIDER_MALFORMED)
    prose = document.get(PROVIDER_RESPONSE_PROSE_FIELD)
    if not isinstance(prose, str):
        raise BrokerRefused(DIAG_PROVIDER_MALFORMED)
    return prose


# ---------------------------------------------------------------------------
# the mint ledger (the 2026-08-26 ruling's "visibly recorded")
# ---------------------------------------------------------------------------

REASON_FIRST_MINT = "first_mint"
REASON_EXPIRY_REMINT = "remint_after_expiry"
REASON_PAID_RETRY = "paid_retry"
MINT_REASONS: tuple[str, ...] = (
    REASON_FIRST_MINT, REASON_EXPIRY_REMINT, REASON_PAID_RETRY)

#: The most mint events one served process keeps. A bound, not a policy.
MAX_LEDGER_EVENTS = 256


@dataclasses.dataclass(frozen=True, slots=True)
class MintEvent:
    """ONE content-free record of a mint or a paid retry.

    Carries no token, no prompt, no document text and no provider detail: a
    binding id, a reason from the closed vocabulary above, and when it happened.
    That is what makes it safe to disclose, which is the whole point of
    recording it — Brett's 2026-08-26 ruling is that a re-mint and the paid
    retry it buys are VISIBLE, and a record nobody may show would not satisfy
    it."""

    binding_id: str
    reason: str
    at: float

    def as_dict(self) -> dict:
        return {"binding_id": self.binding_id, "reason": self.reason,
                "at": self.at}


#: The operator-visible sentence a re-mint prints. FIXED, and content-free.
REMINT_NOTICE = (
    "[model-provider] the minted token expired mid-turn: re-minted once and "
    "retried the turn (one further paid provider call). A second expiry in the "
    "same turn refuses instead.")


# ---------------------------------------------------------------------------
# the port
# ---------------------------------------------------------------------------


class BrokeredProviderPort:
    """A `doxbench_model.WorkbenchModelPort` backed by a broker-minted token.

    THREE MEMBERS AND NO FOURTH, exactly like every other adapter this seam
    accepts: `timeout_seconds`, `catalog()`, `dispatch(envelope)`. Everything
    below them — minting, expiry, the retry ruling, the provider call — is this
    class's business and reaches the seam as one opaque dispatch.

    ONE INSTANCE PER PROCESS, for the same reason the harness bridge is:
    `_workbench_model_port` resolves per REQUEST, and a port constructed per
    call would mint a fresh token for every turn and throw away a perfectly
    live one. The token is guarded by a lock because the server is a
    `ThreadingHTTPServer`.

    `catalog()` NEVER MINTS. A menu is not a paid call, and a console that
    minted a token to render one would spend a mint on every capabilities
    probe."""

    def __init__(self, binding, catalog, *,
                 timeout_seconds: float = 60.0,
                 runner=subprocess_broker_runner,
                 opener=urllib.request.urlopen,
                 clock=time.time,
                 notice=None) -> None:
        if not isinstance(binding, binding_mod.ModelProviderBinding):
            raise TypeError(
                "binding must be a ModelProviderBinding, got "
                f"{type(binding).__name__}")
        if not isinstance(catalog, model_mod.ModelCatalog):
            raise TypeError(
                f"catalog must be a ModelCatalog, got {type(catalog).__name__}")
        self._binding = binding
        self._declared_catalog = catalog
        self._timeout_seconds = model_mod.validated_timeout_seconds(
            timeout_seconds)
        self._runner = runner
        self._opener = opener
        self._clock = clock
        self._notice = notice if notice is not None else sys.stderr.write
        self._lock = threading.Lock()
        self._token: MintedToken | None = None
        self._mintable = True
        self.ledger: list[MintEvent] = []

    # -- the three port members --------------------------------------------

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    def catalog(self) -> model_mod.ModelCatalog:
        """The install's declared catalog, marked unavailable once this port
        knows it cannot mint.

        The same honesty the harness bridge keeps: a declaration is available
        until something is measured, and a broker that has refused is measured.
        Nothing here contacts the broker to find out."""
        if self._mintable:
            return self._declared_catalog
        return model_mod.ModelCatalog.from_entries([
            dataclasses.replace(entry, available=False)
            for entry in self._declared_catalog.entries])

    def dispatch(self, prompt_envelope: object) -> object:
        """ONE turn: mint (or reuse), call the provider, and honour the expiry
        ruling.

        Returns the shape `doxbench_model.dispatch_turn` validates — prose plus
        an empty proposal list — so typed proposals stay the route's injected
        validator's business, exactly as they are for the harness bridge.

        THE 2026-08-26 EXPIRY RULING, in full and in one place:

          * before the call, a token past its declared expiry is DISCARDED and a
            fresh one minted. That half is unconditional and is not the retry:
            it is simply never presenting a token known to be dead;
          * if the provider nevertheless says the token expired — the race the
            ruling is actually about, where a long generation outlives a short
            token — the port re-mints and retries the turn ONCE, recording both
            the re-mint and the paid retry in `ledger` and printing
            `REMINT_NOTICE`, because silently buying a second paid call is the
            decision this ruling refused to leave implicit;
          * a SECOND expiry inside the same turn raises the standard refusal.
            No third call is bought."""
        model_id = getattr(prompt_envelope, "model_id", None)
        if not isinstance(model_id, str) or not model_id:
            entries = self._declared_catalog.entries
            model_id = entries[0].model_id if entries else ""
        prompt = bridge_mod.render_prompt_message(prompt_envelope)
        token = self._current_token(REASON_FIRST_MINT)
        try:
            prose = _post_to_provider(token, model_id=model_id, prompt=prompt,
                                      timeout=self._timeout_seconds,
                                      opener=self._opener)
        except _TokenExpired:
            self._forget_token()
            self._record(REASON_EXPIRY_REMINT)
            self._notice(REMINT_NOTICE + "\n")
            token = self._current_token(REASON_PAID_RETRY)
            try:
                prose = _post_to_provider(
                    token, model_id=model_id, prompt=prompt,
                    timeout=self._timeout_seconds, opener=self._opener)
            except _TokenExpired:
                self._forget_token()
                raise BrokerRefused(DIAG_TOKEN_EXPIRED_TWICE) from None
        return {"assistant_prose": prose, "proposals": []}

    # -- token custody ------------------------------------------------------

    def _current_token(self, reason: str) -> MintedToken:
        """The live token, minting one when there is none or the one held has
        passed the broker's declared expiry (discard-on-expiry, task 2.4)."""
        with self._lock:
            held = self._token
            if held is not None and not held.expired(self._clock()):
                return held
            self._token = None
            try:
                minted = mint(self._binding, runner=self._runner)
            except BrokerRefused:
                self._mintable = False
                raise
            self._mintable = True
            self._token = minted
        self._record(reason)
        return minted

    def _forget_token(self) -> None:
        with self._lock:
            self._token = None

    def _record(self, reason: str) -> None:
        event = MintEvent(binding_id=self._binding.id, reason=reason,
                          at=self._clock())
        with self._lock:
            self.ledger.append(event)
            if len(self.ledger) > MAX_LEDGER_EVENTS:
                del self.ledger[:-MAX_LEDGER_EVENTS]

    def __repr__(self) -> str:
        return (f"BrokeredProviderPort(binding={self._binding.id!r}, "
                f"mintable={self._mintable}, "
                f"token={'held' if self._token is not None else 'none'})")
