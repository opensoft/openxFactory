# credential-contracts Delta: SOPS Ciphertext Ruling

## ADDED Requirements

### Requirement: SOPS ciphertext repository pattern
A SOPS document with AES-256-GCM-encrypted credential leaves SHALL NOT be classified as a raw credential, and SOPS plus an
externally custodied decryption identity SHALL be an approved
secret-provider pattern, only while every one of the following controls
holds: the repository stores only ciphertext, non-secret object metadata,
SOPS integrity metadata and MAC, and public recipients; the private
decryption identity lives durably only in an approved secret provider and
is projected separately into the runtime decryption controller; recipients
are unique per environment or stronger trust boundary; repository policy
rejects plaintext secret values and private decryption identities before
commit; a compromise of the decryption controller is treated as a
compromise of every secret that controller can decrypt; and an exposed
decryption identity triggers rotation of both the identity and every
credential encrypted to it, because historical git ciphertext remains
recoverable with the exposed identity. Base64 encoding, ad hoc encryption
without SOPS integrity metadata, a private decryption identity present in
any repository, and any value decryptable without the approved external
identity remain raw credentials and stay prohibited.

#### Scenario: A compliant SOPS-encrypted secret is committed
- **WHEN** a repository commits a secret manifest whose secret-bearing leaves are SOPS AES-256-GCM ciphertext, only public recipients are committed, and the private identity is custodied in an approved secret provider
- **THEN** the commit does not violate the no-raw-credentials core rule

#### Scenario: A plaintext or trivially encoded secret is committed
- **WHEN** a commit introduces a secret value in plaintext or bare base64, or introduces a private decryption identity
- **THEN** repository policy MUST reject it as a raw credential

#### Scenario: A decryption identity is exposed
- **WHEN** a private decryption identity is exposed outside its approved custody
- **THEN** the identity MUST be rotated
- **AND** every credential encrypted to it MUST be rotated, because historical ciphertext in git remains recoverable

#### Scenario: A recipient is reused across environments
- **WHEN** a deployment proposes encrypting one environment's secrets to another environment's recipient
- **THEN** the binding MUST be rejected; recipients are per-environment or per stronger trust boundary
