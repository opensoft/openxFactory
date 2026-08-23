## 1. Governance and upstream capture

- [x] 1.1 Record the current reachable openPractice revision and repository URL.
- [x] 1.2 Create the MedxPractice composition files, pin manifest, and portable
  agent context.

## 2. Repository and aggregate migration

- [x] 2.1 Move the standalone openPractice checkout to the shared projects
  area without rewriting its history.
- [x] 2.2 Publish MedxPractice as a private `opensoft` repository with the
  nested openPractice gitlink.
- [x] 2.3 Add MedxPractice to xFactory and remove any direct public
  openPractice aggregate entry without staging unrelated workspace changes.
- [x] 2.4 Update xFactory orientation and project-register documentation.

## 3. MedxFactory integration

- [x] 3.1 Update MedxFactory orientation/composition documentation to use
  MedxPractice as the branded practice-operations boundary.
- [x] 3.2 Update the xFactory MedxFactory submodule pointer after the child
  repository change is committed and pushed.

## 4. Verification

- [x] 4.1 Validate the OpenSpec change and verify the nested gitlink/manifest
  revision agreement.
- [ ] 4.2 Verify remote reachability, recursive submodule status, and clean
  status for the newly changed repositories.
