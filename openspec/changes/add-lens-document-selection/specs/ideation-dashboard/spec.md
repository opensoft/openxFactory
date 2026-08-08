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
A view whose picture supports a single finding SHALL state that finding in text and SHALL make the picture available rather than permanent, because a finding that fits in a sentence does not warrant the most valuable space on the screen to render.

The signature grid SHALL summarise how many documents share a signature with another, how many such groups exist and the largest of them, and SHALL open on request. Its summary SHALL say what the finding MEANS — documents with the same signature carry exactly the same checked terms, which is the closest thing to a duplicate the lens can see.

#### Scenario: The grid states its finding while closed
- WHEN documents are on the radar and terms are checked
- THEN the grid's summary reports the repeated signatures and their largest group without the grid being open

#### Scenario: No repetition is reported as such
- WHEN every document carries a different combination of the checked terms
- THEN the summary says so rather than reporting an empty group

### Requirement: The theme owns every colour a view chooses
View code SHALL choose only a HUE and the stylesheet SHALL resolve it into a colour, because a lightness that reads on a light ground disappears on a dark one and the choice belongs where the theme is known. Saturation, lightness and opacity SHALL be defined per theme as custom properties, and no view SHALL write a complete colour.

Every custom property the stylesheet reads SHALL be one the stylesheet defines. An undefined custom property does not fail — it silently becomes its fallback — so a token that never existed can paint a control's ground in a colour the theme never chose. Any rule that removes a control's default background SHALL also state its colour, because a `<button>` does not inherit colour and takes the user agent's instead.

#### Scenario: A tint adapts to the theme
- WHEN a term's hue is rendered on the dark theme
- THEN its lightness comes from the dark theme's own token, not from the view

#### Scenario: An undefined token cannot ship
- WHEN the stylesheet reads a custom property it does not define
- THEN the check fails
