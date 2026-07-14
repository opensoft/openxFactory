# Lens Keyword Search and Ad-Hoc Keywords — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Feat request against the realized keyword lens — a search/typeahead over the keyword rail, plus the ability to add an AD-HOC keyword that is not in the declared vocabulary and have it participate in the bullseye; explores what an ad-hoc keyword can honestly match (declared Topics only vs summary text vs a proposed-tag invitation) inside the snapshot-only data path.
Topics: feat-request, ideation-dashboard, keyword-lens, user-management, doc-management, doc-workflow
Repository context: openxFactory (capability owner; realization would be a codexFactory delta)
Captured: 2026-07-14
Origin: Brett, 2026-07-14, using the deployed dashboard at
ideation-dashboard.xforge.us.

Brainstorm — contradiction and half-formed options are legal here.

## The request

The keyword rail shows the declared vocabulary with counts. Two things are
missing when the vocabulary grows past a screenful or the word you are
thinking of is not (yet) a declared topic:

1. **Search the rail** — type to filter keywords, counts intact.
2. **Add a keyword ad-hoc** — type a term that is NOT in the declared
   vocabulary and have it join the checked set like any other keyword.

## Search: the easy half

Typeahead filter over `keyword_index` — pure renderer state, no new data,
no new fetch. Sort modes already sketched in the cluster-combining
brainstorm (by count / by co-occurrence with the current selection /
alphabetic) fold in here. Cheap, unambiguous, no open questions.

## Ad-hoc keywords: what can they honestly match?

The snapshot carries declared `Topics:` per doc and (later) inferred tags —
it does NOT carry document bodies. Options, weakest contract first:

- **A. Match declared topics only (fuzzy/substring).** An ad-hoc term
  matches topics it resembles (`credential` → `credential-contracts`).
  Honest, zero new data, but disappointing — it is search over the rail,
  not a new keyword.
- **B. Match summary text.** The snapshot carries each doc's `Summary:` —
  an ad-hoc keyword could match summaries, rendered visually distinct
  (hollow ring segment? dashed sector?) so a text-match is never confused
  with a declared-topic edge. Modest additive value, no schema change.
- **C. Match full body text.** Requires either body text in the snapshot
  (fattens it hugely — rejected once already for the viewer), a serve-side
  search endpoint (breaks static-only hosting), or a generator-emitted
  token index (additive schema field; real cost). Strongest match,
  heaviest machinery.
- **D. The ad-hoc keyword as a PROPOSED TAG.** Typing a new keyword is a
  vocabulary event: it matches nothing yet, renders as an empty invitation
  ("0 docs — tag some"), and the existing override-evidence loop does the
  rest — including a doc under it emits the Topics-edit scaffold that
  makes the match real on the next snapshot. This turns ad-hoc keywords
  into the human half of the tag-suggestion loop the cataloging change
  and the AI tag suggester feed from the machine side.

Leaning: **B + D together** — summaries give immediate (visibly weaker)
matches; the proposed-tag flow gives the durable path; C waits for a real
need and its own delta.

## Boundary fit

All rendering-side except the Topics-edit scaffolds, which already exist
(human edit via editor launch; agent create-only untouched). Ad-hoc
keywords live in session state / the workbench recipe (`checked` already
accepts any string — the schema does not restrict to declared vocabulary;
verify at realization).

## Possible feats

- Keyword rail typeahead + sort modes (pure renderer).
- Ad-hoc keyword entry joining the checked set, with summary-text matches
  rendered visually distinct from declared-topic edges.
- Proposed-tag flow: empty ad-hoc keyword as an invitation, wired to the
  existing Topics-edit scaffold and recorded as vocabulary evidence for
  the cataloging registry.
- (deferred) Generator token index for body-text matching as an additive
  snapshot field.

## Exit

Clusters with the other lens feat requests; picked possibles go to one
staged `lens-enhancements` topic and realize as a MODIFIED
`ideation-dashboard` OpenSpec delta with a codexFactory feature.
