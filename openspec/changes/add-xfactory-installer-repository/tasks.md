## 1. Proposal And Provenance

- [x] 1.1 Record explicit ad hoc proposal provenance and validate supporting-document hashes.
- [x] 1.2 Run strict OpenSpec validation before repository creation.

## 2. Private Repository Bootstrap

- [x] 2.1 Create `opensoft/xFactory-Installer` with private GitHub visibility and verify the remote owner and default branch.
- [x] 2.2 Add truthful repository, architecture, security, compatibility, release, ownership, and validation surfaces without placeholder application claims.
- [x] 2.3 Run repository validation and prohibited credential/package scanning against the bootstrap tree.

## 3. Initial Release

- [x] 3.1 Commit the validated repository bootstrap on `main` and push it to the private remote.
- [x] 3.2 Tag and push immutable bootstrap release `v0.1.0-bootstrap` and verify that the tag resolves to the validated commit.

## 4. Aggregation Integration

- [x] 4.1 Add the SSH submodule at `installs/xfactory-installer` and update the xFactory topology and current-submodule documentation.
- [x] 4.2 Verify private visibility, remote URL, exact gitlink, compatibility declaration, repository validation, and recursive checkout behavior.
- [x] 4.3 Commit and push only the installer proposal, new installer pin, and parent integration paths without including unrelated dirty work.

## 5. Completion

- [x] 5.1 Run repository validation, strict OpenSpec validation, parent diff checks, and final status verification.
- [x] 5.2 Record that WinUI implementation, Intune enrollment, Graph grants, signing, and Store submission remain successor work rather than bootstrap realization claims.
