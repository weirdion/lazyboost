# Context

## What it is

LazyBoost syncs Etsy orders into Shopify, matching products by SKU, so a sale on Etsy is reflected in
Shopify inventory and customer records. It runs unattended as an AWS Lambda on a schedule. The repo
also holds a CLI (`lazyboost`) for local runs, a clipboard helper, and a review-sync path (Etsy →
Judge.me) that is currently disabled.

It is in KTLO mode: it keeps working and stays patched, and nothing new is built here. New capability
goes to the sibling `lazyboost-app` repo, which will eventually replace it (see decisions.md).

## Architecture

Three CDK stacks (TypeScript, `infra/`), entrypoint `infra/bin/lazyboost.ts`:

| Stack | What it holds |
|---|---|
| `LazyboostBaseStack` | The Secrets Manager secret `LAZYBOOST_CREDS` (retained on delete): Etsy and Shopify credentials and the Etsy OAuth tokens. |
| `LazyboostEtsyOauthStack` | Two Node 22 Lambdas (`infra/resources/lambdas/etsy-auth-init`, `etsy-auth-redirect`) and an API Gateway `/api/redirect` route for the Etsy OAuth handshake. They write tokens to the secret. |
| `LazyboostLambdaStack` | The Python 3.12 arm64 sync Lambda (`lazyboost.index.handler`, code from `src/`), its dependency layer (`layer.zip`), an SNS error topic with an email subscription, and an EventBridge rule that fires `{"task": "sync"}` every 17 minutes. |

Sync flow: `index.handler` → `OrderHandler` → `EtsyClient` (orders created within the last
`SYNC_INTERVAL_ORDERS_MIN`, default 20 minutes; this overlaps the 17-minute schedule so no order
falls between runs) → `ShopifyClient`: find or create the customer, skip orders that already exist
(`does_order_exist` on the Etsy receipt id, which makes the overlap safe), and create the order with
line items resolved by SKU. Any exception
is published to the SNS topic and then re-raised.

Python code: `src/lazyboost/` — `clients/` (Etsy, Shopify, Secrets Manager, Judge.me, Stamped.io),
`handlers/` (orders, reviews, listings), `models/`, `utilities/`. `app/` is not part of the build.

## Build and deploy

- Python dependencies: Poetry (`pyproject.toml`, `poetry.lock`). Only the `main` group ships; the
  layer is built by `scripts/build-layer.sh` (`poetry export --only main`, then `pip install` inside
  the `public.ecr.aws/lambda/python:3.12-arm64` image). Dev tools (black, isort, pytest, safety,
  pre-commit) never reach the Lambda.
- CDK: root `package.json`. The OAuth Lambdas are deployed as plain directories; CI does not run
  `npm install` in them, so in production they use the AWS SDK v3 bundled with the Node runtime.
- CI (`.github/workflows/`): `preview.yml` builds the layer and runs `cdk diff` on PRs;
  `deploy.yml` builds and runs `cdk deploy --all` on every push to `main`; `update.yml` opens a
  weekly lockfile-refresh PR from the `workflow-dependency-update` branch.
- Runtime configuration: see `.env.sample`. Deploying needs `LAZYBOOST_ERROR_EMAIL` and AWS
  credentials (CI gets them through an OIDC role).

## Verifying a change

No automated tests exist (see backlog). Offline checks that have caught real breakage:

1. `poetry run black --check ./src && poetry run isort --check-only ./src`
2. Smoke import: import every `lazyboost.*` module and call `index.handler` with invalid events,
   expecting `ValueError`. This makes no network calls.
3. Build `layer.zip` with `scripts/build-layer.sh`, then repeat step 2 inside the Lambda image with the
   unzipped layer mounted at `/opt` and `src/` at `/var/task`. This tests what production loads.
4. `npx tsc --noEmit` and `LAZYBOOST_ERROR_EMAIL=x@example.invalid npx cdk synth --all`. For
   dependency-only changes, compare the templates against the previous lockfile with 64-character
   hex asset hashes masked; resources should be identical.
5. Live: only the operator can confirm a real sync (see the session log for the steps).
