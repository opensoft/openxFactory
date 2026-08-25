"""The single server-side provider boundary for doxBench.

This module is intentionally the only dashboard module that knows about a
provider endpoint, a provider authorization header, or a broker-minted token.
The rest of the dashboard sees only ``WorkbenchModelPort`` and the public
catalog.  The broker command is supplied by each binding; openProfiler is not
assumed to have a particular executable name or CLI shape.

The small command protocol used here is deliberately transport-neutral:

* the configured argv receives one JSON request on stdin;
* a credential handoff returns ``{"credential_ref": "..."}``;
* a mint returns ``{"token": "...", "expires_at": <unix seconds>,
  "provider": {"catalog_endpoint": "...", "completion_endpoint":
  "...", "timeout_seconds": <number>}}``.

The last response is an adapter contract for the not-yet-built openProfiler.
It is not a provider command hardcoded into the repository.  Until a binding
names a broker that implements it, this module is inert and the server keeps
its existing no-model-capability posture.
"""

from __future__ import annotations

import datetime as _datetime
import json
import math
import os
import re
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping

from ideation_dashboard import doxbench_model


AUTH_KINDS = frozenset({"api_key", "oauth"})
MODEL_PROVIDER_BINDING_FIELDS = (
    "id", "label", "credential_ref", "auth_kind", "broker_invocation",
)
BROKER_OPERATIONS = frozenset({"store_credential", "mint"})
DEFAULT_BROKER_TIMEOUT_SECONDS = 30.0
MAX_BROKER_OUTPUT_BYTES = 256 * 1024
MAX_BINDINGS = 32
DEFAULT_PROVIDER_TIMEOUT_SECONDS = 120.0
_BINDING_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


class ModelProviderError(Exception):
    """Base class for failures whose detail must never leave this module."""


class BindingError(ModelProviderError):
    """A binding was malformed or could not be safely persisted."""


class BrokerError(ModelProviderError):
    """The configured broker could not complete a safe operation."""


class ProviderError(ModelProviderError):
    """The provider could not answer or returned an unusable shape."""


class ProviderTokenExpired(ProviderError):
    """The current in-memory capability expired; it is not retried."""


def _text(value: object, field: str, *, maximum: int = 4096) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise BindingError(f"invalid {field}")
    if "\x00" in value:
        raise BindingError(f"invalid {field}")
    return value


def _argv(value: object) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)):
        raise BindingError("broker_invocation must be an argv array")
    try:
        result = tuple(value)  # type: ignore[arg-type]
    except TypeError as exc:
        raise BindingError("broker_invocation must be an argv array") from exc
    if not result or len(result) > 64:
        raise BindingError("invalid broker_invocation")
    checked = []
    for item in result:
        checked.append(_text(item, "broker_invocation item", maximum=4096))
    return tuple(checked)


@dataclass(frozen=True, slots=True)
class ModelProviderBinding:
    """The complete persisted binding shape.

    There is intentionally no ``secret``, ``api_key`` or token field.  Passing
    one to the constructor is rejected by Python's dataclass call boundary,
    and the public projection is closed to the five fields above.
    """

    id: str
    label: str
    credential_ref: str
    auth_kind: str
    broker_invocation: tuple[str, ...]

    def __post_init__(self) -> None:
        identifier = _text(self.id, "id", maximum=64)
        if _BINDING_ID.fullmatch(identifier) is None:
            raise BindingError("invalid id")
        object.__setattr__(self, "id", identifier)
        object.__setattr__(self, "label", _text(self.label, "label", maximum=200))
        object.__setattr__(
            self, "credential_ref", _text(self.credential_ref,
                                           "credential_ref", maximum=2048))
        if self.auth_kind not in AUTH_KINDS:
            raise BindingError("invalid auth_kind")
        object.__setattr__(self, "broker_invocation",
                           _argv(self.broker_invocation))

    def as_public_dict(self) -> dict:
        """Return the exact safe-to-read/write/commit binding shape."""
        return {
            "id": self.id,
            "label": self.label,
            "credential_ref": self.credential_ref,
            "auth_kind": self.auth_kind,
            "broker_invocation": list(self.broker_invocation),
        }


def _binding_from_dict(value: object) -> ModelProviderBinding:
    if not isinstance(value, dict) or set(value) != set(MODEL_PROVIDER_BINDING_FIELDS):
        raise BindingError("invalid model-provider binding")
    return ModelProviderBinding(
        id=value["id"], label=value["label"],
        credential_ref=value["credential_ref"], auth_kind=value["auth_kind"],
        broker_invocation=value["broker_invocation"],
    )


class ModelProviderBindingStore:
    """A small safe binding store.

    ``path`` is normally ``ideation/workbench/model-provider-bindings.json``,
    which is already gitignored by this repository.  Tests can use ``None``
    for a process-only store.  The store writes only public binding records and
    rejects a file containing a secret-shaped field rather than attempting to
    migrate it silently.
    """

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path).resolve() if path is not None else None
        self._lock = threading.RLock()
        self._bindings: dict[str, ModelProviderBinding] = {}
        self._load()

    def _load(self) -> None:
        if self.path is None or not self.path.is_file():
            return
        try:
            document = json.loads(self.path.read_text(encoding="utf-8"))
            records = document.get("bindings") if isinstance(document, dict) else None
            if not isinstance(records, list) or len(records) > MAX_BINDINGS:
                raise BindingError("invalid binding store")
            loaded = {}
            for record in records:
                binding = _binding_from_dict(record)
                if binding.id in loaded:
                    raise BindingError("duplicate binding")
                loaded[binding.id] = binding
            self._bindings = loaded
        except (OSError, ValueError, BindingError) as exc:
            raise BindingError("could not read binding store") from exc

    def _persist(self) -> None:
        if self.path is None:
            return
        parent = self.path.parent
        parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        document = {"bindings": [
            self._bindings[key].as_public_dict()
            for key in sorted(self._bindings)
        ]}
        encoded = json.dumps(document, sort_keys=True, separators=(",", ":"))
        temporary = None
        try:
            fd, temporary = tempfile.mkstemp(prefix=".model-provider-",
                                             dir=str(parent), text=True)
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            temporary = None
        except OSError as exc:
            raise BindingError("could not persist model-provider binding") from exc
        finally:
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass

    def list(self) -> tuple[ModelProviderBinding, ...]:
        with self._lock:
            return tuple(self._bindings[key] for key in sorted(self._bindings))

    def get(self, binding_id: str) -> ModelProviderBinding | None:
        with self._lock:
            return self._bindings.get(binding_id)

    def put(self, binding: ModelProviderBinding) -> ModelProviderBinding:
        with self._lock:
            if binding.id not in self._bindings and len(self._bindings) >= MAX_BINDINGS:
                raise BindingError("too many model-provider bindings")
            previous = self._bindings.get(binding.id)
            self._bindings[binding.id] = binding
            try:
                self._persist()
            except Exception:
                if previous is None:
                    self._bindings.pop(binding.id, None)
                else:
                    self._bindings[binding.id] = previous
                raise
            return binding

    def remove(self, binding_id: str) -> bool:
        with self._lock:
            if binding_id not in self._bindings:
                return False
            previous = self._bindings.pop(binding_id)
            try:
                self._persist()
            except Exception:
                self._bindings[binding_id] = previous
                raise
            return True

    def public_list(self) -> list[dict]:
        return [binding.as_public_dict() for binding in self.list()]


def _safe_json_bytes(value: Mapping[str, object]) -> bytes:
    try:
        encoded = json.dumps(value, separators=(",", ":"),
                             ensure_ascii=False).encode("utf-8")
    except (TypeError, UnicodeError) as exc:
        raise BrokerError("broker request could not be encoded") from exc
    if len(encoded) > MAX_BROKER_OUTPUT_BYTES:
        raise BrokerError("broker request exceeded its bound")
    return encoded


def _default_runner(argv: tuple[str, ...], stdin: bytes, timeout: float) -> bytes:
    try:
        completed = subprocess.run(
            list(argv), input=stdin, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, shell=False, check=False,
            timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        raise BrokerError("broker invocation failed") from exc
    if completed.returncode != 0:
        raise BrokerError("broker invocation failed")
    if len(completed.stdout) > MAX_BROKER_OUTPUT_BYTES:
        raise BrokerError("broker response exceeded its bound")
    return completed.stdout


class BrokerClient:
    """Invoke a binding's declared broker command without retaining secrets."""

    def __init__(self, *, runner: Callable[[tuple[str, ...], bytes, float], bytes]
                 | None = None, timeout_seconds: float = DEFAULT_BROKER_TIMEOUT_SECONDS):
        if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool):
            raise ValueError("invalid broker timeout")
        if not 0 < float(timeout_seconds) <= 120:
            raise ValueError("invalid broker timeout")
        self._runner = runner or _default_runner
        self.timeout_seconds = float(timeout_seconds)

    def _invoke(self, binding: ModelProviderBinding, operation: str,
                fields: Mapping[str, object]) -> dict:
        if operation not in BROKER_OPERATIONS:
            raise BrokerError("unsupported broker operation")
        request = {"operation": operation, "binding_id": binding.id,
                   "auth_kind": binding.auth_kind, **dict(fields)}
        try:
            raw = self._runner(binding.broker_invocation,
                               _safe_json_bytes(request), self.timeout_seconds)
        except BrokerError:
            raise
        except Exception as exc:
            # An injected runner is a test seam, but production and tests share
            # the same redaction rule: runner text is never propagated.
            raise BrokerError("broker invocation failed") from exc
        if not isinstance(raw, bytes) or len(raw) > MAX_BROKER_OUTPUT_BYTES:
            raise BrokerError("invalid broker response")
        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise BrokerError("invalid broker response") from exc
        if not isinstance(result, dict):
            raise BrokerError("invalid broker response")
        return result

    def store_credential(self, *, binding_id: str, label: str, auth_kind: str,
                         broker_invocation: Iterable[str], credential: str) -> str:
        """Pass the supplied value to stdin and return only the broker ref."""
        # This object is deliberately constructed without a persisted reference;
        # the temporary binding exists only for the one handoff call.
        temporary = ModelProviderBinding(
            id=binding_id, label=label, credential_ref="pending",
            auth_kind=auth_kind, broker_invocation=tuple(broker_invocation))
        if not isinstance(credential, str) or not credential:
            raise BindingError("credential is required for handoff")
        try:
            result = self._invoke(temporary, "store_credential",
                                  {"credential": credential})
        finally:
            # Drop the local reference before returning to the route.  Python
            # cannot guarantee allocator wiping, but no owning store, object
            # field, log, file, response, or subprocess environment retains it.
            credential = ""
        reference = result.get("credential_ref")
        if not isinstance(reference, str) or not reference.strip():
            raise BrokerError("broker returned no credential reference")
        return reference

    def mint(self, binding: ModelProviderBinding) -> "MintedCapability":
        result = self._invoke(
            binding, "mint", {"credential_ref": binding.credential_ref})
        token = result.get("token")
        expires_at = _expiry_seconds(result.get("expires_at"))
        provider = result.get("provider")
        if not isinstance(token, str) or not token or not isinstance(provider, dict):
            raise BrokerError("broker returned an unusable capability")
        catalog_endpoint = _endpoint(provider.get("catalog_endpoint"))
        completion_endpoint = _endpoint(provider.get("completion_endpoint"))
        timeout = provider.get("timeout_seconds", DEFAULT_PROVIDER_TIMEOUT_SECONDS)
        try:
            timeout = doxbench_model.validated_timeout_seconds(timeout)
        except Exception as exc:
            raise BrokerError("broker returned an unusable timeout") from exc
        return MintedCapability(
            token=token, expires_at=expires_at,
            catalog_endpoint=catalog_endpoint,
            completion_endpoint=completion_endpoint,
            timeout_seconds=timeout)


def _expiry_seconds(value: object) -> float:
    if isinstance(value, bool):
        raise BrokerError("broker returned an invalid expiry")
    if isinstance(value, (int, float)):
        result = float(value)
    elif isinstance(value, str):
        try:
            result = _datetime.datetime.fromisoformat(
                value.replace("Z", "+00:00")).timestamp()
        except (TypeError, ValueError, OverflowError) as exc:
            raise BrokerError("broker returned an invalid expiry") from exc
    else:
        raise BrokerError("broker returned an invalid expiry")
    if not math.isfinite(result) or not result > time.time():
        raise BrokerError("broker returned an expired capability")
    return result


def _endpoint(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise BrokerError("broker returned no provider endpoint")
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username:
        raise BrokerError("broker returned an invalid provider endpoint")
    return value


@dataclass(slots=True)
class MintedCapability:
    """A process-memory-only capability and its provider routing metadata."""

    token: str | None
    expires_at: float
    catalog_endpoint: str
    completion_endpoint: str
    timeout_seconds: float

    def expired(self, now: float | None = None) -> bool:
        return (time.time() if now is None else now) >= self.expires_at

    def authorization(self) -> str:
        if self.token is None or self.expired():
            raise ProviderTokenExpired("expired capability")
        return "Bearer " + self.token

    def discard(self) -> None:
        # Strings are immutable, so replacing the owning reference is the
        # strongest portable guarantee Python provides at this boundary.
        self.token = None

    def __repr__(self) -> str:
        # A future diagnostic or debugger must not turn an accidental repr into
        # a credential log line.
        return (f"MintedCapability(expires_at={self.expires_at!r}, "
                f"catalog_endpoint=<redacted>, completion_endpoint=<redacted>)")


class HttpProviderClient:
    """The one direct provider transport; it never escapes this module."""

    def __init__(self, *, opener=None):
        self._opener = opener or urllib.request.urlopen

    def _post(self, endpoint: str, capability: MintedCapability,
              payload: Mapping[str, object]) -> dict:
        try:
            authorization = capability.authorization()
            body = json.dumps(payload, ensure_ascii=False,
                              separators=(",", ":")).encode("utf-8")
            request = urllib.request.Request(
                endpoint, data=body, method="POST",
                headers={"Authorization": authorization,
                         "Content-Type": "application/json"})
            with self._opener(request, timeout=capability.timeout_seconds) as response:
                raw = response.read(MAX_BROKER_OUTPUT_BYTES + 1)
        except ProviderTokenExpired:
            raise
        except (OSError, ValueError, TypeError, urllib.error.URLError) as exc:
            raise ProviderError("provider request failed") from exc
        if len(raw) > MAX_BROKER_OUTPUT_BYTES:
            raise ProviderError("provider response exceeded its bound")
        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ProviderError("provider response was not JSON") from exc
        if not isinstance(result, dict):
            raise ProviderError("provider response was not an object")
        return result

    def catalog(self, capability: MintedCapability) -> doxbench_model.ModelCatalog:
        result = self._post(capability.catalog_endpoint, capability,
                            {"operation": "catalog"})
        models = result.get("models")
        if not isinstance(models, list):
            raise ProviderError("provider catalog was malformed")
        entries = []
        try:
            for model in models:
                if not isinstance(model, dict):
                    raise ProviderError("provider catalog was malformed")
                entries.append(doxbench_model.ModelCatalogEntry(**model))
            return doxbench_model.ModelCatalog.from_entries(entries)
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError("provider catalog was malformed") from exc

    def dispatch(self, capability: MintedCapability, prompt_envelope: object) -> object:
        result = self._post(capability.completion_endpoint, capability,
                            {"operation": "chat", "prompt": prompt_envelope})
        if set(result) != {"assistant_prose", "proposals"}:
            raise ProviderError("provider response was malformed")
        return result


class BrokerBackedWorkbenchModelPort:
    """A narrow ``WorkbenchModelPort`` backed by one configured binding."""

    def __init__(self, binding: ModelProviderBinding, *, broker: BrokerClient | None = None,
                 provider: HttpProviderClient | None = None):
        self.binding = binding
        self._broker = broker or BrokerClient()
        self._provider = provider or HttpProviderClient()
        self._capability: MintedCapability | None = None
        self._timeout_seconds = DEFAULT_PROVIDER_TIMEOUT_SECONDS

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    def _capability_for_call(self) -> MintedCapability:
        current = self._capability
        if current is not None:
            if current.expired():
                current.discard()
                self._capability = None
                raise ProviderTokenExpired("expired capability")
            return current
        current = self._broker.mint(self.binding)
        self._capability = current
        self._timeout_seconds = current.timeout_seconds
        return current

    def catalog(self) -> doxbench_model.ModelCatalog:
        capability = self._capability_for_call()
        try:
            return self._provider.catalog(capability)
        except Exception:
            capability.discard()
            self._capability = None
            raise

    def dispatch(self, prompt_envelope: object) -> object:
        capability = self._capability_for_call()
        try:
            return self._provider.dispatch(capability, prompt_envelope)
        except Exception:
            capability.discard()
            self._capability = None
            raise


def provider_store_path(checkout_root: Path | str) -> Path:
    """The existing gitignored workbench area is the default safe location."""
    return Path(checkout_root).resolve() / "ideation" / "workbench" / \
        "model-provider-bindings.json"


def model_port_for_store(store: ModelProviderBindingStore, *,
                         broker: BrokerClient | None = None,
                         provider: HttpProviderClient | None = None):
    """Return a fresh port for the first configured binding, or ``None``."""
    bindings = store.list()
    if not bindings:
        return None
    return BrokerBackedWorkbenchModelPort(bindings[0], broker=broker,
                                          provider=provider)
