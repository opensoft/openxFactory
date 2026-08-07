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
- [ ] 4.4 Brett's first real drill-in session.
