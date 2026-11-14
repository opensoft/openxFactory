# Source commissioning authentication

Status: draft

Brett Heap is the accepted source-evidence custodian. Actual authentication is
pending review of the immutable commissioning container and the separate T010
receipt. Ratifying E, its bootstrap amendment and N did not authenticate unseen
outputs. This record grants no deployment, spend, enrollment, release or Q0–Q5
acceptance, and all three PRs remain draft.

The prepared container preserves the original T001–T005 commands and source
observations, actual T006 owner/custody decisions, exact committed T007–T009
regression outputs, original human-message timestamps and individual raw-record
digests. The failed development regression remains visible. Source/governance
artifacts retain their real Git references. No T001.json–T009.json is created.

Before acceptance, review the actual command, source, exit, timing, original
stdout, original/export digests and stated redaction method for each import.
Confirm the source-only scope and original human provenance; successful source
tests and synthetic fixtures supply no provider/customer/live qualification.
T010 additionally requires the actual successful exact-head required GitHub
run/job and explicit zero-skip collection of both feature suites.

The final decision must name the reviewed immutable manifest and its canonical
content SHA-256. That core excludes only the review pointer and derived pin
inventory, so authentication and the final control manifest can occupy distinct
commits without a self-containing hash. A payload/binding/authority change needs
new review. Until the actual decision exists, the verifier refuses admission.

```json
{
  "schema": "043-source-authentication-v1",
  "decision": "pending",
  "custodian": "Brett Heap",
  "reviewed_manifest": null,
  "content_sha256": null,
  "reviewed_at": null
}
```
