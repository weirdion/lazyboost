# Backlog

Scoped but not being built. Each entry: what, why it's deferred, and what would pull it forward.
Delete an entry when it ships or is dropped; the commit and session log are its record.

## No automated tests
`tests/` is empty, and `make test` fails because `pytest-cov` isn't a dependency. Verification is the
offline procedure in context.md. The useful first tests: model parsing of recorded Etsy and Shopify
payloads, and customer name and address matching, which is where every past hotfix landed.
*Deferred:* maintenance mode; the smoke checks cover dependency updates.
*Pull forward:* any change to matching or order-mapping logic.

## Human-facing setup docs
The README is stale: it describes a Docker Lambda and Facebook shop sync. Missing for a human
operator (from closed issues #118, #121, #122):
- the Etsy OAuth handshake (the two Node Lambdas, API Gateway `/api/redirect`, where tokens land in
  Secrets Manager);
- Shopify credentials and required permissions;
- deploy order and variables. Variables are partly covered by `.env.sample` and context.md.
*Deferred:* KTLO, the successor replaces this, and agent-facing docs live in `.agents/`.
*Pull forward:* someone other than the operator has to deploy or recover it.

## Workflow upkeep
`update.yml` pins Node `lts/Hydrogen` (EOL) while the other workflows use `lts/Krypton`. Actions
are on older major versions. CI installs the CDK CLI globally and unpinned instead of using the
repo's devDependency.
Also (closed issues #71, #72): replace the third-party create-pull-request action with
`actions/github-script`, and tag merge deploys so a deploy can be repeated.
*Deferred:* everything still runs.
*Pull forward:* a workflow breaks, or GitHub deprecates a pinned action version.
