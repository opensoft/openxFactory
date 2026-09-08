"""`scripts/signed_execution_chain/ed25519.py`, pinned by PUBLISHED vectors.

WHY THIS FILE CARRIES THE WHOLE ARGUMENT for a hand-written verifier. "Do not
write your own crypto" is the right default, and the exception here is bounded:
the module VERIFIES and never signs, holds no secret, and every input it touches
is public — which is what the usual timing-side-channel warning is about. What
makes the exception SAFE rather than merely small is this file: RFC 8032's own
section 7.1 vectors, plus the mutations a permissive implementation would
accept.

A verifier that accepts everything passes every positive test ever written. So
the negatives are the real content here: a flipped message byte, a flipped
signature byte, the wrong public key, a non-canonical scalar, inputs of the wrong
length, and EVERY SMALL-ORDER POINT must each be REFUSED, and each of those is a
way a real implementation has historically gone wrong.

THE SMALL-ORDER CASE IS NOT HYPOTHETICAL HERE, and it is why this file grew. It
was a live forgery in this module's first version — measured, not argued: an
identity public key made the verification equation stop depending on the message,
so `R = identity, S = 0` verified over everything, with no private key involved.
Codex and Copilot both raised it as P1 in the same review round.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.signed_execution_chain import ed25519  # noqa: E402

#: RFC 8032 section 7.1, TEST 1, TEST 2 and TEST 3 — (public key, message,
#: signature), hex, verbatim from the RFC.
RFC_8032_VECTORS = [
    (
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
        "",
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a"
        "33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b",
    ),
    (
        "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
        "72",
        "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e1"
        "5996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00",
    ),
    (
        "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
        "af82",
        "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d1"
        "6f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a",
    ),
]


def _vector(index):
    public, message, signature = RFC_8032_VECTORS[index]
    return bytes.fromhex(public), bytes.fromhex(message), bytes.fromhex(signature)


def test_every_rfc_8032_vector_verifies():
    for index in range(len(RFC_8032_VECTORS)):
        public, message, signature = _vector(index)
        assert ed25519.verify(public, message, signature), f"vector {index}"


def test_a_flipped_message_byte_is_refused():
    public, _, signature = _vector(2)
    assert not ed25519.verify(public, bytes.fromhex("af83"), signature)


def test_an_empty_message_is_not_interchangeable_with_a_nonempty_one():
    public, _, signature = _vector(2)
    assert not ed25519.verify(public, b"", signature)


def test_a_flipped_signature_byte_is_refused():
    public, message, signature = _vector(2)
    for position in (0, 31, 32, 63):
        mutated = bytearray(signature)
        mutated[position] ^= 0x01
        assert not ed25519.verify(public, message, bytes(mutated)), position


def test_another_keys_signature_is_refused():
    _, message, signature = _vector(2)
    other_public, _, _ = _vector(1)
    assert not ed25519.verify(other_public, message, signature)


def test_a_non_canonical_scalar_is_refused():
    """S >= L is a MALLEABLE signature: the same message and key would verify
    under more than one signature, which is not what "the signature over this
    ratification" is allowed to mean."""
    public, message, signature = _vector(2)
    order = 2 ** 252 + 27742317777372353535851937790883648493
    scalar = int.from_bytes(signature[32:], "little")
    mutated = signature[:32] + int.to_bytes(scalar + order, 32, "little")
    assert len(mutated) == 64
    assert not ed25519.verify(public, message, mutated)


def test_wrong_length_inputs_are_refused_rather_than_raising():
    public, message, signature = _vector(2)
    assert not ed25519.verify(public[:31], message, signature)
    assert not ed25519.verify(public + b"\x00", message, signature)
    assert not ed25519.verify(public, message, signature[:63])
    assert not ed25519.verify(public, message, signature + b"\x00")


#: The canonical encodings of the small-order points on this curve: the
#: identity, the order-2 point, the two order-4 points and the four order-8
#: points. Published values, and each one is independently confirmed below to be
#: small-order by the group arithmetic rather than trusted from a list.
SMALL_ORDER_ENCODINGS = [
    bytes([1] + [0] * 31),
    bytes.fromhex(
        "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f"),
    bytes(32),
    bytes(31) + bytes([0x80]),
    bytes.fromhex(
        "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05"),
    bytes.fromhex(
        "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa"),
    bytes.fromhex(
        "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85"),
    bytes.fromhex(
        "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a"),
]

#: The forgery: R = identity, S = 0. It needs no private key.
IDENTITY_FORGERY = SMALL_ORDER_ENCODINGS[0] + bytes(32)


def test_the_identity_public_key_cannot_forge_a_signature():
    """THE NEGATIVE CONTROL FOR A REAL FORGERY, and it is measured rather than
    argued.

    With an identity public key the `[h]A` term of `[S]B == R + [h]A` vanishes,
    the equation stops depending on `h` — and so on the message — and
    `R = identity, S = 0` satisfies it for ANY message. Against this module's
    PRE-FIX code that construction verified over every message tried; two of the
    order-4 points verified over some. Codex and Copilot both raised it as P1 in
    the same round.

    An attacker needs no private key for this: every public half in this family
    arrives inside a record — a `did:key` in a CARRIED wallet — chosen by
    whoever assembled the chain."""
    for message in (b"", b"anything", b"a completely different message",
                    bytes(range(256))):
        assert not ed25519.verify(
            SMALL_ORDER_ENCODINGS[0], message, IDENTITY_FORGERY), message


def test_no_small_order_public_key_verifies_anything():
    """The whole CLASS, not the one encoding the finding named. A fix that
    rejected the identity alone would leave the order-4 points, which the pre-fix
    measurement showed accepting the same forgery over some messages."""
    for index, encoded in enumerate(SMALL_ORDER_ENCODINGS):
        for signature in (IDENTITY_FORGERY, encoded + bytes(32)):
            assert not ed25519.verify(encoded, b"", signature), index
            assert not ed25519.verify(encoded, b"a message", signature), index


def test_every_listed_encoding_really_is_small_order():
    """The list above is published values, and a published value transcribed
    wrongly is a test that guards nothing. `[8]P == identity` is exactly "the
    order divides 8", so the arithmetic confirms the list rather than the list
    being taken on trust."""
    # pylint: disable=protected-access
    for index, encoded in enumerate(SMALL_ORDER_ENCODINGS):
        point = ed25519._decompress(encoded)
        assert point is not None, f"{index}: does not decompress"
        assert ed25519._is_small_order(point), index


def test_a_legitimate_public_key_is_not_small_order():
    """The other half of the control: the rejection must not be rejecting
    everything. Each RFC vector's key passes the same predicate the forgeries
    fail, and each vector still verifies."""
    # pylint: disable=protected-access
    for index in range(len(RFC_8032_VECTORS)):
        public, message, signature = _vector(index)
        point = ed25519._decompress(public)
        assert not ed25519._is_small_order(point), index
        assert ed25519.verify(public, message, signature), index


def test_a_small_order_r_is_refused():
    """Not the forgery vector — with `A` in the prime-order subgroup a
    small-order `R` confers no advantage — but an honest signer produces one only
    at probability about 2**-252, so refusing it costs no legitimate signature
    and removes the last case whose acceptance would depend on a cofactored
    reading of the equation."""
    public, message, _ = _vector(2)
    for encoded in SMALL_ORDER_ENCODINGS:
        assert not ed25519.verify(public, message, encoded + bytes(32))


def test_a_public_key_that_does_not_decompress_is_refused():
    """A y outside the field has no point on the curve. It must be refused, not
    treated as a verification failure of a valid key and not raise."""
    _, message, signature = _vector(2)
    assert not ed25519.verify(b"\xff" * 32, message, signature)


def test_did_key_recovers_the_public_half_the_live_wallet_declares():
    """The one live wallet in this repository, `wal-agent-mrc-0001`, declares its
    `did` and its `public_key_multibase` as one string. Recovering the same 32
    bytes from both is what lets a carried wallet be read from the DID — which
    the pinned record schema REQUIRES — rather than from the multibase, which it
    leaves optional."""
    did = "did:key:z6Mko2FefScUQg9opCriwQmjfcb3Qjnb5bN49hQsEVMo6gee"
    from_did = ed25519.public_key_from_did(did)
    from_multibase = ed25519.public_key_from_multibase(did[len("did:key:"):])
    assert from_did == from_multibase
    assert len(from_did) == ed25519.PUBLIC_KEY_BYTES


def test_a_non_ed25519_multicodec_is_a_recovery_error_not_a_false_key():
    """`did:key` carries a multicodec prefix naming the algorithm. A prefix this
    capability does not verify must RAISE rather than yield 32 arbitrary bytes
    that a verification would then fail on — an unresolvable key is an unevaluable
    chain, and a failed signature is a different event."""
    import pytest

    from scripts.signed_execution_chain.ed25519 import KeyRecoveryError

    B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    def b58(raw: bytes) -> str:
        value = int.from_bytes(raw, "big")
        out = ""
        while value:
            value, rem = divmod(value, 58)
            out = B58[rem] + out
        return out

    # multicodec 0x1200 = p256-pub, with a 32-byte body.
    p256ish = "z" + b58(b"\x80\x24" + b"\x01" * 32)
    with pytest.raises(KeyRecoveryError):
        ed25519.public_key_from_multibase(p256ish)
    with pytest.raises(KeyRecoveryError):
        ed25519.public_key_from_did("did:web:example.org")
    with pytest.raises(KeyRecoveryError):
        ed25519.public_key_from_multibase("Qmnotbase58btcmultibase")


def test_base58btc_keeps_leading_zero_bytes():
    """A bare integer conversion silently drops them, and the multicodec prefix
    means a dropped leading byte is a key of the wrong length rather than a
    visible error."""
    assert ed25519.base58btc_decode("11z") == b"\x00\x00" + \
        ed25519.base58btc_decode("z")
