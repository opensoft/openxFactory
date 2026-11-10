# Transient Validation Data

Status: draft

Input: PR body as an opaque string. Derived values: CRLF-normalized lines, first nonempty line and declaration count. Output: success for absence or a unique valid first declaration; failure otherwise. No persisted identity, enrollment, claim, secret or state transition is added.
