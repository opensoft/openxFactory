# Tasks: add-authored-body-on-create

## 0. Ratification

- [ ] 0.1 Brett accepts the shape: the BODY rides the create, rather than
      widening `edit-document` to a scope-free first save. The alternative is
      recorded in the proposal.

## 1. The verb

- [ ] 1.1 `authoring.create_scaffold` accepts an optional `body` and writes it
      below the generated header.
- [ ] 1.2 `_create_body` parses it; `execute_create_document` passes it
      through. Absent = today's behaviour, byte for byte.
- [ ] 1.3 A body cannot restate a header field: the generated header wins.

## 2. The draft view

- [ ] 2.1 doxBench's draft view makes the body EDITABLE again and sends it
      with the create — currently read-only, and honestly so, because there
      was nowhere for typed text to land.

## 3. Verification

- [ ] 3.1 Wire test: a create with a body lands header + body in ONE commit.
- [ ] 3.2 The no-body create is unchanged.
- [ ] 3.3 CLI parity.
