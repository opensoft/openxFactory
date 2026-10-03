# Recovery verification

Run from the feature checkout inside py-bench:

```sh
python3 -m pytest tests/notebooklm -q
python3 -m pytest tests/notebooklm --collect-only -q
python3 tests/hermetic_unittest.py tests/notebooklm/
python3 scripts/check-notebooklm-sync-quality.py --show-surface
PROGRAMMING_CHECKER="$PROGRAMMING_CHECKER" python3 scripts/check-notebooklm-sync-quality.py
python3 scripts/sync-notebooklm-books.py --help
OPENSPEC_TELEMETRY=0 openspec validate harden-notebooklm-sync-tooling --strict
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

The checker environment variable must identify the verified original checker.
Guard unittest discovery with the existing real-nlm refusal mechanism. Run
hermetic dry-run and invalid-input probes without live provider access.
Do not publish until the repository-wide strict gate passes or Brett grants
an explicit baseline exception. Do not delete the old branch before landing.
