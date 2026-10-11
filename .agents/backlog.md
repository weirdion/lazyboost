# Backlog

Scoped but not being built. Each entry: what, why it's deferred, and what would pull it forward.
Delete an entry when it ships or is dropped; the commit and session log are its record.

## No automated tests
`tests/` is empty, and `make test` fails because `pytest-cov` isn't a dependency. Verification is the
offline procedure in context.md. The useful first tests: model parsing of recorded Etsy and Shopify
payloads, and customer name and address matching, which is where every past hotfix landed.
*Deferred:* maintenance mode; the smoke checks cover dependency updates.
*Pull forward:* any change to matching or order-mapping logic.

## Branch cleanup after the lazyboost-app discovery spike
`develop` (2 unmerged commits) and `feat/rework-cleanup` (1 unmerged commit) hold an earlier OAuth
rework attempt, locally and on GitHub. The rework now happens in `lazyboost-app` (decisions.md,
2026-10-11).
*Deferred:* the operator wants them as reference during the discovery spike.
*Pull forward:* the spike is done. **Then delete both, locally and on GitHub.**

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
