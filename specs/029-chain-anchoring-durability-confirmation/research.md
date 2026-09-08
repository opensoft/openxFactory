# Research: 029-chain-anchoring-durability-confirmation

Status: draft
Kind: research record

## What was measured before anything was authored

**Is the family published?** `git tag --contains 11feff75` → EMPTY.
`grep -c chain-anchoring contracts/releases/contract-v3.3.digests.yaml` → 0.
`grep -c chain-anchoring contracts/manifest.yaml` → 54 references at the basis.
Conclusion: REGISTERED and UNSHIPPED, so a closed enumeration may be replaced.

**Is anybody else in this family?** `gh pr list --state open` at the branch
point: seven open PRs, none a cut (`cut/*`, a "Cut contract-v3.x" title, or a
release-inventory change) and none touching `contracts/chain-anchoring/`.
Conclusion: no collision, and the ordering constraint is this feature's to
carry.

**Is the delta already promoted?** `openspec/specs/chain-anchoring/spec.md` does
not exist — `add-chain-anchoring` is realized but not archived — so both
requirements were realized against the DELTA and cited as the delta.

## Where the precedent came from

* **Registration at realization, no bundle number.** `add-chain-attestation`
  added its eight manifest rows in its realization (`518c670b`) and left the
  version bump and the changelog entry to the cut (`bbbbeda9`);
  `add-chain-anchoring` did the same for twelve rows on the owner's word
  (*"register now"*). This feature adds six rows the same way and leaves
  `contract_bundle_version` and `contracts/CHANGELOG.md` untouched.
* **Subjects, never a second construction.**
  `digest-construction.schema.yaml`'s own header invites a later tranche to add
  SUBJECTS. Tranche two added eleven, tranche three added eleven and then one;
  this amendment adds six, and `canonical.py`'s frozen mirror moves with the
  contract because a reader refusing a subject the contract admits is the same
  defect as a reader admitting one it does not.
* **One fixture per code, filename as index.** Tranche one's carried rule, and
  the reader's self-test enforces it: a code with no probe, a misnamed fixture
  and a fixture that fails for the wrong reason are each findings.

## Two alternatives considered and refused

**Widening `[in_flight, landed, terminally_failed]` instead of replacing it.**
Adding `submitted` and `confirmed` beside the existing three would leave
`in_flight` and `landed` in the vocabulary as a second, ambiguous spelling of
the same states — the drift the family's one-definition rule exists to prevent —
and would leave every consumer free to keep using the word that conflates the
two facts requirement 3 separates. Replacement is available exactly once, before
publication, and this is that window.

**Making the confirmation-profile snapshot OPTIONAL on `configured_witness` and
required only for daily items.** It would have avoided migrating thirty-odd
corpus files. Refused: requirement 3 obliges EVERY configured witness to
reference its window-snapshotted profile in the committed block, and a receipt
whose witnesses name no profile cannot support the submitted/confirmed
distinction the same requirement mandates for every configured witness. The
migration was scripted instead, and the reader's self-test is what proves it.
