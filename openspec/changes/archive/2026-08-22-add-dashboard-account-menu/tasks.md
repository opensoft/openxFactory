# Tasks: add-dashboard-account-menu

## 1. The serve surfaces the hosted actor

- [x] 1.1 `/capabilities` reports `hosted_actor`, resolved PER REQUEST from the
      `X-Auth-Request-User` header beside the existing per-request `repository`
      field, and `null` when the header is absent. Additive to the unversioned
      shape — no version bump, matching the prior `model` and `repository`
      fields.
- [x] 1.2 The field is DISPLAY-ONLY: it feeds no capability verdict and no
      route consults it to authorize. Add the D16 boundary comment where the
      field is set, so no reader over-reads a stamped header as a credential.

## 2. The account-menu view

- [x] 2.1 New `web/views/account-menu.js` following the settings.js header-
      popover pattern: an aside appended to `<body>`, anchored under its
      button, Escape and outside-click close, keyboard-focusable, every dynamic
      value bound via `textContent` (never `innerHTML`).
- [x] 2.2 The menu renders the signed-in username from `hosted_actor`, the
      derived access level (read from `/capabilities.actions` + loopback state —
      read-only when no write/gate/edit action, otherwise naming the granted
      capabilities), and a logout control.
- [x] 2.3 Graceful local mode: with `hosted_actor` absent, show the local actor
      if the serve resolved one, or a generic "local session" label, and render
      NO logout control.
- [x] 2.4 Logout navigates the browser to the gateway-owned `/logout`; the view
      terminates no session itself.

## 3. index.html wiring

- [x] 3.1 Add a user-account button to the `.cornerbtns` span beside the theme
      and settings buttons, with `aria-expanded` / `aria-controls` matching the
      settings button's accessibility shape, and wire it to the account-menu
      view.

## 4. Tests

- [x] 4.1 A serve.py test for the `hosted_actor` field: present → the stamped
      username; absent → `null`; and a hosted request with a stamped actor
      still yields no write/gate/edit capability.
- [x] 4.2 A node/DOM test for the account menu following the settings.js test
      pattern: open/close on button, Escape, and outside click; keyboard focus;
      username + access level render; local mode hides logout; logout targets
      `/logout`.

## 5. Docs

- [x] 5.1 Add the active change to the openxFactory README "OpenSpec Records"
      block, matching the existing line format. (Landed with the spec PR #246.)

## 6. Verification

- [x] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-dashboard-account-menu
      --strict` and `--all --strict` both green.
- [ ] 6.2 Full dashboard suites green; live proof of the menu in hosted and
      local modes (username + access level shown; logout leaves for `/logout`
      hosted, absent local). Full dashboard suites GREEN (3836 passed, 13
      skipped, 2026-08-21). Live
      browser proof is DEFERRED to post-deploy — the menu only renders a hosted
      `hosted_actor` behind the dox-auth gateway, so it is verified once the
      rebuilt dashboard image is rolled (same pattern as the login-form flow).

## Bookkeeping note — ratification flip CONSIDERED AND DECLINED (2026-08-22, `archive-record-discrepancies`), THEN RULED AND APPLIED (2026-08-22, `archive-register-rulings`)

> **Superseded later the same day — read "Bookkeeping resolution" below before
> acting on anything in this section.** This forward pointer and the heading's
> second clause are the only additions above the resolution; not one word of the
> note that follows has been altered, so it still says what was true when the
> `archive-record-discrepancies` sweep closed. Its opening sentence — "Nothing
> in this change's record is edited" — was true then and is false now, and that
> is exactly what the append discipline preserves rather than tidies away.

Nothing in this change's record is edited. The `Status:` header still reads
`draft`, the value it has carried from proposal through archive. This note
records that flipping it to `ratified` was considered in the
`archive-record-discrepancies` sweep, drafted, and then withdrawn on review —
so that the next reader who spots the same anomaly finds the reasoning instead
of re-opening it.

The anomaly is real. The ratification flip that `document-lifecycle` requires
in the same change as the transition was never made, and the transition itself
is implied by this change's own record three times over: the realization commit
`c09fe68` opens "Realizes the ratified add-dashboard-account-menu change"; the
archive commit `afd7b33` archived it under `release-realization`'s gate, which
admits only a ratified change; and the archival promoted this change's four
requirements into `openspec/specs/ideation-dashboard/spec.md`, which is an act
a proposal that was never ratified cannot reach.

Why the flip was declined anyway. `docs/document-lifecycle.md` § Status Claim
Rules does not merely permit a `ratified` header — it requires that header to
name its ratification ("A `ratified` header names the approving OpenSpec
change"). Every one of the thirty-eight archived proposals that read
`Status: ratified` carries such a citation, in one of two spellings
(`Ratified by:` on twenty-nine, `Ratified:` on nine), and each names an
approver, a date, or a resolvable record. This change's record supplies none of
the three. `c09fe68` says the change *was* ratified; it does not say by whom or
on what date, and neither does `afd7b33`, the README row, or any file in this
directory — there is no `.openspec.yaml` here at all. Writing a bare
`Status: ratified` with no citation would assert a provenance the record cannot
back, and writing a citation would mean inventing a ratifier or a date. That is
exactly the hazard this change's sibling entry in the register (C3) refuses
when it declines to write `approved_by`/`approved_on` into a missing origin
declaration from inference. The same refusal has to apply to the same two
facts on the lifecycle axis.

Held for a Brett ruling, and it is a cheap one: naming the ratifier and the
ratification date for `add-dashboard-account-menu` closes this note and C3's
account-menu half at the same time, since both are blocked on that single pair
of facts. Recorded as its own entry in
`docs/archive-record-discrepancies.md` (C7), alongside C3.

Note for a reader who checks the tooling: no gate is involved either way. The
doc-health `record-immutability` family reads only documents whose own header
says `Status: record`, drawn from the governed roots `contracts/`, `docs/`,
`examples/`, `ideation/`, `templates/` — `openspec/` is not among them, so no
file in this directory is in that family's reach. Nothing mechanical would have
stopped the flip; the lifecycle rule is what stops it.

## Bookkeeping resolution — the ruling arrived (2026-08-22, `archive-register-rulings`)

**RULED 2026-08-22 by Brett Heap, in-session** (a multiple-choice round over
the whole `docs/archive-record-discrepancies.md` register; the recommended
option was adopted on every item). The annotation is added at Brett's
instruction, and the declined note above is left as written — this is an
APPEND, in the shape of Brett's own 2026-08-10 ruling as recorded at
`2026-08-13-align-doxbench-contract-pin-to-publisher` task 6.2, where the
original open-item sentence was "left standing word for word and the resolution
follows it, so the record still says what was true when the tranche closed."
The forward pointer and the heading's second clause added above that note are
a second extension of the same ruling, not an instance of it: the precedent as
recorded appends strictly below the original sentence and never touches
anything above it, while this addition sits above the preserved text —
extending the discipline rather than instancing it, and named as such here
too.

**The one fact that was missing, and where it came from.** The note above is
blocked on exactly one pair of facts — who ratified this change and when — and
it is precise about why no file could supply them. Brett supplied them himself:
he ratified `add-dashboard-account-menu` in-session on **2026-08-21**, its
authoring date. That is a DECLARATION, not a discovery. Nothing in this
change's directory, in `c09fe68`, in `afd7b33`, or in the README row carried it
before, and nothing has been found since; re-reading the record will still turn
up no contemporaneous trace. What changed is not the evidence but the
authority: the ratifier stated the fact, which is the one source the note above
said it was waiting for ("Held for a Brett ruling, and it is a cheap one").

**What was executed, all three of them.**

1. `proposal.md`'s `Status: draft` became `Status: ratified`. The original
   value is preserved verbatim in prose — it "read `draft` from proposal
   through archive" — on the new `Ratified:` line, in this note, and in the
   register, because an append on a single-valued header is mechanically
   impossible (`doc_health.corpus.STATUS_RE` is `^Status:\s*(.+?)\s*$`, which
   swallows any trailing annotation into the value). Like B1 before it, this is
   an in-place overwrite and an **extension** of the 2026-08-10 ruling, not an
   instance of it, and is named as one.
2. A `Ratified:` citation line was added beside it, satisfying
   `docs/document-lifecycle.md` § Status Claim Rules. The spelling is the
   record-citing `Ratified:` form rather than `Ratified by: <change>`, for the
   reason the note above already established and this ruling did not change:
   no approving OpenSpec change exists to name, and no contemporaneous
   quotation was written down. The record it cites is the 2026-08-22 ruling
   round captured in `docs/archive-record-discrepancies.md`. It deliberately
   does NOT cite this change's new `.openspec.yaml`, the way B1 cites its own:
   B1's origin file predated the correction and was independent evidence,
   whereas this one was written in the same act from the same declaration, so
   citing it would be circular.
3. A `.openspec.yaml` was written, closing C3's account-menu half — an
   `ad_hoc` origin, since no staging topic exists behind this change and the
   `proposal-origin` family requires a non-empty `reason`, `approved_by`, and
   `approved_on` for that kind. Its `reason` states in full that the file was
   written on 2026-08-22 rather than at the transition, and that the approval
   pair is Brett's declaration rather than a contemporaneous record, so no
   later reader mistakes a backfilled origin for an original one.

**What this does NOT do.** It ticks no box: 6.2's live browser proof is still
deferred and still open, on its own recorded reasoning. It touches no
requirement text, no spec delta, and no promoted spec, so `efa42cf`'s rule —
that an archived change must not be amended into disagreement with the spec its
own archival promoted — is untouched here as it was for B1. And it says nothing
about `add-worker-credential-by-reference`, C3's other half: Brett supplied no
ratification fact for that change, so it stays exactly as it was, and the
register records that this round closed only one of the two.

**On the tooling paragraph above: still true, and now load-bearing in the other
direction.** `record-immutability` still does not reach any file under
`openspec/`, so nothing in this directory tripped a gate. The register itself
is a different matter — it is `Status: record` under `docs/`, squarely in the
family's reach, and recording this ruling in it trips the critical by design.
That cost was accepted when the register was written, and how it was measured
and dispositioned is recorded there, not here.
