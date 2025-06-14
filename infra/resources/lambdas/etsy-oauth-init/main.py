#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2025  Ankit Patterson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import time
import hmac
import hashlib
import boto3
import urllib.parse

HMAC_SECRET = os.environ.get("HMAC_SECRET", "default-dev-secret")

ETSY_SCOPE = [
    'address_r',
    'email_r',
    'listings_d', 'listings_r', 'listings_w',
    'shops_r', 'shops_w',
    'transactions_r', 'transactions_w'
]

def generate_state_token(tenant: str, secret: str) -> str:
    ts = str(int(time.time()))
    payload = f"{tenant}|{ts}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}|{sig}"

def handler(event, context):
    tenant = os.environ["TENANT_DOMAIN"]
    secret_name = os.environ["TENANT_SECRET_NAME"]

    secrets = boto3.client("secretsmanager")
    try:
        raw_secret = secrets.get_secret_value(SecretId=secret_name)
        creds = json.loads(raw_secret["SecretString"])
    except Exception as e:
        return {"statusCode": 500, "body": f"Secret retrieval failed: {str(e)}"}

    state_token = generate_state_token(tenant, HMAC_SECRET)

    redirect_uri = f"https://{event['requestContext']['domainName']}/{tenant.replace('.', '-')}/callback"

    query = urllib.parse.urlencode({
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "client_id": creds["client_id"],
        "scope": " ".join(ETSY_SCOPE),
        "state": state_token
    })

    auth_url = f"https://www.etsy.com/oauth/connect?{query}"

    return {
        "statusCode": 302,
        "headers": {
            "Location": auth_url
        },
        "body": ""
    }
