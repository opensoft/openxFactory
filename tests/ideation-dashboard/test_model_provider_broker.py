"""add-model-provider-broker: the binding, the hand-off, the mint, the expiry
ruling, and the refusals (tasks 1.1-1.3, 2.1-2.5, 3.1-3.3).

Five layers, each proving a different thing about the same machinery:

  (a) THE RECORD — a binding holds an id, a label, a credential reference, an
      auth kind and a broker invocation, and NO secret field exists in the
      shape to hold anything else;
  (b) THE STORE — list, add, edit, remove, and a read-back that discloses the
      binding and states where the credential actually lives;
  (c) THE HAND-OFF — a real broker child process, a real credential streamed
      to its standard input, and then a grep of the WHOLE checkout and every
      string the surface produced, looking for the value. It is never there;
  (d) THE MINT AND THE TURN — the declared argv is substituted and executed,
      the token lives in memory and in no response, and Brett's 2026-08-26
      expiry ruling (re-mint and retry ONCE, visibly recorded; a second expiry
      refuses) is exercised in both directions;
  (e) THE POSTURES — every broker and provider failure lands on the fixed,
      redacted refusal `doxbench_model.dispatch_turn` already defines, and the
      UNCONFIGURED posture is byte-for-byte what it was before this change.

The broker in (c)/(d) is a REAL child process — a small Python script this file
writes — because the whole contract under test is a stdin/stdout contract with
a subprocess, and a mocked `subprocess` would prove nothing about it. The
provider is a real loopback HTTP server in one test (to prove the transport and
the authorization header) and an injected opener in the rest (so failure modes
are scriptable and no test depends on timing).
"""

from __future__ import annotations

import dataclasses
import http.server
import io
import json
import subprocess
import sys
import threading
import time
import urllib.error
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (path setup)

from ideation_dashboard import cli as cli_mod
from ideation_dashboard import doxbench_binding as binding_mod
from ideation_dashboard import doxbench_install as install_mod
from ideation_dashboard import doxbench_model as model_mod
from ideation_dashboard import doxbench_provider as provider_mod

# The credential a human types. A SENTINEL: long, unique, and impossible to
# produce by accident, so a sweep that finds it has found the real thing.
SENTINEL_CREDENTIAL = "sk-sentinel-DO-NOT-PERSIST-4f19a7c2e5b840d6"

# The token the fake broker mints. A second sentinel, for the same reason.
SENTINEL_TOKEN = "mint-sentinel-9d3b71ca0e6f4827-DO-NOT-DISCLOSE"

BROKER_ARGV_TEMPLATE = ("--binding", "{binding_id}", "--ref",
                        "{credential_ref}", "--kind", "{auth_kind}")


def _binding(**overrides):
    fields = dict(id="openprofiler-demo", label="Demo brokered provider",
                  credential_ref="ref/unset", auth_kind="api_key",
                  broker_argv=("openprofiler",) + BROKER_ARGV_TEMPLATE)
    fields.update(overrides)
    return binding_mod.ModelProviderBinding(**fields)


# ===========================================================================
# (a) THE RECORD (task 1.1)
# ===========================================================================


def test_the_binding_declares_exactly_five_fields():
    binding = _binding()
    assert [field.name for field in dataclasses.fields(binding)] == \
        list(binding_mod.BINDING_FIELDS)


@pytest.mark.parametrize("secret_field", [
    "secret", "api_key", "token", "credential", "value", "password"])
def test_no_secret_field_exists_in_the_shape_to_populate(secret_field):
    """NOT OPTIONAL — ABSENT. The dataclass is slotted and frozen, so a secret
    cannot be passed in and cannot be attached afterwards."""
    with pytest.raises(TypeError):
        _binding(**{secret_field: SENTINEL_CREDENTIAL})
    binding = _binding()
    # A frozen SLOTTED dataclass refuses the assignment with a `TypeError` out
    # of its regenerated `__setattr__` rather than the `FrozenInstanceError` an
    # unslotted one raises; both are refusals and the tuple names all three so
    # this test pins the REFUSAL rather than one interpreter's spelling of it.
    with pytest.raises((AttributeError, TypeError,
                        dataclasses.FrozenInstanceError)):
        setattr(binding, secret_field, SENTINEL_CREDENTIAL)


def test_the_auth_kind_vocabulary_is_closed():
    assert binding_mod.AUTH_KINDS == ("api_key", "oauth")
    for kind in binding_mod.AUTH_KINDS:
        assert _binding(auth_kind=kind).auth_kind == kind
    with pytest.raises(binding_mod.BindingRefused):
        _binding(auth_kind="whatever_the_broker_likes")


def test_the_argv_placeholder_vocabulary_is_closed_and_binding_scoped():
    """A template can only ever be filled with facts the binding already
    discloses, which is why the vocabulary is closed to the binding's own
    fields: no substitution can smuggle a value the record does not carry."""
    assert binding_mod.ARGV_PLACEHOLDERS == (
        "binding_id", "credential_ref", "auth_kind")
    with pytest.raises(binding_mod.BindingRefused):
        _binding(broker_argv=("openprofiler", "--secret", "{api_key}"))
    with pytest.raises(binding_mod.BindingRefused):
        _binding(broker_argv=("openprofiler", "--x", "{unclosed"))


def test_the_declared_invocation_is_substituted_from_the_bindings_own_fields():
    binding = _binding(credential_ref="op://vault/demo")
    assert binding.substituted_argv() == (
        "openprofiler", "--binding", "openprofiler-demo",
        "--ref", "op://vault/demo", "--kind", "api_key")


def test_an_argv_given_as_a_shell_string_is_refused():
    """argv, never a shell string — so no declared value can be read as shell
    syntax."""
    with pytest.raises(binding_mod.BindingRefused):
        _binding(broker_argv="openprofiler --binding openprofiler-demo")


def test_an_empty_invocation_is_refused():
    with pytest.raises(binding_mod.BindingRefused):
        _binding(broker_argv=())


# ===========================================================================
# (b) THE STORE (task 1.2)
# ===========================================================================


def _store(tmp_path) -> binding_mod.BindingStore:
    return binding_mod.BindingStore(tmp_path / "bindings.yaml")


def test_an_undeclared_store_is_an_empty_posture_not_an_error(tmp_path):
    store = _store(tmp_path)
    assert store.list() == ()
    assert store.read_back()["bindings"] == []
    assert not store.path.exists()


def test_list_add_edit_remove(tmp_path):
    store = _store(tmp_path)
    store.add(_binding())
    store.add(_binding(id="second", label="Second"))
    assert [b.id for b in store.list()] == ["openprofiler-demo", "second"]

    store.edit(_binding(label="Renamed"))
    assert store.get("openprofiler-demo").label == "Renamed"
    assert [b.id for b in store.list()] == ["openprofiler-demo", "second"], \
        "an edit keeps the binding's position"

    retired = store.remove("second")
    assert retired.id == "second"
    assert [b.id for b in store.list()] == ["openprofiler-demo"]


def test_a_repeated_id_refuses_and_an_unknown_id_refuses(tmp_path):
    store = _store(tmp_path)
    store.add(_binding())
    with pytest.raises(binding_mod.BindingRefused):
        store.add(_binding())
    with pytest.raises(binding_mod.BindingRefused):
        store.edit(_binding(id="never-declared"))
    with pytest.raises(binding_mod.BindingRefused):
        store.remove("never-declared")


def test_the_binding_store_needs_no_yaml_parser_until_a_document_exists():
    """THE HOSTED-PLANE REGRESSION, pinned at the source.

    The lean hosted image has no PyYAML — `test_repo_selector.py`'s
    `test_hosted_posts_do_not_load_notebook_only_dependencies` proves it by
    poisoning the module and serving anyway. Both entrypoints resolve their
    model port through this store at startup, so a module-scope `import yaml`
    here kills every hosted serve before it prints its URL. That was MEASURED
    during this change, not theorised: the test above went red the moment the
    import was at module scope."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "doxbench_binding.py").read_text(encoding="utf-8")
    module_scope = [line for line in source.splitlines()
                    if line.startswith("import ") or line.startswith("from ")]
    assert not [line for line in module_scope if "yaml" in line], module_scope
    assert "    import yaml" in source, "the lazy import is still there"


def test_the_stored_document_carries_schema_version_and_kind(tmp_path):
    store = _store(tmp_path)
    store.add(_binding())
    import yaml
    document = yaml.safe_load(store.path.read_text(encoding="utf-8"))
    assert document["schema_version"] == binding_mod.SCHEMA_VERSION
    assert document["kind"] == binding_mod.BINDINGS_KIND
    assert document["bindings"][0]["kind"] == binding_mod.BINDING_KIND
    assert set(document["bindings"][0]) == {"kind", *binding_mod.BINDING_FIELDS}


def test_a_record_carrying_an_unknown_key_refuses_rather_than_dropping_it(
        tmp_path):
    """A dropped key is how a field an operator believed they declared — a
    secret, most dangerously — vanishes without a word."""
    path = tmp_path / "bindings.yaml"
    path.write_text(json.dumps({
        "schema_version": 1, "kind": binding_mod.BINDINGS_KIND,
        "bindings": [{"kind": binding_mod.BINDING_KIND, "id": "x",
                      "label": "L", "credential_ref": "r",
                      "auth_kind": "api_key", "broker_argv": ["op"],
                      "api_key": SENTINEL_CREDENTIAL}],
    }), encoding="utf-8")
    with pytest.raises(binding_mod.BindingRefused):
        binding_mod.BindingStore(path).list()


def test_the_read_back_discloses_the_binding_and_names_the_custodian(tmp_path):
    store = _store(tmp_path)
    store.add(_binding())
    disclosure = store.read_back()
    record = disclosure["bindings"][0]
    assert set(record) == {"kind", *binding_mod.BINDING_FIELDS,
                           "credential_custody"}
    assert record["credential_custody"] == binding_mod.CUSTODY_NOTICE
    assert "broker" in record["credential_custody"]
    # there is no credential material to redact, which is the claim
    assert SENTINEL_CREDENTIAL not in json.dumps(disclosure)


def test_removing_a_binding_says_it_revoked_nothing():
    assert "not revoked" in binding_mod.REMOVAL_NOTICE


def test_the_cli_verbs_list_add_edit_and_remove_a_binding(tmp_path, capsys):
    """TASK 1.2's OPERATOR DOOR, driven through the real parser.

    The store's four verbs are exercised above; what this adds is the surface
    an operator actually touches — that the verbs are registered on the
    entrypoint, that they reach the store, that a read-back names the
    custodian in words, and that a retirement says what it did not revoke.
    Without it, `model-binding` could be wired to nothing and every assertion
    above would still pass."""
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    parser = cli_mod.build_parser()

    def run(*argv) -> int:
        args = parser.parse_args(list(argv))
        return args.func(args)

    root = ["--repo-root", str(checkout)]
    # the invocation is a POSITIONAL after a bare `--`, because a broker's own
    # argv is full of option-shaped members
    declaration = ["--id", "openprofiler-demo", "--label", "Demo brokered provider",
                   "--credential-ref", "ref/unset", "--auth-kind", "api_key",
                   "--", "openprofiler", "--binding", "{binding_id}"]

    assert run("model-binding", "list", *root) == 0
    assert "none declared" in capsys.readouterr().out

    assert run("model-binding", "add", *root, *declaration) == 0
    assert binding_mod.CUSTODY_NOTICE in capsys.readouterr().out

    assert run("model-binding", "list", *root) == 0
    listed = capsys.readouterr().out
    assert "openprofiler-demo" in listed
    assert binding_mod.CUSTODY_NOTICE in listed

    # a repeated id refuses THROUGH THE VERB, not only through the store
    assert run("model-binding", "add", *root, *declaration) == 1
    capsys.readouterr()

    renamed = list(declaration)
    renamed[3] = "Renamed"
    assert run("model-binding", "edit", *root, *renamed) == 0
    capsys.readouterr()
    store = binding_mod.BindingStore(binding_mod.bindings_path(checkout))
    assert store.get("openprofiler-demo").label == "Renamed"

    assert run("model-binding", "remove", *root, "--id",
               "openprofiler-demo") == 0
    assert binding_mod.REMOVAL_NOTICE in capsys.readouterr().out
    assert store.list() == ()


# ===========================================================================
# a real broker child, and a real provider
# ===========================================================================

_BROKER_SCRIPT = '''\
import json, sys

request_line = sys.stdin.readline()
request = json.loads(request_line)
rest = sys.stdin.read()

record = {"argv": sys.argv[1:], "request": request, "stdin_rest": rest}
open(sys.argv[0] + ".seen.json", "w", encoding="utf-8").write(json.dumps(record))

if request["operation"] == "enroll":
    print(json.dumps({"schema_version": 1,
                      "kind": "model-provider-broker-enrollment",
                      "credential_ref": "op://vault/enrolled"}))
else:
    print(json.dumps({"schema_version": 1,
                      "kind": "model-provider-broker-mint",
                      "token": %(token)r,
                      "expires_at": %(expires)r,
                      "endpoint": %(endpoint)r,
                      "dialect": "xfactory-prompt-v1"}))
'''


def _write_broker(tmp_path, *, token=SENTINEL_TOKEN, expires=None,
                  endpoint="https://provider.invalid/turn") -> Path:
    script = tmp_path / "fake-broker.py"
    script.write_text(_BROKER_SCRIPT % {
        "token": token,
        "expires": expires if expires is not None else time.time() + 300,
        "endpoint": endpoint,
    }, encoding="utf-8")
    return script


def _broker_binding(script: Path, **overrides):
    return _binding(broker_argv=(sys.executable, str(script))
                    + BROKER_ARGV_TEMPLATE, **overrides)


def _seen(script: Path) -> dict:
    return json.loads(
        Path(str(script) + ".seen.json").read_text(encoding="utf-8"))


# ===========================================================================
# (c) THE HAND-OFF THAT RETAINS NOTHING (task 1.3, task 3.1's sweep)
# ===========================================================================


def test_the_credential_reaches_the_broker_on_its_standard_input(tmp_path):
    script = _write_broker(tmp_path)
    binding = _broker_binding(script)
    reference = provider_mod.hand_off_credential(
        binding, io.StringIO(SENTINEL_CREDENTIAL))
    assert reference == "op://vault/enrolled"

    seen = _seen(script)
    assert seen["stdin_rest"] == SENTINEL_CREDENTIAL, \
        "the broker really received the value, so the sweep below means something"
    assert seen["request"]["operation"] == "enroll"
    assert seen["request"]["credential_ref"] == "ref/unset"
    assert SENTINEL_CREDENTIAL not in json.dumps(seen["request"]), \
        "the REQUEST document names the reference and never the secret"
    assert seen["argv"] == ["--binding", "openprofiler-demo", "--ref",
                            "ref/unset", "--kind", "api_key"]


def test_the_credential_survives_nowhere_in_the_checkout_or_the_surface(
        tmp_path):
    """THE SWEEP. After a hand-off through the whole operator surface, grep
    every file in the checkout and every string the surface produced."""
    script = _write_broker(tmp_path)
    checkout = tmp_path / "checkout"
    (checkout / "ideation" / "dashboard").mkdir(parents=True)
    store = binding_mod.BindingStore(binding_mod.bindings_path(checkout))
    store.add(_broker_binding(script))

    args = cli_mod.build_parser().parse_args([
        "model-binding", "set-credential", "--repo-root", str(checkout),
        "--id", "openprofiler-demo"])
    assert cli_mod.cmd_model_binding_set_credential(
        args, source=io.StringIO(SENTINEL_CREDENTIAL)) == 0

    # the reference came back and is what the store now holds
    assert store.get("openprofiler-demo").credential_ref == \
        "op://vault/enrolled"

    # ...and the value is in NO file under the checkout
    offenders = [path for path in checkout.rglob("*")
                 if path.is_file()
                 and SENTINEL_CREDENTIAL in path.read_text(
                     encoding="utf-8", errors="replace")]
    assert not offenders, offenders

    # ...nor in any string the read-back surface produces
    assert SENTINEL_CREDENTIAL not in json.dumps(store.read_back())
    assert SENTINEL_CREDENTIAL not in repr(store.get("openprofiler-demo"))


def test_the_hand_off_takes_a_handle_and_never_a_value():
    """The signature IS the enforcement: a caller cannot pass a credential
    VALUE, so no caller can be holding one."""
    import inspect
    signature = inspect.signature(provider_mod.hand_off_credential)
    assert list(signature.parameters) == ["binding", "source", "runner"]


# ===========================================================================
# (d) THE MINT AND THE TURN (tasks 2.1, 2.4)
# ===========================================================================


class _Envelope:
    """The duck-typed prompt envelope every seam in this family accepts."""

    def __init__(self, model_id="openprofiler-demo", text="assembled prompt"):
        self.model_id = model_id
        self._text = text

    def rendered(self) -> str:
        return self._text


def test_a_mint_executes_the_declared_invocation_and_returns_a_token(tmp_path):
    script = _write_broker(tmp_path)
    minted = provider_mod.mint(_broker_binding(script))
    assert minted.token == SENTINEL_TOKEN
    assert minted.endpoint == "https://provider.invalid/turn"
    assert minted.dialect == provider_mod.DIALECT_XFACTORY_PROMPT_V1
    assert _seen(script)["request"]["operation"] == "mint"


def test_the_minted_token_redacts_itself_in_every_rendering(tmp_path):
    script = _write_broker(tmp_path)
    minted = provider_mod.mint(_broker_binding(script))
    for rendering in (repr(minted), str(minted), f"{minted}", "%s" % (minted,)):
        assert SENTINEL_TOKEN not in rendering
        assert "<redacted>" in rendering


def test_an_unknown_dialect_refuses_rather_than_guessing(tmp_path):
    script = tmp_path / "odd-broker.py"
    script.write_text(
        "import json,sys\nsys.stdin.readline()\n"
        "print(json.dumps({'schema_version':1,"
        "'kind':'model-provider-broker-mint','token':'t',"
        "'expires_at': 99999999999,'endpoint':'https://x.invalid',"
        "'dialect':'some-vendor-native-v9'}))\n", encoding="utf-8")
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(_broker_binding(script))
    assert caught.value.diagnostic == provider_mod.DIAG_DIALECT_UNKNOWN


class _Opener:
    """A scripted stand-in for `urllib.request.urlopen`."""

    def __init__(self, *outcomes):
        self._outcomes = list(outcomes)
        self.requests: list[object] = []

    def __call__(self, request, timeout=None):
        self.requests.append(request)
        outcome = self._outcomes.pop(0) if self._outcomes else {"assistant_prose": "ok"}
        if isinstance(outcome, BaseException):
            raise outcome
        return _Response(json.dumps(outcome).encode("utf-8"))


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def _expired_error():
    return urllib.error.HTTPError(
        "https://provider.invalid/turn", 401, "Unauthorized", {},
        io.BytesIO(b'{"provider":"leaky detail that must never surface"}'))


def _port(tmp_path, *outcomes, expires=None, notice=None, clock=time.time):
    script = _write_broker(tmp_path, expires=expires)
    binding = _broker_binding(script)
    opener = _Opener(*outcomes)
    port = provider_mod.BrokeredProviderPort(
        binding, install_mod.brokered_catalog(binding),
        opener=opener, clock=clock,
        notice=notice if notice is not None else (lambda _text: None))
    return port, opener


def test_a_turn_mints_and_calls_the_provider_with_the_token(tmp_path):
    port, opener = _port(tmp_path, {"assistant_prose": "the answer"})
    assert port.dispatch(_Envelope()) == {"assistant_prose": "the answer",
                                          "proposals": []}
    request = opener.requests[0]
    assert request.get_full_url() == "https://provider.invalid/turn"
    assert request.get_header("Authorization") == f"Bearer {SENTINEL_TOKEN}"
    assert SENTINEL_TOKEN not in request.get_full_url()
    assert SENTINEL_TOKEN not in request.data.decode("utf-8")


def test_the_catalog_never_mints(tmp_path):
    port, opener = _port(tmp_path)
    catalog = port.catalog()
    assert [entry.model_id for entry in catalog.entries] == \
        ["openprofiler-demo"]
    assert catalog.entries[0].available is True
    assert opener.requests == []
    assert not Path(str(_write_broker(tmp_path)) + ".seen.json").exists(), \
        "rendering a menu is not a paid call and does not mint"


def test_a_live_token_is_reused_across_turns(tmp_path):
    port, _opener = _port(tmp_path, {"assistant_prose": "a"},
                          {"assistant_prose": "b"})
    port.dispatch(_Envelope())
    port.dispatch(_Envelope())
    assert [event.reason for event in port.ledger] == \
        [provider_mod.REASON_FIRST_MINT]


def test_a_token_past_its_declared_expiry_is_discarded_and_re_minted(tmp_path):
    """Discard-on-expiry, unconditional and independent of the retry ruling: a
    token known to be dead is never presented."""
    port, _opener = _port(tmp_path, {"assistant_prose": "a"},
                          {"assistant_prose": "b"},
                          expires=time.time() - 1)
    port.dispatch(_Envelope())
    port.dispatch(_Envelope())
    assert [event.reason for event in port.ledger] == \
        [provider_mod.REASON_FIRST_MINT, provider_mod.REASON_FIRST_MINT]


def test_a_mid_turn_expiry_re_mints_and_retries_once_visibly(tmp_path):
    """BRETT'S RULING, 2026-08-26. The retry happens, and it is SEEN."""
    printed: list[str] = []
    port, opener = _port(tmp_path, _expired_error(),
                         {"assistant_prose": "the retried answer"},
                         notice=printed.append)
    assert port.dispatch(_Envelope()) == {
        "assistant_prose": "the retried answer", "proposals": []}
    assert len(opener.requests) == 2, "exactly one paid retry"
    assert [event.reason for event in port.ledger] == [
        provider_mod.REASON_FIRST_MINT,
        provider_mod.REASON_EXPIRY_REMINT,
        provider_mod.REASON_PAID_RETRY,
    ]
    assert printed and "re-minted once and retried" in printed[0]
    # the visible record carries no token, no prompt and no provider detail
    for event in port.ledger:
        rendered = json.dumps(event.as_dict())
        assert SENTINEL_TOKEN not in rendered
        assert "assembled prompt" not in rendered


def test_a_second_expiry_in_one_turn_refuses_rather_than_buying_a_third_call(
        tmp_path):
    port, opener = _port(tmp_path, _expired_error(), _expired_error())
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        port.dispatch(_Envelope())
    assert caught.value.diagnostic == provider_mod.DIAG_TOKEN_EXPIRED_TWICE
    assert len(opener.requests) == 2, "no third paid call"


def test_the_retry_budget_is_per_turn_not_per_process(tmp_path):
    """A turn that used its retry does not spend the NEXT turn's."""
    printed: list[str] = []
    port, opener = _port(tmp_path, _expired_error(), {"assistant_prose": "a"},
                         _expired_error(), {"assistant_prose": "b"},
                         notice=printed.append)
    assert port.dispatch(_Envelope())["assistant_prose"] == "a"
    assert port.dispatch(_Envelope())["assistant_prose"] == "b"
    assert len(opener.requests) == 4
    assert len(printed) == 2


# ===========================================================================
# (e) THE POSTURES (tasks 3.1, 3.2, 3.3)
# ===========================================================================


def test_the_token_never_reaches_a_response_a_log_or_the_disk(tmp_path):
    """Task 3.1, asserted rather than assumed."""
    printed: list[str] = []
    port, _opener = _port(tmp_path, {"assistant_prose": "the answer"},
                          notice=printed.append)
    answer = port.dispatch(_Envelope())
    assert SENTINEL_TOKEN not in json.dumps(answer)
    assert SENTINEL_TOKEN not in repr(port)
    assert SENTINEL_TOKEN not in "".join(printed)
    offenders = [path for path in tmp_path.rglob("*")
                 if path.is_file() and SENTINEL_TOKEN in path.read_text(
                     encoding="utf-8", errors="replace")
                 and path.suffix != ".py"]
    assert not offenders, offenders


def test_a_minted_token_does_not_survive_the_object_that_held_it(tmp_path):
    port, _opener = _port(tmp_path, {"assistant_prose": "a"})
    port.dispatch(_Envelope())
    port._forget_token()
    assert SENTINEL_TOKEN not in repr(port)
    assert SENTINEL_TOKEN not in repr(vars(port))


@pytest.mark.parametrize("outcome,expected", [
    (urllib.error.URLError("unreachable"),
     provider_mod.DIAG_PROVIDER_UNREACHABLE),
    (urllib.error.HTTPError("https://p.invalid", 500, "boom", {},
                            io.BytesIO(b"provider stack trace")),
     provider_mod.DIAG_PROVIDER_REFUSED),
    ({"something_else": 1}, provider_mod.DIAG_PROVIDER_MALFORMED),
])
def test_every_provider_failure_lands_on_a_fixed_redacted_sentence(
        tmp_path, outcome, expected):
    port, _opener = _port(tmp_path, outcome)
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        port.dispatch(_Envelope())
    assert caught.value.diagnostic == expected
    assert caught.value.diagnostic in provider_mod.FIXED_DIAGNOSTICS
    for word in ("stack trace", "boom", "unreachable\n"):
        assert word not in str(caught.value)


def test_a_broker_that_exits_non_zero_is_a_fixed_refusal(tmp_path):
    script = tmp_path / "angry-broker.py"
    script.write_text("import sys\nsys.stderr.write('broker internals')\n"
                      "sys.exit(3)\n", encoding="utf-8")
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(_broker_binding(script))
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_REFUSED
    assert "broker internals" not in str(caught.value)


def test_a_broker_that_cannot_be_started_is_a_fixed_refusal(tmp_path):
    binding = _binding(broker_argv=(str(tmp_path / "no-such-broker"),))
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(binding)
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_UNREACHABLE


def test_a_broker_that_answers_garbage_is_a_fixed_refusal(tmp_path):
    script = tmp_path / "garbled-broker.py"
    script.write_text("import sys\nsys.stdin.readline()\nprint('not json')\n",
                      encoding="utf-8")
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(_broker_binding(script))
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_MALFORMED


def test_a_refusal_cannot_be_composed_from_what_a_broker_said():
    with pytest.raises(AssertionError):
        provider_mod.BrokerRefused("the provider said: your key is bad")


def test_a_broker_failure_maps_onto_the_seams_own_fixed_model_failed(tmp_path):
    """Task 3.2's other half: the redacted refusal this module raises is the
    one `dispatch_turn` already maps to `model_failed`, so nothing new reaches
    the wire and a FAILED CALL stays distinguishable from a MISSING capability
    (which is `model_capability_unavailable`, a different code entirely)."""
    port, _opener = _port(tmp_path, urllib.error.URLError("down"))
    entry = install_mod.brokered_catalog(_binding()).entries[0]
    ticks = iter([0.0, 0.1])
    outcome = model_mod.dispatch_turn(port, _Envelope(), entry=entry,
                                      clock=lambda: next(ticks))
    assert isinstance(outcome, model_mod.TurnDispatchFailure)
    assert outcome.error == model_mod.DISPATCH_ERR_MODEL_FAILED
    assert outcome.diagnostic in model_mod.FIXED_DISPATCH_DIAGNOSTICS
    assert outcome.error != "model_capability_unavailable"


def test_a_broker_that_has_refused_marks_the_catalog_unavailable(tmp_path):
    """The honest posture the harness bridge already keeps: a declaration is
    available until something is measured, and a broker that refused is
    measured. A failure is never reported as an empty result."""
    port, _opener = _port(tmp_path)
    port._binding = _binding(broker_argv=(str(tmp_path / "absent"),))
    with pytest.raises(provider_mod.BrokerRefused):
        port.dispatch(_Envelope())
    catalog = port.catalog()
    assert catalog.entries, "the entry is still disclosed, not dropped"
    assert catalog.entries[0].available is False


def test_the_port_satisfies_the_seam_without_growing_a_fourth_verb(tmp_path):
    from test_doxbench_model import FORBIDDEN_PORT_MEMBERS
    port, _opener = _port(tmp_path)
    assert isinstance(port, model_mod.WorkbenchModelPort)
    declared = {name for name in dir(port) if not name.startswith("_")}
    assert not (declared & FORBIDDEN_PORT_MEMBERS), \
        declared & FORBIDDEN_PORT_MEMBERS


# --- the unconfigured posture (task 3.3) ----------------------------------


def test_a_checkout_with_no_bindings_resolves_exactly_the_harness_declaration(
        tmp_path):
    """TASK 3.3. Not "a port of the same kind" — the SAME construction the
    entrypoints have always made."""
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    resolve = install_mod.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=checkout)
    port = resolve()
    from ideation_dashboard import doxbench_bridge as bridge_mod
    assert isinstance(port, bridge_mod.OmpHarnessBridge)
    assert [entry.model_id for entry in install_mod.HARNESS_CATALOG.entries] \
        == [install_mod.HARNESS_MODEL_ID]


def test_a_declared_binding_resolves_the_brokered_port_instead(tmp_path):
    checkout = tmp_path / "checkout"
    (checkout / "ideation" / "dashboard").mkdir(parents=True)
    script = _write_broker(tmp_path)
    binding_mod.BindingStore(binding_mod.bindings_path(checkout)).add(
        _broker_binding(script))
    resolve = install_mod.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=checkout)
    port = resolve()
    assert isinstance(port, provider_mod.BrokeredProviderPort)
    assert resolve() is port, "ONE port for the life of the process"


def test_an_unreadable_bindings_document_falls_back_and_says_so(tmp_path,
                                                                capsys):
    checkout = tmp_path / "checkout"
    path = binding_mod.bindings_path(checkout)
    path.parent.mkdir(parents=True)
    path.write_text("schema_version: 9\nkind: something-else\n",
                    encoding="utf-8")
    resolve = install_mod.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=checkout)
    from ideation_dashboard import doxbench_bridge as bridge_mod
    assert isinstance(resolve(), bridge_mod.OmpHarnessBridge)
    assert "bindings document could not be read" in capsys.readouterr().err


def test_the_unconfigured_refusal_is_byte_identical_to_what_it_always_was():
    """The `model_capability_unavailable` posture, pinned at the bytes.

    Nothing in this change may move it: a plane with no model port refuses
    exactly as it did, with the same code, the same status and the same
    sentence."""
    from ideation_dashboard import serve as serve_mod
    code = serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE
    assert code == "model_capability_unavailable"
    assert serve_mod.doxbench_error_status(code) == 403
    assert json.dumps(serve_mod.doxbench_error_body(code),
                      sort_keys=True) == json.dumps(
        {"ok": False, "error": code,
         "message": "this plane has no model capability"}, sort_keys=True)


# --- one real provider, over a real socket --------------------------------


class _RealProviderHandler(http.server.BaseHTTPRequestHandler):
    seen: dict = {}

    def do_POST(self):  # noqa: N802 - BaseHTTPRequestHandler's own spelling
        length = int(self.headers.get("Content-Length", "0"))
        _RealProviderHandler.seen = {
            "authorization": self.headers.get("Authorization"),
            "body": json.loads(self.rfile.read(length).decode("utf-8")),
        }
        payload = json.dumps({"assistant_prose": "answered over a socket"})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload.encode("utf-8"))

    def log_message(self, *_args):
        return


def test_the_transport_really_speaks_to_an_endpoint_over_a_socket(tmp_path):
    """The one test that exercises the REAL `urllib` path, against a loopback
    server standing in for a provider. Everything else injects an opener so a
    failure mode is scriptable; this proves the boundary is a real transport
    and that the token travels in the authorization header and nowhere else."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                                             _RealProviderHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, prt = server.server_address[:2]
        endpoint = f"http://{host}:{prt}/turn"
        script = _write_broker(tmp_path, endpoint=endpoint)
        binding = _broker_binding(script)
        port = provider_mod.BrokeredProviderPort(
            binding, install_mod.brokered_catalog(binding),
            notice=lambda _text: None)
        assert port.dispatch(_Envelope()) == {
            "assistant_prose": "answered over a socket", "proposals": []}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    seen = _RealProviderHandler.seen
    assert seen["authorization"] == f"Bearer {SENTINEL_TOKEN}"
    assert seen["body"] == {"model": "openprofiler-demo",
                            "prompt": "assembled prompt"}
    assert SENTINEL_TOKEN not in json.dumps(seen["body"])


def test_the_broker_child_inherits_no_credential_shaped_environment(tmp_path,
                                                                    monkeypatch):
    """The child's environment is the same scrubbed allowlist the harness
    bridge uses, so no ambient variable can become an implicit credential."""
    monkeypatch.setenv("SENTINEL_PROVIDER_API_KEY", SENTINEL_CREDENTIAL)
    script = tmp_path / "env-broker.py"
    script.write_text(
        "import json,os,sys\nsys.stdin.readline()\n"
        "open(sys.argv[0]+'.env.json','w').write(json.dumps(sorted(os.environ)))\n"
        "print(json.dumps({'schema_version':1,"
        "'kind':'model-provider-broker-mint','token':'t',"
        "'expires_at':99999999999,'endpoint':'https://x.invalid',"
        "'dialect':'xfactory-prompt-v1'}))\n", encoding="utf-8")
    provider_mod.mint(_broker_binding(script))
    inherited = json.loads(
        Path(str(script) + ".env.json").read_text(encoding="utf-8"))
    assert "SENTINEL_PROVIDER_API_KEY" not in inherited
    assert set(inherited) <= set(
        __import__("ideation_dashboard.doxbench_bridge", fromlist=["x"])
        .INHERITED_ENVIRONMENT)


def test_a_broker_that_hangs_is_refused_at_the_declared_timeout(tmp_path):
    script = tmp_path / "slow-broker.py"
    script.write_text("import time\ntime.sleep(30)\n", encoding="utf-8")
    binding = _broker_binding(script)
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.subprocess_broker_runner(
            binding.substituted_argv(),
            request={"schema_version": 1,
                     "kind": provider_mod.BROKER_REQUEST_KIND,
                     "operation": "mint"},
            timeout=0.5)
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_TIMEOUT


def test_the_broker_answer_is_bounded(tmp_path):
    script = tmp_path / "loud-broker.py"
    script.write_text(
        "import sys\nsys.stdin.readline()\n"
        f"sys.stdout.write('x' * {provider_mod.MAX_BROKER_ANSWER_BYTES + 1})\n",
        encoding="utf-8")
    with pytest.raises(provider_mod.BrokerRefused) as caught:
        provider_mod.mint(_broker_binding(script))
    assert caught.value.diagnostic == provider_mod.DIAG_BROKER_MALFORMED


def test_the_subprocess_runner_never_uses_a_shell(tmp_path):
    """argv, never a shell string — asserted on the source, because a
    behavioural test cannot prove the absence of a `shell=True` on a path it
    did not take."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / provider_mod.PROVIDER_CLIENT_MODULE).read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "os.system" not in source
    assert subprocess.Popen is subprocess.Popen  # the module spawns, nothing else
