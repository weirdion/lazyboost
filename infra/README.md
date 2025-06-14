# Lazyboost - Infra
---

## Etsy OAuth Stack

This stack provisions AWS Secrets Manager entries per tenant for securely storing Etsy OAuth credentials using AWS CDK.

### Playbook

#### 1. Register Etsy App

Go to: [Etsy Developer Portal](https://www.etsy.com/developers/register)

Register a new app and note:
- **Client ID**
- **Client Secret**
- **Callback URL** (e.g., `https://yourdomain.com/oauth/etsy/callback`)

> You can change the callback URL later as your app evolves.

#### 2. Create `secrets.json` (ONLY locally - DO NOT COMMIT)

Create a `secrets.json` file in the root of your project with the following structure:

```json
{
  "tenants": {
    "myshop.myshopify.com": {
      "client_id": "your-etsy-client-id",
      "client_secret": "your-etsy-client-secret"
    }
  }
}
```

#### 3. Bootstrap CDK & Deploy

Run the following commands to bootstrap and deploy the CDK stack:

```bash
cdk boostrap
cdk deploy --context tenantSecretsFile=secrets.json
```

#### 4. (Optional) Hydrate Secrets Separately

If you need to hydrate secrets separately instead, you can run:

```bash
python3 scripts/hydrate_etsy_secrets.py --file secrets.json
```
