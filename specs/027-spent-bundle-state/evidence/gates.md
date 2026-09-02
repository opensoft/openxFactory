# Gates — every command, and its output

Run from this branch's head in a fresh clone
(`git clone git@github.com:opensoft/openxFactory.git`), never a shared
checkout.

## OpenSpec

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

```text
Totals: 85 passed, 0 failed (85 items)
```

```bash
python3 scripts/proposal-support.py . verify declare-spent-bundle-state
```

```text
proposal support verification ok
```

The packet keeps `Status: ratified` and is NOT archived — OpenSpec § 5 follows
the merge and is not this feature's.

## sequenced-after — NO PIN MOVED

```bash
python3 scripts/validate-sequenced-after.py .
```

```text
sequenced_after validation passed (32 active changes, 1 declaring the field).
```

```bash
python3 -m pytest tests/sequenced_after -q
```

```text
118 passed in 3.07s
```

**No pin moved, and the reason is structural rather than lucky**: this feature
adds no OpenSpec change directory, moves none, and authors no MODIFIED block —
the MODIFIED block it realizes was authored by PR #578 and is already counted
on `main`. The `32 active` reading is one higher than the packet's § 4.7
measurement of `31` because `add-clearing-dispatch-boundary` (#555) landed on
`main` in between; the sweep test passes at that reading, so the pin was
already moved by whoever landed it.

## Release surface — verify-commit, disclosed in full

```bash
python3 scripts/validate-contract-release.py verify-commit --commit HEAD
```

```text
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/CHANGELOG.md: digest does not match the raw Git blob at the pinned commit
HGR-RELEASE-DIGEST-MISMATCH error path=docs/contract-versioning-policy.md: digest does not match the raw Git blob at the pinned commit
exit=1
```

**EXACTLY TWO MEMBERS, AND THEY ARE DIFFERENT KINDS OF FACT.**

| member | whose | class | clears |
|---|---|---|---|
| `contracts/CHANGELOG.md` | THIS feature | **EDITORIAL** — one of the three the versioning policy allows to move between cuts, so its drift is an `info` labelled *expected between cuts* | at the next cut |
| `docs/contract-versioning-policy.md` | **INHERITED** from PR #577 (`2898b104`, 2026-09-02) | NON-editorial — an unconditional `error` | at the next cut |

The same command at `origin/main` (`f4fddf7c`) reports the SECOND one alone,
exit 1 — so this feature adds exactly one mismatch, on an editorial member, and
inherits the other:

```text
HGR-RELEASE-DIGEST-MISMATCH error path=docs/contract-versioning-policy.md: digest does not match the raw Git blob at the pinned commit
exit=1
```

## The TAG is unaffected

```bash
python3 scripts/validate-contract-release.py verify-tag --remote origin --tag contract-v3.0
```

```text
release verify-tag: pass
exit=0
```

```bash
git ls-remote origin refs/tags/contract-v3.0 'refs/tags/contract-v3.0^{}'
```

```text
59f4f51f2e0ac7c833cdaee9f385e9e83777650e    refs/tags/contract-v3.0
ff9ed81541ab3eb2ebeb2e79676e5a875dd58064    refs/tags/contract-v3.0^{}
```

**`contract-v3.0`'s published bundle verifies at its own commit exactly, and
this feature does not touch it.** A between-cuts edit to an editorial member
reddens `verify-commit --commit HEAD`, which is the state § *What a red
verify-commit at HEAD means* describes and permits; it does NOT redden
`verify-tag`, because the tag verifies the bundle at `ff9ed815` where nothing
moved. That is the whole distinction OD-6 turns on, and it is measured here
rather than argued.
