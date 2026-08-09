# Tasks: add-repository-lens

## 1. The vocabulary

- [x] 1.1 `repositoryVocabulary(snapshot)`: composed snapshot -> the lens's
      own shape (rail = members with identity counts, one row per identity
      carrying its repositories and its real per-repository `copies`),
      deterministic order, null off a composed snapshot.
- [x] 1.2 The lens engine is UNCHANGED — the projection is the whole adapter.

## 2. The widget

- [x] 2.1 Vocabulary switch in the Lens tab head, offered only on a composed
      view; the keyword lens's behaviour and appearance untouched.
- [x] 2.2 Rail, bullseye header and notes speak the active vocabulary.
- [x] 2.3 The repository rail opens on the visible set and writes ticks
      through to it (no reload — the lens holds the whole aggregate).
- [x] 2.4 The drill-in pane: one labelled row per region, innermost first,
      the discoverable twin of the bullseye's hit regions.
- [x] 2.5 Brett's 2026-08-07 annotation ("I do not understand how to use this
      section. The words are jumbled together and do not make clear intuitive
      UI"): each row states what its SET IS in repository names ("in all 2
      visible repositories", "only in AdxFactory") on its own line, with the
      count and the actions beneath it; the pane opens with a sentence saying
      what its rows are; and a single-carrier row omits the seed control
      rather than showing a disabled one.

## 3. The drill-in

- [x] 3.1 `identitiesFor(vocabulary, checked, region)` — the centre is
      every checked repository; a sector is that combination exactly.
- [x] 3.2 `scopedSnapshot(snapshot, identities)` — a document set, with
      every other plane keeping only what references it.
- [x] 3.3 App shell: stored scope applied after the visible-set narrowing
      and before the cluster union; a banner stating documents, identities
      and combination, with a clear control.

## 4. Verification

- [x] 4.1 Node tests: the projection (rail counts, identities, carriers,
      copies), rings as carrier counts through the REAL lens engine, centre
      and sector targets, the narrowed-checked-set case, and the non-composed
      null.
- [x] 4.2 Node tests: scoping keeps referencing planes only, leaves
      unrelated planes alone, and passes a null scope through untouched.
- [x] 4.3 Live browser check on the real multi-repository plane.
      (Verified 2026-08-07 against the 14-repository plane, project
      `domains`: the Lens tab offered `keywords | repositories`; the
      repository lens drew the 5-member rail with identity counts
      (Adx 7, Ledgerx 90, Medx 81, Ops 22, codex 30), 219 identities on
      rings 5..1 — 215 single-carrier, 1 in two, 1 in three, 2 in all five
      — and sectors naming the real combinations, including
      `docs/credentialing.md` under Ledgerx ∧ Ops ∧ codex. Unticking a
      repository in the rail redrew to 4 repositories / 214 identities with
      NO reload and wrote the visible set through, after which the filter
      label read "⧩ 4 of 5 Repos". Drilling into the centre scoped the shell
      to 8 documents / 2 identities with the banner naming the region, the
      doc list showing exactly those, and `clear` restoring the full view.
      Zero console errors, page errors, and >=400 responses.)
- [x] 4.4 Brett's first real drill-in session.
      (Ruled satisfied by Brett 2026-08-09, on the Playwright acceptance
      session he commissioned against the live 13-repository local plane,
      project `domains`, 4 published members: the vocabulary switch offered
      `301 Keywords | 4 Repositories`; the repository rail stated each
      member's split (Ledgerx 92, Medx 85, codex 28, Adx 7, each "N shared ·
      M only here"); 205 identities drew on rings ALL 4/3/2/1 with sectors
      naming real combinations (A ∧ C); the drill-in rows carried the seed
      control only where a seed can mean anything (omitted, not disabled, on
      single-carrier rows). Drilling the centre scoped the shell to
      8 documents — "2 identities carried by all 4 visible repositories" in
      the banner — with the doc list showing exactly those copies, and
      `clear` restoring 212 documents. Zero console errors, page errors, and
      >=400 responses. Play-by-play report: "doxBench acceptance run",
      2026-08-09.)
