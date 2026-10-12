# LazyBoost — agent boot

## Read first

0. **STEER** — read `agent-steer/INDEX.md` (the operator's steer repo, checked out alongside this one),
   load the spine, pull ways-of-working / preferences on relevance. The files below state only what
   is local to this project or overrides the steer.
1. [context.md](context.md) — what LazyBoost is, how it's built, deployed, and verified.
2. [decisions.md](decisions.md) — settled choices; don't re-debate without new information.
3. [backlog.md](backlog.md) — deferred work. Read before scoping anything new.
4. [session-log.md](session-log.md) — top entry is the current state, next step, and anything
   awaiting operator verification.

## Local rules

LOCAL: This is a live production service in KTLO mode: fixes and patches only, and new features go to
`lazyboost-app` (decisions.md). **Every push to `main` deploys**
(`.github/workflows/deploy.yml` runs `cdk deploy --all`). Work on a branch and open a PR; the PR
preview job runs `cdk diff`. Merging is the deploy decision and belongs to the operator.
— A merge is not a code-review formality here; it changes what runs against real orders.

LOCAL: CDK bundles `src/` and the Lambda directories straight from the working tree. Never deploy
from a dirty tree, and never commit local debugging overrides (hardcoded AWS profile/region in a
client, widened Etsy sync windows). — Both have existed as uncommitted edits; the profile override
would break the Lambda, which has no such profile.

LOCAL: GitHub is the source of truth. GitLab is a read-only mirror, synced by the operator's mirror
tooling. `origin` fetches from GitHub and pushes to both. GitHub merges don't reach GitLab on their own:
after a PR merges, run `git pull && git push origin main`. Push feature branches to the GitHub URL
directly so they don't land on the mirror.

LOCAL: The repo is public. Committed files carry no vulnerability/alert specifics, account
identifiers, email addresses, AWS profile names, or secret values. — Alert details belong in the
GitHub security tab, not in history.

LOCAL: There is no automated test suite. Verify changes with the offline procedure in
[context.md](context.md#verifying-a-change); an end-to-end sync can only be confirmed by the operator
against the live shops, so record it as needs-verification in the session log.
