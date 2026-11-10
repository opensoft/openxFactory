# Private connectivity binding

Status: draft

This is the approved feature-local pilot candidate. It is outside the published contract bundle. A later serialized bundle realization promotes these bytes into `contracts/private-connectivity/`, registers their digests, updates the changelog and release inventory atomically, and re-pins consumers before customer release.

This pilot candidate implements the reference-only binding shape authorized by [implement-private-connectivity-binding](../../../../openspec/changes/implement-private-connectivity-binding/proposal.md).

A runtime adapter supplies the installation context under `installation` and an optional `private_connectivity` record. Existing manifests without that record remain compatible. The binding identifies the customer, environment, operator, endpoint, network, state, approved access, and separately approved routes. Enrolled and ready declarations require matching enrollment authority. Ready declarations also require observed policy scope and verification references.

Run `python3 scripts/validate-private-connectivity.py <manifest.json>`. Add `--now <UTC timestamp>` for deterministic fixture checks. The validator reports conformance codes and omits input values from errors. Provider connectivity and genuine evidence are verified separately in the authorized owner and pilot gates.

The state vocabulary is requested, approved, enrolled, ready, unready, and revoked. Keep credentials in custody and use the credential reference on enrollment. Publish the exact candidate revision and conformance output before consumers use it. The additive bundle release follows the [contract versioning policy](../../../../docs/contract-versioning-policy.md).

Connectivity and separate route approvals bind the exact HTTPS endpoint as well as the network and installation boundary. Reusing an approval for a different syntactically valid endpoint is rejected.

The validator CLI resolves the manifest against its current working directory and rejects paths outside that directory and symlink inputs. Run the CLI from the directory containing the intended manifest, passing the validator script by path when needed. The in-process conformance function performs no manifest file access.
