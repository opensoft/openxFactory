# Verification

Status: draft

From the selected feature worktree in the owning bench:

```sh
python3 -m pytest tests/lane_line/test_conditional_lane_line.py -q
OPENSPEC_TELEMETRY=0 openspec validate honor-conditional-lane-attribution --strict
```

Run the repository's required validation route before landing. Verify a real outside-lane PR's lane-line result after the workflow update. An absent tag does not attest actual non-membership.
