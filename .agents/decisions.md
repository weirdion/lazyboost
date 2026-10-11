# Decisions

Append-only, newest first. Entries before 2026-10 were reconstructed from git history; only
decisions whose reason is visible there are recorded.

## 2026-10-11 — Python floor is 3.12
`pyproject.toml` requires `>=3.12`. The Lambda and CI both run 3.12, 3.9 is end-of-life, and
current dev tooling (pytest 9, isort 9) dropped 3.9. Raise it together with the Lambda runtime.

## 2026-10-11 — Drop unused build tooling instead of patching it
Removed `@aws-cdk/aws-lambda-python-alpha` (unused since the layer build), jest/ts-jest (no TS
tests), and the aws-sdk v2 / TypeScript dev deps from the plain-JS OAuth Lambdas. Unused
dependencies only add advisories to triage. Re-add a test runner when tests are written.

## 2026-10-11 — Agent knowledge lives in `.agents/`, single context
The repo is small and tightly coupled, so one agent context is enough. `CLAUDE.md` is a thin pointer.
No memory directory until there is a behavior-shaping lesson with no other home.

## 2026-01-01 — Zip Lambda + dependency layer instead of a Docker image Lambda
The sync Lambda deploys `src/` as a zip with `layer.zip` built by `scripts/build-layer.sh`, on
arm64. The layer is built inside the Lambda base image so compiled wheels match the runtime
architecture; several CI fixes that day (architecture mismatch, export plugin, permissions)
traced back to building it any other way.

## 2024-05-05 — CDK split into base / OAuth / sync stacks
The secret lives in its own stack with `RETAIN`, so redeploying or replacing the Lambda or OAuth
stacks can never delete the stored credentials.

## 2024-02-06 — Match Shopify customers by Etsy buyer id, name/address as fallback
Customers are found by an Etsy buyer tag first, then by name and address for legacy customers
created before tagging (issue #60). Name parsing tolerates single names and non-alphabetic
characters (later hotfixes).

## 2024-02-06 — Review sync disabled
The `review_sync` task still exists, but the schedule only triggers `sync` (orders).
