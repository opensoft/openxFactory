from datetime import UTC, datetime

from scripts.intent_compliance.temporal import parse_timestamp


def test_timestamp_when_utc_suffix_is_lowercase_then_rfc3339_is_accepted() -> None:
    # Given
    timestamp = "2026-06-01T00:00:00z"

    # When
    parsed = parse_timestamp(timestamp)

    # Then
    assert parsed == datetime(2026, 6, 1, tzinfo=UTC)
