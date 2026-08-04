from __future__ import annotations

import pytest

from conftest import make_ctx  # noqa: F401  (sys.path side effect)

from doc_health.runner import _contained_cli_path


def test_runner_cli_paths_must_stay_inside_checkout(tmp_path):
    inside = _contained_cli_path("prepared/inventory.json", tmp_path,
                                 "prepared inventory")
    assert inside == tmp_path / "prepared" / "inventory.json"
    with pytest.raises(SystemExit, match="must stay inside"):
        _contained_cli_path("../outside.json", tmp_path,
                            "prepared inventory")


# `test_readiness_cli_rejects_input_and_output_path_escape` (and its
# `check-worker-readiness.py` loader) stayed with that CLI: the CloudPC
# worker-readiness evaluators are NOT adopted here — they ride
# adopt-neutral-tooling-home tranche D to the aggregation repo (design D3).
