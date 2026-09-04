# Red-first, measured rather than asserted

Status: record
Kind: evidence

## The question a red-proof has to answer

"Every refusal has been seen to fire" is cheap: 118 of 118 closed codes have a
packaged negative and the reader's own self-test refuses to pass otherwise. The
harder question is whether each of the amendment's fifty-two fixtures fails **for
the rule it is named for and for nothing else** — a fixture that fails because a
schema rejects it, or because an unrelated sweep catches it, is a fixture that
proves nothing about the new check.

The self-test's `expected_failure_detail` pinning answers that per fixture. This
answers it for the whole set at once, from the other direction.

## The measurement

The amendment's eight check layers are replaced by no-ops, and each of its
fifty-two negatives is then validated INSIDE the positive corpus:

```python
noop = lambda *a, **k: None
for name in ("check_confirmation_profiles", "check_profile_registries",
             "check_merkle_profiles", "check_eligibility_registries",
             "check_admissions", "check_manifests",
             "check_manifest_window_profiles", "check_confirmation_bindings"):
    setattr(reader, name, noop)

for code in NEW_CODES:               # 48 closed + 4 kebab-case findings
    f = reader.Findings()
    reader.validate_scope(f, positives + labelled(NEGATIVE_DIR / f"{code}.yaml"),
                          registry, docs)
    assert not f.errors
```

## The result

```
with the amendment's checks DISABLED: 52/52 of its negatives validate cleanly
positive corpus with the checks disabled: 0 error(s)
```

**Every one of the fifty-two is red BECAUSE OF the new rule.** None of them is
caught by a shape, by the payload sweep, by the closure rule, by the timing
model or by any check the basis realization already had — turn the new layers
off and the whole set goes green. And the positive corpus reports zero errors
with the layers off as well, which says the new checks add refusals rather than
re-reporting old ones.

## The other direction, per fixture

Each fixture's `# expected_failure_detail:` substring pins the finding to the
MESSAGE, not just the code, so a fixture cannot be mutated into testing a
different instance of the same rule while staying green. One detail moved with
this amendment and is recorded as moving:
`receipt_entry_incomplete_for_pending_witness` was pinned to *"still in
flight"*, which is a retired spelling; it is now pinned to *"no confirmation
evidence yet"*, and the migration script carries the substitution explicitly so
the move is a deliberate edit rather than a silent one.
