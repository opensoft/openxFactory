# Implementation Notes — The First Wallet (013)

## Operator rulings (Brett Heap, 2026-08-24, in-session)

Task 4.1's `[OPERATOR]` tag discharged by four decisions:

1. **Key identity**: OPERATOR mints an ed25519 keypair (private half to his
   vault); only the public multibase reaches this lane, where it becomes
   `key_reference.did = did:key:<multibase>` +
   `public_key_multibase`. No private material enters git, CI, or any agent
   session.
2. **holder_class**: `agent` — the council body is software deliberation; the
   OXWA agent-profile targets exactly this class. Core imposes composition on
   no class, so minting legally precedes task 4.4's codexFactory-side
   composition mapping.
3. **Attestation content**: drafted for confirmation rather than dictated;
   draft lives in the attestation file and data-model.md.
4. **Placement**: new `governance/review-authority/` namespace (wallets/ +
   attestations/), chosen over `credentials/wallets/`; S4's register joins
   the same directory (N7 same-tree).

## Grounding facts

See [research.md](./research.md) — eleven verified substrate facts including
the two that shaped this feature most: N7 (same-tree residency or the ceiling
check silently has nothing to resolve against) and the unattested-custody cap
at `request` (the reason task 4.3 exists).

## Gate evidence

### Finalization run (2026-08-24, record complete) — ALL GREEN

- **Operator mint discharged**: Brett Heap supplied the raw 32-byte ed25519
  public key (`7f513713…9dc24ab`); `did:key:z6Mko2FefScUQg9opCriwQmjfcb3Qjnb5bN49hQsEVMo6gee`
  + `public_key_multibase` derived from the public bytes only (multicodec
  `0xed01` + base58btc). Private half never entered this repository or any
  agent session.
- Whole-checkout sweep `--strict`: **exit 0** — `repo scan: 1 openxWallet
  artifact(s) validated, 1546 document(s) skipped as another kind`; corpus
  note unchanged: **17 positives / 36 negatives across 13/13 requirements**
  (SC-001, FR-006, SC-002).
- `pytest tests/wallet_yaml_syntax_gate/ -q`: **4 passed**.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **74 passed,
  0 failed**.
- SC-003 boundary proofs: `git diff origin/main --stat -- contracts/
  scripts/ .github/` → empty; branch diff private-material scan → clean.

### Pre-finalization run (2026-08-24, PENDING did still in tree)

Key-independent gates captured early so finalization is one paste wide:

- `pytest tests/wallet_yaml_syntax_gate/ -q`: **4 passed**
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **74 passed, 0 failed**
- SC-003 contract half: `git diff origin/main --stat -- contracts/ scripts/ .github/`
  → **empty** (zero contract/script/workflow bytes touched)
- SC-002 packaged corpus: exit 0 at **17 positives / 36 negatives across 13/13
  requirements** — unchanged from S2 baseline
- Whole-checkout sweep: **fails closed** on the PENDING record
  (`key_reference/did 'PENDING-OPERATOR-MINT' does not match pattern`) — an
  unfinalized live record cannot slip into a commit; full sweep re-runs green
  at T007x once the mint fills `did` + `public_key_multibase`.

## Boundary ledger

- NOT done here, deliberately: first grant, register + reader (S4), exercise
  records (S3), revocation reconciliation (S5), composition mapping (task
  4.4, codexFactory), README active-changes edits (no OpenSpec change was
  created — this realizes §4 of an existing ratified change).
- Durable note for S4: when the register lands, its path must be named in
  tasks 5.4's floor entry BY NAME together with `governance/review-authority/wallets/`
  — the rows reference wallets that must resolve in the same scan.
