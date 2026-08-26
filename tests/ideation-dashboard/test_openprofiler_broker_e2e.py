"""THE SEAM AGAINST THE REAL BROKER (add-model-provider-broker task 2.6).

Everything else in this lane drives a broker child THIS repository writes, which
is the right way to exercise a stdin/stdout contract's failure modes and the
wrong way to find out whether the contract is the one openProfiler actually
declares. Task 0.2's cross-check found six incompatibilities exactly because
nothing here had ever met the real program; a fake that agrees with the adapter
proves the adapter agrees with itself.

So this file drives `openprofiler-broker` — the real binary, built from
`opensoft/openProfiler` — through the whole custody lifecycle the dashboard
uses:

    intake a sentinel secret  ->  mint  ->  a mid-turn expiry that re-mints
    with `--retry-of`  ->  the broker's own audit trail  ->  revoke

and then greps the broker's store for the sentinel. The credential must appear
in exactly one place while it is held (`custody/<reference>.json`, the
declaration's ONLY secret-bearing file) and nowhere at all once it is revoked.

IT SKIPS WHEN THE BINARY IS ABSENT, with a reason that says how to get one. CI
has no Rust toolchain and no reason to grow one: this repository is the CONSUMER
of that declaration, and the binary is another repository's build artefact. The
skip is not a softened assertion — every claim below is exact, and the file is
run against the real program before the seam is called reconciled.

    Build it:  cargo build -p opensoft-open-profiler-broker --release
    Then:      PATH=<openProfiler>/target/release:$PATH python3 -m pytest ...
    Or:        OPENPROFILER_BROKER_BIN=<path>/openprofiler-broker python3 -m pytest ...

THE CUSTODY ROOT IS REDIRECTED THROUGH `HOME`, and that is a fact about the
seam rather than a test convenience. The broker resolves its store from
`OPENPROFILER_BROKER_HOME`, defaulting to `~/.openprofiler/broker`; the adapter
hands its child the same scrubbed allowlist the harness bridge uses
(`doxbench_bridge.INHERITED_ENVIRONMENT`), which carries `HOME` and `PATH` and
nothing else. So a test can point the store somewhere disposable exactly the way
an operator's own account already points it — and no environment widening was
needed to reach a real broker, which is worth proving rather than assuming.
"""

from __future__ import annotations

import dataclasses
import io
import json
import os
import shutil
import time
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (path setup)

from ideation_dashboard import doxbench_binding as binding_mod
from ideation_dashboard import doxbench_install as install_mod
from ideation_dashboard import doxbench_provider as provider_mod

#: The credential this test enrols. A SENTINEL: long, unique, and impossible to
#: produce by accident, so a sweep that finds it has found the real thing. On
#: the `api_key` path the declaration is explicit that the MINTED TOKEN IS THIS
#: VALUE VERBATIM, which is why the same sentinel proves both halves.
SENTINEL_SECRET = "sk-e2e-sentinel-DO-NOT-PERSIST-8b41c7d0e926af53"

#: The program name the declaration gives itself.
BROKER_PROGRAM = "openprofiler-broker"

#: An override for a build that is not on PATH.
BROKER_BIN_ENV = "OPENPROFILER_BROKER_BIN"

SKIP_REASON = (
    f"the real {BROKER_PROGRAM} is not on PATH and {BROKER_BIN_ENV} names no "
    "executable, so the seam cannot be measured against the program it "
    "consumes. Build it in an openProfiler checkout with "
    "`cargo build -p opensoft-open-profiler-broker --release` and put "
    "`target/release` on PATH (or point " + BROKER_BIN_ENV + " at the binary). "
    "Every other test in this lane drives a fake broker that speaks the same "
    "DECLARED contract, so the suite still covers the seam's behaviour — what "
    "it cannot cover without the binary is whether the declaration and the "
    "program agree.")

ENDPOINT = "https://provider.invalid/turn"


def _broker_binary() -> str | None:
    declared = os.environ.get(BROKER_BIN_ENV)
    if declared:
        path = Path(declared)
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
        return None
    return shutil.which(BROKER_PROGRAM)


BROKER_BINARY = _broker_binary()

pytestmark = pytest.mark.skipif(BROKER_BINARY is None, reason=SKIP_REASON)


# ---------------------------------------------------------------------------
# the fixtures: a disposable custody root, and a binding that names the binary
# ---------------------------------------------------------------------------


@pytest.fixture
def broker_home(tmp_path, monkeypatch) -> Path:
    """A disposable custody root, reached the way the seam reaches one."""
    home = tmp_path / "operator-home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home / ".openprofiler" / "broker"


@pytest.fixture
def binding(broker_home):
    """A binding naming the REAL broker, with no reference yet.

    `credential_ref` is reference-SHAPED but names nothing the store holds:
    intake does not read it, and the declaration refuses a malformed reference
    with a usage error distinct from an absent one, so a placeholder that is not
    reference-shaped would fail for the wrong reason later."""
    return binding_mod.ModelProviderBinding(
        id="openprofiler-e2e",
        label="openProfiler end-to-end",
        provider="e2e-provider",
        credential_ref="opref-" + "0" * 24,
        auth_kind="api_key",
        approved_by="brett@opensoft.one",
        endpoint=ENDPOINT,
        dialect=binding_mod.DIALECT_XFACTORY_PROMPT_V1,
        broker_argv=(BROKER_BINARY,),
    )


def _audit_records(broker_home: Path) -> list[dict]:
    """The broker's append-only trail, parsed line by line.

    Line by line WITHOUT LOCKING, as the declaration says a reader may: a record
    and its newline are handed to exactly one `write`, so two brokers appending
    at the same moment produce two whole lines and never one spliced line."""
    path = broker_home / "audit" / "broker-audit.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines() if line]


def _files_holding(root: Path, needle: str) -> list[str]:
    return sorted(path.relative_to(root).as_posix()
                  for path in root.rglob("*")
                  if path.is_file()
                  and needle in path.read_text(encoding="utf-8",
                                               errors="replace"))


class _Opener:
    """A scripted stand-in for `urllib.request.urlopen`.

    The PROVIDER is not real here and must not be: this file is about the seam
    between the dashboard and the broker, and a real paid provider call is
    neither available to a test nor something a test should buy."""

    def __init__(self, *outcomes):
        self._outcomes = list(outcomes)
        self.requests: list[object] = []

    def __call__(self, request, timeout=None):
        self.requests.append(request)
        outcome = (self._outcomes.pop(0) if self._outcomes
                   else {"assistant_prose": "ok"})
        if isinstance(outcome, BaseException):
            raise outcome
        return _Response(json.dumps(outcome).encode("utf-8"))


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self, amount=None):
        return self._payload if amount is None else self._payload[:amount]

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


class _Envelope:
    def __init__(self, model_id="openprofiler-e2e", text="assembled prompt"):
        self.model_id = model_id
        self._text = text

    def rendered(self) -> str:
        return self._text


def _expired_error():
    import urllib.error
    return urllib.error.HTTPError(
        ENDPOINT, 401, "Unauthorized", {},
        io.BytesIO(b'{"provider":"leaky detail that must never surface"}'))


# ---------------------------------------------------------------------------
# the declared answer shapes, measured against the program
# ---------------------------------------------------------------------------


def test_the_declared_answer_fields_are_exactly_what_the_binary_emits(
        binding, broker_home):
    """The four field tuples this adapter parses against are QUOTATIONS from
    `docs/broker-cli.md`. This is the test that keeps them honest: it reads the
    real program's own answers and compares the key sets, so a quotation that
    drifted from the declaration fails here rather than at an operator's first
    mint.

    It is also what makes the EXACT parse defensible (PR #392 review note a):
    exactness is only safe if the enumerated set is the real one, and this
    measures it rather than trusting the transcription."""
    intake = json.loads(provider_mod.subprocess_broker_runner(
        provider_mod.broker_operation_argv(
            binding, provider_mod.OPERATION_INTAKE),
        source=io.StringIO(SENTINEL_SECRET)))
    assert set(intake) == set(provider_mod.INTAKE_FIELDS)
    assert intake["kind"] == provider_mod.BROKER_INTAKE_KIND

    held = dataclasses.replace(binding, credential_ref=intake["reference"])
    mint = json.loads(provider_mod.subprocess_broker_runner(
        provider_mod.broker_operation_argv(held, provider_mod.OPERATION_MINT)))
    assert set(mint) == set(provider_mod.MINT_FIELDS)
    assert mint["kind"] == provider_mod.BROKER_MINT_KIND
    # 0.2 FINDING 3, measured rather than quoted: the mint answer names no
    # route, so the binding is the only place one can come from.
    assert "endpoint" not in mint
    assert "dialect" not in mint

    listed = json.loads(provider_mod.subprocess_broker_runner(
        provider_mod.broker_operation_argv(held, provider_mod.OPERATION_LIST)))
    assert set(listed) == set(provider_mod.REFERENCE_LIST_FIELDS)

    revocation = json.loads(provider_mod.subprocess_broker_runner(
        provider_mod.broker_operation_argv(held,
                                           provider_mod.OPERATION_REVOKE)))
    assert set(revocation) == set(provider_mod.REVOCATION_FIELDS)
    assert revocation["kind"] == provider_mod.BROKER_REVOCATION_KIND


def test_an_oauth_intake_is_refused_before_the_secret_is_read(binding,
                                                              broker_home):
    """0.2 FINDING 6 against the REAL program. The declaration refuses an
    `--auth-kind oauth` intake with exit 5 BEFORE reading standard input, on
    purpose, so a grant never enters a process that cannot store it correctly —
    and a consumer writing a credential to that child sees a broken pipe.

    The adapter must read that as the refusal it is. A credential large enough
    to overflow the pipe buffer is used so the write really fails rather than
    landing in the kernel's buffer; either way the answer is the exit code."""
    oauth = dataclasses.replace(binding, auth_kind="oauth")
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.hand_off_credential(
            oauth, io.StringIO("x" * 4_000_000))
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_REFUSED
    assert caught.value.diagnostic != provider_mod.DIAG_BROKER_UNREACHABLE
    # and nothing was taken into custody
    assert not (broker_home / "custody").exists() or not list(
        (broker_home / "custody").iterdir())


# ---------------------------------------------------------------------------
# THE LIFECYCLE
# ---------------------------------------------------------------------------


def test_the_whole_custody_lifecycle_against_the_real_broker(binding,
                                                             broker_home,
                                                             tmp_path):
    """intake -> mint -> mid-turn expiry -> re-mint with `--retry-of` -> the
    broker's audit trail -> revoke, and the sentinel's whereabouts at every
    step."""
    # --- INTAKE: the credential crosses to the broker and nothing else ------
    started = time.time()
    reference = provider_mod.hand_off_credential(
        binding, io.StringIO(SENTINEL_SECRET))
    assert reference.startswith("opref-"), reference
    assert len(reference) == len("opref-") + 24
    held = dataclasses.replace(binding, credential_ref=reference)

    # THE SENTINEL IS IN EXACTLY ONE FILE, the one the declaration names as the
    # only secret-bearing one. Not the index, not the audit trail, not a log.
    assert _files_holding(broker_home, SENTINEL_SECRET) == [
        f"custody/{reference}.json"]
    assert (broker_home / "references.json").is_file()
    assert SENTINEL_SECRET not in (
        broker_home / "references.json").read_text(encoding="utf-8")

    intake_records = [record for record in _audit_records(broker_home)
                      if record["event"] == "intake"]
    assert len(intake_records) == 1
    assert intake_records[0]["binding"] == binding.id, \
        "the consumer's own binding id is carried into the trail, so the two " \
        "sides correlate"
    assert intake_records[0]["approved_by"] == binding.approved_by
    assert SENTINEL_SECRET not in json.dumps(intake_records)

    # --- MINT: the token, its expiry, and the audit reference ---------------
    minted = provider_mod.mint(held)
    # On the api_key path the declaration is explicit: the minted token IS the
    # stored key, verbatim. It says so rather than burying it, and this asserts
    # the consumer is not being handed something else.
    assert minted.token == SENTINEL_SECRET
    assert minted.audit_ref.startswith("opaud-")
    assert len(minted.audit_ref) == len("opaud-") + 24
    # `expires_at` is HONOURED: the default maximum lifetime is 300 seconds,
    # and the token is live now and dead after it.
    assert 240 <= minted.expires_at - started <= 360, minted.expires_at
    assert minted.expired(minted.expires_at + 1) is True
    assert minted.expired(minted.expires_at - 1) is False
    # the route came from the BINDING, because the mint answer carries none
    assert minted.endpoint == binding.endpoint
    assert minted.dialect == binding.dialect
    # ...and the token is still in exactly one file on disk
    assert _files_holding(broker_home, SENTINEL_SECRET) == [
        f"custody/{reference}.json"]

    # --- A MID-TURN EXPIRY: re-mint and retry once, correlated --------------
    printed: list[str] = []
    opener = _Opener(_expired_error(), {"assistant_prose": "the retried answer"})
    port = provider_mod.BrokeredProviderPort(
        held, install_mod.brokered_catalog(held),
        opener=opener, notice=printed.append)
    assert port.dispatch(_Envelope()) == {
        "assistant_prose": "the retried answer", "proposals": []}
    assert len(opener.requests) == 2, "exactly one paid retry"
    assert [event.reason for event in port.ledger] == [
        provider_mod.REASON_FIRST_MINT,
        provider_mod.REASON_EXPIRY_REMINT,
        provider_mod.REASON_PAID_RETRY,
    ]
    assert printed and "re-minted once and retried" in printed[0]

    first_mint_ref = port.ledger[0].audit_ref
    remint_ref = port.ledger[1].audit_ref
    assert first_mint_ref and remint_ref and first_mint_ref != remint_ref

    # THE BROKER'S OWN TRAIL SHOWS THE CORRELATION (0.2 FINDING 5). Not this
    # process's ledger — the broker's `broker-audit.jsonl`, written by the
    # program, which is the half of the ruling that could not be discharged
    # until the seam passed `--retry-of`.
    mints = [record for record in _audit_records(broker_home)
             if record["event"] == "mint"]
    assert len(mints) == 3, [record["audit_ref"] for record in mints]
    assert mints[0]["retry_of"] is None, "the standalone mint replaced nothing"
    assert mints[1]["retry_of"] is None, "the turn's first mint replaced nothing"
    correlated = mints[2]
    assert correlated["audit_ref"] == remint_ref
    assert correlated["retry_of"] == first_mint_ref, \
        "the retry is visible in the broker's trail rather than reading as an " \
        "unrelated second issuance"
    assert SENTINEL_SECRET not in json.dumps(mints), \
        "no token material is recorded: not the token, not a prefix, not a hash"

    # --- DISCARD-ON-EXPIRY against the broker's OWN declared expiry ---------
    # A clock past `expires_at` is what the ruling's unconditional half turns
    # on, and the expiry it is measured against is the real broker's, not one
    # this client assumed.
    far_future = minted.expires_at + 10_000
    aged = provider_mod.BrokeredProviderPort(
        held, install_mod.brokered_catalog(held),
        opener=_Opener({"assistant_prose": "a"}, {"assistant_prose": "b"}),
        clock=lambda: far_future, notice=lambda _text: None)
    aged.dispatch(_Envelope())
    aged.dispatch(_Envelope())
    assert [event.reason for event in aged.ledger] == [
        provider_mod.REASON_FIRST_MINT, provider_mod.REASON_FIRST_MINT], \
        "a token known to be dead is never presented; each turn mints afresh"
    assert len({event.audit_ref for event in aged.ledger}) == 2
    # a discard is NOT a retry, so nothing it minted claims to replace anything
    assert [record["retry_of"] for record in _audit_records(broker_home)
            if record["event"] == "mint"][-2:] == [None, None]

    # --- LIST: the non-secret index, which never opens a custody file -------
    listed = provider_mod.list_references(held)
    assert [entry["reference"] for entry in listed] == [reference]
    assert listed[0]["binding"] == binding.id
    assert SENTINEL_SECRET not in json.dumps(listed)

    # --- REVOKE: custody is destroyed and the trail survives ----------------
    revocation_ref = provider_mod.revoke(held)
    assert revocation_ref.startswith("opaud-")
    assert provider_mod.list_references(held) == []

    # THE SENTINEL IS NOW NOWHERE — not in the store, not in the audit trail
    # that outlives it, and not anywhere else this test wrote.
    assert _files_holding(broker_home, SENTINEL_SECRET) == []
    assert _files_holding(tmp_path, SENTINEL_SECRET) == []
    assert _audit_records(broker_home), "revocation does not erase the trail"
    assert [record["event"] for record in _audit_records(broker_home)][-1] == \
        "revoke"
    assert SENTINEL_SECRET not in json.dumps(_audit_records(broker_home))

    # --- and a mint against a revoked reference refuses ---------------------
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(held)
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_REFUSED
    assert reference not in str(caught.value), \
        "the refusal is fixed and redacted; the broker's own words are dropped"
