"""Suite-wide hygiene guard: behavioral tests use no wall-time/randomness/network
(T060a, SC-004). Complements the package scanner (which targets the runtime
package, not the tests)."""

from __future__ import annotations

from pathlib import Path

from boundary.scanner import scan_hygiene_source, scan_test_hygiene

TESTS_DIR = Path(__file__).resolve().parents[1]  # tests/avatar_runtime/


def test_behavioral_tests_are_hermetic():
    violations = scan_test_hygiene(TESTS_DIR)
    assert violations == [], "\n".join(str(v) for v in violations)


def test_hygiene_scanner_flags_forbidden_usage():
    # Negative control: prove the scanner detects a forbidden import.
    v = scan_hygiene_source("import random\nx = random.random()\n", "x.py")
    assert any(x.kind == "test-hygiene" for x in v)


def test_hygiene_scanner_flags_wall_clock_idioms():
    # Negative control: every wall-clock idiom the scanner learned must be caught.
    cases = [
        "import datetime\nx = datetime.datetime.now()\n",  # Attribute base is Attribute
        "import datetime\nx = datetime.now()\n",
        "import time\nx = time.monotonic()\n",
        "import time\nx = time.perf_counter()\n",
        "import time\nx = time.time()\n",
        "from time import time\nx = time()\n",  # bare Name call
    ]
    for src in cases:
        v = scan_hygiene_source(src, "x.py")
        assert any(x.kind == "test-hygiene" for x in v), f"missed idiom:\n{src}"
