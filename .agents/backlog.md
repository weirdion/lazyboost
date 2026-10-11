# Backlog

Scoped but not being built. Each entry: what, why it's deferred, and what would pull it forward.
Delete an entry when it ships or is dropped; the commit and session log are its record.

## No automated tests
`tests/` is empty, and `make test` fails because `pytest-cov` isn't a dependency. Verification is the
offline procedure in context.md. The useful first tests: model parsing of recorded Etsy and Shopify
payloads, and customer name and address matching, which is where every past hotfix landed.
*Deferred:* maintenance mode; the smoke checks cover dependency updates.
*Pull forward:* any change to matching or order-mapping logic.

## Etsy OAuth / larger rework
The operator plans a bigger rework, starting with a discovery spike. Earlier attempts remain on
`develop` (2 unmerged commits) and `feat/rework-cleanup` (1 unmerged commit), local and on GitHub.
Earlier stashed attempts and a FastAPI stub (`app/`) were deleted on 2026-10-11 at the operator's request.
*Deferred:* the current handshake works (token refresh confirmed in production on 2026-10-11).
*Pull forward:* the discovery spike starts. **When it's done, delete `develop` and
`feat/rework-cleanup`, locally and on GitHub.**

## README is stale
It describes a Docker Lambda and Facebook shop sync, and has no deploy or verify instructions.
*Deferred:* agent-facing docs live in `.agents/`; human docs are lower priority.
*Pull forward:* when issues are migrated (several are documentation requests).

## Workflow upkeep
`update.yml` pins Node `lts/Hydrogen` (EOL) while the other workflows use `lts/Krypton`. Actions
are on older major versions. CI installs the CDK CLI globally and unpinned instead of using the
repo's devDependency.
*Deferred:* everything still runs.
*Pull forward:* a workflow breaks, or GitHub deprecates a pinned action version.
