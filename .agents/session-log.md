# Session log

Newest first. The top entry is the current handoff.

## 2026-10-11 (later) — Deploy verified, cleanup finished

**Done**
- #165 merged by the operator and deployed by "Deploy on merge" (merge commit `8be2db5`). The sync
  Lambda now uses dependency layer v12; both OAuth Lambdas were updated.
- Verified read-only in production: the 10 scheduled runs after the deploy all succeeded with no
  errors, at about 2–3 s and 98–99 MB (unchanged from before). The Etsy token refresh and Secrets
  Manager write succeeded twice. Shopify sessions initialized.
- Dependabot: all runtime alerts are closed. One stayed open because it has no upstream fix and the
  vulnerable code is unreachable; it was dismissed as not used, with the reason. One dev-only alert
  remains open: no upstream fix, pulled in by `safety`, not in the layer.
- Cleanup finished. Merged local branches and the stale `workflow-dependency-update` remote branch
  are deleted. Local `refs/archive/*` is deleted at the operator's request, so the old stashes and
  the `app/` stub are gone. `develop` and `feat/rework-cleanup` are kept until the operator's
  rework discovery spike is done (see backlog).

**Needs verification (operator)**
- Order creation in Shopify hasn't run since the deploy, because every run saw no new Etsy orders.
  When the next Etsy order arrives, confirm it appears in Shopify within one 17-minute cycle and
  that no SNS error email arrives.

**Next**
- Brief step 4: migrate the 14 open issues into the backlog (the close list needs operator approval).
- Brief step 5: sync the GitLab mirror (`repoUpsert`; read the script before running it).
- Optional: drop `safety` (the source of the last dev-only alert) or dismiss that alert.

## 2026-10-11 — Restart: steer adoption, local cleanup, dependency refresh

**Done**
- Adopted agent-steer: `.agents/` (prompt, context, decisions, backlog, this log) plus a `CLAUDE.md` pointer.
- Local cleanup. Stashes, uncommitted debug edits (AWS profile override, 3-day Etsy window), `.idea`
  edits and the untracked `app/` stub were archived to local refs (since deleted, see above).
  `.idea/` is now untracked and ignored. `.env.sample` is committed.
- `main` fast-forwarded to origin. Dependencies refreshed in PR #165 and verified offline
  (context.md, "Verifying a change", steps 1–4). PRs #162–#164 closed as superseded.
- Dependabot classification: most pip alerts are in dev-only packages that never enter the layer
  (confirmed by inspecting the built `layer.zip`).
