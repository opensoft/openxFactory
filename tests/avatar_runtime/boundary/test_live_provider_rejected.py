"""Reference code loading a provider key / making a network call is rejected
and routed to a live-runtime change (ARR-001-S02, FR-002)."""

from __future__ import annotations

from boundary.scanner import scan_source


def test_network_provider_call_is_rejected():
    src = "import socket\ns = socket.socket()\ns.connect(('provider', 443))\n"
    kinds = {v.kind for v in scan_source(src, "would_be_runtime.py")}
    assert "forbidden-stdlib" in kinds


def test_provider_credential_loading_is_rejected():
    src = "import os\nkey = os.getenv('OPENAI_API_KEY')\n"
    v = scan_source(src, "would_be_runtime.py")
    assert any(x.kind == "deployment-surface" and "getenv" in x.detail for x in v)


def test_live_provider_sdk_import_is_rejected():
    v = scan_source("import openai\n", "would_be_runtime.py")
    assert any(x.kind == "provider-sdk" for x in v)
