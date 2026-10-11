# Backlog

Scoped but not being built. Each entry: what, why it's deferred, and what would pull it forward.
Delete an entry when it ships or is dropped; the commit and session log are its record.

## No automated tests
`tests/` is empty, and `make test` fails because `pytest-cov` isn't a dependency. Verification is the
offline procedure in context.md. The useful first tests: model parsing of recorded Etsy and Shopify
payloads, and customer name and address matching, which is where every past hotfix landed.
*Deferred:* maintenance mode; the smoke checks cover dependency updates.
*Pull forward:* any change to matching or order-mapping logic.

## Etsy OAuth handshake rework
Unfinished work lives in three places: `develop` (2 unmerged commits), `feat/rework-cleanup`
(1 unmerged commit), and archived stashes under `refs/archive/stash/2025-05-21-idx2` and
`2025-06-08-idx1` (an `etsy-oauth-stack.ts` rework). A FastAPI stub that was likely meant for this
(previously untracked `app/`) is archived in `refs/archive/worktree-2026-10-11`. The archive refs
are local only.
*Deferred:* the current handshake works.
*Pull forward:* Etsy changes its OAuth requirements, or token refresh starts failing.

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
