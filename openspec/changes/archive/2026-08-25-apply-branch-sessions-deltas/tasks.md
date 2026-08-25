# Tasks: Apply the Branch-Sessions Deltas

## 1. Restate the ratified delta

- [x] 1.1 Confirm the gap before writing anything, from the real family
      rather than by eye: `python3 scripts/doc-health.py --single-repo .
      --family promotion-fidelity` reports exactly two findings, both against
      `2026-08-01-add-workbench-branch-sessions` — ADDED
      `Branch-session notebooks` absent from
      `openspec/specs/lifecycle-notebook-projection/spec.md` entirely, and
      `Corpus scan scope` arrived without 1 of its 4 ratified scenarios
- [x] 1.2 Confirm canon has NOT drifted since the 2026-07-31 archive. The
      `Corpus scan scope` region hashes to `bbb402c4…e3d57` at `1efa5756`
      (its 2026-07-12 introduction), at `a0ea7666` (the source archive), and
      at all three later commits touching the file — `d5e6d428`, `e9a4be6e`,
      `18a4ffc3` — and at the pre-apply head; `Branch-session notebooks`
      hashes ABSENT at every one. The three later commits touched other
      requirements only. No archived delta for this capability carries a
      `RENAMED` block. Applying the ratified text therefore clobbers no later
      ratified work
- [x] 1.3 Author this packet's delta as a byte-for-byte copy of the archived
      delta file — same SHA-256
      `f6ffd39abeab7a1548a93ed78fda9a24d8da19606fbc5f30dc85fe013b0361cd`, no
      re-wording, no re-derivation

## 2. Validation

- [x] 2.1 `OPENSPEC_TELEMETRY=0 openspec validate apply-branch-sessions-deltas --strict`
- [x] 2.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
- [x] 2.3 List this change in the README's OpenSpec Records block

## 3. Promotion and archive

- [x] 3.1 Promote the delta into
      `openspec/specs/lifecycle-notebook-projection/spec.md` through
      `openspec archive` and archive this packet (promotion-only;
      `code_surface: none`, so it archives on landing)
- [x] 3.2 Prove the fidelity by sha256 rather than asserting it: each
      promoted requirement block extracted from canon hashes identical to the
      same block extracted from the ratified delta
- [x] 3.3 Re-validate after promotion (`--all --strict`; the single-change
      form no longer applies once archived) and re-run the promotion-fidelity
      family: openxFactory reads ZERO findings. Re-run
      `python3 -m pytest tests/doc-health` and
      `python3 -m pytest tests/ideation-dashboard -k workbench` at baseline,
      and confirm the whole-repo doc-health report moves on the
      promotion-fidelity line and nowhere else
- [x] 3.4 Tick `add-promotion-fidelity-check` task 5.1, which its own RULED
      note says closes when this change lands
