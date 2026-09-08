"""THE ONE MODULE IN THIS REPOSITORY THAT MAY CONTACT A PROVIDER, HOLD A
MINTED TOKEN, OR HOLD A CREDENTIAL IN FLIGHT (add-model-provider-broker tasks
1.3/2.1/2.2/2.4/2.6).

Until this module existed, no provider was contacted from anywhere in this
repository, and a test read the source to keep it true. Minting means the
dashboard becomes a provider client, so the invariant NARROWS rather than
disappearing: exactly one module may hold those three things, this is that
module, it says so in its own `PROVIDER_CLIENT_MODULE` constant, and
`tests/ideation-dashboard/test_provider_boundary.py` sweeps every other module
in the package to keep the rest of the boundary exactly where it was. The views
clause stays ABSOLUTE — no browser module is exempt from anything, because a
token in a page is exfiltratable by anything able to run script there.

ONE PRECISION THE RECONCILIATION FORCED, stated rather than left to erode: the
binding RECORD now carries an `endpoint`, because openProfiler's declaration
will not name one (see below). That is a declared FACT in an operator's settings
document, validated by `doxbench_binding`, and it is not a transport: no module
but this one opens a socket, imports an HTTP client, or holds a token to put on
one, and the structural sweep is unchanged. "Holds a provider endpoint" as the
boundary test means it — a provider host or path written into source — remains
true of this module alone.

WHAT HAPPENS HERE, in the order a turn meets it:

  * the BROKER is invoked — the binding's declared BASE argv plus the DECLARED
    subcommand and flags, executed with a scrubbed environment. Four operations,
    exactly the four openProfiler declares: INTAKE hands a human's credential to
    the broker on standard input and keeps the `reference` it returns; MINT asks
    for a short-lived token and gets back the token, its `expires_at` and the
    `audit_ref` that names the issuance; REVOKE destroys custody; LIST reads the
    non-secret reference index;
  * the PROVIDER is called with that token, server-side, from the loopback
    console process. Brett's ruling of 2026-08-08: the broker mints, doxBench
    calls, because a broker in the request path adds a hop to every turn and to
    every chunk of a streamed one. WHERE to call and WHAT GRAMMAR to speak are
    the BINDING's — the broker's declaration emits neither, deliberately;
  * EXPIRY is handled by the 2026-08-26 ruling: re-mint and retry ONCE, with the
    re-mint and the paid retry visibly recorded, and a second expiry inside one
    turn surfaces the standard refusal rather than buying a third call. The
    re-mint carries `--retry-of <audit_ref>`, so the correlation exists on the
    BROKER's side of the seam too and a retry never reads as an unrelated
    second issuance.

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

THE PROGRAM IS DECLARED; THE VERBS ARE THE DECLARATION'S (task 2.6). This was
written while openProfiler was unbuilt, so it named the operation in a JSON
request document of its own invention and demanded an answer shape to match. The
declaration landed (`opensoft/openProfiler`, `docs/broker-cli.md`, main
`d0538c31`) and named six incompatibilities, recorded in tasks.md 0.2; this
module is now reconciled against it and proven against the real
`openprofiler-broker` binary.

What that means in practice, and where the line falls:

  * the BINDING still declares the program and its fixed leading arguments, so
    NO command path appears in this file and an operator who moves the broker
    changes a record rather than code;
  * the SUBCOMMANDS and FLAGS are the declaration's own closed vocabulary and
    are recorded here — `intake`/`mint`/`revoke`/`list`, `--binding`,
    `--provider`, `--auth-kind`, `--approved-by`, `--label`, `--reference`,
    `--retry-of`. They are not the operator's to respell: four argv templates in
    a settings file is four ways to get the declaration subtly wrong. Every
    constant below cites the section of `docs/broker-cli.md` it comes from;
  * the ANSWER shapes are the declaration's too, parsed EXACTLY (see
    `_answer_document`).
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
# THE DECLARED BROKER SURFACE (task 2.6; openProfiler `docs/broker-cli.md`)
#
# Every constant in this block is a quotation, not a choice. The citation on
# each names the section of the declaration it was read from, at openProfiler
# main `d0538c31`, and each is asserted against the real binary by
# `tests/ideation-dashboard/test_openprofiler_broker_e2e.py`.
# ---------------------------------------------------------------------------

#: § "CLI surface" — the operation is an argv SUBCOMMAND. CLOSED: the
#: declaration names four and this seam expresses four.
OPERATION_INTAKE = "intake"
OPERATION_MINT = "mint"
OPERATION_REVOKE = "revoke"
OPERATION_LIST = "list"
OPERATIONS: tuple[str, ...] = (
    OPERATION_INTAKE, OPERATION_MINT, OPERATION_REVOKE, OPERATION_LIST)

#: § "intake" and § "mint" — the declared flag names. Spelled once, here.
FLAG_BINDING = "--binding"
FLAG_PROVIDER = "--provider"
FLAG_AUTH_KIND = "--auth-kind"
FLAG_APPROVED_BY = "--approved-by"
FLAG_LABEL = "--label"
FLAG_REFERENCE = "--reference"
FLAG_RETRY_OF = "--retry-of"

#: § "Output discipline" — every answer object carries this `schema_version`.
BROKER_ANSWER_SCHEMA_VERSION = 1

#: § "intake" / "mint" / "revoke" / "list" — the answer kinds.
BROKER_INTAKE_KIND = "openprofiler_broker_intake"
BROKER_MINT_KIND = "openprofiler_broker_mint"
BROKER_REVOCATION_KIND = "openprofiler_broker_revocation"
BROKER_REFERENCE_LIST_KIND = "openprofiler_broker_reference_list"

#: § "intake" — the intake answer's keys, EXACTLY. `label` is present and null
#: when none was given, so it is a key of every answer rather than an optional
#: one. The credential appears in none of them, which is the point of storing
#: exactly this.
INTAKE_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "reference", "binding", "provider", "auth_kind",
    "label", "created_at", "max_lifetime_seconds", "issued_by", "approved_by",
    "audit_ref")

#: § "mint" — the mint answer's keys, EXACTLY. NEITHER `endpoint` NOR `dialect`
#: is here, and that is the declaration's deliberate refusal to name a route it
#: would then be accountable for (0.2 FINDING 3): both facts come from the
#: BINDING. `retry_of` is present and null on a first mint.
MINT_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "reference", "binding", "provider", "auth_kind",
    "token", "token_type", "issued_at", "expires_at", "expires_in_seconds",
    "scope", "issued_by", "approved_by", "audit_ref", "retry_of",
    "enforcement")

#: § "revoke" — the revocation answer's keys, EXACTLY.
REVOCATION_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "reference", "binding", "provider", "auth_kind",
    "revoked", "revoked_at", "audit_ref")

#: § "list" — the reference-index answer's keys, EXACTLY.
REFERENCE_LIST_FIELDS: tuple[str, ...] = (
    "schema_version", "kind", "references")

#: The dialect vocabulary, READ FROM THE BINDING MODULE that now declares it
#: (0.2 FINDING 3: the route is the consumer's fact, so the record that carries
#: it is the record that validates it). Aliased rather than respelled so the two
#: modules cannot drift into two vocabularies. An unknown dialect is refused
#: when an operator DECLARES the binding — earlier than a mint, and earlier than
#: a paid call.
DIALECT_XFACTORY_PROMPT_V1 = binding_mod.DIALECT_XFACTORY_PROMPT_V1
DIALECTS: tuple[str, ...] = binding_mod.DIALECTS

#: How long a broker invocation may take. A mint is a local process doing local
#: custody work; a broker that cannot answer in this long is a broker that
#: cannot answer.
BROKER_TIMEOUT_SECONDS = 30.0

#: The largest answer a broker may write. A bound, not a policy: an unbounded
#: read of a child's stdout is a way to spend this process's memory by
#: misconfiguring a binding.
MAX_BROKER_ANSWER_BYTES = 65_536

#: The largest PROVIDER answer this client will read, bounding what was an
#: unbounded `response.read()` (PR #392 review note b). REUSED rather than
#: newly chosen: `doxbench_model.SERVER_MAX_OUTPUT_LIMIT_BYTES` is this server's
#: own declared output ceiling, and a body larger than the largest answer the
#: seam could ever accept is a body there is no reason to page into memory. An
#: overflow lands on the same fixed `DIAG_PROVIDER_MALFORMED` every other
#: unusable provider answer lands on — a body this client cannot use is
#: malformed for its purposes, and inventing a tenth sentence for it would tell
#: a caller something the redaction discipline says it must not.
MAX_PROVIDER_ANSWER_BYTES = model_mod.SERVER_MAX_OUTPUT_LIMIT_BYTES

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
#: EIGHT, not the nine this set held before the reconciliation.
#: `DIAG_DIALECT_UNKNOWN` is gone because the fact it guarded moved: the dialect
#: is the BINDING's, validated against the closed vocabulary when the operator
#: declares it (`doxbench_binding.ModelProviderBinding.__post_init__`), so an
#: unknown grammar can no longer reach a mint. Keeping a sentence here that no
#: path can raise would be a refusal nobody can trigger, asserted by a test that
#: proves nothing.
FIXED_DIAGNOSTICS: frozenset[str] = frozenset({
    DIAG_BROKER_UNREACHABLE, DIAG_BROKER_REFUSED, DIAG_BROKER_MALFORMED,
    DIAG_BROKER_TIMEOUT, DIAG_PROVIDER_UNREACHABLE,
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
    of those routes discloses the same nothing.

    ``endpoint`` and ``dialect`` come from the BINDING and ``audit_ref`` from
    the mint answer. The audit reference is DISCLOSABLE by construction — the
    declaration records no token material against it, not the token, not a
    prefix, not a hash — and it is carried because the re-mint passes it as
    ``--retry-of`` so the broker's own trail shows one turn that needed two
    tokens rather than two unrelated issuances (0.2 FINDING 5)."""

    token: str
    expires_at: float
    endpoint: str
    dialect: str
    audit_ref: str

    def __repr__(self) -> str:
        return (f"MintedToken(token=<redacted>, expires_at={self.expires_at!r},"
                f" endpoint={self.endpoint!r}, dialect={self.dialect!r},"
                f" audit_ref={self.audit_ref!r})")

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


def subprocess_broker_runner(argv, *, source=None,
                             timeout: float = BROKER_TIMEOUT_SECONDS) -> str:
    """Run one declared broker invocation and return its standard output.

    THE STDIN CONTRACT IS THE DECLARATION'S, and it is one thing rather than
    two (0.2 FINDING 2). `intake` reads standard input TO EOF and treats ALL of
    it as the secret, so an `intake` receives the credential and NOTHING ELSE —
    no request line, no framing, no trailing byte this module chose. Every other
    operation reads no standard input at all, and this function closes the pipe
    immediately for them, which is what the declaration says a caller may do.

    The credential is STREAMED, not read: `shutil.copyfileobj` moves it in
    chunks from the operator's handle to the child's pipe, so the whole value
    never becomes a string in this process and there is no variable holding it
    to outlive the call.

    A BROKEN PIPE IS A REFUSAL ARRIVING, NOT A BROKER THAT WOULD NOT START
    (0.2 FINDING 6). The declaration obliges a consumer to treat `EPIPE` on that
    write as "read the refusal": some invocations are refused BEFORE standard
    input is read at all — an `--auth-kind oauth` intake is refused that way on
    purpose, so a grant never enters a process that cannot store it correctly —
    and the child may have exited before the write completes. So the write error
    is swallowed and the ANSWER is taken from where the declaration says it
    lives: the exit code and what the child wrote. A broker that could not be
    STARTED is a different fact, raised from `Popen` itself, and keeps the
    different sentence.

    The child's environment is the same scrubbed allowlist the harness bridge
    already uses (`doxbench_bridge.INHERITED_ENVIRONMENT`), reused rather than
    respelled: a broker inherits a PATH and a HOME and nothing else, so no
    credential-shaped variable of this process's environment can reach it and
    no accident can turn an ambient variable into an implicit credential. HOME
    is how the declaration's own default custody root
    (`~/.openprofiler/broker`) resolves, so the allowlist already carries
    everything a broker needs and nothing it does not.

    Stderr is DISCARDED AT THE DESCRIPTOR (DEVNULL, PR #392 review note): a
    broker's own words must never reach a caller, inheriting this process's
    stderr would put them on the console, and capturing them into a pipe would
    make this process's memory a function of how noisy a declared program
    chooses to be. The kernel drops them instead, unread by construction."""
    try:
        child = subprocess.Popen(  # noqa: S603 - argv from a declared binding plus the declared subcommand, never a shell string
            list(argv),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=bridge_mod.child_environment(os.environ),
            text=True,
        )
    except (OSError, ValueError) as error:
        raise BrokerRefused(DIAG_BROKER_UNREACHABLE) from error
    try:
        try:
            if source is not None:
                # The credential's ONLY path through this process: handle to
                # pipe, in chunks, never assembled.
                shutil.copyfileobj(source, child.stdin)
            child.stdin.close()
        except BrokenPipeError:
            # THE REFUSAL ARRIVING. Nothing is raised here; the exit code and
            # the child's own answer are read below, exactly as the declaration
            # instructs. The close is still attempted so the descriptor is not
            # left to a garbage collector, and its own broken pipe is dropped
            # for the same reason the first one was.
            try:
                child.stdin.close()
            except OSError:
                pass
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


def broker_operation_argv(binding, operation: str, *,
                          retry_of: str | None = None) -> tuple[str, ...]:
    """The whole argv for one DECLARED operation: the binding's base invocation,
    then the subcommand and its declared flags.

    ONE function for all four, so the declaration's vocabulary is recorded in
    one readable place and a test can assert every operation against
    `docs/broker-cli.md` without spawning anything. It builds no command PATH —
    that is the binding's — and it names no flag the declaration does not.

    NO FLAG HERE CAN CARRY A SECRET, and that is structural rather than
    careful: every value comes from a field of the binding, the binding has no
    secret field to read, and the declaration refuses a credential-shaped flag
    on every command with its own `secret_in_argv` code. Two independent
    refusals, agreeing."""
    if operation not in OPERATIONS:
        raise AssertionError(
            f"{operation!r} is outside the broker's declared operation "
            f"vocabulary {OPERATIONS}")
    argv = list(binding.substituted_argv())
    if operation == OPERATION_INTAKE:
        argv += [OPERATION_INTAKE,
                 FLAG_BINDING, binding.id,
                 FLAG_PROVIDER, binding.provider,
                 FLAG_AUTH_KIND, binding.auth_kind,
                 FLAG_APPROVED_BY, binding.approved_by,
                 FLAG_LABEL, binding.label]
    elif operation == OPERATION_MINT:
        argv += [OPERATION_MINT, FLAG_REFERENCE, binding.credential_ref]
        if retry_of is not None:
            argv += [FLAG_RETRY_OF, retry_of]
    elif operation == OPERATION_REVOKE:
        argv += [OPERATION_REVOKE, FLAG_REFERENCE, binding.credential_ref]
    else:
        argv += [OPERATION_LIST]
    return tuple(argv)


def _answer_document(text: object, kind: str, fields) -> dict:
    """One broker answer, parsed against the declared shape EXACTLY.

    EXACTLY MEANS EXACTLY (PR #392 review note a). This used to demand that
    every named field be PRESENT and tolerate any others beside them, while its
    own comment claimed "the required keys, exactly" — the docstring was the
    stricter of the two, and the code was the one that mattered. The declaration
    says a successful command writes ONE JSON object whose fields it enumerates,
    so an object carrying a key the declaration does not name is not this
    broker's answer, and reading a token out of it would be reading a document
    written against a contract this parser has not been shown.

    THE COST IS STATED RATHER THAN HIDDEN: a future broker that adds a field
    without moving `schema_version` refuses here instead of being tolerated. That
    is the right way round for a document that carries a credential — an
    unrecognised answer shape is exactly when a consumer should stop — and the
    fix is this repository reading the newer declaration, which is a code change
    because the PARSER is what changed, not the operator's binding."""
    if not isinstance(text, str):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    try:
        document = json.loads(text)
    except (ValueError, TypeError) as error:
        raise BrokerRefused(DIAG_BROKER_MALFORMED) from error
    if not isinstance(document, dict):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if document.get("schema_version") != BROKER_ANSWER_SCHEMA_VERSION:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if document.get("kind") != kind:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    if set(document) != set(fields):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return document


def _declared_string(document: Mapping, field: str) -> str:
    value = document[field]
    if not isinstance(value, str) or not value.strip():
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return value


# ---------------------------------------------------------------------------
# the credential hand-off (task 1.3)
# ---------------------------------------------------------------------------


def hand_off_credential(binding, source, *,
                        runner=subprocess_broker_runner) -> str:
    """Hand a human's credential to the broker's `intake` and keep only the
    reference.

    `source` is an OPEN HANDLE the caller supplies — `sys.stdin`, a pipe, a
    test's `io.StringIO` — and never a string. That signature is the enforcement
    rather than a convention: a caller cannot pass a credential VALUE to this
    function, so no caller can be holding one either, and the value's whole
    journey is handle to pipe to broker.

    THE HANDLE IS THE WHOLE OF STANDARD INPUT (0.2 FINDING 2). `intake` reads to
    EOF and treats everything it read as the secret, so nothing is written
    before the credential and nothing after it. Every fact the operation needs —
    the binding id, the provider, the auth kind, the approver, the label — rides
    the declared FLAGS, where a fact belongs and a secret may not.

    Returns the `reference` the broker gives back — the declaration's own field
    name (0.2 FINDING 4). That reference is the only thing that then lives in a
    binding, in a file, in a log or in a review."""
    answer = runner(broker_operation_argv(binding, OPERATION_INTAKE),
                    source=source)
    document = _answer_document(answer, BROKER_INTAKE_KIND, INTAKE_FIELDS)
    return _declared_string(document, "reference")


# ---------------------------------------------------------------------------
# minting (task 2.1)
# ---------------------------------------------------------------------------


def mint(binding, *, retry_of: str | None = None,
         runner=subprocess_broker_runner) -> MintedToken:
    """Ask the broker for a short-lived token.

    Returns the token IN MEMORY. Nothing in this function writes it, and its
    only caller is the port below, which holds at most one at a time.

    `retry_of` is the `audit_ref` of the mint this one REPLACES, passed as the
    declared `--retry-of` so the broker's audit trail correlates a mid-turn
    re-mint with the issuance it replaced (Brett's 0.3 ruling; 0.2 FINDING 5).
    It is `None` on a first mint, which is also what the broker records.

    WHERE the token is good and WHAT GRAMMAR that endpoint speaks come from the
    BINDING, not from this answer: the declaration emits neither and says why —
    the broker is provider-agnostic about the request grammar and will not name
    an endpoint it would then be accountable for (0.2 FINDING 3)."""
    answer = runner(broker_operation_argv(binding, OPERATION_MINT,
                                          retry_of=retry_of))
    document = _answer_document(answer, BROKER_MINT_KIND, MINT_FIELDS)
    return MintedToken(
        token=_declared_string(document, "token"),
        expires_at=_parse_expires_at(document["expires_at"]),
        endpoint=binding.endpoint,
        dialect=binding.dialect,
        audit_ref=_declared_string(document, "audit_ref"))


def revoke(binding, *, runner=subprocess_broker_runner) -> str:
    """Destroy the broker's custody of this binding's credential.

    Returns the revocation's own `audit_ref`. The declaration keeps the audit
    trail through a revocation and refuses an unknown reference rather than
    answering silently, so "there was nothing there" and "it is gone now" stay
    different answers — and both reach a caller here as the same fixed refusal
    or the same returned reference, never as the broker's own words."""
    answer = runner(broker_operation_argv(binding, OPERATION_REVOKE))
    document = _answer_document(answer, BROKER_REVOCATION_KIND,
                                REVOCATION_FIELDS)
    if document["revoked"] is not True:
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return _declared_string(document, "audit_ref")


def list_references(binding, *, runner=subprocess_broker_runner) -> list:
    """The broker's NON-SECRET reference index, as the declaration returns it.

    Safe to read and safe to print: `list` never opens a custody file, and the
    index it reads carries no credential material. Returned as the declaration's
    own list of entries rather than reshaped, because a consumer that reshapes
    an index it does not own invents a second contract for it."""
    answer = runner(broker_operation_argv(binding, OPERATION_LIST))
    document = _answer_document(answer, BROKER_REFERENCE_LIST_KIND,
                                REFERENCE_LIST_FIELDS)
    references = document["references"]
    if not isinstance(references, list):
        raise BrokerRefused(DIAG_BROKER_MALFORMED)
    return references


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
    handler might echo), and not in this function's return value.

    THE ANSWER IS BOUNDED (PR #392 review note b). `response.read()` with no
    argument reads until the peer stops sending, which makes the memory of this
    process a function of what a declared endpoint chooses to send — and the
    endpoint is a binding's declaration, so a misdeclared one was enough. One
    byte over `MAX_PROVIDER_ANSWER_BYTES` is read deliberately, so an answer
    that is exactly at the bound is still honoured while one past it is
    detected rather than truncated into a shorter document that would parse."""
    body = json.dumps({
        PROVIDER_REQUEST_MODEL_FIELD: model_id,
        PROVIDER_REQUEST_PROMPT_FIELD: prompt,
    }).encode("utf-8")
    request = urllib.request.Request(  # noqa: S310 - endpoint declared on the binding by its operator, carried on the minted token
        token.endpoint, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {token.token}")
    try:
        with opener(request, timeout=timeout) as response:
            payload = response.read(MAX_PROVIDER_ANSWER_BYTES + 1)
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
    if not isinstance(payload, (bytes, bytearray)):
        raise BrokerRefused(DIAG_PROVIDER_MALFORMED)
    if len(payload) > MAX_PROVIDER_ANSWER_BYTES:
        # TRUNCATED IS NOT PARSED. The extra byte proves the overflow and the
        # document is dropped whole rather than decoded — a prefix of a JSON
        # body is not a smaller answer, it is a different one.
        raise BrokerRefused(DIAG_PROVIDER_MALFORMED)
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
    binding id, a reason from the closed vocabulary above, when it happened, and
    the mint's `audit_ref`. That is what makes it safe to disclose, which is the
    whole point of recording it — Brett's 2026-08-26 ruling is that a re-mint
    and the paid retry it buys are VISIBLE, and a record nobody may show would
    not satisfy it.

    THE `audit_ref` IS DISCLOSABLE BY CONSTRUCTION and is carried since the
    reconciliation (task 2.6): the declaration records no token material against
    an audit reference — not the token, not a prefix, not a hash — and it is the
    identifier the broker's own trail is keyed by. So a reader of this ledger
    and a reader of `broker-audit.jsonl` can be shown to be reading about the
    same issuance, which is what makes "visibly recorded" mean something on both
    sides of the seam rather than only on this one. `None` on the
    `paid_retry` event, which records the CALL rather than an issuance."""

    binding_id: str
    reason: str
    at: float
    audit_ref: str | None = None

    def as_dict(self) -> dict:
        return {"binding_id": self.binding_id, "reason": self.reason,
                "at": self.at, "audit_ref": self.audit_ref}


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
            decision this ruling refused to leave implicit. THE RE-MINT CARRIES
            `--retry-of <audit_ref>` (task 2.6, 0.2 FINDING 5), so the broker's
            audit trail shows one turn that needed two tokens instead of two
            unrelated issuances. The expired mint's reference is read off the
            token this turn is holding and lives no longer than the turn;
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
            # PER-TURN STATE, and no longer than the turn: the expired mint's
            # own audit reference, read before the token is dropped, so the
            # re-mint can name what it replaces.
            replaced = token.audit_ref
            self._forget_token()
            self._notice(REMINT_NOTICE + "\n")
            token = self._current_token(REASON_EXPIRY_REMINT,
                                        retry_of=replaced)
            self._record(REASON_PAID_RETRY)
            try:
                prose = _post_to_provider(
                    token, model_id=model_id, prompt=prompt,
                    timeout=self._timeout_seconds, opener=self._opener)
            except _TokenExpired:
                self._forget_token()
                raise BrokerRefused(DIAG_TOKEN_EXPIRED_TWICE) from None
        return {"assistant_prose": prose, "proposals": []}

    # -- token custody ------------------------------------------------------

    def _current_token(self, reason: str, *,
                       retry_of: str | None = None) -> MintedToken:
        """The live token, minting one when there is none or the one held has
        passed the broker's declared expiry (discard-on-expiry, task 2.4).

        `retry_of` names the mint this one REPLACES and is passed to the broker
        as `--retry-of`. It is set only on the mid-turn re-mint the 0.3 ruling
        is about. DISCARD-ON-EXPIRY PASSES NOTHING, deliberately: a token
        dropped before it was ever presented bought no provider call, so there
        is no retry for the trail to correlate and claiming one would put a
        retry in the broker's audit record that never happened."""
        with self._lock:
            held = self._token
            if held is not None and not held.expired(self._clock()):
                return held
            self._token = None
            try:
                minted = mint(self._binding, retry_of=retry_of,
                              runner=self._runner)
            except BrokerRefused:
                self._mintable = False
                raise
            self._mintable = True
            self._token = minted
        self._record(reason, audit_ref=minted.audit_ref)
        return minted

    def _forget_token(self) -> None:
        with self._lock:
            self._token = None

    def _record(self, reason: str, *, audit_ref: str | None = None) -> None:
        event = MintEvent(binding_id=self._binding.id, reason=reason,
                          at=self._clock(), audit_ref=audit_ref)
        with self._lock:
            self.ledger.append(event)
            if len(self.ledger) > MAX_LEDGER_EVENTS:
                del self.ledger[:-MAX_LEDGER_EVENTS]

    def __repr__(self) -> str:
        return (f"BrokeredProviderPort(binding={self._binding.id!r}, "
                f"mintable={self._mintable}, "
                f"token={'held' if self._token is not None else 'none'})")
