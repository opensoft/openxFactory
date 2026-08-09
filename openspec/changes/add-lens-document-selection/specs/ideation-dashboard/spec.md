# ideation-dashboard

## ADDED Requirements

### Requirement: Every view of a document is one hover away from the others
The lens SHALL join its views of a document so that pointing at any one of them identifies the same document in all of them. The radar's dot, the matrix's row and the signature grid's row SHALL each publish the document's identity, and the lens SHALL highlight every view carrying that identity while the pointer rests on any of them, because three renderings that number a document identically still leave the reader performing the join by eye.

The join SHALL be made once, by the pane, rather than by each renderer subscribing to the others: a renderer publishes a key and knows nothing of the other views, so a redraw cannot leave a stale binding behind and no widget carries cross-view state.

#### Scenario: Pointing at a row lights its dot
- WHEN the pointer rests on a matrix row
- THEN that document's dot on the radar and its row in the signature grid are highlighted
- AND the highlight is removed when the pointer leaves

#### Scenario: The join survives a redraw
- WHEN the checked terms change and the lens redraws
- THEN pointing at a row still lights the corresponding dot

### Requirement: A document selection drafts a staging-queue seed
The lens matrix SHALL let a human select documents and SHALL draft a staging-queue fragment covering exactly the selected set, because the question a reader of the keyword radar has — these documents keep meeting, what is the topic? — exits into `ideation/staging/`, and until now that exit was hand work performed from a screen of numbers.

The draft SHALL be a SCAFFOLD. What is computable SHALL be computed: the documents, their repositories, the terms every selected document carries, the terms only some carry, and a staging identifier whose folder name does not collide with a topic already in the queue. What is not computable SHALL be left as explicitly marked prompts — the summary, why the topic is staged now, the claims, the open questions and the exit path — because a drafter that argued its own case would be the machine deciding what is worth staging.

The drafting SHALL write nothing: the response is TEXT and the path it belongs at, and the fragment enters the queue only when a human places and completes it. The evidence SHALL be recomputed by the serving side from its own snapshot — the client names the documents and never their terms — and a selected document the snapshot does not carry SHALL be refused by name rather than silently dropped, because a seed missing a selected document misstates the convergence it claims.

#### Scenario: A selection drafts a fragment
- WHEN a human selects two or more documents in the matrix and drafts a seed
- THEN the response is a staging fragment naming each document, its repository and its terms, plus the terms all of them share
- AND every section requiring human judgment is marked as unwritten
- AND nothing in the checkout is created or modified

#### Scenario: The client cannot supply the evidence
- WHEN the request names documents
- THEN their terms and repositories are read from the serving side's own snapshot

#### Scenario: An unknown document is refused by name
- WHEN a selected document is absent from that snapshot
- THEN the request is refused and the response names the missing document

#### Scenario: A selection with no shared term says so
- WHEN the selected documents share no declared term
- THEN the draft states that the connection is a human judgment rather than naming a term none of them carry

### Requirement: A finding is stated before it is drawn
A view whose picture supports a single finding SHALL state that finding in text rather than requiring the picture to be read, because a finding that fits in a sentence does not warrant the most valuable space on the screen to render.

Where the surface's own purpose leaves no room for the picture at all, the derivation SHALL remain available to the surface that wants it rather than being deleted with the view. The keyword lens is such a surface: it became a DRAFTING pane — radar, drafted seed, document list — where even a collapsed summary row costs the document list (Brett, 2026-08-08: "we do not need this in this view… add the room to make the viewport to the doc list larger"), so the signature grid left it and `signatureSummary` stayed in the model, tested.

#### Scenario: A finding is available without its picture
- WHEN a repeated-signature finding is computed
- THEN it is expressed as counts a caller can state in one line

#### Scenario: No repetition is reported as such
- WHEN every document carries a different combination of the checked terms
- THEN the summary says so rather than reporting an empty group

### Requirement: A panel in contested space carries one row of chrome
A panel occupying a pane's scarce vertical space SHALL confine its chrome to a single row — its title, its action and its dismissal — and SHALL give every other pixel to its content. Explanatory text that is read once and re-read rarely SHALL be attached to that row as a hover rather than held permanently on screen, because a permanent note costs the content viewport beneath it on every appearance.

Such a panel SHALL NOT scroll: its CONTENT scrolls within it. Two nested scrollers put a panel's own chrome out of reach of the very scroll that is trying to read its text.

An action bar SHALL position its controls by role — an undo beneath the control it undoes, the bar's primary action at its true centre — and a control whose label states a count SHALL carry that count rather than repeating it in a separate sentence. Centring SHALL survive a label that changes length.

#### Scenario: The panel's chrome is one row
- WHEN a drafted seed is shown
- THEN its title, its action and its dismissal share one row, and the placement instructions are that row's hover

#### Scenario: The content scrolls, not the panel
- WHEN the drafted text is longer than the panel
- THEN the text scrolls within the panel and the panel itself does not

#### Scenario: An action reads what it will do
- WHEN a draft is already on screen
- THEN the action reads as a REPLACEMENT of it rather than implying a second, separate draft

### Requirement: The theme owns every colour a view chooses
View code SHALL choose only a HUE and the stylesheet SHALL resolve it into a colour, because a lightness that reads on a light ground disappears on a dark one and the choice belongs where the theme is known. Saturation, lightness and opacity SHALL be defined per theme as custom properties, and no view SHALL write a complete colour.

Every custom property the stylesheet reads SHALL be one the stylesheet defines. An undefined custom property does not fail — it silently becomes its fallback — so a token that never existed can paint a control's ground in a colour the theme never chose. Any rule that removes a control's default background SHALL also state its colour, because a `<button>` does not inherit colour and takes the user agent's instead.

#### Scenario: A tint adapts to the theme
- WHEN a term's hue is rendered on the dark theme
- THEN its lightness comes from the dark theme's own token, not from the view

#### Scenario: An undefined token cannot ship
- WHEN the stylesheet reads a custom property it does not define
- THEN the check fails
