# Staged fragment: Chain Selection Study — signed execution chain and records anchoring

Status: staged
Kind: research
Summary: Research input for this topic's chain-selection question (Q3) and its
on-chain layer. Reviews Kaspa in depth as the named candidate against a
comparison set, tests the stakeholder's three priors, and recommends an
off-chain signed transparency log as the primary custody record, Bitcoin
(OpenTimestamps aggregation) as the primary anchor, Kaspa as an optional
low-latency secondary anchor, and consent logic in a governed permissioned
layer whose state roots are anchored — NOT smart contracts on the anchoring
chain. Vendored verbatim 2026-08-27.

Provenance and standing. Prepared 2026-08-27 as a parallel research fan-out for
the `signed-execution-chain` topic and vendored here unchanged below this
header. It is RESEARCH INPUT, not governance text: nothing in it is ratified by
being vendored, and the topic cites its recommendation rather than restating it
as settled. Its original header read `**Status:** brainstorm (research input;
not a governance doc)`; it is relabelled `staged` here only because a
brainstorm-status document may not live under `ideation/staging/`
(document-lifecycle location-conformance) — the relabel changes the filing, not
the epistemic status. One citation in §1.2 labels a live price page as a
`2026-08-28 snapshot` where every other source line reads `checked 2026-08-27`;
the original meta line's *unless noted* clause covers exactly that case, and
the body is not edited to reconcile it. Original meta lines, verbatim:

**Date:** 2026-08-27 (all prices/fees/network figures are snapshots as of this date unless noted)
**Scope:** Deep review of Kaspa as the named candidate; comparison set (Bitcoin, Ethereum+L2, Algorand, Hedera, Cardano, Ergo, permissioned/hybrid); architecture recommendation; cost model.
**Method note:** Every load-bearing claim carries a source and a date-check. Where sources conflict or could not be verified, that is stated inline and collected in §9.

---

---

## 0. Executive verdicts

**On Kaspa:** Real, live, fast, absurdly cheap, and genuinely fair-launched — but small ($0.8B cap, ~$20M/yr security budget, thin liquidity, 582 public nodes), with mining-pool concentration roughly as bad as Bitcoin's, a smart-contract stack that is weeks-to-months old, and an L1 that **prunes transaction data after ~3 days**, which directly constrains the anchoring use case. Fit as a *low-latency secondary anchor*: good. Fit as the *sole 10-year anchor of regulated records* or as the *consent-logic execution layer*: not today.

**The three priors:**
1. *"Kaspa is one of the only non-captured chains besides Bitcoin"* — **QUALIFIED.** The launch-fairness and no-foundation-control claims check out; the operational-capture picture (pools, ASICs, one public miner targeting 16% of hashrate, VC-funded L2 companies absorbing core devs) does not support "non-captured" as an absolute, and the set of credibly neutral chains is larger than {Bitcoin, Kaspa}.
2. *"Bitcoin is just too expensive"* — **REFUTED for anchoring** (Merkle aggregation / OpenTimestamps makes Bitcoin anchoring ~$0 marginal per record, and even naive hourly self-anchoring is ~$2k/yr); **CONFIRMED only** for per-record individual transactions and for smart-contract execution, which Bitcoin cannot do anyway.
3. *"KAS is fractions of a penny per transaction"* — **CONFIRMED**, and understated: typical fees are fractions of a *thousandth* of a penny (~$0.000001–0.000003). Caveat: this is partly a symptom of low demand and a security budget the fee market does not yet fund.

**Recommended architecture (§7):** an off-chain signed transparency log as the primary custody record; **Bitcoin (OpenTimestamps-style aggregation) as the primary anchor**; **Kaspa as an optional low-latency secondary anchor** (cost is negligible, honors the stakeholder's direction, adds an independent PoW witness); **consent/enrollment logic in the governed permissioned layer** (Hermes policy plane / consortium ledger) with state roots anchored publicly — *not* on the anchoring chain, and *not* on Kasplex/Igra in 2026; **no PHI or PHI-derived plain hashes on any public chain** (salted commitments only — EDPB Guidelines 02/2025 v2.0 treat hashes of personal data as personal data). Chain-agnostic receipt format so anchoring targets are pluggable over the 10-year horizon.

---

## 1. Kaspa in depth

### 1.1 Architecture and current throughput — VERIFIED LIVE

- **blockDAG + GHOSTDAG (PHANTOM):** parallel blocks are incorporated rather than orphaned; consensus produces a linear ordering over the DAG; the "freeloading bound" prevents attackers leveraging honest blocks for reorgs. PoW hash function is **kHeavyHash** (ASIC-dominated since 2023–24). ([kaspa.org — What is GHOSTDAG and DAGKNIGHT](https://kaspa.org/what-is-ghostdag-and-dagknight/); [kaspahub — time to finality](https://kaspahub.org/post/kaspa-time-to-finality/), checked 2026-08-27)
- **Crescendo hardfork (May 5, 2025):** raised block rate from 1 to **10 blocks/sec** (100 ms blocks); live and stable for ~16 months. ([kaspa.org Crescendo roadmap](https://kaspa.org/crescendo-hard-fork-roadmap-10bps/); [kasmedia](https://kasmedia.com/article/the-crescendo), checked 2026-08-27)
- **Toccata hardfork (activated June 30, 2026, DAA 474,165,565):** the "Covenants++" upgrade — native **L1 covenants**, transaction introspection, transaction v1, script pricing, an **OpZkPrecompile** for trustless L1 ZK-proof verification, partitioned sequencing commitments for based-rollup scaling, and "Silverscript" tooling. This is L1 programmability of the covenant/introspection kind — **not** an EVM and not general smart contracts on L1. ([rusty-kaspa toccata-guide.md](https://github.com/kaspanet/rusty-kaspa/blob/master/docs/toccata-guide.md); [BSCN activation announcement](https://x.com/BSCNews/status/2062907796589260907); [kaspahub Toccata explainer](https://kaspahub.org/post/kaspa-toccata-hard-fork/), checked 2026-08-27)
- **Confirmation/finality:** probabilistic finality typically **<7 seconds** to reach Bitcoin-6-block-equivalent security; deterministic finality depth ~**12 hours** (post-Crescendo; was 24h) — until that depth a reorg is theoretically possible. **DAGKnight** (2027 target) aims at parameterless, latency-responsive consensus, sub-second finality, 32→100 bps. ([kaspahub TTF](https://kaspahub.org/post/kaspa-time-to-finality/); [Kaspalytics glossary](https://www.kaspalytics.com/learn/glossary); [gate.com DAGKnight guide](https://www.gate.com/post/status/16375253), checked 2026-08-27)

### 1.2 Fees and payload capacity — CONFIRMED CHEAP; payload natively supported

- Minimum fee is 1 sompi/gram of "mass"; a typical transaction is ~**0.00002 KAS**; common wallet formula ~0.0001 KAS/UTXO. At $0.0290/KAS ([CoinGecko/crypto.news, 2026-08-28 snapshot](https://crypto.news/price/kaspa/)) that is **$0.0000006–$0.000003 per transaction** — millionths of a dollar. Fees are dynamic and rise under congestion; Kaspalytics tracks the live average. ([kaspa.aspectron fee docs](https://kaspa.aspectron.org/transactions/fees/fee-rate-qos.html); [Kaspalytics average-fee chart](https://www.kaspalytics.com/app/transactions/accepted/fees/average), checked 2026-08-27)
- **Data-carrying:** transaction payloads are enabled (post-Crescendo; KIP-9 mass model + KIP-13 payload charging). Max transaction size **100 KB**; payload bytes charged ~1 gram/byte; block transient-storage cap ~125 KB. A 32-byte anchor commitment is trivial and costs effectively nothing. ([kaspanet/docs Transactions.md](https://github.com/kaspanet/docs/blob/main/Reference/Transactions.md); [KIP-9](https://github.com/kaspanet/kips/blob/master/kip-0009.md); [KIP-13](https://github.com/kaspanet/kips/blob/master/kip-0013.md), checked 2026-08-27)

### 1.3 The smart-contract situation, honestly

**L1:** no general smart contracts. Toccata (live 2026-06-30) gives covenants + introspection + ZK verification — powerful primitives for vaults and based-rollup commitments, but low-level, ~8 weeks old in production, with tooling ("Silverscript") that has no meaningful audit history yet. On-chain covenant usage is real but small (~1,200 covenant-creating txs/day per CoinMarketCap's AI digest of late-Aug 2026 on-chain data — **weak source, treat as order-of-magnitude**). ([CMC latest-updates](https://coinmarketcap.com/cmc-ai/kaspa/latest-updates/), checked 2026-08-27)

**L2s — both mainnet, both very young, both tiny:**
- **Kasplex zkEVM** — EVM-compatible based rollup, KEF-affiliated; public testnet May 2025; mainnet launch announced Aug 2025, slipped, then **went live ~late Sept 2025**; uses bridged KAS as gas; published a pre-launch security audit. First place Kaspa DeFi existed. TVL reached **~$3.7M by Oct 2025** and remains single-digit millions. ([Kasplex mainnet announcement](https://x.com/kasplex/status/1971469795317960800); [delay notice](https://x.com/kasplex/status/1961062004057166266); [KaspaDaily audit note](https://kaspadaily.com/kasplex-publishes-security-audit-ahead-of-l2-mainnet-launch/); [DailyKaspa TVL](https://x.com/DailyKaspa/status/1976250036515111350); [DefiLlama chain page](https://defillama.com/chain/kasplex), checked 2026-08-27)
- **Igra Network** — based rollup with full EVM, no centralized sequencer (Kaspa miners order Igra txs blind → structural MEV/censorship resistance), claimed 3,000+ TPS, sub-second finality; **public mainnet March 19, 2026** after ~6 months of testnet (730k txs, zero state divergence); ~**54k txs/day** by late Aug 2026 (CMC AI digest — weak source); team includes ex-DAGLabs engineers; **IGRA token auction March 2026** (i.e., a VC/token-funded company). ([Chainwire launch release](https://chainwire.org/2026/03/19/igra-network-launches-public-mainnet-as-decentralized-evm-layer-on-kaspas-proof-of-work-blockdag/); [kaspa.org node rollout](https://kaspa.org/igra-labs-public-node-rollout/), checked 2026-08-27)

**What can be deployed TODAY:** an EVM contract on Kasplex or Igra mainnet — genuinely, not vaporware. **What should not be deployed today:** regulated consent/enrollment logic on either — both are <12 months old in production, TVL is a rounding error (aggregate ecosystem protocols like KaspaCom hold ~$78k; ([DefiLlama](https://defillama.com/protocol/kaspacom))), bridge/custody trust assumptions are not yet independently documented in depth (we could not locate a public, third-party analysis of the Kasplex bridge's mint-control or Igra's bridging modules — see §9), and the L1 primitives they settle against changed two months ago.

### 1.4 Decentralization: nodes, mining, ASICs — the uncomfortable numbers

- **Public nodes: 582 active** (2026-08-16; lifetime average 459). Compare Bitcoin's ~20k reachable listeners. Low but not trivial. ([kaspanodes.com](https://kaspanodes.com/), checked 2026-08-27)
- **Hashrate:** ~350–420 PH/s in mid-2026 (down from 700+ PH/s 2024 peaks as margins compressed). ([MiningReturns 2026 guide](https://miningreturns.com/news/kaspa-asic-mining-era-what-you-need-to-know); [MiningPoolStats](https://miningpoolstats.net/coins/kaspa/), checked 2026-08-27)
- **Pool concentration:** our 2026-08-27 read of MiningPoolStats shows the top pool (HumPool) at roughly **~35%** and the **top three pools at ~70%** of network hashrate (site scrape is imprecise — see §9 — but the concentration order-of-magnitude is robust). That is a Nakamoto coefficient of ~2–3 at the pool level — **comparable to Bitcoin's** (Foundry ~27–31%, top-4 >70%, Nakamoto coefficient 3; ([CoinDesk 2026-05-11](https://www.coindesk.com/markets/2026/05/11/bitcoin-mining-pools-with-75-of-btc-hashrate-join-open-standard-for-block-construction); [D-Central H1-2026](https://d-central.tech/bitcoin-mining-pool-comparison-2026/))).
- **ASIC concentration:** kHeavyHash hardware is a Bitmain (KS-series) / IceRiver duopoly-ish supply chain; GPUs are non-competitive by ~100x. ([MiningReturns](https://miningreturns.com/news/kaspa-asic-mining-era-what-you-need-to-know), checked 2026-08-27)
- **Institutional hashrate:** MARA (Marathon) publicly deployed Kaspa ASICs from Sept 2023 with a stated plan to reach **~16% of global Kaspa hashrate** single-handedly. Whatever its current share, one US-listed, KYC-compliant company being able to buy a sixth of the network for ~$60M of hardware is the concrete measure of how cheap Kaspa capture-by-hashrate is. ([MARA press release](https://ir.mara.com/news-events/press-releases/detail/1360/marathon-digital-holdings-announces-kaspa-mining-operations); [CryptoSlate](https://cryptoslate.com/marathon-digital-diversifies-revenue-by-mining-kaspa-aims-for-16-global-hash-rate/), checked 2026-08-27)

### 1.5 Governance, funding, and the "non-captured" claim

**Supports the claim:**
- **Fair launch verified:** Nov 7, 2021; no premine, no ICO, no allocations. DAGLabs (the pre-launch R&D company) was funded ~$8M by Polychain, Accomplice and Genesis Mining, but the funding bought equity in a company, not tokens; DAGLabs mined **<3% of supply openly post-launch** on rented hardware, then dissolved; DAGLabs and Polychain waived IP (Feb 2024). ([Kaspa wiki — prehistory/tokenomics](https://wiki.kaspa.org/en/prehistory); [Messari profile](https://messari.io/project/kaspa/profile), checked 2026-08-27)
- **No controlling foundation or treasury:** protocol direction is KIPs + rough consensus among community core devs (Sutton, Newman, Wyborski, with Sompolinsky as research lead); the Kaspa Ecosystem Foundation (KEF) is a community support/grants body, not a protocol owner; there is no protocol treasury. ([kaspa.org LORE](https://kaspa.org/about-kaspa/); [KasLens history](https://kaspa-lens.com/kaspa/wiki/introduction-to-kaspa/history-of-kaspa-and-fair-launch), checked 2026-08-27)

**Cuts against the claim:**
- Operational concentration (§1.4) is what capture actually looks like in PoW, and Kaspa's is no better than Bitcoin's — on a network ~150x smaller in hashrate value, so absolute capture cost is far lower.
- **No treasury cuts both ways:** nothing to capture, but also no funded immune system — ecosystem observers note Kaspa "relies almost entirely on organic growth," with no budget for listings, audits, or sustained development ([CaptainAltcoin on the fair-launch curse](https://captainaltcoin.com/why-kaspa-kas-fair-launch-might-be-its-biggest-curse/), checked 2026-08-27). The programmability layer is consequently being built by **VC/token-funded private companies** (Igra Labs — token auction; Kasplex — KEF-backed), including ex-DAGLabs personnel. If Kaspa's usable functionality migrates to L2s, effective control of the *platform users touch* sits with those companies: an emerging capture vector the "fair launch" framing hides.
- **Adversarial material reviewed for balance:** a Substack piece ("a factual account of the kaspa fraud") alleges an undisclosed two-week post-launch genesis restart and unverifiable early history due to pruning. The piece presents speculation as fact and advocates delisting (low credibility), but its one structural observation is real and appears independently in Kaspa's own docs: **pre-pruning-point history is not cryptographically re-verifiable from genesis; it rests on a social-consensus assumption** ([JC/Medium — why archive nodes are no longer essential (describes the hybrid trust model)](https://medium.com/@jcroger/why-archive-nodes-are-no-longer-essential-the-kaspa-proof-f15d3b64d24a); [techleaks24 substack](https://techleaks24.substack.com/p/a-factual-account-of-the-kaspa-fraud), both checked 2026-08-27).

**Verdict on "non-captured":** Kaspa has *credibly neutral issuance and protocol governance* — rarer than it should be, and the stakeholder's instinct is directionally sound. But by measurable operational criteria (pool concentration, ASIC supply, purchasable hashrate share, corporate L2 layer) it is not categorically different from several other chains, and its small economic size makes capture *cheaper*, not harder. See §5 for the cross-chain capture table.

### 1.6 Ecosystem maturity

- **Wallets:** Kaspium (iOS/Android, open source), Kaspa NG/KDX, Kasware (browser), Ledger support. ([kaspium.org](https://www.kaspium.org/); [kaspa.org/build](https://kaspa.org/build), checked 2026-08-27)
- **Libraries/indexers:** rusty-kaspa (Rust node, v1.1.0 Apr 2026), first-class **WASM32 SDK** for JS/TS (RPC, wallet, transaction primitives) — integration-quality tooling genuinely exists; REST API and community indexers exist but are few and largely volunteer-run. ([rusty-kaspa/wasm](https://github.com/kaspanet/rusty-kaspa/tree/master/wasm); [aspectron SDK docs](https://kaspa.aspectron.org/docs/), checked 2026-08-27)
- **Liquidity/market:** KAS ~$0.029, market cap ~**$0.80B, rank #85**, reported 24h volume ~$10M+ (per crypto.news snapshot — thin; see §9), **~85% below its 2024 peak**. Listed on Kraken, Bitget, Bybit, Bitvavo, MEXC, Gate, HTX and (reported) Coinbase; **still no Binance spot listing** (futures only) — community attributes this to having no treasury to pay listing costs. ([crypto.news price page](https://crypto.news/price/kaspa/); [Bitget exchange-listings guide](https://www.bitget.com/academy/12560603876303); [CaptainAltcoin on Binance absence](https://captainaltcoin.com/why-kaspa-kas-is-not-yet-on-binance-alleged-listing-demand-raises-eyebrows/), checked 2026-08-27)

### 1.7 Kaspa-specific risks for THIS workload

1. **Pruning vs. long-horizon proof availability (the big one).** Standard nodes retain ~**3 days** of transaction data; older history lives only on **archival nodes**, which are hard to run (rsync bootstrap from an existing archival operator) and few. History before the pruning point is guaranteed socially, not cryptographically. For an anchoring layer whose proofs must be independently verifiable in year 10 — possibly in litigation — this means: capture full inclusion proofs at anchor time, retain them in the factory's evidence store, and **run your own archival node** if Kaspa anchors carry any compliance weight. Verification then depends on your own retained evidence plus a socially-maintained header history — materially weaker than Bitcoin, where every one of ~20k full nodes can re-derive any anchor from genesis. ([KasLens node guide](https://kaspa-lens.com/kaspa/wiki/getting-started-with-kaspa/running-a-kaspa-node); [Kaspa wiki FAQ](https://wiki.kaspa.org/en/faq); [JC/Medium](https://medium.com/@jcroger/why-archive-nodes-are-no-longer-essential-the-kaspa-proof-f15d3b64d24a), checked 2026-08-27)
2. **Security budget, small and falling.** Emission is ~21–22 KAS/s in Aug 2026 (32.70 KAS/s Jan 2026 → 17.32 Dec 2026, smooth monthly (1/2)^(1/12) decay; ~95% of the 28.7B supply already mined as of July 2026). That is ≈ **$20M/yr of security spend at current prices** (our computation from the emission schedule × $0.029) vs. Bitcoin's ≈ $13B/yr. Fee revenue is negligible, so security rides on emission that halves yearly into a fee market that does not yet exist. Ten-year survivability is an open bet. ([kaspa.org emission schedule PDF](https://kaspa.org/wp-content/uploads/2022/09/KASPA-EMISSION-SCHEDULE.pdf); [kas.live rewards](https://kas.live/rewards.html); [Kaspa wiki tokenomics](https://wiki.kaspa.org/en/tokenomics), checked 2026-08-27)
3. **Reorg/finality nuance.** Practical confirmation is seconds; deterministic finality is ~12h. For anchoring this is fine (an anchor that lands is cheap to re-issue if a rare deep reorg dropped it), but the evidence pipeline must tolerate anchor-tx invalidation within the finality window.
4. **L2 trust assumptions.** Based-rollup sequencing inherits L1 ordering (good), but *bridges* (Kasplex's bridged-KAS gas custody, Igra's bridging modules) are the trust point, and neither has deep independent public analysis yet (§9). Two hardforks in 14 months (Crescendo, Toccata) also means L1 consensus surface is still moving under the L2s.
5. **Historical-data explorers** and indexer infrastructure are community-run; there is no Blockstream/Mempool.space-grade neutral archive institution.

---

## 2. Bitcoin — and the aggregated-anchoring counterargument

- **Fees now:** ~1–3 sat/vB typical (economy 1, next-block ~3, Aug 2026); a ~140–150 vB tx = ~150–450 sats ≈ **$0.12–$0.36** at BTC ≈ $79k (BTC opened $78,982 on 2026-08-25). Median 2025–26 conditions 1–20 sat/vB; historical spikes (ordinals era 2023–24) exceeded 100 sat/vB — fee volatility is real and must be assumed to recur. ([SatsBeat live fees / starlighttools, Aug 2026](https://satsbeat.com/fees); [Coinbase ETH/BTC price pages](https://www.coinbase.com/price/ethereum), checked 2026-08-27)
- **The aggregation counterargument — decisive.** OpenTimestamps calendar servers batch unbounded numbers of digests into one Merkle tree and commit its root in **one Bitcoin tx every few hours**; public calendars are free, no registration; each client keeps a compact proof (digest → Merkle path → Bitcoin block header). Marginal cost per anchored record: **$0** on public calendars; running your *own* calendar at hourly cadence costs ~24 × $0.24 ≈ **$6/day ≈ $2.1k/yr flat, at any volume**. "Bitcoin is too expensive" is simply false for commitment anchoring; it is true only for one-tx-per-record designs. ([opentimestamps.org](https://opentimestamps.org/); [Peter Todd's design announcement](https://petertodd.org/2016/opentimestamps-announcement); [opentimestamps-server README](https://github.com/opentimestamps/opentimestamps-server), checked 2026-08-27)
- **Trade-off:** anchor *latency* is Bitcoin's block cadence plus calendar batching (minutes–hours to first confirmation, ~1h to deep confirmation). For "the merge decision was anchored within seconds," Bitcoin alone doesn't give you that; that is the one legitimate gap a fast secondary anchor (Kaspa) fills.
- **Capture status:** most credibly neutral asset issuance and protocol ossification in the industry; but mining-pool concentration is real (Foundry ~27–31%, Foundry+AntPool >51% of blocks, Nakamoto coefficient 3; 75%-of-hashrate pools did adopt an open block-construction standard in May 2026, a mild decentralizing step). Template-level censorship by pools is a live theoretical concern for *payments*; for *anchoring* it is weak (an anchor tx is indistinguishable from any payment, and one confirmed tx anywhere suffices). ([CoinDesk 2026-05-11](https://www.coindesk.com/markets/2026/05/11/bitcoin-mining-pools-with-75-of-btc-hashrate-join-open-standard-for-block-construction); [D-Central](https://d-central.tech/bitcoin-mining-pool-comparison-2026/), checked 2026-08-27)
- **Smart contracts:** none of the kind this design needs. Bitcoin is an anchor, not an execution layer.
- **Longevity/verifiability:** the strongest 10-year survivor probability in the field; every full node holds all history; OTS proofs remain verifiable against nothing but a header chain.

## 3. Ethereum + representative L2 (Base)

- **L1:** gas ~0.43 gwei (near historic lows, Aug 2026). A simple 21k-gas anchor tx ≈ 9k gwei ≈ $0.03–0.04; a ~100k-gas EAS attestation ≈ **$0.10–0.15**. History is permanent on archive infra; enormous tooling. Capture status: contested-but-decent — Lido holds **~28.5% of staked ETH** (>60% of liquid staking), one consensus client still >50% of validators; execution-client diversity is now healthy (Geth/Nethermind ~⅓ each); post-Merge OFAC-relay censorship pressure has been reduced but the stake-concentration trend line is adverse. ([BlockAlive 2026 scorecard](https://www.blockalive.com/how-decentralized-is-ethereum/); [CoinDesk staking 2026-08-27](https://www.coindesk.com/coindesk-indices/2026/08/27/crypto-for-advisors-how-staking-on-ethereum-is-changing-in-2026); [Lido scorecard](https://lido.fi/scorecard), checked 2026-08-27)
- **Base (representative L2):** median fee **~$0.02–0.05/tx** (Q1–Q2 2026); EIP-4844 blobs cut L2 costs 80–90% since 2024. **Ethereum Attestation Service (EAS)** is deployed, mature, schema-based, with on-chain and free off-chain attestation modes — the closest existing production system to "signed build/review attestations." Capture honesty: Base's sequencer is run by Coinbase (a single US corporation); it has fraud-proof exit to L1 (Stage 1), so the *records* inherit Ethereum's neutrality even though *liveness/ordering* is corporate. For consent/enrollment *logic* (not value custody), that trade is often acceptable; Arbitrum is the less-corporate alternative at ~$0.04–0.09/tx. ([eco.com L2 comparison 2026](https://eco.com/support/en/articles/14798699-best-ethereum-l2s-in-2026-fees-tvl-tps-compared); [Everstake L2 2026](https://everstake.one/resources/blog/arbitrum-vs-optimism-vs-base); [attest.org docs](https://docs.attest.org/docs/core--concepts/onchain-vs-offchain), checked 2026-08-27)

## 4. The capture-axis comparators

- **Algorand** — technically a good anchoring fit (flat 0.001 ALGO ≈ **$0.000094**/tx at ALGO $0.094; ~1 KB note field; instant finality). Capture: **foundation-centric** — relay nodes historically hand-picked and rewarded by the Algorand Foundation, a structural gatekeeping point critics note could be compelled into OFAC-style compliance; a P2P gossip network to remove relay reliance is live opt-in and rolling out, but governance and funding remain foundation-anchored. Fails the stakeholder's axis today, on a trajectory to improve. ([Algorand dev portal fees](https://dev.algorand.co/concepts/transactions/fees/); [algonaut.space relay-node critique](https://algonaut.space/algorand-nodes/); [Algorand 2025 roadmap](https://algorand.co/blog/web3-core-values-from-algorands-2025-roadmap); [CoinMarketCap ALGO 2026-08-23](https://coinmarketcap.com/currencies/algorand/), checked 2026-08-27)
- **Hedera** — the strongest pure *workload* comparator: Hedera Consensus Service is literally a purpose-built, ordered, timestamped attestation log ("decentralized Kafka") marketed for audit logs and healthcare access-grant logging. But it is **captured by design**: up to 39 council corporations run the permissioned consensus nodes and vote on fees/upgrades; and in **January 2026 the council raised the HCS message fee 8x, $0.0001 → $0.0008** — a live demonstration of pricing power the stakeholder is right to distrust. Included here as the honest benchmark of "what the captured version of exactly this product looks like." ([hedera.com HCS](https://hedera.com/service/consensus-service/); [price-update blog, Jan 2026](https://hedera.com/blog/price-update-to-consensussubmitmessage-in-consensus-service-january-2026/); [hederacouncil.org](https://hederacouncil.org/), checked 2026-08-27)
- **Cardano** — the interesting counterexample to "only Bitcoin and Kaspa": Voltaire governance completed (March 2026) — on-chain tripartite governance (DReps / constitutional committee / SPOs) now controls 100% of treasury allocation, and IOG is actively devolving core development to independent teams (three node implementations targeted by 2027). Genuinely decentralizing, with a *funded* treasury — arguably a stronger 10-year institutional posture than Kaspa's unfunded volunteerism. Workload fit is mediocre (fees ~0.17 ADA ≈ several cents; modest throughput; Plutus contracts capable but nothing here needs them). ([CoinReporter, Voltaire completion 2026-03](https://www.coinreporter.io/2026/03/cardano-completes-voltaire-governance-phase-unlocking-full-decentralization/); [Decrypt on IOG devolution](https://decrypt.co/373749/caradno-ada-price-spikes-iohk-decentralizing-development); [Cardano docs governance](https://docs.cardano.org/about-cardano/governance-overview), checked 2026-08-27)
- **Ergo** — closest to Kaspa's ethos (fair-launch PoW, ASIC-resistant Autolykos v2, UTXO smart contracts) and by launch criteria as "non-captured" as anything — which itself falsifies the "only Kaspa and Bitcoin" framing. But network hashrate is ~**2 TH/s** of GPU work with a micro-cap economy: the security budget is far too small to anchor regulated records against a motivated adversary. Assessed and excluded on security-budget grounds. ([2Miners ERG hashrate](https://2miners.com/erg-network-hashrate); [ergoblockchain.org miners page](https://www.ergoblockchain.org/miners), checked 2026-08-27)

## 5. Capture scorecard (as of 2026-08-27)

| Chain | Issuance fairness | Protocol governance | Operational concentration | Treasury/funding capture | Net "non-captured" grade |
|---|---|---|---|---|---|
| Bitcoin | Clean (2009 caveat: none) | Ossified, no owner | Pools: top-4 >70%, NC=3 | None | **A−** |
| Kaspa | Clean fair launch, <3% DAGLabs open mining | KIPs, no foundation control | Pools ~top-3 ≈70%; MARA alone targeted 16%; ASIC duopoly | No treasury (unfunded ≠ uncapturable); VC-funded L2 layer | **B+** (A− issuance, B− operations) |
| Ergo | Clean | Community | GPU-dispersed but tiny | Minimal | B+ (but security-irrelevant scale) |
| Ethereum | ICO-era premine legacy | EF-influenced, broadly credible | Lido 28.5% stake; CL client >50% | EF treasury, large | **B−** |
| Cardano | ICO-era allocations | On-chain, newly community-controlled | SPO distribution decent | On-chain treasury, community-voted | B− and improving |
| Base (L2) | n/a | Coinbase-controlled sequencer/upgrades (Stage 1 exits) | Single corporate operator | Corporate | D as a chain; records inherit ETH L1 |
| Algorand | Foundation/insider allocations | Foundation-led | Relay-node gatekeeping (migrating to P2P) | Foundation treasury | **C** |
| Hedera | Corporate allocation | 39-corporation council; fee votes (8x HCS raise, Jan 2026) | Permissioned nodes | Council treasury | **D** (by design) |

**Reading:** the stakeholder's capture instinct correctly sorts Hedera/Algorand to the bottom and Bitcoin to the top. It errs in treating Kaspa as Bitcoin's peer (operationally it is a much cheaper capture target) and in ignoring that capture-resistance must be *weighted by the economic security actually protecting the record* — where Bitcoin is ~650x Kaspa.

## 6. The PHI / regulated-records layer

- **Non-negotiable baseline:** raw or encrypted PHI never goes on a public chain. Universal 2025–26 guidance is the hybrid pattern: PHI off-chain in HIPAA-controlled repositories (BAAs, access controls, audit); on-chain only tamper-evidence. Permissioned networks are the standard vehicle where multiple covered entities must *share* state (the Avaneer Health consortium — Aetna/Anthem/Cleveland Clinic/HCSC/IBM/PNC/Sentara — and Synaptic Health Alliance are the live precedents; note both pivoted toward FHIR-based utility networks where blockchain is plumbing, not product). ([HIPAA Vault strategies](https://www.hipaavault.com/resources/blockchain-integration-healthcare-records/); [AccountableHQ HIPAA+blockchain guide](https://www.accountablehq.com/post/hipaa-and-blockchain-a-practical-guide-to-compliance-and-healthcare-use-cases); [Ledger Insights on Avaneer](https://www.ledgerinsights.com/leading-healthcare-firms-launch-blockchain-utility-avaneer-health/), checked 2026-08-27)
- **Sharper than the folk wisdom — hashes are not safe either.** EDPB **Guidelines 02/2025 (v2.0 adopted 2026-07-07)**: do not store clear, encrypted **or hashed** personal data on-chain; *a hash of personal data is itself personal data*; erasure/rectification must be designed in from the start. Under HIPAA, a bare hash of a record is not Safe-Harbor de-identified either. **Design consequence:** anchor only *salted, keyed commitments* (e.g., HMAC over content with a per-record secret salt held in the governed layer); destroying the salt renders the on-chain residue effectively anonymous, satisfying erasure by design. Consent *state* likewise must not be publicly linkable to a person — consent lives in the permissioned layer; the public chain sees only opaque commitments to consent-log checkpoints. ([EDPB Guidelines 02/2025 v2 PDF](https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf); [Bird & Bird practical guide](https://www.twobirds.com/en/insights/2026/netherlands/edpb-adopts-final-guidelines-on-blockchain-and-personal-data-a-practical-guide-for-organisations), checked 2026-08-27)
- **Interop reality check:** hospital/insurer interoperability in the US runs on FHIR/TEFCA rails, not chains; a chain layer earns its place only as the *neutral integrity witness* those rails lack (who consented to what, when; which record version was exchanged). Scope the chain ambition accordingly.

## 7. Recommended architecture

**Layer 0 — Evidence plane (off-chain, the actual record).** An append-only signed transparency log (RFC-6962-style Merkle tree — the Sigstore/Rekor and Certificate Transparency pattern) inside the factory's governed store: every proposal ratification, build attestation, review verdict, merge decision is a signed leaf (content hash + signature + role identity from the roles-authority model). This — not any blockchain — is the primary chain of custody. Blockchains only make it *externally undeniable*.

**Layer 1 — Public anchoring (commitments only).**
- **Primary: Bitcoin**, via OpenTimestamps aggregation (public calendars for $0, or a self-run calendar committing the log's Merkle root hourly ≈ $2.1k/yr). Rationale: maximal capture-resistance × maximal 10-year survivability × full-history verifiability × ~zero marginal cost — the stakeholder's cost objection does not survive aggregation (§2).
- **Secondary (optional, per stakeholder preference): Kaspa** — direct per-event or per-minute anchors in tx payloads. Cost is genuinely negligible (<$1/yr at factory volumes), latency is seconds, and it adds an independent PoW witness under different governance. Conditions: run an archival node; capture and retain full inclusion proofs at anchor time; treat Kaspa anchors as corroborating, never sole, evidence (pruning + security-budget caveats, §1.7).
- Receipts stored per-record in a **chain-agnostic multi-anchor format** (digest → Merkle path → {chain, block header, tx ref} list), so anchor targets can be added/dropped without touching the evidence plane. This is the 10-year exit strategy: if Kaspa thrives (DAGKnight lands, fee market forms, archival infra institutionalizes), promote it; if it fades, drop it and lose nothing.

**Layer 2 — Execution/consent logic: NOT on the anchoring chain.**
- Consent, enrollment handshakes, and access policy are *authority* questions — they belong in the factory's governed policy plane (Hermes) and, where multiple external covered entities must share state, a **permissioned consortium ledger** (Hyperledger Fabric / Besu class), whose state roots are themselves anchored via Layer 1. This is also the only posture EDPB/HIPAA guidance cleanly supports (§6).
- If/when a *public* programmable layer is genuinely required (e.g., patient-facing consent verifiability across organizations that share no consortium), use an **Ethereum L2 with EAS** (Base for cost, Arbitrum for less corporate custody) — mature, audited, $0.001–0.05/action. **Do not** put regulated logic on Kasplex/Igra in 2026; re-evaluate both (and Kaspa L1 covenants + the ZK precompile, which are architecturally interesting for exactly this) in 12–24 months once audit history, bridge documentation, and post-Toccata stability exist.

**Medical-records specifics:** per-record salted commitments (HMAC, salt custody in the permissioned layer; erasure = salt destruction); per-exchange anchoring of consent-log checkpoints, not per-patient public rows; the factory's financial-analysis records follow the same pattern minus the PHI constraints.

## 8. Cost model (prices of 2026-08-27: BTC $79k, KAS $0.029, ALGO $0.094, ETH-gas 0.43 gwei; all per-tx figures scale with token price)

**Workload A — factory custody chain:** assume 100 PRs/day × 8 attestations = 800 events/day ≈ 292k/yr.

| Design | Bitcoin | Kaspa | Base L2 (EAS) | Hedera HCS | Algorand |
|---|---|---|---|---|---|
| One tx per event | ~$70k/yr (800×~$0.24) — the prior's "too expensive" is real here | **<$1/yr** | ~$1.5k/yr | ~$234/yr | ~$27/yr |
| Merkle-batched (hourly root) | **$0** (public OTS) / ~$2.1k/yr self-run | <$1/yr | ~$20–50/yr | ~$7/yr | ~$1/yr |

**Workload B — records anchoring at scale:** assume 10M record-events/yr.

| Design | Bitcoin | Kaspa | Base L2 | Hedera HCS | Algorand |
|---|---|---|---|---|---|
| One tx per record | ~$2.4M/yr — prohibitive, correctly | ~$20–30/yr | ~$200–500k/yr | ~$8k/yr | ~$940/yr |
| Merkle-batched | **$0–2.1k/yr flat at any volume** | <$5/yr | ~$50/yr | ~$70/yr | ~$10/yr |

**The structural lesson:** batching collapses *every* chain's cost to noise; therefore cost cannot be the deciding axis, and the stakeholder's fee argument — while numerically correct per-transaction — does not discriminate between candidates once the architecture is right. The deciding axes are capture-resistance, proof longevity, and execution-layer maturity, which is exactly where the recommendation above lands. (Fee sources: §§1.2, 2, 3, 4.)

## 9. What we could not establish (honest gaps)

1. **Exact current Kaspa pool shares** — MiningPoolStats scrape returned internally inconsistent percentages; "top pool ~35%, top-3 ~70%" is our best read, not a precise figure. A manual re-read of the live page is warranted before quoting numbers in a governance doc.
2. **Kasplex/Igra bridge custody details** — no independent public analysis found of who controls the Kasplex bridged-KAS mint or Igra's bridging modules (multisig composition, upgrade keys). The Kasplex audit is publisher-announced; we did not verify its scope. This is the single most important diligence item if any Kaspa L2 use is ever contemplated.
3. **Reliability of late-Aug-2026 usage figures** (1,196 covenant txs/day; 54k Igra txs/day) — sourced from CoinMarketCap's AI digest; order-of-magnitude only.
4. **KAS real liquidity depth** — the $10.6M 24h-volume snapshot may undercount aggregate volume across venues; Coinbase spot listing is reported by a secondary source (Bitget Academy) and should be verified directly before being relied on.
5. **Kaspa archival-node count** — no census exists; we could not quantify how many independent archival operators preserve pre-pruning history.
6. **Post-Toccata stability** — only ~8 weeks of mainnet history; no incident data either way.
7. **Whether Igra's "no centralized sequencer" claim holds under adversarial review** — launch-PR sourced; no third-party audit located.
8. **Long-run Kaspa fee-market formation** — no evidence yet that fees can replace emission; this is the crux of the 10-year survivability question and is currently unanswerable.
9. **Hedera council fee trajectory** — the Jan-2026 8x HCS increase is documented; whether further increases are planned is not public.

## 10. Ranked recommendation

1. **Bitcoin (OTS-aggregated)** — primary anchor. Wins capture-resistance, longevity, verifiability; cost objection dissolved by aggregation.
2. **Ethereum L2 (Base or Arbitrum) + EAS** — execution layer *if and only if* public programmability is required; otherwise the permissioned/Hermes layer carries consent logic. Records inherit ETH L1 neutrality; sequencer capture accepted for logic, never for custody of the evidence plane.
3. **Kaspa** — secondary low-latency anchor, adopted under the three conditions of §7 (own archival node, retained inclusion proofs, corroborating-only status). Re-evaluate for promotion (and for its covenant/ZK L1 primitives) in 12–24 months.
4. **Permissioned consortium ledger (Fabric/Besu class)** — required component of the PHI layer, anchored publicly; not a competitor to the above.
5. **Algorand** — attractive mechanics, fails the capture axis today; watch the relay-node → P2P migration.
6. **Hedera HCS** — best off-the-shelf workload fit; excluded on capture grounds, reinforced by the Jan-2026 unilateral 8x fee action.
7. **Cardano** — commendable governance decentralization; no workload advantage here.
8. **Ergo** — ideologically aligned; security budget too small for regulated records.

---
*Prepared as research input for the openxFactory chain-selection decision. All web sources accessed and date-checked 2026-08-27.*
