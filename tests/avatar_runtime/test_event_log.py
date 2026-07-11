"""Single sequenced event log + producer-authority checks (ARR-006-S05, FR-026)."""

from __future__ import annotations

import pytest

from xfactory.avatar_runtime.events import ProducerAuthorityError
from xfactory.avatar_runtime.values import ProducerAuthority


def test_single_sequence_increments(runtime):
    e1 = runtime.append_observation("s", ProducerAuthority.CLIENT, "obs1")
    e2 = runtime.append_observation("s", ProducerAuthority.PROVIDER, "obs2")
    e3 = runtime.append_observation("s", ProducerAuthority.CLIENT, "obs3")
    assert [e1.sequence, e2.sequence, e3.sequence] == [1, 2, 3]


@pytest.mark.parametrize("producer", [ProducerAuthority.CLIENT, ProducerAuthority.PROVIDER])
def test_observation_claiming_authority_is_rejected(runtime, producer):
    with pytest.raises(ProducerAuthorityError):
        runtime.append_observation("s", producer, "approve-and-execute", authoritative=True)


def test_runtime_authority_may_append_authoritative_result(runtime):
    e = runtime.append_observation(
        "s", ProducerAuthority.RUNTIME_AUTHORITY, "result", authoritative=True
    )
    assert e.sequence == 1
