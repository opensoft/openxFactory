# The post-merge proof — and the red-first control, over the REAL repository

**WHY THIS FILE EXISTS.** The family reads `contracts/CHANGELOG.md` at the
PUBLISHED TIP, resolved by `git ls-remote origin refs/heads/main`. So the one
claim this PR most needs to make — *`main` goes green, and it goes green
BECAUSE the bundle is declared spent* — cannot be measured from the branch:
the branch's declaration is not on `origin/main` until the squash lands.

**The closest legal stand-in**: a bare repository whose `main` IS this branch,
a clone of it, and the family run there. Nothing is faked — the family does
exactly what it does in CI, over a remote whose `main` happens to carry the
declaration.

## Setup

```bash
git init -q --bare -b main $PROOF/origin.git
cd $SRC && git push -q $PROOF/origin.git HEAD:refs/heads/main
             git push -q $PROOF/origin.git --tags
cd $PROOF && git clone -q $PROOF/origin.git work && cd work
```

The simulated origin, read back:

```text
2c3e0c9eb005566113967be077ece57c7e99b748    refs/heads/main
59f4f51f2e0ac7c833cdaee9f385e9e83777650e    refs/tags/contract-v3.0
```

`59f4f51f` is `contract-v3.0`'s REAL published tag object and it peels to
`ff9ed81541ab3eb2ebeb2e79676e5a875dd58064`, the squash of PR #573 — so the
successor guard is satisfied by the actual published tag, not by a fixture.

## A. WITH the declaration at the published tip — the state is ACCEPTED

```text
findings: 1
  [info] key=('release-tag-publication', 'openxFactory',
              'contracts/releases/contract-v2.6.digests.yaml')  class=contested
  rule: contract-v2.6 is SPENT: it was cut, was never publishable, and is
        declared spent by the reserved SPENT declaration at
        contracts/CHANGELOG.md line 374, inside the contract-v3.0 entry —
        contract-v3.0 superseded it and carries a published annotated tag on a
        commit that declares it. …
```

And the self-gate, unedited, over that same clone:

```bash
python3 -m pytest "tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire" -q
```

```text
1 passed in 2.02s
```

**THAT IS THE "GREEN AT THE SQUASH" CLAIM, MEASURED RATHER THAN PREDICTED.**

## B. WITHOUT it — the `error` returns. This is the red-first control.

The declaration line removed from that origin's `main` and re-pushed; nothing
else touched:

```text
findings: 1
  [error] key=('release-tag-publication', 'openxFactory',
               'contracts/manifest.yaml')
  rule: contract-v2.6 was cut and SUPERSEDED without ever being published: it
        has a release inventory, the manifest has moved on to contract-v3.0,
        and it has no published annotated tag …
```

```text
FAILED tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed in 1.67s
```

## What the two halves together establish

* `main` goes green **because `contract-v2.6` is EXPLICITLY DECLARED spent**,
  and **never** because an undeclared bundle started passing — which is
  precisely what OpenSpec task 2.1 requires be verified rather than asserted.
* The finding key the estate acquires is
  `(release-tag-publication, openxFactory, contracts/releases/contract-v2.6.digests.yaml)`
  at `info`, class `contested` — a NEW path, not the `contracts/manifest.yaml`
  identity the `error` held, which is OD-5 as amended working as designed.
* The severity moved `error` → `info` and the PATH moved with it, so the
  pre-existing key simply ceases to exist rather than changing class. It was
  `auto-fixable`, so its disappearance raises no uncited-resolution; the key
  that replaces it is `contested`, so ITS disappearance would.
